// Where a video is in the pipeline, derived from the files that exist rather than from a log.
//
// Each stage writes its outputs with the hash of the inputs it was built from (the ARTIFACTS
// contract below), so "is this step done?" is answered by comparing hashes: a timeline built for
// an older script is not done, whatever state.json says. state.json only keeps the history of
// runs, for the handover.
import { existsSync, readdirSync } from "node:fs";
import path from "node:path";

import { approvalState } from "./approvals.mjs";
import { burnIn, isDrama, lookHash, mixHash, subtitlesHash } from "./drama.mjs";
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
  // render: { visual_hash, states: [...] }; burning subtitles in adds { speech_hash, subtitles_hash, subtitles }
  frames: path.join("frames", "manifest.json"),
  contactSheet: "contact-sheet.png", // render
  video: "final.mp4", // assemble
  // assemble: { ok, speech_hash, visual_hash, problems: [...] }; a drama adds look_hash, clips_hash, subtitles_hash, mix_hash
  checks: "checks.json",
  captions: path.join("captions", "manifest.json"), // captions: { speech_hash, locales: { <locale>: {...} } }
  upload: path.join("upload", "metadata.json"), // package: { final_sha256, ... }
  state: "state.json",
  // The drama format's media stages (docs/videos/DRAMA.md).
  characters: path.join("characters", "manifest.json"), // look: { look_hash, characters: { <id>: { candidates: [...], suggested } } }
  characterChoice: path.join("characters", "choice.json"), // review-pull or look --choose: { look_hash, chosen: { <id>: n } }
  keyframes: path.join("keyframes", "manifest.json"), // keyframes: { look_hash, visual_hash, shots: { <id>: { file, sha256, needs_review? } } }
  clips: path.join("clips", "manifest.json"), // clips: { speech_hash, visual_hash, look_hash, clips_hash, shots: { <id>: { file, sha256, needs_review? } } }
  music: path.join("music", "manifest.json"), // music: { mix_hash, file, sha256 }
  mediaCache: path.join("media", "cache.json"), // media client: request key -> file
  mediaJobs: path.join("media", "jobs.json"), // media client: jobs still running on the server, resumed on the next run
  mediaLedger: path.join("media", "ledger.json"), // media client: what each generation cost
};

/** The pipeline steps of a slides video, in order; `pipelineStatus` reports them in this order. */
export const SLIDES_STEPS = [
  "brief",
  "outline approved",
  "script passes lint",
  "fact-checked",
  "narration synthesized",
  "narration approved",
  "frames rendered",
  "video assembled",
  "captions written",
  "final video approved",
  "upload package",
  "on YouTube",
];

/**
 * A drama's steps. The look comes before the narration so the owner can drop a concept before
 * anything else is paid for; render (local, cheap, fails on a missing glyph) comes before clips,
 * the most expensive stage; music is skipped when the script has none.
 */
export const DRAMA_STEPS = [
  "brief",
  "outline approved",
  "script passes lint",
  "fact-checked",
  "look generated",
  "look approved",
  "narration synthesized",
  "narration approved",
  "keyframes drawn",
  "storyboard approved",
  "frames rendered",
  "clips generated",
  "music generated",
  "video assembled",
  "captions written",
  "final video approved",
  "upload package",
  "on YouTube",
];

export function stepsFor(doc) {
  if (!isDrama(doc)) return SLIDES_STEPS;
  return doc.music ? DRAMA_STEPS : DRAMA_STEPS.filter((id) => id !== "music generated");
}

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

/**
 * Which candidate sheet each character uses: the owner's choice when it was made for these
 * sheets, else the sheet the judge suggested. Null when a character has neither.
 */
export function lookChosen(manifest, choice, look) {
  if (!manifest || manifest.look_hash !== look) return null;
  const chosen = choice?.look_hash === look ? choice.chosen ?? {} : {};
  const result = {};
  for (const [id, character] of Object.entries(manifest.characters ?? {})) {
    const pick = chosen[id] ?? character?.suggested ?? null;
    if (pick === null || pick === undefined) return null;
    result[id] = pick;
  }
  return result;
}

const needsReview = (manifest) => Object.values(manifest?.shots ?? {}).some((shot) => shot?.needs_review);

/** The pipeline checklist for one video and the next command to run. */
export async function pipelineStatus({ slug, root, workdir }) {
  const dir = docDir(slug, root);
  const read = (name) => readJson(path.join(workdir, name), null);
  const project = existsSync(videoFile(slug, root)) ? loadProject({ slug, root }) : null;
  const lint = project ? lintProject(project) : null;
  const doc = project?.doc;
  const drama = isDrama(doc);
  const gate = (name) => approvalState({ gate: name, docDir: dir, workdir });
  const outline = await gate("outline");
  const audio = await gate("audio");
  const final = await gate("final");
  const look = drama ? await gate("look") : null;
  const storyboard = drama ? await gate("storyboard") : null;
  const timeline = read(ARTIFACTS.timeline);
  const frames = read(ARTIFACTS.frames);
  const checks = read(ARTIFACTS.checks);
  const captions = read(ARTIFACTS.captions);
  const upload = read(ARTIFACTS.upload);
  const characters = drama ? read(ARTIFACTS.characters) : null;
  const keyframes = drama ? read(ARTIFACTS.keyframes) : null;
  const clips = drama ? read(ARTIFACTS.clips) : null;
  const music = drama ? read(ARTIFACTS.music) : null;
  const valid = Boolean(lint) && lint.errors.length === 0;
  const speech = valid ? speechHash(doc, project.lexicon) : null;
  const visual = valid ? visualHash(doc) : null;
  const lookNow = valid && drama ? lookHash(doc) : null;
  const subtitles = valid && drama ? subtitlesHash(doc) : null;
  const mix = valid && drama ? mixHash(doc) : null;
  const chosen = drama ? lookChosen(characters, read(ARTIFACTS.characterChoice), lookNow) : null;

  const framesDone = Boolean(visual) && frames?.visual_hash === visual && (!drama || !burnIn(doc) || (frames.speech_hash === speech && frames.subtitles_hash === subtitles));
  const assembledDrama = !drama || (checks?.look_hash === lookNow && checks.clips_hash === clips?.clips_hash && checks.subtitles_hash === subtitles && checks.mix_hash === mix);

  const definitions = {
    brief: { done: existsSync(path.join(dir, "brief.md")), todo: `the planner agent writes docs/videos/${slug}/brief.md` },
    "outline approved": {
      done: outline.status === "approved",
      note: describe(outline),
      todo: `ask the owner to choose the outline (a question with options), then ${cli("approve", slug, "--gate outline")}`,
    },
    "script passes lint": {
      done: valid,
      note: lint ? `${lint.errors.length} errors, ${lint.warnings.length} warnings` : "no video.json",
      todo: lint ? cli("lint", slug) : `the writer agent drafts docs/videos/${slug}/video.json`,
    },
    "fact-checked": { done: existsSync(path.join(dir, "verify-1.md")), todo: drama ? "a different agent checks continuity and the story bible and writes verify-1.md" : "a different agent fact-checks and writes verify-1.md" },
    "look generated": {
      done: Boolean(lookNow) && characters?.look_hash === lookNow,
      note: characters && characters.look_hash !== lookNow ? "characters/manifest.json was made for an older look" : undefined,
      todo: cli("look", slug),
    },
    "look approved": {
      done: look?.status === "approved" && chosen !== null,
      note: look ? (look.status === "approved" && chosen === null ? "a character has no chosen sheet" : describe(look)) : undefined,
      todo: `${cli("review-push", slug, "--gate look")}; the owner picks a sheet per character on /admin/videos; then ${cli("review-pull", slug)}`,
    },
    "narration synthesized": {
      done: Boolean(speech) && timeline?.speech_hash === speech,
      note: timeline && timeline.speech_hash !== speech ? "timeline.json was built for an older script" : undefined,
      todo: cli("tts", slug),
    },
    "narration approved": {
      done: audio.status === "approved",
      note: describe(audio),
      todo: `${cli("review", slug)}; the owner listens and flags lines; then ${cli("approve", slug, "--gate audio")}`,
    },
    "keyframes drawn": {
      done: Boolean(lookNow) && keyframes?.look_hash === lookNow && keyframes.visual_hash === visual && !needsReview(keyframes),
      note: keyframes && needsReview(keyframes) ? "some shots need a prompt fix (needs_review in keyframes/manifest.json)" : undefined,
      todo: cli("keyframes", slug),
    },
    "storyboard approved": {
      done: storyboard?.status === "approved",
      note: storyboard ? describe(storyboard) : undefined,
      todo: `${cli("review-push", slug, "--gate storyboard")}; the owner looks at the keyframes on /admin/videos; then ${cli("review-pull", slug)}`,
    },
    "frames rendered": { done: framesDone, todo: cli("render", slug) },
    "clips generated": {
      done: Boolean(speech) && clips?.speech_hash === speech && clips.visual_hash === visual && clips.look_hash === lookNow && !needsReview(clips),
      note: clips && needsReview(clips) ? "some shots failed the clip checks (needs_review in clips/manifest.json)" : undefined,
      todo: cli("clips", slug),
    },
    "music generated": { done: Boolean(mix) && music?.mix_hash === mix, todo: cli("music", slug) },
    "video assembled": {
      done: Boolean(checks?.ok) && checks.speech_hash === speech && checks.visual_hash === visual && assembledDrama && existsSync(path.join(workdir, ARTIFACTS.video)),
      note: checks && !checks.ok ? `checks failed: ${(checks.problems ?? []).join("; ")}` : undefined,
      todo: cli("assemble", slug),
    },
    "captions written": { done: Boolean(speech) && captions?.speech_hash === speech, todo: cli("captions", slug) },
    "final video approved": {
      done: final.status === "approved",
      note: describe(final),
      todo: `the owner watches review/final.html; then ${cli("approve", slug, "--gate final")}`,
    },
    "upload package": { done: Boolean(upload) && upload.final_sha256 === final.sha256, todo: cli("package", slug) },
    "on YouTube": {
      done: Boolean(doc?.youtube?.video_id),
      todo: `the owner uploads final.mp4 in YouTube Studio as Private; then ${cli("youtube-sync", slug, "--video-id <id> --dry-run")}`,
    },
  };
  const steps = stepsFor(doc).map((id) => ({ id, ...definitions[id] }));
  const next = steps.find((step) => !step.done) ?? null;
  return { steps, next, stop: stopRequested(workdir), lint };
}
