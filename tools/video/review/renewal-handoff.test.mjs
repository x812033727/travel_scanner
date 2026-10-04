import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { validateBranding } from "../core/branding.mjs";
import { fixture as sourceFixture, fixtureLexicon, writeAudioFixture } from "../core/fixtures/load.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { checkPackage, listFiles, packageFiles } from "../package/check.mjs";
import { activateHandoff, bindManualSubmission, fileInventory, prepareHandoff, shiftSrt, stageManualPublish, verifyHandoff } from "./renewal-handoff.mjs";

const sha = (b) => createHash("sha256").update(b).digest("hex");
const oldId = "11111111-1111-4111-8111-111111111111", finalId = "22222222-2222-4222-8222-222222222222", publishId = "33333333-3333-4333-8333-333333333333";
const json = (file, value) => { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, `${JSON.stringify(value)}\n`); };
const caption = "1\n00:00:00,100 --> 00:00:01,250\n第一句\n\n2\n00:00:02,500 --> 00:00:03,000\n第二句\n";
const proof = (file, role, review_id = publishId) => ({ file, review_id, role, sha256: sha(readFileSync(file)), size: readFileSync(file).length, content_type: role === "final" ? "video/mp4" : "text/plain" });

export function handoffFixture(base, { choices = { en: { metadata: true, captions: true, dub: false } } } = {}) {
  const old = path.join(base, "source"), canonical = path.join(base, "canonical"), out = path.join(base, "prepared");
  mkdirSync(old); mkdirSync(canonical); writeFileSync(path.join(canonical, "cache.wav"), "canonical cache"); writeFileSync(path.join(base, "STOP"), "held");
  for (const [name, bytes] of Object.entries({ "original.mp4": "original final", "body.mp4": "retained body", "candidate.mp4": "new final", "thumbnail.jpg": "original thumbnail", "intro.mp4": "intro", "outro.mp4": "outro", "zh-TW.srt": caption, "en.srt": caption.replace("第一句", "First sentence").replace("第二句", "Second sentence") })) writeFileSync(path.join(old, name), bytes);
  const metadata = { title: "Original title", description: "Original text\n00:00 開始\n00:10 第二章", default_language: "zh-TW", localizations: { en: { title: "English title", description: "Original translation\n00:00 Start\n00:10 Chapter two" } }, chapters: [{ time: "00:00", title: "開始" }, { time: "00:10", title: "第二章" }], contains_synthetic_media: true, disclosure_reason: "Synthetic voice and images" };
  json(path.join(old, "metadata.json"), metadata);
  const pin = validateBranding({ schema_version: 1, id: "new", intro: { file: "intro.mp4", sha256: sha("intro"), frames: 150 }, outro: { file: "outro.mp4", sha256: sha("outro"), frames: 90 } }, { base: old });
  json(path.join(old, "branding.json"), pin);
  const original = { id: oldId, gate: "final", status: "superseded", content_sha256: sha("original final"), payload: { metadata: { "zh-TW": { title: metadata.title, description: metadata.description } }, chapters: metadata.chapters }, files: [] };
  const published = { id: publishId, gate: "publish", status: "superseded", files: [proof(path.join(old, "metadata.json"), "metadata"), proof(path.join(old, "thumbnail.jpg"), "thumbnail"), proof(path.join(old, "zh-TW.srt"), "captions_zh-TW"), proof(path.join(old, "en.srt"), "captions_en"), proof(path.join(old, "original.mp4"), "final")] };
  original.files = published.files.filter((f) => f.role !== "metadata");
  const final = { id: finalId, gate: "final", status: "approved", decided_at: "2026-10-04T04:00:00Z", content_sha256: sha("new final"), files: [{ role: "final", sha256: sha("new final"), size: 9 }, { role: "captions_zh-TW", sha256: sha(shiftSrt(caption, 5000)), size: shiftSrt(caption, 5000).length }], payload: { branding_hash: pin.hash, _final_renewal: { previous_review_id: oldId, previous_sha256: sha("original final"), retained_review_ids: [oldId, publishId] }, renewal_candidate: { source: { final_review_id: oldId, final_sha256: sha("original final"), body_sha256: sha("retained body") }, candidate: { final_sha256: sha("new final"), branding_hash: pin.hash, final_bytes: 9 } } } };
  const remote = { slug: "video-one", format: "slides", locales: choices, locales_decided_at: "2026-10-04T03:00:00Z", reviews: [final, published, original] };
  const source = { original: path.join(old, "original.mp4"), body: path.join(old, "body.mp4"), body_frames: 600, package: { metadata: proof(path.join(old, "metadata.json"), "metadata"), thumbnail: proof(path.join(old, "thumbnail.jpg"), "thumbnail"), captions: { "zh-TW": proof(path.join(old, "zh-TW.srt"), "captions_zh-TW"), en: proof(path.join(old, "en.srt"), "captions_en") } } };
  const config = { slug: remote.slug, canonical, out, source, candidate: path.join(old, "candidate.mp4"), branding: path.join(old, "branding.json"), remote, mode: "manual-import", verifyMedia: async () => ({ full_decode_ok: true, video_packets: 600, seconds: 28, loudness: { integrated: -14, truePeak: -0.8 } }) };
  return { ...config, old, final, published, original, config };
}

function fixture(t, options) { const base = mkdtempSync(path.join(os.tmpdir(), "renewal-handoff-")); t.after(() => rmSync(base, { recursive: true, force: true })); return handoffFixture(base, options); }
const idle = async () => ({ stopped: true, idle: true, active_jobs: 0, upload_inactive: true });

test("manual preparation preserves originals and binds every emitted chapter/cue to retained reviews", async (t) => {
  const f = fixture(t), before = await fileInventory(f.canonical), receipt = await prepareHandoff(f.config);
  assert.deepEqual(await fileInventory(f.canonical), before);
  assert.equal(existsSync(path.join(f.out, "timeline.json")), false);
  assert.equal(existsSync(path.join(f.out, "checks.json")), false);
  assert.equal(readFileSync(path.join(f.out, "upload/captions/zh-TW.srt"), "utf8"), shiftSrt(caption, 5000));
  const meta = JSON.parse(readFileSync(path.join(f.out, "upload/metadata.json")));
  assert.equal(meta.chapters[1].time, "00:15"); assert.match(meta.localizations.en.description, /00:15 Chapter two/);
  assert.equal(meta.final_review_id, finalId); assert.equal(meta.final_sha256, f.final.content_sha256);
  assert.equal(meta.renewal_handoff.captions.en.source_sha256, f.source.package.captions.en.sha256);
  assert.equal(readFileSync(path.join(f.out, "upload/thumbnail.jpg"), "utf8"), "original thumbnail");
  await verifyHandoff({ receipt, remote: f.remote });
});

test("stale approval, upload session and changed owner language choice refuse transfer", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config);
  for (const patch of [{ youtube_upload_session: {} }, { youtube_publish_at: "now" }, { youtube_video_id: "existing" }]) await assert.rejects(verifyHandoff({ receipt, remote: { ...f.remote, ...patch } }), /activity prevents/);
  f.final.status = "pending"; await assert.rejects(verifyHandoff({ receipt, remote: f.remote }), /not owner-approved/); f.final.status = "approved";
  f.remote.locales.ja = { metadata: true }; await assert.rejects(verifyHandoff({ receipt, remote: f.remote }), /choice changed/);
});

test("source and prepared byte tampering cannot be hidden by changing an approval id", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config);
  writeFileSync(path.join(f.canonical, "cache.wav"), "new source"); await assert.rejects(verifyHandoff({ receipt, remote: f.remote }), /canonical source changed/);
  writeFileSync(path.join(f.canonical, "cache.wav"), "canonical cache");
  writeFileSync(path.join(f.out, "final.mp4"), "other final"); await assert.rejects(verifyHandoff({ receipt, remote: f.remote }), /snapshot bytes changed/);
});

test("activation requires drained worker and global STOP, archives originals and remains held", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config);
  await assert.rejects(activateHandoff({ receipt, readRemote: async () => f.remote, workerIdle: async () => ({ stopped: true, idle: false, active_jobs: 1 }) }), /still active/);
  assert.equal(readFileSync(path.join(f.canonical, "cache.wav"), "utf8"), "canonical cache");
  // Failed attempt is deliberately not auto-retried. A fresh preparation is required.
  assert.equal(JSON.parse(readFileSync(`${f.canonical}.handoff-${receipt.id}.json`)).phase, "failed-held");
});

test("successful activation preserves archive and requires fresh owner readback", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config); let reads = 0;
  const result = await activateHandoff({ receipt, readRemote: async () => { reads++; return f.remote; }, workerIdle: idle });
  assert.equal(result.activation.phase, "activated-held"); assert.equal(reads, 3);
  assert.equal(readFileSync(path.join(receipt.archive, "cache.wav"), "utf8"), "canonical cache");
  assert.equal(readFileSync(path.join(f.canonical, "final.mp4"), "utf8"), "new final");
  assert.ok(existsSync(path.join(f.canonical, "STOP")));
  await assert.rejects(activateHandoff({ receipt, readRemote: async () => f.remote, workerIdle: idle }), /already attempted/);
});

test("promotion failure rolls back exact originals without deleting candidate or archive evidence", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config);
  await assert.rejects(activateHandoff({ receipt, readRemote: async () => f.remote, workerIdle: idle, rename: (from, to) => { if (from === f.out) throw new Error("promotion interrupted"); renameSync(from, to); } }), /promotion interrupted/);
  assert.equal(readFileSync(path.join(f.canonical, "cache.wav"), "utf8"), "canonical cache"); assert.ok(existsSync(path.join(f.out, "final.mp4")));
  assert.equal(JSON.parse(readFileSync(`${f.canonical}.handoff-${receipt.id}.json`)).phase, "failed-held");
});

test("owner activity starting during promotion triggers rollback and keeps STOP", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config); let calls = 0;
  await assert.rejects(activateHandoff({ receipt, readRemote: async () => ++calls === 3 ? { ...f.remote, youtube_sync: {} } : f.remote, workerIdle: idle }), /activity prevents/);
  const journal = JSON.parse(readFileSync(`${f.canonical}.handoff-${receipt.id}.json`)); assert.equal(journal.phase, "failed-held", JSON.stringify(journal));
  assert.ok(existsSync(path.join(f.out, "STOP"))); assert.equal(readFileSync(path.join(f.canonical, "cache.wav"), "utf8"), "canonical cache");
});

test("missing translations and renewed dubs remain holds rather than stale ready or fake skips", async (t) => {
  const f = fixture(t, { choices: { ja: { metadata: true, captions: true, dub: true } } }), receipt = await prepareHandoff(f.config);
  assert.equal(receipt.holds.length, 3); for (const kind of ["metadata", "caption", "dub"]) assert.ok(receipt.holds.some((v) => v.includes(kind)));
  await assert.rejects(stageManualPublish({ workdir: f.out, client: {} }), /remains held/);
});

test("an explicit base-only review preserves pending selected languages and does not deadlock their source", async (t) => {
  const f = fixture(t, { choices: { en: { metadata: true, captions: true, dub: true } } }); await prepareHandoff(f.config);
  const choice = structuredClone(f.remote.locales); let posted;
  const client = { project: async () => f.remote, submit: async (_slug, body) => { posted = body; const review = { ...body, id: publishId, status: "pending" }; f.remote.reviews.unshift(review); return review; } };
  const result = await stageManualPublish({ workdir: f.out, client, baseOnly: true, uploadInactive: async () => true, send: async (_client, _slug, file, role) => proof(file, role) });
  assert.equal(result.status, "pending"); assert.equal(posted.payload.base_only, true); assert.ok(posted.payload.pending_language_sources.some((v) => v.includes("dub")));
  assert.equal(posted.payload.final_review_id, finalId); assert.deepEqual(f.remote.locales, choice);
  assert.equal(JSON.parse(readFileSync(path.join(f.out, "review/manual-publish-submission.json"))).status, "confirmed");
});

test("an original final payload can supply manual text without a fabricated timeline", async (t) => {
  const f = fixture(t, { choices: {} });
  f.source.package.metadata = { kind: "final-payload", review_id: oldId }; f.source.package.disclosure = { synthetic: true, reason: "Owner package disclosure" };
  const receipt = await prepareHandoff(f.config);
  const meta = JSON.parse(readFileSync(path.join(f.out, "upload/metadata.json")));
  assert.equal(meta.renewal_handoff.source_metadata.kind, "final-payload"); assert.match(meta.renewal_handoff.source_metadata.sha256, /^[a-f0-9]{64}$/); assert.equal(receipt.holds.length, 0);
});

test("caption text/offset must match the exact approved replacement attachment", async (t) => {
  const f = fixture(t); f.final.files.find((v) => v.role === "captions_zh-TW").sha256 = sha(caption);
  await assert.rejects(prepareHandoff(f.config), /shifted default captions differ/);
  assert.ok(existsSync(path.join(f.out, "STOP"))); assert.ok(existsSync(path.join(f.canonical, "cache.wav")));
});

test("changed original body or failed fresh decode cannot create a transfer receipt", async (t) => {
  const f = fixture(t); writeFileSync(f.source.body, "wrong body"); await assert.rejects(prepareHandoff(f.config), /source binding/); assert.equal(existsSync(f.out), false);
  writeFileSync(f.source.body, "retained body"); f.config.verifyMedia = async () => ({ full_decode_ok: false, video_packets: 600 });
  await assert.rejects(prepareHandoff(f.config), /proof is incomplete/); assert.equal(existsSync(f.out), false);
});

test("SRT transfer validates all cues, negative shifts and chronology", () => {
  assert.match(shiftSrt(caption, 5000), /00:00:07,500 --> 00:00:08,000/);
  assert.throws(() => shiftSrt(caption, -5000), /invalid timing/);
  assert.throws(() => shiftSrt(caption.replace("2\n", "3\n"), 5000), /invalid or empty/);
  assert.throws(() => shiftSrt(caption.replace("00:00:02,500", "00:00:00,000"), 0), /invalid timing/);
});

test("manual publish stages actual emitted bytes and a lost POST response is never resubmitted", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config); let submissions = 0;
  const client = { project: async () => f.remote, submit: async () => { submissions++; throw new Error("lost response"); } };
  await assert.rejects(stageManualPublish({ workdir: f.out, client, uploadInactive: async () => true, send: async (_client, _slug, file, role) => proof(file, role) }), /lost response/);
  assert.equal(submissions, 1); assert.ok(existsSync(path.join(f.out, "review/manual-publish-submission.json")));
  await assert.rejects(stageManualPublish({ workdir: f.out, client }), /already attempted/); assert.equal(submissions, 1);
  assert.equal(receipt.owner_final.review_id, finalId);
});

test("a forged package-ok flag cannot accept changed bytes or incomplete parts", async (t) => {
  const f = fixture(t); await prepareHandoff(f.config);
  const metadata = JSON.parse(readFileSync(path.join(f.out, "upload/metadata.json"))), digest = sha(readFileSync(path.join(f.out, "upload/metadata.json")));
  const files = packageFiles([...listFiles(path.join(f.out, "upload")).keys()]).map((v) => proof(path.join(f.out, "upload", v.path), v.role));
  const report = checkPackage({ files: listFiles(path.join(f.out, "upload")), metadata, finalSha256: f.final.content_sha256, approvedSha256: f.final.content_sha256, metadataSha256: digest, locales: ["zh-TW", "en"], descriptionLocales: ["zh-TW", "en"] });
  const body = { gate: "publish", content_sha256: digest, payload: { package: report }, files };
  const bound = await bindManualSubmission({ body, remote: f.remote, workdir: f.out }); assert.equal(bound.payload.final_review_id, finalId);
  writeFileSync(path.join(f.out, "upload/captions/en.srt"), caption); await assert.rejects(bindManualSubmission({ body, remote: f.remote, workdir: f.out }), /attachment changed/);
});

test("normal handoff retains actual narration/timeline and rejects a new document after prepare", async (t) => {
  const f = fixture(t), doc = sourceFixture(); doc.slug = f.slug;
  const project = { doc, lexicon: fixtureLexicon() };
  const timeline = writeAudioFixture({ fps: 30, total_frames: 600, speech_hash: speechHash(doc, project.lexicon), lines: [{ id: "aaaa", start_frame: 0, end_frame: 600, audio_samples: 960000 }] }, f.old);
  json(path.join(f.old, "checks.json"), { ok: true, speech_hash: timeline.speech_hash, visual_hash: visualHash(doc), narration_sha256: timeline.audio_evidence.narration_sha256, metrics: { frames: 600 } });
  writeFileSync(path.join(f.old, "final.mp4"), "retained body");
  const receipt = await prepareHandoff({ ...f.config, mode: "normal", source: { ...f.source, workdir: f.old }, project });
  assert.equal(sha(readFileSync(path.join(f.out, "timeline.json"))), sha(readFileSync(path.join(f.old, "timeline.json"))));
  assert.equal(sha(readFileSync(path.join(f.out, "narration.wav"))), sha(readFileSync(path.join(f.old, "narration.wav"))));
  assert.equal(JSON.parse(readFileSync(path.join(f.out, "checks.json"))).metrics.frames, 840);
  await verifyHandoff({ receipt, remote: f.remote, project });
  project.doc.youtube.title += " changed";
  await assert.rejects(verifyHandoff({ receipt, remote: f.remote, project }), /document or lexicon changed/);
});

test("manual original-cut range records packet provenance without inventing a missing body container hash", async (t) => {
  const f = fixture(t, { choices: {} });
  const receipt = await prepareHandoff({ ...f.config, source: { ...f.source, body: undefined, body_from_original: true, old_intro_frames: 0, old_intro_ms: 0 } });
  assert.equal(receipt.source.body_proof.kind, "original-cut-range");
  assert.equal(receipt.source.body_proof.sha256, sha("original final"));
  assert.equal(receipt.source.body_sha256, sha("retained body"));
  assert.equal(receipt.source.body_proof.candidate_body_container_unavailable, true);
  assert.equal(existsSync(path.join(f.out, "build/body.mp4")), false);
  await verifyHandoff({ receipt, remote: f.remote });
});
