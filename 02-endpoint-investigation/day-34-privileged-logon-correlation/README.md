# Day 34 - Privileged logons and event correlation

Today I investigated real Windows Security logon records and practised linking events using their **Logon ID**. I also completed a simulated SOC investigation of a privileged remote login.

## Windows Security events covered

| Event ID | Meaning |
| --- | --- |
| 4624 | An account successfully logged on |
| 4672 | Special privileges were assigned to a new logon |
| 4688 | A new process was created (where auditing is configured) |

**Event 4672 is not proof of an attack or of someone manually granting new permissions.** It records privileges assigned to a logon session. SYSTEM and administrator activity can generate it during normal use.

### Logon types to remember

| Logon Type | Meaning |
| --- | --- |
| 2 | Interactive (including local desktop activity and some Windows-managed desktop sessions) |
| 3 | Network logon |
| 5 | Service logon |
| 10 | RemoteInteractive / RDP |

**Logon Type** describes *how* the logon occurred. **Logon ID** identifies the session and can help correlate related events on the same system.

## Practical 1 - Event 4672

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4672
} -MaxEvents 3 |
Format-List TimeCreated,Id,Message
```

Observed multiple records with:

```text
Account Name: SYSTEM
Security ID: S-1-5-18
Logon ID:    0x3E7
```

The privilege list included `SeDebugPrivilege`, `SeBackupPrivilege`, `SeTakeOwnershipPrivilege` and `SeLoadDriverPrivilege`.

Looking at ten recent records produced the same SYSTEM identity and Logon ID. This is consistent with normal SYSTEM activity and is not, by itself, suspicious. **0x3E7 is the well-known LocalSystem logon ID**, so it should not be treated as a unique sign of one unusual event.

I also practised `-notmatch` in PowerShell to exclude SYSTEM events from a sample:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4672
} -MaxEvents 100 |
Where-Object {
    $_.Message -notmatch 'Account Name:\s+SYSTEM'
} |
Select-Object -First 3 TimeCreated,Message |
Format-List
```

## Practical 2 - Comparing Event 4624 with 4672

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4624
} -MaxEvents 30 |
Select-Object -First 3 TimeCreated,Message |
Format-List
```

The newest three events were service logons. An example at **14 October 2026, 15:13:15** contained:

```text
Subject Account: <COMPUTER>$
Logon Type:      5
New Logon:       NT AUTHORITY\SYSTEM
Logon ID:        0x3E7
Process:         C:\Windows\System32\services.exe
Source IP:       -
Elevated Token:  Yes
```

A 4672 event at the same time also concerned SYSTEM and `0x3E7`. This is consistent with related SYSTEM activity. Because `0x3E7` is reused for LocalSystem, correlation should consider the **time, account and machine** as well as the Logon ID.

Important distinctions:

- **Subject** = security context requesting the logon.
- **New Logon** = account for which the logon session was created.
- `services.exe` is the process involved, **not an IP address**.
- The `-` source address means no network source was recorded in that event.

## Practical 3 - Looking for interactive and RDP logons

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4624
} -MaxEvents 500 |
Where-Object {
    $_.Message -match 'Logon Type:\s+(2|10)\b'
} |
Select-Object -First 2 TimeCreated,Message |
Format-List
```

Found two logons dated **13 October 2026, 15:39:02**:

```text
New Logon:      DWM-22
Account Domain: Window Manager
Virtual Account: Yes
Logon Type:      2
Process:         C:\Windows\System32\winlogon.exe
Source IP:       -
```

The two records had linked logon sessions, with `Elevated Token: No` and `Elevated Token: Yes`, respectively. They were consistent with Windows-managed Desktop Window Manager activity. Elevated tokens and linked sessions do not automatically indicate malicious privilege escalation.

I then tried filtering out common desktop virtual accounts:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4624
} -MaxEvents 1000 |
Where-Object {
    $_.Message -match 'Logon Type:\s+(2|10)\b' -and
    $_.Message -notmatch 'Account Name:\s+(DWM-|UMFD-)'
} |
Select-Object -First 2 TimeCreated,Message |
Format-List
```

No events matched that filter in the records searched. This is a limited search result, **not proof that no human has logged in**.

## Simulated SOC case (not observed on my computer)

At 02:30:15, account `FinanceAdmin` logged in using RDP (4624, Type 10) from an unfamiliar external IP. A 4672 event at the same time showed special privileges for the same account and Logon ID `0x5A21`. At 02:31:02, a 4688 event recorded `powershell.exe -EncodedCommand ...`.

**Priority:** High, pending investigation.

**Evidence:**
- Privileged account logged in remotely at an unusual time from an unfamiliar address.
- Successful logon and privilege event had matching Logon IDs.
- Encoded PowerShell execution followed shortly after.

**Assessment:** Potentially unauthorised privileged remote access and command execution. RDP and encoded PowerShell can have legitimate uses, and the event sequence alone does not prove a compromise.

**Next steps:**
1. Verify with IT/the account owner whether the RDP connection was authorised.
2. Check the source IP, related authentication history and endpoint activity.
3. Examine the encoded PowerShell safely, without executing it.
4. Correlate process details and any other activity with the account and logon session.

**Decision:** Escalate for investigation.

## Main takeaways

- **Logon Type 10 = RDP**; **Logon Type 5 = service**; **Logon Type 2 = interactive**.
- **Logon ID** is a way to associate events with the same session.
- Event **4672** doesn't automatically mean an attacker received new privileges.
- SYSTEM and DWM records are common Windows activity.
- Check multiple fields and corroborating evidence before deciding an alert is malicious.
- Make SOC recommendations specific: verify authorisation, source, process activity and commands.
