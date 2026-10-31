# Cybersecurity Core Memory

This is my quick recap file. Each section can be opened and closed on GitHub.

<details>
<summary><strong>Day 1 - DNS, IP, ports and traceroute</strong></summary>

- DNS = domain name to IP address
- IPv4 uses dotted decimal
- IPv6 uses hexadecimal numbers separated by colons
- IP = network address/destination
- Port = service/application clue
- 443 = HTTPS
- A hop = one router/network step
- Basic flow: domain -> DNS -> IP -> route -> server

</details>

<details>
<summary><strong>Day 2 - TCP, UDP and connections</strong></summary>

- TCP = reliable, connection-oriented transport
- UDP = connectionless transport with no built-in delivery guarantee
- TCP handshake = SYN -> SYN-ACK -> ACK
- PID = Process ID
- ESTABLISHED = active TCP connection
- Network investigation flow: connection -> PID -> process -> service
- Suspicious-looking does not automatically mean malicious

</details>

<details>
<summary><strong>Day 3 - Private IP, DHCP, NAT and gateway</strong></summary>

- Private IPv4 ranges include 10.x.x.x, 172.16-31.x.x and 192.168.x.x
- Default gateway = route to other networks
- DHCP gives automatic network settings
- NAT allows private devices to communicate using a public-facing address
- Subnet mask decides what is local
- Ping can test reachability, but failure does not always prove the host is down

</details>

<details>
<summary><strong>Day 4 - MAC and ARP</strong></summary>

- MAC address = local network interface identifier
- ARP = IPv4 address -> MAC address
- ARP is used on the local network
- ARP spoofing = false IP-to-MAC mapping
- Media disconnected usually means an adapter exists but is not connected

</details>

<details>
<summary><strong>Day 5 - DNS records and cache</strong></summary>

- A = IPv4
- AAAA = IPv6
- CNAME = alias
- MX = mail server
- NS = name server
- DNS cache stores answers temporarily
- TTL = how long a DNS answer can be cached
- Weird-looking DNS names can still be normal CDN/service infrastructure

</details>

<details>
<summary><strong>Day 6 - Wireshark</strong></summary>

- Wireshark captures network packets
- dns filter = DNS traffic
- icmp filter = ping traffic
- tcp filter = TCP traffic
- SYN = start TCP connection
- SYN-ACK = server response
- ACK = completes handshake
- Retransmission = TCP sends data again
- Suspicious packet != automatically malicious

</details>

<details>
<summary><strong>Day 7 - Ports and listening services</strong></summary>

- LISTENING = waiting for connections
- ESTABLISHED = active TCP connection
- 443 = HTTPS
- 3389 = RDP
- 127.0.0.1 = localhost only
- 0.0.0.0 = all IPv4 interfaces
- [::] = all IPv6 interfaces
- Unknown port = investigate, not automatically malware

</details>

<details>
<summary><strong>Day 8 - Firewalls</strong></summary>

- Firewall = allows or blocks traffic using rules
- Inbound = traffic coming toward the computer
- Outbound = traffic leaving the computer
- Listening port != automatically exposed to the Internet
- 443 != automatically safe
- Companies often allow expected outbound traffic and restrict random inbound traffic

</details>

<details>
<summary><strong>Day 9 - Following a connection</strong></summary>

- Flow: domain -> DNS -> IP -> port -> PID -> process
- PID identifies a running process
- 443 normally means HTTPS
- One browser can have many HTTPS connections at once
- PID alone does not prove which exact website a connection belongs to
- Unknown process + unknown destination = investigate further

</details>

<details>
<summary><strong>Day 10 - HTTPS, TLS and certificates</strong></summary>

- HTTP/HTTPS = web protocols
- IPv4/IPv6 = addressing systems
- TLS = encryption/security layer
- HTTPS = HTTP protected by TLS
- 443 = HTTPS
- Certificate helps validate the server/domain
- HTTPS does not prove the website itself is trustworthy
- Wireshark normally cannot read encrypted HTTPS application data directly

</details>

<details>
<summary><strong>Day 11 - DNS security and NXDOMAIN</strong></summary>

- NXDOMAIN = domain/hostname does not exist
- One failed lookup is normal
- Lots of strange repeated DNS failures can be worth investigating
- DNS logs show which domains a device tried to contact
- Strange domain != automatically malware

</details>

<details>
<summary><strong>Day 12 - Traceroute and latency</strong></summary>

- Hop = one router/network step
- tracert shows the route to a destination
- First hop is usually the local gateway
- * * * = no reply, not automatically failure
- One high latency result does not prove a problem
- Look for patterns across later hops

</details>

<details>
<summary><strong>Day 13 - ARP security and cache</strong></summary>

- ARP = IPv4 address -> MAC address
- ARP does not encrypt traffic
- Dynamic ARP entries can be relearned automatically
- ARP cache can repopulate very quickly
- Gateway MAC change = investigate, not proof of attack
- One latency spike is not enough to diagnose a problem

</details>

<details>
<summary><strong>Day 14 - DHCP</strong></summary>

- DHCP = automatic network configuration
- It can provide IP address, subnet mask, gateway and DNS
- DHCP lease = temporary permission to use assigned configuration
- Lease expiry does not mean the IP must change
- DHCP does not encrypt traffic
- Unexpected DNS/gateway settings from DHCP should be investigated
- Remember: DHCP gives settings, DNS resolves names, HTTPS/TLS encrypts web traffic

</details>

<details>
<summary><strong>Day 15 - Subnets and routing</strong></summary>

- Subnet mask helps decide whether a destination is local or remote
- 255.255.255.0 = /24
- On this network, 192.168.0.x is local
- Local destination -> use ARP for the destination MAC
- Remote destination -> send to the default gateway
- 0.0.0.0/0 = default route
- Route table = which path traffic should use
- Quick memory: Subnet = local? ARP = which MAC? Gateway = where remote traffic goes?

</details>

<details>
<summary><strong>Day 16 - NAT and PAT</strong></summary>

- NAT = translate private/internal addressing to public-facing addressing
- PAT = use port mappings to keep many connections separate
- Many devices can appear to websites as the same public IP
- Source ports, timestamps and NAT logs can help identify the original connection
- 127.0.0.1 = localhost only
- 443 normally means HTTPS
- Quick memory: NAT = addresses, PAT = ports

</details>


<details>
<summary><strong>Day 17 - TCP vs UDP in real traffic</strong></summary>

- TCP = reliable, connection-oriented transport
- UDP = connectionless transport with no built-in delivery guarantee
- TCP retransmission = resend unacknowledged data
- UDP does not use TCP-style ESTABLISHED states
- DNS usually uses UDP port 53 for normal queries
- HTTPS normally uses TCP port 443
- Wireshark can help compare TCP and UDP traffic directly

</details>


<details>
<summary><strong>Day 18 - SOC-style connection investigation</strong></summary>

- Start with the connection, then identify the PID and process
- 443 normally means HTTPS, but not automatically safe
- Check executable path for context
- Check digital signature for authenticity evidence
- Reverse DNS failure does not automatically mean malicious
- Stronger conclusion comes from combining several pieces of evidence
- Useful flow: connection -> PID -> process -> path -> signature -> destination context

</details>


<details>
<summary><strong>Day 19 - Process investigation</strong></summary>

- PID = Process ID
- Parent process = what launched the process
- Executable path helps show whether a process is running from an expected location
- Signature status is supporting evidence, not absolute proof
- NotSigned does not automatically mean malicious
- Microsoft Store apps can be checked with Get-AppxPackage
- SignatureKind: Store + Status: Ok gives useful package-level context
- Temp/AppData executables can deserve more investigation depending on context

</details>


<details>
<summary><strong>Day 20 - Windows services and persistence</strong></summary>

- Service = background program
- Auto = configured to start automatically
- PathName = what executable actually runs
- Persistence = ability to survive/restart after reboot
- Auto-start + strange path = investigate
- LocalSystem = high privilege, not automatically malicious
- Service name, path, startup mode and account should be checked together

</details>


<details>
<summary><strong>Day 21 - Startup programs and persistence</strong></summary>

- Persistence = survives/restarts after reboot or login
- HKLM\...\Run = common startup registry location
- Command = what executable is launched
- Path = where the startup executable is running from
- Valid signature = useful evidence, not absolute proof
- Microsoft Windows Hardware Compatibility Publisher is consistent with properly signed driver software
- Temp/AppData startup executable = investigate further

</details>



<details>
<summary><strong>Day 22 - Scheduled tasks and persistence</strong></summary>

- Scheduled tasks can run on startup, logon, a schedule, or an event
- Scheduled tasks can be used for normal automation or persistence
- Check TaskPath, action, trigger, and run history
- Some tasks use COM handlers rather than an executable path
- Investigated the .NET Framework NGEN task
- Task had a COM handler and a nonzero last result
- A failed task does not automatically mean malicious activity

</details>

<details>
<summary><strong>Day 23 - Triage prioritisation</strong></summary>

- Triage = decide what should be investigated first
- Several suspicious indicators together matter more than one field alone
- Check path, parent, command line, signature, network destination and persistence
- Successful execution does not mean legitimate execution
- Temp/AppData + unsigned + persistence = higher priority
- Word -> PowerShell + encoded command + external connection = very high priority
- Useful questions: Where is it? Who launched it? What is it doing? Where is it connecting? Does it come back?

</details>


<details>
<summary><strong>Day 24 - Windows Security event log investigation</strong></summary>

- 4624 = successful logon
- 4625 = failed logon
- 4688 = process creation
- Logon Type 2 = local / interactive
- Logon Type 3 = network
- Logon Type 10 = RDP / remote interactive
- Main checks: Event ID -> Account -> Logon Type -> Source IP -> Failure reason -> Caller process -> Frequency
- One failed logon with no remote IP and a legitimate local process is usually low priority
- Verified msedgewebview2.exe from the expected Microsoft Edge WebView Program Files path
- Authenticode signature was Valid and signed by Microsoft Corporation
- Filename alone is weak evidence; path + signature + behaviour + event pattern is much stronger

</details>


<details>
<summary><strong>Day 25 - Process creation and parent-child relationships</strong></summary>

- 4688 = a new process has been created
- Check: child process -> parent -> command line -> path -> signature -> network behaviour
- Parent-child relationships help show whether process execution makes sense
- smss.exe -> autochk.exe can be normal Windows startup activity
- smss.exe -> csrss.exe can be normal Windows startup activity
- WINWORD.EXE -> powershell.exe with Bypass + EncodedCommand is high priority
- Legitimate process names can still be abused
- Investigated WUDFHost.exe in System32
- Signature was Valid and signed by Microsoft Windows
- Parent was services.exe
- services.exe -> WUDFHost.exe was consistent with normal Windows behaviour
- Several reassuring signals together can justify low-priority / likely-benign triage

</details>


<details>
<summary><strong>Day 26 - PowerShell logging and command building</strong></summary>

- 4104 = PowerShell Script Block Logging
- 40961/40962 = PowerShell console startup/ready events
- Large 4104 logs can be normal and may be split into several parts
- Filter first instead of reading pages of PowerShell output
- Interesting terms include EncodedCommand, ExecutionPolicy Bypass, Invoke-WebRequest, Invoke-Expression and external URLs
- One keyword alone does not prove malicious activity
- Learn PowerShell by understanding each command part, not memorising full commands
- Core SOC commands: Get-Process, Get-CimInstance, Get-NetTCPConnection, Get-WinEvent, Get-AuthenticodeSignature, Get-FileHash
- Select-Object chooses fields, Where-Object filters, | passes output to the next command
- Get-Help can be used when syntax is forgotten
- From now on, gradually build commands independently instead of only copying them

</details>


<details>
<summary><strong>Day 27 - File hashes and reputation</strong></summary>

- Get-FileHash calculates a file hash
- SHA256 can be used as a fingerprint for an exact file
- Same exact file = same SHA256 hash
- VirusTotal can search a hash without scanning my computer
- 0/70 detections is reassuring, not proof of safety
- Unknown hash does not automatically mean malicious
- Reputation is supporting evidence, not the final decision
- For suspicious files check: path -> parent -> signature -> command line -> behaviour -> network -> persistence -> hash/reputation
- WUDFHost.exe had expected path, valid Microsoft signature, sensible parent and 0/70 detections, so it looked likely benign

</details>

<details>
<summary><strong>Day 28 - PowerShell filtering and connection investigation</strong></summary>

- Where-Object filters records using a condition
- $_ = the current object being examined
- Select-Object chooses fields/columns
- Useful flow: collect -> filter -> select -> display
- ESTABLISHED = active TCP connection, not proof of safety
- Map OwningProcess PID -> process -> path -> signature
- Valid Microsoft path + signature strongly supports executable legitimacy
- Process legitimacy and destination safety are separate questions
- Remote IP/port provide destination context
- 443 normally means HTTPS, not automatically safe
- Reverse DNS failure does not automatically mean malicious
- DNS cache can help correlate a hostname with an IP
- Cloud/CDN infrastructure can serve many different websites
- Final SOC judgement should combine process, path, signature, destination and behaviour

</details>



<details>
<summary><strong>Day 28 - Microsoft Defender investigation</strong></summary>

- Get-MpComputerStatus checks Defender status
- AntivirusEnabled = True and RealTimeProtectionEnabled = True are reassuring
- 1116 = threat detected
- 1117 = Defender took action
- 5007 = Defender configuration changed
- 5007 is not automatically suspicious
- Always inspect the old value and new value
- UX configuration changes are different from protection being disabled
- No 1116/1117 events in the current log is reassuring, but not proof that no detection ever happened
- SOC conclusion should state evidence, assessment, next step and decision
- Current case: low priority, close

</details>


<details>
<summary><strong>Day 29 - Windows service installation investigation</strong></summary>

- 7045 = a service was installed in Windows
- 7045 does not automatically mean malware
- Check: service name -> file path -> start type -> account -> signature -> context
- Auto start = persistence
- LocalSystem = high privilege
- User mode service is not suspicious by itself
- Investigated MSI Center Service
- Path was under the expected MSI Program Files directory
- Signature was Valid and signer matched MICRO-STAR INTERNATIONAL CO., LTD.
- Service was still running and other MSI services were also present
- Final assessment: low priority / likely legitimate -> close
- Suspicious example: Temp path + auto start + LocalSystem + fake Windows-style name = escalate

</details>

<details>
<summary><strong>Day 30 - Service persistence validation</strong></summary>

- Auto-start service = persistence, not automatically malware
- LocalSystem = high privilege, so executable validation matters
- Check service -> startup mode -> account -> path -> signature -> PID -> running process
- Program Files path is generally more reassuring than a user-writable Temp/AppData path
- Privileged auto-start service from Temp/AppData = investigate further
- Investigated Adobe Acrobat Update Service
- Executable path matched the expected Adobe ARM location
- Signature was Valid and signer was Adobe Inc.
- Running armsvc process matched the configured service executable
- Final assessment: low suspicion / likely legitimate persistence -> no escalation

</details>



<details>
<summary><strong>Day 30 - Windows event correlation</strong></summary>

- Event correlation = connecting events by time, account, process, machine and other evidence
- 4624 = successful logon; 4688 = new process; 7045 = service installed
- Logon Type 10 = remote interactive (RDP)
- Close timestamps are a clue, not proof events were caused by the same activity
- Checked four MSI-related services installed within 25 seconds
- All four executables had Valid signatures from Micro-Star International
- Auto start and LocalSystem can be legitimate, but matter when assessing persistence and privilege
- SOC conclusion: likely benign MSI installation activity; low priority; close
- Digital signatures support authenticity but do not prove behaviour is safe

</details>


<details>
<summary><strong>Day 31 - Scheduled task investigation</strong></summary>

- Task Scheduler Operational event IDs: 106 = registered, 140 = updated, 200 = action started, 201 = action completed
- The Operational log was disabled; missing events do not mean tasks were never created or run
- Get-ScheduledTask lists existing tasks
- Task **action** = what executes; **trigger** = when it executes
- Investigated OneDC_Updater: expected MSI updater executable path
- Digital signature was Valid and signer matched Micro-Star International
- Enabled logon and daily triggers were consistent with updater activity
- Ready = waiting for a trigger, not currently running
- An old StartBoundary is not necessarily the task creation date
- SOC conclusion: low priority / likely benign, close based on evidence; historical executions not verified

</details>


<details>
<summary><strong>Day 32 - ATT&CK and analyst triage</strong></summary>

- Tactic = an objective; technique = a way of achieving it
- Persistence means keeping access; privilege escalation means gaining additional permissions
- Checked OneDC_Updater: GroupId Users, LogonType Group, RunLevel Highest
- Highest does not automatically mean Administrator or SYSTEM
- Analysed a fictional sequence of remote sign-in, script execution and scheduled-task creation
- Related timestamps suggest a hypothesis but do not prove causation
- Assessment in the exercise: high priority, escalate for verification

</details>


<details>
<summary><strong>Day 33 - Local accounts and administrator auditing</strong></summary>

- Get-LocalGroupMember -Group "Administrators" shows local administrator group members
- Get-LocalUser shows local accounts, enabled status, and available last-logon information
- My PC showed the expected admin-group accounts; only my normal local account was enabled
- 4720 = user account created
- 4732 = member added to a security-enabled local group; check which group
- 4624 with Logon Type 10 = successful remote interactive (RDP) login
- No matching 4720/4732 records in current logs does not prove no historical changes
- auditpol showed Success for User Account Management and Security Group Management
- Simulated case: unexpected account created, added to Administrators, then used for unfamiliar RDP login
- SOC conclusion for simulation: High priority; verify authorisation, source, account changes and follow-on activity; escalate

</details>


<details>
<summary><strong>Day 34 - Privileged logons and event correlation</strong></summary>

- 4624 = successful logon; 4672 = special privileges assigned at logon; 4688 = process creation
- Logon Type 2 = interactive; 3 = network; 5 = service; 10 = remote interactive (RDP)
- Logon Type tells *how* someone/something logged in; Logon ID helps associate events with the session
- Real logs: SYSTEM (SID S-1-5-18) and Logon ID 0x3E7 appeared repeatedly in 4672 and service-type 4624 events; normal pattern, not proof of compromise
- In 4624, Subject is the requester, New Logon is the account signing in, and Process Name is not a source IP
- Real DWM-22 interactive logons were Windows virtual desktop account activity, including linked elevated/non-elevated tokens
- A limited search for non-DWM/UMFD interactive or RDP records found no matching results; this does not prove no user logons occurred
- 4672 and Elevated Token: Yes are not by themselves evidence of attacker privilege escalation
- Simulated case: unfamiliar RDP logon, same-ID privileged-logon event, then encoded PowerShell; high priority, escalate and verify authorisation and activity
- Key memory: Logon Type 10 = RDP; matching Logon IDs link related events (consider timestamps and host, especially for SYSTEM 0x3E7)

</details>


<details>
<summary><strong>Day 35 - Failed logons and password attack detection</strong></summary>

- Windows Security Event 4625 = failed logon; 4624 = successful logon; 4740 = account locked out; 4720 = account created
- Real practical: queried Event 4625 and found no matching events in retained Security log
- `auditpol /get /subcategory:"Logon"` showed Success and Failure auditing enabled
- No matching recorded failures does not prove there were never any failed logins
- Brute-force guessing: many password attempts targeting one account
- Password spraying: one or a few passwords tried across many accounts
- Credential stuffing: trying username/password pairs exposed in prior breaches
- Simulated case: 20 failed logons, then one successful logon from the same IP, followed by PowerShell; assessed High and escalated for investigation
- Check whether access was authorised, correlate account/source/time/logon type, and inspect subsequent PowerShell activity
- Core distinction: suspicious event sequence is evidence for investigation, not proof of attacker compromise

</details>


<details>
<summary><strong>Day 36 - Account lockouts and Windows policy</strong></summary>

- Event 4740 = user account locked out; 4625 = failed logon; 4624 = successful logon
- Queried Security log for Event 4740; no retained matching records were found locally
- Event 4740 Caller Computer Name can be a clue; domain-account lockouts are often investigated on domain controllers
- Read-only command: `net accounts`
- Actual local workstation policy: lockout threshold 10; lockout duration 10 minutes; observation window 10 minutes
- Other local settings: minimum password length 0; password history None; maximum password age 42 days; not necessarily online Microsoft-account rules
- An attacker could deliberately trigger account lockouts without knowing the correct password
- Simulated scenario: employee's old saved application password likely caused repeated failures and a lockout
- SOC assessment: low priority when contextual evidence supports a routine cause; confirm source, fix saved credentials and verify failures stopped before closing
- Key lesson: a plausible benign explanation needs validation before closing an alert

</details>


<details>
<summary><strong>Day 37 - PowerShell logging, process IDs and audit gaps</strong></summary>

- Event 4104 = PowerShell script-block logging; 4688 = process creation (if audited); 4624 = successful logon
- Used a calculated Select-Object `Preview` property to inspect only the first 200 characters of three 4104 records
- Actual 4104 event process IDs: 18152 (16 Oct), 6412 (15 Oct), 7388 (13 Oct)
- PID identifies a process, not a person; correlate PID with timestamps because Windows can reuse IDs
- Searched for 4688 matching PID 18152 (`0x46e8`) near 16 Oct 20:52; no matching record returned
- `auditpol /get /subcategory:"Process Creation"` returned `No Auditing`; this is consistent with the missing 4688 record but does not establish earlier audit settings
- Nothing in the three short script previews alone proved malicious activity; the third contained familiar file-hash practice code
- Simulated scenario: unfamiliar Administrator RDP login followed by PowerShell download activity with missing process telemetry
- SOC response: High priority, escalate and verify RDP authorisation, script content and available other logs; recommend separate process-auditing review
- Key lesson: missing event telemetry creates uncertainty; lack of a matching log event does not establish safety

</details>


<details>
<summary><strong>Day 38 - Building a Windows incident timeline</strong></summary>

- Combined PowerShell Operational Event 4104 and Security Event 4624 using $start, $end, arrays, +, and Sort-Object TimeCreated
- Actual 16 Oct 2026 sample: six 4624 events around 20:52:45-20:53:07, with one 4104 at 20:52:47 (PowerShell PID 18152)
- Inspected one 4624 at 20:52:46: service logon Type 5, NT AUTHORITY\\SYSTEM, Logon ID 0x3E7, services.exe, no remote source IP
- Filtered the collected six 4624 records for Logon Type 2 or 10; none matched; not proof all were Type 5
- Event metadata ProcessId for 4624 is not necessarily the process belonging to the newly logged-on account
- A service logon one second before a PowerShell script is not evidence that the service launched PowerShell
- Process Creation auditing had been found disabled on Day 37, restricting parent process visibility
- SOC assessment: no malicious behaviour established; PowerShell process origin not identified
- Key lesson: a time-ordered sequence suggests leads but does not demonstrate causation; write confirmed facts separately from hypotheses and unknowns

</details>


<details>
<summary><strong>Day 39 - Parent-child process investigation</strong></summary>

- Investigated my live PowerShell session using `Get-CimInstance Win32_Process -Filter "ProcessId = $PID"`
- Real result: powershell.exe PID 20516, ParentProcessId 24240, started 23 Oct 2026 at 15:28
- Identified parent as explorer.exe PID 24240, parent PID 4736, created at 15:22:35, path C:\\WINDOWS\\Explorer.EXE
- `Get-AuthenticodeSignature` on Explorer showed Status Valid, signer Microsoft Windows
- Real process tree explorer.exe -> powershell.exe was consistent with ordinary desktop activity; low concern based on available evidence
- ParentProcessId identifies the recorded parent, not the person responsible; creation times matter because PIDs can be reused
- Simulated SOC case: unfamiliar email attachment opened in WINWORD.EXE PID 4100 -> encoded PowerShell PID 5200 with ParentProcessId 4100 -> attempted external download
- Assessment in simulation: high priority; investigate encoded script, downloaded files and possible persistence; escalate
- Key distinction: a recorded process relationship gives stronger evidence than events merely occurring at nearby timestamps, but it does not prove malicious intent

</details>


<details>
<summary><strong>Day 40 - Network connections and process attribution</strong></summary>

- Used `Get-NetTCPConnection -State Established` to inspect local/remote IPs, ports and owning PIDs
- Observed eight established connections using remote TCP port 443; port alone does not prove HTTPS or safety
- Local interface address was private (`172.16.0.0/12` range); the meaning of the final IP octet depends on subnet mask
- PID 13108 owned multiple connections in an earlier snapshot; a later `Get-CimInstance` lookup returned nothing, possibly because it exited
- Captured another connection: `162.159.128.232:443` owned by PID 1408
- `Get-CimInstance Win32_Process -Filter "ProcessId = 1408"` identified Discord.exe, ParentProcessId 15508, path under AppData\\Local\\Discord
- `Get-AuthenticodeSignature` reported Status Valid, signer Discord Inc.
- SOC assessment: likely expected application traffic if Discord knowingly installed/running; no malicious behaviour established, destination ownership and contents not independently verified
- Main workflow: connection -> owning PID -> process name/path -> digital signature -> contextual assessment
- Multiple connections from one application are not suspicious by count alone; live process information changes rapidly

</details>


<details>
<summary><strong>Day 41 - DNS investigation and logging</strong></summary>

- Used `Get-DnsClientCache` to inspect ten cached DNS records from Steam, Microsoft cloud services, NVIDIA telemetry and certificate infrastructure
- A record (type 1) maps a domain to IPv4; CNAME (type 5) maps a domain to another domain; SOA gives DNS zone information
- `Resolve-DnsName settings-win.data.microsoft.com` demonstrated a CNAME -> CNAME -> A resolution chain
- The standard Sysmon Operational log was not found with `Get-WinEvent -ListLog`; Sysmon Event 22 can associate DNS queries with processes when configured
- `Microsoft-Windows-DNS-Client/Operational` existed but had IsEnabled False
- No DNS-logging settings were changed
- DNS cache presence does not establish that an application connected, downloaded a file, or executed it
- Simulated case: PowerShell PID 6200 queried a domain, connected externally on 443, and an unsigned executable appeared soon after without approved update
- High priority and escalate; examine DNS/connection/file records, file hash and reputation, execution evidence and persistence
- Key lesson: DNS query != network connection != downloaded file != executed file; each needs its own evidence

</details>


<details>
<summary><strong>Day 42 - File inspection, MZ headers and Prefetch evidence</strong></summary>

- Inspected `Microsoft.Services.Store.winmd` from Downloads: 5,120 bytes, created/modified 27 Aug 2026
- SHA256 via `Get-FileHash`: 45715793B8C8571554B0BFB4ECCC29E2884C16481E1C7DBEE78363BBE4DA3DD9; hash alone is not a malware verdict
- `Format-Hex` showed first bytes 4D 5A (ASCII MZ) and standard DOS-stub message; an MZ/PE container signature does not prove execution
- `Get-AuthenticodeSignature` for the .winmd returned NotSigned; this alone does not prove malware
- Used `Get-Process -Name "*notepad*"` and found Notepad running, PID 12388, started 26 Oct 2026 18:45:59
- Found `NOTEPAD.EXE-0D1583A9.pf` under Windows Prefetch, last modified 26 Oct at 18:46:09
- Windows Prefetch helps application startup but can provide forensic evidence consistent with previous execution; artifact times and names need careful interpretation
- Simulated case: unsigned update.exe in Temp, zero hash reputation detections, no current process, matching Prefetch artifact; escalate and investigate origin, artifact, execution evidence and persistence
- Main distinction: file presence != file format != currently running process != historical execution != proven malware

</details>


<details>
<summary><strong>Day 43 - Prefetch, version verification and revoked code-signing certificate</strong></summary>

- Listed 10 recent `.pf` artifacts using `Get-ChildItem "$env:WINDIR\Prefetch" -Filter "*.pf"`, `Sort-Object LastWriteTime -Descending` and `Select-Object -First 10`
- Found Prefetch files for CONSENT.EXE, DTSHELLHLP.EXE, DISCSOFTBUSSERVICELITE.EXE, RUNDLL32.EXE, MSEDGEWEBVIEW2.EXE, AUDIODG.EXE and SVCHOST.EXE; the two unfamiliar names were associated with DAEMON Tools Lite
- Checked Windows uninstall registry with `Get-ItemProperty`; installed DAEMON Tools Lite reported **12.1.0.2211**, outside the specific reported 2026 supply-chain affected range **12.5.0.2421–12.5.0.2434**
- `Get-Item` and `VersionInfo.FileVersion` for DTShellHlp.exe also reported **12.1.0.2211**, with displayed LastWriteTime **26 Sep 2024**; a version match and file timestamp are supporting evidence, not proof of safety
- `Get-AuthenticodeSignature` reported signer certificate subject **AVB Disc Soft, SIA**, but `Status: UnknownError`; `StatusMessage: A certificate was explicitly revoked by its issuer`. A revoked certificate prevents treating its signature as valid and warrants investigation, but does not alone prove malware
- SHA256 for DTShellHlp.exe: **6396460EE441DD2D083F5B1511A513EC8DE606AF8B66B09D8924B92E4B13285F**. Calculating a hash is **not** a malware scan or a clean verdict; no independent hash match or malware verdict was established in the lesson
- SOC outcome: **malware not confirmed, certificate concern unresolved**. Suggested follow-ups include a full Defender scan, reliable hash comparison and reinstalling or uninstalling old software as appropriate (none of those actions verified performed)
- Remember: Prefetch supports prior execution investigation but isn't proof of malicious behaviour; distinguish signature presence, certificate validity, malware reputation and actual behaviour

</details>


<details>
<summary><strong>Day 44 - Microsoft Defender detection and remediation triage</strong></summary>

- Used `Get-MpComputerStatus` to inspect Defender: `AMServiceEnabled=True`, `AntivirusEnabled=True`, `RealTimeProtectionEnabled=True`; antivirus definitions last updated **29 Oct 2026 08:13:13**
- A quick scan end time was recorded for **26 Oct 2026 19:55:32**; `FullScanEndTime` returned no value (not proof a full scan never ran)
- `Get-MpThreatDetection` returned no records in the lesson; this does not prove malware has never been present
- Queried `Microsoft-Windows-Windows Defender/Operational` for **1116** (detection) and **1117** (remediation action) with `Get-WinEvent`; no results were returned. `-ErrorAction SilentlyContinue` can hide query errors
- Also reviewed **5007**, which records Defender configuration changes
- `ActionSuccess=True` means a recorded remediation action succeeded; `ActionSuccess=False` means it was unsuccessful and requires investigation
- Simulated SOC case (not actual machine activity): `FINANCE-PC-04`, `invoice.exe`, Defender 1116 plus 1117, `ActionSuccess=False`, no currently running process; **High priority** training assessment and further investigation warranted
- Suggested checks: inspect remediation failure, verify file presence, look for historical execution evidence, calculate SHA256 and check relevant reputation information, escalate or isolate per incident procedures when justified
- **Key lesson:** Detection != remediation != successful remediation. No current process and no matching logs do not prove a threat never ran; a SHA256 hash is a fingerprint, not a malware verdict

</details>


<details>
<summary><strong>Day 45 - PowerShell script block investigation (Event 4104)</strong></summary>

- Used `Get-WinEvent -ListLog "Microsoft-Windows-PowerShell/Operational"` to confirm PowerShell Operational channel `IsEnabled=True`, with **613 total event records** (not 613 Event 4104 records)
- Queried Event **4104**, the PowerShell script-block logging event. Most recent five were **Warning** level, all timestamped **29 Oct 2026 15:40:05**
- Expanded a 4104 event's message and found generated-looking PowerShell wrappers for Defender `root\Microsoft\Windows\Defender\MSFT_MpBehavioralNetworkBlockingRules`, including definitions for `Get-MpBehavioralNetworkBlockingRules` and `Remove-MpBehavioralNetworkBlockingRules`, plus `Export-ModuleMember`
- Key conclusion: **Defining/exporting a function is not proof that anyone called it or that Defender rules were removed**. Warning severity doesn't independently prove malicious activity
- Analysed five `ScriptBlockId` values using `$_.Properties[3].Value`; all **five distinct IDs**, timestamped alike, and all message text matched `MSFT_Mp` in `MentionsDefender` check
- SOC case: real logs suggest Defender-related module script blocks; **no observed evidence of rule removal or malicious activity in reviewed material**, low concern on available evidence. Next steps only if needed: correlate surrounding PowerShell events and process telemetry, and Defender configuration changes via Event **5007**
- Prefetch may show historical PowerShell execution but doesn't reveal commands, whereas 4104 can show script-block text. Avoid equating log absence with absence of execution
- Practice demonstrated read-only event triage, comparing timestamps and IDs, and documenting the distinction between observed code and executed action

</details>


<details>
<summary><strong>Day 46 - Microsoft Defender configuration changes (Event 5007)</strong></summary>

- Used read-only `Get-WinEvent` with Defender Operational `Id=5007` to inspect three real configuration-change events on 30–31 Oct 2026
- `ToastOrSsoTrigger` under `HKLM\SOFTWARE\Microsoft\Windows Defender\UX Configuration` changed `0x0 -> 0x1` on **30 Oct 17:32:38** and `0x1 -> 0x0` on **31 Oct 14:50:15**; these values alone do **not** establish antivirus was disabled
- `WdConfigHash` under `...\CoreService` changed `0x390D7929 -> 0xE586D652` on **30 Oct 15:03:58**; specific underlying cause wasn't determined
- Day 45 Defender-related PowerShell Event **4104** warnings occurred on **29 Oct 15:40:05**, while the reviewed 5007 events were on 30–31 Oct; no causal link demonstrated. Close timestamps alone would not establish causation either
- `Get-MpComputerStatus` reported **True** for `AntivirusEnabled`, `RealTimeProtectionEnabled`, `BehaviorMonitorEnabled` and `IsTamperProtected` at time of check
- Current protections being enabled doesn't prove they were **never disabled historically**
- SOC outcome: **Low concern on reviewed evidence**, no proven malicious Defender setting change, exact change cause unverified; look for complementary process logs, 4104 records, 5007 changes and alert context if needed
- Key habit: Separate *configuration change*, *actual security-control disablement*, *historical state*, and *attribution to a process/person* before claiming an attack

</details>
