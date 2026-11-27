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
| [Multi-account sign-in correlation](02-endpoint-investigation/day-55-multi-account-signin-correlation/README.md) | Simulated sign-in timeline, worked case | `countif()`, success correlation, incident triage |
| [KQL five-minute window detection](02-endpoint-investigation/day-56-kql-time-window-detection/README.md) | Reproducible synthetic KQL dataset, browser run pending | `bin()`, time windows, threshold filtering |
| [KQL verification and failure-to-success correlation](02-endpoint-investigation/day-57-browser-kql-verification/README.md) | Synthetic query files with locally checked expected results; KQL browser run pending | `count_distinct()`, `join`, query QA and risk interpretation |
| [Executed Windows logon detector](02-endpoint-investigation/day-59-windows-logon-detection-prototype/README.md) | Python code executed against 41 synthetic 4624/4625 logons; 9 passing tests | Rolling windows, login correlation, false-positive tests |
| [Windows Security log collection and validation](02-endpoint-investigation/day-60-windows-authentication-collection/README.md) | Python validator executed on nine synthetic logons; 11 passing tests, PowerShell collection pending | 4624/4625 extraction, privacy, evidence validation |
| [Real Windows logon-type investigation](02-endpoint-investigation/day-61-real-windows-logon-type-investigation/README.md) | User-executed Windows Security event data, 68 grouped successful logons | 4624/4625 triage, type 5/7/11/2, evidence limits |
| [Privileged logon correlation](02-endpoint-investigation/day-62-privileged-logon-correlation/README.md) | User-executed real Windows Security queries: 77 matching 4672 events, 68 service-type | Matching 4624/4672 by Logon ID and host; evidence limits |
| [Sensitive privilege-list triage](02-endpoint-investigation/day-63-windows-privilege-list-triage/README.md) | User-executed 4672 Security-log query: 12 events, 12 privilege names, 135 appearances | Privilege assignment vs. use, risk context, privacy-aware reporting |
| [Windows 4672 account-category ambiguity lab](02-endpoint-investigation/day-64-4672-account-category-hypotheses/README.md) | Two simulated 4672 datasets with identical privilege totals; 12 executed Python tests | Well-known SIDs, account triage, privacy-safe validation |
| [KQL detection unit tests and false-positive controls](02-endpoint-investigation/day-58-kql-detection-unit-tests/README.md) | 24 synthetic sign-ins; independently checked expected outputs, real KQL run pending | `toscalar()`, `materialize()`, joins, positive/negative testing |
| [Windows Security event investigation](practical-labs/2026-09-20-windows-security-event-log-investigation/README.md) | Windows event data | Authentication, privilege context, event correlation |

## Current technical project

The [Day 61 real-Windows logon review](02-endpoint-investigation/day-61-real-windows-logon-type-investigation/README.md), [Day 62 privileged-logon correlation](02-endpoint-investigation/day-62-privileged-logon-correlation/README.md), and [Day 63 privilege-list analysis](02-endpoint-investigation/day-63-windows-privilege-list-triage/README.md) document read-only, user-executed Security log queries. [Day 64](02-endpoint-investigation/day-64-4672-account-category-hypotheses/README.md) adds an **executed synthetic-data test** showing that identical privilege counts can belong to very different account categories; the real account-category check remains pending. Day 62 correlated **77 Event 4672 records with nearby successful 4624 events**, mainly service logons (68). Only aggregated results were shared; these are genuine endpoint observations, not synthetic SIEM results or evidence of compromise.

The [Day 59 detection prototype](02-endpoint-investigation/day-59-windows-logon-detection-prototype/README.md) and [Day 60 collector/validator](02-endpoint-investigation/day-60-windows-authentication-collection/README.md) have executed Python tests on synthetic data. Day 60's Windows PowerShell collector is supplied for authorised local use, **not yet run on a real PC**. Neither lesson is a deployed SIEM or production detection. The planned Wazuh lab remains the next infrastructure milestone.

### [Windows SIEM and Custom Detection Home Lab](projects/windows-siem-detection-lab/README.md)

**Status: Planned — not yet deployed.** The goal is to set up a free, open-source SIEM using Wazuh, ingest Windows events, investigate authentication activity, create and test an original alert rule, and document the results. No real SIEM ingestion or rule execution is claimed yet.

Reproducible [KQL time-window](02-endpoint-investigation/day-56-kql-time-window-detection/README.md) and [failure-to-success correlation](02-endpoint-investigation/day-57-browser-kql-verification/README.md) exercises are prepared for independent execution in Microsoft's free public Azure Data Explorer environment. Expected results were checked locally, but the **real KQL browser runs remain pending**; these are not production Sentinel investigations.

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
