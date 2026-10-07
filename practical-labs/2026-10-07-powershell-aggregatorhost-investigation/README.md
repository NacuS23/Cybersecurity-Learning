# PowerShell practice and AggregatorHost investigation

Completed: 7 October 2026  
Type: Guided, read-only practice on my own Windows computer

## What I did

I practised building PowerShell commands, then chose AggregatorHost from my process list to investigate. I ran the commands myself, shared the output and reviewed my answers with guidance.

## PowerShell command practice

I first limited the output and selected two fields:

```powershell
Get-Process |
Select-Object -First 5 ProcessName, Id
```

```text
ProcessName             Id
-----------             --
AdobeCollabSync      17932
AdobeCollabSync      21280
AggregatorHost        9012
ApplicationFrameHost 21220
armsvc                5852
```

Then I sorted by process name:

```powershell
Get-Process |
Sort-Object ProcessName |
Select-Object -First 5 ProcessName, Id |
Format-Table -AutoSize
```

```text
ProcessName             Id
-----------             --
AdobeCollabSync      21280
AdobeCollabSync      17932
AggregatorHost        9012
ApplicationFrameHost 21220
armsvc                5852
```

The two AdobeCollabSync rows changed order. Sorting only by name does not guarantee PID order for identical names. Multiple processes with the same name are not automatically suspicious.

I also checked Explorer:

```powershell
Get-Process -Name explorer |
Select-Object ProcessName, Id, Path |
Format-List
```

```text
ProcessName : explorer
Id          : 18792
Path        : C:\WINDOWS\Explorer.EXE
```

### My answers and corrections

- I initially thought the pipe symbol might mean another page or process follows. I learned that it passes the results to the next command.
- I correctly identified Select-Object -First 5 as the part that limits the results.
- I correctly identified Select-Object ProcessName, Id as choosing the fields to show.
- I correctly identified Id here as a process ID, not an Event ID.
- When asked to explain the Explorer command in words, I first supplied a working command. We reviewed the meaning: find Explorer, select its name, PID and path, and display a list.
- For the three-process review, I described getting processes, sorting alphabetically and selecting three. We clarified that sorting was by name only; Id was another displayed column.

## Investigating AggregatorHost

I chose PID 9012 from the list.

I tried running -Filter "ProcessId=9012" on its own and received a CommandNotFoundException. I learned that -Filter is a parameter attached to a command, not a separate command.

The full query worked:

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId=9012" |
Select-Object Name, ProcessId, ParentProcessId, ExecutablePath, CommandLine |
Format-List
```

```text
Name            : AggregatorHost.exe
ProcessId       : 9012
ParentProcessId : 5860
ExecutablePath  : C:\WINDOWS\System32\AggregatorHost.exe
CommandLine     : AggregatorHost.exe
```

I learned that Get-CimInstance asks Windows' management system for information. Win32_Process selects process information, and the filter limits the query to one PID.

## Signature check

```powershell
Get-AuthenticodeSignature -FilePath "C:\Windows\System32\AggregatorHost.exe" |
Select-Object Status, StatusMessage,
    @{Name="Signer"; Expression={$_.SignerCertificate.Subject}} |
Format-List
```

```text
Status        : Valid
StatusMessage : Signature verified.
Signer        : CN=Microsoft Windows, O=Microsoft Corporation, L=Redmond, S=Washington, C=US
```

Windows verified the file's signature. The System32 path and valid Microsoft Windows signature support the file being genuine, but do not guarantee harmless activity.

## Parent process and hosted service

I looked up the recorded parent PID:

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId=5860" |
Select-Object Name, ProcessId, ParentProcessId, ExecutablePath, CommandLine |
Format-List
```

```text
Name            : svchost.exe
ProcessId       : 5860
ParentProcessId : 1352
ExecutablePath  : C:\WINDOWS\System32\svchost.exe
CommandLine     : C:\WINDOWS\System32\svchost.exe -k utcsvc -p
```

Then I queried which service was associated with that PID:

```powershell
Get-CimInstance Win32_Service -Filter "ProcessId=5860" |
Select-Object Name, DisplayName, State, StartMode |
Format-List
```

```text
Name        : DiagTrack
DisplayName : Connected User Experiences and Telemetry
State       : Running
StartMode   : Auto
```

My live observations linked AggregatorHost (9012) to parent PID 5860, which was svchost.exe hosting DiagTrack. PIDs are temporary and can be reused; I did not verify this relationship against historical process-creation logs.

## Investigation questions

**Why look up the services inside svchost.exe?**

My answer was that it shows more information about what the process does. We clarified that svchost.exe can host different services, and the lookup identified DiagTrack specifically.

**Does Auto necessarily mean running now?**

I answered no: it starts automatically when the PC turns on. We clarified that Auto describes startup configuration; State: Running confirms its current state.

**Which two findings supported the file being genuine?**

I correctly named the valid Microsoft signature, but initially chose the -k utcsvc -p arguments as the second finding. We corrected that to the System32 executable location. The service-group argument gives context, not proof of authenticity.

## Conclusion and limits

The evidence supports a legitimate Windows explanation, with no clear malware indicators found in the checks performed. I checked AggregatorHost's path, command line and signature, then identified the process at its recorded parent PID and the service that process hosted.

I did not inspect network activity, scan the file, verify the parent's signature or perform a full behavioural investigation in this exercise. No processes were stopped and no settings were changed.

My main takeaway: use several pieces of evidence together, and understand each part of the command instead of just copying it.
