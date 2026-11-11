// 奇聞檔案局 (docs/videos/history-curiosity/, skill curio-episode) is a series of cute cartoon
// illustrations under one narrator, not a deck of cards. The owner chose the look on 2026-10-10
// ("內容相關的可愛插畫", MiniMax image-01, the third audition style, now the cute-mystery preset), and
// every delivered episode draws 73-95% of its body as illustrations with at most three cards in a
// row. The H04-H06 remakes of 2026-10-14 drifted to 88 cards and no illustration at all, with no
// check to stop them: the rules lived in look.md and in one agent's notes. These are that check, so
// whichever model makes an episode, a slug that starts with "curio-" keeps the series look.
import { isExplainer, isShot, resolveLook } from "./drama.mjs";

/** The series' look preset (drama.mjs PRESETS): the style sentence is written once, there. */
export const CURIO_PRESET = "cute-mystery";
/** The least share of the body's scenes that are illustrations (the delivered episodes run 73-95%). */
export const CURIO_MIN_SHOT_SHARE = 0.7;
/** The most cards in a row between two illustrations (the delivered episodes have at most three). */
export const CURIO_MAX_CARD_RUN = 3;
/**
 * The series' music bed (the host writer's prompt reads the same words). Every episode delivered
 * before 2026-10-19 had none, and the owner named it as one reason the brand stories, which carry
 * one at these levels (automation/story.mjs), are better.
 */
export const CURIO_MUSIC = Object.freeze({ prompt: "light, curious, a little mysterious, no vocals", gain_db: -20, duck_db: -10 });

/**
 * The pacing both narrated cartoon series take (owner, 2026-11-05; made the series default on
 * 2026-11-11): no gap between sentences and a short one between scenes, so the cut's silence
 * falls from 7-10% to the reference channels' 3% or less, and stills that hold and then move
 * (push, pan, pull) instead of one slow glide. Until then each video.json had to opt in, and none
 * of the episodes made after the rule did (.agents/skills/producer/references/pace-targets.md).
 */
export const SERIES_PACING = Object.freeze({ pauses: Object.freeze({ line_ms: 0, scene_ms: 150 }), still_motion: "beat" });

/** Whether a video belongs to a series that takes SERIES_PACING: 奇聞檔案局 (curio-) and 原來如此事務所 (sothatswhy-). */
export const isPacedSeries = (doc) => /^(curio|sothatswhy)-/.test(doc?.slug ?? "");

/**
 * What a paced series' drama is missing of SERIES_PACING, as lint warnings. A local video is
 * never changed behind its back: tightening the pauses moves the timeline an owner may already
 * have approved, so the warning names the fields and the re-approval they cost.
 */
export function pacingWarnings(doc) {
  if (!isPacedSeries(doc) || doc.format !== "drama") return [];
  const warnings = [];
  if (doc.pauses === undefined) warnings.push({ path: "pauses", message: `this series closes the gaps between sentences (owner, 2026-11-05): add "pauses": ${JSON.stringify(SERIES_PACING.pauses)}; the timeline moves, so the narration and storyboard go back to the owner (the voice is not re-recorded)` });
  if (doc.still_motion === undefined) warnings.push({ path: "still_motion", message: `this series' stills hold and then move instead of gliding (owner, 2026-11-05): add "still_motion": "${SERIES_PACING.still_motion}" (only the cut changes; no picture is redrawn)` });
  return warnings;
}

/**
 * Below this many minutes an episode of a content-led series is flagged for the owner; it is a
 * warning, never a refusal (owner, 2026-11-11: the target stays ten minutes, the material decides,
 * 10 to 13 when it carries that far, and 「低於 8 分鐘時 lint 會提醒你，讓你決定要不要上」).
 */
export const CONTENT_LENGTH_WARN_MINUTES = 8;
/** From this many minutes a content-led draft is read as an episode (its shape and storytelling checks run). */
export const CONTENT_EPISODE_MINUTES = 5;
const CONTENT_LENGTH_PRESETS = new Set([CURIO_PRESET, "cute-cartoon"]);

/**
 * Whether an episode's length follows its material instead of the eight-minute floor: an
 * explainer of 奇聞檔案局 (cute-mystery) or 原來如此事務所 (cute-cartoon). The owner dropped the
 * floor for these two on 2026-11-11, after the producer review found viewers leaving in the first
 * minute and padding to eight minutes only thinned the script. A brand story (category "story")
 * wears the same look and keeps its own 13-minute rule (by category, slug or series); flat-explainer keeps the floor.
 */
export const followsContentLength = (doc) => isExplainer(doc) && CONTENT_LENGTH_PRESETS.has(doc.look?.preset)
  // A brand story drawn in the cute-mystery look keeps its rules even when its category is
  // "explainer" (the owner's short C08 and C20 revisions carry their own exact bands).
  && !/^story-/.test(doc.slug ?? "") && !/^brand-stories/.test(doc.series?.slug ?? "");

// The bookends are not the body: the opening title, chapter cards and the outro card.
const FRAMES = new Set(["title", "chapter", "outro"]);

/** Whether a video is an episode of 奇聞檔案局: its slug starts with "curio-". */
export const isCurio = (doc) => /^curio-/.test(doc?.slug ?? "");

/** The series-look problems of a 奇聞檔案局 episode, as lint errors; none for any other video. */
export function curioProblems(doc) {
  if (!isCurio(doc)) return [];
  const problems = [];
  const want = resolveLook({ preset: CURIO_PRESET });
  const look = resolveLook(doc.look);
  if (!doc.look) {
    problems.push({ path: "look", message: `a 奇聞檔案局 episode is drawn in the series look: write "look": { "preset": "${CURIO_PRESET}" } (skill curio-episode)` });
  } else if (look.style !== want.style) {
    // A style that adds period materials, landscape shapes or a mood to the series sentence is what
    // drifted to photographs and paintings in the H04-H06 pilots (look.md §樣張): what a shot shows
    // belongs in its prompt, never in the look.
    problems.push({ path: "look.style", message: `the series look is the "${CURIO_PRESET}" preset's style word for word: drop look.style and put what the picture shows in each shot's prompt` });
  }
  if (doc.look && look.negative !== "") problems.push({ path: "look.negative", message: "MiniMax reads look.negative as part of the prompt (\"Avoid: …\"), so the series leaves it empty: say what the picture is instead" });

  const body = (doc.scenes ?? []).filter((scene) => !FRAMES.has(scene.template));
  if (!body.length) return problems;
  const shots = body.filter(isShot).length;
  const share = shots / body.length;
  if (share < CURIO_MIN_SHOT_SHARE) {
    problems.push({ path: "scenes", message: `${shots} of ${body.length} body scenes are illustrations (${Math.round(share * 100)}%); a 奇聞檔案局 episode draws at least ${Math.round(CURIO_MIN_SHOT_SHARE * 100)}% of them as "shot" scenes and keeps cards for a number, a name or a source` });
  }
  let run = [];
  const runs = [];
  for (const scene of [...body, null]) {
    if (scene && !isShot(scene)) { run.push(scene.id); continue; }
    if (run.length > CURIO_MAX_CARD_RUN) runs.push(run);
    run = [];
  }
  for (const ids of runs) {
    problems.push({ path: "scenes", message: `${ids.length} cards in a row (${ids[0]} … ${ids.at(-1)}); a 奇聞檔案局 episode puts an illustration between at most ${CURIO_MAX_CARD_RUN} cards` });
  }
  return problems;
}

/** What a 奇聞檔案局 episode should still have, as lint warnings: its music bed. None for any other video. */
export function curioWarnings(doc) {
  if (!isCurio(doc)) return [];
  const warnings = [];
  // The local route's default is CC, so an episode has to say so (the owner, 2026-10-31).
  // The owner, 2026-11-04: 奇聞檔案局 no longer burns subtitles in (zh-TW is a CC track like the rest).
  if (doc.subtitles?.burn_in === true) warnings.push({ path: "subtitles.burn_in", message: '奇聞檔案局 no longer burns its zh-TW subtitles in (owner, 2026-11-04): write "subtitles": { "burn_in": false } or leave it out' });
  if (doc.music) return warnings;
  return [...warnings, { path: "music", message: `a 奇聞檔案局 episode carries a music bed under the narration, as the brand stories do (owner, 2026-10-19): add "music": ${JSON.stringify(CURIO_MUSIC)} and run the music step (skill curio-episode)` }];
}
