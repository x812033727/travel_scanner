// The storytelling register of an illustrated slides video (docs/videos/ILLUSTRATED.md §說書式旁白),
// decided 2026-09-29: the owner found the tutorials stiff and wants them told the way 黑貓研究院
// tells a business story. One text carries the rules to the planner, the writer and the
// listener (prompts.mjs adds it to their instructions), and the owner can paste the same text
// as a standing instruction on /admin/videos while an older worker runs. The voice style is a
// setting, not a prompt: `settle()` copies the settings tab's `voice` into every new video, and
// STORY_VOICE_STYLE is the text the owner pastes there (it sits in speechHash, so changing it
// records every line again).
import { CHANNEL_ACCENT } from "../core/accent.mjs";
import { eachLine, spokenText } from "../core/schema.mjs";

/** The pauses, in milliseconds, the register asks for around its beats (schema: at most MAX_PAUSE_MS). */
export const PAUSE_BEATS = Object.freeze({
  // After the cold open, before the promise: the viewer settles into the story.
  hook: 900,
  // Before 「其實」: the reveal lands on a breath.
  reveal: 600,
  // After a chapter's closing question: the cliffhanger hangs.
  cliffhanger: 1200,
});

/** The marker of the register's turn: what the viewer believes, then what is so. */
export const TWIST_MARKER = "你以為";

/** Seconds the hook has to land in an illustrated video (core/cadence.mjs HOOK_SECONDS says the same). */
export const HOOK_SECONDS = 20;

// A writing-only route inside the existing slides format. This does not alter the storytelling
// register, voice, schema, pause calculation or QA, and is not sent to drama or translation stages.
export const TEACHING_RULES = `
Teaching route (plain slides; writing only):
- For a tool tutorial or a concept taught through a worked example, the planner writes
  「製作路線：教學卡片」 inside the brief's existing 示範或實算 section. The writer follows the
  chosen outline. An already approved illustrated outline stays illustrated unless the owner
  requested a revision; do not silently restyle or change its scenes in a listener pass.
- Name the intended viewer, a concrete task or decision they need to improve, and what they
  can do after watching in 示範或實算. Choose an example for that benefit, not because an API
  is easy to demonstrate. An audience of everyday users needs a useful workflow, not an
  internal-code tour. Introduce mechanisms and terms only when they explain an observed
  result or help the viewer take the next step; keep their exact official meaning.
- Use one main worked example, a purposeful contrast and a transfer exercise. Show the
  problem and useful outcome early. Provide the starting materials and complete input,
  actions, observable result, why it happened, and how to diagnose a likely failure. Cover
  trust and risk BEFORE installation or any action that grants access; other examples give
  their relevant prerequisites. Compare expected and observed results. The contrast teaches
  when the method applies or fails; the exercise changes a meaningful requirement and gives
  an answer or checking method. These may be variations of the main case, not unrelated demos.
- Reuse the same objects, names and diagram layout across chapters, revealing one new relation
  or state at a time. No forced chapter location, new metaphor, 「你以為…其實」 turn or closing
  question: a short conclusion or the next practical question is enough. If a comparison helps,
  keep one mapping throughout and say where it stops matching the real mechanism.
- This is "format": "slides" with no "shot" scenes, not a new schema field or a QA exemption.
  Use existing cards (steps, compare, chat, code, quote, stats) and public official-page
  screencasts. The automated worker keeps no image assets: build a logical diagram as progressive
  card states or show the actual diagram on a public source page. No diagram/screenshot file
  templates or invented asset paths; omit an optional capture focus selector when none is known.
  Do not add a shot to satisfy an illustration quota. Use a real
  screencast capture for the thumbnail when available, otherwise a text-only thumb.
- The illustration quota, chapter-specific places and storytelling register below apply only
  to illustrated storytelling, not this teaching route. Its existing plain-slides QA still
  limits a state to 15 seconds; aim for meaningful reveals every 5 to 8 seconds without hiding
  the step before a beginner can read it. The eight-minute minimum, CC, facts, pronunciation,
  audio review and final QA remain unchanged; no repetition or silence to fill the runtime.
- A documentation screenshot proves what the page says, not that an installation or test ran.
  Record the input, action, expected result, observed result and evidence for each demonstration
  in 示範或實算 and claims.md. If no run evidence is supplied, label the result as expected and
  the walkthrough as untested; never invent a successful run or a first-person test. Terminal
  output must be copied from a real run with its date and tool version. Keep official-page
  captures public: no login, OBS, secrets or private account screens.
- Untested labels are honest disclosure, not completion of a practical learning promise.
  If evidence for the core demonstration is missing, record that teaching gap for revision;
  do not call the tutorial ready because its length, layout or technical checks pass. Before
  production, an independent first-use review must establish whether the provided materials
  let the intended viewer reproduce, explain, diagnose and adapt the example. A read-only
  script review does not establish successful execution; never invent learner validation.
- A listener preserves the chosen route and all scene/line ids. Report missing steps, unclear
  mappings, weak viewer benefit, missing contrasts/exercises or absent run evidence for a
  writer revision; never repair them by inventing facts,
  adding scenes or claiming a result. Leave "pause_after_ms" out; the tool still sets the beats.
`.trim();

export const REGISTER_RULES = `
The narration is TOLD, not explained (the storytelling register, docs/videos/ILLUSTRATED.md):
- The first sentence is a counter-intuitive claim or the viewer's own question; the hook has landed
  within ${HOOK_SECONDS} seconds. No greeting, no 「今天要來跟大家分享」, no table of contents.
- The first chapter turns at least once on 「${TWIST_MARKER}…其實…」: what the viewer believes, then
  what is so, with the fact that shows it. Later chapters may turn the same way when they have a
  real reversal; never fake one.
- Every chapter's LAST sentence is the question the next chapter answers (「那它到底怎麼做到的？」);
  the last chapter's last sentence answers the opening question instead. Never 「接下來我們來看」.
- Every chapter has at least one concrete scene or comparison a viewer can picture (a kitchen at 2 am,
  a queue at a counter, 「等於一杯咖啡的錢」), and the pictures ("shot" scenes) draw those scenes.
- Sentences alternate long and short; a reveal is a short sentence. Numbers arrive one at a time,
  each with what it means in the viewer's day.
- The pauses are the tool's: it sets "pause_after_ms" from the text after you answer
  (${PAUSE_BEATS.hook} after the cold open's first sentence, ${PAUSE_BEATS.reveal} on the sentence before
  「其實」, ${PAUSE_BEATS.cliffhanger} on a chapter's closing question) and clears it everywhere else. Leave
  "pause_after_ms" out; the beats land where the words put them.
- Facts stay facts: the register changes wording, order and rhythm, never a number, a name, a
  version or who said what; every claim still rests on "sources".
`.trim();

/** The Gemini `voice.style` the owner pastes on the settings tab for this register (≤ 400 characters). */
export const STORY_VOICE_STYLE =
  `${CHANNEL_ACCENT}。說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。`;

const QUESTION = /[？?]\s*$/;
const GREETING = /大家好|今天(要|來)?跟大家|歡迎(回到|來到)|接下來我們來看/;
/** The word the register's reveal turns on (「你以為…其實…」). */
const REVEAL_MARKER = "其實";

/** The script's chapters as scene ranges: the first scene opens one, and so does every scene with a "chapter". */
function chaptersOf(doc) {
  const scenes = doc.scenes ?? [];
  const chapters = [];
  for (const [index, scene] of scenes.entries()) {
    if (!scene?.chapter && index !== 0) continue;
    if (chapters.length) chapters.at(-1).end = index;
    chapters.push({ start: index, end: scenes.length, name: scene?.chapter ?? null });
  }
  return chapters;
}

/**
 * The last line of every chapter but the last (the last chapter answers the opening question
 * instead of asking the next one), or null for a chapter without a line.
 */
function closingLines(doc, chapters) {
  const scenes = doc.scenes ?? [];
  return chapters.slice(0, -1).map((chapter) => {
    for (let index = chapter.end - 1; index >= chapter.start; index--) {
      const own = Array.isArray(scenes[index]?.lines) ? scenes[index].lines : [];
      if (own.length) return own.at(-1);
    }
    return null;
  });
}

/**
 * Set the register's pause beats from the text, in place, and return the script: PAUSE_BEATS.hook
 * after the first spoken line (the cold open's first sentence), PAUSE_BEATS.reveal on the line
 * before every line that says 「其實」, PAUSE_BEATS.cliffhanger on a chapter's last line when it is
 * a question (the chapters and closers registerSummary counts). A line on two beats keeps the
 * longer pause. One line is one spoken sentence (script-writing.md), so "the sentence before"
 * is the line before, across scene boundaries.
 *
 * Every other "pause_after_ms" is cleared first, a model's included: the rule says the beats sit
 * there and nowhere else, so the tool owns the field on a register script. The model no longer
 * sets it (REGISTER_RULES tells it to leave the field out), a stray value from an older prompt or
 * a model that ignored the rule does not survive a save, and running this twice changes nothing.
 */
export function setPauseBeats(doc) {
  if (!Array.isArray(doc?.scenes)) return doc;
  // A draft lint has yet to see may hold a scene without lines or a line that is not an object.
  const lines = doc.scenes.flatMap((scene) => (Array.isArray(scene?.lines) ? scene.lines : [])).filter((line) => line && typeof line === "object");
  const said = (line) => String(spokenText(line) ?? "");
  const beats = new Map();
  const beat = (line, ms) => {
    if (line) beats.set(line, Math.max(beats.get(line) ?? 0, ms));
  };
  beat(lines[0], PAUSE_BEATS.hook);
  for (const [index, line] of lines.entries()) {
    if (index > 0 && said(line).includes(REVEAL_MARKER)) beat(lines[index - 1], PAUSE_BEATS.reveal);
  }
  for (const line of closingLines(doc, chaptersOf(doc))) {
    if (line && typeof line === "object" && QUESTION.test(said(line))) beat(line, PAUSE_BEATS.cliffhanger);
  }
  for (const line of lines) {
    if (beats.has(line)) line.pause_after_ms = beats.get(line);
    else delete line.pause_after_ms;
  }
  return doc;
}

/**
 * How far a script keeps the register, from its text alone (no timeline): the count of
 * 「你以為」 turns, how many chapters close on a question, whether the opener is a question or
 * a claim rather than a greeting, and the pause beats set. `restyle --dry-run` prints it and
 * the tests read it; it judges nothing, the listener does.
 */
export function registerSummary(doc) {
  const lines = [...eachLine(doc)].map(({ line }) => spokenText(line));
  const chapters = chaptersOf(doc);
  const closers = closingLines(doc, chapters).map((line) => (line ? spokenText(line) : ""));
  return {
    lines: lines.length,
    twists: lines.filter((text) => text.includes(TWIST_MARKER)).length,
    chapters: chapters.length,
    chapter_questions: closers.filter((text) => QUESTION.test(text)).length,
    opener_is_greeting: GREETING.test(lines[0] ?? ""),
    pauses: [...eachLine(doc)].filter(({ line }) => Number.isInteger(line.pause_after_ms) && line.pause_after_ms > 0).length,
  };
}

/** The summary as one line for the terminal. */
export function registerLine(summary) {
  const closers = Math.max(summary.chapters - 1, 0);
  return `${summary.lines} lines, ${summary.twists} 「${TWIST_MARKER}」 turn${summary.twists === 1 ? "" : "s"}, ${summary.chapter_questions} of ${closers} chapter${closers === 1 ? "" : "s"} closing on a question, ${summary.pauses} pause beat${summary.pauses === 1 ? "" : "s"}${summary.opener_is_greeting ? "; the opener greets instead of hooking" : ""}`;
}
