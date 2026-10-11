// What the owner's refusal of a finished tutorial on 2026-10-11 added to the content-value rules
// (tasks: 2026-10-11-tutorial-worth-rules). The film met every rule written before it:
// docs/videos/claude-code-mods-delivery-check-tutorial loads a supplied mod whose source is
// never on screen, to report whether three file names are in a folder the viewer has open.
import assert from "node:assert/strict";
import test from "node:test";

import { instructionsFor } from "./prompts.mjs";
import { TEACHING_RULES, VALUE_RULES } from "./register.mjs";

test("an outcome the viewer could already reach in a minute is not an outcome, however it is worded", () => {
  assert.match(VALUE_RULES, /Neither is a result the viewer can already\s+get in about a minute with what they use today/);
  assert.match(VALUE_RULES, /however it is worded as an action, nor a single step\s+of another outcome/);
  // The planner's template still says "one or two" (prompts.mjs is bound by the duration receipt).
  assert.match(VALUE_RULES, /where the brief's template says one or two, this rule's two to four holds/);
});

test("a tutorial's main example has to beat the simple way, and a late admission does not repair it", () => {
  assert.match(VALUE_RULES, /In a tutorial the main example is worth the method/);
  assert.match(VALUE_RULES, /「不用這個方法：…」/);
  assert.match(VALUE_RULES, /the example\s+stands only when the subject does something that way cannot, shown as an observed difference/);
  assert.match(VALUE_RULES, /When the simple way gives the same result, the example is wrong for the\s+video/);
  assert.match(VALUE_RULES, /Telling the viewer in a late chapter that the simpler tool is enough does not repair it/);
  assert.match(VALUE_RULES, /never nothing at\s+all \(a Skill against the same steps left in CLAUDE\.md, not against no instructions\)/);
});

test("the subject is opened on screen and the viewer changes it, on both sets of rules", () => {
  assert.match(VALUE_RULES, /In a tutorial the viewer makes or changes the subject/);
  assert.match(VALUE_RULES, /the cards show its own content: the lines that\s+make it work, each with what it does/);
  assert.match(VALUE_RULES, /A supplied package the viewer only runs is not an outcome, whoever the\s+audience is/);
  assert.match(VALUE_RULES, /a download saves typing and never replaces what the video shows/);
  assert.match(VALUE_RULES, /The verb in the title \(做、寫、建立、設定\) is carried out on screen/);
  // The teaching route's "not an internal-code tour" was read as leave to keep the thing shut.
  assert.match(TEACHING_RULES, /That does not close the thing being taught: its own file is on the\s+cards/);
  assert.match(TEACHING_RULES, /the viewer changes at\s+least one of them/);
});

test("a tutorial opens on a result nobody would have guessed", () => {
  assert.match(VALUE_RULES, /A tutorial opens on a result the viewer would not have predicted/);
  assert.match(VALUE_RULES, /Runs with\s+nothing unexpected in them mean the example is too easy/);
});

test("the narration does not talk about the video's own making, and a label does not keep an unrun part", () => {
  assert.match(VALUE_RULES, /The narration\s+never talks about the video's own making/);
  assert.match(VALUE_RULES, /「這支影片沒有跑過」「還沒看過」\s+「這是整理卡，不是錄影」「尚待驗證」/);
  assert.match(VALUE_RULES, /That label is the card's\s+\(its source, its caption, its date\), not a sentence of narration/);
  assert.match(VALUE_RULES, /a part nobody ran is run or cut/);
  assert.match(TEACHING_RULES, /A part that was not run is run before the script is written, or cut/);
  assert.match(TEACHING_RULES, /the label is the card's, never a sentence\s+of narration/);
});

test("a contrast, a second example or an exercise uses the subject and adds a result", () => {
  assert.match(VALUE_RULES, /Each of those uses the subject and adds an observed result the\s+main example did not give/);
  assert.match(VALUE_RULES, /a habit that would read the same in a video on another subject/);
  assert.match(TEACHING_RULES, /each one uses the subject and ends on an observed result the main example did not\s+give/);
  assert.match(TEACHING_RULES, /The same check on other names, or a task done without the subject, is neither/);
});

test("the listener reports them, and the planner, the writer and the listener of a slides video all read them", () => {
  assert.match(VALUE_RULES, /a sentence about the video's own making, a chapter one line would\s+answer, a chapter that never uses the subject, a main example the simple way equals/);
  for (const stage of ["planner", "writer", "listener"]) {
    const prompt = instructionsFor(stage, "slides");
    assert.ok(prompt.includes("In a tutorial the main example is worth the method"), `${stage} reads the worth of the example`);
    assert.ok(prompt.includes("never talks about the video's own making"), `${stage} reads the narration rule`);
  }
  for (const stage of ["verifier", "translator", "caption_reviewer"]) {
    assert.equal(instructionsFor(stage, "slides").includes("In a tutorial the main example is worth the method"), false, `${stage} is not sent the value rules`);
  }
});
