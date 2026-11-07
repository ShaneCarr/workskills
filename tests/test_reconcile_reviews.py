import unittest

from tools.reconcile_reviews import reconcile


class ReconcileReviewTests(unittest.TestCase):
    def test_reconcile_deduplicates_and_rejects_speculation(self) -> None:
        reports = [
            {
                "reviewer": "local-qwen",
                "findings": [
                    {
                        "fingerprint": "missing-timeout",
                        "severity": "high",
                        "title": "Outbound request has no timeout",
                        "location": "client.py:18",
                        "impact": "A stalled peer can exhaust workers.",
                        "evidence": "urlopen is called without a timeout.",
                        "verified": True,
                        "verification": "Inspected client.py:18 at the frozen revision.",
                        "minimalCorrection": "Pass a bounded timeout.",
                    },
                    {
                        "severity": "medium",
                        "title": "Maybe slow",
                        "location": "client.py:1",
                        "evidence": "No measurement.",
                        "verified": False,
                        "speculative": True,
                    },
                    {
                        "severity": "low",
                        "title": "Plausible but unchecked",
                        "location": "client.py:30",
                        "evidence": "A fallback exists.",
                    },
                ],
            },
            {
                "reviewer": "hosted-reviewer",
                "findings": [
                    {
                        "fingerprint": "missing-timeout",
                        "severity": "medium",
                        "title": "Request can hang",
                        "location": "client.py:18",
                        "impact": "Request never returns.",
                        "evidence": "The only urlopen call omits timeout.",
                        "verified": True,
                        "verification": "Inspected client.py:18 at the frozen revision.",
                        "minimalCorrection": "Set a timeout and handle timeout errors.",
                    }
                ],
            },
        ]

        result = reconcile(reports)
        self.assertEqual(len(result["confirmedFindings"]), 1)
        self.assertEqual(result["confirmedFindings"][0]["severity"], "high")
        self.assertEqual(
            result["confirmedFindings"][0]["independentReviewers"],
            ["hosted-reviewer", "local-qwen"],
        )
        self.assertEqual(len(result["rejectedFindings"]), 2)
        self.assertEqual(
            {finding["reason"] for finding in result["rejectedFindings"]},
            {"insufficient-evidence", "not-code-verified"},
        )


if __name__ == "__main__":
    unittest.main()
