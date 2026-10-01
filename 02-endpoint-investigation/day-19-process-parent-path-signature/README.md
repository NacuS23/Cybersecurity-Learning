# Day 19 - Process investigation: parent, path and signature

Today I investigated a running Windows process and checked more than just its name.

## Process selected

I used:

```powershell
Get-Process | Sort-Object CPU -Descending | Select-Object -First 10 Name, Id, CPU
```

and chose:

```
WhatsApp.Root.exe
PID: 16492
```

## Parent process and executable path

I ran:

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId=16492" |
Select-Object Name, ProcessId, ParentProcessId, ExecutablePath
```

The process details showed:

```
Process: WhatsApp.Root.exe
PID: 16492
Parent PID: 24468
Path: C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2632.100.0_x64__cv1g1gvanyjgm\...
```

I then checked the parent PID:

```powershell
Get-Process -Id 24468
```

The parent process was:

```
sihost.exe
```

A parent process is the process that launched another process.

## Signature check

I checked the executable with:

```powershell
Get-AuthenticodeSignature "C:\Program Files\WindowsApps\5319275A.WhatsAppDesktop_2.2632.100.0_x64__cv1g1gvanyjgm\WhatsApp.Root.exe"
```

The individual executable showed:

```
Status: NotSigned
```

That result alone was not enough to decide whether the app was suspicious.

## Microsoft Store package check

Because the process was running from the WindowsApps directory, I checked the package:

```powershell
Get-AppxPackage *WhatsApp* |
Select-Object Name, Publisher, Version, InstallLocation, SignatureKind, Status
```

The result showed:

```
Name: 5319275A.WhatsAppDesktop
Version: 2.2632.100.0
SignatureKind: Store
Status: Ok
InstallLocation: C:\Program Files\WindowsApps\...
```

This gave better context than relying on the individual EXE signature by itself.

## Investigation summary

The process was running from the WindowsApps directory, had a plausible Windows shell parent process, and belonged to a Microsoft Store package with:

```
SignatureKind: Store
Status: Ok
```

No immediate evidence of malicious activity was identified from these checks.

## What I want to remember

- PID = Process ID
- Parent process = the process that launched another process
- Executable path gives useful context
- A normal-looking filename alone is not enough
- A valid signature is supporting evidence, not absolute proof
- NotSigned does not automatically mean malicious
- Store-packaged apps should also be checked at package level
- Temp/AppData paths can deserve more attention depending on context
