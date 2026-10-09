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

// What a slides video has to be worth to its viewer, whichever route it takes. The owner's review
// of 2026-10-09 set it: a reference tutorial covered our whole nine-minute video in fifteen
// seconds and spent the rest teaching, while a quarter of our sentences named where a fact came
// from. Sent to the planner, the writer and the listener of a slides video, after the teaching
// route and before the register; not sent to drama, story, explainer or translation stages.
// Its first use (docs/videos/claude-code-mods-hands-on, the same day) found 21 places where a
// planner and a writer had to guess; the evidence levels, the limits of the risk cap, what to
// do when real text does not fit a card and where a card names its source answer those.
export const VALUE_RULES = `
Content value (every slides video, teaching cards and illustrated storytelling alike; where these
rules and a route's rules disagree, these win):
- The route follows the subject. When the subject is something the viewer operates (a tool, a
  feature, a setting, a command, a prompting technique, a workflow), the video is a tutorial and
  takes the teaching route. The illustrated route is for a subject with nothing to operate (a
  company's decision, a market, a history), and its outcomes are the judgments the viewer can
  make afterwards.
- 觀眾看完能做到的事 holds two to four things the viewer could not do before this video and can
  do after it, each written as the action, the thing acted on and how the viewer knows it
  worked. These are not outcomes: something the viewer could look up and read off in one line
  (a version, a price, a menu), a caution on its own (be careful, think first, ask before
  installing), or 「了解」「認識」「知道」 something. Running a command and judging its output
  against what was asked is an outcome: the judging is the skill. When the sources carry fewer
  than two real outcomes, the planner takes another topic from "topics", or says so on the
  brief's first line (「含金量不足：<what is missing>」); it does not pad.
- Evidence has three levels, and each outcome names the highest it has. SEEN: observed in the
  product's own interface. RUN: a real run recorded with its input, action, result, date and
  tool version (a command, a test, a headless session). CITED: an official example with its
  page, or a worked calculation. An outcome with none of the three is dropped, not softened.
  The script never shows or tells a lower level as a higher one, and 示範或實算 lists as
  「要先實作：…」 each thing a higher level would need: no run at all, or run but never seen
  where there is something to see (a command and its output have nothing more to see). A
  run counts once it is in the video's run log with its command, output, date and tool
  version, whoever made it. When the plan comes before the runs, an outcome names the level
  its listed run will give and stands until the runs are made; they are made and recorded
  before the outline is chosen, and an outcome whose run failed or was not made is dropped
  then.
  The result that opens the video is the strongest evidence there is, a test's output when
  nothing was seen. For something a model wrote on request, the proof is the artefact and the
  runs made on it; the request is shown as 「可以這樣說」 unless one logged run goes from that
  request to that artefact. A step that is not an outcome (keeping it, turning it off) may
  stand on CITED evidence, and its card says so.
- A warning about the subject itself (it is not sandboxed, it costs money, it can break) is one
  chapter at most, said once, with the one check that answers it. It is never the title, the
  hook or the angle, unless the subject itself is an incident. The cap does not cover what a
  tutorial owes its viewer anyway: a common failure and how to find it, what the video's own
  example does not catch, the exception in an update's fourth move, and a card's label of
  what was and was not run, which is repeated wherever it applies. The owner's own incident may open a tutorial as the reason for its
  example.
- Chapters follow the questions a viewer asks, in the order they ask them: what do I get (the
  result first, on screen), how is it different from what I already use, how do I do it, how
  do I know it worked, how do I keep it or undo it. Each chapter answers the question the one
  before it raised. The opening chapter is the result alone; the mechanism is the second
  chapter. Tutorials share this order; what must differ from an earlier video is the
  example, the opening and the sequence of cards. Name the tools the viewer already uses and give the rule for choosing between them
  in one sentence each (「一直重貼同一段指示，寫成 Skill」), and say plainly when the simpler
  tool is enough. When loading or installing grants access, the check that settles trust
  comes before it, wherever the loading step falls in that order. On the teaching route a
  second worked example is that route's contrast; the main example still carries the video.
- Every step the viewer is meant to repeat shows the exact thing to type or press, in full, on
  a code, chat, steps or terminal card: the command, the sentence to say to the model, the
  setting's name. The narration says what it does, not its characters. When real text does
  not fit a card (code: 64 characters a line, 9 lines beside a title and a caption and 12
  beside a caption alone; chat: 44 characters; terminal: 78 columns, no home directory):
  re-wrap the source file itself and run it again, so the card still shows the real file;
  or show a contiguous excerpt and name the whole file in the caption and the description.
  Real output that is too long or carries a home directory is excerpted in whole lines, in
  their order, or the run is made again from a folder whose path fits; it is never edited. A request longer than a
  chat bubble goes on a code card as plain text. Never alter a character. A real line too
  long for a terminal card, or a tool result read out of a session rather than printed by a
  terminal, goes on a quote, compare, steps or table card whose "source" names the run
  (「實跑 2026-10-09｜<tool and version>」); the events of one run in order are a steps
  card. One card holds one level of evidence: when its rows differ, split it, or name the
  odd row's level in that row or by its number in the source. A command too long for a
  terminal card goes on a code card when it fits as typed; otherwise its parts go in a
  table and the whole command in the description. An excerpt's caption gives the file and
  the line range it shows. A terminal card's tool_version names the program that printed
  the output. A source line takes the room of a row: a table or a list at its limit gives
  up its title or splits. A quote card holds one sentence of its source, or the clause that
  carries the fact. The render stage judges a full card: what it reports as overflowing is
  cut, not shrunk. A choice among alternatives is a table; steps draws a
  sequence.
- An update or a guide is told as numbered points, each in the same four moves: what the
  viewer did before, what changed, exactly what to do now, and the exception.
- Every sentence of narration carries a fact, a step, a reason, a result or a choice; the cta
  card's sentence and the outro's comment question and subscribe invitation are the three
  exceptions. Where a fact comes from is the card's own field and the description ("source"
  on a quote, stats, bullets, compare, steps or table card; the date and version on a
  terminal card; the caption of a code card or a screencast): the narration states the fact
  and never opens on its source (「文件寫」「文件說」「部落格說」「官方說」「官方表示」
  「根據官方」; lint counts the family). A number from an official page is said, and its card
  names the page and the day; a number from the video's own run, a limit in its own code or
  the owner's own incident is said as that, and its card names the run, the file or the date.
  「以官網為準」 is never the fallback: a number with neither source is left out. At most two
  sentences in a video set a scene or describe a picture; pointing at the card on screen
  (「亮起來的這一行」) is not one of them. A comparison is used once, where the mechanism is
  hard to see, and kept, never a new one per chapter. Pictures may still travel; the words do
  not follow them.
- The length comes from substance: a second worked example, a common failure and how to find
  it, a contrast, an exercise. Never from a chapter on something one line answers, from
  restating, or from scene-setting. When the material ends short of the minimum, add an
  example the sources carry or say so in the report; do not fill.
- A listener keeps these rules as well: it reports a sentence that carries nothing, a source
  spoken in the narration, a chapter one line would answer, or an outcome with no proof, for a
  writer revision; it never repairs one by inventing a fact, a run or an example.
`.trim();

// The words the audio check has misheard on this channel, each with the wording that passed
// (the table in script-writing.md §給 TTS 唸的稿子 also says what each was heard as). The check
// transcribes the synthesized voice and compares it with the script; two tutorials on
// 2026-10-09 had 13 and 19 of 151 lines flagged on their first check, and a line that was only
// recorded again was flagged again. Sent to the slides writer and listener.
export const MISHEARD_WORDS = [
  ["實跑", "實際跑過"],
  ["行程", "執行中的程式"],
  ["讀檔", "讀取檔案"],
  ["數什麼", "要數什麼"],
  ["擋呼叫的", "負責擋下呼叫的"],
  ["窗格", "畫面上的介面"],
  ["沒人接手", "沒有人替它處理"],
  ["界線", "原則"],
  ["餵假事件", "送假事件進去"],
  ["印出", "顯示的是"],
  ["放行", "讓它通過"],
  ["無介面", "不開畫面的"],
  ["那一欄", "這個欄位"],
  ["沒接的那次", "沒有接上的那一次"],
  ["測試是紅的", "測試沒有通過"],
];

export const HEARD_RULES = `
Words the audio check mishears (zh-TW narration): the check transcribes the synthesized voice
and compares it with the script, and a homophone is heard the same way when it is recorded
again, so it is the wording that changes. Write the form on the right from the start:
${MISHEARD_WORDS.map(([written, instead]) => `「${written}」→「${instead}」`).join("、")}.
What they share: a one-character verb, a two-character term, or a short sentence that starts
without its subject. Add a character or two, or use the commoner spoken word. Numbers,
Latin-script words and proper names stay exactly as written, and the facts do not change.
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
