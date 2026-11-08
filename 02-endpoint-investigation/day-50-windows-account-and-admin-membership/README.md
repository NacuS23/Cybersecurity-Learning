# Day 50 - Windows Account Creation and Administrator Membership Investigation

**Focus:** Windows Security Events 4720 and 4732, local administrator group membership, and built-in Administrator account status.

**Lab type:** Real Windows endpoint investigation using read-only PowerShell commands.

## Objective

Investigate whether Windows recorded recent user-account creation or local security-group membership changes. Inspect the current Administrators group and verify whether the built-in Administrator account is enabled.

## 1. Search for account and group changes

I queried the Security log for the previous 30 days:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4720,4732
    StartTime = (Get-Date).AddDays(-30)
} -MaxEvents 5 -ErrorAction SilentlyContinue |
Select-Object TimeCreated, Id, Message |
Format-List
```

**Observed result:** No output was returned.

- **4720** — A user account was created.
- **4732** — A member was added to a security-enabled local group.

The absence of matching results from this query does **not** prove no accounts were created or group memberships changed. Auditing, log retention, where events are recorded, and `-ErrorAction SilentlyContinue` can affect the output.

## 2. Review the local Administrators group

I checked which accounts currently have local administrator membership:

```powershell
Get-LocalGroupMember -Group "Administrators" |
Select-Object Name, ObjectClass, PrincipalSource |
Format-Table -AutoSize
```

**Actual result (personal details redacted):**

```text
Name                     ObjectClass  PrincipalSource
<HOST>\Administrator     User         Local
<HOST>\<MY_ACCOUNT>      User         MicrosoftAccount
```

The output identified two accounts in the local Administrators group:

1. The local `Administrator` account.
2. My Microsoft-linked Windows account.

**Interpretation:** Current group membership shows which principals have membership now. It does **not** establish when the accounts were created, when they joined the group, or whether a privilege change was authorised. A local Administrator account being listed in this group is not automatically suspicious.

## 3. Check whether the built-in Administrator account is enabled

```powershell
Get-LocalUser -Name "Administrator" |
Select-Object Name, Enabled, LastLogon
```

**Actual result:**

```text
Name           Enabled LastLogon
Administrator  False   23/05/2024 13:23:58
```

The `Administrator` account reported **Enabled = False**, meaning it was disabled when checked and could not ordinarily be used to sign in in that state. Its last reported logon was **23 May 2024 at 13:23:58**. That historic timestamp alone does not establish a compromise or tell us the reason for the prior sign-in.

**Scope limitation:** This command queried the account *by name*. On a machine where the built-in account has been renamed, identifying the built-in Administrator conclusively would require checking the account SID ending in `-500`. The investigation did not perform that additional check.

## 4. Simulated SOC scenario - New administrator account

*Training scenario only; this was not observed on my computer.*

- Event **4720** indicates that an account called `support_backup` was created.
- Event **4732** shows that the account was added to the local Administrators group.
- Event **4624** shows that the account later signed in successfully.

**Analyst approach:** Investigate which account created the user, which group it joined, when it was used, and whether the activity was approved by IT. Account creation followed by admin-group membership and login may be legitimate provisioning or an attempt to establish persistent access; the events alone do not determine intent.

## SOC investigation summary - Real endpoint

**Title:** Review of account creation telemetry and local administrator access  
**Severity:** Low concern on the evidence reviewed  
**Status:** No unauthorised account creation or privilege change established

### Evidence

- The last-30-days query for Security Events 4720 and 4732 returned no matching output.
- The local Administrators group contained two user entries: `Administrator` and a Microsoft-linked personal account (redacted).
- The account named `Administrator` reported `Enabled = False`.
- Its `LastLogon` property reported **23 May 2024, 13:23:58**.

### Assessment

The inspected output is consistent with ordinary local administrator configuration. The disabled `Administrator` account presents no immediate sign-in exposure through that account in its current state. No evidence of a recently created unauthorised account or administrator membership change was found in the *queried records*.

The available output is limited: historical account/group events may be absent from this machine's logs or outside the queried interval. The account SID was not verified.

### Possible follow-up checks

- Check account SIDs, including the `-500` built-in Administrator account, if needed.
- Review relevant account-management events on the appropriate machine or domain controller when a specific alert warrants it.
- Examine group changes and successful logons together to determine whether access was authorised.

**Disposition:** No immediate escalation based on the current evidence.

## Key lessons

- **4720:** account created; **4732:** member added to a local security group; **4624:** successful logon.
- `Get-LocalGroupMember` shows **current group membership**, not account creation or group-join history.
- `Get-LocalUser` shows current local account properties, including `Enabled` and `LastLogon`.
- Administrator membership does not automatically mean an account is active, newly created, or malicious.
- Empty event queries are not proof that no historical change ever happened.
- Distinguish observed evidence, possible interpretations, and remaining uncertainty in SOC reports.

> **Learning progress:** Day 50 investigation completed. Day 49 account-lockout catch-up was subsequently completed, bringing the total to **50 of 120 lessons (41.7%)**.
