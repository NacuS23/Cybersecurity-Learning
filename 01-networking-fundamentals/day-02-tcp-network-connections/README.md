# Day 2 - TCP and Network Connections

## Objective

The goal of this lab was to understand how computers establish network
connections and how I can investigate active connections on a Windows computer.

I learned about:

- TCP and UDP
- Network packets
- The TCP three-way handshake
- Local and remote IP addresses
- Local and remote ports
- Process IDs (PID)
- Windows network connections
- How to identify the process and service responsible for a connection

---

## TCP vs UDP

TCP stands for Transmission Control Protocol.

TCP is connection-oriented and provides reliable, ordered delivery of data.

UDP stands for User Datagram Protocol.

UDP is connectionless and does not provide the same built-in guarantee that
data will arrive or arrive in order.

---

## TCP Three-Way Handshake

Before a TCP connection is established, the devices perform a three-way
handshake:

SYN -> SYN-ACK -> ACK

My understanding:

1. SYN - The client requests a connection.
2. SYN-ACK - The server acknowledges the request and responds.
3. ACK - The client acknowledges the response.

The TCP connection can then become established.

---

## Investigating Network Connections

I used the following Windows command:

`netstat -ano | findstr ESTABLISHED`

This showed active TCP connections on my computer.

One connection I investigated was:

`TCP 172.20.10.14:60571 140.248.134.172:80 ESTABLISHED 11292`

I learned how to break this information down:

- Protocol: TCP
- Local IP: 172.20.10.14
- Local port: 60571
- Remote IP: 140.248.134.172
- Remote port: 80
- State: ESTABLISHED
- PID: 11292

Port 80 is commonly associated with HTTP.

The ESTABLISHED state means that an active TCP connection has been
successfully established.

---

## Finding the Process

The final number shown by netstat was the Process ID (PID).

I investigated PID 11292 using:

`tasklist | findstr 11292`

The process was:

`svchost.exe`

I then investigated which Windows service was associated with this process:

`tasklist /svc /fi "PID eq 11292"`

The result showed:

`DoSvc`

I learned that DoSvc is the Windows Delivery Optimization service.

---

## Security Investigation Lesson

One of the most important things I learned was that seeing a network
connection is only the beginning of an investigation.

A basic investigation can follow this process:

Network connection
-> Remote IP and port
-> PID
-> Process
-> Service
-> Investigate whether the activity is expected

I also learned that a suspicious-looking process should not automatically be
declared malware.

A security analyst should collect more evidence before reaching a conclusion.

Examples of things that could be investigated include:

- Process name
- Executable location
- Digital signature
- File hash
- Parent process
- Remote IP address
- Remote domain
- Network behaviour

---

## What I Learned

Before this lab, the output from netstat looked like a collection of random
IP addresses and numbers.

I can now read a connection such as:

`TCP 192.168.1.50:51234 8.8.8.8:443 ESTABLISHED 7340`

and identify:

- The network protocol
- The local IP address
- The local port
- The remote IP address
- The remote port
- The connection state
- The PID responsible for the connection

This was my first basic investigation connecting network activity to a
specific Windows process and service.
