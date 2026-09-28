import { test } from "node:test";
import assert from "node:assert/strict";
import { mkdtempSync, rmSync, appendFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { Store } from "../src/store.mjs";
import { hash, Refused, validateManifest } from "../src/contract.mjs";
import { Runner } from "../src/runner.mjs";
import { createServer } from "../src/server.mjs";

const CHANNEL = "UC" + "a".repeat(22);
const ID = "abcdefghijk";
const SECRET = "fixture-only-".repeat(4);
const BYTES = Buffer.from("fixture-video");
function manifest(overrides = {}) {
  return validateManifest({
    version: 1, slug: "test-video", review_sha256: hash("approved"), channel_id: CHANNEL, video_id: null,
    metadata: { title: "Title", description: "Description\n00:00 Introduction", tags: ["test"],
      default_language: "zh-TW", category_id: "28", made_for_kids: false,
      contains_synthetic_media: true, localizations: { en: { title: "English", description: "Full description" } } },
    files: [{ role: "final", sha256: hash(BYTES), size: BYTES.length, content_type: "video/mp4" }],
    ...overrides,
  }, CHANNEL);
}
function fixture(t) {
  const directory = mkdtempSync(path.join(os.tmpdir(), "mokaair-uploader-"));
  let store = new Store(directory);
  t.after(() => {
    store.close();
    assert.ok(path.resolve(directory).startsWith(path.resolve(os.tmpdir(), "mokaair-uploader-")));
    rmSync(directory, { recursive: true });
  });
  return { get store() { return store; }, directory, restart() { store.close(); store = new Store(directory); return store; } };
}
async function queued(store, m = manifest()) {
  const id = hash(m.slug + m.review_sha256);
  store.create(id, m);
  if (m.files.length) await store.put(id, hash(BYTES), 0, BYTES);
  await store.queue(id);
  return id;
}

test("resumable staging verifies the full hash, survives restart and deduplicates a request", async (t) => {
  const f = fixture(t); const m = manifest(); const id = hash("job");
  f.store.create(id, m);
  await f.store.put(id, hash(BYTES), 0, BYTES.subarray(0, 3));
  f.restart();
  assert.equal(f.store.view(f.store.get(id)).files[0].received, 3);
  await assert.rejects(f.store.put(id, hash(BYTES), 0, BYTES), { code: "offset_changed" });
  await f.store.put(id, hash(BYTES), 3, BYTES.subarray(3));
  assert.equal((await f.store.queue(id)).state, "queued");
  assert.equal(f.store.create(id, m).id, id);
  assert.equal(f.store.all().length, 1);
  assert.throws(() => f.store.create(id, manifest({ metadata: { ...m.metadata, title: "changed" } })), { code: "request_changed" });
});

test("wrong hashes, path traversal, a second daemon and incomplete queues are refused", async (t) => {
  const f = fixture(t); const id = hash("job"); f.store.create(id, manifest());
  assert.throws(() => new Store(f.directory), { code: "service_already_running" });
  assert.throws(() => f.store.get("../browser"), { code: "job_not_found" });
  await assert.rejects(f.store.put(id, hash(BYTES), 0, Buffer.alloc(BYTES.length, 1)), { code: "file_hash_mismatch" });
  assert.equal(f.store.received(f.store.get(id), hash(BYTES)), 0);
  await assert.rejects(f.store.queue(id), { code: "files_incomplete" });
});

test("restart after upload began requires reconciliation and never uploads a duplicate", async (t) => {
  const f = fixture(t); const id = await queued(f.store);
  f.store.patch(id, { state: "running", upload_started: true });
  f.restart();
  assert.equal(f.store.get(id).state, "needs_action");
  assert.throws(() => f.store.resume(id), { code: "video_id_required" });
  assert.throws(() => f.store.cancel(id), { code: "video_id_required" });
  let uploads = 0; const opened = [];
  const driver = { connect: async () => {}, channel: async () => {}, openPrivate: async (video) => opened.push(video),
    upload: async () => { uploads++; }, step: async () => {} };
  f.store.resume(id, ID);
  await new Runner(f.store, driver).tick();
  assert.equal(uploads, 0);
  assert.deepEqual(opened, [ID]);
  assert.equal(f.store.get(id).state, "done");
});

test("an uncertain UI action is paused, redacted and holds later jobs until the owner continues", async (t) => {
  const f = fixture(t); const id = await queued(f.store);
  const second = await queued(f.store, manifest({ slug: "next-video" }));
  let uploads = 0;
  const driver = { connect: async () => {}, channel: async () => {}, openPrivate: async () => {},
    upload: async (_job, checkpoint) => { checkpoint.started(); uploads++; throw new Error("secret-cookie-content"); }, step: async () => {} };
  const runner = new Runner(f.store, driver);
  await Promise.all([runner.tick(), runner.tick()]);
  assert.equal(uploads, 1);
  assert.equal(f.store.get(id).code, "studio_changed");
  assert.equal(f.store.get(second).state, "queued");
  await runner.tick();
  assert.equal(uploads, 1);
  assert.ok(!JSON.stringify(f.store.view(f.store.get(id))).includes("secret-cookie-content"));
  assert.ok(!Object.hasOwn(f.store.view(f.store.get(id)), "manifest"));
});

test("private upload checkpoints the ID and only retries unfinished steps", async (t) => {
  const f = fixture(t); const id = await queued(f.store); const steps = [];
  let uploads = 0; let failed = false;
  const driver = { connect: async () => {}, channel: async (channel) => assert.equal(channel, CHANNEL), openPrivate: async () => {},
    upload: async (_job, cp) => { assert.equal(f.store.get(id).upload_started, false); cp.started(); uploads++; cp.identified(ID); },
    step: async (step) => { steps.push(step); if (step === "verify" && !failed) { failed = true; throw new Refused("save_unconfirmed"); } } };
  const runner = new Runner(f.store, driver);
  await runner.tick();
  assert.equal(f.store.get(id).video_id, ID);
  f.store.resume(id);
  await runner.tick();
  assert.equal(uploads, 1);
  assert.deepEqual(steps, ["localization_en", "verify", "verify"]);
  assert.equal(f.store.get(id).state, "done");
});

test("files modified after staging are caught before any browser action", async (t) => {
  const f = fixture(t); const id = await queued(f.store); let connects = 0;
  appendFileSync(f.store.file(f.store.get(id), hash(BYTES)), "changed");
  await new Runner(f.store, { connect: async () => { connects++; } }).tick();
  assert.equal(connects, 0);
  assert.equal(f.store.get(id).code, "file_hash_mismatch");
});

test("manifest rejects missing disclosure, wrong channels, unexpected roles and paths", () => {
  const m = manifest();
  for (const value of [
    { ...m, channel_id: "UC" + "b".repeat(22) }, { ...m, slug: "../escape" },
    { ...m, metadata: { ...m.metadata, contains_synthetic_media: undefined } },
    { ...m, metadata: { ...m.metadata, localizations: { unknown: { title: "x", description: "y" } } } },
    { ...m, files: [{ ...m.files[0], role: "../browser" }] },
  ]) assert.throws(() => validateManifest(value, CHANNEL), Refused);
});

test("HTTP API authenticates every job route and supports staging without exposing credentials", async (t) => {
  const f = fixture(t); const server = createServer({ store: f.store, secret: SECRET, channel: CHANNEL });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  t.after(() => { server.closeAllConnections(); server.close(); });
  const base = "http://127.0.0.1:" + server.address().port;
  const id = hash("http-job");
  assert.equal((await fetch(base + "/health")).status, 200);
  assert.equal((await fetch(base + "/projects/test-video")).status, 401);
  const headers = { Authorization: "Bearer " + SECRET };
  const create = await fetch(base + "/jobs/" + id, { method: "PUT", headers, body: JSON.stringify(manifest()) });
  assert.equal(create.status, 200);
  const file = await fetch(base + "/jobs/" + id + "/files/" + hash(BYTES) + "?offset=0", { method: "PUT", headers, body: BYTES });
  assert.equal(file.status, 200);
  const queue = await fetch(base + "/jobs/" + id + "/queue", { method: "POST", headers });
  assert.equal((await queue.json()).state, "queued");
  const response = await (await fetch(base + "/projects/test-video", { headers })).text();
  assert.ok(!response.includes(SECRET));
  assert.ok(!response.includes("Description"));
});

test("cancel before upload can resume staging, while completed video identities cannot change", async (t) => {
  const f = fixture(t); const id = hash("cancel"); f.store.create(id, manifest());
  f.store.cancel(id);
  assert.equal(f.store.resume(id).state, "staging");
  f.store.patch(id, { state: "needs_action", video_id: ID });
  assert.throws(() => f.store.resume(id, "different01"), { code: "video_changed" });
  f.store.patch(id, { state: "done" });
  assert.throws(() => f.store.create(hash("new-package"), manifest({ review_sha256: hash("new") })), { code: "existing_video_required" });
});

test("an uncertain old package can be reconciled and cancelled without resuming its upload", (t) => {
  const f = fixture(t); const id = hash("old");
  f.store.create(id, manifest());
  f.store.patch(id, { state: "needs_action", upload_started: true });
  assert.throws(() => f.store.cancel(id), { code: "video_id_required" });
  assert.equal(f.store.cancel(id, ID).video_id, ID);
  assert.equal(f.store.get(id).state, "cancelled");
  const next = manifest({ review_sha256: hash("new-approval"), video_id: ID });
  assert.equal(f.store.create(hash("next"), next).video_id, ID);
  assert.equal(f.store.get(id).completed.length, 0);
});
