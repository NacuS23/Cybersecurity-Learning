# Day 29 - Windows service installation investigation

Today I investigated Windows Event ID 7045 and practiced deciding whether a newly installed service looked legitimate or suspicious.

## Event ID 7045

Event ID 7045 means:

```
A service was installed in the system
```

This is not automatically malicious. Legitimate software often installs services, but malware can also use services for persistence.

## Real event investigated

I found:

```
Service Name: MSI Center Service
Service File Name:
C:\Program Files (x86)\MSI\MSI Center\MSI_Central_Service.exe

Service Type: user mode service
Service Start Type: auto start
Service Account: LocalSystem
```

## Initial triage

The service deserved checking because:

- it was configured to start automatically
- it ran as LocalSystem

Those settings are not malicious by themselves, but they matter because an attacker could abuse them for persistence and high privileges.

The path was reassuring because it was under:

```
C:\Program Files (x86)\MSI\MSI Center\
```

## Signature verification

I checked the executable signature:

```powershell
Get-AuthenticodeSignature "C:\Program Files (x86)\MSI\MSI Center\MSI_Central_Service.exe" |
Format-List Status,StatusMessage,SignerCertificate
```

Result:

```
Status: Valid
Signature verified
Signer: MICRO-STAR INTERNATIONAL CO., LTD.
```

The signer matched the expected MSI vendor.

## Checking whether the service still existed

I used:

```powershell
Get-Service -DisplayName "*MSI*" |
Select-Object Status,Name,DisplayName
```

Result included:

```
Running MSI Foundation Service
Running MSI_Center_Service
Running MSI_Companion_Service
```

This showed that MSI Center Service was still installed and running, and that other MSI-related services were also present.

## Assessment

```
Alert:
New Windows service installed - Event ID 7045

Assessment:
Low priority / likely legitimate

Evidence:
- Expected MSI Program Files path
- Valid digital signature
- Signer matched MICRO-STAR INTERNATIONAL CO., LTD.
- Service remained installed and running
- Other MSI services were also present

Decision:
Close
```

## Suspicious comparison

A much more suspicious example would be:

```
Service Name: Windows Update Helper
Service File Name:
C:\Users\User\AppData\Local\Temp\winupdate.exe

Start Type: Auto
Account: LocalSystem
```

Reasons to investigate:

- executable in Temp
- automatic startup
- high privilege through LocalSystem
- service name trying to look like a Windows component

Useful next checks would be:

- digital signature
- SHA256 hash
- hash reputation
- network connections
- related events

## What I want to remember

- 7045 = a service was installed
- New service does not automatically mean malware
- Check service name, path, start type and account
- Auto start = persistence
- LocalSystem = high privilege
- User mode service is not suspicious by itself
- Expected path + valid signer + matching vendor + normal context can support closing an alert
- Suspicious path + persistence + high privileges should raise priority
