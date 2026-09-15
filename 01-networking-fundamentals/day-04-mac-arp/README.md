# Day 4 - MAC addresses and ARP

Today I learned a bit more about how devices find each other on a local network.

I already knew my laptop had an IP, but I did not understand what a MAC address was or why both are needed.

## Commands I used

`getmac /v`

This showed my network adapters and their MAC addresses. I also saw a couple saying `Media disconnected`, which I learned just means those adapters are not currently connected.

`arp -a`

This showed IP addresses on my local network and the MAC addresses Windows currently links to them.

My gateway was:

`172.20.10.1`

and it appeared in the ARP table.

## What ARP does

ARP stands for Address Resolution Protocol.

My simple understanding is:

if my computer knows an IP address on the local network but does not know the MAC address, ARP helps find out which MAC belongs to that IP.

For example:

`172.20.10.1 -> MAC address of the gateway`

## Dynamic and static

Some entries in `arp -a` showed as dynamic and some as static.

I first thought this was about whether my own IP was dynamic, but I learned that here it is talking about the ARP entry itself.

Dynamic means Windows learned the IP-to-MAC mapping automatically.

## Ping test

I tried:

`ping 172.20.10.1`

and got:

- Sent: 4
- Received: 0
- Lost: 4
- 100% packet loss

At first I thought this meant the gateway was not working.

But I learned that a failed ping does not always mean the device is unreachable. The gateway can still exist and work but ignore or block ICMP ping requests.

This made sense because the gateway still appeared in my ARP table and my internet was working.

## Security thing I learned

I also learned why ARP can matter in cybersecurity.

If another device lies and says that the gateway IP belongs to its own MAC address, my computer could send traffic to the wrong device.

That can be related to ARP spoofing or ARP poisoning and can be used in man-in-the-middle attacks.

I am still new to this part, but the main thing I understand is:

- IP address = logical network address
- MAC address = local network interface address
- ARP = finds the MAC address for a local IP
- failed ping does not always mean no connection

This one was a bit more confusing than the other days but I think the local network side is starting to make more sense.