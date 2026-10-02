# Windows process command-line investigation

Completed: 2 October 2026  
Type: Guided hands-on practice on my own Windows computer

## What I practised

I investigated Notepad using PowerShell: its PID, parent PID, executable path, command line and digital signature. I ran the commands myself and reviewed the results and questions with guidance.

## Commands and results

The first command using `$note.Id` did not work for me. I opened Notepad normally and found it by name instead:

```powershell
Get-CimInstance Win32_Process -Filter "Name='notepad.exe'" |
Select-Object Name, ProcessId, ParentProcessId, ExecutablePath, CommandLine |
Format-List
```

| Field | My result |
|---|---|
| Name | Notepad.exe |
| ProcessId | 19232 |
| ParentProcessId | 2968 |
| ExecutablePath | C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2607.14.0_x64__8wekyb3d8bbwe\Notepad\Notepad.exe |
| CommandLine | Quoted executable path followed by a /SESSION: argument |

The session value is omitted from this public note. The path wrapped onto several lines in PowerShell; that was display formatting.

I tried to identify the parent:

```powershell
Get-Process -Id 2968 |
Select-Object ProcessName, Id, Path |
Format-List
```

Result: `Cannot find a process with the process identifier 2968.`

No process with that PID was running when I checked. The recorded parent had exited, so I could not identify its name from this live check. I learned that historical process logs can help when a process has already finished.

I then checked Notepad's signature:

```powershell
$notepadProcess = Get-CimInstance Win32_Process -Filter "ProcessId=19232"
Get-AuthenticodeSignature -FilePath $notepadProcess.ExecutablePath |
Select-Object Status, StatusMessage |
Format-List
```

```text
Status        : Valid
StatusMessage : Signature verified.
```

These PIDs belong to this observation only; they can change and be reused.

## Questions and what I learned

**1. What extra information does the command line give compared with the process name?**

My first answer was "session number?" because I noticed the /SESSION argument. After review, I learned the broader answer: the command line shows how the program was started, including options, files or scripts passed to it.

**2. Does a valid digital signature guarantee harmless activity?**

I answered no, and said further checks are needed. A valid signature supports the file's origin and integrity, but a genuine signed program can still be misused.

**3. Which fictional example deserves investigation first?**

- A: PowerShell deliberately opened by me from Windows Terminal.
- B: PowerShell launched by WINWORD.EXE with an encoded command.

I chose B. During review, we discussed why Word launching PowerShell with an encoded command deserves investigation. Encoding makes a command less readable, but does not prove malware by itself. This was a fictional comparison, not something observed on my computer.

**4. Why does the parent process matter?**

At first I mixed up the parent with the file location, mentioning a Temp folder. I clarified the difference:

- Path: where the executable is stored.
- Parent: which process launched it.
- Command line: how it was launched and what arguments it received.

For the final check about Word launching genuine PowerShell to run a harmful script, my answer was: "what launched, then what it was instructed to do."

## My takeaway

I need to combine the evidence. A familiar name, normal-looking path or valid signature alone does not tell me whether the activity is safe. I completed this exercise with feedback and corrected my confusion between file location and parent process.

This was a controlled learning exercise, not a full malware investigation.
