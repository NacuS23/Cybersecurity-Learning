# Why an empty search can mislead — AND versus OR

**19 November 2026 · Fictional worked example**

This is a solved training exercise using supplied records. It does not claim learner command execution or a real security incident.

## Load the data

Paste the complete block into PowerShell. It creates records in memory only.

```powershell
$events = @'
Time,Computer,Result
09:00,LAB-01,Failed
09:01,FIN-04,Failed
09:02,LAB-01,Success
09:03,OPS-03,Failed
'@ | ConvertFrom-Csv

$events
```

Expected: four records with Time, Computer and Result fields.

## The flawed search

```powershell
$events | Where-Object {
    $_.Computer -eq "LAB-01" -and
    $_.Computer -eq "FIN-04"
}
```

Expected: **no rows**. Each supplied record has one Computer value. That value cannot equal both different computer names simultaneously.

## Corrected search

```powershell
$events | Where-Object {
    ($_.Computer -eq "LAB-01" -or
     $_.Computer -eq "FIN-04") -and
    $_.Result -eq "Failed"
}
```

Expected output:

| Time | Computer | Result |
|---|---|---|
| 09:00 | LAB-01 | Failed |
| 09:01 | FIN-04 | Failed |

The parentheses group the computer alternatives. The Failed requirement applies to either computer. The LAB-01 Success record is excluded.

## Practical task: LAB-01 or OPS-03

```powershell
$events | Where-Object {
    ($_.Computer -eq "LAB-01" -or
     $_.Computer -eq "OPS-03") -and
    $_.Result -eq "Failed"
}
```

Expected output:

| Time | Computer | Result |
|---|---|---|
| 09:00 | LAB-01 | Failed |
| 09:03 | OPS-03 | Failed |

## Plain-English explanation

| Item | Meaning |
|---|---|
| $events | Variable holding the supplied records |
| ConvertFrom-Csv | Turn comma-separated text into records with named fields |
| Where-Object | Keep records for which the condition is true |
| $_ | The current record being checked |
| $_.Computer | The Computer field of that record |
| -eq | Equals |
| -and | Both conditions must be true |
| -or | At least one condition must be true |
| Parentheses | Group the computer choices before combining them with the Failed condition |

## Knowledge-check answers

**Why did the first search return nothing?** It required one Computer value to equal two different names at once. This was a filter problem, not evidence that no failed sign-ins existed.

**Correct the colleague's claim, “There were no failed sign-ins because my search was empty.”** No records matched the flawed filter; the supplied data contains failed sign-ins, so the search must be corrected before drawing a conclusion.

**Does Success prove the legitimate account owner signed in?** No. It records a successful sign-in result but does not establish which human was responsible. Account, device, session and authentication context, plus trusted confirmation where appropriate, would help investigate. Success alone also does not establish an attack.

## SOC relevance and verification

Validate a search against known sample records before trusting an empty result. A search can miss activity because of its logic, time range or available data.

PowerShell was not available in the publishing environment, so these commands were **not executed there**. All output above is labelled expected and was derived from the supplied rows. No learner execution or live SIEM testing is claimed.
