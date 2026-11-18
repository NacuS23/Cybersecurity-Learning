# Day 56 — KQL Time-Window Detection and Sign-in Triage

**Date:** 18 November 2026  
**Evidence type:** Synthetic authentication dataset / reproducible KQL case study  
**Status:** Worked investigation documented; **live KQL execution pending**  
**Environment:** Designed for the free browser-based Azure Data Explorer help cluster

## Investigation objective

Find short bursts of failed sign-ins across multiple accounts, group events by five-minute windows, and decide which source requires escalation of the investigation.

This builds on prior `SigninLogs` exercises by introducing `bin(TimeGenerated, 5m)` and a threshold filter applied **after** aggregation. A reproducible `datatable` is included so the exercise does not require a Microsoft Sentinel subscription or access to personal/company logs.

**Evidence boundary:** I prepared and checked the expected counts from the supplied dataset. I have **not** run the query in a real Kusto engine, connected a Sentinel workspace, or collected any new endpoint evidence for this case.

## 1. Free environment

Microsoft's public Azure Data Explorer help cluster supports browser-based KQL querying without an Azure subscription. A Microsoft or Entra sign-in is required. The help cluster is a KQL practice environment; it is **not** a SIEM collecting my Windows Security logs.

Official starting guide: [Explore sample data in Azure Data Explorer](https://learn.microsoft.com/en-us/azure/data-explorer/web-ui-samples-query).

## 2. Reproducible dataset

The following command creates **12 fictional sign-in events** in memory, filters invalid-credential outcomes, and groups the failures by source address and five-minute windows.

Paste the entire block into a KQL editor:

```kql
let LabSignins = datatable(
    TimeGenerated:datetime,
    UserPrincipalName:string,
    IPAddress:string,
    ResultType:string
)
[
    datetime(2026-11-18T10:00:00Z), "alex@example.com",     "198.51.100.25", "50126",
    datetime(2026-11-18T10:01:00Z), "sam@example.com",      "198.51.100.25", "50126",
    datetime(2026-11-18T10:02:00Z), "maria@example.com",    "198.51.100.25", "50126",
    datetime(2026-11-18T10:03:00Z), "alex@example.com",     "198.51.100.25", "50126",
    datetime(2026-11-18T10:04:00Z), "sam@example.com",      "198.51.100.25", "50126",
    datetime(2026-11-18T10:05:00Z), "sam@example.com",      "198.51.100.25", "0",
    datetime(2026-11-18T10:06:00Z), "maria@example.com",    "198.51.100.25", "50126",
    datetime(2026-11-18T10:07:00Z), "finance@example.com",  "203.0.113.7",   "50126",
    datetime(2026-11-18T10:08:00Z), "finance@example.com",  "203.0.113.7",   "50126",
    datetime(2026-11-18T10:09:00Z), "finance@example.com",  "203.0.113.7",   "0",
    datetime(2026-11-18T10:10:00Z), "external@example.com", "192.0.2.8",     "0",
    datetime(2026-11-18T10:11:00Z), "admin@example.com",    "198.51.100.25", "50126"
];
let FailedByWindow =
    LabSignins
    | where ResultType == "50126"
    | summarize
        FailedAttempts = count(),
        TargetedAccounts = dcount(UserPrincipalName)
        by WindowStart = bin(TimeGenerated, 5m), IPAddress;
FailedByWindow
| order by WindowStart asc, FailedAttempts desc
```

All sample IP addresses are from RFC 5737 documentation ranges. The emails are made-up example accounts.

### Expected results (calculated from the 12 sample records)

| WindowStart (UTC) | IPAddress | FailedAttempts | TargetedAccounts |
| --- | --- | ---: | ---: |
| 2026-11-18 10:00 | `198.51.100.25` | 5 | 3 |
| 2026-11-18 10:05 | `203.0.113.7` | 2 | 1 |
| 2026-11-18 10:05 | `198.51.100.25` | 1 | 1 |
| 2026-11-18 10:10 | `198.51.100.25` | 1 | 1 |

The expected results were checked against the literal data in the table, **not obtained from an executed KQL query**. `dcount()` is an estimate in general; this small dataset has the three unique account names shown in the first five-minute window.

### What the commands mean

- `datatable` creates an inline table so the query can run without imported logs.
- `where ResultType == "50126"` keeps only invalid-username/password outcomes.
- `bin(TimeGenerated, 5m)` places timestamps into five-minute buckets anchored at fixed boundaries.
- `summarize ... by WindowStart, IPAddress` groups the failures by time and source.
- `count()` counts invalid-credential records in each group.
- `dcount(UserPrincipalName)` estimates how many distinct account names each group targeted.
- `order by` displays the earlier windows first.

**Important:** The successful sign-in at 10:05 is intentionally **excluded** from the failed-event summary. Analysts must also inspect successes rather than treating a failure-only table as the whole picture.

## 3. Basic detection threshold

For a simple candidate detection rule, replace the final two lines of the full query with:

```kql
FailedByWindow
| where FailedAttempts >= 5 and TargetedAccounts >= 3
| order by WindowStart asc
```

**Expected match:** One group: `198.51.100.25` during the 10:00–10:04 UTC window, with five failures across three accounts.

These thresholds are **illustrative**, not production-ready. A real detection would need baselining, exclusion decisions, testing on representative events, and false-positive analysis. Running this query against an inline `datatable` does **not** create a Sentinel analytics rule or demonstrate a real alert.

## 4. Follow-up: Examine the source including successful sign-ins

To inspect the suspicious source's full sequence, keep the `let LabSignins = datatable(...)[...];` declaration above, then use:

```kql
LabSignins
| where IPAddress == "198.51.100.25"
| project TimeGenerated, UserPrincipalName, IPAddress, ResultType
| order by TimeGenerated asc
```

**Expected interpretation:**
- Eight events from that source.
- Seven invalid-credential outcomes.
- One success for `sam@example.com` at 10:05, immediately after five failures across three accounts.
- More invalid-credential events at 10:06 and 10:11.

The success requires further investigation, not an automatic assumption of account compromise.

## 5. Simulated SOC ticket

**Title:** Multiple-account authentication failures in a five-minute window with subsequent success  
**Source:** `198.51.100.25` (fictional)  
**Finding:** Five invalid-password results targeting three users between 10:00 and 10:04 UTC; Sam sign-in success at 10:05 UTC  
**Assessment:** Possible password spraying; **unauthorised access not confirmed**  
**Priority:** Prompt review based on asset/account importance and company escalation policy  
**Next steps:** Verify Sam's sign-in, authentication factors, device and network context, user confirmation, and activity after login; search across a broader timeframe and related records  
**Disposition:** Further investigation required

**Limitations:** The 12 records contain no MFA, Conditional Access, device trust, geography, client details, or post-login telemetry. The sign-in sequence alone cannot establish intent or user identity.

## 6. Practical completion checklist

- [x] Create a self-contained fictional sign-in dataset and KQL query.
- [x] Derive expected five-minute failure counts and identify the highest-priority source.
- [x] Draft an illustrative detection threshold and follow-up investigation.
- [ ] Execute the KQL query in the free Azure Data Explorer help cluster.
- [ ] Confirm the returned rows against the expected counts and record any corrections.
- [ ] Build and validate a real detection rule after the planned SIEM lab is operational.

**Current status:** Worked case study complete; live KQL run remains pending. A reproducible query is supplied for later independent verification.

## Official references

- [Azure Data Explorer free public help cluster](https://learn.microsoft.com/en-us/azure/data-explorer/web-ui-samples-query)
- [KQL datatable operator](https://learn.microsoft.com/en-us/azure/data-explorer/kusto/query/datatableoperator)
- [KQL summarize operator](https://learn.microsoft.com/en-us/kusto/query/summarizeoperator)
- [KQL countif aggregation](https://learn.microsoft.com/en-us/kusto/query/countif-aggregation-function)
