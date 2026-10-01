import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { fixture, fixtureLexicon } from "../core/fixtures/load.mjs";
import { validateBranding, presentationTimeline } from "../core/branding.mjs";
import { buildCues, toSrt } from "../core/captions.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { captionLocalesOf, localeTexts, metadataLocalesOf } from "../core/stages.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { dubFingerprint, dubScript, translationHash } from "../dubs/plan.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { bindRenewalSubmission, ownerClient, stageRenewal, submitRenewal, uploadCandidate, validateCandidate } from "./renewal.mjs";

const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const oldId = "11111111-1111-4111-8111-111111111111";
const finalId = "22222222-2222-4222-8222-222222222222";
const publishId = "33333333-3333-4333-8333-333333333333";
const json = (file, value) => { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, JSON.stringify(value)); };
const fileEntry = (file, role, type = "text/plain") => { const raw = readFileSync(file); return { role, sha256: sha(raw), size: raw.length, content_type: type }; };
function receipt() {
  const digest = sha("new final");
  return { schema_version: 1, kind: "long-final-renewal", site: "https://mokaair.com", slug: "video-one", source: { final_review_id: oldId, final_sha256: sha("old final"), body_sha256: sha("body") }, candidate: { final_sha256: digest, branding_hash: sha("branding"), final_bytes: 9 }, review: { gate: "final", content_sha256: digest, summary: "replacement", payload: { branding_hash: sha("branding"), manual_review: true }, files: [{ role: "final", sha256: digest, size: 9, content_type: "video/mp4" }, { role: "preview", sha256: sha("preview"), size: 7, content_type: "video/mp4" }] } };
}

test("owner submission binds fresh version and original identity, creates only human pending", async () => {
  const candidate = receipt(), calls = [];
  const result = await submitRenewal({ receipt: candidate, reason: "New bookends", site: candidate.site, request: async (method, slug, body) => {
    calls.push({ method, slug, body });
    return method === "GET" ? { version: sha("fresh"), final_review_id: calls.length === 1 ? oldId : finalId, final_sha256: calls.length === 1 ? candidate.source.final_sha256 : candidate.candidate.final_sha256 } : { ...candidate.review, id: finalId, status: "pending" };
  } });
  assert.equal(result.status, "pending");
  assert.deepEqual(calls.map((call) => call.method), ["GET", "POST", "GET"]);
  assert.equal(calls[1].body.expected_version, sha("fresh"));
  assert.equal(calls[1].body.expected_final_review_id, oldId);
  assert.equal(calls[1].body.review, candidate.review);
});

test("changed original and failed writes never trigger a blind POST retry", async () => {
  const candidate = receipt();
  let writes = 0;
  await assert.rejects(submitRenewal({ receipt: candidate, reason: "update", site: candidate.site, request: async (method) => { if (method === "POST") writes++; return { version: sha("v"), final_review_id: finalId, final_sha256: candidate.source.final_sha256 }; } }), /original final changed/);
  assert.equal(writes, 0);
  await assert.rejects(submitRenewal({ receipt: candidate, reason: "update", site: candidate.site, request: async (method) => { if (method === "POST") { writes++; throw new Error("ambiguous network result"); } return { version: sha("v"), final_review_id: oldId, final_sha256: candidate.source.final_sha256 }; } }), /ambiguous/);
  assert.equal(writes, 1);
});

test("owner session cannot leak through an arbitrary origin, redirect or retry", async () => {
  assert.throws(() => ownerClient({ site: "http://example.com", session: "secret" }), /HTTPS/);
  assert.throws(() => ownerClient({ site: "https://user:pass@example.com", session: "secret" }), /origin/);
  let calls = 0;
  const request = ownerClient({ session: "secret", fetch: async (_url, init) => { calls++; assert.equal(init.redirect, "error"); assert.equal(init.headers.Cookie, "travel_access=secret"); assert.equal(init.headers.Origin, "https://mokaair.com"); return Response.json({ code: "busy" }, { status: 503 }); } });
  await assert.rejects(request("POST", "video-one", {}), /503/);
  assert.equal(calls, 1);
  assert.throws(() => validateCandidate(receipt(), "video-one", "https://other.example"), /another site/);
});

test("staging snapshots files without reporting, submitting or changing the originals", async (t) => {
  const base = mkdtempSync(path.join(os.tmpdir(), "renewal-stage-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const from = path.join(base, "candidate"), out = path.join(base, "staged");
  mkdirSync(from);
  const original = path.join(base, "original.mp4"), body = path.join(base, "body.mp4"), branding = path.join(base, "branding.json");
  writeFileSync(original, "old"); writeFileSync(body, "body"); writeFileSync(path.join(from, "final.mp4"), "new");
  writeFileSync(path.join(from, "thumbnail.png"), "existing thumbnail");
  writeFileSync(path.join(base, "intro.mp4"), "intro"); writeFileSync(path.join(base, "outro.mp4"), "outro");
  json(branding, { schema_version: 1, id: "v2", intro: { file: "intro.mp4", sha256: sha("intro"), frames: 150 }, outro: { file: "outro.mp4", sha256: sha("outro"), frames: 90 } });
  json(path.join(from, "meta.json"), { slug: "video-one", title: "New final", description: "New final description" });
  const uploads = [];
  const result = await stageRenewal({ from, out, original, body, branding,
    client: { site: "https://mokaair.com", project: async () => ({ format: "slides", reviews: [{ id: oldId, gate: "final", status: "approved", content_sha256: sha("old") }] }) },
    measure: async (file) => ({ probe: { streams: [{ codec_type: "video", codec_name: "h264", width: 1920, height: 1080, r_frame_rate: "30/1", pix_fmt: "yuv420p", duration: file === body ? "30" : "38" }] }, loudness: null }),
    encode: async (_file, target) => writeFileSync(target, "preview"),
    upload: async (_site, _slug, file, role) => { uploads.push(role); return fileEntry(file, role, "video/mp4"); },
  });
  assert.deepEqual(uploads, ["final", "preview", "thumbnail"]);
  assert.equal(readFileSync(path.join(out, "thumbnail.png"), "utf8"), "existing thumbnail");
  assert.equal(result.source.final_sha256, sha("old"));
  assert.equal(result.review.payload.manual_review, true);
  assert.equal(result.review.payload.qa, undefined);
  assert.equal(readFileSync(original, "utf8"), "old");
  assert.equal(readFileSync(path.join(from, "final.mp4"), "utf8"), "new");
  assert.ok(existsSync(path.join(out, "renewal-candidate.json")));
  await assert.rejects(stageRenewal({ from, out, original, body, branding }), /new directory/);
});

test("candidate file receipt requires confirmed complete storage", async (t) => {
  const base = mkdtempSync(path.join(os.tmpdir(), "renewal-file-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const file = path.join(base, "final.mp4"); writeFileSync(file, "cut");
  await assert.rejects(uploadCandidate({ part: async () => ({ complete: false }) }, "v", file, "final"), /incomplete/);
  assert.equal((await uploadCandidate({ part: async () => ({ complete: true }) }, "v", file, "final")).sha256, sha("cut"));
  const png = path.join(base, "thumbnail.png"); writeFileSync(png, "existing png");
  assert.equal((await uploadCandidate({ part: async () => ({ complete: true }) }, "v", png, "thumbnail")).content_type, "image/png");
});

/** Actual emitted manifest bytes are reusable by the Python consumer contract probe. */
export function languageFixture(base) {
  const project = { doc: fixture(), lexicon: fixtureLexicon(), translations: {} };
  const workdir = path.join(base, "work"); mkdirSync(path.join(workdir, "upload", "captions"), { recursive: true });
  const lines = [...eachLine(project.doc)].map(({ line }, index) => ({ id: line.id, start_frame: index * 150, end_frame: (index + 1) * 150 }));
  const timeline = { fps: 30, speech_hash: speechHash(project.doc, project.lexicon), total_frames: lines.length * 150, lines, chapters: [] };
  const pin = validateBranding({ schema_version: 1, id: "new-brand", intro: { file: "intro.mp4", sha256: sha("intro"), frames: 150 }, outro: { file: "outro.mp4", sha256: sha("outro"), frames: 90 } }, { base });
  const applied = { hash: pin.hash, intro_frames: 150, outro_frames: 90, body_frames: timeline.total_frames };
  const locales = Object.fromEntries(["en", "ja", "ko", "zh-CN"].map((locale) => [locale, { metadata: true, captions: true, dub: false }]));
  for (const locale of Object.keys(locales)) project.translations[locale] = { title: `${locale} title`, description: `${locale} description`, lines: Object.fromEntries([...eachLine(project.doc)].map(({ line }) => [line.id, { text: `${locale} ${line.text}`, source_hash: textHash(line.text) }])) };
  const metadata = { ...composeMetadata({ ...project, timeline: presentationTimeline(timeline, applied) }).metadata, final_sha256: sha("new-cut"), branding_hash: pin.hash, language_choice: locales, captions: ["zh-TW", ...Object.keys(locales)].map((locale) => `captions/${locale}.srt`) };
  json(path.join(workdir, "timeline.json"), timeline); json(path.join(workdir, "branding.json"), pin);
  json(path.join(workdir, "checks.json"), { ok: true, speech_hash: timeline.speech_hash, visual_hash: visualHash(project.doc), branding: applied });
  json(path.join(workdir, "languages.json"), { locales, decided_at: "2026-10-01T00:00:00Z" });
  json(path.join(workdir, "captions", "manifest.json"), { speech_hash: timeline.speech_hash, branding_hash: pin.hash });
  json(path.join(workdir, "upload", "metadata.json"), metadata); writeFileSync(path.join(workdir, "upload", "final.mp4"), "new-cut");
  const files = [], payload = { locales: {} };
  const { texts } = localeTexts(project.doc, project.translations);
  for (const locale of ["zh-TW", ...Object.keys(locales)]) {
    const caption = path.join(workdir, "upload", "captions", `${locale}.srt`);
    writeFileSync(caption, toSrt(buildCues(presentationTimeline(timeline, applied), texts[locale], locale).cues));
    if (locale === "zh-TW") continue;
    const description = path.join(workdir, "upload", `description.${locale}.txt`);
    writeFileSync(description, `${metadata.localizations[locale].title}\n\n${metadata.localizations[locale].description}\n`);
    files.push(fileEntry(description, `description_${locale}`), fileEntry(caption, `captions_${locale}`));
    payload.locales[locale] = { metadata: "ready", captions: "ready" };
  }
  const final = { id: finalId, gate: "final", status: "approved", content_sha256: metadata.final_sha256, payload: { _final_renewal: { previous_review_id: oldId }, branding_hash: pin.hash } };
  const publish = { id: publishId, gate: "publish", status: "approved", content_sha256: fileEntry(path.join(workdir, "upload", "metadata.json"), "metadata").sha256 };
  const remote = { slug: project.doc.slug, format: "slides", locales, reviews: [publish, final] };
  const body = { gate: "languages", content_sha256: sha("old-language-manifest"), payload, files };
  const uploaded = new Map();
  const upload = async (_request, _slug, file, role, type) => { const item = fileEntry(file, role, type); uploaded.set(item.sha256, readFileSync(file)); return item; };
  return { project, workdir, remote, body, upload, uploaded };
}

/** Narration-aware bytes exported for the real Python consumer probe, not a second contract. */
export function narrationFixture(base, { locales = { ja: { metadata: false, captions: true, dub: false } } } = {}) {
  const sample = languageFixture(base), { project, workdir, remote } = sample;
  project.doc.narration_locale = "en";
  project.doc.youtube.title = "A renewed English story";
  project.doc.youtube.description = "The original English narration.";
  for (const { line } of eachLine(project.doc)) line.text = `Original English narration for ${line.id}.`;
  project.translations = Object.fromEntries(["zh-TW", "ja", "ko", "zh-CN"].map((locale) => [locale, {
    title: `${locale} translated title`, description: `${locale} translated description`,
    lines: Object.fromEntries([...eachLine(project.doc)].map(({ line }) => [line.id, { text: `${locale} translation of ${line.id}`, source_hash: textHash(line.text) }])),
  }]));
  const timeline = JSON.parse(readFileSync(path.join(workdir, "timeline.json")));
  timeline.speech_hash = speechHash(project.doc, project.lexicon);
  const checks = JSON.parse(readFileSync(path.join(workdir, "checks.json")));
  Object.assign(checks, { speech_hash: timeline.speech_hash, visual_hash: visualHash(project.doc) });
  json(path.join(workdir, "timeline.json"), timeline); json(path.join(workdir, "checks.json"), checks);
  const languages = { locales: structuredClone(locales), decided_at: "2026-10-01T00:00:00Z" };
  remote.locales = structuredClone(locales);
  json(path.join(workdir, "languages.json"), languages);
  json(path.join(workdir, "captions", "manifest.json"), { speech_hash: timeline.speech_hash, branding_hash: checks.branding.hash });
  const presented = presentationTimeline(timeline, checks.branding);
  const metadata = { ...composeMetadata({ ...project, timeline: presented, locales: metadataLocalesOf(languages, "en") }).metadata,
    final_sha256: remote.reviews[1].content_sha256, branding_hash: checks.branding.hash,
    language_choice: languages.locales, captions: captionLocalesOf(languages, "en").map((locale) => `captions/${locale}.srt`),
  };
  const metadataFile = path.join(workdir, "upload", "metadata.json"); json(metadataFile, metadata);
  const allFiles = [fileEntry(metadataFile, "metadata", "application/json"), fileEntry(path.join(workdir, "upload", "final.mp4"), "final", "video/mp4")];
  const { texts } = localeTexts(project.doc, project.translations);
  for (const locale of captionLocalesOf(languages, "en")) {
    const caption = path.join(workdir, "upload", "captions", `${locale}.srt`);
    writeFileSync(caption, toSrt(buildCues(presented, texts[locale], locale).cues));
    allFiles.push(fileEntry(caption, `captions_${locale}`));
  }
  for (const locale of metadataLocalesOf(languages, "en")) {
    const fields = locale === "en" ? metadata : metadata.localizations[locale];
    const description = path.join(workdir, "upload", `description.${locale}.txt`);
    writeFileSync(description, `${fields.title}\n\n${fields.description}\n`);
    allFiles.push(fileEntry(description, `description_${locale}`));
  }
  remote.reviews[0].content_sha256 = allFiles[0].sha256;
  const languageFiles = allFiles.filter((file) => Object.entries(locales).some(([locale, choice]) => choice.metadata && file.role === `description_${locale}` || (choice.captions || choice.dub) && file.role === `captions_${locale}`));
  sample.body = { gate: "languages", content_sha256: sha("unbound language review"), payload: { locales: Object.fromEntries(Object.entries(locales).map(([locale, choice]) => [locale, { ...(choice.metadata ? { metadata: "ready" } : {}), ...(choice.captions || choice.dub ? { captions: "ready" } : {}) }])) }, files: languageFiles };
  const publishBody = { gate: "publish", content_sha256: allFiles[0].sha256, payload: { package: { ok: true } }, files: allFiles };
  return { ...sample, publishBody };
}

for (const selection of ["ja captions", "none", "own metadata and dub"]) {
  test(`renewed English narration follows package locale helpers (${selection})`, async (t) => {
    const base = mkdtempSync(path.join(os.tmpdir(), "renewal-narration-")); t.after(() => rmSync(base, { recursive: true, force: true }));
    const locales = selection === "none" ? {} : selection === "own metadata and dub" ? { en: { metadata: true, captions: true, dub: true } } : { ja: { metadata: false, captions: true, dub: false } };
    const sample = narrationFixture(base, { locales });
    const publish = await bindRenewalSubmission({ ...sample, body: sample.publishBody });
    assert.equal(publish.payload.final_review_id, finalId);
    assert.ok(publish.files.some((file) => file.role === "captions_en"));
    assert.ok(publish.files.some((file) => file.role === "captions_zh-TW"));
    const result = await bindRenewalSubmission(sample);
    const manifest = JSON.parse(sample.uploaded.get(result.content_sha256));
    assert.deepEqual(manifest.choice.locales, locales);
    if (selection === "own metadata and dub") {
      assert.equal(manifest.locales.en.dub.status, "skipped");
      assert.match(manifest.locales.en.dub.reason, /original narration/);
      assert.equal(result.files.some((file) => file.role === "dub_en"), false);
    }
  });
}

for (const broken of ["automatic CC missing", "automatic CC stale", "automatic CC attachment missing", "automatic metadata missing", "duplicate original dub"]) {
  test(`renewed English narration refuses ${broken} before submission`, async (t) => {
    const base = mkdtempSync(path.join(os.tmpdir(), "renewal-narration-refuse-")); t.after(() => rmSync(base, { recursive: true, force: true }));
    const sample = narrationFixture(base, { locales: { en: { metadata: true, captions: true, dub: true }, ja: { metadata: false, captions: true, dub: false } } });
    const caption = path.join(sample.workdir, "upload", "captions", "zh-TW.srt");
    if (broken === "automatic CC missing") rmSync(caption);
    if (broken === "automatic CC stale") writeFileSync(caption, readFileSync(caption, "utf8").replace("00:00:05,000", "00:00:00,000"));
    if (broken === "automatic CC attachment missing") sample.publishBody.files = sample.publishBody.files.filter((file) => file.role !== "captions_zh-TW");
    if (broken === "automatic metadata missing") {
      const file = path.join(sample.workdir, "upload", "metadata.json"), metadata = JSON.parse(readFileSync(file));
      delete metadata.localizations["zh-TW"]; json(file, metadata);
      const entry = fileEntry(file, "metadata", "application/json"); sample.publishBody.files[0] = entry; sample.publishBody.content_sha256 = entry.sha256;
    }
    if (broken === "duplicate original dub") sample.publishBody.files.push({ role: "dub_en", sha256: sha("duplicate"), size: 9, content_type: "audio/mp4" });
    await assert.rejects(bindRenewalSubmission({ ...sample, body: sample.publishBody }));
    assert.equal(sample.uploaded.size, 0);
  });
}

test("renewed five-language output binds real metadata/manifest bytes and new final identity", async (t) => {
  const base = mkdtempSync(path.join(os.tmpdir(), "renewal-bind-")); t.after(() => rmSync(base, { recursive: true, force: true }));
  const fixture = languageFixture(base);
  const result = await bindRenewalSubmission(fixture);
  assert.equal(result.payload.final_review_id, finalId);
  const manifest = JSON.parse(fixture.uploaded.get(result.content_sha256));
  assert.equal(manifest.source.final.review_id, finalId);
  assert.equal(manifest.source.publish.review_id, publishId);
  assert.equal(manifest.source.script, null);
  assert.equal(manifest.source.branding_hash, fixture.remote.reviews[1].payload.branding_hash);
  assert.equal(manifest.files.length, 9);
  assert.equal(result.files.filter((file) => file.role === "languages_manifest").length, 1);
  assert.equal(manifest.files.some((file) => file.role === "languages_manifest"), false);
  assert.equal(sha(readFileSync(path.join(fixture.workdir, "review", "languages.json"))), result.content_sha256, "review-pull sees the exact approved manifest");
  const firstCaption = readFileSync(path.join(fixture.workdir, "upload", "captions", "en.srt"), "utf8");
  assert.match(firstCaption, /00:00:05,000/);
});

for (const problem of ["old final", "old branding", "pending final", "changed choice", "old caption bytes", "pending publish", "old description bytes"]) {
  test(`renewed producer rejects ${problem} without publishing a review`, async (t) => {
    const base = mkdtempSync(path.join(os.tmpdir(), "renewal-refuse-")); t.after(() => rmSync(base, { recursive: true, force: true }));
    const fixture = languageFixture(base);
    if (problem === "old final") writeFileSync(path.join(fixture.workdir, "upload", "final.mp4"), "old-cut");
    if (problem === "old branding") fixture.remote.reviews[1].payload.branding_hash = sha("old-branding");
    if (problem === "pending final") fixture.remote.reviews[1].status = "pending";
    if (problem === "pending publish") fixture.remote.reviews[0].status = "pending";
    if (problem === "changed choice") fixture.remote.locales.en.dub = true;
    if (problem === "old caption bytes") fixture.body.files.find((file) => file.role === "captions_en").sha256 = sha("captions on old offsets");
    if (problem === "old description bytes") fixture.body.files.find((file) => file.role === "description_en").sha256 = sha("old description");
    await assert.rejects(bindRenewalSubmission(fixture));
    assert.equal(fixture.uploaded.size, 0);
  });
}

test("legacy non-renewed submissions retain their existing body", async () => {
  const body = { gate: "publish" };
  assert.equal(await bindRenewalSubmission({ body, remote: { reviews: [] } }), body);
});

for (const wrong of ["none", "default captions", "foreign captions", "chapters", "padded choices", "missing dub", "skipped dub", "current dub", "old packaged dub"]) {
  test(`renewed publish verifies default narration timing (${wrong}) before adding an id`, async (t) => {
    const base = mkdtempSync(path.join(os.tmpdir(), "renewal-publish-")); t.after(() => rmSync(base, { recursive: true, force: true }));
    const fixture = languageFixture(base), uploadDir = path.join(fixture.workdir, "upload");
    const metadataFile = path.join(uploadDir, "metadata.json"), captionFile = path.join(uploadDir, "captions", "zh-TW.srt");
    if (wrong === "default captions") writeFileSync(captionFile, readFileSync(captionFile, "utf8").replace("00:00:05,000", "00:00:00,000"));
    if (wrong === "chapters") {
      const metadata = JSON.parse(readFileSync(metadataFile)); metadata.chapters = [{ at: "00:05", title: "standalone short intro" }]; json(metadataFile, metadata);
    }
    if (wrong === "padded choices") {
      const metadata = JSON.parse(readFileSync(metadataFile)); metadata.language_choice.unknown = { metadata: false, captions: false, dub: false }; json(metadataFile, metadata);
    }
    if (wrong === "foreign captions") {
      const foreign = path.join(uploadDir, "captions", "en.srt");
      writeFileSync(foreign, readFileSync(foreign, "utf8").replace("00:00:05,000", "00:00:00,000"));
      Object.assign(fixture.body.files.find((file) => file.role === "captions_en"), fileEntry(foreign, "captions_en"));
    }
    if (wrong.includes("dub")) {
      fixture.remote.locales.en.dub = true;
      const metadata = JSON.parse(readFileSync(metadataFile)); metadata.language_choice.en.dub = true;
      json(path.join(fixture.workdir, "languages.json"), { locales: fixture.remote.locales });
      if (wrong === "skipped dub") {
        metadata.skipped_dub_locales = { en: "Voice generation skipped by the owner" };
        json(path.join(fixture.workdir, "dubs", "en", "skipped.json"), { reason: metadata.skipped_dub_locales.en });
      }
      if (["current dub", "old packaged dub"].includes(wrong)) {
        const timeline = JSON.parse(readFileSync(path.join(fixture.workdir, "timeline.json")));
        const branding = JSON.parse(readFileSync(path.join(fixture.workdir, "checks.json"))).branding;
        const dub = { ...presentationTimeline(timeline, branding), content_end_frame: 150 + timeline.total_frames, body_total_frames: timeline.total_frames, speech_hash: timeline.speech_hash, translation_hash: translationHash(dubScript(fixture.project.doc, fixture.project.translations.en, "en").doc), speech_fingerprint: dubFingerprint(fixture.project, "en"), branding_hash: branding.hash, format: "m4a" };
        json(path.join(fixture.workdir, "dubs", "en", "timeline.json"), dub);
        writeFileSync(path.join(fixture.workdir, "dubs", "en.m4a"), "new dub track");
        mkdirSync(path.join(uploadDir, "dubs"));
        writeFileSync(path.join(uploadDir, "dubs", "en.m4a"), wrong === "current dub" ? "new dub track" : "old dub track");
        metadata.dubs = [{ locale: "en", file: "dubs/en.m4a", branding_hash: branding.hash }];
      }
      json(metadataFile, metadata);
    }
    const metadata = fileEntry(metadataFile, "metadata", "application/json");
    const body = { gate: "publish", content_sha256: metadata.sha256, payload: { package: { ok: true } }, files: [metadata, fileEntry(captionFile, "captions_zh-TW"), ...fixture.body.files] };
    if (["none", "skipped dub", "current dub"].includes(wrong)) assert.equal((await bindRenewalSubmission({ ...fixture, body })).payload.final_review_id, finalId);
    else await assert.rejects(bindRenewalSubmission({ ...fixture, body }), /presentation timeline|stale offsets|compact choice|published dub/);
  });
}
