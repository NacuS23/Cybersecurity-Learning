# Adobe service persistence investigation

**Date:** 9 October 2026  
**Type:** Hands-on SOC practice  
**Focus:** Windows services, persistence, privilege level, executable validation and process correlation

## Objective

Investigate an automatically starting Windows service and determine whether its persistence and privilege level are consistent with legitimate software or deserve escalation.

## Initial service review

I listed running services configured to start automatically:

```powershell
Get-CimInstance Win32_Service |
Where-Object { $_.StartMode -eq 'Auto' -and $_.State -eq 'Running' } |
Select-Object -First 10 Name, DisplayName, StartMode, State, StartName, PathName |
Format-Table -AutoSize
```

I selected the third-party service:

```text
AdobeARMservice
Adobe Acrobat Update Service
```

The service was:

- Running
- Configured for automatic startup
- Running as `LocalSystem`

Automatic startup provides persistence, while `LocalSystem` gives the service powerful privileges. Neither property is malicious by itself, so the executable path and publisher needed to be verified.

## Full service details

I retrieved the complete service configuration:

```powershell
Get-CimInstance Win32_Service -Filter "Name='AdobeARMservice'" |
Select-Object Name, DisplayName, State, StartMode, StartName, PathName |
Format-List
```

The executable path was:

```text
C:\Program Files (x86)\Common Files\Adobe\ARM\1.0\armsvc.exe
```

This path is consistent with installed Adobe software and is more reassuring than a privileged auto-start service executing from a user-writable temporary directory.

## Digital signature verification

I checked the executable with:

```powershell
Get-AuthenticodeSignature "C:\Program Files (x86)\Common Files\Adobe\ARM\1.0\armsvc.exe" |
Format-List Status, StatusMessage, SignerCertificate
```

Observed result:

- Status: **Valid**
- Signature verification succeeded
- Signer: **Adobe Inc.**

This provided strong supporting evidence that the executable was the legitimate Adobe service binary.

## Service-to-process correlation

I checked the process ID assigned to the service:

```powershell
Get-CimInstance Win32_Service -Filter "Name='AdobeARMservice'" |
Select-Object Name, ProcessId
```

I then mapped the PID to the running process:

```powershell
Get-Process -Id <PID> |
Select-Object Id, ProcessName, Path
```

The running process was:

```text
ProcessName: armsvc
Path: C:\Program Files (x86)\Common Files\Adobe\ARM\1.0\armsvc.exe
```

The running process path matched the path configured for the service.

## Analyst reasoning

An auto-start service running as `LocalSystem` deserves careful review because it combines persistence with high privileges.

A service with those same properties pointing to a path such as:

```text
C:\Users\<user>\AppData\Local\Temp\update.exe
```

would deserve significantly more attention because a user-writable temporary directory is an unusual location for a privileged persistent service.

The next checks would include the file signature, publisher, parent/process context, network activity, creation history and whether the persistence mechanism makes sense for the software.

## Final assessment

**Low suspicion / likely legitimate persistence.**

The service is configured to start automatically and runs with high privileges, but:

- the executable is stored in an expected Adobe installation path,
- the Authenticode signature is valid,
- the signer is Adobe Inc.,
- and the running process matches the configured service executable.

Based on the evidence collected, there was no reason to escalate the service.

## What I learned

- Persistence is not automatically malicious.
- `StartMode = Auto` means the service can survive a reboot.
- `LocalSystem` is a high-privilege account and increases the importance of validating the executable.
- The executable path is a major context clue.
- A privileged service running from a user-writable Temp/AppData location deserves more investigation.
- A valid publisher signature is strong supporting evidence, but should be considered with path and behaviour.
- The configured service executable should be correlated with the actual running process.
- Several consistent pieces of evidence are stronger than relying on one indicator.

## SOC investigation flow

```text
service
-> startup mode
-> service account / privilege level
-> executable path
-> digital signature
-> PID
-> running process
-> compare configured path with running process
-> conclusion
```

## Privacy

Session-specific process IDs and personal account details are omitted from this public write-up.

## SOC relevance

This exercise practised validating a persistence mechanism instead of treating persistence itself as malicious. It also reinforced the importance of combining privilege level, file location, signature and process correlation before deciding whether to escalate.
