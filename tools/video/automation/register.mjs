// The storytelling register of an illustrated slides video (docs/videos/ILLUSTRATED.md §說書式旁白),
// decided 2026-09-29: the owner found the tutorials stiff and wants them told the way 黑貓研究院
// tells a business story. One text carries the rules to the planner, the writer and the
// listener (prompts.mjs adds it to their instructions), and the owner can paste the same text
// as a standing instruction on /admin/videos while an older worker runs. The voice style is a
// setting, not a prompt: `settle()` copies the settings tab's `voice` into every new video, and
// STORY_VOICE_STYLE is the text the owner pastes there (it sits in speechHash, so changing it
// records every line again).
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

export const REGISTER_RULES = `
The narration is TOLD, not explained (the storytelling register, docs/videos/ILLUSTRATED.md):
- The first sentence is a counter-intuitive claim or the viewer's own question; the hook has landed
  within ${HOOK_SECONDS} seconds. No greeting, no 「今天要來跟大家分享」, no table of contents.
- The first chapter turns at least once on 「${TWIST_MARKER}…其實…」: what the viewer believes, then
  what is so, with the fact that shows it. Later chapters may turn the same way when they have a
  real reversal; never fake one.
- Every chapter's LAST sentence is the question the next chapter answers (「那它到底怎麼做到的？」);
  the last chapter's last sentence answers the opening question instead. Never 「接下來我們來看」.
- Every chapter has at least one concrete scene or comparison a viewer can picture (a desk at 2 am,
  a queue at a counter, 「等於一杯咖啡的錢」), and the pictures ("shot" scenes) draw those scenes.
- Sentences alternate long and short; a reveal is a short sentence. Numbers arrive one at a time,
  each with what it means in the viewer's day.
- Beats as pauses ("pause_after_ms"): ${PAUSE_BEATS.hook} after the cold open's first sentence,
  ${PAUSE_BEATS.reveal} on the sentence before 「其實」, ${PAUSE_BEATS.cliffhanger} on a chapter's closing
  question. Nowhere else, and never over 5000.
- Facts stay facts: the register changes wording, order and rhythm, never a number, a name, a
  version or who said what; every claim still rests on "sources".
`.trim();

/** The Gemini `voice.style` the owner pastes on the settings tab for this register (≤ 400 characters). */
export const STORY_VOICE_STYLE =
  "台灣國語說書人，像在跟朋友講一個等不及要分享的故事。有起伏、有戲：揭曉前刻意停一拍，問句上揚，「你以為」放慢放輕，「其實」亮起來。關鍵數字放慢，清單段落加快。絕不平、絕不像在念稿。";

const QUESTION = /[？?]\s*$/;
const GREETING = /大家好|今天(要|來)?跟大家|歡迎(回到|來到)|接下來我們來看/;

/**
 * How far a script keeps the register, from its text alone (no timeline): the count of
 * 「你以為」 turns, how many chapters close on a question, whether the opener is a question or
 * a claim rather than a greeting, and the pause beats set. `restyle --dry-run` prints it and
 * the tests read it; it judges nothing, the listener does.
 */
export function registerSummary(doc) {
  const scenes = doc.scenes ?? [];
  const lines = [...eachLine(doc)].map(({ line }) => spokenText(line));
  const chapters = [];
  for (const [index, scene] of scenes.entries()) {
    if (!scene.chapter && index !== 0) continue;
    if (chapters.length) chapters.at(-1).end = index;
    chapters.push({ start: index, end: scenes.length, name: scene.chapter ?? null });
  }
  const lastLineOf = (chapter) => {
    for (let index = chapter.end - 1; index >= chapter.start; index--) {
      const own = scenes[index].lines ?? [];
      if (own.length) return spokenText(own.at(-1));
    }
    return "";
  };
  const closers = chapters.slice(0, -1).map(lastLineOf);
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
