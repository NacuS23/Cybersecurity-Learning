# Day 15 - Subnets, routing and local vs remote traffic

Today I focused on how my computer decides whether a destination is on the local network or needs to be sent to the default gateway.

## Current network

My current IPv4 setup is:

```
IP address: 192.168.0.188
Subnet mask: 255.255.255.0
Default gateway: 192.168.0.1
```

The subnet mask `255.255.255.0` is also written as `/24`.

For this network, addresses in `192.168.0.x` are local.

## Route table

I ran:

```powershell
route print
```

Two important entries were:

```
0.0.0.0        0.0.0.0        192.168.0.1    192.168.0.188
192.168.0.0    255.255.255.0  On-link         192.168.0.188
```

The `192.168.0.0/24` entry shows that this network is directly reachable.

The `0.0.0.0/0` entry is the default route. If Windows does not have a more specific route, traffic is sent to the gateway at `192.168.0.1`.

## Local vs remote

I tested a few addresses:

```
192.168.0.50   = local
192.168.1.50   = remote
192.168.0.1    = local
8.8.8.8        = remote
192.168.0.200  = local
```

For a local destination, the computer can use ARP to find the destination MAC address and send traffic directly on the local network.

For a remote destination, the computer sends the frame to the gateway MAC address and the router forwards the packet toward the final destination.

## What I want to remember

```
Subnet = is the destination local?
ARP = what MAC address do I send to?
Gateway = where do I send remote traffic?
Route table = which path should traffic use?
```

This helped connect several earlier topics together instead of treating ARP, gateways and routing as separate ideas.
