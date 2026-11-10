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


## Catch-up review - 8 November 2026

I repeated a read-only query for Event 4740 across the preceding 30 days using the filter below:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4740
    StartTime = (Get-Date).AddDays(-30)
} -MaxEvents 5 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id |
Format-Table -AutoSize
```

**Result:** No matching records were returned in this follow-up query.

**Simulated SOC decision:** In a scenario with 20 failed logons, an account already locked by the authentication system, and an employee who denies trying to sign in, I would promptly investigate the source and check whether any successful logon occurred. The recorded lockout already restricts new sign-ins under the applicable policy; further containment, session revocation or account disablement would depend on findings and authorised incident-response procedures. Employee denial raises concern but doesn't confirm an attacker or successful compromise.

**Day 49 status: Completed.** All 50 lessons through Day 50 are now completed.

## Final simulated SOC case — source found and credentials corrected

*Training scenario only. These details were not observed in my real Windows logs.*

Further investigation found the following:

| Item | Simulated finding |
| --- | --- |
| Failed logons | 20 |
| Source workstation | `FINANCE-PC-07` |
| Logon type | 3 (network) |
| Account lockouts | 3 |
| Successful logons | None identified in the records reviewed |
| IT finding | A scheduled service on the workstation was using the employee's previous password |

**Assessment:** The most likely explanation is a misconfigured service using stale credentials, **not** a confirmed brute-force attack. A lack of successes in the inspected records is not proof no other access occurred.

**Recommended action:** Have the authorised IT team update the service's saved credentials using approved credential-management procedures, check that the service continues operating, and monitor Events 4625 and 4740 to confirm failed attempts and lockouts stop. Close the alert only when the cause and fix are verified; investigate any unexplained authentication events further.

**Learner's final decision:** Correctly classified the scenario as **B — likely a misconfigured service** and recommended updating the service credentials to the current valid password.

**Progress:** Day 49 complete, alongside Day 50; **50/120 lessons completed (41.7%)**.
