// The automated pipeline, one unit of work at a time (docs/videos/AUTOMATION.md).
//
// `pipelineStatus` already knows the next step of a video from the hashes in its files. This
// adds what it cannot see (whether the fact-check rounds and the listener edit are done, how
// many retakes were tried, what the owner wrote when sending something back) in
// <workdir>/<slug>/auto.json, and does that step: a writing stage through the server's model
// runner, or one of the existing commands. The gates stop the video until the site decides: the
// owner on /admin/videos, or the site itself on arrival when the owner let it (docs/videos/
// HANDS-OFF.md) — Jev picks the outline against the channel stance, the quality check approves
// the final cut, the package check approves the upload, Jev's line check approves the narration.
// What still waits for a person: a check that did not pass, an outline Jev could not pick after
// the rewrites, a blocked video, and the upload itself, whose YouTube id comes back from the site.
import { existsSync, mkdirSync, readdirSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

import { CHANNEL_ACCENT } from "../core/accent.mjs";
import { hasAnimePolicy, isLongAnime, requireAnimePolicy } from "../core/anime-policy.mjs";
import { writeAnimeActs } from "./anime-write.mjs";
import { approvalState, approve, GATES, sha256File } from "../core/approvals.mjs";
import { audioEvidenceProblems } from "../core/audio-evidence.mjs";
import { craftChecks } from "../core/craft.mjs";
import { EXPLAINER_PRESET, hasCast, illustrated, resolveLook, SLIDES_PRESETS, slidesPresetFor } from "../core/drama.mjs";
import { effectiveEpisodeMinutes } from "../core/duration.mjs";
import { emptyLexicon } from "../core/lexicon.mjs";
import { stanceProblems } from "../core/lint.mjs";
import { articlePath, SITE } from "../core/metadata.mjs";
import { atomicWrite, contentPackFile, docDir, lexiconFile, readJson, resolveWorkBase, resolveWorkdir, ROOT, stopRequested, UsageError } from "../core/paths.mjs";
import { eachLine, LINE_ID, LOCALES, minEpisodeMinutes, NARRATION_LOCALE, narrationLocale, spokenText, textHash, VIDEO_CATEGORIES } from "../core/schema.mjs";
import { writeScreenplay } from "../core/screenplay.mjs";
import { scriptCheckBinding, scriptCheckMatches, scriptCheckUnbound } from "../core/script-check.mjs";
import { LOCALE_PARTS, readLanguages, writeLanguages } from "../core/stages.mjs";
import { ARTIFACTS, dubArtifacts, dubsStatus, lintProject, loadProject, pipelineStatus } from "../core/state.mjs";
import { estimateTimeline, speechHash } from "../core/timeline.mjs";
import { localizedThumbnailHash } from "../core/translations.mjs";
import { MAX_TEMPO } from "../dubs/plan.mjs";
import { checkPackage, listFiles, METADATA_FILE, packageLocalesWanted, UPLOAD_DIR } from "../package/check.mjs";
import { productionForEpisode } from "../production/design.mjs";
import { localizationPlan, writeLocalizationRetention } from "../production/retention.mjs";
import { buildSheet, SHEET_PARTS, sheetContext, withoutContext } from "../i18n/cli.mjs";
import { MAX_KEYFRAME_TAKES, MAX_SEED_OFFSET } from "../media/keyframes.mjs";
import { imageModelVendor, imagePromptLimit, promptOverhead, shotPromptBudget } from "../media/prompt-budget.mjs";
import { checklistFrom, guideSlugs, judgeOutline, outlineOptions, outlineReview, sourceGuideOf } from "../review/sync.mjs";
import { AutomationError, OUTPUT_INVALID, PAUSE_CODES, POLICY_HOLD, RUN_PENDING, RUN_UNCERTAIN } from "./client.mjs";
import { acquireProjectLease, ProjectLeaseError } from "../core/project-lease.mjs";
import { discussStep, SCRIPT_DISCUSSION_VARIANTS } from "./discuss.mjs";
import { JOB_GONE_KIND, RunReceiptError } from "./run-receipts.mjs";
import { pageReader, urlsIn } from "./fetch.mjs";
import { advanceStory, fixStoryPrompts } from "./story.mjs";
import { instructionsFor, parseAnswer, references, SLIDES_CAMERA_WORDS } from "./prompts.mjs";
import { registerLine, registerSummary, setPauseBeats } from "./register.mjs";
import { rewriteProblems } from "./rewrite.mjs";
import { assembleSheet, clearUnits, readUnits, refusedUnits, sheetUnits, UNIT_CHARS, UNIT_LINES, unitGaps, unitKey, unitVideo, writeUnits } from "./sheet-units.mjs";
import { advanceCompilation, startCompilation } from "./compilation.mjs";
import { castFrom, episodeBrief, isExplainerOneOff, isOneOff, retentionNumbers, scriptVerdict, seriesStep } from "./series.mjs";
import { episodeSeries, episodeShortFields, episodeShortsProblems, shortsFile } from "../shorts/episode.mjs";
import { SPEECH_UNCERTAIN } from "../tts/client.mjs";
import { flaggedLines } from "../tts/synthesis.mjs";
import { staleTakes } from "../tts/takes.mjs";

// Slides keep the general eight-minute floor. Explainers use the reviewed ten-minute default
// when an older request or saved state still names a shorter length.
const slidesMinutes = (settings) => {
  const low = Math.max(minEpisodeMinutes(), settings.target_minutes_min);
  return [low, Math.max(low, settings.target_minutes_max)];
};
const episodeMinutes = (minutes, preset) => {
  try {
    return effectiveEpisodeMinutes(minutes, preset) ?? 3;
  } catch (error) {
    if (error instanceof RangeError) throw new UsageError(error.message);
    throw error;
  }
};

export const STATE_FILE = "auto.json";
const GLOBAL_FILE = "auto-state.json";
// A requested video's first plan whose answer was lost before the request could be claimed is
// remembered this long (Automation.keepLostPlan): long enough for any site trouble to pass.
const LOST_PLAN_KEEP_MS = 14 * 86_400_000;
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,58}[a-z0-9])?$/;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
export const MAX_LINT_FIXES = 3;
export const MAX_REPLANS = 2;
export const MAX_STAGE_FAILURES = 2;
// A drama's failed sheets, keyframes or clips are handed to the writer to fix the prompts, this
// many times per kind, before the video is blocked for a person (docs/videos/DRAMA.md).
export const MAX_PROMPT_FIX_ROUNDS = 2;
// The media stages that take `--seed-offset` (media/keyframes.mjs): an owner retry of a video
// the server stopped answering for (every seed's request hash spent its attempts) shifts the
// stage's seeds, and `media()` passes the shift from state.seed_offsets.
const SEED_OFFSET_COMMANDS = new Set(["keyframes"]);
// The most a shot prompt may have whatever the image model (core/drama.mjs LIMITS.prompt, the
// writer's own figure), and the camera word that takes the most of a shot's request: the first
// draft is told the budget of the model that will draw it, counted as media/keyframes.mjs
// counts it, so a MiniMax video's prompts are not written to a limit the model has not got.
const WRITER_PROMPT_MAX = 1000;
const LONGEST_CAMERA_WORD = SLIDES_CAMERA_WORDS.reduce((longest, word) => (word.length > longest.length ? word : longest));
// The looks a slides video may end up drawn in: the channel's print rotation (settle picks one
// by the slug) and the writer's own choice among them, or tech-story, which the scripts from
// before the rotation carry. The writer is told the budget under the heaviest of them (its
// style and its negative take the most of a request), so whichever look the video gets, a
// prompt written to the number fits.
const SLIDES_WRITER_PRESETS = [...SLIDES_PRESETS, "tech-story"];
const HEAVIEST_SLIDES_LOOK = SLIDES_WRITER_PRESETS.map((preset) => resolveLook({ preset })).reduce((heaviest, look) => (promptOverhead({ look }) > promptOverhead({ look: heaviest }) ? look : heaviest));

/**
 * The vendor of the image model the server will draw a slides video with, from the worker's
 * settings, which name the slides model by id alone: the slides' own model while their switch is
 * on, else the drama's choice (apps/api/app/video_automation/settings.py slides_image_choice,
 * media/stages.mjs choiceFor); null when nothing says.
 */
export function slidesImageVendor(settings) {
  const slides = settings?.slides ?? {};
  const drama = settings?.drama ?? {};
  const own = slides.slides_media_enabled ? slides.slides_image_model : null;
  if (own) return imageModelVendor(own, own === drama.image_model ? drama.image_provider ?? null : null);
  return imageModelVendor(drama.image_model, drama.image_provider ?? null);
}
// What a blocked video's reason reads as, for a state from before `blocked_kind` was recorded
// (the nine host videos blocked on 2026-10-06): the counter an owner retry has to reset.
// The server's spent attempts first: a stage blocked on them by `media()` (exit 3) or by
// `fixPrompts` (the fixes left the request as it was) needs other seeds, not only its rounds
// back; then `prompt_fixes:<kind>`, whose wording also contains "fails".
const LEGACY_BLOCKED_KINDS = [
  [/^(?:([a-z_]+) needs the owner: |([a-z_]+) still fails after \d+ prompt fixes )?.*(?:video_media_job_exhausted|已經失敗 \d+ 次)/, (match) => `media_exhausted:${match[1] ?? match[2] ?? "keyframes"}`],
  [/^([a-z_]+) still fails after \d+ prompt fixes/, (match) => `prompt_fixes:${match[1]}`],
  [/sent the screenplay back \d+ times/, () => "prompt_fixes:script"],
  [/^the outline was sent back \d+ times/, () => "replans"],
  [/^([a-z_]+) failed \d+ times in a row:/, (match) => `failures:${match[1]}`],
];

/** The kind of block a state carries: recorded by `block()`, else read from the legacy reason; null when neither says. */
export function blockedKindOf(state) {
  if (typeof state.blocked_kind === "string" && state.blocked_kind) return state.blocked_kind;
  for (const [pattern, kind] of LEGACY_BLOCKED_KINDS) {
    const match = pattern.exec(state.blocked ?? "");
    if (match) return kind(match);
  }
  return null;
}

/**
 * What an owner's retry on /admin/videos resets, so the stage that blocked the video runs again
 * instead of blocking at the same line: the prompt-fix rounds of the kind that ran out, the
 * outline replans, a stage's failures in a row; a media request the server stopped answering
 * for gets the next seeds (state.seed_offsets, MAX_KEYFRAME_TAKES further) and its prompt-fix
 * rounds back, since the fix that could not change the request is what blocked it. An
 * uncertain writer run is the retry transport's (client.mjs retryRuns), and so is a saved job the
 * server no longer has (`job_gone:<stage>`); a lost policy verdict (`uncertain:policy`) is
 * the retry's to drop (forgetLostPolicy). Deferrals that reached their limit
 * (`deferred:<what>`) and an approval that cannot be recorded (`unrecorded:<gate>`) have no
 * counter left: `block()` cleared the wait, and the retry tries the video as it stands. Returns
 * the kind.
 */
export function resetForRetry(state) {
  const kind = blockedKindOf(state);
  const [group, name] = kind ? kind.split(":") : [];
  if (group === "prompt_fixes" && state.prompt_fixes) delete state.prompt_fixes[name];
  else if (group === "replans") state.replans = 0;
  else if (group === "failures" && state.failures) delete state.failures[name];
  else if (group === "media_exhausted") {
    if (state.prompt_fixes) delete state.prompt_fixes[name];
    if (SEED_OFFSET_COMMANDS.has(name)) state.seed_offsets = { ...(state.seed_offsets ?? {}), [name]: Math.min((state.seed_offsets?.[name] ?? 0) + MAX_KEYFRAME_TAKES, MAX_SEED_OFFSET) };
  }
  return kind;
}
// Once the retakes are spent, the lines Jev still hears wrong are reworded by the listener and
// retaken, this many rounds in all, before the narration waits for the owner (docs/videos/HANDS-OFF.md §旁白).
export const MAX_REWRITE_ROUNDS = 2;
// A dub track (docs/videos/DUBS.md): a window that does not fit even sped up has its lines
// shortened by the translator this many rounds, and the lines Jev hears wrong are retaken this
// many rounds, before the worker gives the locale up with the reason and the video goes on
// without that track (docs/videos/LANGUAGES.md).
export const MAX_DUB_SHORTEN_ROUNDS = 2;
export const MAX_DUB_RETAKE_ROUNDS = 2;
// The lines Jev still hears wrong after the retakes are reworded by the translator (variant
// "reword") this many rounds: a homophone is heard the same way on every take.
export const MAX_DUB_REWORD_ROUNDS = 2;
const MAX_SOURCE_PAGES = 25;
const MAX_SOURCE_CHARS = 350_000;
const REQUIRED_SECTIONS = ["## 觀眾看完能做到的事", "## 站主觀點", "## 大綱"];
const DRAMA_SECTIONS = ["## 故事前提", "## 角色", "## 站主觀點", "## 大綱"];
// An explainer's brief (docs/videos/so-thats-why/) answers a question and has no cast.
const EXPLAINER_SECTIONS = ["## 問題", "## 一句答案", "## 站主觀點", "## 大綱"];
const YOUTUBE_ID = /^[A-Za-z0-9_-]{11}$/;
// The site's refusals of a slides claim that mean the request is no longer the worker's to make:
// the owner cancelled it while it was planned, or another request holds the slug (draftSlides).
const WITHDRAWN_CLAIMS = new Set(["video_slides_request_not_queued", "video_slides_request_slug_taken"]);
// Which manifest a drama stage's failures are read from, and what its entries are called.
const FIX_SOURCES = {
  look: { manifest: ARTIFACTS.characters, entries: "characters", what: "character" },
  keyframes: { manifest: ARTIFACTS.keyframes, entries: "shots", what: "shot" },
  clips: { manifest: ARTIFACTS.clips, entries: "shots", what: "shot" },
};

const today = (ctx) => ctx.now().toISOString().slice(0, 10);
/**
 * The prompt variant of an episode's writer and checker: "episode" for an episode of a long
 * series (the beats, the recaps, the next episode's promise); a one-off drama, though it is an
 * episode of its own one-episode series (docs/videos/DRAMA-FLOW.md, section 2), is written with
 * the drama prompts, since its story ends. A brand story (story.mjs) has variants of its own and
 * no recap.
 */
const episodeVariant = (state) => (state.series && !["one-off", "story"].includes(state.series.kind) ? "episode" : null);

/**
 * The owner retried a video whose final cut's policy verdict from Jev was lost (`uncertain:policy`,
 * Automation.submissionFailure): qa keeps the loss in review/qa.json (`policy_lost`) and does not
 * ask Jev again for the same narration while it is there, so the retry drops it.
 */
function forgetLostPolicy(workdir) {
  const file = path.join(workdir, "review", "qa.json");
  const report = readJson(file, null);
  if (!report?.policy_lost) return;
  delete report.policy_lost;
  atomicWrite(file, `${JSON.stringify(report, null, 2)}\n`);
}

/** Every video the automation started, oldest first. */
export function automatedVideos(workBase) {
  if (!existsSync(workBase)) return [];
  return readdirSync(workBase, { withFileTypes: true })
    .filter((entry) => entry.isDirectory() && existsSync(path.join(workBase, entry.name, STATE_FILE)))
    .map((entry) => readJson(path.join(workBase, entry.name, STATE_FILE)))
    .filter((state) => state && SLUG.test(state.slug ?? ""))
    .sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)));
}

function saveState(workdir, state) {
  mkdirSync(workdir, { recursive: true });
  atomicWrite(path.join(workdir, STATE_FILE), `${JSON.stringify(state, null, 2)}\n`);
}

/**
 * Whether a translation worksheet has nothing left to fill, for the parts it holds (i18n-sheet
 * --parts). The thumbnail's words count only when the sheet has a `thumbnail` entry and the
 * translator has not been asked for those words yet: `askedThumbnail` is the hash
 * (thumbnailAskHash) recorded when it was. They are optional (i18n-merge only notes them), so
 * a translator that leaves them empty is asked once per thumbnail, not every round.
 */
export function sheetDone(sheet, askedThumbnail = null) {
  const filled = (entry) => typeof entry?.text === "string" && entry.text.trim() !== "";
  const parts = Array.isArray(sheet.parts) && sheet.parts.length ? sheet.parts : ["metadata", "captions"];
  const captions = !parts.includes("captions") || !(sheet.lines ?? []).some((line) => line.todo);
  const metadata = !parts.includes("metadata") || (filled(sheet.title) && filled(sheet.description) && (sheet.chapters ?? []).every(filled) && Array.isArray(sheet.tags?.text) && sheet.tags.text.length > 0);
  const words = sheet.thumbnail?.source;
  const thumbnail = !parts.includes("metadata") || !words || thumbnailAskHash(sheet) === askedThumbnail
    || Object.keys(words).every((name) => typeof sheet.thumbnail.text?.[name] === "string" && sheet.thumbnail.text[name].trim() !== "");
  return captions && metadata && thumbnail;
}

/** The hash of the thumbnail words a sheet asks for (its `thumbnail.source`), or null without them. */
export function thumbnailAskHash(sheet) {
  const words = sheet?.thumbnail?.source;
  return words && typeof words === "object" ? textHash(JSON.stringify(words)) : null;
}

/**
 * The worksheet a model hands back, with the sheet's identity and its thumbnail's `source` and
 * `todo` whatever the model left out. A model that drops the thumbnail keeps `fallback`'s words
 * (the translator's, when the caption reviewer answers without them), else the sheet's own.
 */
/**
 * What a unit's request carries beside its worksheet (i18n/cli.mjs translationContext): the
 * sheet's glossary, and the cue boundaries of the unit's own lines (a metadata unit has no lines,
 * so none); a sheet from before the context adds nothing, and the prompts read both as optional.
 */
function unitContext(context, unit) {
  const carried = {};
  if (context.glossary) carried.glossary = context.glossary;
  const lines = unit.lines ?? [];
  if (context.boundaries && lines.length) carried.boundaries = Object.fromEntries(lines.filter((line) => context.boundaries[line.id]).map((line) => [line.id, context.boundaries[line.id]]));
  return carried;
}

function keptWorksheet(worksheet, sheet, locale, fallback = null) {
  const kept = { ...worksheet, locale, slug: sheet.slug, parts: sheet.parts };
  if (!sheet.thumbnail) return kept;
  const words = (entry) => (entry?.text && typeof entry.text === "object" && !Array.isArray(entry.text) ? entry.text : null);
  kept.thumbnail = { ...sheet.thumbnail, text: words(worksheet.thumbnail) ?? words(fallback?.thumbnail) ?? sheet.thumbnail.text };
  return kept;
}

/**
 * What a translation payload adds for a video narrated in another language than zh-TW:
 * { source_locale }, which also picks the translator's and the caption reviewer's texts for that
 * source (prompts.mjs SOURCE_INSTRUCTIONS). Nothing for a zh-TW video, whose payload and prompts
 * stay as they were.
 */
function sourceLocale(video) {
  const source = narrationLocale(video);
  return source === NARRATION_LOCALE ? {} : { source_locale: source };
}

function titleOf(brief) {
  return (/^#\s+(.+)$/m.exec(brief)?.[1] ?? "").trim().slice(0, 200);
}

/** The site article a video retells: its source_guide, or else the first site article it rests on. */
export function mainGuide({ source_guide: guide, source_urls: urls }) {
  return (GUIDE_SLUG.test(guide ?? "") ? guide : null) ?? guideSlugs(urls)[0] ?? null;
}

// Until 2026-09-27 drafts read their article at /<locale>/guides/<slug>, a kind's list page the
// site answers with 404 for an article; the writer of gpt-6-sol-luna-where-to-use refused twice
// for want of a source. Addresses saved that way are read where the article is served.
const STALE_ARTICLE_URL = /^https:\/\/(?:www\.)?mokaair\.com\/([A-Za-z-]+)\/guides\/([a-z0-9][a-z0-9-]{0,118}[a-z0-9])\/?(?:[?#].*)?$/;

/**
 * Where a stage reads a site article: the path its content pack's kind gives (core/metadata.mjs
 * articlePath). A slug with no pack here is read as a life article, the section the drafts'
 * topics come from (apps/api/app/video_automation/topics.py).
 */
export function siteArticleUrl(slug, root = ROOT, locale = "zh-TW") {
  const kind = readJson(contentPackFile(slug, root), null)?.kind ?? "life";
  return `${SITE}/${locale}${articlePath({ slug, kind })}`;
}

/**
 * The pages a stage reads for a video: its site article first, then the rest, each stale
 * /<locale>/guides/<slug> address moved to where the article is served. A kind's list page has
 * no content pack, so it stays as it is.
 */
export function siteSources(sourceGuide, urls = [], root = ROOT) {
  const moved = (urls ?? []).map((url) => {
    const stale = STALE_ARTICLE_URL.exec(String(url));
    if (!stale) return url;
    if (stale[2] === sourceGuide || existsSync(contentPackFile(stale[2], root))) return siteArticleUrl(stale[2], root, stale[1]);
    return url;
  });
  return [...new Set([...(sourceGuide ? [siteArticleUrl(sourceGuide, root)] : []), ...moved])];
}

/**
 * What makes a planner's answer unusable, or null. `usedGuides` are earlier videos' main
 * articles; a drama's brief has the story bible's sections instead of a tutorial's, and an
 * explainer's (`preset` "flat-explainer") the question's. With a
 * channel stance, 站主觀點 must open by naming the stance points it applies (core/lint.mjs
 * stanceProblems); the local `lint` has no stance and does not check this. `requiredGuide` is
 * the site article the owner asked a slides video of (draftSlides): the brief must retell that
 * one, whatever earlier video used it.
 */
export function planProblem(plan, taken, usedGuides = new Set(), format = "slides", stance = "", preset = null, requiredGuide = null) {
  if (!plan || typeof plan !== "object") return "the answer is not an object";
  if (!SLUG.test(plan.slug ?? "")) return `slug "${plan.slug}" is not lowercase kebab-case of at most 60 characters`;
  if (taken.has(plan.slug)) return `slug "${plan.slug}" is already used by an earlier video`;
  if (typeof plan.brief !== "string") return "brief is missing";
  const sections = format !== "drama" ? REQUIRED_SECTIONS : preset === EXPLAINER_PRESET ? EXPLAINER_SECTIONS : DRAMA_SECTIONS;
  const missing = sections.filter((heading) => !plan.brief.includes(heading));
  if (missing.length) return `brief lacks ${missing.join(", ")}`;
  const stanceIssues = stanceProblems(plan.brief, stance);
  if (stanceIssues.length) return `站主觀點 does not apply the channel stance: ${stanceIssues.join("; ")}`;
  if (outlineOptions(plan.brief).length < 2) return "brief needs 2 or 3 options written as 「### 選項 A：…」 with 一行說明 and 開場鉤子 lines";
  if (!Array.isArray(plan.source_urls) || !plan.source_urls.every((url) => /^https:\/\//.test(url))) return "source_urls must be https URLs";
  if (requiredGuide && plan.source_guide !== requiredGuide) return `source_guide must be "${requiredGuide}", the site article the owner asked for (requested_guide)`;
  const guide = mainGuide(plan);
  if (guide && usedGuides.has(guide)) return `the site article "${guide}" is what an earlier video retells (see used_guides); pick another topic`;
  return null;
}

/** The pages a stage rests on, read now, within the payload's size budget. */
async function readSources(read, urls) {
  const pages = [];
  let chars = 0;
  for (const url of [...new Set(urls)].slice(0, MAX_SOURCE_PAGES)) {
    const page = await read(url);
    if (page.ok && chars + page.text.length > MAX_SOURCE_CHARS) {
      pages.push({ url, ok: false, error: "not read: the payload is full" });
      continue;
    }
    chars += page.ok ? page.text.length : 0;
    pages.push(page);
  }
  return pages;
}

function writeVideo(dir, video) {
  writeFileSync(path.join(dir, "video.json"), `${JSON.stringify(video, null, 2)}\n`);
}

function mergeLexicon(root, additions) {
  if (!additions || typeof additions !== "object") return [];
  const file = lexiconFile(root);
  const lexicon = readJson(file, { schema_version: 1, terms: {} });
  const added = [];
  for (const [term, spoken] of Object.entries(additions)) {
    if (!/^[A-Za-z0-9][A-Za-z0-9.+#'_-]{0,39}$/.test(term) || term in lexicon.terms) continue;
    if (spoken !== null && (typeof spoken !== "string" || !spoken.trim() || spoken.length > 80)) continue;
    lexicon.terms[term] = spoken === null ? null : spoken.trim();
    added.push(term);
  }
  if (added.length) atomicWrite(file, `${JSON.stringify(lexicon, null, 2)}\n`);
  return added;
}

/**
 * The settings a video reads by its format (docs/videos/DRAMA-FLOW.md, section 1). A drama has
 * its own standing instructions, narrator voice, fact-check and retake rounds and topic scope on
 * drama tab's settings; a null voice, and a site from before the split that sends none
 * of them, mean the tutorial's. The languages a video is made in are not here at all: the owner
 * chooses them per video after the final cut (docs/videos/LANGUAGES.md), and `caption_locales`
 * only pre-ticks that panel.
 */
export function settingsFor(settings, format = "slides") {
  const tutorial = {
    voice: settings.voice,
    instructions: settings.stage_instructions ?? {},
    verifyRounds: settings.max_verify_rounds,
    retakeRounds: settings.max_retake_rounds,
    topicScope: settings.topic_scope ?? [],
  };
  if (format !== "drama") return tutorial;
  const drama = settings.drama ?? {};
  return {
    voice: drama.drama_voice ?? tutorial.voice,
    instructions: drama.drama_stage_instructions ?? tutorial.instructions,
    verifyRounds: drama.drama_max_verify_rounds ?? tutorial.verifyRounds,
    retakeRounds: drama.drama_max_retake_rounds ?? tutorial.retakeRounds,
    topicScope: drama.drama_topic_scope ?? tutorial.topicScope,
  };
}

/**
 * The settings tab's voice as video.json may carry it: the site serialises every field (a null
 * model, a "+0%" rate), and lint refuses the ones the provider does not use. Gemini takes its
 * pace from the style and has no rate; Azure has a rate and no style or model.
 */
export function settledVoice(voice) {
  const unused = voice.provider === "gemini" ? ["rate"] : ["style", "model"];
  return Object.fromEntries(Object.entries(voice).filter(([key, value]) => value !== null && value !== "" && !unused.includes(key)));
}

/**
 * video.json as the owner's settings say it must be, whatever the model returned. A drama
 * (docs/videos/DRAMA.md) also takes the settings tab's style preset and whether music is made,
 * uses selectable CC, and its narrator voice is the drama part's when the owner chose
 * one; the writer's own look fields stay. The owner's request's preset (`stylePreset`) wins over
 * the settings tab's; an explainer's preset is not the writer's to change, and it has no characters.
 */
export function settle(video, { slug, settings, sourceGuide, root, format = "slides", series = null, cast = null, stylePreset = null, production = null }) {
  const settled = { ...video, slug, voice: settledVoice(settingsFor(settings, format).voice) };
  if (format === "drama" && production?.profile?.phases?.primary?.locale === "zh-TW") {
    const narrator = production.narrator;
    if (typeof narrator?.voice_name !== "string" || !narrator.voice_name.trim() || typeof narrator.performance !== "string" || !narrator.performance.trim()) {
      throw new AutomationError("the approved Chinese production needs a selected narrator voice and performance direction", { code: "video_production_voice_mismatch", who: "owner" });
    }
    if ((cast ?? video.characters ?? []).some((character) => character.voice?.provider === "gemini" && character.voice.name === narrator.voice_name)) {
      throw new AutomationError("the production narrator must have a voice distinct from every character; revise the approved narrator selection", { code: "video_production_voice_mismatch", who: "owner" });
    }
    settled.voice = { provider: "gemini", name: narrator.voice_name, style: `${CHANNEL_ACCENT}。${narrator.performance}`.slice(0, 400) };
    settled.pronunciation_hints = { ...(production.pronunciation_hints ?? {}) };
    const laterLanguages = localizationPlan(production);
    if (laterLanguages) settled.localization_plan = laterLanguages;
    settled.narration_locale = "zh-TW";
    if (settled.youtube) settled.youtube = { ...settled.youtube, default_language: "zh-TW" };
  }
  // The description links the article through its content pack. An article the news automation
  // published lives only in the database, so without a pack the script names it in sources instead.
  if (sourceGuide && existsSync(contentPackFile(sourceGuide, root))) settled.source_guide = sourceGuide;
  else delete settled.source_guide;
  settled.assets = [];
  if (settled.youtube) settled.youtube = { ...settled.youtube, video_id: null };
  const drama = settings.drama ?? {};
  if (format === "drama") {
    settled.format = "drama";
    const preset = stylePreset ?? drama.style_preset ?? "cinematic-3d";
    settled.look = { preset, ...(video.look ?? {}) };
    if (isLongAnime(series)) settled.look.preset = "anime-2d";
    if (preset === EXPLAINER_PRESET) {
      settled.look.preset = EXPLAINER_PRESET;
      settled.characters = [];
    }
    // New automatic productions use selectable CC, even if an old site setting or writer
    // asks for burn-in. Explicit legacy video.json files remain readable by assemble.
    settled.subtitles = { ...(video.subtitles ?? {}), burn_in: false };
  } else if (illustrated(video)) {
    // Illustrated slides (docs/videos/ILLUSTRATED.md): one of the channel's print looks by the
    // slug unless the writer named one, and the owner's licensed music file and sound-effect set
    // from the settings tab's slides object (migration 0114; a site from before it sends none)
    // when the writer named none.
    settled.look = { preset: slidesPresetFor(slug), ...(video.look ?? {}) };
    const slides = settings.slides ?? {};
    if (!settled.music && slides.slides_music_track) settled.music = { track: slides.slides_music_track };
    if (!settled.sfx && slides.slides_sfx_set) settled.sfx = { set: slides.slides_sfx_set };
  } else if (format !== "drama") {
    // Plain slides: the writer is told the look rides on shots, so a look without any is dropped
    // rather than left for lint to refuse.
    delete settled.look;
  }
  // Music is the owner's switch for every format.
  if (drama.music_enabled === false) delete settled.music;
  if (format === "drama" && series) {
    // An episode of a series (docs/videos/SERIES.md): the cast is the setting book's, word for
    // word, listed by id; a character the book does not have stays for lint to refuse. An
    // explainer (a one-off of the flat-explainer preset) has no cast whatever the writer returned.
    settled.series = { slug: series.slug, episode: series.episode, chapter: series.chapter };
    const book = new Map((cast ?? []).map((character) => [character.id, character]));
    settled.characters = settled.look?.preset === EXPLAINER_PRESET ? [] : (video.characters ?? []).map((character) => book.get(character?.id) ?? character).sort((a, b) => (a?.id < b?.id ? -1 : a?.id > b?.id ? 1 : 0));
  }
  // Production authority comes from the approved request, never model-generated metadata.
  if (hasAnimePolicy(series)) {
    const runtime = requireAnimePolicy(series);
    settled.production_policy = series.production_policy;
    settled.runtime_spec = { ...runtime };
    settled.category = "anime";
    settled.target_minutes = [runtime.body_target_seconds / 60, runtime.body_target_seconds / 60];
    settled.look = { ...settled.look, preset: "anime-2d" };
    settled.series = { slug: series.slug, episode: series.episode, chapter: series.chapter, kind: "series", genre: "custom", lead: "ensemble", planned_episodes: series.planned_episodes, open_ended: series.open_ended, closed_ending: series.closed_ending };
    delete settled.compilation;
  } else {
    delete settled.production_policy;
    delete settled.runtime_spec;
  }
  return settled;
}

function lintErrors(ctx, slug) {
  const result = lintProject(loadProject({ slug, root: ctx.root }));
  return result.errors.map((error) => `${error.path}: ${error.message}`);
}

async function run(ctx, command) {
  // Tests hand in a runner that plays the media stages without any vendor.
  if (ctx.runCommand) return ctx.runCommand(command, ctx);
  const { main } = await import("../cli.mjs");
  let out = "";
  const sink = { write: (text) => (out += text) };
  const code = await main(command, { ...ctx, stdout: sink, stderr: sink });
  return { code, out };
}

const lastLine = (out, lines = 1) => out.trim().split("\n").slice(-lines).join(" ");
/**
 * A speech command (tts, dub, check-audio) that stopped because a paid request went out and its
 * answer was lost (tts/client.mjs SPEECH_UNCERTAIN, exit 3 with the code in its last line). It
 * may have been charged: running the command again would buy it again, and giving a dub up would
 * drop the language for good, so the video waits for the owner.
 */
const speechUncertain = (result) => result.code === 3 && lastLine(result.out).includes(SPEECH_UNCERTAIN);
/**
 * A review-push whose quality check lost Jev's policy verdict on the way back (exit 3 with the
 * client's RUN_UNCERTAIN code in its last line; review/sync.mjs qualityCheck).
 */
const lostPolicy = (result) => result.code === 3 && lastLine(result.out).includes(RUN_UNCERTAIN);
/** The digits of a line, in order: a shortened translation must keep every one of them. */
const digitsOf = (text) => (String(text).match(/\d+(?:[.,]\d+)*/g) ?? []).join(" ");
/** A unit's report line names its video once: a phrase gets the slug, a line that has it stays. */
const lineFor = (slug, text) => (text.startsWith(`${slug}: `) ? text : `${slug}: ${text}`);
const blockedLabel = (state) => `卡住，需要人處理：${state.blocked}`.slice(0, 120);
const BLOCKED_REPORT_BACKOFF_MS = 5 * 60_000;
// A video that could not move for a reason of its own that passes (a vendor busy, a push the site
// did not take, Jev away) waits on its own (Automation.defer): auto.json `deferred_until`, five
// minutes the first time and twice as long each time in a row (`defer_count`, cleared by the
// next visit that ends without trouble), at most two hours, while the lane goes on with the next
// video. Until 2026-10-06 such a video ended its lane's run (`later()`), and since the videos go
// oldest first, the same video ended every run and the second lane ran into it next.
export const DEFER_BASE_MS = 5 * 60_000;
export const DEFER_MAX_MS = 2 * 3600_000;
// Waiting is not for ever: after this many deferrals in a row (5, 10, 20, 40, 80 and 120 minutes,
// about four and a half hours) the next failure blocks the video with the last reason, so the
// owner reads it on /admin/videos and a retry starts it again at once. Without the limit a
// condition that waiting cannot cure (a revoked vendor key, a push the site will always refuse)
// was tried every two hours for ever with nothing on the page.
export const DEFER_LIMIT = 6;
// An approval the site gave that review-pull cannot record (pulled) is refused here, on this
// machine, and does not pass by waiting: three deferrals (35 minutes), then the block.
export const UNRECORDED_LIMIT = 3;
// From this deferral in a row on the site is told, as a checklist row the owner reads on
// /admin/videos; the first one is usually over by the next round.
export const DEFER_REPORT_FROM = 2;
/** The checklist row of a video that waits on its own: why, until when (UTC) and which try in a row. */
const deferredLabel = (state, why) => `暫時過不去，${String(state.deferred_until).slice(0, 16).replace("T", " ")} UTC 後再試（連續第 ${state.defer_count} 次）：${why}`.slice(0, 120);
// How much of the client's reason a pending writer's line carries (a server's detail can run long).
const PENDING_WHY_LENGTH = 160;
// How long every lane of this run leaves a video whose writer is still running on the server
// (RUN_PENDING): the worker's round (ops/video/worker.sh, 300 s), so its receipt is looked up
// once a round, not by each lane in turn (two lanes polling one job got a 429 on 2026-10-06).
export const PENDING_RECHECK_MS = 5 * 60_000;
// A video's unit met its project's STOP file, or lost the project's lease, before a paid request
// or a write to its canonical files (Automation.fence): the video sits the rest of the run out,
// nothing is sent or written, and an answer already received stays saved for the next unit.
export const PROJECT_HELD = "video_project_held";
// What an error from moving one video means for the others (errorScope). The token, the
// owner's settings and budget, every subscription account and a site out of reach are everyone's;
// so are a 4xx about the settings of the whole site (no model chosen for the Shorts' test, the
// outline judge switched off) and one about the worker's own list request. None of them may
// block the one video that happened to meet it.
const RUN_CODES = new Set([
  "video_tool_token_invalid", "video_ai_provider_not_configured", "video_ai_budget_exhausted", "video_ai_subscription_cli_outdated",
  "video_automation_settings_invalid", "video_ai_subject_not_chosen", "video_judge_not_enabled", "video_list_filter_invalid",
  "video_shorts_state_needs_only", "network", ...PAUSE_CODES,
]);
// A service busy, briefly away or still working: asking later may well go through. So may a
// durable writer job the server failed before it reached the model (apps/api/app/video_automation
// ai.py run_stage, run_jobs.py): the work base's STOP file or one video's, the automation switched
// off, a job the queue lost before its dispatch. Nothing ran and the journal is already gone
// (client.mjs removeFailed), so the next attempt sends the job once; a 409 that blocked the
// video here needed an owner retry for each video that had a job queued.
const WAIT_CODES = new Set([
  "video_ai_upstream_busy", "video_ai_upstream_unreachable", "rate_limit_exceeded", "upstream_unavailable", RUN_PENDING,
  "video_ai_worker_stopped", "video_ai_automation_disabled", "video_ai_job_interrupted_before_dispatch", "video_ai_job_dispatch_closed",
]);

/**
 * What an error thrown while moving one video means for the run (Automation.move): "run" — the
 * token, the owner's settings or budget, every subscription account, the site out of reach, or
 * an error that is no AutomationError: the run ends, as every error did before 2026-10-06;
 * "wait" — a rate limit, a 5xx, a busy or unreachable model service, a run still pending, a job
 * the server failed before dispatching it: this video waits (defer, no sooner than the server's
 * `retry_after` when it gave one) and the others move; "video" — any other refusal of this
 * video's request (a 4xx: the project dropped, a job whose input changed, a setting this
 * production lacks): asking again would be refused the same way, so the video is blocked with
 * the reason and the others move. The table in automation.test.mjs lists every code the
 * worker's routes answer with its scope.
 */
export function errorScope(error) {
  if (!(error instanceof AutomationError)) return "run";
  const code = error.code ?? "";
  const status = error.status ?? 0;
  if (RUN_CODES.has(code) || status === 401 || status === 403) return "run";
  if (WAIT_CODES.has(code) || status === 408 || status === 429 || status >= 500) return "wait";
  if ((status >= 400 && status < 500) || error.who === "owner") return "video";
  return "run";
}

// Trouble that is the whole worker's or the site's and passes without anyone touching the video:
// Jev's daily calls or the month's speech characters spent, the review store full, the API's rate
// limit or its limiter away, the job queue away, the work base's STOP file or the switch. Such a
// deferral waits and shows on the card like any other and never counts toward DEFER_LIMIT
// (Automation.defer `everyone`). While it did, a Jev budget spent in the morning blocked every
// video that reached an outline judgement or a narration check by the afternoon, and each stayed
// blocked, one owner retry apiece, after the budget came back at midnight. Left out on purpose: a
// vendor's own answers (a revoked key reads as a 502 for every video and must reach a card), the
// two codes of a job the queue lost before its dispatch (a queue that loses every job must too),
// and the forwarders' 502 `upstream_unavailable`, which is also what a request the API did not
// answer in time gets (apps/web/app/api/video/reviews/[...path]/forward.ts aborts and answers
// the same 502), so it may be one video's own; with the API down the unit's list read ends the
// run before any video is deferred.
const EVERYONE_CODES = new Set([
  "jev_budget_exhausted", "video_speech_budget_exhausted", "video_review_store_full", "rate_limit_exceeded", "rate_limit_unavailable",
  "video_ai_job_queue_unavailable", "video_ai_worker_stopped", "video_ai_automation_disabled",
]);
// The same trouble as a command that exits 4 words it: tts, dub, check-audio, qa and review-push
// print the server's detail and not its code, so the worker reads the setting or the sentence
// the detail names (apps/api/app/video_automation/judge.py and video_speech/checking.py for Jev's
// budget, video_reviews/storage.py, video_speech/admin_api.py and align_api.py and the tools' own
// pre-check for the month's characters, app/infra.py and middleware.py for the rate limit). A
// wording the server changes is counted again, which is how every deferral was before.
const EVERYONE_WORDING = [
  [/JEV_DAILY_CALL_BUDGET/, "jev_budget_exhausted"],
  [/the review store is full/, "video_review_store_full"],
  [/語音字數預算|billable characters needed[^\n]* left this month/, "video_speech_budget_exhausted"],
  [/請求過於頻繁/, "rate_limit_exceeded"],
  [/安全驗證服務暫時無法使用/, "rate_limit_unavailable"],
];

/**
 * The code of trouble that is everyone's (EVERYONE_CODES), or null for one video's own: from an
 * error's code, or from what a command that exited 4 printed. What defer() is told as `everyone`.
 */
export function everyones(trouble) {
  if (typeof trouble === "string") return EVERYONE_WORDING.find(([wording]) => wording.test(trouble))?.[1] ?? null;
  return trouble instanceof Error && EVERYONE_CODES.has(trouble.code ?? "") ? trouble.code : null;
}

/** A file's sha256, or null when it cannot be read. */
function fileSha256(file) {
  try {
    return createHash("sha256").update(readFileSync(file)).digest("hex");
  } catch {
    return null;
  }
}

/**
 * The takes on disk (audio/<id>.wav) that differ from the ones timeline.json binds, as id → the
 * sha256 of the take on disk, for the lines in `ids` (every line without); null when the timeline
 * names no lines or a take cannot be read.
 */
function changedTakes(timeline, workdir, ids = null) {
  if (!Array.isArray(timeline?.lines)) return null;
  const changed = {};
  for (const line of timeline.lines) {
    if (ids && !ids.has(line.id)) continue;
    const hash = LINE_ID.test(line.id ?? "") ? fileSha256(path.join(workdir, ARTIFACTS.audio, `${line.id}.wav`)) : null;
    if (!hash) return null;
    if (hash !== line.audio_sha256) changed[line.id] = hash;
  }
  return changed;
}

/** How a retake that exited 4 waits: as a tts would, everyone's trouble never counting toward a block. */
const retakeWait = (redo) => ({ what: "tts", everyone: Boolean(everyones(redo.out)) });

/**
 * Whether every take that no longer matches timeline.json is one made by the retake that a STOP
 * file or a service ended (auto.json `stopped_retake`, written by retakeStopped), with the very
 * bytes it wrote, and narration.wav, which a stopped tts never writes, is still the bound one. A
 * take changed on any other line, or to other bytes, is not explained, and the guard before tts
 * stays shut.
 */
function retakeExplains(stopped, timeline, workdir) {
  const made = stopped?.takes;
  if (!made || typeof made !== "object") return false;
  const changed = changedTakes(timeline, workdir);
  if (!changed || !Object.keys(changed).length) return false;
  if (fileSha256(path.join(workdir, ARTIFACTS.narration)) !== timeline.audio_evidence?.narration_sha256) return false;
  return Object.entries(changed).every(([id, hash]) => made[id] === hash);
}

// The package check's problems that only `package` run for the current choice fixes
// (tools/video/package/check.mjs): a metadata.json written for another choice, and a part of a
// locale the choice does not have.
const CHOICE_PROBLEM = /written for another language choice|the language choice does not have/;

/**
 * Whether the upload package no longer fits the owner's language choice in the work directory:
 * written for another choice, or holding a description, caption file, dub track or language
 * thumbnail of a locale the choice does not have, which the package check fails with "run
 * package again". Read the way that check reads it but without hashing final.mp4, so it costs
 * little to ask every round. False without a package (it is written later, with the choice) or
 * without a choice. A metadata.json that cannot be parsed, or is not an object, leaves the answer
 * unknown: false too, so the language round goes on instead of ending `auto` in an exception. A
 * field not of the type package writes (a caption list that is a number, say) fails its own item
 * by name, which is no choice problem, so only the choice decides.
 */
function packageChoiceStale(workdir) {
  const upload = path.join(workdir, UPLOAD_DIR);
  try {
    const metadata = readJson(path.join(upload, METADATA_FILE), null);
    if (!metadata || typeof metadata !== "object" || Array.isArray(metadata)) return false;
    const { languages, locales, descriptionLocales } = packageLocalesWanted(workdir, metadata);
    if (!languages) return false;
    // Only the choice's problems are read, so the final's hashes are left out.
    const report = checkPackage({ files: listFiles(upload), metadata, finalSha256: null, approvedSha256: null, metadataSha256: null, locales, descriptionLocales, languages });
    return report.items.some((item) => !item.ok && CHOICE_PROBLEM.test(item.detail));
  } catch {
    return false;
  }
}

/**
 * Whether the video is past its upload confirmation: the publish review approved (status done)
 * or the owner's YouTube id recorded. Its package went up with that review, and nothing writes or
 * pushes the publish gate again.
 */
const pastUpload = (state) => Boolean(state.youtube_video_id) || state.status === "done";

/**
 * What the script records for the site: the YouTube id, or null (a report without it would clear
 * the site's), and the video's category, the state's first (a brand story has it before its
 * video.json exists), or null. The site fills a category only on a video nobody has filed yet.
 */
function recorded(state, root) {
  const video = readJson(path.join(docDir(state.slug, root), "video.json"), null);
  const id = video?.youtube?.video_id;
  const category = state.category ?? video?.category;
  return { videoId: YOUTUBE_ID.test(id ?? "") ? id : null, category: VIDEO_CATEGORIES.includes(category) ? category : null };
}

// The stage the site last took for a state object in hand (one unit's copy of auto.json), so a
// deferral reported later in the same unit keeps that stage instead of the list's older one
// (Automation.shownStage).
const REPORTED_STAGE = new WeakMap();

/**
 * Hand everything the automation knows to /admin/videos: title, stage, checklist, article, format,
 * category, YouTube id. `deferred` is the label of a video waiting on its own (Automation.defer):
 * the checklist opens with that row, and auto.json's `deferred_reported` remembers the page shows
 * it; any report without it takes the row off again, so the next stage that reports clears it.
 * `progress` is a translation's row the same way (Automation.unitCheckpoint), until the next
 * report without it.
 */
async function report(ctx, api, state, stage, { deferred = null, progress = null } = {}) {
  const workdir = resolveWorkdir({ env: ctx.env, slug: state.slug, root: ctx.root, home: ctx.home });
  const status = await pipelineStatus({ slug: state.slug, root: ctx.root, workdir });
  const guide = mainGuide(state);
  const { videoId, category } = recorded(state, ctx.root);
  // The page has no field for why a video stopped or waits; the checklist is what the owner reads.
  const blocked = state.status === "blocked" && state.blocked ? [{ key: "blocked", label: blockedLabel(state), done: false }] : [];
  const waiting = deferred && !blocked.length ? [{ key: "deferred", label: deferred, done: false }] : [];
  // A translation part by part (Automation.unitCheckpoint): how many units are reviewed so far.
  const partial = progress && !blocked.length ? [{ key: "languages_progress", label: progress.slice(0, 120), done: false }] : [];
  await api.report(state.slug, {
    title: state.title || state.slug,
    stage: stage.slice(0, 40),
    checklist: [...blocked, ...waiting, ...partial, ...checklistFrom(status.steps)],
    format: state.format ?? "slides",
    youtube_video_id: videoId,
    ...(guide ? { source_guide: guide } : {}),
    ...(category ? { category } : {}),
    ...(hasAnimePolicy(state) ? { production_policy: state.production_policy, runtime_spec: state.runtime_spec } : {}),
    ...(state.series ? { series_slug: state.series.slug, ...(Number.isInteger(state.series.episode) ? { episode_number: state.series.episode } : {}) } : {}),
    ...(state.retry_request_id ? { retry_acknowledged_id: state.retry_request_id } : {}),
    // What kind of block it is (`block()`), for a site that will read it; today's ignores the key.
    ...(state.status === "blocked" && state.blocked_kind ? { blocked_kind: state.blocked_kind } : {}),
  });
  REPORTED_STAGE.set(state, stage);
  if (waiting.length) state.deferred_reported = true;
  else delete state.deferred_reported;
}

export class Automation {
  /**
   * `lane` runs several of these side by side in one `auto` (VIDEO_WORKER_LANES): `busy` is the
   * slugs some lane is moving right now (in the video's own unit, or answering a line on its
   * screenplay), shared by every lane, and a `secondary` lane only moves
   * videos already under way, never drops, retries, drafts, discussions or series, which stay
   * with the first lane so two lanes never start the same thing. `skipped` (the videos left for
   * the rest of this run, defer) and `pendingUntil` (slug → when a writer still running on the
   * server may be looked up again) are shared by every lane the same way, so one lane does not
   * pick up the video another just set aside.
   */
  constructor(ctx, api, settings, { busy = new Set(), skipped = new Set(), pendingUntil = new Map(), secondary = false } = {}) {
    this.ctx = ctx;
    this.api = api;
    this.settings = settings;
    this.busy = busy;
    this.skipped = skipped;
    this.pendingUntil = pendingUntil;
    // The project leases this lane holds, by slug: one for the video its unit moves, and those
    // fence() took for this step outside a unit (stepLeases), released when the step ends.
    this.leases = new Map();
    this.stepLeases = new Map();
    this.secondary = secondary;
    this.read = pageReader({ fetchImpl: ctx.fetch ?? globalThis.fetch, sleep: ctx.sleep, now: () => ctx.now().getTime() });
    this.refs = null;
    this.log = (text) => ctx.stdout.write(`${text}\n`);
    // Set when nothing could move for a reason that is everyone's (later()): `auto` ends the
    // run, and the worker tries again on its next round. One video's trouble defers that video.
    this.halted = false;
    // The video the current unit is moving, for a writer still pending on the server (step()).
    this.unitVideo = null;
    // The videos the current unit's loop left alone (stepUnit), which are not at rest (resting).
    this.passedOver = new Set();
    // The owner's lines this run left unanswered because their video was not at rest
    // (discuss.mjs answerScript), by message id, so the log says so once.
    this.heldLines = new Set();
    // The owner's lines on a document whose planner request met a busy service or a rate limit
    // (discuss.mjs answerDocument), by message id: they wait for the next run, and this one goes
    // on with the series work, the drama requests and the scheduled draft.
    this.waitingLines = new Set();
    this.lastAnswer = null;
    // How much of a translation worksheet one model call is asked for (sheet-units.mjs).
    this.unitLimits = { lines: UNIT_LINES, chars: UNIT_CHARS };
  }

  get workBase() {
    return resolveWorkBase({ env: this.ctx.env, root: this.ctx.root, home: this.ctx.home });
  }

  workdir(slug) {
    return resolveWorkdir({ env: this.ctx.env, slug, root: this.ctx.root, home: this.ctx.home });
  }

  /** Every video this worker started, oldest first (auto.json), for the modules beside this one. */
  states() {
    return automatedVideos(this.workBase);
  }

  /** Write a video's auto.json as it stands. */
  persist(state) {
    saveState(this.workdir(state.slug), state);
  }

  /**
   * A speech command the unit runs (tts, dub, check-audio). One that exits 3 because it lost the
   * project's lease, or met a STOP, sets the video aside (fence) before its exit is read as the
   * owner's: a dub is not given up, nothing is blocked, and nothing is written into the project of
   * the producer that holds it now. An answer lost after it was paid for (speechUncertain) keeps
   * its own handling, since setting it aside would buy it again.
   */
  async speech(slug, command) {
    const result = await run(this.ctx, command);
    if (result.code === this.ctx.EXIT.owner && !speechUncertain(result)) this.fence(slug, `recording ${command[0]}`);
    return result;
  }

  /**
   * Put back the script a refused rewrite replaced (discuss.mjs). Only while this step still
   * holds the project's lease; a STOP does not keep it from leaving the last good script.
   */
  restoreVideo(state, source) {
    this.fence(state.slug, "restoring video.json", { stop: false });
    writeFileSync(path.join(docDir(state.slug, this.ctx.root), "video.json"), source);
  }

  /** The skill's reference texts, from the tool's own repository whatever root the docs are under. */
  reference() {
    this.refs ??= references(ROOT);
    return this.refs;
  }

  // The module's helpers as methods, for the compilation module (compilation.mjs) that works
  // on this automation without reaching into the file's private functions.
  saveState(workdir, state) {
    saveState(workdir, state);
  }

  report(state, stage) {
    return report(this.ctx, this.api, state, stage);
  }

  run(command) {
    return run(this.ctx, command);
  }

  lastLine(out, lines = 1) {
    return lastLine(out, lines);
  }

  /** The channel's stance from the settings tab (docs/videos/HANDS-OFF.md §頻道立場); "" while the owner has not written one. */
  get stance() {
    return typeof this.settings.channel_stance === "string" ? this.settings.channel_stance.trim() : "";
  }

  /**
   * The prompt variant of a drama's planner, writer and checker: an episode of a long series has
   * its own (episodeVariant); an explainer (the flat-explainer preset), a one-off or a legacy
   * request, has the question's; any other drama none.
   */
  variantOf(state) {
    const episode = episodeVariant(state);
    if (episode) return episode;
    return state.format === "drama" && state.style_preset === EXPLAINER_PRESET ? "explainer" : null;
  }

  /**
   * Right before a paid request or a write to the video's canonical files: its STOP file, and
   * the lease its unit holds (core/project-lease.mjs, still this process's). Either throws
   * PROJECT_HELD, which move() turns into the video sitting the run out. The slug leaves
   * runSlugs first, so step() does not settle an answer this unit already received: it stays
   * saved under its request key, and the unit after the STOP is gone takes it without paying again.
   */
  fence(slug, what, { stop = true } = {}) {
    const workdir = this.workdir(slug);
    let why = stop && stopRequested(workdir) ? "the project's STOP file holds it" : null;
    if (!why) {
      try {
        // A path outside the video's unit (a discussion of its screenplay) takes the lease here,
        // for the rest of the step (step() lets it go). A slug with no work directory yet (a series
        // document, or a new draft before its first save, which only the first lane makes and
        // under a slug nobody else has) has nothing of a video's to hold.
        const held = this.leases.get(slug) ?? this.stepLeases.get(slug);
        if (held) held.verify();
        else if (existsSync(workdir)) this.stepLeases.set(slug, acquireProjectLease(workdir, { owner: "auto", now: this.ctx.now }));
      } catch (error) {
        if (!(error instanceof ProjectLeaseError)) throw error;
        why = error.message;
      }
    }
    if (!why) return;
    this.runSlugs?.delete(slug);
    throw Object.assign(new AutomationError(`${what} was not sent or written: ${why}`, { code: PROJECT_HELD }), { slug });
  }

  async stage(stage, slug, payload, maxOutputTokens, format = "slides", variant = null, series = null) {
    this.fence(slug, `the ${stage} request`);
    this.runSlugs?.add(slug);
    // The channel's stance (the planner and the writer read it), a binge series' genre section
    // (docs/videos/BINGE.md) and the owner's standing instructions for the stage end the prompt:
    // the tutorial part's for a slides video, the drama part's for a drama
    // (docs/videos/DRAMA-FLOW.md, section 1). The server keeps what was sent, per stage, format
    // and variant, for the owner to read.
    const standing = settingsFor(this.settings, format).instructions?.[stage] ?? "";
    // A translation of a video narrated in another language than zh-TW carries that language as
    // "source_locale" (sourceLocale), and the instructions name the same source the payload shows.
    const source = typeof payload?.source_locale === "string" ? payload.source_locale : null;
    let answer;
    try {
      answer = await this.api.run(stage, slug, instructionsFor(stage, format, standing, variant, this.stance, series, source), payload, maxOutputTokens, format, variant);
    } catch (error) {
      // Sent, and its answer lost: move() stops the video rather than pay for the stage again.
      // Any other refusal or wait names its stage on the card or in the log line too.
      if (error instanceof AutomationError) error.stage ??= stage;
      throw error;
    }
    this.log(`  ${stage}: ${answer.model}, ${answer.input_tokens + answer.output_tokens} tokens; month ${answer.usage.tokens}/${answer.usage.token_budget}`);
    this.lastAnswer = answer.text;
    try {
      return parseAnswer(answer.text);
    } catch (error) {
      const invalid = new AutomationError(`${stage} answered something that is not JSON: ${error.message}`, { code: OUTPUT_INVALID });
      invalid.stage = stage;
      throw invalid;
    }
  }

  /** Save the last stage's answer as it came, so a person can see why it was unusable. */
  keepAnswer(dir, what) {
    if (typeof this.lastAnswer !== "string") return null;
    const name = `${what.replace(/[^a-z0-9-]+/gi, "-")}-${this.ctx.now().toISOString().replace(/[:.]/g, "-")}.txt`;
    mkdirSync(path.join(dir, "answers"), { recursive: true });
    writeFileSync(path.join(dir, "answers", name), this.lastAnswer);
    this.lastAnswer = null;
    return path.join("answers", name);
  }

  /** The voice a document of this format may carry (settledVoice); a compilation is a drama. */
  voice(format = "drama") {
    return settledVoice(settingsFor(this.settings, format).voice);
  }

  /**
   * Nothing moved for a reason that is every video's (the settings, the site's lists, a draft or
   * a series that could not start, the token or the host's tools): end this run. A reason of one
   * video's own defers that video instead (defer).
   */
  later(line) {
    this.halted = true;
    return line;
  }

  /**
   * This video could not move for a reason that passes (a vendor busy, a push or report the site
   * did not take, Jev away, a STOP file between requests): it waits on its own and the lane goes
   * on with the next video. auto.json gets `deferred_until`: DEFER_BASE_MS doubled for each
   * deferral in a row (`defer_count`, which the next visit that ends without trouble clears) up
   * to DEFER_MAX_MS, and no sooner than the server's `retryAfter` (seconds) when it gave one.
   * The server's time is a floor and such a deferral is counted like any other: the API answers a
   * busy vendor with 30 seconds, and a wait that short would try the video every round and reach
   * the limit within the half hour.
   *
   * Waiting has an end. After `limit` deferrals in a row the next one blocks the video instead,
   * with the last line as the reason and kind `deferred:<what>` (or `blocked`: { why, kind }),
   * so the owner reads it on /admin/videos and a retry starts the video at once. From the
   * DEFER_REPORT_FROM-th in a row the site is told with a checklist row (reportDeferred).
   *
   * `everyone` says the trouble is the whole worker's or the site's (everyones: a budget spent
   * until tomorrow, the review store full, a rate limit): the deferral waits, doubles and shows
   * on the card like any other, and neither blocks nor counts toward the limit (`defer_shared`
   * is how many of the row's deferrals were such), since the video has nothing wrong with it and
   * goes on by itself when the trouble is over. Its own trouble in the same row still counts.
   *
   * `backoffMs` sets the wait outright and is not counted: 0 leaves the video for the rest of
   * this run alone (a STOP file: nothing failed). Every lane leaves it for the rest of this run
   * either way. Resolves to the line.
   */
  async defer(state, line, { backoffMs = null, retryAfter = null, what = null, limit = DEFER_LIMIT, blocked = null, everyone = false } = {}) {
    const now = this.ctx.now().getTime();
    if (Number.isFinite(backoffMs) && backoffMs >= 0 && !(Number.isFinite(retryAfter) && retryAfter > 0)) {
      this.skipped.add(state.slug);
      if (backoffMs > 0) state.deferred_until = new Date(now + backoffMs).toISOString();
      else delete state.deferred_until;
      saveState(this.workdir(state.slug), state);
      return backoffMs > 0 ? `${line}; deferred until ${state.deferred_until}` : line;
    }
    const count = Number.isInteger(state.defer_count) && state.defer_count > 0 ? state.defer_count : 0;
    const why = line.startsWith(`${state.slug}: `) ? line.slice(state.slug.length + 2) : line;
    const shared = Math.min(Number.isInteger(state.defer_shared) && state.defer_shared > 0 ? state.defer_shared : 0, count);
    const own = count - shared;
    if (!everyone && own >= limit) return this.block(state, blocked?.why ?? `still could not move after ${own + 1} tries: ${why}`, blocked?.kind ?? `deferred:${what ?? "stage"}`);
    const asked = Number.isFinite(retryAfter) && retryAfter > 0 ? retryAfter * 1000 : 0;
    const wait = Math.min(Math.max(DEFER_BASE_MS * 2 ** count, asked), DEFER_MAX_MS);
    state.defer_count = count + 1;
    if (everyone) state.defer_shared = shared + 1;
    this.skipped.add(state.slug);
    state.deferred_until = new Date(now + wait).toISOString();
    saveState(this.workdir(state.slug), state);
    // A report the site just refused (the retry's acknowledgement) is not followed by another.
    if (state.defer_count >= DEFER_REPORT_FROM && what !== "report") await this.reportDeferred(state, why);
    return `${line}; deferred until ${state.deferred_until}`;
  }

  /**
   * The stage a report that is not a stage's own carries: the one this unit already reported for
   * the state in hand (a stage that reported and then met trouble keeps its stage), else the one
   * /admin/videos shows now.
   */
  shownStage(state) {
    const shown = REPORTED_STAGE.get(state) ?? (this.site ?? []).find((video) => video.slug === state.slug)?.stage;
    // A retry whose acknowledgement has not arrived still reads "blocked" there.
    if (shown === "blocked") return "retrying";
    return typeof shown === "string" && shown ? shown : "waiting";
  }

  /**
   * Tell /admin/videos that this video waits on its own, why and until when: a checklist row
   * with key "deferred" under the stage the page already shows. Best effort: a report the site
   * does not take is a line in the log, never an error, since the deferral itself is saved.
   */
  async reportDeferred(state, why) {
    try {
      await report(this.ctx, this.api, state, this.shownStage(state), { deferred: deferredLabel(state, why) });
      saveState(this.workdir(state.slug), state);
    } catch (error) {
      this.log(`${state.slug}: could not tell the site about the deferral (${error.message}); it is in this log only`);
    }
  }

  /**
   * A visit to this video ended without trouble, whether it moved the video or found it waiting
   * on someone: it read the site, so the deferrals in a row are over, and its writer is no longer
   * pending. Nothing to do for a unit that deferred or blocked it, or that ended the run for a
   * reason of everyone's (later: the site or the token is what failed, so nothing was read
   * without trouble). Only the wait's own fields are taken off what the unit saved, and when the
   * page shows the deferral row and no stage of this unit reported, a report takes it off (best
   * effort, tried again on the next visit).
   */
  async moved(state) {
    this.pendingUntil.delete(state.slug);
    if (this.halted || this.skipped.has(state.slug) || state.status === "blocked") return;
    if (state.defer_count === undefined && state.deferred_until === undefined && !state.deferred_reported) return;
    const workdir = this.workdir(state.slug);
    const saved = readJson(path.join(workdir, STATE_FILE), null);
    if (!saved || saved.slug !== state.slug || saved.status === "blocked") return;
    for (const each of [saved, state]) {
      delete each.defer_count;
      delete each.defer_shared;
      delete each.deferred_until;
    }
    if (state.deferred_reported) {
      try {
        await report(this.ctx, this.api, state, this.shownStage(state));
      } catch (error) {
        this.log(`${state.slug}: could not take the deferral off the page yet (${error.message})`);
      }
    }
    if (state.deferred_reported) saved.deferred_reported = true;
    else delete saved.deferred_reported;
    saveState(workdir, saved);
  }

  /** Whether a video sits this unit out: deferred (auto.json), left for this run, or its writer still running on the server. */
  waiting(state, now = this.ctx.now().getTime()) {
    return this.skipped.has(state.slug) || (this.pendingUntil.get(state.slug) ?? 0) > now || Date.parse(state.deferred_until ?? "") > now;
  }

  /**
   * Whether a video is at rest: no lane is moving it (`busy`), none set it aside in this run, its
   * writer is not still running on the server, and it does not wait on its own (`state` is its
   * auto.json as just read). A step outside a video's own unit that would send a model request
   * for it (a discussion of its screenplay, discuss.mjs) holds off until then. A deferral saved
   * in an earlier round counts: the video is passed over before its unit, so this run never
   * looked its writer up, and a job sent before the deferral (the read of its reviews failed
   * ahead of the lookup, twice in a row) may still be running on the server.
   *
   * Nor is a video its own STOP file holds (movable): its stages are held, and so is its line.
   * And a video this unit's loop left alone (`passedOver`: busy, waiting or held when the loop
   * came to it) is not at rest for the rest of the unit, whatever the clock says now: the loop
   * read the time before it visited the other videos, so a writer's recheck time or a saved wait
   * that ran out during those visits left the video unvisited and its pending job never looked
   * up, and a discussion sent then was a second writer request beside it.
   */
  resting(state, now = this.ctx.now().getTime()) {
    return !this.passedOver.has(state.slug) && this.movable(state, now);
  }

  /** Whether the unit's loop may take a video now: no lane is moving it, it does not sit the unit out (waiting), and no STOP file of its own holds it. */
  movable(state, now) {
    return !this.busy.has(state.slug) && !this.waiting(state, now) && !existsSync(path.join(this.workdir(state.slug), "STOP"));
  }

  /**
   * Whether a discussion of this video's screenplay has an answer still to take (discuss.mjs
   * answerScript): its writer job was still running when an earlier unit or round ended, or its
   * answer is saved and no unit has taken it. The first lane takes it up before the video's own
   * stages (stepUnit), and the other lanes leave the video to it.
   */
  discussionOpen(slug) {
    return (this.api.untakenRuns?.(slug) ?? []).some((saved) => saved.stage === "writer" && SCRIPT_DISCUSSION_VARIANTS.includes(saved.variant));
  }

  /**
   * The videos that sit out on their own right now (waiting), oldest first, for `auto`'s idle
   * line: [{ slug, until }]. `until` is auto.json's `deferred_until`, or when a writer still
   * running on the server is looked up again, whichever is later; null for a video left for
   * this run only (a STOP file between requests, a stage that gave nothing usable).
   */
  deferredVideos(now = this.ctx.now().getTime()) {
    return automatedVideos(this.workBase)
      .filter((state) => ["active", "done"].includes(state.status) && this.waiting(state, now))
      .map((state) => {
        const until = Math.max(Date.parse(state.deferred_until ?? "") || 0, this.pendingUntil.get(state.slug) ?? 0);
        return { slug: state.slug, until: until > now ? new Date(until).toISOString() : null };
      });
  }

  /**
   * A stage gave nothing usable. Keep what it said and end this run, with no lane taking the
   * video up again in it; after the second time in a row the video is blocked, since a third try
   * of the same payload would most likely fail the same way. On 2026-09-25 a writer that kept
   * answering without a script was asked six times in two minutes, about 106,000 subscription
   * tokens, before the worker was stopped by hand.
   */
  async retryLater(state, what, why) {
    const workdir = this.workdir(state.slug);
    state.failures = { ...(state.failures ?? {}), [what]: (state.failures?.[what] ?? 0) + 1 };
    const kept = this.keepAnswer(workdir, what);
    saveState(workdir, state);
    this.halted = true;
    this.skipped.add(state.slug);
    const detail = `${why}${kept ? `; the answer is in ${kept}` : ""}`;
    if (state.failures[what] >= MAX_STAGE_FAILURES) return this.block(state, `${what} failed ${state.failures[what]} times in a row: ${detail}`, `failures:${what}`);
    return `${state.slug}: ${what} gave nothing usable (${detail}); the next run tries once more`;
  }

  /** A stage worked: its count of failures in a row starts again. */
  cleared(state, what) {
    if (state.failures?.[what]) delete state.failures[what];
  }

  /**
   * A stage was sent and its answer never came back (client.mjs RUN_UNCERTAIN): the model may
   * have run, and been paid for, on the server, which keeps no answer to fetch again. Asking on
   * its own could pay twice for the same work, so the video stops for a person and this run
   * ends; the owner's retry on /admin/videos asks once more, and a translation resumes from the
   * units it kept (sheet-units.mjs).
   */
  async unanswered(state, error) {
    this.halted = true;
    this.lastAnswer = null;
    const what = `${error.stage ?? "a stage"}${error.unit ? ` (${error.unit})` : ""}`;
    return this.block(state, `${what} may have run on the server without its answer reaching the worker (${error.why ?? error.message}); it is not asked again until the owner retries`, `uncertain:${error.stage ?? "stage"}`);
  }

  /** One unit of work; returns a line saying what was done, or null when nothing could be. */
  async step() {
    try {
      return await this.stepOnce();
    } finally {
      for (const lease of this.stepLeases.values()) lease.release();
      this.stepLeases.clear();
    }
  }

  async stepOnce() {
    this.runSlugs = new Set();
    this.unitVideo = null;
    let outcome;
    try {
      outcome = await this.stepUnit();
    } catch (error) {
      // A STOP or another producer's lease met outside a video's unit (a discussion): that video
      // sits the run out, nothing sent or written, and the others move.
      if (error instanceof AutomationError && error.code === PROJECT_HELD && error.slug) {
        this.skipped.add(error.slug);
        return `${error.slug}: ${error.message}`;
      }
      if (!(error instanceof AutomationError && error.code === RUN_PENDING)) throw error;
      // The worker's last request for the job failed (client.mjs `why`: its submission, or a
      // look-up of its saved receipt, met a rate limit or a gateway away): the job may well be
      // done, so the line says what failed rather than that the model is still running. Until
      // 2026-10-07 it said "still running" either way, and a finished job whose look-ups were
      // rate-limited read as a model at work.
      const stage = error.stage ?? "writer";
      const what = error.why
        ? `${stage} has not answered yet: the worker's last request to the server for it failed (${[...String(error.why)].slice(0, PENDING_WHY_LENGTH).join("")}); it is asked again next round`
        : `${stage} is still running; its saved receipt will be checked next round`;
      // A video's writer, sent by its own unit or to answer a line on its screenplay (discuss.mjs,
      // which runs outside the unit and names the video on the error): no lane looks the job up
      // again or moves the video within PENDING_RECHECK_MS, the line waits with it (resting), and
      // the other videos move. Until 2026-10-06 a discussion's pending job only ended this lane's
      // run: the video was in no list, so another lane of the same run sent its own writer or
      // verifier request beside the job. Anything else (a series document) has no such list: the
      // run ends.
      const video = this.unitVideo ?? (automatedVideos(this.workBase).some((state) => state.slug === error.slug) ? error.slug : null);
      if (video) {
        this.pendingUntil.set(video, this.ctx.now().getTime() + PENDING_RECHECK_MS);
        return `${video}: ${what}`;
      }
      return this.later(`${error.slug ?? "video"}: ${what}`);
    }
    // Completed answers remain recoverable until their artifacts/state were saved by a unit.
    // A process crash or an exception before this point keeps the same durable receipt.
    await this.api.settleRuns?.([...this.runSlugs]);
    return outcome;
  }

  async stepUnit() {
    if (!this.settings.enabled) return null;
    // What this unit's loop leaves alone, for resting(); a new unit starts with none.
    this.passedOver = new Set();
    // Every video on /admin/videos, the ones this worker did not make included, read afresh
    // each unit: the owner may drop one at any time.
    this.site = await this.api.videos();
    const siteBySlug = new Map(this.site.map((video) => [video.slug, video]));
    // Another lane is moving these: its copy of auto.json is the one that gets saved.
    const free = (state) => !this.busy.has(state.slug);
    if (!this.secondary) {
      const found = await this.bookkeeping(siteBySlug, free);
      if (found) return found;
    }
    const now = this.ctx.now().getTime();
    // A discussion of a screenplay that an earlier unit or round left unfinished (its writer job
    // was still running, or its answer is saved and not yet taken) comes before its video's own
    // stages: the job is the video's writer job too. Until 2026-10-06 the next round moved the
    // video first, so a screenplay the owner had sent back meanwhile was rewritten beside the
    // running job, the discussion's saved request no longer matched the script, and its paid
    // answer was set aside and bought again. When the site hands no line for it (the thread was
    // answered or withdrawn since) the video moves below as usual.
    let discussed = false;
    const videos = automatedVideos(this.workBase).filter((state) => ["active", "done"].includes(state.status));
    if (!this.secondary && videos.some((state) => state.status === "active" && this.movable(state, now) && this.discussionOpen(state.slug))) {
      discussed = true;
      // The loop has not run yet: what it would leave alone at this reading of the clock is not
      // at rest for a line either (resting).
      for (const state of videos) if (!this.movable(state, now)) this.passedOver.add(state.slug);
      const answered = await discussStep(this);
      if (answered) return answered;
    }
    for (const listed of automatedVideos(this.workBase)) {
      if (!["active", "done"].includes(listed.status)) continue;
      // A video another lane is moving, one waiting on its own (defer, a writer still running),
      // which sits this unit out so the next one moves instead of the oldest ending every round,
      // and one its own STOP file holds (the renewal handoff keeps one there until its readback
      // is verified: its stages would stop at once and end the round on it). The owner's drop
      // still reaches a held video above; a retry waits until the file is gone. The work base's
      // STOP file is auto's, between units.
      if (!this.movable(listed, now)) {
        this.passedOver.add(listed.slug);
        continue;
      }
      // The first lane takes an unfinished discussion up (above); until it has, the video's
      // own stages are not another lane's to run.
      if (this.secondary && this.discussionOpen(listed.slug)) continue;
      // A video the owner retried before it had a brief (unplanned) has its topic chosen now,
      // which stays the first lane's, as every new draft's and request's is: on another lane its
      // planner would read the earlier videos while the first lane's draft() reads them too, and
      // both could pick the same article.
      if (this.secondary && listed.unplanned) continue;
      this.busy.add(listed.slug);
      try {
        // The list was read before this loop's first await. While this lane visited the videos
        // ahead, another lane may have finished a unit on this one, saved it and let it go: the
        // copy in hand would run the stage a second time (a verifier paid for twice) and save
        // over what that lane wrote, a block included. Now that the video is held, auto.json is
        // read again, and that is the state this unit moves.
        const state = readJson(path.join(this.workdir(listed.slug), STATE_FILE), null);
        if (!state || state.slug !== listed.slug || !["active", "done"].includes(state.status) || this.waiting(state, now)) {
          this.passedOver.add(listed.slug);
          continue;
        }
        // The project's lease (core/project-lease.mjs) for the whole unit, shared with the media
        // commands the unit runs in this process: a manual recovery or a command run by hand
        // that holds it keeps this video out of the run, with nothing sent or written.
        let lease;
        try {
          lease = acquireProjectLease(this.workdir(listed.slug), { owner: "auto", now: this.ctx.now });
        } catch (error) {
          if (!(error instanceof ProjectLeaseError)) throw error;
          this.log(`${listed.slug}: left alone this run: ${error.message}`);
          this.skipped.add(listed.slug);
          this.passedOver.add(listed.slug);
          continue;
        }
        this.leases.set(listed.slug, lease);
        try {
          // Kept when move() throws, for step(): a writer still pending is this video's alone.
          this.unitVideo = state.slug;
          const done = await this.move(state, siteBySlug);
          if (done) return done;
          this.unitVideo = null;
        } finally {
          this.leases.delete(listed.slug);
          lease.release();
        }
      } finally {
        this.busy.delete(listed.slug);
      }
    }
    if (this.secondary) return null;
    // The owner's lines on a document or a screenplay are answered first, one per round
    // (docs/videos/DRAMA-FLOW.md, section 3): the owner is waiting, and nothing is paid for. A
    // line on the screenplay of a video that is not at rest (resting) is left for a later unit.
    if (!discussed) {
      const answered = await discussStep(this);
      if (answered) return answered;
    }
    // A series in the making comes next (docs/videos/SERIES.md), then the owner's one-off
    // requests from before one-offs became series, then the owner's slides requests, then a
    // scheduled draft, all within the same waiting cap.
    const series = await seriesStep(this);
    if (series) return series;
    // The owner's drama requests come before any scheduled draft, within the same waiting cap.
    if (this.settings.drama?.drama_enabled && this.room()) {
      const request = await this.api.dramaNext();
      if (request) return this.draftDrama(request);
    }
    // Then the owner's slides requests (a site article named on /admin/videos): they skip the
    // draft interval, not the waiting cap. A hand-built api without the call has none.
    if (this.room()) {
      const request = await this.api.slidesNext?.();
      if (request) return this.draftSlides(request);
    }
    if (this.due()) return this.draft();
    return null;
  }

  /** The first lane's bookkeeping before any stage: drops, retries, pasted addresses, compilations. */
  async bookkeeping(siteBySlug, free) {
    const dropped = new Map(this.site.filter((video) => video.dropped_at).map((video) => [video.slug, video]));
    for (const state of automatedVideos(this.workBase)) {
      if (state.status !== "dropped" && dropped.has(state.slug) && free(state)) return this.drop(state, dropped.get(state.slug));
    }
    // A retry belongs to one site request and one local state transition. Remember the request
    // before doing any paid stage so a stale list response or a failed report cannot replay it.
    for (const state of automatedVideos(this.workBase)) {
      const siteVideo = siteBySlug.get(state.slug);
      const request = siteVideo?.retry_request_id;
      if (state.status !== "blocked" || !free(state) || !request || request === siteVideo.retry_acknowledged_id || request === state.retry_request_id) continue;
      if (siteVideo?.dropped_at || stopRequested(this.workdir(state.slug))) continue;
      const currentVideo = readJson(path.join(docDir(state.slug, this.ctx.root), "video.json"), null);
      if (state.policy_hold && state.format && currentVideo?.format && state.format !== currentVideo.format) {
        state.retry_request_id = request;
        return this.block(state, `policy retry refused: auto.json is ${state.format}, video.json is ${currentVideo.format}`);
      }
      if (state.policy_hold?.source_files && JSON.stringify(state.policy_hold.source_files) !== JSON.stringify(this.policySource(state))) {
        state.retry_request_id = request;
        return this.block(state, "policy retry refused: the source changed since the held request; restore its exact source or inspect the retained receipt before resuming");
      }
      // The retry archives or clears the video's saved runs: not while another producer holds the
      // project. The request stays unconsumed and the next round asks again.
      let lease;
      try {
        lease = acquireProjectLease(this.workdir(state.slug), { owner: "auto retry", now: this.ctx.now });
      } catch (error) {
        if (!(error instanceof ProjectLeaseError)) throw error;
        this.log(`${state.slug}: retry waits: ${error.message}`);
        continue;
      }
      try {
        // The kind travels with the retry: `job_gone:<stage>` is what lets the transport set aside
        // a queued or running journal whose job the server no longer has (client.mjs retryRuns).
        await this.api.retryRuns?.(state.slug, { requestId: request, reason: state.blocked ?? "", format: state.format ?? currentVideo?.format ?? "slides", kind: blockedKindOf(state) });
      } catch (error) {
        if (error instanceof AutomationError && error.code === POLICY_HOLD) {
          state.retry_request_id = request;
          return this.policyHold(state, error);
        }
        // The run the owner wants replaced is still on the server: the request stays unconsumed
        // and this video waits for it; the next round asks again. The other videos go on.
        if (error instanceof AutomationError && error.code === RUN_PENDING) {
          this.log(`${state.slug}: retry waits; the saved ${error.stage ?? "writer"} run is still running on the server, its receipt is checked next round`);
          continue;
        }
        // Any other answer of the retry transport (an uncertain saved run, a lookup that failed, a
        // receipt that cannot be read): this video alone is blocked with the reason, and the
        // request is consumed, so the page stops showing the retry as pending and the owner reads
        // why. Until 2026-10-06 the error ended the whole run, every round. A programming error
        // is not the owner's to read: it still ends the run. The kind stays what blocked the video
        // in the first place (read from a legacy reason now, before it is replaced): nothing ran,
        // and that counter is still the one a retry that goes through has to reset.
        if (!(error instanceof AutomationError || error instanceof RunReceiptError)) throw error;
        state.retry_request_id = request;
        return this.block(state, `retry could not verify the saved writer run: ${error.message}`, blockedKindOf(state) ?? "uncertain:writer");
      } finally {
        lease.release();
      }
      state.retry_request_id = request;
      // A language batch can fail after the finished video reached YouTube. Resume
      // only its languages, rather than revisiting the production stages.
      state.status = state.blocked_from_status === "done" ? "done" : "active";
      delete state.blocked_from_status;
      // The counter that blocked it starts again, or the stage would block at the same line. A
      // policy verdict lost under the final cut's quality check is kept by qa until this retry,
      // which is what asks Jev once more (forgetLostPolicy).
      if (resetForRetry(state) === "uncertain:policy") forgetLostPolicy(this.workdir(state.slug));
      this.skipped.delete(state.slug);
      delete state.blocked;
      delete state.blocked_kind;
      delete state.blocked_report_pending;
      delete state.blocked_report_retry_at;
      delete state.policy_hold;
      // The owner's line whose request blocked the video (discuss.mjs answerScript) is sent once
      // more now, like any other line, with a row of deferrals of its own anew; a later block is
      // not this line's.
      delete state.blocked_line;
      delete state.line_defers;
      // From the moment auto.json says "active" another lane could take the video. This lane
      // holds it until the acknowledgement is over, so a deferral saved below is the only copy:
      // without the hold a second lane ran the video's stage while the report was in flight, and
      // the deferral then wrote this lane's older state over what that stage had saved.
      this.busy.add(state.slug);
      try {
        saveState(this.workdir(state.slug), state);
        try {
          await report(this.ctx, this.api, state, "retrying");
          siteVideo.retry_acknowledged_id = request;
        } catch (error) {
          // move() sends the acknowledgement before any stage of this video, which waits; the
          // others go on, unless the site or the token is what failed.
          const line = `${state.slug}: retry saved; could not report it yet (${error.message})`;
          return errorScope(error) === "run" ? this.later(line) : await this.defer(state, line, { what: "report", everyone: Boolean(everyones(error)) });
        }
      } finally {
        this.busy.delete(state.slug);
      }
      break;
    }
    // A failed PUT never resumes media: reconcile only the saved reason. Legacy blocked
    // states have no pending flag, so compare the fresh site checklist as well.
    const unreported = (state) => {
      const siteVideo = siteBySlug.get(state.slug);
      if (state.status !== "blocked" || !state.blocked) return false;
      if (!siteVideo && !state.blocked_report_pending) return false;
      const matches = siteVideo?.stage === "blocked" && siteVideo.checklist?.some((item) => item.key === "blocked" && item.label === blockedLabel(state) && item.done === false);
      if (matches && !state.blocked_report_pending) return false;
      return !(Date.parse(state.blocked_report_retry_at) > this.ctx.now().getTime());
    };
    // Read again once held (holding): the list outlives an earlier video's failed report, and a
    // lane that blocked a video meanwhile may have saved its own report's outcome since and let
    // the video go. Its backoff was written over, and the report sent again at once.
    for (const listed of automatedVideos(this.workBase)) {
      if (!unreported(listed) || !free(listed)) continue;
      if (await this.holding(listed.slug, (state) => unreported(state) && this.reportBlocked(state))) return `${listed.slug}: blocked reason reported`;
      // Continue other videos after a failed report; a stopped video cannot starve them.
    }
    // The owner uploaded a finished video and pasted its address on /admin/videos: the id goes
    // into the script, and the video reads as complete (docs/videos/HANDS-OFF.md).
    const uploaded = new Map(this.site.filter((video) => YOUTUBE_ID.test(video.youtube_video_id ?? "")).map((video) => [video.slug, video.youtube_video_id]));
    const unrecorded = (state) => ["active", "done"].includes(state.status) && uploaded.has(state.slug);
    for (const listed of automatedVideos(this.workBase)) {
      if (!unrecorded(listed) || !free(listed)) continue;
      const recorded = await this.holding(listed.slug, (state) => unrecorded(state) && this.recordVideoId(state, uploaded.get(state.slug)));
      if (recorded) return recorded;
    }
    // A finished compilation the site has not heard about yet (the call failed on the round
    // that finished it): tell it now, or the series stays 合集正在做.
    const untold = (state) => state.status === "done" && state.compilation && !state.compilation_told;
    for (const listed of automatedVideos(this.workBase)) {
      if (!untold(listed) || !free(listed)) continue;
      if (await this.holding(listed.slug, (state) => untold(state) && this.tellCompilationDone(state))) {
        return `${listed.slug}: the site now knows the compilation of ${listed.compilation.series} is done`;
      }
    }
    return null;
  }

  /**
   * `act` on a video's auto.json as read once this lane holds the video, holding it until `act`
   * is over: the bookkeeping's site calls (reportBlocked, recordVideoId, tellCompilationDone)
   * save the video after they await the site. Until 2026-10-07 they held nothing, so a second lane could take
   * the video during the call (a done video's languages) and save its progress, and the copy
   * this lane then saved, read before the call, wrote over it; a loop that lists the videos
   * before its first await could also save a copy another lane had moved on since. Resolves to
   * what `act` does, or null when another lane holds the video or it has no auto.json of its own.
   */
  async holding(slug, act) {
    if (this.busy.has(slug)) return null;
    this.busy.add(slug);
    try {
      const state = readJson(path.join(this.workdir(slug), STATE_FILE), null);
      return state?.slug === slug ? await act(state) : null;
    } finally {
      this.busy.delete(slug);
    }
  }

  /**
   * One video's next stage, or its languages; null when it waits on someone. An error is sorted
   * by errorScope: everyone's ends the run as before, one this video's request will always meet
   * blocks it, and one that passes defers it; either way the next video moves in the same run.
   * A saved job the server no longer has blocks the video as `job_gone:<stage>`, the one block
   * whose retry may set a queued or running journal aside. A visit that ends without trouble,
   * with or without a line, ends the deferrals in a row (moved).
   */
  async move(state, siteBySlug) {
    // If the first acknowledgement of a retry could not reach the site, send it before another stage.
    if (state.retry_request_id && siteBySlug.get(state.slug)?.retry_acknowledged_id !== state.retry_request_id) {
      try {
        await report(this.ctx, this.api, state, "retrying");
      } catch (error) {
        const line = `${state.slug}: retry saved; could not report it yet (${error.message})`;
        return errorScope(error) === "run" ? this.later(line) : this.defer(state, line, { what: "report", everyone: Boolean(everyones(error)) });
      }
    }
    let done = null;
    try {
      if (state.status === "active") done = await this.advance(state);
      // The languages the owner chose after the final cut (docs/videos/LANGUAGES.md), for a
      // video still on its way to YouTube or already there; nothing while a step of its own is due.
      done ??= await this.languages(state);
    } catch (error) {
      if (!(error instanceof AutomationError)) throw error;
      // Its STOP file arrived, or its lease went, during the unit: nothing was sent or written
      // after it, and the video is not blocked or deferred. The run leaves it alone.
      if (error.code === PROJECT_HELD) {
        this.skipped.add(state.slug);
        return `${state.slug}: ${error.message}`;
      }
      if (error.code === OUTPUT_INVALID) return this.retryLater(state, error.stage, error.message);
      return this.requestFailed(state, error);
    }
    await this.moved(state);
    return done;
  }

  /**
   * An AutomationError of a request made for this video, sorted by errorScope: a policy hold
   * parks the project (policyHold); an answer lost after it was sent blocks the video for the
   * owner (unanswered); a saved job the server no longer has blocks it as `job_gone:<stage>`
   * (jobGone, `sends` wording what the retry sends); a refusal this request will always meet
   * blocks it with the reason; one that passes defers it. Trouble that is everyone's ("run") is
   * thrown, and so is a writer still running on the server (RUN_PENDING), which step() sets
   * aside for the run: it neither counts as a deferral nor ends a row of them, since a queue that
   * loses every job before its dispatch (queued, failed, queued again) must still reach the limit
   * and a card. Resolves to the line; `request` names the request in it when the stage alone
   * would not. The video's own stages (move) and the writer's answer to a line on its screenplay
   * (discuss.mjs answerScript) share it: both are this video's requests.
   */
  async requestFailed(state, error, { sends = null, request: named = null } = {}) {
    if (error.code === POLICY_HOLD) return this.policyHold(state, error);
    if (error.code === RUN_UNCERTAIN) return this.unanswered(state, error);
    if (error.code === RUN_PENDING) throw error;
    const scope = errorScope(error);
    if (scope === "run") throw error;
    const request = named ?? (error.stage ? `the ${error.stage} request` : "a request");
    const code = error.code || `HTTP ${error.status}`;
    if (error.gone) return this.jobGone(state, error, sends);
    if (scope === "video") return this.block(state, `the site refused ${request} (${code}): ${error.message}`);
    const retryAfter = Number(error.retry_after);
    return this.defer(state, `${state.slug}: ${request} could not finish (${code}: ${error.message})`, { retryAfter: Number.isFinite(retryAfter) && retryAfter > 0 ? retryAfter : null, what: error.stage ?? "request", everyone: Boolean(everyones(error)) });
  }

  /** errorScope, for the modules flow.mjs imports (discuss.mjs), which cannot import it back. */
  errorScope(error) {
    return errorScope(error);
  }

  /**
   * The lookup of a saved job answered with a settled 4xx (client.mjs durableRun `gone`: no such
   * job under this token after the worker was paired again, or not the receipt's job). Its
   * journal stays where it is, since the old job may still be running under the old token: the
   * video is blocked as `job_gone:<stage>`, and only the owner's retry of that kind sets the
   * journal aside (client.mjs retryRuns), after which the request is sent once. `sends` words
   * what the retry sends for a job that is not the video's own stage (a discussion's).
   */
  jobGone(state, error, sends = null) {
    const stage = error.stage ?? "writer";
    const code = error.code || `HTTP ${error.status}`;
    // The instruction comes before the server's words: the card's label is cut at 120 characters.
    return this.block(state, `saved ${stage} job gone from the server; a retry ${sends ?? `sends the ${stage} stage once more`} (${code}: ${error.message})`, `${JOB_GONE_KIND}${stage}`);
  }

  /** Whether another video may start without passing the owner's cap on drafts waiting on them. */
  room() {
    const active = automatedVideos(this.workBase).filter((state) => state.status === "active").length;
    return active < this.settings.max_waiting_drafts;
  }

  /**
   * Write the YouTube id the site reports into docs/videos/<slug>/video.json (youtube.video_id),
   * the file the worker's docs volume holds, once: a script that already names a video keeps it.
   * `status` then reads the video as on YouTube, and /admin/videos gets the finished checklist.
   */
  async recordVideoId(state, videoId) {
    const file = path.join(docDir(state.slug, this.ctx.root), "video.json");
    if (!existsSync(file)) return null;
    const video = JSON.parse(readFileSync(file, "utf8"));
    if (video.youtube?.video_id) return null;
    atomicWrite(file, `${JSON.stringify({ ...video, youtube: { ...(video.youtube ?? {}), video_id: videoId } }, null, 2)}\n`);
    state.status = "done";
    state.youtube_video_id = videoId;
    saveState(this.workdir(state.slug), state);
    await report(this.ctx, this.api, state, "on YouTube");
    // The owner may paste the address before the worker read the publish approval: the series
    // still has to hear that its compilation is done.
    if (state.compilation) await this.tellCompilationDone(state);
    return `${state.slug}: on YouTube as ${videoId}; video.json records it and the video is complete`;
  }

  /**
   * Tell the site the compilation is done (docs/videos/BINGE.md), once: until it hears, the
   * series page says 合集正在做 and refuses another. A call that fails is made again on a later
   * round (step), so a site that was down for a minute does not leave the series waiting forever.
   */
  async tellCompilationDone(state) {
    if (!state.compilation || state.compilation_told) return false;
    try {
      await this.api.compilationDone(state.compilation.series);
    } catch (error) {
      this.log(`  could not mark the compilation of ${state.compilation.series} done: ${error.message}`);
      return false;
    }
    state.compilation_told = true;
    saveState(this.workdir(state.slug), state);
    return true;
  }

  /** The owner dropped this video on /admin/videos: leave it, files and all. */
  drop(state, video) {
    state.status = "dropped";
    state.dropped = { at: video.dropped_at, note: video.dropped_note ?? "" };
    saveState(this.workdir(state.slug), state);
    return `${state.slug}: the owner dropped it (${state.dropped.note}); the worker leaves it`;
  }

  /** Whether a new draft may start: on, interval passed, not too many waiting on the owner. */
  due() {
    if (!this.room()) return false;
    const last = this.globalState().last_draft_at;
    return !last || this.ctx.now().getTime() - Date.parse(last) >= this.settings.draft_interval_hours * 3600_000;
  }

  /** auto-state.json: what the worker keeps across its videos (the last draft, lost first plans). */
  globalState() {
    return readJson(path.join(this.workBase, GLOBAL_FILE), {}) ?? {};
  }

  saveGlobal(global) {
    atomicWrite(path.join(this.workBase, GLOBAL_FILE), `${JSON.stringify(global, null, 2)}\n`);
  }

  /**
   * A slides video was planned, a scheduled draft or an owner's request: the next scheduled
   * draft waits a whole interval from now, so requested videos take the place of scheduled ones
   * instead of piling on top of them.
   */
  markDrafted() {
    this.saveGlobal({ ...this.globalState(), last_draft_at: this.ctx.now().toISOString() });
  }

  /**
   * The first plan of an owner's request whose answer was lost (draftSlides, draftDrama), kept
   * from the loss until the blocked video that holds it from then on is saved: the site offers
   * the request until its claim goes through, and a claim that fails would otherwise have the
   * next round ask the planner again. Answers { at, why } or null.
   */
  lostPlan(slug) {
    return this.globalState().lost_plans?.[slug] ?? null;
  }

  keepLostPlan(slug, error) {
    const global = this.globalState();
    const now = this.ctx.now();
    const kept = Object.entries(global.lost_plans ?? {}).filter(([, entry]) => now.getTime() - Date.parse(entry?.at) < LOST_PLAN_KEEP_MS);
    this.saveGlobal({ ...global, lost_plans: { ...Object.fromEntries(kept), [slug]: { at: now.toISOString(), why: error.why ?? error.message } } });
  }

  forgetLostPlan(slug) {
    const global = this.globalState();
    if (!global.lost_plans?.[slug]) return;
    delete global.lost_plans[slug];
    if (!Object.keys(global.lost_plans).length) delete global.lost_plans;
    this.saveGlobal(global);
  }

  /**
   * A first brief from the planner (draft, draftSlides, draftDrama, planUnplanned), asked twice at
   * most, the second time told why the first answer could not be used (`check`). A request whose
   * answer was lost after it went out (client.mjs RUN_UNCERTAIN) is not asked again: the planner
   * may have run and been paid for, and the server keeps no answer to fetch. Answers { plan },
   * { problem } or { lost } (the error).
   */
  async firstPlan(slug, payload, check, { maxOutputTokens, format = "slides", variant = null } = {}) {
    let problem = null;
    for (let attempt = 0; attempt < 2; attempt++) {
      let answer;
      try {
        answer = await this.stage("planner", slug, payload(problem ? { previous_problem: problem } : {}), maxOutputTokens, format, variant);
      } catch (error) {
        if (error instanceof AutomationError && error.code === RUN_UNCERTAIN) return { lost: error };
        if (!(error instanceof AutomationError && error.code === OUTPUT_INVALID)) throw error;
        problem = error.message;
        continue;
      }
      problem = check(answer);
      if (!problem) return { plan: answer };
    }
    return { problem };
  }

  /**
   * Every video made or started: the ones in docs/videos, the worker's own drafts, and every video
   * on /admin/videos (the owner's branches and dropped ones too), with the article each retells.
   * A folder in docs/videos is a video only when it holds a video.json or a brief.md; the others
   * (ai-shorts, story-plans, validation and the like) are plans and notes, not videos.
   */
  earlierVideos() {
    const found = new Map();
    const videos = path.join(this.ctx.root, "docs", "videos");
    const dirs = existsSync(videos) ? readdirSync(videos, { withFileTypes: true }).filter((entry) => entry.isDirectory()) : [];
    for (const entry of dirs) {
      const brief = path.join(videos, entry.name, "brief.md");
      const script = path.join(videos, entry.name, "video.json");
      if (!existsSync(script) && !existsSync(brief)) continue;
      const video = readJson(script, null);
      found.set(entry.name, {
        slug: entry.name,
        title: video?.youtube?.title ?? (existsSync(brief) ? titleOf(readFileSync(brief, "utf8")) : ""),
        source_guide: video ? sourceGuideOf(video) : null,
        templates: (video?.scenes ?? []).map((scene) => scene.template),
      });
    }
    for (const state of automatedVideos(this.workBase)) {
      const known = found.get(state.slug);
      const entry = known ?? { slug: state.slug, title: state.title ?? "", source_guide: null, templates: [] };
      entry.source_guide ??= mainGuide(state);
      if (state.status === "dropped") entry.dropped = true;
      found.set(state.slug, entry);
    }
    for (const video of this.site ?? []) {
      const entry = found.get(video.slug) ?? { slug: video.slug, title: video.title ?? "", source_guide: null, templates: [] };
      entry.source_guide ??= video.source_guide ?? null;
      if (video.dropped_at) entry.dropped = true;
      found.set(video.slug, entry);
    }
    return [...found.values()];
  }

  planPayload(extra, earlier = this.earlierVideos(), format = "slides") {
    const refs = this.reference();
    return {
      today: today(this.ctx),
      // A drama's own topic scope (the drama part's), the topics to avoid shared by both.
      scope: settingsFor(this.settings, format).topicScope,
      avoid: this.settings.topic_avoid,
      target_minutes: slidesMinutes(this.settings),
      channel: refs.channel,
      formats: refs.formats,
      script_writing: refs.script_writing,
      earlier_videos: earlier,
      used_guides: [...new Set(earlier.map((video) => video.source_guide).filter(Boolean))],
      ...extra,
    };
  }

  /**
   * Pick a topic and write a brief; the owner chooses an outline next. A brief whose answer was
   * lost leaves a blocked video under the draft's own slug, so the owner sees it on /admin/videos
   * and the planner is not asked again on its own; a retry plans it once more (planUnplanned).
   */
  async draft() {
    const { topics, notes } = await this.api.topics();
    const now = this.ctx.now().toISOString();
    const draftSlug = `draft-${now.slice(0, 16).replace(/[-:T]/g, "")}`;
    const earlier = this.earlierVideos();
    const taken = new Set(earlier.map((video) => video.slug));
    const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
    const { plan, problem, lost } = await this.firstPlan(draftSlug, (extra) => this.planPayload({ topics, topic_notes: notes, ...extra }, earlier), (answer) => planProblem(answer, taken, usedGuides, "slides", this.stance));
    // Written whatever came of it: a failed draft waits for the next interval like a good one.
    this.markDrafted();
    if (lost) return this.unanswered(this.unplannedVideo({ slug: draftSlug, format: "slides", title: `排程草稿 ${now.slice(0, 16).replace("T", " ")} UTC`, source_guide: null }, "draft"), lost);
    if (!plan) {
      const kept = this.keepAnswer(this.workBase, "planner");
      return this.later(`draft: the planner's brief was not usable (${problem}${kept ? `; the answer is in ${kept}` : ""}); trying again after the next interval`);
    }
    const dir = docDir(plan.slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "brief.md"), plan.brief.endsWith("\n") ? plan.brief : `${plan.brief}\n`);
    const state = {
      slug: plan.slug,
      format: "slides",
      title: String(plan.title || titleOf(plan.brief)).slice(0, 200),
      status: "active",
      created_at: this.ctx.now().toISOString(),
      source_guide: plan.source_guide || null,
      source_urls: plan.source_urls.slice(0, 12),
      replans: 0,
      verify_rounds: 0,
      verified: false,
      listener_done: false,
      retakes: 0,
      rewrites: 0,
      notes: [],
    };
    return `draft: ${plan.slug} planned from ${topics.length} topics; ${await this.firstOutline(state)}`;
  }

  /**
   * Save a new video and send its first outline, holding the video the whole time. auto.json
   * says "active" from the save on, so without the hold a second lane could take the video
   * while Jev judges the outline here, submit it again and, when Jev fails it, pay the planner
   * twice for one rewrite.
   */
  async firstOutline(state) {
    this.busy.add(state.slug);
    try {
      saveState(this.workdir(state.slug), state);
      return await this.submitOutline(state);
    } catch (error) {
      // The rewrite's planner (replan, once Jev failed the first outline) lost its answer: the
      // video stops as it would in its own unit (move), instead of leaving the step still active,
      // so that the next round asked Jev and the planner again.
      if (error instanceof AutomationError && error.code === RUN_UNCERTAIN) return await this.unanswered(state, error);
      throw error;
    } finally {
      this.busy.delete(state.slug);
    }
  }

  /**
   * A video whose first plan never came (`unplanned`: "draft", "slides" or "drama"), saved with
   * what the planner is asked again from when the owner retries it (planUnplanned).
   */
  unplannedVideo(fields, kind) {
    return { status: "active", created_at: this.ctx.now().toISOString(), source_urls: [], replans: 0, verify_rounds: 0, verified: false, listener_done: false, retakes: 0, rewrites: 0, notes: [], ...fields, unplanned: kind };
  }

  /** The planner's "requested_guide": the site article the owner asked a slides video of, and their note. */
  requestedGuide(request) {
    return { slug: request.source_guide, title: request.title ?? null, url: siteArticleUrl(request.source_guide, this.ctx.root), note: request.note ?? null };
  }

  /**
   * A slides video of a site article the owner named on /admin/videos: plan it from that article
   * alone, claim the request under the video's slug, and send the outline as a draft's. The
   * planner call has no variant, so the server counts it toward the month's drafts, once under
   * its stable slug. An article that cannot be read now ends the round before anything is paid
   * for or claimed; a planner that fails twice, or one whose answer was lost, leaves a blocked
   * video behind, so the owner sees why on the page instead of a request that never starts (or
   * one planned again every round); the owner's retry plans it once more (planUnplanned).
   */
  async draftSlides(request) {
    const requested = this.requestedGuide(request);
    const runSlug = `slides-${String(request.id).slice(0, 8)}`;
    // A first plan lost on an earlier round before the claim went through (lostPlan): the request
    // is claimed and held now, and the planner is not asked again.
    const before = this.lostPlan(runSlug);
    let plan = null;
    let problem = null;
    let lost = null;
    if (!before) {
      const sources = await readSources(this.read, [requested.url]);
      if (!sources[0]?.ok) return this.later(`slides: the owner's article ${request.source_guide} could not be read (${sources[0]?.error ?? "no page"}); the next round tries again`);
      const earlier = this.earlierVideos();
      const taken = new Set(earlier.map((video) => video.slug));
      // The owner chose the article: an earlier video that used it does not refuse it.
      ({ plan, problem, lost } = await this.firstPlan(runSlug, (extra) => this.planPayload({ topics: [], requested_guide: requested, sources, ...extra }, earlier), (answer) => planProblem(answer, taken, new Set(), "slides", this.stance, null, request.source_guide)));
      if (lost) this.keepLostPlan(runSlug, lost);
      this.markDrafted();
    }
    const slug = plan?.slug ?? runSlug;
    try {
      await this.api.slidesStart(request.id, slug);
    } catch (error) {
      // Cancelled on the page while it was being planned, or its slug taken since: nothing is kept.
      // Only these two codes say so. The client sends the claim again after a lost answer, and
      // the site answers that repeat as it did the first (slides_requests.start_request), so any
      // other refusal is an error to look into, not the owner withdrawing the request.
      if (error instanceof AutomationError && WITHDRAWN_CLAIMS.has(error.code)) {
        this.forgetLostPlan(runSlug);
        return this.later(`slides: the owner's request for ${request.source_guide} could not be claimed (${error.message}); nothing was kept`);
      }
      throw error;
    }
    const state = {
      slug,
      title: String(plan?.title || request.title || titleOf(plan?.brief ?? "") || slug).slice(0, 200),
      status: "active",
      created_at: this.ctx.now().toISOString(),
      source_guide: request.source_guide,
      source_urls: (plan?.source_urls ?? []).slice(0, 12),
      slides_request: { id: request.id, source_guide: request.source_guide, title: request.title ?? null, note: request.note ?? null },
      replans: 0,
      verify_rounds: 0,
      verified: false,
      listener_done: false,
      retakes: 0,
      rewrites: 0,
      // The writer reads these as owner_notes.
      notes: request.note ? [`owner request: ${request.note}`] : [],
      // No brief: the owner's retry plans it (planUnplanned).
      ...(plan ? {} : { unplanned: "slides" }),
    };
    if (lost || before) return this.heldPlan(state, runSlug, lost ?? before);
    if (!plan) {
      const kept = this.keepAnswer(this.workdir(slug), "planner");
      return this.block(state, `the planner could not write a usable brief for the owner's article ${request.source_guide} (${problem}${kept ? `; the answer is in ${kept}` : ""})`);
    }
    const dir = docDir(slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "brief.md"), plan.brief.endsWith("\n") ? plan.brief : `${plan.brief}\n`);
    return `slides: ${slug} planned from the owner's article ${request.source_guide}; ${await this.firstOutline(state)}`;
  }

  /**
   * An owner's request claimed after its first plan's answer was lost (`lost`, the error or the
   * lostPlan entry): the video is blocked for the owner's retry, and the entry that held the
   * request until then is spent once the blocked video is saved.
   */
  async heldPlan(state, runSlug, lost) {
    const line = await this.unanswered(state, { stage: "planner", why: lost.why ?? lost.message, message: lost.message ?? lost.why });
    this.forgetLostPlan(runSlug);
    return line;
  }

  /**
   * Send the outline for review, and say what became of it. With the channel stance written and
   * the switch on, Jev picks first (docs/videos/HANDS-OFF.md §Jev 挑大綱): a pick that clears the
   * thresholds goes up with the review and the site approves it on arrival; one that does not is
   * the planner's note for a rewrite, MAX_REPLANS times in all, after which the outline waits for
   * the owner with the last pick attached, so the review card shows Jev's table. A site whose
   * judge is off (409) means the owner chooses as before; Jev or the site being down defers the
   * video, and a later round asks again; an answer lost on the way back blocks it for the
   * owner's retry (`uncertain:judge`).
   */
  async submitOutline(state) {
    const file = path.join(docDir(state.slug, this.ctx.root), "brief.md");
    const brief = readFileSync(file, "utf8");
    const options = outlineOptions(brief);
    // judgeOutline answers a wait with its reason alone; the error is kept here for its code.
    let trouble = null;
    const judge = {
      judgeOutline: async (body) => {
        try {
          return await this.api.judgeOutline(body);
        } catch (error) {
          trouble = error;
          throw error;
        }
      },
    };
    const verdict = await judgeOutline(judge, state.slug, brief, options);
    // Sent, and the answer lost on the way back: Jev may have judged it and used one of the day's
    // calls, so the video stops for the owner, whose retry asks Jev once more about this brief.
    // Until 2026-10-07 it waited like Jev being away, and Jev was asked again every few minutes,
    // up to seven times, before the video was blocked.
    if (verdict.status === "lost") return this.unanswered(state, Object.assign(trouble, { stage: "judge", unit: "Jev's outline pick" }));
    // Jev or the site away: this outline waits, and the other videos move. Jev's daily calls
    // spent is every outline's until midnight UTC: it waits without counting toward a block.
    if (verdict.status === "later") return this.defer(state, `Jev could not judge the outline (${verdict.reason})`, { what: "judge", everyone: Boolean(everyones(trouble)) });
    if (verdict.pick) {
      state.last_pick = verdict.pick;
      saveState(this.workdir(state.slug), state);
    }
    if (verdict.status === "failed" && state.replans < MAX_REPLANS) return this.replan(state, verdict.pick.note, "Jev");
    await report(this.ctx, this.api, state, "outline approved");
    const { payload, summary } = outlineReview(brief, options, verdict, "（自動產生）");
    await this.api.submit(state.slug, { gate: "outline", content_sha256: await sha256File(file), summary, payload, files: [] });
    if (verdict.status === "passed") return `Jev picked outline ${verdict.pick.choice}; outline sent to /admin/videos`;
    if (verdict.status === "failed") return `Jev found no outline that passes after ${state.replans} rewrites (${verdict.pick.note}); outline sent to /admin/videos for the owner, pick attached`;
    return `outline sent to /admin/videos for the owner (${verdict.reason})`;
  }

  /** What the drama planner and writer get beyond a tutorial's payload. */
  dramaPayload(state) {
    const refs = this.reference();
    const drama = this.settings.drama ?? {};
    return {
      drama: refs.drama,
      drama_example: refs.drama_example,
      drama_brief: refs.drama_brief,
      drama_settings: { style_preset: state.style_preset ?? drama.style_preset ?? "cinematic-3d", voices: drama.character_voice_pool ?? [], subtitle_burn_in: drama.subtitle_burn_in ?? true, music_enabled: drama.music_enabled !== false },
    };
  }

  /**
   * The payload of a drama request's first plan, for the planner's tries (draftDrama, and
   * planUnplanned after the owner's retry): the premise, the owner's title and note, and the
   * site article it retells when there is one, read now.
   */
  async dramaPlanPayload(state, earlier) {
    const request = state.drama_request ?? {};
    const sources = state.source_guide ? await readSources(this.read, [siteArticleUrl(state.source_guide, this.ctx.root)]) : [];
    return (extra) => this.planPayload({ premise: state.premise, title: request.title ?? null, note: request.note ?? null, source_guide: state.source_guide ?? null, sources, target_minutes: [state.target_minutes, state.target_minutes], ...this.dramaPayload(state), ...extra }, earlier, "drama");
  }

  /**
   * An episode the owner asked for on /admin/videos: plan it from the premise, claim the request
   * under the video's slug, and send the outline. A planner that fails twice, or one whose answer
   * was lost, leaves a blocked video behind, so the owner sees why on the page instead of a
   * request that never starts (or one planned again every round); the owner's retry plans it
   * once more (planUnplanned).
   */
  async draftDrama(request) {
    const minutes = episodeMinutes(request.target_minutes, request.style_preset);
    const stateBase = { format: "drama", request_id: request.id, premise: request.premise, style_preset: request.style_preset ?? null, target_minutes: minutes, source_guide: request.source_guide ?? null, drama_request: { title: request.title ?? null, note: request.note ?? null } };
    const runSlug = `drama-${String(request.id).slice(0, 8)}`;
    // As for a slides request (draftSlides): a first plan lost before the claim is not asked again.
    const before = this.lostPlan(runSlug);
    let plan = null;
    let problem = null;
    let lost = null;
    if (!before) {
      const earlier = this.earlierVideos();
      const taken = new Set(earlier.map((video) => video.slug));
      const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
      ({ plan, problem, lost } = await this.firstPlan(runSlug, await this.dramaPlanPayload(stateBase, earlier), (answer) => planProblem(answer, taken, request.source_guide ? new Set() : usedGuides, "drama", this.stance, stateBase.style_preset), { maxOutputTokens: 16_000, format: "drama", variant: this.variantOf(stateBase) }));
      if (lost) this.keepLostPlan(runSlug, lost);
    }
    const slug = plan?.slug ?? runSlug;
    const state = {
      slug,
      title: String(plan?.title || request.title || titleOf(plan?.brief ?? "") || slug).slice(0, 200),
      status: "active",
      created_at: this.ctx.now().toISOString(),
      ...stateBase,
      source_urls: (plan?.source_urls ?? []).slice(0, 12),
      replans: 0,
      verify_rounds: 0,
      verified: false,
      listener_done: false,
      retakes: 0,
      rewrites: 0,
      prompt_fixes: {},
      notes: request.note ? [`owner request: ${request.note}`] : [],
      // No brief: the owner's retry plans it (planUnplanned).
      ...(plan ? {} : { unplanned: "drama" }),
    };
    await this.api.dramaStart(request.id, slug);
    if (lost || before) return this.heldPlan(state, runSlug, lost ?? before);
    if (!plan) {
      const kept = this.keepAnswer(this.workdir(slug), "planner");
      return this.block(state, `the planner could not write a usable brief for the owner's request (${problem}${kept ? `; the answer is in ${kept}` : ""})`);
    }
    const dir = docDir(slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "brief.md"), plan.brief.endsWith("\n") ? plan.brief : `${plan.brief}\n`);
    return `drama: ${slug} planned from the owner's request; ${await this.firstOutline(state)}`;
  }

  /**
   * An episode of a series (docs/videos/SERIES.md), started on the site from the chapter's
   * approved outline: the brief is written from the episode's beats and approved here, since
   * the owner already chose the chapter; series.json beside it carries the cast and the context
   * the writer, the checker and lint read.
   */
  async draftEpisode(request, context, episode) {
    const series = context.series;
    if (series.planning_only) throw new AutomationError("planning-only series cannot be drafted", { code: OUTPUT_INVALID });
    const animeRuntime = hasAnimePolicy(series) ? requireAnimePolicy(series) : null;
    const slug = request.slug;
    // A one-off's story bible stands where the setting book does (docs/videos/DRAMA-FLOW.md,
    // section 2): the site hands it over as "setting", and its one outline is the episode's beats.
    const oneOff = isOneOff(series);
    // The cast as this episode wears it: a character's look that covers the episode stands in for
    // the book's appearance, sheet prompt and voice style (docs/videos/SERIES.md, 換裝與變化).
    const cast = castFrom(context.setting?.body_json, episode.number);
    const production = productionForEpisode(context.setting?.body_json, episode.number);
    const visualTier = production?.profile ? "clips" : series.visual_tier ?? "clips";
    const beats = episode.beats ?? {};
    const state = {
      slug,
      title: String(request.title || (oneOff ? episode.title || series.title : `${series.title} 第 ${episode.number} 集 ${episode.title}`)).slice(0, 200),
      status: "active",
      created_at: this.ctx.now().toISOString(),
      format: "drama",
      request_id: request.id,
      premise: request.premise,
      style_preset: series.style_preset ?? null,
      target_minutes: animeRuntime ? animeRuntime.body_target_seconds / 60 : episodeMinutes(request.target_minutes ?? series.target_minutes, series.style_preset),
      ...(animeRuntime ? { category: "anime", production_policy: series.production_policy, runtime_spec: { ...animeRuntime } } : {}),
      source_guide: request.source_guide ?? null,
      // The binge fields (docs/videos/BINGE.md) travel with a series' episode: the genre section
      // of every prompt, the visual tier lint holds the script to, whether the gates are
      // hands-off. A one-off is no binge series and carries none of them.
      series: {
        slug: series.slug,
        episode: episode.number,
        chapter: episode.chapter_number,
        ...(animeRuntime ? { kind: "series", category: "anime", production_policy: series.production_policy, runtime_spec: { ...animeRuntime }, style_preset: "anime-2d", target_minutes: animeRuntime.body_target_seconds / 60, planned_episodes: series.planned_episodes, open_ended: series.open_ended, closed_ending: beats.closed_ending === true } : {}),
        ...(oneOff
          ? { kind: "one-off" }
          : {
              genre: series.genre ?? "xianxia-bonds",
              lead: series.lead ?? "dual-male",
              visual_tier: visualTier,
              compilation: Boolean(series.compilation),
              hands_off: Boolean(series.hands_off),
            }),
      },
      // An explainer's facts rest on the pages its bible names; the checker reads them.
      source_urls: isExplainerOneOff(series) && Array.isArray(beats.sources) ? beats.sources.filter((url) => /^https:\/\//.test(url)).slice(0, 12) : [],
      replans: 0,
      verify_rounds: 0,
      verified: false,
      listener_done: false,
      retakes: 0,
      rewrites: 0,
      prompt_fixes: {},
      chosen: "A",
      notes: series.note ? [`series note: ${series.note}`] : [],
    };
    const dir = docDir(slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    const episodes = context.episodes ?? [];
    const following = episodes.find((each) => each.number === episode.number + 1);
    writeFileSync(path.join(dir, "series.json"), `${JSON.stringify({
      slug: series.slug,
      episode: episode.number,
      chapter: episode.chapter_number,
      title: episode.title,
      logline: episode.logline,
      characters: cast,
      ...(production ? { production } : {}),
      beats,
      recaps: context.recaps ?? [],
      earlier: episodes.filter((each) => each.number < episode.number).map(({ number, title, logline }) => ({ number, title, logline })),
      next_logline: following?.logline ?? null,
      mysteries: context.mysteries ?? [],
      setting_md: context.setting?.body_md ?? "",
      chapter_md: context.chapter?.body_md ?? "",
      series: { ...(animeRuntime ? { kind: "series", category: "anime", production_policy: series.production_policy, runtime_spec: { ...animeRuntime }, target_minutes: animeRuntime.body_target_seconds / 60, planned_episodes: series.planned_episodes, closed_ending: beats.closed_ending === true } : {}), title: series.title, premise: series.premise, tone: series.tone, aspects: series.aspects, note: series.note, style_preset: series.style_preset, open_ended: series.open_ended, genre: series.genre ?? "xianxia-bonds", lead: series.lead ?? "dual-male", visual_tier: visualTier, compilation: Boolean(series.compilation), hands_off: Boolean(series.hands_off), total_minutes: series.total_minutes ?? null },
      visual_tier: visualTier,
      compilation: Boolean(series.compilation),
      ...(animeRuntime ? { ...state.series, category: "anime", production_policy: series.production_policy, runtime_spec: { ...animeRuntime } } : {}),
    }, null, 2)}\n`);
    writeFileSync(path.join(dir, "brief.md"), episodeBrief(series, episode, cast, beats));
    const workdir = this.workdir(slug);
    writeLocalizationRetention(workdir, { slug, seriesSlug: series.slug, production });
    // Held from the save until the outline's approval is written and reported, as firstOutline
    // holds a new video: a lane that listed it before the approval would submit its outline.
    this.busy.add(slug);
    try {
      saveState(workdir, state);
      await approve({ gate: "outline", docDir: dir, workdir, now: this.ctx.now(), note: oneOff ? "依故事聖經" : `planned by chapter ${episode.chapter_number}'s approved outline` });
      await report(this.ctx, this.api, state, "outline approved");
    } finally {
      this.busy.delete(slug);
    }
    if (oneOff) return `one-off ${series.slug}: ${slug} started from the approved story bible`;
    return `series ${series.slug}: episode ${episode.number} (${slug}) started from the chapter outline`;
  }

  /**
   * The script gate (docs/videos/DRAMA-FLOW.md, section 2): every drama's screenplay is read by
   * the owner, who may discuss it, before any image or clip is paid for. With 「劇本先給我看」
   * (series_script_gate) switched off on the settings tab, the screenplay is approved here. On a
   * hands-off series (docs/videos/BINGE.md) the checker's coverage and the measured timing stand
   * in for the owner: a script that fails the site's rule is fixed by the writer here,
   * MAX_PROMPT_FIX_ROUNDS times, before anything is sent; then it goes up, and the site approves
   * it on arrival when it passes, or leaves it for the owner with the problems on the card when
   * the rounds are spent.
   */
  async scriptGate(state) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const check = readJson(path.join(this.workdir(state.slug), "review", "script-check.json"), null);
    if (state.series && !scriptCheckMatches(check, video)) {
      state.verified = false;
      saveState(this.workdir(state.slug), state);
      return this.verify(state);
    }
    const file = writeScreenplay(dir, video);
    if (!hasAnimePolicy(state) && this.settings.drama?.series_script_gate === false) {
      await approve({ gate: "script", docDir: dir, workdir: this.workdir(state.slug), now: this.ctx.now(), note: "「劇本先給我看」關著，依設定自動核准" });
      return `${state.slug}: screenplay approved by the settings (劇本先給我看 is off)`;
    }
    const review = await this.decision(state, "script", file);
    if (!review) {
      if (state.series?.hands_off) {
        // The craft rows are read on the script itself (drama-craft.md); a long anime keeps to its own policy.
        const craft = hasCast(video) && !isLongAnime(state) ? craftChecks(video, { timeline: estimateTimeline(video) }) : null;
        const verdict = scriptVerdict(check, state.series, craft);
        const rounds = state.prompt_fixes?.script ?? 0;
        if (!verdict.passed && rounds < MAX_PROMPT_FIX_ROUNDS) return this.fixScript(state, verdict.problems.join("；"), "the checker");
      }
      const result = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", "script"]);
      if (result.code !== 0) return this.block(state, `review-push failed: ${lastLine(result.out)}`);
      return `${state.slug}: screenplay sent to /admin/videos`;
    }
    if (review.status === "approved") {
      const unrecorded = await this.pulled(state, "script");
      if (unrecorded) return unrecorded;
      if (review.note) state.notes.push(`script: ${review.note}`);
      saveState(this.workdir(state.slug), state);
      const checker = review.note && /依作品設定自動核准/.test(review.note);
      return `${state.slug}: ${checker ? "the site" : "the owner"} approved the screenplay`;
    }
    if (review.status === "rejected") return this.fixScript(state, review.note ?? "");
    return null;
  }

  /** The screenplay was sent back (by the owner, or the checker on a hands-off series): the writer rewrites from the note, then it is checked again. */
  async fixScript(state, note, by = "the owner") {
    const rounds = state.prompt_fixes?.script ?? 0;
    if (rounds >= MAX_PROMPT_FIX_ROUNDS) return this.block(state, `${by} sent the screenplay back ${rounds + 1} times: ${note}`, "prompt_fixes:script");
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const fix = { kind: "script", targets: [], problems: [note], owner_note: note };
    const answer = isLongAnime(state) ? await this.animeRewrite(state, { fix }, video, "writer", `script-fix-${rounds + 1}`) : await this.stage("writer", state.slug, this.scriptPayload(state, { video, fix, line_ids: this.freshIds(state, video, 40), ...this.draftBudget(state) }), 32_000, state.format, this.variantOf(state), state.series ?? null);
    const problem = await this.saveAndLint(state, answer);
    state.prompt_fixes = { ...(state.prompt_fixes ?? {}), script: rounds + 1 };
    state.notes.push(`script sent back by ${by}: ${note}`);
    state.verified = false;
    state.listener_done = false;
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "writer", `the rewritten screenplay ${problem}`);
    return `${state.slug}: screenplay rewritten after ${by === "the owner" ? "the owner's" : "the checker's"} note (round ${rounds + 1}); it is checked again`;
  }

  /** The compilation of a binge series (docs/videos/BINGE.md): started from the site's job. */
  startCompilation(job) {
    return startCompilation(this, job);
  }

  /** The finished episode's recap, kept on the site for the next episode's writer and checker. */
  async recap(state) {
    const dir = docDir(state.slug, this.ctx.root);
    const info = readJson(path.join(dir, "series.json"), {});
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    try {
      const answer = await this.stage("verifier", state.slug, { video, beats: info.beats ?? {}, previous_recaps: info.recaps ?? [], episode: state.series.episode }, 16_000, state.format, "recap");
      if (typeof answer.recap !== "string" || !answer.recap.trim()) throw new AutomationError("the recap answer has no recap text", { code: OUTPUT_INVALID });
      await this.api.episodeRecap(state.series.slug, state.series.episode, { recap: answer.recap.trim().slice(0, 4000), state: answer.state && typeof answer.state === "object" ? answer.state : {} });
      state.recap_sent = true;
      saveState(this.workdir(state.slug), state);
      return true;
    } catch (error) {
      if (error instanceof AutomationError) {
        this.log(`  recap of episode ${state.series.episode} not kept yet: ${error.message}`);
        return false;
      }
      throw error;
    }
  }

  /** The newest decision on a gate for the current file: {status, choice, note} or null. */
  async decision(state, gate, file) {
    const project = await this.api.reviews(state.slug);
    const sha = existsSync(file) ? await sha256File(file) : null;
    return project?.reviews?.find((review) => review.gate === gate && review.content_sha256 === sha) ?? null;
  }

  async pull(slug) {
    return run(this.ctx, ["review-pull", "--slug", slug]);
  }

  /**
   * `review-pull` once the site approved a gate, and whether the approval reached approvals.json:
   * null when it did, else this video's deferral with what the pull said. Until 2026-10-06 a pull
   * that recorded nothing (the file changed since, the storyboard's checks, the site away) was
   * reported as the approval, and the next unit found the gate open and did the same: one video
   * could spend a run's 40 units on it. `file` is for a gate just pushed, whose review may well be
   * waiting for the owner: nothing to record unless the site says it is approved.
   *
   * What refuses to record an approval is on this machine (the file changed since the push, the
   * episode's context did, an earlier entry of the same file), and the gate is only pushed again
   * when no review matches the file, so most of these do not pass by waiting: after
   * UNRECORDED_LIMIT deferrals in a row the video is blocked as `unrecorded:<gate>` with what the
   * pull said, for a person to push or approve it by hand.
   */
  async pulled(state, gate, file = null) {
    const result = await this.pull(state.slug);
    const places = { gate, docDir: docDir(state.slug, this.ctx.root), workdir: this.workdir(state.slug) };
    const approval = await approvalState(places);
    if (approval.status === "approved") return null;
    if (file && (await this.decision(state, gate, file))?.status !== "approved") return null;
    const said = String(result?.out ?? "").trim().split("\n").filter((line) => line.startsWith(gate)).at(-1) ?? lastLine(String(result?.out ?? ""));
    const detail = `approval ${approval.status}; review-pull exit ${result?.code ?? "?"}${said ? `: ${said}` : ""}`;
    return this.defer(state, `${state.slug}: the ${gate} is approved on the site but not recorded locally (${detail})`, {
      limit: UNRECORDED_LIMIT,
      blocked: { why: `the ${gate} is approved on the site but cannot be recorded locally: ${said || detail}`, kind: `unrecorded:${gate}` },
    });
  }

  /**
   * Stop working on a video and say why on /admin/videos; the owner or a person takes over.
   * `kind` names what blocked it (`prompt_fixes:<kind>`, `replans`, `failures:<stage>`,
   * `media_owner:<command>`, `media_exhausted:<command>`, `uncertain:<stage>`), which is what
   * the owner's retry resets (resetForRetry); a block with none is only retried as it was. So are
   * the kinds that have no counter to reset: `deferred:<what>` (deferrals in a row reached their
   * limit, defer), `unrecorded:<gate>` (pulled) and `job_gone:<stage>` (move), the last of which
   * the retry transport reads (client.mjs retryRuns).
   */
  async block(state, why, kind = null) {
    if (state.status !== "blocked") state.blocked_from_status = state.status;
    state.status = "blocked";
    state.blocked = why;
    if (kind) state.blocked_kind = kind;
    else delete state.blocked_kind;
    // A wait of its own (defer) means nothing once the video waits for the owner, and a retry
    // starts it at once.
    delete state.deferred_until;
    delete state.defer_count;
    delete state.defer_shared;
    state.blocked_report_pending = true;
    saveState(this.workdir(state.slug), state);
    const reported = await this.reportBlocked(state);
    return `${state.slug}: blocked — ${why}${reported ? "" : "; could not report it yet"}`;
  }

  /** The canonical source a policy-held writer must still be bound to before an explicit retry. */
  policySource(state) {
    const dir = docDir(state.slug, this.ctx.root);
    return Object.fromEntries(["brief.md", "video.json", "series.json", "script.md"].map((name) => {
      const file = path.join(dir, name);
      return [name, existsSync(file) ? createHash("sha256").update(readFileSync(file)).digest("hex") : null];
    }));
  }

  /** A settled policy rejection parks only its project; a failed report cannot buy another run. */
  policyHold(state, error) {
    state.policy_hold = { code: error.code, ...error.policy_hold, source_files: state.policy_hold?.source_files ?? this.policySource(state) };
    return this.block(state, `${error.stage ?? error.policy_hold?.stage ?? "writer"} is held by policy (${error.code}): ${error.message}`);
  }

  /**
   * Permanent rejected payloads stop this video, and so does a final cut whose quality check lost
   * Jev's policy verdict on the way back (lostPolicy: exit 3 with the client's RUN_UNCERTAIN code
   * last), until the owner's retry asks Jev once more; any other failed push (the site busy or
   * away, a token it refused, a file the push wants) defers this video alone. A token the site refuses
   * refuses the next unit's video list too, which ends the run. A push that keeps failing (a 409
   * of the site's own, a local refusal) reaches the deferrals' limit and blocks with its line;
   * one that says the trouble is everyone's (the review store full, Jev's budget spent under the
   * final cut's quality check, which prints it above the push's own last lines) does not.
   */
  submissionFailure(state, gate, result) {
    const detail = lastLine(result.out, 2);
    if (result.code === this.ctx.EXIT.lint) return this.block(state, `${gate} submission rejected: ${detail}`);
    // The final cut's quality check sent Jev the policy question and lost the answer (review/sync.mjs
    // qualityCheck, qa.json `policy_lost`): Jev may have judged it and used a call, and qa does not
    // ask again for the same narration, so the video stops for the owner, whose retry asks once more.
    if (lostPolicy(result)) return this.unanswered(state, { stage: "policy", unit: "Jev's policy check", why: lastLine(result.out), message: lastLine(result.out) });
    return this.defer(state, `${state.slug}: could not send the ${gate} for review: ${detail}`, { what: "review-push", everyone: Boolean(everyones(result.out)) });
  }

  async reportBlocked(state) {
    state.blocked_report_pending = true;
    saveState(this.workdir(state.slug), state);
    try {
      await report(this.ctx, this.api, state, "blocked");
      delete state.blocked_report_pending;
      delete state.blocked_report_retry_at;
      saveState(this.workdir(state.slug), state);
      return true;
    } catch (error) {
      state.blocked_report_retry_at = new Date(this.ctx.now().getTime() + BLOCKED_REPORT_BACKOFF_MS).toISOString();
      saveState(this.workdir(state.slug), state);
      this.log(`${state.slug}: could not report blocked reason (${error.message}); retrying the report later`);
      return false;
    }
  }

  /** Move one video on by one step; null when it waits on the owner or cannot move. */
  async advance(state) {
    const { ctx } = this;
    this.fence(state.slug, "the next step");
    const workdir = this.workdir(state.slug);
    const dir = docDir(state.slug, ctx.root);
    // Native silent actions are part of the reviewed story. Refresh their readable artifact
    // before computing gates so a changed action cannot reach another paid media stage.
    const animeScript = path.join(dir, "video.json");
    if (isLongAnime(state) && existsSync(animeScript)) writeScreenplay(dir, JSON.parse(readFileSync(animeScript, "utf8")));
    const status = await pipelineStatus({ slug: state.slug, root: ctx.root, workdir });
    const next = status.next?.id;

    // A compilation (docs/videos/BINGE.md) has its own first steps; the final cut, the upload
    // package and the YouTube id go the same way as any video.
    if (state.compilation) {
      const moved = await advanceCompilation(this, state, next);
      if (moved !== undefined) return moved;
    }
    // A brand story (docs/videos/STORY.md) is written, checked and heard a chapter at a time.
    if (state.story) {
      const moved = await advanceStory(this, state, next);
      if (moved !== undefined) return moved;
    }

    if (next === "outline approved") {
      const review = await this.decision(state, "outline", path.join(dir, "brief.md"));
      if (!review) return lineFor(state.slug, await this.submitOutline(state));
      if (review.status === "approved") {
        const unrecorded = await this.pulled(state, "outline");
        if (unrecorded) return unrecorded;
        state.chosen = review.choice;
        state.notes.push(...(review.note ? [`outline: ${review.note}`] : []));
        saveState(workdir, state);
        // The site approves on arrival when Jev's pick passed; otherwise the owner chose.
        const jev = review.payload?.pick?.passed === true && review.payload.pick.choice === review.choice;
        return `${state.slug}: ${jev ? "Jev" : "the owner"} chose outline ${review.choice}${review.note ? ` (${review.note})` : ""}`;
      }
      if (review.status === "rejected") {
        if (state.replans >= MAX_REPLANS) return this.block(state, `the outline was sent back ${state.replans + 1} times (Jev and the owner together): ${review.note}`, "replans");
        return lineFor(state.slug, await this.replan(state, review.note ?? ""));
      }
      return null;
    }

    // A video whose first plan never came (unplanned) is planned once the owner retries it; any
    // other video without its brief has lost a file, and a person looks.
    if (next === "brief") return state.unplanned ? this.planUnplanned(state) : this.block(state,"brief.md is gone");
    if (next === "script passes lint") return this.write(state);
    // Prompt repairs and resumed workers can reach this point after a saved script
    // changed without changing script.md (for example its spoken form or pauses).
    // Check the evidence before every downstream stage, even after script approval.
    // A brand story has no whole-script report: story.mjs checks it a chapter at a time.
    if (state.series && !state.compilation && !state.story && state.verified) {
      const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
      const check = readJson(path.join(workdir, "review", "script-check.json"), null);
      // A report from before reports named their script has nothing to compare. It is made again
      // only while the script gate is still ahead, where the owner reads it (scriptGate asks for
      // it); an episode already past the gate when the worker learned to bind its reports has an
      // approved screenplay and perhaps paid media, and a checker's rewrite would undo both.
      const gateAhead = status.steps.some((step) => step.id === "script approved" && !step.done);
      const spared = !hasAnimePolicy(state) && scriptCheckUnbound(check) && !gateAhead;
      if (!spared && !scriptCheckMatches(check, video)) state.verified = false;
    }
    // status only knows that verify-1.md exists; the rounds and the listener edit are ours.
    if (!state.verified) return this.verify(state);
    if (!state.listener_done) return this.listen(state);
    // An episode of a series: the owner reads the screenplay before any image or clip is paid for.
    if (next === "script approved") return this.scriptGate(state);

    // The drama's own steps (docs/videos/DRAMA.md): each media stage runs as a command, a failed
    // check goes back to the writer as a prompt fix, and two gates wait on the owner.
    if (next === "look generated") return this.media(state, "look");
    if (next === "look approved") return this.lookGate(state);
    if (next === "keyframes drawn") return this.media(state, "keyframes");
    if (next === "storyboard approved") return this.storyboardGate(state);
    if (next === "clips generated") return this.media(state, "clips");
    if (next === "music generated") return this.media(state, "music");

    if (next === "narration synthesized") {
      const previous = readJson(path.join(workdir, "timeline.json"), null);
      const project = loadProject({ slug: state.slug, root: ctx.root });
      const sameScript = previous?.speech_hash === speechHash(project.doc, project.lexicon);
      // Takes that no longer match stop the video, unless they are the ones a retake made before a
      // STOP file or a service ended it (retakeStopped): the plain tts below binds them without
      // synthesizing anything, and the next round checks them again.
      const resumed = Boolean(sameScript && previous.audio_evidence && audioEvidenceProblems(previous, workdir).length);
      if (resumed && !retakeExplains(state.stopped_retake, previous, workdir)) return this.block(state, "audio evidence no longer matches the saved takes; restore or explicitly retake and review the narration");
      // A refresh binds evidence to the takes on disk and never records. Takes that no longer match
      // what is sent for synthesis (the accent wording changed under them) cannot be bound, and a
      // retry would refuse the same way for ever: those are recorded again by a plain tts, which
      // writes a new timeline, so the narration is reviewed again.
      const refresh = sameScript && !previous.audio_evidence && !staleTakes(project.doc, project.lexicon, workdir).length;
      const result = await this.speech(state.slug, ["tts", "--slug", state.slug, ...(refresh ? ["--refresh-evidence"] : [])]);
      // A STOP file ended it between requests: the takes are saved and the next run continues.
      if (result.code === ctx.EXIT.incomplete) return this.defer(state, `${state.slug}: tts stopped (${lastLine(result.out)}); the next run continues`, { backoffMs: 0 });
      // A service away, the month's characters spent or the speech routes' rate limit (exit 4), as
      // for every other stage: the takes made so far are cached, the next tts goes on from them,
      // and trouble that is everyone's never blocks the video.
      if (result.code === 4) return this.defer(state, `${state.slug}: tts could not finish (${lastLine(result.out)})`, { what: "tts", everyone: Boolean(everyones(result.out)) });
      if (result.code !== 0) return this.block(state,`tts failed: ${result.out.trim().split("\n").at(-1)}`);
      if (state.stopped_retake) {
        delete state.stopped_retake;
        saveState(workdir, state);
      }
      await report(ctx, this.api, state, "narration synthesized");
      return `${state.slug}: narration synthesized${resumed ? " from the takes of the retake that stopped halfway" : ""}`;
    }
    if (next === "narration approved") return this.narration(state);
    if (next === "frames rendered") {
      const channel = ctx.env.VIDEO_BROWSER_CHANNEL ? ["--channel", ctx.env.VIDEO_BROWSER_CHANNEL] : [];
      const result = await run(ctx, ["render", "--slug", state.slug, ...channel]);
      if (result.code !== 0) return this.block(state,`render failed: ${result.out.trim().split("\n").at(-1)}`);
      return `${state.slug}: frames rendered`;
    }
    if (next === "video assembled") {
      const result = await run(ctx, ["assemble", "--slug", state.slug]);
      if (result.code !== 0) return this.block(state,`assemble failed: ${result.out.trim().split("\n").slice(-3).join(" ")}`);
      await report(ctx, this.api, state, "video assembled");
      // The script is final now: the episode's recap goes to the site for the next episode.
      if (episodeVariant(state) && !state.recap_sent) await this.recap(state);
      return `${state.slug}: video assembled`;
    }
    if (next === "captions written") return this.captions(state);
    if (next === "final video approved") return this.gate(state, "final", path.join(workdir, "final.mp4"));
    if (next === "upload package") {
      const result = await run(ctx, ["package", "--slug", state.slug]);
      if (result.code !== 0) return this.block(state,`package failed: ${result.out.trim().split("\n").at(-1)}`);
      return `${state.slug}: upload package written`;
    }
    if (next === "on YouTube") {
      const upload = path.join(workdir, "upload", "metadata.json");
      const review = await this.decision(state, "publish", upload);
      if (!review) {
        const pushed = await run(ctx, ["review-push", "--slug", state.slug, "--gate", "publish"]);
        if (pushed.code !== 0) return this.submissionFailure(state, "publish", pushed);
        return `${state.slug}: publish confirmation sent to /admin/videos`;
      }
      if (review.status === "approved") {
        const unrecorded = await this.pulled(state, "publish");
        if (unrecorded) return unrecorded;
        state.status = "done";
        state.notes.push(...(review.note ? [`publish: ${review.note}`] : []));
        saveState(workdir, state);
        if (state.compilation) {
          await this.tellCompilationDone(state);
        } else if (state.series) {
          try {
            if (episodeVariant(state) && !state.recap_sent) await this.recap(state);
            await this.api.episodeDone(state.series.slug, state.series.episode);
          } catch (error) {
            // The next round of the series waits until this is reported; the log says why.
            this.log(`  could not mark episode ${state.series.episode} done: ${error.message}`);
          }
        } else if (state.request_id) {
          try {
            await this.api.dramaDone(state.request_id);
          } catch (error) {
            // The request reads as done once the video is on YouTube anyway.
            this.log(`  could not mark the drama request done: ${error.message}`);
          }
        } else if (state.slides_request?.id) {
          try {
            await this.api.slidesDone(state.slides_request.id);
          } catch (error) {
            // The same: the site derives done from the YouTube id it is given later.
            this.log(`  could not mark the slides request done: ${error.message}`);
          }
        }
        return `${state.slug}: the upload is confirmed${review.note ? ` (${review.note})` : ""}; the owner uploads it in YouTube Studio and pastes the address on /admin/videos`;
      }
      if (review.status === "rejected") return this.block(state,`the owner sent the upload back: ${review.note}`);
      return null;
    }
    if (!next) {
      state.status = "done";
      saveState(workdir, state);
      return `${state.slug}: done`;
    }
    return null;
  }

  /**
   * The first brief of a video that has none (`unplanned`): its answer was lost, or the planner
   * gave nothing usable twice, and the owner retried it. The planner is asked as the first time
   * was (a scheduled draft's topics, the owner's article, the owner's premise), under the
   * video's own slug, which the site already holds (the request's claim, the card), whatever slug
   * it answers. A lost answer stops the video again (move), and nothing usable twice blocks it
   * with the planner's problem; both wait for the next retry.
   */
  async planUnplanned(state) {
    const earlier = this.earlierVideos().filter((video) => video.slug !== state.slug);
    const taken = new Set(earlier.map((video) => video.slug));
    const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
    const own = (answer) => ({ ...answer, slug: state.slug });
    let ask;
    if (state.unplanned === "slides") {
      const requested = this.requestedGuide(state.slides_request);
      const sources = await readSources(this.read, [requested.url]);
      if (!sources[0]?.ok) return this.defer(state, `${state.slug}: the owner's article ${requested.slug} could not be read (${sources[0]?.error ?? "no page"})`, { what: "planner" });
      ask = { payload: (extra) => this.planPayload({ topics: [], requested_guide: requested, sources, ...extra }, earlier), check: (answer) => planProblem(own(answer), taken, new Set(), "slides", this.stance, null, requested.slug) };
    } else if (state.unplanned === "drama") {
      ask = { payload: await this.dramaPlanPayload(state, earlier), check: (answer) => planProblem(own(answer), taken, state.source_guide ? new Set() : usedGuides, "drama", this.stance, state.style_preset ?? null), options: { maxOutputTokens: 16_000, format: "drama", variant: this.variantOf(state) } };
    } else {
      const { topics, notes } = await this.api.topics();
      ask = { payload: (extra) => this.planPayload({ topics, topic_notes: notes, ...extra }, earlier), check: (answer) => planProblem(own(answer), taken, usedGuides, "slides", this.stance) };
    }
    const { plan, problem, lost } = await this.firstPlan(state.slug, ask.payload, ask.check, ask.options);
    if (lost) throw lost;
    if (!plan) {
      const kept = this.keepAnswer(this.workdir(state.slug), "planner");
      return this.block(state, `the planner could not write a usable brief again (${problem}${kept ? `; the answer is in ${kept}` : ""})`);
    }
    const dir = docDir(state.slug, this.ctx.root);
    mkdirSync(dir, { recursive: true });
    writeFileSync(path.join(dir, "brief.md"), plan.brief.endsWith("\n") ? plan.brief : `${plan.brief}\n`);
    state.title = String(plan.title || titleOf(plan.brief) || state.title).slice(0, 200);
    state.source_urls = plan.source_urls.slice(0, 12);
    if (state.unplanned === "draft") state.source_guide = plan.source_guide || null;
    delete state.unplanned;
    saveState(this.workdir(state.slug), state);
    return lineFor(state.slug, `planned after the owner's retry; ${await this.submitOutline(state)}`);
  }

  /**
   * Rewrite the brief from a note — the owner's when they sent the outline back, Jev's when no
   * option passed (`by`) — then send it again; both count toward MAX_REPLANS.
   */
  async replan(state, note, by = "the owner") {
    const dir = docDir(state.slug, this.ctx.root);
    const previous = readFileSync(path.join(dir, "brief.md"), "utf8");
    const earlier = this.earlierVideos().filter((video) => video.slug !== state.slug);
    const taken = new Set(earlier.map((video) => video.slug));
    const usedGuides = new Set(earlier.map((video) => video.source_guide).filter(Boolean));
    const drama = state.format === "drama";
    // An owner's slides request keeps its article through every re-plan (draftSlides): no topics.
    const requested = state.slides_request ?? null;
    const { topics } = drama || requested ? { topics: [] } : await this.api.topics();
    if (drama) state.target_minutes = hasAnimePolicy(state) ? requireAnimePolicy(state.series).body_target_seconds / 60 : episodeMinutes(state.target_minutes, state.style_preset);
    const extra = drama
      ? { premise: state.premise, target_minutes: [state.target_minutes, state.target_minutes], source_guide: state.source_guide, ...this.dramaPayload(state) }
      : { topics, ...(requested ? { requested_guide: this.requestedGuide(requested) } : {}) };
    const answer = await this.stage("planner", state.slug, this.planPayload({ ...extra, owner_note: note, sent_back_by: by === "Jev" ? "jev" : "owner", previous_brief: previous, slug: state.slug }, earlier, state.format), 16_000, state.format, drama ? this.variantOf(state) : null);
    const chosen = (drama && state.source_guide) || requested;
    const problem = planProblem({ ...answer, slug: state.slug }, taken, chosen ? new Set() : usedGuides, state.format, this.stance, state.style_preset ?? null, requested?.source_guide ?? null);
    state.replans += 1;
    state.notes.push(`outline sent back by ${by}: ${note}`);
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "planner", `the re-planned brief was not usable (${problem})`);
    this.cleared(state, "planner");
    writeFileSync(path.join(dir, "brief.md"), answer.brief.endsWith("\n") ? answer.brief : `${answer.brief}\n`);
    state.source_urls = (answer.source_urls ?? state.source_urls).slice(0, 12);
    state.source_guide = requested?.source_guide ?? answer.source_guide ?? state.source_guide;
    saveState(this.workdir(state.slug), state);
    return `brief rewritten after ${by === "Jev" ? "Jev's" : "the owner's"} note (round ${state.replans}); ${await this.submitOutline(state)}`;
  }

  scriptPayload(state, extra) {
    const refs = this.reference();
    const lexicon = readJson(lexiconFile(this.ctx.root), { terms: {} });
    const drama = state.format === "drama";
    if (drama) state.target_minutes = hasAnimePolicy(state) ? requireAnimePolicy(state.series).body_target_seconds / 60 : episodeMinutes(state.target_minutes, state.style_preset);
    return {
      today: today(this.ctx),
      slug: state.slug,
      voice: settingsFor(this.settings, state.format).voice,
      source_guide: state.source_guide,
      target_minutes: drama ? [state.target_minutes, state.target_minutes] : slidesMinutes(this.settings),
      ...(hasAnimePolicy(state) ? { category: "anime", production_policy: state.production_policy, runtime_spec: state.runtime_spec } : {}),
      lexicon: Object.keys(lexicon.terms),
      script_writing: refs.script_writing,
      channel: refs.channel,
      minimal: refs.minimal,
      showcase: refs.showcase,
      owner_notes: state.notes,
      ...(drama ? this.dramaPayload(state) : {}),
      ...(state.series ? this.seriesPayload(state) : {}),
      ...extra,
    };
  }

  /** What an episode of a series adds for the writer and the checker: series.json's context. */
  seriesPayload(state) {
    const info = readJson(path.join(docDir(state.slug, this.ctx.root), "series.json"), null);
    if (!info) return {};
    // The approved book stays intact on disk. Its generated whole-series appendix
    // repeats future episode direction; each model receives that only through the
    // current episode's production payload. Keep owner notes outside the markers.
    const settingMd = info.production
      ? (info.setting_md ?? "").replace(/<!-- BEGIN GENERATED PRODUCTION DIRECTION -->[\s\S]*?<!-- END GENERATED PRODUCTION DIRECTION -->/g, "")
      : info.setting_md ?? "";
    return {
      series: { ...(info.series ?? {}), ...(hasAnimePolicy(state) ? state.series : {}), slug: state.series.slug, episode: state.series.episode, chapter: state.series.chapter, title_of_episode: info.title, logline: info.logline },
      series_reference: this.reference().series,
      cast: info.characters ?? [],
      ...(info.production ? { production: info.production } : {}),
      setting_md: settingMd,
      chapter_md: info.chapter_md ?? "",
      beats: info.beats ?? {},
      recaps: info.recaps ?? [],
      earlier_episodes: info.earlier ?? [],
      next_logline: info.next_logline ?? null,
      mysteries: info.mysteries ?? [],
    };
  }

  /** A stage's video.json as it is saved: the owner's settings and the series' cast over what the model returned. */
  settled(state, video) {
    const info = state.series ? readJson(path.join(docDir(state.slug, this.ctx.root), "series.json"), {}) : null;
    const cast = info ? info.characters ?? [] : null;
    const settledVideo = settle(video, { slug: state.slug, settings: this.settings, sourceGuide: state.source_guide, root: this.ctx.root, format: state.format, series: state.series ?? null, cast, stylePreset: state.style_preset ?? null, production: info?.production ?? null });
    // The storytelling register's pause beats are the tool's (register.mjs setPauseBeats): set on
    // every save of a script whose prompts carry the register, before lint, whichever stage wrote it.
    return this.usesRegister(state) ? setPauseBeats(settledVideo) : settledVideo;
  }

  /** Rewrite/generate a long anime through durable bounded acts, including repairs and listening. */
  async animeRewrite(state, extra, existingVideo = null, stage = "writer", operation = "write") {
    const source = this.scriptPayload(state, extra);
    delete source.video;
    delete source.line_ids;
    return writeAnimeActs({
      workdir: this.workdir(state.slug), source, existingVideo, operation,
      freshIds: (count, taken) => this.freshIds(state, { scenes: [{ lines: [...taken].map((id) => ({ id })) }] }, count),
      stage: (payload, maxTokens) => this.stage(stage, state.slug, payload, maxTokens, "drama", "anime-act", state.series),
    });
  }

  /** Whether a video's planner, writer and listener read REGISTER_RULES (prompts.mjs INSTRUCTIONS): a slides video without a variant. */
  usesRegister(state) {
    return state.format !== "drama" && !state.story && this.variantOf(state) === null;
  }

  /**
   * Whether the saved script is the candidate the checker returned. The candidate is compared
   * as saveAndLint saves it, so an answer that lists the voice's keys or the cast in another
   * order, or leaves the voice out, is still the script that was saved; a candidate too broken
   * to settle or hash is one lint had repaired, and is not.
   */
  checkedIsSaved(state, candidate, saved) {
    try {
      return scriptCheckMatches(scriptCheckBinding(this.settled(state, candidate)), saved);
    } catch {
      return false;
    }
  }

  /** Save a stage's video.json and lexicon terms, then fix lint errors with the writer, up to 3 times. */
  async saveAndLint(state, answer) {
    const dir = docDir(state.slug, this.ctx.root);
    let current = answer;
    for (let fix = 0; ; fix++) {
      if (!current?.video || typeof current.video !== "object") return "the answer has no video object";
      this.fence(state.slug, "saving video.json");
      writeVideo(dir, this.settled(state, current.video));
      const added = mergeLexicon(this.ctx.root, current.lexicon_additions);
      if (added.length) state.lexicon_added = [...new Set([...(state.lexicon_added ?? []), ...added])];
      if (this.api.adoptRuns) {
        // A rewrite may start another durable operation before this unit returns. Bind the
        // completed answer to saved output now so a restart can poll that next operation.
        saveState(this.workdir(state.slug), state);
        const files = [path.join(dir, "video.json"), lexiconFile(this.ctx.root), path.join(this.workdir(state.slug), "auto.json")];
        const artifacts = await Promise.all(files.filter(existsSync).map(async (file) => ({ path: file, sha256: await sha256File(file) })));
        await this.api.adoptRuns(state.slug, { artifacts });
      }
      const errors = lintErrors(this.ctx, state.slug);
      if (!errors.length) {
        if (isLongAnime(state)) writeScreenplay(dir, JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8")));
        return null;
      }
      if (fix >= MAX_LINT_FIXES) return `lint still fails after ${MAX_LINT_FIXES} fixes: ${errors.slice(0, 3).join("; ")}`;
      const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
      current = isLongAnime(state) ? await this.animeRewrite(state, { lint_errors: errors }, video, "writer", `lint-${fix + 1}`) : await this.stage("writer", state.slug, this.scriptPayload(state, { video, lint_errors: errors, line_ids: this.freshIds(state, video, 40), ...this.draftBudget(state) }), 32_000, state.format, this.variantOf(state), state.series ?? null);
    }
  }

  /**
   * Run one of the drama's media stages. Exit 1 means the checks failed some sheets, keyframes or
   * clips: the writer fixes their prompts and the stage runs again next round. Exit 3 needs the
   * owner (the cap, a setting, a key) and blocks the video with the reason on /admin/videos; exit
   * 4 is a vendor or the budget server-side, tried again next round; anything else blocks.
   */
  async media(state, command) {
    const { ctx } = this;
    const channel = ["look", "keyframes"].includes(command) && ctx.env.VIDEO_BROWSER_CHANNEL ? ["--channel", ctx.env.VIDEO_BROWSER_CHANNEL] : [];
    // The seeds an owner retry moved this stage to (resetForRetry), once the server stopped
    // answering for the seeds before them.
    const offset = state.seed_offsets?.[command];
    const seedOffset = SEED_OFFSET_COMMANDS.has(command) && Number.isInteger(offset) && offset > 0 ? ["--seed-offset", String(offset)] : [];
    this.fence(state.slug, command);
    const result = await run(ctx, [command, "--slug", state.slug, ...channel, ...seedOffset]);
    if (result.code === 0) {
      // A STOP that came during the command: an exit 0 is not recorded as done (a stage that
      // stopped exits 0 too). Other exits keep their own STOP handling below.
      this.fence(state.slug, `recording ${command}`);
      this.cleared(state, command);
      delete state.prompt_fixes?.[command];
      // A picture kept with the judge's remarks (acceptBestPictures) that a rewritten prompt had
      // drawn again since is a judged picture now, not a kept one.
      if (command === "keyframes" && state.accepted_pictures?.length) {
        const manifest = readJson(path.join(this.workdir(state.slug), ARTIFACTS.keyframes), null);
        state.accepted_pictures = state.accepted_pictures.filter((picture) => Array.isArray(manifest?.shots?.[picture.id]?.accepted_with_problems));
        if (!state.accepted_pictures.length) delete state.accepted_pictures;
      }
      // The stage is through its seeds: a later rerun (a storyboard sent back, say) starts at
      // seeds 1 to 3 again, with other prompts.
      delete state.seed_offsets?.[command];
      saveState(this.workdir(state.slug), state);
      await report(ctx, this.api, state, `${command} done`);
      return `${state.slug}: ${command} done`;
    }
    if (result.code === 1 && FIX_SOURCES[command]) return this.fixPrompts(state, command, {});
    if (result.code === 3) {
      // The command lost the project's lease, or met a STOP, while it ran: the video sits the run
      // out, as fence() sets it aside anywhere else, rather than waiting on the owner.
      this.fence(state.slug, `recording ${command}`);
      // The server's attempts for a request are spent (media/client.mjs EXHAUSTED_CODES): the
      // owner's retry moves the stage to other seeds, where a cap or a setting it leaves as it
      // is. Only the reason the owner reads (the last line) says which: a run that logged a
      // spent seed on its way to the cap stopped for the cap.
      const reason = lastLine(result.out);
      const kind = /video_media_job_exhausted|已經失敗 \d+ 次/.test(reason) ? `media_exhausted:${command}` : `media_owner:${command}`;
      return this.block(state, `${command} needs the owner: ${reason}`, kind);
    }
    if (result.code === 4) {
      const said = lastLine(result.out);
      const line = `${state.slug}: ${command} could not finish (${said})`;
      // A STOP file is not a failure: music has no handler of its own for it and exits 4 with the
      // stage's "stopped by the STOP file" line (media/stages.mjs stoppedError), as does any stage
      // the file reached between requests. The video is left for this run and nothing is counted
      // or saved as a wait, like a tts or a check the file ended.
      if (stopRequested(this.workdir(state.slug)) || said.startsWith("stopped ")) return this.defer(state, line, { backoffMs: 0 });
      // A vendor or the server's budget: this video's stage waits, the other videos move.
      return this.defer(state, line, { what: command, everyone: Boolean(everyones(result.out)) });
    }
    // An incomplete exit (6) is the command's STOP check (media/stages.mjs mayWriteProject): the
    // video waits for the next run, as a stopped tts does, even when the file is gone by now.
    if (result.code === ctx.EXIT.incomplete) return this.defer(state, `${state.slug}: ${command} stopped (${lastLine(result.out)}); the next run continues`, { backoffMs: 0 });
    this.fence(state.slug, `recording ${command}`);
    return this.block(state, `${command} failed: ${lastLine(result.out, 2)}`);
  }

  /** The ids a stage left for a prompt fix, with what the judge or the checks said about each. */
  failedTargets(state, kind) {
    const source = FIX_SOURCES[kind];
    const manifest = readJson(path.join(this.workdir(state.slug), source.manifest), null);
    const targets = [];
    for (const [id, entry] of Object.entries(manifest?.[source.entries] ?? {})) {
      if (!entry?.needs_review) continue;
      const problems = entry.problems ?? [...new Set((entry.candidates ?? entry.takes ?? []).flatMap((take) => take.judge?.problems ?? take.qc?.problems ?? []))];
      // How long this shot's prompt may be for the image model (keyframes.mjs): the writer is
      // told the number, since a prompt it only makes fuller is refused again on every seed.
      const budget = typeof entry.prompt_budget_chars === "number" ? { prompt_budget_chars: entry.prompt_budget_chars } : {};
      targets.push({ id, problems, ...budget });
    }
    return targets;
  }

  /**
   * Hand failed sheets, keyframes or clips (or a gate the owner sent back) to the writer as a
   * prompt fix, at most MAX_PROMPT_FIX_ROUNDS times per kind; then the video waits for a person.
   */
  async fixPrompts(state, kind, { targets = null, ownerNote = null }) {
    // A story's fix is a patch of the named shots alone (story.mjs).
    if (state.story) return fixStoryPrompts(this, state, kind, { targets, ownerNote });
    this.fence(state.slug, `the ${kind} prompt fix`);
    const workdir = this.workdir(state.slug);
    const found = targets ?? this.failedTargets(state, kind);
    const what = FIX_SOURCES[kind]?.what ?? "shot";
    const summary = found.map((target) => `${target.id}: ${(target.problems ?? []).join("; ") || "failed"}`).join(" | ") || ownerNote || "no detail";
    const rounds = state.prompt_fixes?.[kind] ?? 0;
    // A kind whose every seed the server stopped answering for (the fixes did not change the
    // request enough) is retried on other seeds; any other, with its rounds given back.
    const blockedKind = /video_media_job_exhausted|已經失敗 \d+ 次/.test(summary) ? `media_exhausted:${kind}` : `prompt_fixes:${kind}`;
    if (rounds >= MAX_PROMPT_FIX_ROUNDS) {
      // Illustrated slides keep the judge's best take of each failing shot and go on to the cut,
      // which the owner reviews; a drama's pictures, and a storyboard the owner sent back, wait here.
      const kept = kind === "keyframes" && !ownerNote ? await this.acceptBestPictures(state, found, rounds) : null;
      return kept ?? this.block(state, `${kind} still fails after ${rounds} prompt fixes (${summary})`, blockedKind);
    }
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    if (state.format && video.format && state.format !== video.format) return this.block(state, `prompt repair format conflicts: auto.json is ${state.format}, video.json is ${video.format}`);
    // Historical teaching drafts omit format. Bind their repair to the saved script,
    // while an explicit drama retains its own settings and policy checks.
    state.format ??= video.format ?? "slides";
    saveState(workdir, state);
    // The tightest budget among the targets that carry one; each target keeps its own.
    const budgets = found.map((target) => target.prompt_budget_chars).filter((value) => typeof value === "number");
    const fix = { kind, targets: found, problems: found.flatMap((target) => target.problems ?? []), owner_note: ownerNote, ...(budgets.length ? { prompt_budget_chars: Math.min(...budgets) } : {}) };
    const answer = isLongAnime(state) ? await this.animeRewrite(state, { fix }, video, "writer", `prompt-${kind}-${rounds + 1}`) : await this.stage("writer", state.slug, this.scriptPayload(state, { video, fix, line_ids: this.freshIds(state, video, 40), ...this.draftBudget(state) }), 32_000, state.format ?? "slides", this.variantOf(state), state.series ?? null);
    const problem = await this.saveAndLint(state, answer);
    if (problem) return this.retryLater(state, "writer", `the ${kind} fix ${problem}`);
    this.cleared(state, "writer");
    state.prompt_fixes = { ...(state.prompt_fixes ?? {}), [kind]: rounds + 1 };
    if (ownerNote) state.notes.push(`${kind} sent back: ${ownerNote}`);
    saveState(workdir, state);
    return `${state.slug}: ${kind} prompts fixed (round ${rounds + 1}) for ${found.map((target) => target.id).join(", ") || what}; ${kind} runs again next`;
  }

  /**
   * Once the prompt fixes are spent, illustrated slides keep the judge's best take of every shot
   * still failing (media/keyframes.mjs --accept-best; the owner's decision of 2026-10-06: a video
   * no longer blocks on its pictures) and go on to the cut, which `gate()` sends for the owner's
   * manual review with the kept pictures listed (review/sync.mjs). Returns the line, or null when
   * this is not such a video, or a failing shot has no picture at all (every seed refused: that
   * one still needs a prompt, and the video waits as before).
   */
  async acceptBestPictures(state, found, rounds) {
    const workdir = this.workdir(state.slug);
    const video = readJson(path.join(docDir(state.slug, this.ctx.root), "video.json"), null);
    if (!video || !illustrated(video) || isLongAnime(state)) return null;
    const manifest = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
    const ids = found.map((target) => target.id);
    if (!ids.length || !ids.every((id) => manifest?.shots?.[id]?.file)) return null;
    const channel = this.ctx.env.VIDEO_BROWSER_CHANNEL ? ["--channel", this.ctx.env.VIDEO_BROWSER_CHANNEL] : [];
    this.fence(state.slug, "keeping the best pictures");
    const result = await run(this.ctx, ["keyframes", "--slug", state.slug, ...channel, "--accept-best", ids.join(",")]);
    this.fence(state.slug, "recording the kept pictures");
    // Stopped by its own STOP check (exit 6): the pictures are kept on the next run, not blocked.
    if (result.code === this.ctx.EXIT.incomplete) return this.defer(state, `${state.slug}: keeping the best pictures stopped (${lastLine(result.out)}); the next run continues`, { backoffMs: 0 });
    if (result.code !== 0) return this.block(state, `keyframes could not keep the pictures after ${rounds} prompt fixes: ${lastLine(result.out)}`, "prompt_fixes:keyframes");
    const pictures = found.map((target) => ({ id: target.id, problems: target.problems ?? [] }));
    state.accepted_pictures = [...(state.accepted_pictures ?? []).filter((picture) => !ids.includes(picture.id)), ...pictures];
    // The rounds were spent on these pictures: a prompt the owner rewrites later gets its own.
    delete state.prompt_fixes?.keyframes;
    this.cleared(state, "keyframes");
    state.notes.push(`keyframes: ${ids.length} pictures kept with the judge's remarks after ${rounds} prompt fixes (${ids.join(", ")}); the final cut goes to the owner`);
    saveState(workdir, state);
    return `${state.slug}: ${ids.length} pictures kept with the judge's remarks after ${rounds} prompt fixes; the final cut goes to the owner`;
  }

  /**
   * The look gate: one review per character. Nothing sent yet for these sheets: send them. Every
   * character approved: record the choice and the approval. One sent back: the writer rewrites
   * that character and the sheets are drawn again.
   */
  async lookGate(state) {
    const workdir = this.workdir(state.slug);
    const file = path.join(workdir, ARTIFACTS.characters);
    const manifest = readJson(file, null);
    if (!manifest?.characters) return this.block(state, "characters/manifest.json is gone; run look again");
    const project = await this.api.reviews(state.slug);
    const sha = await sha256File(file);
    const reviews = (project?.reviews ?? []).filter((review) => review.gate === "look" && review.content_sha256 === sha);
    if (!reviews.length) {
      const pushed = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", "look"]);
      if (pushed.code !== 0) return this.submissionFailure(state, "look", pushed);
      return `${state.slug}: character sheets sent to /admin/videos`;
    }
    const rejected = reviews.filter((review) => review.status === "rejected");
    if (rejected.length) {
      const targets = rejected.map((review) => ({ id: review.subject, problems: review.note ? [review.note] : [] }));
      return this.fixPrompts(state, "look", { targets, ownerNote: rejected.map((review) => `${review.subject}: ${review.note ?? ""}`).join("; ") });
    }
    const approved = new Set(reviews.filter((review) => review.status === "approved").map((review) => review.subject));
    if (Object.keys(manifest.characters).every((id) => approved.has(id))) {
      const unrecorded = await this.pulled(state, "look");
      if (unrecorded) return unrecorded;
      return `${state.slug}: the owner chose the character sheets`;
    }
    return null;
  }

  /** The storyboard gate: sent when nothing is pending for these keyframes; sent back means a prompt fix. */
  async storyboardGate(state) {
    const workdir = this.workdir(state.slug);
    const review = await this.decision(state, "storyboard", path.join(workdir, ARTIFACTS.keyframes));
    if (!review) {
      const pushed = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", "storyboard"]);
      if (pushed.code !== 0) return this.submissionFailure(state, "storyboard", pushed);
      return `${state.slug}: storyboard sent to /admin/videos`;
    }
    if (review.status === "approved") {
      const unrecorded = await this.pulled(state, "storyboard");
      if (unrecorded) return unrecorded;
      return `${state.slug}: the owner approved the storyboard${review.note ? ` (${review.note})` : ""}`;
    }
    if (review.status === "rejected") {
      const shots = (review.payload?.shots ?? []).filter((shot) => shot.needs_review).map((shot) => ({ id: shot.id, problems: shot.judge?.problems ?? [] }));
      return this.fixPrompts(state, "keyframes", { targets: shots, ownerNote: review.note ?? "" });
    }
    return null;
  }

  /** Line ids for the model to use, none already in the script (the same alphabet as `ids`). */
  freshIds(state, video, count) {
    const taken = new Set(video ? [...eachLine(video)].map(({ line }) => line.id) : []);
    const ids = [];
    const alphabet = "abcdefghijkmnpqrstuvwxyz23456789";
    // Reconstructing an unfinished durable writer after restart must send identical inputs.
    const seed = JSON.stringify({ slug: state.slug, taken: [...taken].sort(), count });
    let round = 0;
    while (ids.length < count) {
      let id = "";
      const bytes = createHash("sha256").update(`${seed}:${round++}`).digest();
      for (let index = 0; index < 4; index++) id += alphabet[bytes[index] % alphabet.length];
      if (LINE_ID.test(id) && !taken.has(id) && !ids.includes(id)) ids.push(id);
    }
    return ids;
  }

  async write(state) {
    if (state.format === "drama") state.target_minutes = hasAnimePolicy(state) ? requireAnimePolicy(state.series).body_target_seconds / 60 : episodeMinutes(state.target_minutes, state.style_preset);
    const dir = docDir(state.slug, this.ctx.root);
    if (existsSync(path.join(dir, "video.json"))) {
      // A draft exists and only fails lint: fix it rather than write a new one.
      const problem = await this.saveAndLint(state, { video: JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8")) });
      saveState(this.workdir(state.slug), state);
      return problem ? await this.block(state, problem) : `${state.slug}: script fixed and passes lint`;
    }
    const brief = readFileSync(path.join(dir, "brief.md"), "utf8");
    const option = outlineOptions(brief).find((each) => each.key === state.chosen) ?? null;
    const sources = await readSources(this.read, siteSources(state.source_guide, state.source_urls, this.ctx.root));
    const answer = isLongAnime(state) ? await this.animeRewrite(state, { brief, chosen_option: option, sources }) : await this.stage("writer", state.slug, this.scriptPayload(state, { brief, chosen_option: option, sources, line_ids: this.freshIds(state, null, 140), ...this.draftBudget(state) }), 32_000, state.format, this.variantOf(state), state.series ?? null);
    if (typeof answer.claims === "string") writeFileSync(path.join(dir, "claims.md"), answer.claims.endsWith("\n") ? answer.claims : `${answer.claims}\n`);
    const problem = await this.saveAndLint(state, answer);
    saveState(this.workdir(state.slug), state);
    if (problem) return this.retryLater(state, "writer", `the script ${problem}`);
    this.cleared(state, "writer");
    // An explainer's and an illustrated slides video's two Shorts are drafted with the script (docs/videos/ILLUSTRATED.md).
    const shorts = this.variantOf(state) === "explainer" || illustrated(JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"))) ? this.saveShorts(state, answer.shorts) : null;
    saveState(this.workdir(state.slug), state);
    await report(this.ctx, this.api, state, "fact-checked");
    return `${state.slug}: script drafted and passes lint${shorts ? `; ${shorts}` : ""}`;
  }

  /**
   * What a slides video's shot prompts may have (`prompt_budget_chars`), for the image model the
   * settings will draw them with: the heaviest look the video may get (HEAVIEST_SLIDES_LOOK: the
   * writer may name one of its own), the longest camera word the writer may choose and that
   * model's limit, counted as media/keyframes.mjs counts a shot's request; never more than the
   * writer's own 1000. The first draft and every whole-script rewrite after it (a lint fix, a
   * screenplay or prompt fix) carry it, so a rewrite cannot lengthen a prompt past it. A drama
   * and a story are drawn otherwise and hear nothing; a look that leaves no room at all is the
   * keyframes stage's to refuse, with the owner's number.
   */
  draftBudget(state) {
    if (state.format === "drama" || state.story) return {};
    try {
      const limit = imagePromptLimit({ provider: slidesImageVendor(this.settings) }, null);
      const budget = shotPromptBudget({ look: HEAVIEST_SLIDES_LOOK, camera: LONGEST_CAMERA_WORD, cast: null, limit });
      return { prompt_budget_chars: Math.min(budget, WRITER_PROMPT_MAX) };
    } catch {
      return {};
    }
  }

  /**
   * An explainer's two Shorts (docs/videos/so-thats-why/), drafted with its script: the fields the
   * tool decides are set here, and shorts.json is written only when both Shorts fit this video.
   * A bad draft is noted and never holds the long video back; the Shorts can be written later.
   */
  saveShorts(state, drafted) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const shorts = Array.isArray(drafted)
      ? drafted.map((doc, index) => ({ ...doc, ...episodeShortFields(state.slug, index, episodeSeries(video)) }))
      : drafted;
    const problems = episodeShortsProblems(shorts, video);
    if (problems.length) {
      state.notes.push(`the drafted Shorts were not saved: ${problems.slice(0, 3).join("; ")}`);
      return "Shorts not saved (see notes)";
    }
    writeFileSync(shortsFile(state.slug, this.ctx.root), `${JSON.stringify(shorts, null, 2)}\n`);
    return "2 Shorts drafted";
  }

  async verify(state) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const claims = existsSync(path.join(dir, "claims.md")) ? readFileSync(path.join(dir, "claims.md"), "utf8") : "";
    const round = state.verify_rounds + 1;
    const urls = siteSources(null, [...urlsIn(claims), ...(video.sources ?? []).map((source) => source.url), ...(state.source_urls ?? [])], this.ctx.root);
    const sources = await readSources(this.read, urls);
    const answer = await this.stage("verifier", state.slug, { today: today(this.ctx), round, video, claims, brief: readFileSync(path.join(dir, "brief.md"), "utf8"), sources, ...(state.series ? this.seriesPayload(state) : {}) }, isLongAnime(state) ? 8_000 : 32_000, state.format, this.variantOf(state), state.series ?? null);
    if (isLongAnime(state) && answer.video) return this.retryLater(state, "verifier", "long-anime verification must return findings, not a whole-script rewrite");
    if (typeof answer.report !== "string") return this.retryLater(state, "verifier", `fact-check round ${round} returned no report`);
    writeFileSync(path.join(dir, `verify-${round}.md`), answer.report.endsWith("\n") ? answer.report : `${answer.report}\n`);
    if (typeof answer.claims === "string") writeFileSync(path.join(dir, "claims.md"), answer.claims.endsWith("\n") ? answer.claims : `${answer.claims}\n`);
    state.verify_rounds = round;
    const changed = Number(answer.changed_facts) || 0;
    if (answer.video) {
      const problem = await this.saveAndLint(state, { video: answer.video });
      if (problem) return this.retryLater(state, "verifier", `fact-check round ${round} changed ${changed} facts but ${problem}`);
    }
    const saved = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    if (state.series) {
      // A lint repair may rewrite the verifier's candidate. Never bind that candidate's
      // verdict to the repair: another bounded verification must read the saved script.
      // Without a candidate nothing was saved, and the script read is the script on disk.
      if (answer.video && !this.checkedIsSaved(state, answer.video, saved)) {
        state.verified = false;
        return this.retryLater(state, "verifier", "the lint repair changed the checked script; verification must run again");
      }
      const reviewDir = path.join(this.workdir(state.slug), "review");
      mkdirSync(reviewDir, { recursive: true });
      atomicWrite(path.join(reviewDir, "script-check.json"), `${JSON.stringify({ ...scriptCheckBinding(saved), round, coverage: answer.coverage ?? null, problems: Array.isArray(answer.problems) ? answer.problems : [], similar_works: Array.isArray(answer.similar_works) ? answer.similar_works : [], ...(isLongAnime(state) ? { continuity_problems: Array.isArray(answer.continuity_problems) ? answer.continuity_problems : ["checker omitted continuity_problems"] } : {}), retention: retentionNumbers(saved, answer.retention) }, null, 2)}\n`);
    }
    state.verified = changed <= 3 || round >= settingsFor(this.settings, state.format).verifyRounds;
    this.cleared(state, "verifier");
    saveState(this.workdir(state.slug), state);
    return `${state.slug}: fact-check round ${round}, ${changed} facts changed${state.verified ? "" : "; another round follows"}`;
  }

  async listen(state, note = null) {
    const dir = docDir(state.slug, this.ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    // A drama's listener reads the format alone, as before; a slides video's carries the variant
    // (the storytelling register of docs/videos/ILLUSTRATED.md rides on it).
    const variant = state.format === "drama" ? null : this.variantOf(state);
    const listenPayload = { script_writing: this.reference().script_writing, brief: readFileSync(path.join(dir, "brief.md"), "utf8"), ...(note ? { owner_note: note } : {}) };
    const answer = isLongAnime(state) ? await this.animeRewrite(state, listenPayload, video, "listener", "listen") : await this.stage("listener", state.slug, { video, ...listenPayload, ...(state.series ? this.seriesPayload(state) : {}) }, 32_000, state.format, variant);
    const problem = await this.saveAndLint(state, answer);
    const saved = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    if (!scriptCheckMatches(scriptCheckBinding(video), saved)) state.verified = false;
    // Keep listener_done after the recheck, so a meaningful edit causes one new
    // verification sequence rather than a verifier/listener loop.
    state.listener_done = !problem;
    if (problem) return this.retryLater(state, "listener", `the listener edit ${problem}`);
    this.cleared(state, "listener");
    saveState(this.workdir(state.slug), state);
    return `${state.slug}: listener edit, ${(answer.edits ?? []).length} changes`;
  }

  /**
   * `restyle --slug S` (docs/videos/ILLUSTRATED.md §說書式旁白): a video the worker started, not
   * yet on YouTube, has its narration retold in the storytelling register without a new script.
   * The listener's register pass (variant "register") answers line by line; a line that keeps
   * every number, Latin word and dictionary term (rewrite.mjs) and a pause within the schema
   * replaces the script's, the rest are refused with the reason; a script the accepted lines
   * make fail lint goes back as it was. brief.md is not touched (the outline approval holds) and
   * no line is added, dropped or moved (the translations' ids still match), but the wording is
   * new: the fact-check runs once more, the narration is recorded again and the audio gate is
   * reviewed anew, all by the worker's next rounds. Returns the line for the terminal.
   */
  async restyle(slug, { dryRun = false } = {}) {
    const state = automatedVideos(this.workBase).find((each) => each.slug === slug);
    if (!state) throw new UsageError(`${slug} was not started by the worker (no ${STATE_FILE} in its work directory); restyle works on the worker's videos`);
    if (state.format === "drama") throw new UsageError(`${slug} is a drama: its narration is the screenplay's, the register is for slides videos`);
    if (pastUpload(state)) throw new UsageError(`${slug} is already on YouTube; a restyle would make a different video`);
    const dir = docDir(slug, this.ctx.root);
    const file = path.join(dir, "video.json");
    if (!existsSync(file)) throw new UsageError(`${slug} has no video.json yet; restyle retells a written script`);
    const source = readFileSync(file, "utf8");
    const video = JSON.parse(source);
    const before = registerSummary(video);
    if (dryRun) return `${slug}: ${registerLine(before)}; a restyle would send ${before.lines} lines to the listener's register pass, then fact-check, record and review the narration again`;
    const lexicon = readJson(lexiconFile(this.ctx.root), emptyLexicon());
    const lines = new Map();
    const listed = [];
    for (const scene of video.scenes ?? []) {
      for (const line of scene.lines ?? []) {
        lines.set(line.id, line);
        listed.push({ id: line.id, scene: scene.id, ...(scene.chapter ? { chapter: scene.chapter } : {}), text: spokenText(line) });
      }
    }
    const answer = await this.stage("listener", slug, { video, lines: listed, lexicon: Object.keys(lexicon.terms) }, 32_000, state.format, "register");
    if (!Array.isArray(answer?.lines)) throw new AutomationError("the register pass answered without a lines array", { code: OUTPUT_INVALID });
    const accepted = [];
    const refused = [];
    const seen = new Set();
    for (const entry of answer.lines) {
      const id = String(entry?.id ?? "");
      const line = lines.get(id);
      if (!line) {
        refused.push(`${id || "?"}: not a line of this video`);
        continue;
      }
      if (seen.has(id)) continue;
      seen.add(id);
      const was = spokenText(line);
      const text = typeof entry.text === "string" ? entry.text.trim() : "";
      if (!text) {
        refused.push(`${id}: the retold line is empty`);
        continue;
      }
      // A "pause_after_ms" in the answer is ignored: the tool sets the beats from the retold text below.
      if (text === was) continue;
      const problems = rewriteProblems(was, text, { lexicon });
      if (problems.length) {
        refused.push(`${id}: ${problems.join("; ")}`);
        continue;
      }
      accepted.push({ id, before: was, after: text });
    }
    if (accepted.length) {
      for (const { id, after } of accepted) {
        const line = lines.get(id);
        line.text = after;
        // The retold line is what the voice says now; a spoken form written for the old text would fail lint.
        delete line.say;
        delete line.say_for;
      }
      // The beats follow the retold text (a new closing question, a 「其實」 moved), and only the tool sets them.
      writeVideo(dir, setPauseBeats(video));
      const errors = lintErrors(this.ctx, slug);
      if (errors.length) {
        writeFileSync(file, source);
        throw new AutomationError(`lint refuses the retold script, so video.json is back as it was: ${errors.slice(0, 3).join("; ")}`, { code: OUTPUT_INVALID });
      }
    }
    const workdir = this.workdir(slug);
    mkdirSync(path.join(workdir, "review"), { recursive: true });
    atomicWrite(path.join(workdir, "review", "restyle.json"), `${JSON.stringify({ restyled_at: this.ctx.now().toISOString(), accepted, refused, before, after: registerSummary(readJson(file)) }, null, 2)}\n`);
    if (accepted.length) {
      // The register pass was the listener's edit; the facts are checked once more, then the
      // worker records the narration again and the audio gate is reviewed anew.
      state.verified = false;
      state.listener_done = true;
      state.notes.push(`restyled on ${today(this.ctx)}: ${accepted.length} lines retold in the storytelling register${refused.length ? `, ${refused.length} refused (review/restyle.json)` : ""}`);
      saveState(workdir, state);
    }
    const after = registerSummary(readJson(file));
    return `${slug}: ${accepted.length} of ${listed.length} lines retold${refused.length ? `, ${refused.length} refused (review/restyle.json)` : ""}; now ${registerLine(after)}${accepted.length ? "; the worker fact-checks, records and reviews the narration again" : ""}`;
  }

  /**
   * A `tts --redo` that a STOP file ended (exit 6) after some of its requests were paid for: their
   * takes are on disk and in audio/cache.json, while timeline.json still binds the takes before.
   * auto.json keeps the lines it was retaking and the takes it made (`stopped_retake`), so the
   * next run's guard before tts tells them from a take swapped without review and rebuilds the
   * narration from them. A retake stopped before its first request made nothing and records
   * nothing. Either way the video is left for this run and the next one continues: a STOP is
   * never a block. A retake that met a service away or a limit (exit 4) leaves the same takes
   * behind and is recorded the same way, but waits as any deferral does (`wait`, defer's options).
   * `giveBack` returns the retake round it was counted under when it made no take at all: an
   * outage repeated round after round would otherwise spend every retake and send lines that were
   * never retaken to the listener's rewrite (docs/videos/HANDS-OFF.md §旁白).
   */
  retakeStopped(state, flagsFile, line, wait = { backoffMs: 0 }, { giveBack = false } = {}) {
    const workdir = this.workdir(state.slug);
    let ids;
    try {
      ids = flaggedLines(readJson(flagsFile));
    } catch {
      ids = new Set();
    }
    // A flagged repeat is retaken through the original it repeats (tts --redo).
    const doc = readJson(path.join(docDir(state.slug, this.ctx.root), "video.json"), null);
    for (const { line: each } of doc ? eachLine(doc) : []) if (ids.has(each.id) && each.audio_ref) ids.add(each.audio_ref);
    const takes = changedTakes(readJson(path.join(workdir, "timeline.json"), null), workdir, ids);
    if (takes && Object.keys(takes).length) {
      state.stopped_retake = { flags: path.relative(workdir, flagsFile).split(path.sep).join("/"), ids: [...ids], takes };
      saveState(workdir, state);
    } else if (giveBack && takes && state.retakes > 0) {
      // defer() below saves it.
      state.retakes -= 1;
    }
    return this.defer(state, `${state.slug}: ${line}`, wait);
  }

  async narration(state) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const timeline = path.join(workdir, "timeline.json");
    const audioProblems = audioEvidenceProblems(readJson(timeline, null), workdir);
    if (audioProblems.length) return this.block(state, `narration needs current audio evidence: ${audioProblems[0]}`);
    const review = await this.decision(state, "audio", timeline);
    if (review?.status === "approved") {
      const unrecorded = await this.pulled(state, "audio");
      if (unrecorded) return unrecorded;
      return `${state.slug}: narration approved${review.note ? ` (${review.note})` : ""}`;
    }
    if (review?.status === "rejected") {
      state.notes.push(`narration sent back: ${review.note}`);
      state.listener_done = false;
      saveState(workdir, state);
      return this.listen(state, review.note);
    }
    if (review?.status === "pending") return null;
    let check = await this.speech(state.slug, ["check-audio", "--slug", state.slug]);
    const retakeRounds = settingsFor(this.settings, state.format).retakeRounds;
    while (check.code === 1 && state.retakes < retakeRounds) {
      state.retakes += 1;
      saveState(workdir, state);
      const flagsFile = path.join(workdir, "review", "check-flags.json");
      const redo = await this.speech(state.slug, ["tts", "--slug", state.slug, "--redo", flagsFile]);
      if (redo.code === ctx.EXIT.incomplete) return this.retakeStopped(state, flagsFile, `the retake stopped (${lastLine(redo.out)}); the next run continues`);
      if (redo.code === 4) return this.retakeStopped(state, flagsFile, `the retake could not finish (${lastLine(redo.out)})`, retakeWait(redo), { giveBack: true });
      if (redo.code !== 0) return this.block(state,`retake failed: ${redo.out.trim().split("\n").at(-1)}`);
      check = await this.speech(state.slug, ["check-audio", "--slug", state.slug]);
    }
    // The retakes are spent and Jev still hears some lines wrong: the listener rewords those
    // lines, they are retaken and checked again, MAX_REWRITE_ROUNDS rounds in all
    // (docs/videos/HANDS-OFF.md §旁白). What is still flagged after that waits for the owner.
    let rounds = 0;
    let rewritten = 0;
    let problems = [];
    while (check.code === 1 && (state.rewrites ?? 0) < MAX_REWRITE_ROUNDS) {
      const round = await this.rewriteNarration(state, problems);
      if (round.stopped) return round.stopped;
      rounds += 1;
      rewritten += round.ids.length;
      problems = round.problems;
      // Nothing changed: the same clips would only be flagged again; the next round, if any,
      // is told why the rewrites were refused.
      if (!round.ids.length) continue;
      const redo = await this.speech(state.slug, ["tts", "--slug", state.slug, "--redo", round.flagsFile]);
      if (redo.code === ctx.EXIT.incomplete) return this.retakeStopped(state, round.flagsFile, `the retake after the rewrite stopped (${lastLine(redo.out)}); the next run continues`);
      if (redo.code === 4) return this.retakeStopped(state, round.flagsFile, `the retake after the rewrite could not finish (${lastLine(redo.out)})`, retakeWait(redo));
      if (redo.code !== 0) return this.block(state, `retake after the rewrite failed: ${lastLine(redo.out)}`);
      check = await this.speech(state.slug, ["check-audio", "--slug", state.slug]);
    }
    // A service away, or Jev's daily calls spent (everyone's until midnight UTC, and never a block).
    if (check.code === 4) return this.defer(state, `${state.slug}: narration check could not finish (${check.out.trim().split("\n").at(-1)})`, { what: "check-audio", everyone: Boolean(everyones(check.out)) });
    // Stopped by a STOP file before every line was heard: nothing is judged yet, so nothing goes
    // for review, and the next run continues where it stopped.
    if (check.code === ctx.EXIT.incomplete) return this.defer(state, `${state.slug}: narration check stopped (${lastLine(check.out)}); the next run continues`, { backoffMs: 0 });
    // Only a finished check (0, or 1 with lines still flagged) goes for review. One that stopped
    // for the owner (a token, a key, a paid transcription or judgement whose answer was lost) did
    // not finish check.json, and the lines Jev never judged would read as fine on the card.
    if (check.code === 3) return this.block(state, `check-audio needs the owner: ${lastLine(check.out)}`);
    if (check.code !== 0 && check.code !== 1) return this.block(state, `check-audio failed: ${lastLine(check.out, 2)}`);
    const pushed = await run(ctx, ["review-push", "--slug", state.slug, "--gate", "audio"]);
    if (pushed.code !== 0) return this.submissionFailure(state, "narration", pushed);
    // Approved on arrival (Jev passed every line, the owner's switch on), it is recorded now.
    const unrecorded = await this.pulled(state, "audio", timeline);
    if (unrecorded) return unrecorded;
    const rewriting = rounds ? `; ${rewritten} lines rewritten in ${rounds} rewrite round${rounds === 1 ? "" : "s"}` : "";
    return `${state.slug}: narration checked (${check.code === 0 ? "Jev passed every line" : "some lines flagged"}${rewriting}) and sent for review`;
  }

  /**
   * One rewrite round (docs/videos/HANDS-OFF.md §旁白): the lines check-audio still flags, with
   * what the transcriber heard, go to the listener's rewrite pass. A rewrite that keeps every
   * number, Latin word and dictionary term (rewrite.mjs) replaces the line in video.json, the
   * rest are dropped with the reason in the notes; a script the rewrites make fail lint is put
   * back as it was. The accepted rewrites go to review/rewrites.json for the review card and
   * their ids to a flags file for `tts --redo`. `previousProblems` are the refusals of the round
   * before, so the listener does not repeat them. Answers { ids, flagsFile, problems }, or
   * { stopped } with this run's line when the answer was unusable.
   */
  async rewriteNarration(state, previousProblems = []) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const dir = docDir(state.slug, ctx.root);
    const reviewDir = path.join(workdir, "review");
    const check = readJson(path.join(reviewDir, "check.json"), { lines: {} });
    const flags = readJson(path.join(reviewDir, "check-flags.json"), { flags: [], notes: {} });
    const file = path.join(dir, "video.json");
    const source = readFileSync(file, "utf8");
    const video = JSON.parse(source);
    const lines = new Map([...eachLine(video)].map(({ line }) => [line.id, line]));
    const flagged = (flags.flags ?? [])
      .filter((id) => lines.has(id))
      .map((id) => ({ id, text: spokenText(lines.get(id)), heard: check.lines?.[id]?.heard ?? "", jev: typeof check.lines?.[id]?.noul === "number" ? check.lines[id].noul : null }));
    const round = (state.rewrites ?? 0) + 1;
    const lexicon = readJson(lexiconFile(ctx.root), emptyLexicon());
    const payload = { lines: flagged, lexicon: Object.keys(lexicon.terms), round, ...(previousProblems.length ? { previous_problems: previousProblems } : {}) };
    const revised = isLongAnime(state) ? await this.animeRewrite(state, { ...payload, rewrite_lines: flagged }, video, "listener", `audio-rewrite-${round}`) : null;
    const answer = revised ? { lines: [...eachLine(revised.video)].filter(({ line }) => flagged.some((entry) => entry.id === line.id)).map(({ line }) => ({ id: line.id, text: spokenText(line) })) } : await this.stage("listener", state.slug, payload, 16_000, state.format, "rewrite");
    if (!Array.isArray(answer?.lines)) return { stopped: await this.retryLater(state, "listener", `rewrite round ${round} answered without a lines array`) };
    this.cleared(state, "listener");
    const accepted = [];
    const problems = [];
    const seen = new Set();
    for (const entry of answer.lines) {
      const id = String(entry?.id ?? "");
      const before = flagged.find((each) => each.id === id);
      if (!before) {
        problems.push(`${id || "?"}: not one of the flagged lines`);
        continue;
      }
      if (seen.has(id)) continue;
      seen.add(id);
      const after = typeof entry.text === "string" ? entry.text.trim() : "";
      if (!after) {
        problems.push(`${id}: the rewrite is empty`);
        continue;
      }
      if (after === before.text) continue;
      const found = rewriteProblems(before.text, after, { lexicon });
      if (found.length) {
        problems.push(`${id}: ${found.join("; ")}`);
        continue;
      }
      accepted.push({ id, before: before.text, after, heard: before.heard });
    }
    if (accepted.length) {
      for (const { id, after } of accepted) {
        const line = lines.get(id);
        line.text = after;
        // The rewrite is what the voice says now; a spoken form written for the old text would fail lint.
        delete line.say;
        delete line.say_for;
      }
      writeVideo(dir, video);
      const errors = lintErrors(ctx, state.slug);
      if (errors.length) {
        writeFileSync(file, source);
        problems.push(`${accepted.map((each) => each.id).join(", ")}: lint refuses the rewritten script: ${errors.slice(0, 3).join("; ")}`);
        accepted.length = 0;
      }
    }
    state.rewrites = round;
    for (const each of accepted) state.notes.push(`narration rewritten: ${each.id} 「${each.before}」 → 「${each.after}」`);
    for (const problem of problems) state.notes.push(`narration rewrite dropped: ${problem}`);
    // Every round's accepted rewrites, in order: review/sync.mjs sends them as the audio review's payload.rewrites.
    atomicWrite(path.join(reviewDir, "rewrites.json"), `${JSON.stringify([...readJson(path.join(reviewDir, "rewrites.json"), []), ...accepted], null, 2)}\n`);
    const flagsFile = path.join(reviewDir, "rewrite-flags.json");
    if (accepted.length) atomicWrite(flagsFile, `${JSON.stringify({ slug: state.slug, flags: accepted.map((each) => each.id) }, null, 2)}\n`);
    saveState(workdir, state);
    this.log(`  rewrite round ${round}: ${accepted.length} of ${flagged.length} flagged lines rewritten${problems.length ? `, ${problems.length} dropped` : ""}`);
    return { ids: accepted.map((each) => each.id), flagsFile, problems };
  }

  /**
   * The zh-TW captions, cut from the approved narration. The other languages are no longer made
   * here: the owner chooses them per video once the final cut is approved, and `languages` makes
   * exactly those (docs/videos/LANGUAGES.md), so the final gate never waits on a translation.
   */
  async captions(state) {
    const result = await run(this.ctx, ["captions", "--slug", state.slug]);
    if (result.code !== 0) return this.block(state, `captions failed: ${result.out.trim()}`);
    return `${state.slug}: captions written`;
  }

  /**
   * One unit of the languages work (docs/videos/LANGUAGES.md). Once the final cut is approved
   * and the owner has chosen the video's languages on /admin/videos, the choice is copied into
   * the work directory (captions, package, qa and review-push read it there); then a round
   * translates one locale's chosen parts, or makes one locale's dub track (shortening and
   * retaking within the round), and once every chosen part the site still reports as in the
   * making is made, the captions and the package are written again and the batch goes up as a
   * languages review. Null when there is nothing to do: no choice yet, nothing pending, or the
   * final cut not approved. A video the owner already uploaded takes the same round for the
   * languages ticked after the fact. A video narrated in another language is translated into
   * zh-TW first, once, whatever was chosen (channelLocale).
   */
  async languages(state) {
    const { ctx } = this;
    const slug = state.slug;
    const video = (this.site ?? []).find((each) => each.slug === slug);
    if (!video || video.dropped_at || !video.locales_decided_at) return null;
    const dir = docDir(slug, ctx.root);
    const workdir = this.workdir(slug);
    if (!existsSync(path.join(dir, "video.json"))) return null;
    // A tidied video's final.mp4 is gone, so its final approval reads as absent: say why its new
    // parts will not be made instead of leaving them in the making for good.
    if (state.tidied_at) return this.tidiedLanguages(state, video);
    if ((await approvalState({ gate: "final", docDir: dir, workdir })).status !== "approved") return null;
    writeLanguages(workdir, { locales: video.locales ?? {}, decided_at: video.locales_decided_at, synced_at: ctx.now().toISOString() });
    const choice = readLanguages(workdir);
    const pending = this.pendingLanguages(video, choice);
    // A zh-TW video reads nothing more than before; one narrated in another language may still
    // owe its zh-TW, which no choice lists (channelLocale).
    const zhNarrated = narrationLocale(readJson(path.join(dir, "video.json"), null)) === NARRATION_LOCALE;
    // Nothing to make, but the owner changed the choice after the package was written (narrowed
    // it, or chose 只出繁體中文 for a package from before the panel): the package check would fail
    // it at the publish push, so it is written again once; the package it writes records this
    // choice, and the next round finds nothing to do. Only before the upload confirmation: past
    // it (pastUpload) the package already went up and no publish push reads it again, and one
    // that can no longer be written (final.mp4's checks older than the script) would block a
    // published video every round. That package is left as it is.
    const repackage = !pending.length && !pastUpload(state) && packageChoiceStale(workdir);
    if (!pending.length && zhNarrated && !repackage) return null;
    const project = loadProject({ slug, root: ctx.root });
    const doc = project.doc;
    const channel = zhNarrated ? null : this.channelLocale(project, workdir, state);
    if (!pending.length && !channel && !repackage) return null;
    // The narration's own language, when the owner ticks it, is the video's own title, captions
    // and audio: nothing is translated or dubbed, and the batch sends them as made, its dub as a
    // skip (review/sync.mjs languagesSubmission).
    const narrated = narrationLocale(doc);
    for (const { locale, parts } of [...(channel ? [channel] : []), ...pending]) {
      if (locale === narrated) continue;
      const sheetParts = parts.filter((part) => part !== "dub");
      if (!sheetParts.length) continue;
      const translated = await this.translateLocale(state, locale, sheetParts, doc);
      if (translated) return translated;
    }
    // Only zh-TW was owed (the owner chose no other language), or only the package is behind the
    // choice: write the captions and the package; there is no batch to send, since the panel never
    // offers zh-TW and no chosen part is still in the making.
    if (!pending.length) {
      await this.drawLanguageThumbnails(slug, project, workdir);
      const captions = await run(ctx, ["captions", "--slug", slug]);
      if (captions.code !== 0) return this.block(state, `captions failed: ${lastLine(captions.out)}`);
      const packaged = await run(ctx, ["package", "--slug", slug]);
      if (packaged.code !== 0) return this.block(state, `package failed: ${lastLine(packaged.out)}`);
      if (!channel) return `${slug}: upload package written again for the current language choice`;
      return `${slug}: ${NARRATION_LOCALE} captions, title and description written into the upload package`;
    }
    const dubs = dubsStatus(project, workdir, speechHash(doc, project.lexicon));
    for (const { locale, parts } of pending) {
      // A track is current once `dub` wrote it; one left unheard by a visit that did not end with
      // Jev passing it or the locale given up (a STOP file, a limit or a service away, a lost
      // answer, a translator answer that could not be used, a block; see makeDub) is made and
      // checked again.
      const unheard = dubs[locale]?.status === "current" && state.languages?.[locale]?.check_stopped;
      if (locale === narrated || !parts.includes("dub") || (["current", "skipped"].includes(dubs[locale]?.status) && !unheard)) continue;
      return this.makeDub(state, locale);
    }
    // Every chosen part is made: cut the captions on the dubs, write the package with the chosen
    // locales, and send the batch; the site marks the parts ready (or waits for the owner's
    // "uploaded" when a dub track is among them).
    await this.drawLanguageThumbnails(slug, project, workdir);
    const captions = await run(ctx, ["captions", "--slug", slug]);
    if (captions.code !== 0) return this.block(state, `captions failed: ${lastLine(captions.out)}`);
    const packaged = await run(ctx, ["package", "--slug", slug]);
    if (packaged.code !== 0) return this.block(state, `package failed: ${lastLine(packaged.out)}`);
    const pushed = await run(ctx, ["review-push", "--slug", slug, "--gate", "languages"]);
    // A rejected payload will not recover next round. Park only this video so later
    // videos can run; the existing one-shot retry resumes it after the payload is fixed.
    if (pushed.code === ctx.EXIT.lint) return this.block(state, `language submission rejected: ${lastLine(pushed.out, 2)}`);
    // Any other failed push waits for this video alone (submissionFailure).
    if (pushed.code !== 0) return this.defer(state, `${slug}: could not send the language batch: ${lastLine(pushed.out, 2)}`, { what: "review-push", everyone: Boolean(everyones(pushed.out)) });
    // A batch with no dub track is approved on arrival, and recorded now.
    const unrecorded = await this.pulled(state, "languages", GATES.languages({ workdir }));
    // A pull that ended in a block, or in a deferral the page was told about, has said what the
    // card must show; this stage's report would take that row off again.
    if (!(unrecorded && (state.status === "blocked" || state.deferred_reported))) await report(ctx, this.api, state, "languages sent");
    if (unrecorded) return unrecorded;
    return `${slug}: language batch sent to /admin/videos (${pending.map(({ locale, parts }) => `${locale} ${parts.join("+")}`).join(", ")})`;
  }

  /**
   * The languages ticked after the worker tidied the video (tools/video/automation/tidy.mjs,
   * docs/videos/AUTOMATION.md §清理工作區): the cut, the narration and the frames are gone, and
   * `package` cannot be written without final.mp4, so nothing is translated or dubbed. Each part
   * the site still reports as in the making goes up in a languages batch as {status: "skipped",
   * reason}, the way a dub the worker gave up does (dubs/<locale>/skipped.json), so the panel
   * shows 跳過 with the reason and the card leaves 語言製作中. The batch names only those parts,
   * so the parts made before keep their state (the tidy waits for every batch to be decided, so
   * no pending one is replaced), and it has no dub track, so the site approves it on arrival.
   * Null when nothing is pending, which is every round after the batch is in.
   */
  async tidiedLanguages(state, video) {
    const { ctx } = this;
    const slug = state.slug;
    const workdir = this.workdir(slug);
    writeLanguages(workdir, { locales: video.locales ?? {}, decided_at: video.locales_decided_at, synced_at: ctx.now().toISOString() });
    const pending = this.pendingLanguages(video, readLanguages(workdir));
    if (!pending.length) return null;
    const day = String(state.tidied_at).slice(0, 10);
    const reason = `工作檔已在 ${day} 清掉，成片與旁白都不在了，清理後才勾的部件做不出來；要這個語言得重做影片`;
    const locales = Object.fromEntries(pending.map(({ locale, parts }) => [locale, Object.fromEntries(parts.map((part) => [part, { status: "skipped", reason }]))]));
    // What was sent, as languagesSubmission (review/sync.mjs) writes it: the approval binds to it.
    const file = GATES.languages({ workdir });
    atomicWrite(file, `${JSON.stringify({ speech_hash: null, decided_at: video.locales_decided_at, tidied_at: state.tidied_at, locales }, null, 2)}\n`);
    const names = { metadata: "標題說明", captions: "CC", dub: "配音" };
    const said = pending.map(({ locale, parts }) => `${locale} ${parts.map((part) => names[part]).join("、")}`).join("；");
    try {
      await this.api.submit(slug, { gate: "languages", content_sha256: await sha256File(file), summary: `語言：${said} 跳過（${reason}）。沒有要你上傳的配音`, payload: { locales }, files: [] });
    } catch (error) {
      if (!(error instanceof AutomationError)) throw error;
      // A payload the site refuses will be refused again: park only this video, as review-push does.
      if (error.who !== "owner" && [400, 422].includes(error.status)) return this.block(state, `language submission rejected: ${error.message}`);
      // The token or the site out of reach end the run; anything else waits for this video alone.
      const line = `${slug}: could not send the language batch: ${error.message}`;
      return errorScope(error) === "run" ? this.later(line) : this.defer(state, line, { what: "review-push", everyone: Boolean(everyones(error)) });
    }
    await report(ctx, this.api, state, "languages skipped");
    return `${slug}: work files cleared on ${day}; ${pending.map(({ locale, parts }) => `${locale} ${parts.join("+")}`).join(", ")} reported to /admin/videos as skipped, not made`;
  }

  /**
   * The languages' own thumbnails (thumbnails/<locale>.jpg, YouTube Studio's 「語言」 page), for
   * thumbnail words the translator merged after the frames were rendered: `render
   * --thumbnails-only` draws just those, so the slide states, thumbnail.jpg and the approved
   * final.mp4 stay as they are. It runs only while a locale's current words are not what its
   * drawn thumbnail was made from (the hash package compares). A thumbnail that cannot be drawn
   * (a glyph no font has, words that do not fit, no browser) is a note: that locale keeps the
   * video's own thumbnail, package says why, and the batch goes up regardless.
   */
  async drawLanguageThumbnails(slug, project, workdir) {
    const { doc, translations } = project;
    if (!doc.thumbnail) return;
    const drawn = readJson(path.join(workdir, ARTIFACTS.frames), null)?.thumbnail_locales ?? {};
    const owed = LOCALES.filter((locale) => {
      const hash = localizedThumbnailHash(doc, translations[locale]);
      return hash && (drawn[locale]?.hash !== hash || !existsSync(path.join(workdir, drawn[locale].file)));
    });
    if (!owed.length) return;
    const channel = this.ctx.env.VIDEO_BROWSER_CHANNEL ? ["--channel", this.ctx.env.VIDEO_BROWSER_CHANNEL] : [];
    let result;
    try {
      result = await run(this.ctx, ["render", "--slug", slug, "--thumbnails-only", ...channel]);
    } catch (error) {
      // A browser that dies mid-draw is no reason to hold the languages back either.
      result = { code: -1, out: String(error?.message ?? error) };
    }
    if (result.code !== 0) {
      this.log(`  ${owed.join(", ")} thumbnails not drawn, they keep the video's own: ${lastLine(result.out)}`);
      return;
    }
    for (const note of result.out.split("\n").filter((line) => line.startsWith("note: "))) this.log(`  ${note.trim()}`);
  }

  /** The chosen parts the site still reports as in the making, by locale in the page's order. */
  pendingLanguages(video, choice) {
    const pending = [];
    for (const [locale, chosen] of Object.entries(choice?.locales ?? {})) {
      const states = video.languages?.[locale] ?? {};
      const working = LOCALE_PARTS.filter((part) => chosen[part] && (states[part]?.state ?? "working") === "working");
      if (working.length) pending.push({ locale, parts: working });
    }
    return pending;
  }

  /**
   * zh-TW, the channel's own language, for a video narrated in another one: captions, package
   * and qa want its captions, title and description whatever the owner chose (alwaysLocales in
   * core/stages.mjs), and the panel never offers it, so the site never reports it as in the
   * making. Owed, as { locale, parts } like a pending choice, while its translation is not
   * current or while an upload package written before it lacks it; null once both are in.
   */
  channelLocale(project, workdir, state) {
    const translated = sheetDone(buildSheet(project.doc, project.translations[NARRATION_LOCALE], NARRATION_LOCALE, null, SHEET_PARTS), state.thumbnails_asked?.[NARRATION_LOCALE] ?? null);
    const upload = path.join(workdir, "upload");
    const packaged = !existsSync(path.join(upload, "metadata.json"))
      || (existsSync(path.join(upload, `description.${NARRATION_LOCALE}.txt`)) && existsSync(path.join(upload, "captions", `${NARRATION_LOCALE}.srt`)));
    return translated && packaged ? null : { locale: NARRATION_LOCALE, parts: [...SHEET_PARTS] };
  }

  /**
   * A translation unit's answer was just kept in <workdir>/i18n/<locale>.units.json
   * (sheet-units.mjs writeUnits). The durable run that gave it is bound to that file now
   * (client.mjs adoptRuns), as the writer's is to video.json: a round that stops on the next
   * request (its caption reviewer still running, a restart) leaves no unsettled journal that the
   * next unit's request would read as a changed input. Then /admin/videos is told how far the
   * locale is, best effort: a report that fails is sent again at the next checkpoint, and the
   * locale's own report once it merges takes the row off.
   */
  async unitCheckpoint(state, locale, kept, keys) {
    if (this.api.adoptRuns) {
      const file = path.join(this.workdir(state.slug), "i18n", `${locale}.units.json`);
      await this.api.adoptRuns(state.slug, { artifacts: [{ path: file, sha256: await sha256File(file) }] });
    }
    const reviewed = keys.filter((key) => kept[key]?.reviewed).length;
    const waiting = keys.filter((key) => kept[key]?.translated && !kept[key]?.reviewed).length;
    const progress = `${locale} 翻譯：${reviewed}／${keys.length} 段已審${waiting ? `，${waiting} 段譯好待審` : ""}`;
    try {
      await report(this.ctx, this.api, state, "languages", { progress });
    } catch (error) {
      if (!(error instanceof AutomationError)) throw error;
      this.log(`${state.slug}: could not report the ${locale} translation's progress yet (${error.message})`);
    }
  }

  /**
   * One locale's translation of the parts the owner chose (docs/videos/LANGUAGES.md): the sheet
   * `i18n-sheet --parts` writes (with each line's dub budget when a dub is chosen), filled by the
   * translator and read by the caption reviewer, then merged. A sheet too long for one model call
   * is asked in units, one unit a round (sheet-units.mjs); each answer is kept as it comes, so a
   * round that stops resumes without asking an answered unit again, and only the caption
   * reviewer's own worksheet completes a unit. The sheet's glossary and cue boundaries
   * (i18n/cli.mjs translationContext) travel beside the worksheet in every request, the
   * worksheet itself without them, and a unit's key still hashes the sheet as written, so a
   * glossary that changed asks the unit again. Null when the sheet has nothing left to translate;
   * else this run's line.
   */
  async translateLocale(state, locale, parts, video) {
    const { ctx } = this;
    const workdir = this.workdir(state.slug);
    const sheetResult = await run(ctx, ["i18n-sheet", "--slug", state.slug, "--locale", locale, "--parts", parts.join(",")]);
    if (sheetResult.code !== 0) return this.block(state, `i18n-sheet ${locale} failed: ${sheetResult.out.trim()}`);
    const sheetFile = path.join(workdir, "i18n", `${locale}.todo.json`);
    const sheet = readJson(sheetFile, null);
    if (!sheet) return this.block(state, `no ${locale} worksheet was written`);
    if (sheetDone(sheet, state.thumbnails_asked?.[locale] ?? null)) {
      clearUnits(workdir, locale);
      return null;
    }
    const source = sourceLocale(video);
    const context = sheetContext(sheet);
    const units = sheetUnits(sheet, this.unitLimits);
    const whole = units.length === 1 && units[0] === sheet;
    const keys = units.map((unit) => unitKey(unit, source.source_locale ?? null));
    const kept = readUnits(workdir, locale);
    const keep = () => writeUnits(workdir, locale, kept, keys);
    for (const [index, unit] of units.entries()) {
      if (kept[keys[index]]?.reviewed) continue;
      const label = whole ? locale : `${locale} part ${index + 1} of ${units.length}`;
      const ask = async (stage, worksheet) => {
        try {
          return await this.stage(stage, state.slug, { locale, parts: whole ? parts : unit.parts, worksheet: withoutContext(worksheet), video: unitVideo(video, unit, whole), ...unitContext(context, unit), ...source }, 32_000, state.format);
        } catch (error) {
          if (error instanceof AutomationError && error.code === RUN_UNCERTAIN) error.unit = label;
          throw error;
        }
      };
      // The sheet's identity and its thumbnail's source travel with it, whatever the model leaves out.
      let draft = kept[keys[index]]?.translated ?? null;
      if (!draft) {
        const translated = await ask("translator", unit);
        if (!Array.isArray(translated.worksheet?.lines)) return this.retryLater(state, "translator", `the ${label} translation returned no worksheet`);
        draft = keptWorksheet(translated.worksheet, unit, locale);
        const gaps = unitGaps(draft, unit);
        if (gaps) return this.retryLater(state, "translator", `the ${label} translation ${gaps}`);
        kept[keys[index]] = { translated: draft };
        keep();
        await this.unitCheckpoint(state, locale, kept, keys);
      }
      // A review without its own worksheet leaves the translation kept, unreviewed, for the next
      // round's reviewer: it never goes in as if it had been read.
      const reviewed = await ask("caption_reviewer", draft);
      if (!Array.isArray(reviewed.worksheet?.lines)) return this.retryLater(state, "caption_reviewer", `the ${label} review returned no worksheet; the translation waits for its review`);
      const checked = keptWorksheet(reviewed.worksheet, unit, locale, draft);
      const gaps = unitGaps(checked, unit);
      if (gaps) return this.retryLater(state, "caption_reviewer", `the ${label} review ${gaps}; the translation waits for its review`);
      kept[keys[index]] = { translated: draft, reviewed: checked };
      keep();
      await this.unitCheckpoint(state, locale, kept, keys);
      this.cleared(state, "caption_reviewer");
      if (keys.some((key) => !kept[key]?.reviewed)) {
        saveState(workdir, state);
        return `${state.slug}: ${label} translated and reviewed; the next part follows`;
      }
    }
    const finished = whole ? kept[keys[0]].reviewed : assembleSheet(sheet, keys.map((key) => kept[key].reviewed));
    this.fence(state.slug, `merging the ${locale} translation`);
    writeFileSync(sheetFile, `${JSON.stringify(finished, null, 2)}\n`);
    const merged = await run(ctx, ["i18n-merge", "--slug", state.slug, "--locale", locale]);
    if (merged.code !== 0) {
      // What the merge refused is asked again; the units it did not name stay kept.
      for (const unit of refusedUnits(merged.out, units)) delete kept[keys[units.indexOf(unit)]];
      keep();
      return this.retryLater(state, "translator", `the ${locale} translation does not merge: ${lastLine(merged.out, 2)}`);
    }
    clearUnits(workdir, locale);
    this.cleared(state, "translator");
    // The thumbnail's words were asked for once: words i18n-merge left out (its note) keep the
    // video's own thumbnail for this locale instead of sending the translation round again.
    const asked = thumbnailAskHash(sheet);
    if (asked) state.thumbnails_asked = { ...(state.thumbnails_asked ?? {}), [locale]: asked };
    for (const note of merged.out.split("\n").filter((line) => /^\s*note: thumbnail:/.test(line))) this.log(`  ${locale} ${note.trim()}`);
    saveState(workdir, state);
    await report(ctx, this.api, state, "languages");
    return `${state.slug}: ${locale} ${parts.join(" and ")} translated and reviewed`;
  }

  /**
   * One locale's dub track (docs/videos/DUBS.md): `dub`, and when a window does not fit even at
   * MAX_TEMPO, the translator shortens those lines and `dub` runs again, MAX_DUB_SHORTEN_ROUNDS
   * times; then Jev listens (`check-audio --locale`) and the flagged lines are retaken,
   * MAX_DUB_RETAKE_ROUNDS times, and the lines still heard wrong after that are reworded by the
   * translator and dubbed again, MAX_DUB_REWORD_ROUNDS times. A retake that no longer fits its
   * window goes back to the shortening. What still fails after that, and what needs the owner (a
   * voice that speaks one language, a missing key), gives the locale up with the reason instead
   * of blocking the video. A service that is down or a limit (exit 4) defers this video only, and
   * the lane goes on with the others; a STOP file that ends `dub`, a retake or the check (exit 6)
   * defers it for the rest of the run. Either way the next visit goes on from the takes already
   * paid for, and a retake that exited 4 without making a take gives its round back. A paid
   * request whose answer was lost (speechUncertain) blocks the video: the locale is not given up
   * for a request that may well have worked, nor bought again without the owner.
   */
  async makeDub(state, locale) {
    const { ctx } = this;
    const slug = state.slug;
    const workdir = this.workdir(slug);
    const rounds = { shorten: 0, retakes: 0, reword: 0, ...(state.languages?.[locale] ?? {}) };
    const remember = () => {
      state.languages = { ...(state.languages ?? {}), [locale]: rounds };
      saveState(workdir, state);
    };
    // Unheard until Jev passes the track or the locale is given up, the two endings that clear
    // these rounds. A track `dub` wrote reads as current once its words and voice are, so any
    // other way this visit ends (a deferral, a STOP, a lost answer, a translator answer that
    // could not be used, a block and the owner's retry) leaves a track that the language step
    // makes and checks again instead of sending (`unheard` there).
    rounds.check_stopped = true;
    remember();
    const dubArgs = ["dub", "--slug", slug, "--locale", locale];
    const flags = path.join(workdir, "review", `check-flags.${locale}.json`);
    const checkArgs = ["check-audio", "--slug", slug, "--locale", locale];
    const overLines = () => readJson(dubArtifacts(workdir, locale).fit, null)?.over;
    // The flagged lines' takes as they are (a retake writes each one's <id>.wav again): a retake
    // that exits 4 having changed none of them made no take, so its round is given back, as for
    // the narration (retakeStopped's giveBack). An outage repeated round after round would
    // otherwise spend every retake and send lines never retaken to the rewording.
    const flaggedTakes = () => {
      let ids;
      try {
        ids = flaggedLines(readJson(flags));
      } catch {
        ids = new Set();
      }
      const audio = dubArtifacts(workdir, locale).audio;
      return JSON.stringify([...ids].sort().map((id) => {
        const file = path.join(audio, `${id}.wav`);
        return [id, existsSync(file) ? createHash("sha256").update(readFileSync(file)).digest("hex") : null];
      }));
    };
    // A paid request whose answer was lost: the video waits for the owner, and the owner's retry
    // runs this locale again, its check included, though its track may already read as current.
    const lost = (what, result) => this.block(state, `${what} needs the owner: ${lastLine(result.out)}`);
    // A STOP file ended `dub`, a retake or the check before it finished: the takes paid for so far
    // are in the dub's cache, and the next run makes this locale's track again from the cache and
    // hears it to the end.
    const stopped = (what, result) => this.defer(state, `${slug}: ${locale} ${what} stopped (${lastLine(result.out)}); the next run continues`, { backoffMs: 0 });
    // `dub`, a retake or the check met a limit or a service away (exit 4): this video waits, and
    // the next visit goes on from the takes already paid for.
    const unfinished = (what, result) => this.defer(state, `${slug}: ${locale} ${what} could not finish (${lastLine(result.out)})`, { what: what === "dub check" ? "check-audio" : "dub", everyone: Boolean(everyones(result.out)) });
    // Each pass makes the track (only the lines whose words changed are synthesized again) and
    // checks it; a reworded line or a retake that no longer fits starts another pass.
    for (;;) {
      let made = await this.speech(slug, dubArgs);
      while (made.code === 1 && rounds.shorten < MAX_DUB_SHORTEN_ROUNDS) {
        const over = overLines();
        if (!Array.isArray(over) || !over.length) break;
        rounds.shorten += 1;
        remember();
        const shortened = await this.shortenDub(state, locale, over);
        if (shortened.stopped) return shortened.stopped;
        // Nothing usable came back: the same windows would only be over again.
        if (!shortened.ids.length) break;
        made = await this.speech(slug, dubArgs);
      }
      if (made.code === ctx.EXIT.incomplete) return stopped("dub", made);
      if (made.code === 1) {
        const over = overLines() ?? [];
        const why = over.length ? `${over.length} lines (${over.map((line) => line.id).join(", ")}) do not fit even at ${MAX_TEMPO}x after ${rounds.shorten} shortening round${rounds.shorten === 1 ? "" : "s"}` : lastLine(made.out);
        return this.giveUpDub(state, locale, why);
      }
      if (speechUncertain(made)) return lost(`dub ${locale}`, made);
      if (made.code === 3) return this.giveUpDub(state, locale, `dub needs the owner: ${lastLine(made.out)}`);
      if (made.code === 4) return unfinished("dub", made);
      if (made.code !== 0) return this.block(state, `dub ${locale} failed: ${lastLine(made.out, 2)}`);
      let check = await this.speech(slug, checkArgs);
      let refit = false;
      while (check.code === 1 && rounds.retakes < MAX_DUB_RETAKE_ROUNDS) {
        rounds.retakes += 1;
        remember();
        const takes = flaggedTakes();
        const redo = await this.speech(slug, [...dubArgs, "--redo", flags]);
        if (redo.code === ctx.EXIT.incomplete) return stopped("dub retake", redo);
        if (redo.code === 4) {
          if (flaggedTakes() === takes) rounds.retakes -= 1;
          return unfinished("dub retake", redo);
        }
        if (speechUncertain(redo)) return lost(`dub ${locale} retake`, redo);
        // The new take is longer than its window allows: the next pass's `dub` reports the same
        // window and shortens it, while shortening rounds are left.
        if (redo.code === 1 && overLines()?.length && rounds.shorten < MAX_DUB_SHORTEN_ROUNDS) {
          refit = true;
          break;
        }
        if (redo.code === 1 || redo.code === 3) return this.giveUpDub(state, locale, `the retake failed: ${lastLine(redo.out)}`);
        if (redo.code !== 0) return this.block(state, `dub ${locale} retake failed: ${lastLine(redo.out, 2)}`);
        check = await this.speech(slug, checkArgs);
      }
      if (refit) continue;
      if (check.code === 1 && rounds.reword < MAX_DUB_REWORD_ROUNDS) {
        rounds.reword += 1;
        remember();
        const reworded = await this.rewordDub(state, locale);
        if (reworded.stopped) return reworded.stopped;
        // Nothing usable came back: the same words would only be heard wrong again.
        if (reworded.ids.length) continue;
      }
      if (check.code === 4) return unfinished("dub check", check);
      if (check.code === ctx.EXIT.incomplete) return stopped("dub check", check);
      if (check.code === 1) {
        const reworded = rounds.reword ? ` and ${rounds.reword} rewording round${rounds.reword === 1 ? "" : "s"}` : "";
        return this.giveUpDub(state, locale, `Jev still hears lines wrong after ${rounds.retakes} retake${rounds.retakes === 1 ? "" : "s"}${reworded}: ${lastLine(check.out)}`);
      }
      if (speechUncertain(check)) return lost(`check-audio ${locale}`, check);
      if (check.code === 3) return this.giveUpDub(state, locale, `the dub check needs the owner: ${lastLine(check.out)}`);
      if (check.code !== 0) return this.block(state, `check-audio ${locale} failed: ${lastLine(check.out, 2)}`);
      break;
    }
    if (state.languages) delete state.languages[locale];
    saveState(workdir, state);
    await report(ctx, this.api, state, "languages");
    const plural = (count, word) => (count ? `${count} ${word}${count === 1 ? "" : "s"}` : "");
    const rounding = [plural(rounds.shorten, "shortening round"), plural(rounds.retakes, "retake"), plural(rounds.reword, "rewording round")].filter(Boolean).join(", ");
    return `${slug}: ${locale} dub made${rounding ? ` after ${rounding}` : ""}; Jev passed every line`;
  }

  /** Give a locale's dub up with the reason (dubs/<locale>/skipped.json); the batch reports it, the video goes on. */
  giveUpDub(state, locale, reason) {
    const workdir = this.workdir(state.slug);
    const files = dubArtifacts(workdir, locale);
    mkdirSync(files.dir, { recursive: true });
    atomicWrite(files.skipped, `${JSON.stringify({ reason, at: this.ctx.now().toISOString() }, null, 2)}\n`);
    state.notes.push(`${locale} dub skipped: ${reason}`);
    if (state.languages) delete state.languages[locale];
    saveState(workdir, state);
    this.log(`  ${locale} dub given up: ${reason}`);
    return `${state.slug}: ${locale} dub given up (${reason}); the video goes on without it`;
  }

  /**
   * The translator's shortening pass (docs/videos/DUBS.md): the lines of the windows that do not
   * fit even sped up, with their budgets from fit.json, go to the translator (variant "shorten").
   * A shortened line that is shorter and keeps every digit replaces the translation through a
   * captions-only sheet and i18n-merge, so the captions and the dub read the same words and the
   * hashes are the tool's; the rest are dropped with the reason in the notes. Answers { ids,
   * problems }, or { stopped } with this run's line when the answer was unusable.
   */
  async shortenDub(state, locale, over) {
    const { ctx } = this;
    const slug = state.slug;
    const workdir = this.workdir(slug);
    const dir = docDir(slug, ctx.root);
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const translation = readJson(path.join(dir, "i18n", `${locale}.json`), { lines: {} });
    const sources = new Map([...eachLine(video)].map(({ line }) => [line.id, line.text]));
    const lines = over
      .filter((entry) => sources.has(entry.id) && typeof translation.lines?.[entry.id]?.text === "string")
      .map((entry) => ({ id: entry.id, source: sources.get(entry.id), text: translation.lines[entry.id].text, chars: entry.chars, max_chars: entry.max_chars, ...(entry.seconds === undefined ? {} : { seconds: entry.seconds }), window_over_seconds: entry.window_over_seconds }));
    if (!lines.length) return { ids: [], problems: ["no line to shorten has a current translation"] };
    const answer = await this.stage("translator", slug, { locale, lines, video, ...sourceLocale(video) }, 16_000, state.format, "shorten");
    if (!Array.isArray(answer?.lines)) return { stopped: await this.retryLater(state, "translator", `the ${locale} shortening pass answered without a lines array`) };
    this.cleared(state, "translator");
    const accepted = new Map();
    const problems = [];
    for (const entry of answer.lines) {
      const id = String(entry?.id ?? "");
      const before = lines.find((each) => each.id === id);
      if (!before) {
        problems.push(`${id || "?"}: not one of the lines to shorten`);
        continue;
      }
      if (accepted.has(id)) continue;
      const after = typeof entry.text === "string" ? entry.text.trim() : "";
      if (!after) {
        problems.push(`${id}: the shortened line is empty`);
        continue;
      }
      if ([...after].length >= [...before.text].length) {
        problems.push(`${id}: not shorter (${[...after].length} characters, was ${[...before.text].length})`);
        continue;
      }
      if (digitsOf(after) !== digitsOf(before.text)) {
        problems.push(`${id}: the numbers changed`);
        continue;
      }
      accepted.set(id, after);
    }
    if (accepted.size) {
      const merged = await this.mergeDubLines(state, locale, accepted, "shortened");
      if (merged) return { stopped: merged };
    }
    for (const [id, text] of accepted) state.notes.push(`${locale} dub line shortened: ${id} → 「${text}」`);
    for (const problem of problems) state.notes.push(`${locale} shortening dropped: ${problem}`);
    saveState(workdir, state);
    this.log(`  ${locale} shortening: ${accepted.size} of ${lines.length} lines shortened${problems.length ? `, ${problems.length} dropped` : ""}`);
    return { ids: [...accepted.keys()], problems };
  }

  /**
   * The translator's rewording pass: the lines `check-audio --locale` still flags after the
   * retakes, with what the transcriber heard (review/check.<locale>.json) and their budgets from a
   * fresh captions sheet, go to the translator (variant "reword"). A reworded line that differs,
   * keeps every digit and stays within its budget (or its current length, when the sheet has
   * none) replaces the translation the way a shortened one does; the rest are dropped with the
   * reason in the notes. Answers { ids, problems }, or { stopped } with this run's line.
   */
  async rewordDub(state, locale) {
    const { ctx } = this;
    const slug = state.slug;
    const workdir = this.workdir(slug);
    const dir = docDir(slug, ctx.root);
    const flagged = readJson(path.join(workdir, "review", `check-flags.${locale}.json`), { flags: [] }).flags ?? [];
    const heard = readJson(path.join(workdir, "review", `check.${locale}.json`), { lines: {} }).lines ?? {};
    const video = JSON.parse(readFileSync(path.join(dir, "video.json"), "utf8"));
    const translation = readJson(path.join(dir, "i18n", `${locale}.json`), { lines: {} });
    const sources = new Map([...eachLine(video)].map(({ line }) => [line.id, line.text]));
    // The sheet carries each line's budget when the owner chose a dub (i18n-sheet's max_chars).
    const sheetResult = await run(ctx, ["i18n-sheet", "--slug", slug, "--locale", locale, "--parts", "captions"]);
    if (sheetResult.code !== 0) return { stopped: await this.block(state, `i18n-sheet ${locale} failed: ${lastLine(sheetResult.out)}`) };
    const budgets = new Map((readJson(path.join(workdir, "i18n", `${locale}.todo.json`), { lines: [] }).lines ?? []).map((line) => [line.id, line.max_chars]));
    const lines = flagged
      .filter((id) => sources.has(id) && typeof translation.lines?.[id]?.text === "string")
      .map((id) => {
        const text = translation.lines[id].text;
        const budget = Number.isInteger(budgets.get(id)) ? budgets.get(id) : [...text].length;
        return { id, source: sources.get(id), text, heard: String(heard[id]?.heard ?? ""), max_chars: Math.max(budget, [...text].length) };
      });
    if (!lines.length) return { ids: [], problems: ["no flagged line has a current translation"] };
    const answer = await this.stage("translator", slug, { locale, lines, video, ...sourceLocale(video) }, 16_000, state.format, "reword");
    if (!Array.isArray(answer?.lines)) return { stopped: await this.retryLater(state, "translator", `the ${locale} rewording pass answered without a lines array`) };
    this.cleared(state, "translator");
    const accepted = new Map();
    const problems = [];
    for (const entry of answer.lines) {
      const id = String(entry?.id ?? "");
      const before = lines.find((each) => each.id === id);
      if (!before) {
        problems.push(`${id || "?"}: not one of the lines to reword`);
        continue;
      }
      if (accepted.has(id)) continue;
      const after = typeof entry.text === "string" ? entry.text.trim() : "";
      if (!after) problems.push(`${id}: the reworded line is empty`);
      else if (after === before.text) problems.push(`${id}: unchanged`);
      else if ([...after].length > before.max_chars) problems.push(`${id}: over its budget (${[...after].length} characters, at most ${before.max_chars})`);
      else if (digitsOf(after) !== digitsOf(before.text)) problems.push(`${id}: the numbers changed`);
      else accepted.set(id, after);
    }
    if (accepted.size) {
      const merged = await this.mergeDubLines(state, locale, accepted, "reworded");
      if (merged) return { stopped: merged };
    }
    for (const [id, text] of accepted) state.notes.push(`${locale} dub line reworded: ${id} → 「${text}」`);
    for (const problem of problems) state.notes.push(`${locale} rewording dropped: ${problem}`);
    saveState(workdir, state);
    this.log(`  ${locale} rewording: ${accepted.size} of ${lines.length} lines reworded${problems.length ? `, ${problems.length} dropped` : ""}`);
    return { ids: [...accepted.keys()], problems };
  }

  /**
   * Put a dub pass's new translations into docs/videos/<slug>/i18n/<locale>.json through a
   * captions-only sheet and i18n-merge, so the captions and the dub read the same words and the
   * hashes are the tool's. Null when merged; else this run's line.
   */
  async mergeDubLines(state, locale, accepted, how) {
    const { ctx } = this;
    const slug = state.slug;
    const sheetResult = await run(ctx, ["i18n-sheet", "--slug", slug, "--locale", locale, "--parts", "captions"]);
    if (sheetResult.code !== 0) return this.block(state, `i18n-sheet ${locale} failed: ${lastLine(sheetResult.out)}`);
    const sheetFile = path.join(this.workdir(slug), "i18n", `${locale}.todo.json`);
    const sheet = readJson(sheetFile);
    sheet.lines = sheet.lines.map((line) => (accepted.has(line.id) ? { ...line, text: accepted.get(line.id) } : line));
    writeFileSync(sheetFile, `${JSON.stringify(sheet, null, 2)}\n`);
    const merged = await run(ctx, ["i18n-merge", "--slug", slug, "--locale", locale]);
    if (merged.code !== 0) return this.retryLater(state, "translator", `the ${how} ${locale} lines do not merge: ${lastLine(merged.out, 2)}`);
    return null;
  }

  /**
   * A gate the site decides: the final cut. `review-push --gate final` runs the quality check
   * and sends its report; the site approves on arrival when every item passed and the owner's
   * switch is on, else the owner decides. A push that could not finish (the check's service, the
   * site) waits and is tried again later (submissionFailure); one whose Jev policy verdict was
   * lost waits for the owner's retry.
   */
  async gate(state, gate, file) {
    const review = await this.decision(state, gate, file);
    if (!review) {
      // The cut of a video whose pictures were kept with the judge's remarks (acceptBestPictures)
      // is the owner's to look at whatever the quality check says (review/sync.mjs manual_review).
      const manual = gate === "final" && state.accepted_pictures?.length ? ["--manual-review"] : [];
      const pushed = await run(this.ctx, ["review-push", "--slug", state.slug, "--gate", gate, ...manual]);
      if (pushed.code !== 0) return this.submissionFailure(state, gate, pushed);
      return `${state.slug}: ${gate} sent to /admin/videos (${lastLine(pushed.out)})`;
    }
    if (review.status === "approved") {
      const unrecorded = await this.pulled(state, gate);
      if (unrecorded) return unrecorded;
      if (review.note) state.notes.push(`${gate}: ${review.note}`);
      saveState(this.workdir(state.slug), state);
      // The site's checklist shows the step done at once: the language panel opens on it (docs/videos/LANGUAGES.md).
      await report(this.ctx, this.api, state, `${gate} approved`);
      return `${state.slug}: the ${gate} is approved${review.note ? ` (${review.note})` : ""}`;
    }
    if (review.status === "rejected") return this.block(state,`the owner sent the ${gate} back: ${review.note}`);
    return null;
  }
}
