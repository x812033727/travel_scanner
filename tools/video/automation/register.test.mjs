import assert from "node:assert/strict";
import test from "node:test";

import { illustratedFixture } from "../core/fixtures/load.mjs";
import { MAX_PAUSE_MS } from "../core/schema.mjs";
import { HOOK_SECONDS, PAUSE_BEATS, REGISTER_RULES, registerLine, registerSummary, setPauseBeats, STORY_VOICE_STYLE, TWIST_MARKER } from "./register.mjs";

test("the register's rules carry the hook, the turn, the closing questions and the pause beats, and the voice style fits the settings field", () => {
  assert.match(REGISTER_RULES, new RegExp(`within ${HOOK_SECONDS} seconds`));
  assert.match(REGISTER_RULES, /「你以為…其實…」/);
  assert.match(REGISTER_RULES, /The next chapter's first sentence is what happened next, or the answer to what the chapter\s+before left hanging/);
  assert.match(REGISTER_RULES, /Chapters end in turns: a question, a stop before the event/);
  assert.match(REGISTER_RULES, /Every 60 to 90 seconds of the body, one question is left hanging/);
  assert.match(REGISTER_RULES, /It never\s+names the next video, the next file or the next episode/);
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
  assert.deepEqual(summary, { lines: 11, twists: 1, chapters: 4, chapter_questions: 0, loops: 0, opener_is_greeting: false, pauses: 2 });
  assert.equal(registerLine(summary), "11 lines, 1 「你以為」 turn, 0 of 3 chapters closing on a question, 0 open loops, 2 pause beats");

  // Retold: two chapters close on a question, one more turn, a greeting slipped into the opener.
  doc.scenes[0].lines[0].text = "大家好，今天要跟大家分享排行榜第一名的模型。";
  doc.scenes[1].lines[0].text = "你以為它考的是你的工作，其實排行榜考的是另一份考卷。";
  doc.scenes[3].lines[0].text = "答案可能讓你意外，三個數字到底說了什麼？";
  doc.scenes[6].lines[0].text = "一句話，先看工作，那到底該怎麼選？";
  doc.scenes[6].lines[0].pause_after_ms = 1200;
  doc.loops = [{ setup: "a1hk", payoff: "b2wr", what: "三個數字到底說了什麼" }];
  const retold = registerSummary(doc);
  assert.deepEqual(retold, { lines: 11, twists: 1, chapters: 4, chapter_questions: 2, loops: 1, opener_is_greeting: true, pauses: 3 }, "the opener lost its turn to the greeting, the podium gained one");
  assert.match(registerLine(retold), /^11 lines, 1 「你以為」 turn, 2 of 3 chapters closing on a question, 1 open loop, 3 pause beats; the opener greets instead of hooking$/);

  // A script with one chapter has no closer to count; no lines is no story.
  assert.equal(registerLine(registerSummary({ scenes: [{ id: "a", template: "title", data: {}, lines: [{ id: "a1", text: "一句。" }] }] })), "1 lines, 0 「你以為」 turns, 0 of 0 chapters closing on a question, 0 open loops, 0 pause beats");
  assert.deepEqual(registerSummary({ scenes: [] }), { lines: 0, twists: 0, chapters: 0, chapter_questions: 0, loops: 0, opener_is_greeting: false, pauses: 0 });
});

const pausesOf = (doc) => Object.fromEntries(doc.scenes.flatMap((scene) => scene.lines).filter((line) => line.pause_after_ms !== undefined).map((line) => [line.id, line.pause_after_ms]));
const scene = (id, lines, chapter = null) => ({ id, template: "title", data: {}, ...(chapter ? { chapter } : {}), lines: lines.map(([lineId, text, pause]) => ({ id: lineId, text, ...(pause !== undefined ? { pause_after_ms: pause } : {}) })) });

test("setPauseBeats puts the hook after the first line, the reveal before 「其實」 and the cliffhanger on every chapter's last line", () => {
  const doc = {
    scenes: [
      scene("open", [["a1", "你每天用的那個模型，真的是最好的嗎？"], ["a2", "答案藏在一張考卷裡。"]], "開場"),
      scene("turn", [["b1", "你以為分數高就是好用。"], ["b2", "其實考卷考的不是你的工作。"], ["b3", "那它到底在考什麼？"]], "考卷"),
      // The closing beat is on the last line of the chapter's last scene that has lines, whether
      // or not it is a question: a chapter turns on a question, a stop before the event, a number
      // or a reversal (register.mjs NARRATIVE_RULES; owner, 2026-10-13).
      scene("exam", [["c1", "第一題考的是數學。"], ["c2", "可是你每天寫的是報告，對吧？"]], "題目"),
      scene("empty", []),
      scene("end", [["d1", "先看工作，再看排行榜。"]], "結論"),
    ],
  };
  assert.equal(setPauseBeats(doc), doc, "set in place and returned");
  assert.deepEqual(pausesOf(doc), { a1: PAUSE_BEATS.hook, a2: PAUSE_BEATS.cliffhanger, b1: PAUSE_BEATS.reveal, b3: PAUSE_BEATS.cliffhanger, c2: PAUSE_BEATS.cliffhanger });
  // The last chapter answers the opening question instead of leaving one: it closes the video, so it gets no beat.
  doc.scenes[4].lines[0].text = "所以，你要先看工作嗎？";
  assert.equal(pausesOf(setPauseBeats(doc)).d1, undefined);
  // A spoken form is what the voice says, so it decides the beat.
  doc.scenes[1].lines[1].say = "考卷考的不是你的工作。";
  assert.equal(pausesOf(setPauseBeats(doc)).b1, undefined);
  // The reveal reaches back across a scene boundary, and a line on two beats keeps the longer pause.
  doc.scenes[1].lines[0].text = "其實分數只是一部分。";
  doc.scenes[0].lines[1].text = "答案藏在一張考卷裡嗎？";
  assert.deepEqual(pausesOf(setPauseBeats(doc)), { a1: PAUSE_BEATS.hook, a2: PAUSE_BEATS.cliffhanger, b3: PAUSE_BEATS.cliffhanger, c2: PAUSE_BEATS.cliffhanger });
  // The fixture: the opener is both the hook and the line before 「其實」, and each chapter but the last closes on a beat.
  assert.deepEqual(pausesOf(setPauseBeats(illustratedFixture())), { a1hk: PAUSE_BEATS.hook, a2pd: PAUSE_BEATS.cliffhanger, a4dk: PAUSE_BEATS.cliffhanger, a9rl: PAUSE_BEATS.cliffhanger });
});

test("setPauseBeats clears the pauses a model set elsewhere, sets nothing on a script without beats, and changes nothing the second time", () => {
  const doc = {
    scenes: [
      scene("open", [["a1", "排行榜第一名不一定最好用。", 3000], ["a2", "先看三個數字。", 0]], "開場"),
      scene("numbers", [["b1", "第一個數字是三秒。", 2500], ["b2", "第二個數字是二十秒。"]], "數字"),
    ],
  };
  setPauseBeats(doc);
  assert.deepEqual(pausesOf(doc), { a1: PAUSE_BEATS.hook, a2: PAUSE_BEATS.cliffhanger }, "the model's 3000 on the hook becomes the beat, the first chapter's last line takes the cliffhanger, and its 2500 elsewhere is gone");
  const once = JSON.stringify(doc);
  assert.equal(JSON.stringify(setPauseBeats(doc)), once, "a second run changes nothing");
  assert.equal(registerSummary(doc).pauses, 2, "registerSummary counts the beats the tool set");

  // Nothing to beat: scenes without lines, no scenes, or a draft lint has yet to refuse.
  assert.deepEqual(pausesOf(setPauseBeats({ scenes: [scene("a", []), scene("b", [], "二")] })), {});
  assert.deepEqual(setPauseBeats({ scenes: [] }), { scenes: [] });
  assert.deepEqual(setPauseBeats({}), {});
  // The rule tells the model that the tool sets the beats, so it leaves the field out.
  assert.match(REGISTER_RULES, /The pauses are the tool's/);
  assert.match(REGISTER_RULES, /Leave\s+"pause_after_ms" out/);
});
