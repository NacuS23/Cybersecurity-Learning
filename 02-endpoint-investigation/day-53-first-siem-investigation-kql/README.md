# Day 53 — First SIEM Investigation with KQL

**Topic:** Microsoft Sentinel, Kusto Query Language (KQL), and authentication alert triage  
**Environment:** Simulated sign-in dataset for SOC practice

## Objective

I focused on how a SOC analyst can review account sign-in activity in a SIEM, identify suspicious sequences, and determine what additional evidence is needed before classifying an event as an attack.

A **SIEM (Security Information and Event Management)** centralises logs and alerts from multiple systems. Instead of checking individual Windows computers, analysts can query events from many devices and services in one place.

## 1. Understanding KQL

I studied this example query for Microsoft Entra sign-in records in a Microsoft Sentinel environment:

```kql
SigninLogs
| where TimeGenerated > ago(24h)
| where ResultType != "0"
| project TimeGenerated, UserPrincipalName, IPAddress, ResultType
```

- `SigninLogs`: the Entra sign-in log table
- `where`: filters records
- `ago(24h)`: limits results to the previous 24 hours
- `ResultType != "0"`: selects outcomes other than a successful sign-in (not necessarily just wrong-password attempts)
- `project`: chooses fields to display

**Important detail:** This query filters out successful logins. To investigate failures **followed by a success**, I would need to include successful sign-ins as well.

Example query to review all sign-in outcomes for one account (for a Sentinel environment where the table exists):

```kql
SigninLogs
| where TimeGenerated > ago(24h)
| where UserPrincipalName == "alex@example.com"
| project TimeGenerated, UserPrincipalName, IPAddress,
          ResultType, AppDisplayName, ConditionalAccessStatus
| order by TimeGenerated asc
```

The UPN above is a placeholder. These are example queries; the lesson did **not** include execution against a live Sentinel workspace.

## 2. SOC scenario: failed sign-ins followed by success

The following is a **simulated** training dataset. The IP addresses belong to documentation ranges, not real threat indicators.

| Time | User | IP address | Sign-in result |
| --- | --- | --- | --- |
| 09:00 | alex | 203.0.113.45 | Failed |
| 09:01 | alex | 203.0.113.45 | Failed |
| 09:02 | alex | 203.0.113.45 | Failed |
| 09:03 | alex | 203.0.113.45 | Failed |
| 09:04 | alex | 203.0.113.45 | Failed |
| 09:05 | alex | 203.0.113.45 | Success |
| 09:06 | sam | 192.0.2.20 | Success |

### Q1. Which account should be investigated first?

**Alex.** The account shows five consecutive failures and then one successful sign-in from the same IP address. Sam has only a single successful sign-in in this dataset, with no accompanying suspicious pattern.

### Q2. Why is the sequence suspicious?

Repeated failed attempts immediately followed by a successful login may indicate password guessing that eventually succeeded. However, it could also mean a legitimate employee entered the wrong password several times and then corrected it.

**The pattern requires investigation; it is not proof of account compromise.**

### Q3. What evidence would help verify the successful login?

I would investigate:

1. **User confirmation:** Does Alex recognise the sign-in and its time?
2. **Source context:** Is the IP address typical for Alex? What device and client application were used?
3. **Authentication details:** Was multifactor authentication requested and completed? Were any Conditional Access policies applied?
4. **Historical activity:** Does the sign-in differ from the account's normal pattern?
5. **Post-login activity:** Were there unusual downloads, mailbox changes, privilege changes, or related alerts?

I would compare the relevant log records, not jump to conclusions based on the failed-login count alone.

## 3. SOC investigation summary

**Alert:** Multiple failed sign-ins followed by a success  
**Affected identity:** `alex` (simulated)  
**Sequence:** Five failures from 09:00 to 09:04, followed by a success at 09:05 from the same example IP  
**Initial assessment:** Suspicious authentication pattern; **compromise not confirmed**  
**Priority:** Prompt triage based on organisational policy and account importance  
**Recommended next step:** Verify with the account owner and correlate sign-in context, MFA, device history, and subsequent activity  
**Escalation:** Follow incident-response procedures if findings indicate unauthorised access

**Current disposition:** Further evidence needed. Do not close as benign or label as a confirmed attack without verification.

## Key takeaways

- SIEM platforms help analysts investigate events across multiple systems.
- KQL uses operators such as `where`, `project`, and `order by` to query security data.
- When investigating a failure-then-success sequence, include **both failed and successful outcomes**.
- A suspicious pattern is not the same as a confirmed compromise.
- A useful SOC ticket explains the observed evidence, uncertainties, and next investigative actions.

**Progress:** Day 53 learning exercise completed — **53/120 lessons (44.2%)**, 67 remaining.
