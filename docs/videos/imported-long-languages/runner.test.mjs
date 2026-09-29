import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { approve, sha256File } from "../../../tools/video/core/approvals.mjs";
import { loadProject, recordStage } from "../../../tools/video/core/state.mjs";
import { speechHash } from "../../../tools/video/core/timeline.mjs";
import { SLUGS, HardStop, VideoStop, assertProject, checkedDubReceipt, createSiteClient, cumulativeSnapshot, missingPhaseParts, resolveManifest, run, submitSnapshot, verifyLocal } from "./runner.mjs";

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
