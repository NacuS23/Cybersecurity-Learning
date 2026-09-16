# Day 6 - Wireshark and packets

Today was the first time I actually looked at network packets instead of only using command prompt commands.

I installed Wireshark and Npcap and used my active network connection to capture traffic.

At first it was confusing because the page was constantly filling with new packets and there was a lot of information happening at once.

## Filters I tried

I used:

`dns`

This showed DNS traffic and I could click on packets and look at things like the protocol and addresses.

Then I changed the filter to:

`icmp`

and used:

`ping 8.8.8.8`

This let me see ICMP traffic from ping.

Then I changed the filter to:

`tcp`

There was a lot of TCP traffic so I stopped the live capture and used:

`tcp.flags.syn == 1`

That made it easier to see SYN packets.

I also saw TCP retransmissions.

## Things I learned

Wireshark captures network packets that my computer can see going in and out.

Ping normally uses ICMP.

The TCP handshake is:

`SYN -> SYN-ACK -> ACK`

I got this order wrong at first but now I know it.

A TCP retransmission means data was sent again because the expected acknowledgement did not arrive in time. This can happen because of packet loss, Wi-Fi problems, congestion or timing.

The biggest thing I noticed is that there is a massive amount of normal traffic. Just because something looks unusual does not automatically mean there is a problem.

I am starting to understand that I need context, for example:

- where the connection is going
- what process started it
- what port it is using
- what domain it contacted
- if it keeps happening
- what other evidence is available

Wireshark feels like a microscope for network traffic. It lets me see the packets, but I still need practice learning what the information means.
