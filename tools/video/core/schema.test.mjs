import assert from "node:assert/strict";
import test from "node:test";

import { fixture } from "./fixtures/load.mjs";
import { eachLine, spokenText, textHash, validateVideo } from "./schema.mjs";

const paths = (errors) => errors.map((error) => error.path);

test("the minimal example is valid", () => {
  assert.deepEqual(validateVideo(fixture()), []);
});

test("unknown fields are errors, so a typo cannot pass as an ignored field", () => {
  const doc = fixture();
  doc.titel = "typo";
  doc.scenes[0].lines[0].txt = "typo";
  assert.deepEqual(paths(validateVideo(doc)), [".titel", "scenes[0].lines[0] (k7p2).txt"]);
});

test("line ids must be short, well-formed and unique across the whole video", () => {
  const doc = fixture();
  doc.scenes[1].lines[0].id = "k7p2";
  doc.scenes[1].lines[1].id = "Line-1";
  const errors = validateVideo(doc);
  assert.match(errors[0].message, /duplicates scenes\[0\]\.lines\[0\]/);
  assert.equal(errors[1].path, "scenes[1].lines[1] (Line-1).id");
});

test("the first scene must open a chapter, because YouTube needs one at 00:00", () => {
  const doc = fixture();
  delete doc.scenes[0].chapter;
  assert.deepEqual(paths(validateVideo(doc)), ["scenes[0].chapter"]);
});

test("say and say_for come together", () => {
  const doc = fixture();
  delete doc.scenes[2].lines[1].say_for;
  doc.scenes[0].lines[0].say_for = "abc";
  assert.deepEqual(paths(validateVideo(doc)).sort(), ["scenes[0].lines[0] (k7p2).say_for", "scenes[2].lines[1] (p5vs).say_for"]);
});

test("pauses, reveals, templates and YouTube fields are range-checked", () => {
  const doc = fixture();
  doc.scenes[0].lines[0].pause_after_ms = 9000;
  doc.scenes[1].lines[0].reveal = 0;
  doc.scenes[2].template = "carousel";
  doc.youtube.default_language = "en";
  doc.youtube.video_id = "not-an-id";
  doc.sources[0].url = "http://insecure.example";
  assert.deepEqual(paths(validateVideo(doc)).sort(), [
    "scenes[0].lines[0] (k7p2).pause_after_ms",
    "scenes[1].lines[0] (x9fe).reveal",
    "scenes[2].template",
    "sources[0]",
    "youtube.default_language",
    "youtube.video_id",
  ]);
});

test("a non-object document is one clear error", () => {
  assert.equal(validateVideo([]).length, 1);
  assert.equal(validateVideo(null)[0].message, "video.json must hold a JSON object");
});

test("textHash is short, stable and ignores Unicode normalization differences", () => {
  assert.equal(textHash("排行榜"), textHash("排行榜"));
  assert.equal(textHash("é"), textHash("é"));
  assert.match(textHash("x"), /^[0-9a-f]{12}$/);
  assert.notEqual(textHash("a"), textHash("b"));
});

test("eachLine walks lines in narration order and marks each scene's last line", () => {
  const walked = [...eachLine(fixture())].map(({ line, last }) => `${line.id}${last ? "!" : ""}`);
  assert.deepEqual(walked, ["k7p2", "m4qa!", "x9fe", "b3tn", "r8wd!", "h2cz", "p5vs!"]);
});

test("spokenText prefers say over text", () => {
  assert.equal(spokenText({ text: "A", say: "B" }), "B");
  assert.equal(spokenText({ text: "A" }), "A");
});
