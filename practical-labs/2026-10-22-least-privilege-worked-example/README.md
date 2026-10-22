# Fictional access review: applying least privilege

Date: 22 October 2026

**Assisted worked example:** This solution was prepared with ChatGPT at my request as a study reference. It is not an independently completed assessment or a review of a real company's accounts. No permissions were changed.

## Objective and core idea

Identify permissions that exceed what an account needs for its job. Least privilege means providing only the access needed, for only as long as needed.

Authentication checks identity; authorisation determines permitted actions. Excess permissions increase the possible impact of account compromise, but do not prove compromise.

## Supplied fictional scenario

Assume these job requirements are complete and Lee's contract has not been extended.

| Account | Job requirement | Current access |
|---|---|---|
| `alex-support` | Read support guides | Read and edit support guides |
| `maya-finance` | Read and update payroll | Read and edit payroll |
| `backup-service` | Read payroll files to make backups | Read payroll and manage payroll permissions |
| `lee-contractor` | Edit project documents until 17 October | Edit project documents; access remains active on 22 October |

## Worked access review

| Account | Access needed | Extra or expired access | Smallest recommended change |
|---|---|---|---|
| `alex-support` | Read support guides | Edit support guides | Remove Edit and retain Read. |
| `maya-finance` | Read and edit payroll | None shown | Keep the listed access. It matches the documented task. |
| `backup-service` | Read payroll for backups | Manage payroll permissions | Remove Manage permissions and retain Read. |
| `lee-contractor` | Project access only until 17 October | Project access has expired but remains active | Revoke project access. If the account has no remaining authorised purpose, request account disabling through the offboarding process. |

These recommendations follow the simplified requirements. In a real environment, confirm dependencies with the resource owner, obtain the required approval, and check that authorised work still functions after a change. A backup product may have additional documented requirements not present in this exercise.

## Example SOC note

**Observed fact:** The fictional `backup-service` account can read payroll files and manage payroll permissions, although its documented task requires only reading payroll for backups.

**Risk:** If misused or compromised, the account could change who can access payroll. That adds risk beyond the access needed to perform backups. The supplied evidence does not show that this has happened.

**Verification before a change:** Confirm the service's requirements with the backup owner and check whether it genuinely needs permission-management rights. Review how the access is granted, including group membership, so the proposed change targets the correct source.

**Recommendation:** Under the exercise assumptions, request removal of permission-management rights while retaining the required read access; verify backup operation after the approved change.

## Knowledge-check answers

1. **Is reducing unnecessary permissions mainly authentication or authorisation?** Authorisation: it changes what an account is allowed to do, not how it proves its identity.
2. **Why is Manage permissions powerful?** It can allow an account to grant or remove access for other accounts, potentially exposing sensitive resources or disrupting legitimate access.
3. **Does excess access prove misuse?** No. It might result from a configuration mistake, outdated role assignment or incomplete offboarding. Activity logs and other evidence are needed to investigate misuse.
4. **What should replace giving everyone administrator access?** Give access based on each person's job. Identify the specific permission needed when someone is blocked, obtain approval, and grant only that access. Where elevated access is genuinely required, use a controlled, time-limited approach where supported instead of permanent administrator access for everyone.

## Takeaway

Compare the job requirement with actual access, identify the gap, explain the risk, and recommend the smallest justified change. A permissions problem is a finding to investigate, not automatic proof of an attack.
