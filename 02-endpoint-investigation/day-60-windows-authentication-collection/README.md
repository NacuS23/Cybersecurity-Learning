# Day 60 — Windows Security Event Collection and Privacy-Safe Validation

**Date:** 23 November 2026  
**Scope:** Windows Event IDs 4624 and 4625, collection design, pseudonymisation, schema checks, detection hand-off  
**Status:** **Python validation and 11 automated tests executed; Windows collector not executed on user's PC**  
**Evidence:** Nine completely fictional authentication events; recorded test output and validation summary.

## Investigation question

Can we collect Windows authentication events in a format suitable for our [Day 59 login detector](../day-59-windows-logon-detection-prototype/README.md), while reducing the chance of disclosing personal account names, IP addresses, and workstation names in a public learning portfolio?

**Answer:** A Windows PowerShell collector and JSONL validation workflow are now available. The validator was tested successfully against synthetic data. **No real Windows event logs were accessed in this lesson.** The collector remains to be tried on a Windows computer that the learner owns or has permission to administer.

## 1. Security events to collect

- **4624** — successful account logon.
- **4625** — failed account logon.
- **LogonType 3** — network logon. This is the initial scope of the Day 59 detector, not a statement that every network logon is an interactive remote compromise.
- **IpAddress** — may be missing or shown as `-`; do not infer that all such events have a usable external IP.
- **TargetUserName** and **TargetDomainName** — identify the targeted/logged-on account in event XML; must not be put unredacted in a public repository.

Relevant PowerShell API: `Get-WinEvent -FilterHashtable @{LogName='Security'; Id=@(4624,4625); StartTime=...}`.

Official Microsoft references: [4624 event reference](https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4624), [4625 event reference](https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4625), [Get-WinEvent documentation](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.diagnostics/get-winevent).

## 2. Files supplied

| File | Purpose | Actual test status |
| --- | --- | --- |
| [`collect_signins.ps1`](collect_signins.ps1) | Read-only Windows event query, XML field extraction and pseudonymised local JSONL export | **Not run on Windows in this session** |
| [`verify_export.py`](verify_export.py) | Validate exact exported fields, pseudonym format and UTC timestamps; summarize logon outcomes | **Executed on synthetic fixture** |
| [`sample/synthetic_export.jsonl`](sample/synthetic_export.jsonl) | Nine fictional records matching expected normalized export schema | **Used in tests** |
| [`tests/test_verify_export.py`](tests/test_verify_export.py) | Eleven unit tests for schema, counts, pseudonym mapping and rejection of unredacted fields | **11 passed** |
| [`evidence/test_results.txt`](evidence/test_results.txt) | Local unit-test execution output | **Observed output** |
| [`evidence/sample_validation.txt`](evidence/sample_validation.txt) | Local synthetic fixture-validation output | **Observed output** |

## 3. Verified synthetic data results

The Python validator was executed in an isolated Python 3 environment against the committed synthetic schema and tests:

```text
python -m unittest discover -s tests -v
Ran 11 tests in 0.003s
OK
```

The command `python verify_export.py sample/synthetic_export.jsonl` returned:

| Metric | Observed on synthetic data |
| --- | ---: |
| Records | 9 |
| Event 4625 failures | 7 |
| Event 4624 successes | 2 |
| Network LogonType 3 | 8 |
| Missing/local IP placeholder | 1 |
| Distinct account pseudonyms | 4 |

The test suite checks consistent account/source pseudonyms, rejects raw-looking names, hostnames and IPs, rejects unexpected fields and invalid Event IDs, and requires UTC timestamps.

**What this establishes:** The Python validation utility and test cases behave as expected for this synthetic input.

**What it does not establish:** The Windows PowerShell collector has not been runtime-tested on a Windows computer, nor have real audit logs been parsed. The schema test cannot guarantee privacy or security of every real export.

## 4. Run on your own Windows computer (optional hands-on completion)

Only collect logs from a Windows PC you own or are authorised to examine. Review the script before running it.

1. Download or clone this repository and open Windows PowerShell as Administrator **if needed for Security log read access**.
2. In the Day 60 folder, execute this read-only collection command, which writes a new file locally:

   ```powershell
   .\collect_signins.ps1 -Hours 24 -MaxEvents 1000
   ```

3. Run the Python validator against the output; the default location is a local Temp folder:

   ```powershell
   python .\verify_export.py "$env:TEMP\day60_signins_anonymized.jsonl"
   ```

4. Optionally use the Day 59 detector on the same pseudonymised file:

   ```powershell
   python ..\day-59-windows-logon-detection-prototype\detector.py "$env:TEMP\day60_signins_anonymized.jsonl"
   ```

5. Compare any alerts to the actual event context on the computer; avoid making a compromise claim based solely on raw failure counts.

If an execution-policy restriction occurs, review your local PowerShell security settings rather than blindly disabling protections. If a Security log query returns no entries or access denied, the result does not mean the system is secure. Logging configuration, access privileges and query limits need checking.

**Privacy:** Do **not** upload raw Security logs or even pseudonymised log exports to a public GitHub repository. The export keeps exact event timestamps and correlation patterns. Fresh per-run salted pseudonyms reduce direct disclosure and permit grouping within one export, but are **not equivalent to full anonymisation**. For a learning review, a short summary of record counts is usually sufficient.

## 5. SOC interpretation

With genuine data, investigate repeated 4625 failures across multiple distinct account pseudonyms, and correlate with 4624 successes from the same source. Confirm device context and whether the account actually belongs to a person, application or service; assess false positives such as stored credentials and automated tasks. Note that an unknown or local IP cannot be correlated by this source-IP-based method.

Neither a matched success nor a null result proves compromise or safety without supporting context.

## 6. Completion checklist

- [x] Confirm 4624/4625 field references in official Windows documentation.
- [x] Create PowerShell collector with local export and per-run salted pseudonyms.
- [x] Create synthetic JSONL fixture matching the Day 59 detector schema.
- [x] Execute Python validation and 11 unit tests; preserve outputs.
- [ ] Execute PowerShell collector against authorised **real Windows Security logs**.
- [ ] Verify actual output schema and compare a small sample to the local Windows Event Viewer.
- [ ] Review local results privately and document a privacy-safe observation, if any.
- [ ] Advance toward a genuinely deployed Wazuh/SIEM detection and validation.

**Conclusion:** Day 60 worked lesson prepared and Python-tested; *real endpoint ingestion remains pending*. This is **not** a production SOC investigation or a deployed SIEM. Code and analysis were AI-assisted.

[Back to portfolio](../../README.md)
