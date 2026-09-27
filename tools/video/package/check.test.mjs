import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { sandbox } from "../core/fixtures/load.mjs";
import { writeLanguages } from "../core/stages.mjs";
import { captionsItem, checkPackage, descriptionsItem, disclosureItem, filesItem, listFiles, PACKAGE_ITEM_IDS, packageFiles, packageReport, readPackageReport, skipReason } from "./check.mjs";

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const FINAL = "f".repeat(64);

const files = () =>
  new Map([
    ["final.mp4", 100],
    ["thumbnail.jpg", 10],
    ["metadata.json", 50],
    ["captions/zh-TW.srt", 20],
    ["captions/en.srt", 20],
    ["description.zh-TW.txt", 30],
    ["description.en.txt", 30],
    ["UPLOAD.md", 5],
  ]);

const metadata = () => ({
  default_language: "zh-TW",
  localizations: { en: { title: "t", description: "d" } },
  final_sha256: FINAL,
  thumbnail: "thumbnail.jpg",
  captions: ["captions/en.srt", "captions/zh-TW.srt"],
  skipped_caption_locales: { ja: ["k7p2", "m4qa"], ko: "no translation (i18n/ko.json missing)", "zh-CN": "no translation (i18n/zh-CN.json missing)" },
  contains_synthetic_media: false,
  disclosure_reason: "slides read by a stock TTS voice",
});

test("a complete package passes every item, and the report binds to metadata.json's hash", () => {
  const report = checkPackage({ files: files(), metadata: metadata(), finalSha256: FINAL, approvedSha256: FINAL, metadataSha256: "m".repeat(64) });
  assert.equal(report.ok, true);
  assert.equal(report.final_sha256, "m".repeat(64));
  assert.deepEqual(report.items.map((item) => item.id), PACKAGE_ITEM_IDS);
  const byId = Object.fromEntries(report.items.map((item) => [item.id, item.detail]));
  assert.equal(byId.files, "final.mp4, thumbnail.jpg, metadata.json; final.mp4 is the approved final (ffffffffffff)");
  assert.equal(byId.descriptions, "descriptions for zh-TW, en");
  assert.equal(byId.captions, "caption files for zh-TW, en; skipped ja (2 lines missing or older than zh-TW), ko (no translation (i18n/ko.json missing)), zh-CN (no translation (i18n/zh-CN.json missing))");
  assert.equal(byId.disclosure, "no disclosure needed: slides read by a stock TTS voice");
  assert.throws(() => packageReport(report.items.slice(1), "x"), /package items must be exactly files, descriptions, captions, disclosure/);
});

test("each item fails for its own reason", () => {
  const present = files();
  assert.match(filesItem({ files: present, metadata: metadata(), finalSha256: "a".repeat(64), approvedSha256: FINAL }).detail, /final\.mp4 is not the approved final \(aaaaaaaaaaaa vs ffffffffffff\)/);
  assert.match(filesItem({ files: present, metadata: metadata(), finalSha256: FINAL, approvedSha256: null }).detail, /no approved final to compare/);
  assert.match(filesItem({ files: present, metadata: { ...metadata(), final_sha256: "b".repeat(64) }, finalSha256: FINAL, approvedSha256: FINAL }).detail, /metadata\.json records another final \(bbbbbbbbbbbb\)/);
  const noThumbnail = files();
  noThumbnail.delete("thumbnail.jpg");
  assert.match(filesItem({ files: noThumbnail, metadata: metadata(), finalSha256: FINAL, approvedSha256: FINAL }).detail, /thumbnail\.jpg is missing/);
  assert.equal(filesItem({ files: noThumbnail, metadata: { ...metadata(), thumbnail: null }, finalSha256: FINAL, approvedSha256: FINAL }).ok, true, "no thumbnail when the video has none");
  const noFinal = files();
  noFinal.delete("final.mp4");
  assert.match(filesItem({ files: noFinal, metadata: metadata(), finalSha256: null, approvedSha256: FINAL }).detail, /final\.mp4 is missing/);
  assert.match(filesItem({ files: noFinal, metadata: null, finalSha256: null, approvedSha256: null }).detail, /metadata\.json is missing; final\.mp4 is missing/);

  const noEnglish = files();
  noEnglish.delete("description.en.txt");
  assert.equal(descriptionsItem({ files: noEnglish, metadata: metadata() }).detail, "no description for en");
  const empty = files();
  empty.set("description.zh-TW.txt", 0);
  assert.equal(descriptionsItem({ files: empty, metadata: metadata() }).detail, "no description for zh-TW");

  assert.equal(skipReason({ ja: [] }, "ja"), null, "an empty list is no reason");
  assert.equal(skipReason({ ja: "  " }, "ja"), null);
  assert.equal(skipReason(undefined, "ja"), null);
  const unexplained = captionsItem({ files: present, metadata: { ...metadata(), skipped_caption_locales: { ja: [] } } });
  assert.equal(unexplained.ok, false);
  assert.equal(unexplained.detail, "ja: no caption file and no reason in skipped_caption_locales; ko: no caption file and no reason in skipped_caption_locales; zh-CN: no caption file and no reason in skipped_caption_locales");
  const listedButGone = captionsItem({ files: present, metadata: { ...metadata(), captions: ["captions/en.srt", "captions/ja.srt"] } });
  assert.equal(listedButGone.detail, "captions/ja.srt is listed but missing");
  assert.equal(captionsItem({ files: present, metadata: metadata(), locales: ["zh-TW", "en"] }).detail, "caption files for zh-TW, en", "the configured locales can be narrowed");

  assert.match(disclosureItem({ metadata: { ...metadata(), contains_synthetic_media: undefined } }).detail, /no contains_synthetic_media answer; run package again/);
  assert.match(disclosureItem({ metadata: { ...metadata(), disclosure_reason: "" } }).detail, /no disclosure_reason/);
  assert.equal(disclosureItem({ metadata: { ...metadata(), contains_synthetic_media: true, disclosure_reason: "a drama" } }).detail, "tick altered or synthetic content: a drama");
  const broken = checkPackage({ files: noThumbnail, metadata: metadata(), finalSha256: FINAL, approvedSha256: FINAL, metadataSha256: "m".repeat(64) });
  assert.equal(broken.ok, false);
  assert.deepEqual(broken.items.filter((item) => !item.ok).map((item) => item.id), ["files"]);
});

test("the package's files get the review roles the site knows, and UPLOAD.md stays home", () => {
  assert.deepEqual(packageFiles(files().keys()), [
    { path: "captions/en.srt", role: "captions_en", content_type: "text/plain" },
    { path: "captions/zh-TW.srt", role: "captions_zh-TW", content_type: "text/plain" },
    { path: "description.en.txt", role: "description_en", content_type: "text/plain" },
    { path: "description.zh-TW.txt", role: "description_zh-TW", content_type: "text/plain" },
    { path: "final.mp4", role: "final", content_type: "video/mp4" },
    { path: "metadata.json", role: "metadata", content_type: "application/json" },
    { path: "thumbnail.jpg", role: "thumbnail", content_type: "image/jpeg" },
  ]);
  assert.deepEqual(packageFiles(["notes.txt", "captions/en.vtt"]), [], "anything unknown is left out");
});

test("readPackageReport reads upload/ and compares final.mp4 with the final gate's approval", async () => {
  const box = sandbox();
  const upload = path.join(box.workdir, "upload");
  mkdirSync(path.join(upload, "captions"), { recursive: true });
  const final = Buffer.from("the approved cut");
  writeFileSync(path.join(upload, "final.mp4"), final);
  writeFileSync(path.join(upload, "captions", "zh-TW.srt"), "1\n00:00:00,000 --> 00:00:01,000\nx\n");
  writeFileSync(path.join(upload, "description.zh-TW.txt"), "title\n\nbody\n");
  writeFileSync(path.join(upload, "UPLOAD.md"), "# steps\n");
  const record = { ...metadata(), final_sha256: sha(final), thumbnail: null, localizations: {}, captions: ["captions/zh-TW.srt"], skipped_caption_locales: { en: "no translation", ja: "no translation", ko: "no translation", "zh-CN": "no translation" } };
  const bytes = `${JSON.stringify(record, null, 2)}\n`;
  writeFileSync(path.join(upload, "metadata.json"), bytes);
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", file: "final.mp4", sha256: sha(final), approved_at: "2026-09-27T00:00:00Z", note: "" }] }));
  const { report, files: listed } = await readPackageReport(box.workdir);
  assert.equal(report.ok, true, JSON.stringify(report.items));
  assert.equal(report.final_sha256, sha(bytes));
  assert.deepEqual([...listed.keys()].sort(), ["UPLOAD.md", "captions/zh-TW.srt", "description.zh-TW.txt", "final.mp4", "metadata.json"]);
  assert.equal(listFiles(path.join(box.workdir, "nowhere")).size, 0);

  // An older approval: the package holds a final.mp4 the owner never approved.
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", file: "final.mp4", sha256: "0".repeat(64), approved_at: "2026-09-27T00:00:00Z", note: "" }] }));
  const stale = await readPackageReport(box.workdir);
  assert.equal(stale.report.ok, false);
  assert.match(stale.report.items[0].detail, /is not the approved final/);
  const none = await readPackageReport(path.join(box.work, "missing"));
  assert.equal(none.report.final_sha256, null);
  assert.ok(none.report.items.every((item) => !item.ok));
});

test("with the owner's choice, descriptions and captions are checked for zh-TW and the chosen locales, read from languages.json", async () => {
  const present = files();
  assert.equal(descriptionsItem({ files: present, metadata: metadata(), locales: ["zh-TW", "en"] }).detail, "descriptions for zh-TW, en");
  assert.equal(descriptionsItem({ files: present, metadata: metadata(), locales: ["zh-TW", "ja"] }).detail, "no description for ja", "a chosen locale without its file fails, whatever metadata.json lists");
  assert.equal(descriptionsItem({ files: present, metadata: { ...metadata(), localizations: {} }, locales: ["zh-TW"] }).ok, true);
  const zhOnly = checkPackage({ files: present, metadata: { ...metadata(), skipped_caption_locales: {} }, finalSha256: FINAL, approvedSha256: FINAL, metadataSha256: "m".repeat(64), locales: ["zh-TW"], descriptionLocales: ["zh-TW"] });
  assert.equal(zhOnly.ok, true, "nothing chosen: no reason needed for the other locales");
  assert.equal(zhOnly.items[2].detail, "caption files for zh-TW");

  const box = sandbox();
  const upload = path.join(box.workdir, "upload");
  mkdirSync(path.join(upload, "captions"), { recursive: true });
  const final = Buffer.from("the approved cut");
  writeFileSync(path.join(upload, "final.mp4"), final);
  writeFileSync(path.join(upload, "captions", "zh-TW.srt"), "1\n00:00:00,000 --> 00:00:01,000\nx\n");
  writeFileSync(path.join(upload, "description.zh-TW.txt"), "title\n\nbody\n");
  const record = { ...metadata(), final_sha256: sha(final), thumbnail: null, localizations: {}, captions: ["captions/zh-TW.srt"], skipped_caption_locales: {} };
  writeFileSync(path.join(upload, "metadata.json"), `${JSON.stringify(record, null, 2)}\n`);
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", file: "final.mp4", sha256: sha(final), approved_at: "2026-09-27T00:00:00Z", note: "" }] }));
  const noChoice = await readPackageReport(box.workdir);
  assert.equal(noChoice.report.ok, false, "without a choice every locale needs captions or a reason");
  assert.match(noChoice.report.items[2].detail, /en: no caption file and no reason/);
  writeLanguages(box.workdir, { locales: {}, decided_at: "2026-09-27T10:00:00Z" });
  const zh = await readPackageReport(box.workdir);
  assert.equal(zh.report.ok, true, JSON.stringify(zh.report.items));
  assert.deepEqual(zh.report.items.slice(1, 3).map((item) => item.detail), ["descriptions for zh-TW", "caption files for zh-TW"]);
  writeLanguages(box.workdir, { locales: { ja: { metadata: true, captions: true, dub: false } }, decided_at: "2026-09-27T10:00:00Z" });
  const ja = await readPackageReport(box.workdir);
  assert.equal(ja.report.ok, false);
  assert.deepEqual(ja.report.items.slice(1, 3).map((item) => item.detail), ["no description for ja", "ja: no caption file and no reason in skipped_caption_locales"]);
});
