import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { createServer } from "node:http";
import { existsSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import os from "node:os";
import path from "node:path";
import { approve, sha256File } from "../../../tools/video/core/approvals.mjs";
import { loadProject, recordStage } from "../../../tools/video/core/state.mjs";
import { speechHash } from "../../../tools/video/core/timeline.mjs";
import { main as videoMain } from "../../../tools/video/cli.mjs";
import { Automation } from "../../../tools/video/automation/flow.mjs";
import { SLUGS, DIRECT_STAGE_TIMEOUT_MS, HardStop, VideoStop, assertProject, checkedDubReceipt, createSiteClient, cumulativeSnapshot, directStageOrigin, missingPhaseParts, nativeStageRequest, resolveManifest, run, submitSnapshot, translateLocaleResuming, validateResumeSheet, verifyLocal } from "./runner.mjs";

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
  assert.deepEqual(JSON.parse(readFileSync(f.file, "utf8")), f.translated, "successful translation remains available after a failed review");
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
