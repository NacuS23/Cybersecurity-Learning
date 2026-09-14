# Day 3 - Private IPs, DHCP, Gateways and NAT

## Objective

The goal of this lab was to understand how my own device receives network settings and how traffic leaves a private network to reach the Internet.

I learned about:

- Private IP addresses
- Default gateways
- DHCP
- NAT
- Subnet masks
- Basic connectivity testing with ping

---

## My Network Configuration

I used:

`ipconfig /all`

My active network settings included:

- DHCP Enabled: Yes
- IPv4 Address: 172.20.10.14
- Subnet Mask: 255.255.255.240
- Default Gateway: 172.20.10.1
- DHCP Server: 172.20.10.1
- DNS Server: 172.20.10.1

I also saw IPv6 DNS information.

---

## Private IP Address

My IPv4 address was:

`172.20.10.14`

This is a private IPv4 address because it is inside the private range:

`172.16.0.0 - 172.31.255.255`

Private IP addresses are used inside private networks and are not directly routed across the public Internet.

---

## Default Gateway

My default gateway was:

`172.20.10.1`

The default gateway is the device my computer normally sends traffic to when the destination is outside the local network.

My current understanding is:

Computer -> Default Gateway -> Internet

---

## DHCP

DHCP automatically provides network configuration to devices.

Examples include:

- IP address
- Subnet mask
- Default gateway
- DNS server

In my network, the DHCP server was:

`172.20.10.1`

---

## NAT

NAT stands for Network Address Translation.

NAT allows devices using private IP addresses to communicate with the wider Internet by translating private network traffic to a public-facing address.

A simplified view is:

Private IP -> Router/Gateway -> NAT -> Public Internet

---

## Subnet Mask

My subnet mask was:

`255.255.255.240`

This is equivalent to:

`/28`

The subnet mask helps determine which IP addresses belong to the local network.

I have not yet learned the binary calculations behind subnetting.

---

## Connectivity Testing

I used ping to test connectivity.

I first tested my local gateway.

I then tested the public IP:

`8.8.8.8`

The result was:

- Sent: 4
- Received: 4
- Lost: 0
- Packet loss: 0%
- Minimum: 31 ms
- Maximum: 60 ms
- Average: 40 ms

This showed that my device could successfully communicate beyond the local network.

---

## Troubleshooting Lesson

I learned an important troubleshooting method.

If I can reach my default gateway but cannot reach a public IP, then the local connection may be working while the problem could be somewhere beyond the local network.

Possible causes could include:

- Router problems
- ISP problems
- Routing problems
- Firewall or filtering
- ICMP being blocked

A security or IT analyst should test each stage instead of assuming one cause immediately.

---

## Key Concepts

My current understanding is:

- DHCP gives my device its network settings
- The default gateway is the normal path to other networks
- NAT translates private-network traffic for Internet communication
- A private IP is different from a public IP
- Ping can help test network connectivity

This lab helped me better understand how my own device connects from a private network to the Internet.
