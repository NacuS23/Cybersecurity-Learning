# Does one IP address mean one computer?

**Date:** 25 November 2026  
**Type:** Fictional worked example — supplied training records  
**Status:** Worked solution for review; not evidence of learner command execution or a live incident.

## Objective

Use device information to investigate failures behind a shared source IP without assuming the IP identifies one computer or person. Several devices can share a public IP through an office router or VPN. For this exercise, device labels come from endpoint records already matched to the sign-in events; that correlation is supplied, not independently verified here.

## Supplied evidence

| Time | Source IP | Device | Account | Result |
| --- | --- | --- | --- | --- |
| 10:00 | 192.0.2.40 | LAPTOP-01 | alex | Failed |
| 10:01 | 192.0.2.40 | LAPTOP-02 | sam | Failed |
| 10:02 | 192.0.2.40 | LAPTOP-01 | maya | Failed |
| 10:03 | 192.0.2.40 | LAPTOP-01 | alex | Failed |
| 10:04 | 192.0.2.40 | LAPTOP-02 | sam | Failed |
| 10:05 | 192.0.2.40 | LAPTOP-02 | sam | Success |

Additional context: Sam reports mistyping a password on LAPTOP-02. Activity on LAPTOP-01 has not yet been explained. Sam's report is information to corroborate, not proof.

## Reproducible PowerShell

The following commands analyse only the supplied text in memory.

```powershell
$events = @'
Time,SourceIP,Device,Account,Result
10:00,192.0.2.40,LAPTOP-01,alex,Failed
10:01,192.0.2.40,LAPTOP-02,sam,Failed
10:02,192.0.2.40,LAPTOP-01,maya,Failed
10:03,192.0.2.40,LAPTOP-01,alex,Failed
10:04,192.0.2.40,LAPTOP-02,sam,Failed
10:05,192.0.2.40,LAPTOP-02,sam,Success
'@ | ConvertFrom-Csv

$events | Format-Table -AutoSize

$failures = $events | Where-Object { $_.Result -eq "Failed" }
$failures | Format-Table -AutoSize

$failures |
    Group-Object Device |
    Select-Object Name, Count
```

- `$events` holds the original records; `$failures` holds the filtered records.
- `ConvertFrom-Csv` turns CSV text into records with named fields.
- `$_` means the current record being checked.
- `-eq` means equals.
- `|` passes records to the next command.
- `Where-Object` keeps matching records. It does not remove the success from the original `$events`.
- `Group-Object Device` puts records with the same device label into groups.
- `Select-Object Name, Count` displays each group label and its record count.

**Execution status:** PowerShell is not available in the publishing environment, so these commands were not executed here. The outputs below are expected results derived from the sample, not tested output.

## Expected results and solved practical check

These results are derived from the supplied records. They must not be presented as output captured from the learner's computer.

The original view contains six rows. Filtering for Failed retains the first five rows and excludes the 10:05 success.

Expected grouped output (display order may vary):

```text
Name      Count
----      -----
LAPTOP-01     3
LAPTOP-02     2
```

1. **Failures on LAPTOP-01:** 3.
2. **Failures on LAPTOP-02:** 2.
3. **Accounts with failures on LAPTOP-01:** alex and maya. These are account labels, not identified human operators.
4. **First device to investigate:** LAPTOP-01, because it has unexplained failures involving two accounts. This is a triage priority, not a maliciousness verdict. Sam's explanation for LAPTOP-02 still needs corroboration.
5. **Does the shared IP prove one person caused everything?** No. The supplied records associate that IP with two devices, and neither an IP nor a device label identifies the human responsible.
6. **Does Sam's success erase earlier failures?** No. The two failures remain historical events. Success alone also does not prove Sam personally performed the sign-in.
7. **Next evidence request:** Endpoint process and authentication records for LAPTOP-01 around 10:00–10:03, correlated with sign-in/session identifiers where available.
8. **Question that evidence would answer:** Which process or session initiated the attempts, and whether the pattern fits an expected application, user activity or something requiring escalation. Owner confirmation can add context but should be compared with the technical evidence.

## Concise SOC handover

Five failed sign-ins in the supplied records share source IP 192.0.2.40. Matched endpoint labels attribute three failures to LAPTOP-01 (alex twice, maya once) and two to LAPTOP-02 (sam twice), followed by a successful sam sign-in on LAPTOP-02. Prioritise the unexplained LAPTOP-01 activity and request correlated endpoint/authentication evidence. Corroborate Sam's mistyped-password report separately.

## Evidence limits

The records do not establish an attack, a single operator, credential theft or legitimate human identity. The device correlation is stipulated for training. No claim is made about complete log coverage, activity beyond these six rows, containment or live SIEM deployment.

This worked example is separate from audited learner completion totals.
