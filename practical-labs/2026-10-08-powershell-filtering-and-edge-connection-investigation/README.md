# PowerShell filtering and Edge connection investigation

**Date:** 8 October 2026  
**Type:** Hands-on SOC practice  
**Focus:** PowerShell filtering, TCP connection analysis, process identification, signature verification and destination context

## Objective

Use PowerShell to collect TCP connections, filter them with `Where-Object`, identify the process behind an established connection, verify the executable, and investigate remote destinations using DNS evidence.

## PowerShell filtering

I first collected a snapshot of TCP connections:

```powershell
$connections = Get-NetTCPConnection
```

I then filtered the saved connections by state.

Example for listening connections:

```powershell
$connections |
Where-Object { $_.State -eq 'Listen' } |
Select-Object -First 5 LocalAddress, LocalPort, State, OwningProcess |
Format-Table -AutoSize
```

Example for established connections:

```powershell
$connections |
Where-Object { $_.State -eq 'Established' } |
Select-Object -First 3 LocalAddress, LocalPort, State, OwningProcess |
Format-Table -AutoSize
```

### PowerShell concepts practised

- `$_` means the current object being examined inside the pipeline.
- `Where-Object` keeps only records that match a condition.
- `Select-Object` chooses the fields/columns to display.
- `Format-Table` controls how the final output is displayed.

Useful mental model:

```text
collect -> filter -> select -> display
```

## Mapping a connection to a process

One established connection was owned by a process ID that mapped to:

```text
Process: msedge.exe
Path: C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe
```

I checked the process with:

```powershell
Get-Process -Id <PID> | Select-Object Id, ProcessName, Path
```

The executable path was consistent with a normal Microsoft Edge installation.

## Digital signature verification

I then checked the executable signature:

```powershell
Get-AuthenticodeSignature "C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe" |
Format-List Status, SignerCertificate
```

Observed result:

- Signature status: **Valid**
- Signer: **Microsoft Corporation**

This was strong supporting evidence that the executable itself was legitimate, but it did not automatically prove every network connection made by the browser was safe.

## Investigating remote connections

I listed the TCP connections owned by the Edge process:

```powershell
Get-NetTCPConnection -OwningProcess <PID> |
Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State |
Format-Table -AutoSize
```

The established connections used remote port `443`, consistent with HTTPS traffic.

The local private address is generalized in this public write-up.

## Reverse DNS

I tested remote addresses with:

```powershell
Resolve-DnsName <REMOTE_IP>
```

One remote address returned a GitHub reverse-DNS hostname.

Other remote addresses returned no PTR record.

A missing reverse-DNS record was treated as a lack of hostname information, not as evidence of malicious activity.

## DNS cache investigation

I tried to correlate a remote IP with the Windows DNS cache:

```powershell
Get-DnsClientCache |
Where-Object { $_.Data -eq '<REMOTE_IP>' } |
Select-Object Entry, RecordName, Data, TimeToLive |
Format-Table -AutoSize
```

No matching cached hostname was found for one investigated remote IP.

I then created a controlled DNS example:

```powershell
Resolve-DnsName github.com
```

Windows returned an IPv4 address for `github.com`.

Immediately afterwards, I checked the DNS cache:

```powershell
Get-DnsClientCache |
Where-Object { $_.Entry -like "*github*" -or $_.RecordName -like "*github*" } |
Format-Table Entry, RecordName, Data, TimeToLive -AutoSize
```

This showed the same hostname-to-IP relationship in the Windows DNS cache.

## What I learned

- `Where-Object` filters records; `Select-Object` selects fields.
- `$_` represents the current object being evaluated in a pipeline.
- `Established` means a TCP connection exists; it does not mean the connection is harmless.
- A local `192.168.x.x` address is a private LAN address.
- The remote address is the destination the process is connected to.
- Port `443` normally indicates HTTPS, but HTTPS is not automatically safe.
- A valid process path and valid Microsoft signature strongly support the legitimacy of the Edge executable.
- A legitimate browser can still connect to an unsafe destination, so process legitimacy and destination safety are separate questions.
- Reverse DNS may return a hostname, but the absence of PTR data is not automatically suspicious.
- Shared cloud/CDN infrastructure means an IP owner does not necessarily identify the exact website behind a connection.
- DNS cache data can help correlate domains and IPs, but it may be temporary or absent.
- Large services can legitimately use different IP addresses over time and across regions.

## SOC investigation flow

A practical workflow from this exercise:

```text
TCP connection
-> filter interesting state
-> identify PID
-> map PID to process
-> check executable path
-> verify digital signature
-> inspect remote IP and port
-> check DNS / reverse DNS / cache
-> combine all evidence before deciding
```

## Privacy

Private LAN addresses, process IDs and other session-specific values are generalized or omitted from this public write-up.

## SOC relevance

This exercise practised narrowing a large set of network records with PowerShell and then moving from a connection to the process and destination evidence behind it. The main lesson was to avoid treating any single clue—port, IP owner, process name, signature or DNS result—as a final verdict.
