# Day 21 - Startup programs and persistence

Today I looked at startup programs and how they can be used for persistence.

## Startup entry investigated

I used:

```powershell
Get-CimInstance Win32_StartupCommand |
Where-Object {$_.Name -eq "RtkAudUService"} |
Format-List Name, Command, Location, User
```

The startup entry was:

```
Name     : RtkAudUService
Command  : "C:\WINDOWS\System32\DriverStore\FileRepository\realtekservice.inf_amd64_a112e46fc636d880\RtkAudUService64.exe" -background
Location : HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
User     : Public
```

## What the fields mean

The `Command` field shows what executable is launched.

The executable path was inside the Windows DriverStore:

```
C:\WINDOWS\System32\DriverStore\FileRepository\...
```

The startup location was:

```
HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run
```

This is a common registry location used to launch programs automatically when users log in.

## Digital signature check

I checked the executable with:

```powershell
Get-AuthenticodeSignature "C:\WINDOWS\System32\DriverStore\FileRepository\realtekservice.inf_amd64_a112e46fc636d880\RtkAudUService64.exe"
```

The result was:

```
Status: Valid
```

I then checked the signer certificate:

```powershell
(Get-AuthenticodeSignature "C:\WINDOWS\System32\DriverStore\FileRepository\realtekservice.inf_amd64_a112e46fc636d880\RtkAudUService64.exe").SignerCertificate |
Select-Object Subject, Issuer, NotBefore, NotAfter
```

The certificate subject showed:

```
Microsoft Windows Hardware Compatibility Publisher
```

This is consistent with a properly signed Windows hardware/driver component.

## Persistence

Persistence means a program has a way to keep running or start again after reboot or login.

Malware can use startup locations to survive restarts, so startup entries are useful to inspect during an investigation.

A suspicious combination might be:

```
Unknown startup item
+
Temp/AppData executable
+
unexpected publisher/signature
```

## What I want to remember

- Startup entries can create persistence
- HKLM\...\Run is a startup registry location
- Command shows what executable is launched
- Path helps show whether the file is in an expected location
- A valid signature is supporting evidence, not proof
- Microsoft Windows Hardware Compatibility Publisher is consistent with a properly signed driver component
- Temp/AppData startup executables can deserve more investigation
