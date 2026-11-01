# Day 47 - Building an Incident Timeline from Windows Event Logs

**Date:** 1 November 2026  
**Focus:** PowerShell Event 4104, Microsoft Defender Events 5007 / 5000 / 5001 / 5004, and evidence-based event correlation

## Objective

Create a chronological view of events from two Windows logs and investigate whether PowerShell script activity can be linked to later changes in Microsoft Defender configuration.

This was a **real, read-only investigation** of events on my Windows computer. No attack was confirmed.

## 1. Merge events from different logs

I collected the three most recent PowerShell Event 4104 records and the three most recent Defender Event 5007 records, combined the arrays, and sorted the results by time.

```powershell
$psEvents = @(Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-PowerShell/Operational'
    Id = 4104
} -MaxEvents 3 -ErrorAction SilentlyContinue)

$defEvents = @(Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Windows Defender/Operational'
    Id = 5007
} -MaxEvents 3 -ErrorAction SilentlyContinue)

$psEvents + $defEvents |
Sort-Object TimeCreated |
Select-Object TimeCreated, Id, ProviderName |
Format-Table -AutoSize
```

### Actual timeline

```text
TimeCreated           Id ProviderName
31/10/2026 14:59:52 4104 Microsoft-Windows-PowerShell
31/10/2026 14:59:52 4104 Microsoft-Windows-PowerShell
31/10/2026 14:59:52 4104 Microsoft-Windows-PowerShell
31/10/2026 15:09:13 5007 Microsoft-Windows-Windows Defender
31/10/2026 19:18:43 5007 Microsoft-Windows-Windows Defender
01/11/2026 15:11:00 5007 Microsoft-Windows-Windows Defender
```

The first Defender configuration event followed the PowerShell events by **9 minutes and 21 seconds**.

**Limitation:** The command selected only the **three most recent records from each log**, so this was a partial timeline, not a comprehensive event history. Event order alone does not establish causality.

## 2. Examine the first Defender change

I narrowed the search to the first Defender event:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Windows Defender/Operational'
    Id = 5007
    StartTime = [datetime]'2026-10-31 15:08:00'
    EndTime = [datetime]'2026-10-31 15:11:00'
} |
Select-Object TimeCreated, Message |
Format-List
```

### Actual event detail

```text
TimeCreated : 31/10/2026 15:09:13
Id          : 5007
Old value   : HKLM\SOFTWARE\Microsoft\Windows Defender\CoreService\WdConfigHash = 0xE586D652
New value   : HKLM\SOFTWARE\Microsoft\Windows Defender\CoreService\WdConfigHash = 0x9EEDB5AF
```

**Interpretation:** The `WdConfigHash` value changed. This event alone does **not** identify the underlying cause or show that antivirus protection was turned off. It also does not identify PowerShell as the initiator.

## 3. Inspect nearby PowerShell script blocks

I searched the two-minute window around 14:59 for Event 4104 records and checked whether their text contained common Defender-related or download-related strings.

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-PowerShell/Operational'
    Id = 4104
    StartTime = [datetime]'2026-10-31 14:59:00'
    EndTime = [datetime]'2026-10-31 15:01:00'
} |
Select-Object TimeCreated,
    @{Name='MentionsDefender';Expression={$_.Message -match 'MSFT_Mp|Windows\\Defender'}},
    @{Name='MentionsDownload';Expression={$_.Message -match 'Invoke-WebRequest|DownloadFile|Start-BitsTransfer'}} |
Format-Table -AutoSize
```

### Actual findings

- Multiple 4104 records appeared at **14:59:51–14:59:52**, rather than just the three selected in the first query.
- Several events returned `MentionsDefender = True`; others returned `False`.
- All records displayed returned `MentionsDownload = False` for the **specific command strings searched**.

**Interpretation:** Some logged script text mentioned Defender. That does not prove that Defender settings were changed. The negative download-string search does not rule out all ways of downloading files; it only establishes that these particular terms were not found in the returned messages.

Earlier training on Event 4104 showed that PowerShell can log **function definitions**, including Defender-management functions, without showing that those functions were actually invoked.

## 4. Look for evidence of real-time protection being toggled

Relevant Defender Operational event IDs:

| Event ID | Investigation purpose |
| --- | --- |
| 5000 | Real-time protection enabled |
| 5001 | Real-time protection disabled |
| 5004 | Real-time protection configuration changed |
| 5007 | Defender configuration changed |

I searched for real-time protection events on 31 October:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Windows Defender/Operational'
    Id = 5000,5001,5004
    StartTime = [datetime]'2026-10-31 00:00:00'
    EndTime = [datetime]'2026-11-01 00:00:00'
} -MaxEvents 20 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, Message |
Format-List
```

**Observed:** The query returned no output.

This means **no matching records were returned by that query**. It does not conclusively prove there was never a protection interruption. The command's `-ErrorAction SilentlyContinue` parameter may also hide an error.

### Interruption example — hypothetical, not an observed event

If a genuine **5001** event showed protection disabled at **15:05** and a later **5000** event showed it enabled at **15:10**, that would be evidence of a roughly **five-minute protection gap**. Those events did **not** appear in this investigation.

## SOC investigation report

**Title:** Correlation of PowerShell script block logging and Defender configuration changes  
**Case type:** Real endpoint telemetry review  
**Priority:** Low concern on the evidence examined  
**Disposition:** No confirmed malicious activity or Defender shutdown

### Confirmed observations

1. PowerShell Event 4104 script blocks were logged on **31 October 2026 at 14:59:51–52**.
2. Defender Event 5007 recorded a `WdConfigHash` change at **15:09:13**, followed by additional Event 5007 records later on 31 October and on 1 November.
3. A portion of the 4104 script-block messages contained Defender-related text.
4. None of the checked 4104 messages contained the particular download-command strings used in the search.
5. The query for Defender Events 5000, 5001 and 5004 on 31 October returned no output.

### Assessment

A timeline establishes the **order and interval** between observed events. It does not show that the earlier PowerShell activity caused the subsequent `WdConfigHash` change. The configuration-hash change is not equivalent to evidence that antivirus protection was disabled. No download, compromise or protection gap was established by the reviewed records.

### Possible next investigative steps

- Examine relevant 4104 script contents and process context more closely if new alerts justify it.
- Investigate additional Event 5007 details and other relevant Defender records.
- Correlate with process-creation telemetry, user/admin activity, and protection history if available.
- Avoid claiming causality without a link such as an executed configuration-changing command, corroborating endpoint activity, or a verified protection-state change.

## Key learning

- Use arrays `@(...)`, `+` and `Sort-Object TimeCreated` to combine log sources into a chronological timeline.
- A timeline provides **sequence**, not necessarily **cause**.
- Searching for strings in script-block logs is a useful filter, not proof that an operation succeeded.
- **Defender Event 5007** is a configuration-change signal, not automatically an antivirus-disablement event.
- Clearly distinguish **observed activity**, **plausible hypotheses**, **missing evidence** and **final assessment** when documenting a SOC investigation.
