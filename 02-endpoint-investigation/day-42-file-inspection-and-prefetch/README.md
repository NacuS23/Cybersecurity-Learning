# Day 42 - File inspection and Prefetch evidence

Today I examined a real Windows metadata file without executing it, calculated its SHA256 hash, inspected its hex header and signature status, and used Notepad to see the difference between a currently running process and evidence of previous execution. I then assessed a simulated suspicious executable.

## Key question

A file **existing** on disk does not prove it was **executed**. A file's format, signature and hash can inform an investigation, but none of these alone establishes whether it is malware.

## Practical 1 - Review recent downloads

I listed files in my Downloads folder:

```powershell
Get-ChildItem "$env:USERPROFILE\Downloads" -File |
Sort-Object LastWriteTime -Descending |
Select-Object -First 8 Name, Extension, Length, LastWriteTime |
Format-Table -AutoSize
```

The command returned one file:

```text
Name                           Extension  Length  LastWriteTime
Microsoft.Services.Store.winmd .winmd        5120  27/08/2026 19:51:22
```

A `.winmd` file contains Windows Runtime metadata. Its filename is consistent with a Microsoft Store-related component, but a name isn't proof of origin.

## Practical 2 - Calculate its SHA256 fingerprint

```powershell
Get-FileHash "$env:USERPROFILE\Downloads\Microsoft.Services.Store.winmd" -Algorithm SHA256
```

Actual result:

```text
SHA256 45715793B8C8571554B0BFB4ECCC29E2884C16481E1C7DBEE78363BBE4DA3DD9
```

**A SHA256 hash is a fingerprint of the file contents, not a malware verdict.** A reputation lookup with zero detections cannot establish that a file is completely harmless. For sensitive files, prefer checking the hash instead of uploading the file to a public scanner.

I also inspected basic file metadata:

```powershell
Get-Item "$env:USERPROFILE\Downloads\Microsoft.Services.Store.winmd" |
Select-Object Name,Length,CreationTime,LastWriteTime
```

Observed `CreationTime` and `LastWriteTime` were both **27 August 2026, 19:51:22**. File timestamps can be copied or altered, so they are supporting evidence rather than proof of origin.

## Practical 3 - Inspect raw file bytes without executing it

```powershell
Format-Hex -Path "$env:USERPROFILE\Downloads\Microsoft.Services.Store.winmd" |
Select-Object -First 8
```

Selected actual header bytes and readable text:

```text
00000000   4D 5A 90 00 03 00 00 00 ...  MZ......
00000050   69 73 20 70 72 6F 67 72 ...  is progr...
00000060   74 20 62 65 20 72 75 6E ...  t be run...
00000070   6F 64 65 2E ...              ode...
```

The DOS stub contained the standard phrase:

```text
This program cannot be run in DOS mode.
```

### What is MZ?

- The first two hexadecimal bytes were `4D 5A`, or **MZ** in ASCII.
- This is the conventional DOS header signature retained in Windows Portable Executable (PE) format containers. The initials relate to Mark Zbikowski.
- An MZ header doesn't prove the file is an ordinary runnable `.exe`, nor does it prove that Windows executed it.
- A `.winmd` metadata file can use the PE container structure without being an application that a user runs.

## Practical 4 - Check digital signature

```powershell
Get-AuthenticodeSignature "$env:USERPROFILE\Downloads\Microsoft.Services.Store.winmd" |
Select-Object Status,StatusMessage,@{
    Name='Signer'
    Expression={$_.SignerCertificate.Subject}
}
```

**Result:** `NotSigned`. No verified individual Authenticode signature was reported for this metadata file.

NotSigned is not itself a malware detection. The file's purpose and other evidence matter. The file was **not executed** during the inspection.

## Practical 5 - Current process versus historical execution

I opened the trusted Windows Notepad application, then ran:

```powershell
Get-Process -Name "*notepad*" -ErrorAction SilentlyContinue |
Select-Object ProcessName,Id,StartTime
```

Result:

```text
ProcessName  Id    StartTime
Notepad      12388 26/10/2026 18:45:59
```

This shows a Notepad process **running at the time of inspection**. It does not prove anything about execution before the captured start time. No result would also not prove a program has never run.

## Practical 6 - Look for a Windows Prefetch artifact

Prefetch is a Windows application startup performance feature. Its `.pf` artifacts can also be useful in forensic investigations because they can provide evidence consistent with previous program execution.

Read-only query:

```powershell
Get-ChildItem "$env:WINDIR\Prefetch" -Filter "NOTEPAD.EXE-*.pf" -ErrorAction SilentlyContinue |
Select-Object Name,LastWriteTime,Length
```

Observed result:

```text
Name                    LastWriteTime        Length
NOTEPAD.EXE-0D1583A9.pf 26/10/2026 18:46:09  68842
```

The Prefetch file was last modified shortly after Notepad was launched. The eight hexadecimal characters in the Prefetch filename are part of a path-derived identifier, **not the executable's SHA256 hash**.

Important limitations:

- A matching Prefetch artifact is useful evidence consistent with earlier execution, but it needs validation to attribute the exact executable and path.
- `LastWriteTime` is the artifact's file-modification time and should not automatically be treated as a precise first or last execution timestamp.
- Missing Prefetch records don't prove a program never ran; Prefetch can be unavailable, disabled or missing an artifact.

## Simulated SOC investigation (fictional, not activity found on my computer)

An unsigned `update.exe` was discovered in a temporary directory. A hash reputation lookup returned **zero detections**. No matching process was running at the time of investigation, but an `UPDATE.EXE-XXXXXXXX.pf` Prefetch artifact was found.

### SOC ticket

**Title:** Unsigned executable with possible prior execution.

**Priority:** High for the training scenario, pending context and additional evidence.

**Evidence:**
- Unsigned executable in a user temporary directory.
- Zero detections from a hash reputation lookup.
- No currently running matching process.
- A Prefetch artifact associated with the executable name exists.

**Assessment:** The Prefetch artifact supports the possibility that a matching executable previously ran, even though the process is no longer active. Exact file/path attribution and malicious behaviour have not been confirmed. A zero-detection hash reputation result doesn't guarantee safety.

**Next steps:**
1. Inspect the Prefetch record using an appropriate forensic parser and verify associated path/execution details.
2. Review file metadata, origin, SHA256, and relevant endpoint protection detections.
3. Look for supporting process or execution evidence in available logs and other artifacts.
4. Check services, scheduled tasks and startup entries for persistence.
5. Follow the organisation's investigation and containment procedures where justified.

**Decision:** Escalate for further investigation; do not execute the unknown file.

## What I want to remember

- `Get-ChildItem` lists files; `Get-Item` retrieves file properties.
- `Get-FileHash -Algorithm SHA256` identifies file contents, not whether they are malicious.
- `Format-Hex` reveals bytes without executing the file.
- **MZ** (`4D 5A`) is a traditional executable-format header signature, not execution evidence.
- `Get-AuthenticodeSignature` checks whether an individual file has a verifiable signature.
- `Get-Process` shows processes currently running, not a complete execution history.
- Prefetch `.pf` artifacts can support historical execution analysis, with limitations.
- Separate **presence, file type, running process, historical execution evidence and malicious activity** in SOC reporting.
