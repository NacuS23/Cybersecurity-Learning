# Put delayed logs in the right order

**22 November 2026 · Fictional worked example**

This solution analyses supplied training records. It does not claim learner execution, a real incident, or a live SIEM deployment.

## Objective and core concept

Build an activity timeline using event time while tracking what evidence was available at each search. Event time records when activity happened; received time records when the central logging system received its record.

## Supplied evidence

All records concern FIN-04 on the same date, with the same timezone and synchronised clocks. Each row is a separate event.

| Row | Event time | Received time | Recorded event | Delivery delay |
|---|---|---|---|---|
| A | 10:02 | 10:08 | Alex — failed sign-in | 6 minutes |
| B | 10:03 | 10:08 | Alex — failed sign-in | 5 minutes |
| C | 10:06 | 10:06 | Alex — successful sign-in | 0 minutes |
| D | 10:05 | 10:05 | Logging agent reconnects | 0 minutes |

Delays are calculated at the minute precision supplied.

## Completed timeline

**Event-time order: A, B, D, C.**

1. 10:02 — Alex failed sign-in.
2. 10:03 — Alex failed sign-in.
3. 10:05 — Logging agent reconnects.
4. 10:06 — Alex successful sign-in.

The successful sign-in arrived centrally before either failure, but occurred after both failures. Arrival order is not activity order. The relative arrival order of A and B within 10:08 is not supplied.

## Compare the searches

Both searches request Alex's sign-ins with event times from 10:00 through 10:06 inclusive. For this exercise, availability is determined by received time.

| Search time | Available matching rows | Explanation |
|---|---|---|
| 10:07 | C only | The success had arrived; A and B had not. |
| 10:09 | A, B and C | Both older failures arrived at 10:08 and match the unchanged event-time window. |

D was received by both searches but is not a sign-in record and therefore does not match the question.

**Why the results changed:** Delayed delivery made two older events available after the first search. The query conditions stayed the same, but the evidence available centrally changed.

## Knowledge-check answers

**Correct “The successful sign-in happened before both failures because it appeared in the system first.”**

The failures happened at 10:02 and 10:03, before the success at 10:06. Their records arrived later, at 10:08.

**Does success prove Alex personally entered the credentials?**

No. It establishes a recorded successful sign-in for the account, not the identity of the human responsible. Device, session and authentication context, and trusted confirmation where appropriate, would help investigate.

**Does reconnecting at 10:05 establish the exact cause of the delayed records?**

No. It is relevant context, but does not establish where or why delivery was delayed. Agent queue and forwarding records, transport errors and collector processing records could help locate the delay. A temporary disconnection is a possible explanation, not a confirmed cause.

## SOC handover

FIN-04 recorded two failed sign-ins for Alex before a successful sign-in. The failures arrived five and six minutes late, so the 10:07 central search showed only the success; the same search at 10:09 included both failures. Agent reconnection provides context, but the delivery-delay cause and the identity behind the sign-ins remain unconfirmed.

## Evidence limits

The supplied timestamps support ordering because synchronised clocks and a common timezone are stipulated. The records do not establish malicious activity, that the failures and success had the same human actor, or that all relevant events were collected. No new sign-in activity is needed to explain why the repeated search returned more results.
