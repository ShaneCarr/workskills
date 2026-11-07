from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ADAPTER = ROOT / "adapters" / "ollama_review.py"


class Handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        assert self.path == "/api/tags"
        body = json.dumps({"models": [{"name": "fixture-qwen"}]}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self) -> None:
        assert self.path == "/api/generate"
        length = int(self.headers["Content-Length"])
        payload = json.loads(self.rfile.read(length))
        assert payload["model"] == "fixture-qwen"
        body = json.dumps({"response": "No actionable defects found."}).encode()
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *_: object) -> None:
        return


class OllamaAdapterTests(unittest.TestCase):
    def test_ollama_http_adapter_against_fixture_server(self) -> None:
        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever)
        thread.start()
        try:
            host = f"http://127.0.0.1:{server.server_port}"
            listed = subprocess.run(
                [sys.executable, str(ADAPTER), "--host", host, "--list-models"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(listed.returncode, 0)
            self.assertEqual(listed.stdout.strip(), "fixture-qwen")

            with tempfile.TemporaryDirectory() as directory:
                source = Path(directory) / "public-fixture.py"
                source.write_text("print('fixture')\n", encoding="utf-8")
                reviewed = subprocess.run(
                    [
                        sys.executable,
                        str(ADAPTER),
                        "--host",
                        host,
                        "--model",
                        "fixture-qwen",
                        "--input",
                        str(source),
                    ],
                    check=False,
                    capture_output=True,
                    text=True,
                )
                self.assertEqual(reviewed.returncode, 0)
                self.assertIn("No actionable defects", reviewed.stdout)
        finally:
            server.shutdown()
            thread.join()
            server.server_close()


if __name__ == "__main__":
    unittest.main()
