# Day 28 - Microsoft Defender investigation

Today I checked Microsoft Defender status, reviewed Defender events, and wrote a short SOC-style conclusion.

## Defender status

I ran:

```powershell
Get-MpComputerStatus |
Select-Object AntivirusEnabled,RealTimeProtectionEnabled,AntivirusSignatureLastUpdated
```

Result:

```
AntivirusEnabled: True
RealTimeProtectionEnabled: True
AntivirusSignatureLastUpdated: 07/10/2026 09:47:31
```

This confirmed that Microsoft Defender and real-time protection were enabled.

## Defender event log

I checked:

```
Microsoft-Windows-Windows Defender/Operational
```

Important event IDs:

```
1116 = threat detected
1117 = action taken on a threat
5007 = Defender configuration changed
```

The recent events were mostly Event ID 5007.

## Investigating Event 5007

The newest 5007 event showed:

```
Old value:
HKLM\SOFTWARE\Microsoft\Windows Defender\UX Configuration\ToastOrSsoTrigger = 0x1

New value:
HKLM\SOFTWARE\Microsoft\Windows Defender\UX Configuration\ToastOrSsoTrigger = 0x0
```

This was a UX configuration change, not evidence that antivirus or real-time protection had been disabled.

I also searched separately for Defender detections and remediation events:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Microsoft-Windows-Windows Defender/Operational'
    Id=1116,1117
} -MaxEvents 10 |
Select-Object TimeCreated,Id,Message
```

No matching 1116 or 1117 events were found in the current log.

## Assessment

The event was low priority because:

- Defender antivirus was enabled
- Real-time protection was enabled
- the 5007 event changed a UX setting
- there were no 1116 threat detections found
- there were no 1117 remediation events found
- there was no other suspicious activity linked to the change

## SOC ticket practice

```
Alert:
Microsoft Defender configuration change

Evidence:
- Event ID 5007 recorded
- ToastOrSsoTrigger changed from 1 to 0
- AntivirusEnabled = True
- RealTimeProtectionEnabled = True
- No 1116 threat detections found
- No 1117 remediation events found

Assessment:
Low priority. No evidence that Defender protection was disabled or weakened.

Next step:
No further action unless similar events appear with suspicious activity.

Decision:
Close
```

## What I want to remember

- 1116 = threat detected
- 1117 = Defender took action
- 5007 = Defender configuration changed
- 5007 does not automatically mean malware
- Always check what actually changed
- A configuration change matters more if protection was weakened or suspicious activity happened at the same time
- SOC conclusions should explain what was checked and why the evidence supports the decision
