# Day 1 - DNS, IPs and traceroute

This was my first proper day learning networking for cybersecurity.

I wanted to understand what actually happens when I type something like `google.com` in the browser because before this I never really thought about what happens in the background.

## Commands I tried

`ipconfig`

This showed me my network information and my local IP address.

`nslookup google.com`

This was interesting because Google did not give me only one IP. It gave me a few IPv4 and IPv6 addresses.

One IPv4 I got was:

`142.251.30.102`

At first I thought the addresses that came back were the DNS server, but I learned they were actually IP addresses returned by DNS for Google.

`tracert google.com`

Mine showed around 15 hops.

I understood this as my traffic not going straight from my laptop to Google. It goes through different routers/networks before reaching the destination.

## Things I learned today

- DNS changes a domain name like `google.com` into an IP address
- an IP address tells you where a device/server is on a network
- a port is more like which service you want to talk to
- port 443 is normally HTTPS
- HTTPS is encrypted using TLS
- one website can have more than one IP address
- a hop is one step along the route to the destination

The order I learned for opening a website was basically:

`type website -> DNS finds IP -> traffic travels through networks -> HTTPS connection -> website sends data back`

I am still new to all of this but after actually using the commands it made more sense than just reading definitions.