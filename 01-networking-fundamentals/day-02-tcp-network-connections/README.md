# Day 2 - TCP and network connections

Today I started looking at actual connections on my Windows laptop instead of only learning definitions.

At the start `netstat` looked like a mess of random numbers but by the end I could understand most of one line.

## TCP and UDP

What I understand so far:

- TCP is connection based and tries to make sure data arrives properly and in order
- UDP is more direct and does not have the same built-in delivery guarantee

The TCP handshake I need to remember is:

`SYN -> SYN-ACK -> ACK`

## Looking at my connections

I used:

`netstat -ano | findstr ESTABLISHED`

One connection I looked at was:

`TCP 172.20.10.14:60571 140.248.134.172:80 ESTABLISHED 11292`

I learned how to split it up:

- TCP = protocol
- 172.20.10.14 = my local IP
- 60571 = my local port
- 140.248.134.172 = remote IP
- 80 = remote port
- ESTABLISHED = the TCP connection is active
- 11292 = PID

I already knew from Day 1 that port 80 is normally HTTP.

## Finding which program made the connection

I used:

`tasklist | findstr 11292`

and got:

`svchost.exe`

Then I checked the service with:

`tasklist /svc /fi "PID eq 11292"`

and it showed:

`DoSvc`

I learned that this is the Windows Delivery Optimization service.

## What clicked for me

A PID is just a Process ID. It helps connect a network connection to the program/process that owns it.

So the investigation was basically:

`connection -> PID -> process -> service`

I also learned not to call something malware just because it looks suspicious. First I should check more evidence like the process name, where the file is, what IP it connects to and what the process is doing.

I still mix up some of the terminology sometimes, but I can now read a basic `netstat` line and explain what most of it means.