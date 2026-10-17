# Day 37 - PowerShell script-block logging and process auditing

Today I investigated **PowerShell Event 4104** on my Windows workstation, inspected process IDs, looked for a related process-creation event and checked whether process-creation auditing was enabled. I also practised handling a simulated SOC alert when important telemetry is missing.

## Key Windows events

| Event ID | Log | What it can tell us |
| --- | --- | --- |
| 4104 | Microsoft-Windows-PowerShell/Operational | PowerShell script-block content that was logged |
| 4688 | Security | Process creation, when auditing is configured |
| 4624 | Security | A successful logon, including the account, logon type and logon ID |

An encoded PowerShell command can be used by IT scripts as well as attackers. To judge it, an analyst needs the command's contents and surrounding evidence.

## Practical 1 - Inspecting script-block records

I queried the latest three Event 4104 entries. I used a calculated `Preview` property to avoid displaying entire script blocks:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-PowerShell/Operational'
    Id=4104
} -MaxEvents 3 |
Select-Object TimeCreated, Id, @{
    Name='Preview'
    Expression={
        $_.Message.Substring(0,[Math]::Min(200,$_.Message.Length))
    }
} |
Format-List
```

The three preview results were:

| Time | Preview / context |
| --- | --- |
| 16 Oct 2026, 20:52:47 | Copyright notice and `Import-LocalizedData`, consistent with a utility script |
| 15 Oct 2026, 15:36:54 | `$InboxIMEs` and GUID values, potentially related to Windows input-method settings |
| 13 Oct 2026, 15:36:25 | UTF-8 bytes, `MemoryStream` and `Get-FileHash` from earlier learning exercises |

**Assessment:** None of the short previews alone demonstrates malicious activity. Script-block previews do not substitute for reviewing the full relevant record.

## Practical 2 - Extracting Process IDs

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-PowerShell/Operational'
    Id=4104
} -MaxEvents 3 |
Select-Object TimeCreated, Id, ProcessId |
Format-Table -AutoSize
```

Output:

```text
TimeCreated           Id  ProcessId
16/10/2026 20:52:47  4104 18152
15/10/2026 15:36:54  4104  6412
13/10/2026 15:36:25  4104  7388
```

A **PID identifies a process, not a user or an attacker**. Windows may reuse PIDs later, so the event time and other context are important when correlating records.

## Practical 3 - Looking for the matching process-creation event

I looked for Event 4688 with the corresponding Windows process ID `0x46e8` (decimal `18152`) around 16 October at 20:52:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4688
    StartTime=[datetime]'2026-10-16T20:50:00'
    EndTime=[datetime]'2026-10-16T20:55:00'
} -ErrorAction SilentlyContinue |
Where-Object {
    $_.Message -match 'New Process ID:\s+0x46e8\b'
} |
Select-Object TimeCreated,Message |
Format-List
```

**Result:** No matching record appeared in the queried time window.

Possible explanations include missing audit configuration, unavailable events or a process that started outside the time window. A missing 4688 event does **not** prove that the process didn't run or that the activity was benign.

## Practical 4 - Checking Windows process-creation auditing

```powershell
auditpol /get /subcategory:"Process Creation"
```

Actual result:

```text
Detailed Tracking
  Process Creation    No Auditing
```

This means the workstation was **not configured to audit process creation through this Security audit setting at the time of the check**. This is consistent with the missing Event 4688, although I cannot establish that the setting was the same when the earlier process ran.

I made **no Windows configuration changes** during this investigation.

## Simulated SOC investigation (training data, not activity on my computer)

**Scenario:**

- 14:02 — Event 4624: Administrator RDP logon from an unfamiliar IP
- 14:04 — Event 4104: PowerShell script containing an unfamiliar download command
- Search for Event 4688 produces no matching result
- Process Creation auditing is found disabled

### SOC ticket

**Title:** Suspicious remote logon and PowerShell activity with incomplete process telemetry.

**Priority:** High.

**Evidence:** An unfamiliar-source Administrator RDP login was followed closely by a PowerShell script-block event containing a download command. A process-creation event wasn't available; process-creation auditing was disabled when checked.

**Assessment:** Possible unauthorised remote access and suspicious PowerShell execution. The observed timestamps do not conclusively link the script to the RDP session. Missing telemetry limits certainty; disabled auditing alone is **not** evidence that an attacker tampered with the machine.

**Next steps:**
1. Verify whether the Administrator RDP session and source IP were authorised.
2. Review the script's full relevant content and destination safely, without running it.
3. Look for other telemetry, such as available endpoint security, PowerShell and authentication records, to correlate the session with the process.
4. Report the process-creation logging gap and recommend an appropriate audit-policy review.

**Decision:** Escalate the suspicious sequence for further investigation; investigate the logging gap separately.

## What I want to remember

- **4104** can reveal PowerShell script-block content; **4688** can show process creation; **4624** shows successful logons.
- `Select-Object` calculated properties can create a short preview of a large log message.
- Event `ProcessId` is useful for correlation, but a PID doesn't identify the person responsible.
- A close timestamp does not prove two actions belong to the same actor or session.
- `auditpol /get /subcategory:"Process Creation"` shows the current process-creation auditing setting.
- No matching process-creation event can mean a **visibility gap**, not a clean security bill.
- Separate **observed facts, hypotheses, unknowns and concrete next steps** in a SOC report.
