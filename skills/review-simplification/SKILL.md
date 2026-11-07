---
name: review-simplification
description: Challenge a change for unnecessary abstractions, configuration, indirection, duplication, and scope while preserving required behavior.
license: MIT
---

# Review for simplification

Start from required behavior and current repository patterns. Look for code or concepts that can be
removed, collapsed, or reused without weakening contracts, diagnostics, safety, or testability.

Challenge speculative extension points, one-use frameworks, parallel representations, excessive
configuration, wrappers without policy, duplicated logic, and changes outside the requested scope.

Propose a concrete smaller shape and explain what remains equivalent. Do not recommend clever
compression, hidden coupling, or removal of necessary error handling merely to reduce line count.
