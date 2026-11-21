# Validating log coverage — fictional worked example

**Date:** 21 November 2026  
**Evidence type:** Supplied fictional records; worked solution for study. No live endpoint checks or learner execution are claimed.

## Objective

Distinguish an empty central search from evidence that no activity occurred. Check whether logs were being collected before relying on a search result.

## Supplied evidence

Each computer should send one heartbeat per minute. The heartbeat collection report is complete for 10:00–10:05 inclusive.

| Computer | Heartbeats received | Failed sign-ins found centrally |
|---|---|---:|
| LAB-01 | Every minute, 10:00–10:05 | 0 |
| FIN-04 | 10:00 and 10:05 only | 0 |

At 10:06, a local log export is taken directly from FIN-04. It contains failed sign-ins at 10:02 and 10:03. Those records are absent from the central search. No explanation for the gap is supplied.

## Completed investigation note

| Question | Worked answer |
|---|---|
| FIN-04 missing heartbeat times | 10:01, 10:02, 10:03 and 10:04 |
| Failed sign-ins in central search | 0 |
| Failed sign-ins in local export | 2, at 10:02 and 10:03 |
| Confirmed observation | Four expected heartbeats are missing, and two locally recorded sign-in failures are absent from the central search. |
| Unconfirmed explanation | A temporary connection problem between the agent and collector could explain missing heartbeats and delayed event delivery. This is a hypothesis, not an established cause. |
| Next check | Review the agent's operational history around 10:00–10:06 for send failures, disconnects, restarts and queued-event delivery. |
| Question that check would answer | Was the agent running and attempting to forward data, and were there recorded errors or later retries? This can help distinguish agent failure from transport or downstream collection problems. |

## Knowledge-check answers

**1. Correct “FIN-04 had no failed sign-ins because the central search returned zero.”**

The central search returned no failed sign-ins, but FIN-04's local export contains two. The central result is incomplete relative to the supplied local evidence and cannot establish an absence of activity.

**2. Do missing heartbeats prove an attacker disabled logging?**

No. They establish that expected heartbeat messages were not received in the report. Agent faults, connectivity problems or other collection issues are possible. Deliberate interference would need additional evidence. The local sign-in records show that some local logging continued during the heartbeat gap.

**3. Does LAB-01 having every heartbeat guarantee all security events were collected?**

No. Heartbeats show that heartbeat messages arrived. Security events could still be excluded by configuration, delayed, dropped or unavailable to the collection process. Check the relevant event source, collection configuration and delivery health before claiming complete coverage.

## SOC handover

FIN-04 is missing four expected heartbeats between its 10:00 and 10:05 messages. Its local export contains two failed sign-ins absent from the central search, so the zero-result search must not be used to close the activity question. Review agent history and event forwarding, then check whether the missing events arrive later. The cause of the gap and the explanation for the sign-in failures remain unconfirmed.

## Limits

The missing heartbeat times do not establish the exact start or duration of an outage. The supplied records do not establish whether the sign-in failures were malicious or whether all other local or central events were collected. This write-up analyses the provided scenario only; it does not claim a running SIEM deployment or tests on a real device.
