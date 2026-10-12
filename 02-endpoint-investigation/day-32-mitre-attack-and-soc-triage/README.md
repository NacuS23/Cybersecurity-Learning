# Day 32 - MITRE ATT&CK and SOC triage

Today I started connecting the technical things I've investigated to attacker goals using MITRE ATT&CK. The main lesson was understanding the difference between **execution**, **persistence**, and **privilege escalation**.

## MITRE ATT&CK basics

- A **tactic** is what an attacker wants to achieve.
- A **technique** is how they try to do it.
- Seeing a technique or a Windows feature doesn't automatically prove malicious activity.

Techniques covered today:

| Technique | Example | Tactic |
| --- | --- | --- |
| T1059.001 - PowerShell | Executing commands through PowerShell | Execution |
| T1053.005 - Scheduled Task | Setting a task to run at logon | Persistence (also used for execution) |
| T1543.003 - Windows Service | Creating a service that runs automatically | Persistence (also potentially privilege escalation) |

## Real PowerShell practical: task security context

I checked the security principal of the MSI updater scheduled task from Day 31:

```powershell
(Get-ScheduledTask -TaskName "OneDC_Updater").Principal |
Select-Object UserId,GroupId,LogonType,RunLevel |
Format-List
```

Result:

```
UserId    :
GroupId   : Users
LogonType : Group
RunLevel  : Highest
```

What this told me:

- `GroupId: Users` means the task uses a group-based principal for the Users group.
- `LogonType: Group` means a group-based logon configuration.
- `RunLevel: Highest` requests the highest available privileges for the configured security context.
- **Highest does not automatically mean Administrator or SYSTEM.** A task doesn't gain new permissions just by setting this flag.

## Persistence vs privilege escalation

- **Persistence** means keeping access or restarting activity later, such as using a scheduled task at logon.
- **Privilege escalation** means gaining higher permissions than before, such as a regular user gaining SYSTEM privileges.
- An attacker can establish persistence without gaining higher privileges.

## Simulated SOC investigation

This was a **fictional training scenario**, not an incident observed on my computer.

**Device:** PC-ACCOUNTING-04

Timeline:

```
10:05 - Event 4624
Administrator RDP login from unfamiliar source IP

10:07 - Event 4688
cmd.exe launches powershell.exe -EncodedCommand ...

10:09 - Scheduled task registered
Name: WindowsHealthCheck
Action: C:\Users\Public\healthcheck.exe
Trigger: AtLogOn
GroupId: Users
RunLevel: Highest
Signature: NotSigned
```

Possible ATT&CK mapping:
- Encoded PowerShell: **T1059.001 (PowerShell / Execution)**
- Logon-triggered scheduled task: **T1053.005 (Scheduled Task / Persistence)**

The close timing suggests a possible attack chain, but doesn't prove that the PowerShell command created the task or that privileges were escalated.

## SOC ticket

**Alert:** Suspicious RDP login, PowerShell execution and scheduled-task registration (simulated).

**Priority:** High.

**Evidence:**
- Successful remote interactive Administrator login from an unfamiliar IP.
- PowerShell launched using an encoded command.
- Unsigned executable in `C:\Users\Public\` configured to run at logon.
- Events occurred within a four-minute window.

**Assessment:** Possible account compromise, command execution and persistence. Privilege escalation has **not** been established.

**Next steps:**
- Examine/decode the PowerShell command safely without executing it.
- Check RDP source IP, account activity and whether the login was authorised.
- Inspect the scheduled-task executable, its hash, signature, and behaviour.
- Correlate further process and task-registration events.

**Decision:** Escalate promptly and follow the incident-response process, including containment if warranted.

## What I want to remember

- Being an Administrator is already powerful; lack of SYSTEM access does not make an incident low priority.
- Encoded PowerShell commands deserve context, not automatic condemnation.
- A logon task can create persistence without privilege escalation.
- GroupId and RunLevel show configured context, not proof of a successful privilege escalation.
- MITRE ATT&CK helps describe observed behaviours and hypotheses, not declare malware confirmed.
- In a SOC ticket, separate **observed evidence**, **hypothesis**, **priority**, and **next steps**.
