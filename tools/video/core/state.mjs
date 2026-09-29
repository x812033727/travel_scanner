// Where a video is in the pipeline, derived from the files that exist rather than from a log.
//
// Each stage writes its outputs with the hash of the inputs it was built from (the ARTIFACTS
// contract below), so "is this step done?" is answered by comparing hashes: a timeline built for
// an older script is not done, whatever state.json says. state.json only keeps the history of
// runs, for the handover.
import { existsSync, readdirSync } from "node:fs";
import path from "node:path";

import { approvalState, readApprovals } from "./approvals.mjs";
import { COMPILATION_HEADLINE_PLACEHOLDER, COMPILATION_STEPS, compilationChecksCurrent, isCompilation, lintCompilation, PLACEHOLDER_TITLE } from "./compilation.mjs";
import { burnIn, illustrated, isDrama, keyframesHash, lookHash, mixHash, picturesHash, resolveMusic, resolveSfx, sfxHash, subtitlesHash } from "./drama.mjs";
import { emptyLexicon } from "./lexicon.mjs";
import { lintVideo } from "./lint.mjs";
import { dubLocales, dubScript, speechLexicon, translationHash } from "../dubs/plan.mjs";
import { atomicWrite, contentPackFile, docDir, readJson, readText, stopRequested, videoFile } from "./paths.mjs";
import { LOCALES, narrationLocale } from "./schema.mjs";
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
  thumbnail: "thumbnail.jpg", // render
  video: "final.mp4", // assemble, or compile for a compilation
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
  // dub: one directory per locale (dubArtifacts) and the upload track beside them, dubs/<locale>.<format>
  dubs: "dubs",
  // compile (docs/videos/BINGE.md): { compilation_hash, visual_hash, total_frames, layout, chapters, episodes }
  compilation: path.join("compile", "manifest.json"),
};

/** The files one locale's dub leaves under <workdir>/dubs/ (docs/videos/DUBS.md). */
export function dubArtifacts(workdir, locale) {
  const dir = path.join(workdir, ARTIFACTS.dubs, locale);
  return {
    dir,
    audio: path.join(dir, "audio"), // one WAV per line id, plus <id>.x<tempo>.wav for sped-up takes
    cache: path.join(dir, "audio", "cache.json"), // { lines: { id: key }, stretched: { id: key@tempo } }
    narration: path.join(dir, "narration.wav"), // the whole track, frame-aligned, before loudness
    timeline: path.join(dir, "timeline.json"), // { speech_hash, translation_hash, total_frames, windows, lines }
    fit: path.join(dir, "fit.json"), // { rates, windows, over: [{ id, chars, max_chars }] }
    skipped: path.join(dir, "skipped.json"), // the worker gave up on this locale: { reason, at }
    track: (format) => path.join(workdir, ARTIFACTS.dubs, `${locale}.${format}`),
  };
}

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
 * An illustrated slides video's steps (docs/videos/ILLUSTRATED.md): the slides steps with the
 * pictures drawn and the storyboard approved once the narration is, and the music made once the
 * cards are rendered. `formatSteps` drops the music step when the script has none.
 */
export const ILLUSTRATED_STEPS = [
  "brief",
  "outline approved",
  "script passes lint",
  "fact-checked",
  "narration synthesized",
  "narration approved",
  "keyframes drawn",
  "storyboard approved",
  "frames rendered",
  "music generated",
  "video assembled",
  "captions written",
  "final video approved",
  "upload package",
  "on YouTube",
];

/**
 * A drama's steps. The look comes before the narration so the owner can drop a concept before
 * anything else is paid for; render (local, cheap, fails on a missing glyph) comes before clips,
 * the most expensive stage; music is skipped when the script has none, and the two look steps
 * when it has no characters (`narratorOnly`).
 */
export const DRAMA_STEPS = [
  "brief",
  "outline approved",
  "script passes lint",
  "fact-checked",
  "script approved",
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

/**
 * A series' compilation (docs/videos/BINGE.md) joins cuts the owner already approved, so it has
 * no narration, look or storyboard steps: the planned metadata and thumbnail, the cards, the
 * join, the translations, then the usual final, package and YouTube steps. The list lives in
 * compilation.mjs beside the document it describes; the worker reads it from either module.
 */
export { COMPILATION_STEPS };

/** The steps of the video's format, before `stepsFor` drops the look of a drama with no characters. */
function formatSteps(doc) {
  if (isCompilation(doc)) return COMPILATION_STEPS;
  if (illustrated(doc)) return ILLUSTRATED_STEPS.filter((id) => id !== "music generated" || doc.music);
  if (!isDrama(doc)) return SLIDES_STEPS;
  // Every drama has the script gate (docs/videos/DRAMA-FLOW.md, section 2): the owner reads the
  // screenplay, and may discuss it, before any image or clip is paid for. Music is skipped when
  // the script has none.
  return DRAMA_STEPS.filter((id) => id !== "music generated" || doc.music);
}

/** The two steps that draw and choose the cast's character sheets. */
export const LOOK_STEPS = ["look generated", "look approved"];

/**
 * Whether a drama is told by the narrator alone, as a brand story may be (docs/videos/STORY.md):
 * with no characters there is no sheet to draw or choose, so it has no look steps and its
 * keyframes are drawn from the look's style frames alone.
 */
export const narratorOnly = (doc) => isDrama(doc) && !isCompilation(doc) && !doc.characters?.length;

/** The steps `pipelineStatus` walks for this video, in order. */
export function stepsFor(doc) {
  const steps = formatSteps(doc);
  return narratorOnly(doc) ? steps.filter((id) => !LOOK_STEPS.includes(id)) : steps;
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
  for (const locale of LOCALES.filter((each) => each !== narrationLocale(doc))) {
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
    // An episode of a series: the cast as the setting book has it, and this episode's beats
    // (docs/videos/SERIES.md); the worker writes it when it starts the episode.
    series: readJson(path.join(dir, "series.json"), null),
    // The dictionary as this narration's voice may use it: an English narration drops the
    // Chinese-character aliases, like a dub does (docs/videos/DUBS.md).
    lexicon: speechLexicon(readJson(path.join(shelf, "lexicon.json"), emptyLexicon()), narrationLocale(doc)),
    pack: doc.source_guide ? readJson(contentPackFile(doc.source_guide, root), null) : undefined,
    translations,
    others,
  };
}

export function lintProject(project) {
  // A compilation narrates nothing: the brief, lexicon and shot rules do not apply to it.
  if (isCompilation(project.doc)) return lintCompilation(project.doc, project);
  return lintVideo(project.doc, project);
}

/**
 * The cuts a compilation joins, as approved: each episode's last `final` approval in its own
 * work directory beside the compilation's. An episode without one has `sha256: null`, and the
 * compilation cannot be current until it is cleared.
 */
export function approvedEpisodes(doc, workBase) {
  return doc.compilation.episodes.map((slug) => {
    const entry = readApprovals(path.join(workBase, slug)).approvals.filter((each) => each.gate === "final").at(-1) ?? null;
    return { slug, sha256: entry?.sha256 ?? null };
  });
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

/**
 * Each dub locale's state: "current" (a track made from this script and this translation),
 * "stale", "over" (the last run found windows that do not fit; no track), "skipped" (the worker
 * gave up, with its reason) or "missing". A video with no dubs is all "missing".
 */
export function dubsStatus(project, workdir, speech) {
  const result = {};
  for (const locale of dubLocales(project?.doc)) {
    const files = dubArtifacts(workdir, locale);
    const skipped = readJson(files.skipped, null);
    const timeline = readJson(files.timeline, null);
    const fit = readJson(files.fit, null);
    if (skipped) {
      result[locale] = { status: "skipped", note: skipped.reason ?? "" };
      continue;
    }
    const hash = project && speech ? translationHash(dubScript(project.doc, project.translations[locale], locale).doc) : null;
    if (timeline && existsSync(files.track(timeline.format))) {
      // A dub also carries the script's music bed and the cut's effects (docs/videos/ILLUSTRATED.md):
      // one made before either existed, or for another bed or set, is stale like an older script.
      const doc = project?.doc ?? null;
      const soundCurrent = !doc || ((timeline.mix_hash ?? null) === (resolveMusic(doc) ? mixHash(doc) : null) && (timeline.sfx_hash ?? null) === (resolveSfx(doc) ? sfxHash(doc) : null));
      const current = timeline.speech_hash === speech && timeline.translation_hash === hash && soundCurrent;
      result[locale] = { status: current ? "current" : "stale", note: current ? timeline.file : soundCurrent ? "made from an older script or translation" : "made without the video's music or sound effects; run dub again" };
      continue;
    }
    if (fit?.over?.length && fit.speech_hash === speech && fit.translation_hash === hash) {
      result[locale] = { status: "over", note: `${fit.over.length} lines to shorten (dubs/${locale}/fit.json)` };
      continue;
    }
    result[locale] = { status: "missing", note: "" };
  }
  return result;
}

/** The pipeline checklist for one video and the next command to run. */
export async function pipelineStatus({ slug, root, workdir }) {
  const dir = docDir(slug, root);
  const read = (name) => readJson(path.join(workdir, name), null);
  const project = existsSync(videoFile(slug, root)) ? loadProject({ slug, root }) : null;
  const lint = project ? lintProject(project) : null;
  const doc = project?.doc;
  const compilation = isCompilation(doc);
  // A compilation is a drama for the disclosure and the steps, not for the media stages here.
  const drama = isDrama(doc) && !compilation;
  // Illustrated slides (docs/videos/ILLUSTRATED.md) draw pictures and a storyboard like a drama,
  // and keep the slides gates otherwise.
  const pictures = drama || (illustrated(doc) && !compilation);
  // A narrator-only drama has no cast: no look gate to ask about, no character sheets to read.
  const cast = drama && !narratorOnly(doc);
  const gate = (name) => approvalState({ gate: name, docDir: dir, workdir });
  const outline = await gate("outline");
  const audio = await gate("audio");
  const final = await gate("final");
  const look = cast ? await gate("look") : null;
  const storyboard = pictures ? await gate("storyboard") : null;
  const script = drama ? await gate("script") : null;
  const timeline = read(ARTIFACTS.timeline);
  const frames = read(ARTIFACTS.frames);
  const checks = read(ARTIFACTS.checks);
  const captions = read(ARTIFACTS.captions);
  const upload = read(ARTIFACTS.upload);
  const characters = cast ? read(ARTIFACTS.characters) : null;
  const keyframes = pictures ? read(ARTIFACTS.keyframes) : null;
  const clips = drama ? read(ARTIFACTS.clips) : null;
  const music = (drama || doc?.music) && !compilation ? read(ARTIFACTS.music) : null;
  const valid = Boolean(lint) && lint.errors.length === 0;
  const speech = valid && !compilation ? speechHash(doc, project.lexicon) : null;
  const visual = valid ? visualHash(doc) : null;
  const lookNow = valid && pictures ? lookHash(doc) : null;
  const subtitles = valid && drama ? subtitlesHash(doc) : null;
  // A drama's checks.json always carries a mix hash (of no music, when it has none); slides carry one only with music.
  const mix = valid && (drama || doc.music) && !compilation ? mixHash(doc) : null;
  const chosen = cast ? lookChosen(characters, read(ARTIFACTS.characterChoice), lookNow) : null;

  const framesDone = Boolean(visual) && frames?.visual_hash === visual && (!drama || !burnIn(doc) || (frames.speech_hash === speech && frames.subtitles_hash === subtitles));
  // A drama's keyframes are bound to the whole picture; illustrated slides bind theirs to the shots
  // alone, so a card edit does not have every picture judged again.
  const keyframesDone = Boolean(lookNow) && keyframes?.look_hash === lookNow && (drama ? keyframes.visual_hash === visual : keyframes.pictures_hash === picturesHash(doc)) && !needsReview(keyframes);
  const assembledDrama = !drama || (checks?.look_hash === lookNow && checks.clips_hash === clips?.clips_hash && checks.subtitles_hash === subtitles && checks.mix_hash === mix);
  const assembledIllustrated = !(pictures && !drama) || (checks?.look_hash === lookNow && checks.pictures_hash === keyframesHash(doc, keyframes));
  const assembledSound = compilation || ((!doc?.music || checks?.mix_hash === mix) && (!doc?.sfx || checks?.sfx_hash === sfxHash(doc)));
  const assembledMedia = assembledDrama && assembledIllustrated && assembledSound;

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
    "script approved": {
      done: script?.status === "approved",
      note: script ? describe(script) : undefined,
      todo: `${cli("script", slug)}, then ${cli("review-push", slug, "--gate script")}; the owner reads the screenplay on /admin/videos; then ${cli("review-pull", slug)}`,
    },
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
      done: keyframesDone,
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
      done: Boolean(checks?.ok) && checks.speech_hash === speech && checks.visual_hash === visual && assembledMedia && existsSync(path.join(workdir, ARTIFACTS.video)),
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
  if (compilation) Object.assign(definitions, compilationDefinitions({ slug, workdir, doc, project, valid, lint, visual, read, frames, checks, captions }));
  const steps = stepsFor(doc).map((id) => ({ id, ...definitions[id] }));
  const next = steps.find((step) => !step.done) ?? null;
  const dubs = drama || compilation ? {} : dubsStatus(project, workdir, speech);
  return { steps, next, stop: stopRequested(workdir), lint, dubs };
}

const isText = (value) => typeof value === "string" && value.trim().length > 0;

/** A compilation's locale translation is complete when the four YouTube fields are there. */
export function translationComplete(translation) {
  return isText(translation?.title) && isText(translation?.description) && Array.isArray(translation?.tags) && translation.tags.length > 0 && translation?.chapters !== null && typeof translation?.chapters === "object";
}

/**
 * The compilation's own steps (docs/videos/BINGE.md). The episodes' work directories sit beside
 * the compilation's, so their approvals say which cuts are current; the final, package and
 * YouTube steps are the shared definitions.
 */
function compilationDefinitions({ slug, workdir, doc, project, valid, lint, visual, read, frames, checks, captions }) {
  const episodes = valid ? approvedEpisodes(doc, path.dirname(workdir)) : [];
  const uncleared = episodes.filter((episode) => !episode.sha256).map((episode) => episode.slug);
  const keyframes = read(ARTIFACTS.keyframes);
  const planned = valid && isText(doc.youtube.title) && doc.youtube.title !== PLACEHOLDER_TITLE && Boolean(doc.thumbnail) && doc.thumbnail.data?.headline !== COMPILATION_HEADLINE_PLACEHOLDER;
  // The thumbnail draws on an episode keyframe when the planner picked one; a compilation whose
  // episodes left no keyframe to pick draws on the theme alone and needs no source.
  const thumbSource = doc?.thumbnail?.data?.shot === undefined || Boolean(keyframes?.shots?.thumb?.file);
  const compiled = valid && compilationChecksCurrent(doc, checks, episodes);
  const locales = LOCALES.filter((locale) => locale !== narrationLocale(doc));
  const untranslated = locales.filter((locale) => !translationComplete(project.translations[locale]));
  return {
    "metadata planned": {
      done: planned && thumbSource,
      note: !valid ? `video.json has ${lint?.errors.length ?? "?"} lint errors` : !planned ? "the title or the thumbnail headline is still the placeholder, or there is no thumbnail" : !thumbSource ? "keyframes/manifest.json has no shots.thumb: the thumbnail's background is not chosen" : undefined,
      todo: `the worker plans the compilation's title, description and thumbnail on an episode keyframe (docs/videos/BINGE.md), then ${cli("lint", slug)}`,
    },
    "cards rendered": {
      done: Boolean(visual) && frames?.visual_hash === visual && existsSync(path.join(workdir, ARTIFACTS.thumbnail)),
      note: frames && frames.visual_hash !== visual ? "frames/manifest.json was rendered for older cards" : undefined,
      todo: cli("render", slug),
    },
    "video compiled": {
      done: compiled && captions?.compilation_hash === checks.compilation_hash && existsSync(path.join(workdir, ARTIFACTS.video)),
      note: uncleared.length ? `episodes not cleared for upload: ${uncleared.join(", ")}` : checks && !checks.ok ? `checks failed: ${(checks.problems ?? []).join("; ")}` : checks && !compiled ? "checks.json was written for other cuts or cards" : undefined,
      todo: cli("compile", slug),
    },
    "metadata translated": {
      done: valid && untranslated.length === 0,
      note: untranslated.length && untranslated.length < locales.length ? `missing or incomplete: ${untranslated.join(", ")}` : undefined,
      todo: `the translator agent writes docs/videos/${slug}/i18n/<locale>.json with title, description, tags and chapters for ${locales.join(", ")}`,
    },
  };
}
