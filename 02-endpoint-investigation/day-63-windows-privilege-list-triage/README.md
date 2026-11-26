# Day 63 — Windows Event 4672 Privilege-List Triage

**Date:** 26 November 2026  
**Evidence source:** User-executed, read-only PowerShell query on an actual Windows Security event log  
**Status:** **Real endpoint aggregate analysis completed.** Account classification and per-session correlation not yet performed.  
**Privacy:** Only aggregated privilege names and frequencies are recorded. No usernames, account SIDs, logon IDs, computer names, IP addresses, or raw events were committed.

## The question

Which sensitive privileges were assigned to new logon sessions according to Windows Security **Event 4672**? Can the counts alone establish whether a computer was compromised?

This extends [Day 62's real 4624/4672 session correlation](../day-62-privileged-logon-correlation/README.md).

**Microsoft's definition:** Event 4672 records sensitive privileges *assigned to a new logon*. It does not prove that those privileges were used, abused or exploited. Legitimate privileged accounts and Windows services can generate these events.

## 1. How the observation was collected

The learner ran the read-only PowerShell query supplied in the Day 63 lesson:

- `Get-WinEvent` selected Security Event **4672** records within a rolling **24-hour** interval, with `-MaxEvents 2000`.
- `ToXml()` extracted the event XML; the `PrivilegeList` field was selected by its named XML attribute.
- Strings matching `^Se[A-Za-z]+Privilege$` were split on whitespace and grouped by privilege name.
- Only the **event count, privilege names and frequency counts** were shared.

This report documents **user-provided genuine endpoint output**, not a simulated KQL/Windows query or an assistant-executed command on the learner's PC.

## 2. Actual output provided by the learner

```text
4672 events analysed: 12

Name                                      Count
----                                      -----
SeRestorePrivilege                           12
SeDelegateSessionUserImpersonatePrivilege    12
SeDebugPrivilege                             12
SeImpersonatePrivilege                       12
SeSystemEnvironmentPrivilege                 12
SeSecurityPrivilege                          12
SeBackupPrivilege                            12
SeLoadDriverPrivilege                        12
SeTakeOwnershipPrivilege                     12
SeAssignPrimaryTokenPrivilege                 9
SeAuditPrivilege                              9
SeTcbPrivilege                                9
```

### Verified arithmetic from the supplied output

| Measurement | Count |
| --- | ---: |
| Event 4672 records analysed by this query | **12** |
| Different privilege names present | **12** |
| Privilege types seen in all 12 events | **9** |
| Additional privilege types seen in 9 of 12 events | **3** |
| Total privilege appearances (sum of grouped counts) | **135** |

`9 × 12 + 3 × 9 = 135`.

**Important:** These are **135 privilege appearances across 12 events**, **not** 135 separate events, distinct logon sessions, actions, or security incidents.

The query's output proves that the nine ubiquitous privileges were reported in all 12 events; the other three each appeared in nine. It **does not by itself confirm which nine events contain each of those three privileges**, or which accounts owned the sessions.

## 3. What matters for a SOC analyst

| Privilege | Occurrences | Why analysts care |
| --- | ---: | --- |
| `SeDebugPrivilege` | 12 | Can facilitate powerful process inspection/debugging in suitable contexts |
| `SeBackupPrivilege` | 12 | Supports backup access to protected files |
| `SeRestorePrivilege` | 12 | Supports restoring files and security-related operations |
| `SeImpersonatePrivilege` | 12 | Allows impersonation of an authenticated client in applicable contexts |
| `SeSecurityPrivilege` | 12 | Involves security auditing and the Security log |
| `SeTakeOwnershipPrivilege` | 12 | Enables taking ownership of securable objects |
| `SeLoadDriverPrivilege` | 12 | Can allow loading and unloading device drivers |
| `SeSystemEnvironmentPrivilege` | 12 | Can modify system environment settings |
| `SeDelegateSessionUserImpersonatePrivilege` | 12 | Relates to obtaining an impersonation token for another user in the same session |
| `SeAssignPrimaryTokenPrivilege` | 9 | Can replace or assign process-level primary tokens in supported contexts |
| `SeAuditPrivilege` | 9 | Allows generating security audits |
| `SeTcbPrivilege` | 9 | Highly sensitive: acting as part of the operating system |

These permissions warrant **contextual** analysis because they are powerful, but seeing them assigned at logon is normal for many Windows system/service contexts. Event 4672 alone cannot tell whether a privilege was later used.

## 4. Compare with Day 62 accurately

**Day 62**: 77 Event 4672 records in a different 24-hour query and 77 nearby Event 4624 matches.  
**Day 63**: 12 Event 4672 records in today's rolling 24-hour query and their privilege totals.

Do **not** assume 65 privileged logons disappeared or that an attack stopped. The queries were executed at different times, potentially over different rolling windows and different retained records. There is no shared fixed interval or saved event-ID-level comparison to explain the difference.

The previous day's service-logon predominance **does not prove** that today's 12 Event 4672 records were all service logons or came from SYSTEM. Establishing that requires checking the event's account category or correlating the actual logons.

## 5. SOC decision

**Observation:** 12 real Event 4672 records, with a consistent set of nine privilege types in all records and three more types in nine records.

**Assessment:** The distribution is **compatible with ordinary privileged Windows account and service activity**, but **the actor or account type is unknown** from the shared output. The high count of sensitive rights is not, by itself, evidence of compromise.

**Severity/disposition:** **No confirmed attack from the supplied aggregate evidence.** Do not disable services, change audit policy or reset credentials solely on these counts.

**Evidence gaps:** No `SubjectUserSid`, account classification, Event 4624 logon types for this exact sample, host context, or proof of privilege exercise; no other corroborating alerts supplied.

## 6. Recommended private follow-up

A useful next step is to classify the **account categories** that received the privileges (built-in SYSTEM, LOCAL SERVICE, NETWORK SERVICE, or other) without printing usernames or SIDs. The included [privacy-focused read-only PowerShell script](classify_privileged_accounts.ps1) prints **only a category/count table** and does not upload or store event records.

**This follow-up script has been prepared but has NOT been run on the learner's Windows PC.** No result should be claimed until the user executes it and shares the aggregated output.

This script can help establish whether the 12 events are principally system logons. It still won't prove that the event source or any process is safe.

## 7. Lesson completion

- [x] Execute a read-only query of real 4672 events.
- [x] Extract and group the actual `PrivilegeList` values.
- [x] Interpret assignment versus actual privilege use.
- [x] Independently check the arithmetic of the supplied totals.
- [x] Document cautious SOC triage with no raw/private identifiers.
- [ ] Identify built-in versus other account categories for the **same or next** 24-hour window.
- [ ] Correlate selected cases with Event 4624 and supporting context if indicated.
- [ ] Build and validate a rule in a real SIEM when a lab becomes available.

**Result:** Day 63 real-data aggregate investigation documented. The learning-programme topic is complete; advanced session/account attribution remains future work.

## References

- [Microsoft Learn — Event 4672: Special privileges assigned to new logon](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672)
- [Microsoft Learn — Event 4624: An account was successfully logged on](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)
- [Microsoft Learn — Audit Special Logon](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/audit-special-logon)

[Back to the portfolio](../../README.md)
