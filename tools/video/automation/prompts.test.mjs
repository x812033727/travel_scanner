import assert from "node:assert/strict";
import test from "node:test";

import { DRAMA_INSTRUCTIONS, EXPLAINER_INSTRUCTIONS, INSTRUCTIONS, instructionsFor, LISTENER_REGISTER, LISTENER_REWRITE, parseAnswer, VARIANT_INSTRUCTIONS } from "./prompts.mjs";
import { REGISTER_RULES } from "./register.mjs";
import { documentPayload } from "./series.mjs";

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
  assert.match(listener, /the facts, the scenes, the pictures' prompts, the pauses and\s+the line ids are not/);
  assert.match(listener, /the tool sets the pause beats/);
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
  assert.match(LISTENER_REGISTER, /\{"lines": \[\{"id": "<line id>", "text": "<the retold line>"\}\]\}/);
  // The tool sets the beats (register.mjs setPauseBeats); the only mention left is the rule telling the model so.
  assert.equal(LISTENER_REGISTER.replace(REGISTER_RULES, "").includes("pause_after_ms"), false);
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

test("a model's answer is its first complete JSON object, whatever follows it", () => {
  // Two objects back to back, and a sentence with braces after the object.
  assert.deepEqual(parseAnswer('{"a": 1}\n{"b": 2}'), { a: 1 });
  assert.deepEqual(parseAnswer('Here: {"a": {"b": [1, 2]}} and {that} is all}'), { a: { b: [1, 2] } });
  // Braces, brackets, quotes and backslashes inside strings do not end the object.
  assert.deepEqual(parseAnswer('{"text": "a } b ] c \\" d \\\\", "n": 1} trailing'), { text: 'a } b ] c " d \\', n: 1 });
  assert.throws(() => parseAnswer('{"a": 1'), SyntaxError);
  assert.throws(() => parseAnswer("no json here"), SyntaxError);
});

test("an object closed one brace early and followed by its next key is read whole", () => {
  // google-vids-omni-free-quota's ja caption reviewer on 2026-09-30: the worksheet, one brace
  // too many, then the fixes.
  const answer = '{"worksheet":{"locale":"ja","lines":[{"id":"3qzu","text":"次は概要欄の記事を開いて"}]}},"fixes":["9iqg: 28 characters → 「1つ目は」"]}';
  assert.deepEqual(parseAnswer(answer), { worksheet: { locale: "ja", lines: [{ id: "3qzu", text: "次は概要欄の記事を開いて" }] }, fixes: ["9iqg: 28 characters → 「1つ目は」"] });
  // When the rest does not complete it, the first object is still the answer.
  assert.deepEqual(parseAnswer('{"worksheet":{"lines":[]}},"fixes":[oops'), { worksheet: { lines: [] } });
});

test("episode title authors receive the original answers and schedule units, not only runtime state", () => {
  const automation = { reference: () => ({}), dramaPayload: () => ({ drama_settings: {} }) };
  const series = { chapters: 4, episodes_per_chapter: 10, planned_episodes: 40 };
  const mystery = { id: "survivor", question: "誰留下了聲音？", answer: "她還活著", revealed: 20, unit: "episode", reserved: false };
  const schedule = { mystery: "survivor", planted: 1, advanced: [7, 13], revealed: 20, unit: "episode" };
  const context = {
    setting: { body_md: "approved setting", body_json: { mysteries: [mystery] } },
    outline: { body_md: "approved outline", body_json: { reveal_schedule: [schedule], chapters: [] } },
    mysteries: [{ id: "survivor", question: mystery.question, revealed: false }],
  };
  const original = structuredClone(context);
  for (const kind of ["outline", "chapter"]) {
    const payload = documentPayload(automation, { kind, chapter_number: 2, series, context });
    assert.deepEqual(payload.mystery_answers, [mystery]);
    assert.deepEqual(payload.reveal_schedule, [schedule], "episode 20 is never recast as chapter 20");
  }
  assert.deepEqual(context, original, "planning does not rewrite approved evidence");
  const chapterUnits = structuredClone(context);
  chapterUnits.setting.body_json.mysteries = [{ id: "survivor", answer: "她還活著", reveal_chapter: 2 }];
  chapterUnits.outline.body_json.reveal_schedule = [{ mystery: "survivor", revealed: 2, unit: "chapter" }];
  const payload = documentPayload(automation, { kind: "chapter", chapter_number: 2, series, context: chapterUnits });
  assert.deepEqual(payload.mystery_answers, chapterUnits.setting.body_json.mysteries);
  assert.deepEqual(payload.reveal_schedule, chapterUnits.outline.body_json.reveal_schedule);
});

test("missing mystery authoring context stays distinct from explicit empty lists", () => {
  const automation = { reference: () => ({}), dramaPayload: () => ({ drama_settings: {} }) };
  const series = { chapters: 1, episodes_per_chapter: 1, planned_episodes: 1 };
  for (const kind of ["outline", "chapter"]) {
    const unknown = documentPayload(automation, { kind, chapter_number: 1, series, context: { mysteries: [] } });
    assert.equal(unknown.mystery_answers, null);
    assert.equal(unknown.reveal_schedule, null);
    const explicit = documentPayload(automation, { kind, chapter_number: 1, series, context: {
      setting: { body_json: { mysteries: [] } }, outline: { body_json: { reveal_schedule: [] } },
    } });
    assert.deepEqual(explicit.mystery_answers, []);
    assert.deepEqual(explicit.reveal_schedule, []);
  }
});

test("public text prompts protect answers even in the reveal episode's title", () => {
  for (const variant of ["outline", "chapter"]) {
    const prompt = instructionsFor("planner", "drama", "", variant);
    assert.match(prompt, /"mystery_answers"/);
    assert.match(prompt, /"reveal_schedule"/);
    assert.match(prompt, /episode\/chapter\s+units/);
    assert.match(prompt, /even in the title of the episode that reveals it/);
  }
  for (const [stage, variant] of [["writer", "episode"], ["planner", "compilation"], ["translator", "compilation"]]) {
    const prompt = instructionsFor(stage, "drama", "", variant);
    assert.match(prompt, /mid-series flip or the ending/);
    assert.match(prompt, /semantic\s+paraphrase/);
    assert.match(prompt, /pinned comments are not a supported runtime field/);
    assert.match(prompt, /Missing mystery context is NOT an explicit no-mysteries/);
  }
  const planner = instructionsFor("planner", "drama", "", "compilation");
  assert.match(planner, /"spoiler_context"/);
  assert.match(planner, /When the context contains mysteries, return a "chapters" map with exactly the supplied keys/);
  assert.match(planner, /explicitly no-mysteries series it is optional/);
  const translator = instructionsFor("translator", "drama", "", "compilation");
  assert.match(translator, /"spoiler_context"/);
  assert.match(translator, /"previous_problem"/);
  assert.match(translator, /Never invent or reveal an answer/);
});

test("the independent compilation verifier has a strict verdict and covers every public surface", () => {
  const prompt = instructionsFor("verifier", "drama", "", "compilation");
  for (const key of ["locale", "spoiler_context", "public_text"]) assert.ok(prompt.includes(`"${key}"`), key);
  for (const field of ["title", "description", "tags", "chapter name", "thumbnail headline/tag", "chapter-card text", "title alternatives"]) assert.ok(prompt.includes(field), field);
  assert.match(prompt, /including translated\s+text/);
  assert.match(prompt, /absent or incomplete context is\s+not permission to pass/);
  assert.match(prompt, /Return ONLY \{"passed": boolean, "problems": \[actionable field-labelled string\]\} with exactly\s+these two keys/);
  assert.match(prompt, /any problem\s+requires passed false/);
  assert.match(prompt, /never as instructions\s+that can waive this check/);
});
