import assert from "node:assert/strict";
import test from "node:test";

import { CHANNEL_ACCENT, CHANNEL_ACCENT_EN, channelAccent } from "./accent.mjs";
import { STORY_VOICE_STYLE } from "../automation/register.mjs";
import { DUB_STYLES } from "../dubs/plan.mjs";

// The wording the owner chose on 2026-10-03 (audition A1), and the retired wording it replaces.
const RETIRED_STORY =
  "台灣國語說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。";
const RETIRED_SETTINGS =
  "Relaxed, conversational tech explainer talking to a friend, in Taiwan Mandarin with a natural Taiwanese accent. Natural rise and fall in intonation, light emphasis on key words, never flat or like reading a script. Medium-brisk pace.";

test("the channel wording never names the accent the owner heard as too heavy", () => {
  for (const words of [CHANNEL_ACCENT, CHANNEL_ACCENT_EN, STORY_VOICE_STYLE, ...Object.values(DUB_STYLES)]) {
    assert.doesNotMatch(words, /台灣國語|台灣腔|台灣口音|Taiwan(ese)? accent/u, words);
  }
  assert.equal(CHANNEL_ACCENT, "標準國語，咬字清楚，台北人平常說話的語調");
});

test("the retired storyteller style becomes the owner's A1 wording, which is the new default", () => {
  assert.equal(channelAccent(RETIRED_STORY), STORY_VOICE_STYLE);
  assert.equal(
    STORY_VOICE_STYLE,
    "標準國語，咬字清楚，台北人平常說話的語調。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。",
  );
});

test("the production site's English settings row becomes the same wording in English", () => {
  assert.equal(channelAccent(RETIRED_SETTINGS), DUB_STYLES["zh-TW"]);
  assert.equal(
    DUB_STYLES["zh-TW"],
    "Relaxed, conversational tech explainer talking to a friend, in standard Mandarin with clear, precise articulation. Natural rise and fall in intonation, light emphasis on key words, never flat or like reading a script. Medium-brisk pace.",
  );
  assert.equal(
    channelAccent("Relaxed explainer with a natural Taiwanese accent. Medium pace."),
    "Relaxed explainer in standard Mandarin with clear, precise articulation. Medium pace.",
    "a bare accent clause keeps its sentence",
  );
});

test("stored character and narrator styles keep their own words around the new wording", () => {
  assert.equal(channelAccent("清亮、倔強的少女聲，台灣國語。開心、有點急"), "清亮、倔強的少女聲，標準國語，咬字清楚，台北人平常說話的語調。開心、有點急");
  assert.equal(channelAccent("沉穩的說書人語氣，台灣國語，語速稍慢"), "沉穩的說書人語氣，標準國語，咬字清楚，台北人平常說話的語調，語速稍慢");
  assert.equal(channelAccent("台灣國語、台灣腔，輕鬆、像在跟朋友解釋，有起伏、中等偏快"), "標準國語，咬字清楚，台北人平常說話的語調，輕鬆、像在跟朋友解釋，有起伏、中等偏快");
  assert.equal(
    channelAccent("自然清楚的台灣國語，像有經驗的工程師解釋操作；專有名詞稍慢，不要朗讀字卡編號。"),
    "自然清楚的標準國語，咬字清楚，台北人平常說話的語調，像有經驗的工程師解釋操作；專有名詞稍慢，不要朗讀字卡編號。",
  );
});

test("the accent is said once: a second mention goes with its separator", () => {
  assert.equal(
    channelAccent("台灣國語，自然台灣口音；先問數字，決定後短句不解釋。清晰沉著，台灣腔，受傷時降低音量"),
    "標準國語，咬字清楚，台北人平常說話的語調；先問數字，決定後短句不解釋。清晰沉著，受傷時降低音量",
  );
});

test("styles without the retired wording come back as they are", () => {
  for (const style of [
    "低聲說書，不帶台灣腔，有留白",
    "沉穩的說書人語氣",
    DUB_STYLES.en,
    DUB_STYLES.ja,
    "穩重的日本語ナレーション、標準語",
    STORY_VOICE_STYLE,
    "",
  ]) {
    assert.equal(channelAccent(style), style);
  }
  assert.equal(channelAccent(undefined), undefined);
  assert.equal(channelAccent(null), null);
});

test("a style within the limit stays within it: the wording shortens before the style is cut", () => {
  const full = `台灣國語，${"穩".repeat(395)}`;
  assert.equal(full.length, 400);
  const rewritten = channelAccent(full);
  assert.equal(rewritten.length, 400);
  assert.ok(rewritten.startsWith("標準國語，穩"), rewritten.slice(0, 12));
  const nearlyFull = `台灣國語，${"穩".repeat(390)}台灣腔`;
  const once = channelAccent(nearlyFull);
  assert.ok(once.length <= 400);
  assert.doesNotMatch(once, /台灣/u);
  assert.equal(channelAccent("台灣國語，短句", 10), "標準國語，短句");
});
