#!/usr/bin/env python3
"""Run an authorized review prompt through an Ollama HTTP endpoint."""

from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path


DEFAULT_HOST = os.environ.get("OLLAMA_HOST", "http://127.0.0.1:11434")
SYSTEM_PROMPT = """You are an independent code reviewer. Report only actionable defects.
For each finding include severity, source location, triggering conditions, concrete impact,
evidence, uncertainty, and a minimal correction. It is acceptable to report no findings."""


def is_local_host(host: str) -> bool:
    parsed = urllib.parse.urlparse(host)
    return parsed.hostname in {"127.0.0.1", "localhost", "::1"}


def request_json(host: str, path: str, payload: dict | None = None, timeout: int = 120) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    request = urllib.request.Request(
        host.rstrip("/") + path,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST" if payload is not None else "GET",
    )
    with urllib.request.urlopen(request, timeout=timeout) as response:
        return json.load(response)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", default=DEFAULT_HOST)
    parser.add_argument("--allow-remote", action="store_true")
    parser.add_argument("--list-models", action="store_true")
    parser.add_argument("--model")
    parser.add_argument("--input", type=Path)
    parser.add_argument("--prompt", default=SYSTEM_PROMPT)
    parser.add_argument("--timeout", type=int, default=120)
    args = parser.parse_args()

    if not is_local_host(args.host) and not args.allow_remote:
        parser.error("Remote Ollama hosts require --allow-remote because input leaves this machine.")

    try:
        if args.list_models:
            response = request_json(args.host, "/api/tags", timeout=args.timeout)
            for model in response.get("models", []):
                print(model.get("name", ""))
            return 0
        if not args.model or not args.input:
            parser.error("--model and --input are required unless --list-models is used.")
        source = args.input.read_text(encoding="utf-8")
        response = request_json(
            args.host,
            "/api/generate",
            {
                "model": args.model,
                "system": args.prompt,
                "prompt": source,
                "stream": False,
            },
            timeout=args.timeout,
        )
        print(response.get("response", ""))
        return 0
    except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
        print(f"Ollama adapter unavailable: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
