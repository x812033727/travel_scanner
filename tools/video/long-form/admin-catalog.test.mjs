import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, mkdirSync, readFileSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { buildAdminCatalog, OUTPUT_PATH, PLANS_PATH, requireSourcePath, serializeCatalog, sourceReader } from "./admin-catalog.mjs";
import { CATALOG_COUNTS, ROOT } from "./plans.mjs";

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const actualReader = sourceReader();
const snapshots = new Map();
const original = (relative) => {
  if (!snapshots.has(relative)) snapshots.set(relative, actualReader(relative));
  return snapshots.get(relative);
};
const readChanged = (changes) => (relative) => changes.get(relative) ?? original(relative);
const changePlans = (edit) => {
  const plans = JSON.parse(original(PLANS_PATH));
  edit(plans);
  return new Map([[PLANS_PATH, Buffer.from(JSON.stringify(plans))]]);
};
const catalog = buildAdminCatalog({ readSource: original });
const entry = (name, id) => catalog.entries.find((row) => row.catalog === name && row.id === id);

test("the API bundle exactly reproduces 473 source-bound entries without production flags", () => {
  assert.equal(catalog.format_version, 1);
  assert.equal(catalog.plans_sha256, sha(original(PLANS_PATH)));
  assert.deepEqual(catalog.catalog_counts, CATALOG_COUNTS);
  assert.equal(catalog.entries.length, 473);
  assert.equal(new Set(catalog.entries.map((row) => `${row.catalog}/${row.id}`)).size, 473);
  assert.equal(new Set(catalog.entries.map((row) => row.video_slug)).size, 473);
  assert.equal(readFileSync(path.join(ROOT, OUTPUT_PATH), "utf8"), serializeCatalog(catalog));
  assert.deepEqual(Object.keys(catalog), ["format_version", "plans_sha256", "catalog_counts", "entries"]);
  for (const row of catalog.entries) {
    assert.equal(row.min_duration_seconds, 480);
    assert.equal(row.target_duration_seconds, row.catalog === "brand-stories" ? 780 : 600);
    assert.equal(row.source_sha256, sha(original(row.source_path)));
    assert.match(row.source_record_sha256, /^[a-f0-9]{64}$/);
    assert.ok(row.details.length > 0 && row.details.every((detail) => detail.text.trim()));
    assert.equal(new Set(row.details.map((detail) => detail.label)).size, row.details.length);
    assert.equal(Boolean(row.source_package_path), row.details.some((detail) => detail.label === "source_package"));
    if (row.source_package_path) assert.equal(row.source_package_sha256, sha(original(row.source_package_path)));
  }
});

test("source titles are preserved, including corrected second-season production angles", () => {
  const sources = [
    ["season1", "docs/videos/so-thats-why/episodes.json", "episodes", "title"],
    ["season2", "docs/videos/so-thats-why/season2/dispositions.json", "episodes", "production_title"],
    ["season3", "docs/videos/so-thats-why/season3-topics.json", "episodes", "title"],
    ["brand-stories", "docs/videos/story-plans/brand-stories-100/stories.json", "stories", "title"],
    ["ai-terms", "docs/videos/ai-terms/terms.json", "terms", "zh"],
  ];
  for (const [name, file, key, title] of sources) {
    const byId = new Map(JSON.parse(original(file))[key].map((record) => [record.id, record]));
    for (const row of catalog.entries.filter((record) => record.catalog === name)) {
      assert.equal(row.title, byId.get(row.id)[title], `${name}/${row.id}`);
    }
  }
  assert.equal(entry("season2", "B28").title, "2018年Saks，為何把美妝搬到二樓？");
  assert.equal(entry("season2", "B30"), undefined);
  assert.equal(entry("ai-terms", "token").title, "token");
  assert.ok(entry("ai-terms", "token").details[0].text.includes("來源文章標題\ntoken（Token）是什麼：AI 如何計算文字長度"));
});

test("candidate, backlog, planned and covered source stages do not turn into production states", () => {
  const candidates = catalog.entries.filter((row) => row.catalog === "season3");
  assert.equal(candidates.length, 100);
  assert.ok(candidates.every((row) => row.stage === "CHECKED_CANDIDATE_REQUIRES_OUTLINE" && row.source_status === "checked"));
  assert.ok(candidates.every((row) => row.source_package_path === null && row.details.length === 1));
  const terms = catalog.entries.filter((row) => row.catalog === "ai-terms");
  assert.equal(terms.filter((row) => row.source_status === "backlog").length, 77);
  assert.equal(terms.filter((row) => row.source_status === "planned").length, 3);
  const covered = entry("ai-terms", "ai-agent");
  assert.equal(covered.source_status, "covered");
  assert.equal(covered.stage, "COVERED_DO_NOT_REMAKE");
  for (const slug of ["ai-agent-vs-chatbot", "ai-agents-explained-what-they-cost", "always-on-agent-explained"]) {
    assert.ok(covered.details[0].text.includes(slug));
  }
  assert.ok(covered.details[0].text.includes("不再單出一集"));
});

test("details are readable authored text and effective budgets remain separate from historical packages", () => {
  const first = entry("season1", "B01");
  assert.match(first.details.find((detail) => detail.label === "source_package").text, /^# B01 /);
  assert.ok(first.details.find((detail) => detail.label === "effective_inputs").text.includes("製作目標10分鐘"));
  const second = entry("season2", "B28");
  assert.ok(second.details.find((detail) => detail.label === "source_package").text.includes("TEXT_ONLY"));
  assert.ok(second.details.find((detail) => detail.label === "effective_chapters").text.includes("章節預算"));
  const story = entry("brand-stories", "A01").details[0].text;
  assert.ok(story.includes("Bernard Sadow"));
  assert.ok(story.includes("第 6 章"));
  assert.ok(story.includes("查核限制與未採用說法"));
  assert.ok(story.includes("原企劃的發布順序提案（不是正式排程）"));
  assert.ok(!story.trimStart().startsWith("{"));
  assert.ok(!entry("ai-terms", "token").details[0].text.trimStart().startsWith("{"));
});

test("every brand's sensitivity, related article and original writing metadata remain visible", () => {
  const stories = JSON.parse(original("docs/videos/story-plans/brand-stories-100/stories.json")).stories;
  assert.equal(stories.filter((record) => record.sensitivity === "care").length, 23);
  assert.equal(stories.filter((record) => record.related_guide !== null).length, 19);
  const metadata = [
    ["subject", "故事主題"], ["category", "原企劃分類"], ["region", "原企劃地區"],
    ["sensitivity", "原企劃敏感議題標記"], ["related_guide", "相關站內文章"], ["number", "原企劃製作序號"],
  ];
  for (const record of stories) {
    const text = entry("brand-stories", record.id).details.find((detail) => detail.label === "source_record").text;
    for (const [key, heading] of metadata) {
      if (record[key] !== null) assert.ok(text.includes(`${heading}\n${record[key]}`), `${record.id}: ${key}`);
    }
    for (const source of record.sources) assert.ok(text.includes(`原來源類型\n${source.kind}`), record.id);
    if (record.must_verify.some((claim) => claim.core)) assert.ok(text.includes("原企劃標示為核心主張。"), record.id);
  }
  for (const row of catalog.entries) {
    for (const detail of row.details) assert.doesNotMatch(detail.text, /\[object Object\]/, `${row.catalog}/${row.id}/${detail.label}`);
  }
});

test("raw file drift is refused even when parsed JSON is unchanged", () => {
  const relative = "docs/videos/ai-terms/terms.json";
  const changes = new Map([[relative, Buffer.concat([original(relative), Buffer.from("\n")])]]);
  assert.throws(() => buildAdminCatalog({ readSource: readChanged(changes) }), /source hash drift/);
});

test("source records are checked independently of their containing file hash", () => {
  const relative = "docs/videos/ai-terms/terms.json";
  const document = JSON.parse(original(relative));
  document.terms.find((record) => record.id === "token").hook += " drift";
  const modified = Buffer.from(JSON.stringify(document));
  const changes = changePlans((plans) => { plans.source_hashes[relative] = sha(modified); });
  changes.set(relative, modified);
  assert.throws(() => buildAdminCatalog({ readSource: readChanged(changes) }), /source record drift: ai-terms\/token/);
});

test("malformed identities, shortened targets and relabelled source stages are refused", () => {
  const cases = [
    [(plans) => plans.entries.push(plans.entries[0]), /473 plans/],
    [(plans) => { plans.entries[1] = plans.entries[0]; }, /duplicate plan identity/],
    [(plans) => { plans.entries.find((row) => row.catalog === "season3").stage = "REVIEWED_OUTLINE_NOT_MEDIA"; }, /identity\/stage drift/],
    [(plans) => { plans.entries[0].target_seconds = 479; }, /duration drift/],
    [(plans) => { plans.entries[0].source_record_sha256 = "0".repeat(64); }, /source record drift/],
  ];
  for (const [edit, problem] of cases) assert.throws(() => buildAdminCatalog({ readSource: readChanged(changePlans(edit)) }), problem);
});

test("effective inputs, chapters and package paths cannot drift from their authored sources", () => {
  const cases = [
    [(plan) => { plan.backend_inputs.note += " new claim"; }, /effective input drift/],
    [(plan) => { plan.proposed_chapters[0].content += " new claim"; }, /chapter revision drift/],
    [(plan) => { plan.source_package = "docs/videos/so-thats-why/season2/B27.md"; }, /source package path drift/],
  ];
  for (const [edit, problem] of cases) {
    const changes = changePlans((plans) => edit(plans.entries.find((row) => row.catalog === "season2" && row.id === "B26")));
    assert.throws(() => buildAdminCatalog({ readSource: readChanged(changes) }), problem);
  }
});

test("unbound and unsafe paths are refused without reading outside the source tree", () => {
  for (const relative of ["../secret", "docs/videos/../secret", "/docs/videos/test", "docs/videos/a\\b", "docs/videos/a:stream", "docs/videos/a\0b", "docs/videos//test"]) {
    assert.throws(() => requireSourcePath(relative), /inside docs\/videos/);
  }
  const changes = changePlans((plans) => { plans.source_hashes["../../secret"] = "0".repeat(64); });
  assert.throws(() => buildAdminCatalog({ readSource: readChanged(changes) }), /inside docs\/videos/);
  const unbound = changePlans((plans) => { delete plans.source_hashes["docs/videos/ai-terms/terms.json"]; });
  assert.throws(() => buildAdminCatalog({ readSource: readChanged(unbound) }), /source binding missing/);
});

test("a confined reader cannot be pointed at a parent path", (t) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), "admin-catalog-source-"));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  mkdirSync(path.join(directory, "docs", "videos"), { recursive: true });
  writeFileSync(path.join(directory, "docs", "videos", "safe.md"), "authored text");
  const read = sourceReader(directory);
  assert.equal(read("docs/videos/safe.md").toString(), "authored text");
  assert.throws(() => read("docs/videos/../../secret"), /inside docs\/videos/);
});

test("source-directory symlinks cannot expose a file outside docs/videos", (t) => {
  const directory = mkdtempSync(path.join(os.tmpdir(), "admin-catalog-symlink-"));
  t.after(() => rmSync(directory, { recursive: true, force: true }));
  const source = path.join(directory, "docs", "videos");
  const outside = path.join(directory, "outside");
  mkdirSync(source, { recursive: true });
  mkdirSync(outside);
  writeFileSync(path.join(outside, "unrelated.md"), "unrelated file");
  symlinkSync(outside, path.join(source, "alias"), "junction");
  assert.throws(() => sourceReader(directory)("docs/videos/alias/unrelated.md"), /inside docs\/videos/);
  assert.equal(readFileSync(path.join(outside, "unrelated.md"), "utf8"), "unrelated file");
});

test("check CLI is read-only, succeeds for current bytes and refuses unexpected arguments", () => {
  const before = readFileSync(path.join(ROOT, OUTPUT_PATH));
  const command = path.join(ROOT, "tools/video/long-form/admin-catalog.mjs");
  const checked = spawnSync(process.execPath, [command, "check"], { encoding: "utf8" });
  assert.equal(checked.status, 0, checked.stderr);
  assert.match(checked.stdout, /PASS: all 473 source planning entries/);
  assert.deepEqual(readFileSync(path.join(ROOT, OUTPUT_PATH)), before);
  const rejected = spawnSync(process.execPath, [command, "build", "--unexpected"], { encoding: "utf8" });
  assert.equal(rejected.status, 1);
  assert.match(rejected.stderr, /use build \| check/);
  assert.deepEqual(readFileSync(path.join(ROOT, OUTPUT_PATH)), before);
});
