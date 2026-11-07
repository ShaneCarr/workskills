---
name: work-item-planning
description: Turn an ambiguous engineering discussion into concise, appropriately sized work items with dependencies, acceptance criteria, risks, and controlled scope.
license: MIT
---

# Plan engineering work items

Identify the user outcome, current behavior, desired behavior, non-goals, constraints, evidence,
and unresolved decisions. Ask only questions that materially change implementation or acceptance.
Do not turn every conversation into a long specification.

Split work only at independently reviewable or deployable boundaries. Keep one coherent behavior
change together when splitting would create integration overhead. Record real prerequisites rather
than treating list order as dependency.

For each item provide:

- a short outcome-based title;
- two to five sentences of scope and context;
- observable acceptance criteria;
- dependencies and affected interfaces;
- material risks or open decisions; and
- explicit non-goals when they prevent scope creep.

Acceptance criteria must be testable and avoid prescribing implementation unless the constraint is
itself required. Identify missing ownership, data, migration, rollout, security, observability, or
compatibility work. Distinguish a blocker from a follow-up improvement.

For issue triage, classify impact and urgency from evidence, identify the smallest reproduction,
separate confirmed behavior from hypotheses, and recommend close, clarify, investigate, or plan.

When an Azure DevOps or GitHub integration is available, preview proposed mutations before writing.
Without an integration, emit provider-neutral Markdown or JSON that can be copied safely. Never
claim a work item was created unless the provider confirmed it.
