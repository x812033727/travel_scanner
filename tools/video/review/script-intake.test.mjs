import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { afterEach, test } from "node:test";

import { loadIntake, parseScript, runIntake } from "./script-intake.mjs";

const tempRoots = [];
afterEach(() => { while (tempRoots.length) rmSync(tempRoots.pop(), { recursive: true, force: true }); });
const sha = (value) => createHash("sha256").update(value).digest("hex");

function fixture() {
  const root = mkdtempSync(path.join(os.tmpdir(), "script-intake-"));
  tempRoots.push(root);
  const entries = [];
  for (const number of [3, 4, 5, 6, 7, 8, 10, 11, 14, 15]) {
    const id = `C${String(number).padStart(2, "0")}`;
    const slug = `story-everyday-fixture-${id.toLowerCase()}`;
    const script_path = `docs/videos/${slug}/script.md`;
    const script = Array.from({ length: 6 }, (_, i) =>
      `## ${i + 1} hook｜章 ${i + 1}\n\n| ID | 旁白 | 依據 |\n| --- | --- | --- |\n| ${id.toLowerCase()}0${i + 1}01 | 第 ${i + 1} 句。 | S1 |\n`
    ).join("\n");
    const file = path.join(root, script_path);
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, script);
    entries.push({ id, number, slug, title: `${id} test`, script_path,
      script_sha256: sha(script), expected_lines: 6, approval_pr: 1000 + number,
      approval_basis: "owner approved exact PR script" });
  }
  const manifestPath = "docs/videos/brand-stories-everyday-reversals-20261020/approved-scripts.json";
  const file = path.join(root, manifestPath);
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, JSON.stringify({ schema_version: 1, series_slug: "brand-stories-everyday-reversals", entries }));
  return { root, manifestPath, entries, manifestFile: file };
}

test("dry-run validates exact local sources without even calling the transport", async () => {
  const box = fixture();
  let calls = 0;
  const result = await runIntake({ ...box, request: () => { calls++; throw new Error("network call"); } });
  assert.equal(calls, 0);
  assert.equal(result.length, 10);
  assert.ok(result.every((row) => row.action === "dry-run-local-only"));
});

test("a changed script refuses before any remote call", async () => {
  const box = fixture();
  const target = path.join(box.root, box.entries[0].script_path);
  writeFileSync(target, readFileSync(target, "utf8") + "changed\n");
  let calls = 0;
  await assert.rejects(runIntake({ ...box, apply: true, request: () => { calls++; } }), /SHA256 mismatch/);
  assert.equal(calls, 0);
});

test("a nonpaused series refuses before PUT or POST", async () => {
  const box = fixture();
  const calls = [];
  const request = async (method, route) => {
    calls.push([method, route]);
    return { series: { slug: "brand-stories-everyday-reversals", kind: "story", status: "active" },
      episode: { number: 3, slug: box.entries[0].slug } };
  };
  await assert.rejects(runIntake({ ...box, ids: ["C03"], apply: true, request }), /not paused/);
  assert.deepEqual(calls.map(([method]) => method), ["GET"]);
});

test("submission remains pending and rerun does not repeat a write", async () => {
  const box = fixture();
  const entry = box.entries[0];
  const calls = [];
  let project = null;
  const request = async (method, route, options = {}) => {
    calls.push({ method, route, options });
    if (route.includes("/context?episode=")) return {
      series: { slug: "brand-stories-everyday-reversals", kind: "story", status: "paused" },
      episode: { number: 3, slug: entry.slug, status: "planned" } };
    if (method === "GET") {
      if (project) return structuredClone(project);
      const error = new Error("not found"); error.status = 404; throw error;
    }
    if (method === "PUT") {
      assert.equal(options.json.episode_number, 3);
      project = { slug: entry.slug, ...options.json, reviews: [], dropped_at: null };
      return structuredClone(project);
    }
    if (method === "POST") {
      assert.equal(options.json.content_sha256, entry.script_sha256);
      assert.equal(options.json.payload.hand_pushed, true);
      assert.equal(options.json.payload.scenes.length, 6);
      const review = { id: "review-1", gate: "script", subject: null, status: "pending",
        content_sha256: entry.script_sha256, summary: options.json.summary,
        payload: options.json.payload };
      project.reviews.push(review);
      return structuredClone(review);
    }
    throw new Error(`unexpected ${method}`);
  };
  const first = await runIntake({ ...box, ids: ["C03"], apply: true, request });
  assert.equal(first[0].action, "submitted");
  const writes = calls.filter(({ method }) => method === "PUT" || method === "POST").length;
  const second = await runIntake({ ...box, ids: ["C03"], apply: true, request });
  assert.equal(second[0].action, "already-present");
  assert.equal(calls.filter(({ method }) => method === "PUT" || method === "POST").length, writes);
});

test("the existing C03 approved exact-hash narration is retained without a new card", async () => {
  const box = fixture();
  const entry = loadIntake(box.manifestPath, { root: box.root, ids: ["C03"] }).entries[0];
  const calls = [];
  const request = async (method, route) => {
    calls.push([method, route]);
    if (route.includes("/context?episode=")) return {
      series: { slug: "brand-stories-everyday-reversals", kind: "story", status: "paused" },
      episode: { number: 3, slug: entry.slug, status: "planned" },
    };
    return { slug: entry.slug, series_slug: "brand-stories-everyday-reversals",
      episode_number: 3, format: "drama", shorts_line: null, dropped_at: null,
      reviews: [{ id: "legacy", gate: "script", subject: null, status: "approved",
        content_sha256: entry.script_sha256, summary: "Earlier approved C03 script",
        payload: { hand_pushed: true, scenes: entry.scenes } }] };
  };
  const result = await runIntake({ ...box, ids: ["C03"], apply: true, request });
  assert.equal(result[0].action, "already-present");
  assert.deepEqual(calls.map(([method]) => method), ["GET", "GET"]);
});

test("strict parser rejects an unsupported or ambiguous row", () => {
  const box = fixture();
  const source = readFileSync(path.join(box.root, box.entries[0].script_path), "utf8");
  assert.equal(parseScript(source, "C03").length, 6);
  assert.throws(() => parseScript(source.replace("| c030101 |", "| c030101 | extra |"), "C03"), /malformed table row/);
  assert.equal(loadIntake(box.manifestPath, { root: box.root }).entries.length, 10);
});
