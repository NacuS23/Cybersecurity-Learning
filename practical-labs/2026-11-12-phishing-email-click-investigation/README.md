# Phishing email and click investigation
Date: 12 November 2026

## Scope
Completed fictional exercise with reviewed answers and corrections. No real email, website or device was investigated.

## Supplied evidence
Approved hostname: `login.northbridge.example`

| Field | Value |
|---|---|
| Display name | Northbridge IT Support |
| Sender | support@account-review.example |
| Subject | Your account closes in 30 minutes |
| Request | Follow the link and enter a work password |
| Link | `https://login.northbridge.example.account-review.example/verify` |

| Row | Time | Source | Record |
|---|---|---|---|
| A | 10:00 | Email gateway | M55 delivered to Sam |
| B | 10:04 | Web security log | Sam's laptop requested the link; request blocked |
| C | 10:06 | User report | Sam reported clicking, seeing a blocked page and entering nothing |

Web evidence covers only Sam's laptop from 10:00 to 10:10. No phone evidence was supplied.

## Findings and reviewed answers
- Approved hostname: `login.northbridge.example`.
- Link hostname: `login.northbridge.example.account-review.example`. The sender email address is a different field.
- Reasons to investigate: urgent threat of losing access, a request for a work password, and a link hostname that differs from the approved destination. The block is relevant evidence but alone does not explain why the tool blocked it.
- Delivery: row A.
- Click: row B supports the website request; row C supplies Sam's confirmation of clicking.
- Password submission: Sam reports entering nothing. The supplied evidence does not establish credential theft.
- Block: that request from the laptop was blocked. This does not establish what happened on another device.
- HTTPS: does not alone establish website trustworthiness.
- Next check: contact Sam through a trusted method to ask whether the link was opened on another device or outside the recorded period.

## Clarifications from the exercise
I initially copied the sender address as the link hostname and thought the laptop block would also apply to a phone. After review, I recognised that the phone could open the link if it lacked the relevant filtering.

Web filtering can cover a company network or individual devices. This case does not specify the full deployment. The limitation is that the evidence demonstrates a block on one laptop, not universal protection. A phone might use different controls or mobile data. The company's website is not identified as the system performing the block.

## Factual handover
Message M55 was delivered to Sam at 10:00, and the link request from Sam's laptop was blocked at 10:04. Sam reports entering no password; the available evidence does not establish credential theft or what occurred on other devices.

## Takeaway
Keep delivery, clicking and password submission separate. State what each record supports and where coverage ends.

[Back to learning journal](../../README.md)
