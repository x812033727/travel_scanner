/**
 * The shot reading the animation-camera skill ships
 * (.agents/skills/animation-camera/scripts/shot_reading.mjs).
 *
 * The skill's claim is that one camera line is read three ways in the tools — the craft rows
 * (tools/video/core/craft.mjs shotSize / cameraMove / isLookOnly), the illustrated slides'
 * variety rule (tools/video/core/drama.mjs cameraMove) and the still-shot animation
 * (tools/video/assemble/drama.mjs motionMove, whose push-in, drift and locked start on the whole
 * keyframe and are PSNR-checked at frame 0) — and that the reference's example table says what
 * each reads. So the example rows of references/camera-keywords.md are parsed here and asserted
 * through the imported readers themselves, a second table of rows is pinned directly (the
 * contract's facts: "pan left" is pan-right, a written drift wins over static, a person's verb is
 * not a move), every trap has a shot that trips it and a clean shot trips none, and the command's
 * exit codes are what the skill says.
 */
import assert from "node:assert/strict";
import test from "node:test";
import { spawnSync } from "node:child_process";
import { existsSync, mkdtempSync, readFileSync, rmSync, writeFileSync } from "node:fs";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

import { cameraMove as craftMove, isLookOnly, shotSize, sizesDisagree } from "./video/core/craft.mjs";
import { cameraMove as slidesMove } from "./video/core/drama.mjs";
import { motionMove } from "./video/assemble/drama.mjs";
import { DRAMA_FIXTURE_FILE, dramaFixture, sandbox } from "./video/core/fixtures/load.mjs";
import {
  MAX_PROMPT_CHARS,
  PRODUCTION_CLIP_SECONDS,
  TRAP_IDS,
  boughtSeconds,
  keyframePrompt,
  lookMotionMove,
  offScreenRoles,
  personClause,
  readDocument,
  renderReading,
  shotFileDocument,
} from "../.agents/skills/animation-camera/scripts/shot_reading.mjs";

const SCRIPT = fileURLToPath(new URL("../.agents/skills/animation-camera/scripts/shot_reading.mjs", import.meta.url));
const KEYWORDS = fileURLToPath(new URL("../.agents/skills/animation-camera/references/camera-keywords.md", import.meta.url));
const MINIMAL_FIXTURE = fileURLToPath(new URL("./video/core/fixtures/minimal/video.json", import.meta.url));

// The reading of one camera line, in the order the reference table lists it.
const reading = (camera) => {
  const move = motionMove({ camera }, "row");
  return { size: shotSize({ camera }), craft: craftMove({ camera }), slides: slidesMove({ camera }), assemble: move.name, psnr: move.startsAtIdentity };
};

// What a cell of the reference table means: `-` is none, yes/no (or 是/否) is the PSNR flag.
const cell = (text) => {
  const code = /`([^`]*)`/.exec(text);
  return (code ? code[1] : text).trim();
};
const none = (value, asNone) => (value === "-" || value === "" ? asNone : value);
const flag = (value) => /^(?:yes|true|✓|是|checked|y)$/i.test(value) ? true : /^(?:no|false|✗|否|-|n)$/i.test(value) ? false : null;

/** The rows of the fenced table under "## 例子": [{ camera, size, craft, slides, assemble, psnr }]. */
function exampleRows(markdown) {
  const lines = markdown.split(/\r?\n/);
  const start = lines.findIndex((line) => /^##\s*例子/.test(line));
  assert.ok(start >= 0, 'references/camera-keywords.md has no "## 例子" heading');
  let end = lines.findIndex((line, index) => index > start && /^##\s/.test(line));
  if (end < 0) end = lines.length;
  const table = lines.slice(start, end).filter((line) => /^\s*\|/.test(line));
  assert.ok(table.length >= 3, 'the "## 例子" section holds no markdown table with a header, a separator and at least one row');
  const cells = (line) => line.trim().replace(/^\|/, "").replace(/\|$/, "").split("|").map((part) => part.trim());
  const header = cells(table[0]).map((part) => part.toLowerCase());
  const column = (fallback, ...needles) => {
    const found = header.findIndex((part) => needles.every((needle) => part.includes(needle)));
    return found >= 0 ? found : fallback;
  };
  const at = {
    camera: column(0, "camera"),
    size: column(1, "size"),
    craft: column(2, "craft", "move"),
    slides: column(3, "slides"),
    assemble: column(4, "assemble"),
    psnr: column(5, "psnr"),
  };
  return table.slice(1).filter((line) => !/^\s*\|?\s*:?-{2,}/.test(line)).map(cells).filter((parts) => parts.length >= 6).map((parts) => ({
    camera: cell(parts[at.camera]),
    size: none(cell(parts[at.size]), null),
    craft: none(cell(parts[at.craft]), "none"),
    slides: none(cell(parts[at.slides]), "drift"),
    assemble: none(cell(parts[at.assemble]), "drift"),
    psnr: flag(cell(parts[at.psnr])),
  }));
}

test("the reference's example rows read through the tools exactly as the table says", () => {
  assert.ok(existsSync(KEYWORDS), "references/camera-keywords.md is missing: the animation-camera reference has not been written (or was renamed); this test parses its \"## 例子\" table");
  const rows = exampleRows(readFileSync(KEYWORDS, "utf8"));
  assert.ok(rows.length >= 8, `only ${rows.length} example rows; the table should cover the sizes, every move and the traps`);
  for (const row of rows) {
    const read = reading(row.camera);
    assert.equal(read.size, row.size, `${row.camera}: craft size`);
    assert.equal(read.craft, row.craft, `${row.camera}: craft move`);
    assert.equal(read.slides, row.slides, `${row.camera}: slides move`);
    assert.equal(read.assemble, row.assemble, `${row.camera}: assemble move`);
    assert.notEqual(row.psnr, null, `${row.camera}: the PSNR column must say yes or no`);
    assert.equal(read.psnr, row.psnr, `${row.camera}: frame-0 PSNR check`);
  }
});

// The contract's facts, pinned here whatever the reference says: camera line, craft size, craft
// move, slides move, assemble move, PSNR-checked at frame 0.
const OWN_ROWS = [
  ["Wide establishing shot of the hall, locked", "ws", "locked", "locked", "locked", true],
  ["Medium close-up, static", "mcu", "locked", "locked", "locked", true],
  ["Close-up, fixed camera", "cu", "locked", "locked", "locked", true],
  ["Insert of the seal, tripod", "insert", "locked", "locked", "locked", true],
  ["Medium shot, slow push in", "ms", "push", "push in", "push-in", true],
  ["Two-shot, dolly in", "group", "push", "push in", "push-in", true],
  ["Over-the-shoulder on Zhao, pull back", "ots", "pull", "pull out", "pull-out", false],
  ["Wide, zoom out", "ws", "pull", "pull out", "pull-out", false],
  ["Medium shot, pan left", "ms", "pan", "pan left", "pan-right", false],
  ["Medium shot, left to right", "ms", "none", "pan left", "pan-right", false],
  ["Medium shot, pan right", "ms", "pan", "pan right", "pan-left", false],
  ["Wide, tilt up", "ws", "tilt", "tilt up", "tilt-up", false],
  ["Wide, crane down", "ws", "tilt", "tilt down", "tilt-down", false],
  ["Extreme close-up of her eyes, drift", "ecu", "none", "drift", "drift", true],
  ["Medium close-up", "mcu", "none", "drift", "drift", true],
  ["Close-up, handheld", "cu", "track", "drift", "drift", true],
  ["Close-up, slow orbit", "cu", "track", "drift", "drift", true],
  ["POV: wide view of the hall from the stage", "pov", "none", "drift", "drift", true],
  // a written drift wins over static (assemble's table tries drift first)
  ["Medium shot, static, slight handheld drift", "ms", "locked", "drift", "drift", true],
  // a person's verb: the clause reader refuses it, the whole-word readers take it
  ["Medium shot as she pushes the box back", "ms", "none", "push in", "push-in", true],
  ["Medium close-up; her eyes fixed on the door, slow push in", "mcu", "push", "locked", "locked", true],
  ["Wide shot, the hall seen through the archway", "ws", "none", "drift", "drift", true],
];

test("the contract's own rows read the same way (pan left is pan-right, drift beats static, a person's verb is not a move)", () => {
  for (const [camera, size, craft, slides, assemble, psnr] of OWN_ROWS) {
    assert.deepEqual(reading(camera), { size, craft, slides, assemble, psnr }, camera);
  }
  assert.equal(motionMove({ camera: "Close-up" }, "bird").direction, motionMove({ camera: "Close-up" }, "bird").direction, "a drift's direction comes from the shot id");
  assert.ok(["left", "right"].includes(motionMove({ camera: "Close-up" }, "bird").direction));
});

test("sizes disagree only across families, and a prompt names a size only with a shot phrase", () => {
  assert.equal(sizesDisagree({ camera: "Medium close-up", prompt: "Wide shot of the hall" }), true);
  assert.equal(sizesDisagree({ camera: "Close-up", prompt: "Medium close-up of Lin" }), false, "two face sizes are one family");
  assert.equal(sizesDisagree({ camera: "Close-up", prompt: "a girl in wide sleeves" }), false);
  assert.equal(isLookOnly({ motion: "Her fingers tighten once around the pen." }), true);
  assert.equal(isLookOnly({ motion: "Lin offers the cup with both hands." }), false);
});

test("a person's clause in the camera line is found by pronoun, noun phrase or character name", () => {
  assert.equal(personClause("Medium shot as she pushes the box back"), "she pushes");
  assert.equal(personClause("Close-up; her hand trembles on the pen"), "her hand trembles");
  assert.equal(personClause("Medium shot while Lin rises from the chair"), "Lin rises");
  assert.equal(personClause("Medium shot while lin rises", ["lin"]), "lin rises");
  assert.equal(personClause("Medium shot, slow push in"), null, "a camera's own words are not a person");
  assert.equal(personClause("Camera pushes in slowly"), null);
  assert.equal(personClause("Wide establishing shot of the hall"), null);
});

test("the keyframe prompt is composed the way keyframes.mjs composes it", () => {
  const look = { style: "2D anime" };
  const cast = [{ id: "lin", name: "林", appearance: "a bride in red" }];
  assert.equal(keyframePrompt({ prompt: "Lin at the table", camera: "Close-up" }, look, cast), "Lin at the table. Style: 2D anime. Camera: Close-up. Characters: 林: a bride in red");
  assert.equal(keyframePrompt({ prompt: "A hall" }, look, []), "A hall. Style: 2D anime");
});

// One shot through the --file path: its traps' ids.
const trapsOf = (shot) => {
  const { doc, series } = shotFileDocument(shot);
  return readDocument(doc, { series, single: true }).shots[0].traps.map((trap) => trap.id);
};
const CLEAN = {
  camera: "Medium close-up, slow push in",
  prompt: "Lin lifts the teacup with both hands at the banquet table, Zhao speaks off screen",
  motion: "Lin offers the cup with both hands.",
  characters: [{ id: "lin", name: "林", appearance: "a young bride in red" }, { id: "zhao", name: "趙", appearance: "the mother-in-law" }],
  lines: [{ speaker: "zhao", text: "這杯茶我不喝。" }],
  look: { preset: "anime-2d" },
};
const clean = (change = {}) => ({ ...CLEAN, characters: [CLEAN.characters[0]], ...change });

test("a clean clip shot trips no trap", () => {
  assert.deepEqual(trapsOf(clean()), []);
  assert.deepEqual(trapsOf(clean({ visual: "still", camera: "Medium close-up, locked", lines: [], action_seconds: 2 })), ["still.locked"], "a locked still is reported, so the hold is a decision");
});

// One change to the clean shot, one trap it must trip.
const cases = [
  ["size.none", "a camera line without a size", { camera: "slow push in" }],
  ["size.disagree", "a prompt that names another family", { prompt: "Wide shot of the hall, Zhao speaks off screen" }],
  ["still.drift", "a still whose camera names no table move", { visual: "still", camera: "Medium close-up, slow orbit" }],
  ["still.locked", "a locked still", { visual: "still", camera: "Medium close-up, locked" }],
  ["camera.person", "a person's verb in the camera line", { camera: "Medium shot as she pushes the cup back" }],
  ["move.disagree", "drift written after static", { camera: "Medium close-up, static, slight handheld drift" }],
  ["motion.empty", "a clip with no motion", { motion: "" }],
  ["motion.look", "a wide clip whose only behaviour is a look", { camera: "Wide, slow push in", motion: "She stares at the door." }],
  ["look.motion", "a locked camera under a look whose motion names a camera move", { camera: "Medium close-up, locked", look: { preset: "cinematic-3d" } }],
  ["cast.offscreen", "an off-screen speaker listed in characters", { characters: CLEAN.characters, prompt: "Lin lifts the teacup, Zhao speaks off screen" }],
  ["cast.speaker", "a line's speaker not in characters and no off-screen note", { prompt: "Lin lifts the teacup with both hands at the banquet table" }],
  ["cast.count", "four characters", { characters: ["lin", "zhao", "father", "uncle"], prompt: "Lin lifts the teacup, Zhao speaks off screen" }],
  ["prompt.camera", "a prompt that repeats the camera line", { prompt: "Medium close-up, slow push in, Lin lifts the teacup, Zhao speaks off screen" }],
  ["prompt.length", "a composed keyframe prompt past 4000 characters", { prompt: "x".repeat(MAX_PROMPT_CHARS) }],
  ["source.length", "a cut that ends past the clip under a production profile", { source: { shot: "s1", from_s: 6 }, production: true, lines: [{ speaker: "zhao", text: "一二三四五六七八九十一二三四五" }] }],
];
for (const [id, what, change] of cases) {
  test(`${id} trips on ${what}`, () => {
    const ids = trapsOf(clean(change));
    assert.ok(ids.includes(id), `${id} missing from ${JSON.stringify(ids)}`);
  });
}

// cast.offscreen reads whom the off-screen words attach to. A visible actor aiming at someone off
// screen keeps its place in characters; the one off screen is still reported; a clause it cannot
// read is still reported, as a question rather than an instruction to remove a character.
const DUEL = [{ id: "yan", name: "Yan", appearance: "a swordsman in grey" }, { id: "wei", name: "Wei", appearance: "a rival in black" }];
const duel = (data) => ({
  format: "drama",
  characters: DUEL,
  look: { preset: "anime-2d" },
  scenes: [{ id: "s1", template: "shot", data: { camera: "Medium close-up, slow push in", prompt: "Medium close-up of Yan on screen left facing right", motion: "Yan swings the sword once.", characters: ["yan"], ...data }, lines: [{ id: "l1", speaker: "yan", text: "接招。" }] }],
});
const offscreenTraps = (data) => readDocument(duel(data)).shots[0].traps.filter((trap) => trap.id === "cast.offscreen");

test("offScreenRoles tells the visible actor from the named off-screen target, and leaves what it cannot read unsure", () => {
  const rows = [
    // the ticket's sentence: Yan acts, Wei is the target off screen
    ["One cyan arc leaves Yan's sword toward Wei off screen right", ["wei"], []],
    ["Yan with his eyes on Wei off screen right", ["wei"], []],
    ["Yan turns to Wei off screen left", ["wei"], []],
    ["Yan bows toward Old Wei off screen", ["wei"], []],
    ["Yan looks off screen right", [], []],
    ["Yan glances off screen right at Wei", ["wei"], []],
    ["Yan looks toward the gate off screen", [], []],
    // an explicit off-screen subject, alone in its clause
    ["Wei speaks off screen", ["wei"], []],
    ["Wei off screen left at his eyeline", ["wei"], []],
    ["Wei is off screen to the right", ["wei"], []],
    ["the gift remains held by Wei off screen", ["wei"], []],
    ["a voice from off screen", ["yan"], []],
    // what the wording does not settle
    ["Yan raises the sword as Wei shouts off screen", [], ["yan", "wei"]],
    ["Yan speaks to Wei off screen", [], ["yan", "wei"]],
    ["Yan swings toward the gate off screen", [], ["yan"]],
    ["Yan faces the unseen Wei", [], ["yan", "wei"]],
  ];
  for (const [clause, off, unsure] of rows) {
    const roles = offScreenRoles(clause, DUEL, ["yan"]);
    assert.deepEqual({ off: roles.off, unsure: roles.unsure }, { off, unsure }, clause);
    assert.equal(Boolean(roles.why), unsure.length > 0, `${clause}: an unsure reading says why`);
  }
  // --file lists only who is in the shot: an unlisted capitalised name after toward is still a target, not the actor
  assert.deepEqual(offScreenRoles("One cyan arc leaves Yan's sword toward Wei off screen right", [DUEL[0]]), { off: [], unsure: [], why: "" });
});

test("cast.offscreen leaves a visible actor aiming at a named off-screen target alone", () => {
  const motion = "One cyan arc leaves Yan's sword toward Wei off screen right.";
  assert.deepEqual(offscreenTraps({ motion }), [], "Yan is in the shot and stays in characters");
  assert.ok(!trapsOf({ ...clean(), characters: [{ id: "yan", name: "Yan", appearance: "a swordsman" }], prompt: "Medium close-up of Yan on screen left facing right", motion, lines: [{ speaker: "yan", text: "接招。" }] }).includes("cast.offscreen"), "--file mode, where Wei is not in the cast at all");
  const both = offscreenTraps({ motion, characters: ["yan", "wei"] });
  assert.equal(both.length, 1, "only the target listed by mistake is reported");
  assert.match(both[0].message, /列了 wei/);
  assert.equal(both[0].fix, "從 characters 拿掉 wei；台詞的 speaker 留著");
});

test("cast.offscreen still reports an explicit off-screen subject listed in characters", () => {
  const traps = offscreenTraps({ prompt: "Medium close-up of Yan on screen left facing right, Wei speaks off screen", characters: ["yan", "wei"] });
  assert.equal(traps.length, 1);
  assert.match(traps[0].message, /（「Wei speaks off screen」），但 data\.characters 列了 wei/);
  assert.equal(traps[0].fix, "從 characters 拿掉 wei；台詞的 speaker 留著");
});

test("cast.offscreen keeps an ambiguous clause reviewable without telling the author to remove a visible character", () => {
  const traps = offscreenTraps({ motion: "Yan raises the sword as Wei shouts off screen." });
  assert.equal(traps.length, 1, "the clause names Yan and Wei and says off screen: still a trap, so --strict stops on it");
  assert.match(traps[0].message, /讀不出是誰（同一子句點了 yan、wei）/);
  assert.match(traps[0].fix, /^先確認 yan 在不在畫面裡/);
  assert.match(traps[0].fix, /在畫面裡就留著/);
  assert.ok(!traps[0].fix.startsWith("從 characters 拿掉"));
  const split = offscreenTraps({ motion: "Yan raises the sword, Wei shouts off screen." });
  assert.deepEqual(split, [], "split into its own clause, the off-screen subject is read and Yan is left alone");
  assert.match(offscreenTraps({ motion: "Yan speaks to Wei off screen." })[0].message, /說話的動詞接「to Wei」/);
});

test("o.s. and v.o. survive the clause split and read as off screen", () => {
  const listed = trapsOf(clean({ characters: CLEAN.characters, prompt: "Close-up of Lin, Zhao (o.s.)" }));
  assert.ok(listed.includes("cast.offscreen"), `(o.s.) marks Zhao off screen: ${JSON.stringify(listed)}`);
  for (const prompt of ["Close-up of Lin, Zhao (O.S.)", "Close-up of Lin, Zhao V.O.", "Close-up of Lin, Zhao v.o."]) {
    const ids = trapsOf(clean({ prompt }));
    assert.ok(!ids.includes("cast.speaker"), `${prompt}: the abbreviation already says Zhao is off screen`);
  }
  const message = offscreenTraps({ prompt: "Medium close-up of Yan on screen left facing right, Wei (o.s.)", characters: ["yan", "wei"] });
  assert.equal(message.length, 1);
  assert.match(message[0].message, /（「Wei \(off screen\)」），但 data\.characters 列了 wei/);
  // a period that ends an honorific still splits as before; only the two abbreviations are spelled out
  assert.ok(trapsOf(clean({ prompt: "Mr. Lin lifts the teacup with both hands at the banquet table" })).includes("cast.speaker"));
});

test("look.motion claims a contradiction only when the look's motion names a camera move", () => {
  // The pilot's override (production-run-20261003.md) names no move, so a locked clip under it is not two instructions.
  const plain = { style: "2D anime", motion: "One clearly motivated character or prop action per clip, consistent adult identity, no morphing, no internal cuts." };
  assert.ok(!trapsOf(clean({ camera: "Medium close-up, locked", look: plain })).includes("look.motion"));
  assert.ok(trapsOf(clean({ camera: "Medium close-up, locked", look: { ...plain, motion: "slow drifting camera, limited animation" } })).includes("look.motion"));
  assert.ok(!trapsOf(clean({ camera: "Medium close-up, slow push in" })).includes("look.motion"), "an unlocked camera takes the preset's move");
  assert.equal(lookMotionMove("gentle camera move, limited animation, consistent character design, no morphing, no cuts"), "camera move");
  assert.equal(lookMotionMove("slow push in or gentle drift, subtle natural motion"), "push");
  assert.equal(lookMotionMove(plain.motion), null);
  assert.equal(lookMotionMove(""), null);
  const { doc } = shotFileDocument(clean({ camera: "Medium close-up, locked", look: plain }));
  const report = readDocument(doc, { single: true });
  assert.equal(report.look.move, null);
  assert.match(renderReading(report), /look custom，look.motion「One clearly[^」]*」（沒有運鏡字；仍接在每支 clip 的 camera 後面）/);
});

test("source.shot trips in a document whose cut names a still or a missing shot, never in --file mode", () => {
  const doc = {
    format: "drama",
    characters: [{ id: "lin", name: "林", appearance: "a bride" }],
    scenes: [
      { id: "a", template: "shot", data: { prompt: "the hall", camera: "Wide, locked", motion: "Guests turn.", characters: ["lin"], visual: "still" }, lines: [{ id: "l1", speaker: "lin", text: "開始。" }] },
      { id: "b", template: "shot", data: { prompt: "the hall", camera: "Wide, locked", motion: "Guests turn.", characters: ["lin"], source: { shot: "a", from_s: 0 } }, lines: [{ id: "l2", speaker: "lin", text: "坐。" }] },
      { id: "c", template: "shot", data: { prompt: "the hall", camera: "Wide, locked", motion: "Guests turn.", characters: ["lin"], source: { shot: "zzz", from_s: 0 } }, lines: [{ id: "l3", speaker: "lin", text: "好。" }] },
    ],
  };
  const report = readDocument(doc);
  assert.deepEqual(report.shots.map((shot) => shot.visual_label), ["still", "cut from a@0s", "cut from zzz@0s"]);
  assert.ok(report.shots[1].traps.some((trap) => trap.id === "source.shot" && /still/.test(trap.message)));
  assert.ok(report.shots[2].traps.some((trap) => trap.id === "source.shot" && /不在/.test(trap.message)));
  assert.ok(!trapsOf(clean({ source: { shot: "s1", from_s: 0 } })).includes("source.shot"));
});

test("source.bought trips when a cut ends past what its source buys under the server's default model, and not under the profile's fixed 8 s", () => {
  // The source says six characters (2.2 s with the pause and the gap): the server's default model
  // buys clamp(ceil(frames/30), 4, 10) = 4 s for it, not the 10 s lint allows a cut to reach; the
  // cut itself is about 3.3 s, so from 3 s it ends near 6.3 s and from 0.5 s near 3.8 s.
  const cut = (from_s) => ({
    format: "drama",
    characters: [{ id: "lin", name: "林", appearance: "a bride" }],
    scenes: [
      { id: "a", template: "shot", data: { prompt: "the hall", camera: "Wide, locked", motion: "Guests turn.", characters: ["lin"] }, lines: [{ id: "l1", speaker: "lin", text: "大家請坐下。" }] },
      { id: "b", template: "shot", data: { prompt: "the hall", camera: "Wide, locked", motion: "Guests turn.", characters: ["lin"], source: { shot: "a", from_s } }, lines: [{ id: "l2", speaker: "lin", text: "坐下來，喝口茶。" }] },
    ],
  });
  const without = readDocument(cut(3));
  const [a, b] = without.shots;
  assert.equal(boughtSeconds(a.seconds, false), 4, `a is ${a.seconds} s and buys 4 s without a profile`);
  assert.equal(boughtSeconds(a.seconds, true), PRODUCTION_CLIP_SECONDS);
  assert.ok(3 + b.seconds > 4 && 3 + b.seconds <= 10, `the cut ends at ${3 + b.seconds} s: inside lint's 10 s, past the 4 s bought`);
  const trap = b.traps.find((each) => each.id === "source.bought");
  assert.ok(trap, `source.bought missing from ${JSON.stringify(b.traps.map((each) => each.id))}`);
  assert.match(trap.message, /只買 4 s/);
  assert.match(trap.fix, /from_s 提早到/);
  assert.ok(!b.traps.some((each) => each.id === "source.length"), "lint itself lets this cut through");
  assert.ok(!readDocument(cut(0.5)).shots[1].traps.some((each) => each.id === "source.bought"), "a cut that ends inside the 4 s is fine");
  const production = readDocument(cut(3), { series: { production: { profile: { id: "test" } } } });
  assert.ok(!production.shots[1].traps.some((each) => each.id === "source.bought"), "under the profile the source buys 8 s and the cut fits");
  assert.ok(!trapsOf(clean({ source: { shot: "s1", from_s: 3 } })).includes("source.bought"), "--file mode has no source to measure");
});

test("every trap id has a case above, so a deleted trap is noticed", () => {
  const covered = new Set([...cases.map(([id]) => id), "source.shot", "source.bought"]);
  assert.deepEqual([...TRAP_IDS].sort(), [...covered].sort());
});

test("the repository's drama fixture reads as the contract describes it", () => {
  const report = readDocument(dramaFixture(), { file: "fixture" });
  const byId = Object.fromEntries(report.shots.map((shot) => [shot.id, shot]));
  assert.deepEqual(Object.keys(byId), ["opening", "farewell", "sea-storm", "bird"], "the outro card is not a shot");
  assert.deepEqual(byId.opening.size, { craft: "ws", family: "wide", camera: null, prompt: "ws" }, "a size the camera line lacks is read from the prompt");
  assert.deepEqual(byId.opening.move, { craft: "push", slides: "push in", assemble: { name: "push-in", psnr_checked: true } });
  assert.equal(byId.farewell.move.craft, "locked", "craft reads static as locked");
  assert.equal(byId.farewell.move.assemble.name, "drift", "assemble lets the written drift win");
  assert.deepEqual(byId.farewell.speakers, ["jingwei", "yandi"]);
  assert.deepEqual(byId.bird.characters, []);
  for (const shot of report.shots) assert.ok(shot.traps.some((trap) => trap.id === "size.none"), `${shot.id} names no size in its camera line`);
  assert.deepEqual(byId.farewell.traps.map((trap) => trap.id), ["size.none", "move.disagree", "look.motion"]);
  assert.deepEqual(byId.bird.traps.map((trap) => trap.id), ["size.none", "cast.speaker"]);
  assert.equal(report.summary.traps, 7);
  assert.equal(report.look.preset, "cinematic-3d");
  assert.ok(byId.opening.keyframe_prompt_chars > 0 && byId.opening.keyframe_prompt_chars < MAX_PROMPT_CHARS);
  const text = renderReading(report);
  assert.match(text, /\[opening\] clip · 約 [\d.]+ s · 2 lines（narrator） · characters: jingwei/);
  assert.match(text, /craft cameraMove: locked \| slides cameraMove: drift \| assemble motionMove（still 時）: drift (?:left|right)（第 0 格驗 PSNR: yes）/);
  assert.match(text, /讀了 4 個鏡頭，7 個陷阱：size\.none 4、move\.disagree 1、look\.motion 1、cast\.speaker 1/);
});

test("a series.json beside the video turns on the production profile's 8-second clip", () => {
  const box = sandbox("fixture-drama", "drama");
  try {
    const file = join(box.dir, "video.json");
    const doc = JSON.parse(readFileSync(file, "utf8"));
    // A cut from the opening's clip that ends past 8 s but inside 10 s: eleven characters are
    // about 3.6 s with the pause and the scene gap, so from 5 s it ends near 8.6 s.
    doc.scenes.splice(1, 0, { id: "opening-again", template: "shot", data: { ...doc.scenes[0].data, source: { shot: "opening", from_s: 5 } }, lines: [{ id: "cut1", speaker: "jingwei", text: "我去看看海就回來，父王。" }] });
    writeFileSync(file, JSON.stringify(doc));
    const without = JSON.parse(spawnSync(process.execPath, [SCRIPT, file, "--json", "--shot", "opening-again"], { encoding: "utf8" }).stdout);
    assert.equal(without.production, false);
    assert.ok(!without.shots[0].traps.some((trap) => trap.id === "source.length"), "inside MAX_SOURCE_CLIP_SECONDS without a profile");
    writeFileSync(join(box.dir, "series.json"), JSON.stringify({ slug: "fixture-drama", production: { profile: { id: "test" } } }));
    const result = spawnSync(process.execPath, [SCRIPT, file, "--json", "--shot", "opening-again"], { encoding: "utf8" });
    const report = JSON.parse(result.stdout);
    assert.equal(report.production, true);
    const trap = report.shots[0].traps.find((each) => each.id === "source.length");
    assert.ok(trap, "the same cut is too long under the profile");
    assert.match(trap.message, new RegExp(`超過 ${PRODUCTION_CLIP_SECONDS} s`));
    assert.equal(PRODUCTION_CLIP_SECONDS, 8);
  } finally {
    rmSync(box.base, { recursive: true, force: true });
  }
});

test("the command exits 0, 1 with --strict on a trap, and 2 on what it cannot read", () => {
  const dir = mkdtempSync(join(tmpdir(), "shot-reading-"));
  try {
    const run = (...args) => spawnSync(process.execPath, [SCRIPT, ...args], { encoding: "utf8" });
    assert.equal(run(DRAMA_FIXTURE_FILE).status, 0, "traps alone do not fail the command");
    const strict = run(DRAMA_FIXTURE_FILE, "--strict");
    assert.equal(strict.status, 1);
    assert.match(strict.stdout, /陷阱  size\.none/);
    const json = JSON.parse(run(DRAMA_FIXTURE_FILE, "--json").stdout);
    assert.equal(json.shots.length, 4);
    assert.deepEqual(Object.keys(json.summary), ["shots", "traps", "by_kind"]);
    const only = JSON.parse(run(DRAMA_FIXTURE_FILE, "--json", "--shot", "bird,farewell").stdout);
    assert.deepEqual(only.shots.map((shot) => shot.id), ["farewell", "bird"], "--shot keeps the document's order");
    const missing = run(DRAMA_FIXTURE_FILE, "--shot", "nope");
    assert.equal(missing.status, 2);
    assert.match(missing.stderr, /找不到鏡頭 nope/);
    assert.equal(run().status, 2);
    assert.equal(run(join(dir, "missing.json")).status, 2);
    assert.equal(run(MINIMAL_FIXTURE).status, 2, "a slides video is not a drama");
    assert.equal(run(DRAMA_FIXTURE_FILE, "--bogus").status, 2);

    const good = join(dir, "clean.json"), bad = join(dir, "bad.json"), list = join(dir, "list.json");
    writeFileSync(good, JSON.stringify(clean()));
    writeFileSync(bad, JSON.stringify(clean({ camera: "slow push in" })));
    writeFileSync(list, JSON.stringify([clean()]));
    assert.equal(run("--file", good, "--strict").status, 0);
    const failed = run("--file", bad, "--strict");
    assert.equal(failed.status, 1);
    assert.match(failed.stdout, /size\.none/);
    assert.equal(JSON.parse(run("--file", bad, "--json").stdout).shots[0].traps[0].id, "size.none");
    assert.equal(run("--file", list).status, 2, "a one-shot file is an object");
    assert.equal(run("--file").status, 2);
  } finally {
    rmSync(dir, { recursive: true, force: true });
  }
});
