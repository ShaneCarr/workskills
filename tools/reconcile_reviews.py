#!/usr/bin/env python3
"""Reconcile independent review reports into evidence-backed findings."""

from __future__ import annotations

import argparse
import json
from collections import defaultdict
from pathlib import Path


SEVERITY = {"critical": 4, "high": 3, "medium": 2, "low": 1}


def reconcile(reports: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    rejected = []
    for report in reports:
        reviewer = report.get("reviewer", "unknown")
        for finding in report.get("findings", []):
            if finding.get("speculative") or not finding.get("evidence") or not finding.get("location"):
                rejected.append(
                    {"reviewer": reviewer, "finding": finding, "reason": "insufficient-evidence"}
                )
                continue
            if not finding.get("verified") or not finding.get("verification"):
                rejected.append(
                    {"reviewer": reviewer, "finding": finding, "reason": "not-code-verified"}
                )
                continue
            fingerprint = finding.get("fingerprint")
            if not fingerprint:
                fingerprint = f"{finding['location']}::{finding.get('title', '').strip().lower()}"
            grouped[fingerprint].append({**finding, "reviewer": reviewer})

    confirmed = []
    for fingerprint, findings in grouped.items():
        strongest = max(findings, key=lambda item: SEVERITY.get(item.get("severity", "low"), 0))
        confirmed.append(
            {
                "fingerprint": fingerprint,
                "severity": strongest.get("severity", "low"),
                "title": strongest.get("title", fingerprint),
                "location": strongest["location"],
                "impact": strongest.get("impact", ""),
                "evidence": strongest["evidence"],
                "verification": strongest["verification"],
                "minimalCorrection": strongest.get("minimalCorrection", ""),
                "independentReviewers": sorted({item["reviewer"] for item in findings}),
            }
        )
    confirmed.sort(key=lambda item: (-SEVERITY.get(item["severity"], 0), item["location"]))
    return {"confirmedFindings": confirmed, "rejectedFindings": rejected}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", type=Path, nargs="+")
    args = parser.parse_args()
    payloads = [json.loads(path.read_text(encoding="utf-8")) for path in args.reports]
    print(json.dumps(reconcile(payloads), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
