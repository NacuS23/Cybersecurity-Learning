# Test a simple detection rule

**23 November 2026 · Fictional worked example**

This is a worked solution based on supplied training records. No learner execution, production incident, or live SIEM testing is claimed.

## Rule under test

At 10:05, raise one alert per account with **at least three failed sign-ins** whose event times are **10:00 inclusive to 10:05 exclusive**.

For the baseline calculation, all supplied records are stipulated to be available before evaluation. Availability does not override the event-time filter: the record at exactly 10:05 is excluded.

## Full supplied evidence and filtering

| Row | Event time | Account | Result | Counted? | Reason |
|---|---|---|---|---|---|
| A | 09:59 | alex | Failed | No | Before the window |
| B | 10:00 | alex | Failed | Yes | Inclusive start and failure |
| C | 10:01 | backup-service | Failed | Yes | Within window and failure |
| D | 10:02 | alex | Failed | Yes | Within window and failure |
| E | 10:03 | backup-service | Failed | Yes | Within window and failure |
| F | 10:04 | alex | Success | No | Not a failure |
| G | 10:04 | backup-service | Failed | Yes | Within window and failure |
| H | 10:05 | alex | Failed | No | Exactly at the excluded end |

Matching rows: **B, C, D, E and G**.

## Counts and expected alert

| Account | Matching failure rows | Failure count | Meets threshold? |
|---|---|---:|---|
| alex | B, D | 2 | No |
| backup-service | C, E, G | 3 | Yes |

**Expected result: one alert, for backup-service.**

“At least three” includes exactly three. Alex's success does not subtract or erase earlier failures; it is simply excluded from this failure-count rule. No failure-reset condition is defined.

## Investigation answers

**Possible explanation:** The backup-service password changed at 09:55. An application may still be using a stale stored credential. Its configuration has not been checked, so this is an unconfirmed hypothesis.

**Next evidence check:** With the service owner, review application authentication logs, configuration-change history, credential-update status and the source of the attempts. Look for retries from the expected application after the password change and whether its credential configuration was updated. Do not retrieve, display or publish passwords.

**Does a triggered alert prove an attack?** No. It establishes that the defined pattern matched the supplied records. Operational errors, legitimate mistakes and malicious attempts need to be distinguished using additional evidence. A password change alone does not confirm the stale-credential explanation.

## Late-arrival counterfactual

If G arrives at **10:06**, it is unavailable to the 10:05 evaluation despite its event time of 10:04.

| Account | Available matching failure rows at 10:05 | Count | Alert? |
|---|---|---:|---|
| alex | B, D | 2 | No |
| backup-service | C, E | 2 | No |

**No account reaches the threshold in that evaluation.** Later detection is not guaranteed. It depends on whether a later run or rerun includes the earlier event-time window and processes late-arriving records. Scheduling, lookback and late-event handling were not supplied.

## SOC handover

The baseline rule matches three backup-service failures within the stated five-minute window and produces one expected alert. Alex has two matching failures and does not trigger. A recent service-account password change provides a possible operational explanation, but application configuration and attempt sources still need verification. Delayed arrival of the third failure would prevent this particular 10:05 evaluation from reaching the threshold.

## Evidence limits and verification

The counts were derived directly from the supplied rows and rule conditions; this was not executed in a live SIEM. The exercise does not establish the source, human actor or cause of the failures, complete environmental log coverage, or a real incident. A non-triggering account is not automatically safe: it only failed to meet this rule's threshold for this window.
