#!/usr/bin/env node
// Craft check for one drama episode with a cast: is the storyboard structured the way the
// dramas that were measured are, before any picture is paid for?
//
//   node .agents/skills/youtube-video/scripts/drama_craft_check.mjs <file> [--json] [--strict]
//
// <file> is a drama `video.json` (lengths are estimated from the lines, the way `lint` does) or a
// measured edit (`shots[]` with `editorial_duration_s`, as the competition pilot writes them).
// It prints one row per check: the value, the target, what the reference dramas measured, and
// under a missed row the shots that cause it. --json adds one entry per shot (how its size, its
// camera move and its motion were read), which is how a misreading is found.
// Exit code 0 unless --strict is given and a check missed (1); 2 when the file cannot be read.
//
// `lint` answers "can the pipeline build this"; this answers "is the storyboard built like the
// ones that were measured". Every target comes from
// .agents/skills/youtube-video/references/drama-craft.md, which records where the numbers were
// measured, which targets are editorial rules, and what none of them prove. A miss is a question
// the writer answers in the report (fix it, or say why this episode is different); it blocks no
// command, and it is never a reason to lower a target for one episode.
//
// The shot-size, camera-move and motion rows read the English `camera`, `prompt` and `motion`
// text, so they are heuristics. They agree with a shot-by-shot hand reading of the 81 pilot
// shots on 80 sizes and 81 motions (the study record has the comparison); a shot that names no
// size counts as unknown rather than guessed; and meeting every row says the storyboard is
// structured, not that the picture is good.
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

// The estimate `tools/video/core/timeline.mjs` uses, repeated here so the script has no imports:
// a spoken character is 0.24 s, each line adds its pause, each scene adds the gap.
export const CPM = 250;
export const PAUSE_MS = 300;
export const SCENE_GAP_MS = 700;
const NARRATOR = "narrator";
// `lint` refuses a scene without lines; when one is met anyway it is counted with this length so
// it cannot make an opening look denser than it is.
export const SILENT_SHOT_SECONDS = 2;

export const TARGETS = {
  medianShotSeconds: [2, 4],
  p90ShotSeconds: 6,
  longestShotSeconds: 8,
  spread: 2, // 90th percentile length divided by the 10th
  opening10Shots: 4, // shots that start inside the first ten seconds
  opening30Shots: 10, // and inside the first thirty
  firstCharacterLineSeconds: 10,
  medianLineUnits: 12,
  longLineUnits: 20,
  longLineShare: 0.1,
  narratorShare: 0.35,
  unknownSizeShare: 0.2,
  faceShare: 0.4,
  insertShare: [0.05, 0.25],
  wideShare: [0.05, 0.3],
  wideGapShots: 9, // at most nine shots in a row without a wide or group shot
  sameSetupRun: 2,
  lookOnlyShare: 1 / 3,
  lookOnlyRun: 2,
  sameMoveRun: 3,
  dissolveShare: 0.1,
};

// What the five reference dramas measured on 2026-10-03 (drama-craft.md has the table). A row
// without a reference is an editorial rule.
const REFERENCE = {
  median: "1.5–2.25 s",
  p90: "2.5–4.75 s",
  longest: "3.75–10.25 s",
  spread: "3.3–6.3",
  opening10: "4–8",
  opening30: "12–18",
  firstLine: "first subtitle at 0.6–1.3 s",
  lineUnits: "1–11, median 4 in the one counted",
  narrator: "the first minute's subtitles read as dialogue in four of five",
  face: "a readable face in most shots, by eye",
  insert: "about 5–17%, one counted and two by eye",
  wide: "a wide or group shot every 6–8 shots, by eye",
};

const CJK = /[぀-ヿ㐀-鿿豈-﫿가-힯]/u;
const SPOKEN_TOKEN = /[A-Za-z][A-Za-z0-9.+#'_-]*|[0-9][0-9.,:/%]*|[぀-ヿ㐀-鿿豈-﫿가-힯]/gu;

/** Characters as they are spoken: a CJK character is one, a Latin word or a run of digits two. */
export function spokenUnits(text) {
  let units = 0;
  for (const token of String(text ?? "").match(SPOKEN_TOKEN) ?? []) units += CJK.test(token) ? 1 : 2;
  return units;
}

// A thing rather than a face: a close framing "of" one of these is an insert.
const OBJECT = "(?:hands?|fingers?|fist|palm|thumb|pen|papers?|documents?|copy|copies|pages?|phone|ring|cup|bowl|keys?|letter|screen|ticket|seal|stamp|blade|sword|foot|feet|props?|objects?|original|contract|envelope|receipt|box|bag|tray|table)";
const EXPLICIT_INSERT = /\binsert\b|detail shot|\bmacro\b/;
// "close-up of <a thing>": the words between may describe the thing, not a person doing something.
const OF_OBJECT = new RegExp(`(?:close[- ]?up|shot|view|framing) (?:of|on) ((?:[\\w'’-]+ ){0,3}?)${OBJECT}\\b`);
const NOT_A_MODIFIER = /ing$|^(?:at|around|with|near|behind|beside|by|in|from|over|under|across)$/;
const OBJECT_SHOT = new RegExp(`\\b${OBJECT}(?:-[\\w-]+)? (?:close[- ]?up|shot)`);
const OVERHEAD_CLOSE = /(?:overhead|top-down)[\w ,-]{0,24}close[- ]?up/;
const FACE_IN_FRAME = /\bface\b|medium close[- ]?up|reaction shot|over[- ]the[- ]shoulder/;

function isInsert(lower) {
  if (FACE_IN_FRAME.test(lower)) return false;
  const of = OF_OBJECT.exec(lower);
  if (of && !of[1].trim().split(" ").filter(Boolean).some((word) => NOT_A_MODIFIER.test(word))) return true;
  return OBJECT_SHOT.test(lower) || OVERHEAD_CLOSE.test(lower);
}
// The size a `camera` line leads with wins: the spec asks writers to start the line with it.
const LEADING_SIZE = [
  ["ecu", /^extreme close[- ]?up\b/],
  ["mcu", /^medium close[- ]?up\b/],
  ["cu", /^close[- ]?up\b/],
  ["ots", /^over[- ]the[- ]shoulder\b/],
  ["group", /^(?:two|three)[- ]shot\b|^group shot\b/],
  ["ms", /^(?:medium|mid) shot\b/],
  ["ws", /^(?:extreme )?wide\b|^establishing\b/],
  ["pov", /^pov\b|^point of view\b/],
];
const LEADING_QUALIFIER = /^(?:(?:locked|static|fixed|handheld|slow|oblique|overhead|low[- ]angle|high[- ]angle|table[- ]level)[ ,]+)+/;
// Otherwise the first size named anywhere in the `camera` line, in this order.
const CAMERA_SIZES = [
  ["ecu", /extreme close[- ]?up|\becu\b/],
  ["mcu", /medium close[- ]?up|\bmcu\b|head[- ]and[- ]shoulders|chest[- ]up/],
  ["cu", /close[- ]?up|closeup/],
  ["ots", /over[- ]the[- ]shoulder|\bots\b/],
  ["group", /(?:two|three)[- ]shot|group shot|ensemble shot/],
  ["ms", /medium shot|mid shot|medium wide|waist[- ]up|cowboy shot/],
  ["ws", /wide[- ](?:shot|angle|view|establishing|frame|framing)|establishing|long shot|full shot|full-body shot|aerial|bird'?s[- ]eye/],
  ["pov", /\bpov\b|point of view/],
];
// From a `prompt` only an explicit shot-size phrase counts: a prompt also says "wide sleeves".
const PROMPT_SIZES = [
  ["ecu", /extreme close[- ]?up/],
  ["mcu", /medium close[- ]?up/],
  ["cu", /\bclose[- ]?up\b/],
  ["ots", /over[- ]the[- ]shoulder/],
  ["group", /(?:two|three)[- ]shot|group shot/],
  ["ms", /medium shot|mid shot|waist[- ]up/],
  ["ws", /wide (?:shot|angle|establishing)|establishing shot|long shot|full shot|aerial shot|bird'?s[- ]eye view/],
  ["pov", /\bpov\b|point of view/],
];
// A face the audience can read: the close sizes, and the far person of an over-the-shoulder.
const FACE = new Set(["ecu", "cu", "mcu", "ots"]);
// Where everyone stands: a wide shot, or two or more people held in one frame.
const WIDE = new Set(["ws", "group"]);
const family = (size) => (FACE.has(size) ? "face" : WIDE.has(size) ? "wide" : size);

// The word "Insert" wins; then the size the line leads with, unless that is a plain close-up,
// which is an insert when it is a close-up of a thing; then the first size named anywhere.
function sizeIn(text, sizes) {
  const lower = String(text ?? "").toLowerCase().trim();
  if (!lower) return null;
  if (EXPLICIT_INSERT.test(lower)) return "insert";
  const head = lower.replace(LEADING_QUALIFIER, "");
  const leading = LEADING_SIZE.find(([, pattern]) => pattern.test(head))?.[0] ?? null;
  if (leading && leading !== "cu") return leading;
  if (isInsert(lower)) return "insert";
  if (leading) return leading;
  for (const [size, pattern] of sizes) if (pattern.test(lower)) return size;
  return null;
}

/**
 * The shot size a shot names: "insert", "ecu", "cu", "mcu", "ots", "group", "ms", "ws", "pov",
 * or null when neither its camera line nor its prompt says. A close framing of a hand or a prop
 * is an insert unless the line also says a face is in the frame.
 */
export function shotSize(data) {
  return sizeIn(data?.camera, CAMERA_SIZES) ?? sizeIn(data?.prompt, PROMPT_SIZES);
}

/** True when the camera line and the prompt each name a size and the two are of different kinds. */
export function sizesDisagree(data) {
  const camera = sizeIn(data?.camera, CAMERA_SIZES), prompt = sizeIn(data?.prompt, PROMPT_SIZES);
  return camera !== null && prompt !== null && family(camera) !== family(prompt);
}

// Camera phrasing only: a move counts at the start of the line or of a clause, or after a word
// that describes a camera ("slow push in"), never after a person ("she pushes in the drawer").
const AT_CLAUSE = "(?:^|[,;.:] ?|\\b(?:and|then|slow|slowly|gentle|gently|subtle|quick|fast|smooth|steady|camera|handheld|low|high) )";
const move = (phrases) => new RegExp(`${AT_CLAUSE}(?:${phrases})\\b`);
const MOVES = [
  ["locked", /\blocked\b|\bstatic\b|fixed (?:camera|frame|shot)|tripod|no camera move|still camera/],
  ["pull", move("pull(?:s|ing)?[- ](?:back|out)|pull-?back|dolly(?:ing)? out|zoom(?:s|ing)? out|widen(?:s|ing)?|back(?:s|ing)? away")],
  ["push", move("push(?:es|ing)?[- ]?in|dolly(?:ing)? in|zoom(?:s|ing)?(?: in)?|mov(?:e|es|ing) in|closer")],
  ["pan", move("pan(?:s|ning)?")],
  ["tilt", move("tilt(?:s|ing)?|crane(?:s|ing)?|pedestal|rises?|descend(?:s|ing)?")],
  ["track", move("track(?:s|ing)?|truck(?:s|ing)?|follow(?:s|ing)?|handheld|orbit(?:s|ing)?|arc(?:s|ing)? (?:left|right|around)|steadicam")],
];

/** The camera move a shot's camera line names; "none" when it names none. */
export function cameraMove(data) {
  const lower = String(data?.camera ?? "").toLowerCase();
  for (const [move, pattern] of MOVES) if (pattern.test(lower)) return move;
  return "none";
}

// Small behaviour: the eyes, the expression, a breath, a tremor, holding still. Everything else
// a motion line can say is treated as an action, because the small set is the closed one.
const FACE_PART = "(?:gaze|eyes?|eyelids?|expression|smile|brows?|lips?|jaw|mouth|breath|breathing)";
const SMALL = [
  // the subject is a part of the face: "His polite smile fades", "Her eyes close"
  new RegExp(`^(?:[\\w'’-]+ ){0,6}?${FACE_PART} \\w+`),
  // a person moves only their eyes: "She turns her gaze back", "He lifts his eyes"
  new RegExp(`\\b(?:turns?|lifts?|raises?|lowers?|drops?|shifts?|moves?|holds?|keeps?|fixes|narrows?|closes?|shuts?|squeezes?|opens?|widens?) (?:his|her|their|the) (?:[\\w-]+ )?${FACE_PART}\\b`),
  /\b(?:his|her|their) face (?:falls|hardens|softens|tightens|pales|flushes|darkens|stills|freezes|crumples)\b/,
  // being there is not doing something: "She stands at the table", "He waits", "She holds the pen"
  /^(?:[\w'’-]+ ){0,4}?(?:stands?|sits?|kneels?|lies|waits?|pauses?|hesitates?|faces|remains?|stays?|holds?)\b(?! (?:up|down|out|back|away|off)\b)/,
  /^(?:[\w'’-]+ ){0,4}?(?:looks?|glances?|stares?|gazes?|studies|watches|blinks?|breathes?|swallows?|frowns?|smiles?|smirks?|squints?|waits?|listens?|reads?)\b/,
  /(?:^|\b(?:a|her|his|their|the) )(?:single |lone )?tears? (?:falls?|wells?|rolls?|streams?|runs?|slides?)\b/,
  // a hand that only tightens or shakes
  /\b(?:hands?|fingers?|fist|grip|knuckles?) (?:\w+ly )?(?:tightens?|trembles?|quivers?|twitch(?:es)?|shakes?|clench(?:es)?|whitens?|curls?)\b/,
  /\b(?:tightens?|clench(?:es)?|closes?|curls?) (?:his|her|their) (?:fingers?|fist|grip|hand)\b/,
  /\b(?:stands?|sits?|remains?|stays?|holds?) (?:very |perfectly |completely )?(?:still|motionless|frozen)\b/,
  /^(?:[\w'’-]+ ){0,3}?(?:trembles?|shivers?|sways?|flickers?)\b/,
];

/** The first clause of a motion line: the one behaviour the shot is about. */
function mainClause(motion) {
  return String(motion ?? "").toLowerCase().trim().split(/[,;.]| and | while | without | as | then /)[0].trim();
}

/**
 * The shot's one behaviour is no larger than a look, a breath or a tremor (or it names none).
 * A camera move does not change the answer: a slow push on a face that only looks is still a
 * look. Reaction shots are these, and a scene needs them; the rows ask how many and how many
 * in a row.
 */
export function isLookOnly(data) {
  const motion = String(data?.motion ?? "").toLowerCase();
  // lifting or turning the head in order to look is a look written another way
  if (/\b(?:lifts?|raises?|turns?|tilts?) (?:his|her|their) head (?:to|toward|towards|and) (?:looks?|faces?|sees?|watch(?:es)?|meets?|stares?|gazes?)\b/.test(motion)) return true;
  const clause = mainClause(motion);
  return clause === "" || SMALL.some((pattern) => pattern.test(clause));
}

function lineSeconds(line) {
  return (spokenUnits(line.text) * 60) / CPM + (line.pause_after_ms ?? PAUSE_MS) / 1000;
}

/**
 * Either input as one list: [{ id, card, seconds, silent, data, lines: [{ speaker, text, at }] }].
 * In an estimated document a shot without lines has no length of its own (`lint` refuses it);
 * it is given SILENT_SHOT_SECONDS and marked `silent`.
 */
export function normalize(doc) {
  if (Array.isArray(doc?.shots) && doc.shots.some((shot) => Number.isFinite(shot?.editorial_duration_s))) {
    return {
      measured: true,
      cast: true,
      shots: doc.shots.map((shot) => ({
        id: shot.shot_id ?? shot.scene_id,
        card: false,
        seconds: Number.isFinite(shot.editorial_duration_s) ? shot.editorial_duration_s : SILENT_SHOT_SECONDS,
        silent: false,
        data: shot.data ?? {},
        lines: (shot.voice_placements ?? []).map((line) => ({ speaker: line.speaker_id ?? NARRATOR, text: line.text, at: line.start_s })),
      })),
    };
  }
  if (!Array.isArray(doc?.scenes)) throw new Error("neither a video.json (scenes[]) nor a measured edit (shots[] with editorial_duration_s)");
  if (doc.format !== undefined && doc.format !== "drama") throw new Error(`format "${doc.format}" is not a drama; these targets are for dramas with a cast`);
  return {
    measured: false,
    cast: Array.isArray(doc.characters) && doc.characters.length > 0,
    shots: doc.scenes.map((scene) => {
      const lines = (scene?.lines ?? []).map((line) => ({ speaker: line.speaker ?? NARRATOR, text: line.text, seconds: lineSeconds(line), inner: /^內心獨白/.test(line.emotion ?? "") }));
      const spoken = lines.reduce((sum, line) => sum + line.seconds, 0);
      // A long-anime production may time a shot without lines with `action_seconds`.
      const action = !lines.length && Number.isFinite(scene?.action_seconds) ? scene.action_seconds : null;
      return {
        id: scene?.id,
        card: scene?.template !== "shot",
        seconds: lines.length ? spoken + SCENE_GAP_MS / 1000 : (action ?? SILENT_SHOT_SECONDS),
        silent: lines.length === 0 && action === null,
        data: scene?.data ?? {},
        lines,
      };
    }),
  };
}

export const quantile = (sorted, p) => sorted[Math.min(sorted.length - 1, Math.floor(p * sorted.length))];
const share = (count, total) => (total ? count / total : 0);
const percent = (value) => `${Math.round(value * 100)}%`;
const seconds = (value) => `${value.toFixed(1)} s`;

/** The longest run of consecutive eligible items that are each `same` as the one before, as the items themselves. */
function longestRun(items, eligible, same = () => true) {
  let best = [], run = [];
  for (const item of items) {
    if (!eligible(item)) run = [];
    else if (run.length && same(item, run.at(-1))) run = [...run, item];
    else run = [item];
    if (run.length > best.length) best = run;
  }
  return best;
}

// The same camera position again: the camera line and the prompt up to its first comma, verbatim.
const setupKey = (row) => `${String(row.data.camera ?? "").trim().toLowerCase()}|${String(row.data.prompt ?? "").split(/[,.;]/)[0].trim().toLowerCase()}`;

/**
 * { applies, measured, shots, total_seconds, rows, checks }.
 * rows: one per shot, { id, start, seconds, size, move, look_only, lines }.
 * checks: { id, label, value, target, reference, ok, hint, shots } — `shots` names the shots
 * that cause a miss, `info: true` marks a row that is only reported.
 * `applies` is false for a document without a cast (an explainer, a brand story): their pace
 * and narration follow their own references, and no row is printed.
 */
export function craftChecks(doc) {
  const { shots: all, measured, cast } = normalize(doc);
  let clock = 0;
  const placed = all.map((shot) => {
    const start = clock;
    clock += shot.seconds;
    return { ...shot, start };
  });
  const rows = placed.filter((shot) => !shot.card).map((shot) => ({
    id: shot.id,
    start: +shot.start.toFixed(2),
    seconds: +shot.seconds.toFixed(2),
    size: shotSize(shot.data),
    move: cameraMove(shot.data),
    look_only: isLookOnly(shot.data),
    lines: shot.lines.length,
    data: shot.data,
    silent: shot.silent,
    spoken: shot.lines,
  }));
  const total = rows.reduce((sum, row) => sum + row.seconds, 0);
  const publicRows = rows.map(({ data, spoken, silent, ...row }) => row);
  if (!cast) return { applies: false, measured, shots: rows.length, total_seconds: total, rows: publicRows, checks: [] };
  const checks = [];
  const add = (id, label, value, target, ok, hint, { reference = "", shots = [], info = false } = {}) =>
    checks.push({ id, label, value, target, reference, ok, hint, shots: ok ? [] : shots.map((row) => row.id), ...(info ? { info: true } : {}) });

  // Pace.
  const byLength = [...rows].sort((a, b) => a.seconds - b.seconds);
  const lengths = byLength.map((row) => row.seconds);
  if (lengths.length >= 3) {
    const median = quantile(lengths, 0.5), p90 = quantile(lengths, 0.9), p10 = quantile(lengths, 0.1), longest = lengths.at(-1);
    const [low, high] = TARGETS.medianShotSeconds;
    add("pace.median", "median shot", seconds(median), `${low}–${high} s`, median >= low && median <= high, median > high ? "split the long shots: one short line, one picture" : "faster than the references themselves: merge shots", { reference: REFERENCE.median });
    add("pace.p90", "90th percentile shot", seconds(p90), `≤ ${TARGETS.p90ShotSeconds} s`, p90 <= TARGETS.p90ShotSeconds, "a long hold has to be a designed one; cut to the listener's face or an insert", { reference: REFERENCE.p90, shots: rows.filter((row) => row.seconds > TARGETS.p90ShotSeconds) });
    add("pace.longest", "longest shot", seconds(longest), `≤ ${TARGETS.longestShotSeconds} s`, longest <= TARGETS.longestShotSeconds, "longer than the shortest clip the pipeline buys", { reference: REFERENCE.longest, shots: rows.filter((row) => row.seconds > TARGETS.longestShotSeconds) });
    const spread = p10 > 0 ? p90 / p10 : 0;
    const brief = rows.filter((row) => row.seconds < 2);
    add("pace.short", "shots under 2 s", `${brief.length}${brief.length ? `: ${brief.slice(0, 8).map((row) => row.id).join(", ")}` : ""}`, "reported", true, "", { info: true });
    add("pace.spread", "long shots against short ones (90th ÷ 10th percentile)", spread.toFixed(1), `≥ ${TARGETS.spread}`, spread >= TARGETS.spread, "every shot the same length is a metronome: a three-to-five-character line for a quick shot, two lines held on one shot before a reveal", { reference: REFERENCE.spread });
  }

  // The opening, on the body's own clock (a channel intro, when one is installed, plays before it).
  const opening10 = rows.filter((row) => row.start < 10).length, opening30 = rows.filter((row) => row.start < 30).length;
  let firstCharacterAt = null;
  for (const row of rows) {
    let at = row.start;
    for (const line of row.spoken) {
      const start = Number.isFinite(line.at) ? line.at : at;
      if (firstCharacterAt === null && line.speaker !== NARRATOR) firstCharacterAt = start;
      at += line.seconds ?? 0;
    }
  }
  add("hook.opening", "shots that start in the first 10 s", String(opening10), `≥ ${TARGETS.opening10Shots}`, opening10 >= TARGETS.opening10Shots, "open inside the event: place, the lead doing something, the lead's face, the other side's reaction", { reference: REFERENCE.opening10, shots: rows.filter((row) => row.start < 10) });
  if (clock >= 30) add("hook.opening30", "shots that start in the first 30 s", String(opening30), `≥ ${TARGETS.opening30Shots}`, opening30 >= TARGETS.opening30Shots, "the opening half-minute is where the density goes", { reference: REFERENCE.opening30 });
  add("hook.card", "first scene", all[0]?.card ? "a card" : "a shot", "a shot", !all[0]?.card, "no title card before the first picture; a title can follow the cold open");
  add("hook.dialogue", "first line spoken by a character", firstCharacterAt === null ? "never" : seconds(firstCharacterAt), `≤ ${TARGETS.firstCharacterLineSeconds} s`, firstCharacterAt !== null && firstCharacterAt <= TARGETS.firstCharacterLineSeconds, "let someone in the scene speak first; a retelling with no speaking characters answers this row in the report", { reference: REFERENCE.firstLine });

  // Lines.
  if (!measured) add("lines.empty", "shots without a line", String(rows.filter((row) => row.silent).length), "0", rows.every((row) => !row.silent), "outside a long-anime production (`action_seconds`) `lint` refuses a scene without lines; put the off-screen speaker's line on the reaction shot", { shots: rows.filter((row) => row.silent) });
  const lines = rows.flatMap((row) => row.spoken.map((line) => ({ ...line, row })));
  if (lines.length) {
    const units = lines.map((line) => spokenUnits(line.text)).sort((a, b) => a - b);
    const spokenTotal = units.reduce((sum, value) => sum + value, 0);
    const medianUnits = quantile(units, 0.5);
    const long = lines.filter((line) => spokenUnits(line.text) > TARGETS.longLineUnits);
    add("lines.median", "median line length", `${medianUnits} characters`, `≤ ${TARGETS.medianLineUnits}`, medianUnits <= TARGETS.medianLineUnits, "people in a scene speak in short turns; break the sentence where the cut goes", { reference: REFERENCE.lineUnits });
    add("lines.long", `lines over ${TARGETS.longLineUnits} characters`, percent(share(long.length, lines.length)), `≤ ${percent(TARGETS.longLineShare)}`, share(long.length, lines.length) <= TARGETS.longLineShare, "a line this long holds one picture too long; split it across two shots", { shots: long.map((line) => line.row) });
    const narrator = share(lines.filter((line) => line.speaker === NARRATOR || line.inner).reduce((sum, line) => sum + spokenUnits(line.text), 0), spokenTotal);
    add("lines.narrator", "narration and inner voice, share of the spoken text", percent(narrator), `≤ ${percent(TARGETS.narratorShare)}`, narrator <= TARGETS.narratorShare, "turn narration into what a character says or does; keep it for time jumps", { reference: REFERENCE.narrator });
  }

  // Coverage.
  if (rows.length >= 6) {
    const named = rows.filter((row) => row.size !== null);
    const unnamed = rows.filter((row) => row.size === null);
    add("size.named", "shots that name no shot size", percent(share(unnamed.length, rows.length)), `≤ ${percent(TARGETS.unknownSizeShare)}`, share(unnamed.length, rows.length) <= TARGETS.unknownSizeShare, "start `camera` with the size: Wide, Medium shot, Medium close-up, Close-up, Insert …", { shots: unnamed });
    const disagree = rows.filter((row) => sizesDisagree(row.data));
    add("size.agree", "shots whose camera line and prompt name different sizes", String(disagree.length), "0", disagree.length === 0, "the picture model receives both; write one size, in both places or only in `camera`", { shots: disagree });
    if (named.length >= 6) {
      const of = (test) => share(named.filter((row) => test(row.size)).length, named.length);
      const face = of((size) => FACE.has(size)), insert = of((size) => size === "insert"), wide = of((size) => WIDE.has(size));
      add("size.face", "faces (medium close-up and closer, over-the-shoulder)", percent(face), `≥ ${percent(TARGETS.faceShare)}`, face >= TARGETS.faceShare, "the audience follows a face; give each turn of the scene a face that reacts", { reference: REFERENCE.face });
      add("size.insert", "inserts", percent(insert), `${percent(TARGETS.insertShare[0])}–${percent(TARGETS.insertShare[1])}`, insert >= TARGETS.insertShare[0] && insert <= TARGETS.insertShare[1], "an insert answers a story question (which paper, whose hand); too few hides the proof, too many hides the people", { reference: REFERENCE.insert, shots: insert > TARGETS.insertShare[1] ? named.filter((row) => row.size === "insert") : [] });
      add("size.wide", "wide and group shots", percent(wide), `${percent(TARGETS.wideShare[0])}–${percent(TARGETS.wideShare[1])}`, wide >= TARGETS.wideShare[0] && wide <= TARGETS.wideShare[1], "show where everyone stands, briefly, then go back in", { reference: REFERENCE.wide });
      const gap = longestRun(rows, (row) => !WIDE.has(row.size));
      add("size.reestablish", "longest run without a wide or group shot", `${gap.length} shots`, `≤ ${TARGETS.wideGapShots}`, gap.length <= TARGETS.wideGapShots, "after a move, an entrance or a new beat, re-establish the room", { reference: REFERENCE.wide, shots: gap.length ? [gap[0], gap.at(-1)] : [] });
    }
    const cast = (row) => String([...(row.data.characters ?? [])].sort());
    // Shots with nobody in them (inserts) are "the same people" only when they are the same setup.
    const samePeople = (row, previous) => (cast(row) || cast(previous) ? cast(row) === cast(previous) : setupKey(row) === setupKey(previous));
    const stall = longestRun(rows, (row) => row.size !== null, (row, previous) => row.size === previous.size && samePeople(row, previous));
    add("size.stall", "same size on the same people in a row", `${stall.length} shots`, `≤ ${TARGETS.sameSetupRun}`, stall.length <= TARGETS.sameSetupRun, "the third one reads as a stall: cut to who is listening, or to what the hands are doing", { shots: stall });
    const uses = new Map();
    for (const row of rows) uses.set(setupKey(row), (uses.get(setupKey(row)) ?? 0) + 1);
    const reused = [...uses.values()].filter((count) => count > 1);
    add("size.setups", "camera setups", `${reused.length} used more than once (${reused.reduce((sum, count) => sum + count, 0)} shots), ${uses.size - reused.length} used once`, "reported", true, "", { info: true });
    const faces = rows.filter((row) => FACE.has(row.size));
    const listeners = faces.filter((row) => row.spoken.some((line) => line.speaker !== NARRATOR && !line.inner && !(row.data.characters ?? []).includes(line.speaker)));
    add("size.listeners", "faces shown while someone off screen speaks", `${listeners.length} of ${faces.length} face shots`, "reported", true, "", { info: true });
  }

  // Motion.
  if (rows.length >= 3) {
    const looks = rows.filter((row) => row.look_only);
    add("motion.look", "shots where the only behaviour is a look, a breath or a tremor", percent(share(looks.length, rows.length)), `≤ ${percent(TARGETS.lookOnlyShare)}`, share(looks.length, rows.length) <= TARGETS.lookOnlyShare, "reaction shots are needed, a third is the ceiling: elsewhere write what the person does to someone or something", { shots: looks });
    const lookRun = longestRun(rows, (row) => row.look_only);
    add("motion.run", "such shots in a row", `${lookRun.length} shots`, `≤ ${TARGETS.lookOnlyRun}`, lookRun.length <= TARGETS.lookOnlyRun, "three looks in a row is three portraits: put an action between them", { shots: lookRun });
    const openingStill = rows.slice(0, 3).every((row) => row.look_only);
    add("motion.opening", "first three shots", openingStill ? "all looks" : "something happens", "something happens", !openingStill, "the opening is an action in progress, not three portraits", { shots: rows.slice(0, 3) });
    // A locked camera is the absence of a move; a run of locked shots is judged by what happens in them.
    const moving = (row) => !["none", "locked"].includes(row.move);
    const moveRun = longestRun(rows, moving, (row, previous) => row.move === previous.move);
    add("motion.repeat", "same camera move in a row", `${moveRun.length} shots`, `≤ ${TARGETS.sameMoveRun}`, moveRun.length <= TARGETS.sameMoveRun, "vary it, or let the cut do the moving", { shots: moveRun });
    const locked = rows.filter((row) => row.move === "locked");
    add("motion.locked", "locked camera", `${locked.length} of ${rows.length}, longest run ${longestRun(rows, (row) => row.move === "locked").length}`, "reported", true, "", { info: true });
    const double = rows.filter((row) => /\b(?:and|then)\b/.test(String(row.data.motion ?? "").toLowerCase()));
    add("motion.double", "motion lines with a second action (and / then)", `${double.length}${double.length ? `: ${double.slice(0, 8).map((row) => row.id).join(", ")}` : ""}`, "reported", true, "", { info: true });
  }
  if (rows.length >= 6) {
    const dissolves = rows.filter((row) => row.data.transition === "dissolve");
    add("cut.dissolve", "dissolves", percent(share(dissolves.length, rows.length)), `≤ ${percent(TARGETS.dissolveShare)}`, share(dissolves.length, rows.length) <= TARGETS.dissolveShare, "a dissolve says time passed; everything else is a cut", { shots: dissolves });
  }

  return { applies: true, measured, shots: rows.length, total_seconds: total, rows: publicRows, checks };
}

function render(report, file) {
  const basis = report.measured ? "measured edit" : `estimated as lint does: ${60 / CPM} s a character, ${PAUSE_MS / 1000} s a line, ${SCENE_GAP_MS / 1000} s a shot`;
  const head = `${file}: ${report.shots} shots, ${report.total_seconds.toFixed(0)} s (${basis})`;
  if (!report.applies) return `${head}\nno cast: these targets are for dramas with characters; nothing checked.`;
  const out = [head];
  const width = Math.max(...report.checks.map((check) => check.label.length));
  for (const check of report.checks) {
    const mark = check.info ? "info" : check.ok ? "ok  " : "MISS";
    const basisNote = check.info ? "" : `  (target ${check.target}${check.reference ? `; reference ${check.reference}` : "; editorial rule"})`;
    out.push(`${mark}  ${check.label.padEnd(width)}  ${check.value}${basisNote}`);
    if (!check.ok) {
      out.push(`      → ${check.hint}  [${check.id}]`);
      if (check.shots.length) out.push(`      shots: ${check.shots.slice(0, 14).join(", ")}${check.shots.length > 14 ? `, … (${check.shots.length})` : ""}`);
    }
  }
  const judged = report.checks.filter((check) => !check.info);
  const missed = judged.filter((check) => !check.ok).length;
  out.push(missed ? `${missed} of ${judged.length} checks missed: fix them or answer each one in the report.` : `all ${judged.length} checks met: the storyboard is structured; whether it is good is judged on the picture.`);
  return out.join("\n");
}

function main(argv) {
  const flags = new Set(argv.filter((arg) => arg.startsWith("--")));
  const file = argv.find((arg) => !arg.startsWith("--"));
  if (!file) {
    console.error("usage: drama_craft_check.mjs <video.json | measured-edit.json> [--json] [--strict]");
    return 2;
  }
  let report;
  try {
    report = craftChecks(JSON.parse(readFileSync(file, "utf8")));
  } catch (error) {
    console.error(`${file}: ${error.message}`);
    return 2;
  }
  console.log(flags.has("--json") ? JSON.stringify(report, null, 2) : render(report, file));
  return flags.has("--strict") && report.checks.some((check) => !check.ok) ? 1 : 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) process.exitCode = main(process.argv.slice(2));
