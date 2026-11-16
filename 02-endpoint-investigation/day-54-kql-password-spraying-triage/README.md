# Day 54 — Investigating Password Spraying with KQL

**Focus:** Authentication triage, password spraying versus single-account guessing, KQL aggregation and follow-up queries  
**Evidence type:** Simulated Microsoft Entra sign-in results for SOC practice  
**Status:** Completed learning exercise — no live Microsoft Sentinel workspace or production sign-ins used

## Investigation objective

Identify which source addresses are associated with multiple failed sign-ins, distinguish a possible password-spraying pattern from repeated failures against one account, and check whether a suspicious source has any successful sign-ins.

## 1. KQL: Count failed sign-ins and distinct accounts

The following query searches Microsoft Entra `SigninLogs` for invalid username/password results during the last hour:

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where ResultType == "50126"
| summarize
    FailedAttempts = count(),
    TargetedAccounts = dcount(UserPrincipalName)
    by IPAddress
| order by TargetedAccounts desc
```

- `ResultType == "50126"` filters for a common invalid-username-or-password outcome.
- `count()` counts all matching sign-in records for each IP.
- `dcount(UserPrincipalName)` **estimates** the number of distinct accounts involved, rather than counting the exact number of failures.
- `by IPAddress` groups the resulting statistics by source IP.

### Supplied dataset

*The following are simulated KQL summary results. The IP addresses are reserved documentation examples, not threat indicators.*

| IP address | Failed sign-ins | Distinct accounts (estimated) |
| --- | ---: | ---: |
| `198.51.100.25` | 15 | 10 |
| `203.0.113.70` | 28 | 1 |
| `192.0.2.40` | 3 | 3 |

## 2. Analysis and triage

**Possible password spraying — `198.51.100.25`:** Fifteen failed sign-ins spread across about ten accounts in one hour. This pattern warrants investigating whether a source was trying a small set of passwords across multiple users.

**Possible repeated guessing against one account — `203.0.113.70`:** Twenty-eight failed attempts were associated with a single account. This pattern is more consistent with repeated guessing against that account than with a broad spray, although stale credentials, user mistakes or another benign explanation are still possible.

**Insufficient evidence to classify — `192.0.2.40`:** Only three failures across three accounts. This alone doesn't establish malicious automation.

A summary table shows counts and distinct targets; it does **not** show which passwords were attempted, who controlled the source, whether a successful login occurred, or whether accounts were compromised.

## 3. Follow-up: Search for successes from the suspicious IP

To investigate possible impact, I worked through how to query successful sign-ins from `198.51.100.25` during the same hour:

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where IPAddress == "198.51.100.25"
| where ResultType == "0"
| project TimeGenerated, UserPrincipalName, IPAddress, ResultType
```

Key syntax:
- `==` compares values for equality; a standalone `=` is not the same comparison.
- IP addresses are quoted as strings.
- `ResultType == "0"` selects successful sign-ins.
- Multiple `where` lines further narrow the results: here both IP and result criteria must hold.

**Result interpretation:** If this query returns no rows, the only supported finding is that **no matching successes were returned from available logs for this IP and time window**. It cannot exclude successful access from a different address or outside the interval, gaps in log availability, or other means of compromise.

The query above is a **completed learning exercise**; no actual Sentinel query results were collected.

## 4. Additional evidence and next steps

If the pattern were observed in a real SOC, I would:

1. Check successful sign-ins associated with the same source IP, affected accounts, and relevant broader time ranges.
2. Review the individual sign-in events to identify specific targeted accounts and precise timing.
3. Assess account owner confirmation, device identity, typical locations and source network context.
4. Review MFA and Conditional Access outcomes, as well as account and session activity after any successful sign-in.
5. Apply the organisation's investigation and escalation procedures if access seems unauthorised.

## SOC conclusion — simulated case

**Classification:** Suspicious authentication pattern requiring investigation.  
**Primary candidate for password spraying:** `198.51.100.25`.  
**Separate single-account failure pattern:** `203.0.113.70`.  
**Compromise status:** Not established.  
**Action:** Correlate success and failure events; investigate identity, MFA, device and subsequent activity before recommending containment or closure.

## Learning outcomes

- Group failed sign-ins by source and calculate totals using `summarize`.
- Distinguish `count()` from `dcount(UserPrincipalName)`.
- Recognise that account breadth and failure volume are separate signals.
- Build a KQL filter for successful sign-ins from a particular IP.
- Interpret zero query results without overclaiming a clean outcome.
- Separate simulated sign-in exercises from real endpoint or production SIEM findings.

**Progress after this lesson:** **54 of 120 (45%)** completed; **66** remaining.
