// `compile`: a binge series' cleared episodes joined into its compilation (docs/videos/BINGE.md).
//
// Reads each episode's approved final.mp4 from the work directory beside the compilation's,
// refuses one that is not the cut the owner approved, encodes the chapter cards render drew,
// joins picture by copy and sound by one encode, checks the result, merges the episodes'
// captions and writes the chapters, so `qa`, `package` and `review-push` read the compilation
// like any other finished video. Every ffmpeg argument is built in plan.mjs.
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, renameSync, rmSync, statfsSync, statSync, writeFileSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { commitBrandedVideo, wrapVideo } from "../assemble/branding.mjs";
import { checkProbe, concatList, ebur128Args, parseEbur128, probeArgs, segmentArgs } from "../assemble/plan.mjs";
import { readApprovals, sha256File } from "../core/approvals.mjs";
import { presentationTimeline, selectBrandingForBuild, shiftBrandingCues } from "../core/branding.mjs";
import { toSrt, toVtt } from "../core/captions.mjs";
import { chapterList, compilationHash, compilationLayout, compilationTimeline, isCompilation, mergeCaptions, totalFrames } from "../core/compilation.mjs";
import { atomicWrite, isInside, readJson, resolveWorkBase, resolveWorkdir, stopRequested, UsageError } from "../core/paths.mjs";
import { LOCALES } from "../core/schema.mjs";
import { ARTIFACTS, lintProject, loadProject, recordStage } from "../core/state.mjs";
import { frameToMs, visualHash } from "../core/timeline.mjs";
import { audioInputs, cardSegments, checkCompilationLoudness, CompileError, diskProblem, episodeProblem, gigabytes, joinArgs, joinList, layoutLines, overlapProblems } from "./plan.mjs";

/** Bytes free on the file system holding `dir`. */
export function freeBytes(dir) {
  const stats = statfsSync(dir);
  return Number(stats.bavail) * Number(stats.bsize);
}

/**
 * Each episode as the join needs it, or the first refusal: { episodes, bytes } or { problem }.
 * The cut's hash is measured, not trusted: it must be the one the owner's final approval bound.
 */
async function readEpisodes(doc, workBase) {
  const episodes = [];
  let bytes = 0;
  for (const slug of doc.compilation.episodes) {
    const dir = path.join(workBase, slug);
    const final = path.join(dir, ARTIFACTS.video);
    const exists = existsSync(final);
    const timeline = readJson(path.join(dir, ARTIFACTS.timeline), null);
    const checks = readJson(path.join(dir, ARTIFACTS.checks), null);
    const sha256 = exists ? await sha256File(final) : null;
    const problem = episodeProblem({
      approval: readApprovals(dir).approvals.filter((entry) => entry.gate === "final").at(-1) ?? null,
      exists,
      sha256,
      checks,
      timeline,
    });
    if (problem) return { problem: `episode ${slug} is not cleared for upload: ${problem}` };
    // Approval always binds the published cut first. Only then may we use the retained body,
    // whose separate hash prevents an edited body from entering the compilation unnoticed.
    const branding = checks.branding;
    let file = final;
    if (branding) {
      if (typeof branding.body_file !== "string" || !branding.body_file || path.isAbsolute(branding.body_file)) return { problem: `episode ${slug} has no relative branding body_file` };
      file = path.resolve(dir, branding.body_file);
      if (!isInside(file, dir) || file === final) return { problem: `episode ${slug} branding body_file must name a retained body inside its work directory` };
      if (!existsSync(file)) return { problem: `episode ${slug} branding body is missing: ${branding.body_file}` };
      if (!/^[0-9a-f]{64}$/.test(branding.body_sha256 ?? "") || await sha256File(file) !== branding.body_sha256) return { problem: `episode ${slug} branding body is not the checked body (body_sha256 mismatch)` };
      if (!/^[0-9a-f]{64}$/.test(branding.hash ?? "") || !Number.isInteger(branding.intro_frames) || branding.intro_frames < 0 || !Number.isInteger(branding.outro_frames) || branding.outro_frames < 0 || branding.body_frames !== timeline.total_frames) return { problem: `episode ${slug} branding frame counts or hash do not match its body timeline` };
    }
    const size = statSync(file).size;
    bytes += size;
    episodes.push({ slug, frames: timeline.total_frames, file, sha256, bytes: size, ...(branding ? { body_sha256: branding.body_sha256, branding_hash: branding.hash, intro_frames: branding.intro_frames } : {}) });
  }
  return { episodes, bytes };
}

/**
 * The episodes' caption files as one track per locale, for every locale every episode has.
 * Returns the manifest: { compilation_hash, locales: { <locale>: { cues, problems } }, skipped:
 * { <locale>: [episode slugs without the file] } }.
 */
function mergeEpisodeCaptions({ layout, workBase, workdir, hash, branding }) {
  const manifest = { compilation_hash: hash, ...(branding ? { branding_hash: branding.hash } : {}), locales: {}, skipped: {} };
  const episodes = layout.filter((entry) => entry.kind === "episode");
  // A branded cut can be approved before captions are regenerated. Its existing SRT must not
  // be interpreted as presentation timing until its manifest binds it to that exact branding.
  const current = new Map(episodes.map((entry) => [entry.slug, !entry.branding_hash || readJson(path.join(workBase, entry.slug, "captions", "manifest.json"), null)?.branding_hash === entry.branding_hash]));
  for (const locale of LOCALES) {
    const file = (slug) => path.join(workBase, slug, "captions", `${locale}.srt`);
    const missing = episodes.filter((entry) => !current.get(entry.slug) || !existsSync(file(entry.slug))).map((entry) => entry.slug);
    if (missing.length) {
      manifest.skipped[locale] = missing;
      for (const extension of ["srt", "vtt"]) rmSync(path.join(workdir, "captions", `${locale}.${extension}`), { force: true });
      continue;
    }
    const cues = shiftBrandingCues(mergeCaptions(episodes.map((entry) => ({ srt: readFileSync(file(entry.slug), "utf8"), offsetMs: frameToMs(entry.start_frame), introMs: frameToMs(entry.intro_frames ?? 0) }))), branding);
    atomicWrite(path.join(workdir, "captions", `${locale}.srt`), toSrt(cues));
    atomicWrite(path.join(workdir, "captions", `${locale}.vtt`), toVtt(cues));
    manifest.locales[locale] = { cues: cues.length, problems: overlapProblems(cues), timing: "compilation" };
  }
  return manifest;
}

export async function run(command, args, ctx) {
  const { EXIT } = ctx;
  const values = parseArgs({ args, options: { slug: { type: "string" }, workdir: { type: "string" }, force: { type: "boolean" }, "dry-run": { type: "boolean" }, "adopt-branding": { type: "boolean" } }, strict: true }).values;
  if (!values.slug) throw new UsageError("compile needs --slug");
  const project = loadProject({ slug: values.slug, root: ctx.root });
  const { doc } = project;
  if (!isCompilation(doc)) {
    ctx.stderr.write(`${doc.slug} is not a compilation: video.json has no "compilation" block (docs/videos/BINGE.md)\n`);
    return EXIT.usage;
  }
  const lint = lintProject(project);
  if (lint.errors.length) {
    ctx.stdout.write(`${doc.slug} has ${lint.errors.length} lint errors; run lint first\n`);
    return EXIT.lint;
  }
  const workBase = resolveWorkBase({ flag: values.workdir, env: ctx.env, root: ctx.root, home: ctx.home });
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: doc.slug, root: ctx.root, home: ctx.home });
  const titles = doc.compilation.titles ?? {};

  const cuts = await readEpisodes(doc, workBase);
  if (cuts.problem) {
    ctx.stderr.write(`${cuts.problem}\n`);
    return EXIT.usage;
  }
  const { episodes, bytes } = cuts;
  const branding = await selectBrandingForBuild({ doc, workdir, workBase, adoptCurrent: values["adopt-branding"] ?? false, now: ctx.now() });
  const layout = compilationLayout(doc, episodes, { branding });
  const bodyFrames = totalFrames(layout);
  const total = bodyFrames + (branding ? branding.intro.frames + branding.outro.frames : 0);
  const chapters = chapterList(layout, titles);
  const hash = compilationHash(doc, episodes);
  const free = (ctx.freeBytes ?? freeBytes)(workBase);
  const disk = diskProblem(free, bytes, workBase);
  if (values["dry-run"]) {
    ctx.stdout.write(`${doc.slug}: ${episodes.length} episodes, ${total} frames (${(total / 30 / 60).toFixed(1)} min), ${chapters.length} chapters, compilation ${hash}\n`);
    for (const line of layoutLines(layout, chapters)) ctx.stdout.write(`  ${line}\n`);
    for (const episode of episodes) ctx.stdout.write(`  ${episode.slug}: ${gigabytes(episode.bytes)} GB, ${episode.sha256.slice(0, 12)}\n`);
    if (branding) ctx.stdout.write(`  branding ${branding.id}: one ${branding.intro.frames}-frame intro and ${branding.outro.frames}-frame outro around the complete body\n`);
    ctx.stdout.write(disk ? `disk: ${disk}\n` : `disk: ${gigabytes(free)} GB free on ${workBase}, enough for ${gigabytes(bytes)} GB of cuts\n`);
    ctx.stdout.write("dry run: nothing encoded\n");
    return EXIT.ok;
  }
  if (disk) {
    ctx.stderr.write(`${disk}\n`);
    return EXIT.owner;
  }
  const manifest = readJson(path.join(workdir, ARTIFACTS.frames), null);
  const visual = visualHash(doc);
  if (!manifest || manifest.visual_hash !== visual) {
    ctx.stderr.write("frames/manifest.json is missing or was rendered for older cards; run render first\n");
    return EXIT.usage;
  }
  let tools = ctx.tools ?? null;
  if (!tools) {
    try {
      tools = await locateFfmpeg(ctx.env);
    } catch (error) {
      if (!(error instanceof ToolMissing)) throw error;
      ctx.stderr.write(`${error.message}\n`);
      return EXIT.missing;
    }
  }
  const exec = ctx.runTool ?? runTool;
  let cards;
  try {
    cards = cardSegments(layout, manifest);
  } catch (error) {
    if (!(error instanceof CompileError)) throw error;
    ctx.stderr.write(`${error.message}\n`);
    return EXIT.usage;
  }

  const started = Date.now();
  const segmentsDir = path.join(workdir, "segments");
  const buildDir = path.join(workdir, "build");
  mkdirSync(segmentsDir, { recursive: true });
  mkdirSync(buildDir, { recursive: true });
  const resolve = (file) => path.join(workdir, file);
  const segmentFiles = {};
  let encoded = 0;
  for (const card of cards) {
    if (stopRequested(workdir)) {
      ctx.stdout.write(`stopped by the STOP file after ${encoded} cards; rerun to continue\n`);
      return EXIT.ok;
    }
    const segment = path.join(segmentsDir, `${card.id}-${card.key}.mp4`);
    segmentFiles[card.id] = segment;
    if (existsSync(segment) && !values.force) continue;
    const list = path.join(segmentsDir, `${card.id}.ffconcat`);
    writeFileSync(list, concatList(card.entries, resolve));
    const partial = `${segment}.partial.mp4`;
    await exec(tools.ffmpeg, segmentArgs(list, partial, card.frames));
    renameSync(partial, segment);
    encoded += 1;
    ctx.stdout.write(`encoded ${card.id} (${card.frames} frames)\n`);
  }
  // Segments of cards that have since changed are never used again.
  const kept = new Set(Object.values(segmentFiles).map((file) => path.basename(file)));
  for (const name of readdirSync(segmentsDir)) {
    if (name.endsWith(".mp4") && !kept.has(name)) rmSync(path.join(segmentsDir, name), { force: true });
  }
  if (stopRequested(workdir)) {
    ctx.stdout.write(`stopped by the STOP file before the join; rerun to continue\n`);
    return EXIT.ok;
  }

  const files = layout.map((entry) => (entry.kind === "episode" ? entry.file : segmentFiles[entry.id]));
  const list = path.join(buildDir, "join.ffconcat");
  writeFileSync(list, joinList(files));
  const final = path.join(workdir, ARTIFACTS.video);
  const partial = path.join(buildDir, "final.partial.mp4");
  const bodyPartial = branding ? path.join(buildDir, "body.partial.mp4") : partial;
  await exec(tools.ffmpeg, joinArgs(list, audioInputs(layout, {}), bodyPartial));
  let applied = null;
  if (branding) {
    applied = await wrapVideo({ tools, exec, workdir, bodyFile: bodyPartial, bodyFrames, branding, outFile: partial });
    applied.body_file = "build/body.mp4";
  } else {
    rmSync(final, { force: true });
    renameSync(partial, final);
  }
  const candidate = branding ? partial : final;

  const problems = [];
  const probe = JSON.parse((await exec(tools.ffprobe, probeArgs(candidate))).stdout);
  problems.push(...checkProbe(probe, { frames: total }));
  const loudness = parseEbur128((await exec(tools.ffmpeg, ebur128Args(candidate))).stderr);
  problems.push(...checkCompilationLoudness(loudness));
  const seconds = Math.round((Date.now() - started) / 1000);
  const placed = layout.filter((entry) => entry.kind === "episode").map(({ slug, start_frame, frames, sha256, body_sha256, branding_hash }) => ({ slug, start_frame, frames, sha256, ...(body_sha256 ? { body_sha256, branding_hash } : {}) }));
  const checks = {
    ok: problems.length === 0,
    compilation_hash: hash,
    visual_hash: visual,
    ...(applied ? { branding: applied } : {}),
    problems,
    metrics: { frames: total, loudness, episodes: placed },
    ffmpeg: tools.version,
    encoded_segments: encoded,
    seconds,
  };
  if (branding && !checks.ok) {
    atomicWrite(path.join(buildDir, "branding-failed-checks.json"), `${JSON.stringify(checks, null, 2)}\n`);
    recordStage(workdir, "compile", { ok: false, episodes: episodes.length, encoded_segments: encoded, seconds }, ctx.now());
    ctx.stdout.write(`${candidate}: failed checks; the previous compilation and its captions remain unchanged\n`);
    for (const problem of problems) ctx.stdout.write(`CHECK ${problem}\n`);
    return EXIT.lint;
  }
  if (!branding) atomicWrite(path.join(workdir, ARTIFACTS.checks), `${JSON.stringify(checks, null, 2)}\n`);

  // Captions and the timing records belong to the same replacement as the media. Prepare them
  // separately so a failed merge or rename cannot pair an old approved cut with new timings.
  const staged = branding ? mkdtempSync(path.join(buildDir, "compile-pending-")) : workdir;
  let captions;
  try {
    captions = mergeEpisodeCaptions({ layout, workBase, workdir: staged, hash, branding: applied });
    atomicWrite(path.join(staged, ARTIFACTS.captions), `${JSON.stringify(captions, null, 2)}\n`);
    const presented = presentationTimeline(compilationTimeline(layout, titles), applied);
    const finalChapters = chapters.map((chapter, index) => ({ ...chapter, start_frame: presented.chapters[index].start_frame, at: Math.floor(presented.chapters[index].start_frame / 30) }));
    atomicWrite(path.join(staged, ARTIFACTS.compilation), `${JSON.stringify({ compilation_hash: hash, visual_hash: visual, total_frames: total, ...(applied ? { body_total_frames: bodyFrames, branding: applied } : {}), layout, chapters: finalChapters, episodes: placed }, null, 2)}\n`);
    // The saved timeline remains the body, while the compilation manifest describes playback.
    atomicWrite(path.join(staged, ARTIFACTS.timeline), `${JSON.stringify({ ...compilationTimeline(layout, titles), compilation_hash: hash }, null, 2)}\n`);
    if (branding) {
      mkdirSync(path.dirname(path.join(workdir, ARTIFACTS.compilation)), { recursive: true });
      commitBrandedVideo({
        workdir, branding, finalPartial: partial, bodyPartial, checks, now: ctx.now(),
        ...(ctx.renameBranding ? { rename: ctx.renameBranding } : {}),
        artifacts: ["captions", ARTIFACTS.compilation, ARTIFACTS.timeline].map((name) => ({ source: path.join(staged, name), target: path.join(workdir, name) })),
      });
      rmSync(path.join(buildDir, "branding-failed-checks.json"), { force: true });
    }
  } finally {
    if (branding) rmSync(staged, { recursive: true, force: true });
  }
  recordStage(workdir, "compile", { ok: checks.ok, episodes: episodes.length, encoded_segments: encoded, captions: Object.keys(captions.locales), seconds }, ctx.now());

  ctx.stdout.write(`${final}: ${episodes.length} episodes, ${total} frames, ${loudness.integrated} LUFS, true peak ${loudness.truePeak} dBFS; ${encoded} of ${cards.length} cards encoded in ${seconds} s\n`);
  ctx.stdout.write(`captions: ${Object.keys(captions.locales).join(", ") || "none"}${Object.keys(captions.skipped).length ? `; skipped ${Object.entries(captions.skipped).map(([locale, missing]) => `${locale} (no current file in ${missing.join(", ")})`).join(", ")}` : ""}\n`);
  for (const problem of problems) ctx.stdout.write(`CHECK ${problem}\n`);
  if (!checks.ok) return EXIT.lint;
  ctx.stdout.write(`next: node tools/video/cli.mjs qa --slug ${doc.slug}\n`);
  return EXIT.ok;
}
