// The opening review of 原來如此事務所, 奇聞檔案局 and the brand stories (owner, 2026-11-19: 「應該要前300秒
// 都不會滑走比較好，嚴格審核」, with several independent agents). Before any paid voice, three
// independent readers, each in a fresh session and each reading as a different viewer, read the
// first 300 seconds of the script with the thumbnail and the title beside it, and say where they
// would swipe away. The script passes only when every one of them would stay all 300 seconds and
// names nothing to fix. The verdicts are bound to the script, so any edit asks for a new round.
import { existsSync } from "node:fs";
import path from "node:path";

import { readApprovals } from "./approvals.mjs";
import { isOpeningHookSeries } from "./narrative.mjs";
import { eachLine } from "./schema.mjs";
import { scriptCheckBinding, scriptCheckMatches } from "./script-check.mjs";
import { estimateTimeline, formatClock, frameToSeconds } from "./timeline.mjs";

/** Where the round's verdicts are kept, under the video's work directory. */
export const OPENING_REVIEW = ["review", "opening-review.json"];
/** Where the packet the readers read is written. */
export const OPENING_PACKET = ["review", "opening-packet.md"];
export const OPENING_REVIEW_SECONDS = 300;
export const OPENING_REVIEW_MIN_SCORE = 8.5;

/** The three viewers the readers read as; one reader each, every one must pass. */
export const OPENING_PERSONAS = Object.freeze({
  newcomer: "第一次點進這個頻道的路人：對這個題目沒有任何背景，只因為縮圖和標題點進來。你在找「這是什麼、為什麼值得看下去」，聽不懂或覺得跟縮圖無關就走。",
  scroller: "邊滑手機邊看的觀眾：耐心很少，任何一段拖、重複、繞遠路、像在念資料或念目錄，你就滑走。你在意每 30–45 秒有沒有讓你想知道下一句。",
  stickler: "挑剔的老觀眾：專抓不順和沒頭沒尾——人名、名詞、物件第一次出現有沒有先交代；句子和段落有沒有接上；有沒有突然跳到別的事、或說出前後接不起來的話；兩個人對話時回答有沒有接住剛被問的那句。",
});

/** Whether a video must pass the opening review before its voice is made. */
export function needsOpeningReview(doc, { series = null, workdir = null } = {}) {
  if (!isOpeningHookSeries(doc, series)) return false;
  // The host's worker holds its own scripts with the blind panel; this review is the gate of the
  // episodes a session makes by hand (no auto.json in the work directory).
  if (workdir && existsSync(path.join(workdir, "auto.json"))) return false;
  // A cut the owner already approved is not asked again.
  if (workdir && readApprovals(workdir).approvals.some((approval) => approval.gate === "final")) return false;
  return true;
}

/** The packet each reader reads: the thumbnail, the title and the first 300 seconds, timed. */
export function openingPacket(doc, timeline = estimateTimeline(doc)) {
  const starts = new Map((timeline.lines ?? []).map((line) => [line.id, line.start_frame]));
  const lines = [];
  for (const { line } of eachLine(doc)) {
    const frame = starts.get(line.id);
    if (frame === undefined) continue;
    const at = frameToSeconds(frame);
    if (at >= OPENING_REVIEW_SECONDS) continue;
    lines.push(`- [${formatClock(at)}] ${line.speaker && line.speaker !== "narrator" ? `${line.speaker}：` : ""}${line.text}`);
  }
  const headline = String(doc.thumbnail?.data?.headline ?? "").replace(/\*\*/g, "").replace(/\n/g, " ");
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
{"agent": "<你的名字>", "persona": "newcomer|scroller|stickler", "score": 0-10, "would_stay_300": true|false, "swipe_at": null 或 "mm:ss", "problems": [{"at": "mm:ss", "line": "原句", "why": "為什麼想走或皺眉", "fix": "具體改法"}]}
\`\`\`

通過條件（三位都要）：score ≥ ${OPENING_REVIEW_MIN_SCORE}、would_stay_300 為 true、swipe_at 為 null、problems 為空陣列。
`;
}

/** A record of one round, bound to the script the readers read. */
export function openingReviewRecord(doc, verdicts, { author, round = 1, at = new Date() } = {}) {
  return { ...scriptCheckBinding(doc), window_seconds: OPENING_REVIEW_SECONDS, author_agent: author ?? null, round, recorded_at: at.toISOString(), verdicts };
}

/** What keeps a record from passing: empty when the current script passed the strict round. */
export function openingReviewProblems(doc, record) {
  if (!record) return ["no opening review yet: run `opening-review --slug <slug>` and have three independent readers answer it"];
  const problems = [];
  if (!scriptCheckMatches(record, doc)) problems.push("the script changed after the opening review; run a new round on the current script");
  if (record.window_seconds !== OPENING_REVIEW_SECONDS) problems.push(`the review must read the first ${OPENING_REVIEW_SECONDS} seconds`);
  const verdicts = Array.isArray(record.verdicts) ? record.verdicts : [];
  const agents = verdicts.map((verdict) => String(verdict?.agent ?? "").trim());
  if (!record.author_agent) problems.push("the record names no author_agent");
  if (agents.some((agent) => !agent)) problems.push("every verdict names its reader (agent)");
  if (new Set(agents).size !== agents.length) problems.push("each reader is a different agent");
  if (record.author_agent && agents.includes(record.author_agent)) problems.push("the author cannot be a reader");
  for (const persona of Object.keys(OPENING_PERSONAS)) {
    if (!verdicts.some((verdict) => verdict?.persona === persona)) problems.push(`no reader read as ${persona}`);
  }
  for (const verdict of verdicts) {
    const who = `${verdict?.agent ?? "?"} (${verdict?.persona ?? "?"})`;
    if (!Object.hasOwn(OPENING_PERSONAS, verdict?.persona)) problems.push(`${who}: unknown persona`);
    if (!(Number(verdict?.score) >= OPENING_REVIEW_MIN_SCORE)) problems.push(`${who}: score ${verdict?.score} is under ${OPENING_REVIEW_MIN_SCORE}`);
    if (verdict?.would_stay_300 !== true) problems.push(`${who}: would not stay the first ${OPENING_REVIEW_SECONDS} seconds`);
    if (verdict?.swipe_at !== null && verdict?.swipe_at !== undefined) problems.push(`${who}: would swipe away at ${verdict.swipe_at}`);
    const listed = Array.isArray(verdict?.problems) ? verdict.problems : [];
    for (const each of listed) problems.push(`${who}: ${each?.at ?? "?"} 「${each?.line ?? ""}」 ${each?.why ?? ""} → ${each?.fix ?? ""}`);
  }
  return problems;
}
