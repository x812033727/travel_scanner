import assert from "node:assert/strict";
import { existsSync, mkdirSync, readdirSync, readFileSync, renameSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";
import test from "node:test";

import { AREAS, EXIT, main } from "../cli.mjs";
import { brandingHash } from "../core/branding.mjs";
import { parseSrt } from "../core/captions.mjs";
import { CARD_FRAMES, compilationHash, compilationLayout, OUTRO_FRAMES } from "../core/compilation.mjs";
import { pipelineStatus } from "../core/state.mjs";
import { visualHash } from "../core/timeline.mjs";
import { compilationSandbox, compileContext, EPISODE_FRAMES, EPISODES, fakeFfmpeg, sha, TITLES, writeEpisode } from "./fixture.mjs";
import { audioInputs, cardEntries, cardSegments, checkCompilationLoudness, CompileError, diskNeeded, diskProblem, episodeProblem, joinArgs, joinList, layoutLines, overlapProblems, seconds } from "./plan.mjs";

const TOTAL = EPISODES.reduce((sum, slug) => sum + EPISODE_FRAMES[slug], 0) + EPISODES.length * CARD_FRAMES + OUTRO_FRAMES;
const readWork = (box, name) => JSON.parse(readFileSync(path.join(box.workdir, name), "utf8"));

function installBranding(box) {
  const dir = path.join(box.work, "_branding");
  mkdirSync(dir, { recursive: true });
  const spec = { schema_version: 1, id: "channel-v1" };
  for (const [role, frames] of [["intro", 150], ["outro", 90]]) {
    const bytes = Buffer.from(`channel ${role}`);
    const file = path.join(dir, `${role}.mp4`);
    writeFileSync(file, bytes);
    spec[role] = { file, frames, sha256: sha(bytes) };
  }
  writeFileSync(path.join(dir, "current.json"), JSON.stringify(spec));
  return spec;
}

test("compile is a registered command of the pipeline", () => {
  assert.deepEqual(AREAS.compile, ["compile", "2026-09-27-video-binge-compile"]);
});

test("an episode is cleared for upload only with an approved, present, checked cut and a timeline", () => {
  const approval = { gate: "final", sha256: "a".repeat(64) };
  const good = { approval, exists: true, sha256: "a".repeat(64), checks: { ok: true }, timeline: { total_frames: 100 } };
  assert.equal(episodeProblem(good), null);
  assert.match(episodeProblem({ ...good, approval: null }), /never approved/);
  assert.match(episodeProblem({ ...good, exists: false, sha256: null }), /final\.mp4 is missing/);
  assert.match(episodeProblem({ ...good, sha256: "b".repeat(64) }), /\(bbbbbbbbbbbb\) is not the approved cut \(aaaaaaaaaaaa\)/);
  assert.match(episodeProblem({ ...good, checks: { ok: false, problems: ["1 frame short"] } }), /checks\.json failed: 1 frame short/);
  assert.match(episodeProblem({ ...good, checks: null }), /checks\.json is missing/);
  assert.match(episodeProblem({ ...good, timeline: {} }), /no total_frames/);
});

test("the disk check wants the cuts one and a half times over plus a reserve, and says the numbers", () => {
  const twoGb = 2 * 1024 ** 3;
  assert.equal(diskNeeded(twoGb), Math.ceil(twoGb * 1.5 + 2.5 * 1024 ** 3));
  assert.equal(diskProblem(10 * 1024 ** 3, twoGb, "/work"), null);
  assert.match(diskProblem(3 * 1024 ** 3, twoGb, "/work"), /^not enough free disk on \/work: 3\.00 GB free, 5\.50 GB needed \(2\.00 GB of cuts × 1\.5 \+ 2\.50 GB\)$/);
});

test("a card lays out its transition frames then its still, and is keyed like a slide segment", () => {
  const rendered = { id: "card-1", states: [{ still: "frames/a.png", transition: ["frames/a-t00.png", "frames/a-t01.png"] }] };
  assert.deepEqual(cardEntries(rendered, 60), [{ file: "frames/a-t00.png", frames: 1 }, { file: "frames/a-t01.png", frames: 1 }, { file: "frames/a.png", frames: 58 }]);
  assert.deepEqual(cardEntries({ id: "x", states: [{ still: "frames/b.png", transition: [] }] }, 2), [{ file: "frames/b.png", frames: 2 }]);
  assert.throws(() => cardEntries({ id: "x", states: [] }, 60), CompileError);
  const layout = [{ kind: "card", id: "card-1", frames: 60 }, { kind: "episode", id: "ep", frames: 900 }, { kind: "outro", id: "outro", frames: 120 }];
  const manifest = { scenes: [rendered, { id: "outro", states: [{ still: "frames/o.png", transition: [] }] }] };
  const segments = cardSegments(layout, manifest);
  assert.deepEqual(segments.map((segment) => [segment.id, segment.kind, segment.frames, segment.entries.length]), [["card-1", "card", 60, 3], ["outro", "outro", 120, 1]]);
  assert.match(segments[0].key, /^[0-9a-f]{16}$/);
  assert.notEqual(segments[0].key, segments[1].key);
  assert.throws(() => cardSegments(layout, { scenes: [rendered] }), /no card outro/);
});

test("the join list quotes absolute paths the concat demuxer reads, and the audio is rebuilt per input on the sample grid", () => {
  assert.equal(joinList(["C:\\work\\card-1.mp4", "/work/ep's.mp4"]), "ffconcat version 1.0\nfile 'C:/work/card-1.mp4'\nfile '/work/ep'\\''s.mp4'\n");
  const layout = [{ kind: "card", id: "card-1", frames: 60 }, { kind: "episode", id: "ep", frames: 4321, file: "/work/ep/final.mp4" }, { kind: "outro", id: "outro", frames: 120 }];
  const inputs = audioInputs(layout, {});
  assert.deepEqual(inputs, [{ file: null, frames: 60, samples: 96_000 }, { file: "/work/ep/final.mp4", frames: 4321, samples: 6_913_600 }, { file: null, frames: 120, samples: 192_000 }]);
  assert.equal(seconds(4321), "144.033333");
  assert.equal(seconds(60), "2");
  const args = joinArgs("/work/build/join.ffconcat", inputs, "/work/build/final.partial.mp4");
  const text = args.join(" ");
  assert.ok(text.startsWith("-hide_banner -y -loglevel error -f concat -safe 0 -i /work/build/join.ffconcat -f lavfi -t 2 -i anullsrc=r=48000:cl=stereo -i /work/ep/final.mp4 -f lavfi -t 4 -i anullsrc=r=48000:cl=stereo -filter_complex "), text);
  const filter = args[args.indexOf("-filter_complex") + 1];
  assert.equal(filter, "[1:a]atrim=end_sample=96000,apad=whole_len=96000[a1];[2:a]atrim=end_sample=6913600,apad=whole_len=6913600[a2];[3:a]atrim=end_sample=192000,apad=whole_len=192000[a3];[a1][a2][a3]concat=n=3:v=0:a=1[a]");
  assert.ok(text.endsWith("-map 0:v:0 -c:v copy -map [a] -c:a aac -b:a 384k -ar 48000 -movflags +faststart /work/build/final.partial.mp4"), text);
  assert.equal(args.filter((arg) => arg === "-i").length, 4, "the list plus one input per layout entry");
});

test("the loudness tolerance is wider than a single cut's, the true peak the same", () => {
  assert.deepEqual(checkCompilationLoudness({ integrated: -15.4, truePeak: -1.2 }), []);
  assert.deepEqual(checkCompilationLoudness({ integrated: -12.4, truePeak: -1.2 }), ["loudness -12.4 LUFS, target -14 ± 1.5"]);
  assert.equal(checkCompilationLoudness({ integrated: -14, truePeak: -0.2 }).length, 1);
  assert.deepEqual(checkCompilationLoudness({ integrated: -14, truePeak: null }), []);
  assert.deepEqual(overlapProblems([{ start_ms: 0, end_ms: 10 }, { start_ms: 5, end_ms: 20 }, { start_ms: 20, end_ms: 30 }]), ["cue 2 overlaps the previous cue"]);
});

test("the dry run prints the layout with clocks and titles, the sizes and the disk verdict, and encodes nothing", async () => {
  const box = compilationSandbox();
  const fake = fakeFfmpeg({ total: TOTAL });
  const { out, ctx } = compileContext(box, fake);
  assert.equal(await main(["compile", "--slug", box.slug, "--dry-run"], ctx), EXIT.ok, out.stderr);
  assert.match(out.stdout, /wuxia-full: 3 episodes, \d+ frames \([\d.]+ min\), 3 chapters, compilation [0-9a-f]{16}/);
  assert.match(out.stdout, /0:00:00 {2}card {4}card-1 {2}60 frames {2}第 1 集 初入山門/);
  assert.match(out.stdout, /0:00:02 {2}episode wuxia-ep-1 {2}4321 frames/);
  assert.match(out.stdout, /outro {3}outro {2}120 frames/);
  assert.match(out.stdout, /wuxia-ep-1: 0\.00 GB, [0-9a-f]{12}/);
  assert.match(out.stdout, /disk: 100\.00 GB free/);
  assert.match(out.stdout, /dry run: nothing encoded/);
  assert.equal(fake.calls.length, 0);
  assert.equal(existsSync(path.join(box.workdir, "final.mp4")), false);
  const layout = layoutLines(compilationLayout(box.doc, EPISODES.map((slug) => ({ slug, frames: 30 }))), []);
  assert.equal(layout.length, 7);
});

test("compile encodes the cards, joins the cuts, checks the result, merges the captions and writes the chapters", async () => {
  const box = compilationSandbox({ captions: { "wuxia-ep-2": ["zh-TW", "en", "ja"] } });
  const fake = fakeFfmpeg({ total: TOTAL });
  const { out, ctx } = compileContext(box, fake);
  assert.equal(await main(["compile", "--slug", box.slug], ctx), EXIT.ok, out.stderr + out.stdout);
  // Four cards encoded with the slides' segment settings, then one join, one probe, one loudness measure.
  const encodes = fake.calls.filter((call) => call.tool === "ffmpeg" && call.args.includes("-frames:v"));
  assert.equal(encodes.length, 4);
  assert.deepEqual(encodes.map((call) => call.args[call.args.indexOf("-frames:v") + 1]), ["60", "60", "60", "120"]);
  const join = fake.calls.find((call) => call.args.includes("-filter_complex"));
  assert.ok(join, "one join call");
  const list = readFileSync(join.args[join.args.indexOf("-i") + 1], "utf8").trim().split("\n");
  assert.equal(list.length, 8, "the header, three cards, three cuts and the outro");
  assert.match(list[1], /segments\/card-1-[0-9a-f]{16}\.mp4'$/);
  assert.match(list[2], /wuxia-ep-1\/final\.mp4'$/);
  assert.match(list[7], /segments\/outro-[0-9a-f]{16}\.mp4'$/);
  assert.equal(join.args.filter((arg) => arg === "-i").length, 8);
  assert.equal(join.args[join.args.indexOf("-filter_complex") + 1].split(";").length, 8);
  assert.deepEqual(fake.calls.map((call) => call.tool).slice(-3), ["ffmpeg", "ffprobe", "ffmpeg"]);
  assert.ok(existsSync(path.join(box.workdir, "final.mp4")));
  assert.equal(existsSync(path.join(box.workdir, "build", "final.partial.mp4")), false);

  const episodes = EPISODES.map((slug) => ({ slug, sha256: box.episodes[slug].sha256 }));
  const hash = compilationHash(box.doc, episodes);
  const checks = readWork(box, "checks.json");
  assert.equal(checks.ok, true, JSON.stringify(checks.problems));
  assert.equal(checks.compilation_hash, hash);
  assert.equal(checks.visual_hash, visualHash(box.doc));
  assert.equal(checks.metrics.frames, TOTAL);
  assert.deepEqual(checks.metrics.loudness, { integrated: -14.4, truePeak: -1.6 });
  assert.deepEqual(checks.metrics.episodes.map((episode) => [episode.slug, episode.start_frame, episode.frames]), [["wuxia-ep-1", 60, 4321], ["wuxia-ep-2", 4441, 3900], ["wuxia-ep-3", 8401, 5010]]);
  assert.equal(checks.metrics.episodes[0].sha256, box.episodes["wuxia-ep-1"].sha256);

  // The captions: zh-TW and en from every episode, shifted to where the episode starts; ja only one episode had.
  const captions = readWork(box, "captions/manifest.json");
  assert.equal(captions.compilation_hash, hash);
  assert.deepEqual(Object.keys(captions.locales), ["zh-TW", "en"]);
  assert.deepEqual(captions.skipped, { ja: ["wuxia-ep-1", "wuxia-ep-3"], ko: EPISODES });
  assert.deepEqual(captions.locales.en, { cues: 6, problems: [], timing: "compilation" });
  const en = parseSrt(readFileSync(path.join(box.workdir, "captions", "en.srt"), "utf8"));
  assert.equal(en.length, 6);
  assert.deepEqual([en[0].start_ms, en[0].text], [2000, "en wuxia-ep-1 1"]);
  assert.deepEqual([en[2].start_ms, en[2].end_ms, en[2].text], [Math.round((4441 * 1000) / 30), Math.round((4441 * 1000) / 30) + 1500, "en wuxia-ep-2 1"]);
  assert.ok(existsSync(path.join(box.workdir, "captions", "zh-TW.vtt")));
  assert.equal(existsSync(path.join(box.workdir, "captions", "ja.srt")), false);
  assert.match(out.stdout, /captions: zh-TW, en; skipped ja \(no current file in wuxia-ep-1, wuxia-ep-3\)/);

  // The manifest and the timeline the later stages read.
  const manifest = readWork(box, "compile/manifest.json");
  assert.equal(manifest.total_frames, TOTAL);
  assert.deepEqual(manifest.chapters.map((chapter) => [chapter.at, chapter.title, chapter.scene]), [[0, "第 1 集 初入山門", "wuxia-ep-1"], [146, "第 2 集 夜探藏經閣", "wuxia-ep-2"], [278, "第 3 集 劍冢之約", "wuxia-ep-3"]]);
  assert.equal(manifest.layout.length, 7);
  const timeline = readWork(box, "timeline.json");
  assert.deepEqual(Object.keys(timeline), ["fps", "sample_rate", "total_frames", "scenes", "lines", "chapters", "speech_hash", "compilation_hash"]);
  assert.equal(timeline.speech_hash, null);
  assert.deepEqual(timeline.chapters[1], { title: "第 2 集 夜探藏經閣", scene: "wuxia-ep-2", start_frame: 4381, episode: 2 });
  assert.match(out.stdout, /4 of 4 cards encoded/);
  assert.match(out.stdout, /next: node tools\/video\/cli\.mjs qa --slug wuxia-full/);
  const state = readWork(box, "state.json");
  assert.deepEqual(state.runs.map((run) => run.stage), ["compile"]);

  // Status: compiled; the translations are what is left before the owner's final approval.
  const status = await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  assert.deepEqual(status.steps.map((step) => [step.id, step.done]).slice(0, 4), [["metadata planned", true], ["cards rendered", true], ["video compiled", true], ["metadata translated", false]]);

  // A second run reuses every cached card and still joins.
  const again = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
  assert.match(again.out.stdout, /0 of 4 cards encoded/);
  assert.equal(readdirSync(path.join(box.workdir, "segments")).filter((name) => name.endsWith(".mp4")).length, 4);
});

test("an episode whose cut is not the approved one, a missing render and a full disk each refuse with their code", async () => {
  const box = compilationSandbox();
  // The second episode was re-cut after its approval.
  writeFileSync(path.join(box.work, "wuxia-ep-2", "final.mp4"), Buffer.from("a newer cut"));
  const stale = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], stale.ctx), EXIT.usage);
  assert.match(stale.out.stderr, /^episode wuxia-ep-2 is not cleared for upload: final\.mp4 \([0-9a-f]{12}\) is not the approved cut/);
  writeEpisode(box.work, "wuxia-ep-2", { approved: false });
  const never = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], never.ctx), EXIT.usage);
  assert.match(never.out.stderr, /episode wuxia-ep-2 is not cleared for upload: final\.mp4 was never approved/);
  writeEpisode(box.work, "wuxia-ep-2");

  const full = compileContext(box, fakeFfmpeg({ total: TOTAL }), { freeBytes: () => 1024 });
  assert.equal(await main(["compile", "--slug", box.slug], full.ctx), EXIT.owner);
  assert.match(full.out.stderr, /not enough free disk .* GB needed/);

  const stripped = compilationSandbox({ rendered: false });
  const unrendered = compileContext(stripped, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", stripped.slug], unrendered.ctx), EXIT.usage);
  assert.match(unrendered.out.stderr, /frames\/manifest\.json is missing .*run render first/);

  const box2 = compilationSandbox();
  const fake = fakeFfmpeg({ total: TOTAL });
  writeFileSync(path.join(box2.work, "STOP"), "");
  const stopped = compileContext(box2, fake);
  assert.equal(await main(["compile", "--slug", box2.slug], stopped.ctx), EXIT.ok);
  assert.match(stopped.out.stdout, /stopped by the STOP file after 0 cards/);
  assert.equal(fake.calls.length, 0);

  const drama = compilationSandbox();
  const { ctx, out } = compileContext(drama, fakeFfmpeg());
  assert.equal(await main(["compile", "--slug", "fixture-drama"], { ...ctx, root: drama.root }).catch((error) => error.message), EXIT.usage, "the fixture is not there");
  assert.equal(await main(["compile"], ctx), EXIT.usage);
  assert.match(out.stderr, /compile needs --slug/);
});

test("a failed probe leaves checks.json failed and exits 1, and a changed card title re-encodes that card", async () => {
  const box = compilationSandbox();
  const fake = fakeFfmpeg({ total: TOTAL - 1 });
  const { out, ctx } = compileContext(box, fake);
  assert.equal(await main(["compile", "--slug", box.slug], ctx), EXIT.lint);
  assert.match(out.stdout, /CHECK \d+ video frames, the timeline has \d+/);
  assert.equal(readWork(box, "checks.json").ok, false);
  const status = await pipelineStatus({ slug: box.slug, root: box.root, workdir: box.workdir });
  const compiled = status.steps.find((step) => step.id === "video compiled");
  assert.equal(compiled.done, false);
  assert.match(compiled.note, /checks failed/);

  // A new title changes the card's picture: render again, then compile encodes that card only.
  const doc = { ...box.doc, compilation: { ...box.doc.compilation, titles: { ...TITLES, "wuxia-ep-2": "改了的標題" } } };
  doc.scenes[1] = { ...doc.scenes[1], chapter: "第 2 集 改了的標題", data: { title: "改了的標題" }, lines: [{ id: "c002", text: "第 2 集 改了的標題" }] };
  writeFileSync(path.join(box.dir, "video.json"), JSON.stringify(doc));
  const before = fakeFfmpeg({ total: TOTAL });
  const unrendered = compileContext(box, before);
  assert.equal(await main(["compile", "--slug", box.slug], unrendered.ctx), EXIT.usage, "the cards are stale");
  assert.match(unrendered.out.stderr, /rendered for older cards/);
  const { renderCards } = await import("./fixture.mjs");
  renderCards(box, doc);
  const after = fakeFfmpeg({ total: TOTAL });
  const redo = compileContext(box, after);
  assert.equal(await main(["compile", "--slug", box.slug], redo.ctx), EXIT.ok, redo.out.stderr);
  assert.match(redo.out.stdout, /encoded card-2 \(60 frames\)\n/);
  assert.match(redo.out.stdout, /1 of 4 cards encoded/);
  assert.equal(readWork(box, "checks.json").visual_hash, visualHash(doc));
  assert.equal(sha(readFileSync(path.join(box.workdir, "final.mp4"))).length, 64);
});

test("a compilation strips episode bookends and wraps the joined body only once, preserving caption and chapter positions", async () => {
  const box = compilationSandbox();
  const spec = installBranding(box);
  const sourceBranding = { hash: "a".repeat(64), id: "earlier-channel", intro_frames: 150, outro_frames: 90 };
  for (const slug of [EPISODES[0], EPISODES[2]]) box.episodes[slug] = writeEpisode(box.work, slug, { branding: sourceBranding });
  const bodyFrames = TOTAL - OUTRO_FRAMES;
  const total = bodyFrames + 240;
  const fake = fakeFfmpeg({ total, framesByFile: { [spec.intro.file]: 150, [spec.outro.file]: 90 } });
  const { out, ctx } = compileContext(box, fake);
  assert.equal(await main(["compile", "--slug", box.slug], ctx), EXIT.ok, out.stderr);
  const bodyJoin = fake.calls.find((call) => call.args.at(-1).endsWith("body.partial.mp4"));
  const bodyList = readFileSync(bodyJoin.args[bodyJoin.args.indexOf("-i") + 1], "utf8");
  assert.match(bodyList, /wuxia-ep-1\/build\/body\.mp4/);
  assert.match(bodyList, /wuxia-ep-2\/final\.mp4/);
  assert.match(bodyList, /wuxia-ep-3\/build\/body\.mp4/);
  assert.doesNotMatch(bodyList, /outro-/);
  const joins = fake.calls.filter((call) => call.args.includes("-filter_complex"));
  assert.equal(joins.length, 2, "one body join and one channel wrap");
  const outerList = readFileSync(joins[1].args[joins[1].args.indexOf("-i") + 1], "utf8").trim().split("\n");
  assert.equal(outerList.length, 4, "one intro, one complete body, one outro");
  assert.match(outerList[1], /\/intro\.mp4'$/);
  assert.match(outerList[2], /\/build\/body\.partial\.mp4'$/, "the old retained body survives until the wrap succeeds");
  assert.match(outerList[3], /\/outro\.mp4'$/);
  const checks = readWork(box, "checks.json");
  assert.equal(checks.branding.hash, brandingHash(spec));
  assert.equal(checks.branding.body_frames, bodyFrames);
  assert.equal(checks.branding.body_file, "build/body.mp4");
  assert.equal(checks.branding.body_sha256, sha(readFileSync(path.join(box.workdir, "build", "body.mp4"))));
  assert.equal(checks.metrics.frames, total);
  assert.equal(readWork(box, "branding.json").hash, brandingHash(spec));
  const hash = compilationHash(box.doc, EPISODES.map((slug) => ({ slug, ...box.episodes[slug] })));
  assert.equal(checks.compilation_hash, hash);
  const timeline = readWork(box, "timeline.json");
  assert.equal(timeline.total_frames, bodyFrames, "the saved timeline remains body-only");
  assert.equal(timeline.chapters[1].start_frame, 4381);
  const manifest = readWork(box, "compile/manifest.json");
  assert.equal(manifest.chapters[0].start_frame, 0);
  assert.equal(manifest.chapters[1].start_frame, 4531);
  assert.equal(manifest.layout.some((entry) => entry.kind === "outro"), false);
  const cues = parseSrt(readFileSync(path.join(box.workdir, "captions", "en.srt"), "utf8"));
  assert.equal(cues[0].start_ms, 7000, "the source's intro is replaced, not stacked");
  assert.equal(cues[2].start_ms, Math.round(4441 * 1000 / 30) + 5000, "legacy episode captions get the single channel intro");
  assert.equal(cues[4].start_ms, Math.round(8401 * 1000 / 30) + 5000);
  assert.equal(readWork(box, "captions/manifest.json").branding_hash, brandingHash(spec));
});

test("an approved source cut cannot hide a changed or missing branded body", async () => {
  const box = compilationSandbox();
  const sourceBranding = { hash: "a".repeat(64), id: "channel-v1", intro_frames: 150, outro_frames: 90 };
  const source = writeEpisode(box.work, EPISODES[0], { branding: sourceBranding });
  writeFileSync(path.join(source.dir, "build", "body.mp4"), "changed body");
  const changed = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], changed.ctx), EXIT.usage);
  assert.match(changed.out.stderr, /body_sha256 mismatch/);
  writeEpisode(box.work, EPISODES[0], { branding: sourceBranding });
  const checksFile = path.join(source.dir, "checks.json");
  const checks = JSON.parse(readFileSync(checksFile, "utf8"));
  checks.branding.body_file = "build/missing.mp4";
  writeFileSync(checksFile, JSON.stringify(checks));
  const missing = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], missing.ctx), EXIT.usage);
  assert.match(missing.out.stderr, /branding body is missing/);
  checks.branding.body_file = "../another-video/final.mp4";
  writeFileSync(checksFile, JSON.stringify(checks));
  const outside = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], outside.ctx), EXIT.usage);
  assert.match(outside.out.stderr, /inside its work directory/);
  writeEpisode(box.work, EPISODES[0], { branding: sourceBranding });
  writeFileSync(path.join(source.dir, "final.mp4"), "changed final");
  const final = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], final.ctx), EXIT.usage);
  assert.match(final.out.stderr, /not the approved cut/, "final approval is checked before the retained body");
});

test("branded source captions need their matching manifest before their intro can be removed", async () => {
  for (const stale of ["different branding", "missing manifest"]) {
    const box = compilationSandbox();
    const sourceBranding = { hash: "a".repeat(64), id: "channel-v1", intro_frames: 150, outro_frames: 90 };
    const source = writeEpisode(box.work, EPISODES[0], { branding: sourceBranding });
    const first = compileContext(box, fakeFfmpeg({ total: TOTAL }));
    assert.equal(await main(["compile", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
    assert.ok(existsSync(path.join(box.workdir, "captions", "en.srt")));
    // Model adopting branding while the episode still has captions on its old body timeline.
    const manifestFile = path.join(source.dir, "captions", "manifest.json");
    if (stale === "missing manifest") rmSync(manifestFile);
    else writeFileSync(manifestFile, JSON.stringify({ branding_hash: "b".repeat(64), locales: { en: {} } }));
    writeFileSync(path.join(source.dir, "captions", "en.srt"), "1\n00:00:00,000 --> 00:00:01,500\nold body timing\n");
    const again = compileContext(box, fakeFfmpeg({ total: TOTAL }));
    assert.equal(await main(["compile", "--slug", box.slug], again.ctx), EXIT.ok, again.out.stderr);
    const captions = readWork(box, "captions/manifest.json");
    assert.equal(captions.locales.en, undefined, stale);
    assert.deepEqual(captions.skipped.en, [EPISODES[0]], stale);
    assert.deepEqual(captions.skipped["zh-TW"], [EPISODES[0]], stale);
    for (const extension of ["srt", "vtt"]) assert.equal(existsSync(path.join(box.workdir, "captions", `en.${extension}`)), false, `${stale}: an old merged track must not survive for package`);
    assert.match(again.out.stdout, /no current file in wuxia-ep-1/);
  }
});

test("an existing unpinned compilation ignores a new default until explicitly adopted", async () => {
  const box = compilationSandbox();
  const first = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
  const spec = installBranding(box);
  const again = compileContext(box, fakeFfmpeg({ total: TOTAL }));
  assert.equal(await main(["compile", "--slug", box.slug, "--force"], again.ctx), EXIT.ok, again.out.stderr);
  assert.equal(readWork(box, "checks.json").branding, undefined);
  assert.equal(existsSync(path.join(box.workdir, "branding.json")), false);
  const adopted = compileContext(box, fakeFfmpeg({ total: TOTAL - OUTRO_FRAMES + 240, framesByFile: { [spec.intro.file]: 150, [spec.outro.file]: 90 } }));
  assert.equal(await main(["compile", "--slug", box.slug, "--adopt-branding"], adopted.ctx), EXIT.ok, adopted.out.stderr);
  assert.equal(readWork(box, "checks.json").branding.hash, brandingHash(spec));
});

test("a failed channel wrap preserves the existing final, retained body and branding pin", async () => {
  const box = compilationSandbox();
  const spec = installBranding(box);
  const fake = fakeFfmpeg({ total: TOTAL - OUTRO_FRAMES + 240, framesByFile: { [spec.intro.file]: 150, [spec.outro.file]: 90 } });
  const first = compileContext(box, fake);
  assert.equal(await main(["compile", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
  const previous = Object.fromEntries(["final.mp4", "build/body.mp4", "branding.json", "checks.json"].map((file) => [file, readFileSync(path.join(box.workdir, file))]));
  const failing = compileContext(box, fake, { runTool: async (tool, args) => {
    if (args.at(-1).endsWith("final.partial.mp4")) throw new Error("wrapper failed");
    return fake.runTool(tool, args);
  } });
  await assert.rejects(main(["compile", "--slug", box.slug], failing.ctx), /wrapper failed/);
  for (const [file, bytes] of Object.entries(previous)) assert.deepEqual(readFileSync(path.join(box.workdir, file)), bytes, file);
});

test("a failed branded probe preserves the approved compilation and all timing records", async () => {
  const box = compilationSandbox();
  const spec = installBranding(box);
  const total = TOTAL - OUTRO_FRAMES + 240;
  const framesByFile = { [spec.intro.file]: 150, [spec.outro.file]: 90 };
  const first = compileContext(box, fakeFfmpeg({ total, framesByFile }));
  assert.equal(await main(["compile", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
  writeFileSync(path.join(box.workdir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", sha256: sha(readFileSync(path.join(box.workdir, "final.mp4"))) }] }));
  const files = ["final.mp4", "build/body.mp4", "branding.json", "checks.json", "approvals.json", "timeline.json", "compile/manifest.json", "captions/manifest.json", "captions/en.srt"];
  const previous = Object.fromEntries(files.map((file) => [file, readFileSync(path.join(box.workdir, file))]));
  const fake = fakeFfmpeg({ total: total - 1, framesByFile });
  const failed = compileContext(box, fake);
  assert.equal(await main(["compile", "--slug", box.slug], failed.ctx), EXIT.lint);
  assert.match(failed.out.stdout, /previous compilation and its captions remain unchanged/);
  for (const [file, bytes] of Object.entries(previous)) assert.deepEqual(readFileSync(path.join(box.workdir, file)), bytes, file);
  assert.equal(readWork(box, "build/branding-failed-checks.json").ok, false);
  assert.equal(fake.calls.filter((call) => call.tool === "ffprobe").at(-1).args.at(-1), path.join(box.workdir, "build", "final.partial.mp4"));
  assert.equal(existsSync(path.join(box.workdir, "build", "body.partial.mp4")), true);
});

test("a first branded build that fails QA still adopts the channel package on retry", async () => {
  const box = compilationSandbox();
  const spec = installBranding(box);
  const total = TOTAL - OUTRO_FRAMES + 240;
  const framesByFile = { [spec.intro.file]: 150, [spec.outro.file]: 90 };
  const failed = compileContext(box, fakeFfmpeg({ total: total - 1, framesByFile }));
  assert.equal(await main(["compile", "--slug", box.slug], failed.ctx), EXIT.lint);
  assert.equal(existsSync(path.join(box.workdir, "final.mp4")), false);
  assert.equal(existsSync(path.join(box.workdir, "branding.json")), false);
  assert.equal(existsSync(path.join(box.workdir, "checks.json")), false);
  const retry = compileContext(box, fakeFfmpeg({ total, framesByFile }));
  assert.equal(await main(["compile", "--slug", box.slug], retry.ctx), EXIT.ok, retry.out.stderr + retry.out.stdout);
  assert.equal(readWork(box, "checks.json").branding.hash, brandingHash(spec));
  assert.equal(readWork(box, "timeline.json").total_frames, TOTAL - OUTRO_FRAMES);
  assert.equal(existsSync(path.join(box.workdir, "build", "branding-failed-checks.json")), false);
});

test("a failed branded commit rolls captions and timing records back with the media", async () => {
  const box = compilationSandbox();
  const spec = installBranding(box);
  const makeFake = () => fakeFfmpeg({ total: TOTAL - OUTRO_FRAMES + 240, framesByFile: { [spec.intro.file]: 150, [spec.outro.file]: 90 } });
  const first = compileContext(box, makeFake());
  assert.equal(await main(["compile", "--slug", box.slug], first.ctx), EXIT.ok, first.out.stderr);
  writeFileSync(path.join(box.workdir, "captions", "ja.srt"), "previous stale caption");
  const files = ["final.mp4", "build/body.mp4", "branding.json", "checks.json", "timeline.json", "compile/manifest.json", "captions/manifest.json", "captions/en.srt", "captions/ja.srt"];
  const previous = Object.fromEntries(files.map((file) => [file, readFileSync(path.join(box.workdir, file))]));
  const failed = compileContext(box, makeFake(), { renameBranding: (from, to) => {
    if (to === path.join(box.workdir, "checks.json")) throw new Error("injected commit failure");
    renameSync(from, to);
  } });
  await assert.rejects(main(["compile", "--slug", box.slug], failed.ctx), /injected commit failure/);
  for (const [file, bytes] of Object.entries(previous)) assert.deepEqual(readFileSync(path.join(box.workdir, file)), bytes, file);
  assert.equal(existsSync(path.join(box.workdir, "build", "final.partial.mp4")), true);
  const retry = compileContext(box, makeFake());
  assert.equal(await main(["compile", "--slug", box.slug], retry.ctx), EXIT.ok, retry.out.stderr);
  assert.equal(existsSync(path.join(box.workdir, "captions", "ja.srt")), false, "only the complete current caption set is promoted");
  assert.equal(readdirSync(path.join(box.workdir, "build")).some((name) => name.startsWith("compile-pending-")), false);
});
