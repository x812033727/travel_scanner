import assert from "node:assert/strict";
import test from "node:test";

import { compilationDocument, compilationLayout, compilationTimeline } from "./compilation.mjs";
import { contextFromSeries, publicTexts, reviewCurrent, reviewHash, reviewProblem } from "./compilation-review.mjs";
import { composeMetadata } from "../package/metadata.mjs";

const context = {
  mysteries: [{ id: "m1", question: "誰回來了？", answer: "她還活著", revealed: 20, reveal_chapter: 2 }],
  setting: { id: "setting-1", version: 3, body_md: "The private answer.", body_json: { secret: "她還活著" } },
  outline: { id: "outline-1", version: 7, body_md: "Episode twenty reveals the answer.", body_json: { reveal_schedule: [{ mystery: "m1", revealed: 20 }] } },
};

function example({ cards = true } = {}) {
  const doc = compilationDocument({ series: "mystery", episodes: [{ slug: "mystery-e020", number: 20, title: "門後的腳步" }], chapterCards: cards });
  doc.youtube = { ...doc.youtube, title: "追查失蹤的人", description: "一道門，兩種選擇。", tags: ["懸疑"] };
  doc.thumbnail.data = { headline: "誰在門後", tag: "全集" };
  const timeline = compilationTimeline(compilationLayout(doc, [{ slug: "mystery-e020", frames: 3600 }]), { "mystery-e020": "她還活著" });
  const translations = { en: { title: "At the door", description: "Two choices.", tags: ["Mystery"], chapters: { "mystery-e020": "Footsteps" } } };
  return { doc, timeline, translations, plan: { titles: ["追查失蹤的人", "誰在門後"], pinned_comment: "你會開門嗎？" } };
}

test("mystery context distinguishes unknown from explicit empty and keeps raw schedules, answers and versions", () => {
  assert.equal(contextFromSeries(null), null);
  assert.equal(contextFromSeries({ setting: { body_json: { mysteries: [] } } }), null);
  assert.deepEqual(contextFromSeries({ mysteries: [] }).mysteries, []);
  const saved = contextFromSeries(context);
  assert.deepEqual(saved.mysteries, context.mysteries);
  assert.deepEqual(saved.reveal_schedule, context.outline.body_json.reveal_schedule);
  assert.deepEqual(saved.setting, { id: "setting-1", version: 3, body_json: context.setting.body_json });
  assert.equal(saved.outline.version, 7);
  assert.equal(saved.setting_md, context.setting.body_md);
  assert.equal(saved.outline_md, context.outline.body_md);
  saved.mysteries[0].answer = "edited";
  saved.outline.body_json.reveal_schedule[0].revealed = 40;
  assert.equal(context.mysteries[0].answer, "她還活著");
  assert.equal(context.outline.body_json.reveal_schedule[0].revealed, 20);
});

test("public text contains actual composed metadata and current chapter names, thumbnail, cards and alternatives", () => {
  const input = example();
  const before = structuredClone(input);
  const fields = publicTexts(input);
  const { metadata } = composeMetadata(input);
  assert.equal(fields["zh-TW"].description, metadata.description);
  assert.equal(fields.en.description, metadata.localizations.en.description);
  assert.deepEqual(fields["zh-TW"].chapters, [{ at: "00:00", title: "第 20 集 門後的腳步" }]);
  assert.deepEqual(fields.en.chapters, [{ at: "00:00", title: "Footsteps" }]);
  assert.doesNotMatch(fields["zh-TW"].description, /她還活著/);
  assert.deepEqual(fields["zh-TW"].thumbnail, { headline: "誰在門後", tag: "全集" });
  assert.equal(fields["zh-TW"].cards[0].data.title, "門後的腳步");
  assert.deepEqual(fields["zh-TW"].titles, input.plan.titles);
  assert.equal(fields["zh-TW"].pinned_comment, "你會開門嗎？");
  assert.deepEqual(fields.en.tags, ["Mystery"]);
  assert.equal(fields.en.cards, undefined);
  assert.deepEqual(input, before);
  assert.match(publicTexts({ ...input, timeline: null })["zh-TW"].description, /第 20 集 門後的腳步/);
  const withArticle = { ...input, pack: { slug: "mystery-guide", kind: "life", locales: { en: {} } } };
  const localized = publicTexts(withArticle);
  assert.equal(localized.en.description, composeMetadata(withArticle).metadata.localizations.en.description);
  assert.match(localized.en.description, /https:\/\/mokaair\.com\/en\/life\/mystery-guide/);
});

test("reviewed chapter names use the same description-budget fallback as the actual package", () => {
  const episodes = Array.from({ length: 80 }, (_, n) => ({ slug: `mystery-e${n + 1}`, number: n + 1, title: "很長的篇名".repeat(8) }));
  const doc = compilationDocument({ series: "mystery", episodes, chapterCards: false });
  doc.youtube = { ...doc.youtube, title: "合集", description: "全集。", tags: [] };
  const fields = publicTexts({ doc });
  assert.equal(fields["zh-TW"].chapters.length, 80);
  assert.equal(fields["zh-TW"].chapters[0].title, "第 1 集");
  assert.doesNotMatch(fields["zh-TW"].description, /很長的篇名/);
});

test("only strict independent passing verdicts with no problems are accepted", () => {
  assert.equal(reviewProblem({ passed: true, problems: [] }), null);
  for (const verdict of [null, {}, { passed: "true", problems: [] }, { passed: true }, { passed: false, problems: [] }, { passed: true, problems: ["title reveals m1"] }, { passed: true, problems: [""] }, { passed: true, problems: [1] }, { passed: true, problems: [], error: "no context" }]) {
    assert.equal(typeof reviewProblem(verdict), "string", JSON.stringify(verdict));
  }
});

test("receipts bind private answers and every public field, and cannot cross locale or schema versions", () => {
  const input = example();
  const saved = contextFromSeries(context);
  const fields = publicTexts(input)["zh-TW"];
  const receipt = { passed: true, input_sha256: reviewHash(saved, "zh-TW", fields), reviewed_at: "2026-09-30T00:00:00Z" };
  const receipts = { schema_version: 1, locales: { "zh-TW": receipt } };
  assert.match(receipt.input_sha256, /^[a-f0-9]{64}$/);
  assert.equal(reviewCurrent(receipts, saved, "zh-TW", fields), true);
  assert.equal(reviewHash({ ...saved, mysteries: saved.mysteries }, "zh-TW", { ...fields, title: fields.title }), receipt.input_sha256);
  for (const key of ["title", "description", "tags", "chapters", "thumbnail", "cards", "titles", "pinned_comment"]) {
    assert.equal(reviewCurrent(receipts, saved, "zh-TW", { ...fields, [key]: "changed" }), false, key);
  }
  const changed = structuredClone(saved);
  changed.mysteries[0].answer = "another answer";
  assert.equal(reviewCurrent(receipts, changed, "zh-TW", fields), false);
  assert.equal(reviewCurrent(receipts, null, "zh-TW", fields), false);
  assert.equal(reviewCurrent({ ...receipts, schema_version: 0 }, saved, "zh-TW", fields), false);
  assert.equal(reviewCurrent({ schema_version: 1, locales: { "zh-TW": { ...receipt, passed: "true" } } }, saved, "zh-TW", fields), false);
  assert.equal(reviewCurrent({ schema_version: 1, locales: { en: receipt } }, saved, "en", fields), false);
});
