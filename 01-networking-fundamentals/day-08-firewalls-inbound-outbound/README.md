# Day 8 - Firewalls, inbound and outbound traffic

Today I learned the basics of firewalls and how they decide what network traffic should be allowed or blocked.

## What I checked

I ran:

```
netsh advfirewall show allprofiles
```

My results were:

- Domain firewall: ON
- Private firewall: ON
- Public firewall: ON

I also used PowerShell:

```powershell
Get-NetFirewallProfile
```

All three profiles showed as enabled.

## Things I learned

A firewall is like a filter for network traffic. It can allow or block traffic based on rules.

Inbound traffic means traffic coming towards my computer.

Outbound traffic means traffic my computer is sending out.

I also learned that just because a port is LISTENING, it does not automatically mean anyone on the internet can reach it. There can still be Windows Firewall, router/NAT rules and other network controls in the way.

Port 3389 is RDP (Remote Desktop Protocol).

Port 443 is normally HTTPS, but I initially thought that meant it was automatically safe. It does not. Malware can also use port 443, so the port alone is not enough to decide whether traffic is good or bad.

## One mistake I made

I thought an inbound rule blocking local port 443 meant it would block my internet access on HTTPS.

What it actually means is that incoming TCP connections to local port 443 are blocked when that rule applies. Outbound HTTPS connections can still be allowed.

## Security idea from today

A company might allow users to make outbound HTTPS connections because they need websites, cloud services and other normal internet services.

At the same time, it can block most random inbound connections because employee laptops usually do not need strangers on the internet starting connections to them.

## What I want to remember

- Firewall = allows or blocks traffic using rules
- Inbound = coming towards my computer
- Outbound = leaving my computer
- 3389 = RDP
- 443 = HTTPS
- LISTENING does not mean internet exposed
- Port 443 does not automatically mean safe
