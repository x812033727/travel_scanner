import assert from "node:assert/strict";
import { cpSync, existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { factsChecks } from "../qa/facts.mjs";
import { prepareLesson, PRODUCTION } from "./prepare.mjs";
import { assertReviewBindingCurrent, bindReviews, contentHash, englishContentHash, planReviewBinding, preparedArtifacts } from "./review-bindings.mjs";

const json = (file) => JSON.parse(readFileSync(file, "utf8"));
const save = (file, value) => writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
const name = (day) => `day${String(day).padStart(2, "0")}`;

// Fixtures copy actual independent reports. Tests never mint a successful review
// for invented lesson content; only negative tests alter existing attestations.
function fixture(t, days = [1]) {
  const production = mkdtempSync(path.join(os.tmpdir(), "airport-review-binding-"));
  t.after(() => rmSync(production, { recursive: true, force: true }));
  mkdirSync(path.join(production, "lessons"));
  cpSync(path.join(PRODUCTION, "reviews"), path.join(production, "reviews"), { recursive: true });
  for (const file of ["profile.json", "lexicon.json"]) cpSync(path.join(PRODUCTION, file), path.join(production, file));
  for (const day of days) {
    cpSync(path.join(PRODUCTION, "lessons", `${name(day)}.json`), path.join(production, "lessons", `${name(day)}.json`));
    refresh(production, day);
  }
  return production;
}
function refresh(production, day) {
  const lesson = json(path.join(production, "lessons", `${name(day)}.json`));
  const result = prepareLesson(lesson, json(path.join(production, "profile.json")));
  for (const [file, bytes] of Object.entries(preparedArtifacts(lesson, result))) {
    const dest = path.join(production, name(day), file);
    mkdirSync(path.dirname(dest), { recursive: true });
    writeFileSync(dest, bytes);
  }
}
function mutateJson(production, relative, change) {
  const file = path.join(production, relative), value = json(file);
  change(value); save(file, value);
}
function mutateMarker(production, file, kind, change) {
  const target = path.join(production, "reviews", file), text = readFileSync(target, "utf8");
  const regex = new RegExp(`<!-- airport-${kind}-review-v1 (\\{[^\\n]+\\}) -->`);
  assert.match(text, regex);
  writeFileSync(target, text.replace(regex, (_, raw) => {
    const record = JSON.parse(raw); change(record);
    return `<!-- airport-${kind}-review-v1 ${JSON.stringify(record)} -->`;
  }));
}

test("current real reviews bind only text evidence and official facts accept its table", (t) => {
  const production = fixture(t, [1, 28, 42]);
  assert.deepEqual(bindReviews({ production }), { episodes: 3, mode: "bound_existing_independent_reviews", approvals_created: false, media_created: false, release_ready: false });
  for (const day of [1, 28, 42]) {
    const binding = assertReviewBindingCurrent({ production, day });
    assert.equal(binding.production_approval, false);
    assert.equal(binding.release_ready, false);
    assert.equal(binding.generated_artifacts["video.json"].length, 64);
    const dir = path.join(production, name(day));
    assert.equal(factsChecks({ doc: json(path.join(dir, "video.json")), report: { name: "verify-1.md", markdown: readFileSync(path.join(dir, "verify-1.md"), "utf8") } }).ok, true);
    assert.ok(!readdirSync(dir).some((file) => /approv|\.mp4$|\.wav$|qa\.json/.test(file)));
  }
  const binding28 = json(path.join(production, "day28/review-binding.json"));
  assert.ok(binding28.claims.some((claim) => claim.verdict === "CHANGED" && claim.scene_ids.length));
  assert.equal(bindReviews({ production, check: true }).episodes, 3);
});

test("full-file metadata changes remain usable only with freshly generated artifacts", (t) => {
  const production = fixture(t), file = "lessons/day01.json", original = json(path.join(production, file));
  mutateJson(production, file, (lesson) => { lesson.status = "metadata-only bookkeeping revision"; });
  const changed = json(path.join(production, file));
  assert.equal(contentHash(changed), contentHash(original));
  assert.equal(englishContentHash(changed), englishContentHash(original));
  assert.throws(() => planReviewBinding({ production, day: 1 }), /stale generated artifact line-map/);
  refresh(production, 1);
  assert.equal(planReviewBinding({ production, day: 1 }).binding.editorial_content_sha256, contentHash(original));
});

test("translations, roles, quiz evidence and all teaching fields cannot reuse historical review", (t) => {
  const production = fixture(t), file = path.join(production, "lessons/day01.json"), original = readFileSync(file);
  const mutations = [
    (lesson) => { lesson.A[0].all[3] += " 変更"; },
    (lesson) => { lesson.A[0].speaker = "S"; },
    (lesson) => { lesson.quiz[1].evidence_ids = ["B03", "B04"]; },
    (lesson) => { lesson.guides.goal[0] += " New teaching advice."; },
    (lesson) => { lesson.title_all[4] += " 변경"; },
  ];
  for (const change of mutations) {
    const lesson = JSON.parse(original); change(lesson); save(file, lesson);
    assert.throws(() => bindReviews({ production }), /teaching content changed/);
    assert.equal(existsSync(path.join(production, "day01/verify-1.md")), false);
    writeFileSync(file, original);
  }
});

test("missing, rejected, superseded, ambiguous or wrong-reviewer decisions fail closed", (t) => {
  const production = fixture(t), target = path.join(production, "reviews/verify-day01.md"), original = readFileSync(target, "utf8");
  for (const decision of ["rejected", "superseded", "pending"]) {
    mutateMarker(production, "verify-day01.md", "editorial", (record) => { record.decision = decision; });
    assert.throws(() => planReviewBinding({ production, day: 1 }), /editorial decision or reviewer/);
    writeFileSync(target, original);
  }
  mutateMarker(production, "verify-day01.md", "editorial", (record) => { record.reviewer = "lesson_author"; });
  assert.throws(() => planReviewBinding({ production, day: 1 }), /editorial decision or reviewer/);
  writeFileSync(target, original.replace(/<!-- airport-editorial-review-v1[^\n]+ -->/, ""));
  assert.throws(() => planReviewBinding({ production, day: 1 }), /decision is missing or ambiguous/);
  writeFileSync(target, original + "\n" + original.match(/<!-- airport-editorial-review-v1[^\n]+ -->/)[0]);
  assert.throws(() => planReviewBinding({ production, day: 1 }), /decision is missing or ambiguous/);
  writeFileSync(target, original);
  mutateMarker(production, "verify-day01.md", "editorial", (record) => { record.content_hashes["1"] = "0".repeat(64); });
  assert.throws(() => planReviewBinding({ production, day: 1 }), /attestation differs/);
});

test("separately recorded historical PASS cannot silently become rejected or superseded", (t) => {
  const production = fixture(t, [2]);
  assert.equal(planReviewBinding({ production, day: 2 }).day, 2);
  const target = path.join(production, "reviews/verify-02-21.md"), original = readFileSync(target, "utf8");
  for (const text of [original.replace("Result: the revised text passes", "Result: REJECTED. The revised text previously passed"), original + "\nSuperseded by a new review.\n"]) {
    writeFileSync(target, text);
    assert.throws(() => planReviewBinding({ production, day: 2 }), /PASS report differs/);
  }
});

test("factual ledger identity, current verdict, content snapshot and retrieval evidence are checked", (t) => {
  const production = fixture(t, [28]), relative = "reviews/claims-review.json", target = path.join(production, relative), original = readFileSync(target);
  const mutations = [
    [(facts) => { facts.reviewer = "different_reviewer"; }, /identity or schema/],
    [(facts) => { facts.schema_version = 2; }, /identity or schema/],
    [(facts) => { facts.series = "another_series"; }, /identity or schema/],
    [(facts) => { facts.review_type = "author_self_review"; }, /identity or schema/],
    [(facts) => { facts.status = "superseded"; }, /unresolved claims/],
    [(facts) => { facts.remaining_factual_corrections = 1; }, /unresolved claims/],
    [(facts) => { facts.production_source_hashes.find((row) => row.day === 28).reviewed_english_content_sha256 = "0".repeat(64); }, /English content changed/],
    [(facts) => { facts.claims.find((claim) => claim.days.includes(28)).verdict = "NOT FOUND"; }, /unresolved reviewed claims/],
    [(facts) => { const claim = facts.claims.find((c) => c.days.includes(28) && c.sources.length); facts.sources.find((s) => s.id === claim.sources[0]).http_status = 403; }, /lacks retrieved official-source/],
    [(facts) => { const claim = facts.claims.find((c) => c.days.includes(28) && c.sources.length); facts.sources.find((s) => s.id === claim.sources[0]).response_sha256 = "missing"; }, /lacks retrieved official-source/],
  ];
  for (const [change, expected] of mutations) {
    const facts = JSON.parse(original); change(facts); save(target, facts);
    assert.throws(() => planReviewBinding({ production, day: 28 }), expected);
    writeFileSync(target, original);
  }
});

test("claims and source metadata cannot drift even when generated artifacts are fresh", (t) => {
  const production = fixture(t, [28]), target = path.join(production, "lessons/day28.json"), original = readFileSync(target);
  for (const [change, expected] of [
    [(lesson) => { lesson.claims[0].text += " Guaranteed everywhere."; }, /claim text, verdict or source URLs/],
    [(lesson) => { lesson.sources[0].checked_on = "2099-01-01"; }, /source metadata/],
    [(lesson) => { lesson.claims.find((claim) => claim.source_urls.length).source_urls[0] = "https://example.com/unreviewed"; }, /claim text, verdict or source URLs/],
  ]) {
    const lesson = JSON.parse(original); change(lesson); save(target, lesson); refresh(production, 28);
    assert.throws(() => planReviewBinding({ production, day: 28 }), expected);
    writeFileSync(target, original);
  }
});

test("every generated artifact must match current preparation bytes", (t) => {
  const production = fixture(t), plan = planReviewBinding({ production, day: 1 });
  for (const file of Object.keys(plan.binding.generated_artifacts)) {
    const target = path.join(production, "day01", file), original = readFileSync(target);
    writeFileSync(target, Buffer.concat([original, Buffer.from("\n")]));
    assert.throws(() => planReviewBinding({ production, day: 1 }), /stale generated artifact/);
    writeFileSync(target, original);
  }
});

test("shared instructions and thumbnail words require the recorded text review", (t) => {
  const production = fixture(t), target = path.join(production, "reviews/verify-shared-instructions.md"), original = readFileSync(target);
  for (const [change, expected] of [
    [(record) => { record.decision = "rejected"; }, /binding record is incomplete/],
    [(record) => { record.reviewer = "generator_author"; }, /binding record is incomplete/],
    [(record) => { record.shared_instructions_sha256 = "0".repeat(64); }, /shared teaching instructions changed/],
    [(record) => { record.thumbnail_headlines["1"] = "Unreviewed words"; }, /thumbnail wording changed/],
  ]) {
    mutateMarker(production, "verify-shared-instructions.md", "shared", change);
    assert.throws(() => planReviewBinding({ production, day: 1 }), expected);
    writeFileSync(target, original);
  }
});

test("batch preflight writes nothing when one selected episode is stale", (t) => {
  const production = fixture(t, [1, 2]);
  mutateJson(production, "day02/video.json", (doc) => { doc.youtube.title += " stale version"; });
  assert.throws(() => bindReviews({ production }), /day02: stale generated artifact/);
  for (const day of [1, 2]) for (const file of ["verify-1.md", "review-binding.json"]) assert.equal(existsSync(path.join(production, name(day), file)), false);
});

test("existing bindings become stale when their evidence, profile or lexicon changes", (t) => {
  const production = fixture(t);
  bindReviews({ production });
  for (const relative of ["reviews/verify-day01.md", "reviews/claims-review.md", "lexicon.json", "profile.json"]) {
    const target = path.join(production, relative), original = readFileSync(target);
    writeFileSync(target, Buffer.concat([original, Buffer.from("\n")]));
    assert.throws(() => assertReviewBindingCurrent({ production, day: 1 }), /review-binding.json is missing or stale/);
    writeFileSync(target, original);
  }
  assert.equal(assertReviewBindingCurrent({ production, day: 1 }).day, 1);
});
