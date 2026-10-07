import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { sandbox } from "../core/fixtures/load.mjs";
import { pinBranding, validateBranding } from "../core/branding.mjs";
import { captionLocalesOf, metadataLocalesOf, writeLanguages } from "../core/stages.mjs";
import { captionsItem, checkPackage, descriptionsItem, disclosureItem, filesItem, listFiles, PACKAGE_ITEM_IDS, packageFiles, packageLocales, packageReport, readPackageReport, skipReason } from "./check.mjs";

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

test("each language's own thumbnail metadata.json lists must be there and travels as thumbnail_<locale>; the skipped ones are only notes", () => {
  const withThumbs = { ...metadata(), thumbnails: { en: "thumbnails/en.jpg" }, skipped_thumbnail_locales: { ja: "i18n/ja.json has no thumbnail words" } };
  const present = new Map([...files(), ["thumbnails/en.jpg", 12]]);
  const ok = filesItem({ files: present, metadata: withThumbs, finalSha256: FINAL, approvedSha256: FINAL });
  assert.equal(ok.ok, true);
  assert.match(ok.detail, /^final\.mp4, thumbnail\.jpg, thumbnails\/en\.jpg, metadata\.json;/);
  const missing = filesItem({ files: files(), metadata: withThumbs, finalSha256: FINAL, approvedSha256: FINAL });
  assert.deepEqual([missing.ok, missing.detail], [false, "thumbnails/en.jpg is listed but missing"]);
  assert.deepEqual(packageFiles(["thumbnails/en.jpg", "thumbnails/zh-CN.jpg", "thumbnails/notes.txt"]), [
    { path: "thumbnails/en.jpg", role: "thumbnail_en", content_type: "image/jpeg" },
    { path: "thumbnails/zh-CN.jpg", role: "thumbnail_zh-CN", content_type: "image/jpeg" },
  ]);
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
  const { report, files: listed, finalSha256 } = await readPackageReport(box.workdir);
  assert.equal(report.ok, true, JSON.stringify(report.items));
  assert.equal(report.final_sha256, sha(bytes));
  assert.equal(finalSha256, sha(final), "the publish gate reuses the hash for a compilation's download entry");
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

test("an unchanged approved final cannot publish a package with a stale brand binding or changed pin", async () => {
  const box = sandbox();
  const upload = path.join(box.workdir, "upload");
  mkdirSync(path.join(upload, "captions"), { recursive: true });
  const final = Buffer.from("branded approved cut");
  writeFileSync(path.join(upload, "final.mp4"), final);
  writeFileSync(path.join(upload, "captions", "zh-TW.srt"), "1\n00:00:05,000 --> 00:00:06,000\nx\n");
  writeFileSync(path.join(upload, "description.zh-TW.txt"), "title\n\nbody\n");
  writeLanguages(box.workdir, { locales: {} });
  const selection = validateBranding({ schema_version: 1, id: "v1", intro: { file: "intro.mp4", sha256: "a".repeat(64), frames: 150 }, outro: { file: "outro.mp4", sha256: "b".repeat(64), frames: 90 } }, { base: box.workdir });
  pinBranding(box.workdir, selection);
  writeFileSync(path.join(box.workdir, "checks.json"), JSON.stringify({ branding: { hash: selection.hash, intro_frames: 150, outro_frames: 90 } }));
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", file: "final.mp4", sha256: sha(final), approved_at: "2026-09-30T00:00:00Z" }] }));
  const record = { ...metadata(), final_sha256: sha(final), thumbnail: null, localizations: {}, captions: ["captions/zh-TW.srt"] };
  const metadataPath = path.join(upload, "metadata.json");
  writeFileSync(metadataPath, JSON.stringify(record));
  const unbound = await readPackageReport(box.workdir);
  assert.equal(unbound.report.ok, false);
  assert.match(unbound.report.items[0].detail, /selected and applied branding/);
  writeFileSync(metadataPath, JSON.stringify({ ...record, branding_hash: selection.hash }));
  assert.equal((await readPackageReport(box.workdir)).report.ok, true);
  pinBranding(box.workdir, validateBranding({ ...selection, hash: undefined, intro: { ...selection.intro, sha256: "d".repeat(64) } }));
  const changed = await readPackageReport(box.workdir);
  assert.equal(changed.report.ok, false);
  assert.match(changed.report.items[0].detail, /selected and applied branding/);
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

// The owner's choice as readLanguages returns it, and the locales package and readPackageReport
// derive from it around the narration (packageLocalesWanted).
const chosen = (locales, narration = "zh-TW") => {
  const languages = { locales, decided_at: "2026-10-04T10:00:00Z" };
  return { languages, locales: captionLocalesOf(languages, narration), descriptionLocales: metadataLocalesOf(languages, narration) };
};
const checked = (present, record, choice = {}) => checkPackage({ files: present, metadata: record, finalSha256: FINAL, approvedSha256: FINAL, metadataSha256: "m".repeat(64), ...choice });
const failing = (report) => Object.fromEntries(report.items.filter((item) => !item.ok).map((item) => [item.id, item.detail]));
const without = (present, ...names) => {
  const copy = new Map(present);
  for (const name of names) copy.delete(name);
  return copy;
};
const EN_CHOICE = { en: { metadata: true, captions: true, dub: false } };

test("a zh-TW-only choice refuses a package still carrying English parts, each part on its own", () => {
  const zhOnly = chosen({});
  // The probe's package: English description, captions, localization and language choice left over.
  const leftover = checked(files(), { ...metadata(), language_choice: EN_CHOICE }, zhOnly);
  assert.equal(leftover.ok, false);
  assert.deepEqual(failing(leftover), {
    files: "metadata.json was written for another language choice; run package again",
    descriptions: "titles and descriptions the language choice does not have: en (description.en.txt, localizations.en); run package again",
    captions: "caption files the language choice does not have: en (captions/en.srt); run package again",
  });

  // The clean zh-TW package passes.
  const clean = without(files(), "description.en.txt", "captions/en.srt");
  const cleanRecord = { ...metadata(), localizations: {}, captions: ["captions/zh-TW.srt"], skipped_caption_locales: {}, language_choice: {} };
  const control = checked(clean, cleanRecord, zhOnly);
  assert.equal(control.ok, true, JSON.stringify(control.items));
  assert.deepEqual(control.items.slice(1, 3).map((item) => item.detail), ["descriptions for zh-TW", "caption files for zh-TW"]);

  // Every leftover part fails on its own, in its own item.
  assert.deepEqual(failing(checked(new Map([...clean, ["description.en.txt", 30]]), cleanRecord, zhOnly)), { descriptions: "titles and descriptions the language choice does not have: en (description.en.txt); run package again" });
  assert.deepEqual(failing(checked(clean, { ...cleanRecord, localizations: { en: { title: "t", description: "d" } } }, zhOnly)), { descriptions: "titles and descriptions the language choice does not have: en (localizations.en); run package again" });
  assert.deepEqual(failing(checked(clean, { ...cleanRecord, default_language: "en" }, zhOnly)), { descriptions: "titles and descriptions the language choice does not have: en (default_language); run package again" });
  assert.deepEqual(failing(checked(new Map([...clean, ["captions/en.srt", 20]]), cleanRecord, zhOnly)), { captions: "caption files the language choice does not have: en (captions/en.srt); run package again" });
  assert.deepEqual(failing(checked(new Map([...clean, ["captions/en.srt", 20]]), { ...cleanRecord, captions: ["captions/en.srt", "captions/zh-TW.srt"] }, zhOnly)), { captions: "caption files the language choice does not have: en (captions/en.srt); run package again" });
  assert.deepEqual(failing(checked(clean, { ...cleanRecord, language_choice: EN_CHOICE }, zhOnly)), { files: "metadata.json was written for another language choice; run package again" });
  assert.deepEqual(failing(checked(new Map([...clean, ["thumbnails/en.jpg", 12]]), { ...cleanRecord, thumbnails: { en: "thumbnails/en.jpg" } }, zhOnly)), { files: "language thumbnails the language choice does not have: en (thumbnails/en.jpg); run package again" });
  assert.deepEqual(failing(checked(new Map([...clean, ["dubs/en.m4a", 40]]), { ...cleanRecord, dubs: [{ locale: "en", file: "dubs/en.m4a", format: "m4a" }] }, zhOnly)), { files: "dub tracks the language choice does not have: en (dubs/en.m4a); run package again" });

  // A chosen part still missing fails as before.
  assert.deepEqual(failing(checked(clean, { ...cleanRecord, language_choice: { ja: { metadata: true, captions: false, dub: false } } }, chosen({ ja: { metadata: true, captions: false, dub: false } }))), { descriptions: "no description for ja" });
});

test("without a choice nothing extra is refused: a package from before the panel and the explicit locales of a renewed hand-off", () => {
  const extras = new Map([...files(), ["dubs/ko.m4a", 40], ["thumbnails/ja.jpg", 12]]);
  const record = { ...metadata(), language_choice: EN_CHOICE, thumbnails: { ja: "thumbnails/ja.jpg" } };
  assert.equal(checked(extras, record).ok, true, "legacy: every locale, whatever else the package holds");
  assert.equal(checked(extras, { ...record, skipped_caption_locales: {} }, { locales: ["zh-TW"], descriptionLocales: ["zh-TW"] }).ok, true, "locales given without a choice keep today's rule");
});

test("valid part choices pass: mixed parts, a dub choosing its captions, skipped captions, absent or given-up dubs, an English narration and a compilation", () => {
  // English titles only; Japanese captions and a Japanese dub.
  const mixed = { en: { metadata: true, captions: false, dub: false }, ja: { metadata: false, captions: true, dub: true } };
  const present = new Map([["final.mp4", 100], ["thumbnail.jpg", 10], ["metadata.json", 50], ["captions/zh-TW.srt", 20], ["captions/ja.srt", 20], ["description.zh-TW.txt", 30], ["description.en.txt", 30], ["dubs/ja.m4a", 40], ["thumbnails/ja.jpg", 12], ["thumbnails/en.jpg", 12]]);
  const record = {
    ...metadata(),
    thumbnails: { en: "thumbnails/en.jpg", ja: "thumbnails/ja.jpg" },
    captions: ["captions/ja.srt", "captions/zh-TW.srt"],
    skipped_caption_locales: {},
    dubs: [{ locale: "ja", file: "dubs/ja.m4a", format: "m4a", total_frames: 900, tempo_max: 1 }],
    skipped_dub_locales: {},
    language_choice: mixed,
  };
  const ok = checked(present, record, chosen(mixed));
  assert.equal(ok.ok, true, JSON.stringify(ok.items));
  assert.deepEqual(ok.items.slice(1, 3).map((item) => item.detail), ["descriptions for zh-TW, en", "caption files for zh-TW, ja"]);

  // A dub chooses its captions: the choice as the site sent it ({ dub: true }) is the same choice.
  assert.equal(checked(present, { ...record, language_choice: { en: { metadata: true }, ja: { dub: true } } }, chosen(mixed)).ok, true);
  // The chosen dub given up with its reason, or still being made, or a compilation's (which has none).
  const noDub = without(present, "dubs/ja.m4a");
  assert.equal(checked(noDub, { ...record, dubs: [], skipped_dub_locales: { ja: "the voice was refused" } }, chosen(mixed)).ok, true);
  assert.equal(checked(noDub, { ...record, dubs: [], skipped_dub_locales: {} }, chosen(mixed)).ok, true);
  assert.equal(checked(noDub, { ...record, dubs: [], skipped_dub_locales: {}, compilation: true, download: "upload/final.mp4" }, chosen(mixed)).ok, true);
  // Chosen captions skipped with a reason.
  const skipped = checked(without(present, "captions/ja.srt"), { ...record, captions: ["captions/zh-TW.srt"], skipped_caption_locales: { ja: ["k7p2"] } }, chosen(mixed));
  assert.equal(skipped.ok, true, JSON.stringify(skipped.items));
  assert.equal(skipped.items[2].detail, "caption files for zh-TW; skipped ja (1 lines missing or older than zh-TW)");

  // Dub problems under the same choice.
  assert.deepEqual(failing(checked(noDub, record, chosen(mixed))), { files: "dubs/ja.m4a is listed but missing" });
  assert.deepEqual(failing(checked(present, { ...record, dubs: [] }, chosen(mixed))), { files: "dubs/ja.m4a is not listed in metadata.json" });
  assert.deepEqual(failing(checked(new Map([...present, ["dubs/en.m4a", 40]]), { ...record, dubs: [...record.dubs, { locale: "en", file: "dubs/en.m4a", format: "m4a" }] }, chosen(mixed))), { files: "dub tracks the language choice does not have: en (dubs/en.m4a); run package again" });
  assert.deepEqual(failing(checked(new Map([...present, ["thumbnails/ko.jpg", 12]]), { ...record, thumbnails: { ...record.thumbnails, ko: "thumbnails/ko.jpg" } }, chosen(mixed))), { files: "language thumbnails the language choice does not have: ko (thumbnails/ko.jpg); run package again" });

  // An English-narrated video: English and zh-TW always, and English chosen on its own video adds no dub.
  const english = new Map([["final.mp4", 100], ["metadata.json", 50], ["captions/en.srt", 20], ["captions/zh-TW.srt", 20], ["description.en.txt", 30], ["description.zh-TW.txt", 30]]);
  const englishRecord = { ...metadata(), default_language: "en", thumbnail: null, localizations: { "zh-TW": { title: "t", description: "d" } }, captions: ["captions/en.srt", "captions/zh-TW.srt"], skipped_caption_locales: {}, dubs: [], skipped_dub_locales: {}, language_choice: {} };
  const narratedInEnglish = checked(english, englishRecord, chosen({}, "en"));
  assert.equal(narratedInEnglish.ok, true, JSON.stringify(narratedInEnglish.items));
  assert.deepEqual(narratedInEnglish.items.slice(1, 3).map((item) => item.detail), ["descriptions for en, zh-TW", "caption files for en, zh-TW"]);
  const ownLocale = { en: { metadata: true, captions: true, dub: true } };
  assert.equal(checked(english, { ...englishRecord, language_choice: ownLocale }, chosen(ownLocale, "en")).ok, true);
  assert.deepEqual(failing(checked(new Map([...english, ["dubs/en.m4a", 40]]), { ...englishRecord, language_choice: ownLocale, dubs: [{ locale: "en", file: "dubs/en.m4a", format: "m4a" }] }, chosen(ownLocale, "en"))), { files: "dub tracks the language choice does not have: en (dubs/en.m4a); run package again" });
});

/** A work directory whose upload/ holds final.mp4 (approved), metadata.json and `parts` ({ path: text }). */
function workPackage({ record, parts, languages }) {
  const box = sandbox();
  const upload = path.join(box.workdir, "upload");
  const final = Buffer.from("the approved cut");
  mkdirSync(upload, { recursive: true });
  writeFileSync(path.join(upload, "final.mp4"), final);
  for (const [file, text] of Object.entries(parts)) {
    mkdirSync(path.dirname(path.join(upload, file)), { recursive: true });
    writeFileSync(path.join(upload, file), text);
  }
  const bytes = `${JSON.stringify({ ...record, final_sha256: sha(final) }, null, 2)}\n`;
  writeFileSync(path.join(upload, "metadata.json"), bytes);
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", file: "final.mp4", sha256: sha(final), approved_at: "2026-10-04T00:00:00Z", note: "" }] }));
  if (languages) writeLanguages(box.workdir, { locales: languages, decided_at: "2026-10-04T10:00:00Z" });
  return { workdir: box.workdir, upload, bytes };
}

const CAPTION = "1\n00:00:00,000 --> 00:00:01,000\nx\n";
const zhRecord = { ...metadata(), thumbnail: null, localizations: {}, captions: ["captions/zh-TW.srt"], skipped_caption_locales: {}, dubs: [], skipped_dub_locales: {}, language_choice: {} };

test("readPackageReport refuses a zh-TW-only work directory whose package still holds English parts, and passes the clean one", async () => {
  const zhParts = { "captions/zh-TW.srt": CAPTION, "description.zh-TW.txt": "title\n\nbody\n" };
  const clean = workPackage({ record: zhRecord, parts: zhParts, languages: {} });
  assert.equal((await readPackageReport(clean.workdir)).report.ok, true);

  const leftover = workPackage({
    record: { ...zhRecord, localizations: { en: { title: "t", description: "d" } }, captions: ["captions/en.srt", "captions/zh-TW.srt"], language_choice: EN_CHOICE },
    parts: { ...zhParts, "captions/en.srt": CAPTION, "description.en.txt": "title\n\nbody\n" },
    languages: {},
  });
  const { report } = await readPackageReport(leftover.workdir);
  assert.equal(report.ok, false);
  assert.deepEqual(Object.keys(failing(report)), ["files", "descriptions", "captions"]);

  // A dub chosen on the site ({ dub: true }) brings its captions, and package records the choice as read.
  const dubbed = workPackage({
    record: { ...zhRecord, captions: ["captions/ja.srt", "captions/zh-TW.srt"], dubs: [{ locale: "ja", file: "dubs/ja.m4a", format: "m4a" }], language_choice: { ja: { metadata: false, captions: true, dub: true } } },
    parts: { ...zhParts, "captions/ja.srt": CAPTION, "dubs/ja.m4a": "track" },
    languages: { ja: { dub: true } },
  });
  const dub = await readPackageReport(dubbed.workdir);
  assert.equal(dub.report.ok, true, JSON.stringify(dub.report.items));
  assert.equal(dub.report.items[2].detail, "caption files for zh-TW, ja");
});

test("a package that changes while it is checked fails, and the report binds the metadata bytes it read", async () => {
  const zhParts = { "captions/zh-TW.srt": CAPTION, "description.zh-TW.txt": "title\n\nbody\n" };
  const work = workPackage({ record: zhRecord, parts: zhParts, languages: {} });
  const metadataFile = path.join(work.upload, "metadata.json");
  const changed = /upload\/ or the language choice changed while the package was being checked; check it again/;

  // metadata.json rewritten (same size) after it was read, while final.mp4 is being hashed.
  const rewritten = work.bytes.replace("a stock TTS voice", "a stock TTS VOICE");
  assert.equal(rewritten.length, work.bytes.length);
  const pending = readPackageReport(work.workdir);
  writeFileSync(metadataFile, rewritten);
  const raced = (await pending).report;
  assert.equal(raced.ok, false);
  assert.match(raced.items[0].detail, changed);
  assert.equal(raced.final_sha256, sha(work.bytes), "the hash is of the bytes the check read, not the newer file");
  const again = (await readPackageReport(work.workdir)).report;
  assert.equal(again.ok, true, JSON.stringify(again.items));
  assert.equal(again.final_sha256, sha(rewritten));

  // A leftover part copied in mid-check, then the next run sees it for what it is.
  const copying = readPackageReport(work.workdir);
  writeFileSync(path.join(work.upload, "description.en.txt"), "title\n\nbody\n");
  assert.match((await copying).report.items[0].detail, changed);
  assert.deepEqual(Object.keys(failing((await readPackageReport(work.workdir)).report)), ["descriptions"]);
  rmSync(path.join(work.upload, "description.en.txt"));

  // The language choice changed mid-check.
  const deciding = readPackageReport(work.workdir);
  writeLanguages(work.workdir, { locales: { ja: { metadata: true, captions: false, dub: false } }, decided_at: "2026-10-04T11:00:00Z" });
  assert.match((await deciding).report.items[0].detail, changed);
});

// A hand-edited metadata.json whose list or map has another type: [field, value, the item that reads it, "list" or "object"].
const MISTYPED = [
  ["captions", 5, "captions", "list"],
  ["captions", {}, "captions", "list"],
  ["captions", "captions/en.srt", "captions", "list"],
  ["captions", false, "captions", "list"],
  ["skipped_caption_locales", 5, "captions", "object"],
  ["skipped_caption_locales", [], "captions", "object"],
  ["thumbnails", "ab", "files", "object"],
  ["thumbnails", [], "files", "object"],
  ["thumbnail_variants", {}, "files", "list"],
  ["localizations", "en", "descriptions", "object"],
  ["localizations", 5, "descriptions", "object"],
];
// Read only with the owner's choice.
const MISTYPED_WITH_CHOICE = [
  ["dubs", {}, "files", "list"],
  ["language_choice", "en", "files", "object"],
];

test("a list or map field of another type fails the item that reads it, naming the field, instead of throwing", () => {
  const legacy = metadata();
  const withChoice = { ...metadata(), skipped_caption_locales: {}, language_choice: EN_CHOICE };
  assert.equal(checked(files(), legacy).ok, true, "the controls pass");
  assert.equal(checked(files(), withChoice, chosen(EN_CHOICE)).ok, true);
  const cases = [...MISTYPED.map((each) => [...each, legacy, {}]), ...[...MISTYPED, ...MISTYPED_WITH_CHOICE].map((each) => [...each, withChoice, chosen(EN_CHOICE)])];
  for (const [field, value, id, kind, record, choice] of cases) {
    const name = `${field}: ${JSON.stringify(value)}${choice.languages ? " with a choice" : ""}`;
    const report = checked(files(), { ...record, [field]: value }, choice);
    assert.equal(report.ok, false, name);
    assert.deepEqual(Object.keys(failing(report)), [id], name);
    assert.ok(failing(report)[id].includes(`metadata.json ${field} is not ${kind === "list" ? "a list" : "an object"}; run package again`), `${name}: ${failing(report)[id]}`);
  }
  // A string is not read character by character, nor a map's keys as indexes.
  assert.equal(failing(checked(files(), { ...legacy, captions: "captions/en.srt" })).captions, "metadata.json captions is not a list; run package again");
  assert.equal(failing(checked(files(), { ...legacy, localizations: "en" })).descriptions, "metadata.json localizations is not an object; run package again");
  assert.deepEqual(packageLocales({ ...legacy, localizations: "en" }), ["zh-TW"], "the publish payload's locales leave it out");
  // Absent or null reads as empty, as before.
  assert.equal(checked(files(), { ...legacy, captions: null, thumbnails: null, localizations: null }).ok, true);
});

test("a metadata.json that is not an object fails every item for that reason", () => {
  for (const record of [5, [], "metadata", true]) {
    const report = checked(files(), record);
    assert.deepEqual(failing(report), Object.fromEntries(PACKAGE_ITEM_IDS.map((id) => [id, "metadata.json is not an object; run package again"])), JSON.stringify(record));
  }
});

test("readPackageReport, which review-push --gate publish sends, reports a caption list that is a number instead of throwing", async () => {
  const zhParts = { "captions/zh-TW.srt": CAPTION, "description.zh-TW.txt": "title\n\nbody\n" };
  for (const languages of [{}, undefined]) {
    const work = workPackage({ record: { ...zhRecord, captions: 5, ...(languages ? {} : { skipped_caption_locales: { en: "x", ja: "x", ko: "x", "zh-CN": "x" } }) }, parts: zhParts, languages });
    const { report } = await readPackageReport(work.workdir);
    assert.equal(report.ok, false);
    assert.equal(report.final_sha256, sha(work.bytes), "bound to the bytes read, like any failing package");
    assert.deepEqual(failing(report), { captions: "metadata.json captions is not a list; run package again" }, languages ? "with a choice" : "without one");
  }
});
