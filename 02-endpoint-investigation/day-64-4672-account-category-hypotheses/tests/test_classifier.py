import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from classify_4672 import classify_sid, load, summarize, validate_event  # noqa: E402

BASE = Path(__file__).resolve().parents[1] / "samples"

class TestClassification(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.a = summarize(load(BASE / "scenario_a.jsonl"))
        cls.b = summarize(load(BASE / "scenario_b.jsonl"))

    def test_known_system_sid(self):
        self.assertEqual(classify_sid("S-1-5-18"), "SYSTEM")

    def test_local_service_sid(self):
        self.assertEqual(classify_sid("S-1-5-19"), "LOCAL SERVICE")

    def test_network_service_sid(self):
        self.assertEqual(classify_sid("S-1-5-20"), "NETWORK SERVICE")

    def test_unknown_sid_is_not_assumed_malicious(self):
        self.assertEqual(classify_sid("S-1-5-21-999999-888888-777777-1001"), "OTHER / UNCLASSIFIED")

    def test_missing_and_invalid_sid(self):
        self.assertEqual(classify_sid(""), "MISSING SID")
        self.assertEqual(classify_sid("alice@work"), "INVALID SID")

    def test_same_privilege_frequencies_with_different_owners(self):
        self.assertEqual(self.a["events"], self.b["events"])
        self.assertEqual(self.a["events"], 12)
        self.assertEqual(self.a["privilege_counts"], self.b["privilege_counts"])
        self.assertEqual(self.a["different_privileges"], 12)
        self.assertEqual(self.a["privilege_appearances"], 135)

    def test_scenario_a_account_categories(self):
        self.assertEqual(self.a["category_counts"], {
            "SYSTEM": 9, "LOCAL SERVICE": 2, "NETWORK SERVICE": 1
        })
        self.assertEqual(self.a["other_or_invalid_or_missing"], 0)

    def test_scenario_b_account_categories(self):
        self.assertEqual(self.b["category_counts"], {
            "SYSTEM": 3, "OTHER / UNCLASSIFIED": 9
        })
        self.assertEqual(self.b["other_or_invalid_or_missing"], 9)

    def test_no_raw_sid_exposed_in_summary(self):
        for report in (self.a, self.b):
            output = json.dumps(report)
            self.assertNotIn("S-1-5-18", output)
            self.assertNotIn("S-1-5-21", output)

    def test_rejects_unexpected_fields(self):
        with self.assertRaisesRegex(ValueError, "expected only fields"):
            validate_event({"EventID": 4672, "SubjectUserSid": "S-1-5-18", "PrivilegeList": "SeDebugPrivilege", "username": "alice"}, 1)

    def test_rejects_invalid_event_id(self):
        with self.assertRaisesRegex(ValueError, "4672"):
            validate_event({"EventID": 4624, "SubjectUserSid": "S-1-5-18", "PrivilegeList": "SeDebugPrivilege"}, 1)

    def test_rejects_invalid_privilege_field(self):
        with self.assertRaisesRegex(ValueError, "PrivilegeList"):
            validate_event({"EventID": 4672, "SubjectUserSid": "S-1-5-18", "PrivilegeList": "not_a_privilege"}, 1)

if __name__ == "__main__":
    unittest.main()
