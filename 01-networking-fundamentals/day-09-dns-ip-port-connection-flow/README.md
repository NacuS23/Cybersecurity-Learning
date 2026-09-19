# Day 9 - Following a connection from DNS to IP and port

Today I tried to connect together some of the things from the previous days: DNS, IP addresses, ports, PID and processes.

The basic flow I want to remember is:

```
Domain name -> DNS -> IP address -> Port -> PID -> Process
```

## What I practiced

I ran:

```powershell
nslookup example.com
```

The DNS server answering me was:

```
cache1.service.virginmedia.net
194.168.4.100
```

For `example.com` I got two IPv6 addresses and two IPv4 addresses.

IPv4:

```
172.66.147.243
104.20.23.154
```

Then I ran:

```powershell
ping example.com
```

Ping used:

```
172.66.147.243
```

So the IP used by ping was one of the IPv4 addresses that DNS had returned.

## Ping result

I sent 4 packets and received 3 replies.

```
Sent = 4
Received = 3
Lost = 1
25% loss
```

The replies I did get were around 11-15 ms.

I learned that one missed ping does not automatically mean there is a serious network problem. ICMP replies can sometimes be dropped or deprioritised.

## Things I corrected today

I initially described DNS as a connection between things.

A better way to remember it is:

```
DNS = domain name -> IP address
```

I also want to remember:

- IP = network address/destination
- Port = clue about the service/application
- PID = Process ID
- 443 = normally HTTPS
- An unknown program using port 443 is not automatically safe just because it is HTTPS

## Security thinking

If I see something like:

```
unknown.exe -> unknown IP:443
```

I should not immediately call it malware, but it is more interesting because I would want to know:

- what the program is
- where the executable is located
- whether it is signed
- what domain resolved to that IP
- how often it connects
- whether the destination is expected

## What I want to remember

```
DNS = name to IP
IP = network address
Port = service/application clue
PID = Process ID
443 = HTTPS
Unknown process + unknown destination = investigate further
```
