# Day 41 - DNS investigation and Windows logging

Today I investigated real Windows DNS cache entries, checked which DNS monitoring logs were available, and practised analysing a simulated PowerShell-to-network incident. The most important lesson was that **a DNS lookup, a network connection, a file download and execution are separate actions that need separate evidence**.

## Practical 1 - Inspect the local DNS cache

I used this read-only PowerShell command:

```powershell
Get-DnsClientCache |
Select-Object -First 10 Entry, Type, Data, TimeToLive |
Format-Table -AutoSize
```

Some of the actual cached results:

| Entry | Record type | Data |
| --- | --- | --- |
| cache8-lhr1.steamcontent.com | A (1) | 162.254.196.15 |
| cmp1-iad1.steamserver.net | A (1) | 162.254.192.98 |
| settings-win.data.microsoft.com | CNAME (5) | atm-settingsfe-prod-geo2.trafficmanager.net |
| events.telemetry.data.nvidia.com | A (1) | 18.198.233.49 |
| crl.globalsign.com | CNAME (5) | ocsp.globalsign.com |

Other entries related to Steam infrastructure and Microsoft Azure services.

**Assessment:** The names were consistent with normal Steam, Microsoft, NVIDIA and certificate infrastructure activity. A cached record alone does not prove that a connection was made, a file was transferred or a process behaved maliciously. Cache entries also do not normally identify the requesting process.

### DNS record types learned

- **A:** Maps a domain to an IPv4 address. Mnemonic: *A = Address*.
- **CNAME:** Maps a domain (alias) to another domain name.
- **SOA (Start of Authority):** Contains administrative information about a DNS zone, not a step in an alias chain.

Windows DNS cache showed types numerically, including `1` for A and `5` for CNAME.

## Practical 2 - Check for Sysmon DNS telemetry

Sysmon can record DNS query events as **Event ID 22** when it is installed and configured to do so.

I checked the standard Sysmon Operational log:

```powershell
Get-WinEvent -ListLog 'Microsoft-Windows-Sysmon/Operational' -ErrorAction SilentlyContinue |
Select-Object LogName, IsEnabled, RecordCount
```

**Result:** No output. The standard Sysmon Operational log was not found through that query. I did not confirm whether other monitoring software or a custom Sysmon setup was present.

## Practical 3 - Check built-in DNS Client logging

```powershell
Get-WinEvent -ListLog 'Microsoft-Windows-DNS-Client/Operational' |
Select-Object LogName, IsEnabled, RecordCount
```

Actual result:

```text
LogName                                  IsEnabled
Microsoft-Windows-DNS-Client/Operational     False
```

This Windows DNS Client Operational log was disabled at the time of inspection. DNS resolution still functions, but this log did not provide the historical query records we would need for a process-level investigation.

I **did not** enable logging, install Sysmon or change any settings.

## Practical 4 - Follow a CNAME chain

I used:

```powershell
Resolve-DnsName settings-win.data.microsoft.com |
Select-Object Name, Type, NameHost, IPAddress |
Format-Table -AutoSize
```

The actual resolution included:

```text
settings-win.data.microsoft.com
  CNAME -> atm-settingsfe-prod-geo2.trafficmanager.net
  CNAME -> settings-prod-wus2-1-tagged.westus2.cloudapp.azure.com
  A     -> an IPv4 address (truncated in the displayed output)
```

The command also displayed an SOA record for `westus2.cloudapp.azure.com`.

**Interpretation:** The resolver followed aliases from the original name to another hostname, then reached an IPv4 A record. DNS answers can differ between queries, locations and times.

## Simulated SOC case - DNS, PowerShell and a new executable

This is **training data, not activity observed on my own computer**.

On `FINANCE-PC-08`:

```text
14:15 - powershell.exe, PID 6200, queries updates-check.example.com
14:16 - same PID establishes a TCP connection to 203.0.113.45:443
14:17 - unsigned update.exe appears in a user temporary folder
       - no authorised update was recorded by IT
```

### SOC ticket

**Title:** Suspicious DNS and outbound PowerShell connection followed by file creation.

**Priority:** High.

**Evidence:**
- PowerShell PID 6200 made the DNS query and owned the later network connection.
- A new unsigned executable appeared shortly afterwards in a temporary directory.
- IT had no record of an approved update at that time.

**Assessment:** Possible unauthorised PowerShell activity and payload download. The current evidence **does not** yet prove that this specific connection downloaded the file, that the executable ran, or that persistence was established. Port 443 is not inherently safe or malicious.

**Next steps:**
1. Correlate full DNS, network and file-creation telemetry, including timestamps and process context.
2. Calculate the executable's SHA256 hash and check permitted reputation sources, e.g. VirusTotal hash lookup; do not upload confidential files to public scanners.
3. Investigate whether the executable was launched and which process created it.
4. Check for persistence through scheduled tasks, services and startup entries.
5. Verify activity with IT and consider containment using the organisation's incident-response procedure.

**Decision:** Escalate promptly for investigation.

## Key takeaways

- `Get-DnsClientCache` shows cached DNS responses, not proof of a website visit or download.
- `Resolve-DnsName` can show A, CNAME and SOA records in a resolution.
- A records point to **IPv4 addresses**; CNAME records point to **other hostnames**.
- Sysmon Event 22 can provide DNS and process context if that logging exists and is configured.
- My standard Sysmon log was not found, and Windows DNS Client Operational logging was disabled.
- Matching PIDs and close timestamps strengthen a hypothesis, but file downloads and execution require additional evidence.
- An unsigned executable in a temporary folder after unexpected PowerShell networking warrants investigation; its presence alone does not prove that it ran.
