# One event, two copies
Date: 9 November 2026

## Worked example
Fictional log-analysis exercise with a worked solution for study. These records are supplied training data, not observations from my computer.

## Objective
Count distinct sign-in events without counting duplicate deliveries twice.

Each EventKey uniquely identifies an event in this fictional system. Copies keep the same key. A Windows Event ID instead identifies an event type; it is not a unique occurrence identifier.

## Supplied evidence
All rows concern account sam on LAB-PC.

| Row | Event time | Received time | EventKey | Action | Result |
|---|---|---|---|---|---|
| A | 10:00:00 | 10:00:01 | K101 | Sign-in | Failed |
| B | 10:00:00 | 10:00:04 | K101 | Sign-in | Failed |
| C | 10:00:30 | 10:00:31 | K102 | Sign-in | Failed |
| D | 10:01:00 | 10:01:01 | K103 | Sign-in | Failed |
| E | 10:01:00 | 10:01:05 | K103 | Sign-in | Failed |
| F | 10:02:00 | 10:02:01 | K104 | Sign-in | Success |

Event time records when the action happened; received time records when the collector received that copy.

## Solution
- Failed rows: **5** — A, B, C, D and E.
- Repeated keys: **K101** (A/B) and **K103** (D/E).
- Distinct failed events: **3** — K101, K102 and K103.
- Successful sign-in key: **K104**.
- Timeline: Three distinct failed sign-ins occurred at 10:00:00, 10:00:30 and 10:01:00, followed by a successful sign-in at 10:02:00.
- Evidence limit: The records do not establish which human used the account, whether this was password guessing, or what happened after the successful sign-in.

## Knowledge-check answers
1. **Were there five separate failed sign-ins?** No. There were five received failed rows but only three distinct failed events. Two rows were additional copies.
2. **Does a later received time necessarily mean another sign-in?** No. The same event may arrive again after a delivery retry. Here the repeated EventKeys identify copies.
3. **Should different keys with the same account and result automatically be treated as duplicates?** No. In this exercise different keys identify distinct events. Matching account and result alone is insufficient.
4. **Does success establish who physically used the account?** No. It establishes a successful sign-in for the account, not the human's identity.

## SOC takeaway
Duplicate records can inflate counts and alert severity. Check the source's identifier rules before deduplicating; do not collapse separate events simply because they look similar. In a real investigation, request session activity and source-device evidence to investigate the successful sign-in.

[Back to learning journal](../../README.md)
