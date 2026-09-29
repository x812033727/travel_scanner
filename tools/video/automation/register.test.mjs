import assert from "node:assert/strict";
import test from "node:test";

import { illustratedFixture } from "../core/fixtures/load.mjs";
import { MAX_PAUSE_MS } from "../core/schema.mjs";
import { HOOK_SECONDS, PAUSE_BEATS, REGISTER_RULES, registerLine, registerSummary, STORY_VOICE_STYLE, TWIST_MARKER } from "./register.mjs";

test("the register's rules carry the hook, the turn, the closing questions and the pause beats, and the voice style fits the settings field", () => {
  assert.match(REGISTER_RULES, new RegExp(`within ${HOOK_SECONDS} seconds`));
  assert.match(REGISTER_RULES, /「你以為…其實…」/);
  assert.match(REGISTER_RULES, /LAST sentence is the question the next chapter answers/);
  assert.match(REGISTER_RULES, /never a number, a name, a\s+version/);
  for (const beat of Object.values(PAUSE_BEATS)) {
    assert.ok(Number.isInteger(beat) && beat > 0 && beat <= MAX_PAUSE_MS, `beat ${beat} within the schema`);
    assert.match(REGISTER_RULES, new RegExp(`\\b${beat}\\b`));
  }
  assert.ok(STORY_VOICE_STYLE.length <= 400, "the settings tab takes at most 400 characters of style");
  assert.match(STORY_VOICE_STYLE, /說書人/);
  assert.equal(TWIST_MARKER, "你以為");
});

test("registerSummary counts the turns, the chapters closing on a question and the beats from the text alone", () => {
  const doc = illustratedFixture();
  const summary = registerSummary(doc);
  assert.deepEqual(summary, { lines: 11, twists: 1, chapters: 4, chapter_questions: 0, opener_is_greeting: false, pauses: 2 });
  assert.equal(registerLine(summary), "11 lines, 1 「你以為」 turn, 0 of 3 chapters closing on a question, 2 pause beats");

  // Retold: two chapters close on a question, one more turn, a greeting slipped into the opener.
  doc.scenes[0].lines[0].text = "大家好，今天要跟大家分享排行榜第一名的模型。";
  doc.scenes[1].lines[0].text = "你以為它考的是你的工作，其實排行榜考的是另一份考卷。";
  doc.scenes[3].lines[0].text = "答案可能讓你意外，三個數字到底說了什麼？";
  doc.scenes[6].lines[0].text = "一句話，先看工作，那到底該怎麼選？";
  doc.scenes[6].lines[0].pause_after_ms = 1200;
  const retold = registerSummary(doc);
  assert.deepEqual(retold, { lines: 11, twists: 1, chapters: 4, chapter_questions: 2, opener_is_greeting: true, pauses: 3 }, "the opener lost its turn to the greeting, the podium gained one");
  assert.match(registerLine(retold), /^11 lines, 1 「你以為」 turn, 2 of 3 chapters closing on a question, 3 pause beats; the opener greets instead of hooking$/);

  // A script with one chapter has no closer to count; no lines is no story.
  assert.equal(registerLine(registerSummary({ scenes: [{ id: "a", template: "title", data: {}, lines: [{ id: "a1", text: "一句。" }] }] })), "1 lines, 0 「你以為」 turns, 0 of 0 chapters closing on a question, 0 pause beats");
  assert.deepEqual(registerSummary({ scenes: [] }), { lines: 0, twists: 0, chapters: 0, chapter_questions: 0, opener_is_greeting: false, pauses: 0 });
});
