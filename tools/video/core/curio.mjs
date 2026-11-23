// 奇聞檔案局 (docs/videos/history-curiosity/, skill curio-episode) is a series of cute cartoon
// illustrations under one narrator, not a deck of cards. The owner chose the look on 2026-10-10
// ("內容相關的可愛插畫", MiniMax image-01, the third audition style, now the cute-mystery preset), and
// every delivered episode draws 73-95% of its body as illustrations with at most three cards in a
// row. The H04-H06 remakes of 2026-10-14 drifted to 88 cards and no illustration at all, with no
// check to stop them: the rules lived in look.md and in one agent's notes. These are that check, so
// whichever model makes an episode, a slug that starts with "curio-" keeps the series look.
import { isShot, resolveLook } from "./drama.mjs";

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
 * The most shots in one episode that may lean on the same generic stand-in prop (a fat/flat purse
 * or wallet, a thick plain-covered book). Measured on curio-w01 (4 purses), curio-w02 (7 purses),
 * curio-s13-v2 (9 plain books) and curio-s26-v2 (10 plain books) against 黑貓研究院's topic-specific
 * physical props (2026-11-18; register.mjs STORY_SERIES_SCREEN_RULE).
 */
export const GENERIC_PROP_MAX = 2;
export const GENERIC_PROP_FAMILIES = Object.freeze([
  Object.freeze({ id: "purse", label: "purse/wallet (錢包／皮夾)", pattern: /\b(?:purses?|wallets?)\b/i }),
  Object.freeze({ id: "plain-book", label: "thick/plain-covered book (空白厚書)", pattern: /\b(?:thick\s+(?:plain[- ]covered\s+)?books?|plain[- ]covered\s+books?)\b/i }),
]);
export const isGenericPropSeries = (doc) => /^(?:curio|sothatswhy|story)-/.test(doc?.slug ?? "");

/** Warn when a paced or story episode repeats a generic purse/wallet or plain-book stand-in in 3+ shots. */
export function genericPropWarnings(doc) {
  if (!isGenericPropSeries(doc) || doc?.format !== "drama") return [];
  const shots = (doc.scenes ?? []).filter((scene) => isShot(scene) && typeof scene.data?.prompt === "string");
  if (shots.length <= GENERIC_PROP_MAX) return [];
  const warnings = [];
  for (const family of GENERIC_PROP_FAMILIES) {
    const matched = shots.filter((scene) => family.pattern.test(scene.data.prompt)).map((scene) => scene.id);
    if (matched.length <= GENERIC_PROP_MAX) continue;
    warnings.push({
      path: "scenes",
      message: `${matched.length} shots draw the generic ${family.label} stand-in (${matched.slice(0, 6).join(", ")}${matched.length > 6 ? " …" : ""}); cap any generic stand-in at ${GENERIC_PROP_MAX} shots an episode and draw topic-specific wordless physical objects or cross-sections from this story instead (register.mjs STORY_SERIES_SCREEN_RULE)`,
    });
  }
  return warnings;
}

/**
 * Nameless demonstrative/pronoun openings that hide the episode's subject on a Heimao thumbnail
 * (owner, 2026-11-20: curio-s10-v2 dropped to 1.8% CTR when "本能寺" was hidden behind "這句話根本沒寫？").
 */
export const NAMELESS_HEIMAO_HEADLINE = /^(?:這句話|這個人|這兩(?:個)?字|這件事|這本書|這張紙|這顆(?![A-Za-z0-9\u4e00-\u9fff]*錶)|這台|這支|這個|它(?![A-Za-z0-9])|他(?![A-Za-z0-9])|她(?![A-Za-z0-9])|誰喊的)/u;

/** Warn when a curio-, sothatswhy- or story- Heimao thumbnail opens with a nameless pronoun instead of naming the subject. */
export function heimaoSubjectWarnings(doc) {
  if (!isGenericPropSeries(doc) || doc?.format !== "drama") return [];
  const data = doc.thumbnail?.data;
  if (!data || !["heimao", "heimao-left"].includes(data.layout) || typeof data.headline !== "string") return [];
  const plain = data.headline.replace(/\*\*/g, "").replace(/^[\s「『"“¿¡]+/u, "");
  if (!NAMELESS_HEIMAO_HEADLINE.test(plain)) return [];
  return [{
    path: "thumbnail.data.headline",
    message: `heimao headline "${data.headline}" opens with a nameless demonstrative/pronoun instead of naming the recognizable person, event, brand or signature object up front (owner, 2026-11-20); put the subject name in line 1`,
  }];
}

/**
 * What a paced series' drama is missing of SERIES_PACING (plus generic-prop overuse and nameless
 * Heimao headlines across the illustrated series), as lint warnings. A local video is never changed
 * behind its back: tightening the pauses moves the timeline an owner may already have approved, so
 * the warning names the fields and the re-approval they cost.
 */
export function pacingWarnings(doc) {
  if (doc?.format !== "drama") return [];
  if (!isPacedSeries(doc)) return [...genericPropWarnings(doc), ...heimaoSubjectWarnings(doc)];
  const warnings = [];
  if (doc.pauses === undefined) warnings.push({ path: "pauses", message: `this series closes the gaps between sentences (owner, 2026-11-05): add "pauses": ${JSON.stringify(SERIES_PACING.pauses)}; the timeline moves, so the narration and storyboard go back to the owner (the voice is not re-recorded)` });
  if (doc.still_motion === undefined) warnings.push({ path: "still_motion", message: `this series' stills hold and then move instead of gliding (owner, 2026-11-05): add "still_motion": "${SERIES_PACING.still_motion}" (only the cut changes; no picture is redrawn)` });
  warnings.push(...genericPropWarnings(doc), ...heimaoSubjectWarnings(doc));
  return warnings;
}

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
