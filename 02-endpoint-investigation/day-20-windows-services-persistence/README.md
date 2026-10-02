# Day 20 - Windows services and persistence basics

Today I looked at Windows services and how they can be useful during an endpoint investigation.

## What a Windows service is

A Windows service is a background program that Windows or an application can run, often without a normal user interface.

Services can be used for things like:

- updates
- networking
- antivirus
- printing
- application support
- other background system tasks

## Service I investigated

I checked the service:

```
AppXSvc
```

using:

```powershell
Get-CimInstance Win32_Service -Filter "Name='AppXSvc'" |
Select-Object Name, State, StartMode, PathName, StartName
```

The result showed:

```
Name      : AppXSvc
State     : Running
StartMode : Auto
PathName  : C:\WINDOWS\system32\svchost.exe -k wsappx -p
StartName : LocalSystem
```

## What the fields mean

`State: Running` means the service is currently active.

`StartMode: Auto` means the service is configured to start automatically.

`PathName` shows the executable and arguments the service uses.

The path in this case pointed to:

```
C:\Windows\System32\svchost.exe
```

which is an expected Windows location.

`StartName: LocalSystem` means the service runs under the LocalSystem account, which has high privileges.

## Persistence

One security reason services matter is persistence.

If malware creates or modifies a service and configures it to start automatically, it may be able to come back after a reboot.

That is why combinations like this deserve attention:

```
Auto-start
+
unexpected executable path
```

For example, an auto-start service pointing to a strange executable in a Temp folder would deserve more investigation.

## What I want to remember

- Service = background program
- Auto = configured to start automatically
- PathName = what executable actually runs
- Persistence = ability to survive/restart after reboot
- Auto-start + strange path = investigate
- LocalSystem = high privilege, not automatically malicious
- One field alone is not enough to decide whether a service is safe or malicious
