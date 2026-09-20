# Day 10 - HTTPS, TLS and certificates

Today I learned what makes HTTPS different from HTTP and why port 443 does not automatically mean something is safe.

## What I practiced

I used curl against example.com:

```powershell
curl.exe -v https://example.com
```

Some of the useful lines I got were:

```
Host example.com:443 was resolved
IPv4: 104.20.23.154, 172.66.147.243
Trying 104.20.23.154:443...
Established connection to example.com (104.20.23.154 port 443)
schannel: SSL/TLS connection renegotiated
HTTP/1.1 200 OK
Server: cloudflare
```

This showed me the connection flow:

```
example.com
-> DNS
-> IP address
-> port 443
-> TLS
-> HTTP request
-> HTTP 200 response
```

I also learned that this line:

```
schannel: disabled automatic use of client certificate
```

does not mean the website certificate is disabled. It just means curl is not automatically sending my own client certificate.

## What TLS does

TLS protects the connection by encrypting the traffic between my computer and the server.

That is why HTTPS traffic cannot normally be read directly in Wireshark like plain HTTP traffic.

I can still see things like:

- IP addresses
- ports
- timing
- packet sizes
- TCP connections

but the actual HTTPS application data is encrypted.

## Certificates

A digital certificate helps the browser verify that the server/domain it connected to is presenting a certificate valid for that hostname and chained to a trusted issuer.

A valid certificate does not mean the website itself is trustworthy.

A phishing or malicious website can still use HTTPS and have a valid certificate.

## Mistake I made today

I mixed up HTTPS with IPv6.

I thought HTTPS was the secure version using IPv6 instead of IPv4.

That is wrong.

A better way to remember it is:

```
IPv4 / IPv6 = addressing systems
HTTP / HTTPS = web protocols
TLS = encryption/security layer
443 = HTTPS
```

HTTP and HTTPS can both work over IPv4 or IPv6.

## What I want to remember

- TLS encrypts the connection
- HTTP is not protected by TLS
- HTTPS is HTTP protected by TLS
- 443 normally means HTTPS
- HTTPS does not automatically mean the website is safe
- Certificates help verify the server/domain
- Wireshark usually cannot directly read HTTPS content because it is encrypted
