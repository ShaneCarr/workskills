---
name: review-type-interface
description: Review public types, schemas, APIs, and module interfaces for invalid states, compatibility, ownership, and clear contracts.
license: MIT
---

# Review types and interfaces

Inspect producers, consumers, serialization, validation, versioning, and failure semantics. Check
whether types encode required invariants, optionality reflects reality, names expose domain meaning,
and ownership or lifecycle is clear.

Find breaking changes, ambiguous unions or flags, invalid representable states, unsafe widening,
leaky implementation details, inconsistent null/error behavior, and contracts that callers cannot
use correctly.

Prefer small domain types and existing conventions over abstraction for its own sake. Cite a real
misuse path or compatibility effect for each finding.
