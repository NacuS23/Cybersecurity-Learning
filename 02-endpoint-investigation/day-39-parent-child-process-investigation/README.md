# Day 39 - Investigating parent-child process relationships

Today I used PowerShell to identify the process that launched my current PowerShell session, checked the parent's file path and digital signature, and practised recognising a more suspicious process chain.

## Why parent-child processes matter

Windows records a parent process ID (`ParentProcessId`) for a process. This helps reconstruct which program started another program.

A parent-child relationship is useful context, but it doesn't prove malicious intent. Process IDs can be reused, so process start times matter when investigating historical activity.

## Practical 1 - Find my PowerShell process and its parent

I ran:

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId = $PID" |
Select-Object Name, ProcessId, ParentProcessId, CreationDate
```

The result was:

```text
Name           ProcessId ParentProcessId CreationDate
powershell.exe     20516           24240 23/10/2026 15:28:00
```

- `Get-CimInstance Win32_Process` reads live Windows process information.
- `$PID` is the current PowerShell process's ID.
- `ParentProcessId` is the process ID recorded as its parent.
- `CreationDate` helps show when the process started.

This command inspects **running processes**. It cannot reliably recover a parent that has already exited or attribute old activity using a PID alone.

## Practical 2 - Identify the parent

I used the recorded parent PID:

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId = 24240" |
Select-Object Name, ProcessId, ParentProcessId, CreationDate, ExecutablePath
```

Results:

```text
Name            : explorer.exe
ProcessId       : 24240
ParentProcessId : 4736
CreationDate    : 23/10/2026 15:22:35
ExecutablePath  : C:\WINDOWS\Explorer.EXE
```

The process tree was:

```text
explorer.exe (PID 24240, started 15:22:35)
    |
    +-- powershell.exe (PID 20516, started 15:28:00)
```

This is consistent with PowerShell being opened through the Windows desktop. The parent started before the child, and the parent PID matched the Explorer process inspected.

## Practical 3 - Check the parent executable signature

I ran:

```powershell
Get-AuthenticodeSignature 'C:\Windows\explorer.exe' |
Select-Object Status, @{
    Name='Signer'
    Expression={$_.SignerCertificate.Subject}
}
```

The output showed:

```text
Status : Valid
Signer : CN=Microsoft Windows, O=Microsoft Corporation,
         L=Redmond, S=Washington, C=US
```

The expected path and valid Microsoft Windows signature support a legitimate interpretation, although a trusted parent executable does not guarantee all child process activity is safe.

**Assessment of my real process tree:** Low concern based on the observed parent-child relationship, location and signature. No malicious activity was established.

## Simulated SOC investigation - suspicious Office-to-PowerShell chain

**Training scenario only — not observed on my computer.**

On `FINANCE-PC-09`, an employee opened a document attached to an email from an unfamiliar sender. The subsequent process evidence showed:

```text
WINWORD.EXE       PID 4100
    |
    +-- powershell.exe   PID 5200
                         ParentProcessId 4100
                         Command line: powershell.exe -EncodedCommand ...
```

The PowerShell script then attempted to download a file from an external website.

### Why this matters

- `powershell.exe` has `ParentProcessId 4100`, which matches the observed Word process PID.
- This is direct process relationship evidence, stronger than timestamps alone. When investigating real logs, I would also verify process start times to avoid PID reuse confusion.
- Word starting encoded PowerShell immediately after opening an unexpected attachment is suspicious.
- The attempted external download increases the concern, but the evidence does not yet prove successful compromise.

### SOC ticket

**Title:** Suspicious Office-to-PowerShell execution.

**Priority:** High.

**Evidence:**
- Unfamiliar email attachment opened.
- Microsoft Word recorded as the parent of PowerShell.
- PowerShell launched with an encoded command.
- Script attempted an external file download.

**Assessment:** Possible malicious document triggering command execution and payload retrieval. More evidence is needed to determine whether a file was retrieved, run or made persistent.

**Next steps:**
1. Safely review the decoded PowerShell contents without executing the script.
2. Check the download URL, destination and resulting files, plus endpoint protection telemetry.
3. Investigate scheduled tasks, services and startup entries for persistence.
4. Verify process creation details and consider containment under the incident-response process.

**Decision:** Escalate promptly for investigation.

## What I want to remember

- `Get-CimInstance Win32_Process` can show the live process name, PID, parent PID, creation time and executable path.
- `ParentProcessId` helps identify which process is recorded as having launched another.
- Process IDs identify processes, not people; timestamps help avoid PID reuse mistakes.
- `Get-AuthenticodeSignature` checks signature validity and signer.
- `explorer.exe -> powershell.exe` can be ordinary desktop usage.
- `WINWORD.EXE -> powershell.exe -EncodedCommand`, especially after an unexpected email attachment and with download activity, deserves urgent investigation.
- Separate what process evidence confirms from what still needs checking.
