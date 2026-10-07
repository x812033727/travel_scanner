import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, renameSync, rmSync, symlinkSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import test from "node:test";
import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { validateBranding } from "../core/branding.mjs";
import { fixture as sourceFixture, fixtureLexicon, writeAudioFixture } from "../core/fixtures/load.mjs";
import { speechHash, visualHash } from "../core/timeline.mjs";
import { checkPackage, listFiles, packageFiles } from "../package/check.mjs";
import { activateHandoff, bindManualSubmission, fileInventory, nativeApprovedFinalAdapter, nativeLiteralLexicon, prepareApprovedFinalHandoff, prepareHandoff, readManualLanguageSource, renameRollbackDirectory, shiftSrt, stageManualPublish, verifyHandoff, verifyRetainedMedia, verifyRetainedPictures } from "./renewal-handoff.mjs";

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

test("a hand-edited metadata.json with mistyped captions or localizations is refused by field, never a TypeError", async (t) => {
  const cases = [
    ["captions a number", (m) => { m.captions = 5; }, /metadata\.json captions is not a list/],
    ["captions an object", (m) => { m.captions = {}; }, /metadata\.json captions is not a list/],
    ["captions missing", (m) => { delete m.captions; }, /metadata\.json captions is not a list/],
    ["localizations missing", (m) => { delete m.localizations; }, /metadata\.json localizations is not an object/],
    ["localizations a list", (m) => { m.localizations = ["en"]; }, /metadata\.json localizations is not an object/],
  ];
  for (const baseOnly of [true, false]) {
    for (const [what, edit, refusal] of cases) {
      const f = fixture(t, { choices: {} }); await prepareHandoff(f.config);
      const file = path.join(f.out, "upload/metadata.json"), metadata = JSON.parse(readFileSync(file));
      edit(metadata); writeFileSync(file, JSON.stringify(metadata));
      let submissions = 0;
      const client = { project: async () => f.remote, submit: async () => { submissions++; return {}; } };
      await assert.rejects(stageManualPublish({ workdir: f.out, client, baseOnly, uploadInactive: async () => true, send: async (_client, _slug, path_, role) => proof(path_, role) }), (error) => {
        assert.ok(!(error instanceof TypeError), `${what}: ${error.message}`);
        assert.match(error.message, refusal, what);
        return true;
      });
      assert.equal(submissions, 0, what);
      assert.equal(existsSync(path.join(f.out, "review/manual-publish-submission.json")), false, `${what}: nothing staged`);
    }
  }
  // bindManualSubmission with a base-only body reads the same fields through the same guard; after
  // prepare, metadata.json is itself one of the receipt's file proofs, so an edit is refused there
  // first. Either way it is a refusal, never a TypeError.
  for (const [what, edit, refusal] of cases) {
    const f = fixture(t, { choices: {} }); await prepareHandoff(f.config);
    const file = path.join(f.out, "upload/metadata.json"), metadata = JSON.parse(readFileSync(file));
    edit(metadata); writeFileSync(file, JSON.stringify(metadata));
    const files = packageFiles([...listFiles(path.join(f.out, "upload")).keys()]).map((v) => proof(path.join(f.out, "upload", v.path), v.role));
    const body = { gate: "publish", content_sha256: sha(readFileSync(file)), payload: { base_only: true, package: {} }, files };
    await assert.rejects(bindManualSubmission({ body, remote: f.remote, workdir: f.out }), (error) => {
      assert.ok(!(error instanceof TypeError), `bind, ${what}: ${error.message}`);
      assert.ok(refusal.test(error.message) || /manual package attachment changed: metadata/.test(error.message), `bind, ${what}: ${error.message}`);
      return true;
    });
  }
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

const windowCaption = "1\n00:00:00,100 --> 00:00:03,000\n文字12\n\n2\n00:00:03,000 --> 00:00:09,000\n句內；末句\n\n3\n00:00:10,100 --> 00:00:19,000\n數字34？「引號」\n";
function currentFixture(t) {
  const f = windowFixture(t), evidence = {};
  const values = { evidence_script: f.source.adapter.project.doc, evidence_body_timeline: f.source.adapter.timeline, "captions_zh-TW": shiftSrt(windowCaption, 5000), narration: "current AAC preview", thumbnail: "current thumbnail" };
  for (const [role, value] of Object.entries(values)) {
    const file = path.join(f.old, `current-${role}`); if (typeof value === "object") json(file, value); else writeFileSync(file, value);
    evidence[role] = { ...proof(file, role, finalId), content_type: role === "narration" ? "audio/mp4" : role.startsWith("evidence") ? "application/json" : "text/plain" };
  }
  f.final.files = [f.final.files[0], ...Object.values(evidence)];
  f.final.payload = { ...f.final.payload, manual_review: true, metadata: { "zh-TW": { title: "Current title", description: "Current chapter text\n00:00 開始\n00:12 新章" } }, chapters: [{ time: "00:00", title: "開始" }, { time: "00:12", title: "新章" }], body_change: { new_script: evidence.evidence_script, new_body_timeline: evidence.evidence_body_timeline, new_body: { sha256: sha("unavailable changed master") }, new_voice: { sha256: sha("unavailable raw WAV") }, speech_hash: f.source.adapter.timeline.speech_hash, full_playback_owner_accepted: false, audio_owner_accepted: false, source_body_changed: true } };
  const actor = "55555555-5555-4555-8555-555555555555";
  const decisionAuthority = { slug: f.slug, status: "approved", review_id: finalId, content_sha256: f.final.content_sha256, decided_at: f.final.decided_at, decided_by_user_id: actor, approval_audits: [{ id: "66666666-6666-4666-8666-666666666666", action: "video_review_approved", actor_user_id: actor, target: `video_review:${finalId}`, metadata_json: { slug: f.slug, gate: "final", sha256: f.final.content_sha256 } }] };
  const media = { scope: "approved-current-media-identity", preservation_claim: false, full_decode_ok: true, video_packets: 600, body_range_sha256: sha("actual packets"), body_audio_pcm_sha256: sha("actual decoded current PCM"), narration: { sha256: evidence.narration.sha256, full_decode_ok: true, raw_voice_claimed: false, listening_approval_claimed: false } };
  return { ...f, config: { ...f.config, source: { evidence, adapter: f.source.adapter, disclosure: { synthetic: true, reason: "Current synthetic narration" } }, decisionAuthority, verifyMedia: async () => media } };
}

test("changed approved final is an independent current identity, keeps current captions/chapters and never fabricates old-body or listening approval", async (t) => {
  const f = currentFixture(t), receipt = await prepareApprovedFinalHandoff(f.config), contract = await readManualLanguageSource({ workdir: f.out, remote: f.remote });
  assert.equal(receipt.mode, "approved-final-body-range"); assert.equal(receipt.media.preservation_claim, false);
  assert.equal(contract.source.body.sha256, f.final.content_sha256); assert.equal(contract.source.body.file, "final.mp4");
  assert.equal(contract.source.historical_declarations.audio_owner_accepted, false); assert.notEqual(contract.source.body.sha256, contract.source.historical_declarations.new_body.sha256);
  assert.deepEqual(JSON.parse(readFileSync(path.join(f.out, "upload/metadata.json"))).chapters, f.final.payload.chapters);
  assert.equal(readFileSync(path.join(f.out, "upload/captions/zh-TW.srt"), "utf8"), shiftSrt(windowCaption, 5000));
  for (const file of ["checks.json", "narration.wav", "approvals.json", "build/body.mp4"]) assert.equal(existsSync(path.join(f.out, file)), false);
  await verifyHandoff({ receipt, remote: f.remote });
  f.final.payload.body_change.audio_owner_accepted = true;
  await assert.rejects(readManualLanguageSource({ workdir: f.out, remote: f.remote }), /owner decision|authority changed/);
});

test("current final source rejects audit actor, missing actual narration, stale evidence and claimed preservation", async (t) => {
  for (const [name, change, pattern] of [["wrong actor", (f) => { f.config.decisionAuthority.approval_audits[0].actor_user_id = oldId; }, /matching approval audit/], ["missing narration", (f) => { delete f.config.source.evidence.narration; }, /narration/], ["wrong source script", (f) => { f.final.payload.body_change.new_script = { sha256: sha("old script") }; }, /changed script/], ["false preservation", (f) => { f.config.verifyMedia = async () => ({ scope: "approved-current-media-identity", preservation_claim: true }); }, /identity evidence/]]) await t.test(name, async (child) => { const f = currentFixture(child); change(f); await assert.rejects(prepareApprovedFinalHandoff(f.config), pattern); });
});

test("current-source native aliases preserve valid IDs, every raw word/window and speech identity, and reject collisions", (t) => {
  const f = currentFixture(t), raw = structuredClone(f.config.source.adapter), hash = sha("raw current script bytes");
  raw.project.doc.slug = "ai-real-world-01-image-trust"; raw.project.doc.scenes[0].lines[0].id = "ext8-01-01"; raw.timeline.lines[0].id = "ext8-01-01"; raw.timeline.speech_hash = speechHash(raw.project.doc, raw.project.lexicon);
  const before = structuredClone(raw), adapted = nativeApprovedFinalAdapter(raw.project, raw.timeline, hash), alias = adapted.line_id_aliases.map["ext8-01-01"];
  assert.match(alias, /^r[a-f0-9]{7}$/); assert.equal(adapted.project.doc.scenes[0].lines[1].id, "bbbb"); assert.deepEqual(raw, before);
  assert.equal(adapted.project.doc.scenes[0].lines[0].text, raw.project.doc.scenes[0].lines[0].text); assert.equal(adapted.timeline.lines[0].end_frame, raw.timeline.lines[0].end_frame);
  assert.equal(adapted.line_id_aliases.raw_speech_hash, raw.timeline.speech_hash); assert.notEqual(adapted.timeline.speech_hash, raw.timeline.speech_hash);
  raw.project.doc.scenes[0].lines[1].id = alias; raw.timeline.lines[1].id = alias; raw.timeline.speech_hash = speechHash(raw.project.doc, raw.project.lexicon);
  assert.throws(() => nativeApprovedFinalAdapter(raw.project, raw.timeline, hash), /alias collision/);
  raw.project.doc.scenes[0].lines[0].id = "unsupported-legacy-id"; raw.timeline.lines[0].id = "unsupported-legacy-id"; raw.timeline.speech_hash = speechHash(raw.project.doc, raw.project.lexicon);
  assert.throws(() => nativeApprovedFinalAdapter(raw.project, raw.timeline, hash), /only the approved/);
});

test("EP06 native literal annotation changes only the spelling allowlist, preserves speech and claims no pronunciation approval", (t) => {
  const f = currentFixture(t), project = structuredClone(f.config.source.adapter.project);
  project.doc.slug = "ai-real-world-06-digital-yesman"; project.lexicon = { schema_version: 1, terms: {} };
  project.doc.scenes[0].lines[0].text = "Anthropic 做模型。"; delete project.doc.scenes[0].lines[0].say; delete project.doc.scenes[0].lines[0].say_for;
  const before = structuredClone(project), result = nativeLiteralLexicon(project);
  assert.deepEqual(project, before); assert.deepEqual(result.lexicon, { schema_version: 1, terms: { Anthropic: null } });
  assert.equal(speechHash(project.doc, result.lexicon), speechHash(project.doc, project.lexicon));
  assert.equal(result.literal_term_annotations.listening_approval_claimed, false); assert.equal(result.literal_term_annotations.pronunciation_approval_claimed, false);
  const timeline = structuredClone(f.config.source.adapter.timeline); timeline.speech_hash = speechHash(project.doc, project.lexicon);
  assert.throws(() => nativeApprovedFinalAdapter(project, timeline, sha("different owner source")), /exact approved raw\/native speech identities/);
  project.doc.scenes[0].lines[0].text += "OpenAI。"; assert.throws(() => nativeLiteralLexicon(project), /only the EP06/);
  project.doc.scenes[0].lines[0].text = "Anthropic。"; project.lexicon.terms.Unrelated = null; assert.throws(() => nativeLiteralLexicon(project), /only the EP06/);
});

test("current readers rederive aliases and refuse jointly relabelled mapping, valid ID, words or raw evidence", async (t) => {
  const f = currentFixture(t), receipt = await prepareApprovedFinalHandoff(f.config), contractFile = path.join(f.out, "renewal-language-source.json"), original = readFileSync(contractFile);
  for (const [name, change] of [["unknown mode", (v) => { v.adapter.line_id_aliases.algorithm = "ignore-ids"; }], ["changed alias", (v) => { v.adapter.line_id_aliases.map.aaaa = "r0000000"; }]]) await t.test(name, async () => {
    const contract = JSON.parse(original); change(contract); json(contractFile, contract); receipt.files["renewal-language-source.json"].sha256 = sha(readFileSync(contractFile)); json(path.join(f.out, "renewal-handoff.json"), receipt);
    await assert.rejects(readManualLanguageSource({ workdir: f.out, remote: f.remote }), /native adapter\/alias map/);
  });
  writeFileSync(contractFile, original); receipt.files["renewal-language-source.json"].sha256 = sha(original); json(path.join(f.out, "renewal-handoff.json"), receipt);
  const projectFile = path.join(f.out, "language-adapter/project.json"), timingFile = path.join(f.out, "language-adapter/timeline.json"), projectBytes = readFileSync(projectFile), timingBytes = readFileSync(timingFile);
  for (const [name, change] of [["legal ID renamed", (p, v) => { p.doc.scenes[0].lines[1].id = "cccc"; v.lines[1].id = "cccc"; }], ["source word changed", (p) => { p.doc.scenes[0].lines[0].text += "改字"; }], ["source timing changed", (_p, v) => { v.lines[0].start_frame = 1; }]]) await t.test(name, async () => {
    const p = JSON.parse(projectBytes), timing = JSON.parse(timingBytes), contract = JSON.parse(original); change(p, timing); timing.speech_hash = speechHash(p.doc, p.lexicon); json(projectFile, p); json(timingFile, timing);
    Object.assign(contract.adapter, { project_sha256: sha(readFileSync(projectFile)), timeline_sha256: sha(readFileSync(timingFile)), doc_sha256: sha(JSON.stringify(p.doc)), speech_hash: timing.speech_hash });
    json(contractFile, contract); for (const file of ["renewal-language-source.json", "language-adapter/project.json", "language-adapter/timeline.json"]) receipt.files[file].sha256 = sha(readFileSync(path.join(f.out, file))); json(path.join(f.out, "renewal-handoff.json"), receipt);
    await assert.rejects(readManualLanguageSource({ workdir: f.out, remote: f.remote }), /native adapter\/alias map/);
  });
  writeFileSync(projectFile, projectBytes); writeFileSync(timingFile, timingBytes); writeFileSync(contractFile, original); for (const file of ["renewal-language-source.json", "language-adapter/project.json", "language-adapter/timeline.json"]) receipt.files[file].sha256 = sha(readFileSync(path.join(f.out, file))); json(path.join(f.out, "renewal-handoff.json"), receipt);
  const evidence = path.join(f.out, "approved-source/evidence_script"); writeFileSync(evidence, "changed raw source");
  await assert.rejects(readManualLanguageSource({ workdir: f.out, remote: f.remote }), /approved evidence changed/);
});
function windowFixture(t, bytes = windowCaption) {
  const f = fixture(t, { choices: {} }), doc = sourceFixture(); doc.slug = f.slug;
  doc.scenes = [{ ...doc.scenes[0], lines: [{ id: "aaaa", text: "文字12，句內；末句。", pause_after_ms: 0 }, { id: "bbbb", text: "數字34？「引號」", pause_after_ms: 0 }] }];
  const project = { doc, lexicon: fixtureLexicon(), translations: {} };
  f.source.adapter = { caption_mode: "approved-line-windows", project, timeline: { fps: 30, total_frames: 600, speech_hash: speechHash(doc, project.lexicon), lines: [{ id: "aaaa", start_frame: 0, end_frame: 300, audio_samples: 480000 }, { id: "bbbb", start_frame: 300, end_frame: 600, audio_samples: 480000 }] } };
  writeFileSync(f.source.package.captions["zh-TW"].file, bytes);
  Object.assign(f.source.package.captions["zh-TW"], proof(f.source.package.captions["zh-TW"].file, "captions_zh-TW"));
  for (const row of [f.original, f.published]) Object.assign(row.files.find((v) => v.role === "captions_zh-TW"), f.source.package.captions["zh-TW"]);
  f.final.files.find((v) => v.role === "captions_zh-TW").sha256 = sha(shiftSrt(bytes, 5000));
  return f;
}

test("explicit approved line windows retain actual split cues and pin mode, text and exact source timing", async (t) => {
  const f = windowFixture(t); await prepareHandoff(f.config);
  const contract = await readManualLanguageSource({ workdir: f.out, remote: f.remote });
  assert.equal(contract.adapter.caption_mode, "approved-line-windows");
  assert.equal(readFileSync(path.join(f.out, contract.captions_zh_TW.file), "utf8"), shiftSrt(windowCaption, 5000));
  assert.equal(existsSync(path.join(f.out, "checks.json")), false);
  const file = path.join(f.out, contract.captions_zh_TW.file);
  writeFileSync(file, readFileSync(file, "utf8").replace("00:00:05,100", "00:00:05,101"));
  await assert.rejects(readManualLanguageSource({ workdir: f.out, remote: f.remote }), /source changed|prepared source receipt/);
});

test("approved line windows cannot omit words, digits, internal punctuation, questions or source cues", async (t) => {
  const repeated = windowCaption.replace("2\n00:00:03,000 --> 00:00:09,000\n句內；末句", "2\n00:00:03,000 --> 00:00:09,000\n文字12");
  const missing = windowCaption.replace("1\n00:00:00,100 --> 00:00:03,000\n文字12\n\n", "").replace("2\n", "1\n").replace("3\n", "2\n");
  for (const [name, bytes] of [["CJK word", windowCaption.replace("末句", "末字")], ["number", windowCaption.replace("12", "13")], ["internal punctuation", windowCaption.replace("句內；末句", "句內末句")], ["question punctuation", windowCaption.replace("34？", "34")], ["quotation punctuation", windowCaption.replace("「引號」", "引號")], ["repeated cue", repeated], ["missing cue", missing], ["cross-window cue", windowCaption.replace("00:00:09,000", "00:00:10,002")]]) {
    await t.test(name, async (child) => { const f = windowFixture(child, bytes); await assert.rejects(prepareHandoff(f.config), /approved caption/); });
  }
});

test("approved source line windows require bounded integer frames in source order without overlap", async (t) => {
  for (const [name, change] of [["negative start", (v) => { v.lines[0].start_frame = -30; }], ["fractional start", (v) => { v.lines[0].start_frame = 0.5; }], ["end beyond body", (v) => { v.lines[1].end_frame = 601; }], ["overlapping line windows", (v) => { v.lines[1].start_frame = 299; }]]) {
    await t.test(name, async (child) => { const f = windowFixture(child); change(f.source.adapter.timeline); await assert.rejects(prepareHandoff(f.config), /approved caption source line order\/window/); });
  }
});

test("actual H.264 concat preserves every Annex-B byte and rejects altered pictures, parameters and timestamps", async (t) => {
  let tools;
  try { tools = await locateFfmpeg(); } catch (error) { if (error instanceof ToolMissing) { t.skip(error.message); return; } throw error; }
  const base = mkdtempSync(path.join(os.tmpdir(), "renewal-real-packets-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const body = path.join(base, "body.mp4"), final = path.join(base, "final.mp4"), intro = path.join(base, "intro.mp4"), outro = path.join(base, "outro.mp4");
  const video = ["-c:v", "libx264", "-threads", "1", "-preset", "veryfast", "-crf", "18", "-profile:v", "high", "-pix_fmt", "yuv420p", "-g", "30", "-bf", "2"];
  await runTool(tools.ffmpeg, ["-v", "error", "-f", "lavfi", "-i", "color=blue:s=1920x1080:r=30:d=2", "-f", "lavfi", "-i", "sine=frequency=220:sample_rate=48000:duration=2", ...video, "-af", "loudnorm=I=-14:TP=-1:LRA=7", "-c:a", "aac", "-b:a", "384k", "-ar", "48000", "-ac", "2", "-t", "2", body]);
  for (const [file, color] of [[intro, "red"], [outro, "green"]]) await runTool(tools.ffmpeg, ["-v", "error", "-f", "lavfi", "-i", `color=${color}:s=1920x1080:r=30:d=1`, ...video, file]);
  const list = path.join(base, "join.ffconcat");
  writeFileSync(list, `ffconcat version 1.0\n${[intro, body, outro].map((file) => `file '${file.replaceAll("\\", "/")}'`).join("\n")}\n`);
  await runTool(tools.ffmpeg, ["-v", "error", "-f", "concat", "-safe", "0", "-i", list, "-i", body, "-map", "0:v:0", "-filter_complex", "[1:a]adelay=1000|1000,apad,atrim=duration=4[a]", "-map", "[a]", "-c:v", "copy", "-c:a", "aac", "-b:a", "384k", "-ar", "48000", "-ac", "2", final]);
  const config = { body, final, branding: { intro: { frames: 30 }, outro: { frames: 30 } }, bodyFrames: 60 };
  await t.test("real concat gets exact parameter-inclusive proof plus fresh audio and full decode", async () => {
    const result = await verifyRetainedMedia(config);
    assert.equal(result.full_decode_ok, true); assert.equal(result.video_packets, 60);
    assert.equal(result.video_proof.kind, "h264-annexb-exact"); assert.equal(result.video_proof.raw_packets_identical, false);
    assert.equal(result.video_proof.source_file_sha256, sha(readFileSync(body))); assert.equal(result.video_proof.final_file_sha256, sha(readFileSync(final)));
    assert.match(result.video_proof.annexb_sha256, /^[a-f0-9]{64}$/); assert.ok(result.video_proof.annexb_bytes > 0);
  });
  const raw = path.join(base, "original.h264");
  await runTool(tools.ffmpeg, ["-v", "error", "-i", body, "-map", "0:v:0", "-c:v", "copy", "-bsf:v", "h264_mp4toannexb", "-an", "-f", "h264", raw]);
  const original = readFileSync(raw), starts = [];
  for (let i = 0; i < original.length - 3; i++) if (original[i] === 0 && original[i + 1] === 0 && (original[i + 2] === 1 || original[i + 2] === 0 && original[i + 3] === 1)) { const length = original[i + 2] === 1 ? 3 : 4; starts.push({ at: i, start: i + length, type: original[i + length] & 31 }); i += length - 1; }
  for (const [kind, type] of [["VCL", 5], ["SPS", 7]]) await t.test(`a changed ${kind} byte is refused`, async () => {
    const index = starts.findIndex((v) => v.type === type), begin = starts[index].start, end = starts[index + 1]?.at ?? original.length;
    const nal = original.subarray(begin, end), bytes = readFileSync(body), at = bytes.indexOf(nal);
    assert.ok(at >= 0, `${kind} NAL occurs in the actual MP4 packet/avcC data`);
    // Mutate the actual MP4's slice or avcC parameter bytes without remuxing:
    // unchanged timestamps ensure this exercises the parameter-inclusive proof.
    bytes[at + (type === 7 ? 3 : Math.floor(nal.length / 2))] ^= 1;
    const changed = path.join(base, `${kind}.mp4`); writeFileSync(changed, bytes);
    await assert.rejects(verifyRetainedPictures({ ...config, body: changed }), /changes retained H.264 pictures or codec parameters/);
  });
  await t.test("a timestamp shift is refused before bitstream fallback", async () => {
    const changed = path.join(base, "shifted.mp4");
    await runTool(tools.ffmpeg, ["-v", "error", "-itsoffset", "0.005", "-i", final, "-map", "0:v:0", "-c:v", "copy", "-copyts", changed]);
    await assert.rejects(verifyRetainedPictures({ ...config, final: changed }), /picture timestamp|packet count/);
  });
});

function rollbackDirectoryFixture(t) {
  const base = mkdtempSync(path.join(os.tmpdir(), "renewal-rollback-retry-")), from = path.join(base, "canonical"), to = path.join(base, "prepared");
  t.after(() => rmSync(base, { recursive: true, force: true }));
  mkdirSync(from); writeFileSync(path.join(from, "STOP"), "held candidate");
  return { from, to };
}

test("Windows rollback retries transient sharing errors on the exact pair without losing STOP", async (t) => {
  for (const code of ["EPERM", "EACCES", "EBUSY"]) await t.test(code, async (child) => {
    const { from, to } = rollbackDirectoryFixture(child), pairs = [], delays = [];
    await renameRollbackDirectory(from, to, { platform: "win32", wait: async (ms) => { delays.push(ms); }, rename: (a, b) => {
      pairs.push([a, b]); if (pairs.length === 1) throw Object.assign(new Error("transient sharing obstruction"), { code });
      renameSync(a, b);
    } });
    assert.ok(pairs.length >= 2 && pairs.length <= 5); assert.ok(pairs.every(([a, b]) => a === from && b === to));
    assert.equal(delays[0], 25); assert.ok(delays.reduce((sum, ms) => sum + ms, 0) <= 375);
    assert.equal(existsSync(from), false); assert.equal(readFileSync(path.join(to, "STOP"), "utf8"), "held candidate");
  });
});

test("Windows rollback retry exhaustion retains source and never replaces a destination", async (t) => {
  for (const code of ["EPERM", "EACCES", "EBUSY"]) await t.test(code, async (child) => {
    const { from, to } = rollbackDirectoryFixture(child), delays = []; let attempts = 0;
    await assert.rejects(renameRollbackDirectory(from, to, { platform: "win32", wait: async (ms) => { delays.push(ms); }, rename: (a, b) => {
      assert.equal(a, from); assert.equal(b, to); attempts++;
      throw Object.assign(new Error("permanent sharing obstruction"), { code });
    } }), /permanent sharing obstruction/);
    assert.equal(attempts, 5); assert.deepEqual(delays, [25, 50, 100, 200]);
    assert.equal(readFileSync(path.join(from, "STOP"), "utf8"), "held candidate"); assert.equal(existsSync(to), false);
  });
  await t.test("destination appears while waiting", async (child) => {
    const { from, to } = rollbackDirectoryFixture(child); let attempts = 0;
    await assert.rejects(renameRollbackDirectory(from, to, { platform: "win32", wait: async () => { mkdirSync(to); writeFileSync(path.join(to, "keep.wav"), "other owner source"); }, rename: () => {
      attempts++; throw Object.assign(new Error("transient sharing obstruction"), { code: "EPERM" });
    } }), /rollback paths changed/);
    assert.equal(attempts, 1); assert.equal(readFileSync(path.join(to, "keep.wav"), "utf8"), "other owner source");
    assert.equal(readFileSync(path.join(from, "STOP"), "utf8"), "held candidate");
  });
  await t.test("source moves while waiting", async (child) => {
    const { from, to } = rollbackDirectoryFixture(child), retained = `${from}.retained`; let attempts = 0;
    await assert.rejects(renameRollbackDirectory(from, to, { platform: "win32", wait: async () => { renameSync(from, retained); }, rename: () => {
      attempts++; throw Object.assign(new Error("transient sharing obstruction"), { code: "EPERM" });
    } }), /rollback paths changed/);
    assert.equal(attempts, 1); assert.equal(readFileSync(path.join(retained, "STOP"), "utf8"), "held candidate"); assert.equal(existsSync(to), false);
  });
  await t.test("same source path with a replacement directory is not renamed", async (child) => {
    const { from, to } = rollbackDirectoryFixture(child), retained = `${from}.retained`; let attempts = 0;
    await assert.rejects(renameRollbackDirectory(from, to, { platform: "win32", wait: async () => {
      renameSync(from, retained); mkdirSync(from); writeFileSync(path.join(from, "owner.wav"), "new owner data");
    }, rename: () => {
      attempts++; throw Object.assign(new Error("transient sharing obstruction"), { code: "EPERM" });
    } }), /rollback paths changed/);
    assert.equal(attempts, 1); assert.equal(readFileSync(path.join(retained, "STOP"), "utf8"), "held candidate");
    assert.equal(readFileSync(path.join(from, "owner.wav"), "utf8"), "new owner data"); assert.equal(existsSync(to), false);
  });
  await t.test("dangling destination link is not replaced", async (child) => {
    const { from, to } = rollbackDirectoryFixture(child); symlinkSync(`${to}.missing`, to, "junction");
    assert.equal(existsSync(to), false);
    await assert.rejects(renameRollbackDirectory(from, to, { platform: "win32", rename: () => assert.fail("destination link would be replaced") }), /rollback paths changed/);
    assert.equal(readFileSync(path.join(from, "STOP"), "utf8"), "held candidate");
  });
  for (const [platform, code] of [["linux", "EPERM"], ["win32", "EIO"]]) await t.test(`${platform} ${code} is not retried`, async (child) => {
    const { from, to } = rollbackDirectoryFixture(child); let attempts = 0;
    await assert.rejects(renameRollbackDirectory(from, to, { platform, wait: async () => assert.fail("unexpected retry"), rename: () => {
      attempts++; throw Object.assign(new Error("nonretryable obstruction"), { code });
    } }), /nonretryable obstruction/);
    assert.equal(attempts, 1); assert.ok(existsSync(from)); assert.equal(existsSync(to), false);
  });
});

test("permanent rollback obstruction keeps recovery-required, both exact sources and STOP", async (t) => {
  const f = fixture(t), receipt = await prepareHandoff(f.config); let calls = 0, rollbackAttempts = 0;
  await assert.rejects(activateHandoff({ receipt, readRemote: async () => ++calls === 3 ? { ...f.remote, youtube_sync: {} } : f.remote, workerIdle: idle, rename: (from, to) => {
    if (from === f.canonical && to === f.out) { rollbackAttempts++; throw Object.assign(new Error("permanent rollback obstruction"), { code: "EPERM" }); }
    renameSync(from, to);
  } }), /activity prevents/);
  const journal = JSON.parse(readFileSync(`${f.canonical}.handoff-${receipt.id}.json`));
  assert.equal(journal.phase, "recovery-required"); assert.match(journal.rollback_error, /permanent rollback obstruction/);
  assert.equal(rollbackAttempts, process.platform === "win32" ? 5 : 1);
  assert.equal(readFileSync(path.join(receipt.archive, "cache.wav"), "utf8"), "canonical cache");
  assert.equal(readFileSync(path.join(f.canonical, "final.mp4"), "utf8"), "new final"); assert.ok(existsSync(path.join(f.canonical, "STOP")));
  assert.ok(existsSync(path.join(path.dirname(f.canonical), "STOP"))); assert.equal(existsSync(f.out), false);
  await assert.rejects(activateHandoff({ receipt, readRemote: async () => f.remote, workerIdle: idle }), /already attempted/);
});
