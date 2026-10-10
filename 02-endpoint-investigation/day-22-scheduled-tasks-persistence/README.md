# Day 22 - Scheduled tasks and persistence

Today I investigated a real Windows scheduled task and learned why scheduled tasks matter for persistence.

## Why scheduled tasks matter

Windows Task Scheduler can run programs or actions at logon, startup, a specific time, or in response to an event. Legitimate software uses this all the time. Attackers can also abuse scheduled tasks to restart something automatically.

A scheduled task existing does not automatically mean malware.

## Finding tasks

I listed enabled tasks with PowerShell:

```powershell
Get-ScheduledTask |
Where-Object {$_.State -ne "Disabled"} |
Select-Object -First 20 TaskName, TaskPath, State
```

I selected the following real task:

```
TaskName: .NET Framework NGEN v4.0.30319
TaskPath: \Microsoft\Windows\.NET Framework\
State: Ready
```

## Checking what it runs

I inspected its action:

```powershell
(Get-ScheduledTask -TaskName ".NET Framework NGEN v4.0.30319").Actions |
Format-List *
```

The action used a **COM handler**, not a direct executable path:

```
ClassId: {84F0FAE1-C27B-4F6F-807B-28CF6F96287D}
Data: /RuntimeWide
Action type: MSFT_TaskComHandlerAction
```

Scheduled tasks can use different kinds of actions. Not all of them launch an .exe directly.

## Checking task history

I checked the task's execution information using its full TaskPath:

```powershell
Get-ScheduledTaskInfo -TaskName ".NET Framework NGEN v4.0.30319" -TaskPath "\Microsoft\Windows\.NET Framework\"
```

Results included:

```
LastRunTime: 03/10/2026 20:05:57
LastTaskResult: 2147943467
NumberOfMissedRuns: 0
```

The non-zero result deserves context if troubleshooting, but a failed task does not automatically mean malware.

## Assessment

The task was in the expected Microsoft Windows .NET Framework task folder and used a COM handler. From the information reviewed, there was no clear evidence of malicious persistence.

## What I want to remember

- Scheduled tasks can run at startup, logon, a schedule, or on an event
- They can be used for legitimate automation or malicious persistence
- A trusted-looking task name alone proves nothing
- Check the **TaskPath**, action, trigger, and execution history
- Actions may use a **COM handler**, not necessarily an .exe
- A failed LastTaskResult is not automatically suspicious
- Investigation means combining context before deciding what to escalate
