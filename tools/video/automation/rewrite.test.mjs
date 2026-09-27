import assert from "node:assert/strict";
import test from "node:test";

import { factTokens, rewriteProblems } from "./rewrite.mjs";

const lexicon = { schema_version: 1, terms: { API: "A P I", "Claude Code": null, LLM: "L L M" } };

test("the 2026-09-26 rewordings pass, and an unchanged or a fully rewritten line with the same facts passes", () => {
  assert.deepEqual(rewriteProblems("你可以問它和它的回答", "你可以問它跟它的回答", { lexicon }), []);
  assert.deepEqual(rewriteProblems("這就是它的答", "這就是它的回答", { lexicon }), []);
  assert.deepEqual(rewriteProblems("旗艦每月 20 美元", "旗艦模型每月 20 美元", { lexicon }), []);
  const same = "用 API 問 LLM，2026 年每月 US$3。";
  assert.deepEqual(rewriteProblems(same, same, { lexicon }), []);
  assert.deepEqual(rewriteProblems(same, "到了 2026 年，每月 US$3 就能用 API 問 LLM。", { lexicon }), [], "order and wording may change");
  assert.deepEqual(rewriteProblems("成長 １０％", "成長 10%", { lexicon }), [], "full-width digits read as the same number");
  assert.deepEqual(rewriteProblems("這句", "這句"), [], "no lexicon at all is fine");
});

test("numbers are read as written, currency and percent marks included, and each must survive as often as before", () => {
  assert.deepEqual(factTokens("每月 1.5 萬、2026 年、10%、US$3、NT$1,200、GPT-5 和 p95。").numbers, ["1.5", "2026", "10%", "US$3", "NT$1,200"]);
  assert.deepEqual(rewriteProblems("每月 US$3", "每月 3 美元", { lexicon }), ["number US$3 is missing", "number 3 was added"]);
  assert.deepEqual(rewriteProblems("成長 10%", "成長 10", { lexicon }), ["number 10% is missing", "number 10 was added"]);
  assert.deepEqual(rewriteProblems("1.5 倍", "1 點 5 倍", { lexicon }), ["number 1.5 is missing", "number 1 was added", "number 5 was added"]);
  assert.deepEqual(rewriteProblems("2026 年的 2026 個理由", "2026 年的理由", { lexicon }), ["number 2026 appears 1 times instead of 2"]);
  assert.deepEqual(rewriteProblems("第一個問題", "第 1 個問題", { lexicon }), ["number 1 was added"]);
});

test("Latin words must survive, case aside; a joined term is one word; a new one is refused", () => {
  assert.deepEqual(factTokens("用 Gemini 和 Node.js、GPT-5、C#、OpenAI.").words, ["Gemini", "Node.js", "GPT-5", "C#", "OpenAI"]);
  assert.deepEqual(rewriteProblems("用 Gemini 和 Claude", "用 gemini 跟 Claude"), [], "the voice reads either case the same");
  assert.deepEqual(rewriteProblems("用 Gemini 和 Claude", "用 Gemini 跟 Claude Pro"), ['word "Pro" was added']);
  assert.deepEqual(rewriteProblems("用 Gemini 和 Claude", "用 Gemini"), ['word "Claude" is missing']);
  assert.deepEqual(rewriteProblems("升級到 GPT-5", "升級到 GPT 5"), ["number 5 was added", 'word "GPT-5" is missing', 'word "GPT" was added']);
  assert.deepEqual(rewriteProblems("旗艦", "旗艦模型 Opus", { lexicon }), ['word "Opus" was added']);
});

test("dictionary terms must survive as the dictionary spells them, multi-word terms whole", () => {
  assert.deepEqual(rewriteProblems("打開 Claude Code 的 API", "打開 Code Claude 的 API", { lexicon }), ['term "Claude Code" is missing'], "the words are all there but the term is not");
  assert.deepEqual(rewriteProblems("打開 Claude Code 的 API", "打開 Claude Code 的 api", { lexicon }), ['term "API" is missing'], "lint would refuse the other spelling");
  assert.deepEqual(rewriteProblems("打開 Claude Code", "打開 Claude Code 跟 Claude Code", { lexicon }), ['word "Claude" appears 2 times instead of 1', 'word "Code" appears 2 times instead of 1', 'term "Claude Code" appears 2 times instead of 1']);
  assert.deepEqual(rewriteProblems("問 LLM", "問模型", { lexicon }), ['word "LLM" is missing'], "a one-word term is reported once, as a word");
  assert.deepEqual(rewriteProblems("APIs 的用法", "API 的用法", { lexicon }), ['word "APIs" is missing', 'word "API" was added'], "the term matches whole words only, as the synthesis does, and a word reported once is not reported again as a term");
});

test("something that is not a line is refused rather than compared", () => {
  assert.deepEqual(rewriteProblems("這句", null, { lexicon }), ["a line's text must be a string"]);
  assert.deepEqual(rewriteProblems(undefined, "這句"), ["a line's text must be a string"]);
});
