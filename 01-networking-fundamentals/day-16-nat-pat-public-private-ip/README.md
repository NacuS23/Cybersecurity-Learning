# Day 16 - NAT, PAT and public vs private IPs

Today I focused on how devices on a private network can share one public IP when connecting to the internet.

## NAT

NAT stands for Network Address Translation.

It allows private/internal addresses such as:

```
192.168.x.x
172.16.x.x - 172.31.x.x
10.x.x.x
```

to communicate with the internet through a public-facing address.

A simple way to think about it is:

```
Private device
-> router
-> NAT
-> public IP
-> internet
```

## PAT

PAT stands for Port Address Translation.

PAT uses port numbers to keep different connections separate even when several devices are sharing the same public IP.

For example:

```
192.168.0.188:52000
-> PublicIP:61001

192.168.0.25:52000
-> PublicIP:61002
```

This is one reason a public IP does not always identify one specific device.

## What I practiced

I checked active connections with:

```powershell
netstat -ano | findstr ESTABLISHED
```

One local-only connection was:

```
127.0.0.1:60995 -> 127.0.0.1:33683
```

Both sides use `127.0.0.1`, so the traffic stays on the same computer.

Another connection was:

```
172.20.10.14:50476 -> 92.223.127.187:443
```

This can be read as:

```
Local IP: 172.20.10.14
Local/source port: 50476
Remote IP: 92.223.127.187
Remote port: 443
State: ESTABLISHED
```

The remote port `443` normally indicates HTTPS.

## Why this matters in security

If several devices share one public IP, an analyst may need more than just the public IP to identify the original connection.

Useful context can include:

- source port
- timestamp
- NAT logs
- internal IP
- process or device information

## What I want to remember

```
NAT = translate addresses
PAT = use ports to distinguish connections
One public IP can represent many devices
Source ports help identify individual connections
127.0.0.1 = localhost only
```
