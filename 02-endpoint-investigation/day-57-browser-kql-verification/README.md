# Day 57 — KQL Query Verification and Failure-to-Success Correlation

**Date:** 19 November 2026  
**Topic:** Validating KQL logic, understanding query scope, and correlating failed sign-in clusters with subsequent successful logins  
**Status:** **Worked example complete; execution on Microsoft's live KQL help cluster still pending**  
**Evidence:** Self-contained synthetic dataset; expected results independently checked against its 12 literal records using a local JavaScript calculation, **not** by running KQL in Azure Data Explorer.

## Goal

Learn to verify that a security query returns what the analyst thinks it returns. This lab reuses Day 56's fictional sign-ins and expands them with a two-stage test:

1. **Sanity check:** confirm all log records are present and the total failures/successes are correct.
2. **Correlation:** detect a source IP with at least five invalid-password events across at least three accounts in a five-minute bucket, then find a successful authentication from that **same IP** within the following ten minutes.

This is an analytical **worked solution**, not independently performed work or evidence of production SOC access.

## Where to run this for free

Open the [Microsoft Azure Data Explorer web UI](https://dataexplorer.azure.com/) and sign in with a Microsoft account. Microsoft's public **help cluster** contains sample databases and permits KQL queries without an Azure subscription. Follow the official [quickstart for running a query in the web UI](https://learn.microsoft.com/en-us/azure/data-explorer/web-query-data).

The snippets here define their own in-memory `datatable`, so they do not depend on actual sign-in tables, personal credentials, trial Sentinel subscriptions, or an imported dataset. They can be pasted into the query editor even though the help cluster does not contain a `SigninLogs` table.

**Important:** The query editor requires a signed-in browser session. The browser-based KQL engine was **not accessed or run** for this report; live execution remains an unchecked task.

## 1. Query A — Check the dataset before investigating

[Open the standalone KQL file](queries/01-baseline-check.kql) and paste it into the KQL editor. It declares the 12 fabricated sign-in events using `datatable`, then runs:

```kql
LabSignins
| summarize
    TotalEvents = count(),
    InvalidCredentials = countif(ResultType == "50126"),
    SuccessfulSignins = countif(ResultType == "0"),
    DifferentAccounts = count_distinct(UserPrincipalName)
```

### Expected result

| TotalEvents | InvalidCredentials | SuccessfulSignins | DifferentAccounts |
| ---: | ---: | ---: | ---: |
| 12 | 9 | 3 | 6 |

**Local verification method:** independently counted the entries from the inline data (12 rows), classified result codes (nine `50126`, three `0`), and counted six unique user names. This is a check of the *expected answer*, not evidence that the KQL executed correctly.

**Learning point:** `count_distinct()` provides an exact distinct count (a preview Kusto aggregation), unlike the approximate `dcount()` used in previous days.

## 2. Query B — Detect a failed-sign-in burst followed by success

[Open the full correlation query](queries/02-failure-success-correlation.kql) and paste the *whole file* into the same editor. It first calculates suspicious failure windows and then performs a `join kind=inner` on the source `IPAddress`:

```kql
let SuspectWindows =
    LabSignins
    | where ResultType == "50126"
    | summarize
        FailedAttempts = count(),
        TargetedAccounts = count_distinct(UserPrincipalName)
      by IPAddress, WindowStart = bin(TimeGenerated, 5m)
    | where FailedAttempts >= 5 and TargetedAccounts >= 3;
let Successes =
    LabSignins
    | where ResultType == "0"
    | project IPAddress, SuccessfulUser = UserPrincipalName, SuccessfulAt = TimeGenerated;
SuspectWindows
| join kind=inner (Successes) on IPAddress
| where SuccessfulAt >= WindowStart + 5m and SuccessfulAt < WindowStart + 15m
| project IPAddress, WindowStart, FailedAttempts, TargetedAccounts, SuccessfulUser, SuccessfulAt
| order by WindowStart asc
```

*(The file also contains the necessary `let LabSignins = datatable(...)` statement; the excerpt above is the query logic after the dataset definition.)*

### Expected matching row

| IPAddress | WindowStart (UTC) | FailedAttempts | TargetedAccounts | SuccessfulUser | SuccessfulAt (UTC) |
| --- | --- | ---: | ---: | --- | --- |
| `198.51.100.25` | 2026-11-18 10:00 | 5 | 3 | `sam@example.com` | 2026-11-18 10:05 |

**Why this matches:** `198.51.100.25` produced five `50126` failures from 10:00–10:04 against Alex, Sam and Maria, then a successful Sam sign-in at 10:05 from the same source. The separate Finance source had two failures followed by success, but did not meet the five-failure / three-account threshold.

**Critical limitation:** This query correlates activity by **IP**, not by proof that the same human controlled the login. A NAT, proxy, or shared corporate egress can make many legitimate users appear to share an IP. The successful login might also be authorised.

## 3. Understanding the KQL

- `let`: names an expression or intermediate query; each statement ends with `;`.
- `datatable`: defines an inline synthetic dataset.
- `summarize`: groups data and computes statistics.
- `countif()`: counts only rows satisfying a condition.
- `count_distinct()`: exact distinct account count; distinguish it from approximate `dcount()`.
- `bin(TimeGenerated, 5m)`: groups timestamps into aligned five-minute windows.
- `join kind=inner ... on IPAddress`: retains matches between suspicious windows and successful sign-ins sharing an IP.
- The later `where` limits the success to 10 minutes **after** the five-minute failure window (`WindowStart + 5m` through just before `WindowStart + 15m`).

The condition uses exact window boundaries. For real attacks, attempts can straddle adjacent buckets, so a production detection may need sliding/overlapping windows and broader validation.

## 4. Simulated SOC assessment

**Finding:** Possible password-spraying pattern at `198.51.100.25` with a subsequent successful login by Sam from the same sample IP.

**Risk:** The post-failure success deserves prompt attention but does not confirm the account was compromised.

**Next checks:** Verify Sam's actual MFA result, device details, source-network context, historical account activity, user confirmation and post-login behaviour. Review other source IPs, result codes and relevant time periods; consider shared address infrastructure and false positives.

**Disposition:** Investigate further; insufficient evidence to mark malicious or safe.

## 5. Evidence and completion checklist

- [x] Confirm Microsoft's public KQL help cluster is available for free query practice (official documentation).
- [x] Build the reproducible KQL dataset and two standalone query files.
- [x] Independently validate the expected arithmetic and the single correlated match against the dataset.
- [x] Document the simulated SOC conclusion and the limitations of source-IP correlation.
- [ ] Execute both snippets in the actual Azure Data Explorer browser UI.
- [ ] Record the actual returned rows or error messages; compare with the expected outputs and amend the query if necessary.
- [ ] Add a redacted screenshot or exported query result from a successful real run.

**Final status:** Day 57 worked lesson prepared. **No live KQL execution claimed**. Future Day 58/59 work should prioritise executing a real query rather than adding only more simulated exercises.

## References

- [Microsoft Learn — Query sample data in Azure Data Explorer web UI](https://learn.microsoft.com/en-us/azure/data-explorer/web-query-data)
- [Microsoft Learn — Public help cluster and samples](https://learn.microsoft.com/en-us/azure/data-explorer/web-ui-samples-query)
- [Microsoft Learn — `count_distinct()` function](https://learn.microsoft.com/en-us/kusto/query/count-distinct-aggregation-function)
- [Microsoft Learn — `join` operator](https://learn.microsoft.com/en-us/kusto/query/join-operator)
- [Microsoft Learn — `bin` function](https://learn.microsoft.com/en-us/kusto/query/bin-function)

[Back to main portfolio](../../README.md)
