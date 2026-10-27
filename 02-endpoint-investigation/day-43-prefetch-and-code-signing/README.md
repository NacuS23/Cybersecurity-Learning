# Day 43 - Prefetch, file versions, and a revoked signing certificate

**Date:** 27 October 2026  
**Focus:** Endpoint investigation and evidence-based SOC triage

Today I looked through Windows Prefetch artifacts, investigated two unfamiliar process names, compared an installed software version with the version of its executable, and checked a digital signature and SHA256 hash. I learned why a revoked certificate is a finding to investigate, not automatic proof of malware.

## 1. Reviewing recent Prefetch artifacts

I ran this read-only command:

```powershell
Get-ChildItem "$env:WINDIR\Prefetch" -Filter "*.pf" -File |
Sort-Object LastWriteTime -Descending |
Select-Object -First 10 Name, LastWriteTime, Length |
Format-Table -AutoSize
```

My ten results were:

```text
Name                                   LastWriteTime       Length
CONSENT.EXE-40419367.pf                27/10/2026 19:32:20  47197
DTSHELLHLP.EXE-2F7A94EE.pf             27/10/2026 19:32:17  10771
DISCSOFTBUSSERVICELITE.EXE-E019C04A.pf 27/10/2026 19:32:17   9660
RUNDLL32.EXE-BE8830B6.pf               27/10/2026 19:32:16   4636
MSEDGEWEBVIEW2.EXE-F67C40AA.pf         27/10/2026 19:31:57  18116
MSEDGEWEBVIEW2.EXE-F67C40B2.pf         27/10/2026 19:31:24  17509
AUDIODG.EXE-AB22E9A6.pf                27/10/2026 19:29:45   9647
SVCHOST.EXE-5F87ABED.pf                27/10/2026 19:28:33  14394
SVCHOST.EXE-EA9BB143.pf                27/10/2026 19:28:33   5777
SVCHOST.EXE-9A28EB78.pf                27/10/2026 19:27:15   5417
```

The names **DTSHELLHLP.EXE** and **DISCSOFTBUSSERVICELITE.EXE** were worth looking into because they were unfamiliar to me. They are associated with DAEMON Tools Lite.

**Prefetch reminder:** A `.pf` artifact is evidence consistent with a program having executed previously, even if it is not running now. Its file modification time is not necessarily the exact last execution time; a forensic parser would be needed to inspect embedded execution details. Finding a normal application such as Chrome in Prefetch does not make it suspicious.

## 2. Checking the installed application version

During the lesson, we discussed public reports of a 2026 DAEMON Tools Lite supply-chain incident affecting versions **12.5.0.2421–12.5.0.2434**. I checked my installation instead of assuming that a matching executable name meant infection.

```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*", "HKLM:\SOFTWARE\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" -ErrorAction SilentlyContinue |
Where-Object { $_.DisplayName -like "*DAEMON Tools*" } |
Select-Object DisplayName, DisplayVersion, InstallLocation
```

Actual result:

```text
DisplayName       DisplayVersion
DAEMON Tools Lite 12.1.0.2211
```

My installed version was **outside the reported affected range**. This was reassuring about the *specific reported incident*, but it was not proof that every component on my computer was harmless.

## 3. Checking the actual executable

```powershell
Get-Item "C:\Program Files\DAEMON Tools Lite\DTShellHlp.exe" |
Select-Object Name,
    @{Name="Version";Expression={$_.VersionInfo.FileVersion}},
    LastWriteTime
```

Actual result:

```text
Name           Version     LastWriteTime
DTShellHlp.exe 12.1.0.2211 26/09/2024 18:26:50
```

The executable version **matched** the installed application version. The file's displayed modification date was in 2024, predating the reported 2026 incident, though file timestamps can be altered and do not prove authenticity.

If the installed app reported **12.1** but an executable reported **12.5**, that difference would be a reason to investigate further.

## 4. Checking its digital signature

```powershell
Get-AuthenticodeSignature "C:\Program Files\DAEMON Tools Lite\DTShellHlp.exe" |
Select-Object Status, @{
    Name="Signer"
    Expression={$_.SignerCertificate.Subject}
}
```

The result identified signing-certificate subject **AVB Disc Soft, SIA**, but its status was **UnknownError**, not `Valid`.

To investigate the error, I ran:

```powershell
Get-AuthenticodeSignature "C:\Program Files\DAEMON Tools Lite\DTShellHlp.exe" |
Format-List Status, StatusMessage, SignatureType
```

Actual result:

```text
Status        : UnknownError
StatusMessage : A certificate was explicitly revoked by its issuer
SignatureType : Authenticode
```

**Interpretation:** Windows reported a revoked signing certificate. This means I cannot treat the digital signature as a valid assurance of trust. A revoked certificate can result from several circumstances and does **not**, on its own, prove that this executable is malicious or modified.

This finding still needs investigation, despite the reassuring version match.

## 5. Getting the SHA256 fingerprint

```powershell
Get-FileHash "C:\Program Files\DAEMON Tools Lite\DTShellHlp.exe" -Algorithm SHA256
```

Actual SHA256:

```text
6396460EE441DD2D083F5B1511A513EC8DE606AF8B66B09D8924B92E4B13285F
```

**Important correction:** Successfully generating a hash is **not a clean malware scan**. I did not establish a trusted matching hash or a verified malware reputation result for this exact file. The hash is available for comparison with trusted sources or threat intelligence.

## SOC case summary — Real observations

**Title:** DAEMON Tools Lite executable with a revoked signing certificate

**Source:** My Windows endpoint; inspection commands were read-only.

**Observed evidence:**
- Prefetch artifacts associated with two DAEMON Tools Lite executable names.
- Installed application version **12.1.0.2211**.
- `DTShellHlp.exe` file version **12.1.0.2211**; reported LastWriteTime **26/09/2024**.
- Certificate subject **AVB Disc Soft, SIA**.
- Authenticode verification **UnknownError**: certificate explicitly revoked by issuer.
- SHA256 hash collected as recorded above.

**Assessment:** There is **no established evidence of malware** from these results. The installed version is outside the specific reported 2026 affected range, which reduces concern about that incident. The revoked signing certificate is an unresolved trust issue. A real SOC analyst would consider endpoint context, available alerts, source authenticity and additional evidence before assigning final incident severity.

**Recommended next steps (not performed in this session):**
1. Run a full Microsoft Defender scan and review any detections.
2. Check the exact file hash against a reputable, trusted reference if available, without uploading sensitive files publicly.
3. Investigate the certificate revocation or obtain a fresh signed installer from the official developer if the application is still needed.
4. If no longer needed, consider uninstalling the older application.
5. Review other available execution and persistence evidence only if additional suspicious indicators arise.

**Case status:** Investigated; **signature concern unresolved**, **malware not confirmed**. Do not claim the file is verified clean.

## What I learned

- `Get-ChildItem`, `Sort-Object` and `Select-Object` help triage recent forensic artifacts.
- `Get-ItemProperty` can inspect software uninstall registry records.
- `Get-Item` and `.VersionInfo.FileVersion` reveal a file's reported version.
- `Get-AuthenticodeSignature` reports certificate and verification status; `StatusMessage` can explain an error.
- A signing certificate being present is different from a **valid** signature.
- `Get-FileHash` calculates an identifying fingerprint, not a malware verdict.
- **Version match ≠ proof of safety. Revoked certificate ≠ proof of malware.** Follow the evidence and document uncertainty.
