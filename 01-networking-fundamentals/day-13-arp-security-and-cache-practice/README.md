# Day 13 - ARP security and cache practice

Today I practiced ARP again, this time more like a small investigation instead of just learning the definition.

## What ARP does

ARP maps a local IPv4 address to a MAC address.

A simple way I want to remember it is:

```
IPv4 address -> MAC address
```

My computer needs this so it knows which local network interface should receive traffic for a local IP, especially the gateway.

ARP does not encrypt traffic.

## ARP spoofing

ARP spoofing/poisoning is when a device lies about an IP-to-MAC mapping.

For example, if an attacker claims that the gateway IP belongs to the attacker's MAC address, traffic could potentially be redirected through the attacker.

That does not mean every MAC change is an attack. A change could also happen because of a router replacement, failover, virtual networking or another network change.

## First attempt

I ran:

```powershell
arp -a
```

My gateway entry was:

```
192.168.0.1 -> 68-ab-a9-dc-33-c1
```

and it was marked as:

```
dynamic
```

Then I tried:

```powershell
arp -d *
```

but got:

```
The ARP entry deletion failed: The requested operation requires elevation.
```

So I learned that clearing the ARP cache requires running PowerShell as Administrator.

## Second attempt as Administrator

I opened PowerShell as Administrator and ran:

```powershell
arp -a
arp -d *
arp -a
```

The delete command worked without an error.

The gateway entry was already visible again almost immediately:

```
192.168.0.1 -> 68-ab-a9-dc-33-c1
```

At first this looked like the clear might not have worked, but the better explanation is that Windows needed the gateway again and quickly relearned the ARP mapping in the background.

The basic flow is:

```
ARP mapping exists
-> clear ARP cache
-> Windows needs gateway again
-> ARP request happens
-> gateway replies with its MAC
-> mapping is added again
```

## Ping test

I then ran:

```powershell
ping 192.168.0.1
```

The result was:

```
Sent = 4
Received = 4
Lost = 0
```

The times were:

```
2 ms
2 ms
133 ms
2 ms
```

The gateway MAC stayed the same after the test.

I also connected this back to yesterday's traceroute lesson: one high latency result by itself does not prove there is a problem.

The 133 ms reply was much higher than the others, but the other three were 2 ms and there was 0% packet loss.

## Security thinking

If the gateway MAC suddenly changed later, I should not immediately say it is ARP spoofing.

I would investigate things like:

- whether the router or network changed
- whether the gateway IP stayed the same
- whether the new MAC stays consistent
- whether another device appeared on the network
- whether there are other signs of traffic interception or network problems

## What I want to remember

- ARP = IPv4 address to MAC address
- ARP does not encrypt traffic
- Dynamic ARP entries can be relearned automatically
- Clearing the ARP cache requires Administrator privileges on Windows
- Gateway MAC changes should be investigated, not automatically called an attack
- One latency spike is not enough to diagnose a problem
