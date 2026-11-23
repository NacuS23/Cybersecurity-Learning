"""Day 60 schema checks using fictional, pseudonym-shaped JSONL only."""
import json
import tempfile
import unittest
from pathlib import Path

from verify_export import read_and_validate, summarize, validate_row

FIXTURE = Path(__file__).resolve().parents[1] / "sample/synthetic_export.jsonl"


class ExportValidationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.events = read_and_validate(FIXTURE)

    def test_loads_all_nine_fixture_records(self):
        self.assertEqual(len(self.events), 9)

    def test_expected_counts(self):
        self.assertEqual(summarize(self.events), {
            "records": 9,
            "logon_success_4624": 2,
            "logon_failure_4625": 7,
            "network_type3": 8,
            "unknown_or_local_source": 1,
            "distinct_account_pseudonyms": 4
        })

    def test_pseudonyms_are_consistent_for_same_account_and_ip(self):
        self.assertEqual(self.events[0]["TargetUserName"], self.events[3]["TargetUserName"])
        self.assertEqual(self.events[1]["TargetUserName"], self.events[5]["TargetUserName"])
        self.assertEqual(self.events[0]["IpAddress"], self.events[5]["IpAddress"])

    def test_rejects_unredacted_username(self):
        row = self.events[0].copy()
        row["TargetUserName"] = "Alice"
        with self.assertRaisesRegex(ValueError, "pseudonymised"):
            validate_row(row, 1)

    def test_rejects_unredacted_ip(self):
        row = self.events[0].copy()
        row["IpAddress"] = "198.51.100.5"
        with self.assertRaisesRegex(ValueError, "pseudonymised"):
            validate_row(row, 1)

    def test_rejects_unredacted_computer(self):
        row = self.events[0].copy()
        row["Computer"] = "DESKTOP-PC"
        with self.assertRaisesRegex(ValueError, "pseudonymised"):
            validate_row(row, 1)

    def test_rejects_time_without_utc_timezone(self):
        row = self.events[0].copy()
        row["TimeCreated"] = "2026-11-23T10:00:00"
        with self.assertRaisesRegex(ValueError, "timestamp must be UTC"):
            validate_row(row, 1)

    def test_rejects_extra_sensitive_field(self):
        row = self.events[0].copy()
        row["TargetDomainName"] = "CORPORATE"
        with self.assertRaisesRegex(ValueError, "unexpected or missing"):
            validate_row(row, 1)

    def test_rejects_invalid_logon_type(self):
        row = self.events[0].copy()
        row["LogonType"] = "3"
        with self.assertRaisesRegex(ValueError, "LogonType"):
            validate_row(row, 1)

    def test_rejects_invalid_event_id(self):
        row = self.events[0].copy()
        row["EventID"] = 9999
        with self.assertRaisesRegex(ValueError, "EventID"):
            validate_row(row, 1)

    def test_jsonl_read_rejects_malformed_row(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "data.jsonl"
            path.write_text(json.dumps(self.events[0]) + "\nnot json\n", encoding="utf8")
            with self.assertRaisesRegex(ValueError, "line 2"):
                read_and_validate(path)


if __name__ == "__main__":
    unittest.main()
