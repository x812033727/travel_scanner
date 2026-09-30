// A compilation's sandbox for the tests: a series' episodes as their pipelines leave them
// (approved cuts, checks, timelines, captions) beside the compilation project with its cards
// rendered, and an ffmpeg that writes what it is asked for without encoding anything.
// Not a test file itself: compile, state, qa, package and review tests all build on it.
import { createHash, randomBytes } from "node:crypto";
import { mkdirSync, rmSync, writeFileSync } from "node:fs";
import path from "node:path";

import { compilationDocument, THUMB_SHOT, THUMB_SOURCE } from "../core/compilation.mjs";
import { toSrt } from "../core/captions.mjs";
import { sandbox } from "../core/fixtures/load.mjs";
import { atomicWrite } from "../core/paths.mjs";
import { LOCALES } from "../core/schema.mjs";
import { visualHash } from "../core/timeline.mjs";
import { jpegBytes } from "../qa/test-images.mjs";

export const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
export const SERIES = "wuxia";
export const EPISODES = ["wuxia-ep-1", "wuxia-ep-2", "wuxia-ep-3"];
export const TITLES = { "wuxia-ep-1": "初入山門", "wuxia-ep-2": "夜探藏經閣", "wuxia-ep-3": "劍冢之約" };
export const EPISODE_FRAMES = { "wuxia-ep-1": 4321, "wuxia-ep-2": 3900, "wuxia-ep-3": 5010 };
export const VOICE = { provider: "gemini", name: "Sulafat", style: "沉穩的說書人語氣" };

/** One episode's work directory as its pipeline cleared it. `captions` lists the locales with a file. */
export function writeEpisode(workBase, slug, { frames = EPISODE_FRAMES[slug] ?? 3600, captions = ["zh-TW", "en"], approved = true, checksOk = true, cutBytes = 2048, branding = null } = {}) {
  const dir = path.join(workBase, slug);
  mkdirSync(path.join(dir, "captions"), { recursive: true });
  const cut = randomBytes(cutBytes);
  writeFileSync(path.join(dir, "final.mp4"), cut);
  const hash = sha(cut);
  if (approved) atomicWrite(path.join(dir, "approvals.json"), JSON.stringify({ approvals: [{ gate: "final", file: "final.mp4", sha256: hash, approved_at: "2026-09-27T00:00:00Z", note: "" }] }));
  else rmSync(path.join(dir, "approvals.json"), { force: true });
  let applied = null;
  if (branding) {
    const body = randomBytes(cutBytes);
    mkdirSync(path.join(dir, "build"), { recursive: true });
    writeFileSync(path.join(dir, "build", "body.mp4"), body);
    applied = { ...branding, body_frames: frames, body_file: "build/body.mp4", body_sha256: sha(body) };
  }
  atomicWrite(path.join(dir, "checks.json"), JSON.stringify({ ok: checksOk, problems: checksOk ? [] : ["1 frame short"], metrics: { frames: frames + (applied ? applied.intro_frames + applied.outro_frames : 0) }, ...(applied ? { branding: applied } : {}) }));
  atomicWrite(path.join(dir, "timeline.json"), JSON.stringify({ fps: 30, sample_rate: 48000, total_frames: frames, scenes: [], lines: [], chapters: [], speech_hash: "s"}));
  for (const locale of captions) {
    // Two cues per episode, the second ending well inside the episode's length.
    const introMs = applied ? (applied.intro_frames / 30) * 1000 : 0;
    const cues = [{ start_ms: introMs, end_ms: introMs + 1500, text: `${locale} ${slug} 1` }, { start_ms: introMs + 2000, end_ms: introMs + 3200, text: `${locale} ${slug} 2` }];
    writeFileSync(path.join(dir, "captions", `${locale}.srt`), toSrt(cues));
  }
  if (applied) atomicWrite(path.join(dir, "captions", "manifest.json"), JSON.stringify({ speech_hash: "s", branding_hash: applied.hash, locales: Object.fromEntries(captions.map((locale) => [locale, { cues: 2, problems: [], timing: "narration" }])) }));
  return { dir, sha256: hash, frames, bytes: cutBytes, ...(applied ? { body_sha256: applied.body_sha256, branding_hash: applied.hash } : {}) };
}

/**
 * The compilation project in a throwaway repository, its episodes cleared beside it, its cards
 * rendered (a manifest and a still per card) and its thumbnail drawn. Returns the sandbox with
 * `doc`, `episodes` ({ slug: { sha256, frames } }) and the work base.
 */
export function compilationSandbox({ episodes = EPISODES, titles = TITLES, numbers = {}, chapterCards = true, outro = true, captions, youtube = {}, rendered = true, planned = true } = {}) {
  const slug = `${SERIES}-full`;
  const box = sandbox(slug, "drama");
  const built = compilationDocument({
    series: SERIES,
    episodes: episodes.map((episode, index) => ({ slug: episode, number: numbers[episode] ?? index + 1, title: titles[episode] })),
    voice: VOICE,
    chapterCards,
    outro,
  });
  // The planner's work, when the test starts past it: the title, description, tags and thumbnail.
  const doc = planned
    ? { ...built, youtube: { ...built.youtube, title: "仙門風雲 全集：第一部完整版", description: "第一部的每一集，接連著看。", tags: ["仙俠", "AI漫劇"], ...youtube }, thumbnail: { template: "thumb", data: { headline: "仙門風雲 全集", tag: "第一部", shot: THUMB_SHOT } } }
    : { ...built, youtube: { ...built.youtube, ...youtube } };
  writeFileSync(path.join(box.dir, "video.json"), `${JSON.stringify(doc, null, 2)}\n`);
  const cuts = {};
  for (const episode of episodes) cuts[episode] = writeEpisode(box.work, episode, captions?.[episode] ? { captions: captions[episode] } : {});
  mkdirSync(path.join(box.workdir, "keyframes"), { recursive: true });
  if (planned) {
    const source = Buffer.from("keyframe");
    writeFileSync(path.join(box.workdir, THUMB_SOURCE), source);
    atomicWrite(path.join(box.workdir, "keyframes", "manifest.json"), JSON.stringify({ shots: { [THUMB_SHOT]: { file: THUMB_SOURCE, sha256: sha(source), from: episodes[0] } } }));
  }
  if (rendered) renderCards(box, doc);
  return { ...box, doc, episodes: cuts };
}

/** frames/manifest.json and a still per card, as render leaves them, plus the thumbnail. */
export function renderCards(box, doc) {
  mkdirSync(path.join(box.workdir, "frames"), { recursive: true });
  const cache = {};
  const scenes = doc.scenes.map((scene) => {
    // Keyed by what the card shows, as render keys its frames, so a new title is a new still.
    const key = sha(JSON.stringify([scene.id, scene.chapter ?? null, scene.data])).slice(0, 16);
    writeFileSync(path.join(box.workdir, "frames", `${key}.png`), Buffer.from(scene.id));
    cache[key] = { transition: 0, problems: [] };
    return { id: scene.id, kind: "stills", states: [{ reveal: 0, still: `frames/${key}.png`, transition: [] }] };
  });
  atomicWrite(path.join(box.workdir, "frames", "manifest.json"), JSON.stringify({ visual_hash: visualHash(doc), theme_hash: "t", fps: 30, size: { width: 1920, height: 1080 }, scenes, thumbnail: "thumbnail.jpg" }));
  atomicWrite(path.join(box.workdir, "frames", "cache.json"), JSON.stringify(cache));
  writeFileSync(path.join(box.workdir, "thumbnail.jpg"), jpegBytes(1280, 720, 4000));
}

/**
 * An ffmpeg and ffprobe that write the file they are asked for and answer the probes with a
 * well-formed result for `total` frames. `calls` records every invocation.
 */
export function fakeFfmpeg({ total, loudness = -14.4, peak = -1.6, framesByFile = {} } = {}) {
  const calls = [];
  const runTool = async (file, args) => {
    calls.push({ tool: path.basename(file), args });
    if (path.basename(file) === "ffprobe") {
      const frames = framesByFile[args.at(-1)] ?? total ?? 0;
      const streams = [
        { codec_type: "video", codec_name: "h264", profile: "High", width: 1920, height: 1080, r_frame_rate: "30/1", pix_fmt: "yuv420p", color_space: "bt709", color_primaries: "bt709", color_transfer: "bt709", nb_read_packets: String(frames) },
        { codec_type: "audio", codec_name: "aac", sample_rate: "48000", channels: 2, duration: String(frames / 30 + 0.02) },
      ];
      return { stdout: JSON.stringify({ streams }), stderr: "" };
    }
    if (args.includes("ebur128=peak=true")) return { stdout: "", stderr: `... Summary:\n\n  Integrated loudness:\n    I:         ${loudness} LUFS\n\n  True peak:\n    Peak:      ${peak} dBFS\n` };
    const out = args.at(-1);
    writeFileSync(out, Buffer.concat([Buffer.from(`fake ${path.basename(out)} `), randomBytes(16)]));
    return { stdout: "", stderr: "" };
  };
  return { calls, runTool, tools: { ffmpeg: "ffmpeg", ffprobe: "ffprobe", version: "ffmpeg fake" } };
}

/** A CLI context on the sandbox: captured output, the fake tools, plenty of disk. */
export function compileContext(box, fake, extra = {}) {
  const out = { stdout: "", stderr: "" };
  return {
    out,
    ctx: {
      root: box.root,
      env: { VIDEO_WORKDIR: box.work },
      home: box.base,
      tools: fake.tools,
      runTool: fake.runTool,
      freeBytes: () => 100 * 1024 ** 3,
      stdout: { write: (text) => (out.stdout += text) },
      stderr: { write: (text) => (out.stderr += text) },
      now: () => new Date("2026-09-27T05:00:00Z"),
      sleep: async () => {},
      ...extra,
    },
  };
}

export const OTHER_LOCALES = LOCALES.filter((locale) => locale !== "zh-TW");

/** Every locale's translation of the compilation, complete, written beside video.json. */
export function writeTranslations(box, doc) {
  mkdirSync(path.join(box.dir, "i18n"), { recursive: true });
  for (const locale of OTHER_LOCALES) {
    // Chapters key on the episode slugs, as the worker writes them (docs/videos/BINGE.md).
    const chapters = Object.fromEntries(doc.compilation.episodes.map((slug) => [slug, `${locale} ${slug}`]));
    atomicWrite(path.join(box.dir, "i18n", `${locale}.json`), `${JSON.stringify({ title: `${locale} title`, description: `${locale} description`, tags: [`${locale} tag`], chapters, lines: {} }, null, 2)}\n`);
  }
}
