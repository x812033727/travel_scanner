import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test, { after, before } from "node:test";
import { fileURLToPath } from "node:url";

import {
  applyBundle,
  main,
  pacedClient,
  prepareBundle,
  SOURCES,
  validateBundle,
} from "../../../ops/video/import_outline_reviews.mjs";

const root = path.resolve(fileURLToPath(new URL("../../../", import.meta.url)));
const temporaryRoot = path.resolve(os.tmpdir());
const temporary = mkdtempSync(path.join(temporaryRoot, "outline-recovery-test-"));
const workBase = path.join(temporary, "empty-work");
const ctx = { root, env: {} };
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const clone = (value) => structuredClone(value);
let bundle;

before(async () => {
  bundle = await prepareBundle(ctx, workBase);
});

after(() => {
  assert.equal(path.dirname(path.resolve(temporary)), temporaryRoot);
  assert.ok(path.basename(temporary).startsWith("outline-recovery-test-"));
  rmSync(temporary, { recursive: true, force: true });
});

/** A remote site double. Every possible mutation is recorded; no fetch/client is constructed. */
function site() {
  const projects = new Map();
  const calls = [];
  let reportNumber = 0;
  const client = {
    async videos() {
      calls.push(["videos"]);
      return [...projects.values()].map((project) => ({ slug: project.slug }));
    },
    async reviews(slug) {
      calls.push(["reviews", slug]);
      return clone(projects.get(slug) ?? null);
    },
    async report(slug, project) {
      calls.push(["report", slug]);
      const reported = { ...clone(project), slug, last_synced_at: `report-${++reportNumber}`, reviews: [] };
      projects.set(slug, reported);
      return clone(reported);
    },
    async submit(slug, review) {
      calls.push(["submit", slug]);
      const submitted = { ...clone(review), status: "pending", subject: null };
      projects.get(slug).reviews.push(submitted);
      return clone(submitted);
    },
  };
  return {
    client,
    projects,
    calls,
    writes: () => calls.filter(([method]) => ["report", "submit"].includes(method)),
  };
}

function recovery(remote, receipt = { reported: {} }) {
  const saved = [];
  return {
    options: {
      client: remote.client,
      receipt,
      saveReceipt: async (value) => { saved.push(clone(value)); },
    },
    saved,
  };
}

test("all ten authored sources preserve original brief bytes and require a manual outline choice", async () => {
  assert.equal(bundle.items.length, 10);
  assert.equal(bundle.work_base, workBase);
  assert.deepEqual(bundle.items.map(({ slug }) => slug), SOURCES.map(([, slug]) => slug));
  for (const item of bundle.items) {
    const sourceDir = path.join(root, "docs/videos", item.slug);
    const brief = readFileSync(path.join(sourceDir, "brief.md"));
    const video = readFileSync(path.join(sourceDir, "video.json"));
    assert.equal(item.source.brief_sha256, digest(brief));
    assert.equal(item.source.video_sha256, digest(video));
    assert.equal(item.review.content_sha256, digest(brief));
    assert.equal(item.review.payload.brief, brief.toString("utf8"));
    assert.equal(item.review.gate, "outline");
    assert.deepEqual(item.review.files, []);
    assert.equal(Object.hasOwn(item.review.payload, "pick"), false);
    assert.ok(item.review.payload.options.length >= 2 && item.review.payload.options.length <= 3);
    assert.equal(new Set(item.review.payload.options.map(({ key }) => key)).size, item.review.payload.options.length);
    assert.ok(item.project.source_guide);
    assert.equal(item.project.format, "slides");
  }
  await validateBundle(bundle, ctx);
});

test("CLI dry run validates the source bundle without invoking any site method", async () => {
  const input = path.join(temporary, "dry-run.json");
  writeFileSync(input, JSON.stringify(bundle));
  const remote = site();
  let output = "";
  assert.equal(await main(["--input", input], {
    ...ctx,
    client: remote.client,
    stdout: { write: (text) => { output += text; } },
  }), 0);
  const result = JSON.parse(output);
  assert.equal(result.mode, "dry-run");
  assert.equal(result.projects, 10);
  assert.equal(result.manual_outline_reviews, 10);
  assert.equal(result.media_uploads, 0);
  assert.equal(result.model_calls, 0);
  assert.deepEqual(remote.calls, []);
});

test("fresh recovery preflights all ten, makes twenty writes, then replay makes none", async () => {
  const remote = site();
  const { options, saved } = recovery(remote);
  const result = await applyBundle(bundle, options);
  assert.equal(result.length, 10);
  assert.ok(result.every(({ status }) => status === "pending"));
  assert.equal(remote.writes().length, 20);
  assert.equal(saved.length, 10);
  assert.equal(remote.projects.size, 10);
  const firstWrite = remote.calls.findIndex(([method]) => method === "report");
  assert.deepEqual(remote.calls.slice(1, 11), SOURCES.map(([, slug]) => ["reviews", slug]));
  assert.equal(firstWrite, 12); // inventory, ten-project preflight, immediate first-project recheck
  for (const item of bundle.items) {
    const project = remote.projects.get(item.slug);
    assert.equal(project.reviews.length, 1);
    assert.deepEqual(project.reviews[0].payload, item.review.payload);
    assert.equal(project.reviews[0].status, "pending");
  }
  remote.calls.length = 0;
  const replay = await applyBundle(bundle, options);
  assert.ok(replay.every(({ status }) => status === "already_pending"));
  assert.deepEqual(remote.writes(), []);
  assert.equal(saved.length, 10);
});

test("a collision on the last source prevents every write in the batch", async () => {
  const remote = site();
  const item = bundle.items.at(-1);
  remote.projects.set(item.slug, { ...clone(item.project), slug: item.slug, title: "Existing owner work", reviews: [] });
  await assert.rejects(applyBundle(bundle, recovery(remote).options), /collision/);
  assert.deepEqual(remote.writes(), []);
  assert.equal(remote.calls.filter(([method]) => method === "reviews").length, 10);
});

test("a project created after preflight is caught by the immediate recheck", async () => {
  const remote = site();
  const read = remote.client.reviews;
  let reads = 0;
  remote.client.reviews = async (slug) => {
    if (++reads === 11) {
      remote.projects.set(slug, { slug, title: "Another writer created this", reviews: [] });
    }
    return read(slug);
  };
  await assert.rejects(applyBundle(bundle, recovery(remote).options), /collision|changed after preflight/);
  assert.deepEqual(remote.writes(), []);
});

test("a receipt saved before failed submission resumes only that exact reported card", async () => {
  const remote = site();
  const originalSubmit = remote.client.submit;
  remote.client.submit = async () => { throw new Error("injected interrupted submission"); };
  const initial = recovery(remote);
  await assert.rejects(applyBundle(bundle, initial.options), /interrupted submission/);
  assert.deepEqual(remote.writes(), [["report", bundle.items[0].slug]]);
  assert.equal(initial.saved.length, 1);
  const receipt = clone(initial.saved[0]);
  assert.ok(receipt.reported[bundle.items[0].slug].last_synced_at);
  assert.match(receipt.reported[bundle.items[0].slug].project_sha256, /^[0-9a-f]{64}$/);

  // Without the persisted receipt, an empty matching card is not ours to take over.
  await assert.rejects(applyBundle(bundle, recovery(remote).options), /refusing to overwrite/);
  assert.equal(remote.writes().length, 1);
  remote.client.submit = originalSubmit;
  remote.calls.length = 0;
  const resumed = await applyBundle(bundle, recovery(remote, receipt).options);
  assert.ok(resumed.every(({ status }) => status === "pending"));
  assert.equal(remote.writes().length, 19);
  assert.deepEqual(remote.writes().filter(([method, slug]) => method === "report" && slug === bundle.items[0].slug), []);
  assert.ok([...remote.projects.values()].every(({ reviews }) => reviews.length === 1));
});

test("injected judge choices cannot turn authored outlines into auto-approved reviews", async () => {
  const injected = clone(bundle);
  injected.items[0].review.payload.pick = "A";
  await assert.rejects(validateBundle(injected, ctx), /Bundle differs|manual outline/);
});

test("CLI refuses an unapproved bundle hash before any site operation", async () => {
  const input = path.join(temporary, "bad-hash.json");
  writeFileSync(input, JSON.stringify(bundle));
  const remote = site();
  await assert.rejects(main(["--input", input, "--apply", "--expected-sha256", "0".repeat(64)], {
    ...ctx,
    client: remote.client,
    stdout: { write() {} },
  }), /exact reviewed bundle bytes/);
  assert.deepEqual(remote.calls, []);
});

test("paced requests start a second apart, stay sequential and continue after a rejection", async () => {
  let clock = 100;
  let active = 0;
  let peak = 0;
  const starts = [];
  const sleeps = [];
  const methods = ["videos", "reviews", "report", "submit"];
  const client = Object.fromEntries(methods.map((method) => [method, async (...args) => {
    starts.push({ method, at: clock, args });
    peak = Math.max(peak, ++active);
    await Promise.resolve();
    clock += 75;
    active--;
    if (method === "reviews") throw new Error("injected read failure");
    return method;
  }]));
  const paced = pacedClient(client, {
    now: () => clock,
    sleep: async (milliseconds) => { sleeps.push(milliseconds); clock += milliseconds; },
  });
  const results = await Promise.allSettled(methods.map((method) => paced[method](method)));
  assert.deepEqual(starts.map(({ method }) => method), methods);
  assert.deepEqual(starts.map(({ at }) => at), [100, 1100, 2100, 3100]);
  assert.deepEqual(starts.map(({ args }) => args), methods.map((method) => [method]));
  assert.deepEqual(sleeps, [925, 925, 925]);
  assert.equal(peak, 1);
  assert.deepEqual(results.map(({ status }) => status), ["fulfilled", "rejected", "fulfilled", "fulfilled"]);
});
