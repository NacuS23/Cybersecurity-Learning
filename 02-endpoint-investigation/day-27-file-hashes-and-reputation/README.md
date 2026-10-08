# Day 27 - File hashes and reputation

Today I learned how file hashes fit into endpoint investigations and how to use them as supporting evidence rather than as a final answer.

## New PowerShell command

I used:

```powershell
Get-FileHash "C:\Windows\System32\WUDFHost.exe" -Algorithm SHA256
```

This calculates a SHA256 hash for the file.

The result was:

```
SHA256:
580FFE166B064B2AB43A937B3A9002DF4C4D0EE152E482E447B8F7D8B5B6D176
```

## What a hash means

A hash acts like a fingerprint for the exact file.

Important points:

- the hash itself does not tell me whether a file is malicious
- if the file changes, the hash changes
- the same exact file produces the same SHA256 hash
- reputation services can recognise a file by its hash if they have seen that exact file before

## VirusTotal check

I searched the SHA256 hash on VirusTotal instead of uploading the file.

Result:

```
0 / 70 detections
```

This was reassuring, but it was only one part of the investigation.

VirusTotal does not know my laptop. It compares the hash I searched against hashes already in its database.

## Full investigation context

For WUDFHost.exe I already had:

- expected System32 path
- valid Microsoft signature
- sensible parent process
- normal-looking command line
- 0/70 VirusTotal detections

All of those indicators together supported a low-priority / likely-benign conclusion.

## Important lesson

A result such as 0/70 does not automatically prove a file is safe.

For example:

```
random.exe
Temp/AppData path
unsigned
launched by Word
external connection
starts every logon
VirusTotal 0/70
```

would still deserve investigation.

## Investigation flow

For a suspicious file or process:

```
Why am I investigating it?
-> What is the process/file?
-> Path
-> Parent process
-> Signature
-> Command line
-> Behaviour
-> Network connections
-> Persistence
-> SHA256 hash
-> Reputation
-> Overall decision
```

Hashes are useful when a file is involved, but they are not needed for every type of investigation.

## What I want to remember

- Get-FileHash calculates a file hash
- SHA256 is commonly used for file identification
- VirusTotal can look up a hash without accessing my computer
- 0 detections is reassuring, not absolute proof
- Hash reputation is supporting evidence
- Path + signature + parent + behaviour + network + persistence + reputation gives a much stronger conclusion
