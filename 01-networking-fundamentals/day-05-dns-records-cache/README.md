# Day 5 - DNS records and cache

Today I went a bit deeper into DNS.

I already knew DNS changes a name like `google.com` into an IP, but today I learned there are different DNS record types and Windows also keeps DNS answers in a cache.

## Commands I used

`ipconfig /displaydns`

This showed loads of DNS entries saved on my computer.

`ipconfig /flushdns`

This worked and cleared the DNS cache.

`nslookup google.com`

The DNS server that answered me was:

`cache1.service.virginmedia.net`

with IP:

`194.168.4.100`

Google returned both IPv6 and IPv4 addresses.

IPv6 examples:

`2a00:1450:4009:c0b::8b`

`2a00:1450:4009:c0b::64`

IPv4 examples:

`142.250.140.138`

`142.250.140.100`

Easy way I am remembering it for now:

- IPv4 usually has dots
- IPv6 has colons

I also saw `Non-authoritative answer`, which I learned means the DNS server answering me was not Google's own authoritative DNS server. It was giving me an answer it had already learned/cached.

## DNS record types I learned

- A record = IPv4 address
- AAAA record = IPv6 address
- MX record = mail server for a domain
- CNAME = alias to another hostname

I forgot some of these in the memory test, especially MX, so I need to repeat them later.

## Something interesting I found

In my DNS cache I saw entries like:

`assets.msn.com`

which followed CNAMEs through things like Microsoft traffic manager and Akamai.

I also saw Steam-related DNS entries.

At first some of the names looked strange, but I learned that a strange looking domain name does not automatically mean malware. Big companies can use CDNs, aliases and traffic-routing services that make DNS names look complicated.

## What I understood about DNS cache

Windows saves recent DNS answers so it doesn't have to ask a DNS server every single time for the same name.

The answers only stay for a certain amount of time depending on the TTL.

## Why DNS matters for cybersecurity

DNS logs can help show what domains a device was trying to contact.

That could be useful if a computer is talking to a strange or malicious domain, if malware is calling home, or if there is some kind of DNS spoofing/poisoning problem.

My main takeaway today:

`A = IPv4`

`AAAA = IPv6`

`MX = mail server`

`DNS cache = saves recent answers`

I still need more repetition with the record types, but the actual commands are starting to make sense.