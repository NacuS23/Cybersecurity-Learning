# Day 48 - Windows Authentication Log Investigation

**Date:** 2 November 2026  
**Focus:** Security Event IDs 4624, 4625, and 4740; logon types; identifying potentially suspicious access

## Objective

Investigate Windows Security log authentication records using PowerShell. Distinguish failed logons, successful service logons, interactive sessions, cached interactive logons, and workstation unlock events. Assess authentication activity without interpreting ordinary Windows events as an attack.

This report documents **real read-only investigation** on my Windows endpoint. Account identifiers are redacted for privacy.

## 1. Search for failed logon attempts (Event 4625)

Windows **Event 4625** records a failed logon attempt when the relevant auditing is available.

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4625
    StartTime = (Get-Date).AddDays(-7)
} -MaxEvents 10 |
Select-Object TimeCreated, Id, LevelDisplayName |
Format-Table -AutoSize
```

**Actual result:**

```text
Get-WinEvent : No events were found that match the specified selection criteria.
FullyQualifiedErrorId : NoMatchingEventsFound,Microsoft.PowerShell.Commands.GetWinEventCommand
```

No matching 4625 records were returned for the seven-day search window. That does **not** establish that nobody ever entered a wrong password: logging configuration, log retention, and what events the machine records all matter.

Other authentication events discussed:

- **4624** — successful account logon
- **4625** — failed account logon
- **4740** — account locked out

## 2. Inspect recent successful logons (Event 4624)

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4624
} -MaxEvents 10 |
Select-Object TimeCreated,
    @{Name='LogonType';Expression={$_.Properties[8].Value}},
    @{Name='SourceIP';Expression={$_.Properties[18].Value}} |
Format-Table -AutoSize
```

**Actual findings:** All ten most recent events were **Logon Type 5**, and the source-IP column displayed `-`. The events were recorded on **2 November 2026 between 15:02:08 and 15:13:38**.

| Logon type | Meaning |
| --- | --- |
| **2** | Interactive (local sign-in) |
| **3** | Network (e.g. access to a shared resource) |
| **5** | Service logon |
| **7** | Workstation unlock |
| **10** | RemoteInteractive, commonly Remote Desktop |
| **11** | CachedInteractive, logon with cached credentials |

Type 5 events are consistent with background Windows services signing in; they are not, by themselves, evidence of someone remotely accessing the computer. Source-IP values may not be populated for local or service logons.

## 3. Summarise successful logon types

I grouped the 200 most recent Event 4624 records by logon type:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4624
} -MaxEvents 200 |
Group-Object { $_.Properties[8].Value } |
Select-Object Name, Count |
Format-Table -AutoSize
```

**Actual results:**

```text
Name Count
---- -----
5      162
7       10
11      18
2       10
```

| Logon type | Event count | Share of 200 |
| --- | ---: | ---: |
| 5 — Service | 162 | 81% |
| 7 — Unlock | 10 | 5% |
| 11 — Cached interactive | 18 | 9% |
| 2 — Interactive | 10 | 5% |
| **Total** | **200** | **100%** |

**No Type 3 or Type 10 records** were present among these specific 200 most recent events. That does not prove older network or Remote Desktop logons never happened.

Event counts do not equal counts of distinct people: one user, application, or service may generate multiple events.

## 4. Examine interactive logon account information

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4624
} -MaxEvents 200 |
Where-Object { $_.Properties[8].Value -in 2,7,11 } |
Select-Object -First 10 TimeCreated,
    @{Name='LogonType';Expression={$_.Properties[8].Value}},
    @{Name='Account';Expression={$_.Properties[5].Value}} |
Format-Table -AutoSize
```

**Observed excerpts (personal account redacted):**

```text
TimeCreated         LogonType Account
02/11/2026 14:56:11         7 <REDACTED_ACCOUNT>
02/11/2026 14:56:11         7 <REDACTED_ACCOUNT>
02/11/2026 14:56:11        11 <REDACTED_ACCOUNT>
02/11/2026 14:56:11        11 <REDACTED_ACCOUNT>
02/11/2026 14:56:03        11 <REDACTED_ACCOUNT>
02/11/2026 14:56:03        11 <REDACTED_ACCOUNT>
01/11/2026 20:35:24         2 DWM-14
01/11/2026 20:35:24         2 DWM-14
01/11/2026 20:35:23         2 UMFD-14
01/11/2026 19:48:44         7 <REDACTED_ACCOUNT>
```

The personal-account events are consistent with normal unlock and cached interactive authentication. `DWM-14` and `UMFD-14` are Windows desktop-related accounts, not evidence of unknown human users. Several records at the same moment do not automatically represent several people.

## SOC investigation summary

**Title:** Review of Windows successful and failed logon events  
**Source:** Windows Security event log  
**Assessment:** Low concern from the observed sample; no unauthorised login established.

### Evidence

1. The seven-day query for Event 4625 failed logons returned **no matching events**.
2. The ten most recent successful 4624 events all had **Logon Type 5** and no populated source IP in the extracted field.
3. Among the 200 most recent 4624 events, **162 were Type 5**, **18 Type 11**, **10 Type 7**, and **10 Type 2**.
4. The inspected interactive and unlock records involved a redacted local user's account and Windows desktop-related accounts.
5. No Type 3 or Type 10 logons were identified **within the 200-event sample**.

### Analyst interpretation

The records reviewed are consistent with typical Windows service activity, user sign-in, and unlocking the workstation. No suspicious authentication pattern was established from the available results. The sampled data and missing failed-login events do not rule out earlier or unlogged activity.

### When escalation could be appropriate

A hypothetical sequence of **15 failed attempts followed by a successful login** would warrant checking the account, source, logon type, timestamps, and relevant endpoint activity. A successful Type 10 (Remote Desktop) logon outside expected hours deserves context, but is not automatically an intrusion. Multiple Type 3 events represent **events**, not necessarily different remote people.

### Next checks if suspicious authentication appears

- Correlate 4625 failures with 4624 successes for the **same account and source**.
- Investigate Logon Type, Source Network Address, Workstation Name, and available logon identifiers.
- Review Event **4740** account lockouts and any relevant administrative activity.
- Distinguish documented user/admin behaviour from unauthorised access before assigning severity.

**Disposition:** No immediate escalation on the observed evidence.

## What I learned

- PowerShell `Get-WinEvent` retrieves Security logs and targeted event IDs.
- `Group-Object` provides a quick distribution of logon types and event counts.
- Logon Type **5** represents service logons; **7** is unlock; **11** is cached interactive; **2** is an interactive sign-in.
- Logon types **3** and **10** are useful for investigating network and RDP access, but neither automatically proves malicious activity.
- **Number of logon events ≠ number of people.**
- Always distinguish an **absence of matching records in a specific query** from proof that an event never occurred.
