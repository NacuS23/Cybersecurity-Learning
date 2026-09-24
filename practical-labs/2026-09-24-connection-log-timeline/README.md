# Connection logs and timeline practice

**Completed and reviewed:** 24 September 2026  
**Exercise introduced:** 23 September 2026  
**Type:** Fictional log-analysis exercise with guided answer review

## What I practised

I read a small set of connection records, identified repeated attempts, separated IP addresses from ports, and built a factual timeline. This write-up contains the final correct answers after review.

## The fictional test

All records represent TCP connection attempts from the same example computer, `192.168.1.50`. Destination addresses are reserved documentation addresses. These are supplied sample records, not logs captured from my computer or a real incident.

For this exercise, the source initiates each attempt. `ALLOW` and `BLOCK` describe the firewall decision, not whether the connection or data transfer succeeded.

| Time | Program | Source port | Destination IP | Destination port | Action |
|---|---|---:|---|---:|---|
| 09:00:00 | `msedge.exe` | 52110 | `192.0.2.10` | 443 | ALLOW |
| 09:00:02 | `msedge.exe` | 52111 | `192.0.2.10` | 443 | ALLOW |
| 09:01:00 | `update-check.exe` | 53001 | `198.51.100.20` | 443 | BLOCK |
| 09:02:00 | `update-check.exe` | 53012 | `198.51.100.20` | 443 | BLOCK |
| 09:03:00 | `update-check.exe` | 53025 | `198.51.100.20` | 443 | BLOCK |
| 09:04:00 | `update-check.exe` | 53038 | `198.51.100.20` | 443 | ALLOW |

## My results

| Question | Correct answer |
|---|---|
| Program with repeated attempts | `update-check.exe` |
| Destination IP | `198.51.100.20` |
| Destination port | `443` |
| Number of blocked attempts from this program | 3 |
| Interval between consecutive attempts | 1 minute (`00:01:00`) |
| Time the recorded firewall decision changed | `09:04:00` |
| One source port from this program | `53038` |
| Did the source port stay the same? | No: 53001, 53012, 53025 and 53038 |

## Final timeline after review

Between 09:01 and 09:03, `update-check.exe` made three blocked TCP connection attempts to `198.51.100.20:443`, one minute apart. At 09:04, another attempt to the same destination was allowed, using source port 53038.

## Additional evidence to collect

I would check which firewall rule matched each attempt and any relevant rule-change logs. This could help explain why the recorded decision changed. The source ports are already in the table; collecting them again would not explain the change. A different decision alone does not prove that someone changed a rule.

This is a proposed investigation step; no additional rule logs were supplied or inspected.

## Questions and final correct answers

**1. Does the final ALLOW prove that data was successfully sent?**

No. It shows that the firewall permitted the attempt. The server might not respond, and the connection or application data transfer could still fail.

**2. Would a new source port necessarily mean a different program started?**

No. The same program can use different temporary source ports for separate connections.

**3. Give one legitimate explanation for repeated connection attempts.**

An automatic updater could retry every minute because it cannot reach its update server. This is a possible explanation, not something proved by these records.

**4. The firewall allows a connection attempt, but the destination server is offline. Can the log still say ALLOW?**

Yes. The firewall can permit an attempt even when the destination never responds. I confirmed this in the final knowledge check.

## Conclusion

I identified the repeated pattern and the change in firewall decisions. The records do not establish whether the program is legitimate or malicious, why the decision changed, or whether data was successfully transferred. Those questions need additional evidence.

<details>
<summary>Core memory — firewall decisions and connection evidence</summary>

- A firewall decision, a successful TCP connection and successful application data transfer are different things.
- `ALLOW` means permission at that firewall; it does not guarantee delivery or safety.
- Changing source ports can belong to the same program.
- Repeated attempts can have legitimate explanations, including retries after a failure.
- A useful timeline states what happened and when, using the evidence available.
- Separate observed facts, possible explanations and proposed checks.

</details>
