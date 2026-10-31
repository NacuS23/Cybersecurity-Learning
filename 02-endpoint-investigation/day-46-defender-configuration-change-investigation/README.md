# Day 46 - Investigating Microsoft Defender Configuration Changes

**Date:** 31 October 2026  
**Focus:** Defender Event 5007, PowerShell event correlation and verifying endpoint protection status

## Objective

Investigate real Windows Defender configuration-change events and decide whether they are connected to previously observed PowerShell activity. Compare historical log evidence with the system's current protection state.

## 1. Check Microsoft Defender configuration-change events

Defender **Event ID 5007** records changes to antivirus configuration. A configuration change is worth reviewing, but it isn't automatically evidence of malware.

I queried the Defender Operational log with PowerShell:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Windows Defender/Operational'
    Id = 5007
} -MaxEvents 3 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, Message |
Format-List
```

### Actual results

**31 October 2026, 14:50:15 — Event 5007**

```text
Old value: HKLM\SOFTWARE\Microsoft\Windows Defender\UX Configuration\ToastOrSsoTrigger = 0x1
New value: HKLM\SOFTWARE\Microsoft\Windows Defender\UX Configuration\ToastOrSsoTrigger = 0x0
```

**30 October 2026, 17:32:38 — Event 5007**

```text
Old value: HKLM\SOFTWARE\Microsoft\Windows Defender\UX Configuration\ToastOrSsoTrigger = 0x0
New value: HKLM\SOFTWARE\Microsoft\Windows Defender\UX Configuration\ToastOrSsoTrigger = 0x1
```

**30 October 2026, 15:03:58 — Event 5007**

```text
Old value: HKLM\SOFTWARE\Microsoft\Windows Defender\CoreService\WdConfigHash = 0x390D7929
New value: HKLM\SOFTWARE\Microsoft\Windows Defender\CoreService\WdConfigHash = 0xE586D652
```

### Interpretation

- `ToastOrSsoTrigger` is under Defender's **UX Configuration** registry location. It changed from `0x0` to `0x1` and later back to `0x0`. Without authoritative context about that particular setting, I cannot assume these values mean antivirus protection was switched off or on.
- `WdConfigHash` changed value. The event doesn't identify which underlying setting, if any, prompted the hash change, so the cause remains unverified.
- These entries do **not**, on their own, establish that real-time protection or another key security feature was disabled.
- Because the command uses `-ErrorAction SilentlyContinue`, errors could be hidden; the output is evidence of the events shown, not a complete audit.

## 2. Correlate with PowerShell Event 4104

On **Day 45**, five PowerShell **Event 4104** warnings were observed at **29 October 2026, 15:40:05**. Their script-block messages included Microsoft Defender-related generated function definitions, such as `Remove-MpBehavioralNetworkBlockingRules`.

The Event 5007 records from this lesson are dated **30 and 31 October**, not the same moment as those 4104 warnings.

**Correlation assessment:** The logs reviewed do not establish that those PowerShell script blocks caused these Defender configuration changes. Even events with matching timestamps need supporting evidence to prove causality. Also, seeing a function defined in a script block is not proof that anyone called it.

## 3. Verify current Microsoft Defender protection

I ran:

```powershell
Get-MpComputerStatus |
Select-Object AntivirusEnabled,
              RealTimeProtectionEnabled,
              BehaviorMonitorEnabled,
              IsTamperProtected
```

### Actual result

```text
AntivirusEnabled RealTimeProtectionEnabled BehaviorMonitorEnabled IsTamperProtected
---------------- ------------------------- ---------------------- -----------------
            True                      True                   True              True
```

At the time of the check, all four protections reported **True**:

- Antivirus enabled
- Real-time protection enabled
- Behaviour monitoring enabled
- Tamper protection enabled

This is reassuring **current-state evidence**, but it cannot establish that a protection setting was never disabled in the past. Historical logs and other telemetry would be needed to investigate an earlier interruption.

## SOC investigation summary — Real endpoint observations

**Title:** Microsoft Defender Event 5007 configuration changes  
**Priority:** Low concern based on the limited evidence reviewed  
**Status:** No malicious change established; cause of individual changes not verified

### Evidence

1. Three Event 5007 records found on 30–31 October 2026.
2. Two changes involved `UX Configuration\ToastOrSsoTrigger`; another changed `CoreService\WdConfigHash`.
3. The previously examined PowerShell Event 4104 records occurred on 29 October; no causal link to the Defender changes was demonstrated.
4. Defender antivirus, real-time protection, behaviour monitoring and tamper protection all reported **True** during the current-state check.

### Assessment

The inspected changes are not, by themselves, evidence that Defender was disabled or compromised. The current protection state was enabled. The exact causes of the logged configuration changes were not established, and these checks cannot rule out all past security-setting changes.

### Follow-up if related alerts appear

- Inspect additional Event 5007 messages and Defender protection-setting changes across the relevant timeframe.
- Correlate with process-creation logs, PowerShell 4104 content, administrative activity and endpoint alerts where available.
- Check whether any key Defender protection was actually disabled, by whom and for how long, before escalating.

**Decision:** No immediate escalation based on these records alone; review again if more suspicious evidence appears.

## Key lessons

- **Event 5007** shows Defender configuration changes, not necessarily malicious modifications.
- **Event 4104** captures PowerShell script-block content; a logged function definition is not proof of execution.
- Events close in time might be related, but **timing alone doesn't establish causation**.
- Current protection settings can be healthy even if a security control was changed earlier.
- Report observations separately from interpretations and explicitly record what remains unverified.
