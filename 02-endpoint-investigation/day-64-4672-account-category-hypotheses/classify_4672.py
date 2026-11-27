#!/usr/bin/env python3
"""Training-only: classify account categories in synthetic Windows Event 4672 JSONL.

Prints aggregates only; never prints full SIDs. Do not upload real events.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter
from pathlib import Path

WELL_KNOWN = {
    "S-1-5-18": "SYSTEM",
    "S-1-5-19": "LOCAL SERVICE",
    "S-1-5-20": "NETWORK SERVICE",
}
REQUIRED = {"EventID", "SubjectUserSid", "PrivilegeList"}
PRIVILEGE = re.compile(r"Se[A-Za-z]+Privilege\Z")
SID = re.compile(r"S-\d+(?:-\d+)+\Z")


def classify_sid(sid: str) -> str:
    if not isinstance(sid, str) or not sid:
        return "MISSING SID"
    if not SID.fullmatch(sid):
        return "INVALID SID"
    return WELL_KNOWN.get(sid, "OTHER / UNCLASSIFIED")


def validate_event(row: dict, index: int) -> dict:
    if not isinstance(row, dict) or set(row) != REQUIRED:
        raise ValueError(f"line {index}: expected only fields {sorted(REQUIRED)}")
    if type(row["EventID"]) is not int or row["EventID"] != 4672:
        raise ValueError(f"line {index}: expected Windows EventID 4672")
    sid = row["SubjectUserSid"]
    if not isinstance(sid, str):
        raise ValueError(f"line {index}: SubjectUserSid must be text")
    raw = row["PrivilegeList"]
    if not isinstance(raw, str):
        raise ValueError(f"line {index}: PrivilegeList must be text")
    names = raw.split()
    if not names or any(not PRIVILEGE.fullmatch(name) for name in names):
        raise ValueError(f"line {index}: invalid PrivilegeList")
    return {"category": classify_sid(sid), "privileges": set(names)}


def load(path: Path) -> list[dict]:
    events: list[dict] = []
    with path.open(encoding="utf-8") as handle:
        for index, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {index}: malformed JSON") from exc
            events.append(validate_event(obj, index))
    return events


def summarize(events: list[dict]) -> dict:
    cats = Counter(event["category"] for event in events)
    privileges = Counter(name for event in events for name in event["privileges"])
    return {
        "events": len(events),
        "category_counts": dict(sorted(cats.items())),
        "other_or_invalid_or_missing": sum(
            count for category, count in cats.items()
            if category in ("OTHER / UNCLASSIFIED", "INVALID SID", "MISSING SID")
        ),
        "different_privileges": len(privileges),
        "privilege_appearances": sum(privileges.values()),
        "privilege_counts": dict(sorted(privileges.items())),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path, help="fictional normalized 4672 JSONL")
    args = parser.parse_args()
    report = summarize(load(args.events))
    print(json.dumps(report, indent=2, sort_keys=True))
    print("Synthetic training data only. An OTHER category requires context, not automatic alarm.")


if __name__ == "__main__":
    main()
