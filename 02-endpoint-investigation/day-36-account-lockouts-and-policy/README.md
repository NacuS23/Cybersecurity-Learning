# Day 36 - Account lockouts and Windows account policy

Today I investigated Windows account lockouts, checked my computer's local account policy and worked through a simulated SOC case involving repeated failed logons.

## Event IDs and what to investigate

| Event ID | Meaning |
| --- | --- |
| 4625 | Failed logon |
| 4624 | Successful logon |
| 4740 | A user account was locked out |

Event **4740** may contain a **Caller Computer Name** that helps trace the source of a lockout. In domain environments, relevant account-lockout events are often investigated on domain controllers. This field is a lead, not definitive proof of the attacker's machine.

A series of failed logons followed by an account lockout may be caused by password guessing, an employee entering the wrong password or software still using old credentials.

## Practical 1 - Checking for lockout events

Read-only PowerShell query:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4740
} -MaxEvents 3 |
Format-List TimeCreated,Message
```

**Result:** No matching Event 4740 records were found in the available local Security log.

This does not prove that an account has never been locked out. Records may not be retained locally, or the relevant event may be recorded on another machine.

## Practical 2 - Inspecting the local Windows account policy

Read-only command:

```powershell
net accounts
```

Output from my Windows workstation:

```text
Force user logoff how long after time expires?: Never
Minimum password age (days):                   0
Maximum password age (days):                   42
Minimum password length:                       0
Length of password history maintained:         None
Lockout threshold:                             10
Lockout duration (minutes):                    10
Lockout observation window (minutes):          10
Computer role:                                 WORKSTATION
```

### Interpretation

- **Threshold 10:** The local policy can lock an applicable account after ten unsuccessful authentication attempts.
- **Duration 10 minutes:** A lockout generally expires after ten minutes.
- **Observation window 10 minutes:** Windows resets the failed-attempt count after the observation window elapses without additional failures.
- **Minimum password length 0:** This local policy doesn't impose a minimum length; it **does not** mean the actual account has a blank password.
- **Password history None:** This local policy doesn't enforce password-history reuse restrictions.

These are the local workstation's settings. They are not necessarily the same as the requirements of an online Microsoft account or an organisation's domain policy.

An attacker can also deliberately trigger lockouts as a denial-of-service tactic without knowing an employee's password.

## Simulated SOC investigation

**Training scenario — not an incident observed on my computer.**

A finance employee's account received several failed logons from the employee's laptop and then an Event 4740 lockout. The employee had recently changed their password and reported that a work application still had the old credentials saved.

### SOC ticket

**Title:** Account lockout after repeated failed authentication.

**Priority:** Low, based on the available context.

**Evidence:**
- Several Event 4625 failed logons associated with the employee account.
- Event 4740 recorded an account lockout.
- Attempts were associated with the employee's usual laptop.
- The employee reported a recent password change and an application using older credentials.

**Assessment:** A stale saved password in an application is a plausible benign cause of the failures. The explanation needs verification before the alert is closed.

**Next steps:**
1. Confirm which application or service is repeatedly attempting to authenticate.
2. Verify the source computer and expected account ownership.
3. Have IT or the account owner correct/remove outdated stored credentials.
4. Confirm the account can sign in and failed attempts have stopped.
5. Escalate if the source is unrecognised or the failures continue.

**Decision:** Close as a benign authentication issue **only after the source and resolution are verified**.

## Key lessons

- **4740 = account locked out**; **4625 = failed logon**; **4624 = successful logon**.
- Lockouts can result from attacks **or** routine password-management problems.
- An unfamiliar source for repeated failures deserves investigation, but is not proof of an attacker.
- Read the actual account lockout policy rather than assuming all Windows systems use the same settings.
- Finding a plausible benign explanation is not enough; validate it and check the activity has stopped before closing the alert.
