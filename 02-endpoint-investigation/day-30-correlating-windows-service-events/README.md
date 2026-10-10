# Day 30 - Correlating Windows service installation events

Today I practiced connecting several Windows events into one investigation rather than looking at each event separately.

## What I found

I searched the System event log for Event ID 7045 (a service was installed), between 15:22 and 15:23 on 4 October 2026.

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='System'
    Id=7045
    StartTime=(Get-Date '04/10/2026 15:22:00')
    EndTime=(Get-Date '04/10/2026 15:23:00')
} |
Format-List TimeCreated, Message
```

Four services appeared within 25 seconds:

| Time | Service | Executable |
| --- | --- | --- |
| 15:22:15 | Micro Star SCM | `C:\Windows\SysWOW64\MSIService.exe` |
| 15:22:16 | MSI Foundation Service | `C:\Program Files (x86)\MSI\MSI NBFoundation Service\MSIAPService.exe` |
| 15:22:19 | Sensor dev service | `C:\Program Files (x86)\MSI\MSI NBFoundation Service\Sendevsvc.exe` |
| 15:22:40 | MSI Center Service | `C:\Program Files (x86)\MSI\MSI Center\MSI_Central_Service.exe` |

All four were user-mode services configured for automatic start under LocalSystem. Those settings can be legitimate, but they're also why service installation can matter for persistence investigations.

## How I checked them

The MSI names and paths made a related software installation seem likely. I checked digital signatures rather than relying only on filenames or installation times.

For example:

```powershell
Get-AuthenticodeSignature "C:\Windows\SysWOW64\MSIService.exe" |
Format-List Status,SignerCertificate
```

I then repeated that check for the other executables.

All four executable signatures returned **Valid**, with **Micro-Star International Co., Ltd.** as the signer. The files used more than one code-signing certificate, which isn't unusual for one vendor.

## SOC ticket

**Alert:** Multiple new Windows services installed (Event ID 7045)

**Assessment:** Low priority / likely legitimate MSI installation or update activity.

**Evidence:**
- Four services were installed within 25 seconds.
- Names and paths were consistent with MSI software.
- All four executable signatures were valid and signed by Micro-Star International.
- The shared timing and vendor were consistent with a related installation, although timing alone doesn't prove all four were created by the same installer.

**Next steps:** No immediate action based on the reviewed evidence. Reopen if unexpected changes or related suspicious activity appear.

**Decision:** Close as likely benign.

## What I learned

- **Event correlation** means connecting events through time, user, device, process, or other shared evidence.
- Events happening close together don't automatically mean one caused another.
- Event 4624 = successful login; 4688 = process creation; 7045 = service installation.
- Logon Type 10 = remote interactive logon (RDP). A successful remote login is not automatically an attack.
- `Format-List` shows full event details when `Select-Object` truncates messages.
- A valid signature supports authenticity/integrity but doesn't prove that behaviour is safe.
- For a SOC conclusion, state *what was checked and why* the evidence supports a close/escalate decision.
