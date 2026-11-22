"""Regenerate the synthetic Windows authentication fixture. No live events used."""
import json
from datetime import datetime, timedelta
from pathlib import Path

out = []

def add(ip, start, users, eid, logon_type=3, host="LAB-SRV-01"):
    t = datetime.fromisoformat(start.replace("Z", "+00:00"))
    for i, user in enumerate(users):
        out.append({
            "TimeCreated": (t + timedelta(minutes=i)).isoformat().replace("+00:00", "Z"),
            "EventID": eid,
            "TargetUserName": user,
            "IpAddress": ip,
            "LogonType": logon_type,
            "Computer": host
        })

add("198.51.100.25", "2026-11-22T10:00:00Z", ["alex", "sam", "maria", "alex", "sam"], 4625)
add("198.51.100.25", "2026-11-22T10:05:00Z", ["sam"], 4624)
add("203.0.113.80", "2026-11-22T10:10:00Z", ["backup"] * 6, 4625)
add("203.0.113.80", "2026-11-22T10:16:00Z", ["backup"], 4624)
add("192.0.2.70", "2026-11-22T10:20:00Z", ["amy", "ben", "cam", "amy", "ben"], 4625)
add("192.0.2.70", "2026-11-22T10:36:00Z", ["ben"], 4624)
add("203.0.113.75", "2026-11-22T10:30:00Z", ["lee", "pat", "robin", "lee", "pat"], 4625)
add("203.0.113.75", "2026-11-22T10:35:00Z", ["unrelated"], 4624)
add("192.0.2.90", "2026-11-22T10:58:00Z", ["emma", "noah", "olivia", "emma", "noah"], 4625)
add("192.0.2.90", "2026-11-22T11:03:00Z", ["noah"], 4624)
add("-", "2026-11-22T10:40:00Z", ["unknown1", "unknown2", "unknown3", "unknown1", "unknown2"], 4625)
add("198.51.100.66", "2026-11-22T10:45:00Z", ["local1", "local2", "local3", "local1", "local2"], 4625, logon_type=2)
out.sort(key=lambda r: (r["TimeCreated"], r["IpAddress"]))
assert len(out) == 41
path = Path(__file__).parent / "sample_events.jsonl"
path.write_text("".join(json.dumps(r, sort_keys=True) + "\n" for r in out), encoding="utf-8")
print("Created", path.name, "records", len(out))
