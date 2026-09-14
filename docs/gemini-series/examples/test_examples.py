"""Offline validation; the real SDK talks only to a local HTTP fixture."""
import json
import threading
import unittest
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from decimal import Decimal
from types import SimpleNamespace
from unittest.mock import patch

from google import genai
from pydantic import ValidationError
from document_assistant import Extraction, extract, verify
from estimate_cost import estimate

SOURCE = "青葉讀書會在社區中心舉辦。"
DATA = {
    "summary": SOURCE,
    "facts": [
        {"field": "title", "value": "青葉讀書會", "quote": SOURCE},
        {"field": "date", "value": None, "quote": None},
        {"field": "venue", "value": "社區中心", "quote": SOURCE},
        {"field": "fee", "value": None, "quote": None},
        {"field": "registration", "value": None, "quote": None},
    ],
    "questions": ["日期與報名方式為何？"],
}


class ExamplesTest(unittest.TestCase):
    def test_price_units(self):
        self.assertEqual(estimate(2000, 500, "0.75", "3.75"), Decimal("0.003375"))
        with self.assertRaises(ValueError):
            estimate(-1, 0, "0.75", "3.75")

    def test_valid_and_invalid_evidence(self):
        result = Extraction.model_validate(DATA)
        verify(result, SOURCE)
        result.facts[0].quote = "不存在的公告"
        with self.assertRaises(ValueError):
            verify(result, SOURCE)
        result = Extraction.model_validate(DATA)
        result.facts[-1].field = "title"
        with self.assertRaises(ValueError):
            verify(result, SOURCE)

    def test_schema_and_empty_response(self):
        with self.assertRaises(ValidationError):
            Extraction.model_validate({"summary": "", "facts": [], "questions": []})
        client = SimpleNamespace(interactions=SimpleNamespace(create=lambda **_: SimpleNamespace(status="failed", output_text=None)))
        with self.assertRaises(RuntimeError):
            extract(client, SOURCE, "gemini-3.8-flash")

    def test_real_sdk_local_http_roundtrip(self):
        received = []

        class Handler(BaseHTTPRequestHandler):
            def do_POST(self):
                received.append((self.path, json.loads(self.rfile.read(int(self.headers["Content-Length"])))) )
                body = {
                    "id": "fixture-interaction", "status": "completed", "object": "interaction",
                    "model": "gemini-3.8-flash", "created": "2026-09-14T00:00:00Z",
                    "steps": [{"type": "model_output", "content": [{"type": "text", "text": json.dumps(DATA, ensure_ascii=False)}]}],
                }
                encoded = json.dumps(body).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(encoded)))
                self.end_headers()
                self.wfile.write(encoded)

            def log_message(self, *args):
                pass

        server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with genai.Client(api_key="fixture-not-a-real-key", http_options={"base_url": f"http://127.0.0.1:{server.server_port}", "timeout": 5000}) as client:
                result, identity = extract(client, SOURCE, "gemini-3.8-flash")
            self.assertEqual(identity, "fixture-interaction")
            self.assertEqual(result.summary, SOURCE)
            self.assertEqual(len(received), 1)
            route, body = received[0]
            self.assertIn("interactions", route)
            self.assertEqual(body["model"], "gemini-3.8-flash")
            self.assertFalse(body["store"])
            self.assertEqual(body["response_format"]["mime_type"], "application/json")
            self.assertIn(SOURCE, body["input"])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=2)


if __name__ == "__main__":
    unittest.main()
