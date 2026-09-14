# Day 3 - private IP, DHCP, gateway and NAT

Today I looked at my own network settings with:

`ipconfig /all`

My main results were:

- DHCP Enabled: Yes
- IPv4: 172.20.10.14
- Subnet Mask: 255.255.255.240
- Default Gateway: 172.20.10.1
- DHCP Server: 172.20.10.1
- DNS: 172.20.10.1 plus some IPv6 addresses

## What I understood

`172.20.10.14` is my private IP address.

The gateway `172.20.10.1` is basically where my computer sends traffic when it needs to leave the local network.

DHCP gives my device its network settings automatically, like IP, subnet mask, gateway and DNS.

NAT is different. NAT translates private network traffic so devices using private IPs can communicate with the internet.

So the simple version in my head is:

`DHCP = gives me network settings`

`Gateway = way out of my local network`

`NAT = translates private traffic for the internet`

## Ping test

I tested my gateway and also `8.8.8.8`.

The ping to `8.8.8.8` worked:

- sent 4
- received 4
- 0% loss
- minimum 31ms
- maximum 60ms
- average 40ms

This showed me that my laptop could reach outside my local network.

At first I did not know what `8.8.8.8` was. I learned it is a public Google IP commonly used for DNS and it is useful for testing internet connectivity.

## Subnet mask

Mine was:

`255.255.255.240`

I learned this is `/28`.

I do not know the binary maths for subnetting yet, but I understand the subnet mask helps decide what is local to my network.

## What confused me

I mixed up DHCP and NAT at first and I also called the local IP something like a local drive before. Now I understand a drive is storage like `C:\`, while an IP is for networking.

The main thing I learned today is to test step by step. If I can reach the gateway but not something outside the network, the problem could be further out like the router, ISP, routing or filtering.