---
name: review-silent-failures
description: Find swallowed errors, success-shaped fallbacks, missing propagation, misleading status, and observability gaps in a code change.
license: MIT
---

# Review silent failure modes

Trace error creation, transformation, propagation, retries, fallbacks, cleanup, status reporting,
and user/operator visibility across changed call paths. Check asynchronous boundaries, callbacks,
background work, and partial success.

Look for broad catches, ignored return values, empty defaults, stale cached success, missing awaits,
logs without failure signaling, and metrics or API responses that claim success before durable
completion.

For each finding show the failing operation, how the error becomes invisible or misleading, the
observable consequence, and the smallest correction. Do not demand logging when reliable
propagation already exists, and do not call an intentional documented fallback a silent failure.
