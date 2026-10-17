import assert from "node:assert/strict";
import { test } from "node:test";

import { NARRATIVE_RULES } from "./register.mjs";
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
