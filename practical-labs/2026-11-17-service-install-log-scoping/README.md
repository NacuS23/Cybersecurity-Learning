# Scope a Windows service installation with logs

17 November 2026 · Worked example using fictional logs.

CHG-42 approved installing Inventory Agent on LAB-01 and LAB-02 only, from 14:00 inclusive to 14:30 exclusive.

| Row | Time | Computer | Service | Event |
|---|---|---|---|---|
| A | 13:58 | FIN-04 | Inventory Agent | Installed |
| B | 14:05 | LAB-01 | Inventory Agent | Installed |
| C | 14:06 | LAB-01 | Inventory Agent | Started |
| D | 14:10 | FIN-04 | Inventory Agent | Installed |
| E | 14:12 | LAB-02 | Print Helper | Installed |
| F | 14:18 | LAB-02 | Inventory Agent | Installed |
| G | 14:30 | OPS-03 | Inventory Agent | Installed |

## Filter and findings

1. Time filter keeps B–F. A is before the window; G is exactly at the excluded end.
2. Filtering for Inventory Agent removes E.
3. Filtering for Installed removes C, because a start is a different event from an installation.
4. **B, D and F** remain, covering **three distinct computers**. LAB-01 and LAB-02 match the ticket. FIN-04 is inside the time window but outside the approved computer list.

## SOC handover

The supplied logs show Inventory Agent installation records on three computers from 14:00 inclusive to 14:30 exclusive. CHG-42 does not cover the installation on FIN-04. Check for a separate approved change or deployment record before deciding whether it was unauthorised.

Row A also deserves follow-up: it records the same service on FIN-04 before the window. Compare the two FIN-04 events with deployment logs before deciding whether they represent separate installs. Row G is also outside the search and deserves separate review because OPS-03 is outside the approved computer list.

The search describes the supplied records and time window. It does not establish that every installation across the environment was captured.
