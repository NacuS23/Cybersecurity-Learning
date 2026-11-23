#!/usr/bin/env python3
"""Validate Day 60 pseudonymised Windows Security JSONL exports. Python stdlib only.

This is a schema/privacy sanity check, NOT a guarantee of anonymity or security.
"""
from __future__ import annotations

import argparse
import json
import re
from datetime import datetime
from pathlib import Path

REQUIRED = {
    "TimeCreated", "EventID", "TargetUserName", "IpAddress", "LogonType", "Computer"
}
PATTERNS = {
    "TargetUserName": re.compile(r"acct_[0-9a-f]{16}\Z"),
    "IpAddress": re.compile(r"ip_[0-9a-f]{16}\Z"),
    "Computer": re.compile(r"host_[0-9a-f]{16}\Z"),
}


def validate_row(row: dict, line_number: int) -> dict:
    if not isinstance(row, dict):
        raise ValueError(f"line {line_number}: expected JSON object")
    if set(row) != REQUIRED:
        raise ValueError(f"line {line_number}: unexpected or missing fields")
    if type(row["EventID"]) is not int or row["EventID"] not in (4624, 4625):
        raise ValueError(f"line {line_number}: invalid EventID")
    if type(row["LogonType"]) is not int or not (0 <= row["LogonType"] <= 13):
        raise ValueError(f"line {line_number}: invalid LogonType")
    raw_time = row["TimeCreated"]
    if not isinstance(raw_time, str):
        raise ValueError(f"line {line_number}: invalid timestamp")
    try:
        ts = datetime.fromisoformat(raw_time.replace("Z", "+00:00"))
    except ValueError as exc:
        raise ValueError(f"line {line_number}: invalid ISO timestamp") from exc
    if ts.tzinfo is None or not raw_time.endswith("Z"):
        raise ValueError(f"line {line_number}: timestamp must be UTC with Z")
    for key, regex in PATTERNS.items():
        val = row[key]
        if not isinstance(val, str):
            raise ValueError(f"line {line_number}: invalid {key}")
        if val != "-" and not regex.fullmatch(val):
            raise ValueError(f"line {line_number}: {key} is not in pseudonymised format")
    if row["TargetUserName"] == "-":
        raise ValueError(f"line {line_number}: missing account pseudonym")
    return row


def read_and_validate(path: Path) -> list[dict]:
    rows = []
    with path.open(encoding="utf-8-sig") as file:
        for n, line in enumerate(file, start=1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"line {n}: malformed JSON") from exc
            rows.append(validate_row(row, n))
    return rows


def summarize(rows: list[dict]) -> dict:
    return {
        "records": len(rows),
        "logon_success_4624": sum(r["EventID"] == 4624 for r in rows),
        "logon_failure_4625": sum(r["EventID"] == 4625 for r in rows),
        "network_type3": sum(r["LogonType"] == 3 for r in rows),
        "unknown_or_local_source": sum(r["IpAddress"] == "-" for r in rows),
        "distinct_account_pseudonyms": len({r["TargetUserName"] for r in rows}),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("jsonl", type=Path)
    args = parser.parse_args()
    rows = read_and_validate(args.jsonl)
    print(json.dumps(summarize(rows), indent=2, sort_keys=True))
    print("Schema verified; privacy is NOT guaranteed. Keep genuine exports local.")


if __name__ == "__main__":
    main()
