# Day 11 - DNS security and NXDOMAIN

Today I looked at DNS from more of a security point of view.

I already knew that DNS translates a domain name into an IP address. Today I focused more on what happens when a domain does not exist and why DNS activity can be useful during an investigation.

## What I practiced

I ran:

```powershell
nslookup microsoft.com
```

and got:

```
microsoft.com
IPv6:
2620:1ec:48:1::64
2620:1ec:29:1::64

IPv4:
150.171.109.215
```

Then I ran:

```powershell
nslookup github.com
```

and got:

```
github.com
20.26.156.215
```

Both domains resolved successfully.

Then I tested a made-up hostname:

```powershell
nslookup this-domain-should-not-exist-927361.example
```

The result was:

```
Non-existent domain
```

This is the same idea as NXDOMAIN.

## What NXDOMAIN means

NXDOMAIN means DNS could not find that domain or hostname.

One failed DNS lookup is normal.

What becomes more interesting is when a computer makes lots of repeated DNS queries for random-looking names and many of them fail.

That still does not automatically mean malware, but it is something I would investigate.

## Security thinking

If I saw a strange domain in DNS logs, I would want to check things like:

- what IP it resolves to
- which computer queried it
- which process caused the query
- how often it was queried
- whether other computers also queried it
- whether the domain is known for phishing or malware

Certificates could also sometimes be useful later if the domain is actually serving HTTPS.

## Something I noticed

My DNS server showed as:

```
Server: UnKnown
Address: fe80::8c98:6bff:fe13:264
```

The DNS lookups still worked correctly.

I learned that `Server: UnKnown` does not mean DNS is broken. It can simply mean nslookup could not reverse-resolve a hostname for the DNS server address.

## What I want to remember

- DNS = domain name to IP address
- NXDOMAIN = domain/hostname does not exist
- One strange domain does not mean malware
- Repeated random-looking DNS failures can be worth investigating
- DNS logs can show which domains a device tried to contact
- Always look for more context before deciding something is malicious
