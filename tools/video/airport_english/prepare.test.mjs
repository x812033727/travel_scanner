import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";

import { checkCues, LOCALE_RULES, measure, wrapCue } from "../core/captions.mjs";
import { eachLine, textHash, validateVideo } from "../core/schema.mjs";
import { estimateTimeline, speechHash } from "../core/timeline.mjs";
import { planRequests } from "../tts/requests.mjs";
import { factsChecks } from "../qa/facts.mjs";
import { outlineOptions } from "../review/sync.mjs";
import { assertStagedReviewBinding, englishCardText, lessonProblems, localLexicon, LOCALES, prepareLesson, prepareSeries, PRODUCTION, runStage, stableId, stageProject } from "./prepare.mjs";

const profile = JSON.parse(readFileSync(path.join(PRODUCTION, "profile.json"), "utf8"));
const all = (en) => [en, "請確認正確的登機門，並聽取現場工作人員的最新指示。", "请确认正确的登机口，并听取现场工作人员的最新指示。", "正しい搭乗口を確認し、現地の係員の最新の案内を聞いてください。", "올바른 탑승구를 확인하고 현장 직원의 최신 안내를 들어 주세요."];
function fixture() {
  const A = [{ id: "A01", speaker: "T", text: "Which gate should I use?", all: all("Which gate should I use?") }, { id: "A02", speaker: "S", text: "Please go to gate twenty.", all: all("Please go to gate twenty.") }];
  const B = [{ id: "B01", speaker: "T", text: "Has our gate changed?", all: all("Has our gate changed?") }, { id: "B02", speaker: "S", text: "Yes. Please go to gate thirty-two.", all: all("Yes. Please go to gate thirty-two.") }];
  return { day: 59, title_all: all("A new gate"), A, B, guides: Object.fromEntries(["hook", "goal", "recap", "comment", "subscribe"].map((key) => [key, all(key === "subscribe" ? "Subscribe to practice another travel conversation tomorrow." : "Listen for the new gate, then confirm the number before moving.")])), quiz: [1, 2, 3].map(() => ({ question: "What is the new gate?", all: all("What is the new gate?"), choices: ["Twenty", "Thirty-two", "Four"], choices_all: [all("Twenty"), all("Thirty-two"), all("Four")], correct: 1, answer: "Thirty-two", answer_all: all("The correct answer is B. Thirty-two."), evidence_ids: ["B01", "B02"] })) };
}

test("quiz evidence is explicit and cannot fall back to first conversation or matching words", () => {
  const lesson = fixture();
  delete lesson.quiz[1].evidence_ids;
  assert.match(lessonProblems(lesson).join("\n"), /quiz 2: explicit/);
  assert.throws(() => prepareLesson(lesson, profile), /evidence_ids/);
  lesson.quiz[1].evidence_ids = ["Z01"];
  assert.throws(() => prepareLesson(lesson, profile), /evidence_ids/);
  lesson.quiz[1].evidence_ids = ["B02", "B02"];
  assert.throws(() => prepareLesson(lesson, profile), /evidence_ids/);
});

test("official outline review reads two complete options with the current lesson's spoken hook", () => {
  const lesson = fixture();
  lesson.guides.hook[0] = "Your gate has changed. Which number should you listen for?";
  const { brief, entries } = prepareLesson(lesson, profile);
  const options = outlineOptions(brief);
  assert.deepEqual(options.map((option) => option.key), ["A", "B"]);
  assert.ok(options.every((option) => option.title && option.summary));
  assert.ok(options.every((option) => option.hook === lesson.guides.hook[0]));
  assert.ok(entries.some((entry) => entry.all[0] === options[0].hook), "the proposed hook is actually spoken in the current script");
  assert.notEqual(options[0].summary, options[1].summary);
  assert.match(options[0].summary, /每段對話聽懂後立即跟讀/);
  assert.match(options[1].summary, /先完成兩段對話辨識，再集中跟讀/);
  assert.match(brief, /目前產生的劇本採此順序/);
  assert.match(brief, /若選 B，須先調整劇本/);
});

test("the brief works through the reviewed quiz with the actual replay, pause, and answer order", () => {
  const lesson = fixture(), quiz = lesson.quiz[0];
  const { brief, entries, doc } = prepareLesson(lesson, profile);
  const example = brief.split("### 可跟著作答的實例：本集第 1 題\n")[1].split("\n## 章節大綱")[0];
  const actual = entries.filter((entry) => entry.semantic_key.startsWith("quiz-1-") || entry.semantic_key === "coach-choose-1");
  assert.deepEqual(actual.map((entry) => entry.semantic_key), ["quiz-1-question", "quiz-1-choice-0", "quiz-1-choice-1", "quiz-1-choice-2", ...quiz.evidence_ids.map((id) => `quiz-1-evidence-${id}`), "coach-choose-1", "quiz-1-answer"]);
  let previousPosition = -1;
  for (const entry of actual) {
    const position = example.indexOf(entry.all[0]);
    assert.ok(position > previousPosition, `${entry.semantic_key} must appear in actual playback order`);
    previousPosition = position;
  }
  for (const id of quiz.evidence_ids) assert.ok(example.includes(`${id} /`));
  assert.ok(!example.includes(lesson.A[1].text), "the example cannot silently replace designated evidence with another conversation");
  const choose = actual.find((entry) => entry.semantic_key === "coach-choose-1");
  assert.equal(doc.scenes.find((scene) => scene.lines[0].id === choose.id).lines[0].pause_after_ms, 4000);
  assert.match(example, /語句後停頓 4 秒/);
  assert.ok(example.includes(`公布正解：B. ${quiz.answer}`));
  assert.ok(example.includes(`既有答案口播（逐字）：${quiz.answer_all[0]}`));
  assert.equal(outlineOptions(brief).length, 2, "the concrete example must not hide the official outline options");
});

test("current source answer, five translations, and episode guides are required", () => {
  const lesson = fixture();
  lesson.A[0].all[0] = "An older line";
  lesson.quiz[0].answer = "Twenty";
  lesson.guides.recap = ["Incomplete"];
  assert.match(lessonProblems(lesson).join("\n"), /A01.*English mismatch/);
  assert.match(lessonProblems(lesson).join("\n"), /answer differs/);
  assert.match(lessonProblems(lesson).join("\n"), /guides.recap/);
});

test("practice pauses are optional and accept only integer milliseconds from 4000 through 5000", () => {
  for (const invalid of [0, 3999, 5001, 4500.5, "4500", null, undefined]) {
    const lesson = fixture();
    lesson.A[0].practice_pause_ms = invalid;
    assert.match(lessonProblems(lesson).join("\n"), /A01 practice_pause_ms must be an integer from 4000 through 5000/);
    assert.throws(() => prepareLesson(lesson, profile), /practice_pause_ms/);
  }
  const implicit = fixture(), explicit = fixture();
  for (const turn of [...explicit.A, ...explicit.B]) turn.practice_pause_ms = 4000;
  assert.equal(JSON.stringify(prepareLesson(implicit, profile)), JSON.stringify(prepareLesson(explicit, profile)), "an explicit default leaves all generated output bytes unchanged");
});

test("a reviewed turn's response interval changes only its practice pass and the actual pause total", () => {
  const lesson = fixture(), before = prepareLesson(lesson, profile);
  lesson.A[0].practice_pause_ms = 4750;
  lesson.B[1].practice_pause_ms = 5000;
  const after = prepareLesson(lesson, profile);
  const overrides = new Map([[stableId(lesson.day, "practice-A01"), 4750], [stableId(lesson.day, "practice-B02"), 5000]]);
  const oldLines = new Map([...eachLine(before.doc)].map(({ line }) => [line.id, line]));
  for (const { line } of eachLine(after.doc)) {
    assert.deepEqual(line, { ...oldLines.get(line.id), ...(overrides.has(line.id) ? { pause_after_ms: overrides.get(line.id) } : {}) });
  }
  assert.ok(after.entries.some((entry) => entry.semantic_key === "quiz-1-evidence-B02"), "the fixture exercises protected quiz evidence as well as the ordinary listening passes");
  const responseIds = new Set(after.entries.filter((entry) => /^(practice-|coach-choose-)/.test(entry.semantic_key)).map((entry) => entry.id));
  const total = [...eachLine(after.doc)].filter(({ line }) => responseIds.has(line.id)).reduce((sum, { line }) => sum + line.pause_after_ms, 0) / 1000;
  assert.equal(total, 29.75);
  assert.equal(after.duration.fixed_practice_pause_seconds, total);
  assert.equal(after.duration.fixed_practice_pause_seconds - before.duration.fixed_practice_pause_seconds, 1.75);
});

test("practice pacing preserves TTS request and take bytes but invalidates timing and speech hashes", () => {
  const lesson = fixture(), before = prepareLesson(lesson, profile);
  lesson.B[1].practice_pause_ms = 5000;
  const after = prepareLesson(lesson, profile), lexicon = localLexicon([before.doc]);
  assert.equal(JSON.stringify(planRequests(after.doc, lexicon)), JSON.stringify(planRequests(before.doc, lexicon)), "identical request bodies, request keys and individual take keys reuse the original synthesis");
  const oldTimeline = estimateTimeline(before.doc), newTimeline = estimateTimeline(after.doc);
  assert.deepEqual(newTimeline.lines.map(({ id, audio_samples }) => [id, audio_samples]), oldTimeline.lines.map(({ id, audio_samples }) => [id, audio_samples]));
  assert.equal(newTimeline.total_frames - oldTimeline.total_frames, 30);
  assert.notEqual(speechHash(after.doc, lexicon), speechHash(before.doc, lexicon));
  assert.notEqual(after.teachingAudio.source_script_sha256, before.teachingAudio.source_script_sha256);
  assert.equal(after.brief, before.brief);
  assert.deepEqual(after.translations, before.translations);
});

test("a spoken wrong answer or an unknown speaker cannot enter production", () => {
  const wrong = fixture();
  wrong.quiz[0].answer_all[0] = "The answer is A: Twenty.";
  wrong.A[0].speaker = "UNKNOWN";
  assert.match(lessonProblems(wrong).join("\n"), /spoken English answer/);
  assert.match(lessonProblems(wrong).join("\n"), /speaker must/);
  wrong.quiz[0].answer_all[0] = "The answer is B: Four.";
  assert.match(lessonProblems(wrong).join("\n"), /spoken English answer/, "the letter alone is not enough");
  const range = fixture();
  range.quiz[0].answer = range.quiz[0].choices[1] = range.quiz[0].choices_all[1][0] = "30–34";
  range.quiz[0].answer_all[0] = "The answer is B: thirty to thirty-four. Confirm the range.";
  assert.deepEqual(lessonProblems(range), []);
});

test("a subsequently rejected travel claim stays connected to the actual official facts gate", () => {
  const lesson = fixture();
  lesson.claims = [{ id: "AE-C11", text: "Follow the cabin crew's instructions.", source_urls: ["https://www.faa.gov/"], status: "CONFIRMED" }, { id: "AE-C01", text: "Fictional gates.", source_urls: [], status: "fictional_scenario_not_external_fact" }];
  const { doc } = prepareLesson(lesson, profile);
  const cited = doc.scenes.filter((scene) => scene.claims?.includes("AE-C11"));
  assert.ok(cited.length > 0);
  assert.ok(!doc.scenes.some((scene) => scene.claims?.includes("AE-C01")));
  const verdict = factsChecks({ doc, report: { name: "verify-1.md", markdown: "| AE-C11 | Follow instructions | NOT FOUND |" } });
  assert.equal(verdict.ok, false);
  assert.match(verdict.detail, /still cites it/);
});

test("official schema preserves exact replay takes, English audio, and translated CC separately", () => {
  const lesson = fixture();
  const result = prepareLesson(lesson, profile);
  assert.deepEqual(validateVideo(result.doc), []);
  const entries = new Map(result.entries.map((entry) => [entry.id, entry]));
  const evidence = result.entries.filter((entry) => entry.semantic_key.startsWith("quiz-2-evidence"));
  assert.deepEqual(evidence.map((entry) => entry.source_turn_id), ["B01", "B02"]);
  const original = result.entries.find((entry) => entry.semantic_key === "first-B02");
  assert.equal(evidence[1].source_take_id, original.id);
  const requests = planRequests(result.doc, localLexicon([result.doc]));
  assert.equal(requests.find((request) => request.lines[0].id === evidence[1].id).audio_ref, original.id);
  for (const locale of LOCALES.slice(1)) {
    const audio = result.teachingAudio.locales[locale].lines.find((line) => line.id === evidence[1].id);
    assert.equal(audio.text, lesson.B[1].text);
    assert.equal(audio.speech_locale, "en");
    assert.equal(audio.reuse_source_take, original.id);
    assert.notEqual(audio.cc_text, audio.text);
    for (const { line } of eachLine(result.doc)) assert.equal(result.translations[locale].lines[line.id].source_hash, textHash(line.text));
  }
  assert.equal(result.teachingAudio.generic_dub_allowed, false);
  assert.equal(result.duration.measured_total_seconds, null);
  assert.equal(result.duration.release_ready, false);
  assert.equal(entries.size, result.entries.length);
});

test("inserting a new source turn does not renumber existing audio or caption identities", () => {
  const lesson = fixture(), first = prepareLesson(lesson, profile);
  lesson.A.splice(1, 0, { id: "A03", speaker: "S", text: "Let me check the latest information.", all: all("Let me check the latest information.") });
  const second = prepareLesson(lesson, profile);
  const known = new Map(second.entries.map((entry) => [entry.semantic_key, entry.id]));
  for (const entry of first.entries) assert.equal(known.get(entry.semantic_key), entry.id);
  assert.equal(stableId(59, "first-B02"), first.entries.find((entry) => entry.semantic_key === "first-B02").id);
});

test("caption preparation uses official locale wrapping without inventing cue timing", () => {
  const result = prepareLesson(fixture(), profile);
  assert.equal(result.captionPlan.status, "text_segmentation_only_not_timed_captions");
  for (const line of result.captionPlan.lines) for (const [locale, pieces] of Object.entries(line.by_locale)) {
    const rules = LOCALE_RULES[locale];
    for (const piece of pieces) {
      const wrapped = wrapCue(piece, rules);
      assert.ok(wrapped.split("\n").length <= rules.maxLines);
      for (const row of wrapped.split("\n")) assert.ok(measure(row, rules) <= rules.maxChars, `${locale}: ${row}`);
      const problems = checkCues([{ start_ms: 0, end_ms: 12000, text: wrapped }], locale);
      assert.deepEqual(problems, []);
    }
  }
});

test("English cards keep the complete spoken words in at most three explicit rows", () => {
  for (const text of ["Which gate?", "Go straight past the pharmacy, then turn right.", "Now listen to both conversations at a natural pace. For a challenge, switch off translated captions and focus on the voices.", "The answer is B: thirty to thirty-four. Confirm the range before proceeding."]) {
    const shown = englishCardText(text);
    assert.ok(shown.split("\n").length <= 3);
    assert.equal(shown.replace(/\s+/g, " ").replace(/\u2011/g, "-"), text);
    assert.ok(shown.split("\n").every((row) => !row.includes(" ")), "rows cannot wrap at ordinary spaces");
  }
});

test("adapter refuses generic dubbing, fake approvals, uploading, and media inside source control", async () => {
  for (const command of ["dub", "approve", "youtube-sync", "auto", "import"]) await assert.rejects(runStage({ command }), /not allowed/);
  assert.throws(() => stageProject({ projectRoot: PRODUCTION, mediaRoot: "/tmp/airport-media" }), /outside the repository/);
  const tmp = mkdtempSync(path.join(os.tmpdir(), "airport-staging-"));
  try {
    assert.throws(() => stageProject({ projectRoot: tmp, mediaRoot: path.join(tmp, "media") }), /separate directories/);
    assert.throws(() => stageProject({ projectRoot: path.join(tmp, "project"), mediaRoot: tmp }), /separate directories/);
  }
  finally { rmSync(tmp, { recursive: true, force: true }); }
});

test("restaging replaces the source snapshot and removes stale reviews and translations", () => {
  const tmp = mkdtempSync(path.join(os.tmpdir(), "airport-snapshot-"));
  try {
    const production = path.join(tmp, "production"), projectRoot = path.join(tmp, "project"), mediaRoot = path.join(tmp, "media");
    const own = path.join(production, "day59");
    mkdirSync(own, { recursive: true });
    writeFileSync(path.join(production, "profile.json"), JSON.stringify(profile));
    writeFileSync(path.join(production, "lexicon.json"), JSON.stringify({ schema_version: 1, terms: {} }));
    writeFileSync(path.join(own, "video.json"), JSON.stringify(prepareLesson(fixture(), profile).doc));
    writeFileSync(path.join(own, "verify-1.md"), "Current source review");
    mkdirSync(path.join(production, "reviews"));
    writeFileSync(path.join(production, "reviews/independent.md"), "Independent review evidence");
    stageProject({ production, projectRoot, mediaRoot });
    const staged = path.join(projectRoot, "docs/videos/airport-english-day59");
    mkdirSync(path.join(staged, "i18n"));
    writeFileSync(path.join(staged, "verify-9.md"), "Obsolete report");
    writeFileSync(path.join(staged, "i18n/ja.json"), "{}");
    stageProject({ production, projectRoot, mediaRoot });
    assert.equal(existsSync(path.join(staged, "verify-9.md")), false);
    assert.equal(existsSync(path.join(staged, "i18n/ja.json")), false);
    assert.equal(readFileSync(path.join(staged, "verify-1.md"), "utf8"), "Current source review");
    assert.equal(readFileSync(path.join(staged, "../reviews/independent.md"), "utf8"), "Independent review evidence");
  } finally { rmSync(tmp, { recursive: true, force: true }); }
});

test("a partial refresh preserves pronunciation entries needed by another episode", () => {
  const tmp = mkdtempSync(path.join(os.tmpdir(), "airport-partial-"));
  try {
    const lessonsDir = path.join(tmp, "lessons"), out = path.join(tmp, "out");
    mkdirSync(lessonsDir);
    const first = fixture(); first.day = 58;
    first.A[0].text = first.A[0].all[0] = "Where is the QZX counter?";
    writeFileSync(path.join(lessonsDir, "day58.json"), JSON.stringify(first));
    writeFileSync(path.join(lessonsDir, "day59.json"), JSON.stringify(fixture()));
    prepareSeries({ lessonsDir, out, profile });
    prepareSeries({ lessonsDir, out, profile, days: [59] });
    assert.equal(JSON.parse(readFileSync(path.join(out, "lexicon.json"))).terms.QZX, "Q Z X");
  } finally { rmSync(tmp, { recursive: true, force: true }); }
});

test("TTS staging guard checks actual script, source and review evidence bytes", () => {
  const tmp = mkdtempSync(path.join(os.tmpdir(), "airport-bound-stage-"));
  const digest = (value) => createHash("sha256").update(value).digest("hex");
  try {
    const production = path.join(tmp, "production"), projectRoot = path.join(tmp, "project"), mediaRoot = path.join(tmp, "media");
    const files = { "day59/video.json": JSON.stringify(prepareLesson(fixture(), profile).doc), "profile.json": JSON.stringify(profile), "lexicon.json": JSON.stringify({ schema_version: 1, terms: {} }), "lessons/day59.json": JSON.stringify(fixture()), "reviews/evidence.md": "Test integrity evidence, not an approval" };
    const binding = { generated_artifacts: { "video.json": digest(files["day59/video.json"]) }, lesson_sha256: digest(files["lessons/day59.json"]), profile_sha256: digest(files["profile.json"]), lexicon_sha256: digest(files["lexicon.json"]), reviews: [{ path: "../reviews/evidence.md", sha256: digest(files["reviews/evidence.md"]) }] };
    files["day59/review-binding.json"] = JSON.stringify(binding);
    files["day59/verify-1.md"] = "Test source snapshot";
    for (const [file, value] of Object.entries(files)) { mkdirSync(path.dirname(path.join(production, file)), { recursive: true }); writeFileSync(path.join(production, file), value); }
    stageProject({ production, projectRoot, mediaRoot });
    assert.doesNotThrow(() => assertStagedReviewBinding({ production, day: 59, projectRoot, binding }));
    writeFileSync(path.join(projectRoot, "docs/videos/airport-english-day59/video.json"), "{}");
    assert.throws(() => assertStagedReviewBinding({ production, day: 59, projectRoot, binding }), /staged video.json/);
    stageProject({ production, projectRoot, mediaRoot });
    writeFileSync(path.join(projectRoot, "docs/videos/reviews/evidence.md"), "An obsolete review");
    assert.throws(() => assertStagedReviewBinding({ production, day: 59, projectRoot, binding }), /staged .*reviews\/evidence.md/);
  } finally { rmSync(tmp, { recursive: true, force: true }); }
});
