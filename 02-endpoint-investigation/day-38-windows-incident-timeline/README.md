# Day 38 - Building a Windows incident timeline

Today I combined Windows logon events with PowerShell activity into a single timeline. I investigated one of the logons and practised distinguishing **what the logs confirm** from **what still needs evidence**.

## What I investigated

I revisited a real PowerShell script-block record from **16 October 2026 at 20:52:47**, originally found in Day 37. It had **Event ID 4104** and **Process ID 18152**.

I wanted to see whether any successful logons happened around the same time.

### Windows events involved

| Event ID | Log | Meaning |
| --- | --- | --- |
| 4624 | Security | Successful logon |
| 4104 | Microsoft-Windows-PowerShell/Operational | PowerShell script-block activity |
| 4688 | Security | New process created, if auditing was enabled |

## Practical 1 - Combine events into one timeline

I used this PowerShell script:

```powershell
$start = [datetime]'2026-10-16 20:50'
$end = [datetime]'2026-10-16 20:55'

$psEvents = @(Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-PowerShell/Operational'
    Id=4104
    StartTime=$start
    EndTime=$end
} -MaxEvents 20 -ErrorAction SilentlyContinue)

$loginEvents = @(Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4624
    StartTime=$start
    EndTime=$end
} -MaxEvents 20 -ErrorAction SilentlyContinue)

($psEvents + $loginEvents) |
Sort-Object TimeCreated |
Select-Object TimeCreated,Id,LogName,ProcessId |
Format-Table -AutoSize
```

New commands and techniques:

- `$start` / `$end`: variables containing the investigation window.
- `$psEvents` / `$loginEvents`: variables containing the event records retrieved from each log.
- `@(...)`: makes an array of results, including when there are zero or one results.
- `+`: combines the two collections.
- `Sort-Object TimeCreated`: puts the events in chronological order.
- `Select-Object`: chooses the columns for the report.

### Actual timeline

```text
TimeCreated           Id   LogName                                 ProcessId
16/10/2026 20:52:45  4624 Security                                     1388
16/10/2026 20:52:46  4624 Security                                     1388
16/10/2026 20:52:46  4624 Security                                     1388
16/10/2026 20:52:46  4624 Security                                     1388
16/10/2026 20:52:46  4624 Security                                     1388
16/10/2026 20:52:47  4104 Microsoft-Windows-PowerShell/Operational    18152
16/10/2026 20:53:07  4624 Security                                     1388
```

This produced **six Event 4624 records** and **one Event 4104 record** during the window.

These are event metadata Process IDs, so the `ProcessId` property on the Security 4624 entries should not be treated as the PID of the account or user that logged in. The different PIDs are not proof of a process relationship.

## Practical 2 - Inspect one successful logon

I examined a logon just before the PowerShell event:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4624
    StartTime=[datetime]'2026-10-16 20:52:44'
    EndTime=[datetime]'2026-10-16 20:52:47'
} -MaxEvents 1 |
Format-List TimeCreated,Message
```

The returned event at **20:52:46** contained:

```text
Subject Account: <COMPUTER>$
Logon Type:      5
New Logon:       NT AUTHORITY\SYSTEM
Logon ID:        0x3E7
Process:         C:\Windows\System32\services.exe
Source IP:       -
Elevated Token:  Yes
```

Interpretation:

- **Logon Type 5** = service logon, **not RDP**.
- **SYSTEM** with Logon ID `0x3E7` is a common Windows LocalSystem context.
- `services.exe` in System32 is consistent with Windows Service Control Manager activity.
- The event did not record a remote source IP.
- This individual logon is consistent with normal Windows activity; it is not evidence that a service launched the nearby PowerShell script.

## Practical 3 - Search the sample for local interactive and RDP logons

Using the saved variable from the first query:

```powershell
$loginEvents |
Where-Object {
    $_.Message -match 'Logon Type:\s+(2|10)\b'
} |
Select-Object TimeCreated, Message |
Format-List
```

**Result:** No output.

Among the six sampled successful logon records, **none matched Logon Type 2 (interactive) or 10 (RDP)**. This does not establish that all six were Type 5, or that no one signed in outside this sample.

## Assessment: what can I actually conclude?

**Confirmed:**
- Event 4104 recorded PowerShell script activity at 20:52:47, PID 18152.
- Multiple successful logon events were recorded near that time.
- One examined logon was a SYSTEM service logon (Type 5) at 20:52:46.
- No Type 2 or Type 10 logons appeared in the six-event sample.

**Unknown:**
- Which parent process launched the PowerShell process.
- Which account or security context was responsible for that script.
- Whether the script was related to any of the nearby service logons.

Day 37 established that **Process Creation auditing was set to No Auditing when checked**, limiting our ability to identify the parent via Event 4688. We also did not find a matching 4688 record around the PowerShell event.

**Initial assessment:** No malicious behaviour established from the records examined; the PowerShell process origin remains unconfirmed. Temporal proximity does **not** establish causation.

### Concise SOC note

**Title:** PowerShell activity near SYSTEM service logons — source not attributed.

**Evidence:** One PowerShell 4104 record and six successful logon events in a five-minute sample. One logon inspected in detail was an expected-looking SYSTEM Type 5 service logon.

**Assessment:** Insufficient evidence to claim that the service launched PowerShell, or that the activity was malicious.

**Recommended follow-up:** Review full 4104 script content and any available PowerShell/endpoint telemetry; investigate process ancestry if additional monitoring data exists. Note the process-creation audit coverage gap.

**Decision:** Do not label this as a confirmed attack or attribute the PowerShell process to a service without further evidence.

## Key lessons

- Sorting records from different logs gives a useful **timeline**, not automatically a causal chain.
- The same timestamp, or events one second apart, does not prove the same account or process caused them.
- **Logon Type 5 = service; Type 10 = RDP; Type 2 = interactive.**
- Windows Event 4624 **New Logon** contains the account that logged in.
- A PowerShell **PID** may help link activity to process telemetry, but it does not identify the user on its own.
- SOC notes should clearly separate **confirmed facts, suspected relationships, missing evidence and next steps**.
