# Fictional attachment and process-chain investigation

**Date:** 14 November 2026  
**Type:** Supplied fictional evidence, with answers reviewed during practice. This was not an incident observed on my computer.

## Goal

Connect an attachment to the processes it launched by matching process IDs (PIDs) and parent process IDs. Separate confirmed activity from outcomes that still need evidence.

## Supplied case

Sam opened an unexpected attachment called `Invoice.docm` on fictional computer `LAB-PC`. PID 2000 belonged to `explorer.exe`. Each PID was unique within this exercise's time period.

| Row | Time | Recorded event | PID | Parent PID |
|---|---|---|---:|---:|
| A | 14:00:00 | Invoice.docm saved | — | — |
| B | 14:01:00 | WINWORD.EXE starts; Invoice.docm appears in its command line | 3000 | 2000 |
| C | 14:01:05 | powershell.exe starts | 4500 | 3000 |
| D | 14:01:06 | msedge.exe starts | 4600 | 2000 |
| E | 14:01:08 | Network request from PowerShell blocked | 4500 | — |

PowerShell's command line instructed it to download a script into a temporary folder. No record confirming script execution was supplied.

## My answers and the corrections I reviewed

- I correctly identified PowerShell as PID **4500**, its parent PID as **3000** in row C, and PID 4500 as responsible for the blocked request.
- I initially thought Edge was launched by Word because its parent PID was 2000. After reviewing the mapping, I understood that **Explorer (2000) launched both Word and Edge**. Word (3000) launched PowerShell (4500).
- In the final check, I correctly identified **rows B and C together** as the evidence linking Word to PowerShell: B names the process with PID 3000; C records 3000 as PowerShell's parent.
- I initially described the invoice opening and the blocked PowerShell activity as suspicious. The more precise observations are that Word launched PowerShell, and PowerShell was instructed to download a script into a temporary folder.
- I asked why PowerShell was blocked. The evidence actually records a **blocked network request**, not that PowerShell itself was stopped. The reason for the block was not provided.
- My final answer was that a block does not mean the investigation is over or the device is safe. It establishes that this particular request was blocked.

## Reviewed investigation note

Word opened Invoice.docm and launched PowerShell, whose command line instructed it to download a script into a temporary folder. A network request from PowerShell was blocked; these records do not confirm a completed download or script execution, and Edge was launched by Explorer.

## Evidence limits and a next check

A command to download a script does not prove that a file arrived or ran. The block does not establish that the PowerShell process exited, that every request was blocked, or that the device was safe.

A useful next evidence request would be file-creation records for the intended download path and process or script-execution records from the same device and time window. These would help establish whether the file was saved and whether it was executed.

## What I learned

Match a child's parent PID to the parent's own PID. Two processes sharing a parent are not automatically parent and child. Keep the investigation conclusion within what the records actually show.
