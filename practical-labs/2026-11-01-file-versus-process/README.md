# File on disk versus running process — 1 November 2026

## Objective
Distinguish a stored executable, a currently running process and historical evidence of execution.

## My live Windows exercise
I opened a blank Notepad window and ran:

```powershell
Get-Process -Name notepad |
Select-Object ProcessName, Id, Path
```

The output showed **Notepad, PID 22076**, with a path under:
`C:\Program Files\WindowsApps\Microsoft.WindowsNotepad_11.2607.14.0_x64__8wekyb3d8bbwe\Notepad\`

PowerShell truncated the end of the displayed path, so I did not record a complete executable path.

After closing the blank window, I ran the same command and reported that nothing appeared. No running Notepad process was shown in that check. This was a process check, not a separate check that the executable still existed on disk.

## Fictional training case
The following records were supplied for LAB-PC. They are made-up training evidence, not observations from my computer.

| Time | Evidence |
|---|---|
| 11:00 | File created: C:\Training\helper.exe |
| 11:02 | Process starts: helper.exe, PID 5100, path C:\Training\helper.exe |
| 11:03 | Process exits: PID 5100 |
| 11:05 | Current process search finds no running helper.exe |
| 11:06 | File check confirms C:\Training\helper.exe still exists |

## Answers and reviewed conclusions
- **Evidence the file existed:** The file-creation record at 11:00.
- **Evidence it ran:** The process-start record at 11:02. The PID number alone is not proof.
- **Why the later process search was empty:** The process-exit record shows it ended at 11:03. The records do not establish whether a user closed it or it exited for another reason.
- **Did the file remain at 11:06?** Yes, according to the supplied file check.

Initially I entered the fictional PID 5100 in the live-observation section. I then checked Notepad on my own computer and confirmed its actual PID was 22076.

## Historical execution check
When asked what could help establish past execution after a process has ended, I answered: **Prefetch**.

Reviewed learning: Windows Prefetch can provide evidence of earlier execution, but it is not always available. Its absence does not prove a program never ran. Process-start logs are another useful source. I did not inspect Prefetch during this exercise.

## Conclusion
A program can stop running while its executable remains on disk. A current process search answers what is running at the time of the check; historical records are needed to investigate earlier activity.
