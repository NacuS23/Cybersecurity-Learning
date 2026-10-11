# OneDC_Updater scheduled task investigation

**Date:** 11 October 2026  
**Type:** Hands-on SOC practice  
**Focus:** Scheduled-task persistence, triggers, actions, privilege context, digital signatures and file metadata

## Objective

Investigate a non-Microsoft scheduled task and decide whether it looks like legitimate persistence or something that should be escalated.

## Finding third-party scheduled tasks

I listed scheduled tasks outside the Microsoft task path:

```powershell
Get-ScheduledTask |
Where-Object { $_.TaskPath -notlike "\Microsoft\*" } |
Select-Object -First 10 TaskName, TaskPath, State |
Format-Table -AutoSize
```

One task that stood out for investigation was:

```text
OneDC_Updater
```

## Task details

I retrieved the task metadata:

```powershell
Get-ScheduledTask -TaskName "OneDC_Updater" |
Select-Object TaskName, TaskPath, State, Author, Description |
Format-List
```

Observed:

- TaskName: `OneDC_Updater`
- State: `Ready`
- Author: `MSI`
- Description: `OneDC_Updater`

The Author field was treated only as a clue, not as proof of legitimacy.

## Task action

I checked what the task actually launches:

```powershell
(Get-ScheduledTask -TaskName "OneDC_Updater").Actions |
Format-List *
```

Observed action:

```text
Execute: C:\Program Files (x86)\MSI\MSI_Center_Updater\OneDC_Updater.exe
Arguments: OneDragonCenter
```

The executable path was consistent with installed MSI software and was more reassuring than a task launching from a user-writable Temp/AppData directory.

## Task triggers

I checked when the task runs:

```powershell
(Get-ScheduledTask -TaskName "OneDC_Updater").Triggers |
Format-List *
```

Observed two enabled triggers:

- Logon trigger with a two-minute delay
- Daily trigger with a one-day interval

This confirmed that the task provides persistence, but persistence itself is not automatically malicious.

## Principal and run level

I checked the task principal:

```powershell
(Get-ScheduledTask -TaskName "OneDC_Updater").Principal |
Format-List *
```

Observed:

- `RunLevel: Highest`
- `LogonType: Group`
- `GroupId: Users`

This did not show the task running as `SYSTEM`. The task can run with the highest privileges available to its security context.

## Digital signature verification

I verified the executable:

```powershell
Get-AuthenticodeSignature "C:\Program Files (x86)\MSI\MSI_Center_Updater\OneDC_Updater.exe" |
Format-List Status, StatusMessage, SignerCertificate
```

Observed:

- Status: **Valid**
- Signature verification succeeded
- Signer: **Micro-Star International CO., LTD.**

The signer matched the task author and the MSI installation path.

## File metadata

I checked the executable metadata:

```powershell
(Get-Item "C:\Program Files (x86)\MSI\MSI_Center_Updater\OneDC_Updater.exe").VersionInfo |
Select-Object CompanyName, ProductName, FileDescription, FileVersion |
Format-List
```

Observed:

- CompanyName: **Micro-Star International Co., Ltd.**
- ProductName: **OneDC_Updater**
- FileDescription: **OneDC_Updater**

The file metadata was consistent with the task name, path and digital signature.

## Analyst reasoning

The task showed several independent pieces of evidence that agreed with each other:

```text
Author says MSI
-> executable is under an MSI Program Files path
-> signature is valid and signed by Micro-Star International
-> file metadata identifies Micro-Star International and OneDC_Updater
```

A scheduled task should not be trusted only because its Author field says a legitimate company name.

If the task instead launched something like:

```text
C:\Users\<user>\AppData\Local\Temp\update.exe
```

and the executable was unsigned, I would not close it as legitimate just because the Author field said MSI. I would continue with file hash, process, network and task-history checks.

## Final assessment

**Low suspicion / likely legitimate scheduled-task persistence.**

The task runs at logon and daily, but:

- the executable is in an expected MSI installation path,
- the digital signature is valid,
- the signer matches Micro-Star International,
- the file metadata matches the expected product,
- and the privilege context did not show a SYSTEM account.

Based on the evidence collected, there was no reason to escalate this task.

## What I learned

- Scheduled tasks are a persistence mechanism, but persistence is not automatically malicious.
- Task **action** tells me what executes.
- Task **trigger** tells me when it executes.
- `Ready` means the task is waiting for a trigger, not currently running.
- `RunLevel: Highest` means the task can use the highest privileges available to its security context.
- The Author field is only metadata and should not be trusted by itself.
- Path, signature, signer, file metadata and task configuration should be correlated.
- A user-writable Temp/AppData path plus an unsigned executable would deserve more investigation.
- Trust the evidence chain, not the label.

## SOC investigation flow

```text
scheduled task
-> task metadata
-> action
-> trigger
-> principal / run level
-> executable path
-> digital signature
-> file metadata
-> final assessment
```

## Privacy

Session-specific identifiers and personal account details are omitted from this public write-up.
