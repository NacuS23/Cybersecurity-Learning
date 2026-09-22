# Client ports, server ports and the TCP handshake

**Date:** 22 September 2026  
**Type:** Guided Windows networking practice  
**Status:** Answers reviewed; observed port numbers still to be confirmed

## Objective

Distinguish IP addresses from port numbers, identify the process associated with a TCP connection, and explain the TCP handshake and the limits of port-based security judgments.

## Exercise workflow

The instructions used `Test-NetConnection example.com -Port 443`, `curl.exe https://example.com`, and the following connection inspection command:

```powershell
Get-NetTCPConnection -RemotePort 443 -ErrorAction SilentlyContinue |
Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State, OwningProcess |
Format-Table
```

The process lookup used:

```cmd
tasklist /FI "PID eq <PID>"
```

Replace `<PID>` with the observed process ID. For a process lookup, choose a live connection with a nonzero owning PID; a closed connection in `TimeWait` may no longer have an identifiable owner. This filter can show connections from other applications, not just the test request.

## My reported observations

| Field | Reported result |
|---|---|
| Local address | A private IPv4 address; omitted from this public note |
| Remote address | An IPv4 address; omitted from this public note |
| TCP state | `Established` |
| Process name from tasklist | `ms-teams.exe` |
| Local port | Not supplied; still to be confirmed |
| Remote port | Not supplied; still to be confirmed |

The session-specific PID and account details are omitted. The reported process was Teams, so this observation is not evidence that the row belonged to `curl.exe` or `example.com`. The full connection row and connectivity-test result were not supplied. The process name alone does not establish safety.

## My answers and feedback

1. **Who normally sends the first SYN?** I answered: the side that wants to start the connection. Correct: the initiator, usually called the client.
2. **Handshake order:** I answered `SYN → SYN-ACK → ACK`. Correct.
3. **High local client port:** I answered temporary. Correct for the normal client connection described in this exercise; a high port alone does not prove the process's role.
4. **Does port 443 prove safety?** I answered no. Feedback clarified the reason: malware can also communicate over HTTPS, so encrypted traffic can still be malicious.

## Correction and remaining detail

I initially supplied IP addresses where the template requested port numbers. An IP identifies a network address; the port identifies the relevant transport endpoint on that address. I still need to record the actual `LocalPort` and `RemotePort` values. The example port shown during feedback was illustrative and is not recorded as my observation.

## Why this matters for SOC work

Accurate endpoint and process identification helps analysts interpret a connection without confusing addresses, ports or unrelated application traffic. A connection snapshot does not capture the handshake packets or, by itself, prove which side initiated a connection.

<details>
<summary>Core memory — TCP connections</summary>

- Normal TCP handshake: **SYN → SYN-ACK → ACK**.
- The client normally initiates and uses a temporary local port when connecting to a server's service port.
- `Established` means a TCP connection exists; it is not a security verdict.
- IP address and port are separate fields. Record both accurately when investigating.
- Port 443 commonly carries HTTPS. Encryption does not guarantee benign activity.
- A PID connects a live network observation to a running process. PIDs can change or be reused, so correlate observations close together in time.

</details>
