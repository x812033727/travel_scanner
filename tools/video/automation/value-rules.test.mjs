// What the owner's refusal of a finished tutorial on 2026-10-11 added to the content-value rules
// (tasks: 2026-10-11-tutorial-worth-rules). The film met every rule written before it:
// docs/videos/claude-code-mods-delivery-check-tutorial loads a supplied mod whose source is
// never on screen, to report whether three file names are in a folder the viewer has open.
import assert from "node:assert/strict";
import test from "node:test";

import { instructionsFor } from "./prompts.mjs";
import { HEARD_RULES, TEACHING_RULES, VALUE_RULES } from "./register.mjs";

test("an outcome the viewer could already reach in a minute is not an outcome, however it is worded", () => {
  assert.match(VALUE_RULES, /Neither is a result the viewer can already\s+get in about a minute with what they use today/);
  assert.match(VALUE_RULES, /whoever the audience is and however it is worded as\s+an action, nor a single step of another outcome/);
  assert.match(VALUE_RULES, /nor\s+making a thing that gives only such a result: the test is on what the made thing gives the\s+viewer/);
  // The older sentence that admitted by the action what this one refuses by the result.
  assert.match(VALUE_RULES, /is an outcome when no such quick way gives the same judgment/);
  assert.match(VALUE_RULES, /A judgment on the illustrated route is not measured this way/);
  // The planner's own line still says "one or two" (prompts.mjs is bound by the duration receipt).
  assert.match(VALUE_RULES, /where the planner's line for this section says one or two, this rule's\s+two to four holds/);
});

test("a tutorial's main example has to beat the simple way, and a late admission does not repair it", () => {
  assert.match(VALUE_RULES, /In a tutorial the main example is worth the method/);
  assert.match(VALUE_RULES, /「不用這個方法：…」/);
  assert.match(VALUE_RULES, /the example\s+stands only when the subject does something that way cannot, shown as an observed difference/);
  assert.match(VALUE_RULES, /the first of\s+these that reaches it, a look at the folder or the screen, one common command, one ordinary\s+prompt, the product's nearest built-in feature/);
  assert.match(VALUE_RULES, /with the simple way run beside it on the same input/);
  // A good film's simple way cannot always be run by the pipeline (an interactive screen).
  assert.match(VALUE_RULES, /Where that way cannot be run here[\s\S]*its arm is CITED and\s+its card says so/);
  assert.match(VALUE_RULES, /where the answer appears\s+\(a panel, a button, a time beside it\) is not one/);
  assert.match(VALUE_RULES, /The main example's result is shown in the\s+run's own words, on a card whose source names the run/);
  assert.match(VALUE_RULES, /When the simple way gives the same result and the viewer loses nothing the\s+video demonstrates, the example is wrong for the\s+video/);
  assert.match(VALUE_RULES, /the planner takes another example or another topic[\s\S]*a writer given such a brief reports it and does not write around it/);
  assert.match(VALUE_RULES, /unless\s+nothing is what the viewer uses today; a control run without the subject may still show/);
  assert.match(VALUE_RULES, /Telling the viewer in a late chapter that the simpler tool is enough does not repair it/);
  assert.match(VALUE_RULES, /never nothing at\s+all \(a Skill against the same steps left in CLAUDE\.md, not against no instructions\)/);
});

test("the subject is opened on screen and the viewer changes it, on both sets of rules", () => {
  assert.match(VALUE_RULES, /In a tutorial the viewer makes or changes the subject/);
  assert.match(VALUE_RULES, /the cards show its own content: the lines that\s+make it work, each with what it does/);
  assert.match(VALUE_RULES, /A supplied package the viewer only runs is not an outcome, whoever the\s+audience is/);
  assert.match(VALUE_RULES, /a download saves typing and never replaces what the video shows/);
  assert.match(VALUE_RULES, /the thing the title names that the\s+viewer installs, writes or sets[\s\S]*not the errand\s+the example runs it on/);
  assert.match(VALUE_RULES, /A file that fits on three cards is shown whole/);
  assert.match(VALUE_RULES, /Having it written counts only with one\s+logged run from the request on the cards to the file on the cards/);
  assert.match(VALUE_RULES, /for a command or a setting with no file, the full\s+line or the fields/);
  assert.match(VALUE_RULES, /The verb in the brief's title and the video's title \(做、寫、建立、設定\) is carried out on\s+screen/);
  assert.match(TEACHING_RULES, /for a command or a setting with no file, the full line or the fields/);
  // The teaching route's "not an internal-code tour" was read as leave to keep the thing shut.
  assert.match(TEACHING_RULES, /That does not close the thing being taught: its own file is on the\s+cards/);
  assert.match(TEACHING_RULES, /the viewer changes at\s+least one of them/);
});

test("a tutorial's main example gives a result nobody would have guessed, and nobody words one that was not observed", () => {
  assert.match(VALUE_RULES, /A tutorial's main example gives a result the viewer would not have predicted/);
  assert.match(VALUE_RULES, /not an operator's slip \(a\s+mistyped name\) and not a result anyone would guess/);
  // The two films the judges rated highest open on the useful outcome; the rule must not refuse them.
  assert.match(VALUE_RULES, /The video opens on it, or on the useful outcome with\s+that result as the turn of the main example/);
  assert.match(VALUE_RULES, /Runs with\s+nothing unexpected in them mean the example is too easy/);
  assert.match(VALUE_RULES, /an expected\s+result is never worded as a surprise, and a comparison that was not run is never written/);
});

test("the narration does not talk about the video's own making, and a label does not keep an unrun part", () => {
  assert.match(VALUE_RULES, /The narration\s+never talks about the video's own making/);
  assert.match(VALUE_RULES, /「這支影片沒有跑過」「還沒看過」\s+「這是整理卡，不是錄影」「尚待驗證」/);
  assert.match(VALUE_RULES, /That label is the card's\s+\(its source, its caption, its date\), not a sentence of narration/);
  assert.match(VALUE_RULES, /which of the video's makers reported a run's result/);
  // A number said as the video's own run's is what an older sentence of the same rule asks for.
  assert.match(VALUE_RULES, /Saying a number or a result as\s+this video's own run's, or what a run did and how many times it was made, is the step, not\s+the making/);
  assert.match(VALUE_RULES, /In a tutorial a part nobody ran is run or cut, unless it is a step that may\s+stand on CITED evidence/);
  assert.match(TEACHING_RULES, /The labelled walkthrough above is only for a step that is not an outcome\s+and stands on an official example/);
  assert.match(TEACHING_RULES, /A part that was not run is run before the script is written, or cut/);
  assert.match(TEACHING_RULES, /the label is the card's, never a sentence\s+of narration/);
});

test("a contrast, a second example or an exercise uses the subject and adds a result", () => {
  assert.match(VALUE_RULES, /In a tutorial each of those uses the subject and adds an observed result the\s+main example did not give \(outside a tutorial: a sourced fact/);
  assert.match(VALUE_RULES, /a habit that would read the same in a video on another subject/);
  assert.match(TEACHING_RULES, /each one uses the subject and ends on an observed result the main example did not\s+give/);
  assert.match(TEACHING_RULES, /The same check on other names with the same kind of result, the same check on\s+another state of the same input, or a task done without the subject, is neither/);
  assert.match(TEACHING_RULES, /one such\s+state may stand once, as the likely failure/);
  assert.match(VALUE_RULES, /An update's\s+points are not a main example/);
});

test("the listener reports them, and the planner, the writer and the listener of a slides video all read them", () => {
  assert.match(VALUE_RULES, /a sentence about the video's own making, a chapter one line would\s+answer, a chapter that never uses the subject, a main example the simple way equals \(those two\s+in a tutorial only\)/);
  assert.match(VALUE_RULES, /or for a new plan when the example itself is at fault/);
  // The audio-check list no longer hands the writer a sentence the rule keeps out of the narration.
  assert.equal(HEARD_RULES.includes("這支影片沒有跑過"), false);
  for (const stage of ["planner", "writer", "listener"]) {
    const prompt = instructionsFor(stage, "slides");
    assert.ok(prompt.includes("In a tutorial the main example is worth the method"), `${stage} reads the worth of the example`);
    assert.ok(prompt.includes("never talks about the video's own making"), `${stage} reads the narration rule`);
  }
  for (const stage of ["verifier", "translator", "caption_reviewer"]) {
    assert.equal(instructionsFor(stage, "slides").includes("In a tutorial the main example is worth the method"), false, `${stage} is not sent the value rules`);
  }
});
