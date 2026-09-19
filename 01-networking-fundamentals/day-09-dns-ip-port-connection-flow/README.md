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

## Following the connection to a process

After opening the website in Microsoft Edge, I checked HTTPS connections with:

```powershell
netstat -ano | findstr ":443"
```

I then filtered the connections using PID `13848`:

```powershell
netstat -ano | findstr "13848"
```

There were multiple ESTABLISHED TCP connections to remote servers on port 443.

I checked the PID with:

```powershell
tasklist | findstr 13848
```

and got:

```
msedge.exe  13848
```

So I confirmed that PID `13848` belonged to Microsoft Edge and that Edge had several active HTTPS connections.

One thing I noticed is that none of those connections matched the exact `example.com` IP from the earlier DNS lookup. That was useful because it showed me that a browser can have lots of HTTPS connections at the same time, and seeing the same PID does not automatically tell me which exact website a connection belongs to.

I also saw UDP traffic on port `5353`, which is commonly used for mDNS (Multicast DNS) on the local network.

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
- ESTABLISHED = active TCP connection
- One browser can connect to many different remote servers
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
ESTABLISHED = active TCP connection
PID 13848 = msedge.exe in my test
Unknown process + unknown destination = investigate further
```
