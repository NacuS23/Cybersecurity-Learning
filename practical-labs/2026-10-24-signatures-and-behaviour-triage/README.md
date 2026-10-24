# Valid signatures and suspicious behaviour

Date: 24 October 2026

Fictional alert-triage practice. The evidence below was supplied for the exercise, not collected from my computer. My answers and the clarifications from the review are recorded separately.

## Goal

Use several pieces of evidence to prioritise alerts without treating a valid signature or a connection count as proof of safety or malicious activity.

## Supplied scenarios

| Evidence | Alert A | Alert B |
|---|---|---|
| Program | Chat application | PowerShell |
| Signature | Valid, expected publisher | Valid, Microsoft |
| Location | Expected application folder | Expected Windows folder |
| Activity | Four connections while the user joins a voice call | Downloads a script shortly after a document is opened |
| Parent process | Application updater | Word |
| User explanation | Confirms opening the app and joining the call | Expected only to read a document |
| Script contents | Not applicable | Not examined yet |

## My triage answers

### Alert A

**My priority:** Low.

**My reason:**

> It seems everything from the signature, location of the file, parent process it all seems ok

**My next check:**

> I would check the 4 connections and then close if it's nothing dangerous.

**Review:** The low priority is supported by the combined evidence. The user's confirmation of joining a voice call is also relevant. Checking the connection destinations and whether they fit expected activity is sensible. Four connections alone do not establish suspicious activity. Any closure should describe the checks and their limits, for example: “No suspicious indicators found in the checks performed.”

### Alert B

**My priority:** High.

**My reason:**

> The process that it downloaded a script after it opened the file is concerining and the file should only read a document.

**My next check:**

> Check what the script opened. in a text.

**Review:** Prompt investigation is justified by the unexpected script download and Word launching PowerShell when the user expected only to read a document. The next check is to inspect the downloaded script as text without executing it. This priority is not a verdict that malware has been confirmed.

## Knowledge check

1. **Does having four connections alone prove suspicious activity?** My answer: No. Correct; purpose and context matter.
2. **Can a legitimate signed tool be used for harmful purposes?** My answer: Yes. Correct.
3. **Which two details in Alert B need investigation?** My answer: “The script and i don't know the other one.” The additional detail clarified in the review was Word launching PowerShell. Both the script's contents and the process relationship need explaining.
4. **Does decoding a script into readable text automatically execute it?** My answer: No. Correct; decoding and displaying text are different from executing it.

## My conclusion and clarification

Asked to correct “The file has a valid Microsoft signature, so the alert can be closed,” I answered:

> The signature would only say at the time that the signature is valid ,but it could still be malware and be dangerous.

**Clarification:** A valid digital signature supports who signed a file and that its signed contents have not changed since signing. It does not guarantee safe behaviour. PowerShell can be a legitimate signed program while the instructions it runs are harmful.

**Reviewed conclusion for Alert B:** The signature is valid, but Word launching PowerShell to download an unexpected script still needs investigation.

## What I learned

Combine signatures, file locations, parent processes, user activity and network behaviour. A reassuring check is one piece of evidence, not a reason to ignore contradictory behaviour.

No script was executed or real alert closed in this exercise.
