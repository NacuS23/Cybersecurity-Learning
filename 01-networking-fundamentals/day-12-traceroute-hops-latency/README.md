# Day 12 - Traceroute, hops and latency

Today I went back to traceroute, but this time I looked more closely at what each hop means and how to read delays and timeouts.

## What I practiced

I ran:

```powershell
tracert example.com
```

The destination resolved to:

```
172.66.147.243
```

My trace completed in 10 hops.

The first hop was:

```
172.20.10.1
```

which is my local gateway/router.

## My traceroute

```
1     2 ms     2 ms     2 ms  172.20.10.1
2     *        *        *     Request timed out.
3    56 ms   128 ms    30 ms  192.168.254.105
4     *        *        *     Request timed out.
5    47 ms    33 ms    39 ms  172.20.104.56
6     *       37 ms    46 ms  63.130.172.27
7    49 ms    81 ms    53 ms  141.101.71.166
8    62 ms    51 ms    87 ms  141.101.71.175
9    48 ms   150 ms    40 ms  141.101.71.205
10   40 ms    50 ms    47 ms  172.66.147.243
```

The destination was reached successfully.

## What I learned

A hop is one router or network step that traffic passes through on the way to the destination.

`tracert` helps show the route through the network hop by hop and gives rough timing information for each step.

I saw some hops with:

```
* * *
```

That does not automatically mean the connection is broken. A router can ignore or block traceroute probes while still forwarding traffic normally.

That happened in my trace because hops 2 and 4 timed out, but later hops still replied and the final destination was reached.

## Latency

I also saw a few higher numbers, like:

```
128 ms
150 ms
```

I learned not to judge a route from one high number.

For example, hop 3 had a 128 ms reply, but the final destination was around 40-50 ms. That means one router may have responded slowly to the probe without the whole route actually being that slow.

If latency starts increasing and stays high across later hops, that can be more useful because it may show where delay is starting.

## What I want to remember

- Hop = one router/network step
- tracert = shows the route to a destination
- First hop is usually the local gateway/router
- * * * does not automatically mean failure
- One high latency result does not prove a problem
- Look for patterns across later hops
