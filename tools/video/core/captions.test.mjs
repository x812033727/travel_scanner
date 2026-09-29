import assert from "node:assert/strict";
import test from "node:test";

import {
  buildCues,
  checkCues,
  displayText,
  fits,
  joinPieces,
  LOCALE_RULES,
  measure,
  MIN_CUE_MS,
  parseSrt,
  splitText,
  timePieces,
  toSrt,
  toVtt,
  wrapCue,
} from "./captions.mjs";
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

test("a line just over one cue is cut evenly, not into a full cue and a scrap", () => {
  const text = "The prices are the standard rates from the official pricing pages as of September 2026.";
  const pieces = splitText(text, en);
  assert.equal(pieces.length, 2);
  assert.equal(pieces.join(" "), text);
  for (const piece of pieces) assert.ok(piece.length > 30, piece);
});

test("a Korean line short enough by count but not by word wrap becomes two cues that each wrap in two lines", () => {
  const ko = LOCALE_RULES.ko;
  const text = "지난달에 겨우 모델 하나 정했는데, 이번 달엔 또 바뀌었습니다.";
  assert.ok(measure(text, ko) <= ko.maxChars * ko.maxLines);
  assert.equal(fits(text, ko), false);
  const pieces = splitText(text, ko);
  assert.deepEqual(pieces, ["지난달에 겨우 모델 하나 정했는데,", "이번 달엔 또 바뀌었습니다."]);
  for (const piece of pieces) assert.equal(wrapCue(piece, ko).split("\n").length <= ko.maxLines, true);
});

test("merging a piece that would flash past keeps the space and never makes a cue that cannot fit", () => {
  const ko = LOCALE_RULES.ko;
  assert.equal(joinPieces("둘째,", "저는 씁니다.", ko), "둘째, 저는 씁니다.");
  assert.equal(joinPieces("第一句，", "第二句", zh), "第一句，第二句");
  const room = timePieces(["둘째,", "저는 대부분 작업에 저렴하게 시작해"], 0, 3000, ko);
  assert.deepEqual(room.map((cue) => cue.text), ["둘째, 저는 대부분 작업에 저렴하게 시작해"]);
  const full = "I start most work on a small model and step up to the flagship only when needed.";
  assert.equal(fits(joinPieces("Second,", full, en), en), false);
  const kept = timePieces(["Second,", full], 0, 4000, en);
  assert.deepEqual(kept.map((cue) => cue.text), ["Second,", full]);
  const merged = timePieces(["September", "2026."], 0, 1500, en);
  assert.deepEqual(merged.map((cue) => cue.text), ["September 2026."]);
});

test("every cue of a real translation wraps into at most two lines with its spaces intact", () => {
  const ko = LOCALE_RULES.ko;
  const lines = [
    "리더보드 1위만 보면 정확하긴 해도 여러분에게 맞다는 보장은 없습니다.",
    "둘째, 저는 대부분 작업에 저렴하게 시작해 승급하는 캐스케이드를 씁니다.",
    "병렬 교차 검토가 비싼 건 두 모델이 각각 한 번씩 답해야 하기 때문입니다.",
  ];
  for (const text of lines) {
    const cues = timePieces(splitText(text, ko), 0, 4500, ko).map((cue) => wrapCue(displayText(cue.text, ko), ko));
    assert.equal(cues.join(" ").replace(/\n/g, " "), text);
    for (const cue of cues) assert.ok(cue.split("\n").length <= ko.maxLines, cue);
  }
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

for (const locale of ["zh-TW", "zh-CN", "ja"]) {
  test(`${locale} wraps versions, prices and product names only at complete token boundaries`, () => {
    for (const token of ["4.0", "0.50", "GPT-6", "C++", "C#", "A_B", "O'Neil"]) {
      const rules = { ...LOCALE_RULES[locale], maxChars: Math.ceil(measure(token, zh) + 1) };
      const text = `甲${token}乙`;
      const lines = wrapCue(text, rules).split("\n");
      assert.ok(lines.some((line) => line.includes(token)), `${token}: ${lines.join(" / ")}`);
      assert.equal(lines.join(""), text);
      assert.equal(lines.length, 2);
      for (const line of lines) assert.ok(measure(line, rules) <= rules.maxChars, line);
    }
    assert.equal(wrapCue("GPT-6乙", { ...LOCALE_RULES[locale], maxChars: 3 }), "GPT-6\n乙");
  });

  test(`${locale} keeps closing punctuation with preceding text, including spaces and consecutive closers`, () => {
    for (const [text, maxChars] of [["甲甲。乙", 3], ["甲甲甲 。乙", 3], ["甲甲甲。」乙乙", 4], ["甲甲。 \t」乙乙", 4]]) {
      const rules = { ...LOCALE_RULES[locale], maxChars };
      const pieces = splitText(text, rules);
      const lines = pieces.flatMap((piece) => {
        const wrapped = wrapCue(piece, rules).split("\n");
        assert.ok(wrapped.length <= rules.maxLines, wrapped.join(" / "));
        return wrapped;
      });
      assert.equal(lines.join("").replace(/\s/g, ""), text.replace(/\s/g, ""));
      for (const line of lines) {
        assert.doesNotMatch(line.trimStart(), /^[，。！？；：、,.!?;:）」』)\]]/u);
        assert.ok(measure(line, rules) <= maxChars, line);
      }
    }
  });

  test(`${locale} splits a three-line token layout into cues before wrapping or merging`, () => {
    const rules = { ...LOCALE_RULES[locale], maxChars: 4 };
    const text = "甲ABCDEF。乙";
    assert.equal(fits(text, rules), false);
    const pieces = splitText(text, rules);
    assert.equal(pieces.length, 2);
    assert.equal(pieces.join(""), text);
    assert.ok(pieces.some((piece) => piece.includes("ABCDEF。")));
    const timed = timePieces(pieces, 0, 1000, rules);
    assert.equal(timed.length, 2, "a short duration must not merge an unwrappable cue");
    for (const cue of timed) {
      const lines = wrapCue(cue.text, rules).split("\n");
      assert.ok(lines.length <= rules.maxLines);
      for (const line of lines) assert.ok(measure(line, rules) <= rules.maxChars, line);
    }
  });
}

test("an indivisible token with closing punctuation stays intact for width QA", () => {
  const text = `${"A".repeat(32)}。乙`;
  const pieces = splitText(text, zh);
  const wrapped = pieces.map((piece) => wrapCue(piece, zh));
  assert.equal(wrapped.join("").replace(/\n/g, ""), text);
  assert.ok(wrapped.some((piece) => piece.includes(`${"A".repeat(32)}。`)));
  assert.ok(checkCues(wrapped.map((value) => ({ start_ms: 0, end_ms: 10000, text: value })), "zh-TW")
    .some((problem) => problem.includes("wider than 16")));
});

test("safe existing zh-TW fixture captions keep their exact line breaks", () => {
  const doc = fixture();
  const texts = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, line.text]));
  assert.deepEqual(buildCues(estimateTimeline(doc), texts, "zh-TW").cues.map((cue) => cue.text), [
    "每次有新模型出來，排行榜就換一次\n第一名，你真的每次都要跟著換嗎？",
    "今天用三個問題，幫你在五分\n鐘內決定要用哪一個 AI 模型",
    "第一個問題是，你要它做什麼工作",
    "第二個問題是，\n你能接受它想多久才回答",
    "第三個問題是，\n你每個月願意為它付多少錢",
    "把這三個答案寫下來，再去看排\n行榜，你會發現選擇變得很清楚",
    "完整的比較表放在說明欄的\n文章裡，我們下一支影片見",
  ]);
});

// Real source lines that already rendered safely before token-boundary protection.
// Synthetic 100-second speech makes the exact old cue boundaries and weights observable.
for (const [locale, id, text, expected] of [
  ["zh-TW", "akm3", "我的看法是：安全要靠系統真的擋住，不是靠提示詞裡的一句「不要」。", [
    [100400, "我的看法是：安全要靠系統真的擋\n住，不是靠提示詞裡的一句「不要」"],
  ]],
  ["zh-TW", "3xvu", "有公布的：算力、記憶體容量、功耗，還有記憶體頻寬，每秒 300 GB。", [
    [100400, "有公布的：算力、記憶體容量、功\n耗，還有記憶體頻寬，每秒 300 GB"],
  ]],
  ["zh-TW", "3pgu", "每月一號太平洋時間午夜重設；部數、秒數和其他功能的點數要分開看。", [
    [100400, "每月一號太平洋時間午夜重設；部\n數、秒數和其他功能的點數要分開看"],
  ]],
  ["zh-TW", "qwig", "歐盟的 iPhone、iPad、手錶不提供，只有 Mac 和 Vision Pro 可以。", [
    [100400, "歐盟的 iPhone、iPad、手錶不提\n供，只有 Mac 和 Vision Pro 可以"],
  ]],
  ["ja", "rh8y", "では、AIはあなたの仕事を奪うのか。私の答えは「まずタスクを奪う。しかも2月の見出しが示したより速く」です。", [
    [60043, "では、AIはあなたの仕事を奪うの\nか。私の答えは「まずタスクを奪う"],
    [100400, "しかも2月の見出しが\n示したより速く」です"],
  ]],
  ["ja", "wpuc", "私の選択です。これは測定ではなく、私の意見です。毎日の要約には、ちゃんと読める中で一番安いモデル。金額はわずかです。", [
    [54764, "私の選択です。これは測定ではな\nく、私の意見です。毎日の要約には"],
    [100400, "ちゃんと読める中で一番安\nいモデル。金額はわずかです"],
  ]],
  ["zh-CN", "dgig", "AI 安全中心的报告指出，到了七月，Claude Fable 5 达到了 15.8%。", [
    [100400, "AI 安全中心的报告指出，到了七\n月，Claude Fable 5 达到了 15.8%"],
  ]],
  ["zh-CN", "akm3", "我的看法是：安全要靠系统真正挡住，而不是靠提示词里的一句“不要”。", [
    [100400, "我的看法是：安全要靠系统真正挡\n住，而不是靠提示词里的一句“不要”"],
  ]],
]) {
  test(`${locale}/${id} preserves safe rendered cues and raw punctuation timing weights`, () => {
    const actual = buildCues({ lines: [{ id, start_frame: 0, end_frame: 3030, audio_samples: 4800000 }] }, { [id]: text }, locale);
    assert.deepEqual(actual, {
      cues: expected.map(([end_ms, value], index) => ({ start_ms: index ? expected[index - 1][0] : 0, end_ms, text: value, line: id })),
      missing: [],
    });
  });
}

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
