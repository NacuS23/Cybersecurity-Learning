# Windows port and digital signature investigation

**Date:** 18 September 2026  
**Type:** Guided hands-on practice on my own Windows computer  
**Focus:** Networking fundamentals and introductory SOC investigation

## Objective

Identify the program behind a listening port, inspect its file location and digital signature, and distinguish observations from conclusions.

## What I did

1. Used `tasklist` to identify a process by its PID.
2. Filtered `netstat -ano` output for the same PID to connect the program to its network endpoints.
3. Identified a TCP listener on port 2968 and UDP endpoints using the same port.
4. Opened the process's file location through Task Manager.
5. Opened the executable's Properties → Digital Signatures → Details and checked its signer and verification status.

Commands used, with the session-specific PID replaced by a placeholder:

```cmd
tasklist /FI "PID eq <PID>"
netstat -ano | findstr "<PID>"
```

Replace `<PID>` with the actual process ID. Check the final PID column because `findstr` matches text anywhere in the row.

## Evidence recorded

| Check | Observation |
|---|---|
| Executable | `EEventManager.exe` |
| TCP local endpoint | `0.0.0.0:2968` |
| TCP state | `LISTENING` |
| UDP endpoints | Two rows using the local IPv4 address and port 2968 |
| File location | `C:\Program Files (x86)\Epson Software\Event Manager` |
| Signer | `SEIKO EPSON CORPORATION` |
| Signature status | Windows reported that the digital signature was OK |

The local IP address, account name and session-specific PID are omitted from this public write-up. This is a summary of observations, not a full forensic capture.

## What I learned

- `LISTENING` means waiting for incoming TCP connections; it does not mean someone is already connected.
- `0.0.0.0` as a listening local address means all local IPv4 addresses. It does not by itself prove internet accessibility; firewall and network configuration matter.
- UDP does not use TCP's `LISTENING` and `ESTABLISHED` states.
- An unfamiliar port or executable name is not enough to classify a program as malware.
- A digital signature is verified cryptographically by Windows. Editing the protected code would normally invalidate the signature; copying the publisher's name or signature is not enough to forge a valid signature for different code.
- A valid signature supports publisher identity and integrity of the signed code. It does not guarantee harmless behaviour or prove that the whole computer is clean.
- Stolen signing keys or abuse of legitimate signed software are reasons to consider behaviour alongside signatures.

## Assessment and limits

The observed folder and valid Epson signature support a legitimate Epson software explanation. I found no clear malicious indicator in the limited evidence checked. This was a basic investigation, not a definitive malware verdict or a complete system security assessment.

## Follow-up work — not yet verified

We discussed these checks, but no completed results were recorded in this session:

- Scan the Epson folder with Windows Security.
- Calculate a SHA256 hash and search for an existing VirusTotal report.
- Investigate remote connections and child processes if further evidence warrants it.

## Why this matters for SOC work

This exercise practised connecting a network endpoint to a process, gathering supporting evidence, and writing a cautious conclusion with clear limitations.

## References

- [Microsoft: Authenticode digital signatures](https://learn.microsoft.com/en-us/windows-hardware/drivers/install/authenticode)
- [Microsoft: Get-FileHash](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.utility/get-filehash)
- [VirusTotal: Searching](https://docs.virustotal.com/docs/searching)
