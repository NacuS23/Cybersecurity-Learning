"""Generate two *fictional* log sets with the same privilege totals but different account owners."""
from pathlib import Path
import json

OUT = Path(__file__).parent / "samples"
OUT.mkdir(parents=True, exist_ok=True)
COMMON = [
    "SeRestorePrivilege",
    "SeDelegateSessionUserImpersonatePrivilege",
    "SeDebugPrivilege",
    "SeImpersonatePrivilege",
    "SeSystemEnvironmentPrivilege",
    "SeSecurityPrivilege",
    "SeBackupPrivilege",
    "SeLoadDriverPrivilege",
    "SeTakeOwnershipPrivilege",
]
EXTRA = ["SeAssignPrimaryTokenPrivilege", "SeAuditPrivilege", "SeTcbPrivilege"]

# A: the 9 full-privilege events belong to SYSTEM; 3 are other built-ins.
scenario_a = ["S-1-5-18"] * 9 + ["S-1-5-19"] * 2 + ["S-1-5-20"]
# B: the same 9 full-privilege events belong to a made-up OTHER account.
scenario_b = ["S-1-5-21-999999-888888-777777-1001"] * 9 + ["S-1-5-18"] * 3

for name, owners in (("scenario_a.jsonl", scenario_a), ("scenario_b.jsonl", scenario_b)):
    rows = [{
        "EventID": 4672,
        "SubjectUserSid": sid,
        "PrivilegeList": " ".join(COMMON + (EXTRA if idx < 9 else [])),
    } for idx, sid in enumerate(owners)]
    (OUT / name).write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in rows), encoding="utf-8")
    print(name, len(rows))
