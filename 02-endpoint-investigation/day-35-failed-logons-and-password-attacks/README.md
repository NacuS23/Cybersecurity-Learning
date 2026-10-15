# Day 35 - Failed logons, brute force and password spraying

Today I looked for failed Windows logons, checked the audit policy and practised identifying password-guessing attacks from login patterns.

## Windows Security event IDs

| Event ID | Meaning |
| --- | --- |
| 4624 | Successful logon |
| 4625 | Failed logon |
| 4740 | User account locked out |
| 4720 | User account created |

Useful failure codes in Event 4625:

- `0xC000006A` — incorrect password
- `0xC0000064` — username does not exist

These events and codes help investigate authentication problems, but a single event does not prove an attack.

## Practical 1 - Searching for failed logons

I ran this read-only PowerShell query:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4625
} -MaxEvents 2 |
Format-List TimeCreated,Message
```

Windows returned **no matching events** in the available Security log.

That means there were no retained Event 4625 records matching the query at the time. It does **not** establish that the machine has never had a failed login.

If these events are available, I would inspect the account that failed to log on, Logon Type, Source Network Address, Status and Sub Status.

## Practical 2 - Checking logon auditing

I checked whether Windows is configured to record failed and successful logons:

```powershell
auditpol /get /subcategory:"Logon"
```

Actual result:

```text
System audit policy
Category/Subcategory        Setting
Logon/Logoff
  Logon                     Success and Failure
```

This indicates the local Logon audit subcategory is configured for both successes and failures. No matching events in the current log is still limited by retention, event generation and where the authentication actually occurred.

## Password attacks - patterns to recognise

| Pattern | What it might indicate |
| --- | --- |
| Many failed passwords against one account | Brute-force password guessing |
| One or a few passwords tried against many accounts | Password spraying |
| Username/password pairs taken from prior breaches | Credential stuffing |

In MITRE ATT&CK, these fall within **T1110 - Brute Force**, including its subtechniques.

**Practice comparison (simulated):**

- **Alert A:** 85 failed login attempts against `Administrator` from the same IP in five minutes. This is consistent with password guessing against one account.
- **Alert B:** 85 different employee accounts each receive one failed login from the same IP in five minutes. This is consistent with password spraying.

Neither pattern alone proves an attacker was involved; authorisation, source and other events matter.

## Simulated SOC investigation

**Training scenario only — not activity found on my PC.**

A `FinanceAdmin` account had 20 failed logins from the same source IP, then one successful login two minutes later from that IP. PowerShell launched under the account shortly afterwards.

### SOC ticket

**Title:** Repeated failed logons followed by successful access and PowerShell execution.

**Priority:** High.

**Evidence:**
- 20 failed authentication attempts associated with one account and source IP.
- A successful login from the same IP shortly afterwards.
- PowerShell execution observed following the login.

**Assessment:** Possible password-guessing activity and account compromise. The sequence is suspicious but could still have an authorised explanation. The source being the same does not prove the failed attempts and success were performed by the same person.

**Next steps:**
1. Verify whether the account owner or IT authorised the login.
2. Compare Event 4625 and 4624 account, timestamps, Logon Types and source addresses.
3. Review lockout events (4740), if any, and other authentication records.
4. Inspect the PowerShell process, command line, parent process and timing.
5. Escalate and consider containment according to the incident response playbook.

**Decision:** Escalate for investigation.

## What I want to remember

- **4624 = successful logon; 4625 = failed logon.**
- **4720 = account creation; 4740 = account lockout.**
- Many attempts against **one account** can mean password guessing.
- A few attempts against **many accounts** can mean password spraying.
- Repeated failures followed by success from the same source are important to correlate.
- `auditpol` checks whether relevant Windows auditing is configured.
- Missing events are not proof that no incident occurred.
- Separate the evidence recorded in logs from assumptions about attacker intent.
