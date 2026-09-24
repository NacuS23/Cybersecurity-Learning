# Day 17 - TCP vs UDP in real traffic

Today I compared TCP and UDP using real traffic in Wireshark.

## TCP

TCP is connection-oriented and designed for reliable, ordered delivery.

It can retransmit data when expected acknowledgements are not received.

A useful way to remember it is:

```
TCP = reliable connection
```

Common examples include HTTPS, SSH and RDP.

## UDP

UDP is connectionless and does not have the same built-in delivery guarantees as TCP.

It is often used where low overhead and speed are useful, such as DNS, voice calls, streaming and gaming.

A useful way to remember it is:

```
UDP = connectionless, no built-in delivery guarantee
```

## Wireshark TCP practice

I used this filter:

```
tcp.port == 443
```

One example I saw was:

```
Source: 85.234.76.87
Destination: 192.168.0.188
Info: Application Data
```

Because the filter was for TCP port 443, this was TCP traffic related to HTTPS/TLS.

The direction was from the remote server back to my computer.

## Wireshark UDP/DNS practice

I used:

```
udp.port == 53
```

and saw a DNS response:

```
Source: 194.168.4.100
Destination: 192.168.0.188
DNS response for:
p2p-lhr1.discovery.steamserver.net
```

The response included several IPv4 addresses for that hostname.

This helped show the difference between:

```
TCP/443 = web/TLS traffic
UDP/53  = DNS traffic
```

DNS commonly uses UDP for normal queries, although TCP can also be used in some situations.

## What I want to remember

- TCP = reliable, connection-oriented transport
- UDP = connectionless transport with no built-in delivery guarantee
- TCP can retransmit unacknowledged data
- UDP does not use TCP-style ESTABLISHED connection states
- DNS usually uses UDP port 53 for normal queries
- HTTPS normally uses TCP port 443
