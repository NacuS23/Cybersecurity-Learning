# PowerShell: reading a process record and using a variable

Completed: 15 October 2026 (exercise delivered 14 October).

## What I practised

I looked at Windows Explorer on my own PC and practised reading its name, PID and executable path. This was a real read-only exercise, not a fictional alert.

## Exercise commands

```powershell
Get-Process -Name explorer
$explorerRecord = Get-Process -Name explorer | Select-Object -First 1
$explorerRecord.ProcessName
$explorerRecord.Id
$explorerRecord.Path
```

## My recorded results

```text
Process name: Explorer
PID: 10732
Executable path: C:\WINDOWS\Explorer.EXE
```

The PID belongs to this observation; it should not be assumed to identify Explorer in a later session.

## My answers and what we clarified

1. **What does `.Id` ask for?** I answered `10732`. That was the observed value; the property asks for the process ID.
2. **Does saving the result create another Explorer process?** I asked how to save it in `$explorerRecord`. We went through the assignment command above: get Explorer, select one result, then store the result in the variable. This does not launch another Explorer process.
3. **Is the name `explorer.exe` enough to trust a file?** My answer: no. Correct.
4. **Which property shows the executable location?** My answer: `$explorerRecord.Path`. Correct.

Follow-up question: which part tells PowerShell to remember the result in a variable?

My answer: `$explorerRecord =` — correct.

## What I learned

- `$explorerRecord` is a variable name; `=` assigns the result on the right to it.
- `Select-Object -First 1` selects one result.
- An assignment normally shows no output. Entering `$explorerRecord` displays the saved result.
- Here, saving means keeping the result in memory in the PowerShell session, not writing a file.
- The dot accesses a property, such as `.Id` or `.Path`.

This helps me collect process details for an investigation. The name and path alone do not prove a process is safe; no signature or malware scan was performed as part of this exercise.
