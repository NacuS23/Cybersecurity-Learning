# Day 7 - Ports, listening and services

Today I looked more at listening ports and how to find which process owns them.

I ran:

`netstat -ano | findstr LISTENING`

One line I picked was:

`TCP [::]:49664 [::]:0 LISTENING 1384`

At first `[::]` looked strange, but I learned it basically means all IPv6 interfaces on the computer.

Then I checked the PID with:

`tasklist | findstr 1384`

and got:

`lsass.exe 1384`

So I learned the useful process:

`port -> PID -> process`

In this case the port was 49664 and the process was `lsass.exe`.

I also learned that `lsass.exe` is a normal Windows security process, so a listening port that looks weird is not automatically malware.

Things I want to remember:

- LISTENING = waiting for an incoming TCP connection
- ESTABLISHED = an active TCP connection already exists
- 443 = HTTPS
- 3389 = RDP
- 127.0.0.1 means localhost / only this computer
- 0.0.0.0 means listening on all IPv4 interfaces
- [::] is the similar idea for IPv6

One thing I got wrong at first was thinking 127.0.0.1 had something to do with MAC addresses. It doesn't. It is just the loopback/localhost address.

Main lesson for me: if I see an unfamiliar port, I should not immediately think it is malware. I should first find the PID, the process and then investigate if that process and behaviour make sense.