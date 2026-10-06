/**
 * The drama craft check the youtube-video skill ships
 * (.agents/skills/youtube-video/scripts/drama_craft_check.mjs).
 *
 * The script is what turns "it felt flat" into rows a writer has to answer, so what is pinned
 * here is the reading of a storyboard: which size a shot names, when a shot is only a look, and
 * that each row misses on the storyboard it exists to catch while a covered scene meets them
 * all. The camera and motion lines in the tables are real ones: from the wedding pilot's edits,
 * from the first review of this script (which misread them), and the size words the craft spec
 * tells writers to use. The targets themselves are editorial
 * (.agents/skills/youtube-video/references/drama-craft.md); the tests read the exported TARGETS
 * rather than repeating the numbers.
 */
import assert from "node:assert/strict";
import test from "node:test";
import { spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import {
  CPM,
  PAUSE_MS,
  SCENE_GAP_MS,
  SILENT_SHOT_SECONDS,
  TARGETS,
  cameraInMotion,
  cameraMove,
  castWords,
  craftChecks,
  isLookOnly,
  nobodyIn,
  normalize,
  placeOf,
  quantile,
  shotSize,
  sizesDisagree,
  spokenUnits,
} from "../.agents/skills/youtube-video/scripts/drama_craft_check.mjs";

const SCRIPT = fileURLToPath(new URL("../.agents/skills/youtube-video/scripts/drama_craft_check.mjs", import.meta.url));

const shot = (id, camera, motion, lines, extra = {}) => ({
  id,
  template: "shot",
  data: { prompt: "A banquet hall.", camera, motion, characters: ["lin"], ...extra },
  lines: lines.map(([speaker, text], index) => ({ id: `${id}-${index}`, speaker, text })),
});
const drama = (scenes, characters = [{ id: "lin" }, { id: "zhao" }]) => ({ format: "drama", characters, scenes });
const byId = (report) => Object.fromEntries(report.checks.map((check) => [check.id, check]));
const missed = (report) => report.checks.filter((check) => !check.ok).map((check) => check.id);

// A scene covered the way the references cut one: place, action, face, reaction, proof; short
// turns, one line held longer, and a return to the room.
const PATTERN = [
  ["Wide establishing shot of the hall", "Guests turn toward the stage.", [["lin", "開始吧。"]], { characters: ["lin", "zhao"] }],
  ["Medium shot, slow push in", "Lin offers the cup with both hands.", [["lin", "媽，請喝茶。"]], {}],
  ["Close-up", "Zhao turns her face away.", [["zhao", "這杯茶我不喝。"]], { characters: ["zhao"] }],
  ["Medium close-up", "Lin lowers the cup.", [["lin", "為什麼不喝？"]], {}],
  ["Insert of the cup", "Tea spills over the rim onto her fingers.", [["zhao", "因為妳不配進這個門。"]], { characters: [] }],
  ["Close-up", "Lin's father rises from his chair.", [["lin", "爸，你先別動。"]], { characters: ["father"] }],
  ["Over-the-shoulder on Zhao", "Zhao leans in and points at the door.", [["zhao", "現在就出去，別讓我說第二次。"], ["zhao", "聽見沒有？"]], { characters: ["lin", "zhao"] }],
  ["Medium close-up", "Lin sets the cup down and stands.", [["lin", "好，我知道了。"]], {}],
];
const covered = () =>
  drama([0, 1, 2, 3].flatMap((round) => PATTERN.map(([camera, motion, lines, extra], index) => shot(`s${round}${index}`, camera, motion, lines, extra))), [
    { id: "lin" },
    { id: "zhao" },
    { id: "father" },
  ]);

// The rejected look: narrated, locked, a person standing while a finger moves.
const portraits = () =>
  drama(
    Array.from({ length: 8 }, (_, index) =>
      shot(`p${index}`, "Locked medium close-up", "Her fingers tighten once around the pen.", [["narrator", "上一世她在這裡簽了字，從此再也沒能走出這扇門。"]]),
    ),
    [{ id: "lin" }],
  );

test("spoken length counts a CJK character as one and a Latin word or number as two", () => {
  assert.equal(spokenUnits("請喝茶。"), 3);
  assert.equal(spokenUnits("第 17 次用 API"), 1 + 2 + 1 + 1 + 2);
});

test("a shot's length is estimated the way lint estimates it", () => {
  const { shots } = normalize(drama([shot("a", "Wide", "She waves.", [["lin", "請喝茶請喝茶請喝"]])]));
  assert.equal(shots[0].seconds, (8 * 60) / CPM + PAUSE_MS / 1000 + SCENE_GAP_MS / 1000);
  assert.ok(Math.abs(shots[0].seconds - 2.92) < 1e-9, "eight characters are about 2.9 s");
  assert.deepEqual([CPM, PAUSE_MS, SCENE_GAP_MS], [250, 300, 700], "the constants of tools/video/core/timeline.mjs");
});

test("the quantile is the one lint and the probe use", () => {
  assert.equal(quantile([1, 2, 3, 4], 0.5), 3);
  assert.equal(quantile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.9), 10);
  assert.equal(quantile([1, 2, 3, 4, 5, 6, 7, 8, 9, 10], 0.1), 2);
});

test("a shot's size is read from its camera line as a person would read it", () => {
  const lines = [
    // the wedding pilot's own camera lines
    ["Locked medium close-up; full face, suit and pen-holding hand remain visible.", "mcu"],
    ["Locked view through the door gap.", null],
    ["Locked close-up of the pen hand.", "insert"],
    ["Locked insert of the hand and original.", "insert"],
    ["Locked oblique overhead hand shot.", "insert"],
    ["Locked hand close-up.", "insert"],
    ["Locked oblique overhead close-up.", "insert"],
    ["Locked prop close-up.", "insert"],
    ["Locked hand-and-copy close-up.", "insert"],
    ["Locked view of the hands and table.", "insert"],
    ["Locked over-the-shoulder reaction shot.", "ots"],
    ["Locked medium close-up including hand and phone.", "mcu"],
    ["Locked medium shot.", "ms"],
    ["Locked over-table medium close-up.", "mcu"],
    ["Locked close-up with the copy edge soft in foreground.", "cu"],
    ["Locked wide enough to separate original and retained copy.", "ws"],
    ["Locked table-height two-position framing; only bride identifiable.", null],
    // the words the craft spec tells writers to start with
    ["Wide establishing shot of the hall", "ws"],
    ["Medium shot, pan left", "ms"],
    ["Medium close-up", "mcu"],
    ["Close-up, handheld", "cu"],
    ["Extreme close-up of her eyes", "ecu"],
    ["Over-the-shoulder close-up on Zhao", "ots"],
    ["Two-shot, locked", "group"],
    ["Insert: the seal on the paper", "insert"],
    ["POV: wide view of the hall from the stage", "pov"],
    // phrasings the first version misread
    ["Wide two-shot of the bride and groom across the table", "ws"],
    ["Wide; the couple in the medium distance", "ws"],
    ["Medium close up of her face", "mcu"],
    ["Close up on her eyes", "cu"],
    ["Close-up of Zhitang's hand", "insert"],
    ["Close-up on the receipt", "insert"],
    ["Close-up of his face", "cu"],
    ["Slow push in on her wide eyes", null],
    ["High angle on her hands", null],
  ];
  for (const [camera, size] of lines) assert.equal(shotSize({ camera }), size, camera);
});

test("a prompt names a size only with an explicit shot phrase, and the camera line wins", () => {
  assert.equal(shotSize({ camera: "Slow push in", prompt: "Wide shot of the banquet hall" }), "ws");
  assert.equal(shotSize({ camera: "Slow push in", prompt: "A wide-eyed girl in wide sleeves under an overhead lantern, medium ink wash" }), null);
  assert.equal(shotSize({ camera: "Close-up", prompt: "Wide shot of the hall behind her" }), "cu");
  assert.equal(sizesDisagree({ camera: "Medium close-up", prompt: "Medium shot of Lin at the stall" }), true);
  assert.equal(sizesDisagree({ camera: "Medium close-up", prompt: "Lin at the stall" }), false);
});

test("a camera move is read from camera phrasing, not from what a person in the line does", () => {
  const lines = [
    ["Locked medium close-up", "locked"],
    ["Static", "locked"],
    ["Medium shot, slow push in", "push"],
    ["Slow zoom", "push"],
    ["Closer on her face", "push"],
    ["Dolly out", "pull"],
    ["Zoom out to the hall", "pull"],
    ["Pan left to the door", "pan"],
    ["Crane up over the courtyard", "tilt"],
    ["Handheld follow", "track"],
    ["Truck right along the table", "track"],
    ["Slow orbit around the table", "track"],
    ["Medium close-up; her eyes fixed on the door, slow push in", "push"],
    ["Medium shot as she pushes the box back across the table", "none"],
    ["Medium shot; he pulls the chair out", "none"],
    ["Wide shot, the hall seen through the archway", "none"],
    ["Medium close-up", "none"],
  ];
  for (const [camera, move] of lines) assert.equal(cameraMove({ camera }), move, camera);
});

test("a look, a breath or a tremor is a look; anything done to someone or something is not", () => {
  const lines = [
    // the wedding pilot's own motion lines
    ["Her fingers tighten once around the pen.", true],
    ["The trace of a smile leaves his face.", true],
    ["Her pen-holding hand trembles briefly and steadies without touching the paper.", true],
    ["His gaze shifts from the ring box to the unsigned original.", true],
    ["She turns her gaze directly back to Chengchuan.", true],
    ["Zhitang lifts her gaze from the gift bag toward Zhixia.", true],
    ["His remaining polite expression vanishes.", true],
    ["He reads the indicated voting-rights item aloud with restrained mouth movement.", true],
    ["She holds his gaze while answering with restrained facial movement.", true],
    ["She closes her fingers once around the receipt without crumpling it.", true],
    ["She raises her eyes toward her uncle, still holding her copy and receipt.", true],
    ["Her left index finger traces one existing page number on the original.", false],
    ["She sets the pen down beside the original.", false],
    ["She tears the thin display copy once with both hands.", false],
    ["The witness squares the copy attachment pages into the copy stack.", false],
    ["She approaches Zhitang from the left rear.", false],
    ["He leans slightly toward Zhitang.", false],
    ["He gives one small confirming nod.", false],
    ["She turns her head toward her maternal uncle.", false],
    // lines the first version misread
    ["She sets the cup down.", false],
    ["She stands still, breathing.", true],
    ["Her eyes close.", true],
    ["A tear falls down her cheek.", true],
    ["She slaps him across the mouth.", false],
    ["He wipes the tears from her eyes.", false],
    ["She closes the door.", false],
    ["", true],
  ];
  for (const [motion, look] of lines) assert.equal(isLookOnly({ camera: "Locked medium close-up", motion }), look, motion);
  assert.equal(isLookOnly({ camera: "Slow push in", motion: "She looks at the door." }), true, "a camera move does not turn a look into an action");
});

test("the slideshow rows read who is in the shot, where it is, and whether the camera is the one acting", () => {
  const cast = castWords({ characters: [{ id: "nie-gutie", name: "聶孤鐵" }, { id: "lin", name: "Lin Zhitang" }] });
  assert.deepEqual([...cast], ["nie", "gutie", "lin", "lin zhitang"]);
  assert.equal(placeOf({ prompt: "From the south side of a stone forge on a night wasteland: the forge mouth glowing" }), "forge wasteland");
  assert.equal(placeOf({ prompt: "Nie at the forge mouth, turned toward it" }), "forge");
  assert.equal(placeOf({ prompt: "Her hands folded on the cup" }), "");
  const nobody = [
    [{ prompt: "Lanterns over the empty courtyard at dusk", motion: "Mist drifts across the stones.", characters: [] }, true],
    [{ prompt: "A scroll on the table", motion: "The wind lifts a page" }, true],
    [{ prompt: "Nie at the forge mouth", characters: [] }, false],
    [{ prompt: "close-up of a small bird on a wet rock", characters: [] }, false],
    [{ prompt: "The banquet hall", characters: ["lin"] }, false],
    [{ prompt: "The hall at night", motion: "She closes the door." }, false],
    [{ camera: "Close-up" }, false],
  ];
  for (const [data, expected] of nobody) assert.equal(nobodyIn(data, cast), expected, JSON.stringify(data));
  const camera = [
    ["The camera pushes in slowly on her face.", true, false],
    ["Slow push in on her face, her eyes narrow", true, false],
    ["Pan across the table to the empty chair", true, false],
    ["She sets the cup down, the camera tilts up", true, true],
    ["Nie walks three slow steps toward the camera", false, true],
    ["A gust snaps all three banners out flat and the crane feather on his crown lifts", false, true],
    ["Her fingers tighten once around the pen.", false, false],
  ];
  for (const [motion, moves, event] of camera) assert.deepEqual(cameraInMotion({ motion }), { camera: moves, event }, motion);
});

test("a covered scene meets every check", () => {
  assert.deepEqual(missed(craftChecks(covered())), []);
});

test("narrated portraits miss on the opening, the lines, the coverage and the motion", () => {
  const report = craftChecks(portraits());
  const checks = byId(report);
  for (const id of ["pace.median", "pace.spread", "hook.opening", "hook.dialogue", "lines.median", "lines.long", "lines.narrator", "size.wide", "size.stall", "motion.look", "motion.run", "motion.opening", "risk.setup_repeat"]) {
    assert.equal(checks[id]?.ok, false, `${id} should miss`);
  }
  assert.equal(checks["hook.card"].ok, true);
  assert.deepEqual(checks["motion.opening"].shots, ["p0", "p1", "p2"], "a miss names its shots");
  assert.equal(report.rows[0].size, "mcu");
  assert.equal(report.rows[0].look_only, true);
});

// One change to the covered scene, one row it must turn.
const cases = [
  ["pace.median", "shots faster than the references' own median", (doc) => doc.scenes.forEach((scene) => { scene.lines = [{ id: `${scene.id}-x`, speaker: "lin", text: "好" }]; })],
  ["pace.p90", "a fifth of the shots held long", (doc) => doc.scenes.forEach((scene, index) => { if (index % 5 === 0) scene.lines = [{ id: `${scene.id}-x`, speaker: "lin", text: "一二三四五六七八九十一二三四五六七八九十二" }]; })],
  ["pace.longest", "one shot longer than a clip", (doc) => { doc.scenes[9].lines = ["a", "b", "c"].map((id) => ({ id: `long-${id}`, speaker: "lin", text: "一二三四五六七八九十" })); }],
  ["pace.spread", "every shot the same length", (doc) => doc.scenes.forEach((scene) => { scene.lines = [{ id: `${scene.id}-x`, speaker: scene.lines[0].speaker, text: "請妳喝茶吧好" }]; })],
  ["hook.opening", "a slow first ten seconds", (doc) => { doc.scenes[0].lines = [{ id: "slow", speaker: "lin", text: "一二三四五六七八九十一二三四五六七八九十" }]; doc.scenes[1].lines = [{ id: "slow2", speaker: "lin", text: "一二三四五六七八九十一二三四五" }]; }],
  ["hook.opening30", "a thin first half minute", (doc) => doc.scenes.slice(0, 6).forEach((scene) => { scene.lines = [{ id: `${scene.id}-x`, speaker: "lin", text: "一二三四五六七八九十一二三四五六七八" }]; })],
  ["hook.card", "a title card first", (doc) => doc.scenes.unshift({ id: "title", template: "title", data: {}, lines: [{ id: "t", text: "第一集" }] })],
  ["hook.dialogue", "narration until the thirteenth second", (doc) => doc.scenes.slice(0, 6).forEach((scene) => scene.lines.forEach((line) => { line.speaker = "narrator"; }))],
  ["lines.empty", "a shot without a line", (doc) => { doc.scenes[5].lines = []; }],
  ["lines.median", "long turns", (doc) => doc.scenes.forEach((scene) => { scene.lines = [{ id: `${scene.id}-x`, speaker: "lin", text: "這杯茶我敬了六次妳一次都沒接" }]; })],
  ["lines.long", "many lines over twenty characters", (doc) => doc.scenes.forEach((scene, index) => { if (index % 4 === 0) scene.lines = [{ id: `${scene.id}-x`, speaker: "lin", text: "一二三四五六七八九十一二三四五六七八九十一" }]; })],
  ["lines.narrator", "a narrator who carries it", (doc) => doc.scenes.forEach((scene, index) => { if (index % 2 === 0) scene.lines.forEach((line) => { line.speaker = "narrator"; }); })],
  ["size.named", "camera lines without a size", (doc) => doc.scenes.forEach((scene, index) => { if (index % 3 === 0) scene.data.camera = "Slow push in"; })],
  ["size.agree", "a prompt that names another size", (doc) => { doc.scenes[3].data.prompt = "Medium shot of Lin at the table"; }],
  ["size.face", "too few faces", (doc) => doc.scenes.forEach((scene) => { if (/close-up|shoulder/i.test(scene.data.camera)) scene.data.camera = "Medium shot"; })],
  ["size.insert", "half the shots are inserts", (doc) => doc.scenes.forEach((scene, index) => { if (index % 2 === 1) scene.data.camera = "Insert of the cup"; })],
  ["size.wide", "no room is ever shown", (doc) => doc.scenes.forEach((scene) => { if (/^wide/i.test(scene.data.camera)) scene.data.camera = "Medium shot"; })],
  ["size.reestablish", "ten shots without the room", (doc) => { doc.scenes[8].data.camera = "Medium shot"; doc.scenes[16].data.camera = "Medium shot"; }],
  ["size.stall", "the same face three times", (doc) => { for (const index of [2, 3, 4]) Object.assign(doc.scenes[index].data, { camera: "Close-up", characters: ["zhao"] }); }],
  ["motion.look", "looks instead of actions", (doc) => doc.scenes.forEach((scene, index) => { if (index % 2 === 0) scene.data.motion = "She looks at him."; })],
  ["motion.run", "three looks in a row", (doc) => { for (const index of [10, 11, 12]) doc.scenes[index].data.motion = "Her eyes narrow."; }],
  ["motion.opening", "an opening of three looks, each with a camera move", (doc) => { for (const index of [0, 1, 2]) Object.assign(doc.scenes[index].data, { motion: "She stares ahead.", camera: `${doc.scenes[index].data.camera}, slow push in` }); }],
  ["motion.repeat", "the same push four times", (doc) => { for (const index of [8, 9, 10, 11]) doc.scenes[index].data.camera = `${doc.scenes[index].data.camera}, slow push in`; }],
  ["cut.dissolve", "dissolves as a habit", (doc) => doc.scenes.forEach((scene, index) => { if (index % 5 === 0) scene.data.transition = "dissolve"; })],
  // The slideshow rows: the same face from three distances passes size.stall (three sizes) and is still one setup drawn three times.
  ["risk.setup_repeat", "the same face three times from three distances", (doc) => { for (const [index, camera] of [[2, "Close-up"], [3, "Medium close-up"], [4, "Extreme close-up"]]) Object.assign(doc.scenes[index].data, { camera, characters: ["zhao"] }); }],
  ["risk.decorative", "postcards of the place between the people", (doc) => doc.scenes.forEach((scene, index) => { if (index % 8 === 1) Object.assign(scene.data, { prompt: "Lanterns over the empty courtyard at dusk, mist on the stones", motion: "Mist drifts across the stones.", characters: [] }); })],
  ["risk.motion_purpose", "the camera moving while nobody does anything", (doc) => { doc.scenes[6].data.motion = "The camera pushes in slowly on her face, her eyes narrow."; }],
  ["risk.intent", "silent looks timed as beats", (doc) => { for (const index of [5, 13]) Object.assign(doc.scenes[index], { lines: [], action_seconds: 3, data: { ...doc.scenes[index].data, motion: "She looks down." } }); }],
  ["risk.text_first", "cards carrying the story", (doc) => { doc.scenes = doc.scenes.flatMap((scene, index) => (index % 8 === 7 ? [scene, { id: `card${index}`, template: "chapter", data: { title: "三年後" }, lines: [{ id: `card${index}-l`, text: "三年後，她回到了這座大廳，手裡握著當年那份沒有簽的契約。" }] }] : [scene])); }],
  ["risk.cinematic_claim", "a cinematic wish instead of a shot", (doc) => { Object.assign(doc.scenes[3].data, { camera: "", prompt: "Cinematic, epic lighting on Lin at the table" }); }],
];
for (const [id, what, change] of cases) {
  test(`${id} misses on ${what}`, () => {
    const doc = covered();
    change(doc);
    assert.equal(byId(craftChecks(doc))[id]?.ok, false);
  });
}

test("every judged row has a case above, so a deleted row is noticed", () => {
  const judged = craftChecks(covered()).checks.filter((check) => !check.info).map((check) => check.id).sort();
  assert.deepEqual(judged, cases.map(([id]) => id).sort());
});

test("ten shots without a wide is one too many, nine is allowed", () => {
  const run = (count) => drama([shot("w", "Wide", "They sit.", [["lin", "坐。"]]), ...Array.from({ length: count }, (_, index) => shot(`m${index}`, index % 2 ? "Medium close-up" : "Close-up", "She pours the tea.", [["lin", "喝。"]], { characters: [index % 2 ? "lin" : "zhao"] }))]);
  assert.equal(byId(craftChecks(run(TARGETS.wideGapShots)))["size.reestablish"].ok, true);
  assert.equal(byId(craftChecks(run(TARGETS.wideGapShots + 1)))["size.reestablish"].ok, false);
});

test("a shot without lines cannot make an opening look denser", () => {
  const doc = drama([...Array.from({ length: 6 }, (_, index) => shot(`e${index}`, "Close-up", "She pours.", [])), shot("long", "Wide", "She waits.", [["lin", "一二三四五六七八九十一二三四五六七八九十"]])]);
  const report = craftChecks(doc);
  assert.equal(report.rows[1].start, SILENT_SHOT_SECONDS);
  assert.equal(byId(report)["hook.opening"].value, "5");
  assert.equal(byId(report)["lines.empty"].value, "6");
});

test("a measured edit is read with its real lengths and line times, and may hold silent shots", () => {
  const measured = {
    shots: [
      { shot_id: "A", editorial_duration_s: 2, data: { camera: "Wide" }, voice_placements: [{ speaker_id: "lin", text: "開始。", start_s: 0.2 }] },
      { shot_id: "B", editorial_duration_s: 3, data: { camera: "Close-up" }, voice_placements: [] },
      { shot_id: "C", editorial_duration_s: 9, data: { camera: "Insert" }, voice_placements: [{ speaker_id: "narrator", text: "她沒有簽。", start_s: 5.5 }] },
    ],
  };
  const report = craftChecks(measured);
  assert.equal(report.measured, true);
  assert.deepEqual(report.rows.map((row) => row.seconds), [2, 3, 9]);
  const checks = byId(report);
  assert.equal(checks["risk.decorative"].value, "0% (0)", "a measured edit without its storyboard is not read as empty");
  assert.equal(checks["risk.intent"].value, "0% (0)", "nor its silent shots as beats with nothing in them");
  assert.equal(checks["pace.longest"].ok, false);
  assert.deepEqual(checks["pace.longest"].shots, ["C"]);
  assert.equal(checks["hook.dialogue"].value, "0.2 s");
  assert.equal(checks["lines.empty"], undefined, "silence is allowed in a measured edit");
});

test("a document without a cast is not judged, and one that is not a drama is refused", () => {
  const explainer = drama([shot("a", "Wide", "", [["narrator", "為什麼飛機窗戶是圓的？"]])], []);
  const report = craftChecks(explainer);
  assert.equal(report.applies, false);
  assert.deepEqual(report.checks, []);
  assert.throws(() => craftChecks({ format: "slides", scenes: [] }), /not a drama/);
  assert.throws(() => craftChecks({ slides: [] }), /neither a video\.json/);
});

test("the repository's drama fixture can be read", () => {
  const fixture = JSON.parse(readFileSync(new URL("./video/core/fixtures/drama/video.json", import.meta.url), "utf8"));
  const report = craftChecks(fixture);
  assert.ok(report.applies && report.shots > 0 && report.checks.length > 0);
  assert.deepEqual(report.checks.filter((check) => check.id.startsWith("risk.") && !check.ok).map((check) => check.id), [], "the fixture is not a slideshow");
  assert.deepEqual(report.rows.map((row) => [row.place, row.nobody]), [["forest mountain ridge", false], ["gate palace", false], ["boat sea", false], ["sea", false]], "each shot's place is its prompt's place nouns; the bird is somebody");
  assert.deepEqual(craftChecks({ ...fixture, scenes: fixture.scenes.map((scene, index) => (index === 3 ? { ...scene, data: { ...scene.data, prompt: "close-up of a small bird, a pebble in its beak" } } : scene)) }).rows[3].place, "boat sea", "a shot that names no place is read as the previous shot's");
});

test("the command exits 0, 1 with --strict on a miss, and 2 on a file it cannot read", () => {
  const dir = mkdtempSync(join(tmpdir(), "craft-"));
  try {
    const good = join(dir, "good.json"), bad = join(dir, "bad.json");
    writeFileSync(good, JSON.stringify(covered()));
    writeFileSync(bad, JSON.stringify(portraits()));
    const run = (...args) => spawnSync(process.execPath, [SCRIPT, ...args], { encoding: "utf8" });
    assert.equal(run(good, "--strict").status, 0);
    assert.equal(run(bad).status, 0);
    const strict = run(bad, "--strict");
    assert.equal(strict.status, 1);
    assert.match(strict.stdout, /MISS/);
    assert.match(strict.stdout, /shots: p0, p1, p2/);
    assert.equal(JSON.parse(run(bad, "--json").stdout).rows.length, 8);
    assert.equal(run(join(dir, "missing.json")).status, 2);
    assert.equal(run().status, 2);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});

test("lint and the worker read the same rows through tools/video/core/craft.mjs, on lint's own timeline", async () => {
  const { CRAFT_GATE_ROWS, craftChecks: checks, craftGateProblems, craftProblems } = await import("../tools/video/core/craft.mjs");
  const { estimateTimeline } = await import("../tools/video/core/timeline.mjs");
  const doc = covered();
  const timeline = estimateTimeline({ ...doc, scenes: doc.scenes.map((scene) => ({ ...scene, chapter: scene.id === "s00" ? "一" : undefined })) });
  const onTimeline = checks(doc, { timeline });
  const placed = timeline.scenes.find((scene) => scene.id === "s11");
  assert.equal(onTimeline.rows.find((row) => row.id === "s11").seconds, +((placed.end_frame - placed.start_frame) / 30).toFixed(2), "with a timeline the lengths are its frames");
  assert.ok(Math.abs(onTimeline.rows[3].seconds - checks(doc).rows[3].seconds) < 0.1, "and the estimate agrees with it to a frame or two");
  assert.deepEqual(craftProblems(doc, timeline), [], "a covered scene prints nothing");
  const problems = craftProblems(portraits());
  assert.ok(problems.length && problems.every((problem) => problem.path === "scenes" && /^craft [a-z]+\.[a-z0-9_]+: .*drama-craft\.md\)$/.test(problem.message)), JSON.stringify(problems));
  const gate = craftGateProblems(checks(portraits()));
  assert.ok(gate.some((problem) => /^craft hook\.opening: /.test(problem)));
  assert.ok(gate.some((problem) => /^craft risk\.setup_repeat: /.test(problem)), "eight portraits of one face are sent back");
  assert.ok(["risk.setup_repeat", "risk.decorative", "risk.text_first"].every((id) => CRAFT_GATE_ROWS.includes(id)) && !["risk.intent", "risk.motion_purpose", "risk.cinematic_claim"].some((id) => CRAFT_GATE_ROWS.includes(id)), "the three structural slideshow rows gate; the three that read one line's words warn");
  assert.ok(gate.every((problem) => CRAFT_GATE_ROWS.some((id) => problem.startsWith(`craft ${id}: `))), "only the opening and coverage rows send a script back");
  assert.ok(!gate.some((problem) => /lines\.narrator/.test(problem)), "the narration share is a warning, not a gate");
  assert.deepEqual(craftGateProblems(null), []);
  assert.deepEqual(craftProblems({ format: "drama", characters: [], scenes: portraits().scenes }), [], "no cast, no rows");
});
