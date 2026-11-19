// The opening review of 原來如此事務所, 奇聞檔案局 and the brand stories (owner, 2026-11-19: 「應該要前300秒
// 都不會滑走比較好，嚴格審核」, with several independent readers). Before any paid voice, three readers,
// each reading as a different viewer, read the first 300 seconds of the script with the thumbnail and
// the title beside it, and say where they would swipe away: by default three fresh subagents of the AI
// making the episode (--record), or the site's model (--ask). The script passes only when every one
// of them would stay all 300 seconds and names nothing to fix. The verdicts are bound to what the
// readers read (openingHash: the title, the thumbnail headline and every line that can start in the
// first 300 seconds, with its speaker): an edit there asks for a new round, an edit later does not.
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import path from "node:path";

import { isOpeningHookSeries } from "./narrative.mjs";
import { eachLine } from "./schema.mjs";
import { estimateTimeline, formatClock, frameToSeconds } from "./timeline.mjs";

/** Where the round's verdicts are kept, under the video's work directory. */
export const OPENING_REVIEW = ["review", "opening-review.json"];
/** Where the packet the readers read is written. */
export const OPENING_PACKET = ["review", "opening-packet.md"];
/** Which opening the voice on disk speaks (tts writes it), so a retake cannot carry a new opening. */
export const OPENING_VOICED = ["review", "opening-voiced.json"];
export const OPENING_REVIEW_SECONDS = 300;
export const OPENING_REVIEW_MIN_SCORE = 8.5;
/** Room for a reasoning model to finish its JSON answer. */
export const OPENING_REVIEW_MAX_TOKENS = 8_000;

/** The three viewers the readers read as; one reader each, every one must pass. */
export const OPENING_PERSONAS = Object.freeze({
  newcomer: "第一次點進這個頻道的路人：對這個題目沒有任何背景，只因為縮圖和標題點進來。你在找「這是什麼、為什麼值得看下去」，聽不懂或覺得跟縮圖無關就走。",
  scroller: "邊滑手機邊看的觀眾：耐心很少，任何一段拖、重複、繞遠路、像在念資料或念目錄，你就滑走。你在意每 30–45 秒有沒有讓你想知道下一句。",
  stickler: "挑剔的老觀眾：專抓不順和沒頭沒尾——人名、名詞、物件第一次出現有沒有先交代；句子和段落有沒有接上；有沒有突然跳到別的事、或說出前後接不起來的話；兩個人對話時回答有沒有接住剛被問的那句。",
});

/**
 * Whether a video must pass the opening review before its voice is made. `voiced`: the voice on disk
 * is already this script's (timeline.json's speech hash is current), so nothing new is paid for; a
 * retake (--redo, --refresh-evidence) of a voice made before is not asked either.
 */
export function needsOpeningReview(doc, { series = null, workdir = null, voiced = false, retake = false } = {}) {
  if (!isOpeningHookSeries(doc, series)) return false;
  // The host's worker holds its own scripts with the blind panel; this review is the gate of the
  // episodes a session makes by hand (no auto.json in the work directory).
  if (workdir && existsSync(path.join(workdir, "auto.json"))) return false;
  return !voiced && !retake;
}

const speakerName = (doc, id) => (doc.characters ?? []).find((character) => character.id === id)?.name ?? id;
const cleanHeadline = (doc) => String(doc.thumbnail?.data?.headline ?? "").replace(/\*\*/g, "").replace(/\n/g, " ");

/** What the readers read, in order: [time, speaker name or "", text] for every line under 300 s. */
export function openingLines(doc, timeline = estimateTimeline(doc)) {
  const starts = new Map((timeline.lines ?? []).map((line) => [line.id, line.start_frame]));
  const lines = [];
  for (const { line } of eachLine(doc)) {
    const frame = starts.get(line.id);
    if (frame === undefined) continue;
    const at = frameToSeconds(frame);
    if (at >= OPENING_REVIEW_SECONDS) continue;
    lines.push([formatClock(at), line.speaker && line.speaker !== "narrator" ? speakerName(doc, line.speaker) : "", String(line.text ?? "")]);
  }
  return lines;
}

/** The hash of what the readers read: the title, the thumbnail headline and the opening lines. */
export function openingHash(doc) {
  // The window is read with no gaps between lines or scenes, so it always holds every line the packet
  // shows, and a change of the episode's gaps alone keeps the review. A line's own pause_after_ms or
  // an action's seconds early in the script can still move a line across the 300 s edge.
  const lines = openingLines(doc, estimateTimeline({ ...doc, pauses: { line_ms: 0, scene_ms: 0 } })).map(([, speaker, text]) => [speaker, text]);
  return createHash("sha256").update(JSON.stringify(["opening-review-v1", doc.youtube?.title ?? "", cleanHeadline(doc), lines])).digest("hex");
}

/** The packet each reader reads: the thumbnail, the title and the first 300 seconds, timed. */
export function openingPacket(doc, timeline = estimateTimeline(doc)) {
  const lines = openingLines(doc, timeline).map(([at, speaker, text]) => `- [${at}] ${speaker ? `${speaker}：` : ""}${text}`);
  const hash = openingHash(doc);
  const headline = cleanHeadline(doc);
  const personas = Object.entries(OPENING_PERSONAS).map(([id, text]) => `- \`${id}\`：${text}`).join("\n");
  return `# 前 ${OPENING_REVIEW_SECONDS} 秒觀眾審查：${doc.slug}

你是一位**獨立的審查者**，沒有參與這支影片的製作，也不知道後面會講什麼。只讀這份文件，不讀其他檔案。
請用指定給你的觀眾身分讀下面的口白（時間是估計的），誠實回答：你會不會在前 ${OPENING_REVIEW_SECONDS} 秒內滑走？

## 你點進來之前看到的

- 縮圖大字：「${headline}」
- 標題：「${doc.youtube?.title ?? ""}」

## 前 ${OPENING_REVIEW_SECONDS} 秒的口白

${lines.join("\n")}

## 三種觀眾身分（你只扮演被指定的那一種）

${personas}

## 嚴格標準

- 第一句有沒有接上縮圖和標題答應的那件事？開場是不是只問一個問題，而不是一串問題菜單？
- 每一段有沒有讓你想知道下一句？有沒有拖、重複、念資料、念目錄、岔題？
- 有沒有沒頭沒尾：沒交代就冒出來的人名或名詞、接不上前一句的話、突然跳到別的事？
- 只要有任何一處會讓你想滑走或皺眉，就寫進 problems，並給出具體改法。寧可嚴格。

## 只回這個 JSON

\`\`\`json
{"opening_hash": "${hash}", "agent": "<你的名字>", "persona": "newcomer|scroller|stickler", "score": 0-10, "would_stay_300": true|false, "swipe_at": null 或 "mm:ss", "problems": [{"at": "mm:ss", "line": "原句", "why": "為什麼想走或皺眉", "fix": "具體改法"}]}
\`\`\`

\`opening_hash\` 照抄上面那串，不要改（它證明你讀的是這一版）。

通過條件（三位都要）：score ≥ ${OPENING_REVIEW_MIN_SCORE}、would_stay_300 為 true、swipe_at 為 null、problems 為空陣列。
`;
}

/** A record of one round, bound to what the readers read. */
export function openingReviewRecord(doc, verdicts, { round = 1, at = new Date(), author = null } = {}) {
  return { opening_hash: openingHash(doc), window_seconds: OPENING_REVIEW_SECONDS, ...(author ? { author_agent: author } : {}), round, recorded_at: at.toISOString(), verdicts };
}

/**
 * The readers a production session asked itself (owner, 2026-11-19: 「用每個跑的AI」): three fresh
 * subagents of the AI making the episode, one per viewer, each given only the packet. They cost no
 * site quota; the author names itself so it can never be one of its readers, and each reader echoes
 * the packet's opening_hash.
 */
export function sessionVerdicts(verdicts) {
  // Fresh subagents of one model often all call themselves "Claude"; the reader is named by its
  // persona, and the name it gave is kept beside it for the author check.
  return verdicts.map((verdict) => ({ ...verdict, swipe_at: swipeAt(verdict?.swipe_at), reader_name: String(verdict?.agent ?? "").trim(), agent: `session#${verdict?.persona ?? "?"}`, via: "session" }));
}

/** What each reader is told; the packet and its persona come in the payload. */
export const OPENING_REVIEW_INSTRUCTIONS = `You are ONE independent viewer of a zh-TW YouTube video. You did not make it and know nothing
about it beyond the payload. payload.packet is everything you see: the thumbnail headline, the title
and the first 300 seconds of the script, timed. Read it strictly as the viewer payload.persona
describes (payload.persona_description), and answer honestly whether you would swipe away inside
the first 300 seconds and why. Be strict: anything that would make you leave or frown is a problem,
with a concrete fix. Answer with the JSON object the packet asks for and nothing else, in zh-TW,
copying payload.opening_hash into "opening_hash" and payload.persona into "persona".`;

/** The JSON object of an answer, also when the model wrapped it in a fence or a sentence. */
export function parseOpeningAnswer(text) {
  const body = String(text ?? "");
  const start = body.indexOf("{");
  const end = body.lastIndexOf("}");
  if (start < 0 || end <= start) throw new Error("the reader's answer holds no JSON object");
  return JSON.parse(body.slice(start, end + 1));
}

/**
 * Ask the site's model for the three readers, one request each (the verifier stage, the model the
 * owner chose for it). The verdicts record that the site gave them (via, model): the gate takes no
 * verdict typed in by hand.
 */
export async function askOpeningReview(api, doc, { onVerdict = () => {} } = {}) {
  const packet = openingPacket(doc);
  const hash = openingHash(doc);
  const verdicts = [];
  for (const [persona, description] of Object.entries(OPENING_PERSONAS)) {
    let verdict;
    try {
      const answer = await api.run("verifier", doc.slug, OPENING_REVIEW_INSTRUCTIONS, { packet, persona, persona_description: description, opening_hash: hash }, OPENING_REVIEW_MAX_TOKENS, "drama", "opening-review");
      let parsed;
      try {
        parsed = parseOpeningAnswer(answer.text);
      } catch (error) {
        parsed = { score: 0, would_stay_300: false, swipe_at: null, problems: [{ at: "?", line: "", why: `the answer could not be read: ${error.message}`, fix: "ask again" }] };
      }
      // The tool sent the packet, so it binds the verdict to that packet itself; the model's copy
      // of the hash is not trusted either way. A rerun of --ask asks all three again.
      verdict = { ...parsed, swipe_at: swipeAt(parsed.swipe_at), opening_hash: hash, persona, agent: `site:${answer.model}#${persona}`, via: "site", model: answer.model, tokens: (answer.input_tokens ?? 0) + (answer.output_tokens ?? 0) };
    } catch (error) {
      // A refused or lost request is a failed reader, recorded with the ones already answered, so
      // the paid answers before it are kept and the next --ask names what went wrong.
      verdict = { persona, opening_hash: hash, agent: `site:error#${persona}`, via: "error", score: 0, would_stay_300: false, swipe_at: null, problems: [{ at: "?", line: "", why: `the site did not answer: ${error.message}`, fix: "run opening-review --ask again" }] };
    }
    verdicts.push(verdict);
    onVerdict(verdicts);
  }
  return verdicts;
}

/** "would not swipe" said as null, an empty string, 無, none or N/A all mean the same: no swipe. */
function swipeAt(value) {
  if (value === null || value === undefined) return null;
  const text = String(value).trim();
  // Only a plain "no" is no swipe; anything else (「不到一分鐘就會滑走」, a time) names a swipe.
  return !text || /^(?:null|none|n\/a|no|-|無|沒有|不會|否|不會滑走|不會離開|沒有滑走|不會走)$/i.test(text) ? null : text;
}

const who = (name) => String(name ?? "").trim().toLowerCase();

/** What keeps a record from passing: empty when the current script passed the strict round. */
export function openingReviewProblems(doc, record) {
  if (!record) return ["no opening review yet: have three fresh subagents read `opening-review --slug <slug>`'s packet and record them with --record, or run --ask on the site's model"];
  const problems = [];
  const current = openingHash(doc);
  if (record.opening_hash !== current) problems.push("the title, the thumbnail headline or the first 300 seconds changed after the opening review; run a new round on the current packet");
  if (record.window_seconds !== OPENING_REVIEW_SECONDS) problems.push(`the review must read the first ${OPENING_REVIEW_SECONDS} seconds`);
  const verdicts = Array.isArray(record.verdicts) ? record.verdicts : [];
  const agents = verdicts.map((verdict) => who(verdict?.agent));
  if (agents.some((agent) => !agent)) problems.push("every verdict names its reader (agent)");
  if (new Set(agents).size !== agents.length) problems.push("each reader is a different agent");
  if (verdicts.some((verdict) => verdict?.via === "session")) {
    if (!who(record.author_agent)) problems.push("a round of session readers names its author (--author)");
    if (verdicts.some((verdict) => verdict?.via === "session" && !who(verdict?.reader_name))) problems.push("every session reader gives its name (agent)");
    else if (verdicts.some((verdict) => who(verdict?.reader_name ?? verdict?.agent) === who(record.author_agent))) problems.push("the author cannot be a reader");
  }
  for (const persona of Object.keys(OPENING_PERSONAS)) {
    if (!verdicts.some((verdict) => verdict?.persona === persona)) problems.push(`no reader read as ${persona}`);
  }
  for (const verdict of verdicts) {
    const reader = `${verdict?.agent ?? "?"} (${verdict?.persona ?? "?"})`;
    if (!Object.hasOwn(OPENING_PERSONAS, verdict?.persona)) problems.push(`${reader}: unknown persona`);
    const fromSite = verdict?.via === "site" && verdict?.model;
    if (!fromSite && verdict?.via !== "session") problems.push(`${reader}: not a recorded reader (record session readers with --record, or ask the site with --ask)`);
    if (!(Number(verdict?.score) >= OPENING_REVIEW_MIN_SCORE)) problems.push(`${reader}: score ${verdict?.score} is under ${OPENING_REVIEW_MIN_SCORE}`);
    if (verdict?.would_stay_300 !== true) problems.push(`${reader}: would not stay the first ${OPENING_REVIEW_SECONDS} seconds`);
    if (verdict?.swipe_at !== null && verdict?.swipe_at !== undefined) problems.push(`${reader}: would swipe away at ${verdict.swipe_at}`);
    if (verdict?.opening_hash !== current) problems.push(`${reader}: read another version of the packet (its opening_hash is not the current one)`);
    if (!Array.isArray(verdict?.problems)) problems.push(`${reader}: "problems" must be a list (empty when there is nothing to fix)`);
    const listed = Array.isArray(verdict?.problems) ? verdict.problems : [];
    for (const each of listed) problems.push(`${reader}: ${each?.at ?? "?"} 「${each?.line ?? ""}」 ${each?.why ?? ""} → ${each?.fix ?? ""}`);
  }
  return problems;
}
