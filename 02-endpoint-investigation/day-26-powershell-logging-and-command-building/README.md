# Day 26 - PowerShell logging and command building

Today I looked at PowerShell event logs and started learning how to understand PowerShell commands instead of just copying them.

## PowerShell Operational log

I checked:

```
Microsoft-Windows-PowerShell/Operational
```

and found several events including:

```
4104 - Script Block Logging
40961 - PowerShell console starting
40962 - PowerShell console ready
53504 - PowerShell IPC activity
```

The important one for investigations was Event ID 4104 because it can record PowerShell script content.

## Large 4104 events

Some 4104 entries were pages long and split into parts such as:

```
Creating Scriptblock text (1 of 4)
Creating Scriptblock text (2 of 4)
Creating Scriptblock text (3 of 4)
Creating Scriptblock text (4 of 4)
```

The lesson was not to read everything line by line.

Instead, filter for interesting terms such as:

```
EncodedCommand
ExecutionPolicy Bypass
Invoke-WebRequest
Invoke-Expression
DownloadString
http://
https://
Temp
AppData
```

These are clues to investigate, not automatic proof of malware.

## Learning PowerShell properly

Instead of memorising full commands, I started breaking them into pieces.

Example:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4625
} -MaxEvents 5 |
Select-Object TimeCreated, Id, Message
```

The logic is:

```
Get-WinEvent
-> Security log
-> Event 4625
-> maximum 5 events
-> show TimeCreated, Id and Message
```

Important PowerShell commands for SOC work:

```
Get-Process
Get-CimInstance
Get-NetTCPConnection
Get-WinEvent
Get-AuthenticodeSignature
Get-FileHash
Select-Object
Where-Object
Format-List
Format-Table
```

The pipe symbol:

```
|
```

passes output from one command into the next command.

## Learning plan from now on

The goal is not to memorise every command immediately.

The progression will be:

```
1. Understand commands I am given
2. Start completing parts of commands myself
3. Choose the right command for a task
4. Know how to use Get-Help when I forget
```

Useful help command:

```powershell
Get-Help Get-WinEvent -Examples
```

## What I want to remember

- 4104 = PowerShell Script Block Logging
- Large PowerShell logs are normal
- Filter first instead of reading pages of output
- Suspicious keywords are clues, not proof
- Learn the meaning of each PowerShell command part
- Build commands gradually instead of memorising full syntax
- Use Get-Help when needed
