import assert from "node:assert/strict";
import { appendFileSync, existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { approvalState, approve } from "./approvals.mjs";
import { parseSrt } from "./captions.mjs";
import { sandbox } from "./fixtures/load.mjs";
import { atomicWrite, isInside, resolveWorkdir, stopRequested, UsageError } from "./paths.mjs";
import { eachLine, textHash } from "./schema.mjs";
import { localeTexts, runCaptions, StageError } from "./stages.mjs";
import { loadProject, pipelineStatus, recordStage } from "./state.mjs";
import { estimateTimeline, speechHash } from "./timeline.mjs";

/** What the TTS stage will write: a timeline with the hash of the script it was built from. */
function writeTimeline(box) {
  const project = loadProject({ slug: box.slug, root: box.root });
  const timeline = { ...estimateTimeline(project.doc), speech_hash: speechHash(project.doc, project.lexicon) };
  atomicWrite(path.join(box.workdir, "timeline.json"), JSON.stringify(timeline));
  return timeline;
}

test("the work directory is <base>/<slug> and never inside the repository", () => {
  const box = sandbox();
  assert.equal(resolveWorkdir({ flag: box.work, slug: "a", root: box.root }), path.join(box.work, "a"));
  assert.equal(resolveWorkdir({ env: { VIDEO_WORKDIR: box.work }, slug: "a", root: box.root }), path.join(box.work, "a"));
  // With neither, videos go under the home directory, so nobody has to set a variable first.
  assert.equal(resolveWorkdir({ env: {}, slug: "a", root: box.root, home: box.base }), path.join(box.base, "mokaair-work", "videos", "a"));
  assert.throws(() => resolveWorkdir({ env: {}, slug: "a", root: box.root, home: box.root }), UsageError);
  assert.throws(() => resolveWorkdir({ flag: path.join(box.root, "tmp"), slug: "a", root: box.root }), /inside the repository/);
  assert.ok(isInside(path.join(box.root, "x", "y"), box.root));
  assert.ok(!isInside(box.work, box.root));
});

test("atomicWrite leaves the finished file and no temporary", () => {
  const box = sandbox();
  const file = path.join(box.workdir, "deep", "a.json");
  atomicWrite(file, "{}");
  atomicWrite(file, '{"b":1}');
  assert.equal(readFileSync(file, "utf8"), '{"b":1}');
  assert.deepEqual(readdirSync(path.dirname(file)), ["a.json"]);
});

test("a STOP file in the video's directory or the base above it asks stages to stop", () => {
  const box = sandbox();
  mkdirSync(box.workdir);
  assert.ok(!stopRequested(box.workdir));
  writeFileSync(path.join(box.work, "STOP"), "");
  assert.ok(stopRequested(box.workdir));
});

test("an approval binds the exact file and goes stale when the file changes", async () => {
  const box = sandbox();
  const places = { docDir: box.dir, workdir: box.workdir };
  assert.equal((await approvalState({ gate: "outline", ...places })).status, "missing");
  assert.equal((await approvalState({ gate: "final", ...places })).status, "absent");
  const entry = await approve({ gate: "outline", ...places, now: new Date("2026-09-24T01:00:00Z"), note: "owner chose outline B" });
  assert.equal(entry.file, "brief.md");
  assert.equal((await approvalState({ gate: "outline", ...places })).status, "approved");
  appendFileSync(path.join(box.dir, "brief.md"), "\n一行新增的字\n");
  assert.equal((await approvalState({ gate: "outline", ...places })).status, "stale");
  await assert.rejects(approve({ gate: "final", ...places }), /does not exist yet/);
});

test("status walks the checklist and names the next command", async () => {
  const box = sandbox();
  const status = async () => (await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir })).next;
  assert.match((await status()).todo, /approve --slug fixture-minimal --gate outline/);
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir });
  assert.equal((await status()).id, "fact-checked");
  writeFileSync(path.join(box.dir, "verify-1.md"), "# 查核\n");
  assert.equal((await status()).id, "narration synthesized");
  writeTimeline(box);
  assert.equal((await status()).id, "narration approved");
  await approve({ gate: "audio", docDir: box.dir, workdir: box.workdir });
  const next = await status();
  assert.equal(next.id, "frames rendered");
  assert.match(next.todo, /cli\.mjs render --slug fixture-minimal/);
});

test("editing the script after synthesis makes the narration stale again", async () => {
  const box = sandbox();
  await approve({ gate: "outline", docDir: box.dir, workdir: box.workdir });
  writeFileSync(path.join(box.dir, "verify-1.md"), "ok");
  writeTimeline(box);
  const file = path.join(box.dir, "video.json");
  writeFileSync(file, readFileSync(file, "utf8").replace("今天用三個問題", "今天只用三個問題"));
  const status = await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.equal(status.next.id, "narration synthesized");
  assert.equal(status.next.note, "timeline.json was built for an older script");
});

test("captions: zh-TW always, a translated locale only when every line is current", () => {
  const box = sandbox();
  assert.throws(() => runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir }), StageError);
  writeTimeline(box);
  const project = loadProject({ slug: box.slug, root: box.root });
  const lines = Object.fromEntries([...eachLine(project.doc)].map(({ line }) => [line.id, { source_hash: textHash(line.text), text: `English for ${line.id}.` }]));
  mkdirSync(path.join(box.dir, "i18n"));
  writeFileSync(path.join(box.dir, "i18n", "en.json"), JSON.stringify({ lines }));
  writeFileSync(path.join(box.dir, "i18n", "ja.json"), JSON.stringify({ lines: { ...lines, k7p2: { source_hash: "stale0000000", text: "古い" } } }));

  const manifest = runCaptions({ slug: box.slug, root: box.root, workdir: box.workdir, now: new Date("2026-09-24T02:00:00Z") });
  assert.deepEqual(Object.keys(manifest.locales).sort(), ["en", "zh-TW"]);
  assert.deepEqual(manifest.skipped, { ja: ["k7p2"] });
  assert.deepEqual(manifest.chapters, []);
  const zh = parseSrt(readFileSync(path.join(box.workdir, "captions", "zh-TW.srt"), "utf8"));
  // 32 characters: one cue, two lines of at most 16. No comma lets both halves fit, so the break
  // falls at the middle.
  assert.equal(zh[0].text, "每次有新模型出來，排行榜就換一次\n第一名，你真的每次都要跟著換嗎？");
  assert.ok(existsSync(path.join(box.workdir, "captions", "en.vtt")));
  assert.ok(!existsSync(path.join(box.workdir, "captions", "ja.srt")));
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.deepEqual(state.runs.map((run) => run.stage), ["captions"]);
});

test("localeTexts leaves out translations older than their line", () => {
  const box = sandbox();
  const { doc } = loadProject({ slug: box.slug, root: box.root });
  const { texts, skipped } = localeTexts(doc, { ko: { lines: { k7p2: { source_hash: textHash(doc.scenes[0].lines[0].text), text: "안녕" } } } });
  assert.equal(texts.ko.k7p2, "안녕");
  assert.equal(skipped.ko.length, 6);
});

test("recordStage appends runs for the handover", () => {
  const box = sandbox();
  recordStage(box.workdir, "tts", { lines: 7 }, new Date("2026-09-24T03:00:00Z"));
  recordStage(box.workdir, "render", {}, new Date("2026-09-24T03:05:00Z"));
  const state = JSON.parse(readFileSync(path.join(box.workdir, "state.json"), "utf8"));
  assert.deepEqual(state.runs, [
    { stage: "tts", at: "2026-09-24T03:00:00.000Z", lines: 7 },
    { stage: "render", at: "2026-09-24T03:05:00.000Z" },
  ]);
});
