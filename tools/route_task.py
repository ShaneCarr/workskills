#!/usr/bin/env python3
"""Recommend a proportionate engineering workflow for a task."""

from __future__ import annotations

import argparse
import json
import re


REVIEW_SIGNALS = {
    "security": ("security", "auth", "permission", "secret", "credential", "injection"),
    "performance-concurrency": (
        "performance",
        "latency",
        "throughput",
        "concurrency",
        "thread",
        "lock",
        "race",
    ),
    "test-quality": ("test infrastructure", "test framework", "fixture", "coverage"),
    "type-interface": ("api", "interface", "schema", "contract", "type"),
}


def route(text: str, size: str, production_impact: bool) -> dict:
    normalized = text.lower()
    reviews = ["correctness"]
    for review, signals in REVIEW_SIGNALS.items():
        if any(signal in normalized for signal in signals):
            reviews.append(review)

    is_work_item = bool(re.search(r"\b(ticket|work item|backlog|triage|acceptance criteria)\b", normalized))
    is_design = bool(re.search(r"\b(architecture|design|domain model|module boundary|trade-?off)\b", normalized))
    is_bug = bool(re.search(r"\b(bug|fix|regression|failure|crash)\b", normalized))
    is_pr_follow_through = bool(
        re.search(r"\b(review feedback|review comment|merge conflict|resolve conflict|failing ci)\b", normalized)
    )
    high_stakes = production_impact or size == "large" or "migration" in normalized

    if is_pr_follow_through:
        workflow = ["pr-follow-through", "targeted-verification", "focused-re-review"]
    elif is_work_item:
        workflow = ["work-item-planning"]
    elif is_design and high_stakes:
        workflow = ["software-design", "design-review-comprehensive"]
    elif is_design:
        workflow = ["software-design", "design-review-lightweight"]
    elif is_bug and size == "small" and not high_stakes:
        workflow = ["systematic-debugging", "targeted-verification", "code-review-fast"]
    else:
        workflow = ["requirements-clarification", "software-design-if-needed", "implementation"]
        workflow.append("review-suite" if high_stakes else "code-review-fast")
        workflow.append("verification-before-completion")

    if high_stakes:
        reviews.extend(["spec-compliance", "silent-failures", "test-quality", "simplification"])

    return {
        "workflow": workflow,
        "reviewMode": "comprehensive" if high_stakes else "fast",
        "specializedReviews": list(dict.fromkeys(reviews)),
        "independentModels": high_stakes,
        "externalCodeSharing": "requires explicit authorization",
        "reason": "High-impact or large change." if high_stakes else "Proportionate default for the stated task.",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("task")
    parser.add_argument("--size", choices=("small", "medium", "large"), default="medium")
    parser.add_argument("--production-impact", action="store_true")
    args = parser.parse_args()
    print(json.dumps(route(args.task, args.size, args.production_impact), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
