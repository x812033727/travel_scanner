import assert from "node:assert/strict";
import { existsSync, mkdirSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { compilationDocument, estimatedCompilationTimeline } from "../core/compilation.mjs";
import { COMPILATION_REVIEW_FILE, reviewHash } from "../core/compilation-review.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { readJson } from "../core/paths.mjs";
import { LOCALES } from "../core/schema.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { advanceCompilation, planMetadata, translateMetadata } from "./compilation.mjs";

const SERIES = "old-city";
const EPISODES = Array.from({ length: 40 }, (_, index) => ({
  slug: `${SERIES}-e${String(index + 1).padStart(3, "0")}`,
  number: index + 1,
  title: index === 19 ? "她還活著" : `舊城第${index + 1}夜`,
  logline: "主角尋找失蹤的人。",
  recap: index === 19 ? "失蹤者仍然活著，真相在第二十集揭露。" : "主角追查線索。",
}));
const REVEAL = EPISODES[19].slug;
const SAFE_CHAPTER = "門後的腳步";
const FOREIGN = LOCALES.filter((locale) => locale !== "zh-TW");
const CONTEXT = {
  mysteries: [{ id: "missing-person", question: "她是否還活著？", answer: "她還活著", reveal_episode: 20 }],
  reveal_schedule: [{ mystery_id: "missing-person", episode: 20 }],
  setting_md: "失蹤者生死不明，公開介紹不可透露她仍然活著。",
  outline_md: "第 20 集才揭露她還活著。",
};
const PASS = { passed: true, problems: [] };
const writeJson = (file, value) => writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);

function fixture(t, { context = CONTEXT, planned = false } = {}) {
  const box = sandbox(`${SERIES}-full`, "drama");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = compilationDocument({ series: SERIES, episodes: EPISODES, voice: { provider: "gemini", name: "Sulafat", style: "沉穩的說書人語氣" } });
  if (planned) {
    const { title, description, tags, thumbnail } = proposal();
    doc.youtube = { ...doc.youtube, title, description, tags };
    doc.thumbnail = { template: "thumb", data: thumbnail };
  }
  const infoFile = path.join(box.dir, "compilation.json");
  const videoFile = path.join(box.dir, "video.json");
  const receiptFile = path.join(box.dir, COMPILATION_REVIEW_FILE);
  writeJson(videoFile, doc);
  mkdirSync(box.workdir, { recursive: true });
  writeJson(path.join(box.workdir, "timeline.json"), estimatedCompilationTimeline(doc));
  writeJson(infoFile, {
    series: { slug: SERIES, title: "舊城懸案", genre: "rebirth-revenge" },
    episodes: EPISODES,
    all_recaps: EPISODES.map(({ number, title, recap }) => ({ number, title, recap })),
    ...(context === undefined ? {} : { spoiler_context: structuredClone(context) }),
  });
  const state = { slug: box.slug, format: "drama", status: "active", compilation: { series: SERIES, episodes: EPISODES.map(({ slug }) => slug) }, series: { slug: SERIES, genre: "rebirth-revenge", compilation: true }, notes: [] };
  const calls = { stages: [], retries: [], runs: [], contexts: [], reports: [] };
  const automation = {
    ctx: { root: box.root, env: { VIDEO_WORKDIR: box.work }, now: () => new Date("2026-09-30T00:00:00Z") },
    workBase: box.work,
    workdir: () => box.workdir,
    reference: () => ({ series: "Protect every unrevealed mystery in public copy." }),
    cleared: () => {},
    saveState: () => {},
    report: async (...args) => calls.reports.push(args),
    retryLater: async (_state, stage, problem) => { calls.retries.push({ stage, problem }); return `retry ${stage}: ${problem}`; },
    later: async (problem) => `later: ${problem}`,
    block: async (_state, problem) => `blocked: ${problem}`,
    lastLine: (text) => text,
    run: async (command) => { calls.runs.push(command); return { code: 0, out: "ok" }; },
    api: { seriesContext: async (slug) => { calls.contexts.push(slug); return {}; } },
    stage: async (stage, slug, payload, budget, format, variant) => {
      calls.stages.push({ stage, slug, payload: structuredClone(payload), budget, format, variant });
      return responder(stage, payload);
    },
  };
  let responder = (stage, payload) => {
    if (stage === "planner") return proposal();
    if (stage === "translator") return translation(payload.locale);
    if (stage === "verifier") return structuredClone(PASS);
    throw new Error(`Unexpected stage ${stage}`);
  };
  return {
    ...box, infoFile, videoFile, receiptFile, state, calls, automation,
    respond: (fn) => { responder = fn; },
    stages: (stage) => calls.stages.filter((call) => call.stage === stage),
    video: () => readJson(videoFile),
  };
}

function proposal({ spoiler = false } = {}) {
  return {
    title: "一封失蹤的信，揭開舊城懸案", titles: ["舊城裡的最後一封信"],
    description: "一封沒有署名的信，讓沉睡的舊城再次醒來。",
    tags: ["懸疑", "AI漫劇"],
    thumbnail: { headline: "誰寄來這封信", tag: "懸案" },
    chapters: Object.fromEntries(EPISODES.map(({ slug, title }) => [slug, slug === REVEAL && !spoiler ? SAFE_CHAPTER : title])),
  };
}

function translation(locale, { spoiler = false } = {}) {
  return {
    title: `${locale} The missing letter`, description: `${locale} A letter awakens an old mystery.`, tags: [`${locale} mystery`],
    chapters: Object.fromEntries(EPISODES.map(({ slug, number }) => [slug, slug === REVEAL ? (spoiler ? "She is still alive" : "Footsteps behind the door") : `${locale} Night ${number}`])),
    lines: {},
  };
}

function fillTranslations(box) {
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  for (const locale of FOREIGN) writeJson(path.join(box.dir, "i18n", `${locale}.json`), translation(locale));
}

function writePackage(box) {
  const translations = Object.fromEntries(FOREIGN.map((locale) => [locale, readJson(path.join(box.dir, "i18n", `${locale}.json`))]));
  const timeline = readJson(path.join(box.workdir, "timeline.json"));
  const { metadata } = composeMetadata({ doc: box.video(), timeline, translations });
  mkdirSync(path.join(box.workdir, "upload"), { recursive: true });
  writeJson(path.join(box.workdir, "upload", "metadata.json"), metadata);
}

async function reviewAll(box, next) {
  const outcomes = [];
  for (let round = 0; round < 8; round++) {
    const result = await advanceCompilation(box.automation, box.state, next);
    if (result === undefined) return;
    outcomes.push(result);
  }
  assert.fail(`all source and translated public text should clear in bounded steps: ${outcomes.join("; ")}`);
}

test("a 40-episode compilation rewrites an e020 revelation before saving titles, cards or a review receipt", async (t) => {
  const box = fixture(t);
  const original = readFileSync(box.videoFile, "utf8");
  box.respond((stage, payload) => {
    if (stage === "planner") {
      assert.deepEqual(payload.spoiler_context, CONTEXT);
      assert.equal(payload.episodes.length, 40);
      assert.equal(payload.episodes[19].title, "她還活著");
      return proposal({ spoiler: !payload.previous_problem });
    }
    assert.equal(stage, "verifier");
    assert.equal(readFileSync(box.videoFile, "utf8"), original, "neither candidate is saved before its verdict");
    assert.equal(existsSync(box.receiptFile), false);
    assert.equal(existsSync(path.join(box.dir, "metadata-plan.json")), false);
    assert.equal(payload.locale, "zh-TW");
    assert.deepEqual(payload.spoiler_context, CONTEXT);
    const spoiler = JSON.stringify(payload.public_text).includes("她還活著");
    return spoiler ? { passed: false, problems: ["e020 chapter reveals that the missing woman is alive"] } : PASS;
  });
  assert.match(await planMetadata(box.automation, box.state), /planned/);
  assert.equal(box.stages("planner").length, 2);
  assert.match(box.stages("planner")[1].payload.previous_problem, /e020 chapter/);
  assert.equal(box.stages("verifier").length, 2);
  for (const call of box.calls.stages) assert.equal(call.variant, "compilation");
  const first = box.stages("verifier")[0].payload.public_text;
  assert.match(first.description, /她還活著/);
  assert.match(first.chapters[19].title, /她還活著/);
  const saved = box.video();
  assert.equal(saved.compilation.titles[REVEAL], SAFE_CHAPTER);
  const card = saved.scenes.find((scene) => scene.id === "card-20");
  assert.equal(card.data.title, SAFE_CHAPTER);
  assert.match(card.chapter, /門後的腳步/);
  assert.match(card.lines[0].text, /門後的腳步/);
  const accepted = box.stages("verifier")[1].payload.public_text;
  assert.doesNotMatch(JSON.stringify(accepted), /她還活著/);
  const receipt = readJson(box.receiptFile);
  assert.equal(receipt.schema_version, 1);
  assert.deepEqual(receipt.locales["zh-TW"], { passed: true, input_sha256: reviewHash(CONTEXT, "zh-TW", accepted), reviewed_at: "2026-09-30T00:00:00.000Z" });
});

test("rejected or malformed verdicts fail closed after two candidates and preserve all existing files", async (t) => {
  for (const verdict of [null, {}, { passed: "true", problems: [] }, { passed: true }, { passed: true, problems: ["reveals the answer"] }, { passed: false, problems: [] }]) {
    await t.test(JSON.stringify(verdict), async (sub) => {
      const box = fixture(sub);
      const planFile = path.join(box.dir, "metadata-plan.json");
      writeJson(planFile, { titles: ["previously accepted"], planned_at: "old" });
      writeJson(box.receiptFile, { schema_version: 1, locales: { "zh-TW": { passed: true, input_sha256: "old", reviewed_at: "old" } } });
      const files = [box.videoFile, planFile, box.receiptFile];
      const before = files.map((file) => readFileSync(file, "utf8"));
      box.respond((stage) => stage === "planner" ? proposal() : verdict);
      assert.match(await planMetadata(box.automation, box.state), /retry planner/);
      assert.equal(box.stages("planner").length, 2);
      assert.equal(box.stages("verifier").length, 2);
      assert.deepEqual(files.map((file) => readFileSync(file, "utf8")), before);
      assert.equal(box.calls.reports.length, 0);
      assert.equal(box.calls.runs.length, 0);
    });
  }
});

test("mystery-bearing planners must supply every episode's chapter title before review", async (t) => {
  const box = fixture(t);
  box.respond(() => {
    const answer = proposal();
    delete answer.chapters[REVEAL];
    return answer;
  });
  const before = readFileSync(box.videoFile, "utf8");
  assert.match(await planMetadata(box.automation, box.state), /retry planner/);
  assert.equal(box.stages("planner").length, 2);
  assert.equal(box.stages("verifier").length, 0);
  assert.equal(readFileSync(box.videoFile, "utf8"), before);
});

test("legacy context is hydrated from the series, while unknown context stops even a completed compilation", async (t) => {
  for (const hydrated of [true, false]) {
    await t.test(hydrated ? "hydrated" : "unavailable", async (sub) => {
      const box = fixture(sub, { context: null, planned: true });
      const source = { mysteries: CONTEXT.mysteries, setting: { id: "setting-1", version: 3, body_md: CONTEXT.setting_md }, outline: { id: "outline-1", version: 4, body_md: CONTEXT.outline_md, body_json: { reveal_schedule: CONTEXT.reveal_schedule } } };
      box.automation.api.seriesContext = async (slug) => { box.calls.contexts.push(slug); return hydrated ? source : { setting: source.setting }; };
      const result = await advanceCompilation(box.automation, box.state, "on YouTube");
      assert.notEqual(result, undefined, "unknown context must not pass to publishing");
      assert.deepEqual(box.calls.contexts, [SERIES]);
      if (hydrated) {
        const persisted = readJson(box.infoFile).spoiler_context;
        assert.deepEqual(persisted.mysteries, CONTEXT.mysteries);
        assert.deepEqual(persisted.reveal_schedule, CONTEXT.reveal_schedule);
        assert.equal(persisted.setting_md, CONTEXT.setting_md);
        assert.equal(persisted.outline.version, 4);
        assert.equal(box.stages("verifier").length, 1);
      } else {
        assert.match(result, /context/);
        assert.equal(box.calls.stages.length, 0);
        assert.equal(existsSync(box.receiptFile), false);
      }
      assert.deepEqual(box.calls.runs, []);
    });
  }
});

test("an explicit series without mysteries keeps the old planner and translation path without verifier calls", async (t) => {
  const box = fixture(t, { context: { ...CONTEXT, mysteries: [] } });
  box.respond((stage, payload) => {
    if (stage === "planner") { const answer = proposal(); delete answer.chapters; return answer; }
    assert.equal(stage, "translator");
    return translation(payload.locale);
  });
  assert.match(await planMetadata(box.automation, box.state), /planned/);
  assert.equal(box.video().compilation.titles[REVEAL], "她還活著");
  for (const locale of FOREIGN) assert.match(await translateMetadata(box.automation, box.state), new RegExp(locale));
  assert.equal(await advanceCompilation(box.automation, box.state, "on YouTube"), undefined);
  assert.equal(box.stages("verifier").length, 0);
  assert.deepEqual(box.calls.contexts, []);
});

test("a translated revelation is independently rejected and rewritten before its locale is saved", async (t) => {
  const box = fixture(t);
  await planMetadata(box.automation, box.state);
  box.calls.stages.length = 0;
  const locale = FOREIGN[0];
  const file = path.join(box.dir, "i18n", `${locale}.json`);
  box.respond((stage, payload) => {
    if (stage === "translator") {
      assert.deepEqual(payload.spoiler_context, CONTEXT);
      assert.equal(payload.chapters[REVEAL], SAFE_CHAPTER);
      return translation(payload.locale, { spoiler: !payload.previous_problem });
    }
    assert.equal(stage, "verifier");
    assert.equal(existsSync(file), false);
    assert.equal(payload.locale, locale);
    return JSON.stringify(payload.public_text).includes("She is still alive") ? { passed: false, problems: ["translated e020 title gives away survival"] } : PASS;
  });
  assert.match(await translateMetadata(box.automation, box.state), new RegExp(locale));
  assert.equal(box.stages("translator").length, 2);
  assert.match(box.stages("translator")[1].payload.previous_problem, /survival/);
  assert.equal(box.stages("verifier").length, 2);
  assert.equal(readJson(file).chapters[REVEAL], "Footsteps behind the door");
  const accepted = box.stages("verifier")[1].payload.public_text;
  assert.match(accepted.description, /Footsteps behind the door/);
  assert.equal(readJson(box.receiptFile).locales[locale].input_sha256, reviewHash(CONTEXT, locale, accepted));
});

for (const next of ["on YouTube", undefined]) {
  test(`resuming at ${String(next)} reviews already-filled translations before allowing the shared step`, async (t) => {
    const box = fixture(t, { planned: true });
    fillTranslations(box);
    writePackage(box);
    await reviewAll(box, next);
    assert.deepEqual(box.stages("verifier").map(({ payload }) => payload.locale).sort(), [...LOCALES].sort());
    assert.equal(box.stages("translator").length, 0, "safe complete translations need review, not regeneration");
    assert.equal(box.stages("planner").length, 0);
    assert.deepEqual(box.calls.runs, []);
    box.calls.stages.length = 0;
    assert.equal(await advanceCompilation(box.automation, box.state, next), undefined);
    assert.deepEqual(box.calls.stages, [], "unchanged exact copy reuses its receipts");
  });
}

test("resuming a filled but unsafe locale does not overwrite it when both rewritten candidates fail", async (t) => {
  const box = fixture(t);
  await planMetadata(box.automation, box.state);
  fillTranslations(box);
  const locale = FOREIGN[0];
  const file = path.join(box.dir, "i18n", `${locale}.json`);
  writeJson(file, translation(locale, { spoiler: true }));
  const before = readFileSync(file, "utf8");
  box.calls.stages.length = 0;
  box.respond((stage, payload) => stage === "translator" ? translation(payload.locale, { spoiler: true }) : { passed: false, problems: ["spoils the missing person's survival"] });
  assert.match(await advanceCompilation(box.automation, box.state, "on YouTube"), /retry translator/);
  assert.equal(box.stages("translator").length, 2);
  assert.equal(readFileSync(file, "utf8"), before);
  assert.equal(readJson(box.receiptFile).locales[locale], undefined);
  assert.deepEqual(box.calls.runs, []);
});

test("source, chapter, translation, context and measured timeline changes each invalidate accepted public copy", async (t) => {
  const changes = {
    source: (box) => { const doc = box.video(); doc.youtube.description += " 新線索出現。"; writeJson(box.videoFile, doc); },
    chapter: (box) => { const doc = box.video(); doc.compilation.titles[REVEAL] = "她還活著"; writeJson(box.videoFile, doc); },
    translation: (box) => { const file = path.join(box.dir, "i18n", `${FOREIGN[0]}.json`); const body = readJson(file); body.chapters[REVEAL] = "She is still alive"; writeJson(file, body); },
    context: (box) => { const info = readJson(box.infoFile); info.spoiler_context.reveal_schedule[0].episode = 40; writeJson(box.infoFile, info); },
    timeline: (box) => { const timeline = estimatedCompilationTimeline(box.video()); timeline.chapters[19].start_frame += 30; writeJson(path.join(box.workdir, "timeline.json"), timeline); },
  };
  for (const [name, change] of Object.entries(changes)) {
    await t.test(name, async (sub) => {
      const box = fixture(sub);
      await planMetadata(box.automation, box.state);
      fillTranslations(box);
      await reviewAll(box, "final video approved");
      const oldReceipt = readJson(box.receiptFile);
      box.calls.stages.length = 0;
      change(box);
      assert.notEqual(await advanceCompilation(box.automation, box.state, "on YouTube"), undefined);
      const reviewed = box.stages("verifier");
      assert.equal(reviewed.length, 1);
      const locale = name === "translation" ? FOREIGN[0] : "zh-TW";
      assert.equal(reviewed[0].payload.locale, locale);
      assert.notEqual(readJson(box.receiptFile).locales[locale].input_sha256, oldReceipt.locales[locale].input_sha256);
      assert.deepEqual(box.calls.runs, [], "the changed text is a separate unit before any publish step");
    });
  }
});

test("stale upload metadata is rebuilt after public-copy reviews and before a resumed publish", async (t) => {
  const box = fixture(t);
  await planMetadata(box.automation, box.state);
  fillTranslations(box);
  await reviewAll(box, "final video approved");
  mkdirSync(path.join(box.workdir, "upload"), { recursive: true });
  writeJson(path.join(box.workdir, "upload", "metadata.json"), { title: "她還活著", description: "an obsolete upload package", compilation: true, final_sha256: "old" });
  box.calls.stages.length = 0;
  const result = await advanceCompilation(box.automation, box.state, "on YouTube");
  assert.match(result, /metadata rebuilt/);
  assert.deepEqual(box.calls.runs, [["package", "--slug", box.slug]]);
  assert.deepEqual(box.calls.stages, [], "valid receipts do not spend another model call to rebuild a stale package");
});

test("a resumed source with a newly exposed mystery returns to the planner before any shared publishing step", async (t) => {
  const box = fixture(t);
  await planMetadata(box.automation, box.state);
  fillTranslations(box);
  await reviewAll(box, "final video approved");
  writePackage(box);
  const unsafe = box.video();
  unsafe.youtube.description = "她還活著，失蹤只是一場騙局。";
  writeJson(box.videoFile, unsafe);
  const packageFile = path.join(box.workdir, "upload", "metadata.json");
  const previousPackage = readFileSync(packageFile, "utf8");
  box.calls.stages.length = 0;
  box.respond((stage, payload) => {
    if (stage === "planner") {
      assert.match(payload.previous_problem, /survival/);
      return proposal();
    }
    assert.equal(stage, "verifier");
    return payload.public_text.description.includes("她還活著") ? { passed: false, problems: ["the source description reveals survival"] } : PASS;
  });
  assert.match(await advanceCompilation(box.automation, box.state, "on YouTube"), /planned/);
  assert.deepEqual(box.calls.stages.map(({ stage }) => stage), ["verifier", "planner", "verifier"]);
  assert.doesNotMatch(box.video().youtube.description, /她還活著/);
  assert.equal(readFileSync(packageFile, "utf8"), previousPackage);
  assert.deepEqual(box.calls.runs, [], "no packaging or publish work occurs in the rejected-source step");
});
