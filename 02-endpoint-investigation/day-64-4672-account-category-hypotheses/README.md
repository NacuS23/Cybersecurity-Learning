# Day 64 — Which Accounts Received Windows Special Privileges?

**Date:** 27 November 2026  
**Training:** ~10–15 minutes | SOC analyst investigation and evidence limits  
**Status:** **Worked lesson and real Python execution complete; new Windows account-category query NOT executed on user's computer.**  
**Evidence:** Two entirely fictional Windows Event 4672 datasets and 12 locally executed Python unit tests. No new real Windows Security log data was obtained today.

## Investigation objective

Day 63 found **12 real Event 4672 records** in a 24-hour query. Nine named privileges appeared in all twelve, while three additional privileges appeared nine times each, making **135 appearances**. But **who actually received those privileges?** That requires the event's account identity or account category, not just aggregated privilege names.

This lab introduces account classification using the `SubjectUserSid` field in Windows Security Event 4672. Microsoft's well-known security IDs include `S-1-5-18` (SYSTEM), `S-1-5-19` (LOCAL SERVICE), and `S-1-5-20` (NETWORK SERVICE). An identifier outside these three is **unclassified**, not automatically malicious. Administrators, service accounts and other identities can legitimately hold powerful rights.

**Evidence boundary:** The previous day's user-executed privilege counts are real. **Today's account-category breakdowns are artificial test hypotheses.** They are *not* a claimed explanation of the user's Day 63 events.

## 1. What the SOC analyst needs to know

| Account category | Well-known SID | Interpretation |
| --- | --- | --- |
| SYSTEM | `S-1-5-18` | Built-in account used by the operating system and privileged services |
| LOCAL SERVICE | `S-1-5-19` | Built-in service identity, typically with fewer local rights |
| NETWORK SERVICE | `S-1-5-20` | Built-in service identity that can use computer credentials for network access |
| OTHER / UNCLASSIFIED | Any other valid SID | Could be a legitimate user, administrator, service identity or an unexpected principal; review context |
| MISSING / INVALID SID | Missing or malformed identifier | Data-quality issue; investigate availability and parsing before drawing conclusions |

**Important distinction:** Event 4672 documents **privileges assigned at logon**, not that the assigned privileges were *used*. A high count of `SeDebugPrivilege` or `SeTcbPrivilege` assignments is not sufficient evidence of compromise.

## 2. A revealing counterexample — same privilege counts, different account owners

I created **two independent fictional datasets**, each containing **12** normalized 4672 events and exactly the same 12 privilege names/frequencies as the user's Day 63 aggregate:

- Nine common privileges each occur **12** times.
- Three extra privileges (`SeAssignPrimaryTokenPrivilege`, `SeAuditPrivilege`, `SeTcbPrivilege`) each occur **9** times.
- Total privilege appearances: `9 × 12 + 3 × 9 = 135`.

But the *account ownership* is completely different.

| Account classification | Scenario A: mostly built-in | Scenario B: many unclassified |
| --- | ---: | ---: |
| SYSTEM | **9** | **3** |
| LOCAL SERVICE | 2 | 0 |
| NETWORK SERVICE | 1 | 0 |
| OTHER / UNCLASSIFIED | **0** | **9** |
| **Total events** | **12** | **12** |
| **Privilege appearances** | **135** | **135** |

**Lesson:** Knowing only the 12 privilege frequencies **cannot reveal which accounts generated them**. Even in Scenario B, an unclassified SID does *not* prove an attacker was present — it simply deserves contextual review.

The two scenarios were intentionally constructed; neither was observed on a real endpoint.

## 3. Actual executed tests

The standard-library Python scripts were executed locally in the assistant's isolated environment:

```bash
python generate_fixtures.py
python -m unittest discover -s tests -v
python classify_4672.py samples/scenario_a.jsonl
python classify_4672.py samples/scenario_b.jsonl
```

**Observed test result:** `Ran 12 tests ... OK` (12 passed, zero failed).

Tests cover correct well-known SID classification, an unclassified SID, missing/invalid SID handling, unchanged privilege frequency distributions across scenarios, distinct category distributions, avoiding SID leakage in printed summaries, and rejecting unexpected fields, invalid event IDs and malformed privilege strings.

- [Python classification and summary tool](classify_4672.py)
- [Reproducible synthetic data generator](generate_fixtures.py)
- [Scenario A sample](samples/scenario_a.jsonl) / [Scenario B sample](samples/scenario_b.jsonl)
- [Executed unit-test evidence](evidence/unit_tests.txt)
- [Scenario A program output](evidence/scenario_a_output.txt) / [Scenario B program output](evidence/scenario_b_output.txt)

Python execution proves the **test tool functions on fictional data**. It does not prove that the PowerShell collector works correctly on the learner's Windows computer.

## 4. Optional real Windows check — privacy-safe and read-only

The [PowerShell helper](check_account_categories.ps1) is designed to query Event 4672 on an **authorised Windows PC**. It classifies account SIDs in memory but prints only:

- Total Event 4672 records returned within the 24-hour lookback.
- Counts in SYSTEM, LOCAL SERVICE, NETWORK SERVICE, and OTHER / UNCLASSIFIED categories.
- Per-category counts of events that list `SeDebugPrivilege` and `SeTcbPrivilege`.

It does **not** output usernames, raw SIDs, Logon IDs, IP addresses or event XML, and it does not change any security settings. It still requires appropriate local read permissions.

To run on your own Windows PC (if desired):

```powershell
.\check_account_categories.ps1 -Hours 24 -MaxEvents 2000
```

If your execution policy blocks scripts, review your Windows PowerShell settings rather than blindly bypassing protections. The query runs with a **new moving 24-hour window**, so its total may differ substantially from the 12 records in Day 63. Do not claim the data covers the same events without comparing a fixed timestamp interval and event IDs privately.

**Status:** This helper is **prepared but unexecuted** on the learner's PC. Real account categories remain **unknown** as of this Day 64 report.

## 5. SOC conclusion

**Observed on the real PC previously:** Event 4672 privilege assignments did occur. Which specific account categories owned the Day 63 events is not known.

**Established today with a worked, executed test:** Two very different account-category distributions can generate the same observed aggregate privilege totals. That demonstrates why privileges should not be classified as suspicious merely from frequency.

**Further checks:** If a real query returns unclassified accounts, review authorised account/service context locally, correlate to Event 4624 using Logon ID, examine privileged service configurations and assess any corroborating anomalies. Do not expose identifiable logs publicly.

**Case disposition:** No confirmed compromise from the evidence presently reviewed. No reason to change security settings based on the synthetic tests.

## 6. Checklist and next task

- [x] Verify well-known SID classification and 4672 field definitions against Microsoft documentation.
- [x] Create two synthetic scenarios with identical privilege totals but contrasting ownership.
- [x] Run 12 Python tests and preserve actual output.
- [x] Write the read-only, aggregate-only Windows PowerShell classification helper.
- [ ] Run the PowerShell query against authorised genuine Windows logs.
- [ ] Review the real account-category counts before making any SOC finding about their origins.

**Day 64 topic covered (64/120 = 53.3%); independent Windows hands-on evidence for this new account-category task remains pending.**

## References

- [Microsoft Learn — Event 4672](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672)
- [Microsoft Learn — Well-known security identifiers](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/understand-security-identifiers)
- [Microsoft Learn — Local accounts](https://learn.microsoft.com/en-us/windows/security/identity-protection/access-control/local-accounts)

[Back to SOC portfolio](../../README.md)