import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readdirSync, readFileSync, renameSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { sandbox } from "../core/fixtures/load.mjs";
import { AUTO_ARCHIVE_REASON, canonicalJson, INPUT_CHANGED_CODE, JOB_GONE_KIND, jobGoneReason, normalizeRun, POLICY_HOLD_CODE, runReceiptStore, sourceHash, validateRunReceipt } from "./run-receipts.mjs";

const site = "https://site.test";
const request = (slug = "video-one") => ({ stage: "writer", slug, instructions: "Write the checked story.", payload: { locale: "zh-TW", rows: [1, 2] } });
const context = (box) => ({ home: box.base, root: box.root, env: { VIDEO_WORKDIR: box.work } });
const result = { text: '{"scenes":[]}', provider: "gemini", model: "chosen-before-restart", input_tokens: 25, output_tokens: 12, usage: { tokens: 37, token_budget: 1000 } };

test("settled policy refusals cannot be deleted or archived without fresh validated owner authority", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site), entry = store.prepare(request());
  store.receive(entry, { ...receipt(entry, "failed"), error_code: POLICY_HOLD_CODE, dispatched_at: null });
  assert.throws(() => store.removeFailed(entry), /policy refusal must be retained/);
  assert.throws(() => store.archive(entry, { requestId: "11112233-4455-6677-8899-aabbccddeeff" }), /validated policy retry/);
  assert.equal(store.retryCandidates("video-one").length, 0, "an old or unidentified retry cannot clear a policy hold");
  const authorization = { requestId: "11112233-4455-6677-8899-aabbccddeeff", policyValidated: true, reason: "fresh owner retry" };
  assert.equal(store.retryCandidates("video-one", authorization).length, 1);
  store.archive(entry, authorization);
  const again = store.prepare(request());
  store.receive(again, { ...receipt(again, "failed"), error_code: POLICY_HOLD_CODE, dispatched_at: null });
  assert.throws(() => store.archive(again, authorization), /already used/);
  assert.ok(existsSync(again.file), "a repeated acknowledgement preserves the newly held operation");
});
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

test("changed inputs find the unfinished journal as stale, and prepare refuses a new journal beside it until it is reconciled", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site), entry = store.prepare(request());
  store.receive(entry, receipt(entry, "running"));
  const changed = { ...request(), instructions: "Use a different source" };
  const found = store.find(changed);
  assert.equal(found.stale, true);
  assert.equal(found.file, entry.file);
  assert.equal(found.record.request_key, entry.record.request_key, "the caller gets the saved journal to reconcile with the server");
  assert.equal(store.find(request()).stale, undefined, "the exact request is a match, not stale");
  assert.throws(() => store.prepare(changed), (error) => error.code === INPUT_CHANGED_CODE && /inputs changed/.test(error.message));
  assert.ok(existsSync(entry.file));
  assert.equal(readdirSync(path.dirname(entry.file)).length, 1, "no second journal was created");
  // Reconciled by the caller (here: the run is over), the next prepare starts the new request.
  store.receive(entry, receipt(entry));
  store.archive(entry, { autoArchive: true });
  assert.equal(store.find(changed), null);
  const fresh = store.prepare(changed);
  assert.notEqual(fresh.record.request_key, entry.record.request_key);
  assert.equal(fresh.record.receipt, null);
});

test("a stale journal archives itself only when its run is over or never reached the server", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  const done = store.prepare(request("done-video")), never = store.prepare(request("never-video"));
  store.receive(done, receipt(done));
  for (const entry of [done, never]) {
    const before = JSON.parse(readFileSync(entry.file, "utf8"));
    store.archive(entry, { autoArchive: true });
    assert.equal(existsSync(entry.file), false);
    const archiveDir = path.join(path.dirname(entry.file), "archive");
    assert.deepEqual(readdirSync(archiveDir), [`${before.source_hash}-${before.request_key}.json`]);
    const archived = JSON.parse(readFileSync(path.join(archiveDir, readdirSync(archiveDir)[0]), "utf8"));
    assert.deepEqual(archived.receipt, before.receipt, "the saved receipt bytes are kept");
    assert.equal(archived.owner_retry.request_id, null, "no owner request id is consumed");
    assert.equal(archived.owner_retry.reason, AUTO_ARCHIVE_REASON);
    assert.match(archived.owner_retry.archived_at, /^\d{4}-\d{2}-\d{2}T/);
    assert.equal(store.find(request(before.request.slug)), null);
  }
  const running = store.prepare(request("running-video")), failed = store.prepare(request("failed-video")), held = store.prepare(request("held-video"));
  store.receive(running, receipt(running, "running")); store.receive(failed, receipt(failed, "failed"));
  store.hold(held, { error_code: POLICY_HOLD_CODE, error_status: 409, error_detail: "the video route is disabled" });
  for (const entry of [running, failed, held]) {
    assert.throws(() => store.archive(entry, { autoArchive: true }), /terminal stale run/, entry.record.request.slug);
    assert.ok(existsSync(entry.file));
  }
  store.removeFailed(failed);
  assert.equal(existsSync(failed.file), false, "a plain failure is cleared by removeFailed, not archived");
  const adopted = store.prepare(request("adopted-video"));
  store.receive(adopted, receipt(adopted)); store.consume(adopted);
  const artifact = path.join(box.base, "adopted.json"); writeFileSync(artifact, result.text);
  store.adopt("adopted-video", { artifacts: [{ path: artifact, sha256: createHash("sha256").update(result.text).digest("hex") }] });
  assert.throws(() => store.archive(adopted, { autoArchive: true }), /terminal stale run/, "an adopted success is settled, never archived");
});

test("a stale journal whose job the server no longer has is archived with the answer named, whatever its saved status", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  const gone = { status: 404, code: "video_ai_job_not_found" };
  assert.equal(jobGoneReason(gone), "the server no longer has this job (404 video_ai_job_not_found)");
  assert.equal(jobGoneReason({ status: 422, code: "" }), "the server no longer has this job (422)");
  for (const status of ["running", "uncertain", "succeeded"]) {
    const entry = store.prepare(request(`${status}-video`));
    store.receive(entry, receipt(entry, status));
    const before = JSON.parse(readFileSync(entry.file, "utf8"));
    store.archive(entry, { autoArchive: true, gone });
    assert.equal(existsSync(entry.file), false, status);
    const archiveDir = path.join(path.dirname(entry.file), "archive");
    const archived = JSON.parse(readFileSync(path.join(archiveDir, readdirSync(archiveDir)[0]), "utf8"));
    assert.deepEqual(archived.receipt, before.receipt, status);
    assert.equal(archived.owner_retry.request_id, null, status);
    assert.equal(archived.owner_retry.reason, jobGoneReason(gone), status);
  }
  // A policy hold stays for a validated retry; the worker, not the store, classifies the
  // answer, but it must at least be a 4xx with a code, and autoArchive must be asked for.
  const held = store.prepare(request("held-video")), running = store.prepare(request("kept-video"));
  store.receive(held, { ...receipt(held, "failed"), error_code: POLICY_HOLD_CODE, dispatched_at: null });
  store.receive(running, receipt(running, "running"));
  for (const [entry, options] of [[held, { autoArchive: true, gone }], [running, { gone }],
    [running, { autoArchive: true, gone: { status: 502, code: "upstream_unavailable" } }], [running, { autoArchive: true, gone: { status: 404 } }], [running, { autoArchive: true, gone: "404" }]]) {
    assert.throws(() => store.archive(entry, options), /can be archived/, JSON.stringify(options));
    assert.ok(existsSync(entry.file));
  }
  // A journal with no receipt has no job to be gone: it is archived as never dispatched.
  const never = store.prepare(request("never-video"));
  store.archive(never, { autoArchive: true, gone });
  const neverDir = path.join(path.dirname(never.file), "archive");
  assert.equal(JSON.parse(readFileSync(path.join(neverDir, readdirSync(neverDir)[0]), "utf8")).owner_retry.reason, AUTO_ARCHIVE_REASON);
});

test("an owner retry lists plain failed journals so the retry can clear them, and never policy holds without authority", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  const failed = store.prepare(request("video-one")), held = store.prepare(request("video-two"));
  store.receive(failed, receipt(failed, "failed"));
  store.receive(held, { ...receipt(held, "failed"), error_code: POLICY_HOLD_CODE, dispatched_at: null });
  assert.deepEqual(store.retryCandidates("video-one").map((entry) => entry.file), [failed.file]);
  assert.deepEqual(store.retryCandidates("video-two"), []);
});

test("the retry of a job_gone block lists that stage's queued and running journals, under the owner's request id only; no other retry touches a journal whose job may still be running", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  assert.equal(JOB_GONE_KIND, "job_gone:");
  const slug = "video-one";
  const journal = (extra, status) => {
    const entry = store.prepare({ ...request(slug), ...extra });
    if (status) store.receive(entry, receipt(entry, status));
    return entry;
  };
  const queued = journal({}, "queued"), running = journal({ variant: "episode" }, "running"), other = journal({ stage: "verifier" }, "running");
  // Not candidates under this kind: an answer that arrived (the normal run takes it) and a request that never reached the server.
  journal({ variant: "discuss" }, "succeeded");
  journal({ variant: "explainer" }, null);
  const requestId = "11112233-4455-6677-8899-aabbccddeeff";
  const reason = "the server no longer has the saved writer job (video_ai_job_not_found: 找不到這個權杖的影片工作)";
  const listed = (authorization) => store.retryCandidates(slug, authorization).map((entry) => entry.file).sort();
  assert.deepEqual(listed({ requestId, reason, kind: "job_gone:writer" }), [queued.file, running.file].sort());
  assert.deepEqual(listed({ requestId, reason, kind: "job_gone:verifier" }), [other.file]);
  for (const authorization of [undefined, { requestId, reason }, { requestId, reason, kind: null }, { requestId, reason, kind: "uncertain:writer" }, { requestId, reason, kind: "deferred:writer" },
    { requestId, reason, kind: "unrecorded:script" }, { requestId, reason, kind: "job_gone" }, { requestId, reason, kind: "job_gone:" }, { requestId, reason, kind: "job_gone:planner" },
    { reason, kind: "job_gone:writer" }, { requestId: "not-a-request", reason, kind: "job_gone:writer" }]) {
    assert.deepEqual(listed(authorization), [], JSON.stringify(authorization ?? null));
  }
  // The store archives such a journal only with the server's answer in hand (client.mjs retryRuns looks it up first).
  assert.throws(() => store.archive(running, { requestId, reason }), /can be archived/);
  assert.ok(existsSync(running.file));
  store.archive(running, { autoArchive: true, gone: { status: 404, code: "video_ai_job_not_found" } });
  assert.deepEqual(listed({ requestId, reason, kind: "job_gone:writer" }), [queued.file]);
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

// A journal rename that the OS refuses for the first `failures` matching attempts, or for ever.
// The original Windows cause (scanner, indexer, another handle) is not known; only the error is.
function denyRenames({ platform = "win32", code = "EPERM", failures = Infinity, only = () => true } = {}) {
  const io = { platform, attempts: [], waits: [], wait: (ms) => io.waits.push(ms) };
  let denied = 0;
  io.rename = (from, to) => {
    io.attempts.push({ from, to, mode: statSync(from).mode & 0o777, bytes: readFileSync(from, "utf8") });
    if (only(to) && denied++ < failures) throw Object.assign(new Error(`${code}: operation not permitted, rename`), { code, syscall: "rename" });
    renameSync(from, to);
  };
  return io;
}
const sha = (file) => createHash("sha256").update(readFileSync(file)).digest("hex");
const leftovers = (entry) => readdirSync(path.dirname(entry.file)).filter((name) => name.endsWith(".tmp"));

test("a transient Windows rename denial settles the same receipt from the same complete temporary file", () => {
  const box = sandbox(), io = denyRenames({ failures: 2 }), store = runReceiptStore({ ...context(box), receiptIo: io }, site);
  const entry = store.prepare(request()), key = entry.record.request_key;
  const saved = store.receive(entry, receipt(entry));
  assert.equal(io.attempts.length, 3);
  assert.deepEqual(io.waits, [10, 20]);
  assert.equal(new Set(io.attempts.map((attempt) => attempt.from)).size, 1, "every retry renames the one exclusive temporary file");
  assert.match(path.basename(io.attempts[0].from), new RegExp(`^${path.basename(entry.file).replaceAll(".", "\\.")}\\.[0-9a-f-]{36}\\.tmp$`));
  assert.ok(io.attempts.every((attempt) => attempt.to === entry.file));
  const bytes = readFileSync(entry.file, "utf8");
  assert.ok(io.attempts.every((attempt) => attempt.bytes === bytes), "the temporary file was complete before the first rename");
  const restarted = runReceiptStore(context(box), site).find(request());
  assert.equal(restarted.record.request_key, key);
  assert.deepEqual(restarted.record.receipt, saved);
  assert.equal(restarted.record.receipt.id, receipt(entry).id);
  assert.deepEqual(leftovers(entry), []);
});

test("a permanent Windows rename denial fails with the original error and keeps the earlier receipt", () => {
  const box = sandbox(), io = denyRenames(), ctx = { ...context(box), receiptIo: io };
  const plain = runReceiptStore(context(box), site), entry = plain.prepare(request());
  plain.receive(entry, receipt(entry, "running"));
  const before = sha(entry.file), store = runReceiptStore(ctx, site), held = store.prepare(request());
  assert.throws(() => store.receive(held, receipt(held)), (error) => error.code === "EPERM" && error.syscall === "rename");
  assert.equal(io.attempts.length, 7, "one attempt and six bounded retries");
  assert.deepEqual(io.waits, [10, 20, 40, 80, 160, 320]);
  assert.equal(sha(entry.file), before, "the earlier journal bytes are unchanged");
  assert.equal(held.record.receipt.status, "running", "the caller keeps the saved state, not the unsaved answer");
  assert.deepEqual(leftovers(entry), [], "the unsaved temporary file is removed");
  const restarted = runReceiptStore(context(box), site).prepare(request());
  assert.equal(restarted.record.request_key, entry.record.request_key, "a restart resumes the same key instead of buying a new run");
  assert.equal(restarted.record.receipt.id, receipt(entry).id);
});

test("rename errors off Windows, and other codes on Windows, fail on the first attempt", () => {
  for (const [platform, code] of [["linux", "EPERM"], ["linux", "EBUSY"], ["darwin", "EACCES"], ["win32", "ENOSPC"], ["win32", "EXDEV"]]) {
    const box = sandbox(), io = denyRenames({ platform, code, failures: 1 }), store = runReceiptStore({ ...context(box), receiptIo: io }, site);
    const entry = store.prepare(request()), before = sha(entry.file);
    assert.throws(() => store.receive(entry, receipt(entry, "running")), (error) => error.code === code, `${platform} ${code}`);
    assert.equal(io.attempts.length, 1, `${platform} ${code} is not retried`);
    assert.deepEqual(io.waits, []);
    assert.equal(sha(entry.file), before);
    assert.equal(entry.record.receipt, null);
    assert.deepEqual(leftovers(entry), []);
  }
  for (const code of ["EACCES", "EBUSY"]) {
    const box = sandbox(), io = denyRenames({ code, failures: 1 }), store = runReceiptStore({ ...context(box), receiptIo: io }, site);
    const entry = store.prepare(request());
    store.hold(entry, { error_code: POLICY_HOLD_CODE, error_status: 409, error_detail: "the video route is disabled" });
    assert.equal(io.attempts.length, 2, `${code} is retried on Windows`);
    assert.equal(runReceiptStore(context(box), site).find(request()).record.policy_rejection.error_code, POLICY_HOLD_CODE);
  }
});

test("an owner retry archive and a stale run's own archive survive a transient Windows denial of the final move", () => {
  for (const [status, options] of [["uncertain", {}], ["succeeded", { autoArchive: true }]]) {
    const box = sandbox(), io = denyRenames({ code: "EBUSY", failures: 1, only: (to) => path.basename(path.dirname(to)) === "archive" });
    const store = runReceiptStore({ ...context(box), receiptIo: io }, site);
    const entry = store.prepare(request()), archiveDir = path.join(path.dirname(entry.file), "archive");
    store.receive(entry, receipt(entry, status));
    const bytes = readFileSync(entry.file, "utf8");
    store.archive(entry, options);
    assert.equal(existsSync(entry.file), false, status);
    assert.deepEqual(io.waits, [10], status);
    assert.equal(io.attempts.filter((attempt) => attempt.from === entry.file).length, 2, status);
    assert.deepEqual(readdirSync(archiveDir), [`${entry.record.source_hash}-${entry.record.request_key}.json`], status);
    const archived = JSON.parse(readFileSync(path.join(archiveDir, readdirSync(archiveDir)[0]), "utf8"));
    assert.equal(archived.request_key, entry.record.request_key, status);
    assert.deepEqual(archived.receipt, JSON.parse(bytes).receipt, `${status}: the receipt bytes moved, never rewritten`);
    assert.deepEqual(leftovers(entry), [], status);
    if (options.autoArchive) assert.deepEqual({ ...archived.owner_retry, archived_at: null }, { request_id: null, reason: AUTO_ARCHIVE_REASON, archived_at: null });
  }
});

test("a journal replacement's temporary file is owner-only before its rename", { skip: process.platform === "win32" && "Windows does not report POSIX modes" }, () => {
  const box = sandbox(), io = denyRenames({ platform: process.platform, failures: 0 }), store = runReceiptStore({ ...context(box), receiptIo: io }, site);
  const entry = store.prepare(request());
  store.receive(entry, receipt(entry, "running"));
  assert.equal(io.attempts[0].mode, 0o600);
  assert.equal(statSync(entry.file).mode & 0o777, 0o600);
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
  const changed = { ...drift, payload: { ...drift.payload, brief: "new unreviewed facts" } };
  assert.throws(() => restarted.prepare(changed), /inputs changed/);
  assert.equal(restarted.find(changed).stale, true);
});

test("a video's saved runs whose answer is still to be taken are listed by stage and variant: prepared, queued, running, or succeeded and not adopted; the journals are only read", () => {
  const box = sandbox(), store = runReceiptStore(context(box), site);
  assert.deepEqual(store.untaken("video-one"), [], "a video with no journal yet");
  // A discussion of the screenplay: the writer's own variant, beside whatever the video's stages saved.
  const entry = store.prepare({ ...request(), variant: "discuss" });
  const listed = (status) => [{ stage: "writer", variant: "discuss", status }];
  assert.deepEqual(store.untaken("video-one"), listed(null), "prepared and perhaps sent");
  for (const status of ["queued", "running", "succeeded"]) {
    store.receive(entry, receipt(entry, status));
    const bytes = readFileSync(entry.file, "utf8");
    assert.deepEqual(store.untaken("video-one"), listed(status));
    assert.equal(readFileSync(entry.file, "utf8"), bytes, `${status}: nothing is written`);
  }
  assert.deepEqual(runReceiptStore(context(box), site).untaken("video-one"), listed("succeeded"), "another process reads the same");
  assert.deepEqual(store.untaken("video-two"), [], "another video's runs are its own");
  // Once its output is saved the answer has been taken, whether or not the unit settled the journal yet.
  const artifact = path.join(box.base, "video.json"); writeFileSync(artifact, result.text);
  store.consume(entry);
  store.adopt("video-one", { artifacts: [{ path: artifact, sha256: createHash("sha256").update(result.text).digest("hex") }] });
  assert.deepEqual(store.untaken("video-one"), []);

  // A failed run is cleared by the next request, an uncertain one waits for the owner, a policy hold for a validated retry: none has an answer to take.
  for (const [slug, status, extra] of [["video-failed", "failed", {}], ["video-uncertain", "uncertain", {}], ["video-held", "failed", { error_code: POLICY_HOLD_CODE, dispatched_at: null }]]) {
    const other = store.prepare(request(slug));
    store.receive(other, { ...receipt(other, status), ...extra });
    assert.deepEqual(store.untaken(slug), [], slug);
  }
  // A journal set aside is not listed, and one that cannot be read fails closed like every other read.
  const aside = store.prepare(request("video-aside"));
  store.archive(aside, { autoArchive: true });
  assert.deepEqual(store.untaken("video-aside"), []);
  const broken = store.prepare(request("video-broken"));
  writeFileSync(broken.file, "{ not json");
  assert.throws(() => store.untaken("video-broken"), /unreadable/);
});
