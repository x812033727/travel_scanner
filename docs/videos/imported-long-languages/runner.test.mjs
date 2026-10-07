import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { createServer } from "node:http";
import { execFileSync } from "node:child_process";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { approve, sha256File } from "../../../tools/video/core/approvals.mjs";
import { lintProject, loadProject, recordStage } from "../../../tools/video/core/state.mjs";
import { speechHash } from "../../../tools/video/core/timeline.mjs";
import { eachLine, textHash } from "../../../tools/video/core/schema.mjs";
import { presentationTimeline, validateBranding } from "../../../tools/video/core/branding.mjs";
import { localeTexts } from "../../../tools/video/core/stages.mjs";
import { buildCues, toSrt } from "../../../tools/video/core/captions.mjs";
import { composeMetadata } from "../../../tools/video/package/metadata.mjs";
import { prepareApprovedFinalHandoff, prepareHandoff, readManualLanguageSource } from "../../../tools/video/review/renewal-handoff.mjs";
import { main as videoMain } from "../../../tools/video/cli.mjs";
import { Automation } from "../../../tools/video/automation/flow.mjs";
import { readUnits, unitKey } from "../../../tools/video/automation/sheet-units.mjs";
import { buildSheet, mergeSheet } from "../../../tools/video/i18n/cli.mjs";
import { capProblem, ledgerTotals } from "../../../tools/video/media/ledger.mjs";
import { SLUGS, DIRECT_STAGE_TIMEOUT_MS, HardStop, VideoStop, assertProject, checkedDubReceipt, createSiteClient, cumulativeSnapshot, directStageOrigin, journaledStageClient, missingPhaseParts, nativeStageRequest, prepareApprovedFinalBatch, prepareRenewedBatch, resolveManifest, run, submitSnapshot, translateLocaleResuming, validateResumeSheet, verifyLocal } from "./runner.mjs";

const json = (file, value) => { mkdirSync(path.dirname(file), { recursive: true }); writeFileSync(file, JSON.stringify(value)); };
const hash = (value) => createHash("sha256").update(value).digest("hex");
const choice = { en: { metadata: true, captions: true, dub: true } };
const ref = (role, value = role) => ({ role, sha256: hash(value), size: Buffer.byteLength(value), content_type: role.startsWith("dub_") ? "audio/mp4" : "text/plain" });
const remote = (entry) => ({ slug: entry.slug, title: "Original title", stage: "imported-final", checklist: [{ key: "final_video_approved", done: true, label: "Approved" }], format: "slides", youtube_video_id: null, locales: structuredClone(choice), locales_decided_at: "2026-09-29T00:00:00Z", languages: { en: { metadata: { state: "working" }, captions: { state: "working" }, dub: { state: "working" } } }, reviews: [{ id: "final-1", gate: "final", status: "approved", content_sha256: entry.final_sha256, created_at: "2026-09-29T00:00:00Z", decided_at: "2026-09-29T00:01:00Z" }] });

async function fixture(t, count = 1) {
  const base = mkdtempSync(path.join(os.tmpdir(), "imported-languages-"));
  t.after(() => rmSync(base, { recursive: true, force: true }));
  const manifest = { schema_version: 1, root: path.join(base, "root"), work_base: path.join(base, "work"), videos: [] };
  const original = JSON.parse(readFileSync(new URL("../../../tools/video/core/fixtures/minimal/video.json", import.meta.url), "utf8"));
  for (const slug of SLUGS.slice(0, count)) {
    const workdir = path.join(manifest.work_base, slug);
    mkdirSync(workdir, { recursive: true });
    writeFileSync(path.join(workdir, "final.mp4"), `approved video ${slug}`);
    const doc = { ...structuredClone(original), slug };
    const doc_file = path.join(manifest.root, "docs", "videos", slug, "video.json");
    json(doc_file, doc);
    const project = loadProject({ slug, root: manifest.root });
    const timeline = { speech_hash: speechHash(doc, project.lexicon), fps: 30, total_frames: 900, scenes: [], lines: [], chapters: [{ scene: "hook", title: "Opening", start_frame: 0 }, { scene: "questions", title: "Questions", start_frame: 300 }, { scene: "wrap", title: "End", start_frame: 600 }] };
    json(path.join(workdir, "timeline.json"), timeline);
    const final_sha256 = await sha256File(path.join(workdir, "final.mp4"));
    manifest.videos.push({ slug, title: doc.youtube.title, workdir, doc_file, final_sha256, source: { final: path.join(workdir, "final.mp4") }, source_files: [{ role: "import-final", path: path.join(workdir, "final.mp4"), bytes: Buffer.byteLength(`approved video ${slug}`), sha256: final_sha256 }] });
  }
  const manifestFile = path.join(base, "manifest.json");
  json(manifestFile, manifest);
  return { base, manifest, manifestFile };
}

async function renewedFixture(t, { gemini = false, dub = false, brandingBytes } = {}) {
  const f = await fixture(t), entry = f.manifest.videos[0];
  if (gemini) {
    const doc = JSON.parse(readFileSync(entry.doc_file)); doc.voice = { provider: "gemini", name: "Sulafat", model: "gemini-3.8-flash-tts" }; doc.target_minutes = [8, 20];
    let id = 0;
    for (const scene of doc.scenes) scene.lines = Array.from({ length: 20 }, (_, repeat) => scene.lines.map((line) => { const copy = { ...line, id: `n${(id++).toString(36).padStart(3, "0")}` }; delete copy.say; delete copy.say_for; if (repeat) delete copy.reveal; return copy; })).flat();
    json(entry.doc_file, doc); writeFileSync(path.join(path.dirname(entry.doc_file), "brief.md"), "## 站主觀點\n請比較模型的工作需求。\n## 觀眾看完能做到的事\n觀眾能用三個問題選擇模型。\n");
    json(path.join(f.manifest.root, "docs/videos/lexicon.json"), { schema_version: 1, terms: { AI: null } });
  }
  const project = loadProject({ slug: entry.slug, root: f.manifest.root });
  const timeline = JSON.parse(readFileSync(path.join(entry.workdir, "timeline.json")));
  timeline.speech_hash = speechHash(project.doc, project.lexicon);
  const bodyFrames = gemini ? 18000 : 900; timeline.total_frames = bodyFrames;
  if (gemini) timeline.chapters = timeline.chapters.map((v) => ({ ...v, start_frame: v.start_frame * 20 }));
  timeline.lines = [...eachLine(project.doc)].map(({ line, scene }, index, all) => ({ id: line.id, scene: scene.id, start_frame: Math.floor(index * bodyFrames / all.length), end_frame: Math.floor((index + 1) * bodyFrames / all.length), audio_samples: 120 * 1600 }));
  json(path.join(entry.workdir, "timeline.json"), timeline);
  const old = path.join(f.base, "retained"), canonical = path.join(f.base, "canonical"), prepared = path.join(f.base, "handoff"); mkdirSync(old); mkdirSync(canonical);
  for (const [name, value] of Object.entries({ "intro.mp4": brandingBytes?.intro ?? "intro", "outro.mp4": brandingBytes?.outro ?? "outro", "final.mp4": "renewed final", "thumbnail.jpg": "old thumbnail" })) writeFileSync(path.join(old, name), value);
  const pin = validateBranding({ schema_version: 1, id: "new", intro: { file: "intro.mp4", sha256: hash(readFileSync(path.join(old, "intro.mp4"))), frames: 150 }, outro: { file: "outro.mp4", sha256: hash(readFileSync(path.join(old, "outro.mp4"))), frames: 90 } }, { base: old });
  json(path.join(old, "branding.json"), pin);
  const presented = presentationTimeline(timeline, { hash: pin.hash, intro_frames: 150, outro_frames: 90, body_frames: bodyFrames });
  const captions = toSrt(buildCues(timeline, localeTexts(project.doc, {}).texts["zh-TW"], "zh-TW").cues);
  writeFileSync(path.join(old, "zh-TW.srt"), captions);
  const meta = composeMetadata({ ...project, timeline, locales: [] }).metadata;
  meta.chapters = meta.chapters.map(({ at, title }) => ({ time: at, title })); meta.contains_synthetic_media = true; meta.disclosure_reason = "Original synthetic narration";
  json(path.join(old, "metadata.json"), meta);
  const attachment = (file, role) => ({ file, role, review_id: "33333333-3333-4333-8333-333333333333", sha256: hash(readFileSync(file)), size: readFileSync(file).length, content_type: "text/plain" });
  const metadata = attachment(path.join(old, "metadata.json"), "metadata"), caption = attachment(path.join(old, "zh-TW.srt"), "captions_zh-TW"), thumbnail = attachment(path.join(old, "thumbnail.jpg"), "thumbnail");
  const final = { id: "22222222-2222-4222-8222-222222222222", gate: "final", status: "approved", created_at: "2026-10-04T01:00:00Z", decided_at: "2026-10-04T02:00:00Z", content_sha256: hash("renewed final"), files: [{ role: "captions_zh-TW", sha256: hash(toSrt(buildCues(presented, localeTexts(project.doc, {}).texts["zh-TW"], "zh-TW").cues)) }], payload: { branding_hash: pin.hash, _final_renewal: { previous_review_id: "11111111-1111-4111-8111-111111111111", previous_sha256: entry.final_sha256, retained_review_ids: [metadata.review_id] }, renewal_candidate: { source: { final_review_id: "11111111-1111-4111-8111-111111111111", final_sha256: entry.final_sha256, body_sha256: entry.final_sha256 }, candidate: { final_sha256: hash("renewed final"), branding_hash: pin.hash } } } };
  const site = { ...remote(entry), locales: { en: { metadata: true, captions: true, dub } }, reviews: [final, { id: final.payload._final_renewal.previous_review_id, gate: "final", status: "superseded", content_sha256: entry.final_sha256 }, { id: metadata.review_id, gate: "publish", status: "superseded", files: [metadata, caption, thumbnail] }] };
  await prepareHandoff({ slug: entry.slug, canonical, out: prepared, source: { original: path.join(entry.workdir, "final.mp4"), body: path.join(entry.workdir, "final.mp4"), body_frames: bodyFrames, package: { metadata, thumbnail, captions: { "zh-TW": caption } }, adapter: { project, timeline } }, candidate: path.join(old, "final.mp4"), branding: path.join(old, "branding.json"), remote: site, mode: "manual-import", verifyMedia: async () => ({ full_decode_ok: true, video_packets: bodyFrames, seconds: bodyFrames / 30 + 8, loudness: { integrated: -14, truePeak: -0.8 } }) });
  const contract = await readManualLanguageSource({ workdir: prepared, remote: site });
  site.reviews.unshift({ id: "44444444-4444-4444-8444-444444444444", gate: "publish", status: "approved", created_at: "2026-10-04T03:00:00Z", content_sha256: contract.metadata.sha256, payload: { final_review_id: final.id } });
  f.manifest.portable = true; f.manifest.relative_paths = { root: "root", work_base: "work" };
  entry.relative_paths = { doc_file: path.relative(f.base, entry.doc_file), workdir: path.relative(f.base, entry.workdir) };
  entry.generated_files = [{ relative_path: path.relative(f.base, path.join(entry.workdir, "timeline.json")), sha256: hash(readFileSync(path.join(entry.workdir, "timeline.json"))), bytes: readFileSync(path.join(entry.workdir, "timeline.json")).length }];
  json(f.manifestFile, f.manifest);
  const runtimeRoot = path.join(f.base, "code");
  for (const name of ["tools/video/review/renewal-handoff.mjs", ".agents/skills/youtube-video/SKILL.md", ...["runner.mjs", "prepare.mjs", "preflight.mjs", "speech-journal.mjs"].map((v) => `docs/videos/imported-long-languages/${v}`)]) { mkdirSync(path.dirname(path.join(runtimeRoot, name)), { recursive: true }); writeFileSync(path.join(runtimeRoot, name), `reviewed code ${name}`); }
  return { ...f, entry, prepared, site, timeline, presented, contract, runtimeRoot };
}

async function currentApprovedFixture(t, { dub = false, brandingBytes } = {}) {
  const f = await renewedFixture(t, { gemini: true, dub, brandingBytes }), project = structuredClone(loadProject({ slug: f.entry.slug, root: f.manifest.root }));
  project.doc.scenes[0].lines[0].text += "這是新核准正文。";
  const timeline = structuredClone(f.timeline); timeline.speech_hash = speechHash(project.doc, project.lexicon);
  const final = f.site.reviews.find((v) => v.gate === "final"), current = path.join(f.base, "current-attachments"), evidence = {}; mkdirSync(current);
  const presented = presentationTimeline(timeline, { hash: f.contract.source.branding_hash, intro_frames: 150, outro_frames: 90, body_frames: timeline.total_frames }), caption = toSrt(buildCues(presented, localeTexts(project.doc, {}).texts["zh-TW"], "zh-TW").cues);
  for (const [role, value] of Object.entries({ evidence_script: project.doc, evidence_body_timeline: timeline, "captions_zh-TW": caption, narration: "real current AAC attachment", thumbnail: "current thumbnail" })) {
    const file = path.join(current, role); if (typeof value === "object") json(file, value); else writeFileSync(file, value);
    evidence[role] = { file, role, review_id: final.id, sha256: hash(readFileSync(file)), size: readFileSync(file).length, content_type: role === "narration" ? "audio/mp4" : role.startsWith("evidence") ? "application/json" : "text/plain" };
  }
  const meta = composeMetadata({ ...project, timeline: presented, locales: [] }).metadata; final.files = Object.values(evidence);
  final.payload = { ...final.payload, manual_review: true, metadata: { "zh-TW": { title: meta.title, description: meta.description } }, chapters: meta.chapters.map(({ at, title }) => ({ time: at, title })), body_change: { new_script: evidence.evidence_script, new_body_timeline: evidence.evidence_body_timeline, speech_hash: timeline.speech_hash, new_body: { sha256: hash("missing new master") }, new_voice: { sha256: hash("different raw WAV") }, audio_owner_accepted: false, full_playback_owner_accepted: false } };
  const actor = "55555555-5555-4555-8555-555555555555", decisionAuthority = { slug: f.entry.slug, status: "approved", review_id: final.id, content_sha256: final.content_sha256, decided_at: final.decided_at, decided_by_user_id: actor, approval_audits: [{ id: "66666666-6666-4666-8666-666666666666", action: "video_review_approved", actor_user_id: actor, target: `video_review:${final.id}`, metadata_json: { slug: f.entry.slug, gate: "final", sha256: final.content_sha256 } }] };
  const prepared = path.join(f.base, "current-handoff");
  await prepareApprovedFinalHandoff({ slug: f.entry.slug, canonical: path.join(f.base, "canonical"), out: prepared, remote: f.site, candidate: path.join(f.base, "retained/final.mp4"), branding: path.join(f.base, "retained/branding.json"), decisionAuthority, source: { evidence, adapter: { project, timeline, caption_mode: "approved-line-windows" }, disclosure: { synthetic: true, reason: "Current synthetic speech" } }, verifyMedia: async () => ({ scope: "approved-current-media-identity", preservation_claim: false, full_decode_ok: true, video_packets: timeline.total_frames, body_range_sha256: hash("actual current packets"), body_audio_pcm_sha256: hash("actual current decoded audio"), narration: { sha256: evidence.narration.sha256, full_decode_ok: true, raw_voice_claimed: false, listening_approval_claimed: false } }) });
  const contract = await readManualLanguageSource({ workdir: prepared, remote: f.site }); f.site.reviews[0].content_sha256 = contract.metadata.sha256;
  return { ...f, prepared, contract, currentProject: project };
}

test("actual new-source run survives language sync but holds an unknown translator across invocations", async (t) => {
  const f = await currentApprovedFixture(t), group = `${f.base}-roundtrip-group`, out = path.join(group, "current"); mkdirSync(group); t.after(() => rmSync(group, { recursive: true, force: true }));
  const prepared = await prepareApprovedFinalBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out, readRemote: async () => structuredClone(f.site), runtimeRoot: f.runtimeRoot });
  const manifest = resolveManifest(JSON.parse(readFileSync(prepared.manifest)), out), entry = manifest.videos[0];
  assert.equal(entry.generated_files.some((v) => v.relative_path.endsWith("/languages.json")), false);
  rmSync(path.join(out, "STOP")); rmSync(path.join(entry.workdir, "STOP"));
  // A legacy ready display without a current-final-bound language review cannot
  // make the fresh source look complete or reuse old translations implicitly.
  f.site.languages.en.metadata.state = "ready"; f.site.languages.en.captions.state = "ready";
  let posts = 0;
  const api = { reviews: async () => structuredClone(f.site), settings: async () => ({}), run: async () => { posts++; throw new VideoStop("connection closed; POST result may have completed"); } };
  const runMain = async (args, ctx) => {
    if (args[0] === "review-pull") { await approve({ gate: "final", docDir: path.dirname(entry.doc_file), workdir: entry.workdir }); return 0; }
    return videoMain(args, ctx);
  };
  const options = { manifest: prepared.manifest, slugs: [entry.slug], phase: "translations", maxUnits: 1, dryRun: false };
  const ownerLock = path.join(path.dirname(out), ".approved-final-language-runner.lock");
  writeFileSync(ownerLock, "another exact-lexicon producer owns this lock");
  try { await assert.rejects(run(options, { api, runMain }), { code: "EEXIST" }); assert.equal(posts, 0); assert.equal(readFileSync(ownerLock, "utf8"), "another exact-lexicon producer owns this lock"); }
  finally { rmSync(ownerLock); }
  const first = await run(options, { api, runMain }); assert.equal(first.status, "paused"); assert.equal(posts, 1);
  assert.ok(JSON.parse(readFileSync(path.join(entry.workdir, "languages.json"))).synced_at);
  await verifyLocal(manifest, entry);
  const second = await run(options, { api, runMain }); assert.equal(second.status, "paused"); assert.equal(posts, 1);
  assert.equal(existsSync(ownerLock), false);
  assert.match(second.videos[entry.slug].error, /unknown paid result/);
  const journal = JSON.parse(readFileSync(path.join(entry.workdir, "language-stage-journal.json")));
  assert.equal(Object.values(journal.entries)[0].status, "unknown"); assert.equal(journal.identity.final_sha256, entry.final_sha256);
  f.site.locales.en.metadata = false;
  await assert.rejects(run(options, { api, runMain }), /choice changed/); assert.equal(posts, 1);
  f.site.locales.en.metadata = true;
  const raw = JSON.parse(readFileSync(prepared.manifest));
  for (const label of [undefined, "retained-source"]) {
    raw.source_kind = label; json(prepared.manifest, raw);
    await assert.rejects(run({ ...options, phase: "dubs" }, { api, runMain }), /source kind differs/); assert.equal(posts, 1);
  }
});

test("actual renewed run passes its current native project to cumulative language submission without repeating completed translation", async (t) => {
  const f = await currentApprovedFixture(t, { dub: true }), group = `${f.base}-submission-group`, out = path.join(group, "current");
  mkdirSync(group); t.after(() => rmSync(group, { recursive: true, force: true }));
  const prepared = await prepareApprovedFinalBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out, readRemote: async () => structuredClone(f.site), runtimeRoot: f.runtimeRoot });
  const manifest = resolveManifest(JSON.parse(readFileSync(prepared.manifest)), out), entry = manifest.videos[0];
  rmSync(path.join(out, "STOP")); rmSync(path.join(entry.workdir, "STOP"));
  const project = loadProject({ slug: entry.slug, root: manifest.root }), translationFile = path.join(project.dir, "i18n/en.json");
  const sheet = buildSheet(project.doc, undefined, "en", null, ["metadata", "captions"]);
  sheet.title.text = "Reviewed English title"; sheet.description.text = "Reviewed English description."; sheet.tags.text = ["AI"];
  sheet.chapters.forEach((chapter) => { chapter.text = `English ${chapter.scene}`; }); sheet.lines.forEach((line) => { line.text = `English ${line.id}`; });
  const merged = mergeSheet(project.doc, sheet, undefined); assert.equal(merged.problems.length, 0); json(translationFile, merged.translation);
  const translationSha = await sha256File(translationFile), progressFile = path.join(out, "progress.json"), progress = JSON.parse(readFileSync(progressFile));
  progress.videos[entry.slug] = { final_sha256: entry.final_sha256, translations: { en: translationSha }, checked_dubs: {}, skipped_dubs: {}, status: "paused", error: "prior staging failure" };
  json(progressFile, progress);
  const uploads = [], submissions = [];
  const api = {
    reviews: async () => structuredClone(f.site), settings: async () => ({}),
    run: async () => assert.fail("The completed translation must not call a provider again"),
    upload: async (slug, file) => {
      assert.equal(slug, entry.slug); assert.equal(file.sha256, await sha256File(file.path)); uploads.push(file.role);
      const { path: omitted, ...ref } = file; return ref;
    },
    submit: async (slug, body) => {
      assert.equal(slug, entry.slug); assert.equal(body.gate, "languages"); submissions.push(structuredClone(body));
      const review = { id: "77777777-7777-4777-8777-777777777777", gate: "languages", status: "pending", created_at: "2026-10-07T04:00:00Z", content_sha256: body.content_sha256, payload: structuredClone(body.payload), files: structuredClone(body.files) };
      f.site.reviews.push(review); f.site.languages.en.metadata.state = "ready"; f.site.languages.en.captions.state = "ready";
      return structuredClone(review);
    },
  };
  const result = await run({ manifest: prepared.manifest, slugs: [entry.slug], phase: "translations", maxUnits: 1, dryRun: false }, {
    api, fetch: async () => assert.fail("The integration fixture cannot use the network"),
    runMain: async (args, ctx) => {
      if (args[0] === "review-pull") { await approve({ gate: "final", docDir: project.dir, workdir: entry.workdir }); return 0; }
      assert.equal(args[0], "captions"); return videoMain(args, ctx);
    },
  });
  assert.equal(result.status, "phase-complete", result.videos[entry.slug].error);
  assert.equal(result.videos[entry.slug].status, "phase-complete"); assert.equal(submissions.length, 1);
  assert.deepEqual(uploads.sort(), ["captions_en", "description_en", "languages_manifest", "metadata"]);
  const request = submissions[0], review = f.site.reviews.at(-1), receipt = JSON.parse(readFileSync(path.join(entry.workdir, "language-package/last-renewal-submission.json")));
  assert.deepEqual(request.payload.locales, { en: { metadata: "ready", captions: "ready" } });
  assert.equal(request.payload.final_review_id, f.site.reviews.find((item) => item.gate === "final" && item.status === "approved").id);
  assert.deepEqual(request.payload, review.payload); assert.deepEqual(request.files, review.files);
  assert.equal(request.content_sha256, await sha256File(path.join(entry.workdir, "language-package/renewed-languages-manifest.json")));
  assert.equal(receipt.status, "confirmed"); assert.deepEqual(receipt.request, request);
  assert.equal(await sha256File(translationFile), translationSha); assert.equal(result.videos[entry.slug].translations.en, translationSha);
  assert.equal(missingPhaseParts(f.site, "translations").length, 0); assert.deepEqual(missingPhaseParts(f.site, "dubs"), ["en/dub"]);
  assert.equal(result.videos[entry.slug].last_submission.status, "pending");
});

test("sync stage journal reuses completed exact answers and never dispatches past crash or damaged receipts", async (t) => {
  const f = await fixture(t), entry = f.manifest.videos[0], manifest = { request_namespace: "new-current-source" }, now = () => "2026-10-04T00:00:00Z";
  let posts = 0; const answer = { text: '{"worksheet":{"lines":[]}}', model: "selected-alias-actual", usage: { tokens: 30, token_budget: 100 }, input_tokens: 20, output_tokens: 10 };
  const api = { run: async () => { posts++; return structuredClone(answer); } }, args = ["translator", entry.slug, "exact instructions", { locale: "en", optional: undefined }, 32000, "slides"];
  assert.deepEqual(await journaledStageClient(api, manifest, [entry], now).run(...args), answer);
  assert.deepEqual(await journaledStageClient({ run: async () => { throw Error("second dispatch forbidden"); } }, manifest, [entry], now).run(...args), answer); assert.equal(posts, 1);
  await assert.rejects(journaledStageClient(api, manifest, [entry], now).run(...[...args.slice(0, 2), "changed exact instructions", ...args.slice(3)]), /exact stage request changed/); assert.equal(posts, 1);
  await assert.rejects(journaledStageClient(api, manifest, [entry], now).run(...[...args.slice(0, 3), { locale: "en", changed_body: "changed input" }, ...args.slice(4)]), /exact stage request changed/); assert.equal(posts, 1);
  for (const options of [{ settings: { durable_stage_runs: true } }, { settings: { stage_models: { translator: { provider: "new", model: "new" } } } }, { choices: { [entry.slug]: { en: { captions: false } } } }]) await assert.rejects(journaledStageClient(api, manifest, [entry], now, options).run(...args), /source identity changed/);
  const file = path.join(entry.workdir, "language-stage-journal.json"), stored = JSON.parse(readFileSync(file)), record = Object.values(stored.entries)[0];
  assert.equal("optional" in record.request.payload, false);
  record.status = "dispatching"; json(file, stored);
  await assert.rejects(journaledStageClient(api, manifest, [entry], now).run("caption_reviewer", ...args.slice(1)), /unknown paid result/); assert.equal(posts, 1);
  await assert.rejects(journaledStageClient(api, { request_namespace: "changed-source" }, [entry], now).run(...args), /source identity changed/); assert.equal(posts, 1);
  record.status = "succeeded"; record.result.text += "tampered"; json(file, stored);
  await assert.rejects(journaledStageClient(api, manifest, [entry], now).run(...args), /malformed/); assert.equal(posts, 1);
});

test("new approved-final batch archives all old paid answers and permits changed source only through its independent entry", async (t) => {
  const f = await currentApprovedFixture(t), out = `${f.base}-current`; t.after(() => rmSync(out, { recursive: true, force: true }));
  const oldTranslation = path.join(f.manifest.root, "docs/videos", f.entry.slug, "i18n/en.json"); json(oldTranslation, { paid: "old translated answer" });
  json(path.join(f.entry.workdir, "automation/translation-units/en.json"), { uncertain: "unknown paid answer" }); json(path.join(f.base, "progress.json"), { spent: 10, ambiguous: "preserve this charge" });
  json(path.join(f.entry.workdir, "media/ledger.json"), { entries: [{ stage: "keyframes", kind: "image", cost_usd: 19.95, key: "prior-paid" }, { kind: "judge", cost_usd: 0.22, status: "uncertain" }] });
  const result = await prepareApprovedFinalBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out, readRemote: async () => f.site, runtimeRoot: f.runtimeRoot });
  const manifest = resolveManifest(JSON.parse(readFileSync(result.manifest)), out), entry = manifest.videos[0], project = await verifyLocal(manifest, entry);
  assert.equal(result.source_kind, "approved-final-body-range"); assert.equal(result.paid_generation, false); assert.ok(existsSync(path.join(out, "STOP")));
  assert.equal(project.doc.scenes[0].lines[0].text, f.currentProject.doc.scenes[0].lines[0].text);
  assert.equal(existsSync(path.join(project.dir, "i18n/en.json")), false); assert.equal(existsSync(path.join(entry.workdir, "automation")), false); assert.equal(existsSync(path.join(entry.workdir, "approvals.json")), false);
  assert.equal(JSON.parse(readFileSync(path.join(out, "retained-source/original-batch/progress.json"))).ambiguous, "preserve this charge");
  assert.equal(JSON.parse(readFileSync(path.join(out, "progress.json"))).previous_translations_stale, true);
  assert.equal(ledgerTotals(entry.workdir).usd, 20.17); assert.match(capProblem(entry.workdir, 1, 20), /past the per-video cap/);
  assert.equal(JSON.parse(readFileSync(path.join(entry.workdir, "source-accounting.json"))).inherited_media_totals.usd, 20.17);
  const rejected = `${f.base}-old-entry`; t.after(() => rmSync(rejected, { recursive: true, force: true }));
  await assert.rejects(prepareRenewedBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out: rejected, readRemote: async () => f.site, runtimeRoot: f.runtimeRoot }), /old batch.*retained source adapter/);
  await approve({ gate: "final", docDir: project.dir, workdir: entry.workdir });
  let calls = 0, text = ""; const sink = { write: (v) => { text += v; } }, ctx = { root: manifest.root, home: out, env: { VIDEO_WORKDIR: manifest.work_base }, stdout: sink, stderr: sink, fetch: async () => { calls++; assert.fail("new source native dry-run cannot use network"); } };
  assert.equal(await videoMain(["captions", "--slug", entry.slug], ctx), 0, text); assert.match(readFileSync(path.join(entry.workdir, "captions/zh-TW.srt"), "utf8"), /00:00:05,000/);
  json(path.join(project.dir, "i18n/en.json"), { title: "Current English", description: "Current reviewed English", tags: [], chapters: {}, lines: Object.fromEntries([...eachLine(project.doc)].map(({ line }) => [line.id, { text: `English ${line.id}`, source_hash: textHash(line.text) }])) });
  text = ""; assert.equal(await videoMain(["dub", "--slug", entry.slug, "--locale", "en", "--dry-run"], ctx), 0, text); assert.equal(calls, 0);
  writeFileSync(path.join(entry.workdir, "final.mp4"), "stale final"); text = ""; assert.notEqual(await videoMain(["captions", "--slug", entry.slug], ctx), 0); assert.match(text, /exact pulled owner final/); assert.equal(calls, 0);
});

test("renewed portable producer retains old paid evidence, pins actual source adapter and freezes new runtime while held", async (t) => {
  const f = await renewedFixture(t), out = `${f.base}-next-batch`; t.after(() => rmSync(out, { recursive: true, force: true }));
  const oldCode = path.join(f.manifest.root, "tools/video/review/renewal-handoff.mjs"); mkdirSync(path.dirname(oldCode), { recursive: true }); writeFileSync(oldCode, "previous runtime"); json(path.join(f.base, "runtime-receipt.json"), { old: true });
  json(path.join(f.base, "progress.json"), { videos: { [f.entry.slug]: { uncertain: "paid translator answer unknown" } } });
  const old = readFileSync(f.manifestFile);
  const result = await prepareRenewedBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out, readRemote: async () => f.site, runtimeRoot: f.runtimeRoot });
  assert.equal(result.status, "prepared-held"); assert.equal(result.paid_generation, false); assert.ok(existsSync(path.join(out, "STOP")));
  assert.deepEqual(readFileSync(f.manifestFile), old);
  assert.equal(JSON.parse(readFileSync(path.join(out, "retained-source/previous-progress.json"))).videos[f.entry.slug].uncertain, "paid translator answer unknown");
  assert.equal(readFileSync(path.join(out, "retained-source/runtime/tools/video/review/renewal-handoff.mjs"), "utf8"), "previous runtime"); assert.equal(JSON.parse(readFileSync(path.join(out, "retained-source/previous-runtime-receipt.json"))).old, true);
  assert.equal(readFileSync(path.join(out, "root/tools/video/review/renewal-handoff.mjs"), "utf8"), "reviewed code tools/video/review/renewal-handoff.mjs");
  const manifest = resolveManifest(JSON.parse(readFileSync(result.manifest)), out), entry = manifest.videos[0]; await verifyLocal(manifest, entry);
  assert.equal(entry.final_sha256, f.site.reviews.find((v) => v.gate === "final").content_sha256);
  assert.equal(readFileSync(path.join(entry.workdir, "retained-source/adapter-original-final.mp4"), "utf8"), `approved video ${entry.slug}`);
  await readManualLanguageSource({ workdir: entry.workdir, remote: f.site });
  writeFileSync(path.join(entry.workdir, "language-adapter/project.json"), "tampered script");
  await assert.rejects(verifyLocal(manifest, entry), /source changed/);
});

test("renewed source refuses jointly relabelled contract/doc and a different approved metadata version", async (t) => {
  const f = await renewedFixture(t), file = path.join(f.prepared, "renewal-language-source.json"), bytes = readFileSync(file);
  const changed = JSON.parse(bytes); changed.adapter.doc_sha256 = hash("changed source"); json(file, changed);
  await assert.rejects(readManualLanguageSource({ workdir: f.prepared, remote: f.site }), /prepared handoff receipt/);
  writeFileSync(file, bytes);
  const entry = { ...f.entry, workdir: f.prepared, final_sha256: hash("renewed final"), renewal_source: { file: "renewal-language-source.json", sha256: hash(bytes) } };
  f.site.reviews[0].content_sha256 = hash("other base metadata");
  let posts = 0; const api = { reviews: async () => structuredClone(f.site), submit: async () => { posts++; }, upload: async () => {} };
  await assert.rejects(submitSnapshot(api, loadProject({ slug: entry.slug, root: f.manifest.root }), entry, { locales: { en: { captions: "ready" } }, files: [ref("captions_en", "old caption")] }, f.site.locales, () => "2026-10-04T04:00:00Z"), /exact renewed base publish metadata/);
  assert.equal(posts, 0);
});

test("renewed cumulative language manifest uses exact approved source, shifted captions/chapters and never retries a lost POST", async (t) => {
  const f = await renewedFixture(t, { dub: true }), entry = { ...f.entry, workdir: f.prepared, final_sha256: hash("renewed final"), renewal_source: { file: "renewal-language-source.json", sha256: hash(readFileSync(path.join(f.prepared, "renewal-language-source.json"))) } };
  writeFileSync(path.join(entry.workdir, "timeline.json"), readFileSync(path.join(entry.workdir, "language-adapter/timeline.json")));
  json(path.join(entry.workdir, "dubs/en/timeline.json"), { speech_hash: f.timeline.speech_hash, lines: [{ id: "not-checked", start_frame: 900, end_frame: 950 }] });
  const translation = { title: "Actual English title", description: "Actual reviewed description.", tags: ["AI"], chapters: { hook: "Opening", questions: "Questions", wrap: "End" }, lines: Object.fromEntries([...eachLine(loadProject({ slug: entry.slug, root: f.manifest.root }).doc)].map(({ line }) => [line.id, { text: `English ${line.id}`, source_hash: textHash(line.text) }])) };
  json(path.join(path.dirname(entry.doc_file), "i18n/en.json"), translation);
  const project = loadProject({ slug: entry.slug, root: f.manifest.root }), composed = composeMetadata({ ...project, timeline: f.presented, locales: ["en"] }).metadata.localizations.en;
  const description = path.join(entry.workdir, "en.txt"), caption = path.join(entry.workdir, "en.srt"); writeFileSync(description, `${composed.title}\n\n${composed.description}\n`); writeFileSync(caption, toSrt(buildCues(f.presented, localeTexts(project.doc, project.translations).texts.en, "en").cues));
  const additions = { locales: { en: { metadata: "ready", captions: "ready" } }, files: [{ ...ref("description_en", readFileSync(description)), path: description }, { ...ref("captions_en", readFileSync(caption)), path: caption }] };
  let posts = 0; const bodies = [], api = { reviews: async () => structuredClone(f.site), upload: async () => {}, submit: async (_slug, body) => { posts++; bodies.push(body); throw new VideoStop("lost POST answer"); } };
  await assert.rejects(submitSnapshot(api, project, entry, additions, f.site.locales, () => "2026-10-04T04:00:00Z"), /lost POST answer/);
  const body = bodies[0], manifest = JSON.parse(readFileSync(path.join(entry.workdir, "language-package/renewed-languages-manifest.json")));
  assert.deepEqual(manifest.source.final, f.contract.source.final); assert.equal(manifest.source.publish.content_sha256, f.contract.metadata.sha256); assert.equal(manifest.source.script, null); assert.equal(body.content_sha256, hash(readFileSync(path.join(entry.workdir, "language-package/renewed-languages-manifest.json"))));
  assert.match(composed.description, /00:15 Questions/); assert.match(readFileSync(caption, "utf8"), /00:00:05,000/);
  await assert.rejects(submitSnapshot(api, project, entry, additions, f.site.locales, () => "2026-10-04T04:00:00Z"), /lost its answer/); assert.equal(posts, 1);
  writeFileSync(caption, toSrt(buildCues(f.timeline, localeTexts(project.doc, project.translations).texts.en, "en").cues)); additions.files[1] = { ...ref("captions_en", readFileSync(caption)), path: caption };
  await assert.rejects(submitSnapshot(api, project, entry, additions, f.site.locales, () => "2026-10-04T04:00:00Z"), /renewed presentation/); assert.equal(posts, 1);
});

test("native renewed-import captions and dub dry-run use real source presentation with no assemble/TTS checks or network", async (t) => {
  const f = await renewedFixture(t, { gemini: true }), out = `${f.base}-native`; t.after(() => rmSync(out, { recursive: true, force: true }));
  const prepared = await prepareRenewedBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out, readRemote: async () => f.site, runtimeRoot: f.runtimeRoot });
  const manifest = resolveManifest(JSON.parse(readFileSync(prepared.manifest)), out), entry = manifest.videos[0], project = loadProject({ slug: entry.slug, root: manifest.root });
  assert.deepEqual(lintProject(project).errors, []);
  json(path.join(path.dirname(entry.doc_file), "i18n/en.json"), { title: "English title", description: "Reviewed English body", tags: [], chapters: {}, lines: Object.fromEntries([...eachLine(project.doc)].map(({ line }) => [line.id, { text: `Actual ${line.id}`, source_hash: textHash(line.text) }])) });
  await approve({ gate: "final", docDir: path.dirname(entry.doc_file), workdir: entry.workdir });
  let text = "", calls = 0; const sink = { write: (value) => { text += value; } }, ctx = { root: manifest.root, home: out, env: { VIDEO_WORKDIR: manifest.work_base }, stdout: sink, stderr: sink, fetch: async () => { calls++; assert.fail("offline native proof cannot call paid or remote services"); } };
  assert.equal(await videoMain(["captions", "--slug", entry.slug], ctx), 0, text);
  assert.match(readFileSync(path.join(entry.workdir, "captions/en.srt"), "utf8"), /00:00:05,000/);
  const captions = JSON.parse(readFileSync(path.join(entry.workdir, "captions/manifest.json"))); assert.equal(captions.branding_hash, f.contract.source.branding_hash);
  assert.equal(existsSync(path.join(entry.workdir, "checks.json")), false); assert.equal(existsSync(path.join(entry.workdir, "narration.wav")), false);
  text = ""; assert.equal(await videoMain(["dub", "--slug", entry.slug, "--locale", "en", "--dry-run"], ctx), 0, text); assert.match(text, /to synthesize/); assert.equal(calls, 0);
  writeFileSync(path.join(entry.workdir, "final.mp4"), "unapproved replacement"); text = "";
  assert.notEqual(await videoMain(["captions", "--slug", entry.slug], ctx), 0); assert.match(text, /exact pulled owner final/); assert.equal(calls, 0);
});

test("latest final, owner choice, Shorts and allowlist gates fail closed", () => {
  const entry = { slug: SLUGS[0], final_sha256: hash("final") };
  const project = remote(entry);
  assert.equal(assertProject(project, entry).id, "final-1");
  project.reviews.push({ id: "new", gate: "final", status: "pending", content_sha256: entry.final_sha256, created_at: "2026-09-29T01:00:00Z" });
  assert.throws(() => assertProject(project, entry), /latest final/);
  assert.throws(() => assertProject({ ...remote(entry), shorts_line: "cut" }, entry), /long slides/);
  assert.throws(() => assertProject(remote(entry), entry, {}), /choice changed/);
  assert.throws(() => assertProject(project, { ...entry, slug: "other-video" }), /allowlist/);
});

test("a later pending dub batch retains prior pending metadata and captions", () => {
  const entry = { slug: SLUGS[0], final_sha256: hash("final") };
  const project = remote(entry);
  project.reviews.push({ gate: "languages", status: "pending", created_at: "2026-09-29T01:00:00Z", payload: { locales: { en: { metadata: "ready", captions: "ready" } } }, files: [ref("description_en"), ref("captions_en")] });
  const result = cumulativeSnapshot(project, { locales: { en: { dub: "ready" } }, files: [ref("dub_en")] });
  assert.equal(result.locales.en.metadata, "ready");
  assert.equal(result.locales.en.captions, "ready");
  assert.equal(result.locales.en.dub, "ready");
  assert.deepEqual(result.files.map((file) => file.role), ["captions_en", "description_en", "dub_en"]);
  assert.throws(() => cumulativeSnapshot(project, { locales: { en: { dub: "ready" } }, files: [] }), /no hash-bound file/);
});

test("already uploaded dub stays uploaded through a later metadata-only batch", () => {
  const entry = { slug: SLUGS[0], final_sha256: hash("final") };
  const project = remote(entry);
  project.languages.en.dub.state = "uploaded";
  project.reviews.push({ gate: "languages", status: "approved", created_at: "2026-09-29T01:00:00Z", payload: { locales: { en: { dub: "ready" } } }, files: [ref("dub_en")] });
  const result = cumulativeSnapshot(project, { locales: { en: { metadata: "ready", dub: "ready" } }, files: [ref("description_en"), ref("dub_en")] });
  assert.equal(result.locales.en.dub, undefined);
  assert.deepEqual(result.files.map((file) => file.role), ["description_en"]);
});

test("cumulative submission hashes its complete files and is idempotent without any project PUT", async (t) => {
  const f = await fixture(t);
  const entry = f.manifest.videos[0];
  const project = remote(entry);
  const calls = [];
  const file = path.join(entry.workdir, "en.txt");
  writeFileSync(file, "English title\n\nEnglish description");
  const record = { path: file, role: "description_en", content_type: "text/plain", size: readFileSync(file).length, sha256: await sha256File(file) };
  const api = { reviews: async () => structuredClone(project), upload: async (_slug, item) => { calls.push(["upload", item.role]); }, submit: async (_slug, body) => { calls.push(["submit", body]); const review = { ...body, id: "languages-1", status: "approved", created_at: "2026-09-29T01:00:00Z" }; project.reviews.push(review); return review; } };
  const additions = { locales: { en: { metadata: "ready", dub: { status: "skipped", reason: "failed ".repeat(300) } } }, files: [record] };
  const sent = await submitSnapshot(api, project, entry, additions, choice, () => "2026-09-29T01:00:00Z");
  assert.equal(sent.status, "approved");
  const body = calls.find(([kind]) => kind === "submit")[1];
  assert.ok([...body.summary].length <= 500);
  assert.equal(body.payload.locales.en.dub.reason.length, 2100);
  assert.equal(body.files[0].path, undefined);
  assert.equal(body.payload.provenance.final_sha256, entry.final_sha256);
  const manifest = readFileSync(path.join(entry.workdir, "language-package", `${sent.content_sha256}.json`), "utf8");
  assert.match(manifest, new RegExp(record.sha256));
  const again = await submitSnapshot(api, project, entry, additions, choice, () => "2026-09-29T02:00:00Z");
  assert.equal(again.status, "already-submitted");
  assert.equal(calls.filter(([kind]) => kind === "submit").length, 1);
  assert.equal(project.title, "Original title");
  assert.equal(project.stage, "imported-final");
});

test("choice or latest final drift during file upload prevents POST", async (t) => {
  const f = await fixture(t);
  const entry = f.manifest.videos[0];
  const project = remote(entry);
  const file = path.join(entry.workdir, "captions.srt");
  writeFileSync(file, "captions");
  const addition = { locales: { en: { captions: "ready" } }, files: [{ ...ref("captions_en", "captions"), path: file }] };
  let posts = 0;
  const api = { reviews: async () => structuredClone(project), upload: async () => { project.locales = {}; }, submit: async () => { posts++; } };
  await assert.rejects(submitSnapshot(api, project, entry, addition, choice, () => "now"), /choice changed/);
  assert.equal(posts, 0);
});

test("dry-run verifies six-scope data without creating progress, approval or paid calls", async (t) => {
  const f = await fixture(t);
  const before = readdirSync(f.base);
  let reads = 0;
  const result = await run({ manifest: f.manifestFile, slugs: [SLUGS[0]], dryRun: true }, { api: { reviews: async () => { reads++; return remote(f.manifest.videos[0]); } } });
  assert.equal(result.status, "dry-run");
  assert.equal(reads, 1);
  assert.deepEqual(readdirSync(f.base), before);
  assert.equal(existsSync(path.join(f.manifest.videos[0].workdir, "approvals.json")), false);
});

test("portable artifacts relocate and timeline edits fail full-hash validation", async (t) => {
  const f = await fixture(t);
  const raw = f.manifest;
  raw.portable = true;
  raw.relative_paths = { root: "root", work_base: "work" };
  const entry = raw.videos[0];
  entry.relative_paths = { doc_file: path.relative(f.base, entry.doc_file), workdir: path.relative(f.base, entry.workdir) };
  const timelineFile = path.join(entry.workdir, "timeline.json");
  entry.generated_files = [{ relative_path: path.relative(f.base, timelineFile), bytes: readFileSync(timelineFile).length, sha256: await sha256File(timelineFile) }];
  entry.source.final = "Z:/an-original-that-is-not-on-this-host.mp4";
  const manifest = resolveManifest(raw, f.base);
  await verifyLocal(manifest, manifest.videos[0]);
  const timeline = JSON.parse(readFileSync(timelineFile, "utf8"));
  timeline.total_frames++;
  json(timelineFile, timeline);
  await assert.rejects(verifyLocal(manifest, manifest.videos[0]), /source changed/);
});

test("initial runtime freezing resolves a portable relative root and refuses to overwrite an existing runtime", async (t) => {
  const f = await fixture(t), raw = { ...f.manifest, portable: true, root: "Z:/previous-host/root", relative_paths: { root: "root", work_base: "work" } };
  json(f.manifestFile, raw);
  const args = [fileURLToPath(new URL("./package-runtime.mjs", import.meta.url)), "--manifest", f.manifestFile];
  const result = JSON.parse(execFileSync(process.execPath, args, { encoding: "utf8" }));
  assert.equal(result.root, f.manifest.root); assert.ok(result.runtime_files > 0);
  const receipt = JSON.parse(readFileSync(path.join(f.base, "runtime-receipt.json"))); const entry = receipt.files.find((v) => v.path.endsWith("renewal-handoff.mjs")); assert.ok(entry); assert.equal(entry.sha256, hash(readFileSync(path.join(f.base, entry.path))));
  assert.throws(() => execFileSync(process.execPath, args, { encoding: "utf8", stdio: "pipe" }), /Runtime already exists/);
});

test("checked receipt refuses STOP, incomplete checks, or replaced clips", async (t) => {
  const f = await fixture(t);
  const entry = f.manifest.videos[0];
  const timeline = { speech_hash: "speech", translation_hash: "translation", lines: [{ id: "line1" }] };
  json(path.join(entry.workdir, "dubs/en/timeline.json"), timeline);
  writeFileSync(path.join(entry.workdir, "dubs/en.m4a"), "checked m4a");
  const clip = path.join(entry.workdir, "dubs/en/audio/line1.wav");
  mkdirSync(path.dirname(clip), { recursive: true }); writeFileSync(clip, "checked clip");
  json(path.join(path.dirname(entry.doc_file), "i18n/en.json"), { lines: { line1: { text: "The actual words" } } });
  json(path.join(entry.workdir, "review/check-flags.en.json"), { locale: "en", speech_hash: "speech", translation_hash: "translation", flags: [] });
  json(path.join(entry.workdir, "review/check.en.json"), { lines: { line1: { heard: "The actual words", intended: "The actual words", clip: (await sha256File(clip)).slice(0, 16) } } });
  await assert.rejects(checkedDubReceipt(entry, "en", 0), /no new, complete/);
  recordStage(entry.workdir, "check-audio", { locale: "en", lines: 1, unchecked: 1, flagged: 0 });
  await assert.rejects(checkedDubReceipt(entry, "en", 0), /no new, complete/);
  recordStage(entry.workdir, "check-audio", { locale: "en", lines: 1, unchecked: 0, flagged: 0 });
  const receipt = await checkedDubReceipt(entry, "en", 1);
  assert.equal(receipt.sha256, hash("checked m4a"));
  assert.equal(receipt.speech_hash, "speech");
  await assert.rejects(checkedDubReceipt(entry, "en", 2), /no new, complete/);
  writeFileSync(clip, "different clip");
  await assert.rejects(checkedDubReceipt(entry, "en", 1), /current clip/);
});

test("client forwards shortening variant, uploads audio/mp4 references, and stops quota without retry", async (t) => {
  const f = await fixture(t);
  const requests = [];
  const ctx = { home: f.base, env: { MOKAAIR_SITE: "https://example.com", MOKAAIR_VIDEO_TOKEN: "test-token" }, sleep: async () => {}, fetch: async (url, init) => { requests.push({ url, init }); return Response.json({ complete: true }); } };
  const client = createSiteClient(ctx);
  await client.run("translator", SLUGS[0], "instructions", {}, 100, "slides", "shorten");
  assert.equal(JSON.parse(requests[0].init.body).variant, "shorten");
  const file = path.join(f.base, "en.m4a"); writeFileSync(file, "track");
  const record = await client.upload(SLUGS[0], { ...ref("dub_en", "track"), path: file });
  assert.equal(record.content_type, "audio/mp4");
  assert.match(requests[1].url, /\/files\/.*part=0&parts=1&size=5$/);
  let failures = 0;
  const limited = createSiteClient({ ...ctx, fetch: async () => { failures++; return Response.json({ code: "video_ai_budget_exhausted", detail: "cap reached" }, { status: 429 }); } });
  await assert.rejects(limited.run("translator", SLUGS[0], "", {}, 1, "slides"), HardStop);
  assert.equal(failures, 1);
  assert.throws(() => client.submit(SLUGS[0], { gate: "publish" }), /Only a languages/);
});

test("phase completion requires actual server ready states for every selected part", () => {
  const project = remote({ slug: SLUGS[0], final_sha256: hash("final") });
  project.languages.en.metadata.state = "ready";
  assert.deepEqual(missingPhaseParts(project, "translations"), ["en/captions"]);
  assert.deepEqual(missingPhaseParts(project, "dubs"), ["en/dub"]);
  project.languages.en.captions.state = "ready";
  project.languages.en.dub.state = "skipped";
  assert.deepEqual(missingPhaseParts(project, "all"), []);
});

test("direct stage transport is explicit, internal-only, and changes only the stage POST", async (t) => {
  const f = await fixture(t);
  const calls = [];
  const env = { MOKAAIR_SITE: "http://web:3000", MOKAAIR_VIDEO_TOKEN: "test-token", VIDEO_LANGUAGE_API_ORIGIN: "http://api:8000" };
  const client = createSiteClient({ home: f.base, env, sleep: async () => {}, fetch: async (url, init) => { calls.push({ kind: "fetch", url, init }); return Response.json({}); }, nativeStageRequest: async (url, init) => { calls.push({ kind: "native", url, init }); return Response.json({ text: "stage result" }); } });
  await client.settings();
  assert.deepEqual(await client.run("translator", SLUGS[0], "prompt", {}, 100, "slides", "shorten"), { text: "stage result" });
  await client.submit(SLUGS[0], { gate: "languages" });
  assert.deepEqual(calls.map(({ kind }) => kind), ["fetch", "native", "fetch"]);
  assert.equal(calls[1].url, "http://api:8000/api/v1/video/automation/run");
  assert.equal(calls[1].init.headers.Authorization, calls[0].init.headers.Authorization);
  assert.equal(JSON.parse(calls[1].init.body).variant, "shorten");
  assert.equal(calls[2].url, `http://web:3000/api/video/reviews/${SLUGS[0]}/reviews`);
  assert.equal(directStageOrigin({}, "https://mokaair.com"), null);
  for (const origin of ["https://example.com", "http://api:8000/", "http://api:8000/path", "http://user:secret@api:8000", "http://api:8000?x=1", "http://127.0.0.1:8000"]) assert.throws(() => directStageOrigin({ ...env, VIDEO_LANGUAGE_API_ORIGIN: origin }, env.MOKAAIR_SITE), /exact internal origins/);
  assert.throws(() => directStageOrigin(env, "https://mokaair.com"), /exact internal origins/);
  assert.throws(() => directStageOrigin({ VIDEO_LANGUAGE_API_ORIGIN: "http://api:8000" }, "http://web:3000"), /exact internal origins/);
});

test("POST network failures and 5xx are never retried; GET and file PUT retain bounded retries", async (t) => {
  const f = await fixture(t);
  const env = { MOKAAIR_SITE: "https://example.com", MOKAAIR_VIDEO_TOKEN: "test-token" };
  for (const failure of ["network", "503"]) {
    for (const operation of ["run", "submit"]) {
      let calls = 0;
      const client = createSiteClient({ home: f.base, env, sleep: async () => { assert.fail("POST must not sleep for a retry"); }, fetch: async () => { calls++; if (failure === "network") throw new Error("connection closed"); return Response.json({ detail: "gateway timed out" }, { status: 503 }); } });
      await assert.rejects(operation === "run" ? client.run("translator", SLUGS[0], "", {}, 100, "slides") : client.submit(SLUGS[0], { gate: "languages" }), /POST was not retried/);
      assert.equal(calls, 1);
    }
  }
  const counts = { GET: 0, PUT: 0 };
  const client = createSiteClient({ home: f.base, env, sleep: async () => {}, fetch: async (_url, init) => { counts[init.method]++; return counts[init.method] === 1 ? Response.json({}, { status: 503 }) : Response.json({ complete: true }); } });
  await client.settings();
  const file = path.join(f.base, "dub.m4a"); writeFileSync(file, "dub");
  await client.upload(SLUGS[0], { ...ref("dub_en", "dub"), path: file });
  assert.deepEqual(counts, { GET: 2, PUT: 2 });
});

test("direct stage preserves quota/auth hard stops and never retries its unknown result", async (t) => {
  const f = await fixture(t);
  const env = { MOKAAIR_SITE: "http://web:3000", MOKAAIR_VIDEO_TOKEN: "test-token", VIDEO_LANGUAGE_API_ORIGIN: "http://api:8000" };
  for (const status of [401, 403, 429, 503]) {
    let calls = 0;
    const client = createSiteClient({ home: f.base, env, sleep: async () => assert.fail("direct POST must not retry"), fetch: async () => assert.fail("stage cannot use BFF"), nativeStageRequest: async () => { calls++; return Response.json({ detail: "refused" }, { status }); } });
    await assert.rejects(client.run("translator", SLUGS[0], "", {}, 100, "slides"), status === 503 ? VideoStop : HardStop);
    assert.equal(calls, 1);
  }
});

test("native transport accepts delayed headers, bounds the whole request and limits response bytes", async (t) => {
  assert.equal(DIRECT_STAGE_TIMEOUT_MS, 1_020_000);
  const server = createServer((request, response) => {
    if (request.url === "/waiting") return;
    if (request.url === "/large") { response.end("x".repeat(1024)); return; }
    setTimeout(() => { response.setHeader("Content-Type", "application/json"); response.end(JSON.stringify({ received: request.method })); }, 30);
  });
  await new Promise((resolve) => server.listen(0, "127.0.0.1", resolve));
  t.after(() => { server.closeAllConnections(); server.close(); });
  const origin = `http://127.0.0.1:${server.address().port}`;
  const init = { method: "POST", headers: { "Content-Type": "application/json" }, body: "{}" };
  const result = await nativeStageRequest(`${origin}/delayed`, init, { timeoutMs: 1000 });
  assert.deepEqual(await result.json(), { received: "POST" });
  await assert.rejects(nativeStageRequest(`${origin}/waiting`, init, { timeoutMs: 30 }), /total deadline/);
  await assert.rejects(nativeStageRequest(`${origin}/large`, init, { maxBytes: 64, timeoutMs: 1000 }), /byte limit/);
  await assert.rejects(nativeStageRequest(`${origin}/large`, { ...init, body: "x".repeat(4 * 1024 * 1024 + 1) }, { requestImpl: () => assert.fail("oversized request must not leave this process") }), /request exceeds the byte limit/);
});

async function resumeFixture(t) {
  const f = await fixture(t);
  const entry = f.manifest.videos[0];
  const calls = [];
  const ctx = { runCommand: async (args) => {
    calls.push(args[0]);
    let out = "";
    const sink = { write: (text) => { out += text; } };
    const code = await videoMain(args, { root: f.manifest.root, env: { VIDEO_WORKDIR: f.manifest.work_base }, stdout: sink, stderr: sink });
    return { code, out };
  } };
  const parts = ["metadata", "captions"];
  assert.equal((await ctx.runCommand(["i18n-sheet", "--slug", entry.slug, "--locale", "en", "--parts", parts.join(",")])).code, 0);
  const file = path.join(entry.workdir, "i18n/en.todo.json");
  const fresh = JSON.parse(readFileSync(file, "utf8"));
  const translated = structuredClone(fresh);
  translated.lines.forEach((line) => { line.text = `Translated ${line.id}`; });
  translated.chapters.forEach((chapter) => { chapter.text = `Chapter ${chapter.scene}`; });
  translated.title.text = "Translated title";
  translated.description.text = "Translated description";
  translated.tags.text = ["AI"];
  json(file, translated);
  calls.length = 0;
  return { ...f, entry, ctx, parts, file, fresh, translated, calls, project: loadProject({ slug: entry.slug, root: f.manifest.root }), state: { slug: entry.slug, format: "slides" } };
}

test("an interrupted translated worksheet is source-checked then independently reviewed and merged without another translator", async (t) => {
  const f = await resumeFixture(t);
  const saved = readFileSync(f.file, "utf8");
  const events = [];
  const stages = [];
  const automation = {
    translateLocale: () => assert.fail("must reuse the paid translation"),
    stage: async (stage, slug, payload) => {
      stages.push(stage);
      assert.equal(slug, f.entry.slug);
      assert.deepEqual(payload.worksheet, f.translated);
      assert.equal(existsSync(path.join(f.project.dir, "i18n/en.json")), false, "source validation did not merge or approve");
      const checked = structuredClone(payload.worksheet);
      checked.lines[0].text = "Independently corrected English";
      return { worksheet: checked };
    }, cleared: () => {}, persist: () => {},
  };
  await translateLocaleResuming(automation, f.ctx, f.entry, f.state, "en", f.parts, f.project, (event) => events.push(event));
  assert.deepEqual(stages, ["caption_reviewer"]);
  assert.deepEqual(f.calls, ["i18n-sheet", "i18n-merge"]);
  assert.equal(events[0].worksheet_sha256, hash(saved));
  assert.equal(loadProject({ slug: f.entry.slug, root: f.manifest.root }).translations.en.lines[f.translated.lines[0].id].text, "Independently corrected English");
  assert.equal(readFileSync(path.join(f.entry.workdir, "i18n", `en.todo.resume-${hash(saved)}.json`), "utf8"), saved);
});

test("resume refuses changed sources, identity, budgets, missing content and missing reviewer output while preserving the paid worksheet", async (t) => {
  const f = await resumeFixture(t);
  for (const mutate of [
    (sheet) => { sheet.slug = SLUGS[1]; }, (sheet) => { sheet.locale = "ja"; },
    (sheet) => { sheet.parts = ["captions"]; }, (sheet) => { sheet.lines[0].source += " changed"; },
    (sheet) => { sheet.lines[0].id = "wrong"; }, (sheet) => { sheet.lines[0].scene = "wrong"; },
    (sheet) => { sheet.lines[0].max_chars = 1; }, (sheet) => { sheet.lines.pop(); },
    (sheet) => { sheet.title.source += " changed"; }, (sheet) => { sheet.chapters[0].source += " changed"; },
    (sheet) => { sheet.tags.source.push("changed"); }, (sheet) => { sheet.lines[0].text = ""; },
  ]) {
    const wrong = structuredClone(f.translated);
    mutate(wrong);
    assert.throws(() => validateResumeSheet(wrong, f.fresh, f.project.doc), VideoStop);
  }
  const wrong = structuredClone(f.translated);
  wrong.lines[0].source += " changed";
  json(f.file, wrong);
  const badBytes = readFileSync(f.file, "utf8");
  const automation = { stage: () => assert.fail("source drift must stop before paid review"), translateLocale: () => assert.fail("must not overwrite paid translation") };
  await assert.rejects(translateLocaleResuming(automation, f.ctx, f.entry, f.state, "en", f.parts, f.project), /differs from the current sheet/);
  assert.equal(readFileSync(f.file, "utf8"), badBytes);
  assert.equal(existsSync(path.join(f.project.dir, "i18n/en.json")), false);
  json(f.file, f.translated);
  const original = readFileSync(f.file, "utf8");
  for (const answer of [{}, { worksheet: { ...f.translated, lines: [] } }]) {
    await assert.rejects(translateLocaleResuming({ ...automation, stage: async () => answer }, f.ctx, f.entry, f.state, "en", f.parts, f.project), VideoStop);
    assert.equal(readFileSync(f.file, "utf8"), original);
    assert.equal(existsSync(path.join(f.project.dir, "i18n/en.json")), false, "an absent or incomplete review never becomes ready");
  }
  await assert.rejects(translateLocaleResuming({ ...automation, stage: async () => { throw new VideoStop("connection ended after review began"); } }, f.ctx, f.entry, f.state, "en", f.parts, f.project), /connection ended/);
  assert.equal(readFileSync(f.file, "utf8"), original);
  assert.equal(f.calls.includes("i18n-merge"), false);
});

test("fresh translations cannot bypass an absent independent review, and the next invocation resumes only that review", async (t) => {
  const f = await resumeFixture(t);
  json(f.file, f.fresh);
  const stages = [];
  const ctx = { ...f.ctx, root: f.manifest.root, env: { VIDEO_WORKDIR: f.manifest.work_base }, now: () => new Date(), stdout: { write: () => {} } };
  const automation = new Automation(ctx, { report: async () => {} }, {});
  const missingReview = async (stage) => {
    stages.push(stage);
    return stage === "translator" ? { worksheet: structuredClone(f.translated) } : {};
  };
  automation.stage = missingReview;
  await assert.rejects(translateLocaleResuming(automation, ctx, f.entry, f.state, "en", f.parts, f.project), /caption_reviewer returned no worksheet/);
  assert.deepEqual(stages, ["translator", "caption_reviewer"]);
  assert.equal(automation.stage, missingReview, "temporary strict wrapper is always restored");
  assert.equal(f.calls.includes("i18n-merge"), false);
  assert.equal(existsSync(path.join(f.project.dir, "i18n/en.json")), false);
  const kept = readUnits(f.entry.workdir, "en");
  assert.deepEqual(kept[unitKey(f.fresh, null)].translated, f.translated, "successful paid translation remains source-bound in the unit cache after a failed review");
  assert.equal(kept[unitKey({ ...f.fresh, slug: "changed-source" }, null)], undefined);
  stages.length = 0;
  automation.stage = async (stage) => { stages.push(stage); return { worksheet: structuredClone(f.translated) }; };
  await translateLocaleResuming(automation, ctx, f.entry, f.state, "en", f.parts, f.project);
  assert.deepEqual(stages, ["caption_reviewer"]);
  assert.equal(existsSync(path.join(f.project.dir, "i18n/en.json")), true);
});

test("one failed video does not starve the next, while owner/quota failure stops all", async (t) => {
  const f = await fixture(t, 2);
  const projects = new Map(f.manifest.videos.map((entry) => [entry.slug, remote(entry)]));
  const calls = [];
  const api = { reviews: async (slug) => structuredClone(projects.get(slug)), settings: async () => ({}), upload: async () => {}, submit: async (slug, body) => { calls.push(["submit", slug]); const review = { ...body, id: `lang-${slug}`, status: "approved", created_at: "2026-09-29T02:00:00Z" }; projects.get(slug).reviews.push(review); return review; } };
  class FakeAutomation {
    constructor(ctx) { this.ctx = ctx; }
    async translateLocale(state, locale) {
      calls.push(["translate", state.slug]);
      if (state.slug === SLUGS[0]) throw new VideoStop("bad translation");
      json(path.join(f.manifest.root, "docs/videos", state.slug, "i18n", `${locale}.json`), { title: "Evidence", description: "An example description.", tags: [], chapters: {}, lines: {} });
      return "translated and reviewed";
    }
  }
  const runMain = async (args) => {
    const slug = args[args.indexOf("--slug") + 1];
    const entry = f.manifest.videos.find((item) => item.slug === slug);
    if (args[0] === "review-pull") await approve({ gate: "final", docDir: path.dirname(entry.doc_file), workdir: entry.workdir });
    if (args[0] === "captions") {
      const temporaryChoice = JSON.parse(readFileSync(path.join(entry.workdir, "languages.json"), "utf8"));
      assert.equal(temporaryChoice.locales.en.dub, false, "unverified or absent dub cannot drive the captions");
      const timeline = JSON.parse(readFileSync(path.join(entry.workdir, "timeline.json"), "utf8"));
      json(path.join(entry.workdir, "captions/manifest.json"), { speech_hash: timeline.speech_hash, locales: { en: { cues: 1, problems: [] } } });
      writeFileSync(path.join(entry.workdir, "captions/en.srt"), "1\n00:00:00,000 --> 00:00:01,000\nEvidence\n");
    }
    return 0;
  };
  const result = await run({ manifest: f.manifestFile, slugs: SLUGS.slice(0, 2), phase: "translations", maxUnits: 2, dryRun: false }, { api, runMain, AutomationClass: FakeAutomation });
  assert.equal(result.status, "paused");
  assert.deepEqual(calls.filter(([kind]) => kind === "translate").map(([, slug]) => slug), SLUGS.slice(0, 2));
  assert.ok(calls.some(([kind, slug]) => kind === "submit" && slug === SLUGS[1]));
  assert.equal(existsSync(path.join(f.base, "runner.lock")), false);
  assert.equal(projects.get(SLUGS[1]).title, "Original title");
  const restoredChoice = JSON.parse(readFileSync(path.join(f.manifest.videos[1].workdir, "languages.json"), "utf8"));
  assert.equal(restoredChoice.locales.en.dub, true, "the owner's local choice is restored after captions");
  calls.length = 0;
  class FatalAutomation { async translateLocale(state) { calls.push(["translate", state.slug]); throw new HardStop("quota exhausted"); } }
  await assert.rejects(run({ manifest: f.manifestFile, slugs: SLUGS.slice(0, 2), phase: "translations", dryRun: false }, { api, runMain, AutomationClass: FatalAutomation }), /quota exhausted/);
  assert.deepEqual(calls, [["translate", SLUGS[0]]]);
});

// These integration cases use the real runner, videoMain, dub CLI and speech
// client. Only HTTP is stubbed; the source fixture and generated bookends are
// isolated test data, and no listening or language approval is invented.
async function nativeSpeechRunnerFixture(t) {
  const brandDir = mkdtempSync(path.join(os.tmpdir(), "native-speech-brand-"));
  t.after(() => rmSync(brandDir, { recursive: true, force: true }));
  const { locateFfmpeg } = await import("../../../tools/video/assemble/ffmpeg.mjs");
  const binaries = await locateFfmpeg();
  const brandingBytes = {};
  for (const [role, seconds] of [["intro", 5], ["outro", 3]]) {
    const file = path.join(brandDir, `${role}.mp4`);
    execFileSync(binaries.ffmpeg, ["-hide_banner", "-loglevel", "error", "-y", "-f", "lavfi", "-i", "color=black:s=1920x1080:r=30", "-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", String(seconds), "-c:v", "libx264", "-preset", "ultrafast", "-threads", "2", "-pix_fmt", "yuv420p", "-c:a", "aac", file]);
    brandingBytes[role] = readFileSync(file);
  }
  const f = await currentApprovedFixture(t, { dub: true, brandingBytes });
  const group = `${f.base}-native-speech-group`, out = path.join(group, "batch");
  mkdirSync(group); t.after(() => rmSync(group, { recursive: true, force: true }));
  const prepared = await prepareApprovedFinalBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out, readRemote: async () => structuredClone(f.site), runtimeRoot: f.runtimeRoot });
  const manifest = resolveManifest(JSON.parse(readFileSync(prepared.manifest)), out), entry = manifest.videos[0], project = loadProject({ slug: entry.slug, root: manifest.root });
  rmSync(path.join(out, "STOP")); rmSync(path.join(entry.workdir, "STOP"));
  const translation = path.join(project.dir, "i18n/en.json");
  json(translation, { title: "Actual English title", description: "Reviewed English body", tags: [], chapters: {}, lines: Object.fromEntries([...eachLine(project.doc)].map(({ line }) => [line.id, { text: `English ${line.id}`, source_hash: textHash(line.text) }])) });
  const progress = JSON.parse(readFileSync(path.join(out, "progress.json")));
  progress.videos[entry.slug] = { final_sha256: entry.final_sha256, translations: { en: hash(readFileSync(translation)) }, checked_dubs: {}, skipped_dubs: {} };
  json(path.join(out, "progress.json"), progress);
  const api = { reviews: async () => structuredClone(f.site), settings: async () => ({}), run: async () => assert.fail("translator dispatch is outside the seeded dubs fixture") };
  const env = { MOKAAIR_SITE: "https://mokaair.com", MOKAAIR_VIDEO_TOKEN: `mkv_${"x".repeat(40)}` };
  const status = { configured: true, voices: [], gemini_configured: true, gemini_models: ["gemini-3.8-flash-tts"], gemini_voices: ["Sulafat"], max_request_characters: 1500, monthly_limit: 1_000_000, gemini_monthly_limit: 1_000_000 };
  const options = { manifest: prepared.manifest, slugs: [entry.slug], phase: "dubs", maxUnits: 1, dryRun: false };
  const events = () => readFileSync(path.join(out, "events.jsonl"), "utf8").trim().split("\n").map(JSON.parse);
  return { ...f, out, manifest, entry, api, env, status, options, events };
}

test("actual runner and native dub keep an unknown speech POST held across invocations", async (t) => {
  const f = await nativeSpeechRunnerFixture(t);
  let posts = 0, statusGets = 0, reviewGets = 0;
  const fetch = async (url, init = {}) => {
    const route = new URL(url).pathname;
    if (init.method === "POST") {
      assert.equal(route, "/api/video/speech"); posts++;
      throw new Error("response lost after accepted synthesis");
    }
    if (route.startsWith("/api/video/reviews/")) { reviewGets++; return Response.json(f.site); }
    if (route === "/api/video/speech/status") { statusGets++; return Response.json(f.status); }
    assert.fail(`unplanned offline request ${route}`);
  };
  const dependencies = { api: f.api, fetch, env: f.env, home: f.out, sleep: async () => {} };
  for (let attempt = 0; attempt < 2; attempt++) {
    const result = await run(f.options, dependencies);
    assert.equal(result.status, "paused"); assert.equal(posts, 1);
    assert.match(result.videos[f.entry.slug].error, /saved result is held/);
    assert.deepEqual(result.videos[f.entry.slug].checked_dubs, {});
    assert.deepEqual(result.videos[f.entry.slug].skipped_dubs, {});
  }
  assert.equal(reviewGets, 2); assert.equal(statusGets, 4);
  assert.deepEqual(f.events().filter((event) => event.type === "command" && event.command === "dub").map((event) => event.code), [4, 4]);
  const journal = JSON.parse(readFileSync(path.join(f.entry.workdir, "speech-journal/journal.json")));
  assert.equal(Object.keys(journal.entries).length, 1);
  assert.equal(Object.values(journal.entries)[0].status, "unknown");
  assert.equal(journal.identity.final_sha256, f.entry.final_sha256);
  assert.equal(readFileSync(path.join(f.entry.workdir, "speech-journal/journal.json"), "utf8").includes(f.env.MOKAAIR_VIDEO_TOKEN), false);
  await verifyLocal(f.manifest, f.entry);
});

test("actual runner and native dub replay saved raw WAV after consumer interruption without a second POST", async (t) => {
  const f = await nativeSpeechRunnerFixture(t), audio = path.join(f.entry.workdir, "dubs/en/audio"), retained = `${audio}.retained`;
  const { renameSync, statSync } = await import("node:fs");
  const { encodeWav } = await import("../../../tools/video/tts/wav.mjs");
  let posts = 0, statusGets = 0, reviewGets = 0, attempt = 1, faults = 0, rawWav;
  const interruptConsumer = () => {
    assert.ok(statSync(audio).isDirectory()); assert.deepEqual(readdirSync(audio), []);
    renameSync(audio, retained); writeFileSync(audio, "fixture-only blocked audio destination"); faults++;
  };
  const fetch = async (url, init = {}) => {
    const route = new URL(url).pathname;
    if (init.method === "POST") {
      assert.equal(route, "/api/video/speech"); posts++;
      assert.equal(posts, 1, "consumer restart cannot buy the saved response again");
      const body = JSON.parse(init.body), rate = 24_000, parts = [];
      for (const segment of body.segments) {
        const tone = new Int16Array(rate / 5);
        for (let index = 0; index < tone.length; index++) tone[index] = Math.round(8000 * Math.sin(2 * Math.PI * 220 * index / rate));
        parts.push(tone, new Int16Array(Math.round((segment.break_after_ms ?? 0) * rate / 1000)));
      }
      const samples = new Int16Array(parts.reduce((sum, part) => sum + part.length, 0));
      let start = 0; for (const part of parts) { samples.set(part, start); start += part.length; }
      rawWav = encodeWav(samples, rate);
      interruptConsumer();
      return new Response(rawWav, { headers: { "content-type": "audio/wav", "x-billable-characters": "137", "cache-control": "no-store" } });
    }
    if (route.startsWith("/api/video/reviews/")) { reviewGets++; return Response.json(f.site); }
    if (route === "/api/video/speech/status") {
      statusGets++;
      // Each invocation probes status once before mkdir(audio), then again in
      // the journal's fresh paid-boundary identity. Interrupt only the latter,
      // so the second native call must consume the saved WAV before it fails.
      if (attempt === 2 && statusGets === 4) interruptConsumer();
      return Response.json(f.status);
    }
    assert.fail(`unplanned offline request ${route}`);
  };
  const dependencies = { api: f.api, fetch, env: f.env, home: f.out, sleep: async () => {} };
  const first = await run(f.options, dependencies);
  assert.equal(first.status, "paused"); assert.match(first.videos[f.entry.slug].error, /^EEXIST:/);
  const journalFile = path.join(f.entry.workdir, "speech-journal/journal.json"), firstReceipt = readFileSync(journalFile), journal = JSON.parse(firstReceipt), record = Object.values(journal.entries)[0];
  assert.equal(posts, 1); assert.equal(Object.keys(journal.entries).length, 1); assert.equal(record.status, "succeeded");
  assert.equal(record.response.sha256, hash(rawWav));
  assert.equal(record.response.headers["x-billable-characters"], "137");
  assert.deepEqual(readFileSync(path.join(f.entry.workdir, "speech-journal", record.response.file)), rawWav);
  // Repair only the generated test destination; retain the successful journal
  // and source bytes. No approval, transcript or checked dub is fabricated.
  assert.ok(statSync(audio).isFile()); rmSync(audio); renameSync(retained, audio); attempt = 2;
  const second = await run(f.options, dependencies);
  assert.equal(second.status, "paused"); assert.match(second.videos[f.entry.slug].error, /^EEXIST:/);
  assert.equal(posts, 1); assert.equal(faults, 2); assert.equal(statusGets, 4); assert.equal(reviewGets, 2);
  assert.equal(f.events().filter((event) => event.type === "unit-start" && event.kind === "dub").length, 2);
  assert.equal(f.events().filter((event) => event.type === "error" && event.detail.startsWith("EEXIST:")).length, 2);
  assert.deepEqual(readFileSync(journalFile), firstReceipt);
  assert.deepEqual(second.videos[f.entry.slug].checked_dubs, {}); assert.deepEqual(second.videos[f.entry.slug].skipped_dubs, {});
  await verifyLocal(f.manifest, f.entry);
});

test("actual runner refuses a video or batch STOP added during its fresh speech status probe", async (t) => {
  for (const scope of ["video", "batch"]) await t.test(scope, async (t) => {
    const f = await nativeSpeechRunnerFixture(t), stop = path.join(scope === "video" ? f.entry.workdir : f.out, "STOP");
    let posts = 0, statusGets = 0;
    const fetch = async (url, init = {}) => {
      const route = new URL(url).pathname;
      if (init.method === "POST") { posts++; assert.fail("STOP prevents a paid speech POST"); }
      if (route.startsWith("/api/video/reviews/")) return Response.json(f.site);
      if (route === "/api/video/speech/status") {
        if (++statusGets === 2) writeFileSync(stop, "owner STOP during the fresh paid-boundary status probe");
        return Response.json(f.status);
      }
      assert.fail(`unplanned offline request ${route}`);
    };
    const result = await run(f.options, { api: f.api, fetch, env: f.env, home: f.out, sleep: async () => {} });
    assert.equal(result.status, "paused"); assert.equal(posts, 0); assert.equal(statusGets, 2); assert.ok(existsSync(stop));
    assert.equal(existsSync(path.join(f.entry.workdir, "speech-journal")), false);
    assert.deepEqual(result.videos[f.entry.slug].checked_dubs, {}); assert.deepEqual(result.videos[f.entry.slug].skipped_dubs, {});
    await verifyLocal(f.manifest, f.entry);
  });
});

test("actual runner stops the direct translator after the native worksheet without creating a paid intent", async (t) => {
  const f = await nativeSpeechRunnerFixture(t);
  rmSync(path.join(path.dirname(f.entry.doc_file), "i18n/en.json"));
  const progress = JSON.parse(readFileSync(path.join(f.out, "progress.json")));
  progress.videos[f.entry.slug].translations = {}; json(path.join(f.out, "progress.json"), progress);
  let posts = 0, stopWritten = false;
  const worksheet = path.join(f.entry.workdir, "i18n/en.todo.json"), stop = path.join(f.out, "STOP");
  const api = { ...f.api, run: async () => { posts++; assert.fail("STOP prevents direct translator dispatch"); } };
  const now = () => {
    // The real i18n-sheet has finished. Its command event yields before the
    // stage client runs, so this models an owner STOP at that paid boundary.
    if (!stopWritten && existsSync(worksheet)) { writeFileSync(stop, "owner STOP after the actual native worksheet"); stopWritten = true; }
    return new Date("2026-10-04T00:00:00Z");
  };
  const fetch = async (url, init = {}) => {
    assert.notEqual(init.method, "POST"); assert.ok(new URL(url).pathname.startsWith("/api/video/reviews/"));
    return Response.json(f.site);
  };
  const env = { ...f.env, MOKAAIR_SITE: "http://web:3000", VIDEO_LANGUAGE_API_ORIGIN: "http://api:8000" };
  await assert.rejects(run({ ...f.options, phase: "translations" }, { api, fetch, env, now, home: f.out, sleep: async () => {} }), /STOP requested/);
  assert.equal(posts, 0); assert.ok(stopWritten); assert.ok(existsSync(worksheet));
  assert.ok(f.events().some((event) => event.type === "unit-start" && event.kind === "translate"));
  assert.ok(f.events().some((event) => event.type === "command" && event.command === "i18n-sheet" && event.code === 0));
  assert.equal(existsSync(path.join(f.entry.workdir, "language-stage-journal.json")), false);
  assert.ok(existsSync(path.join(f.out, "STOP")));
});

test("direct native stage transport honors STOP before intent and preserves cached or unknown answers", async (t) => {
  for (const savedStatus of ["none", "succeeded", "unknown"]) await t.test(savedStatus, async (t) => {
    const f = await fixture(t), entry = f.manifest.videos[0], stop = path.join(f.base, "STOP");
    const manifest = { ...f.manifest, source_kind: "approved-final-body-range", request_namespace: "11111111-1111-4111-8111-111111111111" };
    entry.renewal_source = { sha256: hash("exact current source") };
    let posts = 0, armStop = false;
    const api = createSiteClient({ env: { MOKAAIR_SITE: "http://web:3000", MOKAAIR_VIDEO_TOKEN: `mkv_${"x".repeat(40)}`, VIDEO_LANGUAGE_API_ORIGIN: "http://api:8000" }, fetch: async () => assert.fail("direct stage must not use BFF fetch"), sleep: async () => {}, nativeStageRequest: async (url, init) => {
      posts++; assert.equal(url, "http://api:8000/api/v1/video/automation/run"); assert.equal(init.method, "POST");
      if (savedStatus === "unknown") throw new Error("direct response lost after accepted request");
      return Response.json({ text: "Actual saved answer", model: "actual upstream alias", usage: { tokens: 30 } });
    } });
    const now = () => { if (armStop) writeFileSync(stop, "owner STOP before the stage intent"); return "2026-10-04T00:00:00Z"; };
    const client = () => journaledStageClient(api, manifest, [entry], now, { readCurrent: async () => ({ settings: {}, choice: null }) }), args = ["translator", entry.slug, "Exact instructions", { locale: "en" }, 32000, "slides"];
    const file = path.join(entry.workdir, "language-stage-journal.json");
    if (savedStatus === "none") {
      armStop = true; await assert.rejects(client().run(...args), /STOP requested/);
      assert.equal(posts, 0); assert.equal(existsSync(file), false);
    } else {
      if (savedStatus === "unknown") await assert.rejects(client().run(...args), /lost/); else await client().run(...args);
      const receipt = readFileSync(file); assert.equal(Object.values(JSON.parse(receipt).entries)[0].status, savedStatus);
      writeFileSync(stop, "owner STOP before reusing any paid answer");
      await assert.rejects(client().run(...args), /STOP requested/); assert.equal(posts, 1);
      assert.deepEqual(readFileSync(file), receipt);
    }
    assert.ok(existsSync(stop));
  });
});

test("actual translator success is retained while fresh owner, source or settings drift stops the next paid reviewer", async (t) => {
  for (const drift of ["choice", "drop", "final", "source", "model", "provider", "instructions"]) await t.test(drift, async (t) => {
    const f = await currentApprovedFixture(t), group = `${f.base}-fresh-stage-${drift}`, out = path.join(group, "batch");
    mkdirSync(group); t.after(() => rmSync(group, { recursive: true, force: true }));
    const prepared = await prepareApprovedFinalBatch({ manifestFile: f.manifestFile, handoffs: [{ slug: f.entry.slug, workdir: f.prepared }], out, readRemote: async () => structuredClone(f.site), runtimeRoot: f.runtimeRoot });
    const workdir = path.join(out, "work", f.entry.slug), file = path.join(workdir, "language-stage-journal.json");
    rmSync(path.join(out, "STOP")); rmSync(path.join(workdir, "STOP"));
    const stages = []; let firstReceipt, firstResult;
    const settings = { durable_stage_runs: true, stage_models: { translator: { provider: "claude_code", model: "selected-translator" }, caption_reviewer: { provider: "claude_code", model: "selected-caption-reviewer" } }, stage_instructions: { translator: "Preserve actual source", caption_reviewer: "Review actual draft" } };
    const api = {
      reviews: async () => {
        if (stages.length === 1 && existsSync(file) && !firstReceipt) firstReceipt = readFileSync(file);
        return structuredClone(f.site);
      },
      settings: async () => structuredClone(settings),
      run: async (stage, _slug, _instructions, payload) => {
        stages.push(stage); assert.equal(stage, "translator", "fresh drift prevents the second paid reviewer");
        const worksheet = structuredClone(payload.worksheet);
        for (const line of worksheet.lines ?? []) line.text = `English ${line.id}`;
        for (const chapter of worksheet.chapters ?? []) chapter.text = "English chapter";
        if (worksheet.title) worksheet.title.text = "English title";
        if (worksheet.description) worksheet.description.text = "Reviewed English description";
        if (worksheet.tags) worksheet.tags.text = ["AI"];
        const final = f.site.reviews.find((review) => review.gate === "final" && review.status === "approved");
        if (drift === "choice") { f.site.locales.en.metadata = false; f.site.locales.en.captions = false; }
        if (drift === "drop") f.site.dropped_at = "2026-10-04T00:00:00Z";
        if (drift === "final") final.status = "pending";
        if (drift === "source") final.files.find((entry) => entry.role === "evidence_script").sha256 = "f".repeat(64);
        if (drift === "model") settings.stage_models.caption_reviewer.model = "owner-selected-new-model";
        if (drift === "provider") settings.stage_models.caption_reviewer.provider = "gemini";
        if (drift === "instructions") settings.stage_instructions.caption_reviewer = "owner-selected-new-instructions";
        // The selected model and actual upstream alias need not be the same.
        firstResult = { text: JSON.stringify({ worksheet }), model: "upstream-actual-alias", input_tokens: 1, output_tokens: 1, usage: { tokens: 2, token_budget: 100 } };
        return structuredClone(firstResult);
      },
    };
    const fetch = async (url, init = {}) => {
      assert.notEqual(init.method, "POST"); assert.ok(new URL(url).pathname.startsWith("/api/video/reviews/"));
      return Response.json(f.site);
    };
    const result = await run({ manifest: prepared.manifest, slugs: [f.entry.slug], phase: "translations", maxUnits: 1, dryRun: false }, { api, fetch, env: { MOKAAIR_SITE: "http://web:3000", VIDEO_LANGUAGE_API_ORIGIN: "http://api:8000", MOKAAIR_VIDEO_TOKEN: `mkv_${"x".repeat(40)}` }, home: out, sleep: async () => {} });
    assert.equal(result.status, "paused"); assert.deepEqual(stages, ["translator"]);
    assert.ok(firstReceipt, "fresh owner probe occurs between the two paid stages");
    assert.deepEqual(readFileSync(file), firstReceipt);
    const journal = JSON.parse(firstReceipt), record = Object.values(journal.entries)[0];
    assert.equal(Object.keys(journal.entries).length, 1); assert.equal(record.status, "succeeded"); assert.deepEqual(record.result, firstResult);
    assert.deepEqual(result.videos[f.entry.slug].checked_dubs, {});
  });
});
