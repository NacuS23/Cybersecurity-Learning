#!/usr/bin/env python3
"""Training-only Windows logon detection prototype (synthetic normalized JSONL input).

No live Security log, SIEM API, or raw EVTX reader is used.
"""
from __future__ import annotations

import argparse
import json
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

FAILURE_ID = 4625
SUCCESS_ID = 4624
WINDOW = timedelta(minutes=5)
FOLLOW_UP = timedelta(minutes=10)
MIN_FAILURES = 5
MIN_ACCOUNTS = 3


def timestamp(value: str) -> datetime:
    """Parse UTC time; reject unzoned timestamps rather than guessing."""
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("TimeCreated must include a timezone")
    return result.astimezone(timezone.utc)


def load_events(path: Path) -> list[dict[str, Any]]:
    """Load a synthetic, normalized JSON-lines data file."""
    events = []
    with path.open(encoding="utf-8") as handle:
        for line_num, line in enumerate(handle, 1):
            if not line.strip():
                continue
            try:
                row = json.loads(line)
                event = {
                    "at": timestamp(str(row["TimeCreated"])),
                    "event_id": int(row["EventID"]),
                    "user": str(row["TargetUserName"]).strip().lower(),
                    "source_ip": str(row["IpAddress"]).strip(),
                    "logon_type": int(row["LogonType"]),
                    "host": str(row.get("Computer", "")),
                }
            except (KeyError, ValueError, TypeError, json.JSONDecodeError) as exc:
                raise ValueError(f"{path.name} line {line_num}: {exc}") from exc
            events.append(event)
    return events


def in_scope(event: dict[str, Any]) -> bool:
    """Only network logons with a reported source IP; not every Windows logon has one."""
    return (
        event["event_id"] in (FAILURE_ID, SUCCESS_ID)
        and event["logon_type"] == 3
        and event["source_ip"] not in ("", "-", "::1", "127.0.0.1")
        and bool(event["user"])
    )


def detect(events: list[dict[str, Any]]) -> dict[str, Any]:
    scoped = sorted((e for e in events if in_scope(e)), key=lambda e: (e["at"], e["source_ip"]))
    by_ip_failures: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_ip_successes: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in scoped:
        if event["event_id"] == FAILURE_ID:
            by_ip_failures[event["source_ip"]].append(event)
        else:
            by_ip_successes[event["source_ip"]].append(event)

    findings = []
    for ip, failures in by_ip_failures.items():
        index = 0
        while index < len(failures):
            start = failures[index]["at"]
            end = start + WINDOW
            end_index = index
            while end_index < len(failures) and failures[end_index]["at"] < end:
                end_index += 1
            window_events = failures[index:end_index]
            accounts = sorted({e["user"] for e in window_events})
            if len(window_events) >= MIN_FAILURES and len(accounts) >= MIN_ACCOUNTS:
                last_failure = window_events[-1]["at"]
                # A subsequent 4624 must be for an account seen in the cluster.
                matched = [
                    e for e in by_ip_successes.get(ip, [])
                    if e["user"] in accounts
                    and last_failure < e["at"] <= last_failure + FOLLOW_UP
                ]
                findings.append({
                    "source_ip": ip,
                    "window_start": start.isoformat(),
                    "last_failure": last_failure.isoformat(),
                    "failed_attempts": len(window_events),
                    "distinct_accounts": len(accounts),
                    "accounts": accounts,
                    "correlated_successes": [
                        {"user": e["user"], "at": e["at"].isoformat(), "host": e["host"]}
                        for e in matched
                    ],
                    "follow_up_needed": bool(matched),
                })
                # Suppress overlapping duplicates from the same burst; a later burst
                # can still be detected after this five-minute candidate window.
                index = end_index
            else:
                index += 1

    findings.sort(key=lambda f: (f["window_start"], f["source_ip"]))
    return {
        "records_loaded": len(events),
        "records_in_scope": len(scoped),
        "records_excluded": len(events) - len(scoped),
        "candidate_bursts": len(findings),
        "bursts_with_targeted_success": sum(f["follow_up_needed"] for f in findings),
        "findings": findings,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("events", type=Path, help="normalized JSONL training data")
    args = parser.parse_args()
    report = detect(load_events(args.events))
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
