# Windows Security Event Log investigation

**Date:** 20 September 2026  
**Type:** Hands-on Windows SOC practice  
**Focus:** Authentication events, privileged logons, event correlation and process auditing

## Objective

Use Windows Security logs to investigate successful logons, identify logon types, distinguish local activity from remote activity, correlate related events with Logon IDs, and review process creation auditing.

## What I investigated

### Successful logons — Event ID 4624

I reviewed recent successful logon events and identified several different logon types.

Key observations:

- **Logon Type 5** was associated with Windows service activity.
- **Logon Type 2** appeared in Windows session-related activity and showed why a logon type should not be interpreted without checking the account, process and context.
- **Logon Type 7** was associated with unlocking an existing user session.
- **Logon Type 11** appeared as cached interactive authentication.
- Local loopback activity used `127.0.0.1`, which represents the local computer rather than a remote host.

I also checked the process involved in authentication events and reviewed whether a remote source address was present.

### Failed logons — Event ID 4625

I queried the Security log for failed logon events.

No Event ID 4625 records were found in the currently retained Security log.

This does not prove that failed authentication has never happened; it only means there were no matching events available in the retained logs at the time of the investigation.

### Privileged logons — Event ID 4672

I reviewed Event ID 4672, which records special privileges assigned to a new logon.

The events included Windows SYSTEM activity and an elevated user session.

Privileges observed included examples such as:

- `SeTakeOwnershipPrivilege`
- `SeBackupPrivilege`
- `SeRestorePrivilege`
- `SeDebugPrivilege`
- `SeLoadDriverPrivilege`

These privileges alone are not evidence of malicious activity. Context and event correlation are required.

## Event correlation with Logon ID

I correlated a privileged Event ID 4672 with its related Event ID 4624 by matching the **Logon ID**.

This allowed me to connect:

`4672 privileged session → Logon ID → 4624 successful logon → logon type/process/source`

The correlated event showed:

- Logon Type 7
- an elevated token
- `C:\Windows\System32\lsass.exe`
- no remote source network address

This supported a local session-unlock explanation rather than a remote login.

## Process creation — Event ID 4688

I reviewed retained Event ID 4688 process creation events.

The events showed a normal Windows startup sequence involving processes such as:

- `smss.exe`
- `wininit.exe`
- `csrss.exe`
- `services.exe`
- `lsass.exe`
- `LsaIso.exe`
- `autochk.exe`

The parent-child relationships were consistent with normal Windows startup behaviour.

The `Process Command Line` field was blank in the retained events, reducing the amount of context available for analysis.

## Audit policy check

I checked the Process Creation audit policy with:

```powershell
auditpol /get /subcategory:"Process Creation"
```

The system reported:

```text
Process Creation    No Auditing
```

This explained why fresh Event ID 4688 records were not being generated during the session.

## Commands used

```powershell
Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4624} -MaxEvents 5 |
Format-List TimeCreated, Id, Message

Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4625} -MaxEvents 10 |
Format-List TimeCreated, Id, Message

Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4672} -MaxEvents 5 |
Format-List TimeCreated, Id, Message

Get-WinEvent -FilterHashtable @{LogName='Security'; ID=4688} -MaxEvents 10 |
Format-List TimeCreated, Id, Message

auditpol /get /subcategory:"Process Creation"
```

## What I learned

- A successful logon event must be interpreted in context; the Event ID or logon type alone is not enough.
- Logon Type 7 indicates an unlock of an existing session.
- `127.0.0.1` is the loopback address and represents the local computer.
- The absence of a remote source address can help distinguish local activity from remote activity, but conclusions should remain evidence-based.
- Event ID 4672 indicates special privileges were assigned, not that malicious activity occurred.
- Logon IDs are useful for correlating related Security events.
- Event ID 4688 can reveal process creation and parent-child relationships.
- Audit policy configuration directly affects what evidence is available in Windows Security logs.
- A missing event is not proof that an action never happened; it may mean auditing was disabled or the event is no longer retained.

## Privacy

Account names, email addresses, Security Identifiers, machine-specific identifiers and other personal values have been removed or generalized from this public write-up.

## SOC relevance

This exercise practised a core SOC workflow: collect authentication evidence, classify the logon type, check the account and process involved, look for remote indicators, correlate related events, and document conclusions without overstating what the evidence proves.
