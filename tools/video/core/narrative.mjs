// The storytelling shape of a narrated video's script (script-writing.md §故事主線與鉤子). The owner
// (2026-10-13) rated the remastered videos' content 50 of 100: it "feels patchwork, the opening
// condensation included", a viewer cannot follow it, and it should be told like one story with
// hooks placed now and then. What can be read off the script and its estimated timeline is here,
// as lint problems for the writer; what only a reader can judge is the blind yes-or-no panel
// (NARRATIVE_PANEL) the worker asks after the listener's edit, and sends back to the writer.
import { createHash } from "node:crypto";
import { isDrama, isExplainer } from "./drama.mjs";
import { eachLine } from "./schema.mjs";
import { scriptCheckBinding, scriptCheckMatches } from "./script-check.mjs";
import { isStory } from "./story.mjs";
import { chapterList, estimateTimeline, formatClock, frameToSeconds } from "./timeline.mjs";

/** Where a video's panel verdict is kept, under its work directory. */
export const NARRATIVE_REVIEW = ["review", "narrative.json"];

/** The body carries an open loop at least this often: a question left hanging, a forward hook, an escalation or a chapter turn. */
export const HOOK_GAP_SECONDS = 90;
// After its one scene the condensation teases this many later moments, each a loop it plants
// (owner, 2026-10-13: the opening needs many hooks that make the viewer want the whole video).
export const OPENING_TEASERS = 3;
/** How many loops a ten-minute narrated video plants (its "loops" table), at least two whatever its length. */
export const LOOPS_PER_10_MINUTES = 3;

/**
 * A chapter that opens on a label instead of on the event: the sentence says what the chapter
 * will do (「先講大家聽過的版本」「打開檔案的第一頁」「回到清單上」「最後一頁的線索」「接下來」), which is
 * what made the owner's videos read as sections stitched together.
 */
export const LABEL_OPENERS = [
  /^(?:先|首先)(?:講|說|從|來|看|聊)/,
  /^回到/,
  /^(?:打開|翻開)(?:第[一二三四五六七八九十\d]+頁|檔案|下一頁)/,
  /^這一?(?:章|段|集)(?:要|就)?(?:回答|講|說|來)/,
  /^接下來/,
  /^(?:我們|現在|這裡)(?:來|先|就)(?:看|講|說|聊|回到)/,
  /^第[一二三四五六七八九十\d]+(?:頁|章|段|部分|個原因|條|份)/,
  /^最後一頁/,
  /^(?:再來|然後)(?:是|看|講|說)/,
  /^下一(?:章|段|頁|份)/,
];

/** The open-loop devices read off the words: a forward hook and an escalation (a question is read from its mark). */
export const OPEN_LOOP_FAMILY = Object.freeze({
  forward: /等一下|等等會|先記住|先記著|之後(?:會|再)|晚一點|後面(?:會|再)|最後再|待會/,
  escalation: /但這還不是|還不是最|更怪的是|更離奇|更麻煩的是|問題來了|結果(?:呢|，|：)|沒想到|偏偏|奇怪的是|怪就怪在/,
});
const QUESTION = /[？?]\s*$/;
/** A sentence that brings a fact back on purpose: not a repeat. */
export const CALLBACK = /還記得|記得嗎|剛剛|剛才|前面|開頭|一開始|回到那/;
/** What the close must not say (the owner, 2026-10-13): what the next video is about. */
export const NEXT_VIDEO = /下一集|下一支|下一份檔案|下一部|下部影片|下次我們|下一期|下一題|下一個故事|下一個名詞|下集/;

/**
 * Whether the script is a narrated video the storytelling rules read: a slides video of any
 * route, an explainer (a drama with no cast in an explainer preset) or a brand story. A drama
 * with a cast keeps its craft spec, and a compilation narrates nothing.
 */
export const isNarrated = (doc, series = null) => !isDrama(doc) || isExplainer(doc) || isStory(series);

/** How many loops a script of `minutes` plants at least. */
export const requiredLoops = (minutes) => Math.max(2, Math.round((minutes / 10) * LOOPS_PER_10_MINUTES));

const lineStarts = (timeline) => new Map((timeline?.lines ?? []).map((line) => [line.id, line.start_frame]));
const sceneStart = (timeline, id) => (timeline?.scenes ?? []).find((scene) => scene.id === id)?.start_frame ?? null;

/**
 * The script as the panel and a reader see it: the title, then each chapter as 「## name（start）」
 * and one spoken sentence a line as 「[id start] text」, nothing else (no emotions, no prompts, no
 * cards, no ids of scenes). The ids let a verdict quote its evidence by line.
 */
export function narrationText(doc, timeline) {
  const opens = new Map(chapterList(timeline).map((chapter) => [chapter.scene, chapter]));
  const starts = lineStarts(timeline);
  const out = [`# ${doc.youtube?.title ?? doc.slug ?? ""}`];
  for (const scene of doc.scenes ?? []) {
    const chapter = opens.get(scene.id);
    if (chapter) out.push("", `## ${chapter.title}（${formatClock(chapter.start)}）`);
    for (const line of scene.lines ?? []) {
      const at = starts.has(line.id) ? ` ${formatClock(frameToSeconds(starts.get(line.id)))}` : "";
      out.push(`[${line.id}${at}] ${line.text}`);
    }
  }
  return `${out.join("\n")}\n`;
}

/** The first spoken line of the scenes from `from` (inclusive) to `to` (exclusive), with its label. */
function firstLine(doc, from, to) {
  for (const entry of eachLine(doc)) {
    if (entry.sceneIndex < from) continue;
    if (entry.sceneIndex >= to) return null;
    return entry;
  }
  return null;
}

/** A chapter after the first whose first sentence is a label (LABEL_OPENERS): warnings for the writer. */
export function chapterOpenerProblems(doc, timeline) {
  const problems = [];
  const chapters = chapterList(timeline);
  const index = new Map((doc.scenes ?? []).map((scene, position) => [scene.id, position]));
  chapters.slice(1).forEach((chapter, position) => {
    const from = index.get(chapter.scene);
    if (from === undefined) return;
    const next = chapters[position + 2];
    const to = next ? (index.get(next.scene) ?? doc.scenes.length) : doc.scenes.length;
    const first = firstLine(doc, from, to);
    if (!first || first.scene.template === "outro") return;
    const text = first.line.text.replace(/^[「『]/, "");
    if (!LABEL_OPENERS.some((pattern) => pattern.test(text))) return;
    problems.push({ path: first.label, message: `the chapter 「${chapter.title}」 opens on a label (「${text.slice(0, 14)}…」): open on the event itself, the consequence of what came before, or its answer; the label is what stitches sections instead of telling a story (script-writing.md §故事主線與鉤子)` });
  });
  return problems;
}

/**
 * The body (after the condensation, before the outro) read for open loops: a chapter turn, a
 * sentence that ends on a question, a forward hook or an escalation (OPEN_LOOP_FAMILY). A stretch
 * longer than HOOK_GAP_SECONDS without one is a warning naming its minutes.
 */
export function hookCadenceProblems(doc, timeline) {
  const chapters = chapterList(timeline);
  if (chapters.length < 2 || !timeline?.total_frames) return [];
  const starts = lineStarts(timeline);
  const total = frameToSeconds(timeline.total_frames);
  const outro = (doc.scenes ?? []).find((scene) => scene.template === "outro");
  const outroAt = outro ? sceneStart(timeline, outro.id) : null;
  const from = chapters[1].start;
  const to = outroAt === null ? total : frameToSeconds(outroAt);
  if (to - from <= HOOK_GAP_SECONDS) return [];
  const devices = chapters.slice(1).map((chapter) => chapter.start).filter((at) => at >= from && at < to);
  for (const { line } of eachLine(doc)) {
    const frame = starts.get(line.id);
    if (frame === undefined) continue;
    const at = frameToSeconds(frame);
    if (at < from || at >= to) continue;
    if (QUESTION.test(line.text) || Object.values(OPEN_LOOP_FAMILY).some((pattern) => pattern.test(line.text))) devices.push(at);
  }
  const points = [from, ...devices.sort((a, b) => a - b), to];
  const problems = [];
  for (let index = 1; index < points.length; index++) {
    const gap = points[index] - points[index - 1];
    if (gap <= HOOK_GAP_SECONDS) continue;
    problems.push({ path: "scenes", message: `no open loop between ${formatClock(points[index - 1])} and ${formatClock(points[index])} (${Math.round(gap)} s): no forward hook (等一下／先記住／之後會), no escalation (但這還不是／更怪的是／問題來了), no question and no chapter turn; plant one at least every ${HOOK_GAP_SECONDS} s (script-writing.md §故事主線與鉤子)` });
  }
  return problems;
}

/**
 * The script's "loops" table (schema.mjs validates its ids and their order): enough of them for
 * the length, one planted in the condensation, none planted in the outro.
 */
export function loopProblems(doc, timeline, minutes) {
  const problems = [];
  const loops = Array.isArray(doc.loops) ? doc.loops : [];
  const required = requiredLoops(minutes);
  if (loops.length < required) problems.push({ path: "loops", message: `${loops.length} open loop${loops.length === 1 ? "" : "s"} planted; a narrated video of about ${Math.round(minutes)} minutes plants at least ${required}: "loops" lists each as the line that plants it ("setup"), the line that pays it off ("payoff") and what it holds back ("what"), so every hook is answered (script-writing.md §故事主線與鉤子)` });
  if (!loops.length) return problems;
  const chapters = chapterList(timeline);
  const starts = lineStarts(timeline);
  const bodyStart = chapters[1]?.start ?? Infinity;
  const planted = (loop) => {
    const frame = starts.get(loop.setup);
    return frame !== undefined && frameToSeconds(frame) < bodyStart;
  };
  const teasers = loops.filter(planted).length;
  if (chapters.length > 1 && !teasers) problems.push({ path: "loops", message: "the condensation plants no loop: at least one setup line sits in the first chapter, paid off in a later one" });
  else if (chapters.length > 1 && teasers < OPENING_TEASERS) problems.push({ path: "loops", message: `the condensation plants ${teasers} loop${teasers === 1 ? "" : "s"}; after its one scene it teases at least ${OPENING_TEASERS} later moments, each cut off before its result and paid off where the body reaches it (script-writing.md §開場濃縮)` });
  const outro = (doc.scenes ?? []).find((scene) => scene.template === "outro");
  const closing = new Set((outro?.lines ?? []).map((line) => line.id));
  loops.forEach((loop, index) => {
    if (closing.has(loop.setup)) problems.push({ path: `loops[${index}]`, message: `the setup of 「${loop.what}」 sits in the outro; nothing after it can pay it off` });
  });
  return problems;
}

const ARABIC = /\d+(?:[.,]\d+)*/g;
const CJK_NUMBER = /[〇零一二兩三四五六七八九十百千萬億兆]{2,}(?:桶|年|月|日|天|次|元|塊|公尺|公里|公斤|公噸|倍|分|秒|度|人|家|間|台|條|頁|個|隻|件|歲|艘|封)?/g;
const REPEATS_SHOWN = 6;

/**
 * A number said in more than two sentences (the 1,701 casks of the owner's example came round
 * five times): a fact is told once and brought back by a callback (CALLBACK), which is not counted.
 */
export function repeatedFactProblems(doc) {
  const where = new Map();
  for (const { line } of eachLine(doc)) {
    const text = String(line.text ?? "");
    if (CALLBACK.test(text)) continue;
    const keys = new Set();
    for (const match of text.match(ARABIC) ?? []) {
      if (match.replace(/[.,]/g, "").length >= 2) keys.add(match.replace(/,/g, ""));
    }
    for (const match of text.match(CJK_NUMBER) ?? []) keys.add(match);
    for (const key of keys) {
      if (!where.has(key)) where.set(key, []);
      where.get(key).push(line.id);
    }
  }
  const problems = [];
  for (const [key, ids] of where) {
    if (ids.length <= 2) continue;
    problems.push({ path: "scenes", message: `「${key}」 is said in ${ids.length} lines (${ids.join(", ")}): a fact is told once, and brought back only by a callback (「還記得那…」「剛剛那…」) (script-writing.md §故事主線與鉤子)` });
  }
  return problems.slice(0, REPEATS_SHOWN);
}

/**
 * The close names the next video (「下一份檔案是五十一區」「下一支拆它的價格表」): an error, since the
 * owner decided the outro says nothing about the next video. Read on the outro card's words and
 * lines and on the last three sentences of the script, wherever they sit.
 */
export function outroNextVideoProblems(doc) {
  const said = [];
  (doc.scenes ?? []).forEach((scene, index) => {
    if (scene.template !== "outro") return;
    const where = `scenes[${index}] (${scene.id})`;
    for (const field of ["title", "cta", "kicker", "sub"]) {
      if (typeof scene.data?.[field] === "string") said.push({ key: `${scene.id}.${field}`, path: `${where}.data.${field}`, text: scene.data[field] });
    }
    (scene.lines ?? []).forEach((line, position) => said.push({ key: line.id, path: `${where}.lines[${position}] (${line.id})`, text: line.text }));
  });
  for (const entry of [...eachLine(doc)].slice(-3)) said.push({ key: entry.line.id, path: entry.label, text: entry.line.text });
  const seen = new Set();
  const problems = [];
  for (const { key, path, text } of said) {
    const hit = NEXT_VIDEO.exec(String(text ?? ""));
    if (!hit || seen.has(key)) continue;
    seen.add(key);
    problems.push({ path, message: `the close names the next video (「${hit[0]}」): the outro's three sentences are the answer with its number, one comment question and one invitation to subscribe with a reason, never what the next video is about (owner, 2026-10-13; script-writing.md §結尾)` });
  }
  return problems;
}

/** Every storytelling problem of a narrated script, tagged "narrative" so the worker can hand the warnings to the writer. */
export function narrativeProblems(doc, timeline, { minutes } = {}) {
  const tag = (problems) => problems.map((problem) => ({ ...problem, kind: "narrative" }));
  const length = Number.isFinite(minutes) ? minutes : frameToSeconds(timeline?.total_frames ?? 0) / 60;
  return {
    errors: tag(outroNextVideoProblems(doc)),
    warnings: tag([...chapterOpenerProblems(doc, timeline), ...hookCadenceProblems(doc, timeline), ...loopProblems(doc, timeline, length), ...repeatedFactProblems(doc)]),
  };
}

// ---------------------------------------------------------------------------------------------
// The blind panel: what only a reader can judge, as yes-or-no questions (the keyframe and
// tutorial judges taught that only yes-or-no questions tell a good script from a bad one; a
// scale pins at the same number for both).

/**
 * The questions, in zh-TW; a "required" one that is not met sends the script back to the writer.
 * one_thread and no_detour came on 2026-10-15, after three AI videos changed example and metaphor
 * from chapter to chapter, went off on detours and read lists out (script-writing.md §故事主線與鉤子).
 */
export const NARRATIVE_PANEL = Object.freeze([
  { id: "scene_first", required: true, question: "前四句（約 15 秒）是否已經在一個具體的時刻裡：有年份或地點，有人（或一艘船、一份文件）在做一件事，而不是在介紹主題、打招呼或預告？" },
  { id: "no_spoiler", required: true, question: "開場（第一章）是否沒有講掉任何後面章節才揭曉的結果：化驗或調查的結果、最後的答案、結局？（開場預告後面的時刻是第 11 題要的：只要停在結果之前，就不算講掉。）" },
  { id: "one_line", required: true, question: "全片是否只有一條故事線，照事情發生或被查出來的順序往前走，沒有回頭把同一段再講一次？" },
  { id: "no_toc", required: true, question: "是否沒有任何一句在宣告「接下來要怎麼講」：接下來、先講、這一章回答、第一…第二…、回到清單、打開第一頁，或把後面的內容排成清單（排成一張表、前四個、剩下的兩個、還沒解釋的是這四件事）？（「先記住這個數字，等一下它會回來」是第 6 題要的前向鉤子，它講的是故事裡的一件事會回來，不是在講這支片的結構，不算宣告。）" },
  { id: "chapters_link", required: true, question: "每一章第一句是否接住上一章留下的具體疑問、動作或物件，讓事情往前走？預告式開場之後可以回到更早的故事起點，但第一句要讓觀眾聽懂它從哪裡接上開場的問題；其餘章首應是上一章的後果或答案。標籤、總結、重述剛問過的話，以及沒有來源支持卻硬說兩件事有因果，都不算銜接；隔了幾分鐘的掛鉤才需要點名回呼。" },
  { id: "open_loops", required: true, question: "正文是否每 90 秒內至少有一個掛著沒回答的問題：前向（等一下會回來）、升級（但這還不是最怪的）、收著不講原因、或轉折？" },
  { id: "payoffs", required: true, question: "每一個掛著的問題後來是否都有清楚的新答案？緊鄰的問答可以直接回答，不必再用「還記得」點名；隔了幾分鐘才回收的問題，須點名原先具體的人、物或疑問，再給出新的事實或結果。只重複問題、換句話說，或回答另一件事，都不算回收。" },
  { id: "no_recap", required: true, question: "同一個數字或事實是否沒有講超過一次（用「還記得」「剛剛那」點名的回呼除外；開場預告過的時刻，正文講到時點名接回來，也不算）？" },
  { id: "chapters_are_events", required: false, question: "章名是不是「發生了什麼」（一件事或一個揭曉），而不是功能（背景、流傳的版本、檔案裡有什麼、結論）？" },
  { id: "outro_no_next", required: true, question: "片尾是否沒有提到下一支影片、下一集或下一份檔案？" },
  { id: "opening_hooks", required: true, question: "開場（第一章）在第一個場景之後，是否還丟出至少三個後面才會揭曉的時刻（一件具體的事停在結果之前，或一個問題），讓人想把整支片看完？（「接下來我們會看到」這種宣告不算時刻。）" },
  { id: "one_thread", required: true, question: "是否有一個可辨認的主角或具體難題，從開場一路帶到結尾，每一章都讓它往前走？主角可以是一個人、團隊、物件或專案；跨年代的產品故事可以追同一個使用難題，但要逐步說出上一種用法留下什麼困難、下一個做法如何回應。只因同屬一類商品就連續換例子，不算同一條線；也不能沒有來源就聲稱不同發明者彼此承襲或互相啟發。" },
  { id: "no_detour", required: true, question: "是否沒有岔出去的段落：每一段都在推進開場那個問題，沒有整段在講跟它無關的事，也沒有一口氣念出產品、分數或誰說了什麼的清單？" },
]);

/** What the panel's reader is told, and nothing else: no brief, no sources, no standing instructions (the stage sends it bare). */
export const PANEL_INSTRUCTIONS = `
You are a blind reader of ONE zh-TW (Traditional Chinese, Taiwan) YouTube narration script. You
have not seen its brief, its sources, its pictures or any rule but these, and you must not guess
at them: "narration" is the whole script, chapter by chapter ("## chapter name（start）"), one
spoken sentence a line, each with its line id and start time in brackets, and that is all you
judge. The owner wants a video told as ONE story with hooks placed now and then, not as sections
stitched together: "questions" are the yes-or-no checks of that, in zh-TW, each with an "id".
Read the whole script once, then answer every question. "yes" means the script fully meets the
check; one sentence that breaks it makes the answer "no"; when you are not sure, the answer is
"no". Give one quoted line, with its line id, as evidence: for a "no", the line that breaks the
check; for a "yes", the line that shows it best. Answer with ONE JSON object and nothing else (no
Markdown fence): {"answers": [{"id": "<question id>", "yes": true|false, "evidence": "[<line id>]
<the quoted line>"}]}, one entry per question, in the questions' order.
`.trim();

// This is only the blind narrative panel's contract. A script may be unchanged while its
// questions or required-answer rules change; other script/fact-check receipts remain valid.
// Increment verdict_version if panelVerdict's PASS semantics change without a text change.
export const PANEL_RULES_SHA256 = createHash("sha256").update(JSON.stringify({
  instructions: PANEL_INSTRUCTIONS,
  questions: NARRATIVE_PANEL.map(({ id, question, required }) => ({ id, question, required })),
  verdict_version: 1,
})).digest("hex");

// Bind the exact rendered narration sent to the blind panel. The shared script check omits
// metadata such as the title, even though the panel reads it above every chapter.
function panelNarrationSha256(doc) {
  return createHash("sha256").update(narrationText(doc, estimateTimeline(doc))).digest("hex");
}

export function narrativeReviewMatches(check, doc) {
  return Boolean(check?.panel_rules_sha256 === PANEL_RULES_SHA256
    && scriptCheckMatches(check, doc)
    && check.panel_narration_sha256 === panelNarrationSha256(doc));
}

/** The panel's payload: the script as text and the questions, nothing a reader could lean on. */
export function panelPayload(doc, timeline) {
  return { narration: narrationText(doc, timeline), questions: NARRATIVE_PANEL.map(({ id, question }) => ({ id, question })) };
}

const isObject = (value) => value !== null && typeof value === "object" && !Array.isArray(value);

/**
 * The panel's answer read: every required question answered "yes" passes; a question left out,
 * answered otherwise or malformed is a "no" (as the checker's missing verdict is a problem in
 * series.mjs scriptVerdict). `problems` are the lines the writer is sent.
 */
/** A line id in brackets, as the panel's own answer format prints it: `[mc1a] …`. */
const EVIDENCE_LINE_ID = /\[[A-Za-z0-9_-]{2,}\]/;

export function panelVerdict(answer) {
  const given = new Map();
  for (const entry of Array.isArray(answer?.answers) ? answer.answers : []) {
    if (isObject(entry) && typeof entry.id === "string") given.set(entry.id, entry);
  }
  const answers = NARRATIVE_PANEL.map(({ id, question, required }) => {
    const entry = given.get(id);
    const quoted = typeof entry?.evidence === "string" && entry.evidence.trim() ? entry.evidence.trim().slice(0, 200) : null;
    // A "yes" has to be auditable: the question asks for one line of the narration quoted with its
    // id in brackets, so a yes with nothing quoted is a malformed answer, not an approval. Without
    // this a truncated or lazy reply ("yes" ten times) would pass a script with no basis at all.
    const cited = Boolean(quoted) && EVIDENCE_LINE_ID.test(quoted);
    const yes = entry?.yes === true && cited;
    const evidence = cited ? quoted : quoted ? `no line id quoted: ${quoted}` : entry ? "no evidence quoted" : "no answer";
    return { id, question, required, yes, evidence };
  });
  const failed = answers.filter((each) => each.required && !each.yes);
  const advisory = answers.filter((each) => !each.required && !each.yes);
  return {
    passed: failed.length === 0,
    answers,
    failed,
    advisory,
    problems: failed.map((each) => `${each.id}：${each.question}（${each.evidence}）`),
  };
}

/**
 * The verdict as it is kept (NARRATIVE_REVIEW), bound to both the script and the blind panel
 * contract. A later edit or rule change makes it stale, without changing other script checks.
 */
export function narrativeRecord(doc, verdict, round) {
  return {
    ...scriptCheckBinding(doc),
    panel_rules_sha256: PANEL_RULES_SHA256,
    panel_narration_sha256: panelNarrationSha256(doc),
    round,
    passed: verdict.passed,
    answers: verdict.answers,
    failed: verdict.failed.map((each) => each.id),
    advisory: verdict.advisory.map((each) => each.id),
  };
}
