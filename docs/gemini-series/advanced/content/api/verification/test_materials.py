"""Real SDK on loopback plus synthetic data/error tests; never a cloud benchmark."""
import copy
import importlib.util
import json
import platform
import sys
import tempfile
import threading
import unittest
from contextlib import contextmanager
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

HERE = Path(__file__).resolve().parent
EX = HERE.parent/"examples"
sys.path.insert(0, str(EX))
from lablib import batch, cache_lab, citations, file_store, function_loop
from lablib.common import client_for, digest, https_url, read_json, write_json


@contextmanager
def server(responses):
    records = []

    class Handler(BaseHTTPRequestHandler):
        def respond(self):
            length = int(self.headers.get("Content-Length", "0"))
            raw = self.rfile.read(length)
            records.append({"method": self.command, "path": self.path, "body": json.loads(raw) if raw else None})
            code, data = responses[min(len(records)-1, len(responses)-1)]
            encoded = json.dumps(data).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(encoded)))
            self.end_headers()
            self.wfile.write(encoded)

        do_POST = respond
        do_GET = respond
        do_DELETE = respond

        def log_message(self, *_):
            pass

    http = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=http.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{http.server_port}", records
    finally:
        http.shutdown()
        http.server_close()
        thread.join()


def interaction(steps, status="completed"):
    return {"id": "fixture-i", "status": status, "object": "interaction", "model": "gemini-3.8-flash", "created": "2026-09-14T00:00:00Z", "steps": steps}


def call(identity="call-1", name="lookup_order", args=None):
    return {"type": "function_call", "id": identity, "name": name, "arguments": args or {"order_id": "DEMO-001"}}


class Materials(unittest.TestCase):
    def test_order_allowed_unknown_invalid(self):
        orders = read_json(EX/"81/orders.json")
        self.assertTrue(function_loop.lookup("lookup_order", {"order_id": "DEMO-001"}, orders)["found"])
        self.assertFalse(function_loop.lookup("lookup_order", {"order_id": "DEMO-999"}, orders)["found"])
        self.assertEqual(function_loop.lookup("delete_order", {}, orders)["error"], "tool_not_allowed")
        self.assertEqual(function_loop.lookup("lookup_order", {"order_id": "../secret"}, orders)["error"], "invalid_order_id")
        self.assertEqual(function_loop.lookup("lookup_order", {"order_id": "DEMO-001", "delete": True}, orders)["error"], "invalid_arguments")

    def test_real_sdk_function_result_and_history(self):
        thought = {"type": "thought", "signature": "fixture-signature", "summary": [{"type": "text", "text": "synthetic"}]}
        end = {"type": "model_output", "content": [{"type": "text", "text": "兩件，包裝中。"}]}
        with server([(200, interaction([thought, call()], "requires_action")), (200, interaction([end]))]) as (url, records), client_for("interactions", test_url=url) as client:
            result = function_loop.run(client.interactions.create, "查 DEMO-001", read_json(EX/"81/orders.json"), "gemini-3.8-flash")
        self.assertEqual(result["status"], "answered")
        self.assertEqual(len(records), 2)
        history = records[1]["body"]["input"]
        self.assertEqual(history[1]["signature"], "fixture-signature")
        self.assertEqual(history[-1]["call_id"], "call-1")
        self.assertTrue(json.loads(history[-1]["result"][0]["text"])["found"])
        self.assertFalse(records[1]["body"]["store"])
        self.assertEqual(records[1]["body"]["tools"], [function_loop.TOOL])

    def test_loop_limit_no_final_tool_execution(self):
        seen = []
        def repeat(**request):
            seen.append(copy.deepcopy(request))
            return interaction([call(f"c-{len(seen)}")], "requires_action")
        result = function_loop.run(repeat, "查訂單", {}, "fixture", max_requests=2)
        self.assertEqual(result["status"], "request_limit")
        self.assertEqual(result["trace"][-1]["tool_results"], [])
        self.assertEqual(len(seen), 2)

    def test_duplicate_call_ids_stop(self):
        reply = interaction([call(), call()], "requires_action")
        self.assertEqual(function_loop.run(lambda **_: reply, "查訂單", {}, "fixture")["status"], "invalid_call_ids_or_count")

    def test_deadline_and_blank_question(self):
        times = iter([0, 46])
        self.assertEqual(function_loop.run(lambda **_: self.fail("network call"), "查訂單", {}, "fixture", clock=lambda: next(times))["status"], "deadline")
        with self.assertRaises(ValueError):
            function_loop.run(None, "", {}, "fixture")

    def test_real_sdk_both_families_do_not_retry_503(self):
        for family in ["interactions", "generateContent"]:
            with self.subTest(family=family), server([(503, {"error": {"code": 503, "status": "UNAVAILABLE", "message": "fixture"}})]) as (url, records):
                with client_for(family, test_url=url) as client:
                    from google.genai.errors import APIError
                    with self.assertRaises((APIError, ValueError)):
                        if family == "interactions":
                            client.interactions.create(model="gemini-3.8-flash", input="fixture", store=False)
                        else:
                            client.models.generate_content(model="gemini-3.8-flash", contents="fixture")
                self.assertEqual(len(records), 1, records)

    def test_utf8_citation_and_split_rejected(self):
        fixture = read_json(EX/"82/response-fixtures/cited.json")
        self.assertEqual(citations.extract_urls(fixture)[0]["citations"][0]["segment"], fixture["steps"][-1]["content"][0]["text"])
        bad = read_json(EX/"82/response-fixtures/wrong-byte-offset.json")
        self.assertEqual(citations.extract_urls(bad)[0]["rejected"], ["citation_splits_utf8_character"])
        self.assertEqual(citations.byte_segment("甲😀乙", 3, 7), "😀")

    def test_unsafe_urls_no_link(self):
        for value in ["javascript:alert(1)", "http://example.com", "https://u:p@example.com", "https://example.com/\nx", "https://example.com\\x"]:
            with self.subTest(value=value), self.assertRaises(ValueError):
                https_url(value)

    def test_grounding_missing_widget_stops_live_display(self):
        with self.assertRaisesRegex(ValueError, "incomplete"):
            citations.search_html(read_json(EX/"82/response-fixtures/no-search.json"))

    def test_widget_scripts_rejected_and_text_escaped(self):
        fixture = read_json(EX/"82/response-fixtures/cited.json")
        fixture["steps"][1]["result"][0]["search_suggestions"] = '<script>alert(1)</script>'
        with self.assertRaisesRegex(ValueError, "widget"):
            citations.search_html(fixture, fixture=True)
        safe = interaction([{"type": "model_output", "content": [{"type": "text", "text": "<script>fake</script>"}]}])
        self.assertIn("&lt;script&gt;fake", citations.search_html(safe, fixture=True))

    def test_file_citation_version_quote_and_missing(self):
        docs = read_json(EX/"83/documents.json")
        text = {"type": "model_output", "content": [{"type": "text", "text": "260 毫升", "annotations": [{"type": "file_citation", "file_name": "S003-v1.txt", "source": "容量：260 毫升"}]}]}
        self.assertEqual(citations.file_answer(interaction([text]), docs)["citations"][0]["document_id"], "S003")
        docs[2]["status"] = "superseded"
        self.assertEqual(citations.file_answer(interaction([text]), docs)["status"], "no_verified_evidence")

    def test_fake_quote_and_duplicate_names_rejected(self):
        docs = read_json(EX/"83/documents.json")
        block = {"type": "model_output", "content": [{"type": "text", "text": "假的", "annotations": [{"type": "file_citation", "file_name": "S003-v1.txt", "source": "容量：999 毫升"}]}]}
        self.assertEqual(citations.file_answer(interaction([block]), docs)["citations"], [])
        block["content"][0]["annotations"][0]["source"] = "容量：260 毫升"
        docs.append(docs[2])
        self.assertEqual(citations.file_answer(interaction([block]), docs)["citations"], [])

    def test_store_creation_uncertainty_prevents_resubmit(self):
        def failed(**_):
            raise TimeoutError("fixture")
        client = SimpleNamespace(file_search_stores=SimpleNamespace(create=failed))
        with tempfile.TemporaryDirectory() as folder:
            ledger = Path(folder)/"ledger.json"
            with self.assertRaises(TimeoutError):
                file_store.create_store(client, ledger)
            self.assertEqual(read_json(ledger)["state"], "create_uncertain")
            with self.assertRaisesRegex(ValueError, "exists"):
                file_store.create_store(client, ledger)

    def test_real_sdk_store_import_and_document_delete(self):
        responses = [(200, {"name": "fileSearchStores/demo", "displayName": "fixture"}), (200, {"name": "operations/import-demo", "done": True, "response": {"parent": "fileSearchStores/demo", "documentName": "fileSearchStores/demo/documents/doc1"}}), (200, {})]
        with server(responses) as (url, records), client_for("generateContent", test_url=url) as client:
            store = client.file_search_stores.create(config={"display_name": "fixture", "embedding_model": "models/gemini-embedding-2"})
            operation = client.file_search_stores.import_file(file_search_store_name=store.name, file_name="files/test1")
            client.file_search_stores.documents.delete(name=operation.response.document_name, config={"force": True})
        self.assertTrue(operation.done)
        self.assertEqual(records[1]["body"]["fileName"], "files/test1")
        self.assertEqual(records[2]["method"], "DELETE")

    def test_poll_completion_is_not_citation_verification(self):
        with tempfile.TemporaryDirectory() as folder:
            ledger = Path(folder)/"ledger.json"
            write_json(ledger, {"owner": "gemini-api-lab", "state": "ready", "store": "fileSearchStores/demo", "documents": [{"id": "S001", "version": "v1", "status": "pending", "operation": {"name": "operations/demo", "done": True, "response": {"document_name": "fileSearchStores/demo/documents/doc1"}}}]})
            result = file_store.poll_document(None, ledger, "S001", "v1")
            self.assertEqual(result["status"], "indexed_pending_review")

    def test_pending_index_blocks_query(self):
        with tempfile.TemporaryDirectory() as folder:
            ledger = Path(folder)/"ledger.json"
            write_json(ledger, {"owner": "gemini-api-lab", "state": "ready", "store": "fileSearchStores/demo", "documents": [{"status": "pending"}]})
            with self.assertRaisesRegex(ValueError, "unresolved"):
                file_store.query_store(None, ledger, "查詢", "fixture")

    def test_foreign_document_delete_blocked(self):
        with tempfile.TemporaryDirectory() as folder:
            ledger = Path(folder)/"ledger.json"
            write_json(ledger, {"owner": "gemini-api-lab", "state": "ready", "store": "fileSearchStores/demo", "documents": [{"id": "S001", "version": "v1", "document": "fileSearchStores/other/documents/doc1"}]})
            with self.assertRaisesRegex(ValueError, "outside"):
                file_store.delete_document(None, ledger, "S001", "v1")

    def test_cache_unknown_is_not_zero_or_hit(self):
        self.assertIsNone(cache_lab.usage({}, "interactions")["cache_hit_observed"])
        self.assertFalse(cache_lab.usage({"usage": {"total_input_tokens": 100, "total_cached_tokens": 0}}, "interactions")["cache_hit_observed"])
        with self.assertRaisesRegex(ValueError, "exceeds"):
            cache_lab.usage({"usage": {"total_input_tokens": 10, "total_cached_tokens": 20}}, "interactions")

    def test_real_sdk_explicit_cache_family(self):
        replies = [(200, {"name": "cachedContents/demo", "model": "models/gemini-3.8-flash"}), (200, {"candidates": [{"content": {"parts": [{"text": "fixture"}]}}], "usageMetadata": {"promptTokenCount": 5000, "cachedContentTokenCount": 4500, "candidatesTokenCount": 5}}), (200, {})]
        with tempfile.TemporaryDirectory() as folder, server(replies) as (url, records):
            ledger = Path(folder)/"cache.json"
            with client_for("generateContent", test_url=url) as client:
                cache_lab.explicit_create(client, EX/"84/cache-lab/document.txt", "gemini-3.8-flash", ledger)
                observed = cache_lab.explicit_query(client, ledger, "前三個識別碼？")
                cache_lab.explicit_delete(client, ledger)
        self.assertEqual(observed["cached"], 4500)
        self.assertIn("generateContent", records[1]["path"])
        self.assertEqual(records[1]["body"]["cachedContent"], "cachedContents/demo")
        self.assertEqual(records[0]["body"]["ttl"], "300s")
        self.assertEqual(records[2]["method"], "DELETE")

    def test_cache_cli_retains_partial_observations_after_failure(self):
        spec = importlib.util.spec_from_file_location("cache_cli", EX/"84/cache-lab/main.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        count = 0
        def respond(**_):
            nonlocal count
            count += 1
            if count == 2:
                raise ValueError("synthetic_second_request_failure")
            return {"usage": {"total_input_tokens": 5000, "total_cached_tokens": 0}}
        @contextmanager
        def local_client(_):
            yield SimpleNamespace(interactions=SimpleNamespace(create=respond))
        with tempfile.TemporaryDirectory() as folder:
            output = Path(folder)/"partial.json"
            with patch.object(module, "client_for", local_client), patch.object(sys, "argv", ["main.py", "implicit", "--live", "--output", str(output)]), self.assertRaises(SystemExit):
                module.main()
            result = read_json(output)
            self.assertEqual(result["status"], "request_failed")
            self.assertEqual(len(result["rows"]), 1)
            self.assertEqual(result["rows"][0]["usage"]["cached"], 0)
            self.assertEqual(count, 2)

    def test_batch_reconcile_only_transient_retry(self):
        cases = batch.jsonl(EX/"85/cases.jsonl")
        result = batch.reconcile(cases, batch.jsonl(EX/"85/response-fixtures/partial.jsonl"))
        self.assertEqual(len(result["accepted"]), 16)
        self.assertEqual(result["retryable"], ["B17"])
        self.assertEqual(result["missing"], ["B19"])
        self.assertEqual(len(result["failed"]), 2)
        self.assertEqual([c["key"] for c in batch.retry_cases(cases, result)], ["B17"])

    def test_batch_unknown_duplicate_and_budget(self):
        cases = batch.jsonl(EX/"85/cases.jsonl")
        results = batch.jsonl(EX/"85/response-fixtures/partial.jsonl")
        with self.assertRaises(ValueError):
            batch.reconcile(cases, results+[results[0]])
        with self.assertRaises(ValueError):
            batch.reconcile(cases, [{"key": "UNKNOWN"}])
        with self.assertRaisesRegex(ValueError, "budget"):
            batch.retry_cases(cases, batch.reconcile(cases, results), attempts=3)

    def test_real_sdk_batch_create_fetch_download_pointer(self):
        replies = [(200, {"name": "batches/demo", "metadata": {"state": "BATCH_STATE_PENDING"}}), (200, {"name": "batches/demo", "metadata": {"state": "BATCH_STATE_SUCCEEDED", "output": {"responsesFile": "files/results1"}}})]
        with server(replies) as (url, records), client_for("generateContent", test_url=url) as client:
            job = client.batches.create(model="gemini-3.8-flash", src="files/cases1", config={"display_name": "fixture"})
            got = client.batches.get(name=job.name)
        self.assertEqual(job.name, "batches/demo")
        self.assertEqual(got.dest.file_name, "files/results1")
        self.assertIn("batchGenerateContent", records[0]["path"])

    def test_retry_parent_hash_keys_model_and_budget(self):
        cases_path = EX/"85/cases.jsonl"
        output_path = EX/"85/response-fixtures/partial.jsonl"
        retry = batch.retry_cases(batch.jsonl(cases_path), batch.reconcile(batch.jsonl(cases_path), batch.jsonl(output_path)))
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            parent = {"owner": "gemini-batch-lab", "remote_state": "JOB_STATE_SUCCEEDED", "attempt": 1, "model": "fixture", "input_path": str(cases_path), "input_sha256": digest(cases_path), "output_path": str(output_path), "output_sha256": digest(output_path)}
            write_json(root/"parent.json", parent)
            (root/"retry.jsonl").write_text(json.dumps(retry[0]), encoding="utf-8")
            client = SimpleNamespace(files=SimpleNamespace(upload=lambda **_: SimpleNamespace(name="files/retry1")), batches=SimpleNamespace(create=lambda **_: SimpleNamespace(name="batches/retry1")))
            result = batch.submit(client, root/"retry.jsonl", root/"child.json", "fixture", parent_ledger=root/"parent.json")
            self.assertEqual(result["attempt"], 2)
            self.assertEqual(result["keys"], ["B17"])
            with self.assertRaisesRegex(ValueError, "match"):
                batch.submit(None, root/"retry.jsonl", root/"wrong.json", "wrong-model", parent_ledger=root/"parent.json")
            parent["attempt"] = 3
            write_json(root/"parent.json", parent)
            with self.assertRaisesRegex(ValueError, "budget"):
                batch.submit(None, root/"retry.jsonl", root/"fourth.json", "fixture", parent_ledger=root/"parent.json")
            parent["input_sha256"] = "changed"
            write_json(root/"parent.json", parent)
            with self.assertRaisesRegex(ValueError, "files_changed"):
                batch.submit(None, root/"retry.jsonl", root/"changed.json", "fixture", parent_ledger=root/"parent.json")

    def test_merge_one_adoption_per_case(self):
        cases = batch.jsonl(EX/"85/cases.jsonl")
        first = batch.reconcile(cases, batch.jsonl(EX/"85/response-fixtures/partial.jsonl"))
        second = {"accepted": {"B17": {"text": "author retry fixture"}}}
        merged = batch.merge_accepted(cases, [first, second])
        self.assertEqual(len(merged["accepted"]), 17)
        self.assertEqual(merged["unresolved"], ["B18", "B19", "B20"])
        with self.assertRaisesRegex(ValueError, "adopted"):
            batch.merge_accepted(cases, [first, first])

    def test_overlapping_index_versions_block_query(self):
        with tempfile.TemporaryDirectory() as folder:
            ledger = Path(folder)/"ledger.json"
            write_json(ledger, {"owner": "gemini-api-lab", "state": "ready", "store": "fileSearchStores/demo", "documents": [{"id": "S003", "version": v, "status": "indexed_pending_review"} for v in ["v1", "v2"]]})
            with self.assertRaisesRegex(ValueError, "one_current"):
                file_store.query_store(None, ledger, "容量？", "fixture")

    def test_batch_cleanup_resumes_only_owned_terminal_job(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder)/"ledger.json"
            ledger = {"owner": "gemini-batch-lab", "remote_state": "JOB_STATE_RUNNING", "job": "batches/demo", "input_file": "files/input1", "output_file": "files/output1"}
            write_json(path, ledger)
            with self.assertRaisesRegex(ValueError, "terminal"):
                batch.cleanup(None, path)
            seen = []
            api = SimpleNamespace(delete=lambda **args: seen.append(args["name"]))
            client = SimpleNamespace(batches=api, files=api)
            ledger["remote_state"] = "JOB_STATE_SUCCEEDED"
            write_json(path, ledger)
            batch.cleanup(client, path)
            batch.cleanup(client, path)
            self.assertEqual(seen, ["batches/demo", "files/input1", "files/output1"])

    def test_service_provider_error_masking_and_source_navigation(self):
        from fastapi.testclient import TestClient
        spec = importlib.util.spec_from_file_location("document_app_errors", EX/"86/document-service/app.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        def failing(_):
            raise RuntimeError("secret-test-marker-do-not-display")
        with TestClient(module.create_app(live=True, provider=failing), base_url="http://127.0.0.1") as client:
            reply = client.post("/ask", json={"question": "S003 的容量是多少？"})
            self.assertEqual(reply.status_code, 502)
            self.assertNotIn("secret-test-marker", reply.text)
            source = client.get("/sources/S003")
            self.assertIn("260 毫升", source.text)
            self.assertIn("text/plain", source.headers["content-type"])
            self.assertEqual(client.get("/sources/S099").status_code, 404)

    def test_local_service_twenty_golden_cases_and_key_absence(self):
        from fastapi.testclient import TestClient
        spec = importlib.util.spec_from_file_location("document_app", EX/"86/document-service/app.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        with TestClient(module.create_app(), base_url="http://127.0.0.1") as client:
            for case in read_json(EX/"86/golden-cases.json"):
                result = client.post("/ask", json={"question": case["question"]})
                if case["expected_status"] == "invalid_input":
                    self.assertEqual(result.status_code, 422)
                else:
                    self.assertEqual(result.status_code, 200)
                    body = result.json()
                    self.assertEqual(body["status"], case["expected_status"], case["key"])
                    self.assertEqual(body["mode"], "author_fixture")
                    if case["expected_text"]:
                        self.assertIn(case["expected_text"], body["answer"])
            self.assertNotIn("GEMINI_API_KEY", client.get("/").text)
            self.assertNotIn("GEMINI_API_KEY", client.get("/app.js").text)
            self.assertEqual(client.post("/ask", headers={"Origin": "https://attacker.example"}, json={"question": "S001 的容量是多少？"}).status_code, 403)
            self.assertEqual(client.get("/health", headers={"Host": "attacker.example"}).status_code, 403)
            self.assertEqual(client.post("/ask", content=b"x"*17000, headers={"Content-Type": "application/json"}).status_code, 413)
            self.assertEqual(client.post("/ask", json={"question": "S001", "key": "extra"}).status_code, 422)
            self.assertEqual(client.get("/orders/DEMO-001").json()["order"]["quantity"], 2)
            self.assertEqual(client.get("/orders/DEMO-999").json()["found"], False)


if __name__ == "__main__":
    result = unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(Materials))
    write_json(HERE/"fixtures.json", {"checkedOn": "2026-09-14", "python": platform.python_version(), "tests": result.testsRun, "success": result.wasSuccessful(), "failures": len(result.failures), "errors": len(result.errors), "modelCalls": 0, "realSdkTransport": "loopback HTTP only", "serviceGoldenCases": 20})
    raise SystemExit(not result.wasSuccessful())
