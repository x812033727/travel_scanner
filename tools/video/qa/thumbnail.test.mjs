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
import { jpegBytes, pngBytes } from "./test-images.mjs";
import { atPhoneWidth, HEADLINE, headlineLayout, headlineSizeEstimate, headlineTokens, imageSize, MAX_BYTES, MIN_HEADLINE_PX_AT_PHONE, PHONE_WIDTH, thumbnailChecks } from "./thumbnail.mjs";

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

test("the headline estimate follows the renderer's shrink: short headlines keep the theme's size, long ones shrink", () => {
  assert.equal(headlineSizeEstimate("第一名不一定最好用"), HEADLINE.fontSize);
  assert.equal(headlineSizeEstimate("它會**自己找路**\n進去？"), HEADLINE.fontSize, "an explicit break and an emphasised run fit on two lines");
  assert.equal(atPhoneWidth(HEADLINE.fontSize), 34);
  // Four lines of CJK at 136 px overflow the 460 px box; the size settles where three lines fit.
  const twenty = "字".repeat(20);
  const size = headlineSizeEstimate(twenty);
  assert.ok(size < HEADLINE.fontSize && size >= HEADLINE.fontSize * HEADLINE.minScale, `${size}`);
  assert.equal(headlineLayout(headlineTokens(twenty), size).lines, 3);
  assert.ok(atPhoneWidth(size) >= MIN_HEADLINE_PX_AT_PHONE, "twenty characters still read on a phone");
  // Forty characters need five lines and shrink below the floor.
  const forty = "字".repeat(40);
  assert.ok(atPhoneWidth(headlineSizeEstimate(forty)) < MIN_HEADLINE_PX_AT_PHONE);
  // A Latin word never breaks inside; one wider than the box forces the shrink.
  const layout = headlineLayout(headlineTokens("Supercalifragilistic 很長"), 136);
  assert.equal(layout.tooWide, true);
  assert.equal(headlineTokens("AI 模型").length, 4, "a word, a space, two glyphs");
  assert.ok(headlineSizeEstimate("字".repeat(400)) >= HEADLINE.fontSize * HEADLINE.minScale, "never below the renderer's floor");
});

test("the numbers the estimate rests on are the theme's and the renderer's", () => {
  const theme = readFileSync(THEME_FILE, "utf8");
  const h1 = /\.thumb h1 \{([^}]*)\}/.exec(theme)[1];
  assert.match(h1, new RegExp(`font-size: ${HEADLINE.fontSize}px`));
  assert.match(h1, new RegExp(`line-height: ${HEADLINE.lineHeight}\\b`));
  assert.match(h1, new RegExp(`max-height: ${HEADLINE.maxHeight}px`));
  assert.match(theme, /\.thumb \{ position: absolute; inset: 0; padding: 64px 72px;/);
  assert.match(theme, /\.thumb \{ padding-right: 340px; \}/);
  assert.equal(HEADLINE.width, 1280 - 72 - 340);
  const renderer = readFileSync(new URL("../render/browser.mjs", import.meta.url), "utf8");
  assert.match(renderer, /size > start \* 0\.6/);
  assert.match(renderer, /size -= 2;/);
  assert.match(renderer, /> size \* 0\.4/);
  assert.deepEqual([HEADLINE.minScale, HEADLINE.step, HEADLINE.tolerance], [0.6, 2, 0.4]);
  assert.equal(MAX_BYTES, THUMBNAIL_MAX_BYTES);
  assert.equal(PHONE_WIDTH, 320);
});

test("the thumbnail item checks the size, the bytes and the headline's height on a phone", () => {
  const good = thumbnailChecks({ bytes: jpegBytes(1280, 720, 2000), headline: "第一名不一定最好用" });
  assert.equal(good.ok, true);
  assert.match(good.detail, /^1280x720 JPEG, 2 KB; the headline is about 34 px tall at 320 px wide$/);
  const wrong = thumbnailChecks({ bytes: pngBytes(1920, 1080), headline: "字".repeat(40) });
  assert.equal(wrong.ok, false);
  assert.match(wrong.detail, /1920x1080; YouTube wants 1280x720/);
  assert.match(wrong.detail, /the headline shrinks to about \d+ px at 320 px wide; at least 24 px/);
  const heavy = thumbnailChecks({ bytes: jpegBytes(1280, 720, MAX_BYTES), headline: "短" });
  assert.match(heavy.detail, /bytes; YouTube's limit is 2 MB/);
  assert.match(thumbnailChecks({ bytes: Buffer.from("not an image"), headline: "短" }).detail, /not a JPEG or PNG/);
  assert.equal(thumbnailChecks({ bytes: jpegBytes(1280, 720), headline: undefined }).ok, true);
});

test("the thumbnail item checks each language's own thumbnail too, and what is wrong with one only warns", () => {
  const doc = fixture();
  const workdir = tempDir("video-qa-thumbs-");
  mkdirSync(path.join(workdir, "frames"));
  mkdirSync(path.join(workdir, "thumbnails"));
  writeFileSync(path.join(workdir, "thumbnail.jpg"), jpegBytes(1280, 720, 2000));
  const merged = (headline) => ({ thumbnail: { tag: "Picking a model", headline }, source_hashes: { thumbnail: thumbnailSourceHash(doc) } });
  const translations = { en: merged("No. 1 is not always best"), ja: merged("一位".repeat(40)) };
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
