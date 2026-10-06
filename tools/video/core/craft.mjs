// The drama craft check: is a storyboard with a cast structured the way the dramas that were
// measured are, before any picture is paid for? One implementation, read three ways: `lint`
// prints the missed rows as warnings, the worker's script verdict sends a hands-off episode
// back on the opening and coverage rows (CRAFT_GATE_ROWS), and the skill's command
// (.agents/skills/youtube-video/scripts/drama_craft_check.mjs) prints the whole table for an
// agent writing by hand. The host worker ships tools/video alone, which is why the reading
// lives here and not in the skill.
//
// Every target comes from .agents/skills/youtube-video/references/drama-craft.md, which records
// where the numbers were measured, which targets are editorial rules, and what none of them
// prove. A miss is a question the writer answers (fix it, or say why this episode is
// different); it blocks no command, and it is never a reason to lower a target for one episode.
//
// The shot-size, camera-move and motion rows read the English `camera`, `prompt` and `motion`
// text, so they are heuristics. They agree with a shot-by-shot hand reading of the 81 pilot
// shots on 80 sizes and 81 motions (the study record has the comparison); a shot that names no
// size counts as unknown rather than guessed; and meeting every row says the storyboard is
// structured, not that the picture is good. The slideshow-risk rows (risk.*) read the `prompt`
// and `motion` for who is in the shot, where it is and whether the camera is the one acting;
// --json shows what each shot was read as.
import { DEFAULT_CPM, DEFAULT_PAUSE_MS, FPS, SCENE_GAP_MS as GAP_MS, spokenUnits as timelineUnits } from "./timeline.mjs";

// The estimate `lint` uses (tools/video/core/timeline.mjs): a spoken character is 0.24 s, each
// line adds its pause, each scene adds the gap. With a timeline the lengths come from it instead.
export const CPM = DEFAULT_CPM;
export const PAUSE_MS = DEFAULT_PAUSE_MS;
export const SCENE_GAP_MS = GAP_MS;
const NARRATOR = "narrator";
// A shot with neither lines nor action_seconds has no length of its own (`lint` refuses it);
// when one is met anyway it is counted with this length so it cannot make an opening look
// denser than it is.
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
  // Slideshow risk (risk.*): the structure of sameness the first takes were sent back for.
  sameFramingRun: 2, // the same framing of the same people in the same place, in a row
  decorativeShare: 0.1, // shots with nobody in them that are not inserts
  cameraAsActor: 0, // motion lines where the camera moves and nobody does anything
  emptyBeatShare: 0.05, // silent shots in which nothing happens and nothing is revealed
  cards: 2, // title, chapter and quote cards, beyond which …
  cardShare: 0.1, // … they may still not carry more than a tenth of the running time
  claims: 0, // prompts that say "cinematic" where a size and a move should be
};

// What the five reference dramas measured on 2026-10-03 (drama-craft.md has the table). A row
// without a reference is an editorial rule.
export const REFERENCE = {
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
  framing: "a dialogue cuts speaker–listener–speaker between three or four setups, by eye",
  decorative: "a readable face in almost every shot, by eye; the 4 of 89 without one were inserts, in the one counted",
  cards: "no title card in five; the longest title picture 0.25 s",
};

// The rows a hands-off episode is sent back to the writer for (series.mjs scriptVerdict): how
// it opens, whether the scene is covered, and the three slideshow-risk rows that are structure
// rather than a reading of one line (the same setup drawn again, a place with nobody in it,
// cards carrying the story; measured 2026-10-05 on the five 偶的江湖 storyboards, which meet all
// three, and on the wedding pilot the owner sent back, which misses the first). The pace, line
// and motion rows stay warnings the writer answers, because a fix loop cannot judge a designed
// hold or a retelling's narration, and the remaining risk rows read one line's words.
export const CRAFT_GATE_ROWS = ["hook.opening", "hook.opening30", "hook.card", "hook.dialogue", "motion.opening", "size.face", "size.wide", "size.reestablish", "size.stall", "risk.setup_repeat", "risk.decorative", "risk.text_first"];

/** Characters as they are spoken: a CJK character is one, a Latin word or a run of digits two. */
export function spokenUnits(text) {
  return timelineUnits(text ?? "");
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
// The same framing, for the setup rows: an over-the-shoulder is its own axis (the camera is
// behind someone), so a close-up, the reverse over a shoulder and the close-up again are three
// setups, while a close-up, a medium close-up and an extreme close-up of one face are one.
const setupFamily = (size) => (size === "ots" ? "ots" : family(size));

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
  for (const [name, pattern] of MOVES) if (pattern.test(lower)) return name;
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

// Somebody in the frame: a person, a creature (a drama's lead may be a bird or a puppet), or a
// member of the cast by id or name. Read from the prompt and the motion line together.
const PERSON = /\b(?:he|she|they|him|his|hers?|their|man|men|woman|women|girls?|boys?|child(?:ren)?|kids?|bab(?:y|ies)|people|persons?|figures?|crowds?|guests?|servants?|maids?|soldiers?|guards?|officers?|villagers?|merchants?|monks?|nuns?|priests?|elders?|masters?|disciples?|students?|teachers?|doctors?|nurses?|mothers?|fathers?|parents?|sons?|daughters?|brothers?|sisters?|uncles?|aunts?|wives|wife|husbands?|brides?|grooms?|emperors?|empress(?:es)?|kings?|queens?|princes?|princess(?:es)?|lords?|lad(?:y|ies)|generals?|stewards?|clerks?|witness(?:es)?|strangers?|rivals?|friends?|couples?|famil(?:y|ies)|puppets?|puppeteers?|silhouettes?|warriors?|assassins?|swordsm[ae]n|hero(?:es)?|heroines?|boss(?:es)?|bod(?:y|ies)|corpses?|bird|birds|cranes?|dogs?|cats?|horses?|wol(?:f|ves)|tigers?|dragons?|fox(?:es)?|snakes?|fish|beasts?|creatures?|monsters?|spirits?|ghosts?|demons?|ox|oxen|cows?|sheep|goats?|deer|rabbits?|eagles?|hawks?|crows?|phoenix|lions?|bears?|monkeys?|pigs?|chickens?|ducks?|butterfl(?:y|ies)|pets?)\b/;
// Where a shot is: the place nouns a prompt names. A prompt that names none is read as the
// previous shot's place, the way a scene continues until the writer says otherwise.
const PLACE = /\b(?:halls?|rooms?|chambers?|courtyards?|yards?|gardens?|corridors?|hallways?|stair(?:s|cases?|wells?)|doorways?|gates?|gateways?|streets?|alleys?|lanes?|roads?|paths?|bridges?|rivers?|riverbanks?|shores?|beach(?:es)?|seas?|lakes?|ponds?|forests?|woods|groves?|mountains?|hills?|ridges?|cliffs?|caves?|valleys?|fields?|meadows?|wastelands?|deserts?|villages?|towns?|cit(?:y|ies)|markets?|stalls?|shops?|inns?|taverns?|teahouses?|kitchens?|bedrooms?|bedchambers?|offices?|librar(?:y|ies)|temples?|shrines?|palaces?|throne rooms?|pavilions?|towers?|rooftops?|roofs?|balcon(?:y|ies)|terraces?|carriages?|carts?|boats?|ships?|decks?|docks?|piers?|harbou?rs?|camps?|tents?|cells?|prisons?|dungeons?|forges?|stables?|barns?|warehouses?|factor(?:y|ies)|hospitals?|schools?|classrooms?|church(?:es)?|cemeter(?:y|ies)|graves?|tombs?|battlefields?|arenas?|stages?|plazas?|platforms?|altars?|academ(?:y|ies)|dojos?|training grounds?|courts?|mansions?|estates?|houses?|huts?|cabins?|cottages?|attics?|cellars?|basements?|tunnels?|cliffside|hillside|lakeside|riverside|seaside|whar(?:f|ves)|porch(?:es)?|gazebos?|galler(?:y|ies))\b/g;
// A clause whose subject is the camera, or that is a camera move written as if it were the
// behaviour ("slow push in on her face"): a move, not an event.
const CAMERA_CLAUSE = /^(?:the |a )?(?:camera|lens|frame|shot)\b|^(?:(?:very|slow(?:ly)?|gentle|gently|subtle|subtly|quick|quickly|fast|smooth|smoothly|steady) )*(?:push(?:es|ing)?[- ]?in|pull(?:s|ing)?[- ](?:back|out)|dolly(?:ing)?|zoom(?:s|ing)?|pan(?:s|ning)? (?:left|right|across|over|up|down|to|with|along)|whip pan|tilt(?:s|ing)? (?:up|down)|crane(?:s|ing)? (?:up|down)|orbit(?:s|ing)?|track(?:s|ing)? (?:left|right|in|out|with|along|back)|rack focus|focus (?:pulls?|racks?|shifts?)|handheld|steadicam)\b/;
const CLAUSES = /[,;.]| and | then | while | as /;
// Words that ask for a look instead of describing a shot.
const CLAIM = /\b(?:cinematic|epic|dramatic|masterpiece|award[- ]winning|breathtaking|stunning|blockbuster|hollywood|(?:movie|film)[- ]still|(?:movie|film)[- ]like|[48]k|ultra[- ]?(?:detailed|realistic|hd)|hyper[- ]?(?:detailed|realistic)|highly detailed|photo-?realistic|best quality|trending on artstation)\b/;

/** A shot whose data says something: a measured edit without its storyboard has nothing to read. */
const readable = (data) => Boolean(String(data?.prompt ?? "").trim() || String(data?.motion ?? "").trim());

/** The words of the cast a prompt may use: each id's parts and each ASCII name, lower-case. */
export function castWords(doc) {
  const words = new Set();
  for (const character of doc?.characters ?? []) {
    for (const part of String(character?.id ?? "").toLowerCase().split(/[^a-z0-9]+/)) if (part.length >= 2) words.add(part);
    const name = String(character?.name ?? "").trim().toLowerCase();
    if (/^[a-z][a-z0-9 '’.-]*$/.test(name)) words.add(name);
  }
  return words;
}

/** The place nouns a shot's prompt names, sorted and joined; "" when it names none. */
export function placeOf(data) {
  const found = new Set(String(data?.prompt ?? "").toLowerCase().match(PLACE) ?? []);
  return [...found].sort().join(" ");
}

/**
 * True when nobody is in the shot: no cast member listed, and neither the prompt nor the
 * motion line names a person, a creature or a member of the cast. An insert is also "nobody"
 * (a hand is not a person); the decorative row leaves inserts out itself.
 */
export function nobodyIn(data, cast = new Set()) {
  if ((data?.characters ?? []).length || !readable(data)) return false;
  const text = `${data?.prompt ?? ""} ${data?.motion ?? ""}`.toLowerCase();
  if (PERSON.test(text)) return false;
  return ![...cast].some((word) => new RegExp(`\\b${word.replace(/[.*+?^${}()|[\]\\]/g, "\\$&")}\\b`).test(text));
}

/**
 * How a motion line uses the camera: { camera, event }. `camera` is true when a clause makes
 * the camera the actor ("the camera pushes in", "slow pan across the table"); `event` is true
 * when what remains, with those clauses taken out, is more than a look (isLookOnly).
 */
export function cameraInMotion(data) {
  const clauses = String(data?.motion ?? "").toLowerCase().split(CLAUSES).map((clause) => clause.trim()).filter(Boolean);
  const rest = clauses.filter((clause) => !CAMERA_CLAUSE.test(clause));
  const camera = rest.length < clauses.length;
  return { camera, event: !isLookOnly({ motion: rest.join(", ") }) };
}

function lineSeconds(line) {
  return (spokenUnits(line.text) * 60) / CPM + (line.pause_after_ms ?? PAUSE_MS) / 1000;
}

/**
 * Either input as one list: [{ id, card, seconds, silent, data, lines: [{ speaker, text, at }] }].
 * A video.json is estimated as lint does, or read from `timeline` (lint's own estimate, or the
 * measured one) when one is given; a measured edit (`shots[]` with `editorial_duration_s`, as the
 * competition pilot writes them) is taken as it is. A shot with neither lines nor
 * `action_seconds` has no length of its own (`lint` refuses it); it is given
 * SILENT_SHOT_SECONDS and marked `silent`.
 */
export function normalize(doc, { timeline = null } = {}) {
  if (Array.isArray(doc?.shots) && doc.shots.some((shot) => Number.isFinite(shot?.editorial_duration_s))) {
    return {
      measured: true,
      cast: true,
      words: castWords(doc),
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
  const placed = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, (scene.end_frame - scene.start_frame) / FPS]));
  return {
    measured: false,
    cast: Array.isArray(doc.characters) && doc.characters.length > 0,
    words: castWords(doc),
    shots: doc.scenes.map((scene) => {
      const lines = (scene?.lines ?? []).map((line) => ({ speaker: line.speaker ?? NARRATOR, text: line.text, seconds: lineSeconds(line), inner: /^內心獨白/.test(line.emotion ?? "") }));
      const spoken = lines.reduce((sum, line) => sum + line.seconds, 0);
      // A shot without lines may be timed with `action_seconds` (a drama with a cast, a long anime).
      const action = !lines.length && Number.isFinite(scene?.action_seconds) ? scene.action_seconds : null;
      const silent = lines.length === 0 && action === null;
      const estimated = lines.length ? spoken + SCENE_GAP_MS / 1000 : (action ?? SILENT_SHOT_SECONDS);
      return {
        id: scene?.id,
        card: scene?.template !== "shot",
        seconds: !silent && placed.has(scene?.id) ? placed.get(scene.id) : estimated,
        silent,
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
 * rows: one per shot, { id, start, seconds, size, move, look_only, lines, place, nobody }:
 * `place` is the place the shot was read to be in (its own prompt's place nouns, else the
 * previous shot's), `nobody` that no person, creature or cast member is in it.
 * checks: { id, label, value, target, reference, ok, hint, shots } — `shots` names the shots
 * that cause a miss, `info: true` marks a row that is only reported.
 * `applies` is false for a document without a cast (an explainer, a brand story): their pace
 * and narration follow their own references, and no row is printed.
 */
export function craftChecks(doc, { timeline = null } = {}) {
  const { shots: all, measured, cast, words } = normalize(doc, { timeline });
  let clock = 0;
  const placed = all.map((shot) => {
    const start = clock;
    clock += shot.seconds;
    return { ...shot, start };
  });
  let place = "";
  const rows = placed.filter((shot) => !shot.card).map((shot) => {
    place = placeOf(shot.data) || place;
    return {
      id: shot.id,
      start: +shot.start.toFixed(2),
      seconds: +shot.seconds.toFixed(2),
      size: shotSize(shot.data),
      move: cameraMove(shot.data),
      look_only: isLookOnly(shot.data),
      lines: shot.lines.length,
      place,
      nobody: nobodyIn(shot.data, words),
      data: shot.data,
      silent: shot.silent,
      spoken: shot.lines,
      camera: cameraInMotion(shot.data),
    };
  });
  const total = rows.reduce((sum, row) => sum + row.seconds, 0);
  const publicRows = rows.map(({ data, spoken, silent, camera, ...row }) => row);
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
  if (!measured) add("lines.empty", "shots with neither a line nor action_seconds", String(rows.filter((row) => row.silent).length), "0", rows.every((row) => !row.silent), "`lint` refuses a scene without lines unless it is timed with action_seconds (1–8 s, a drama with a cast); otherwise put the off-screen speaker's line on the reaction shot", { shots: rows.filter((row) => row.silent) });
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
  const castOf = (row) => String([...(row.data.characters ?? [])].sort());
  // Shots with nobody in them (inserts) are "the same people" only when they are the same setup.
  const samePeople = (row, previous) => (castOf(row) || castOf(previous) ? castOf(row) === castOf(previous) : setupKey(row) === setupKey(previous));
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

  // Slideshow risk: the structure of sameness the first takes were sent back for ("it looks
  // like a slideshow"), read before a picture is paid for. The six things a plan can be scored
  // on before any asset exists (an idea borrowed from OpenMontage, not its code): the same
  // portrait drawn again, a place with nobody in it, a camera that moves while nobody acts, a
  // silent beat with nothing in it, words carrying the story, and "cinematic" written where a
  // size and a move should be.
  if (rows.length) {
    const framing = longestRun(rows, (row) => row.size !== null, (row, previous) => setupFamily(row.size) === setupFamily(previous.size) && samePeople(row, previous) && row.place === previous.place);
    add("risk.setup_repeat", "same framing of the same people in the same place in a row", `${framing.length} shots`, `≤ ${TARGETS.sameFramingRun}`, framing.length <= TARGETS.sameFramingRun, "three framings of one person from one side are one setup drawn three times: cut to who is listening, to what the hands do, or to the room", { reference: REFERENCE.framing, shots: framing });
    const decorative = rows.filter((row) => row.nobody && row.size !== "insert");
    add("risk.decorative", "shots with nobody in them that are not inserts", `${percent(share(decorative.length, rows.length))} (${decorative.length})`, `≤ ${percent(TARGETS.decorativeShare)}`, share(decorative.length, rows.length) <= TARGETS.decorativeShare, "a place with nobody in it is a postcard: put the person about to act in the frame, or make it an insert that answers a question", { reference: REFERENCE.decorative, shots: decorative });
    const aimless = rows.filter((row) => row.camera.camera && !row.camera.event);
    add("risk.motion_purpose", "motion lines where the camera moves and nobody does anything", String(aimless.length), String(TARGETS.cameraAsActor), aimless.length <= TARGETS.cameraAsActor, "the camera is not the one who acts: put the move in `camera` and write in `motion` what the person does", { shots: aimless });
    const empty = rows.filter((row) => row.lines === 0 && !row.silent && readable(row.data) && row.look_only && !["insert", "wide"].includes(family(row.size)) && !row.data.end_frame);
    add("risk.intent", "silent shots in which nothing happens and nothing is revealed", `${percent(share(empty.length, rows.length))} (${empty.length})`, `≤ ${percent(TARGETS.emptyBeatShare)}`, share(empty.length, rows.length) <= TARGETS.emptyBeatShare, "a silent shot has to do something: give it the off-screen line it reacts to, an action, or the thing it reveals (an insert, the room, an end frame); one designed hold in twenty is the ceiling", { shots: empty });
    const cards = placed.filter((shot) => shot.card);
    const cardShare = share(cards.reduce((sum, shot) => sum + shot.seconds, 0), clock);
    add("risk.text_first", "cards (title, chapter, quote …) against the shots", `${cards.length} of ${placed.length} scenes, ${percent(cardShare)} of the time`, `≤ ${TARGETS.cards} cards, or ≤ ${percent(TARGETS.cardShare)} of the time`, cards.length <= TARGETS.cards || cardShare <= TARGETS.cardShare, "a drama is told in pictures: say it in a shot, with a line over it", { reference: REFERENCE.cards, shots: cards });
    const claims = rows.filter((row) => CLAIM.test(String(row.data.prompt ?? "").toLowerCase()) && row.size === null && row.move === "none");
    add("risk.cinematic_claim", "prompts that claim a look (cinematic, epic, 8k …) on a shot with no size and no move", String(claims.length), String(TARGETS.claims), claims.length <= TARGETS.claims, "\"cinematic\" is not a shot: start `camera` with the size and the move, and let the look preset carry the style", { shots: claims });
  }

  return { applies: true, measured, shots: rows.length, total_seconds: total, rows: publicRows, checks };
}

/** The rows a report missed, as one line each: the id, the reading, the target, the hint and the shots at fault. */
export function craftMisses(report) {
  return report.checks.filter((check) => !check.info && !check.ok).map((check) => ({
    id: check.id,
    message: `craft ${check.id}: ${check.label} ${check.value}, target ${check.target}; ${check.hint}${check.shots.length ? ` (${check.shots.slice(0, 8).join(", ")}${check.shots.length > 8 ? `, … ${check.shots.length}` : ""})` : ""}`,
  }));
}

/**
 * What `lint` prints for a drama with a cast: the missed rows as { path, message }, on the
 * timeline lint estimated. Nothing for a document the rows do not apply to.
 */
export function craftProblems(doc, timeline = null) {
  const report = craftChecks(doc, { timeline });
  if (!report.applies) return [];
  return craftMisses(report).map(({ message }) => ({ path: "scenes", message: `${message} (.agents/skills/youtube-video/references/drama-craft.md)` }));
}

/** The missed rows that send a hands-off episode back to its writer (CRAFT_GATE_ROWS), as sentences. */
export function craftGateProblems(report) {
  if (!report?.applies) return [];
  return craftMisses(report).filter(({ id }) => CRAFT_GATE_ROWS.includes(id)).map(({ message }) => message);
}

/** The whole table as the skill's command prints it. */
export function renderCraftReport(report, file) {
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
