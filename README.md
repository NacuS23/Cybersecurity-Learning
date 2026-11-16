# Cybersecurity & SOC Analyst Portfolio

**Based in the UK · Target role: Junior SOC Analyst / Security Operations Centre Analyst · [GitHub profile](https://github.com/NacuS23)**

Practical security investigations focused on Windows endpoints, authentication logs, network analysis and incident triage. My work combines read-only investigations on a Windows computer with clearly labelled simulated SOC cases.

## Selected investigations

| Case study | Evidence type | Skills demonstrated |
| --- | --- | --- |
| [Windows authentication logs](02-endpoint-investigation/day-48-windows-authentication-log-investigation/README.md) | Windows event data | Logon types, 4624/4625, session context |
| [Defender and PowerShell event timeline](02-endpoint-investigation/day-47-windows-event-correlation-timeline/README.md) | Windows event data | Event correlation, timing, evidence limitations |
| [Administrator account review](02-endpoint-investigation/day-50-windows-account-and-admin-membership/README.md) | Windows account checks | Local privilege review, account status, 4720/4732 |
| [Service installation investigation](02-endpoint-investigation/day-52-windows-service-installation-investigation/README.md) | Windows System Event 7045 and executable signatures | Service persistence, publisher validation, SOC triage |
| [Authentication alert investigation with KQL](02-endpoint-investigation/day-53-first-siem-investigation-kql/README.md) | Simulated sign-ins | Failure-to-success patterns, KQL filtering |
| [Password-spraying analysis](02-endpoint-investigation/day-54-kql-password-spraying-triage/README.md) | Simulated aggregated sign-ins | `summarize`, `count()`, `dcount()`, account correlation |
| [Windows Security event investigation](practical-labs/2026-09-20-windows-security-event-log-investigation/README.md) | Windows event data | Authentication, privilege context, event correlation |

## Current technical project

### [Windows SIEM and Custom Detection Home Lab](projects/windows-siem-detection-lab/README.md)

**Status: Planned — not yet deployed.** The goal is to set up a free, open-source SIEM using Wazuh, ingest Windows events, investigate authentication activity, create and test an original alert rule, and document the results. No real SIEM ingestion or rule execution is claimed yet.

Next, I plan to practise KQL in Microsoft's free public Azure Data Explorer sample environment before moving to production-style security datasets. This will be query practice, **not** a claim of access to a live Microsoft Sentinel workspace.

## Technical skills

**Windows and endpoint investigation:** PowerShell, `Get-WinEvent`, `Get-Process`, `Get-NetTCPConnection`, Windows Defender, Authenticode signatures, service and scheduled-task analysis.

**Network security:** DNS, ARP, TCP/IP, TLS, firewalls, process-to-connection correlation, packet interpretation.

**SOC methods:** Authentication log triage, event timelines, suspicious process investigation, persistence mechanisms, evidence-based reporting, and introductory KQL.

## Evidence and lab status

The [Practical Lab Register](practical-labs/README.md) records **23 dated exercises**: **21 completed**, **one pending evidence**, and **one partial** (audit: 16 November 2026).

Open work:
- [TCP ports and handshake](practical-labs/2026-09-22-tcp-ports-handshake/README.md): actual port numbers and correlated process evidence remain pending.
- [Npcap scheduled-task investigation](practical-labs/2026-11-10-npcap-watchdog-scheduled-task-triage/README.md): task trigger, script contents and execution history remain unverified.

Completing an exercise means completing its stated scope, **not** proving that an entire system is secure. Simulated case studies and collected endpoint evidence are clearly distinguished.

## Repository sections

| Area | Contents |
| --- | --- |
| [Networking fundamentals](01-networking-fundamentals/) | DNS, ARP, TCP/UDP, firewalls, TLS and connection troubleshooting |
| [Windows endpoint investigations](02-endpoint-investigation/) | Processes, services, event logs, persistence, Defender and KQL exercises |
| [Practical lab register](practical-labs/README.md) | Date-organised exercises, evidence types and completion statuses |
| [SIEM home lab project](projects/windows-siem-detection-lab/README.md) | Proposed architecture, checklist and untested detection use case |
| [TryHackMe study record](tryhackme/README.md) | Selected completed beginner learning; platform use is optional |
| [Learning journal](notes/learning-journal.md) | Archived chronological learning notes |

## Professional development

My next priority is independently querying real data in a safe lab, deploying a SIEM and validating one detection rule. **CompTIA Security+** is a possible future certification goal; no professional cybersecurity certification is claimed as completed. I am prioritising practical evidence before deciding whether to purchase an exam or subscription.

---

*Learning portfolio for entry-level SOC work. Case studies are training investigations and are not representations of paid SOC employment.*
