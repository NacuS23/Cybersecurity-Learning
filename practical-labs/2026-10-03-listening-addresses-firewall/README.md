# Listening addresses and Windows Firewall profiles

Completed: 3 October 2026  
Type: Guided, read-only practice on my own Windows computer

## What I did

I checked TCP listeners, identified the program behind one port and checked my active network and firewall profiles. I ran the commands myself and answered the review questions.

## 1. List listening ports

```powershell
Get-NetTCPConnection -State Listen |
Sort-Object LocalPort |
Select-Object -First 15 LocalAddress, LocalPort, OwningProcess |
Format-Table -AutoSize
```

Selected rows from my actual output:

```text
LocalAddress  LocalPort OwningProcess
------------  --------- -------------
::                  135          1768
0.0.0.0             135          1768
0.0.0.0            2968         11664
127.0.0.1          9080          6008
```

I learned that:
- 127.0.0.1 is IPv4 loopback: connections from this computer only.
- ::1 is IPv6 loopback.
- 0.0.0.0 is a wildcard: all local IPv4 interfaces.
- :: is the IPv6 wildcard. With a port, it is written like [::]:135.
- The same process can own both IPv4 and IPv6 listeners, as PID 1768 did on port 135.
- Listening means waiting for connections, not proof that another device can reach the port.

## 2. Identify the process behind port 2968

```powershell
Get-Process -Id 11664 |
Select-Object ProcessName, Id, Path |
Format-List
```

```text
ProcessName : EEventManager
Id          : 11664
Path        : C:\Program Files (x86)\Epson Software\Event Manager\EEventManager.exe
```

I linked TCP port 2968 to PID 11664 and then to Epson Event Manager. The name and path matched my earlier Epson exercise, but the PID was different. PIDs can change and be reused.

## 3. Check the active network profile

```powershell
Get-NetConnectionProfile |
Select-Object InterfaceAlias, NetworkCategory |
Format-Table -AutoSize
```

```text
InterfaceAlias NetworkCategory
-------------- ---------------
Wi-Fi                  Private
```

Private is the network category Windows uses to select the applicable firewall profile. It does not prove that the network is safe or that all traffic is allowed.

## 4. Check the Private firewall profile

```powershell
Get-NetFirewallProfile -Name Private |
Select-Object Name, Enabled, DefaultInboundAction |
Format-List
```

```text
Name                 : Private
Enabled              : True
DefaultInboundAction : NotConfigured
```

The Private firewall profile was enabled. During review, I learned that NotConfigured means the default inbound action was not explicitly configured in the policy store queried. It does not mean incoming traffic is automatically allowed. This output alone did not establish the effective inbound decision for Epson.

## My answers

**Does 0.0.0.0:2968 alone prove someone on the internet can connect?**

My answer: "No, it's not enough." Correct. Firewall rules and router/network configuration also matter.

**If Epson listened on 127.0.0.1:2968, could another computer connect directly to that listener over Wi-Fi?**

My answer: "no". Correct. Loopback accepts connections from the same computer only.

**Does an enabled firewall mean every incoming connection is blocked?**

My answer: "no, there are some rules which allow". Correct as a general principle: specific allow rules can exist. I did not inspect or confirm an Epson allow rule in this exercise.

## Conclusion

Epson Event Manager was listening on TCP port 2968 across all local IPv4 interfaces. My Wi-Fi used the Private profile, whose firewall was enabled. I did not inspect the applicable rules or test reachability, so I cannot conclude that another device or the internet could access this port.

This exercise helped me separate a listening service from a reachable service. No firewall settings were changed. The public note uses selected output and omits my device's private IP address.
