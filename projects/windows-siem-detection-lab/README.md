# Windows SIEM & Detection Engineering Home Lab

**Status:** Planned — setup not started  
**Type:** Proposed hands-on portfolio project; not a completed investigation  
**Budget goal:** Free software, existing computer, no paid TryHackMe subscription  
**Focus:** Central log collection, alert triage, and a custom detection rule

## Objective

Build a small, repeatable SOC environment where Windows security events are collected centrally, investigated in a dashboard, and used to trigger at least one detection rule that I can test and document.

This project is the next practical step after introductory PowerShell, Windows Event IDs, and simulated Microsoft Sentinel/KQL exercises.

## Architecture under consideration

```text
Windows endpoint / controlled test VM
    Windows Security event logs
                |
          Wazuh agent
                |
       Wazuh server + indexer
                |
          Wazuh dashboard
                |
     Alert investigation / triage
```

Wazuh is free and open source. The central server, indexer and dashboard run on a supported Linux system or Linux VM; the Windows agent can be installed on a Windows endpoint. A small all-in-one installation has published hardware recommendations, so local machine capacity must be checked before setup.

This is a **planned topology**, not evidence that Wazuh is installed.

## Proposed milestones and evidence checklist

- [ ] **Check local resources.** Record available CPU, RAM, storage and virtualization capability; choose a feasible Linux VM or other non-billable deployment.
- [ ] **Install a test SIEM.** Deploy Wazuh server, indexer and dashboard in an isolated, controlled environment.
- [ ] **Connect one Windows endpoint.** Install and enrol the Wazuh Windows agent; show the endpoint connected to the manager.
- [ ] **Ingest actual events.** Verify at least one Windows Security event appears in the dashboard with its timestamp, host and event ID.
- [ ] **Investigate authentication activity.** Query recent 4624 successes and 4625 failures, recording filters, results and any logging limits.
- [ ] **Write a detection rule.** Create a custom rule for repeated authentication failures and document its actual configuration, scope and false-positive considerations.
- [ ] **Test the detection safely.** Generate a small number of authorised test events in a lab account or use approved test data; avoid locking personal accounts or attempting unauthorised access.
- [ ] **Record the outcome.** Include an actual dashboard alert, relevant event evidence, a redacted screenshot and a concise SOC-style incident note.
- [ ] **Evaluate the rule.** Record what triggered, what did not, and any adjustments needed to reduce false positives.

## Detection use case — design draft only

**Name:** Repeated failed Windows authentication from one source  
**Potential event source:** Windows Security Event 4625 collected through Wazuh  
**Candidate detection idea:** Alert on an unusual cluster of failed logons for the same account or source over a short interval, while accounting for known services and scheduled tasks.  
**Investigation:** Correlate the alert with 4624 successes, device identity, account context, affected assets, and possible stale credentials.  
**Status:** Design concept. No detection rule has been installed, executed or validated. Appropriate event fields and aggregation semantics must be confirmed against the actual Wazuh decoder and lab data before implementation.

## Free KQL practice — complementary, not a SIEM

While the Wazuh environment is pending, I can use Microsoft's public **Azure Data Explorer help cluster** to practise real KQL queries in a browser. This provides a working KQL engine against sample datasets without an Azure subscription. It is **not** equivalent to a running SIEM that ingests my endpoint logs.

A free Azure Data Explorer cluster may later allow ingestion of carefully sanitised test data. Its availability and terms should be checked before use.

**Do not upload personal Security logs, identifiers, tokens or credentials to a public cluster.** Only collect data on machines/accounts I control or am authorised to investigate.

## Why not start with Microsoft Sentinel?

Microsoft Sentinel has a limited free trial, but billing can apply beyond the included thresholds, to additional features or after the trial. To avoid unexpected costs, the initial plan uses free KQL sample data and a locally hosted open-source SIEM. A future Sentinel trial is optional, not required to complete this portfolio project.

## Completion criteria

This project will be marked **Complete** only after a running SIEM collects a real or controlled-lab endpoint event, **one original detection rule is tested**, and the results are documented with evidence. Until then, this page remains **Planned**.

## Official references

- [Wazuh Quickstart and hardware requirements](https://documentation.wazuh.com/current/quickstart.html)
- [Wazuh Windows agent deployment](https://documentation.wazuh.com/current/installation-guide/wazuh-agent/wazuh-agent-package-windows.html)
- [Microsoft Azure Data Explorer samples gallery](https://learn.microsoft.com/en-us/azure/data-explorer/web-ui-samples-query)
- [Microsoft Sentinel billing and trial terms](https://learn.microsoft.com/en-us/azure/sentinel/billing)

[Back to the portfolio](../../README.md)
