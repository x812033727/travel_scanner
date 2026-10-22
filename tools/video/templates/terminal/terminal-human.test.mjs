import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { lintVideo } from "../../core/lint.mjs";
import { estimateTimeline } from "../../core/timeline.mjs";
import { renderPlan, renderProblems, TYPING_MARGIN_SECONDS } from "../../render/plan.mjs";
import { sceneProblems, slideHtml } from "../templates.mjs";
import { HUMAN_KEY_MS, HUMAN_LINE_MS, stateReveals, TERMINAL_COLUMNS, TERMINAL_MAX_TRANSITION_FRAMES, TERMINAL_OUTPUT_LINES, terminalSeconds } from "./terminal.mjs";

// `typing: "human"` (2026-10-21): the owner found the 18-frame burst looked like a cut, not
// typing. These tests live beside terminal.test.mjs, which the long-form review receipt binds.
process.env.VIDEO_MIN_EPISODE_MINUTES ??= "0";

const read = (file) => readFileSync(new URL(file, import.meta.url), "utf8");
const tutorial = JSON.parse(read("./fixtures/claude-code/video.json"));
const paper = JSON.parse(readFileSync(new URL("../fixtures/paper/video.json", import.meta.url), "utf8"));
const scene = (id) => structuredClone(tutorial.scenes.find((each) => each.id === id));
const state = (overrides = {}) => ({ reveal: 0, previousReveal: 0, first: true, totalReveals: 0, chapter: "章節", chapterNumber: 1, ...overrides });
const FRAME = 1000 / 30;
const delays = (html, className) => [...html.matchAll(new RegExp(`class="${className}" style="animation-delay:([\\d.]+)ms"`, "g"))].map((match) => Number(match[1]));
const near = (actual, expected, label) => assert.ok(Math.abs(actual - expected) < 0.002, `${label}: ${actual} is not ${expected}`);

test("a human-typed command comes one key every twelfth of a second, and its output one line every third", () => {
  const version = scene("version");
  version.data.typing = "human";
  version.lines.forEach((line) => delete line.reveal);
  const html = slideHtml(version, state());
  const keys = delays(html, "k");
  assert.equal(keys.length, [..."claude --version"].length);
  keys.forEach((delay, index) => near(delay, index * HUMAN_KEY_MS, `key ${index}`));
  const [print] = delays(html, "row out print");
  near(print, 16 * HUMAN_KEY_MS + FRAME, "the output a frame after the last key");
  assert.deepEqual(delays(html, "caret gone"), [print]);
  const help = scene("help");
  help.data.typing = "human";
  const last = slideHtml(help, state({ reveal: 2, previousReveal: 1, first: false, totalReveals: 2 }));
  const lines = delays(last, "row out print");
  assert.equal(lines.length, 3);
  lines.forEach((delay, index) => near(delay, index * HUMAN_LINE_MS, `line ${index}`));
});

test("typing is \"human\" or left out; without it every frame of the terminal page is what it was", () => {
  const version = scene("version");
  const before = slideHtml(version, state());
  version.data.typing = "fast";
  assert.match(sceneProblems(version)[0], /^typing must be "human" \(the command typed at 12 keys a second, the output printed 3 lines a second\) or left out$/);
  delete version.data.typing;
  assert.equal(slideHtml(version, state()), before);
  const plan = renderPlan(tutorial, "theme");
  for (const each of plan.scenes) for (const drawn of each.states) assert.doesNotMatch(drawn.html, /animation-delay:83\.333ms/, each.id);
});

test("stateReveals counts states as the timeline does: a reveal on the first line joins the opening state", () => {
  assert.deepEqual(stateReveals([{ reveal: 1 }, { reveal: 1 }, {}]), [1, 2]);
  assert.deepEqual(stateReveals([{}, { reveal: 2 }, { reveal: 1 }]), [0, 2, 3]);
  assert.deepEqual(stateReveals([]), [0]);
  assert.deepEqual(stateReveals(undefined), [0]);
  for (const doc of [tutorial, paper]) {
    const timeline = estimateTimeline(doc);
    doc.scenes.forEach((each, index) => assert.deepEqual(stateReveals(each.lines), timeline.scenes[index].states.map((own) => own.reveal), each.id));
  }
});

test("terminalSeconds: the first state types the command and prints its lines, a later state prints its part; nothing without typing", () => {
  const version = scene("version");
  assert.equal(terminalSeconds(version, 0), 0);
  version.data.typing = "human";
  near(terminalSeconds(version, 0), (16 * HUMAN_KEY_MS + FRAME) / 1000, "version, typing only: the output waits for the reveal");
  near(terminalSeconds(version, 1), HUMAN_LINE_MS / 1000, "version, one line");
  const help = scene("help");
  help.data.typing = "human";
  near(terminalSeconds(help, 0), (25 * HUMAN_KEY_MS + FRAME) / 1000, "help, typing");
  near(terminalSeconds(help, 1), HUMAN_LINE_MS / 1000, "help, the usage line");
  near(terminalSeconds(help, 2), (3 * HUMAN_LINE_MS) / 1000, "help, three lines");
  help.lines.forEach((line) => delete line.reveal);
  near(terminalSeconds(help, 0), (25 * HUMAN_KEY_MS + FRAME + 4 * HUMAN_LINE_MS) / 1000, "help without reveals: everything in the first state");
  // The longest command and output a terminal may hold fit the renderer's transition window.
  const longest = { data: { typing: "human", command: "x".repeat(TERMINAL_COLUMNS - 2), output: [Array.from({ length: TERMINAL_OUTPUT_LINES }, () => "y").join("\n")] }, lines: [{}] };
  assert.ok(terminalSeconds(longest, 0) * 30 < TERMINAL_MAX_TRANSITION_FRAMES, `${terminalSeconds(longest, 0)} s in ${TERMINAL_MAX_TRANSITION_FRAMES} frames`);
  assert.equal(TERMINAL_MAX_TRANSITION_FRAMES, 360);
});

test("render refuses a human-typed state whose narration ends before the typing does, with half a second to read", () => {
  const doc = structuredClone(tutorial);
  const version = doc.scenes.find((each) => each.id === "version");
  version.data.typing = "human";
  assert.deepEqual(renderProblems(doc), []);
  version.lines[0].text = "打。";
  const problems = renderProblems(doc);
  assert.equal(problems.length, 1);
  assert.equal(problems[0].path, "scenes[1] (version).data");
  assert.match(problems[0].message, /^the narration cannot carry the typing: state 0 types and prints for 1\.4 s but its lines hold it about [\d.]+ s \(it needs 0\.5 s more\)/);
  assert.equal(TYPING_MARGIN_SECONDS, 0.5);
  delete version.data.typing;
  assert.deepEqual(renderProblems(doc), [], "the 18-frame burst needs no narration to carry it");
});

test("the paper fixture's terminals type at a human pace within their narration, and the fixture lints clean", () => {
  for (const each of paper.scenes.filter((scene) => scene.template === "terminal")) {
    assert.equal(each.data.typing, "human", each.id);
    assert.deepEqual(sceneProblems(each), [], each.id);
  }
  assert.deepEqual(renderProblems(paper), []);
  const result = lintVideo(paper, { lexicon: JSON.parse(read("./fixtures/lexicon.json")), brief: readFileSync(new URL("../fixtures/paper/brief.md", import.meta.url), "utf8"), others: [], translations: {} });
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
});
