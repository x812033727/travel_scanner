// Where a video is in the pipeline, derived from the files that exist rather than from a log.
//
// Each stage writes its outputs with the hash of the inputs it was built from (the ARTIFACTS
// contract below), so "is this step done?" is answered by comparing hashes: a timeline built for
// an older script is not done, whatever state.json says. state.json only keeps the history of
// runs, for the handover.
import { existsSync, readdirSync } from "node:fs";
import path from "node:path";

import { approvalState } from "./approvals.mjs";
import { emptyLexicon } from "./lexicon.mjs";
import { lintVideo } from "./lint.mjs";
import { atomicWrite, contentPackFile, docDir, readJson, readText, stopRequested, videoFile } from "./paths.mjs";
import { LOCALES, NARRATION_LOCALE } from "./schema.mjs";
import { speechHash, visualHash } from "./timeline.mjs";

/**
 * Files each stage leaves in <VIDEO_WORKDIR>/<slug>/, and the hash fields they must carry.
 * The TTS, render, assemble and package stages (their own tickets) write to this contract.
 */
export const ARTIFACTS = {
  timeline: "timeline.json", // tts: buildTimeline() plus { speech_hash }
  narration: "narration.wav", // tts: the whole narration, frame-aligned
  audio: "audio", // tts: one WAV per line id
  frames: path.join("frames", "manifest.json"), // render: { visual_hash, states: [...] }
  contactSheet: "contact-sheet.png", // render
  video: "final.mp4", // assemble
  checks: "checks.json", // assemble: { ok, speech_hash, visual_hash, problems: [...] }
  captions: path.join("captions", "manifest.json"), // captions: { speech_hash, locales: { <locale>: {...} } }
  upload: path.join("upload", "metadata.json"), // package: { final_sha256, ... }
  state: "state.json",
};

/**
 * Everything lint and status need about one video. The shared dictionary and the other videos
 * are found one level above the video's directory: docs/videos/ for real videos, the fixtures
 * directory for the tests' examples.
 */
export function loadProject({ slug, file, root }) {
  const source = file ? path.resolve(file) : videoFile(slug, root);
  const doc = readJson(source);
  const dir = path.dirname(source);
  const translations = {};
  for (const locale of LOCALES.filter((each) => each !== NARRATION_LOCALE)) {
    const translation = readJson(path.join(dir, "i18n", `${locale}.json`), null);
    if (translation) translations[locale] = translation;
  }
  const shelf = path.dirname(dir);
  const others = [];
  if (existsSync(shelf)) {
    for (const entry of readdirSync(shelf, { withFileTypes: true })) {
      const other = path.join(shelf, entry.name, "video.json");
      if (!entry.isDirectory() || path.resolve(other) === source || !existsSync(other)) continue;
      try {
        others.push({ slug: entry.name, doc: readJson(other) });
      } catch {
        // A broken neighbour is its own lint's problem, not this video's.
      }
    }
  }
  return {
    doc,
    file: source,
    dir,
    brief: readText(path.join(dir, "brief.md")),
    lexicon: readJson(path.join(shelf, "lexicon.json"), emptyLexicon()),
    pack: doc.source_guide ? readJson(contentPackFile(doc.source_guide, root), null) : undefined,
    translations,
    others,
  };
}

export function lintProject(project) {
  return lintVideo(project.doc, project);
}

/** Append a run to state.json: which stage ran, when, and whatever it wants the next person to know. */
export function recordStage(workdir, stage, info = {}, now = new Date()) {
  const file = path.join(workdir, ARTIFACTS.state);
  const state = readJson(file, { runs: [] });
  state.runs.push({ stage, at: now.toISOString(), ...info });
  atomicWrite(file, `${JSON.stringify(state, null, 2)}\n`);
}

const cli = (command, slug, extra = "") => `node tools/video/cli.mjs ${command} --slug ${slug}${extra ? ` ${extra}` : ""}`;

function describe(state) {
  return { approved: "approved", stale: "changed since it was approved", missing: "not approved yet", absent: "nothing to approve yet" }[state.status];
}

/** The pipeline checklist for one video and the next command to run. */
export async function pipelineStatus({ slug, root, workdir }) {
  const dir = docDir(slug, root);
  const read = (name) => readJson(path.join(workdir, name), null);
  const project = existsSync(videoFile(slug, root)) ? loadProject({ slug, root }) : null;
  const lint = project ? lintProject(project) : null;
  const doc = project?.doc;
  const outline = await approvalState({ gate: "outline", docDir: dir, workdir });
  const audio = await approvalState({ gate: "audio", docDir: dir, workdir });
  const final = await approvalState({ gate: "final", docDir: dir, workdir });
  const timeline = read(ARTIFACTS.timeline);
  const frames = read(ARTIFACTS.frames);
  const checks = read(ARTIFACTS.checks);
  const captions = read(ARTIFACTS.captions);
  const upload = read(ARTIFACTS.upload);
  const speech = lint && !lint.errors.length ? speechHash(doc, project.lexicon) : null;
  const visual = lint && !lint.errors.length ? visualHash(doc) : null;

  const steps = [
    { id: "brief", done: existsSync(path.join(dir, "brief.md")), todo: `the planner agent writes docs/videos/${slug}/brief.md` },
    {
      id: "outline approved",
      done: outline.status === "approved",
      note: describe(outline),
      todo: `ask the owner to choose the outline (a question with options), then ${cli("approve", slug, "--gate outline")}`,
    },
    {
      id: "script passes lint",
      done: Boolean(lint) && lint.errors.length === 0,
      note: lint ? `${lint.errors.length} errors, ${lint.warnings.length} warnings` : "no video.json",
      todo: lint ? cli("lint", slug) : `the writer agent drafts docs/videos/${slug}/video.json`,
    },
    { id: "fact-checked", done: existsSync(path.join(dir, "verify-1.md")), todo: "a different agent fact-checks and writes verify-1.md" },
    {
      id: "narration synthesized",
      done: Boolean(speech) && timeline?.speech_hash === speech,
      note: timeline && timeline.speech_hash !== speech ? "timeline.json was built for an older script" : undefined,
      todo: cli("tts", slug),
    },
    {
      id: "narration approved",
      done: audio.status === "approved",
      note: describe(audio),
      todo: `${cli("review", slug)}; the owner listens and flags lines; then ${cli("approve", slug, "--gate audio")}`,
    },
    { id: "frames rendered", done: Boolean(visual) && frames?.visual_hash === visual, todo: cli("render", slug) },
    {
      id: "video assembled",
      done: Boolean(checks?.ok) && checks.speech_hash === speech && checks.visual_hash === visual && existsSync(path.join(workdir, ARTIFACTS.video)),
      note: checks && !checks.ok ? `checks failed: ${(checks.problems ?? []).join("; ")}` : undefined,
      todo: cli("assemble", slug),
    },
    { id: "captions written", done: Boolean(speech) && captions?.speech_hash === speech, todo: cli("captions", slug) },
    {
      id: "final video approved",
      done: final.status === "approved",
      note: describe(final),
      todo: `the owner watches review/final.html; then ${cli("approve", slug, "--gate final")}`,
    },
    { id: "upload package", done: Boolean(upload) && upload.final_sha256 === final.sha256, todo: cli("package", slug) },
    {
      id: "on YouTube",
      done: Boolean(doc?.youtube?.video_id),
      todo: `the owner uploads final.mp4 in YouTube Studio as Private; then ${cli("youtube-sync", slug, "--video-id <id> --dry-run")}`,
    },
  ];
  const next = steps.find((step) => !step.done) ?? null;
  return { steps, next, stop: stopRequested(workdir), lint };
}
