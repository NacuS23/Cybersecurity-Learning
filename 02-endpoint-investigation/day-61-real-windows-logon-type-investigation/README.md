# Day 61 — Real Windows Security Logon-Type Investigation

**Date:** 24 November 2026  
**Evidence type:** User-executed, read-only PowerShell queries against actual Windows Security logs  
**Status:** Investigation of event types and counts completed; account-level correlation not performed  
**Privacy:** Only aggregate counts, event IDs and event timestamps are documented. No account names, IP addresses, machine names or raw Security logs were uploaded.

## Objective

Check whether Windows is recording successful and unsuccessful logons, identify which kinds of successful logons are present, and avoid confusing service activity with human interactive sign-ins.

This is a **real endpoint data investigation reported by the learner**, unlike the simulated KQL cases from Days 53–58. The results below are copied from PowerShell output supplied by the learner; the assistant did not connect to the learner's Windows computer or independently run the commands.

## 1. Initial unexpected result

The initial read-only query for Event IDs 4624/4625 in the previous 24 hours returned:

```text
Get-WinEvent : No events were found that match the specified selection criteria.
FullyQualifiedErrorId : NoMatchingEventsFound,Microsoft.PowerShell.Commands.GetWinEventCommand
```

This means the query at that moment returned no matching records; it is **not** evidence that audit logging was disabled or that no sign-ins existed.

## 2. Verify Security log and recent event IDs

The learner ran:

```powershell
Get-WinEvent -ListLog Security |
Select-Object LogName, IsEnabled, RecordCount

Get-WinEvent -LogName Security -MaxEvents 10 |
Select-Object TimeCreated, Id
```

**Observed:**

| LogName | IsEnabled | RecordCount |
| --- | --- | ---: |
| Security | True | 36535 |

The 10 newest listed events, reported in local Windows time on 24 November 2026, were:

| Time | Event ID | Number of rows |
| --- | --- | ---: |
| 16:34:57 | 5379 | 6 |
| 16:33:00 | 4672 | 2 |
| 16:33:00 | 4624 | 2 |

Interpretation:
- **4624:** A successful logon session was created.
- **4672:** Special privileges were assigned to a new logon. It can occur during legitimate SYSTEM or privileged-account activity and requires context.
- **5379:** Credentials were read from Windows Credential Manager. This is not independently proof of credential theft.

**Key finding:** Security auditing was enabled and Event 4624 records demonstrably existed. It is possible that the newly observed 4624 records were written after the first failed search; the exact explanation for that earlier result was **not established**.

## 3. Query the last 24 hours for 4624/4625

The learner ran:

```powershell
Get-WinEvent -FilterHashtable @{
    LogName = 'Security'
    Id = 4624,4625
    StartTime = (Get-Date).AddHours(-24)
} -MaxEvents 2000 -ErrorAction SilentlyContinue |
Group-Object Id |
Select-Object Name, Count
```

**Reported output:**

| Event ID | Returned records |
| --- | ---: |
| 4624 | 65 |
| 4625 | 0 shown (no group returned) |

This query produced no group for 4625, so **no matching failed logon records were returned by that particular query at that time**. It does not prove that failed logon activity could never have occurred, or that all relevant authentication telemetry is present.

## 4. Break down successful logons by LogonType

The learner independently ran a second query which used `Get-WinEvent` to collect 4624s from the last 24 hours, parsed each event's XML `LogonType` field by name, and grouped the results.

**Reported results:**

| LogonType | Microsoft event classification | Count | Approximate share of 68 |
| --- | --- | ---: | ---: |
| 5 | Service | 55 | 80.9% |
| 7 | Unlock | 4 | 5.9% |
| 11 | CachedInteractive | 6 | 8.8% |
| 2 | Interactive | 3 | 4.4% |
| **Total** | | **68** | **100%** |

According to Microsoft's Event 4624 documentation:

- **5 (Service):** Service Control Manager initiated a logon for a service account.
- **7 (Unlock):** The workstation was unlocked.
- **11 (CachedInteractive):** Interactive logon using cached credentials on the computer; this does **not** by itself prove that the computer is domain joined or that access was malicious.
- **2 (Interactive):** A local interactive sign-in.

No type 3 (Network) or type 10 (RemoteInteractive) events appeared in this returned **68-event** distribution. This supports only a statement about the observed query result, not a categorical claim that no remote access ever occurred.

### Count discrepancy

An earlier command returned **65** type-4624 events, while the later `LogonType` breakdown totals **68**. These were separate commands executed at different times, each with a rolling 24-hour selection; new events or the moving search window could explain the difference. The exact cause was not independently verified.

## 5. SOC assessment

**Observations:**
- Security log enabled with 36,535 records at the time of its status check.
- Successful logon activity was present.
- The majority of the most recent grouped successful logons were **Service** (55 of 68).
- Local/interactive or cached interactive activity and workstation unlocks also occurred.
- The separate failure search showed no matching 4625 entries.

**Interpretation:** The type breakdown is compatible with ordinary operating-system service and workstation activity. There is **no specific attack indicator in these aggregate counts alone**.

**Limitations:** Aggregate counts omit target account identity, service name, device context, Logon IDs, source addresses, MFA and surrounding event timing. A privileged logon (4672) or Credential Manager read (5379) needs context before assigning suspicion. Absence of 4625 results from one query is not assurance that the device is secure.

**Disposition:** Low concern *on the evidence reviewed*, with no confirmed intrusion. No containment, password resets or changes to Windows auditing are indicated solely by these counts.

## 6. Learning outcomes

- Confirm that Event 4624 and Event 4625 queries are actually retrieving data.
- Distinguish an empty query result from disabled Security auditing.
- Interpret different logon types rather than counting every successful event as a human login.
- Verify that separate time-scoped queries can give slightly different totals.
- Build a defensible SOC note that clearly separates **observed events**, **reasonable interpretations** and **unknowns**.

## 7. Further practical work

For a future session, investigate service-logon activity using privacy-safe summaries, then selectively correlate a relevant `4624` event with `4672` by **Logon ID** and timeline rather than guessing which event belongs to which session.

**No additional data is needed to document the completed Day 61 aggregate analysis.** Keep raw Security events and identifiers private.

## References

- [Microsoft Learn — Event 4624 (successful logon)](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4624)
- [Microsoft Learn — Event 4672 (privileges assigned)](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4672)
- [Microsoft Learn — Event 5379 (Credential Manager read)](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-5379)

[Back to SOC portfolio](../../README.md)
