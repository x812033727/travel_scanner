import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import test from "node:test";

import {
  buildCues,
  checkCues,
  cuePieces,
  displayText,
  fits,
  inheritBoundaries,
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
import { presentationTimeline } from "./branding.mjs";
import { enFixture, fixture } from "./fixtures/load.mjs";
import { eachLine } from "./schema.mjs";
import { estimateTimeline, FPS, frameToMs } from "./timeline.mjs";

const zh = LOCALE_RULES["zh-TW"];
const en = LOCALE_RULES.en;
const FRAME_MS = 1000 / FPS;
const sha256 = (text) => createHash("sha256").update(text).digest("hex");

// The written units the server times for plain text (apps/api/app/video_speech/align.py
// units_of): a Latin word or number is one, whitespace none, any other character one.
const unitsOf = (text) => (text.match(/[A-Za-z0-9][A-Za-z0-9.+#'_%-]*|\s|./gsu) ?? []).filter((unit) => !/^\s$/u.test(unit));
/** Measured units of `text`, as tts writes them: unit i starts at `at(i, unit)` and lasts until the next one starts. */
function timed(text, at) {
  const units = unitsOf(text);
  const starts = units.map((unit, index) => at(index, unit));
  return units.map((unit, index) => ({ text: unit, start_ms: starts[index], end_ms: index + 1 < units.length ? starts[index + 1] : starts[index] + 200 }));
}
const HEARD = /[\p{L}\p{N}]/u;
/** The unit each cue's first letter or number was timed in: the cues' letters and numbers are the line's, in order. */
function firstUnits(cues, chars) {
  const owners = chars.flatMap((unit, index) => [...unit.text].filter((char) => HEARD.test(char)).map(() => index));
  let at = 0;
  return cues.map((cue) => {
    const first = owners[at];
    at += [...cue.text].filter((char) => HEARD.test(char)).length;
    return first;
  });
}
const untimed = (timeline) => ({ ...timeline, lines: timeline.lines.map((line) => Object.fromEntries(Object.entries(line).filter(([key]) => key !== "timing"))) });

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

test("a number is never cut from its unit, by a cue or by a line break, in Chinese, English and Korean", () => {
  // Cues one line wide, so every number would be the cheapest place to cut.
  const narrow = (rules, maxChars) => ({ ...rules, maxChars, maxLines: 1 });
  const chinese = splitText("記憶體頻寬每秒 300 GB，功耗 15.8%，售價 US$0.135，跑 5 分鐘，2026 年 9 月 24 日量的，比去年快 3 倍。", narrow(zh, 6));
  for (const kept of ["300 GB", "15.8%", "US$0.135", "5 分鐘", "2026 年", "9 月", "24 日", "3 倍"]) {
    assert.ok(chinese.some((piece) => piece.includes(kept)), `${kept} stays whole in ${chinese.join(" / ")}`);
  }
  assert.equal(chinese.join("").replace(/\s/g, ""), "記憶體頻寬每秒300GB，功耗15.8%，售價US$0.135，跑5分鐘，2026年9月24日量的，比去年快3倍。");
  const english = splitText("The card moves 300 GB a second and costs US$0.135 for 5 minutes of use, about 15.8% of the bill.", narrow(en, 12));
  for (const kept of ["300 GB", "US$0.135", "5 minutes", "15.8%"]) assert.ok(english.some((piece) => piece.includes(kept)), `${kept}: ${english.join(" / ")}`);
  const korean = splitText("이 카드는 초당 300 GB 를 옮기고 5 분 동안 15.8% 를 씁니다.", narrow(LOCALE_RULES.ko, 10));
  for (const kept of ["300 GB", "5 분", "15.8%"]) assert.ok(korean.some((piece) => piece.includes(kept)), `${kept}: ${korean.join(" / ")}`);
  // The line break inside a cue keeps them together too.
  assert.equal(wrapCue("頻寬每秒 300 GB 很快", { ...zh, maxChars: 6 }), "頻寬每秒\n300 GB 很快");
  assert.equal(wrapCue("It moves 300 GB fast", { ...en, maxChars: 12 }), "It moves\n300 GB fast");
  // A Latin suffix with no space, a bare number and a version are the whole tokens they always were.
  const tokens = splitText("甲 24fps 乙 2026 丙 4.0 丁", narrow(zh, 3));
  for (const kept of ["24fps", "2026", "4.0"]) assert.ok(tokens.some((piece) => piece.includes(kept)), `${kept}: ${tokens.join(" / ")}`);
  assert.equal(tokens.join("").replace(/\s/g, ""), "甲24fps乙2026丙4.0丁");
});

test("a cut at a sentence end beats one at a comma unless the pieces become lopsided, and a comma still beats mid-clause", () => {
  // 12 + 5 + 17 characters: the even cut is at the comma, the sentence end leaves 12 and 22.
  const text = "這是第一句話已經說完了。然後再說，第二句比較長一直講到結尾才停下來。";
  assert.deepEqual(splitText(text, zh), ["這是第一句話已經說完了。", "然後再說，第二句比較長一直講到結尾才停下來。"]);
  // Sentence ends that would leave a scrap lose to the comma in the middle.
  assert.deepEqual(splitText("第一句話說完了。第二句比較長一點，中間有個逗號，然後結束。第三句也在這裡。", zh), ["第一句話說完了。第二句比較長一點，", "中間有個逗號，然後結束。第三句也在這裡。"]);
  // No sentence end inside: the comma wins over cutting mid-clause, as before.
  assert.deepEqual(splitText("지난달에 겨우 모델 하나 정했는데, 이번 달엔 또 바뀌었습니다.", LOCALE_RULES.ko), ["지난달에 겨우 모델 하나 정했는데,", "이번 달엔 또 바뀌었습니다."]);
});

test("cuePieces is what a translator is shown as the narration's cue boundaries: the pieces before timing, one for a short line", () => {
  assert.deepEqual(cuePieces("今天用三個問題幫你決定。", "zh-TW"), ["今天用三個問題幫你決定。"]);
  const long = "每次有新模型出來，排行榜就換一次第一名，你真的每次都要跟著換嗎？還是應該先想清楚自己要它做什麼，再決定要不要換？";
  const pieces = cuePieces(long, "zh-TW");
  assert.deepEqual(pieces, ["每次有新模型出來，排行榜就換一次第一名，你真的每次都要跟著換嗎？", "還是應該先想清楚自己要它做什麼，再決定要不要換？"]);
  assert.deepEqual(pieces, splitText(long, zh), "the same cut buildCues makes");
  assert.equal(cuePieces("Every week a new model takes the top of the leaderboard, so do you switch every week?", "en").length, 2);
  assert.throws(() => cuePieces("x", "fr"), /no caption rules for locale fr/);
});

// Pinned on main at d829b18dc, before measured timing existed: a timeline whose lines carry no
// `timing` must keep producing these files byte for byte (renewed finals reuse their offsets).
test("a timeline without timing keeps the SRT and VTT it produced before measured timing, byte for byte", () => {
  const doc = fixture();
  const timeline = estimateTimeline(doc);
  const zhTexts = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, line.text]));
  const zhCues = buildCues(timeline, zhTexts, "zh-TW").cues;
  assert.equal(toSrt(zhCues), [
    "1", "00:00:00,000 --> 00:00:07,267", "每次有新模型出來，排行榜就換一次", "第一名，你真的每次都要跟著換嗎？", "",
    "2", "00:00:07,267 --> 00:00:13,667", "今天用三個問題，幫你在五分", "鐘內決定要用哪一個 AI 模型", "",
    "3", "00:00:14,267 --> 00:00:17,933", "第一個問題是，你要它做什麼工作", "",
    "4", "00:00:17,933 --> 00:00:22,333", "第二個問題是，", "你能接受它想多久才回答", "",
    "5", "00:00:22,333 --> 00:00:27,053", "第三個問題是，", "你每個月願意為它付多少錢", "",
    "6", "00:00:27,667 --> 00:00:34,233", "把這三個答案寫下來，再去看排", "行榜，你會發現選擇變得很清楚", "",
    "7", "00:00:34,233 --> 00:00:40,153", "完整的比較表放在說明欄的", "文章裡，我們下一支影片見", "",
  ].join("\n"));
  assert.equal(sha256(toVtt(zhCues)), "b7f01d85db2ce41135e5f35b776dc73a3158bfbd175f6ef730388e56c8b69a8e");
  // The English fixture's lines as this video's translation.
  const english = [...eachLine(enFixture())].map(({ line }) => line.text);
  const enCues = buildCues(timeline, Object.fromEntries([...eachLine(doc)].map(({ line }, index) => [line.id, english[index]])), "en").cues;
  assert.deepEqual([enCues.length, sha256(toSrt(enCues)), sha256(toVtt(enCues))], [8, "82d532ca9301982e9e3b9ca51cb1818cd4ea8050549b8dca3b6a367fa2a790f1", "73c3fe85949f0f25eb52063cb79b55f88b2bb2b9fa657b6e35b7fe8522f20f5f"]);
  // Lines cut into two cues or more, one with a scrap merged, in every locale.
  const lines = { lines: [
    { id: "aaaa", start_frame: 0, end_frame: 330, audio_samples: 489600 },
    { id: "bbbb", start_frame: 330, end_frame: 600, audio_samples: 403200 },
    { id: "cccc", start_frame: 600, end_frame: 900, audio_samples: 456000 },
  ] };
  for (const [locale, texts, cues, srt, vtt] of [
    ["zh-TW", ["每次有新模型出來，排行榜就換一次第一名，你真的每次都要跟著換嗎？還是應該先想清楚自己要它做什麼，再決定要不要換？", "有公布的：算力、記憶體容量、功耗，還有記憶體頻寬，每秒 300 GB。好。", "第一句話說完了。第二句比較長一點，中間有個逗號，然後結束。第三句也在這裡。"],
      6, "1d62f0bc22f2301e0ca9d8fc6d667af7e6836826d5dcfcdcdd7fa421a3bdbbcc", "6d7d4f6480abf5d82646439597cd47199ef543b53a366b8c0f33a48eefdd7609"],
    ["zh-CN", ["每次有新模型出来，排行榜就换一次第一名，你真的每次都要跟着换吗？还是应该先想清楚自己要它做什么，再决定要不要换？", "有公布的：算力、内存容量、功耗，还有内存带宽，每秒 300 GB。好。", "第一句话说完了。第二句比较长一点，中间有个逗号，然后结束。第三句也在这里。"],
      5, "fb2a433a2eb5b29d6744e9d8832743bb7d4f9187e146f5a107c83f1639996730", "50543468f48d94c081c2ae9616213a4ec0ed228a22cad6c5272d227ca1af3a60"],
    ["en", ["Every time a new model comes out, the leaderboard gets a new number one. Do you really switch every time, or decide first what you need it for?", "What was published: compute, memory capacity, power draw, and memory bandwidth, 300 GB a second. Okay.", "The first sentence is done. The second one is a bit longer, with a comma in the middle, and then it ends. The third is here too."],
      6, "62e6b02d2b1a70cc46ce98bf140c927a3347d72278d800e275291671d234d723", "eaac3f6385ac09a0ecebef566864a1f92526d021ef6d09bc1882e1144cd1963b"],
    ["ja", ["では、AIはあなたの仕事を奪うのか。私の答えは「まずタスクを奪う。しかも2月の見出しが示したより速く」です。", "私の選択です。これは測定ではなく、私の意見です。毎日の要約には、ちゃんと読める中で一番安いモデル。金額はわずかです。", "公開されたのは演算性能、メモリ容量、消費電力、そしてメモリ帯域で、毎秒 300 GB です。"],
      6, "8572c13146523a2fe3e1c01264340b0c41743f6133dde742b4897ce65bed3845", "4625c7f540523c2af827b865af1d637f17a6863c240a1e218b611e3380334146"],
    ["ko", ["리더보드 1위만 보면 정확하긴 해도 여러분에게 맞다는 보장은 없습니다.", "둘째, 저는 대부분 작업에 저렴하게 시작해 승급하는 캐스케이드를 씁니다.", "병렬 교차 검토가 비싼 건 두 모델이 각각 한 번씩 답해야 하기 때문입니다."],
      6, "95cf6ebb53d45d2e60bb2a15a20ef69b537825db47b0f79094a02c3670524782", "98a743c78c19e197cde32b79d63b3966f37e4de4fa4df5d18b1109f589eac10e"],
  ]) {
    const built = buildCues(lines, Object.fromEntries(lines.lines.map((line, index) => [line.id, texts[index]])), locale).cues;
    assert.deepEqual([built.length, sha256(toSrt(built)), sha256(toVtt(built))], [cues, srt, vtt], locale);
  }
});

/** One line of a timeline at `startFrame`, its clip `audioMs` long, timed by `chars` when given. */
function timedLine(id, startFrame, audioMs, chars) {
  return { id, start_frame: startFrame, end_frame: startFrame + Math.ceil((audioMs + 700) / FRAME_MS), audio_samples: audioMs * 48, ...(chars ? { timing: { source: "azure", model: "zh-TW-HsiaoChenNeural", chars } } : {}) };
}

test("a line whose timeline entry carries measured characters starts each cue when its first character is spoken, within a frame", () => {
  // A number and its unit open the second cue: its first character is the first of the unit "300".
  const text = "第一個問題很簡單，我們先看第一個例子。GPT-6 每秒處理 300 GB 的資料，比去年快了三倍，這個數字到底代表什麼意思？";
  // Said briskly, with a long breath after the first sentence: nothing like a share by weight.
  let clock = 37;
  const chars = timed(text, (_index, unit) => {
    const start = clock;
    clock += unit === "。" ? 1400 : 170;
    return start;
  });
  const line = timedLine("tm01", 45, clock + 150, chars);
  const { cues } = buildCues({ lines: [line] }, { tm01: text }, "zh-TW");
  const weighted = buildCues(untimed({ lines: [line] }), { tm01: text }, "zh-TW").cues;
  assert.deepEqual(cues.map((cue) => cue.text), ["第一個問題很簡單，我們先看\n第一個例子。GPT-6 每秒處理", "300 GB 的資料，比去年快了三倍，\n這個數字到底代表什麼意思？"]);
  assert.deepEqual(cues.map((cue) => cue.text), weighted.map((cue) => cue.text), "the same cut, timed by what was heard");
  const start = frameToMs(line.start_frame);
  firstUnits(cues, chars).forEach((unit, index) => {
    assert.ok(Math.abs(cues[index].start_ms - (start + chars[unit].start_ms)) <= FRAME_MS, `cue ${index + 1} starts at ${cues[index].start_ms}, its first character at ${start + chars[unit].start_ms}`);
  });
  assert.equal(chars[firstUnits(cues, chars)[1]].text, "300");
  assert.equal(cues[0].end_ms, cues[1].start_ms, "a cue runs to the next one's start");
  assert.equal(cues.at(-1).end_ms, weighted.at(-1).end_ms, "the last still ends after the speech, inside the line");
  assert.ok(Math.abs(cues[1].start_ms - weighted[1].start_ms) > 10 * FRAME_MS, "the weights would have put it elsewhere");
  assert.deepEqual(checkCues(cues, "zh-TW"), []);
});

test("the branded presentation timeline keeps each line's timing: its cues move with the intro and still start on their characters", () => {
  const text = "第一個問題很簡單，我們先看第一個例子。GPT-6 每秒處理 300 GB 的資料，比去年快了三倍，這個數字到底代表什麼意思？";
  const chars = timed(text, (index) => 40 + index * 190);
  const body = { total_frames: 600, lines: [timedLine("br01", 30, 40 + chars.length * 190, chars)], scenes: [], chapters: [] };
  const presented = presentationTimeline(body, { hash: "bookends", intro_frames: 150, outro_frames: 300 });
  assert.deepEqual(presented.lines[0].timing, body.lines[0].timing);
  const plain = buildCues(body, { br01: text }, "zh-TW").cues;
  const branded = buildCues(presented, { br01: text }, "zh-TW").cues;
  assert.deepEqual(branded, plain.map((cue) => ({ ...cue, start_ms: cue.start_ms + 5000, end_ms: cue.end_ms + 5000 })));
  firstUnits(branded, chars).forEach((unit, index) => assert.ok(Math.abs(branded[index].start_ms - (frameToMs(180) + chars[unit].start_ms)) <= FRAME_MS));
});

test("a say that differs from the text only in punctuation still lines up: its letters were all heard, in order", () => {
  const text = "他停了很久很久，才終於開口回答。好。然後我們繼續往下看第三個問題的答案。";
  const say = "他停了很久很久才終於開口回答，好，然後我們繼續往下看第三個問題的答案。";
  const chars = timed(say, (index) => 60 + index * 210);
  const line = timedLine("tm02", 0, 60 + chars.length * 210, chars);
  const { cues } = buildCues({ lines: [line] }, { tm02: text }, "zh-TW");
  assert.equal(cues.length, 2);
  firstUnits(cues, chars).forEach((unit, index) => assert.ok(Math.abs(cues[index].start_ms - chars[unit].start_ms) <= FRAME_MS));
});

test("a measured piece too short to read merges with its neighbour and starts at its own first character", () => {
  const pieces = ["第一句話慢慢說完了。", "很快。", "第三句也慢慢地說完。"];
  let clock = 0;
  const chars = timed(pieces.join(""), (_index, unit) => {
    const start = clock;
    clock += unit === "。" ? 300 : unit === "很" || unit === "快" ? 120 : 280;
    return start;
  });
  const cues = timePieces(pieces, 1000, 1000 + clock + 400, zh, fits, chars);
  assert.deepEqual(cues.map((cue) => cue.text), ["第一句話慢慢說完了。", "很快。第三句也慢慢地說完。"]);
  assert.equal(cues[0].start_ms, 1000);
  assert.equal(cues[1].start_ms, 1000 + chars.find((unit) => unit.text === "很").start_ms);
  assert.equal(cues[1].end_ms, 1000 + clock + 400);
  for (const cue of cues) assert.ok(cue.end_ms - cue.start_ms >= MIN_CUE_MS);
});

test("measured characters that do not line up with the text leave that line's cues on the weighted split", () => {
  const text = "第一個問題很簡單，我們先看第一個例子。GPT-6 每秒處理 300 GB 的資料，比去年快了三倍，這個數字到底代表什麼意思？";
  const even = timed(text, (index) => 40 + index * 200);
  const weighted = buildCues({ lines: [timedLine("mm01", 0, 9000)] }, { mm01: text }, "zh-TW");
  const cases = [
    ["a say that changes the words", timed(text.replace("簡單", "容易"), (index) => 40 + index * 200)],
    ["another language", timed("The first question is simple: GPT-6 moves 300 GB a second.", (index) => 40 + index * 300)],
    ["a unit missing", even.filter((unit) => unit.text !== "GB")],
    ["a unit left over", [...even, { text: "嗎", start_ms: 8600, end_ms: 8800 }]],
    ["a cue that would start before the one before it", even.map((unit) => (unit.text === "300" ? { ...unit, start_ms: 10 } : unit))],
    ["a start outside the speech", even.map((unit) => (unit.text === "300" ? { ...unit, start_ms: 60000 } : unit))],
  ];
  for (const [why, chars] of cases) assert.deepEqual(buildCues({ lines: [timedLine("mm01", 0, 9000, chars)] }, { mm01: text }, "zh-TW"), weighted, why);
  // A cut inside a unit the server timed as one, a term read through its spoken form, has no
  // measured start of its own.
  const pieces = ["請打開 Claude", "Code 再試一次"];
  const term = [..."請打開"].map((unit, index) => ({ text: unit, start_ms: index * 200, end_ms: index * 200 + 200 }))
    .concat([{ text: "Claude Code", start_ms: 600, end_ms: 1400 }], [..."再試一次"].map((unit, index) => ({ text: unit, start_ms: 1400 + index * 200, end_ms: 1600 + index * 200 })));
  assert.deepEqual(timePieces(pieces, 0, 2600, null, fits, term), timePieces(pieces, 0, 2600));
});

test("a translation keeps its own cut and its shares by weight: the measured characters are the narration's", () => {
  const doc = fixture();
  const texts = Object.fromEntries([...eachLine(doc)].map(({ line }) => [line.id, line.text]));
  const timeline = estimateTimeline(doc);
  for (const line of timeline.lines) line.timing = { source: "azure", model: "zh-TW-HsiaoChenNeural", chars: timed(texts[line.id], (index) => 40 + index * 150) };
  const english = [...eachLine(enFixture())].map(({ line }) => line.text);
  const enTexts = Object.fromEntries(timeline.lines.map((line, index) => [line.id, english[index]]));
  assert.deepEqual(buildCues(timeline, enTexts, "en"), buildCues(untimed(timeline), enTexts, "en"));
  assert.notDeepEqual(buildCues(timeline, texts, "zh-TW"), buildCues(untimed(timeline), texts, "zh-TW"), "while the narration's own cues follow what was heard");
});

test("checkCues reads the reading speed from the measured spans", () => {
  const text = "第一句話慢慢地說，說了很久很久才說完。第二句很快就一口氣說完了，第三句也是。";
  let clock = 0;
  const chars = timed(text, (_index, unit) => {
    const start = clock;
    clock += unit === "第" && start > 0 ? 70 : start > 4000 ? 70 : 260;
    return start;
  });
  // The clip ends 100 ms after its last character, so the last cue lingers as it always does.
  const line = timedLine("sp01", 0, clock + 100, chars);
  const measured = buildCues({ lines: [line] }, { sp01: text }, "zh-TW").cues;
  const weighted = buildCues(untimed({ lines: [line] }), { sp01: text }, "zh-TW").cues;
  assert.equal(measured.length, 2);
  assert.deepEqual(checkCues(weighted, "zh-TW"), []);
  assert.deepEqual(checkCues(measured, "zh-TW").map((problem) => problem.split(":")[0]), ["cue 2 (sp01)"]);
  assert.match(checkCues(measured, "zh-TW")[0], /characters a second, above 9/);
});

const spans = (cues) => cues.map((cue) => [cue.start_ms, cue.end_ms]);
const weightedCues = (bounds) => bounds.slice(1).map((end, index) => ({ start_ms: bounds[index], end_ms: end, text: `piece ${index + 1}` }));

test("a translation's cue changes take the narration's measured ones: one for one, the nearest, or pinned with weighted shares between", () => {
  // Equal counts: one for one.
  assert.deepEqual(spans(inheritBoundaries(weightedCues([0, 1000, 3000, 5000]), [1500, 3500])), [[0, 1500], [1500, 3500], [3500, 5000]]);
  // Fewer translated changes: each takes the nearest narration change not yet taken, in order.
  assert.deepEqual(spans(inheritBoundaries(weightedCues([0, 2500, 5000]), [1000, 2200, 4000])), [[0, 2200], [2200, 5000]]);
  assert.deepEqual(spans(inheritBoundaries(weightedCues([0, 1200, 4600, 6000]), [1000, 1400, 4000])), [[0, 1000], [1000, 4000], [4000, 6000]], "never the same change twice");
  // More translated changes: the narration's change is pinned to the nearest translated one, and
  // the others keep their weighted shares of the span between the pins around them.
  const pinned = inheritBoundaries(weightedCues([0, 1000, 2000, 4000, 6000]), [2600]);
  assert.deepEqual(spans(pinned), [[0, 1300], [1300, 2600], [2600, 4300], [4300, 6000]]);
  assert.deepEqual(pinned.map((cue) => cue.text), ["piece 1", "piece 2", "piece 3", "piece 4"], "the translation keeps its own cut");
});

test("a translation keeps its weighted times when the narration's would leave a cue too short to read, or there is nothing to inherit", () => {
  assert.equal(inheritBoundaries(weightedCues([0, 1000, 3000, 5000]), [200, 3500]), null);
  assert.equal(inheritBoundaries(weightedCues([0, 5000]), [2000]), null, "a single cue has no change to move");
  assert.equal(inheritBoundaries(weightedCues([0, 2500, 5000]), []), null);
  // With the locale's rules: a change that makes a cue read faster than maxCps is refused too.
  const worded = [
    { start_ms: 0, end_ms: 2500, text: "Thirty characters of English." },
    { start_ms: 2500, end_ms: 5000, text: "And thirty more to read here." },
  ];
  assert.equal(inheritBoundaries(worded, [1000], en), null, "29 characters in one second");
  assert.deepEqual(spans(inheritBoundaries(worded, [2000], en)), [[0, 2000], [2000, 5000]]);
  // A cue the weights already left short (nothing fitted with it) may stay as short.
  assert.deepEqual(spans(inheritBoundaries(weightedCues([0, 4000, 4500]), [3800])), [[0, 3800], [3800, 4500]]);
});

test("translated cues under a measured narration line change when the narration's cues do, and any other line keeps its weighted split byte for byte", () => {
  const text = "第一個問題很簡單，我們先看第一個例子。GPT-6 每秒處理 300 GB 的資料，比去年快了三倍，這個數字到底代表什麼意思？";
  // A long breath after the first sentence, which a share by weight cannot know about.
  let clock = 37;
  const chars = timed(text, (_index, unit) => {
    const start = clock;
    clock += unit === "。" ? 1400 : 170;
    return start;
  });
  const line = timedLine("tr01", 45, clock + 150, chars);
  const narration = { locale: "zh-TW", texts: { tr01: text } };
  const zhCues = buildCues({ lines: [line] }, { tr01: text }, "zh-TW").cues;
  const english = "The first question is simple. GPT-6 handles 300 GB a second, three times last year's speed; what does it mean?";
  const weighted = buildCues({ lines: [line] }, { tr01: english }, "en").cues;
  const inherited = buildCues({ lines: [line] }, { tr01: english }, "en", narration).cues;
  assert.equal(zhCues.length, 2);
  assert.deepEqual(inherited.map((cue) => cue.text), weighted.map((cue) => cue.text), "its own cut");
  assert.ok(Math.abs(weighted[1].start_ms - zhCues[1].start_ms) > 10 * FRAME_MS, "the weights would have put the change elsewhere");
  assert.equal(inherited[1].start_ms, zhCues[1].start_ms, "the change comes when the narration's does");
  assert.equal(inherited[0].end_ms, inherited[1].start_ms);
  assert.deepEqual([inherited[0].start_ms, inherited.at(-1).end_ms], [weighted[0].start_ms, weighted.at(-1).end_ms]);
  assert.deepEqual(checkCues(inherited, "en"), []);

  const srt = (timeline, words, given) => toSrt(buildCues(timeline, { tr01: words }, "en", given).cues);
  // Dense enough that the narration's changes would make two cues read faster than 20 a second.
  const dense = "The first question is simple, so let's start with the first example. GPT-6 handles 300 GB of data a second, three times faster than last year. What does that number actually mean?";
  assert.equal(srt({ lines: [line] }, dense, narration), srt({ lines: [line] }, dense, null), "too fast to read: weighted");
  const timedLines = { lines: [line] };
  const untimedLines = untimed(timedLines);
  assert.equal(srt(untimedLines, english, narration), srt(untimedLines, english, null), "an untimed line");
  const other = { locale: "zh-TW", texts: { tr01: text.replace("簡單", "容易") } };
  assert.equal(srt(timedLines, english, other), srt(timedLines, english, null), "a narration text the characters were not measured on");
  assert.equal(srt(timedLines, english, { locale: "zh-TW", texts: {} }), srt(timedLines, english, null), "a line the narration has no text for");
});
