# Day 49 - Windows Account Lockout Investigation

**Focus:** Security Event 4740, account lockout policy, and SOC authentication triage.

## Practical investigation

I checked for recorded account lockouts during the previous 30 days.

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4740
    StartTime = (Get-Date).AddDays(-30)
} -MaxEvents 10 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, Message |
Format-List
```

**Observed:** No matching events were returned. This does not prove that account lockouts never occurred; log availability, audit settings, and the account's authentication system matter. Domain account lockouts may need to be investigated on a domain controller.

I then examined the Windows workstation's local account policy using the read-only command:

```powershell
net accounts
```

### Actual local policy results

```text
Minimum password age (days): 0
Maximum password age (days): 42
Minimum password length: 0
Length of password history maintained: None
Lockout threshold: 10
Lockout duration (minutes): 10
Lockout observation window (minutes): 10
Computer role: WORKSTATION
```

These values describe **local policy settings**, not necessarily the policy that applies to a Microsoft account, domain account or another identity provider. They also do not reveal the actual strength of any account password.

The local policy has a 10-attempt lockout threshold and a 10-minute observation window and duration. These are policy settings, **not evidence of any actual lockout**.

## Relevant Windows events

| Event ID | Description |
| --- | --- |
| 4625 | Failed account logon |
| 4624 | Successful account logon |
| 4740 | Account locked out |

## Simulated SOC investigation (not observed on my computer)

A company account experiences 20 failed authentication attempts and three lockouts within one hour. The employee did not attempt these sign-ins; the source is not yet identified.

**Assessment:** The pattern warrants prompt investigation. An external password-guessing attempt is one possibility; a service, scheduled task or application using outdated credentials is another. Account lockouts alone do not prove a successful intrusion.

**Investigation plan:**
1. Review the affected account's 4625 records, including time, source address, and logon type.
2. Compare 4740 account lockout records and identify source systems where recorded.
3. Search for 4624 successful logons for the same account following the failures.
4. Check for stored old passwords in authorised applications or services.
5. Escalate and secure the account according to the company's procedures if evidence suggests unauthorised access.

**Decision:** Investigate rather than declaring an attack or a clean outcome without corroborating evidence.

## Lessons learned

- A Windows Security log search may return no records even when another system has relevant authentication evidence.
- `net accounts` is a useful read-only check for workstation account policy.
- Account lockout thresholds, durations and observation windows have different meanings.
- High volumes of authentication failures should be assessed in context, not simply counted.
- Distinguish **real evidence**, **possible explanations**, and **actions not yet verified**.

**Outcome of my real investigation:** No Event 4740 records were returned, and local account policy was successfully inspected.
