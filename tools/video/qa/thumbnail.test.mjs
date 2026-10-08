import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { fixture, tempDir } from "../core/fixtures/load.mjs";
import { ARTIFACTS } from "../core/state.mjs";
import { thumbnailSourceHash } from "../core/translations.mjs";
import { THUMBNAIL_MAX_BYTES } from "../render/cli.mjs";
import { thumbnailItem } from "./cli.mjs";
import { THEME_FILE } from "../render/plan.mjs";
import { THUMB_HEADLINE_MAX } from "../templates/templates.mjs";
import { jpegBytes, pngBytes } from "./test-images.mjs";
import { atPhoneWidth, HEADLINE, HEADLINE_SERIES, headlineLayout, headlineRule, headlineSizeEstimate, headlineSplitWords, headlineTokens, imageSize, MAX_BYTES, MIN_HEADLINE_PX_AT_PHONE, PHONE_WIDTH, thumbnailChecks, TITLE_HEAD_CHARS, titleOverlap } from "./thumbnail.mjs";

test("width and height are read from JPEG and PNG headers, and nothing else is an image", () => {
  assert.deepEqual(imageSize(jpegBytes(1280, 720)), { format: "jpeg", width: 1280, height: 720 });
  // A progressive JPEG (SOF2) after a fill byte and a restart-interval marker.
  const progressive = Buffer.concat([Buffer.from([0xff, 0xd8, 0xff, 0xff, 0xdd, 0x00, 0x04, 0x00, 0x10, 0xff, 0xc2, 0x00, 0x0b, 0x08]), Buffer.from([0x02, 0xd0, 0x05, 0x00, 1, 1, 0x11, 0])]);
  assert.deepEqual(imageSize(progressive), { format: "jpeg", width: 1280, height: 720 });
  assert.deepEqual(imageSize(pngBytes(1280, 720)), { format: "png", width: 1280, height: 720 });
  assert.equal(imageSize(Buffer.from("GIF89a")), null);
  assert.equal(imageSize(Buffer.from([0xff, 0xd8, 0xff, 0xd9])), null, "a JPEG with no frame has no size");
  assert.equal(imageSize(Buffer.alloc(0)), null);
});

test("the headline estimate follows the renderer's shrink in the channel's column: six characters keep the theme's size, more shrink to two lines", () => {
  assert.equal(headlineSizeEstimate("驗證碼\n別給"), HEADLINE.fontSize);
  assert.equal(headlineSizeEstimate("**不一定**最好用"), HEADLINE.fontSize, "three glyphs a line, two lines");
  assert.equal(headlineSizeEstimate("它會**闖進去**"), HEADLINE.fontSize, "an emphasised run of three fits a line");
  assert.equal(atPhoneWidth(HEADLINE.fontSize), 34);
  // Nine glyphs are three lines at 136 px; the column takes two, so the size settles where two fit.
  const nine = "第一名不一定最好用";
  const size = headlineSizeEstimate(nine);
  assert.ok(size < HEADLINE.fontSize && size >= HEADLINE.fontSize * HEADLINE.minScale, `${size}`);
  // The renderer's 0.4 em tolerance lets a third line in at that size, its foot clipped; the
  // six-character rule is what keeps a headline to two lines, not the box.
  assert.equal(headlineLayout(headlineTokens(nine), size).lines, 3);
  assert.ok(atPhoneWidth(size) >= MIN_HEADLINE_PX_AT_PHONE, "nine characters would still read on a phone");
  // Twenty characters need more lines than the floor allows two of.
  assert.ok(atPhoneWidth(headlineSizeEstimate("字".repeat(20))) < MIN_HEADLINE_PX_AT_PHONE);
  // A Latin word never breaks inside; one wider than the box forces the shrink.
  const layout = headlineLayout(headlineTokens("Supercalifragilistic 很長"), 136);
  assert.equal(layout.tooWide, true);
  assert.equal(headlineTokens("AI 模型").length, 4, "a word, a space, two glyphs");
  assert.ok(headlineSizeEstimate("字".repeat(400)) >= HEADLINE.fontSize * HEADLINE.minScale, "never below the renderer's floor");
  // A series keeps the full-width column: ten glyphs a line on two lines at the theme's size.
  assert.equal(headlineSizeEstimate("冰為什麼\n會**浮**？", HEADLINE_SERIES), HEADLINE.fontSize);
  assert.equal(headlineSizeEstimate("一二三四五六\n七八九十", HEADLINE_SERIES), HEADLINE.fontSize, "six a line, the series' own rule");
  assert.ok(headlineSizeEstimate("一二三四五六\n七八九十") < HEADLINE.fontSize, "the channel's column cannot");
  assert.equal(headlineRule("sothatswhy"), HEADLINE_SERIES);
  assert.equal(headlineRule(null), HEADLINE);
  assert.equal(headlineRule("nosuch"), HEADLINE);
});

test("the layout says where each line starts, and whether the writer chose the break", () => {
  const { breaks } = headlineLayout(headlineTokens("Gem\n11月停用"), 136);
  assert.deepEqual(breaks, [{ at: 4, chosen: true }, { at: 7, chosen: false }], "after 'Gem ' the writer's line; 停用 wraps on its own at 136 px");
  assert.deepEqual(headlineLayout(headlineTokens("驗證碼\n別給"), 136).breaks, [{ at: 3, chosen: true }], "a break between CJK glyphs takes no character");
  assert.deepEqual(headlineLayout(headlineTokens("短"), 136).breaks, []);
});

test("a line break inside a word is found with Intl.Segmenter, whether the browser wraps there or the writer broke there", () => {
  assert.deepEqual(headlineSplitWords("驗證碼\n別給"), []);
  assert.deepEqual(headlineSplitWords("台灣\n能領嗎"), []);
  assert.deepEqual(headlineSplitWords("一半的攻\n擊"), [{ word: "攻擊", chosen: true }], "the first batch's 「一半的攻／擊」");
  assert.deepEqual(headlineSplitWords("建議日不是生效日"), [{ word: "不是", chosen: false }], "the browser's wrap splits 不是");
  assert.deepEqual(headlineSplitWords("Gem\n11月停用"), [], "a chosen break between a word and a number is not inside either");
  assert.deepEqual(headlineSplitWords("Can it cost\n**16x more?**"), [], "Latin words never break inside");
});

test("the headline and the title's first ten characters: their longest shared run, as a share of the headline", () => {
  assert.deepEqual(titleOverlap("ChatGPT 開始有廣告了", "ChatGPT 有廣告了 免費版 Go Plus 該升級嗎"), { shared: "ChatGPT", ratio: 7 / 13 });
  assert.deepEqual(titleOverlap("免費一年你\n符合資格嗎", "免費一年，你符合資格嗎？Gemini 學生方案"), { shared: "免費一年你符合資格嗎", ratio: 1 }, "punctuation and breaks aside, the title again");
  assert.deepEqual(titleOverlap("第一名**不一定**最好用", "AI 模型怎麼挑"), { shared: "", ratio: 0 });
  assert.equal(titleOverlap("它**闖進去**了", "OpenAI 的 AI 代理闖進一個政府入口網站").shared, "", "only the title's first ten characters count, and 闖進 is past them");
  assert.deepEqual(titleOverlap("它**闖進去**了", "AI 代理闖進政府網站"), { shared: "闖進", ratio: 0.4 });
  assert.equal(TITLE_HEAD_CHARS, 10);
});

test("the numbers the estimate rests on are the theme's and the renderer's", () => {
  const theme = readFileSync(THEME_FILE, "utf8");
  const h1 = /\.thumb h1 \{([^}]*)\}/.exec(theme)[1];
  assert.match(h1, new RegExp(`font-size: ${HEADLINE.fontSize}px`));
  assert.match(h1, new RegExp(`line-height: ${HEADLINE.lineHeight}\\b`));
  assert.match(h1, new RegExp(`max-height: ${HEADLINE_SERIES.maxHeight}px`));
  assert.match(theme, /\.thumb \{ position: absolute; inset: 0; padding: 64px 72px;/);
  assert.match(theme, /\.thumb\.series \{ padding-right: 340px; \}/);
  assert.equal(HEADLINE_SERIES.width, 1280 - 72 - 340);
  assert.match(theme, /\.thumb\.column \{ right: 60%; padding: 56px 24px 56px 56px;/);
  assert.match(theme, new RegExp(`\\.thumb\\.column h1 \\{ max-height: ${HEADLINE.maxHeight}px;`));
  assert.equal(HEADLINE.width, 1280 * 0.4 - 56 - 24);
  assert.doesNotMatch(theme, /thumb-art/, "the ring and the dot are gone");
  const renderer = readFileSync(new URL("../render/browser.mjs", import.meta.url), "utf8");
  assert.match(renderer, /size > start \* 0\.6/);
  assert.match(renderer, /size -= 2;/);
  assert.match(renderer, /> size \* 0\.4/);
  assert.deepEqual([HEADLINE.minScale, HEADLINE.step, HEADLINE.tolerance], [0.6, 2, 0.4]);
  assert.equal(MAX_BYTES, THUMBNAIL_MAX_BYTES);
  assert.equal(PHONE_WIDTH, 320);
});

test("the thumbnail item checks the size, the bytes and the headline's height on a phone", () => {
  const good = thumbnailChecks({ bytes: jpegBytes(1280, 720, 2000), headline: "驗證碼\n別給" });
  assert.deepEqual(good, { ok: true, detail: "1280x720 JPEG, 2 KB; the headline is about 34 px tall at 320 px wide", warnings: [] });
  const wrong = thumbnailChecks({ bytes: pngBytes(1920, 1080), headline: "字".repeat(40) });
  assert.equal(wrong.ok, false);
  assert.match(wrong.detail, /1920x1080; YouTube wants 1280x720/);
  assert.match(wrong.detail, /the headline shrinks to about \d+ px at 320 px wide; at least 24 px/);
  const heavy = thumbnailChecks({ bytes: jpegBytes(1280, 720, MAX_BYTES), headline: "短" });
  assert.match(heavy.detail, /bytes; YouTube's limit is 2 MB/);
  assert.match(thumbnailChecks({ bytes: Buffer.from("not an image"), headline: "短" }).detail, /not a JPEG or PNG/);
  assert.equal(thumbnailChecks({ bytes: jpegBytes(1280, 720), headline: undefined }).ok, true);
});

test("the thumbnail item holds the channel's headline to six characters, two Latin words and whole words on each line", () => {
  const bytes = jpegBytes(1280, 720, 2000);
  const check = (headline, extra = {}) => thumbnailChecks({ bytes, headline, ...extra });
  assert.equal(THUMB_HEADLINE_MAX, 6);
  const long = check("第一名不一定最好用");
  assert.equal(long.ok, false);
  assert.match(long.detail, /^the headline counts 9 characters \(a Latin word or a number counts one\); at most 6 read at a glance/);
  assert.equal(check("會回答 ≠ 有完成").ok, true, "six glyphs and a symbol");
  assert.equal(check("$50 vs **$20**").ok, false, "three Latin words");
  assert.match(check("$50 vs **$20**").detail, /3 Latin words or numbers \(50, vs, 20\); at most 2/);
  assert.equal(check("**128 GB**\n裝得下嗎").ok, true, "two numbers and four glyphs");
  const split = check("一半的攻\n擊");
  assert.equal(split.ok, false);
  assert.equal(split.detail, "a line break falls inside the word 「攻擊」; put \\n where a word ends");
  assert.equal(check("一半的\n攻擊").ok, true);
  // A series' thumbnail keeps its own length rule (templates.mjs THUMB_SERIES) and its wider column.
  assert.equal(check("冰為什麼\n會**浮**？", { series: "sothatswhy" }).ok, true);
  assert.equal(check("一二三四五六\n七八九十", { series: "sothatswhy" }).ok, true, "ten glyphs: the series' own length");
  assert.equal(check("一二三四五六\n七八九十").ok, false, "the channel's six");
});

test("a headline that says the title's first ten characters again warns, and only when the title is given", () => {
  const bytes = jpegBytes(1280, 720, 2000);
  const repeat = thumbnailChecks({ bytes, headline: "ChatGPT\n有廣告", title: "ChatGPT 有廣告了 免費版 Go Plus 該升級嗎" });
  assert.equal(repeat.ok, true, "a warning, not a fail");
  assert.deepEqual(repeat.warnings, ["the headline repeats the title: 「ChatGPT有廣告」 is in the title's first 10 characters; say what the title does not"]);
  assert.deepEqual(thumbnailChecks({ bytes, headline: "付錢也有廣告？", title: "ChatGPT 有廣告了 免費版 Go Plus 該升級嗎" }).warnings, []);
  assert.deepEqual(thumbnailChecks({ bytes, headline: "ChatGPT\n有廣告" }).warnings, [], "no title, no comparison");
  assert.deepEqual(thumbnailChecks({ bytes, headline: "ChatGPT\n有廣告", title: "  " }).warnings, []);
});

test("the thumbnail item checks each language's own thumbnail too, and what is wrong with one only warns", () => {
  const doc = fixture();
  doc.thumbnail.data.headline = "**不一定**最好用";
  const workdir = tempDir("video-qa-thumbs-");
  mkdirSync(path.join(workdir, "frames"));
  mkdirSync(path.join(workdir, "thumbnails"));
  writeFileSync(path.join(workdir, "thumbnail.jpg"), jpegBytes(1280, 720, 2000));
  const merged = (headline) => ({ thumbnail: { tag: "Picking a model", headline }, source_hashes: { thumbnail: thumbnailSourceHash(doc) } });
  const translations = { en: merged("**Not** best"), ja: merged("一位".repeat(40)) };
  writeFileSync(path.join(workdir, "thumbnails", "en.jpg"), jpegBytes(1280, 720, 2000));
  writeFileSync(path.join(workdir, "thumbnails", "ja.jpg"), jpegBytes(1280, 720, 2000));
  const drawn = { en: { file: "thumbnails/en.jpg", hash: "x" }, ja: { file: "thumbnails/ja.jpg", hash: "y" }, ko: { file: "thumbnails/ko.jpg", hash: "z" } };
  writeFileSync(path.join(workdir, ARTIFACTS.frames), JSON.stringify({ thumbnail: "thumbnail.jpg", thumbnail_locales: drawn }));
  const result = thumbnailItem(doc, workdir, translations);
  assert.equal(result.ok, true, "the video's own thumbnail decides the item");
  assert.match(result.detail, /; language thumbnails checked: en, ja$/);
  assert.equal(result.warnings.length, 2);
  assert.match(result.warnings[0], /^ja thumbnail \(thumbnails\/ja\.jpg\): the headline shrinks to about \d+ px/);
  assert.match(result.warnings[1], /^ko thumbnail: thumbnails\/ko\.jpg is missing; run render$/);
  // A render from before localized thumbnails: the item reads as it always did.
  writeFileSync(path.join(workdir, ARTIFACTS.frames), JSON.stringify({ thumbnail: "thumbnail.jpg" }));
  const plain = thumbnailItem(doc, workdir, translations);
  assert.deepEqual([plain.ok, plain.warnings], [true, undefined], "no warnings key, as before");
  assert.match(plain.detail, /^1280x720 JPEG, 2 KB; the headline is about \d+ px tall at 320 px wide$/);
});
