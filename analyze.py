# Breakdown risk is most separated by kilometers since service, with daily use and load also mattering.
# Total odometer and age barely differ between outcomes, so the score uses only those three stronger signals.

"""Compare breakdown history and print the ten highest relative-risk cars."""

from math import sqrt

import pandas as pd

DATA_FILE = "fleet_history.csv"
TARGET = "broke_down"
SEPARATION_CUTOFF = 0.5


def compare_features(df: pd.DataFrame, features: list[str]) -> pd.DataFrame:
    """Compare outcome groups and identify practically separated features."""
    no_breakdown = df.loc[df[TARGET] == 0]
    breakdown = df.loc[df[TARGET] == 1]
    comparisons = []

    for feature in features:
        no_values = no_breakdown[feature]
        yes_values = breakdown[feature]
        pooled_std = sqrt(
            (
                (len(no_values) - 1) * no_values.var()
                + (len(yes_values) - 1) * yes_values.var()
            )
            / (len(no_values) + len(yes_values) - 2)
        )
        effect_size = (
            (yes_values.mean() - no_values.mean()) / pooled_std
            if pooled_std
            else 0.0
        )
        comparisons.append(
            {
                "feature": feature,
                "no_breakdown_mean": no_values.mean(),
                "breakdown_mean": yes_values.mean(),
                "no_breakdown_median": no_values.median(),
                "breakdown_median": yes_values.median(),
                "cohens_d": effect_size,
                "separates": abs(effect_size) >= SEPARATION_CUTOFF,
            }
        )

    return pd.DataFrame(comparisons)


def main() -> None:
    """Print feature comparisons and the top ten relative-risk scores."""
    df = pd.read_csv(DATA_FILE)
    features = [
        column for column in df.columns if column not in ("car_id", TARGET)
    ]
    comparisons = compare_features(df, features)

    print(
        f"Loaded {len(df)} cars: {(df[TARGET] == 1).sum()} breakdowns, "
        f"{(df[TARGET] == 0).sum()} without breakdowns."
    )
    print(
        f"\nFeature comparison (a practical separator has |Cohen's d| "
        f">= {SEPARATION_CUTOFF:.1f}):"
    )
    print(
        comparisons[
            [
                "feature",
                "no_breakdown_mean",
                "breakdown_mean",
                "no_breakdown_median",
                "breakdown_median",
                "cohens_d",
                "separates",
            ]
        ].to_string(index=False, float_format=lambda value: f"{value:.2f}")
    )

    selected = comparisons.loc[comparisons["separates"]]
    if selected.empty:
        raise ValueError("No features meet the practical separation cutoff.")

    weights = selected.set_index("feature")["cohens_d"].abs()
    risk_components = pd.DataFrame(index=df.index)
    for feature, effect_size in selected.set_index("feature")["cohens_d"].items():
        risk_components[feature] = df[feature].rank(
            pct=True,
            ascending=effect_size > 0,
        )
    df["risk_score"] = (
        risk_components.mul(weights, axis="columns").sum(axis="columns")
        / weights.sum()
        * 100
    )

    print("\nTop 10 cars by relative risk score (not a breakdown probability):")
    print(
        df.sort_values(
            ["risk_score", "car_id"],
            ascending=[False, True],
        )
        .head(10)[["car_id", "risk_score"]]
        .to_string(index=False, formatters={"risk_score": "{:.1f}".format})
    )


if __name__ == "__main__":
    main()
