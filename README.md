# Cybersecurity & SOC Analyst Learning Portfolio

Practical cybersecurity studies focused on **network troubleshooting, Windows endpoint investigation, authentication logs, incident triage and SIEM analysis**.

This repository documents the path towards an entry-level Security Operations Centre (SOC) analyst role. It contains investigations conducted on a Windows workstation, exercises using supplied security data, and concise write-ups that separate **observed evidence**, **interpretation**, and **remaining uncertainty**.

**Current learning milestone:** 54 of 120 lessons completed (45%) as of 16 November 2026. The latest exercise covers KQL aggregation and password-spraying triage. This tracks study sessions, not professional experience or a job-readiness score.

## Selected investigations

| Investigation | Evidence | SOC skills |
| --- | --- | --- |
| [Windows authentication log investigation](02-endpoint-investigation/day-48-windows-authentication-log-investigation/README.md) | Live Windows Security event data | Logon types, 4624/4625, session context |
| [Defender and PowerShell event timeline](02-endpoint-investigation/day-47-windows-event-correlation-timeline/README.md) | Live Windows event records | Timeline correlation, evidence limits, settings changes |
| [Windows account and administrator membership](02-endpoint-investigation/day-50-windows-account-and-admin-membership/README.md) | Live Windows account checks | Access review, Events 4720/4732, account status |
| [Service installation and signature validation](02-endpoint-investigation/day-52-windows-service-installation-investigation/README.md) | Live System Event 7045 and Authenticode results | Service persistence, publisher checks, low-confidence indicators |
| [First SIEM authentication investigation](02-endpoint-investigation/day-53-first-siem-investigation-kql/README.md) | Simulated sign-in dataset | KQL fundamentals, failure-to-success patterns, alert triage |
| [KQL password-spraying investigation](02-endpoint-investigation/day-54-kql-password-spraying-triage/README.md) | Simulated aggregated sign-in data | `summarize`, `count()`, `dcount()`, success correlation |
| [Windows Security Event Log practice](practical-labs/2026-09-20-windows-security-event-log-investigation/README.md) | Live Windows event data | 4624/4625/4672/4688, event correlation |

## Browse the repository

| Section | What's inside |
| --- | --- |
| [Networking fundamentals](01-networking-fundamentals/) | Days 1–18: DNS, ARP, TCP/UDP, TLS, firewalls and connections |
| [Windows endpoint and security investigations](02-endpoint-investigation/) | Days 19–54: processes, services, scheduled tasks, Defender, log analysis and introductory KQL |
| [Practical labs — status register](practical-labs/README.md) | Date-organised labs with evidence type, completion status and outstanding checks |
| [TryHackMe](tryhackme/README.md) | Completed modules and self-study progress |
| [Detailed learning journal](notes/learning-journal.md) | Archived study notes; separate from the curated case studies |

## Practical lab status

The [lab register](practical-labs/README.md) includes **23 dated exercises**: **21 completed**, **one pending evidence**, and **one partial** (status audit: 16 November 2026).

The two open items are:
- [TCP ports and handshake](practical-labs/2026-09-22-tcp-ports-handshake/README.md) — pending actual local/remote port values and matching process evidence.
- [Npcap scheduled task](practical-labs/2026-11-10-npcap-watchdog-scheduled-task-triage/README.md) — partial; task trigger, batch-file contents and execution history have not yet been verified.

No missing observations are represented as completed checks.

## Tools and methods

**Windows / endpoint:** PowerShell, Get-WinEvent, Get-Process, Get-NetTCPConnection, Event Viewer, Windows Defender, Authenticode signatures and file hashes.

**Network / security concepts:** DNS, TCP/IP, ports, TLS, firewall outcomes, process attribution, persistence and MITRE ATT&CK.

**SIEM:** Introductory Microsoft Sentinel KQL exercises using simulated sign-in records. Live Sentinel query execution has **not** been claimed.

## Documentation approach

Each report aims to show the question under investigation, relevant commands or supplied evidence, the findings, what the findings **do not** prove, and the next appropriate SOC action. Fictional exercises are labelled as simulations; Windows observations are attributed to the workstation where checked.

---

*Learning portfolio — not an assertion of professional incident-response employment or production SOC access.*
