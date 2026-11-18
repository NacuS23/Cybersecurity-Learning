# PowerShell log filtering — fictional worked example

**Date:** 18 November 2026  
**Type:** Supplied fictional service logs; worked solution for study. No user execution or real endpoint investigation is claimed.

## Objective

Load structured records, keep events matching two conditions, and investigate an installation outside the approved computer list. This filtering logic is useful when searching logs in a SOC.

## Reproduce the exercise

Open PowerShell normally and paste the whole block. It creates training records in memory and does not install or change services.

```powershell
$logs = @'
Time,Computer,Service,Action
14:05,LAB-01,Inventory Agent,Installed
14:06,LAB-01,Inventory Agent,Started
14:10,FIN-04,Inventory Agent,Installed
14:12,LAB-02,Print Helper,Installed
14:18,LAB-02,Inventory Agent,Installed
'@ | ConvertFrom-Csv

$logs
```

The here-string holds the text. ConvertFrom-Csv turns it into five records with named fields.

Save the matching installation records:

```powershell
$installs = $logs | Where-Object {
    $_.Service -eq "Inventory Agent" -and
    $_.Action -eq "Installed"
}

$installs
```

Expected output (not a captured execution):

| Time | Computer | Service | Action |
|---|---|---|---|
| 14:05 | LAB-01 | Inventory Agent | Installed |
| 14:10 | FIN-04 | Inventory Agent | Installed |
| 14:18 | LAB-02 | Inventory Agent | Installed |

**Number of records in $installs: 3.** The Started row fails the action condition. Print Helper fails the service condition.

Search the saved results:

```powershell
$installs | Where-Object {
    $_.Computer -eq "FIN-04"
}
```

Expected result:

| Time | Computer | Service | Action |
|---|---|---|---|
| 14:10 | FIN-04 | Inventory Agent | Installed |

## What each part means

| Expression | Meaning |
|---|---|
| $logs | Variable storing the five supplied records |
| $installs = | Assign the command's results to a variable named installs |
| The pipe character | Pass records to the next command |
| Where-Object | Keep records whose condition is true |
| $_ | The current record being checked |
| $_.Service | Read that record's Service field |
| -eq | Equals |
| -and | Both conditions must be true |

Assignment stores results; entering the variable name displays them. A variable is not itself a file saved on disk.

## Investigation conclusion

The supplied approval covers LAB-01 and LAB-02 only. FIN-04 needs checking because its installation is outside that approved computer list. Request a separate change approval or deployment record to establish whether that installation was authorised. Absence from the supplied approval alone does not prove malicious activity.

These installation records do not establish that the service is currently running. A later service-state observation would be needed to establish its state at that later time.

## Verification and limits

PowerShell was not available in the publishing environment, so these commands were not executed there. The expected results were derived by checking the supplied rows against both conditions. No live Windows output or learner completion is claimed. This is a PowerShell filtering exercise, not a running SIEM deployment.
