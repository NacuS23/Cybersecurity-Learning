# Day 58 — KQL Detection Unit Tests and False-Positive Controls

**Date:** 21 November 2026  
**Learning time:** ~10–15 minutes  
**Status:** Reproducible worked lab complete; **real KQL engine execution pending**  
**Evidence:** Synthetic 24-event dataset and independent JavaScript calculation of expected outputs. **No Microsoft Sentinel, Azure Data Explorer, or other KQL engine was actually run for this lesson.**

## Why this day matters

Days 53–57 introduced suspicious authentication patterns, KQL grouping and failure-to-success correlation. This lesson adds a key analyst skill: **testing the detection with both positive and negative cases**. A rule that flags everything is not useful, even if it catches the attack-shaped example.

Microsoft documents a [free public Azure Data Explorer help cluster](https://learn.microsoft.com/en-us/azure/data-explorer/web-ui-samples-query), accessed via [dataexplorer.azure.com](https://dataexplorer.azure.com/). It requires Microsoft-account sign-in, not an Azure subscription. This exercise uses only an inline `datatable`; no paid services, imported logs, or cloud resources are necessary.

## 1. Test cases

All IP addresses are RFC 5737 documentation ranges. All identities are fictional.

| Case | Events | Expected result | Why |
| --- | --- | --- | --- |
| A: possible spraying, then success | `198.51.100.25`: five failures across Alex/Sam/Maria in 10:00–10:04; Sam success at 10:05 | **Correlated** | Meets 5 failures, 3 accounts, success in the next 10 minutes |
| B: repeated failures, single account | `203.0.113.80`: five failures against Backup in 10:15–10:19, then success at 10:20 | **Not a candidate** | Only one account; prevents treating every high-volume single-user failure as spraying |
| C: spraying-shaped, but success too late | `192.0.2.70`: five failures across Amy/Ben/Cam in 10:25–10:29; success at 10:41 | **Candidate, not correlated** | Success is outside the 10:30–10:40 follow-up interval |
| D: small failure burst | `203.0.113.7`: two failures against Finance, then success | **Not a candidate** | Below thresholds |

The first twelve records reuse Day 57's training pattern, with additional negative tests. Note that `198.51.100.25` has other failures in later windows, which do not affect its 10:00 cluster.

## 2. Files and expected outputs

### Query 1 — automated self-check

Run [`queries/01-self-check.kql`](queries/01-self-check.kql) as one whole query. It creates the data in memory, calculates candidate windows, correlates successes, and emits `PASS` or `FAIL` by comparing actual KQL aggregates to these expected values:

| Metric | Expected |
| --- | ---: |
| TotalEvents | 24 |
| FailedEvents | 19 |
| SuccessfulEvents | 5 |
| DistinctAccounts | 10 |
| CandidateWindows | 2 |
| CorrelatedSuccesses | 1 |
| TestResult | `PASS` |

These counts were independently computed from the exact 24 rows using a separate JavaScript implementation. **The PASS value is expected, not an observed KQL result.** The KQL execution may reveal a syntax or runtime issue, which should be documented and fixed rather than hidden.

### Query 2 — explain the matches

Run [`queries/02-candidate-details.kql`](queries/02-candidate-details.kql). Expected candidate rows:

| IP | WindowStart (UTC) | Failures | Accounts | TimelySuccesses |
| --- | --- | ---: | ---: | ---: |
| `198.51.100.25` | 10:00 | 5 | 3 | 1 |
| `192.0.2.70` | 10:25 | 5 | 3 | 0 |

The query uses a **left outer join**, then counts only successful sign-ins inside the time boundary. This preserves candidate windows with no timely success, which an inner join would otherwise discard.

## 3. Important query concepts

- `materialize()`: caches the tabular result of a `let` expression within a query; useful here when the same candidate table is reused.
- `toscalar()`: converts a single-cell tabular aggregate to a scalar, allowing multiple independent checks in one result row.
- `iff()`: returns `PASS` only when every expected count matches.
- `join kind=inner`: returns matched source IPs; **not** proof that the same person controlled each event.
- `join kind=leftouter`: retains candidate windows even if no successful sign-in is found.
- `countif()` and `make_set_if()`: count and collect only records satisfying the follow-up condition.

**Window semantics:** `WindowStart + 5m <= SuccessfulAt < WindowStart + 15m`. For a 10:25 window, a 10:41 success is excluded. An event at exactly 10:40 would also be excluded. Sliding windows may be needed for production detections that must catch attacks straddling fixed five-minute bins.

## 4. How to reproduce in 10–15 minutes

1. Open [Azure Data Explorer web UI](https://dataexplorer.azure.com/), sign in, and select the public help cluster and Samples database (or use the sample gallery).
2. Open the first `.kql` file, copy its **entire contents**, paste into a new query tab, and select **Run** (or Shift+Enter).
3. Compare every returned count to the expected table; record the actual result or any error.
4. Open the second `.kql` file, paste and run it. Check that both candidate windows remain visible and only the first has a timely success.
5. Save a redacted screenshot or exported results as genuine execution evidence, if you run the queries. No screenshot is included here because no browser query was executed.

Microsoft's official instructions: [Explore samples](https://learn.microsoft.com/en-us/azure/data-explorer/web-ui-samples-query) and [Query sample data](https://learn.microsoft.com/en-us/azure/data-explorer/web-query-data).

## 5. Simulated SOC finding

**Alert hypothesis:** Potential password spraying from `198.51.100.25` followed by a successful sign-in from the same source.

**Triage priority:** Investigate Sam's successful sign-in, MFA and Conditional Access outcomes, trusted device context, user confirmation, source IP sharing (NAT/proxy), and subsequent account activity.

**False-positive control:** The Backup example demonstrates repeated wrong credentials against one account; it does not meet the multi-account criterion. The late-success example demonstrates why a time-bounded correlation matters.

**Verdict:** Suspicious **synthetic** pattern; **compromise not confirmed**. No live alert or real account access occurred.

## 6. Evidence checklist

- [x] Source dataset and two reusable KQL files committed.
- [x] Independent local calculation of expected totals, candidate groups and correlated successes.
- [x] Positive and negative test cases documented, including a late-success edge case.
- [ ] Run KQL in the actual free public help cluster.
- [ ] Record genuine query output and investigate any mismatch.
- [ ] Progress to a real log-ingesting SIEM and a tested custom detection rule.

**Portfolio disclosure:** This is a completed **worked training case**, not an independently executed KQL investigation. Query execution remains pending. Future practice should prioritise actually running these snippets rather than generating more simulations.

## References

- [Microsoft Learn — Azure Data Explorer sample gallery](https://learn.microsoft.com/en-us/azure/data-explorer/web-ui-samples-query)
- [Microsoft Learn — Query sample data](https://learn.microsoft.com/en-us/azure/data-explorer/web-query-data)
- [Microsoft Learn — KQL `materialize()`](https://learn.microsoft.com/en-us/kusto/query/materialize-function)
- [Microsoft Learn — KQL `toscalar()`](https://learn.microsoft.com/en-us/kusto/query/toscalar-function)
- [Microsoft Learn — KQL join](https://learn.microsoft.com/en-us/kusto/query/join-operator)

[Back to portfolio](../../README.md)
