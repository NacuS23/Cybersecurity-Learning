# PID reuse and event timing

15 November 2026 · Worked example using fictional Windows logs

## Evidence

All events are from LAB-PC, on the same day and clock. Explorer has PID 2000 throughout.

| Row | Time | Recorded event |
|---|---|---|
| A | 09:00:00 | Word starts with PID 3000 |
| B | 09:01:00 | PowerShell starts with PID 4500, parent PID 3000 |
| C | 09:01:20 | A network request from PID 4500 is blocked |
| D | 09:02:00 | PowerShell, PID 4500, exits |
| E | 09:10:00 | Notepad starts with PID 4500, parent PID 2000 |
| F | 09:12:00 | A live lookup shows Notepad as PID 4500 |

## Investigation note

PowerShell ran from 09:01:00 to 09:02:00, so the blocked request at 09:01:20 belongs to PowerShell (rows B–D). Row A identifies Word as PowerShell's parent. Notepad started at 09:10:00 with Explorer as its parent (row E). The 09:12 lookup shows who had the PID then; it cannot attribute the earlier network request by itself.

The log confirms that one request was blocked. It does not show the request's purpose or what other actions PowerShell took.

## Practical check

- **Correcting the ticket:** PowerShell made the blocked request at 09:01:20. Notepad started later and reused PID 4500.
- **Did exiting undo earlier activity?** No. Exiting ends the process, but changes already made, such as files it created, can remain. This sample does not establish whether any such changes happened.

When matching a network event to a process, use the computer, PID and event time together. Check that the event falls within that process's lifetime.
