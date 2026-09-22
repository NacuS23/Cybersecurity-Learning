# ARP and DNS practice review

**Results reported:** 22 September 2026  
**Type:** Guided Windows networking exercise on my own computer

## Objective and procedure

Distinguish DNS name resolution from ARP's local IPv4-to-MAC mapping. The exercise used `ipconfig` to identify the active gateway, `arp -a` before and after a single ping to that gateway, and `nslookup example.com` to test DNS resolution. No cache clearing or configuration changes were required.

## My reported results

| Check | Result |
|---|---|
| Gateway ARP entry before ping | Present |
| Gateway ARP entry after ping | Present |
| Gateway MAC mapping | Unchanged |
| DNS lookup | Succeeded |

These results are recorded from my answers. Actual IP/MAC addresses and raw output are omitted. I did not separately report the ping result.

## Answer review

- **Next hop:** I understood that traffic needs a next hop, but my answer did not identify whose MAC address is used. The clarification is that for an IPv4 website outside the local subnet, a typical home computer sends the local frame to its gateway's MAC address. The destination IP still identifies the remote server.
- **Encryption:** I correctly answered that ARP does not encrypt traffic. HTTPS uses TLS to protect HTTP communication.
- **Changed gateway MAC:** I correctly answered that this alone would not prove an attack. A change needs context and corroboration; legitimate router replacement or failover could also explain it.

## Assessment and limits

The gateway mapping was stable during this comparison, and the DNS lookup succeeded. These observations show the results of these particular checks; they do not prove that the entire network is secure. No ARP attack was demonstrated or detected by this exercise.

## Why this matters for SOC work

Distinguishing name resolution, local delivery and encryption helps an analyst interpret network evidence and avoid treating every address change or connection problem as an attack.

<details>
<summary>Core memory — DNS, ARP, gateway and TLS</summary>

| Component | Main role |
|---|---|
| DNS | Looks up records such as a hostname's IP address |
| ARP | Maps a local IPv4 next-hop address to a MAC address |
| Gateway | Forwards traffic toward networks outside the local subnet |
| TLS | Protects communication; HTTPS uses it for HTTP |

For a remote IPv4 website on a typical home network: the destination IP belongs to the remote server, while the first local frame normally uses the gateway's MAC address. ARP does not encrypt traffic. A changed MAC mapping is a reason to check context, not a standalone malware verdict.

</details>
