import assert from "node:assert/strict";
import test from "node:test";

import { DRAMA_INSTRUCTIONS, EXPLAINER_INSTRUCTIONS, INSTRUCTIONS, instructionsFor, LISTENER_REGISTER, LISTENER_REWRITE, VARIANT_INSTRUCTIONS } from "./prompts.mjs";
import { REGISTER_RULES } from "./register.mjs";

test("the slides writer is told the shot template, the 5 to 8 second cadence, the storytelling register, the look and the two Shorts", () => {
  const writer = instructionsFor("writer", "slides");
  assert.equal(writer, INSTRUCTIONS.writer);
  assert.match(writer, /- shot \{prompt, camera, visual: "still", transition\?\}/);
  assert.match(writer, /at most 1000 characters/);
  assert.match(writer, /push in, pull out, pan left, pan\s+right, tilt up, tilt down, drift/);
  assert.match(writer, /middle\s+60% of the frame/);
  assert.match(writer, /5 to 8 seconds/);
  assert.match(writer, /shots under at least half of the runtime/);
  assert.match(writer, /"look": \{"preset": "tech-story"\}/);
  assert.match(writer, /"shorts": \[<Short 1>, <Short 2>\]/);
  assert.match(writer, /within 20 seconds/);
  assert.match(writer, /"fix" is present with kind "keyframes"/);
  assert.ok(writer.includes(REGISTER_RULES), "the register's rules, word for word");
  assert.match(writer, /「你以為…其實…」/);
  assert.doesNotMatch(writer, /dark slides and a synthesized/, "the channel is no longer described as dark slides");
  assert.match(writer, /AI-drawn illustrations with camera moves/);
});

test("the planner outlines story beats and the listener keeps the register; the fact-checker and the translators are untouched", () => {
  const planner = instructionsFor("planner", "slides");
  assert.match(planner, /你以為／其實：「<what the viewer believes>/);
  assert.match(planner, /收尾問題：「…」/);
  assert.match(planner, /"shot: <the picture in a few words>"/);
  assert.ok(planner.includes(REGISTER_RULES));
  const listener = instructionsFor("listener", "slides");
  assert.match(listener, /keep the storytelling register below/);
  assert.match(listener, /the facts, the scenes, the pictures' prompts and the line ids are not/);
  assert.ok(listener.endsWith(REGISTER_RULES));
  for (const stage of ["verifier", "translator", "caption_reviewer"]) assert.equal(INSTRUCTIONS[stage].includes(REGISTER_RULES), false, `${stage} reads no register rules`);
});

test("the listener's register pass is a variant for any format, beside the rewrite pass", () => {
  assert.equal(VARIANT_INSTRUCTIONS["listener:register"], LISTENER_REGISTER);
  assert.equal(instructionsFor("listener", "slides", "", "register"), LISTENER_REGISTER);
  assert.equal(instructionsFor("listener", "drama", "", "register"), LISTENER_REGISTER);
  assert.notEqual(LISTENER_REGISTER, LISTENER_REWRITE);
  assert.ok(LISTENER_REGISTER.includes(REGISTER_RULES));
  assert.match(LISTENER_REGISTER, /"lines" lists every narration line as \{id, scene, chapter\?, text\}/);
  assert.match(LISTENER_REGISTER, /add, drop, merge, split or move a line/);
  assert.match(LISTENER_REGISTER, /\{"lines": \[\{"id": "<line id>", "text": "<the retold line>", "pause_after_ms"\?: <integer>\}\]\}/);
  assert.match(instructionsFor("listener", "slides", "先講結論", "register"), /## The owner's standing instructions\n[\s\S]*先講結論$/, "the standing instructions still follow");
});

test("the drama's and the explainer's prompts do not carry the slides register", () => {
  for (const [stage, text] of Object.entries(DRAMA_INSTRUCTIONS)) assert.equal(text.includes(REGISTER_RULES), false, `drama ${stage}`);
  for (const [key, text] of Object.entries(EXPLAINER_INSTRUCTIONS)) assert.equal(text.includes(REGISTER_RULES), false, key);
  assert.equal(instructionsFor("writer", "drama", "", "explainer").includes("shots under at least half"), false, "the explainer keeps its own cadence text");
  assert.match(instructionsFor("writer", "drama", "", "explainer"), /a new picture every 4 to 6 seconds/);
  assert.equal(instructionsFor("writer", "drama"), DRAMA_INSTRUCTIONS.writer);
  assert.equal(instructionsFor("listener", "drama"), DRAMA_INSTRUCTIONS.listener);
  assert.match(DRAMA_INSTRUCTIONS.listener, /You edit for the ear[\s\S]*This is a drama: every line has a "speaker"/);
  assert.equal(DRAMA_INSTRUCTIONS.listener.includes("storytelling register"), false, "a drama's listener keeps its speakers, not the slides register");
});
