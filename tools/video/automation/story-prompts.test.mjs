import assert from "node:assert/strict";
import { test } from "node:test";

import { CONDENSATION_RULE, NARRATIVE_RULES, STORY_OPENING_RULE, STORY_SERIES_SCREEN_RULE, TOLD_TO_ONE_VIEWER } from "./register.mjs";
import { STORY_HOOK_RULES, STORY_INSTRUCTIONS } from "./story-prompts.mjs";

const writer = STORY_INSTRUCTIONS["writer:story"];

test("a story's writer is told to plant a hook every 30 to 45 seconds, never 45 seconds without one", () => {
  assert.ok(writer.includes(STORY_HOOK_RULES), "the story hook rules are in what the worker sends");
  assert.match(writer, /About every 30 to 45 seconds of the body \(about 130 to 200 spoken characters\) at least one\s+question is left hanging/);
  assert.match(writer, /No stretch of the body runs longer than 45 seconds without one\./);
  assert.match(writer, /these replace the 60-to-90-second\s+cadence and the three-loops-for-ten-minutes minimum/, "the shared cadence is replaced, not contradicted");
  assert.ok(writer.indexOf(STORY_HOOK_RULES) > writer.indexOf(NARRATIVE_RULES), "the story's cadence comes after the shared rules it replaces");
});

test("every chapter but now ends on an unanswered question or action that the next one picks up", () => {
  assert.match(writer, /Every chapter but "now" ends its last sentence on one concrete, unanswered question or action/);
  assert.match(writer, /the next chapter's first sentence picks it up/);
});

test("a story's hooks stand on facts, keep the shared limits, and the loops table grows to eight for ten minutes", () => {
  assert.match(writer, /A hook stands on a fact of this story: a number, one person's decision, something that should\s+not have happened\. Never an empty promise \(「接下來更精采」/);
  assert.match(writer, /at most one forward hook in the whole story says\s+so out loud, and 「還記得…」 at most five times/);
  assert.match(writer, /"loops" lists at least 8 for ten minutes of narration/);
  assert.match(writer, /at least 3 of them planted in the hook, and every one is paid off/);
  assert.match(writer, /The hook plants at\s+least three; every chapter but "now" leaves one hanging/);
});

test("the explainer videos' shared rules keep their own cadence", () => {
  assert.match(NARRATIVE_RULES, /Every 60 to 90 seconds of the body/);
  assert.ok(!NARRATIVE_RULES.includes("30 to 45 seconds"), "the story cadence stays in the story's prompt");
});

test("a story's writer follows the ten steps and talks to one viewer, after the hook rules (2026-10-25, 2026-11-05)", () => {
  assert.ok(writer.includes(STORY_OPENING_RULE) && writer.includes(TOLD_TO_ONE_VIEWER), "both series rules are in what the worker sends");
  assert.ok(writer.indexOf(STORY_OPENING_RULE) > writer.indexOf(STORY_HOOK_RULES), "the opening follows the cadence it refines");
  // Owner, 2026-11-05: 黑猫研究院's ten steps replace the condensation in these two series.
  assert.match(STORY_OPENING_RULE, /in place of the condensation\s+rule above, so no 30-to-60-second condensation/);
  assert.match(STORY_OPENING_RULE, /at most one or two labels of later climaxes/);
  assert.match(STORY_OPENING_RULE, /The promise, landing at about 0:40 to 1:05: 「今天我們就來聊聊…」/);
  assert.match(STORY_OPENING_RULE, /The first chapter ends\s+here \(40 to 90 seconds; lint warns outside them\)/);
  assert.match(STORY_OPENING_RULE, /A flashback is a short insert opened by a plain time cue/);
  assert.match(STORY_OPENING_RULE, /Nothing arrives out of nowhere/);
  assert.ok(!writer.includes(CONDENSATION_RULE), "the story writer no longer carries the condensation it replaces");
  assert.match(TOLD_TO_ONE_VIEWER, /Lint warns under two 「你」 a thousand characters/);
  assert.match(TOLD_TO_ONE_VIEWER, /about 4\.5 spoken characters a second/);
  assert.ok(!NARRATIVE_RULES.includes("promise sentence"), "the explainers keep the condensation as it was");
});

test("a story's writer puts no card and no word on screen, writes short MiniMax prompts and draws nobody living or dead since 1956 (2026-11-05)", () => {
  assert.ok(writer.includes(STORY_SERIES_SCREEN_RULE));
  assert.match(STORY_SERIES_SCREEN_RULE, /No card and no word on screen/);
  assert.match(STORY_SERIES_SCREEN_RULE, /100 to 200 characters: ONE subject doing ONE\s+action/);
  assert.match(STORY_SERIES_SCREEN_RULE, /It never uses the words no, not, without, text or blank/);
  assert.match(STORY_SERIES_SCREEN_RULE, /A Latin-letter name is said as it is written/);
  assert.match(writer, /No outro card and no other card/);
  assert.doesNotMatch(writer, /ends with one outro card/);
  assert.doesNotMatch(writer, /mild, overcast, soft grey sky or lamp/, "the old dim-light advice is gone");
  assert.match(writer, /one who is living or died in 1956 or later is not drawn at all/);
});
