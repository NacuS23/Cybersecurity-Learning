"""Executable unit tests for Day 59. No external packages needed."""
import unittest
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from detector import detect, load_events, timestamp  # noqa: E402


FIXTURE = Path(__file__).resolve().parents[1] / "sample_events.jsonl"


class DetectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report = detect(load_events(FIXTURE))
        cls.by_ip = {f["source_ip"]: f for f in cls.report["findings"]}

    def test_expected_counts(self):
        self.assertEqual(self.report["records_loaded"], 41)
        self.assertEqual(self.report["records_in_scope"], 31)
        self.assertEqual(self.report["records_excluded"], 10)
        self.assertEqual(self.report["candidate_bursts"], 4)
        self.assertEqual(self.report["bursts_with_targeted_success"], 2)

    def test_positive_spray_then_targeted_success(self):
        f = self.by_ip["198.51.100.25"]
        self.assertEqual(f["failed_attempts"], 5)
        self.assertEqual(f["distinct_accounts"], 3)
        self.assertEqual([x["user"] for x in f["correlated_successes"]], ["sam"])

    def test_one_account_repeated_failure_not_spray(self):
        self.assertNotIn("203.0.113.80", self.by_ip)

    def test_success_too_late_not_correlated(self):
        f = self.by_ip["192.0.2.70"]
        self.assertFalse(f["follow_up_needed"])

    def test_unrelated_account_same_ip_not_correlated(self):
        f = self.by_ip["203.0.113.75"]
        self.assertFalse(f["follow_up_needed"])

    def test_sliding_window_catches_clock_bin_boundary(self):
        f = self.by_ip["192.0.2.90"]
        self.assertEqual(f["window_start"], "2026-11-22T10:58:00+00:00")
        self.assertEqual(f["last_failure"], "2026-11-22T11:02:00+00:00")
        self.assertTrue(f["follow_up_needed"])

    def test_unknown_source_and_local_logons_excluded(self):
        self.assertNotIn("-", self.by_ip)
        self.assertNotIn("198.51.100.66", self.by_ip)

    def test_timezone_required(self):
        with self.assertRaises(ValueError):
            timestamp("2026-11-22T10:00:00")
        self.assertEqual(str(timestamp("2026-11-22T10:00:00Z").tzinfo), "UTC")

    def test_duplicate_suppression_for_single_window(self):
        self.assertEqual(sum(f["source_ip"] == "198.51.100.25" for f in self.report["findings"]), 1)


if __name__ == "__main__":
    unittest.main()
