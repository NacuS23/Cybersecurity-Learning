# Day 62 — Correlating Privileged Logons with Successful Sessions

**Date:** 25 November 2026  
**Evidence source:** User-executed PowerShell against a real Windows Security log; only privacy-safe aggregate output shared  
**Status:** **Real-data event correlation performed and documented**. No raw Windows logs or account identifiers uploaded.  
**Learning time:** 10–15 minutes; practical command executed by the learner, interpretation assisted by ChatGPT.

## Question

Does a Windows **4672** event (special privileges assigned to a new logon) correspond to a successful **4624** logon session, and what type of logon is it?

Microsoft confirms that 4672's `SubjectLogonId` can be correlated with 4624's `TargetLogonId` on the same computer. These event IDs describe logon/session information; they do **not**, on their own, prove malicious activity.

## Method

The learner ran a read-only Windows PowerShell query using `Get-WinEvent`, searching Event IDs **4624** and **4672** in the last 24 hours with `-MaxEvents 2000`.

The query parsed named XML event data, joined 4672 and 4624 when they shared:
- The **same computer** (`MachineName`).
- The **same Logon ID** (`SubjectLogonId` for 4672, `TargetLogonId` for 4624).
- A **timestamp difference at most 60 seconds**.

For each matching 4672 event, it returned just the matching 4624 event's `LogonType`, and printed only totals and counts grouped by logon type. Identifiers and event XML were never provided to this repository.

The reproducible [read-only PowerShell helper](correlate_privileged_logons.ps1) follows the same logic. **It was written for this case study but not independently executed by the assistant on a Windows machine.** The user's actual result was from the earlier command used during the live lesson.

## Actual results supplied by learner

```text
4624 events: 85
4672 events: 77
Nearby matches: 77

Name Count
---- -----
5       68
2        3
7        2
11       4
```

| Matched 4624 logon type | Windows meaning | 4672 records matched | Share of matches |
| ---: | --- | ---: | ---: |
| **5** | Service | **68** | **88.3%** |
| **2** | Interactive | **3** | **3.9%** |
| **7** | Unlock | **2** | **2.6%** |
| **11** | CachedInteractive | **4** | **5.2%** |
| **Total** | | **77** | **100%** |

**Finding:** In this bounded 24-hour sample, the query found a nearby successful-logon match for **77 of the 77 4672 records**. The majority (**68/77 = 88.3%**) of those matched events correlate to service-type logons.

### Interpreting 77 nearby matches

**77 matches do not establish 77 distinct privileged logon sessions.** The query counts matching **4672 events**, and more than one event might associate with the same 4624, especially if data contains repetition. The query also chooses the nearest 4624 record within 60 seconds; this was not independently validated against raw event XML.

Similarly, do **not** infer from the 85 vs. 77 totals that *exactly eight* sessions lacked special privileges. Totals are event counts, and one-to-one session uniqueness was not tested.

## SOC analysis

- A predominance of **Service (type 5)** matches is compatible with routine Windows service activity. Accounts used by legitimate system components can receive sensitive privileges.
- **Interactive (type 2), Unlock (type 7)** and **CachedInteractive (type 11)** matches deserve context if there is another reason for concern, but are **not** inherently suspicious.
- Event **4672** records privilege assignment at a new logon; it does not by itself show exploitation, privilege escalation by malware, or remote intrusion.
- Microsoft's documentation describes the types of special privileges that can trigger the event, including sensitive token rights. This investigation did **not** examine the specific `PrivilegeList` values or identify accounts.
- The matching method could miss events outside the selected period or event cap, or events more than 60 seconds apart. Logon IDs should be interpreted in the context of the same computer and approximate session time.
- The source machine's security state is **not established** by this one query.

**Disposition:** **No specific compromise indicator in the aggregate evidence reviewed.** Do not recommend containment or security-setting changes based solely on these counts. Further triage needs account/service context, privilege details, session history and corroborating alerts.

## What was learned

1. The operational difference between Windows **4624** (successful logon) and **4672** (special privileges assigned).
2. How to correlate events using a stable **Logon ID** and the same computer rather than relying only on timestamp proximity.
3. Why a high number of 4672 events can occur during legitimate system operation.
4. How to interpret matching **event counts** conservatively without overstating distinct-session counts.
5. How to share aggregate SOC findings in GitHub without publishing account, device or source-IP details.

## Next investigation

For Day 63, a privacy-safe follow-up could count `PrivilegeList` values from Event 4672 **without exporting usernames, identifiers or raw event XML**, then determine which privilege types and logon contexts might warrant closer inspection. This Day 62 report does not claim that follow-up has been run.

## Official documentation

- [Microsoft — Event 4672: Special privileges assigned to new logon](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4672)
- [Microsoft — Event 4624: An account was successfully logged on](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)

[Back to main SOC portfolio](../../README.md)
