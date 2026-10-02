import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";
import { buildPlans, CATALOG_COUNTS, chapterBudget, DIRECTORY, findPlan, recordHash, reviseDurationText, reviseLongDescription, ROOT, validatePlans, validatePolicy } from "./plans.mjs";

const json = (relative) => JSON.parse(readFileSync(path.join(ROOT, relative), "utf8"));

test("all five source catalogs are complete and historical statuses stay intact", () => {
  const plans = buildPlans();
  assert.equal(plans.totals.entries, 473);
  assert.deepEqual(plans.totals.catalogs, CATALOG_COUNTS);
  assert.equal(plans.totals.covered_ai_terms, 1);
  assert.equal(plans.entries.filter((row) => row.catalog === "brand-stories").every((row) => row.target_seconds === 780), true);
  assert.equal(plans.entries.filter((row) => row.catalog === "ai-terms").every((row) => JSON.stringify(row.target_range_seconds) === "[540,660]"), true);
  const covered = findPlan(plans, "ai-terms", "ai-agent");
  assert.equal(covered.source_status, "covered");
  assert.equal(covered.stage, "COVERED_DO_NOT_REMAKE");
  assert.throws(() => findPlan(plans, "ai-terms", "ai-agent", { forProduction: true }), /covered/);
  assert.throws(() => findPlan(plans, "season2", "B30"), /unknown/);
  assert.equal(plans.entries.filter((row) => row.catalog === "season3").every((row) => row.stage === "CHECKED_CANDIDATE_REQUIRES_OUTLINE" && !row.backend_inputs), true);
});

test("every effective season-2 outline is ten minutes without changing content or Shorts", () => {
  const plans = buildPlans();
  const rows = plans.entries.filter((row) => row.catalog === "season2");
  for (const row of rows) {
    assert.equal(row.proposed_chapters.length, 6, row.id);
    for (const chapter of row.proposed_chapters) assert.doesNotMatch(chapter.heading, /\d{2}:\d{2}/, row.id);
    assert.equal(row.proposed_chapters.reduce((sum, chapter) => sum + chapter.proposed_seconds, 0), 600, row.id);
    assert.equal(row.proposed_chapters[0].start_seconds, 0, row.id);
    const last = row.proposed_chapters.at(-1);
    assert.equal(last.start_seconds + last.proposed_seconds, 600, row.id);
    const batch = /reviews\/([^/]+)\//.exec(row.source_review)[1];
    const original = json(`docs/videos/so-thats-why/season2/${batch}-packaging.json`).episodes.find((source) => source.id === row.id);
    assert.equal(row.backend_inputs.premise, original.backend_inputs.premise, row.id);
    assert.equal(row.shorts_sha256, recordHash(original.shorts), row.id);
    assert.equal(original.target_seconds, 480, "the original fact-review source stays historical");
    assert.equal(row.minimum_content_seconds, 480, row.id);
    assert.equal(row.minimum_final_seconds, 480, row.id);
    assert.equal(row.backend_inputs.target_minutes, 10, row.id);
    assert.ok(row.backend_inputs.note.length <= 2000, row.id);
  }
});

test("first-season copyable requests supersede every original eight-minute note", () => {
  for (const row of buildPlans().entries.filter((entry) => entry.catalog === "season1")) {
    assert.equal(row.backend_inputs.target_minutes, 10, row.id);
    assert.match(row.backend_inputs.note, /製作目標(?:10分鐘|600秒)/, row.id);
    assert.doesNotMatch(row.backend_inputs.note, /風格：扁平插畫解說，(?:長度 )?8 分鐘/, row.id);
    assert.ok(row.backend_inputs.premise.length <= 4000 && row.backend_inputs.note.length <= 2000, row.id);
  }
});

test("a missing catalog, stale source, low duration or fake measured acceptance fails", () => {
  const expected = buildPlans();
  const shipped = json(`${DIRECTORY}/plans.json`);
  assert.deepEqual(validatePlans(shipped, expected), []);
  for (const mutate of [
    (value) => value.entries.splice(0, 1),
    (value) => { value.entries[0].source_record_sha256 = "0".repeat(64); },
    (value) => { value.entries[0].target_seconds = 479; },
    (value) => { value.entries.find((row) => row.catalog === "season2").proposed_chapters[1].proposed_seconds -= 1; },
    (value) => { value.entries.find((row) => row.stage === "COVERED_DO_NOT_REMAKE").stage = "READY"; },
    (value) => { value.actual_duration_verified = true; },
  ]) {
    const changed = structuredClone(shipped);
    mutate(changed);
    assert.ok(validatePlans(changed, expected).length);
  }
  const policy = json(`${DIRECTORY}/policy.json`);
  for (const mutate of [
    (value) => { value.minimum_content_seconds = 479; },
    (value) => { value.catalogs.season1.target_seconds = 480; },
    (value) => { value.catalogs["brand-stories"].target_seconds = 600; },
    (value) => { delete value.catalogs.season3; },
    (value) => { value.shorts = "LONG_FORM"; },
  ]) {
    const changed = structuredClone(policy);
    mutate(changed);
    assert.ok(validatePolicy(changed).length);
  }
});

test("revision changes duration instructions while retaining factual numbers and URLs", () => {
  assert.equal(reviseDurationText("目標480秒，PDF第480頁，https://source.test/480"), "製作目標600秒，PDF第480頁，https://source.test/480");
  assert.equal(reviseDurationText("六章480秒、480秒六章、長片480秒；正文最低480秒。"), "六章600秒、600秒六章、長片600秒；正文最低480秒。");
  assert.equal(reviseLongDescription("Six chapters totaling 480 seconds are an outline. https://source.test/480"), "Six chapters totaling 600 seconds are an outline. https://source.test/480");
  assert.equal(reviseLongDescription("The measured experiment took 480 seconds."), "The measured experiment took 480 seconds.");
  assert.equal(reviseLongDescription("六章480秒企劃，並非完整逐字稿。"), "六章600秒企劃，並非完整逐字稿。");
  const revised = chapterBudget([30, 90, 105, 105, 105, 45]);
  assert.equal(revised[0], 30);
  assert.equal(revised[5], 45);
  assert.equal(revised.reduce((sum, seconds) => sum + seconds, 0), 600);
  assert.ok(revised.slice(1, 5).every((seconds, index) => seconds > [90, 105, 105, 105][index]));
  assert.throws(() => chapterBudget([30, 90], 600), /six positive/);
  assert.throws(() => chapterBudget([30, 90, 105, 105, 105, 45], 480), /at least 600/);
});
