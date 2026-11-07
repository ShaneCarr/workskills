import unittest

from tools.route_task import route


class RouteTaskTests(unittest.TestCase):
    def test_small_bug_uses_fast_path(self) -> None:
        result = route("Fix a null dereference regression", "small", False)
        self.assertEqual(result["reviewMode"], "fast")
        self.assertEqual(
            result["workflow"],
            ["systematic-debugging", "targeted-verification", "code-review-fast"],
        )

    def test_large_security_change_uses_comprehensive_review(self) -> None:
        result = route("Change authentication and permission checks", "large", True)
        self.assertEqual(result["reviewMode"], "comprehensive")
        self.assertTrue(result["independentModels"])
        self.assertIn("security", result["specializedReviews"])
        self.assertIn("silent-failures", result["specializedReviews"])

    def test_work_item_refinement_routes_to_planning(self) -> None:
        result = route("Turn this discussion into a concise work item", "medium", False)
        self.assertEqual(result["workflow"], ["work-item-planning"])

    def test_pr_conflict_routes_to_follow_through_without_merge(self) -> None:
        result = route("Resolve the merge conflict and address review feedback", "medium", False)
        self.assertEqual(
            result["workflow"],
            ["pr-follow-through", "targeted-verification", "focused-re-review"],
        )


if __name__ == "__main__":
    unittest.main()
