---
name: independent-multi-model-review
description: Coordinate an explicitly authorized review across different model or provider adapters, then verify and reconcile findings without using agreement as proof.
license: MIT
---

# Run an independent multi-model review

Use only when the user explicitly authorizes the target, providers, and any external code sharing.
Prefer synthetic or public fixtures for adapter smoke tests. Never infer that access to a provider
permits sending proprietary source.

Freeze one target and shared requirements brief. Select distinct available reviewers, for example a
local Ollama model and one or more approved hosted models. Use different review emphases rather than
cosmetically different prompts. Do not show first-pass findings to other reviewers.

Each reviewer must cite source evidence, triggering conditions, impact, uncertainty, and a
falsifiable check. The coordinator then deduplicates, verifies every material finding against code,
rejects speculation, records independent rediscovery, and assigns severity from actual impact.

If a requested adapter or model is unavailable, report it and continue only if the resulting mode
still matches the user's authorization. Never describe a mocked response, prompt rendering, or one
model called twice as a real multi-model review.

The included Ollama adapter is an execution adapter, not an agent:

`python adapters/ollama_review.py --model <installed-model> --input <fixture-or-authorized-file>`
