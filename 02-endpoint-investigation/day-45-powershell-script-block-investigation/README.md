# Day 45 - PowerShell Script Block Investigation (Event 4104)

**Focus:** Windows PowerShell logging, distinguishing script definitions from actual actions, and evaluating suspicious-looking events with evidence.

## Objective

Investigate real PowerShell Operational log events on a Windows endpoint. Identify script-block content, correlate timestamps and identifiers, and decide whether the available evidence supports an alert escalation.

## 1. Confirm the PowerShell Operational log is enabled

```powershell
Get-WinEvent -ListLog "Microsoft-Windows-PowerShell/Operational" |
Select-Object LogName, IsEnabled, RecordCount
```

**Observed:**

```text
LogName                                  IsEnabled RecordCount
Microsoft-Windows-PowerShell/Operational      True         613
```

The PowerShell Operational event channel was enabled and contained **613 records in total** at the time of inspection. The number is not a count of Event 4104 records, and an enabled channel by itself doesn't prove that every PowerShell command is logged.

## 2. Find recent Event 4104 records

Event ID **4104** records PowerShell script-block content when the relevant logging is in effect.

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-PowerShell/Operational'
    Id = 4104
} -MaxEvents 5 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, LevelDisplayName |
Format-Table -AutoSize
```

**Actual result:**

```text
TimeCreated           Id   LevelDisplayName
29/10/2026 15:40:05   4104 Warning
29/10/2026 15:40:05   4104 Warning
29/10/2026 15:40:05   4104 Warning
29/10/2026 15:40:05   4104 Warning
29/10/2026 15:40:05   4104 Warning
```

A **Warning** event is worth examining, but it does not independently establish that malware was executed. Multiple records at one timestamp are not proof of multiple attacks. If logging is disabled or records are missing, it is also wrong to conclude that PowerShell never ran; other sources can be considered, including process creation logs and Prefetch.

## 3. Read the recorded script-block text

To view the most recent script-block message:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-PowerShell/Operational'
    Id = 4104
} -MaxEvents 1 |
Select-Object -ExpandProperty Message
```

The output was long, so here are just the relevant excerpts:

```powershell
$script:ClassName = 'root\Microsoft\Windows\Defender\MSFT_MpBehavioralNetworkBlockingRules'
$script:ObjectModelWrapper = [Microsoft.PowerShell.Cmdletization.Cim.CimCmdletAdapter]

function Remove-MpBehavioralNetworkBlockingRules
{
    # generated function body
}

function Get-MpBehavioralNetworkBlockingRules
{
    # generated function body
}

Microsoft.PowerShell.Core\Export-ModuleMember -Function 'Get-MpBehavioralNetworkBlockingRules' -Alias '*'
```

These are **abridged excerpts** from a much larger logged script. The function bodies above are placeholders in this report, not a literal copy of the full code.

The script appeared consistent with automatically generated PowerShell command wrappers for a Microsoft Defender component.

### Key interpretation

The presence of `function Remove-MpBehavioralNetworkBlockingRules` shows that the script **defines** a function that can remove a rule. It does **not** establish that anyone invoked that function, that a rule was removed, or that Defender protections were disabled.

Similarly, `Export-ModuleMember` makes module functions available; it is not evidence that those functions were invoked.

## 4. Compare five script-block identifiers

I retrieved the identifiers for the five recent records and checked for Defender-related strings.

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-PowerShell/Operational'
    Id = 4104
} -MaxEvents 5 |
Select-Object TimeCreated,
    @{Name='ScriptBlockId';Expression={$_.Properties[3].Value}},
    @{Name='MentionsDefender';Expression={$_.Message -match 'MSFT_Mp'}} |
Format-Table -AutoSize
```

**Observed:**

```text
TimeCreated         ScriptBlockId                        MentionsDefender
29/10/2026 15:40:05 f82c797f-e3ee-4659-9632-cf03f174a8ff True
29/10/2026 15:40:05 e498d7fe-bef5-46dd-b9f9-951a777a15e3 True
29/10/2026 15:40:05 e98e048a-a761-476d-92fa-cd3aed141490 True
29/10/2026 15:40:05 4338b7e6-fd9a-4b3e-9a24-6058eb22a749 True
29/10/2026 15:40:05 ec99fe3f-ede4-48cf-9ea9-c5eac0eb86d7 True
```

The **five distinct ScriptBlock IDs** show separate logged script blocks. All five messages matched the `MSFT_Mp` pattern, consistent with Defender-related PowerShell content. This does not prove that any of the defined Defender functions were executed.

## SOC case summary - Real endpoint investigation

**Title:** Warning-level PowerShell script blocks mentioning Defender functions  
**Source:** Windows PowerShell Operational log, Event 4104  
**Assessment:** Low concern based on the evidence examined; not confirmed malicious.

### Evidence

- Operational channel enabled; 613 total records reported at the time of inspection.
- Five recent Event 4104 records, each at **29 October 2026, 15:40:05**, with **Warning** severity.
- Distinct ScriptBlock IDs for the five records.
- All five messages included text matching `MSFT_Mp`.
- The inspected script appeared to consist of generated Defender-related PowerShell function definitions and module exports.

### Analyst conclusion

The available events show that PowerShell **processed and logged script blocks that define Defender-related functions**. They do **not** establish that the `Remove-MpBehavioralNetworkBlockingRules` function was called or that any blocking rule or protection setting changed. No malicious activity was confirmed by this investigation.

### Further checks if supporting alerts appeared

1. Review neighbouring PowerShell events and any available process-creation telemetry to establish the calling process and command context.
2. Check Defender Operational Event **5007** for configuration changes and correlate timestamps, if relevant.
3. Investigate only confirmed changes or other suspicious behaviour and escalate in accordance with response procedures.

**Disposition:** No Defender rule removal demonstrated; no immediate escalation justified by this excerpt alone.

## What I learned

- Event **4104** can provide script-block text, not just a process name.
- **Defining a function is not the same as invoking it.**
- ScriptBlock IDs help distinguish logged blocks; matching timestamps do not prove multiple attacks.
- A **Warning** label requires context rather than an automatic malware conclusion.
- Prefetch can suggest prior PowerShell execution, but not which PowerShell commands ran.
- A SOC report should separate **observed evidence**, **interpretation**, and **what has not been verified**.
