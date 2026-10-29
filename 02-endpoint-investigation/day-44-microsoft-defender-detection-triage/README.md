# Day 44 - Microsoft Defender Detection and Remediation Triage

**Focus:** Checking endpoint protection, reviewing malware detections, and verifying remediation outcomes.

## Objective

Investigate Microsoft Defender status and understand why detecting a threat is different from successfully removing it. Practise writing a short SOC assessment from Defender telemetry.

## 1. Check Microsoft Defender protection status

I used PowerShell to check whether Defender was enabled, when signatures were updated, and what scans were recorded.

```powershell
Get-MpComputerStatus |
Select-Object AMServiceEnabled,
              AntivirusEnabled,
              RealTimeProtectionEnabled,
              AntivirusSignatureLastUpdated,
              QuickScanEndTime,
              FullScanEndTime
```

**Results from my Windows machine:**

```text
AMServiceEnabled              : True
AntivirusEnabled              : True
RealTimeProtectionEnabled     : True
AntivirusSignatureLastUpdated : 29/10/2026 08:13:13
QuickScanEndTime              : 26/10/2026 19:55:32
FullScanEndTime               :
```

Defender's service, antivirus and real-time protection were enabled when checked. The last recorded signature update was on 29 October 2026. A quick scan completion was recorded for 26 October; no full scan completion time was returned.

These are useful health indicators, but they don't prove that a device is free of malware. A blank `FullScanEndTime` also isn't proof that a full scan has never been run.

## 2. Check Defender threat-detection history

```powershell
Get-MpThreatDetection |
Sort-Object InitialDetectionTime -Descending |
Select-Object -First 5 InitialDetectionTime, ThreatID, ActionSuccess, Resources |
Format-List
```

**Observed:** The command returned no output.

That means no detection records were returned by this query. It does not establish that the machine has never been exposed to malware.

Useful fields:

- `InitialDetectionTime` - when Defender first detected the threat.
- `ThreatID` - Microsoft's identifier for the threat.
- `Resources` - files or other resources associated with the detection.
- `ActionSuccess` - whether the recorded remediation action succeeded. If `False`, the action failed or did not complete successfully and needs investigation.

## 3. Check Defender Operational events

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Microsoft-Windows-Windows Defender/Operational'
    Id = 1116,1117
} -MaxEvents 5 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, Message |
Format-List
```

**Observed:** No matching events were returned by the command.

Windows Defender event IDs discussed:

| Event ID | Meaning |
| --- | --- |
| 1116 | Malware or potentially unwanted software detected |
| 1117 | Defender took an action on a detected threat |
| 5007 | Defender configuration changed |

A detection event is not proof of successful remediation. We need to read the action details and outcome. Note that `-ErrorAction SilentlyContinue` can also hide errors, so empty output alone is not a complete assessment.

## 4. Simulated SOC incident - Failed Trojan remediation

*This is a training scenario, not an alert observed on my computer.*

**Host:** `FINANCE-PC-04`  
**File:** `C:\Users\Public\invoice.exe`  
**Threat:** `Trojan:Win32/Example` (fictional example name)

### Evidence provided

- Defender **Event 1116**: Trojan detected.
- Defender **Event 1117**: Remediation attempted.
- `ActionSuccess = False`: Recorded remediation was unsuccessful.
- No matching `invoice.exe` process was found running at the time of investigation.

### Analyst assessment

**Priority: High for this simulated case.** A Trojan was detected and the remediation action was not successful. The lack of a currently running process doesn't establish that the executable never ran or that the threat is gone.

### Recommended next checks

1. Review the full Defender detection and remediation details to understand the failure.
2. Verify whether the identified file is still present and check endpoint protection state.
3. Look for historical execution evidence (available process logs, Prefetch, and endpoint telemetry).
4. Calculate SHA256 and check reputable threat intelligence where available. **A hash is a fingerprint, not a malware scan; zero reputation detections do not prove safety.**
5. Escalate and consider isolation according to the organisation's incident response procedures if the risk warrants it.

**Disposition:** Do not close the incident until the threat's current status and remediation outcome are verified.

## Takeaways

- **Detection ≠ remediation ≠ successful remediation.**
- `Get-MpComputerStatus` helps assess Defender protection state.
- `Get-MpThreatDetection` provides available local threat-detection records.
- Defender Operational log events help reconstruct a detection and the actions taken.
- `ActionSuccess = False` requires follow-up; no running process doesn't rule out earlier execution.
- Keep real observations separate from simulated cases, and don't claim a device is clean based on missing records.
