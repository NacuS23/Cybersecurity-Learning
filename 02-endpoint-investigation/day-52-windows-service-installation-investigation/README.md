# Day 52 — Investigating Windows Service Installations (Event 7045)

**Lab type:** Actual Windows System log investigation and executable signature checks; separate simulated SOC scenario  
**Status:** Hands-on practical completed  
**Focus:** Windows service persistence, Event 7045, service configuration and Authenticode signatures

## Objective

Identify recently installed Windows services and decide whether the observed services merit further investigation. Understand how automatic startup and powerful service accounts can support persistence if abused.

## 1. Real endpoint: Windows System Event 7045

I used this read-only PowerShell query to retrieve up to five service-installation events from the preceding 30 days:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'System'
    Id = 7045
    StartTime = (Get-Date).AddDays(-30)
} -MaxEvents 5 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, Message |
Format-List
```

### Actual results

| Time recorded | Service | Service executable | Start type | Service account |
| --- | --- | --- | --- | --- |
| 12 Nov 2026 19:16:04 | Google Updater Service (GoogleUpdaterService159.0.8140.0) | `C:\Program Files (x86)\Google\GoogleUpdater\159.0.8140.0\updater.exe` | Auto start | LocalSystem |
| 12 Nov 2026 19:05:22 | Google Updater Internal Service (GoogleUpdaterInternalService159.0.8140.0) | `C:\Program Files (x86)\Google\GoogleUpdater\159.0.8140.0\updater.exe` | Auto start | LocalSystem |
| 4 Nov 2026 16:09:54 | MSI Center Service | `C:\Program Files (x86)\MSI\MSI Center\MSI_Central_Service.exe` | Auto start | LocalSystem |
| 4 Nov 2026 16:09:42 | Sensor dev service | `C:\Program Files (x86)\MSI\MSI NBFoundation Service\Sendevsvc.exe` | Auto start | LocalSystem |
| 4 Nov 2026 16:09:40 | MSI Foundation Service | `C:\Program Files (x86)\MSI\MSI NBFoundation Service\MSIAPService.exe` | Auto start | LocalSystem |

All five records listed a **user-mode service**, **automatic startup** and **LocalSystem**. The Google service commands also included `--system --windows-service --service=update` or `--service=update-internal`.

**Initial interpretation:** Service names and locations are consistent with Google Updater and MSI utilities. Automatic startup is relevant to persistence, and LocalSystem is highly privileged, but these features occur in legitimate services too. The presence of a 7045 event confirms service installation was logged, not that an attacker installed it.

## 2. Real endpoint: Check executable signatures

I verified two executables using this read-only PowerShell command:

```powershell
$paths = @(
    "C:\Program Files (x86)\Google\GoogleUpdater\159.0.8140.0\updater.exe",
    "C:\Program Files (x86)\MSI\MSI Center\MSI_Central_Service.exe"
)

foreach ($path in $paths) {
    if (Test-Path -LiteralPath $path) {
        $sig = Get-AuthenticodeSignature -LiteralPath $path

        [PSCustomObject]@{
            File   = $path
            Status = $sig.Status
            Signer = $sig.SignerCertificate.Subject
        }
    }
    else {
        Write-Output "File not found: $path"
    }
}
```

### Actual results

| File | Authenticode status | Signer |
| --- | --- | --- |
| Google `updater.exe` | **Valid** | **Google LLC** |
| MSI `MSI_Central_Service.exe` | **Valid** | **MICRO-STAR INTERNATIONAL CO., LTD.** |

**Interpretation:** Both checked files reported valid Authenticode signatures with publishers matching their apparent software vendors. This is useful evidence supporting authenticity and integrity of those particular files, but valid signing is **not** a guarantee that software cannot be misused or malicious. The three other service executable files were **not** signature-checked in this exercise.

## 3. Simulated SOC scenario — not observed on the endpoint

A fictional 7045 alert reports a new service named `WindowsBackupHelper` whose executable is `C:\Users\Public\backuphelper.exe`. It is configured for automatic start under LocalSystem.

**Analyst decision:** Investigate before deletion or attribution. Inspect publisher/signature, hash, executable behaviour, installation time, parent/creator activity, and related endpoint or event-log evidence. An unusual location plus elevated privileges and automatic startup warrants scrutiny but does not establish malware by itself.

**Learner answers:**
- Automatic startup enables **persistence**, because a service can start again after a reboot without manual execution.
- If the file were `NotSigned`, **investigate further** rather than automatically call it malware.

## SOC assessment

**Finding:** Five recently installed services in the queried records. All used automatic startup and LocalSystem; their names and paths appeared consistent with Google and MSI software. The two executable files checked had valid signatures from Google LLC and MICRO-STAR INTERNATIONAL CO., LTD.

**Assessment:** **Low concern based on the reviewed evidence.** No malicious service installation or persistence was established.

**Limitations:** Only the five newest matching installation events in the selected window were reviewed. Only two of five service executable files were signature-checked. No binary hashes, service creator identities, full service configurations, live process behaviour or network activity were examined. No claim is made that other service installations are absent.

**Disposition:** No immediate escalation based solely on this sample. Investigate if other telemetry or unexplained behaviour indicates a problem.

## Key takeaways

- **Event 7045:** Records that a service was installed; inspect its name, binary path, startup mode and service account.
- **Automatic startup:** Can support legitimate functionality or attacker persistence.
- **LocalSystem:** Powerful service identity; not itself an indicator of compromise.
- **Authenticode Valid:** Supports publisher identity and integrity of the checked file; not absolute proof of safety.
- **NotSigned:** A prompt for further investigation, not automatic proof of malware.
- Keep observed endpoint output separate from fictional SOC training scenarios.

**Progress after completion:** **52/120 lessons (43.3%)**, 68 remaining.
