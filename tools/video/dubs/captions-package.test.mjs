import assert from "node:assert/strict";
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { EXIT, main } from "../cli.mjs";
import { GATES, readApprovals } from "../core/approvals.mjs";
import { parseSrt } from "../core/captions.mjs";
import { fixture, sandbox } from "../core/fixtures/load.mjs";
import { eachLine, textHash } from "../core/schema.mjs";
import { captionTimelineOf, currentDub, dubRole, dubsForUpload, runCaptions } from "../core/stages.mjs";
import { dubArtifacts, loadProject } from "../core/state.mjs";
import { estimateTimeline, frameToMs, speechHash } from "../core/timeline.mjs";
import { composeMetadata, dubSteps, uploadChecklist } from "../package/metadata.mjs";
import { finalReviewHtml } from "../review/pages.mjs";
import { dubScript, translationHash } from "./plan.mjs";

const TOKEN = `mkv_${"t".repeat(43)}`;

/** The site as review-push and review-pull see it: it keeps files, reviews and the owner's decisions. */
function site() {
  const state = { calls: [], files: new Map(), reviews: [] };
  const fetchImpl = async (url, init = {}) => {
    const { pathname, searchParams } = new URL(url);
    state.calls.push({ method: init.method, pathname });
    const route = pathname.replace("/api/video/reviews/", "");
    if (init.method === "PUT" && route.includes("/files/")) {
      const hash = route.split("/files/")[1];
      const parts = state.files.get(hash) ?? [];
      parts[Number(searchParams.get("part"))] = Buffer.from(init.body);
      state.files.set(hash, parts);
      return Response.json({ received: parts.map((_, index) => index), complete: parts.filter(Boolean).length === Number(searchParams.get("parts")) });
    }
    if (init.method === "PUT") return Response.json({ ...JSON.parse(init.body), reviews: [], pending: 0 });
    if (init.method === "POST") {
      const body = JSON.parse(init.body);
      state.reviews.unshift({ id: `r${state.reviews.length}`, status: "pending", choice: null, note: null, decided_at: null, ...body });
      return Response.json(state.reviews[0], { status: 201 });
    }
    return Response.json({ slug: "fixture-minimal", reviews: state.reviews });
  };
  return { state, fetchImpl };
}

function context(box, fetchImpl) {
  const out = { stdout: "", stderr: "" };
  const ctx = {
    root: box.root,
    env: { VIDEO_WORKDIR: box.work, MOKAAIR_VIDEO_TOKEN: TOKEN },
    home: box.base,
    fetch: fetchImpl,
    stdout: { write: (text) => (out.stdout += text) },
    stderr: { write: (text) => (out.stderr += text) },
    now: () => new Date("2026-09-27T08:00:00Z"),
    sleep: async () => {},
  };
  return { out, ctx };
}

function translationFor(doc, prefix) {
  const lines = {};
  for (const { line } of eachLine(doc)) lines[line.id] = { source_hash: textHash(line.text), text: `${prefix} ${line.id}` };
  return { title: `${prefix} title`, description: `${prefix} description`, tags: [], chapters: {}, source_hashes: {}, lines };
}

/** A fake dub: every line starts five frames after its zh-TW line and speaks for half as long. */
function writeDub(box, project, locale, timeline, { shift = 5, stale = false, format = "m4a" } = {}) {
  const files = dubArtifacts(box.workdir, locale);
  const lines = timeline.lines.map((line) => ({ id: line.id, start_frame: line.start_frame + shift, end_frame: line.start_frame + shift + Math.ceil(line.audio_samples / 2 / 1600), audio_samples: Math.floor(line.audio_samples / 2), tempo: 1 }));
  const words = translationHash(dubScript(project.doc, project.translations[locale], locale).doc);
  const dub = { locale, format, file: `${locale}.${format}`, speech_hash: timeline.speech_hash, translation_hash: stale ? "0000000000000000" : words, total_frames: timeline.total_frames, tempo_max: 1.07, windows: [], lines };
  mkdirSync(files.dir, { recursive: true });
  writeFileSync(files.timeline, JSON.stringify(dub));
  writeFileSync(files.track(format), "not really audio");
  return dub;
}

test("captions of a locale with a current dub follow the dub's timing; the others follow the narration", () => {
  const box = sandbox();
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  const doc = fixture();
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translationFor(doc, "EN")));
  writeFileSync(path.join(box.dir, "i18n", "ja.json"), JSON.stringify(translationFor(doc, "JA")));
  const project = loadProject({ slug: box.slug, root: box.root });
  const speech = speechHash(project.doc, project.lexicon);
  const timeline = { ...estimateTimeline(doc), speech_hash: speech };
  mkdirSync(box.workdir, { recursive: true });
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));

  assert.equal(currentDub(project, box.workdir, "en", speech), null, "no dub yet");
  writeDub(box, project, "en", timeline);
  const en = currentDub(project, box.workdir, "en", speech);
  assert.equal(en.locale, "en");
  assert.ok(en.file.endsWith(path.join("dubs", "en.m4a")));
  assert.equal(dubRole("zh-CN"), "dub_zh_cn");

  const captionLines = captionTimelineOf(en).lines;
  assert.equal(captionLines[0].end_frame, captionLines[1].start_frame, "a dubbed line's cues run to the next dubbed line");
  assert.equal(captionLines.at(-1).end_frame, timeline.total_frames);

  const manifest = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.equal(manifest.locales.en.timing, "dub");
  assert.equal(manifest.locales.ja.timing, "narration");
  assert.equal(manifest.locales["zh-TW"].timing, "narration");
  const enCues = parseSrt(readFileSync(path.join(box.workdir, "captions", "en.srt"), "utf8"));
  const jaCues = parseSrt(readFileSync(path.join(box.workdir, "captions", "ja.srt"), "utf8"));
  assert.equal(enCues[0].start_ms, Math.round(frameToMs(5)), "the English cue starts where the English voice does");
  assert.equal(jaCues[0].start_ms, 0, "Japanese, undubbed, keeps the narration's timing");
  const zh = readFileSync(path.join(box.workdir, "captions", "zh-TW.srt"), "utf8");

  const { dubs, skipped } = dubsForUpload(project, box.workdir, speech);
  assert.deepEqual(dubs.map((dub) => [dub.locale, dub.format, dub.tempo_max]), [["en", "m4a", 1.07]]);
  assert.deepEqual(skipped, {});

  // A stale dub is reported and the cues fall back to the narration; a skipped locale is named.
  writeDub(box, project, "en", timeline, { stale: true });
  mkdirSync(dubArtifacts(box.workdir, "ko").dir, { recursive: true });
  writeFileSync(dubArtifacts(box.workdir, "ko").skipped, JSON.stringify({ reason: "two shortening rounds were not enough", at: "2026-09-27T00:00:00Z" }));
  const again = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.equal(again.locales.en.timing, "narration");
  assert.match(again.locales.en.problems[0], /older than the script or its translation/);
  assert.equal(readFileSync(path.join(box.workdir, "captions", "zh-TW.srt"), "utf8"), zh, "zh-TW captions never change");
  const after = dubsForUpload(project, box.workdir, speech);
  assert.deepEqual(after.dubs, []);
  assert.deepEqual(after.skipped, { ko: "two shortening rounds were not enough" });
});

test("the upload checklist tells the owner where each track goes in Studio, and names the locales given up on", () => {
  const doc = fixture();
  const timeline = { ...estimateTimeline(doc), speech_hash: "abc123" };
  const { metadata } = composeMetadata({ doc, timeline });
  const withDubs = uploadChecklist({ metadata, captions: ["captions/zh-TW.srt"], thumbnail: true, dubs: [{ locale: "en", file: "dubs/en.m4a", format: "m4a", tempo_max: 1.07 }], skippedDubs: { ja: "two shortening rounds were not enough" } });
  assert.match(withDubs, /## 3\. 配音音軌（多語言音訊）/);
  assert.match(withDubs, /`dubs\/en\.m4a`（en，最快處 1\.07 倍速）/);
  assert.match(withDubs, /「語言」→ 這支影片 →「新增語言」→ 選語言 →「配音」旁的「新增」→「選取檔案」/);
  assert.match(withDubs, /ja：two shortening rounds were not enough/);
  assert.match(withDubs, /## 4\. 上架前自我檢查/);
  assert.match(withDubs, /## 5\. 公開/);
  const without = uploadChecklist({ metadata, captions: [], thumbnail: false });
  assert.match(without, /這支沒有配音音軌/);
  assert.doesNotMatch(dubSteps([], {}), /做不出來/);
});

test("review-push --gate dubs sends the tracks bound to a manifest, and the owner's approval means uploaded", async () => {
  const box = sandbox();
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  const doc = fixture();
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify(translationFor(doc, "EN")));
  const project = loadProject({ slug: box.slug, root: box.root });
  const speech = speechHash(project.doc, project.lexicon);
  const timeline = { ...estimateTimeline(doc), speech_hash: speech };
  mkdirSync(box.workdir, { recursive: true });
  writeFileSync(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  const server = site();

  const empty = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "dubs"], empty.ctx), EXIT.owner, "nothing to send before dub ran");
  assert.match(empty.out.stderr, /run dub first/);

  writeDub(box, project, "en", timeline);
  mkdirSync(dubArtifacts(box.workdir, "ja").dir, { recursive: true });
  writeFileSync(dubArtifacts(box.workdir, "ja").skipped, JSON.stringify({ reason: "two shortening rounds were not enough" }));
  const push = context(box, server.fetchImpl);
  assert.equal(await main(["review-push", "--slug", box.slug, "--gate", "dubs"], push.ctx), EXIT.ok);
  const review = server.state.reviews[0];
  assert.equal(review.gate, "dubs");
  assert.deepEqual(review.files.map((file) => [file.role, file.content_type]), [["dub_en", "audio/mp4"]]);
  assert.equal(review.payload.locales.en.status, "ready");
  assert.equal(review.payload.locales.en.file, "en.m4a");
  assert.deepEqual(review.payload.locales.ja, { status: "skipped", reason: "two shortening rounds were not enough" });
  assert.match(review.summary, /配音音軌：en；做不出來：ja/);
  const manifest = JSON.parse(readFileSync(GATES.dubs({ workdir: box.workdir }), "utf8"));
  assert.deepEqual(Object.keys(manifest.locales), ["en", "ja"]);
  assert.ok(server.state.files.size >= 1, "the track went up");

  server.state.reviews[0] = { ...review, status: "approved", decided_at: "2026-09-27T09:00:00Z" };
  const pull = context(box, server.fetchImpl);
  assert.equal(await main(["review-pull", "--slug", box.slug], pull.ctx), EXIT.ok);
  assert.match(pull.out.stdout, /dubs: the owner uploaded these dub tracks/);
  assert.ok(readApprovals(box.workdir).approvals.some((entry) => entry.gate === "dubs" && entry.sha256 === review.content_sha256));
});

test("the final review page plays each dub track beside the video", () => {
  const doc = fixture();
  const timeline = { ...estimateTimeline(doc), speech_hash: "abc123" };
  const html = finalReviewHtml(doc, timeline, { problems: [] }, [{ locale: "en", format: "m4a", tempo_max: 1 }, { locale: "zh-CN", format: "mp3", tempo_max: 1.1 }]);
  assert.match(html, /<h2>配音音軌<\/h2>/);
  assert.match(html, /<audio controls preload="none" src="\.\.\/dubs\/en\.m4a">/);
  assert.match(html, /<audio controls preload="none" src="\.\.\/dubs\/zh-CN\.mp3">/);
  assert.match(html, /最快處 1\.1 倍速/);
  assert.doesNotMatch(finalReviewHtml(doc, timeline, { problems: [] }), /配音音軌/);
});
