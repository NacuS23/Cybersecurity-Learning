# Day 24 - Windows Security event log investigation

Today I investigated a real Windows failed logon event and followed the evidence to the local process involved.

## Event found

Event ID 4625 was recorded on 24/09/2026 at 19:35:59.

Key details:
- Logon Type: 2
- Failure reason: Unknown user name or bad password
- Status: 0xC000006D
- Sub Status: 0xC000006A
- Caller process: Microsoft Edge WebView
- Source Network Address: blank
- Source Port: blank

## Investigation

I checked the surrounding ten-minute window and found only one failed logon event.

I then checked the running Edge WebView processes with PowerShell:

```powershell
Get-CimInstance Win32_Process -Filter "Name='msedgewebview2.exe'" |
Select-Object ProcessId, ParentProcessId, ExecutablePath, CommandLine
```

The current executable path was:

```
C:\Program Files (x86)\Microsoft\EdgeWebView\Application\154.0.4258.53\msedgewebview2.exe
```

I verified its digital signature:

```powershell
Get-AuthenticodeSignature "C:\Program Files (x86)\Microsoft\EdgeWebView\Application\154.0.4258.53\msedgewebview2.exe" |
Format-List Status,StatusMessage,SignerCertificate
```

Result:
- Status: Valid
- Signature verified
- Signer: Microsoft Corporation

## Conclusion

This looked low priority / likely benign because it was a single failed local logon, there was no remote source IP, the caller process was in the expected Microsoft Edge WebView path, and the file had a valid Microsoft signature.

## Investigation checklist

For logon events I should check:

Event ID -> Account -> Logon Type -> Source IP -> Failure reason -> Caller process -> Frequency

If anything still looks suspicious, I can go deeper into path, signature, parent process, command line and related events.

## Memory

- 4624 = successful logon
- 4625 = failed logon
- 4688 = process creation
- Logon Type 2 = local / interactive
- Logon Type 3 = network
- Logon Type 10 = remote interactive / RDP
- One event is different from a repeated pattern
- A valid signature is useful evidence, but it should be considered together with path and behaviour
