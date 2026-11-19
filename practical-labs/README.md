# Practical SOC Labs — Evidence and Status Index

These labs document a mixture of **hands-on observations from a Windows endpoint** and **simulated SOC investigations**. They are learning exercises, not production incident reports.

## Status definitions

- **Complete:** The stated exercise was completed and its findings or answers recorded. The exercise can still have normal evidence limitations; “complete” does not mean a security verdict has been independently verified.
- **Pending evidence:** The concepts were practised, but required live output or measurements were not supplied.
- **Partial — follow-up:** Some endpoint evidence was collected, but specified checks remain outstanding.
- **Hands-on:** Commands or observations from a Windows computer are recorded.
- **Scenario:** Data was provided for analysis; no corresponding real incident is claimed.

## Lab register

| Date | Lab | Evidence type | Status |
| --- | --- | --- | --- |
| 18 Sep 2026 | [Windows process, ports and signatures](2026-09-18-windows-process-investigation/README.md) | Hands-on | Complete |
| 19 Sep 2026 | [Suspicious connection triage](2026-09-19-suspicious-connection-triage/README.md) | Scenario | Complete |
| 20 Sep 2026 | [Windows Security event logs](2026-09-20-windows-security-event-log-investigation/README.md) | Hands-on | Complete |
| 22 Sep 2026 | [ARP and DNS](2026-09-22-arp-dns-review/README.md) | Hands-on (reported observations) | Complete |
| 22 Sep 2026 | [TCP ports and handshake](2026-09-22-tcp-ports-handshake/README.md) | Guided lab | **Pending evidence** |
| 24 Sep 2026 | [Connection log timeline](2026-09-24-connection-log-timeline/README.md) | Scenario | Complete |
| 30 Sep 2026 | [TCP connection outcomes](2026-09-30-tcp-connection-outcome-analysis/README.md) | Scenario | Complete |
| 2 Oct 2026 | [Process command lines](2026-10-02-notepad-process-command-line/README.md) | Hands-on + scenario | Complete |
| 3 Oct 2026 | [Listeners and firewall profiles](2026-10-03-listening-addresses-firewall/README.md) | Hands-on | Complete |
| 7 Oct 2026 | [AggregatorHost and PowerShell](2026-10-07-powershell-aggregatorhost-investigation/README.md) | Hands-on | Complete |
| 8 Oct 2026 | [PowerShell and Edge connections](2026-10-08-powershell-filtering-and-edge-connection-investigation/README.md) | Hands-on | Complete |
| 9 Oct 2026 | [Adobe service persistence](2026-10-09-adobe-service-persistence-investigation/README.md) | Hands-on | Complete |
| 11 Oct 2026 | [OneDC scheduled task](2026-10-11-onedc-updater-scheduled-task-investigation/README.md) | Hands-on | Complete |
| 15 Oct 2026 | [Explorer process records](2026-10-15-explorer-process-record-variables/README.md) | Hands-on | Complete |
| 22 Oct 2026 | [Least privilege](2026-10-22-least-privilege-worked-example/README.md) | Scenario | Complete |
| 24 Oct 2026 | [Code signatures and behaviour](2026-10-24-signatures-and-behaviour-triage/README.md) | Scenario | Complete |
| 31 Oct 2026 | [Configuration-change timeline](2026-10-31-configuration-change-timeline/README.md) | Scenario | Complete |
| 1 Nov 2026 | [File vs running process](2026-11-01-file-versus-process/README.md) | Hands-on + scenario | Complete |
| 9 Nov 2026 | [Log deduplication](2026-11-09-log-deduplication/README.md) | Scenario | Complete |
| 10 Nov 2026 | [Npcap watchdog scheduled task](2026-11-10-npcap-watchdog-scheduled-task-triage/README.md) | Partial hands-on | **Partial — follow-up** |
| 12 Nov 2026 | [Phishing email and click triage](2026-11-12-phishing-email-click-investigation/README.md) | Scenario | Complete |
| 14 Nov 2026 | [Attachment and process chain](2026-11-14-attachment-process-chain/README.md) | Scenario | Complete |
| 15 Nov 2026 | [PID reuse and event timing](2026-11-15-pid-reuse-event-timing/README.md) | Scenario | Complete |

## Unfinished labs — next steps

### TCP ports and handshake — pending evidence

[Open the TCP ports lab](2026-09-22-tcp-ports-handshake/README.md). The TCP handshake concepts and questions were reviewed, but **actual LocalPort, RemotePort, and correlated process output were not supplied**. The connection noted as `ms-teams.exe` must not be presented as the `curl.exe` / example.com test without evidence. To complete, capture a real connection row with ports, PID and the matching process at approximately the same time, plus any claimed test result.

### Npcap watchdog scheduled task — partial

[Open the Npcap lab](2026-11-10-npcap-watchdog-scheduled-task-triage/README.md). Task state, action and principal were observed. The actual trigger, batch-file contents, invoked executables and task execution history were **not verified**. Those checks remain open; the current assessment is low suspicion, **not confirmed safe**.

## Portfolio navigation

- [Portfolio overview](../README.md)
- [Networking fundamentals](../01-networking-fundamentals/)
- [Endpoint investigations](../02-endpoint-investigation/)
- [TryHackMe progress](../tryhackme/README.md)

**Audit date:** 16 November 2026. Statuses reflect evidence in the existing write-ups, not newly performed tests.

## Worked examples for review

- 17 November 2026 — [Scope a Windows service installation with logs](2026-11-17-service-install-log-scoping/README.md). Fictional data; separate from the audited completion totals above.
- 18 November 2026 — [PowerShell log filtering](2026-11-18-powershell-log-filtering/README.md). Fictional worked solution with expected output; commands not executed in the publishing environment. Separate from the audited completion totals above.
- 19 November 2026 — [Why an empty search can mislead: AND versus OR](2026-11-19-and-or-log-filters/README.md). Fictional worked solution with expected output; commands not executed in the publishing environment. Separate from the audited completion totals above.
