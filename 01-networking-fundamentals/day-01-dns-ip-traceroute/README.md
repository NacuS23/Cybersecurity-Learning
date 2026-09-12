# Day 1 - DNS, IP Addresses and Traceroute

## Objective

The goal of this lab was to understand what happens when I enter a website such as google.com into my browser.

I learned about:

- IP addresses
- DNS
- Ports
- HTTP and HTTPS
- Traceroute
- IPv4 and IPv6

## Commands Used

### ipconfig

I used:

`ipconfig`

This allowed me to see the network configuration of my Windows computer, including my local IPv4 address.

### nslookup

I used:

`nslookup google.com`

I learned that DNS translates a domain name such as google.com into IP addresses that computers can use.

Google returned multiple IPv4 and IPv6 addresses.

One IPv4 address I received was:

`142.251.30.102`

This also taught me that one domain does not necessarily have only one IP address.

### tracert

I used:

`tracert google.com`

The destination was reached after approximately 15 hops.

I learned that internet traffic does not simply travel directly from my computer to Google's server. It passes through multiple routers and networks on the way to the destination.

## Important Concepts

### DNS

DNS stands for Domain Name System.

Its job is to translate domain names into IP addresses.

Example:

`google.com -> DNS -> IP address`

### IP Address vs Port

An IP address identifies a destination on a network.

A port identifies the service that I want to communicate with on that destination.

For example:

`443 = HTTPS`

### HTTPS

HTTPS protects communication between my browser and a website using encryption through TLS.

## What Happens When I Visit google.com?

My current understanding is:

1. I enter google.com into my browser.
2. DNS finds an IP address for google.com.
3. Traffic travels through networks and routers towards Google's infrastructure.
4. An HTTPS/TLS connection is established, normally using port 443.
5. Google sends the requested data back to my browser.

## What I Learned

Before this lab, I had very little understanding of what happened behind the scenes when I opened a website.

After running these commands myself, I now understand the basic relationship between DNS, IP addresses, ports and network routing.

This is the first practical lab in my cybersecurity learning journey.
