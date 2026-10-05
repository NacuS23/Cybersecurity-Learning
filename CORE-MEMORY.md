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
