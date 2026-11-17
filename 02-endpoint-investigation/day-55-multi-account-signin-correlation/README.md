# Day 55 — Multi-Account Sign-in Correlation with KQL

**Focus:** SOC authentication-alert triage, password spraying, conditional counts, post-authentication investigation  
**Evidence type:** Simulated Microsoft Entra `SigninLogs` data  
**Status:** Worked case study complete — independent live SIEM practical not performed  
**Date:** 17 November 2026

## Investigation objective

Investigate multiple failed sign-ins from one source IP across several accounts, check whether subsequent successful authentication occurred, and produce a defensible triage recommendation.

This is an **illustrative investigation** using supplied fictional records. The KQL examples are runnable query templates, but no query was executed against a real Microsoft Sentinel workspace and no company account or endpoint was accessed.

## 1. Simulated authentication records

The following sample data covers a short period on 17 November 2026. These IPs are RFC 5737 documentation addresses, not real indicators of compromise.

| Time (UTC) | User | Source IP | Sign-in result |
| --- | --- | --- | --- |
| 09:00 | `alex@example.com` | `198.51.100.25` | Invalid credentials (50126) |
| 09:01 | `sam@example.com` | `198.51.100.25` | Invalid credentials (50126) |
| 09:02 | `maria@example.com` | `198.51.100.25` | Invalid credentials (50126) |
| 09:03 | `alex@example.com` | `198.51.100.25` | Invalid credentials (50126) |
| 09:04 | `sam@example.com` | `198.51.100.25` | Invalid credentials (50126) |
| 09:05 | `maria@example.com` | `198.51.100.25` | Invalid credentials (50126) |
| 09:06 | `sam@example.com` | `198.51.100.25` | Success (0) |
| 09:07 | `alex@example.com` | `203.0.113.20` | Success (0) |
| 09:08 | `maria@example.com` | `192.0.2.55` | Success (0) |
| 09:09 | `support@example.com` | `203.0.113.70` | Invalid credentials (50126) |
| 09:10 | `support@example.com` | `203.0.113.70` | Invalid credentials (50126) |
| 09:11 | `support@example.com` | `203.0.113.70` | Invalid credentials (50126) |

**Observation:** `198.51.100.25` generated six failed sign-ins affecting three different accounts, followed by a successful sign-in for `sam@example.com` from that same source. The records do not show whether the success was authorised or whether MFA was satisfied.

## 2. Query concept: count failures and successes together

This is a production-style KQL example for a workspace that contains a `SigninLogs` table:

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| summarize
    Failures = countif(ResultType == "50126"),
    Successes = countif(ResultType == "0"),
    TargetedAccounts = dcount(UserPrincipalName)
    by IPAddress
| order by Failures desc
```

**Explanation:**

- `countif(ResultType == "50126")` counts records with the invalid-credentials outcome.
- `countif(ResultType == "0")` counts successful sign-in records.
- `dcount(UserPrincipalName)` estimates the number of different accounts represented.
- `summarize ... by IPAddress` groups those measurements by IP address.
- `order by Failures desc` orders IPs by invalid-credential events.

This counts specified outcomes only. Other result codes are excluded from the `Failures` value. The user/account count can include users with successes as well as failures in a group, so an analyst should review the underlying events before calling it a distinct failed-target count.

## 3. Reproducible sample-data KQL

To practise without a live SIEM, the following KQL defines the complete simulated dataset directly using `datatable`. It uses fixed historical times, so it works without an `ago()` condition.

```kql
let SampleSignins = datatable(
    TimeGenerated:datetime,
    UserPrincipalName:string,
    IPAddress:string,
    ResultType:string
)
[
    datetime(2026-11-17T09:00:00Z), "alex@example.com",    "198.51.100.25", "50126",
    datetime(2026-11-17T09:01:00Z), "sam@example.com",     "198.51.100.25", "50126",
    datetime(2026-11-17T09:02:00Z), "maria@example.com",   "198.51.100.25", "50126",
    datetime(2026-11-17T09:03:00Z), "alex@example.com",    "198.51.100.25", "50126",
    datetime(2026-11-17T09:04:00Z), "sam@example.com",     "198.51.100.25", "50126",
    datetime(2026-11-17T09:05:00Z), "maria@example.com",   "198.51.100.25", "50126",
    datetime(2026-11-17T09:06:00Z), "sam@example.com",     "198.51.100.25", "0",
    datetime(2026-11-17T09:07:00Z), "alex@example.com",    "203.0.113.20",  "0",
    datetime(2026-11-17T09:08:00Z), "maria@example.com",   "192.0.2.55",    "0",
    datetime(2026-11-17T09:09:00Z), "support@example.com", "203.0.113.70",  "50126",
    datetime(2026-11-17T09:10:00Z), "support@example.com", "203.0.113.70",  "50126",
    datetime(2026-11-17T09:11:00Z), "support@example.com", "203.0.113.70",  "50126"
];
SampleSignins
| summarize
    InvalidCredentialEvents = countif(ResultType == "50126"),
    SuccessEvents = countif(ResultType == "0"),
    UniqueAccounts = dcount(UserPrincipalName),
    AccountNames = make_set(UserPrincipalName)
    by IPAddress
| order by InvalidCredentialEvents desc, SuccessEvents desc
```

### Expected result from the supplied sample

| IPAddress | InvalidCredentialEvents | SuccessEvents | UniqueAccounts |
| --- | ---: | ---: | ---: |
| `198.51.100.25` | 6 | 1 | 3 |
| `203.0.113.70` | 3 | 0 | 1 |
| `203.0.113.20` | 0 | 1 | 1 |
| `192.0.2.55` | 0 | 1 | 1 |

*These figures are manually derived from the 12 fictional records, not output from a live query. The order of rows tied on both sort fields is not guaranteed.*

A follow-up query in a real Sentinel workspace should inspect the detailed sign-ins, rather than relying only on the summary:

```kql
SigninLogs
| where TimeGenerated > ago(1h)
| where IPAddress == "198.51.100.25"
| project TimeGenerated, UserPrincipalName, IPAddress,
          ResultType, ResultDescription, AppDisplayName,
          ConditionalAccessStatus, DeviceDetail
| order by TimeGenerated asc
```

This query keeps **all results**, including success, so the sequence of failures followed by success remains visible.

## 4. SOC assessment

### Priority 1: `198.51.100.25`

- Repeated failures across several accounts in minutes are consistent with a **possible password-spraying** pattern.
- `sam@example.com` then has a successful sign-in from the same sample source.
- The successful sign-in deserves prompt verification, but does not itself establish malicious control or a successful password-spraying attack.
- Need to verify authentication factors, Conditional Access outcome, source/device familiarity, account owner confirmation, and activity after the sign-in.

### Priority 2: `203.0.113.70`

- Three failures affect only `support@example.com`.
- This could represent repeated guessing against one account or a benign issue such as stale credentials.
- There is no success from this IP in the supplied 12-event dataset.

### Other sign-ins

- The single successful sign-ins for Alex and Maria originate from different documentation IPs.
- The sample does not contain enough context to label those successes suspicious or benign.

## 5. Simulated SOC ticket

**Title:** Multiple failed sign-ins across accounts followed by successful authentication  
**Scope:** Training-only sign-in data, 17 November 2026  
**Indicators:** Six 50126 events affecting three users from one source; a later 0 result for Sam from the same IP  
**Assessment:** Possible password spraying; successful sign-in requires investigation  
**Compromise:** Not confirmed  
**Action:** Examine authentication/MFA details, known device/source history, user confirmation, recent account activity and relevant related alerts  
**Escalation:** Apply incident response policy if corroborating evidence suggests unauthorised access  
**Disposition:** Further triage needed; do not close as safe or confirmed malicious on this dataset alone

## Learning summary

This case reinforces the difference between counting login failures and identifying distinct affected accounts. It introduces `countif()` for counting specific outcomes, `make_set()` for listing associated accounts, and a basic failure-then-success correlation workflow.

**Evidence boundary:** The case is fully worked and documented but no actual query was run in Microsoft Sentinel. A future independent lab should execute the sample query in an available KQL environment and build toward a genuine log-ingesting SIEM and original detection rule.

## References

- [Microsoft Learn — SigninLogs schema](https://learn.microsoft.com/en-us/azure/azure-monitor/reference/tables/signinlogs)
- [Microsoft Learn — summarize operator](https://learn.microsoft.com/en-us/kusto/query/summarizeoperator)
- [Microsoft Learn — countif() function](https://learn.microsoft.com/en-us/kusto/query/countif-aggregation-function)
- [Microsoft Learn — make_set() function](https://learn.microsoft.com/en-us/kusto/query/make-set-aggregation-function)
