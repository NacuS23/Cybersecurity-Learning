# Day 18 - SOC-style connection investigation

Today I followed one live network connection from netstat through to the process and then checked the executable itself.

## Connection observed

I started with an established TCP connection and identified:

```
Local IP: 192.168.0.188
Local/source port: 57525
Remote IP: 172.217.113.4
Remote port: 443
```

Port `443` normally indicates HTTPS traffic.

## Process identification

The connection belonged to PID:

```
21916
```

I checked the process and found:

```
NVIDIA Overlay.exe
```

This gave me the first important link:

```
Network connection
-> PID
-> process
```

## Reverse DNS check

I ran:

```powershell
nslookup 172.217.113.4
```

The lookup returned:

```
Non-existent domain
```

This showed that the IP did not have a reverse-DNS hostname returned by the resolver.

A failed reverse lookup does not automatically mean the IP is malicious.

## Executable path

I checked the process location and found:

```
C:\Program Files\NVIDIA Corporation\NVIDIA App\CEF\NVIDIA Overlay.exe
```

The location is consistent with an NVIDIA application installation.

## Digital signature check

I then checked the file with:

```powershell
Get-AuthenticodeSignature "C:\Program Files\NVIDIA Corporation\NVIDIA App\CEF\NVIDIA Overlay.exe"
```

The result was:

```
Status: Valid
```

This gave additional evidence that the executable had a valid digital signature.

## Investigation summary

The checks I used were:

```
connection
-> remote port
-> PID
-> process name
-> executable path
-> digital signature
-> reverse DNS
```

The process name alone was not enough to make a decision. The path and valid signature gave much stronger context.

At the end of the checks, there was no immediate evidence from the information collected that the connection was malicious.

## What I want to remember

- 443 normally means HTTPS, but that alone does not prove a connection is safe
- PID links a network connection to a running process
- Process path is useful when checking whether an executable looks expected
- A valid digital signature is useful supporting evidence
- Reverse DNS failure does not automatically mean an IP is suspicious
- Good investigation means collecting several pieces of evidence before reaching a conclusion
