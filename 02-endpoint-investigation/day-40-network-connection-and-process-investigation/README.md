# Day 40 - Investigating network connections and owning processes

Today I examined live TCP connections on my Windows workstation, followed an owning PID to its executable and checked the executable's digital signature. I also reviewed how to interpret private/public IP addresses, ports and short-lived processes.

## What I wanted to find out

- Which program owns an established outbound connection?
- Does the destination port alone tell me whether the traffic is safe?
- Can I verify the process path and digital signature?
- What are the limitations of checking live connections after the fact?

## Practical 1 - List established TCP connections

I ran:

```powershell
Get-NetTCPConnection -State Established |
Select-Object -First 8 LocalAddress,LocalPort,RemoteAddress,RemotePort,OwningProcess |
Format-Table -AutoSize
```

I saw eight established TCP connections, all with **remote port 443**. Several belonged to the same owning PID, `13108`. The local address was in the private `172.16.0.0/12` address range.

### Interpreting the fields

| Field | Meaning |
| --- | --- |
| LocalAddress | The local interface IP used for that connection |
| LocalPort | The local TCP port |
| RemoteAddress | IP address of the remote peer |
| RemotePort | TCP port on the remote side |
| OwningProcess | PID of the owning Windows process |

A `172.20.x.x` address is private, not normally an internet-routable public IP. Under a **/24** subnet mask, the final octet would be the host portion; what each octet means depends on the actual subnet mask.

Remote IPv4 addresses starting with numbers such as `13`, `20`, `40`, `104` or `4` do not individually establish the organisation, location or safety of a destination. The full IP needs checking.

**Port 443 is commonly used for HTTPS, but remote port 443 alone does not verify that TLS is in use or that the destination is trustworthy.**

## Practical 2 - Investigating a PID from a snapshot

I tried to look up the process that owned several connections:

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId = 13108" |
Select-Object Name, ProcessId, ParentProcessId, ExecutablePath
```

**Result:** No process details were returned at the time of the query.

One possibility is that the process had already exited or restarted. Live connections and their processes can disappear quickly; a missing result is not evidence of malicious activity.

To collect a connection and promptly query its owning PID, I used:

```powershell
$connection = Get-NetTCPConnection -State Established |
Select-Object -First 1

$connection |
Select-Object RemoteAddress, RemotePort, OwningProcess

Get-Process -Id $connection.OwningProcess -ErrorAction SilentlyContinue |
Select-Object Id, ProcessName, Path
```

This selected one established connection, but the immediate `Get-Process` lookup did not produce process details in the output observed.

The connection showed:

```text
RemoteAddress    RemotePort  OwningProcess
162.159.128.232          443          1408
```

## Practical 3 - Identify the network connection's process

I then checked PID `1408` using CIM:

```powershell
Get-CimInstance Win32_Process -Filter "ProcessId = 1408" |
Select-Object Name, ProcessId, ParentProcessId, ExecutablePath
```

The returned details were:

```text
Name            : Discord.exe
ProcessId       : 1408
ParentProcessId : 15508
ExecutablePath  : C:\Users\<USER>\AppData\Local\Discord\app-1.0.9265\Discord.exe
```

The process name and user-local Discord installation directory were consistent with a normal installed application. The connection was to remote IP `162.159.128.232` on TCP port `443`.

I did not separately verify the owner of the destination IP or inspect the content of the connection.

## Practical 4 - Verify the executable's digital signature

I checked the executable signature with PowerShell:

```powershell
Get-AuthenticodeSignature 'C:\Users\<USER>\AppData\Local\Discord\app-1.0.9265\Discord.exe' |
Select-Object Status, @{
    Name='Signer'
    Expression={$_.SignerCertificate.Subject}
}
```

The output showed:

```text
Status : Valid
Signer : CN=Discord Inc., O=Discord Inc., ...
```

A valid signature from Discord Inc. supports the expected-application interpretation. A signed executable is **not** a guarantee that all traffic or subsequent behaviour is harmless.

## SOC investigation note - Real workstation

**Title:** Established outbound connection associated with Discord.exe.

**Priority:** Low, assuming Discord is an expected installed application.

**Evidence:**
- A live established TCP connection to `162.159.128.232:443` was associated with PID `1408`.
- PID `1408` was subsequently identified as `Discord.exe`.
- Executable path was consistent with an application installed under the user's Discord directory.
- The executable's Authenticode signature was `Valid`, signed by Discord Inc.

**Assessment:** Likely expected Discord network activity. The evidence examined showed no confirmed malicious behaviour. The remote IP's owner, actual traffic contents and complete application behaviour were not independently established.

**Decision:** Reasonable to close as expected application activity if Discord was knowingly installed and running and no related alerts or other suspicious indicators were present.

## What I want to remember

- `Get-NetTCPConnection -State Established` shows currently established TCP sessions and their owning PIDs.
- `OwningProcess` can be matched to a live process using `Get-Process` or `Get-CimInstance Win32_Process`.
- A PID can disappear or be reused. Save timestamps and inspect promptly; don't assume a later PID refers to the same process.
- `Get-AuthenticodeSignature` checks whether the file's signature validates and who signed it.
- **Port 443 does not prove a connection is safe or even confirm it is HTTPS.**
- Multiple connections from a browser or messaging app are normal and are not, on their own, suspicious.
- Investigate the combination of **process, path, signature, network destination and activity**, rather than relying on any single clue.
