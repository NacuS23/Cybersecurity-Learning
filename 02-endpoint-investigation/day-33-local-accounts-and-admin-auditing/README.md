# Day 33 - Local accounts and administrator auditing

Today I checked which accounts have local administrator access on Windows, whether the local accounts are enabled, and whether Windows is set up to audit account changes. I also completed a simulated SOC alert involving an unexpected administrator account.

## Inspecting local Administrators group membership

I used:

```powershell
Get-LocalGroupMember -Group "Administrators"
```

The group contained two entries:

- `MSI\Administrator` — local account
- `MSI\nacu_` — Microsoft-linked account

Only the accounts I expected appeared in the group. Membership alone does not mean that an account is currently logged on or running an elevated process.

## Reviewing local accounts

```powershell
Get-LocalUser |
Select-Object Name, Enabled, LastLogon
```

Results:

| Account | Enabled |
| --- | --- |
| Administrator | False |
| DefaultAccount | False |
| Guest | False |
| nacu_ | True |
| WDAGUtilityAccount | False |

The built-in and Windows-managed accounts shown were disabled, while my usual account was enabled. The `LastLogon` field for my account was blank; that does not mean the account was never used.

**Initial finding:** No unexpected enabled local accounts or extra local administrators identified.

## Looking for account-creation and group-change events

Useful Security event IDs:

- **4720** — A user account was created
- **4732** — A member was added to a security-enabled local group (check the actual group to see whether it was Administrators)
- **4624** — A successful logon (Logon Type 10 indicates remote interactive/RDP)

My event query:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName='Security'
    Id=4720,4732
} -MaxEvents 10 |
Select-Object TimeCreated, Id, Message
```

No matching 4720 or 4732 records were found in the available log. This does **not** prove such activity has never happened; log retention and coverage matter.

## Confirming the audit policy

```powershell
auditpol /get /category:"Account Management"
```

Relevant settings:

```
Security Group Management   Success
User Account Management     Success
Computer Account Management No Auditing
Other Account Management Events No Auditing
```

Successful user-account and security-group management actions are configured to be audited. This makes those events useful for future investigations, subject to event retention and the applicable audit scope.

## Simulated SOC investigation (training case, not activity observed on my PC)

**Alert:** Unexpected administrator account on FINANCE-PC-07.

Timeline:

```
02:15 - Event 4720
New account BackupSupport created by Administrator

02:16 - Event 4732
BackupSupport added to local Administrators group

02:20 - Event 4624
BackupSupport successfully logs in by RDP (Logon Type 10)
from an unfamiliar external IP address
```

### SOC ticket

**Priority:** High.

**Evidence:**
- An unexpected account was created.
- The account was added to Administrators one minute later.
- It subsequently logged in remotely from an unfamiliar address.
- The sequence occurred within five minutes.

**Assessment:** Possible unauthorised account creation and privileged-account access, potentially involving account manipulation or persistence. The events require investigation to establish whether the changes were authorised.

**Next steps:**
- Ask the appropriate IT owner whether the account and changes were approved.
- Confirm the source of the RDP connection and who used the account.
- Examine event details for the account creation and group-membership change.
- Review logon and process activity following the RDP connection.
- Follow incident-response procedures if unauthorised activity is confirmed or strongly indicated.

**Decision:** Escalate promptly.

## What I want to remember

- Local Administrators membership is not the same as proof of active or abused admin privileges.
- `Get-LocalGroupMember` shows who belongs to a local group.
- `Get-LocalUser` shows local account status.
- Event **4720** = account created; **4732** = member added to a local security-enabled group.
- Event **4624**, Logon Type **10** = successful remote interactive logon.
- `auditpol` tells me what categories Windows is configured to audit.
- No matching events is not proof nothing ever happened.
- An unexpected new privileged account can be suspicious even before it is used.
- SOC next steps should name specific evidence to check, not just say "investigate further".
