# Configuration-change timeline — 31 October 2026

Fictional SOC practice using supplied records, followed by reviewed conclusions. No settings were changed and no malware was executed for this exercise.

## Objective

Distinguish notification changes from protection changes, calculate a protection gap, and separate timing from proof of causation.

## Supplied case

All records concern TRAINING-PC on the same day. These are simplified training fields, not actual Windows setting names or event IDs. Protection-change records are assumed complete from 10:00 to 10:10.

| Time | Record | Setting | Old value | New value |
|---|---|---|---|---|
| 10:00 | Configuration change | Notification pop-ups | Enabled | Disabled |
| 10:03 | Configuration change | Real-time protection | Enabled | Disabled |
| 10:07 | Configuration change | Real-time protection | Disabled | Enabled |
| 10:10 | Status check | Real-time protection | — | Enabled |

An approved maintenance ticket permits notification changes only. A process-start record shows update-helper.exe starting from a temporary folder at 10:05. The supplied records do not identify who changed protection.

## Exercise and reviewed findings

| Question | Reviewed conclusion |
|---|---|
| When did notifications change? | 10:00. |
| When did protection stop and return? | Disabled at 10:03; enabled at 10:07. |
| How long was the recorded gap? | Four minutes. |
| Did the process start before, during or after the gap? | During, at 10:05. |
| Did the maintenance ticket authorise the protection change? | No; it covered notifications only. |
| What does the 10:10 record establish? | Protection was enabled at that check. It does not erase the earlier gap. |

## Practice discussion

I correctly identified that 10:10 was a status check and that protection was enabled again at 10:07. Initially I counted the gap from the notification change at 10:00. After reviewing the separate settings, the correct protection gap was 10:03–10:07, lasting four minutes.

I answered “During” for the process start and suggested investigating the file further. My initial suspicion that the file was the main actor was stronger than the evidence supported. I then correctly confirmed the order: “disabled first and then the file.”

## Final investigation note

Real-time protection was disabled at 10:03 and restored at 10:07. update-helper.exe started during that interval at 10:05. Its timing and temporary-folder location warrant investigation but do not prove maliciousness or that this process caused the earlier change. The supplied evidence does not establish an attack or identify the responsible account or process.

The next evidence request is for records identifying the account and process responsible for disabling protection at 10:03. Further file checks would include its full path, signature, parent process and command line. These are proposed next steps, not checks performed in this fictional exercise.

## Key learning

Read the setting name and old/new values together. Current status does not establish historical status, and events occurring close together do not by themselves establish causation.
