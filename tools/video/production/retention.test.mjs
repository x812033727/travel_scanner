import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import path from "node:path";
import test from "node:test";

import { LOCALIZATION_RETENTION_FILE, localizationPlan, localizationPlanProblems, writeLocalizationRetention } from "./retention.mjs";

const production = () => ({
  source_binding: { source_sha256: "a".repeat(64) },
  profile: { phases: { primary: { locale: "zh-TW" }, localization: { locales: ["ja", "ko", "en"], start_after: "approved-chinese-final", automatic_generation_now: false, readiness: "planned-not-implemented-for-drama" } } },
});

test("the later-language promise is bound to its approved source and delivery profile", () => {
  const source = production();
  const plan = localizationPlan(source);
  assert.deepEqual(localizationPlanProblems(plan), []);
  assert.equal(plan.source_sha256, source.source_binding.source_sha256);
  assert.equal(plan.profile_sha256, createHash("sha256").update(JSON.stringify(source.profile)).digest("hex"));
  assert.deepEqual(plan.planned_locales, ["ja", "ko", "en"]);
  assert.equal(plan.retain_source_media, true);
  assert.equal(localizationPlan(null), null);
  assert.equal(localizationPlan({ profile: {} }), null);
  assert.throws(() => localizationPlan({ profile: source.profile }), /source_sha256/);
});

test("invalid and claimed-completed markers cannot authorize cleanup", () => {
  const plan = localizationPlan(production());
  for (const changed of [null, { ...plan, retain_source_media: false }, { ...plan, status: "completed" }, { ...plan, planned_locales: [] }, { ...plan, planned_locales: ["en", "en"] }, { ...plan, source_sha256: "old" }, { ...plan, release: true }]) {
    assert.ok(localizationPlanProblems(changed).length);
  }
});

test("the workdir keeps an append-only promise when a script is rewritten without production context", (t) => {
  const dir = mkdtempSync(path.join(tmpdir(), "video-localization-retention-"));
  t.after(() => rmSync(dir, { recursive: true, force: true }));
  const args = { slug: "story-e001", seriesSlug: "story", production: production() };
  const first = writeLocalizationRetention(dir, args);
  assert.equal(first.plans.length, 1);
  const file = path.join(dir, LOCALIZATION_RETENTION_FILE);
  const before = readFileSync(file, "utf8");
  assert.deepEqual(writeLocalizationRetention(dir, args), first);
  assert.equal(readFileSync(file, "utf8"), before);
  assert.equal(writeLocalizationRetention(dir, { ...args, production: null }), null);
  assert.equal(readFileSync(file, "utf8"), before);
  const changed = production();
  changed.source_binding.source_sha256 = "b".repeat(64);
  const second = writeLocalizationRetention(dir, { ...args, production: changed });
  assert.equal(second.plans.length, 2);
  assert.deepEqual(second.plans[0], first.plans[0]);
  assert.throws(() => writeLocalizationRetention(dir, { ...args, slug: "different" }), /invalid/);
});
