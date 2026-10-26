import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { existsSync, mkdirSync, readFileSync, readdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT } from "../cli.mjs";
import { approve } from "../core/approvals.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { stopRequested } from "../core/paths.mjs";
import { acquireProjectLease } from "../core/project-lease.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { dubArtifacts, lintProject, loadProject } from "../core/state.mjs";
import { estimateTimeline, speechHash } from "../core/timeline.mjs";
import { dubRequests, speechFingerprint, translationHash } from "../dubs/plan.mjs";
import { ITEM_IDS, qaReport } from "../qa/checks.mjs";
import { encodeWav, parseWav, requireNarrationFormat, toNarrationRate } from "../tts/wav.mjs";
import { checkAudio } from "../tts/check.mjs";
import { trimSilence } from "../tts/split.mjs";
import { openSpeechJournal } from "../tts/speech-journal.mjs";
import { assertNoServiceRetakeHold, executeServiceRetake, inspectServiceRetakeIntents, planServiceRetake } from "./service-retake.mjs";

const NOW = "2026-10-26T10:07:17.000Z";
// This fixture exercises real native QA/checking with seconds of audio; duration has its own suite.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";
const BEFORE_DUE = "2026-10-26T10:07:16.000Z";
const LINE = "cab285";
const LOCALE = "th";
const digest = (bytes) => createHash("sha256").update(bytes).digest("hex");
const json = (file) => JSON.parse(readFileSync(file, "utf8"));
const save = (file, value) => {
  mkdirSync(path.dirname(file), { recursive: true });
  writeFileSync(file, `${JSON.stringify(value, null, 2)}\n`);
};
const wav = (seed = 1) => encodeWav(Int16Array.from({ length: 4800 }, (_, i) => Math.round(3000 * Math.sin((i + seed) / (7 + seed)))));
const nativeRaw = (httpWav) => encodeWav(trimSilence(requireNarrationFormat(parseWav(toNarrationRate(httpWav)))));

/** All production-facing files live in an isolated native repository layout. */
async function serviceFixture(t) {
  const box = sandbox("fixture-service-retake");
  t.after(() => rmSync(box.base, { recursive: true, force: true }));
  const doc = fixture();
  doc.slug = box.slug;
  doc.voice = { provider: "gemini", name: "Sulafat", model: "gemini-3.8-flash-tts", style: "Relaxed Taiwan Mandarin." };
  doc.scenes[0].lines[0].id = LINE;
  save(path.join(box.dir, "video.json"), doc);
  const translation = {
    title: "ชื่อเรื่อง", description: "คำอธิบาย", tags: [], chapters: {}, source_hashes: {},
    lines: Object.fromEntries([...eachLine(doc)].map(({ line }, i) => [line.id, { text: `ประโยคทดสอบที่ ${i + 1}`, source_hash: textHash(line.text) }])),
  };
  save(path.join(box.dir, "i18n", "th.json"), translation);
  const project = loadProject({ slug: box.slug, root: box.root });
  const planned = dubRequests(project, LOCALE);
  assert.deepEqual(planned.missing, []);
  const timeline = { ...estimateTimeline(project.doc), speech_hash: speechHash(project.doc, project.lexicon) };
  save(path.join(box.workdir, "timeline.json"), timeline);
  const files = dubArtifacts(box.workdir, LOCALE);
  const cache = { lines: {}, stretched: {} };
  for (const request of planned.requests) for (const line of request.lines) {
    const file = path.join(files.audio, `${line.id}.wav`);
    mkdirSync(path.dirname(file), { recursive: true });
    writeFileSync(file, wav(Object.keys(cache.lines).length + 1));
    cache.lines[line.id] = line.key;
  }
  save(files.cache, cache);
  const provenance = {
    locale: LOCALE, speech_hash: timeline.speech_hash,
    translation_hash: translationHash(planned.script), speech_fingerprint: speechFingerprint(planned.requests), style_override: null,
  };
  save(files.fit, { ...provenance, over: [], kept: [], windows: [] });
  save(files.timeline, { ...timeline, ...provenance, file: "th.m4a", windows: [] });
  writeFileSync(files.track("m4a"), "previous Thai track");
  writeFileSync(path.join(box.workdir, "final.mp4"), "approved primary final bytes");
  const finalSha = digest(readFileSync(path.join(box.workdir, "final.mp4")));
  await approve({ gate: "final", docDir: box.dir, workdir: box.workdir, now: new Date("2026-10-25T00:00:00Z") });
  const qa = qaReport(ITEM_IDS.map((id) => ({ id, ok: true, detail: "fixture evidence" })), finalSha);
  save(path.join(box.workdir, "review", "qa.json"), qa);
  save(path.join(box.workdir, "checks.json"), { ok: true, speech_hash: timeline.speech_hash, problems: [] });
  const choices = { th: { metadata: true, captions: true, dub: true }, en: { metadata: true, captions: true, dub: true } };
  save(path.join(box.workdir, "languages.json"), { locales: choices, decided_at: "2026-10-25T00:00:00Z" });
  const auto = {
    slug: box.slug, status: "done", languages: { th: { shorten: 1, retakes: 1, reword: 0, check_stopped: true } },
    deferred_until: NOW, defer_count: 6, deferred_reason: "Gemini returned no transcript: OTHER", notes: [],
  };
  save(path.join(box.workdir, "auto.json"), auto);
  const flags = path.join(box.workdir, "review", "check-flags.th.json");
  save(flags, { slug: box.slug, ...provenance, flags: [], notes: {} });
  save(path.join(box.workdir, "review", "check.th.json"), { lines: {} });
  const enJournal = path.join(box.workdir, "audio", "speech-journal", `${"e".repeat(64)}.json`);
  save(enJournal, { schema_version: 1, path: "speech/transcribe", request_sha256: "e".repeat(64), status: "sent", sent_at: "2026-10-25T20:00:00Z", request: { audio_sha256: "a".repeat(64), audio_bytes: 100, language: "en" }, generation: "retained-en-generation", producer_pid: 2147483647 });
  const protectedFiles = [
    path.join(box.workdir, "final.mp4"), path.join(box.workdir, "timeline.json"), path.join(box.workdir, "approvals.json"),
    path.join(box.workdir, "checks.json"), path.join(box.workdir, "languages.json"),
    path.join(box.workdir, "review", "qa.json"), flags, enJournal, path.join(box.workdir, "review", "check.th.json"),
  ];
  const protectedHashes = Object.fromEntries(protectedFiles.map((file) => [file, digest(readFileSync(file))]));
  const remote = {
    slug: box.slug, format: "slides", dub_allowed: true, locales: choices, locales_decided_at: "2026-10-25T00:00:00Z",
    languages: { th: { dub: { state: "working" } }, en: { dub: { state: "working" } } },
    reviews: [{ id: "fixture-primary-final", subject: null, gate: "final", status: "approved", content_sha256: finalSha, created_at: "2026-10-25T00:00:00Z", payload: { qa } }],
  };
  const output = [];
  const sink = { write: (value) => output.push(String(value)) };
  const ctx = { root: box.root, home: box.base, env: { VIDEO_WORKDIR: box.work }, stdout: sink, stderr: sink, now: () => new Date(NOW) };
  const clip = path.join(files.audio, `${LINE}.wav`);
  ctx.site = "https://site.test";
  const preflightFile = path.join(box.base, "retained", "source-preflight.json");
  save(preflightFile, { all_preflight_checks_passed: true, media_source_sha256: digest(readFileSync(path.join(box.dir, "video.json"))), remote: { final: { status: "approved", id: "fixture-primary-final", sha256: finalSha } } });
  const failureFile = path.join(box.base, "retained", "known-service-failure.json");
  const failure = {
    slug: box.slug, one_native_invocation_only: true,
    native_quality_result: "unfinished_due_explicit_known_service_refusal_not_quality_ready",
    before_defer_count: 5, after_defer_count: 6, next_native_due_utc: NOW,
    preflight_file: preflightFile, preflight_sha256: digest(readFileSync(preflightFile)),
    TH_source_sha256: digest(readFileSync(path.join(box.dir, "i18n", "th.json"))),
    [`${LINE}_wav_sha256`]: digest(readFileSync(clip)),
    native_log_exact: `${LINE}: Gemini returned no transcript: OTHER; Gemini 暫時無法轉寫`,
    no_new_unknown_speech_journal: true,
    protected_evidence: Object.fromEntries(Object.entries(protectedHashes).map(([file, sha]) => [path.relative(box.workdir, file), { before_sha256: sha, after_sha256: sha, unchanged: true }])),
    unresolved_speech_journals: [{ path: enJournal, status: "sent", sha256: digest(readFileSync(enJournal)) }],
  };
  save(failureFile, failure);
  const failureReceipt = { file: failureFile, sha256: digest(readFileSync(failureFile)) };
  return { ...box, doc, project, planned, timeline, files, remote, ctx, auto, clip, flags, enJournal, protectedHashes, output, finalSha, provenance, failureReceipt, failureFile, failure };
}

function assertProtected(f) {
  for (const [file, sha] of Object.entries(f.protectedHashes)) {
    assert.ok(existsSync(file), `retained evidence must remain: ${file}`);
    assert.equal(digest(readFileSync(file)), sha, `unrelated evidence changed: ${file}`);
  }
}

const planFor = (f, extra = {}) => planServiceRetake({ ctx: f.ctx, slug: f.slug, locale: LOCALE, lineId: LINE, failureReceipt: f.failureReceipt, ...extra });
function rewriteReceipt(f, edit) {
  edit(f.failure);
  save(f.failureFile, f.failure);
  f.failureReceipt.sha256 = digest(readFileSync(f.failureFile));
}
function refreshProtectedReceipt(f, file) {
  const sha = digest(readFileSync(file));
  f.protectedHashes[file] = sha;
  rewriteReceipt(f, (receipt) => {
    receipt.protected_evidence[path.relative(f.workdir, file)] = { before_sha256: sha, after_sha256: sha, unchanged: true };
  });
}
function execution(f, plan, { sameWav = false, nativeCode = 0, beforeNative, afterPost, fetchResponse, providerWav, remote = f.remote } = {}) {
  const posts = [], commands = [], remotes = [];
  const responseWav = providerWav ?? (sameWav ? readFileSync(f.clip) : wav(21));
  return {
    posts, commands, remotes,
    dependencies: {
      plan, ctx: f.ctx,
      getRemote: async () => { remotes.push(true); return remote; },
      fetch: async (url, init) => {
        posts.push({ url: String(url), init });
        return fetchResponse?.(url, init) ?? new Response(responseWav, { status: 200, headers: { "content-type": "audio/wav", "x-billable-characters": "19" } });
      },
      runNative: async (args, context) => {
        commands.push(args);
        await beforeNative?.(args, context);
        const response = await context.fetch(`${plan.site}/api/video/speech`, { method: "POST", body: JSON.stringify(plan.request_body) });
        const audio = Buffer.from(await response.arrayBuffer());
        await afterPost?.(args, context);
        if (response.ok) {
          writeFileSync(f.clip, nativeRaw(audio));
          const cache = json(f.files.cache);
          cache.lines[LINE] = plan.pins.all_clips.find((row) => row.id === LINE).line_key;
          delete cache.stretched[LINE];
          save(f.files.cache, cache);
        }
        return { code: nativeCode, out: `fixture native dub ${nativeCode}` };
      },
    },
  };
}

function assertOriginalRounds(f, retakes) {
  const state = json(path.join(f.workdir, "auto.json"));
  assert.deepEqual(state.languages.th, { shorten: 1, retakes, reword: 0, check_stopped: true });
  assert.equal(state.defer_count, 6);
  assert.equal(state.deferred_until, NOW);
}

test("settled-service fixture uses native source and clip identities, with nine protected artifacts", async (t) => {
  const f = await serviceFixture(t);
  assert.equal(f.planned.requests.flatMap(({ lines }) => lines).length, 7);
  assert.equal(Object.keys(f.protectedHashes).length, 9);
  assert.equal(json(f.flags).flags.length, 0, "service failures are not fake Jev flags");
  assertProtected(f);
});

test("planning is read-only and pins every native clip without fabricating audio flags", async (t) => {
  const f = await serviceFixture(t);
  const beforeState = readFileSync(path.join(f.workdir, "auto.json"));
  const plan = await planFor(f);
  assert.equal(plan.earliest_execution_reached, true);
  assert.equal(plan.voice_ready, false);
  assert.equal(plan.pins.all_clips.length, 7);
  assert.equal(plan.target_wav_sha256, digest(readFileSync(f.clip)));
  const target = f.planned.requests.find(({ lines }) => lines.some(({ id }) => id === LINE));
  const line = target.lines.find(({ id }) => id === LINE);
  assert.deepEqual(plan.request_body, { ...target.body, segments: [{ parts: line.parts, break_after_ms: 0 }] });
  assert.equal(existsSync(path.join(f.workdir, "service-retakes")), false);
  assert.deepEqual(readFileSync(path.join(f.workdir, "auto.json")), beforeState);
  assertProtected(f);
});

test("a fresh plan cannot bind an edited visual source to the old primary approval", async (t) => {
  const f = await serviceFixture(t), file = path.join(f.dir, "video.json"), doc = json(file);
  doc.thumbnail.data.headline = "Different picture";
  save(file, doc);
  await assert.rejects(planFor(f), /source.*historical approved-primary/);
  assertOriginalRounds(f, 1);
  assertProtected(f);
});

test("a future native backoff may be inspected but cannot dispatch or reserve", async (t) => {
  const f = await serviceFixture(t);
  f.ctx.now = () => new Date(BEFORE_DUE);
  const plan = await planFor(f);
  assert.equal(plan.earliest_execution_reached, false);
  const e = execution(f, plan);
  await assert.rejects(executeServiceRetake(e.dependencies), /backoff.*until/i);
  assert.equal(e.posts.length, 0);
  assert.equal(e.commands.length, 0);
  assert.equal(inspectServiceRetakeIntents(f.workdir).length, 0);
  assertOriginalRounds(f, 1);
  assertProtected(f);
});

test("local preflight refuses changed source, stale/missing clips, false evidence, cap and unknown journals", async (t) => {
  const cases = [
    ["STOP", (f) => writeFileSync(path.join(f.workdir, "STOP"), "other producer stop"), /STOP/],
    ["source", (f) => { const doc = json(path.join(f.dir, "video.json")); doc.scenes[0].lines[0].text += "改變。"; save(path.join(f.dir, "video.json"), doc); }, /source.*stale|source binding/i],
    ["translation", (f) => { const file = path.join(f.dir, "i18n", "th.json"), value = json(file); value.lines[LINE].text += "ใหม่"; save(file, value); }, /current translation/],
    ["missing translated line", (f) => { const file = path.join(f.dir, "i18n", "th.json"), value = json(file); delete value.lines.m4qa; save(file, value); rewriteReceipt(f, (r) => { r.TH_source_sha256 = digest(readFileSync(file)); }); }, /incomplete/],
    ["missing clip", (f) => rmSync(f.clip), /Missing.*evidence/i],
    ["changed target bytes", (f) => writeFileSync(f.clip, wav(22)), /current target/],
    ["stale other clip", (f) => { const cache = json(f.files.cache); cache.lines.m4qa = "old-key"; save(f.files.cache, cache); }, /clip is stale.*m4qa/],
    ["old fit", (f) => { const fit = json(f.files.fit); fit.speech_fingerprint = "old"; save(f.files.fit, fit); }, /fit.*stale/],
    ["unresolved fit", (f) => { const fit = json(f.files.fit); fit.over = [{ id: LINE }]; save(f.files.fit, fit); }, /fit.*unresolved/],
    ["earlier take kept", (f) => { const fit = json(f.files.fit); fit.kept = [LINE]; save(f.files.fit, fit); }, /fit.*unresolved/],
    ["native skip", (f) => save(f.files.skipped, { reason: "actual skip" }), /skip/],
    ["retake cap", (f) => { const file = path.join(f.workdir, "auto.json"), state = json(file); state.languages.th.retakes = 2; save(file, state); }, /cap.*reset|first-retake boundary/],
    ["uncertain receipt", (f) => rewriteReceipt(f, (r) => { r.native_log_exact += " video_speech_uncertain"; }), /uncertain/],
    ["new unknown receipt", (f) => rewriteReceipt(f, (r) => { r.no_new_unknown_speech_journal = false; }), /settled sixth/],
    ["receipt changed", (f) => save(f.failureFile, { ...f.failure, ignored: "changed" }), /receipt bytes differ/],
    ["new unknown journal", (f) => save(path.join(f.workdir, "audio", "speech-journal", `${"f".repeat(64)}.json`), { schema_version: 1, request_sha256: "f".repeat(64), status: "sent" }), /journal.*inventory changed/],
  ];
  for (const [name, change, why] of cases) await t.test(name, async (t) => {
    const f = await serviceFixture(t);
    change(f);
    await assert.rejects(planFor(f), why);
    assert.equal(inspectServiceRetakeIntents(f.workdir).length, 0);
  });
});

test("the exact target TTS journal generation holds even if it was in the retained inventory", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f);
  const file = path.join(f.workdir, "audio", "speech-journal", `${plan.request_sha256}.json`);
  save(file, { schema_version: 1, path: "speech", request_sha256: plan.request_sha256, request: plan.request_body, status: "sent", sent_at: NOW });
  rewriteReceipt(f, (r) => { r.unresolved_speech_journals.push({ path: file, status: "sent", sha256: digest(readFileSync(file)) }); });
  await assert.rejects(planFor(f), /target TTS request.*retained\/unknown/);
  assert.equal(json(file).status, "sent");
  assertProtected(f);
});

test("one confirmed native synthesis consumes only the final retake and never marks voice ready", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
  const outcome = await executeServiceRetake(e.dependencies);
  assert.equal(outcome.status, "applied");
  assert.equal(outcome.voice_ready, false);
  assert.equal(outcome.asr_performed, false);
  assert.equal(outcome.check_stopped, true);
  assert.notEqual(outcome.target_before_sha256, outcome.target_after_sha256);
  assert.equal(e.posts.length, 1);
  assert.equal(e.remotes.length, 2, "the actual primary final is checked on both sides of synthesis");
  assert.equal(e.posts[0].init.redirect, "error");
  assert.deepEqual(e.commands[0], ["dub", "--slug", f.slug, "--locale", "th", "--redo", outcome.command[6], "--line-by-line"]);
  assert.deepEqual(json(outcome.command[6]), [LINE], "this is an explicit retake request, not fabricated check flags");
  assertOriginalRounds(f, 2);
  assert.equal(stopRequested(f.workdir), false);
  assertProtected(f);
  const repeated = await executeServiceRetake(e.dependencies);
  assert.equal(repeated.status, "already_applied");
  assert.equal(repeated.dispatched, false);
  assert.equal(repeated.voice_ready, false);
  assert.equal(e.posts.length, 1, "a second invocation cannot buy another same-body take");
});

test("a real confirmed response with identical WAV bytes still consumes the one paid opportunity", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan, { sameWav: true });
  const outcome = await executeServiceRetake(e.dependencies);
  assert.equal(outcome.status, "applied");
  assert.equal(outcome.same_wav_bytes, true);
  assert.equal(outcome.voice_ready, false);
  assert.equal(e.posts.length, 1);
  assertOriginalRounds(f, 2);
  await executeServiceRetake(e.dependencies);
  assert.equal(e.posts.length, 1);
  assertProtected(f);
});

test("a foreign lease and a changed actual primary final refuse without dispatch", async (t) => {
  for (const reason of ["lease", "remote missing", "remote stale", "remote secondary", "source changed after plan"]) await t.test(reason, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f);
    let remote = structuredClone(f.remote);
    if (reason === "lease") save(path.join(f.workdir, "LEASE"), { schema_version: 1, token: "foreign", pid: 2147483647, host: "another-host", owner: "another-producer", acquired_at: NOW });
    if (reason === "remote missing") remote.reviews = [];
    if (reason === "remote stale") remote.reviews[0].content_sha256 = "f".repeat(64);
    if (reason === "remote secondary") remote.reviews[0].subject = "translated-cut";
    if (reason === "source changed after plan") { const file = path.join(f.dir, "video.json"), doc = json(file); doc.youtube.title += "改版"; save(file, doc); }
    const e = execution(f, plan, { remote });
    await assert.rejects(executeServiceRetake(e.dependencies), /held by|remote final|reviewed plan is stale|source.*historical approved-primary/i);
    assert.equal(e.posts.length, 0);
    assert.equal(e.commands.length, 0);
    assertOriginalRounds(f, 1);
  });
});

test("every persisted-intent crash boundary holds forever without refund or replay", async (t) => {
  for (const label of ["after_intent", "after_reservation", "after_dispatch_marker", "after_native_return", "before_applied"]) await t.test(label, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
    e.dependencies.checkpoint = async (at) => { if (at === label) throw new Error(`injected crash at ${label}`); };
    await assert.rejects(executeServiceRetake(e.dependencies), new RegExp(`injected crash at ${label}`));
    const row = inspectServiceRetakeIntents(f.workdir)[0];
    assert.equal(row.phase, "held");
    assert.equal(stopRequested(f.workdir), true, "the original native STOP guard really prevents work");
    assert.equal(e.posts.length, ["after_native_return", "before_applied"].includes(label) ? 1 : 0);
    assertOriginalRounds(f, label === "after_intent" ? 1 : 2);
    const posted = e.posts.length;
    await assert.rejects(executeServiceRetake(e.dependencies), /no replay|unresolved|STOP/);
    assert.equal(e.posts.length, posted);
    assertProtected(f);
  });
});

test("producer hold guard creates an owned STOP after a hard crash and preserves another producer's STOP", async (t) => {
  for (const foreignStop of [false, true]) await t.test(foreignStop ? "foreign STOP" : "missing STOP", async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f);
    const dir = path.join(f.workdir, "service-retakes", plan.intent_id);
    save(path.join(dir, "intent.json"), { schema_version: 1, intent_id: plan.intent_id, phase: "reserved", plan });
    const stop = path.join(f.workdir, "STOP"), foreign = "do not erase another producer's exact STOP bytes\n";
    if (foreignStop) writeFileSync(stop, foreign);
    const lease = acquireProjectLease(f.workdir, { owner: "original-helper-test", now: f.ctx.now });
    try {
      assert.throws(() => assertNoServiceRetakeHold(f.workdir, { lease, now: f.ctx.now }), /no replay|producer/);
      assert.equal(stopRequested(f.workdir), true);
      assert.ok(existsSync(path.join(dir, "stop-owner.json")));
      if (foreignStop) assert.equal(readFileSync(stop, "utf8"), foreign);
      else {
        const proof = json(path.join(dir, "stop-owner.json"));
        assert.equal(digest(readFileSync(stop)), proof.stop_sha256);
      }
    } finally { lease.release(); }
    assertProtected(f);
  });
});

test("eleven successful rows must represent all eleven actual primary QA items", async (t) => {
  const f = await serviceFixture(t), file = path.join(f.workdir, "review", "qa.json"), qa = json(file);
  qa.items[10] = { ...qa.items[0] };
  save(file, qa);
  refreshProtectedReceipt(f, file);
  await assert.rejects(planFor(f), /eleven.*QA|QA item/);
});

test("guarded native transport rejects route, body, origin and a second paid POST", async (t) => {
  for (const kind of ["other origin", "query", "transcribe", "body drift", "second synthesis"]) await t.test(kind, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
    e.dependencies.runNative = async (_args, context) => {
      let url = `${plan.site}/api/video/speech`, body = JSON.stringify(plan.request_body);
      if (kind === "other origin") url = "https://other.test/api/video/speech";
      if (kind === "query") url += "?bypass=1";
      if (kind === "transcribe") url += "/transcribe";
      if (kind === "body drift") body = JSON.stringify({ ...plan.request_body, style: "another performance" });
      await context.fetch(url, { method: "POST", body });
      if (kind === "second synthesis") await context.fetch(url, { method: "POST", body });
      return { code: 0 };
    };
    await assert.rejects(executeServiceRetake(e.dependencies), /origin|exact one.line|no second POST/i);
    assert.equal(e.posts.length, kind === "second synthesis" ? 1 : 0);
    assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "held");
    assertOriginalRounds(f, 2);
    assert.equal(stopRequested(f.workdir), true);
    assertProtected(f);
  });
});

test("settled native failure, lost response, no POST and unrelated raw writes all preserve a held opportunity", async (t) => {
  for (const kind of ["settled refusal", "lost response", "no POST", "other clip write", "new unknown journal"]) await t.test(kind, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f);
    const e = execution(f, plan, {
      nativeCode: kind === "settled refusal" ? 4 : 0,
      fetchResponse: kind === "settled refusal" ? () => Response.json({ code: "video_speech_upstream_failed", detail: "settled service failure" }, { status: 502 }) : undefined,
    });
    if (kind === "lost response") e.dependencies.fetch = async (url, init) => { e.posts.push({ url, init }); throw new Error("lost provider response"); };
    if (kind === "no POST") e.dependencies.runNative = async () => ({ code: 0 });
    if (kind === "other clip write") {
      const native = e.dependencies.runNative;
      e.dependencies.runNative = async (...args) => { const result = await native(...args); writeFileSync(path.join(f.files.audio, "m4qa.wav"), wav(31)); return result; };
    }
    if (kind === "new unknown journal") {
      const native = e.dependencies.runNative;
      e.dependencies.runNative = async (...args) => { const result = await native(...args); save(path.join(f.workdir, "audio", "speech-journal", `${"d".repeat(64)}.json`), { status: "sent" }); return result; };
    }
    await assert.rejects(executeServiceRetake(e.dependencies), /no single confirmed|lost provider|Pinned evidence changed|speech journals changed/i);
    assertOriginalRounds(f, 2);
    assert.equal(stopRequested(f.workdir), true);
    assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "held");
    assertProtected(f);
    const posted = e.posts.length;
    await assert.rejects(executeServiceRetake(e.dependencies), /no replay|STOP|unresolved/);
    assert.equal(e.posts.length, posted);
  });
});

test("a genuine native ASR service refusal after the new take remains unfinished without fake transcript or Jev readiness", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
  assert.deepEqual(lintProject(f.project).errors, []);
  await executeServiceRetake(e.dependencies);
  const calls = [];
  const code = await checkAudio(["--slug", f.slug, "--locale", "th"], { ...f.ctx, EXIT }, {
    site: f.ctx.site, token: "fixture-only-token", attempts: 1, sleep: async () => {},
    fetchImpl: async (url, init) => {
      calls.push({ url, init });
      assert.equal(url, `${f.ctx.site}/api/video/speech/transcribe`, "no Jev or ready endpoint may be reached without a transcript");
      return Response.json({ code: "video_speech_upstream_failed", detail: "Gemini returned no transcript: OTHER" }, { status: 502 });
    },
  });
  assert.equal(code, EXIT.external);
  assert.equal(calls.length, 3, "the native check stops at its actual consecutive-failure bound");
  assert.equal(json(path.join(f.workdir, "review", "check.th.json")).lines[LINE], undefined);
  assert.deepEqual(json(f.flags).flags, []);
  assertOriginalRounds(f, 2);
  assert.equal(inspectServiceRetakeIntents(f.workdir)[0].intent.outcome.voice_ready, false);
  assert.equal(digest(readFileSync(f.enJournal)), f.protectedHashes[f.enJournal]);
});

test("a successful new response cannot be applied while the old raw take remains installed", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan), before = readFileSync(f.clip);
  e.dependencies.runNative = async (_args, context) => {
    const response = await context.fetch(`${plan.site}/api/video/speech`, { method: "POST", body: JSON.stringify(plan.request_body) });
    assert.equal(response.status, 200);
    await response.arrayBuffer();
    return { code: 0, out: "the native process returned without installing its response" };
  };
  await assert.rejects(executeServiceRetake(e.dependencies), /raw.*response|response.*raw|installed|take.*answer/i);
  assert.equal(e.posts.length, 1);
  assert.deepEqual(readFileSync(f.clip), before);
  assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "held");
  assert.equal(stopRequested(f.workdir), true);
  assertOriginalRounds(f, 2);
  await assert.rejects(executeServiceRetake(e.dependencies), /no replay|STOP|unresolved/);
  assert.equal(e.posts.length, 1);
  assertProtected(f);
});

test("the installed raw take matches actual 24 kHz response normalization and native silence trimming", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f);
  const samples24 = new Int16Array(2400 + 4800 + 2400);
  samples24.set(Int16Array.from({ length: 4800 }, (_, i) => Math.round(6000 * Math.sin(i / 9))), 2400);
  const providerWav = encodeWav(samples24, 24_000);
  const expected = nativeRaw(providerWav);
  assert.equal(parseWav(providerWav).sampleRate, 24_000);
  assert.equal(parseWav(expected).sampleRate, 48_000);
  assert.ok(parseWav(expected).samples.length < parseWav(toNarrationRate(providerWav)).samples.length, "the real leading and trailing silence is trimmed");
  const e = execution(f, plan, { providerWav });
  const result = await executeServiceRetake(e.dependencies);
  assert.equal(result.status, "applied");
  assert.equal(result.voice_ready, false);
  assert.equal(result.confirmed_response.response_sha256, digest(providerWav));
  assert.equal(result.target_after_sha256, digest(expected));
  assert.deepEqual(readFileSync(f.clip), expected);
  assert.equal(e.posts.length, 1);
  assertOriginalRounds(f, 2);
  assertProtected(f);
});

test("editing a plan's due_at cannot bypass the genuine native auto backoff", async (t) => {
  const f = await serviceFixture(t);
  f.ctx.now = () => new Date(BEFORE_DUE);
  const plan = await planFor(f);
  assert.equal(plan.earliest_execution_reached, false);
  plan.due_at = "2026-10-25T00:00:00.000Z";
  const e = execution(f, plan);
  await assert.rejects(executeServiceRetake(e.dependencies), /real backoff.*not due|reviewed plan.*stale|backoff.*until/i);
  assert.equal(e.posts.length, 0);
  assert.equal(e.commands.length, 0);
  assert.equal(inspectServiceRetakeIntents(f.workdir).length, 0);
  assertOriginalRounds(f, 1);
  assertProtected(f);
});

test("damaged or fabricated applied history remains fenced by permanent response and native-install proof", async (t) => {
  const cases = [
    ["missing response bytes", ({ dir }) => rmSync(path.join(dir, "http-answer.bin"))],
    ["missing response receipt", ({ dir }) => rmSync(path.join(dir, "http-answer.json"))],
    ["changed response bytes", ({ dir }) => writeFileSync(path.join(dir, "http-answer.bin"), wav(42))],
    ["non-success response status", ({ dir }) => { const file = path.join(dir, "http-answer.json"), receipt = json(file); receipt.response_status = 502; save(file, receipt); }],
    ["changed installed target proof", ({ intent }) => { intent.outcome.target_after_sha256 = "a".repeat(64); }],
    ["fabricated voice readiness", ({ intent }) => { intent.outcome.voice_ready = true; }],
    ["fabricated ASR", ({ intent }) => { intent.outcome.asr_performed = true; }],
    ["failed native exit", ({ intent }) => { intent.outcome.native_exit_code = 4; }],
    ["changed explicit target request", ({ dir }) => save(path.join(dir, "retake-request.json"), [LINE, "m4qa"])],
    ["expanded native command", ({ intent }) => { intent.outcome.command.push("--force"); }],
    ["invalid reserved state proof", ({ intent }) => { intent.state_reserved_sha256 = "not-a-hash"; }],
    ["applied label without outcome", ({ intent }) => { delete intent.outcome; }],
  ];
  for (const [name, tamper] of cases) await t.test(name, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
    const result = await executeServiceRetake(e.dependencies), dir = path.dirname(result.intent_file), intent = json(result.intent_file);
    assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "applied");
    tamper({ f, plan, dir, intent });
    save(result.intent_file, intent);
    assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "unverified-applied");
    assert.throws(() => assertNoServiceRetakeHold(f.workdir, { now: f.ctx.now }), /no replay|producer/);
    assert.equal(stopRequested(f.workdir), false, "a caller without the native lease cannot write STOP");
    assert.equal(existsSync(path.join(dir, "stop-owner.json")), false);
    const lease = acquireProjectLease(f.workdir, { owner: "native-producer-test", now: f.ctx.now });
    try { assert.throws(() => assertNoServiceRetakeHold(f.workdir, { lease, now: f.ctx.now }), /no replay|producer/); }
    finally { lease.release(); }
    assert.equal(stopRequested(f.workdir), true);
    assert.ok(existsSync(path.join(dir, "stop-owner.json")));
    await assert.rejects(executeServiceRetake(e.dependencies), /no replay|STOP|unresolved/);
    assert.equal(e.posts.length, 1, "damaged applied history must not reopen the paid operation");
    assertOriginalRounds(f, 2);
    assertProtected(f);
  });
});

test("historical applied proof stays valid after a later native reword changes the current raw take", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
  await executeServiceRetake(e.dependencies);
  writeFileSync(f.clip, wav(43));
  const cache = json(f.files.cache);
  cache.lines[LINE] = "a-later-native-wording-key";
  save(f.files.cache, cache);
  assert.notEqual(digest(readFileSync(f.clip)), inspectServiceRetakeIntents(f.workdir)[0].intent.outcome.target_after_sha256);
  assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "applied", "validation reads retained history rather than requiring old raw bytes to remain current");
  const lease = acquireProjectLease(f.workdir, { owner: "later-native-producer", now: f.ctx.now });
  try { assert.doesNotThrow(() => assertNoServiceRetakeHold(f.workdir, { lease, now: f.ctx.now })); }
  finally { lease.release(); }
  assert.equal(stopRequested(f.workdir), false);
  const again = await executeServiceRetake(e.dependencies);
  assert.equal(again.status, "already_applied");
  assert.equal(e.posts.length, 1);
  assertProtected(f);
});

test("hard-crash intent phases refuse without a lease and fence the next native producer under its lease", async (t) => {
  for (const phase of ["prepared", "reserved", "dispatched", "malformed-phase"]) await t.test(phase, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f), dir = path.join(f.workdir, "service-retakes", plan.intent_id);
    save(path.join(dir, "intent.json"), { schema_version: 1, intent_id: plan.intent_id, phase, plan });
    assert.throws(() => assertNoServiceRetakeHold(f.workdir, { now: f.ctx.now }), /no replay|producer/);
    assert.equal(stopRequested(f.workdir), false);
    assert.equal(existsSync(path.join(dir, "stop-owner.json")), false);
    const lease = acquireProjectLease(f.workdir, { owner: "original-native-helper", now: f.ctx.now });
    try { assert.throws(() => assertNoServiceRetakeHold(f.workdir, { lease, now: f.ctx.now }), /no replay|producer/); }
    finally { lease.release(); }
    assert.equal(stopRequested(f.workdir), true, "the same STOP predicate used by the original native producer is now set");
    assert.ok(existsSync(path.join(dir, "stop-owner.json")));
    assertProtected(f);
  });
});

test("source drift after the dispatch marker and immediately before native fetch cannot reach the paid transport", async (t) => {
  for (const moment of ["after_dispatch_marker", "before_fetch"]) await t.test(moment, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
    const changeSource = () => { const file = path.join(f.dir, "video.json"), doc = json(file); doc.youtube.title += " changed before HTTP dispatch"; save(file, doc); };
    if (moment === "after_dispatch_marker") e.dependencies.checkpoint = async (label) => { if (label === moment) changeSource(); };
    else {
      const runner = e.dependencies.runNative;
      e.dependencies.runNative = async (...args) => { changeSource(); return runner(...args); };
    }
    await assert.rejects(executeServiceRetake(e.dependencies), /Pinned evidence changed|source.*changed/i);
    assert.equal(e.posts.length, 0);
    const row = inspectServiceRetakeIntents(f.workdir)[0];
    assert.equal(row.phase, "held");
    assert.equal(existsSync(path.join(path.dirname(row.file), "HTTP-SENT.json")), false);
    assertOriginalRounds(f, 2);
    assert.equal(stopRequested(f.workdir), true);
    assertProtected(f);
  });
});

test("the real native speech-journal sent→fetch→confirmed→release path is allowed for this exact producer and request", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
  const journalDir = path.join(f.workdir, "audio", "speech-journal"), targetEntry = path.join(journalDir, `${plan.request_sha256}.json`);
  const transitions = [];
  e.dependencies.runNative = async (_args, context) => {
    const journal = openSpeechJournal(journalDir, { now: f.ctx.now });
    const send = journal.wrap(async (body) => {
      const entry = json(targetEntry);
      transitions.push(entry.status);
      assert.equal(entry.status, "sent");
      assert.equal(entry.producer_pid, process.pid);
      assert.equal(entry.path, "speech");
      assert.deepEqual(entry.request, plan.request_body);
      const response = await context.fetch(`${plan.site}/api/video/speech`, { method: "POST", body: JSON.stringify(body) });
      return { wav: toNarrationRate(Buffer.from(await response.arrayBuffer())), billable: 19 };
    });
    const result = await send(plan.request_body);
    transitions.push(json(targetEntry).status);
    writeFileSync(f.clip, nativeRaw(result.wav));
    const cache = json(f.files.cache);
    cache.lines[LINE] = plan.pins.all_clips.find(({ id }) => id === LINE).line_key;
    delete cache.stretched[LINE];
    save(f.files.cache, cache);
    journal.release();
    assert.equal(existsSync(targetEntry), false);
    transitions.push("released");
    return { code: 0, out: "native journal path completed" };
  };
  const result = await executeServiceRetake(e.dependencies);
  assert.equal(result.status, "applied");
  assert.deepEqual(transitions, ["sent", "confirmed", "released"]);
  assert.equal(e.posts.length, 1);
  assertOriginalRounds(f, 2);
  assertProtected(f);
});

test("another PID or a different body cannot masquerade as the native producer's fresh sent journal", async (t) => {
  for (const corruption of ["another PID", "different request"]) await t.test(corruption, async (t) => {
    const f = await serviceFixture(t), plan = await planFor(f), e = execution(f, plan);
    const targetEntry = path.join(f.workdir, "audio", "speech-journal", `${plan.request_sha256}.json`);
    e.dependencies.runNative = async (_args, context) => {
      save(targetEntry, {
        schema_version: 1, path: "speech", status: "sent", request_sha256: plan.request_sha256,
        sent_at: NOW, generation: "11111111-1111-4111-8111-111111111111",
        producer_pid: corruption === "another PID" ? 2147483647 : process.pid,
        request: corruption === "different request" ? { ...plan.request_body, style: "different generation" } : plan.request_body,
      });
      await context.fetch(`${plan.site}/api/video/speech`, { method: "POST", body: JSON.stringify(plan.request_body) });
      return { code: 0 };
    };
    await assert.rejects(executeServiceRetake(e.dependencies), /journal|producer|generation/i);
    assert.equal(e.posts.length, 0);
    assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "held");
    assert.equal(json(targetEntry).status, "sent", "an unproven generation is retained, never forgotten");
    assertOriginalRounds(f, 2);
    assert.equal(stopRequested(f.workdir), true);
    assertProtected(f);
  });
});

// These subprocesses exercise the scoped wrappers' acquire → guard → await →
// action → release order with the real native filesystem lease. No fake PID,
// lease-IO override, provider, server or global network transport is involved.
const leaseRaceChildSource = `
import fs from 'node:fs';
import path from 'node:path';
import { once } from 'node:events';
import { acquireProjectLease } from ${JSON.stringify(new URL("../core/project-lease.mjs", import.meta.url).href)};
import { assertNoServiceRetakeHold, executeServiceRetake } from ${JSON.stringify(new URL("./service-retake.mjs", import.meta.url).href)};
import { openSpeechJournal } from ${JSON.stringify(new URL("../tts/speech-journal.mjs", import.meta.url).href)};
import { encodeWav, parseWav, requireNarrationFormat, toNarrationRate } from ${JSON.stringify(new URL("../tts/wav.mjs", import.meta.url).href)};
import { trimSilence } from ${JSON.stringify(new URL("../tts/split.mjs", import.meta.url).href)};
const c = JSON.parse(process.argv[1]);
const tell = (type, fields = {}) => process.send({ type, ...fields });
const resume = async () => { const [message] = await once(process, 'message'); if (message !== 'continue') throw Error('Unexpected race-fixture command'); };
const json = file => JSON.parse(fs.readFileSync(file, 'utf8'));
const record = name => fs.appendFileSync(c.calls, name + '\\n');
// Any accidental real network call fails the fixture instead of using session credentials.
globalThis.fetch = async () => { record('FORBIDDEN-NETWORK'); throw Error('Network is disabled in the lease-race fixture'); };
const now = () => new Date(c.now);
try {
  if (c.mode === 'retake') {
    const plan = json(c.planFile);
    const context = { root: c.root, home: c.home, env: { VIDEO_WORKDIR: c.work }, now, site: 'https://site.test' };
    const result = await executeServiceRetake({
      plan, ctx: context, getRemote: async () => c.remote,
      fetch: async () => { record('retake'); return new Response(fs.readFileSync(c.providerWav), { status: 200, headers: { 'content-type': 'audio/wav' } }); },
      runNative: async (_args, ctx) => {
        const journal = openSpeechJournal(path.join(c.workdir, 'audio', 'speech-journal'), { now });
        const send = journal.wrap(async body => {
          const response = await ctx.fetch(plan.site + '/api/video/speech', { method: 'POST', body: JSON.stringify(body) });
          return { wav: toNarrationRate(Buffer.from(await response.arrayBuffer())), billable: 19 };
        });
        const answer = await send(plan.request_body);
        fs.writeFileSync(c.clip, encodeWav(trimSilence(requireNarrationFormat(parseWav(answer.wav)))));
        const cache = json(c.cache);
        cache.lines[plan.lineId] = plan.pins.all_clips.find(row => row.id === plan.lineId).line_key;
        delete cache.stretched[plan.lineId];
        fs.writeFileSync(c.cache, JSON.stringify(cache, null, 2) + '\\n');
        journal.release();
        return { code: 0 };
      },
      checkpoint: async label => {
        if (c.pauseAfterRelease && label === 'after_native_return') { tell('journal-released-before-applied'); await resume(); }
      },
    });
    tell('result', { status: result.status });
  } else {
    if (c.mode === 'early-helper') {
      // Model the old unsafe precheck and its await; the required second check is
      // below, under the real lease, after a concurrent retake's hard crash.
      assertNoServiceRetakeHold(c.workdir, { now });
      tell('early-precheck-passed');
      await resume();
    }
    const lease = acquireProjectLease(c.workdir, { owner: 'scoped-helper-race-fixture', now });
    try {
      lease.verify();
      assertNoServiceRetakeHold(c.workdir, { lease, now });
      tell('guard-passed-under-lease');
      if (c.mode === 'holding-helper') await resume();
      lease.verify();
      record('ordinary-helper');
      tell('result', { status: 'ordinary-action-completed' });
    } finally { lease.release(); }
  }
} catch (error) { tell('result', { status: 'refused', error: error.message, code: error.code }); }
finally { process.disconnect(); }
`;

function leaseRaceProcess(t, config) {
  const child = spawn(process.execPath, ["--input-type=module", "-e", leaseRaceChildSource, JSON.stringify(config)], {
    stdio: ["ignore", "pipe", "pipe", "ipc"],
    env: { PATH: process.env.PATH, VIDEO_MIN_EPISODE_MINUTES: "0" },
  });
  const messages = [], waiting = [];
  let output = "", ended = null;
  child.stdout.on("data", value => { output += value; });
  child.stderr.on("data", value => { output += value; });
  child.on("message", message => {
    const index = waiting.findIndex(row => row.type === message.type);
    if (index === -1) messages.push(message);
    else { const [row] = waiting.splice(index, 1); clearTimeout(row.timer); row.resolve(message); }
  });
  const exit = new Promise(resolve => child.once("exit", (code, signal) => {
    ended = { code, signal };
    for (const row of waiting.splice(0)) { clearTimeout(row.timer); row.reject(Error(`Lease-race subprocess exited before ${row.type}: ${code}/${signal}; ${output}`)); }
    resolve(ended);
  }));
  t.after(async () => { if (!ended) child.kill("SIGKILL"); await exit; });
  return {
    child, exit,
    resume: () => child.send("continue"),
    wait(type) {
      const index = messages.findIndex(row => row.type === type);
      if (index !== -1) return Promise.resolve(messages.splice(index, 1)[0]);
      if (ended) return Promise.reject(Error(`Lease-race subprocess already exited: ${JSON.stringify(ended)}; ${output}`));
      return new Promise((resolve, reject) => {
        const row = { type, resolve, reject };
        row.timer = setTimeout(() => { waiting.splice(waiting.indexOf(row), 1); child.kill("SIGKILL"); reject(Error(`Timed out waiting for lease-race ${type}: ${output}`)); }, 10000);
        waiting.push(row);
      });
    },
  };
}

function leaseRaceConfig(f, plan) {
  const planFile = path.join(f.base, "race-plan.json"), providerWav = path.join(f.base, "fake-provider.wav"), calls = path.join(f.base, "fake-paid-calls.txt");
  save(planFile, plan);
  writeFileSync(providerWav, wav(71));
  writeFileSync(calls, "");
  return { planFile, providerWav, calls, workdir: f.workdir, root: f.root, home: f.base, work: f.work, clip: f.clip, cache: f.files.cache, now: NOW, remote: f.remote };
}

test("a scoped helper rechecks under the real filesystem lease after a competing retake SIGKILLs between journal release and applied proof", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), config = leaseRaceConfig(f, plan);
  const helper = leaseRaceProcess(t, { ...config, mode: "early-helper" });
  await helper.wait("early-precheck-passed");
  const producer = leaseRaceProcess(t, { ...config, mode: "retake", pauseAfterRelease: true });
  await producer.wait("journal-released-before-applied");
  const dir = path.join(f.workdir, "service-retakes", plan.intent_id), journal = path.join(f.workdir, "audio", "speech-journal", `${plan.request_sha256}.json`);
  assert.equal(existsSync(journal), false, "native completion has genuinely released the synthesis journal");
  assert.equal(existsSync(path.join(dir, "HTTP-SENT.json")), true);
  assert.equal(inspectServiceRetakeIntents(f.workdir)[0].phase, "dispatched");
  assert.equal(stopRequested(f.workdir), false, "SIGKILL must test the permanent-intent fence without a catch-created STOP");
  const deadToken = json(path.join(f.workdir, "LEASE")).token;
  producer.child.kill("SIGKILL");
  assert.deepEqual(await producer.exit, { code: null, signal: "SIGKILL" });
  helper.resume();
  const result = await helper.wait("result");
  assert.equal(result.status, "refused");
  assert.match(result.error, /no replay|producer/);
  assert.deepEqual(await helper.exit, { code: 0, signal: null });
  assert.ok(readdirSync(f.workdir).includes(`LEASE.${deadToken}.dead.json`), "the real native lease archived its certainly dead holder");
  assert.equal(stopRequested(f.workdir), true);
  assert.equal(json(path.join(dir, "stop-owner.json")).intent_id, plan.intent_id);
  assert.deepEqual(readFileSync(config.calls, "utf8").trim().split("\n"), ["retake"], "the delayed helper performs zero paid actions after the crash");
  assertOriginalRounds(f, 2);
  assertProtected(f);
});

test("a scoped helper retains its real filesystem lease across awaited work so a competing retake cannot dispatch after its guard", async (t) => {
  const f = await serviceFixture(t), plan = await planFor(f), config = leaseRaceConfig(f, plan);
  const helper = leaseRaceProcess(t, { ...config, mode: "holding-helper" });
  await helper.wait("guard-passed-under-lease");
  const heldToken = json(path.join(f.workdir, "LEASE")).token;
  const producer = leaseRaceProcess(t, { ...config, mode: "retake" });
  const result = await producer.wait("result");
  assert.equal(result.status, "refused");
  assert.match(result.error, /held by/);
  assert.equal(result.code, "video_project_leased");
  assert.deepEqual(await producer.exit, { code: 0, signal: null });
  assert.equal(json(path.join(f.workdir, "LEASE")).token, heldToken);
  assert.deepEqual(inspectServiceRetakeIntents(f.workdir), [], "a blocked competitor cannot create a reservation or dispatch marker");
  assert.equal(readFileSync(config.calls, "utf8"), "", "neither process reaches paid work while the helper awaits");
  helper.resume();
  assert.equal((await helper.wait("result")).status, "ordinary-action-completed");
  assert.deepEqual(await helper.exit, { code: 0, signal: null });
  assert.equal(existsSync(path.join(f.workdir, "LEASE")), false);
  assert.equal(readFileSync(config.calls, "utf8"), "ordinary-helper\n");
  assertOriginalRounds(f, 1);
  assertProtected(f);
});
