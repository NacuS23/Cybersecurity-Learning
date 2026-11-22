# Day 59 — Windows Logon Detection Prototype (Executed Python Lab)

**Date:** 22 November 2026  
**Status:** **Local code execution complete — nine unit tests passed**  
**Evidence type:** Executed Python detector and test suite using **synthetic, normalized** Windows Security events. No events were collected from the learner's PC or any real production endpoint.  
**Authorship:** Prepared as an AI-assisted worked training exercise, not an independently performed SOC investigation.

## Goal

Turn authentication-alert logic into a small **executable detection prototype** rather than another KQL query with unverified expected results. This lab uses two real Windows Security Event IDs as the model for its synthetic data:

- **4625** — failed account logon.
- **4624** — successful account logon.

Both can include account, logon type and network source information when provided by the Windows event. The JSONL fixture is a *simplified normalized representation* of such fields, **not** an exported EVTX file.

## Detection logic

The Python script reads [sample_events.jsonl](sample_events.jsonl) and examines **LogonType 3 (network)** events that have a source IP address.

It looks for:

1. **At least five failed logons** (`EventID=4625`) within a **sliding five-minute window** from the same reported source IP.
2. **At least three distinct targeted usernames** within that window.
3. A **subsequent successful network logon** (`EventID=4624`) from the **same IP** to one of the targeted usernames within **10 minutes after the last failure**.

The script reports *candidate bursts* even if no follow-on success is found, and flags those with a matching success for prompt review. It suppresses duplicate overlapping candidates within a detected burst; it is a demonstration, not a production alert engine. This is more flexible around clock boundaries than fixed `bin(TimeGenerated, 5m)` buckets from Days 56–58.

**Important distinction:** These are possible suspicious patterns. A shared IP (NAT, VPN, proxy), system/service activity or user mistakes can produce similar sequences. A successful login does **not** prove compromise, and the code cannot infer who actually controlled the source IP.

## Files

| File | Purpose |
| --- | --- |
| [detector.py](detector.py) | Executable Python 3 standard-library detector. No third-party packages. |
| [sample_events.jsonl](sample_events.jsonl) | 41 fictional, normalized Windows logon records. |
| [make_fixture.py](make_fixture.py) | Deterministically regenerate the synthetic fixture. |
| [tests/test_detector.py](tests/test_detector.py) | Nine executable unit tests covering positive/negative scenarios. |
| [evidence/unittest_output.txt](evidence/unittest_output.txt) | **Actual** local unit-test output captured from an executed Python process. |
| [evidence/detection_output.json](evidence/detection_output.json) | **Actual** JSON output of the local detector on the synthetic fixture. |

All example source IP addresses are from RFC 5737 documentation ranges; no real users or hosts are included.

## Reproduce without any paid platform

With Python 3 installed, from this folder run:

```bash
python make_fixture.py
python -m unittest discover -s tests -v
python detector.py sample_events.jsonl
```

These are **instructions for reproduction**, not a claim that the learner ran them personally. They were executed in the assistant's separate Python working environment.

## Observed results from local execution

| Metric | Actual result |
| --- | ---: |
| Synthetic events processed | 41 |
| In-scope network logons with usable source IP | 31 |
| Out-of-scope events (unknown IP / local logon type) | 10 |
| Candidate failure bursts | 4 |
| Bursts with a timely success for a targeted user | 2 |
| Unit tests | **9 passed, 0 failed** |

### Investigated scenarios

| Fictional source | Test pattern | Actual detector output | Interpretation |
| --- | --- | --- | --- |
| `198.51.100.25` | Five failures targeting Alex, Sam and Maria; Sam succeeds at 10:05 | Candidate + correlated success | Promptly review Sam's authentication context |
| `203.0.113.80` | Six failures against only `backup`, then success | Not a spray candidate | Repeated single-account attempts are a different pattern |
| `192.0.2.70` | Five failures over three accounts; success at 10:36, 12 minutes after last failure | Candidate, no timely success | Do not count late success as matching the detection window |
| `203.0.113.75` | Five failures across three accounts; success for an *unrelated* account from same IP | Candidate, no targeted success | Matching source IP alone is not sufficient |
| `192.0.2.90` | Five failures from 10:58–11:02 across three accounts, then Noah succeeds at 11:03 | Candidate + correlated success | Sliding window detects a burst crossing the 11:00 clock boundary |

Five additional failed events with a missing IP and five local LogonType 2 events were intentionally excluded by the detector's scope. Those exclusions are **coverage limitations**, not evidence that they are safe.

## Unit-test coverage

The nine executed tests verify:

- Expected input/output totals and event exclusions.
- Positive failure-to-success correlation for a targeted account.
- Single-account guessing does not meet the multi-account threshold.
- Success outside the allowed follow-up window is not correlated.
- Success for an unrelated account on the same IP is not correlated.
- Sliding time window handles a burst crossing a fixed five-minute boundary.
- Events lacking usable source IP and local logons are excluded as designed.
- Timestamps without time zones are rejected.
- Overlapping windows do not produce duplicate candidate alerts for one burst.

Full observed output is committed under [`evidence/`](evidence/). The suite ran on synthetic fixture data; this does not validate the reliability or false-positive rate against real enterprise authentication logs.

## Simulated SOC ticket

**Title:** Repeated network logon failures across accounts followed by a targeted account success  
**Relevant event IDs:** 4625 failures, 4624 success  
**Priority candidates:** `198.51.100.25` and `192.0.2.90` (fictional documentation addresses)  
**Assessment:** Pattern consistent with possible credential attacks, but the identity of the actor and whether access was authorised are unknown.  
**Actions if observed in production:** Examine raw Security events, account/domain, logon type, workstation and network context; cross-check endpoint/server location of events, known shared IPs and service credentials; review post-login activity and escalate according to local policy.  
**Disposition:** Triage required. **No compromise established.**

## Known limitations and next step

- **Not a SIEM.** This runs locally on an offline JSONL file. It does not query Event Viewer, parse raw EVTX, or install/run Wazuh or Microsoft Sentinel.
- **Not KQL execution.** Days 53–58's public Azure Data Explorer verification remains pending.
- **Coverage is deliberately narrow.** Only network LogonType 3 is considered. Real Windows logon events can omit source IPs; local/RDP and other relevant logons are excluded here.
- **Window and matching logic is a prototype.** It omits source-IP reputation, MFA, device risk, alert suppression across hosts, prior baselines, evasion scenarios and production-scale state management.
- **Next hands-on goal:** On the learner's Windows computer, read a small number of actual Event 4624/4625 entries in Event Viewer or PowerShell, determine which fields are available, and build a privacy-safe normalized export; later ingest real logs into the planned free SIEM and validate a detection with genuine lab evidence.

## References

- [Microsoft — Event 4625: An account failed to log on](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4625)
- [Microsoft — Event 4624: An account was successfully logged on](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)
- [Microsoft — Audit Logon](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/audit-logon)

[Back to the SOC portfolio](../../README.md)