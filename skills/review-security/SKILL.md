---
name: review-security
description: Review a change for exploitable authorization, injection, secret handling, data exposure, trust-boundary, and abuse-path vulnerabilities.
license: MIT
---

# Review security

Use the runtime's dedicated security-review capability when one exists. Establish assets, actors,
trust boundaries, entry points, privileges, and data sensitivity before searching for generic
patterns.

Trace authentication and authorization on every affected path, input validation at the receiving
boundary, encoding at the output boundary, secret lifecycle, tenant or ownership isolation,
cryptographic use, dependency risk, and denial-of-service or abuse potential.

Report only plausible vulnerabilities with a concrete attacker capability, triggering input or
state, vulnerable source path, impact, and minimal mitigation. Distinguish defense-in-depth from an
exploitable defect. Do not expose secrets or run destructive exploits.
