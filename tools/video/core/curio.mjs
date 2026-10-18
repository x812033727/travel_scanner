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
