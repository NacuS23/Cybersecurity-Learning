# Day 23 - Triage prioritisation lab

Today I practiced deciding which endpoint activity should be investigated first instead of treating every alert the same.

## The scenarios

I compared five examples:

### Case A

```
Process: chrome.exe
Path: C:\Program Files\Google\Chrome\Application\chrome.exe
Signature: Valid
Parent: explorer.exe
Remote connection: TCP 443
```

This looked low priority because the process name, path, signature, parent and network activity were all consistent with normal browser activity.

### Case B

```
Startup item: Windows Update Helper
Path: C:\Users\User\AppData\Local\Temp\winupdate.exe
Signature: NotSigned
Startup location: HKCU\Software\Microsoft\Windows\CurrentVersion\Run
```

This was high priority because several suspicious indicators appeared together:

- Microsoft-looking name
- executable stored in Temp
- unsigned file
- persistence through a Run key

### Case C

```
Service: Spooler
Path: C:\Windows\System32\spoolsv.exe
StartMode: Auto
StartName: LocalSystem
Signature: Valid
```

This looked lower priority because the service name, Windows path and valid signature were consistent with a normal Windows service.

### Case D

```
Scheduled task: AdobeCheck
Trigger: AtLogOn
Execute: C:\Users\User\AppData\Roaming\Adobe\check.exe
Signature: Unknown
LastRunResult: 0
```

This deserved investigation because it runs at logon, uses an AppData path and has an unknown signature.

A successful LastRunResult does not prove the task is legitimate. It only means the configured task completed successfully.

### Case E

```
Process: powershell.exe
Parent: winword.exe
Command line:
powershell.exe -ExecutionPolicy Bypass -EncodedCommand ...

Network connection:
TCP 185.x.x.x:443
```

This was the highest-priority case.

The combination of Word launching PowerShell, ExecutionPolicy Bypass, an encoded command and an external network connection is much more suspicious than any one of those indicators alone.

## Triage order

A reasonable priority order was:

```
1. Case E
2. Case B
3. Case D
4. Case C
5. Case A
```

## Investigation workflow

For suspicious activity, I should think about:

```
Where is it?
Who launched it?
What is it doing?
Where is it connecting?
Does it come back automatically?
```

Useful checks include:

- executable path
- parent process
- command line
- digital signature
- remote IP/domain
- network connections
- startup/service/scheduled-task persistence
- file hash and creation time when needed

## What I want to remember

- Triage means deciding what needs attention first
- One suspicious field is weaker than several suspicious indicators together
- Successful execution does not mean legitimate execution
- Temp/AppData paths can deserve extra attention depending on context
- Office launching encoded PowerShell is a strong reason to investigate
- Path, parent, command line, signature, network activity and persistence should be looked at together
