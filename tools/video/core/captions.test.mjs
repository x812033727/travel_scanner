import assert from "node:assert/strict";
import test from "node:test";

import { buildCues, checkCues, displayText, LOCALE_RULES, measure, MIN_CUE_MS, parseSrt, splitText, timePieces, toSrt, toVtt, wrapCue } from "./captions.mjs";
import { fixture } from "./fixtures/load.mjs";
import { eachLine } from "./schema.mjs";
import { estimateTimeline, frameToMs } from "./timeline.mjs";

const zh = LOCALE_RULES["zh-TW"];
const en = LOCALE_RULES.en;

test("measure counts half-width characters as half in Chinese captions", () => {
  assert.equal(measure("排行榜", zh), 3);
  assert.equal(measure("GPT-5", zh), 2.5);
  assert.equal(measure("GPT-5", en), 5);
});

test("a short line stays one cue; a long one is cut at clause boundaries within the cue width", () => {
  assert.deepEqual(splitText("今天用三個問題幫你決定。", zh), ["今天用三個問題幫你決定。"]);
  const long = "每次有新模型出來，排行榜就換一次第一名，你真的每次都要跟著換嗎？還是應該先想清楚自己要它做什麼，再決定要不要換？";
  const pieces = splitText(long, zh);
  assert.ok(pieces.length >= 2);
  assert.equal(pieces.join(""), long.replace(/\s/g, ""));
  for (const piece of pieces) assert.ok(measure(piece, zh) <= zh.maxChars * zh.maxLines, piece);
});

test("a clause too long for one cue is cut, but never inside a Latin word or number", () => {
  const text = `這是一段沒有任何標點但是非常非常長而且中間夾著 Claude-Opus-5.5 與 20260924 這種詞的句子一直講下去沒有停下來的意思`;
  const pieces = splitText(text, zh);
  assert.ok(pieces.length >= 2);
  assert.ok(pieces.some((piece) => piece.includes("Claude-Opus-5.5")));
  assert.ok(pieces.some((piece) => piece.includes("20260924")));
});

test("wrapCue breaks near the middle, after punctuation, into lines that fit", () => {
  const wrapped = wrapCue("排行榜就換一次第一名，你真的每次都要跟著換嗎", zh);
  const [first, second] = wrapped.split("\n");
  assert.equal(first, "排行榜就換一次第一名，");
  assert.equal(second, "你真的每次都要跟著換嗎");
  const english = wrapCue("Every time a new model comes out, the leaderboard gets a new number one.", en);
  for (const line of english.split("\n")) assert.ok(line.length <= en.maxChars, line);
  assert.equal(english.split("\n").length, 2);
});

test("Chinese cues drop a trailing comma or full stop; English cues keep their punctuation", () => {
  assert.equal(displayText("我們下一支影片見。", zh), "我們下一支影片見");
  assert.equal(displayText("你真的要換嗎？", zh), "你真的要換嗎？");
  assert.equal(displayText("See you next time.", en), "See you next time.");
});

test("timePieces fills the window exactly and merges pieces that would flash past", () => {
  const cues = timePieces(["第一段比較長的話，", "第二段也不短的話，", "三"], 1000, 7000);
  assert.equal(cues[0].start_ms, 1000);
  assert.equal(cues.at(-1).end_ms, 7000);
  for (let index = 1; index < cues.length; index++) assert.equal(cues[index].start_ms, cues[index - 1].end_ms);
  for (const cue of cues) assert.ok(cue.end_ms - cue.start_ms >= MIN_CUE_MS || cues.length === 1);
  assert.ok(cues.at(-1).text.endsWith("三"));
});

test("cues stay inside their line's window and never overlap", () => {
  const doc = fixture();
  const timeline = estimateTimeline(doc);
  const texts = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, line.text]));
  const { cues, missing } = buildCues(timeline, texts, "zh-TW");
  assert.deepEqual(missing, []);
  for (const cue of cues) {
    const line = timeline.lines.find((each) => each.id === cue.line);
    assert.ok(cue.start_ms >= Math.round(frameToMs(line.start_frame)));
    assert.ok(cue.end_ms <= Math.round(frameToMs(line.end_frame)));
  }
  assert.deepEqual(checkCues(cues, "zh-TW"), []);
});

test("a line with no translation is reported, not captioned with nothing", () => {
  const doc = fixture();
  const texts = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, `Line ${line.id}.`]));
  delete texts.m4qa;
  const { cues, missing } = buildCues(estimateTimeline(doc), texts, "en");
  assert.deepEqual(missing, ["m4qa"]);
  assert.equal(cues.length, 6);
});

test("checkCues flags overlong lines, reading speed and overlaps", () => {
  const problems = checkCues(
    [
      { start_ms: 0, end_ms: 500, text: "這一行字非常非常非常非常非常非常長", line: "a" },
      { start_ms: 400, end_ms: 3000, text: "好", line: "b" },
    ],
    "zh-TW",
  );
  assert.equal(problems.length, 3);
});

test("SRT and WebVTT use their own timestamp separators, and SRT reads back", () => {
  const cues = [
    { start_ms: 0, end_ms: 1500, text: "第一句" },
    { start_ms: 3_723_004, end_ms: 3_724_000, text: "兩行\n字幕" },
  ];
  const srt = toSrt(cues);
  assert.equal(srt, "1\n00:00:00,000 --> 00:00:01,500\n第一句\n\n2\n01:02:03,004 --> 01:02:04,000\n兩行\n字幕\n");
  assert.match(toVtt(cues), /^WEBVTT\n\n00:00:00\.000 --> 00:00:01\.500\n第一句\n/);
  assert.deepEqual(parseSrt(`﻿${srt.replace(/\n/g, "\r\n")}`), cues);
});
