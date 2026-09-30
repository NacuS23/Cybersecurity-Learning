# TCP connection outcome analysis

**Date:** 30 September 2026  
**Type:** SOC network analysis practice  
**Focus:** Distinguishing firewall decisions, TCP connectivity, TLS negotiation and application responses

## Objective

Analyse firewall, TCP, TLS and application-layer evidence to determine whether a connection was merely allowed, whether the TCP three-way handshake completed, and whether an application-level response was received.

## Scenario

### Case A

- Firewall decision: `ALLOW`
- Destination: `192.0.2.10:443`
- Traffic observed: SYN packets and retransmissions
- Result: timeout
- No packets returned from the destination

### Case B

- Firewall decision: `ALLOW`
- Destination: `198.51.100.20:443`
- Traffic observed: `SYN → SYN-ACK → ACK`
- TLS handshake completed
- Server returned `HTTP 503`

The IP addresses used here are reserved documentation addresses and do not represent real systems.

## Analysis

### Case A

**Connection allowed by firewall:** Yes  
**TCP connection succeeded:** No evidence that it did  
**Application response received:** No

The firewall permitted the outbound attempt, but only SYN packets and retransmissions were observed. No SYN-ACK or other reply was received, so the TCP three-way handshake did not complete.

A possible explanation is that the destination host was offline, unreachable, filtered somewhere beyond the local firewall, or not listening on the target port.

An extra check would be to review routing, test reachability where appropriate, compare with another known-good destination, or inspect additional packet-capture evidence.

### Case B

**Connection allowed by firewall:** Yes  
**TCP connection succeeded:** Yes  
**Application response received:** Yes

The sequence `SYN → SYN-ACK → ACK` shows that the TCP three-way handshake completed.

The completed TLS handshake shows that encrypted session negotiation also succeeded.

The `HTTP 503` response proves that an application-layer response was received. A 503 response means the server was reachable and responded, even though the requested service was unavailable.

## Key distinction

A firewall decision of `ALLOW` does not prove that the remote host responded.

These are separate stages:

1. Firewall permits the traffic.
2. TCP handshake succeeds or fails.
3. TLS may negotiate successfully.
4. The application may or may not return a response.

Each stage provides different evidence.

## Does either case prove malicious activity?

No.

Case A shows a failed connection attempt, while Case B shows a successful network and application exchange. Neither case alone is enough to classify the activity as malicious.

Additional context would be required, such as the process responsible, destination reputation, frequency of connections, user activity, file reputation and surrounding endpoint evidence.

## IP address and port parsing

For:

```text
192.168.1.50:53120
```

- IP address: `192.168.1.50`
- Port: `53120`

## What I learned

- `ALLOW` in a firewall log means the firewall permitted the traffic; it does not prove connection success.
- A successful TCP connection requires the three-way handshake.
- SYN retransmissions without a reply are evidence that a connection attempt did not complete.
- TLS success is a separate stage after TCP connectivity.
- An HTTP response confirms application-layer communication.
- A server error such as HTTP 503 still proves the server responded.
- Network evidence should be interpreted in layers rather than as one single success/failure result.
- Connection success by itself does not prove legitimate or malicious activity.

## SOC relevance

This scenario practised reading network evidence in the correct order and avoiding a common analyst mistake: treating a firewall allow event as proof that a full connection succeeded.
