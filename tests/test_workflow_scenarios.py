import unittest

from tools.reconcile_reviews import reconcile
from tools.route_task import route


class RepresentativeWorkflowTests(unittest.TestCase):
    def test_small_bug_fix(self) -> None:
        result = route("Fix a crash when an optional value is absent", "small", False)
        self.assertEqual(result["reviewMode"], "fast")
        self.assertIn("targeted-verification", result["workflow"])

    def test_moderately_complex_feature(self) -> None:
        result = route("Add an API for resumable uploads", "medium", False)
        self.assertIn("requirements-clarification", result["workflow"])
        self.assertIn("type-interface", result["specializedReviews"])

    def test_design_decision(self) -> None:
        result = route("Choose architecture for a durable job scheduler", "large", True)
        self.assertEqual(
            result["workflow"],
            ["software-design", "design-review-comprehensive"],
        )

    def test_work_item_decomposition(self) -> None:
        result = route("Refine this backlog item and its acceptance criteria", "medium", False)
        self.assertEqual(result["workflow"], ["work-item-planning"])

    def test_standard_pr_review(self) -> None:
        result = route("Review this normal pull request", "medium", False)
        self.assertEqual(result["reviewMode"], "fast")

    def test_pr_follow_through_is_separate_from_review(self) -> None:
        result = route("Address review comments and failing CI on this PR", "medium", False)
        self.assertEqual(result["workflow"][0], "pr-follow-through")
        self.assertNotIn("merge", result["workflow"])

    def test_comprehensive_multi_model_review_reconciliation(self) -> None:
        routed = route("Review a production authentication migration", "large", True)
        self.assertTrue(routed["independentModels"])
        reports = [
            {
                "reviewer": "fixture-local",
                "findings": [
                    {
                        "fingerprint": "auth-bypass",
                        "severity": "high",
                        "title": "Missing authorization check",
                        "location": "fixture.py:12",
                        "impact": "Unauthorized access.",
                        "evidence": "Protected branch returns before the authorization call.",
                        "verified": True,
                        "verification": "Inspected fixture.py:8-14.",
                    }
                ],
            },
            {
                "reviewer": "fixture-hosted",
                "findings": [
                    {
                        "fingerprint": "auth-bypass",
                        "severity": "high",
                        "title": "Authorization can be bypassed",
                        "location": "fixture.py:12",
                        "impact": "Unauthorized access.",
                        "evidence": "The early return precedes authorize(user).",
                        "verified": True,
                        "verification": "Inspected fixture.py:8-14.",
                    }
                ],
            },
        ]
        result = reconcile(reports)
        self.assertEqual(len(result["confirmedFindings"]), 1)
        self.assertEqual(len(result["confirmedFindings"][0]["independentReviewers"]), 2)


if __name__ == "__main__":
    unittest.main()
