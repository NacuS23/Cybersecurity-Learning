# Suspicious connection triage practice

**Date:** 19 September 2026  
**Type:** Fictional SOC investigation exercise  
**Focus:** Prioritising suspicious network activity and explaining what evidence to collect next

## Objective

Review three fictional Windows network connections, decide which one deserves investigation first, and explain the decision using multiple pieces of evidence rather than relying on a process name or port alone.

## Scenario

Three established TCP connections were presented for review:

| Evidence | Connection A | Connection B | Connection C |
|---|---|---|---|
| Program | `msedge.exe` | `msedge.exe` | `backup-agent.exe` |
| Location | `C:\Program Files (x86)\Microsoft\Edge\Application\` | `C:\Users\[user]\AppData\Local\Temp\` | `C:\Program Files\CompanyBackup\` |
| Signature | Valid Microsoft signature | No digital signature | Valid backup vendor signature |
| Remote endpoint | `192.0.2.10:443` | `198.51.100.20:443` | `203.0.113.30:443` |
| State | `ESTABLISHED` | `ESTABLISHED` | `ESTABLISHED` |
| Observed behaviour | Connections while browsing | Reconnects every minute after Edge is closed | Transfers data during a scheduled backup |

The IP addresses used in this exercise are reserved documentation addresses and do not represent real systems.

## Investigation decision

### Connection I would investigate first

**Connection B**

### Two reasons

1. The process is named `msedge.exe`, but it is running from `C:\Users\[user]\AppData\Local\Temp\` instead of the normal Microsoft Edge installation directory. A legitimate-looking process name by itself is weak evidence because malware can imitate common program names.
2. The process has no digital signature and reconnects every minute even after Edge has been closed. That behaviour is unusual for a normal browser process and makes the connection more suspicious.

## One extra piece of evidence I would collect

I would inspect the executable further by:

- confirming its full file path,
- calculating its SHA-256 hash,
- checking the hash with VirusTotal,
- checking which parent process launched it,
- and checking whether it has any persistence mechanism such as a startup entry or scheduled task.

These checks would help determine whether the process is legitimate software, unwanted software, or potentially malicious.

## Why I cannot yet say it is definitely malware

The evidence is suspicious, but it is not proof by itself.

A legitimate application could be unsigned, could temporarily run from an unusual directory, or could make repeated network connections. I would need additional evidence before classifying the file as malware.

## Quick checks

### 1. Would port 80 instead of port 443 change the conclusion by itself?

No.

Port 80 commonly carries HTTP and port 443 commonly carries HTTPS, but either legitimate software or malware can use either port. The port number alone is not enough to determine whether the connection is safe.

The process location, signature status, repeated reconnections and overall behaviour are more useful when considered together.

### 2. Would a valid digital signature be enough to stop investigating suspicious behaviour?

No.

A valid signature is useful evidence because it can help confirm the publisher and whether the signed file has been modified. However, it does not guarantee that the behaviour is safe.

Legitimate signed software can be abused, compromised, or used in unexpected ways. Suspicious behaviour should still be investigated even when the executable has a valid signature.

## What I learned

- Port 443 does not automatically mean a connection is safe.
- `ESTABLISHED` only means that a TCP connection currently exists.
- A familiar process name is not enough to trust a process.
- File location is an important part of process investigation.
- Digital signatures are useful evidence, but they are not a complete malware verdict.
- Repeated or unexpected behaviour can increase the priority of an alert.
- Several weak indicators can become more meaningful when they point in the same direction.
- A SOC analyst should explain both why something looks suspicious and why the available evidence is not yet enough for a definitive conclusion.

## SOC-style assessment

Connection B is the highest-priority connection to investigate because several observations are unusual at the same time: the executable is running from a temporary user directory, it has no digital signature, and it continues reconnecting after the legitimate browser is closed.

Connections A and C have behaviour that better matches their described purpose, but they should still be assessed in context if other alerts or evidence appear.

This exercise practised prioritisation rather than proving that any connection was malicious.

## Why this matters for SOC work

SOC analysts regularly receive more alerts than they can investigate at once. They need to identify which activity deserves attention first and explain the decision using evidence.

This exercise practised separating observations from conclusions and avoiding decisions based on only one indicator such as a port number, process name, or digital signature.

## Answer review — 22 September 2026

After the worked example above, I submitted my own answers and reviewed them with guidance:

- I chose Connection B because it lacked a digital signature and reconnected every minute after Edge was closed.
- I identified the Temp folder as another concern and said it was worth investigating rather than immediately calling it malicious.
- Feedback clarified that a file stored in Temp is not necessarily a temporary file. Its location was already supplied, so genuinely new evidence could be a hash reputation result or the parent process. Those were suggested checks, not checks performed on a real executable in this fictional exercise.
- I initially thought port 80 alone would make B more suspicious. The correction was that HTTP is commonly unencrypted, but encryption and maliciousness are different questions: either port 80 or 443 can carry legitimate or malicious traffic.
- I correctly said a valid signature would not be enough to stop investigating the unusual location and behaviour.

<details>
<summary>Core memory — judging suspicious connections</summary>

Use the program, file location, signature, destination and behaviour together. A port number or valid signature alone cannot establish safety. Record what is observed, what is inferred, and which additional evidence is needed.

</details>
