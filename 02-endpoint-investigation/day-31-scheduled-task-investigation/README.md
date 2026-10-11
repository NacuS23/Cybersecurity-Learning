# Day 31 - Scheduled task investigation

Today I investigated an actual Windows scheduled task to understand persistence, task actions, triggers and how to decide whether a task needs attention.

## Task Scheduler event logging

I tried to look for Event ID 106 (task registration) in the `Microsoft-Windows-TaskScheduler/Operational` log, then checked the log status:

```powershell
Get-WinEvent -ListLog "Microsoft-Windows-TaskScheduler/Operational" |
Select-Object LogName, IsEnabled, RecordCount
```

The log showed `IsEnabled: False`. That means I couldn't use that log's event history for this investigation. It does **not** mean scheduled tasks aren't running.

Other useful Task Scheduler Operational event IDs to recognise:
- **106** - task registered
- **140** - task updated
- **200** - task action started
- **201** - task action completed

## Listing scheduled tasks

I inspected enabled tasks:

```powershell
Get-ScheduledTask |
Where-Object {$_.State -ne "Disabled"} |
Select-Object -First 15 TaskName, TaskPath, State
```

I selected `OneDC_Updater` because I wanted to confirm which software owned it.

The task was in the root task path and its state was `Ready`. **Ready** means it is enabled and awaiting a trigger, not that it is currently running.

## What the task launches

```powershell
(Get-ScheduledTask -TaskName "OneDC_Updater").Actions |
Format-List *
```

Result:

```
Execute: C:\Program Files (x86)\MSI\MSI_Center_Updater\OneDC_Updater.exe
Arguments: OneDragonCenter
```

The path and action looked consistent with an MSI software updater.

## Signature verification

```powershell
Get-AuthenticodeSignature "C:\Program Files (x86)\MSI\MSI_Center_Updater\OneDC_Updater.exe" |
Format-List Status, SignerCertificate
```

Results:
- **Status:** Valid
- **Signer:** Micro-Star International Co., Ltd.

That matched the expected MSI publisher. A valid signature supports authenticity and file integrity; it does not automatically prove every action is safe.

## When the task runs

```powershell
(Get-ScheduledTask -TaskName "OneDC_Updater").Triggers |
Select-Object @{Name='TriggerType';Expression={$_.CimClass.CimClassName}},Enabled,StartBoundary,UserId,Repetition |
Format-List
```

The task had two enabled triggers:
- **Logon trigger:** can run when someone signs in
- **Daily trigger:** `StartBoundary: 2006-12-20T06:00:00`

The old `StartBoundary` is a scheduling setting, **not proof** that the task was installed in 2006. The repetition pattern was not expanded in this check.

## SOC ticket

**Alert:** Unknown scheduled task — `OneDC_Updater`

**Assessment:** Low priority; likely legitimate MSI updater activity.

**Evidence:**
- Executable path was in an expected MSI software directory.
- Executable signature was valid and signed by Micro-Star International.
- Logon and daily triggers were consistent with updater activity.
- No suspicious command-line argument or unexpected executable location was identified.

**Decision:** Close as likely benign based on available evidence.

**Limitation:** Task Scheduler Operational logging was disabled, so I did not verify historical executions from that log. Reinvestigate if unusual activity appears.

## What I want to remember

- A scheduled task has an **action** (what it runs) and **trigger** (when it runs).
- Automatic execution can be legitimate or can be used for persistence.
- `Ready` doesn't mean `Running`.
- Check name, action, path, digital signature, triggers and context.
- Task names alone are weak evidence.
- Lack of event logs is not proof of absence of activity.
- Explain **why** evidence supports a low/high rating and a close/escalate decision.
