import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { sandbox } from "../core/fixtures/load.mjs";
import { canonicalJson, normalizeRun, runReceiptStore, sourceHash, validateRunReceipt } from "./run-receipts.mjs";

const site = "https://site.test";
const request = (slug = "video-one") => ({ stage: "writer", slug, instructions: "Write the checked story.", payload: { locale: "zh-TW", rows: [1, 2] } });
const context = (box) => ({ home: box.base, root: box.root, env: { VIDEO_WORKDIR: box.work } });
const result = { text: '{"scenes":[]}', provider: "gemini", model: "chosen-before-restart", input_tokens: 25, output_tokens: 12, usage: { tokens: 37, token_budget: 1000 } };
function receipt(entry, status = "succeeded") {
  return { id: "00112233-4455-6677-8899-aabbccddeeff", request_key: entry.record.request_key,
    request_hash: "a".repeat(64), input_hash: "b".repeat(64), provider: result.provider, model: result.model, status,
    result: status === "succeeded" ? result : null, error_code: null, error_detail: null, error_status: null, retry_after: null };
}

test("canonical source snapshots preserve nested JSON and defaults without a model choice", () => {
  assert.equal(canonicalJson({ z: "原稿", a: [{ y: 2, x: true }, null] }), '{"a":[{"x":true,"y":2},null],"z":"原稿"}');
  const normalized = normalizeRun(request());
  assert.equal(normalized.max_output_tokens, 16_000);
  assert.equal(normalized.format, "slides");
  assert.equal(normalized.variant, null);
  assert.equal(sourceHash(normalized), sourceHash(normalizeRun({ ...request(), max_output_tokens: 16_000, format: "slides", variant: null })));
  assert.throws(() => canonicalJson({ bad: NaN }), /finite/);
  assert.throws(() => canonicalJson({ bad: undefined }), /JSON values/);
  assert.throws(() => normalizeRun(request("../outside")), /invalid stage slug/);
  assert.deepEqual(normalizeRun({ ...request(), payload: { optional: undefined, rows: [undefined, 2] } }).payload, { rows: [null, 2] });
});

test("two clients retain the one key saved before dispatch and an immutable request snapshot", () => {
  const box = sandbox(), ctx = context(box), first = runReceiptStore(ctx, site), second = runReceiptStore(ctx, site);
  const original = request(), entry = first.prepare(original);
  original.payload.rows.push(3);
  assert.deepEqual(JSON.parse(readFileSync(entry.file, "utf8")).request.payload.rows, [1, 2]);
  assert.equal(second.prepare(request()).record.request_key, entry.record.request_key);
  assert.equal(first.find(request()).record.source_hash, sourceHash(normalizeRun(request())));
});

test("corrupted journals and source changes cannot silently produce a new request key", () => {
  for (const corruption of ["partial file", "changed source", "changed site"]) {
    const box = sandbox(), store = runReceiptStore(context(box), site), entry = store.prepare(request());
    const record = JSON.parse(readFileSync(entry.file, "utf8"));
    if (corruption === "changed source") record.request.instructions += "changed";
    if (corruption === "changed site") record.site = "https://other.test";
    writeFileSync(entry.file, corruption === "partial file" ? '{"schema_version":' : JSON.stringify(record));
    assert.throws(() => store.prepare(request()), /unreadable|changed identities/, corruption);
    assert.ok(existsSync(entry.file), "the original journal is preserved for inspection");
  }
});

test("each subsequent receipt must retain its server key, job, opaque hashes, provider and model", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site), entry = store.prepare(request());
  store.receive(entry, receipt(entry, "running"));
  for (const field of ["id", "request_key", "request_hash", "input_hash", "provider", "model"]) {
    const wrong = receipt(entry);
    wrong[field] = field.endsWith("hash") ? "c".repeat(64) : field === "id" || field === "request_key" ? "10112233-4455-6677-8899-aabbccddeeff" : "changed";
    assert.throws(() => store.receive(entry, wrong), /changed|mismatched/, field);
  }
  store.receive(entry, receipt(entry));
  assert.throws(() => validateRunReceipt({ ...receipt(entry), result: { ...result, text: "another answer" } }, entry.record), /settled stage receipt changed/);
});

test("settling one caller's slugs clears only results consumed by that client", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  const first = store.prepare(request("video-one")), second = store.prepare(request("video-two")), pending = store.prepare(request("video-three"));
  store.receive(first, receipt(first)); store.receive(second, receipt(second)); store.receive(pending, receipt(pending, "running"));
  store.consume(first); store.consume(second);
  store.settle(["video-one"]);
  assert.equal(existsSync(first.file), false);
  assert.equal(existsSync(second.file), true);
  assert.equal(existsSync(pending.file), true);
  const restarted = runReceiptStore(context(box), site);
  restarted.settle(["video-two"]);
  assert.ok(existsSync(second.file), "an unrelated unit cannot settle an answer this process did not consume");
});

test("explicit owner retry removes uncertain receipts and preserves running or completed ones", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  const uncertain = store.prepare(request("uncertain-video")), pending = store.prepare(request("running-video")), complete = store.prepare(request("complete-video"));
  store.receive(uncertain, receipt(uncertain, "uncertain")); store.receive(pending, receipt(pending, "running")); store.receive(complete, receipt(complete));
  store.retry("running-video"); store.retry("complete-video"); store.retry("uncertain-video");
  assert.equal(existsSync(uncertain.file), false);
  assert.equal(existsSync(pending.file), true);
  assert.equal(existsSync(complete.file), true);
});

test("changed inputs require an owner while a logical stage still has an unfinished receipt", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site), entry = store.prepare(request());
  store.receive(entry, receipt(entry, "running"));
  assert.throws(() => store.prepare({ ...request(), instructions: "Use a different source" }), (error) => error.code === "video_ai_receipt_input_changed");
  assert.ok(existsSync(entry.file));
});

test("persisted artifact adoption permits a correction after restart and survives later legitimate artifact changes", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site), entry = store.prepare(request());
  store.receive(entry, receipt(entry)); store.consume(entry);
  const artifact = path.join(box.base, "video.json"); writeFileSync(artifact, result.text);
  const proof = { artifacts: [{ path: artifact, sha256: createHash("sha256").update(result.text).digest("hex") }] };
  store.adopt("video-one", proof);
  assert.deepEqual(JSON.parse(readFileSync(entry.file, "utf8")).adoption.artifacts, proof.artifacts);
  writeFileSync(artifact, "a later accepted correction");
  const restarted = runReceiptStore(context(box), site);
  const fix = restarted.prepare({ ...request(), payload: { fix: "repair scene continuity" } });
  assert.notEqual(fix.record.request_key, entry.record.request_key);
  assert.equal(restarted.find(request()).record.receipt.result.text, result.text, "exact request still retains the historical completed result");
  restarted.settle(["video-one"]);
  assert.equal(existsSync(entry.file), false, "the adopted successful receipt can be settled after a later saved unit");
  assert.equal(existsSync(fix.file), true, "an unfinished correction remains recoverable");
});

test("adoption requires a consumed success and current saved artifact hashes", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site), entry = store.prepare(request());
  store.receive(entry, receipt(entry));
  store.adopt("video-one", { artifacts: [] });
  assert.equal(JSON.parse(readFileSync(entry.file, "utf8")).adopted, undefined, "restart or an unrelated writer cannot adopt an unread answer");
  store.consume(entry);
  assert.throws(() => store.adopt("video-one", { artifacts: [] }), /saved artifact proofs/);
  const artifact = path.join(box.base, "video.json"); writeFileSync(artifact, "different bytes");
  assert.throws(() => store.adopt("video-one", { artifacts: [{ path: artifact, sha256: "a".repeat(64) }] }), /bytes changed/);
  assert.equal(JSON.parse(readFileSync(entry.file, "utf8")).adopted, undefined);
  const restarted = runReceiptStore(context(box), site);
  assert.throws(() => restarted.prepare({ ...request(), instructions: "Changed source" }), /inputs changed/);
});

test("pending lookup tolerates only derived date and shared lexicon drift and retains the original wire request", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  const original = { ...request(), payload: { ...request().payload, today: "2026-10-04", lexicon: { terms: { GPU: "old reading" } }, brief: "approved facts" } };
  const entry = store.prepare(original); store.receive(entry, receipt(entry, "running"));
  const restarted = runReceiptStore(context(box), site);
  const drift = { ...original, payload: { ...original.payload, today: "2026-10-05", lexicon: { terms: { GPU: "old reading", CPU: "another lane's addition" } } } };
  const recovered = restarted.prepare(drift);
  assert.equal(recovered.record.request_key, entry.record.request_key);
  assert.deepEqual(recovered.record.request.payload, original.payload);
  assert.throws(() => restarted.prepare({ ...drift, payload: { ...drift.payload, brief: "new unreviewed facts" } }), /inputs changed/);
});
