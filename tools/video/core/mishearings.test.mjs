import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { enFixture, fixture, fixtureBrief, fixtureLexicon } from "./fixtures/load.mjs";
import { lintVideo } from "./lint.mjs";
import { MISHEARD_WORDS, mishearingsIn, phrasesOf } from "./mishearings.mjs";
import { textHash } from "./schema.mjs";
import { MISHEARD_WORDS as SENT_TO_WRITERS } from "../automation/register.mjs";

process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const context = () => ({ lexicon: fixtureLexicon(), brief: fixtureBrief(), others: [], translations: {} });
const warningsAbout = (result) => result.warnings.filter((warning) => warning.message.includes("audio check mishears"));

test("the writers' prompt and lint read one list", () => {
  assert.equal(SENT_TO_WRITERS, MISHEARD_WORDS);
});

test("every row of the guide's table is in the list, and every pair in the list is in the table", () => {
  const guide = readFileSync(new URL("../../../.agents/skills/youtube-video/references/script-writing.md", import.meta.url), "utf8");
  const start = guide.indexOf("| 稿子寫的 | 被聽成 | 改成 |");
  assert.ok(start >= 0, "the table is in script-writing.md");
  const rows = [];
  for (const line of guide.slice(start).split("\n").slice(2)) {
    if (!line.trim().startsWith("|")) break;
    const [written, , instead] = line.trim().replace(/^\||\|$/g, "").split("|").map((cell) => cell.trim());
    rows.push([written, instead]);
  }
  assert.deepEqual(rows, MISHEARD_WORDS);
});

test("each row's own fix never warns", () => {
  for (const [written, instead] of MISHEARD_WORDS) {
    assert.equal(mishearingsIn(instead).some((hit) => hit.written === written), false, `${written} → ${instead}`);
  }
});

test("a known mishearing is found, once per row, with the phrase that matched", () => {
  assert.deepEqual(mishearingsIn("先在本機實跑一次。"), [
    { written: "實跑", instead: "實際跑過", phrase: "實跑" },
    { written: "本機", instead: "這台機器", phrase: "本機" },
  ]);
  assert.deepEqual(mishearingsIn("沒檔的那次比較慢。").map((hit) => hit.phrase), ["沒檔"]);
  assert.deepEqual(phrasesOf("有檔、沒檔"), ["有檔", "沒檔"]);
  assert.deepEqual(phrasesOf("沒接、接上"), ["沒接、接上"]);
});

test("a longer word that only contains the phrase does not warn", () => {
  assert.deepEqual(mishearingsIn("日本機場的報到櫃台。"), []);
  assert.deepEqual(mishearingsIn("這裡有檔案，那裡沒檔案。").map((hit) => hit.written), ["有檔案"]);
  assert.deepEqual(mishearingsIn("一共九行，沒有量到。"), []);
});

test("lint warns on a zh line that says one, and never errors", () => {
  const clean = lintVideo(fixture(), context());
  assert.deepEqual(warningsAbout(clean), []);
  const doc = fixture();
  doc.scenes[0].lines[0].text = "我們先在本機實跑一次。";
  const result = lintVideo(doc, context());
  assert.deepEqual(result.errors, clean.errors);
  const warned = warningsAbout(result);
  assert.equal(warned.length, 2);
  assert.match(warned[0].message, /「實跑」 is a word the audio check mishears .*say 「實際跑過」/);
  assert.match(warned[1].message, /「本機」.*say 「這台機器」/);
});

test("lint reads what the voice says, not the caption", () => {
  const doc = fixture();
  const line = doc.scenes[0].lines[0];
  const clean = warningsAbout(lintVideo(doc, context()));
  line.text = "我們先在這台機器上跑一次。";
  line.say = "我們先在本機跑一次。";
  line.say_for = textHash(line.text);
  const warned = warningsAbout(lintVideo(doc, context()));
  assert.equal(warned.length, clean.length + 1);
  assert.match(warned.at(-1).message, /「本機」/);
});

test("English narration is not checked", () => {
  const doc = enFixture();
  assert.deepEqual(warningsAbout(lintVideo(doc, context())), []);
});
