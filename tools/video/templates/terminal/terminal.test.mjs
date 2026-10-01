import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

import { lintVideo } from "../../core/lint.mjs";
import { renderPlan } from "../../render/plan.mjs";
import { sceneProblems, slideHtml } from "../templates.mjs";
import { columns, TERMINAL_COLUMNS, TERMINAL_OUTPUT_LINES } from "./terminal.mjs";

// A Claude Code tutorial whose two terminal scenes are copied from real runs on 2026-10-01.
const read = (file) => readFileSync(new URL(file, import.meta.url), "utf8");
const tutorial = JSON.parse(read("./fixtures/claude-code/video.json"));
const scene = (id) => structuredClone(tutorial.scenes.find((each) => each.id === id));
const state = (overrides = {}) => ({ reveal: 0, previousReveal: 0, first: true, totalReveals: 0, chapter: "章節", chapterNumber: 1, ...overrides });
const FRAME = 1000 / 30;
const delays = (html, className) => [...html.matchAll(new RegExp(`class="${className}" style="animation-delay:([\\d.]+)ms"`, "g"))].map((match) => Number(match[1]));

test("the Claude Code tutorial lints clean, and each terminal scene carries its run's date and version", () => {
  const result = lintVideo(tutorial, { lexicon: JSON.parse(read("./fixtures/lexicon.json")), brief: read("./fixtures/claude-code/brief.md"), others: [], translations: {} });
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
  const terminals = tutorial.scenes.filter((each) => each.template === "terminal");
  assert.equal(terminals.length, 2);
  for (const each of terminals) {
    assert.deepEqual(sceneProblems(each), [], each.id);
    assert.match(slideHtml(each, state()), new RegExp(`<div class="ran">Ran on ${each.data.ran_on} · ${each.data.tool_version.replace(/[()]/g, "\\$&")}</div>`));
  }
});

test("a terminal scene without the real run's date or tool version is refused", () => {
  const version = scene("version");
  delete version.data.ran_on;
  delete version.data.tool_version;
  const problems = sceneProblems(version);
  assert.equal(problems.length, 2);
  assert.match(problems[0], /^ran_on is required/);
  assert.match(problems[1], /^tool_version is required/);
  for (const ranOn of ["2026-02-30", "1 Oct 2026", "2026-10-1"]) assert.match(sceneProblems({ ...version, data: { ...scene("version").data, ran_on: ranOn } })[0], /^ran_on is required/, ranOn);
  for (const tool of ["Claude Code", "2.1\n(Claude Code)", " "]) assert.match(sceneProblems({ ...version, data: { ...scene("version").data, tool_version: tool } })[0], /^tool_version is required/, JSON.stringify(tool));
});

test("the prompt is a bare $ or > and never a user or host name", () => {
  const version = scene("version");
  const html = slideHtml(version, state());
  assert.match(html, /<div class="screen large"><div class="row"><span class="ps">\$<\/span> <span class="cmd">/, "nothing but the prompt before the command");
  version.data.prompt = ">";
  assert.match(slideHtml(version, state()), /<span class="ps">&gt;<\/span> <span class="cmd">/);
  version.data.prompt = "alice@laptop:~$";
  assert.deepEqual(sceneProblems(version), ['prompt must be "$" or ">": a user or host name never goes on a slide']);
});

test("a user name, a host name or an email address in the command or the output is refused; ~ is fine", () => {
  const version = scene("version");
  const problems = (data) => sceneProblems({ ...version, data: { ...version.data, ...data } });
  assert.deepEqual(problems({ command: "cat ~/.claude/settings.json" }), []);
  assert.deepEqual(problems({ output: ["/Users/Shared/notes.txt"] }), []);
  assert.match(problems({ command: "ls /home/alice/project" })[0], /^the command shows a home folder with a user name in it/);
  assert.match(problems({ output: ["C:\\Users\\alice\\project"] })[0], /^the output shows a home folder/);
  assert.match(problems({ output: ["/Users/alice/project"] })[0], /^the output shows a home folder/);
  assert.match(problems({ output: ["alice@laptop:~/project$ ls"] })[0], /^the output shows a user@host prompt/);
  assert.match(problems({ output: ["Logged in as alice@example.com"] })[0], /^the output shows an email address/);
});

test("long output is refused, not clipped: 80 columns, wide characters counting two, and 8 lines", () => {
  const version = scene("version");
  const problems = (data) => sceneProblems({ ...version, data: { ...version.data, ...data } });
  assert.equal(columns("abc"), 3);
  assert.equal(columns("中文ab"), 6);
  assert.deepEqual(problems({ output: ["x".repeat(TERMINAL_COLUMNS)] }), []);
  assert.match(problems({ output: ["x".repeat(TERMINAL_COLUMNS + 1)] })[0], /an output line is longer than 80 columns/);
  assert.match(problems({ output: ["中".repeat(41)] })[0], /longer than 80 columns/);
  assert.deepEqual(problems({ output: ["a\nb\nc\nd", "e\nf\ng\nh"] }), []);
  assert.match(problems({ output: ["a\nb\nc\nd", "e\nf\ng\nh\ni"] })[0], new RegExp(`output has 9 lines; at most ${TERMINAL_OUTPUT_LINES} fit`));
  assert.match(problems({ output: ["a\tb"] })[0], /expand it to spaces/);
  assert.match(problems({ command: "claude\n--version" })[0], /command must be one line of at most 78 columns/);
  assert.match(problems({ command: "x".repeat(79) })[0], /command must be one line/);
  assert.match(problems({ output: [] })[0], /^output must be 1 to 6 parts/);
});

test("the first state types the command one key per frame, and output it shows comes the frame after the last key", () => {
  const version = scene("version");
  // No reveals: the version is printed in the same state as the typing.
  version.lines.forEach((line) => delete line.reveal);
  const html = slideHtml(version, state());
  const keys = delays(html, "k");
  assert.equal(keys.length, [..."claude --version"].length);
  keys.forEach((delay, index) => assert.ok(Math.abs(delay - index * FRAME) < 0.001, `key ${index} at ${delay}`));
  const [print] = delays(html, "row out print");
  assert.ok(Math.abs(print - 17 * FRAME) < 0.001, "16 keys, then one frame");
  assert.deepEqual(delays(html, "caret gone"), [print], "the caret leaves when the output arrives");
  assert.match(html, /\.t-terminal \.k\{animation:term-key 1ms steps\(1,end\) both\}/);
});

test("a long command is squeezed into the renderer's 18 transition frames", () => {
  const version = scene("version");
  version.data.command = "x".repeat(60);
  const keys = delays(slideHtml(version, state()), "k");
  assert.equal(keys.length, 60);
  assert.ok(keys.at(-1) < 17 * FRAME, `the last key at ${keys.at(-1)} ms`);
});

test("each reveal prints the next output part one line per frame; the command is not typed again", () => {
  const help = scene("help");
  const totalReveals = 2;
  const typing = slideHtml(help, state({ totalReveals }));
  assert.equal((typing.match(/class="row out" data-hidden/g) ?? []).length, 4, "both parts wait, keeping their space");
  assert.match(typing, /<span class="caret"><\/span>/);
  const first = slideHtml(help, state({ reveal: 1, previousReveal: 0, first: false, totalReveals }));
  assert.doesNotMatch(first, /class="k"/);
  assert.match(first, /<span class="cmd">claude --help \| head -n 4<\/span><span class="caret gone" style="animation-delay:0ms"><\/span>/);
  assert.deepEqual(delays(first, "row out print"), [0]);
  const second = slideHtml(help, state({ reveal: 2, previousReveal: 1, first: false, totalReveals }));
  assert.doesNotMatch(second, /<span class="caret/, "the command has printed; no caret is left on its line");
  assert.deepEqual(delays(second, "row out print").map((delay) => Math.round(delay)), [0, 33, 67]);
  assert.match(second, /<div class="row out">Usage: claude \[options\] \[command\] \[prompt\]<\/div>/);
  assert.match(second, /<div class="row out print" style="animation-delay:0ms"> <\/div>/, "a blank line keeps its row");
  help.lines[2].reveal = 2;
  assert.deepEqual(sceneProblems(help), ["reveals 3 elements but the terminal slide has 2"]);
});

test("a short session is set larger; a wide or long one keeps the size that fits 80 columns and 8 lines", () => {
  assert.match(slideHtml(scene("version"), state()), /<div class="screen large">/);
  assert.match(slideHtml(scene("help"), state()), /<div class="screen">/);
});

test("the terminal's CSS rides in its own page, so no other slide's frame key moved", () => {
  const plan = renderPlan(tutorial, "theme");
  for (const each of plan.scenes) {
    for (const drawn of each.states) assert.equal(drawn.html.includes("term-key"), each.template === "terminal", each.id);
  }
});
