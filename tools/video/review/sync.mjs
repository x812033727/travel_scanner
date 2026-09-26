// `review-push` and `review-pull`: the owner reviews on the site's /admin/videos, not in chat.
//
// `review-push` reports where a video is and submits the next thing the owner must decide: the
// outline (brief.md with its options), the narration (a small AAC copy plus the Jev check), the
// final cut (a 720p copy, the contact sheet, the thumbnail, titles in every locale), or the
// upload package. Each is bound to the SHA-256 of the file its approval gate covers, so an
// approval on the site means exactly the file the pipeline has. `review-pull` reads the owner's
// decisions back and records an approval only when that hash still matches the local file.
import { closeSync, existsSync, mkdirSync, openSync, readFileSync, readSync, statSync } from "node:fs";
import path from "node:path";
import { parseArgs } from "node:util";

import { locateFfmpeg, runTool, ToolMissing } from "../assemble/ffmpeg.mjs";
import { GATES, approvalState, approve, readApprovals, sha256File } from "../core/approvals.mjs";
import { isDrama, shotScenes } from "../core/drama.mjs";
import { atomicWrite, docDir, readJson, resolveWorkBase, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { dubRole, dubsForUpload } from "../core/stages.mjs";
import { ARTIFACTS, loadProject, pipelineStatus } from "../core/state.mjs";
import { narrativeHash, scriptScenes, writeScreenplay } from "../core/screenplay.mjs";
import { estimateTimeline, formatClock } from "../core/timeline.mjs";
import { keepSheets } from "../media/series-store.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { USER_AGENT } from "../tts/client.mjs";

// Mirrors PART_BYTES in apps/api/app/video_reviews/storage.py: under nginx's 6 MB request cap.
export const PART_BYTES = 4 * 1024 * 1024;
// look and storyboard are the drama format's gates (docs/videos/DRAMA.md); script is a series
// episode's screenplay, read before any image or clip is paid for (docs/videos/SERIES.md); dubs is
// the owner's "uploaded" on the dub tracks (docs/videos/DUBS.md), sent only when asked for with --gate.
export const REVIEW_GATES = ["outline", "script", "look", "audio", "storyboard", "final", "publish", "dubs"];
const UPLOAD_CHECKLIST = path.join("upload", "UPLOAD.md");

// The owner reads the site in Traditional Chinese; status's step ids are English. Every step of
// both formats (core/state.mjs SLIDES_STEPS and DRAMA_STEPS) has a label here.
export const STEP_LABELS = {
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
  "captions written": "五語字幕",
  "final video approved": "成片核准",
  "upload package": "上傳包",
  "on YouTube": "已上 YouTube",
};

export class ReviewError extends Error {
  constructor(message, { status = 0, code = "", who = "service" } = {}) {
    super(message);
    this.status = status;
    this.code = code;
    this.who = who;
  }
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

const GUIDE_URL = /^https:\/\/(?:www\.)?mokaair\.com\/[A-Za-z-]+\/guides\/([a-z0-9][a-z0-9-]{0,118}[a-z0-9])\/?(?:[?#].*)?$/;

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

/** The Jev check in numbers, and the lines still flagged, from review/check.json and check-flags.json. */
export function audioCheck(check, flags, lineCount) {
  const entries = Object.values(check?.lines ?? {});
  const flagged = new Set(flags?.flags ?? []);
  const exact = entries.filter((entry) => entry.match_kind === "exact").length;
  const alike = entries.filter((entry) => entry.match && entry.match_kind !== "exact").length;
  return {
    check: { lines: lineCount, checked: entries.length, exact, alike, judged_fine: entries.length - exact - alike - flagged.size, flagged: flagged.size },
    flagged_lines: Object.entries(check?.lines ?? {})
      .filter(([id]) => flagged.has(id))
      .map(([id, entry]) => ({ id, script: entry.intended ?? "", heard: entry.heard ?? "", noul: entry.noul ?? null })),
  };
}

/** The unticked items of UPLOAD.md, without their Markdown emphasis. */
export function uploadItems(markdown) {
  return markdown
    .split(/\r?\n/)
    .map((line) => /^- \[ \]\s*(.+)$/.exec(line)?.[1])
    .filter(Boolean)
    .map((item) => item.replace(/\*\*/g, ""));
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
      last = new ReviewError(message, { status: response.status, code: problem.code ?? "", who });
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

/** Encode a smaller copy for the page with ffmpeg, once per source file. */
async function encodeDefault(kind, source, target, env) {
  const tools = await locateFfmpeg(env);
  const args = kind === "narration"
    ? ["-hide_banner", "-y", "-loglevel", "error", "-i", source, "-c:a", "aac", "-b:a", "96k", "-ac", "1", "-movflags", "+faststart", target]
    : ["-hide_banner", "-y", "-loglevel", "error", "-i", source, "-vf", "scale=1280:720:flags=lanczos", "-c:v", "libx264", "-preset", "veryfast", "-crf", "26", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", target];
  await runTool(tools.ffmpeg, args);
}

async function preview(ctx, workdir, kind, source) {
  const hash = (await sha256File(source)).slice(0, 16);
  const target = path.join(workdir, "review", `${kind}-${hash}.${kind === "narration" ? "m4a" : "mp4"}`);
  if (!existsSync(target)) {
    mkdirSync(path.dirname(target), { recursive: true });
    await (ctx.encode ?? encodeDefault)(kind, source, target, ctx.env);
  }
  return target;
}

/** The option letter of candidate n on the review page: 1 → A. */
export const optionKey = (n) => String.fromCharCode(64 + n);
const IMAGE_TYPES = { ".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp" };
const imageType = (file) => IMAGE_TYPES[path.extname(file).toLowerCase()] ?? "application/octet-stream";

/**
 * The next gate whose content exists and is not approved as it stands; null when none. A drama
 * (docs/videos/DRAMA.md) puts the look before the narration and the storyboard before the cut.
 */
async function nextGate(places, workdir, doc) {
  const order = isDrama(doc) ? ["outline", ...(doc.series ? ["script"] : []), "look", "audio", "storyboard", "final"] : ["outline", "audio", "final"];
  for (const gate of order) {
    const state = await approvalState({ gate, ...places });
    if (state.status === "missing" || state.status === "stale") return gate;
    if (state.status === "absent") return null;
  }
  const metadata = path.join(workdir, ARTIFACTS.upload);
  if (!existsSync(metadata)) return null;
  const sha = await sha256File(metadata);
  const confirmed = readApprovals(workdir).approvals.some((entry) => entry.gate === "publish" && entry.sha256 === sha);
  return confirmed ? null : "publish";
}

async function submission(gate, { ctx, request, project, workdir, dir }) {
  const { doc } = project;
  const slug = doc.slug;
  if (gate === "outline") {
    const file = path.join(dir, "brief.md");
    const brief = readFileSync(file, "utf8");
    const options = outlineOptions(brief);
    return { gate, content_sha256: await sha256File(file), summary: `企劃書與 ${options.length} 個大綱選項`, payload: { brief, options }, files: [] };
  }
  if (gate === "script") {
    // Written afresh so the file always matches video.json; the same narrative gives the same
    // bytes, so an approval already given stays valid.
    const file = writeScreenplay(dir, doc);
    const check = readJson(path.join(workdir, "review", "script-check.json"), null);
    const scenes = scriptScenes(doc);
    const lines = scenes.reduce((sum, scene) => sum + scene.lines.length, 0);
    const timeline = estimateTimeline(doc);
    const minutes = Number((timeline.total_frames / timeline.fps / 60).toFixed(1));
    return {
      gate,
      content_sha256: await sha256File(file),
      summary: `劇本 ${scenes.length} 場、${lines} 句，約 ${minutes} 分鐘${check?.coverage ? "；查核已對照細綱" : ""}`,
      payload: {
        scenes,
        characters: (doc.characters ?? []).map(({ id, name }) => ({ id, name })),
        minutes,
        beats: project.series?.beats ?? null,
        coverage: check?.coverage ?? null,
        continuity_problems: check?.problems ?? [],
        narrative_hash: narrativeHash(doc),
      },
      files: [],
    };
  }
  if (gate === "audio") {
    const file = path.join(workdir, ARTIFACTS.timeline);
    const timeline = readJson(file, null);
    const check = audioCheck(readJson(path.join(workdir, "review", "check.json"), null), readJson(path.join(workdir, "review", "check-flags.json"), null), timeline.lines.length);
    const narration = await upload(request, slug, await preview(ctx, workdir, "narration", path.join(workdir, ARTIFACTS.narration)), "narration", "audio/mp4");
    const seconds = timeline.total_frames / timeline.fps;
    return {
      gate,
      content_sha256: await sha256File(file),
      summary: `旁白 ${formatClock(Math.round(seconds))}，${timeline.lines.length} 句；Jev 標記 ${check.check.flagged} 句`,
      payload: { duration_seconds: seconds, ...check },
      files: [narration],
    };
  }
  if (gate === "final") {
    const file = path.join(workdir, ARTIFACTS.video);
    const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
    const checks = readJson(path.join(workdir, ARTIFACTS.checks), null) ?? {};
    const { metadata } = composeMetadata({ doc, timeline, translations: project.translations, pack: project.pack });
    const files = [await upload(request, slug, await preview(ctx, workdir, "preview", file), "preview", "video/mp4")];
    const sheet = path.join(workdir, ARTIFACTS.contactSheet);
    if (existsSync(sheet)) files.push(await upload(request, slug, sheet, "contact_sheet", "image/png"));
    const thumbnail = path.join(workdir, "thumbnail.jpg");
    if (existsSync(thumbnail)) files.push(await upload(request, slug, thumbnail, "thumbnail", "image/jpeg"));
    // The dub tracks made so far go up beside the cut, so the owner can hear them on the site
    // (docs/videos/DUBS.md). Only the m4a form: it is the audio type the review store takes.
    const { dubs, skipped: skippedDubs } = dubsForUpload(project, workdir, timeline.speech_hash);
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
      content_sha256: await sha256File(file),
      summary: `成片 ${formatClock(Math.round(seconds))}，自動檢查${checks.ok ? "全部通過" : `有 ${(checks.problems ?? []).length} 項問題`}${dubs.length ? `，配音 ${dubs.map((dub) => dub.locale).join("、")}` : ""}`,
      payload: {
        duration_seconds: seconds,
        checks: { ok: Boolean(checks.ok), problems: checks.problems ?? [] },
        chapters: metadata.chapters.map((chapter) => ({ time: chapter.at, title: chapter.title })),
        metadata: { [metadata.default_language]: { title: metadata.title, description: metadata.description }, ...metadata.localizations },
        ...(Object.keys(dubEntries).length ? { dubs: dubEntries } : {}),
      },
      files,
    };
  }
  if (gate === "dubs") {
    const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
    const { dubs, skipped } = dubsForUpload(project, workdir, timeline?.speech_hash);
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
  const file = path.join(workdir, ARTIFACTS.upload);
  const checklist = existsSync(path.join(workdir, UPLOAD_CHECKLIST)) ? uploadItems(readFileSync(path.join(workdir, UPLOAD_CHECKLIST), "utf8")) : [];
  return { gate, content_sha256: await sha256File(file), summary: "上傳包已備好：請確認可以上架", payload: { checklist }, files: [] };
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

/** The storyboard gate: every keyframe and the contact sheet, with the judge's verdicts; bound to keyframes/manifest.json. */
async function storyboardSubmission({ request, project, workdir }) {
  const { doc } = project;
  const file = path.join(workdir, ARTIFACTS.keyframes);
  const manifest = readJson(file, null);
  if (!manifest?.shots) throw new ReviewError("keyframes/manifest.json is missing; run keyframes first", { who: "owner" });
  const timeline = readJson(path.join(workdir, ARTIFACTS.timeline), null);
  const seconds = new Map((timeline?.scenes ?? []).map((scene) => [scene.id, Math.round(((scene.end_frame - scene.start_frame) / (timeline.fps || 30)) * 10) / 10]));
  const files = [];
  const shots = [];
  for (const [index, scene] of shotScenes(doc).entries()) {
    const shot = manifest.shots[scene.id];
    if (!shot?.file) continue;
    const role = `shot_${String(index + 1).padStart(2, "0")}`;
    files.push(await upload(request, doc.slug, path.join(workdir, shot.file), role, imageType(shot.file)));
    shots.push({
      id: scene.id,
      chapter: scene.chapter ?? null,
      prompt: scene.data?.prompt ?? "",
      seconds: seconds.get(scene.id) ?? null,
      file_role: role,
      needs_review: Boolean(shot.needs_review),
      judge: { overall: shot.judge?.overall ?? null, problems: shot.judge?.problems ?? [] },
    });
  }
  const sheet = path.join(workdir, "keyframes", "contact-sheet.png");
  if (existsSync(sheet) && files.length < 48) files.push(await upload(request, doc.slug, sheet, "contact_sheet", "image/png"));
  const scores = shots.map((shot) => shot.judge.overall).filter((score) => typeof score === "number");
  const lowest = scores.length ? Math.min(...scores) : null;
  const waiting = shots.filter((shot) => shot.needs_review);
  // Only the shots left for a prompt fix carry problems here: a board the judge passed whole
  // may be approved automatically when the owner allows it.
  const problems = [...new Set(waiting.flatMap((shot) => shot.judge.problems))];
  return {
    gate: "storyboard",
    content_sha256: await sha256File(file),
    summary: `分鏡 ${shots.length} 鏡${lowest === null ? "" : `，judge 最低 ${lowest}/10`}${waiting.length ? `，${waiting.length} 鏡待修` : ""}`,
    payload: { shots, judge: { overall: lowest, problems }, duplicates: manifest.duplicates ?? [] },
    files,
  };
}

/** Everything a gate submits: several reviews for the look, one for the others. */
async function submissions(gate, places) {
  if (gate === "look") return lookSubmissions(places);
  if (gate === "storyboard") return [await storyboardSubmission(places)];
  return [await submission(gate, places)];
}

function common(args) {
  const values = parseArgs({ args, options: { slug: { type: "string" }, workdir: { type: "string" }, gate: { type: "string" }, "report-only": { type: "boolean" } }, strict: true }).values;
  if (!values.slug) throw new UsageError("needs --slug");
  if (values.gate && !REVIEW_GATES.includes(values.gate)) throw new UsageError(`--gate must be one of ${REVIEW_GATES.join(", ")}`);
  return values;
}

function fail(error, ctx) {
  if (error instanceof ToolMissing) {
    ctx.stderr.write(`${error.message}\n`);
    return ctx.EXIT.missing;
  }
  if (!(error instanceof ReviewError)) throw error;
  ctx.stderr.write(`${error.message}\n`);
  return error.who === "owner" ? ctx.EXIT.owner : ctx.EXIT.external;
}

export async function reviewPush(args, ctx) {
  const values = common(args);
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
        ...(sourceGuide ? { source_guide: sourceGuide } : {}),
        ...(project.doc.series ? { series_slug: project.doc.series.slug, episode_number: project.doc.series.episode } : {}),
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
    const bodies = await submissions(gate, { ctx, request, project, workdir, dir });
    for (const body of bodies) {
      const review = await request("POST", `${values.slug}/reviews`, { json: body });
      const what = body.subject ? `${gate} (${body.subject})` : gate;
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
  if (readApprovals(workdir).approvals.some((entry) => entry.gate === review.gate && entry.sha256 === review.content_sha256)) {
    return "already recorded";
  }
  const note = `approved on /admin/videos at ${review.decided_at}${review.choice ? `; chose outline ${review.choice}` : ""}${review.note ? `; ${review.note}` : ""}`;
  await approve({ gate: review.gate, docDir: dir, workdir, now, note });
  if (review.gate === "publish") return "the owner confirmed the upload; follow upload/UPLOAD.md in YouTube Studio";
  if (review.gate === "dubs") return "the owner uploaded these dub tracks in YouTube Studio";
  return `approval recorded${review.choice ? ` (outline ${review.choice})` : ""}`;
}
