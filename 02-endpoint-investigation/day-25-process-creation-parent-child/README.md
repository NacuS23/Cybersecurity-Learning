# Day 25 - Process creation and parent-child relationships

Today I worked with Windows Event ID 4688 and practiced using parent-child process relationships during endpoint triage.

## Event ID 4688

Event ID 4688 means:

```
A new process has been created
```

Useful fields include:

- New Process Name
- New Process ID
- Creator Process Name
- Creator Process ID
- Process Command Line
- Account context

The main questions are:

```
What launched?
Who launched it?
What command did it run?
Does that relationship make sense?
```

## Normal example

I found this process relationship in the Security log:

```
C:\Windows\System32\smss.exe
    ->
C:\Windows\System32\autochk.exe
```

This looked normal because both files were in System32 and the parent-child relationship matched expected Windows startup behaviour.

I also found:

```
C:\Windows\System32\smss.exe
    ->
C:\Windows\System32\csrss.exe
```

Again, this looked consistent with normal Windows startup activity.

## Suspicious example

A simulated high-priority example was:

```
WINWORD.EXE
    ->
powershell.exe -ExecutionPolicy Bypass -EncodedCommand ...
```

The suspicious part was not simply the filenames.

The stronger indicators were:

- Word launching PowerShell
- ExecutionPolicy Bypass
- EncodedCommand
- possible external network activity

This showed how legitimate Microsoft tools can still be abused.

## Real process investigation

I investigated a live process:

```
Process: WUDFHost.exe
PID: 2032
Parent PID: 1352
Path: C:\Windows\System32\WUDFHost.exe
```

The command line contained Windows User-Mode Driver Framework parameters and GUID values.

I checked the digital signature:

```
Status: Valid
Signer: Microsoft Windows
```

The parent process was:

```
services.exe
PID: 1352
```

So the process tree was:

```
services.exe
    ->
WUDFHost.exe
```

This relationship made sense for a Windows driver-framework host.

## Conclusion

The WUDFHost.exe process looked low priority / likely benign because:

- it was in the expected System32 path
- it had a valid Microsoft signature
- its parent was services.exe
- the command line matched normal Windows framework activity
- the parent-child relationship made sense

## What I want to remember

- 4688 = new process created
- Parent-child relationships are important
- A legitimate filename does not automatically mean safe
- A strange-looking command line does not automatically mean malicious
- Context matters more than one field
- Useful flow:

```
Process
-> Parent
-> Path
-> Signature
-> Command line
-> Network behaviour
-> Pattern/context
```

- Several reassuring signals together can justify closing an alert as low priority
