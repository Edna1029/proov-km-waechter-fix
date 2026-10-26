# What I checked, and what the agent got wrong

## What the agent got wrong
The first test run showed three failures: wear was rounded down to zero, a missing
service reading was treated as zero, and the report therefore counted the nearly
due car incorrectly. I checked the calculations and confirmed the service interval
and warning threshold should stay at 15,000 km and 80%. I also checked the mileage
conversion in the helper: its old factor multiplied kilometers by 1.609, which is
the wrong direction for converting kilometers to miles.

## What I checked before I accepted its work
I ran the tests and the repository's verify.py acceptance check. The check confirms
that 14,900 km reports about 99.3% wear, that this car is flagged, and that a car
with no last-service reading is not flagged or rejected by the report. It also
checks that both the Python constants and settings.cfg still say 15,000 and 80.
The test suite passes, and verify.py reports that these checks pass.

## What the data actually said
I compared the 26 cars that later broke down with the 94 that did not. Kilometers
since service showed the clearest difference; average daily kilometers and load
factor also separated the groups. Total odometer and vehicle age were almost the
same across both groups, so I did not use them in the relative risk score. The
score ranks cars for review; it is not a promise or probability that a car will
break down.
