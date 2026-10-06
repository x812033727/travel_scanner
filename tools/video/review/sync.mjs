// `review-push` and `review-pull`: the owner reviews on the site's /admin/videos, not in chat.
//
// `review-push` reports where a video is and submits the next thing to decide: the outline
// (brief.md with its options, and Jev's pick when the channel stance lets it choose), the
// narration (a small AAC copy plus the Jev check), the final cut (a 720p copy, the contact sheet,
// the thumbnail, titles in every locale, and the quality check's report), or the upload package
// (every file in it and the package check). Each is bound to the SHA-256 of the file its
// approval gate covers, so an approval on the site means exactly the file the pipeline has; the
// site approves a review on arrival when the pick, the quality check or the package check passes
// and the owner's switch is on (docs/videos/HANDS-OFF.md). `review-pull` reads the decisions back
// and records an approval only when that hash still matches the local file.
import { closeSync, existsSync, mkdirSync, openSync, readFileSync, readSync, statSync } from "node:fs";
import path from "node:path";
import { isDeepStrictEqual, parseArgs } from "node:util";

import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { AutomationError, automationClient } from "../automation/client.mjs";
import { ANIME_APPROVAL_GATES, approvalRuntimePolicyHash, GATES, approvalState, approve, readApprovals, sha256File } from "../core/approvals.mjs";
import { animeRuntimeContext, hasAnimePolicy, LONG_ANIME_POLICY, runtimePolicyHash, validateAnimeRuntime } from "../core/anime-policy.mjs";
import { assembledAudioProblems, audioEvidenceProblems, currentAudioCheck } from "../core/audio-evidence.mjs";
import { animeBodyDurationProblems, animeRuntimeProof } from "../core/duration.mjs";
import { appliedBranding, brandingCurrent, presentationTimeline, readBranding } from "../core/branding.mjs";
import { isCompilation } from "../core/compilation.mjs";
import { drawnShotScenes, hasCast, illustrated, isDrama } from "../core/drama.mjs";
import { atomicWrite, docDir, isInside, readJson, resolveWorkBase, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { chosenLocales, dubRole, dubsForUpload, LANGUAGES_FILE, metadataLocalesOf, readLanguages } from "../core/stages.mjs";
import { ARTIFACTS, keyframeProblems, loadProject, pipelineStatus } from "../core/state.mjs";
import { narrationLocale, VIDEO_CATEGORIES } from "../core/schema.mjs";
import { narrativeHash, scriptScenes, writeScreenplay } from "../core/screenplay.mjs";
import { scriptCheckMatches } from "../core/script-check.mjs";
import { estimateTimeline, formatClock, speechHash } from "../core/timeline.mjs";
import { keepSheets } from "../media/series-store.mjs";
import { packageFiles, packageLocales, readPackageReport, thumbnailVariants, UPLOAD_DIR, variantRole } from "../package/check.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { USER_AGENT } from "../tts/client.mjs";
import { bindRenewalSubmission } from "./renewal.mjs";

// Mirrors PART_BYTES in apps/api/app/video_reviews/storage.py: under nginx's 6 MB request cap.
export const PART_BYTES = 4 * 1024 * 1024;
// look and storyboard are the drama format's gates (docs/videos/DRAMA.md); script is a series
// episode's screenplay, read before any image or clip is paid for (docs/videos/SERIES.md);
// languages is a batch of the languages the owner chose after the final cut, with their files
// (docs/videos/LANGUAGES.md), and dubs what that gate was when it carried dub tracks alone
// (docs/videos/DUBS.md); both are sent only when asked for with --gate.
export const REVIEW_GATES = ["outline", "script", "look", "audio", "storyboard", "final", "publish", "languages", "dubs"];
const UPLOAD_CHECKLIST = path.join("upload", "UPLOAD.md");

// The owner reads the site in Traditional Chinese; status's step ids are English. Every step of
// every format (core/state.mjs SLIDES_STEPS, DRAMA_STEPS and COMPILATION_STEPS) has a label here.
export const STEP_LABELS = {
  // A series' compilation (docs/videos/BINGE.md).
  "metadata planned": "合集標題與說明",
  "cards rendered": "章節卡與縮圖",
  "video compiled": "合集串接",
  "metadata translated": "五語標題與說明",
  brief: "企劃書",
  "outline approved": "站主選好大綱",
  "script passes lint": "稿子通過檢查",
  "fact-checked": "查核完成",
  "script approved": "劇本核准",
  "look generated": "角色設定圖",
  "look approved": "站主選好設定圖",
  "narration synthesized": "旁白合成",
  "narration approved": "旁白核准",
  "keyframes drawn": "關鍵影格",
  "storyboard approved": "分鏡核准",
  "frames rendered": "畫面完成",
  "clips generated": "片段生成",
  "music generated": "配樂生成",
  "video assembled": "成片合成",
  "captions written": "字幕",
  "final video approved": "成片核准",
  "upload package": "上傳包",
  "on YouTube": "已上 YouTube",
};

export class ReviewError extends Error {
  constructor(message, { status = 0, code = "", who = "service", submission = false } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    this.who = who;
    this.submission = submission;
  }
}

// ReviewIn.summary in apps/api/app/video_reviews/schemas.py takes at most this many characters,
// counted as Unicode code points. A longer one is refused with 422, review-push answers that with
// the lint code, and the worker blocks the video (automation/flow.mjs submissionFailure).
export const MAX_REVIEW_SUMMARY_LENGTH = 500;
// How many pictures kept with the judge's remarks a summary names before it counts the rest: an
// illustrated video may keep dozens, and the whole list is the payload's, which the card shows.
export const SUMMARY_PICTURE_IDS = 5;

/**
 * A review's summary as the site takes it: itself while it fits, else cut to
 * MAX_REVIEW_SUMMARY_LENGTH characters, the last one an ellipsis. Every summary here is written
 * to fit; this is what holds when one does not (an id has no length limit of its own). Every
 * review this file assembles goes through it: reviewPush before it posts one, and outlineReview,
 * whose review the worker posts itself.
 */
export function fitSummary(summary) {
  return cutText(String(summary ?? ""), MAX_REVIEW_SUMMARY_LENGTH);
}

/** A text of at most `length` characters, counted as code points: itself, or cut there with an ellipsis as its last one. */
function cutText(text, length) {
  const characters = [...text];
  return characters.length <= length ? text : `${characters.slice(0, length - 1).join("")}…`;
}

/** The kept pictures as a summary names them: the first SUMMARY_PICTURE_IDS ids, then how many more there are. */
export function namedPictures(ids) {
  const named = ids.slice(0, SUMMARY_PICTURE_IDS).join("、");
  return ids.length > SUMMARY_PICTURE_IDS ? `${named} 等，另 ${ids.length - SUMMARY_PICTURE_IDS} 張` : named;
}

// ReviewIn._small in apps/api/app/video_reviews/schemas.py refuses a payload larger than
// MAX_PAYLOAD_BYTES with 422, and a refused review blocks the video as a summary too long does.
// The screenplay of a long-anime series episode alone may be larger (MAX_ANIME_SCRIPT_BYTES).
export const MAX_REVIEW_PAYLOAD_BYTES = 256 * 1024;
export const MAX_ANIME_SCRIPT_BYTES = 1024 * 1024;
// Where review-push starts leaving more of the judge's remarks out, short of the limit:
// payloadBytes writes a number as JSON.stringify does, and Python writes a few of them a
// character longer.
export const REVIEW_PAYLOAD_BUDGET = 240_000;
// What a review carries of the judge's remarks on one kept picture: this many lines, each cut to
// this many characters. An illustrated video may keep hundreds of pictures, each with what the
// judge said of every take; keyframes/manifest.json keeps all of it (accepted_with_problems).
export const KEPT_REMARK_LINES = 6;
export const KEPT_REMARK_LENGTH = 300;
// The lines a picture keeps when the payload is still past the budget: two, then none.
const FEWER_REMARK_LINES = [2, 0];
const REMARKS_LEFT_OUT = "意見因審核資料的大小上限略去，全文在 keyframes/manifest.json";

/**
 * The judge's remarks on a kept picture as a review carries them: the first `lines` of them, each
 * cut to KEPT_REMARK_LENGTH characters, then one line counting the rest. With no line to spend,
 * the one line that says they were left out for size; none for a picture the judge said nothing of.
 */
export function keptRemarks(problems, lines = KEPT_REMARK_LINES) {
  const remarks = (Array.isArray(problems) ? problems : []).filter((each) => typeof each === "string" && each);
  if (!remarks.length) return [];
  if (lines <= 0) return [REMARKS_LEFT_OUT];
  const shown = remarks.slice(0, lines).map((each) => cutText(each, KEPT_REMARK_LENGTH));
  return remarks.length > lines ? [...shown, `…另有 ${remarks.length - lines} 則，全文在 keyframes/manifest.json`] : shown;
}

/**
 * A payload's size as the server measures it (ReviewIn._small): Python's json.dumps(value,
 * ensure_ascii=False) in UTF-8, which puts a space after every comma and colon and leaves text
 * outside ASCII as it is. Measured on what the request carries: JSON.stringify drops what JSON
 * has no word for.
 */
export function payloadBytes(payload) {
  const written = (value) => {
    if (Array.isArray(value)) return `[${value.map(written).join(", ")}]`;
    if (value !== null && typeof value === "object") return `{${Object.entries(value).map(([key, each]) => `${JSON.stringify(key)}: ${written(each)}`).join(", ")}}`;
    return JSON.stringify(value);
  };
  return Buffer.byteLength(written(JSON.parse(JSON.stringify(payload ?? {}))), "utf8");
}

const isRecord = (value) => value !== null && typeof value === "object" && !Array.isArray(value);

/** The most bytes the server takes for a review's payload: the ordinary limit, or a long-anime series screenplay's, by the rule ReviewIn._small applies. */
function payloadLimit({ gate, payload }) {
  const context = payload?.runtime_context;
  const longScreenplay = gate === "script" && payload?.production_policy === LONG_ANIME_POLICY
    && isRecord(context) && context.kind === "series" && context.genre === "custom" && context.lead === "ensemble"
    && validateAnimeRuntime(payload.runtime_spec).length === 0;
  return longScreenplay ? MAX_ANIME_SCRIPT_BYTES : MAX_REVIEW_PAYLOAD_BYTES;
}

// The list in a review's payload that names the pictures kept with the judge's remarks, by gate.
const KEPT_LIST = { final: "accepted_pictures", storyboard: "accepted" };

/**
 * A review's payload with the judge's remarks on its kept pictures cut to `lines` a picture
 * (keptRemarks) wherever that review carries them: on its list of kept pictures and, on a
 * storyboard, in the own verdict of each kept shot, which is left empty when the lines are none
 * (the list says why). Every picture keeps its id. Null for a review that names no kept picture.
 */
function withKeptRemarks({ gate, payload }, lines) {
  if (!isRecord(payload)) return null;
  const list = KEPT_LIST[gate];
  const pictures = list && Array.isArray(payload[list]) ? payload[list] : [];
  const shots = gate === "storyboard" && Array.isArray(payload.shots) ? payload.shots : [];
  const keptShot = (shot) => isRecord(shot) && shot.accepted === true;
  if (!pictures.length && !shots.some(keptShot)) return null;
  return {
    ...payload,
    ...(pictures.length ? { [list]: pictures.map((picture) => (isRecord(picture) ? { ...picture, problems: keptRemarks(picture.problems, lines) } : picture)) } : {}),
    ...(shots.length ? { shots: shots.map((shot) => (keptShot(shot) ? { ...shot, judge: { ...(isRecord(shot.judge) ? shot.judge : {}), problems: lines > 0 ? keptRemarks(shot.judge?.problems, lines) : [] } } : shot)) } : {}),
  };
}

/**
 * A review as review-push posts it, its payload within what the server takes. The judge's
 * remarks on the kept pictures go up cut to KEPT_REMARK_LINES lines a picture; while the payload
 * is past REVIEW_PAYLOAD_BUDGET they are cut further in steps, to two lines and then to none,
 * every picture keeping its id. A payload still past the server's limit is not sent: the server
 * would answer 422, and this says how large it is. Returns { body, bytes, lines }, `lines` null
 * unless the remarks were cut past their usual lines.
 */
export function fitPayload(body) {
  const limit = payloadLimit(body);
  const budget = limit - (MAX_REVIEW_PAYLOAD_BYTES - REVIEW_PAYLOAD_BUDGET);
  const kept = withKeptRemarks(body, KEPT_REMARK_LINES);
  let payload = kept ?? body.payload;
  let bytes = payloadBytes(payload);
  let lines = null;
  for (const fewer of kept ? FEWER_REMARK_LINES : []) {
    if (bytes <= budget) break;
    payload = withKeptRemarks(body, fewer);
    bytes = payloadBytes(payload);
    lines = fewer;
  }
  if (bytes > limit) {
    throw new ReviewError(`the ${body.gate} review's payload is ${bytes} bytes, over the ${limit} the site takes${kept ? ", even with the judge's remarks on the kept pictures left out" : ""}; nothing was sent`, { code: "payload_too_large", submission: true });
  }
  return { body: kept ? { ...body, payload } : body, bytes, lines };
}

/** The outline options a brief offers: `### 選項 A：title`, its 一行說明, its 開場鉤子. */
export function outlineOptions(brief) {
  const options = [];
  const lines = brief.split(/\r?\n/);
  for (let index = 0; index < lines.length; index++) {
    const heading = /^###\s*選項\s*([A-Z])\s*[：:]\s*(.+?)\s*$/.exec(lines[index]);
    if (!heading) continue;
    const option = { key: heading[1], title: heading[2].replace(/（推薦）|\(推薦\)/, "").trim() };
    for (let next = index + 1; next < lines.length && !/^#{2,3}\s/.test(lines[next]); next++) {
      const summary = /^一行說明[：:]\s*(.+)$/.exec(lines[next]);
      const hook = /^開場鉤子[^：:]*[：:]\s*(.+)$/.exec(lines[next]);
      if (summary && !option.summary) option.summary = summary[1].trim();
      if (hook && !option.hook) option.hook = hook[1].trim().replace(/^「|」$/g, "");
    }
    options.push(option);
  }
  return options;
}

// An article is read at /<locale>/life/<slug> or /<locale>/guides/<kind>/<slug> (core/metadata.mjs
// articlePath). /<locale>/guides/<slug> is what drafts saved before 2026-09-27; it still names
// the article, so earlier videos keep their topic.
const GUIDE_URL = /^https:\/\/(?:www\.)?mokaair\.com\/[A-Za-z-]+\/(?:life|guides(?:\/[a-z0-9-]+)?)\/([a-z0-9][a-z0-9-]{0,118}[a-z0-9])\/?(?:[?#].*)?$/;

/** The site articles among some URLs, by slug. */
export function guideSlugs(urls) {
  return [...new Set((urls ?? []).map((url) => GUIDE_URL.exec(String(url))?.[1]).filter(Boolean))];
}

/** The article a video retells: source_guide, or else the first site article it cites. */
export function sourceGuideOf(doc) {
  return doc.source_guide || guideSlugs((doc.sources ?? []).map((source) => source?.url))[0] || null;
}

/** status's steps as the site's checklist. */
export function checklistFrom(steps) {
  return steps.map((step) => ({ key: step.id.toLowerCase().replace(/[^a-z0-9]+/g, "_").slice(0, 40), label: STEP_LABELS[step.id] ?? step.id, done: Boolean(step.done) }));
}

/**
 * The Jev check in numbers, and the lines still flagged, from review/check.json and check-flags.json.
 * Lines a second transcript cleared (tts/second-opinion.mjs) are counted and listed with both
 * transcripts, so the card says what cleared them; without any, the payload is what it always was.
 */
export function audioCheck(check, flags, lineCount) {
  const entries = Object.values(check?.lines ?? {});
  const flagged = new Set(flags?.flags ?? []);
  const exact = entries.filter((entry) => entry.match_kind === "exact").length;
  const alike = entries.filter((entry) => entry.match && entry.match_kind !== "exact").length;
  const cleared = Object.entries(check?.lines ?? {}).filter(([id, entry]) => !flagged.has(id) && !entry.match && entry.second);
  return {
    check: {
      lines: lineCount,
      checked: entries.length,
      exact,
      alike,
      judged_fine: entries.length - exact - alike - flagged.size - cleared.length,
      flagged: flagged.size,
      ...(cleared.length ? { cleared: cleared.length } : {}),
    },
    flagged_lines: Object.entries(check?.lines ?? {})
      .filter(([id]) => flagged.has(id))
      .map(([id, entry]) => ({ id, script: entry.intended ?? "", heard: entry.heard ?? "", noul: entry.noul ?? null })),
    ...(cleared.length
      ? { cleared_lines: cleared.map(([id, entry]) => ({ id, script: entry.intended ?? "", heard: entry.heard ?? "", second: { by: entry.second.by, heard: entry.second.heard } })) }
      : {}),
  };
}

/**
 * The audio card's summary line for the second transcript's work, or "" when it cleared nothing.
 * `ids: false` leaves the line ids out: a narration with dozens of cleared lines would name them
 * past the summary's limit, and the payload's cleared_lines keeps every one.
 */
export function clearedSummary(check, { ids = true } = {}) {
  const lines = check.cleared_lines ?? [];
  if (!lines.length) return "";
  const by = [...new Set(lines.map((line) => line.second.by))].join("、");
  return `；${by} 另外轉寫、排除 ${lines.length} 句${ids ? `（${lines.map((line) => line.id).join("、")}）` : ""}`;
}

/** The audio review's summary: the cleared lines by id while that fits the site's limit, by their number alone otherwise. */
export function audioSummary({ seconds, lines, check, rewrites }) {
  const said = (ids) => `旁白 ${formatClock(Math.round(seconds))}，${lines} 句；Jev 標記 ${check.check.flagged} 句${clearedSummary(check, { ids })}${rewrites ? `；改寫 ${rewrites} 句` : ""}`;
  const detailed = said(true);
  return [...detailed].length <= MAX_REVIEW_SUMMARY_LENGTH ? detailed : said(false);
}

/** The unticked items of UPLOAD.md, without their Markdown emphasis. */
export function uploadItems(markdown) {
  return markdown
    .split(/\r?\n/)
    .map((line) => /^- \[ \]\s*(.+)$/.exec(line)?.[1])
    .filter(Boolean)
    .map((item) => item.replace(/\*\*/g, ""));
}

// The judge takes 2 to 3 options (judge.py MIN_OPTIONS, MAX_OPTIONS).
export const JUDGE_MIN_OPTIONS = 2;
export const JUDGE_MAX_OPTIONS = 3;

/** The judge endpoint's body, exactly { slug, brief, options: [{ key, title, summary, hook }] }: its request model refuses any other field. */
export function judgeBody(slug, brief, options) {
  return {
    slug,
    brief,
    options: options.slice(0, JUDGE_MAX_OPTIONS).map((option) => ({ key: option.key, title: option.title, summary: option.summary ?? "", hook: option.hook ?? "" })),
  };
}

/** Jev's answer as a review's `pick`: { choice, probabilities, options: { key: { stance, demo } }, advice, passed, note }, or null when it has no verdict. */
export function pickFrom(answer) {
  if (typeof answer?.passed !== "boolean" || typeof answer.choice !== "string" || !answer.choice) return null;
  return {
    choice: answer.choice,
    probabilities: answer.probabilities && typeof answer.probabilities === "object" ? answer.probabilities : {},
    options: answer.options && typeof answer.options === "object" ? answer.options : {},
    advice: typeof answer.advice === "number" ? answer.advice : null,
    passed: answer.passed,
    note: typeof answer.note === "string" ? answer.note : "",
  };
}

/**
 * Ask Jev which outline to make (docs/videos/HANDS-OFF.md §Jev 挑大綱). `api` is the automation
 * client. Answers { status: "passed" | "failed", pick } with Jev's verdict; { status: "owner",
 * reason } when the site says the judge is not enabled (409: the stance is blank or the switch
 * is off) or has no judge yet, so the outline waits for the owner as before; { status: "later",
 * reason } when Jev, its budget or the site could not answer, to try again next round. A revoked
 * token or another error only the owner can fix is thrown.
 */
export async function judgeOutline(api, slug, brief, options) {
  if (options.length < JUDGE_MIN_OPTIONS) return { status: "owner", reason: `the brief has ${options.length} options; the judge takes ${JUDGE_MIN_OPTIONS} to ${JUDGE_MAX_OPTIONS}` };
  let answer;
  try {
    answer = await api.judgeOutline(judgeBody(slug, brief, options));
  } catch (error) {
    if (!(error instanceof AutomationError)) throw error;
    if (error.status === 409 && error.code === "video_judge_not_enabled") return { status: "owner", reason: error.message };
    if (error.status === 404) return { status: "owner", reason: "the site has no judge endpoint yet" };
    if (error.who === "owner") throw error;
    return { status: "later", reason: error.message };
  }
  const pick = pickFrom(answer);
  if (!pick) return { status: "later", reason: "the judge answered without a verdict" };
  return { status: pick.passed ? "passed" : "failed", pick };
}

/**
 * The outline review's payload and summary: the brief, its options and Jev's pick when there is
 * one. The worker posts this one itself (automation/flow.mjs submitOutline), past reviewPush, so
 * the summary is fitted here: the choice is the judge's answer as it came (pickFrom asks only
 * that it is text).
 */
export function outlineReview(brief, options, verdict, suffix = "") {
  const payload = { brief, options };
  let summary = `企劃書與 ${options.length} 個大綱選項${suffix}`;
  if (verdict?.pick) {
    payload.pick = verdict.pick;
    summary += verdict.status === "passed" ? `；Jev 挑了 ${verdict.pick.choice}` : "；Jev 沒有挑出過關的大綱，請站主選";
  }
  return { payload, summary: fitSummary(summary) };
}

/** A review's summary for the quality check's report: 「自動品管 11 項全過」 or 「自動品管 2 項沒過：pace、links」. */
export function qaSummary(report) {
  if (!report) return "自動品管沒有結果";
  const failed = report.items.filter((each) => !each.ok).map((each) => each.id);
  return failed.length ? `自動品管 ${failed.length} 項沒過：${failed.join("、")}` : `自動品管 ${report.items.length} 項全過`;
}

/** The same for the package check: 「上傳包 4 項齊全」 or 「上傳包 1 項沒過：captions」. */
export function packageSummary(report) {
  const failed = report.items.filter((each) => !each.ok).map((each) => each.id);
  return failed.length ? `上傳包 ${failed.length} 項沒過：${failed.join("、")}` : `上傳包 ${report.items.length} 項齊全`;
}

/**
 * Run the quality check before the final cut goes up: exit 0 or 1 means there is a report to
 * send (qa.json for this very final.mp4); 4 means a service was down and the push waits for the
 * next round; 3 needs the owner (the token). A test that plays the commands hands in runCommand.
 */
async function qualityCheck(ctx, slug, workdir, flags) {
  const args = ["qa", "--slug", slug, ...flags];
  let code;
  if (ctx.runCommand) ({ code } = await ctx.runCommand(args, ctx));
  else {
    const qa = await import("../qa/cli.mjs");
    code = await qa.run("qa", args.slice(1), ctx);
  }
  if (code === ctx.EXIT.external) throw new ReviewError("the quality check could not finish (a service was down); run review-push --gate final again later", { who: "service" });
  if (code === ctx.EXIT.owner) throw new ReviewError("the quality check needs the owner (the video tool token); see above", { who: "owner" });
  return readJson(path.join(workdir, "review", "qa.json"), null);
}

function client(ctx) {
  const credentials = readCredentials({ env: ctx.env, home: ctx.home });
  if (!credentials.token) throw new ReviewError("no video tool token yet: run `node tools/video/cli.mjs login`", { who: "owner" });
  const fetchImpl = ctx.fetch ?? globalThis.fetch;
  const sleep = ctx.sleep ?? ((ms) => new Promise((resolve) => setTimeout(resolve, ms)));
  return async function request(method, route, { json, bytes, query } = {}) {
    const url = `${credentials.site}/api/video/reviews/${route}${query ? `?${new URLSearchParams(query)}` : ""}`;
    let last;
    for (let attempt = 0; attempt < 4; attempt++) {
      let response;
      try {
        response = await fetchImpl(url, {
          method,
          headers: {
            Authorization: `Bearer ${credentials.token}`,
            "User-Agent": USER_AGENT,
            Accept: "application/json",
            ...(json ? { "Content-Type": "application/json" } : bytes ? { "Content-Type": "application/octet-stream" } : {}),
          },
          body: json ? JSON.stringify(json) : bytes,
        });
      } catch (error) {
        last = new ReviewError(`cannot reach ${credentials.site}: ${error.message}`, { code: "network" });
        await sleep(2 ** attempt * 1000);
        continue;
      }
      if (response.ok) return response.json();
      const problem = await response.json().catch(() => ({}));
      const message = problem.detail || `HTTP ${response.status}`;
      const who = response.status === 401 ? "owner" : "service";
      const submission = (method === "POST" && route.endsWith("/reviews")) || (method === "PUT" && route.includes("/files/"));
      last = new ReviewError(message, { status: response.status, code: problem.code ?? "", who, submission });
      if (!(response.status === 429 || response.status >= 500)) throw last;
      await sleep(Math.min(Number(response.headers.get("retry-after")) || 2 ** attempt, 30) * 1000);
    }
    throw last;
  };
}

/** Upload one file in parts unless the site has it already; returns its review file entry. */
async function upload(request, slug, file, role, contentType) {
  const sha256 = await sha256File(file);
  const size = statSync(file).size;
  const parts = Math.max(1, Math.ceil(size / PART_BYTES));
  const handle = openSync(file, "r");
  try {
    for (let part = 0; part < parts; part++) {
      const length = Math.min(PART_BYTES, size - part * PART_BYTES);
      const bytes = Buffer.alloc(length);
      readSync(handle, bytes, 0, length, part * PART_BYTES);
      const result = await request("PUT", `${slug}/files/${sha256}`, { bytes, query: { part, parts, size } });
      if (result.complete) break;
    }
  } finally {
    closeSync(handle);
  }
  return { role, sha256, size, content_type: contentType };
}

/**
 * The ffmpeg arguments of a review copy: the narration as a small mono AAC, the cut as 720p.
 * A compilation's preview (docs/videos/BINGE.md) is hours long, so its bitrate is capped as
 * well, or the review store would hold a file nearly the size of the cut.
 */
export function previewArgs(kind, source, target, { compilation = false } = {}) {
  if (kind === "narration") return ["-hide_banner", "-y", "-loglevel", "error", "-i", source, "-c:a", "aac", "-b:a", "96k", "-ac", "1", "-movflags", "+faststart", target];
  return [
    "-hide_banner", "-y", "-loglevel", "error", "-i", source,
    "-vf", "scale=1280:720:flags=lanczos",
    "-c:v", "libx264", "-preset", "veryfast", "-crf", "26",
    ...(compilation ? ["-maxrate", "2M", "-bufsize", "4M"] : []),
    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", target,
  ];
}

/** Encode a smaller copy for the page with ffmpeg, once per source file. */
async function encodeDefault(kind, source, target, env, options = {}) {
  const tools = await locateFfmpeg(env);
  await runTool(tools.ffmpeg, previewArgs(kind, source, target, options));
}

async function preview(ctx, workdir, kind, source, options = {}) {
  const hash = (await sha256File(source)).slice(0, 16);
  const target = path.join(workdir, "review", `${kind}-${hash}.${kind === "narration" ? "m4a" : "mp4"}`);
  if (!existsSync(target)) {
    mkdirSync(path.dirname(target), { recursive: true });
    await (ctx.encode ?? encodeDefault)(kind, source, target, ctx.env, options);
  }
  return target;
}

/** The option letter of candidate n on the review page: 1 → A. */
export const optionKey = (n) => String.fromCharCode(64 + n);
const IMAGE_TYPES = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp" };
const imageType = (file) => IMAGE_TYPES[path.extname(file).toLowerCase()] ?? "application/octet-stream";

/**
 * The next gate whose content exists and is not approved as it stands; null when none. A drama
 * (docs/videos/DRAMA.md) reads its screenplay before the sheets (docs/videos/DRAMA-FLOW.md,
 * section 2), puts the look before the narration and the storyboard before the cut; a drama with
 * no characters has no look to approve.
 */
async function nextGate(places, workdir, doc) {
  // A compilation's episodes went through every gate; the owner sees its cut, then its package.
  // Every other drama has a script gate (docs/videos/DRAMA-FLOW.md, section 2).
  // Illustrated slides (docs/videos/ILLUSTRATED.md) show their storyboard after the narration.
  const order = isCompilation(doc) ? ["final"] : isDrama(doc) ? ["outline", "script", ...(hasCast(doc) ? ["look"] : []), "audio", "storyboard", "final"] : ["outline", "audio", ...(illustrated(doc) ? ["storyboard"] : []), "final"];
  for (const gate of order) {
    const state = await approvalState({ gate, ...places });
    if (state.status === "missing" || state.status === "stale") return gate;
    if (state.status === "absent") return null;
  }
  const metadata = path.join(workdir, ARTIFACTS.upload);
  if (!existsSync(metadata)) return null;
  const confirmation = await approvalState({ gate: "publish", ...places });
  return confirmation.status === "approved" ? null : "publish";
}

async function submission(gate, { ctx, request, project, workdir, dir, flags = [], manualReview = false }) {
  const { doc } = project;
  const slug = doc.slug;
  const runtimeFields = hasAnimePolicy(doc) ? { production_policy: doc.production_policy, runtime_spec: { ...doc.runtime_spec }, runtime_context: animeRuntimeContext(doc), runtime_policy_hash: runtimePolicyHash(doc) } : {};
  if (gate === "outline") {
    const file = path.join(dir, "brief.md");
    const brief = readFileSync(file, "utf8");
    const options = outlineOptions(brief);
    // Jev picks when the stance is written and the switch is on; the site approves the review
    // on arrival when the pick clears the thresholds. Otherwise the owner chooses, as before.
    const verdict = await judgeOutline(automationClient(ctx, { attempts: 2 }), slug, brief, options);
    if (verdict.status === "later") ctx.stdout.write(`${slug}: Jev could not judge the outline (${verdict.reason}); it goes up for the owner, and review-push --gate outline again lets Jev pick\n`);
    else if (verdict.status === "owner") ctx.stdout.write(`${slug}: the owner chooses the outline (${verdict.reason})\n`);
    else ctx.stdout.write(`${slug}: ${verdict.pick.note}\n`);
    const { payload, summary } = outlineReview(brief, options, verdict);
    return { gate, content_sha256: await sha256File(file), summary, payload, files: [] };
  }
  if (gate === "script") {
    // Written afresh so the file always matches video.json; the same narrative gives the same
    // bytes, so an approval already given stays valid.
    const file = writeScreenplay(dir, doc);
    const previousCheck = readJson(path.join(workdir, "review", "script-check.json"), null);
    const check = scriptCheckMatches(previousCheck, doc) ? previousCheck : null;
    const scenes = scriptScenes(doc);
    const lines = scenes.reduce((sum, scene) => sum + scene.lines.length, 0);
    const timeline = estimateTimeline(doc);
    const minutes = Number((timeline.total_frames / timeline.fps / 60).toFixed(1));
    return {
      gate,
      content_sha256: await sha256File(file),
      summary: `劇本 ${scenes.length} 場、${lines} 句，約 ${minutes} 分鐘${check?.coverage ? "；查核已對照細綱" : ""}`,
      payload: {
        ...runtimeFields,
        scenes,
        characters: (doc.characters ?? []).map(({ id, name }) => ({ id, name })),
        minutes,
        beats: project.series?.beats ?? null,
        coverage: check?.coverage ?? null,
        continuity_problems: check?.problems ?? (previousCheck ? ["劇本已修改，舊查核報告不適用；請重新查核。"] : []),
        check_status: check ? "current" : previousCheck ? "stale" : "missing",
        // A binge series' checker also names the works the script resembles and its retention
        // verdict (docs/videos/BINGE.md); the worker writes both into script-check.json.
        similar_works: check?.similar_works ?? [],
        retention: check?.retention ?? null,
        narrative_hash: narrativeHash(doc),
      },
      files: [],
    };
  }
  if (gate === "audio") {
    const file = path.join(workdir, ARTIFACTS.timeline);
    const timeline = readJson(file, null);
    const bodyProblems = animeBodyDurationProblems({ doc, timeline, timelineCurrent: timeline?.speech_hash === speechHash(doc, project.lexicon) });
    if (bodyProblems.length) throw new UsageError(bodyProblems.join("; "));
    const problems = audioEvidenceProblems(timeline, workdir);
    if (problems.length) throw new UsageError(`audio cannot be submitted: ${problems.join("; ")}`);
    const measurement = hasAnimePolicy(doc) ? {
      basis: "measured", stage: "audio", policy_hash: runtimePolicyHash(doc), runtime_spec: { ...doc.runtime_spec },
      runtime_context: animeRuntimeContext(doc),
      body_seconds: timeline.total_frames / timeline.fps, body_frames: timeline.total_frames, fps: timeline.fps, speech_hash: timeline.speech_hash,
    } : null;
    const currentCheck = currentAudioCheck(readJson(path.join(workdir, "review", "check.json"), null), timeline);
    const flagsNow = readJson(path.join(workdir, "review", "check-flags.json"), null);
    const check = audioCheck(currentCheck, { ...flagsNow, flags: (flagsNow?.flags ?? []).filter((id) => currentCheck.lines[id]) }, timeline.lines.length);
    // The lines the listener reworded after the retakes (docs/videos/HANDS-OFF.md §旁白), as the
    // worker wrote them: [{ id, before, after, heard }]; the review card lists them.
    const rewrites = readJson(path.join(workdir, "review", "rewrites.json"), []);
    const narration = await upload(request, slug, await preview(ctx, workdir, "narration", path.join(workdir, ARTIFACTS.narration)), "narration", "audio/mp4");
    const seconds = timeline.total_frames / timeline.fps;
    return {
      gate,
      content_sha256: await sha256File(file),
      summary: audioSummary({ seconds, lines: timeline.lines.length, check, rewrites: rewrites.length }),
      payload: { duration_seconds: seconds, ...check, rewrites, ...runtimeFields, ...(measurement ? { runtime_measurement: measurement } : {}) },
      files: [narration],
    };
  }
  if (gate === "final") {
    const file = path.join(workdir, ARTIFACTS.video);
    const sha = await sha256File(file);
    const bodyTimeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
    const checks = readJson(path.join(workdir, ARTIFACTS.checks), null) ?? {};
    if (!isCompilation(doc)) {
      const problems = assembledAudioProblems(bodyTimeline, checks, workdir);
      if (problems.length) throw new UsageError(problems.join("; "));
    }
    const compilation = isCompilation(doc);
    const applied = appliedBranding(checks);
    const rebuild = compilation ? "compile" : "assemble";
    if (!bodyTimeline) throw new UsageError(`timeline.json is missing; run ${rebuild} before review-push --gate final`);
    if (!brandingCurrent(checks, readBranding(workdir))) throw new UsageError(`final.mp4 does not match the selected branding; run ${rebuild} before review-push --gate final`);
    if (applied) {
      if (applied.body_frames !== bodyTimeline.total_frames
          || checks.speech_hash !== bodyTimeline.speech_hash || checks.compilation_hash !== bodyTimeline.compilation_hash) {
        throw new UsageError(`the branded final was built for another body timeline; run ${rebuild} before review-push --gate final`);
      }
      const bodyFile = typeof applied.body_file === "string" && applied.body_file && !path.isAbsolute(applied.body_file) ? path.resolve(workdir, applied.body_file) : null;
      if (!bodyFile || !isInside(bodyFile, workdir) || bodyFile === file || !existsSync(bodyFile)
          || !/^[0-9a-f]{64}$/.test(applied.body_sha256 ?? "") || await sha256File(bodyFile) !== applied.body_sha256) {
        throw new UsageError(`the branded final's retained body does not match checks.json; run ${rebuild} before review-push --gate final`);
      }
    }
    const timeline = presentationTimeline(bodyTimeline, applied);
    // The quality check first (docs/videos/HANDS-OFF.md §自動品管): its report goes up with the
    // review, and only a report of this very final.mp4 counts; the site approves the cut on
    // arrival when every item passed and the owner's switch is on.
    const report = await qualityCheck(ctx, slug, workdir, flags);
    if (await sha256File(file) !== sha) throw new UsageError("final.mp4 changed during the quality check; run review-push --gate final again");
    const qa = report?.final_sha256 === sha ? report : null;
    if (!qa) ctx.stdout.write(`${slug}: no quality check report for this final.mp4; the review goes up without one\n`);
    let runtimeProof = null;
    if (hasAnimePolicy(doc)) {
      try {
        runtimeProof = animeRuntimeProof({ doc, timeline: bodyTimeline, presented: timeline, timelineCurrent: bodyTimeline.speech_hash === speechHash(doc, project.lexicon), checks, finalSha256: sha });
      } catch (error) { throw new UsageError(error.message); }
      if (qa?.policy_hash !== runtimeProof.policy_hash || !isDeepStrictEqual(qa.runtime_spec, runtimeProof.runtime_spec) || !isDeepStrictEqual(qa.runtime_context, runtimeProof.runtime_context)) throw new UsageError("long-anime final QA needs the current runtime policy and series context; run qa again");
    }
    // The owner's language choice, when there is one already (docs/videos/LANGUAGES.md), with
    // the narration's own locale and zh-TW, which every choice keeps (alwaysLocales).
    const languages = readLanguages(workdir);
    const { metadata } = composeMetadata({ doc, timeline, translations: project.translations, pack: project.pack, locales: metadataLocalesOf(languages, narrationLocale(doc)) });
    // Pictures kept with the judge's remarks once their prompt fixes were spent (keyframes
    // --accept-best): the owner looks at the cut whatever the quality check says, and the
    // card lists them. The worker asks for the manual review too (automation/flow.mjs gate).
    // The summary and the reason name the first few and count the rest (namedPictures): every
    // one of them is in accepted_pictures with what the judge said, which review-push cuts to
    // a few lines a picture where it posts the review (fitPayload).
    const acceptedPictures = acceptedPicturesOf(doc, workdir);
    const keptIds = namedPictures(acceptedPictures.map((picture) => picture.id));
    const manual = manualReview || acceptedPictures.length > 0;
    const manualReason = acceptedPictures.length
      ? `有 ${acceptedPictures.length} 張插圖未通過 judge（${keptIds}），需站主審看成片；機械品管僅供參考。`
      : applied ? "已重製頻道片頭與片尾，需站主重新審看成片與銜接；機械品管僅供參考。" : "此成片明確要求站主重新審看；機械品管僅供參考。";
    const files = [await upload(request, slug, await preview(ctx, workdir, "preview", file, { compilation }), "preview", "video/mp4")];
    const sheet = path.join(workdir, ARTIFACTS.contactSheet);
    if (existsSync(sheet)) files.push(await upload(request, slug, sheet, "contact_sheet", "image/png"));
    const thumbnail = path.join(workdir, "thumbnail.jpg");
    if (existsSync(thumbnail)) {
      files.push(await upload(request, slug, thumbnail, "thumbnail", "image/jpeg"));
      // B and C for Studio's 「測試與比較」 go up beside A (role thumbnail-b), as render listed them.
      for (const variant of thumbnailVariants(readJson(path.join(workdir, ARTIFACTS.frames), null))) {
        const own = path.join(workdir, variant);
        if (existsSync(own)) files.push(await upload(request, slug, own, variantRole(variant), "image/jpeg"));
      }
    }
    // The dub tracks made so far go up beside the cut, so the owner can hear them on the site
    // (docs/videos/DUBS.md). Only the m4a form: it is the audio type the review store takes.
    // A compilation has none of its own: its episodes' dubs are theirs.
    const { dubs, skipped: skippedDubs } = compilation ? { dubs: [], skipped: {} } : dubsForUpload(project, workdir, bodyTimeline.speech_hash, chosenLocales(languages, "dub") ?? undefined);
    const dubEntries = {};
    for (const dub of dubs) {
      const role = dub.format === "m4a" ? dubRole(dub.locale) : null;
      if (role) files.push(await upload(request, slug, dub.file, role, "audio/mp4"));
      dubEntries[dub.locale] = { status: "ready", format: dub.format, tempo_max: dub.tempo_max, file_role: role };
    }
    for (const [locale, reason] of Object.entries(skippedDubs)) dubEntries[locale] = { status: "skipped", reason };
    const seconds = timeline.total_frames / timeline.fps;
    return {
      gate,
      content_sha256: sha,
      summary: `成片 ${formatClock(Math.round(seconds))}，${qa ? qaSummary(qa) : `自動檢查${checks.ok ? "全部通過" : `有 ${(checks.problems ?? []).length} 項問題`}；${qaSummary(null)}`}${dubs.length ? `，配音 ${dubs.map((dub) => dub.locale).join("、")}` : ""}${acceptedPictures.length ? `；${acceptedPictures.length} 張插圖未通過 judge（${keptIds}），需站主審看` : manual ? "；需站主重新審看" : ""}`,
      payload: {
        duration_seconds: seconds,
        ...runtimeFields,
        ...(runtimeProof ? { runtime_proof: runtimeProof } : {}),
        checks: { ok: Boolean(checks.ok), problems: checks.problems ?? [] },
        chapters: metadata.chapters.map((chapter) => ({ time: chapter.at, title: chapter.title })),
        metadata: { [metadata.default_language]: { title: metadata.title, description: metadata.description }, ...metadata.localizations },
        ...(applied ? { branding_hash: applied.hash } : {}),
        // The server auto-approves final only from payload.qa. This one submission keeps its
        // machine report as evidence while explicitly requesting the owner's fresh review.
        ...(manual ? { manual_review: true, manual_review_reason: manualReason, ...(qa ? { manual_review_qa: qa } : {}) } : qa ? { qa } : {}),
        ...(acceptedPictures.length ? { accepted_pictures: acceptedPictures } : {}),
        ...(Object.keys(dubEntries).length ? { dubs: dubEntries } : {}),
        ...(compilation ? { compilation: { series: doc.compilation.series, episodes: doc.compilation.episodes, total_frames: timeline.total_frames } } : {}),
      },
      files,
    };
  }
  if (gate === "languages") return languagesSubmission({ request, project, workdir, slug });
  if (gate === "dubs") {
    const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
    const { dubs, skipped } = dubsForUpload(project, workdir, timeline?.speech_hash, chosenLocales(readLanguages(workdir), "dub") ?? undefined);
    if (!dubs.length && !Object.keys(skipped).length) throw new ReviewError("no dub track to send yet: run dub first", { who: "owner" });
    const files = [];
    const locales = {};
    for (const dub of dubs) {
      const role = dub.format === "m4a" ? dubRole(dub.locale) : null;
      if (role) files.push(await upload(request, slug, dub.file, role, "audio/mp4"));
      locales[dub.locale] = { status: "ready", file: path.basename(dub.file), format: dub.format, tempo_max: dub.tempo_max, file_role: role, sha256: await sha256File(dub.file) };
    }
    for (const [locale, reason] of Object.entries(skipped)) locales[locale] = { status: "skipped", reason };
    // The manifest is what the owner's approval binds to: these tracks, as sent.
    const file = GATES.dubs({ workdir });
    atomicWrite(file, `${JSON.stringify({ speech_hash: timeline?.speech_hash ?? null, locales }, null, 2)}\n`);
    const ready = dubs.map((dub) => dub.locale);
    const gaveUp = Object.keys(skipped);
    return {
      gate,
      content_sha256: await sha256File(file),
      summary: `配音音軌：${ready.length ? ready.join("、") : "無"}${gaveUp.length ? `；做不出來：${gaveUp.join("、")}` : ""}。到 Studio「語言」上傳後按核准`,
      payload: { locales },
      files,
    };
  }
  return publishSubmission({ request, workdir, slug, project, compilation: isCompilation(doc) });
}

/** The publish summary's note for a compilation: the size, and that the file is downloaded from the site. */
export function downloadNote(bytes) {
  return `合集 ${(bytes / 1024 ** 3).toFixed(2)} GB，成片從網站下載後上傳`;
}

// The Traditional Chinese names of a language's parts, for a batch's summary line.
const PART_NAMES = { metadata: "標題說明", captions: "CC", dub: "配音" };

/** Keep every locale and its upload instruction visible; full skip reasons stay in the payload. */
function languagesSummary(locales) {
  const dubbed = Object.values(locales).some((entry) => entry.dub === "ready");
  const ending = dubbed ? "配音到 Studio「語言」上傳後按「已在 Studio 上傳配音」" : "沒有要你上傳的配音";
  const summarize = (reasons) => {
    const said = Object.entries(locales).map(([locale, entry]) => {
      const made = Object.entries(PART_NAMES).flatMap(([part, name]) => {
        if (entry[part] === "ready") return [name];
        if (part === "dub" && entry.dub?.status === "skipped") return [`${name}跳過${reasons ? `（${entry.dub.reason || "沒有寫原因"}）` : ""}`];
        return [];
      });
      return `${locale} ${made.join("、") || "還在做"}`;
    });
    return `語言：${said.join("；")}。${ending}`;
  };
  const detailed = summarize(true);
  return [...detailed].length <= MAX_REVIEW_SUMMARY_LENGTH ? detailed : summarize(false);
}

/**
 * The languages gate (docs/videos/LANGUAGES.md): one batch of the languages the owner chose, as
 * far as they are made. For each chosen language, each chosen part's state and file: the title
 * and description as `description_<locale>` and the captions as `captions_<locale>`, both from
 * the upload package (so `package` runs first); the dub track as `dub_<locale>` (the m4a form,
 * the audio type the store takes) or the reason the worker gave it up. A part not made yet is
 * left out, which the site reads as still in the making. The site approves a batch without a dub
 * track on arrival; one with a track waits for the owner to upload it in Studio and say so. The
 * approval binds to the manifest written here of what was sent.
 */
async function languagesSubmission({ request, project, workdir, slug }) {
  const languages = readLanguages(workdir);
  if (!languages) throw new ReviewError(`no language choice in ${LANGUAGES_FILE}; the worker writes it from /admin/videos`, { who: "owner" });
  const chosen = Object.entries(languages.locales);
  if (!chosen.length) throw new ReviewError("the owner chose Traditional Chinese only; there is no language batch to send", { who: "owner" });
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const { dubs, skipped } = dubsForUpload(project, workdir, timeline?.speech_hash, chosenLocales(languages, "dub"));
  const files = [];
  const locales = {};
  for (const [locale, choice] of chosen) {
    const entry = {};
    const description = path.join(workdir, UPLOAD_DIR, `description.${locale}.txt`);
    if (choice.metadata && existsSync(description)) {
      files.push(await upload(request, slug, description, `description_${locale}`, "text/plain"));
      entry.metadata = "ready";
    }
    const captions = path.join(workdir, UPLOAD_DIR, "captions", `${locale}.srt`);
    if (choice.captions && existsSync(captions)) {
      files.push(await upload(request, slug, captions, `captions_${locale}`, "text/plain"));
      entry.captions = "ready";
    }
    if (choice.dub) {
      const dub = dubs.find((each) => each.locale === locale);
      if (dub) {
        const role = dub.format === "m4a" ? dubRole(locale) : null;
        if (role) files.push(await upload(request, slug, dub.file, role, "audio/mp4"));
        Object.assign(entry, { dub: "ready", file: path.basename(dub.file), format: dub.format, tempo_max: dub.tempo_max, file_role: role, sha256: await sha256File(dub.file) });
      } else if (skipped[locale] !== undefined) {
        entry.dub = { status: "skipped", reason: skipped[locale] };
      }
    }
    locales[locale] = entry;
  }
  const file = GATES.languages({ workdir });
  atomicWrite(file, `${JSON.stringify({ speech_hash: timeline?.speech_hash ?? null, decided_at: languages.decided_at, locales }, null, 2)}\n`);
  return {
    gate: "languages",
    content_sha256: await sha256File(file),
    summary: languagesSummary(locales),
    payload: { locales },
    files,
  };
}

/**
 * The publish gate (docs/videos/HANDS-OFF.md §上傳包與「可以上架」): the package check's report,
 * what the 「可以上架」 card shows, and every file of the package attached, so the owner downloads
 * it from the site. The site approves the confirmation on arrival when the four items pass and
 * the owner's switch is on; final.mp4 goes up in parts like the preview. A compilation's
 * final.mp4 is gigabytes and stays home (docs/videos/BINGE.md): the payload says where it is
 * and how big, and the site serves the download from the work directory instead.
 */
async function publishSubmission({ request, workdir, slug, project, compilation = false }) {
  const file = path.join(workdir, ARTIFACTS.upload);
  const { report, files: listed, metadata, finalSha256 } = await readPackageReport(workdir);
  if (!metadata) throw new ReviewError("upload/metadata.json is missing; run package first", { who: "owner" });
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const doc = project.doc;
  let runtimeProof = null;
  if (hasAnimePolicy(doc)) {
    const checks = readJson(path.join(workdir, ARTIFACTS.checks), null);
    if (!brandingCurrent(checks, readBranding(workdir))) throw new UsageError("long-anime package has another selected OP/ED; run assemble and package again");
    try {
      runtimeProof = animeRuntimeProof({ doc, timeline, presented: presentationTimeline(timeline, appliedBranding(checks)), timelineCurrent: timeline?.speech_hash === speechHash(doc, project.lexicon), checks, finalSha256 });
    } catch (error) { throw new UsageError(error.message); }
    if (!isDeepStrictEqual(metadata.runtime_proof, runtimeProof)) throw new UsageError("long-anime upload metadata needs the current measured runtime proof; run package again");
  }
  const files = [];
  for (const entry of packageFiles(listed.keys())) {
    if (compilation && entry.role === "final") continue;
    files.push(await upload(request, slug, path.join(workdir, UPLOAD_DIR, entry.path), entry.role, entry.content_type));
  }
  const minutes = timeline?.total_frames && timeline.fps ? Math.round((timeline.total_frames / timeline.fps / 60) * 10) / 10 : null;
  const checklist = existsSync(path.join(workdir, UPLOAD_CHECKLIST)) ? uploadItems(readFileSync(path.join(workdir, UPLOAD_CHECKLIST), "utf8")) : [];
  const bytes = listed.get("final.mp4") ?? null;
  const download = compilation ? { path: "upload/final.mp4", bytes, sha256: finalSha256 } : null;
  const note = download && bytes !== null ? `：${downloadNote(bytes)}` : "";
  return {
    gate: "publish",
    content_sha256: await sha256File(file),
    summary: report.ok ? `${packageSummary(report)}${note ? `${note}；` : "："}請確認可以上架` : `${packageSummary(report)}${note}`,
    payload: {
      package: report,
      ...(runtimeProof ? { production_policy: doc.production_policy, runtime_spec: { ...doc.runtime_spec }, runtime_context: runtimeProof.runtime_context, runtime_policy_hash: runtimeProof.policy_hash, runtime_proof: runtimeProof, final_media_sha256: finalSha256 } : {}),
      minutes,
      chapters: (metadata.chapters ?? []).length,
      locales: packageLocales(metadata),
      zh: { title: metadata.title ?? "", description: metadata.description ?? "", tags: metadata.tags ?? [] },
      disclosure: { synthetic: metadata.contains_synthetic_media === true, reason: typeof metadata.disclosure_reason === "string" ? metadata.disclosure_reason : "" },
      checklist,
      ...(download ? { download, episodes: Array.isArray(metadata.episodes) ? metadata.episodes.map((episode) => episode.slug) : [] } : {}),
    },
    files,
  };
}

/**
 * The look gate: one review per character, its candidate sheets as files, the owner picks one
 * (docs/videos/DRAMA.md). Every review is bound to characters/manifest.json.
 */
async function lookSubmissions({ request, project, workdir }) {
  const { doc } = project;
  const file = path.join(workdir, ARTIFACTS.characters);
  const manifest = readJson(file, null);
  if (!manifest?.characters) throw new ReviewError("characters/manifest.json is missing; run look first", { who: "owner" });
  const sha = await sha256File(file);
  const bodies = [];
  for (const [id, entry] of Object.entries(manifest.characters)) {
    const character = doc.characters?.find((each) => each.id === id);
    const files = [];
    const options = [];
    for (const candidate of entry.candidates ?? []) {
      const role = `candidate_${optionKey(candidate.n).toLowerCase()}`;
      files.push(await upload(request, doc.slug, path.join(workdir, candidate.file), role, imageType(candidate.file)));
      options.push({ key: optionKey(candidate.n), index: candidate.n, file_role: role, judge: { overall: candidate.judge?.overall ?? null, problems: candidate.judge?.problems ?? [] } });
    }
    const suggested = entry.suggested ? optionKey(entry.suggested) : null;
    bodies.push({
      gate: "look",
      subject: id,
      content_sha256: sha,
      summary: `${entry.name} 的設定圖 ${options.length} 張${suggested ? `，judge 建議 ${suggested}` : "，judge 沒有推薦"}`,
      payload: {
        subject: id,
        character: { name: entry.name, description: character?.appearance ?? "", voice: character?.voice ? `${character.voice.provider}:${character.voice.name}` : "" },
        options,
        suggested,
        prompt: entry.prompt ?? "",
      },
      files,
    });
  }
  return bodies;
}

// Mirrors MAX_REVIEW_FILES in apps/api/app/video_reviews/schemas.py: the most files one review takes.
export const MAX_REVIEW_FILES = 48;
// The shots on a page of the storyboard's contact sheet (docs/videos/STORY.md); read only when a
// manifest lists its pages without the shots on each.
const SHEET_PAGE_SHOTS = 24;

/**
 * The storyboard's contact sheets as [{ file, shots }] in page order, each file there: the pages
 * the keyframes manifest lists in contact_sheets ({ file, shots }, or a bare file holding the next
 * 24 shots), else the one sheet of every shot. `ids` are the drawn shots, in order.
 */
export function storyboardSheets(manifest, ids, workdir) {
  const pages = Array.isArray(manifest.contact_sheets) && manifest.contact_sheets.length
    ? manifest.contact_sheets.map((page, index) => ({
        file: typeof page === "string" ? page : page?.file,
        shots: Array.isArray(page?.shots) ? page.shots : ids.slice(index * SHEET_PAGE_SHOTS, (index + 1) * SHEET_PAGE_SHOTS),
      }))
    : [{ file: "keyframes/contact-sheet.png", shots: ids }];
  return pages.filter((page) => typeof page.file === "string" && existsSync(path.join(workdir, page.file))).slice(0, MAX_REVIEW_FILES);
}

/**
 * The pictures of an illustrated video kept with the judge's remarks once their prompt fixes were
 * spent (media/keyframes.mjs --accept-best; `accepted_with_problems` in keyframes/manifest.json),
 * as [{ id, problems }] in shot order; none for any other video, or when every shot passed.
 */
export function acceptedPicturesOf(doc, workdir) {
  if (!illustrated(doc)) return [];
  const manifest = readJson(path.join(workdir, ARTIFACTS.keyframes), null);
  return drawnShotScenes(doc)
    .filter((scene) => Array.isArray(manifest?.shots?.[scene.id]?.accepted_with_problems))
    .map((scene) => ({ id: scene.id, problems: manifest.shots[scene.id].accepted_with_problems }));
}

/**
 * The storyboard gate, bound to keyframes/manifest.json: every keyframe and the contact sheet,
 * with the judge's verdicts. When that is more files than a review takes (a brand story has 85 to
 * 100 shots, docs/videos/STORY.md), the contact sheets go up instead, then the keyframes of the
 * shots left for a prompt fix, as many as fit. The payload still lists every shot, `file_role`
 * null for one whose keyframe stayed home; `sheets` names each sheet's role and shots, and
 * `omitted` counts the keyframes that stayed home.
 */
async function storyboardSubmission({ request, project, workdir }) {
  const { doc } = project;
  const file = path.join(workdir, ARTIFACTS.keyframes);
  const manifest = readJson(file, null);
  if (!manifest?.shots) throw new ReviewError("keyframes/manifest.json is missing; run keyframes first", { who: "owner" });
  const problemsWithPictures = await keyframeProblems({ doc, manifest, workdir, allowNeedsReview: true });
  if (problemsWithPictures.length) throw new ReviewError(`${problemsWithPictures.join("; ")}; run keyframes first`, { who: "owner" });
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const seconds = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, Math.round(((scene.end_frame - scene.start_frame) / (timeline.fps || 30)) * 10) / 10]));
  // A shot's role is its place in the video (shot_07) whichever keyframes go up.
  const drawn = [...drawnShotScenes(doc).entries()];
  const sheets = storyboardSheets(manifest, drawn.map(([, scene]) => scene.id), workdir)
    .map((sheet, index, all) => ({ ...sheet, role: all.length === 1 ? "contact_sheet" : `contact_sheet_${String(index + 1).padStart(2, "0")}` }));
  const whole = drawn.length + sheets.length <= MAX_REVIEW_FILES;
  const files = [];
  const sendSheets = async () => {
    for (const sheet of sheets) files.push(await upload(request, doc.slug, path.join(workdir, sheet.file), sheet.role, imageType(sheet.file)));
  };
  if (!whole) await sendSheets();
  const shots = [];
  for (const [index, scene] of drawn) {
    const shot = manifest.shots[scene.id];
    const role = `shot_${String(index + 1).padStart(2, "0")}`;
    const sent = whole || (Boolean(shot.needs_review) && files.length < MAX_REVIEW_FILES);
    if (sent) files.push(await upload(request, doc.slug, path.join(workdir, shot.file), role, imageType(shot.file)));
    // A picture kept with the judge's remarks once its prompt fixes were spent (keyframes
    // --accept-best): sent as accepted, not as a review need, so the board can approve itself
    // (apps/api/app/video_automation/settings.py storyboard_check_passed); the owner sees it on
    // the final cut, which goes up for a manual review. What the judge said of it, here and on
    // the list below, is cut to a few lines where review-push posts the review (fitPayload).
    const accepted = Array.isArray(shot.accepted_with_problems);
    shots.push({
      id: scene.id,
      chapter: scene.chapter ?? null,
      prompt: scene.data?.prompt ?? "",
      seconds: seconds.get(scene.id) ?? null,
      file_role: sent ? role : null,
      needs_review: !accepted && Boolean(shot.needs_review || shot.judge?.passed === false),
      ...(accepted ? { accepted: true } : {}),
      complete: true,
      file_sha256: shot.sha256,
      ...(scene.data?.end_frame?.prompt ? { end_frame_sha256: shot.end_frame.sha256 } : {}),
      judge: { overall: shot.judge?.overall ?? null, problems: shot.judge?.problems ?? [] },
    });
  }
  if (whole) await sendSheets();
  // The lowest score among the shots the judge's word stands for: an accepted shot's is on its
  // own list, and when every shot was accepted there is none.
  const scores = shots.filter((shot) => !shot.accepted).map((shot) => shot.judge.overall).filter((score) => typeof score === "number");
  const lowest = scores.length ? Math.min(...scores) : null;
  const waiting = shots.filter((shot) => shot.needs_review);
  const accepted = shots.filter((shot) => shot.accepted).map((shot) => ({ id: shot.id, overall: shot.judge.overall, problems: manifest.shots[shot.id].accepted_with_problems }));
  // Only the shots left for a prompt fix carry problems here: a board the judge passed whole
  // may be approved automatically when the owner allows it.
  const problems = [...new Set(waiting.flatMap((shot) => shot.judge.problems))];
  // Every keyframe with at most one sheet is the review as it always was; any other names its
  // sheets, so the card can point to the page of a shot listed without its keyframe.
  const asBefore = whole && sheets.length <= 1;
  const unshown = waiting.filter((shot) => !shot.file_role).length;
  const board = asBefore ? "" : `（${sheets.length ? `聯絡表 ${sheets.length} 頁` : "沒有聯絡表"}）`;
  return {
    gate: "storyboard",
    content_sha256: await sha256File(file),
    summary: `分鏡 ${shots.length} 鏡${board}${lowest === null ? "" : `，judge 最低 ${lowest}/10`}${waiting.length ? `，${waiting.length} 鏡待修` : ""}${unshown ? `，其中 ${unshown} 鏡沒附單張圖` : ""}${accepted.length ? `，${accepted.length} 鏡保留（judge 未過，成片時站主審看）` : ""}`,
    payload: {
      expected_shots: drawn.map(([, scene]) => ({ id: scene.id, end_frame_required: Boolean(scene.data?.end_frame?.prompt) })),
      shots,
      judge: { overall: lowest, problems },
      ...(accepted.length ? { accepted } : {}),
      duplicates: manifest.duplicates ?? [],
      ...(asBefore ? {} : { sheets: sheets.map((sheet) => ({ role: sheet.role, shots: sheet.shots })), omitted: shots.filter((shot) => !shot.file_role).length }),
    },
    files,
  };
}

/** Everything a gate submits: several reviews for the look, one for the others. */
async function submissions(gate, places) {
  if (gate === "look") return lookSubmissions(places);
  if (gate === "storyboard") return [await storyboardSubmission(places)];
  return [await submission(gate, places)];
}

function common(args, { allowManualReview = false } = {}) {
  const values = parseArgs({ args, options: { slug: { type: "string" }, workdir: { type: "string" }, gate: { type: "string" }, "report-only": { type: "boolean" }, "manual-review": { type: "boolean" } }, strict: true }).values;
  if (!values.slug) throw new UsageError("needs --slug");
  if (values.gate && !REVIEW_GATES.includes(values.gate)) throw new UsageError(`--gate must be one of ${REVIEW_GATES.join(", ")}`);
  if (values["manual-review"] && (!allowManualReview || values.gate !== "final" || values["report-only"])) throw new UsageError("--manual-review requires review-push with explicit --gate final and cannot use --report-only");
  return values;
}

function fail(error, ctx) {
  if (error instanceof ToolMissing) {
    ctx.stderr.write(`${error.message}\n`);
    return ctx.EXIT.missing;
  }
  // The judge is asked through the automation client; its errors say who can fix them too.
  if (!(error instanceof ReviewError || error instanceof AutomationError)) throw error;
  ctx.stderr.write(`${error.message}\n`);
  // Bad review/file payloads cannot recover by waiting. A failed project report or read still
  // stops the round: the worker could not reliably report a blocked state on that same route.
  // A payload this command found too large itself (fitPayload) is one the site would refuse so.
  if (error instanceof ReviewError && error.submission && ([413, 422].includes(error.status) || error.code === "payload_too_large")) return ctx.EXIT.lint;
  return error.who === "owner" ? ctx.EXIT.owner : ctx.EXIT.external;
}

export async function reviewPush(args, ctx) {
  const values = common(args, { allowManualReview: true });
  const dir = docDir(values.slug, ctx.root);
  const project = loadProject({ slug: values.slug, root: ctx.root });
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: values.slug, root: ctx.root, home: ctx.home });
  try {
    const request = client(ctx);
    const status = await pipelineStatus({ slug: values.slug, root: ctx.root, workdir });
    const sourceGuide = sourceGuideOf(project.doc);
    await request("PUT", values.slug, {
      json: {
        title: project.doc.youtube?.title || project.doc.slug,
        stage: status.next ? status.next.id.slice(0, 40) : "done",
        checklist: checklistFrom(status.steps),
        youtube_video_id: project.doc.youtube?.video_id || null,
        // The site reads the format at its gates (a drama's storyboard rule is not a slides video's,
        // docs/videos/ILLUSTRATED.md); the worker reports it too (automation/flow.mjs).
        format: project.doc.format ?? "slides",
        ...(sourceGuide ? { source_guide: sourceGuide } : {}),
        // The site files an unfiled video under it and never overwrites the owner's choice.
        ...(VIDEO_CATEGORIES.includes(project.doc.category) ? { category: project.doc.category } : {}),
        // An episode names its series and number; a compilation only its series (docs/videos/BINGE.md).
        ...(isCompilation(project.doc) ? { series_slug: project.doc.compilation.series } : project.doc.series ? { series_slug: project.doc.series.slug, episode_number: project.doc.series.episode } : {}),
      },
    });
    if (values["report-only"]) {
      ctx.stdout.write(`${values.slug}: reported to /admin/videos; nothing submitted\n`);
      return ctx.EXIT.ok;
    }
    const gate = values.gate ?? (await nextGate({ docDir: dir, workdir }, workdir, project.doc));
    if (!gate) {
      ctx.stdout.write(`${values.slug}: reported; nothing waits for the owner right now\n`);
      return ctx.EXIT.ok;
    }
    const bodies = await submissions(gate, { ctx, request, project, workdir, dir, flags: values.workdir ? ["--workdir", values.workdir] : [], manualReview: values["manual-review"] ?? false });
    for (const candidate of bodies) {
      // An owner renewal invalidates old downstream approvals. Resolve its identity from
      // the site, then verify bytes/timing before adding the new final-review binding.
      const remote = ["publish", "languages", "dubs"].includes(candidate.gate) ? await request("GET", values.slug) : null;
      const bound = await bindRenewalSubmission({ body: candidate, remote, project, workdir, request, upload });
      // Every review this command sends leaves through here, so none carries a summary the
      // site would refuse for its length, nor a payload it would refuse for its size.
      const { body, bytes, lines } = fitPayload({ ...bound, summary: fitSummary(bound.summary) });
      const what = body.subject ? `${gate} (${body.subject})` : gate;
      if (lines !== null) ctx.stdout.write(`${values.slug}: ${what}: the judge's remarks on the kept pictures were ${lines ? `cut to ${lines} lines a picture` : "left out"} to keep the review's payload within the site's limit (${bytes} bytes now); keyframes/manifest.json has them all\n`);
      const review = await request("POST", `${values.slug}/reviews`, { json: body });
      ctx.stdout.write(`${values.slug}: ${what} submitted for review (${review.status}); the owner decides on /admin/videos, then run review-pull\n`);
    }
    return ctx.EXIT.ok;
  } catch (error) {
    return fail(error, ctx);
  }
}

/**
 * The owner's look decisions: each approved review picks one character's sheet. The picks go
 * to characters/choice.json, and the look gate is approved once every character has a sheet
 * (chosen, or the judge's suggestion when the owner approved without choosing).
 */
async function recordLook(reviews, { dir, workdir, now, doc = null, ctx = null }) {
  const file = GATES.look({ docDir: dir, workdir });
  const manifest = readJson(file, null);
  if (!manifest?.characters) return { message: "approved, but characters/manifest.json is gone; run look again", waiting: 0 };
  const sha = await sha256File(file);
  const usable = reviews.filter((review) => review.content_sha256 === sha && review.subject && manifest.characters[review.subject]);
  if (!usable.length) return { message: "approved a version that has since changed; run review-push --gate look again", waiting: 0 };
  const choiceFile = path.join(workdir, ARTIFACTS.characterChoice);
  const previous = readJson(choiceFile, null);
  const chosen = previous?.look_hash === manifest.look_hash ? { ...(previous.chosen ?? {}) } : {};
  for (const review of usable) {
    const option = (review.payload?.options ?? []).find((each) => each.key === review.choice);
    // Approved without a pick means the judge's suggestion is fine.
    const pick = option?.index ?? (review.choice ? review.choice.charCodeAt(0) - 64 : null) ?? manifest.characters[review.subject].suggested;
    if (pick) chosen[review.subject] = pick;
  }
  atomicWrite(choiceFile, `${JSON.stringify({ look_hash: manifest.look_hash, chosen, chosen_at: now.toISOString() }, null, 2)}\n`);
  // Every character needs the owner's decision, not just a suggestion.
  const missing = Object.keys(manifest.characters).filter((id) => !chosen[id]);
  const picks = Object.entries(chosen).map(([id, n]) => `${id} = ${optionKey(n)}`).join(", ");
  if (missing.length) return { message: `${picks || "no sheet chosen yet"}; waiting for ${missing.join(", ")}`, waiting: missing.length };
  if (readApprovals(workdir).approvals.some((entry) => entry.gate === "look" && entry.sha256 === sha)) return { message: `already recorded (${picks})`, waiting: 0 };
  const decided = usable.map((review) => review.decided_at).filter(Boolean).sort().at(-1) ?? now.toISOString();
  await approve({ gate: "look", docDir: dir, workdir, now, note: `approved on /admin/videos at ${decided}; chose sheets ${picks}` });
  if (doc?.series && ctx) {
    // The chosen sheets go to the series' store, so the next episode reuses them (docs/videos/SERIES.md).
    const kept = keepSheets({ workBase: resolveWorkBase({ env: ctx.env, root: ctx.root, home: ctx.home }), workdir, seriesSlug: doc.series.slug, doc, manifest, chosen, now });
    return { message: `approval recorded (${picks}); ${kept} sheets kept for the series`, waiting: 0 };
  }
  return { message: `approval recorded (${picks})`, waiting: 0 };
}

export async function reviewPull(args, ctx) {
  const values = common(args);
  const dir = docDir(values.slug, ctx.root);
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: values.slug, root: ctx.root, home: ctx.home });
  try {
    const project = await client(ctx)("GET", values.slug);
    let waiting = 0;
    const looks = [];
    // Oldest first, so the newest decision on a gate is the one approvals.json ends with.
    for (const review of [...project.reviews].reverse()) {
      if (values.gate && review.gate !== values.gate) continue;
      const what = review.subject ? `${review.gate} (${review.subject})` : review.gate;
      if (review.status === "pending") {
        waiting += 1;
        ctx.stdout.write(`${what}: waiting for the owner\n`);
      } else if (review.status === "rejected") {
        ctx.stdout.write(`${what}: sent back — ${review.note ?? ""}\n`);
      } else if (review.status === "approved" && review.gate === "look") {
        looks.push(review);
      } else if (review.status === "approved") {
        const message = await recordApproval(review, { dir, workdir, now: ctx.now() });
        ctx.stdout.write(`${what}: ${message}\n`);
      }
    }
    if (looks.length) {
      const doc = existsSync(path.join(dir, "video.json")) ? loadProject({ slug: values.slug, root: ctx.root }).doc : null;
      const result = await recordLook(looks, { dir, workdir, now: ctx.now(), doc, ctx });
      waiting += result.waiting;
      ctx.stdout.write(`look: ${result.message}\n`);
    }
    return waiting ? ctx.EXIT.owner : ctx.EXIT.ok;
  } catch (error) {
    return fail(error, ctx);
  }
}

/** Record a site approval locally, only for the exact file the owner saw. */
async function recordApproval(review, { dir, workdir, now }) {
  const file = GATES[review.gate]({ docDir: dir, workdir });
  if (!existsSync(file) || (await sha256File(file)) !== review.content_sha256) {
    return "approved a version that has since changed; run review-push again";
  }
  let hash = null;
  if (ANIME_APPROVAL_GATES.has(review.gate)) {
    hash = approvalRuntimePolicyHash(review.gate, dir);
    const remoteHash = review.payload?.runtime_policy_hash ?? null;
    if (hash !== remoteHash || (hasAnimePolicy(review.payload) && !remoteHash)) return "approved a runtime policy or episode context that has since changed; run review-push again";
  }
  if (review.gate === "audio") {
    const problems = audioEvidenceProblems(readJson(file), workdir);
    if (problems.length) return `approval not recorded: ${problems.join("; ")}`;
  }
  if (review.gate === "storyboard") {
    const doc = readJson(path.join(dir, "video.json"), null);
    const problems = await keyframeProblems({ doc, manifest: readJson(file), workdir, allowNeedsReview: true });
    if (!doc || problems.length) return `approval not recorded: ${problems.join("; ") || "video.json is missing"}`;
  }
  if (readApprovals(workdir).approvals.some((entry) => entry.gate === review.gate && entry.sha256 === review.content_sha256 && (!ANIME_APPROVAL_GATES.has(review.gate) || (entry.runtime_policy_hash ?? null) === hash))) {
    return "already recorded";
  }
  const note = `approved on /admin/videos at ${review.decided_at}${review.choice ? `; chose outline ${review.choice}` : ""}${review.note ? `; ${review.note}` : ""}`;
  await approve({ gate: review.gate, docDir: dir, workdir, now, note, ...(ANIME_APPROVAL_GATES.has(review.gate) ? { expected_runtime_policy_hash: hash } : {}) });
  // The site approves a package whose check passed by itself, and nothing here knows of an
  // upload: say what was approved and leave YouTube out of it.
  if (review.gate === "publish") return `upload package approved (metadata.json ${review.content_sha256.slice(0, 12)}); this records the approval only, not a YouTube upload — upload/UPLOAD.md has the Studio steps`;
  if (review.gate === "languages") return "the language batch is recorded; its dub tracks, if any, are up in YouTube Studio";
  if (review.gate === "dubs") return "the owner uploaded these dub tracks in YouTube Studio";
  return `approval recorded${review.choice ? ` (outline ${review.choice})` : ""}`;
}
