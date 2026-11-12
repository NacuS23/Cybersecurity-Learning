# Day 51 - Investigating Privileged Windows Logons (Event 4672)

**Dates:** Reference guide 9 November 2026; hands-on verification 12 November 2026  
**Status:** Hands-on lab completed; actual Event 4672 records reviewed  
**Focus:** Event 4672, Event 4624, Logon IDs, and possible privilege escalation

> This report includes a pre-existing worked SOC reference plus **actual Event 4672 endpoint results provided on 12 November 2026**. The fictional scenario is labelled separately; no compromise has been established.

## Objective

Understand what a privileged logon event establishes, correlate it with successful logon data, and distinguish legitimate Windows SYSTEM activity from possible unauthorised elevated access.

## SOC knowledge

| Event ID | Meaning | What it does *not* automatically prove |
| --- | --- | --- |
| **4672** | Special privileges assigned to a new logon session | That an attacker escalated privileges or used them |
| **4624** | Account successfully logged on | That the logon was malicious |
| **4732** | Member added to a security-enabled local group | That the group was Administrators, unless the group is inspected |

A standard Windows **SYSTEM** (`NT AUTHORITY\SYSTEM`) logon can generate Event 4672 because the system account normally holds sensitive privileges. An event for SYSTEM is a starting point for context, not an automatic security incident.

Some privileges visible in 4672 include `SeDebugPrivilege`, `SeBackupPrivilege`, and `SeImpersonatePrivilege`. These identify privileges assigned at logon; the event does **not** establish that someone used those privileges.

**SOC conclusion:** A 4672 event for SYSTEM **does not prove attacker privilege escalation**. Confirm account identity, session context, related events and whether the activity was expected.

## 1. Identify recent privileged logons

Run this **read-only** query in PowerShell:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4672
} -MaxEvents 5 |
Select-Object TimeCreated,
    @{Name='Account';Expression={$_.Properties[1].Value}},
    @{Name='LogonId';Expression={$_.Properties[3].Value}},
    @{Name='Privileges';Expression={$_.Properties[4].Value}} |
Format-Table -AutoSize
```

Relevant Event 4672 fields:

- `Properties[1]`: **SubjectUserName**
- `Properties[3]`: **SubjectLogonId**
- `Properties[4]`: **PrivilegeList**

The above command is the original reference example. A separate live three-event query was later run; its actual results appear in Section 4.

## 2. Correlate Event 4672 with Event 4624

The **Logon ID** is the useful link between the privileged session and its associated successful logon.

In Event **4624**, the relevant **TargetLogonId** is generally `Properties[7]` and **LogonType** is `Properties[8]`. These positional indices apply to the common event schema; verify against the event's actual XML/field names if needed.

The following read-only example finds one recent privileged logon and searches for a matching successful logon within a small time window:

```powershell
$privEvent = Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4672
} -MaxEvents 1

$logonId = [string]$privEvent.Properties[3].Value

Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4624
    StartTime = $privEvent.TimeCreated.AddMinutes(-2)
    EndTime = $privEvent.TimeCreated.AddMinutes(2)
} -ErrorAction SilentlyContinue |
Where-Object { [string]$_.Properties[7].Value -eq $logonId } |
Select-Object TimeCreated,
    @{Name='Account';Expression={$_.Properties[5].Value}},
    @{Name='LogonType';Expression={$_.Properties[8].Value}},
    @{Name='LogonId';Expression={$_.Properties[7].Value}} |
Format-Table -AutoSize
```

If no matches appear, that does **not** establish that a session never existed. Logging, retention, differences between event schemas, and the limited search window can affect results. The `$privEvent` assignment requires at least one 4672 record.

## 3. Interpret the matched session

| Possible finding | Next analytical step |
| --- | --- |
| SYSTEM, expected service/operating-system logon | Check whether it fits normal system activity; don't escalate solely on Event 4672 |
| Expected named administrator account | Verify whether the logon was planned and the source is normal |
| Unfamiliar account with special privileges | Examine the account, logon type, source, processes and related alerts |
| Event 4732 near the same time | Identify **which local group** had a member added; check whether the member was added to Administrators and whether it was authorised |

### Simulated case (NOT observed on the computer)

An alert presents a successful Event 4624 for `helpdesk_temp`, a correlated 4672 with sensitive privileges, and a 4732 showing the account was added to **Administrators**. The changes happened outside the planned IT maintenance window.

**SOC assessment:** Suspicious privileged-access sequence; priority depends on account and asset criticality, access source, authorisation, and any follow-on activity. Do not declare an exploit or compromise without verification.

**Suggested checks:**
1. Confirm that 4672 and 4624 belong to the same session using their Logon IDs and relevant machine/time context.
2. Review 4624 account, logon type and source details; validate expected administrator activity.
3. Read the 4732 **group name, added member and subject account**; determine whether the change was authorised.
4. Check related process creation, PowerShell events, persistence and endpoint alerts if there are signs of suspicious behaviour.
5. Escalate and follow incident response policy when evidence or exposure warrants containment.

**Illustrative decision:** Investigate and verify, rather than treating every 4672 as a privilege-escalation attack.

## 4. Actual Windows Security log results — 12 November 2026

This section documents **real endpoint output** provided after the original reference exercise was prepared.

I ran this read-only PowerShell query for three recent Event 4672 records from the past 24 hours:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4672
    StartTime = (Get-Date).AddDays(-1)
} -MaxEvents 3 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, Message |
Format-List
```

**Observed records:**

| Recorded time | Event ID | Account | Security ID | Logon ID |
| --- | --- | --- | --- | --- |
| 12 Nov 2026 21:27:34 | 4672 | `NT AUTHORITY\SYSTEM` | `S-1-5-18` | `0x3E7` |
| 12 Nov 2026 21:27:34 | 4672 | `NT AUTHORITY\SYSTEM` | `S-1-5-18` | `0x3E7` |
| 12 Nov 2026 21:27:18 | 4672 | `NT AUTHORITY\SYSTEM` | `S-1-5-18` | `0x3E7` |

**Privileges listed** across the results included `SeAssignPrimaryTokenPrivilege`, `SeTcbPrivilege`, `SeSecurityPrivilege`, `SeTakeOwnershipPrivilege`, `SeLoadDriverPrivilege`, `SeBackupPrivilege`, `SeRestorePrivilege`, `SeDebugPrivilege`, `SeSystemEnvironmentPrivilege`, `SeImpersonatePrivilege`, and `SeDelegateSessionUserImpersonatePrivilege`. The two events at 21:27:34 also included `SeAuditPrivilege`. The 21:27:18 event did not list `SeAuditPrivilege`.

**Interpretation:** These are special privileges assigned to the built-in Windows SYSTEM identity. SID `S-1-5-18` and logon ID `0x3E7` are expected identifiers for SYSTEM. Three recorded 4672 events do **not** mean three different people logged in, and event 4672 does **not** prove use of any listed privilege. No unexpected named user account was observed in this three-event sample.

**Scope:** No corresponding Event 4624 correlation query was performed or supplied for this exercise; therefore there is no independently verified matching 4624 event, logon type, or remote source. The three-event sample cannot rule out other privileged logons elsewhere in the Security log.

### Practical SOC decision

**Assessment:** Low concern for the three observed SYSTEM events. No unauthorised privilege escalation was established.

**Learner response:** Correctly identified a SYSTEM 4672 as potentially normal. For the simulated case, prioritised asking what privileges the account received. Full triage should additionally validate the account, matched logon session, source, group membership change, and IT authorisation.

**Disposition:** No immediate escalation justified solely by these three SYSTEM events.

## Assessment and status

- **Actual lab completed:** Three 4672 events from 12 November 2026 were inspected; all showed SYSTEM, SID `S-1-5-18`, and logon ID `0x3E7`.
- **Evidence-based finding:** The reviewed records are consistent with ordinary Windows system activity; privileges being assigned do not prove misuse.
- **Limitations:** Event 4624 correlation was explained but not run in this exercise; no claim about all other logons on the computer.
- **Simulated SOC case:** `helpdesk_temp` / `backup_admin` examples are training scenarios, not actual endpoint findings.
- **Progress:** **51/120 lessons completed (42.5%)**, 69 remaining. Day 51 practical verified.

## References

- [Microsoft Learn — Event 4672: Special privileges assigned to new logon](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4672)
- [Microsoft Learn — Event 4732: Member added to a security-enabled local group](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4732)
