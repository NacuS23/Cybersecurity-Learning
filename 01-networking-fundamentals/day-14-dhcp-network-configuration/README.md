# Day 14 - DHCP and network configuration

Today I focused on DHCP and how my computer receives its network settings automatically.

## What DHCP does

DHCP stands for Dynamic Host Configuration Protocol.

It can give a device things like:

- IPv4 address
- Subnet mask
- Default gateway
- DNS servers

## What I checked

I ran:

```powershell
ipconfig /all
```

My active adapter was Wi-Fi.

The important values were:

```
DHCP Enabled: Yes
IPv4 Address: 192.168.0.188
Subnet Mask: 255.255.255.0
Default Gateway: 192.168.0.1
DHCP Server: 192.168.0.1
DNS Servers:
194.168.4.100
194.168.8.100
```

My DHCP lease was roughly one day long.

I learned that when the lease expires, my IP does not have to change. Windows can renew the lease and receive the same IP again.

## Security thinking

DHCP itself does not encrypt my traffic.

A useful distinction is:

```
DHCP = gives network configuration
DNS = translates domain names to IP addresses
HTTPS/TLS = encrypts web traffic
```

If a device suddenly receives an unexpected DNS server or gateway from DHCP, that is worth investigating.

It does not automatically mean an attack, but a malicious or misconfigured DHCP server could potentially send devices to the wrong DNS server or gateway.

## What I want to remember

- DHCP gives automatic network settings
- DHCP can provide IP, subnet, gateway and DNS
- A DHCP lease is temporary permission to use an assigned configuration
- Lease expiry does not mean the IP must change
- DHCP does not encrypt traffic
- Unexpected DHCP settings should be investigated
