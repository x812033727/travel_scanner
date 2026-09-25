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
import { docDir, readJson, resolveWorkdir, UsageError } from "../core/paths.mjs";
import { ARTIFACTS, loadProject, pipelineStatus } from "../core/state.mjs";
import { formatClock } from "../core/timeline.mjs";
import { composeMetadata } from "../package/metadata.mjs";
import { readCredentials } from "../tts/credentials.mjs";
import { USER_AGENT } from "../tts/client.mjs";

// Mirrors PART_BYTES in apps/api/app/video_reviews/storage.py: under nginx's 6 MB request cap.
export const PART_BYTES = 4 * 1024 * 1024;
export const REVIEW_GATES = ["outline", "audio", "final", "publish"];
const UPLOAD_CHECKLIST = path.join("upload", "UPLOAD.md");

// The owner reads the site in Traditional Chinese; status's step ids are English.
const STEP_LABELS = {
  brief: "企劃書",
  "outline approved": "站主選好大綱",
  "script passes lint": "稿子通過檢查",
  "fact-checked": "查核完成",
  "narration synthesized": "旁白合成",
  "narration approved": "旁白核准",
  "frames rendered": "畫面完成",
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

/** The next gate whose content exists and is not approved as it stands; null when none. */
async function nextGate(places, workdir) {
  for (const gate of ["outline", "audio", "final"]) {
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
    const seconds = timeline.total_frames / timeline.fps;
    return {
      gate,
      content_sha256: await sha256File(file),
      summary: `成片 ${formatClock(Math.round(seconds))}，自動檢查${checks.ok ? "全部通過" : `有 ${(checks.problems ?? []).length} 項問題`}`,
      payload: {
        duration_seconds: seconds,
        checks: { ok: Boolean(checks.ok), problems: checks.problems ?? [] },
        chapters: metadata.chapters.map((chapter) => ({ time: chapter.at, title: chapter.title })),
        metadata: { [metadata.default_language]: { title: metadata.title, description: metadata.description }, ...metadata.localizations },
      },
      files,
    };
  }
  const file = path.join(workdir, ARTIFACTS.upload);
  const checklist = existsSync(path.join(workdir, UPLOAD_CHECKLIST)) ? uploadItems(readFileSync(path.join(workdir, UPLOAD_CHECKLIST), "utf8")) : [];
  return { gate, content_sha256: await sha256File(file), summary: "上傳包已備好：請確認可以上架", payload: { checklist }, files: [] };
}

function common(args) {
  const values = parseArgs({ args, options: { slug: { type: "string" }, workdir: { type: "string" }, gate: { type: "string" } }, strict: true }).values;
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
    await request("PUT", values.slug, {
      json: {
        title: project.doc.youtube?.title || project.doc.slug,
        stage: status.next ? status.next.id.slice(0, 40) : "done",
        checklist: checklistFrom(status.steps),
        youtube_video_id: project.doc.youtube?.video_id || null,
      },
    });
    const gate = values.gate ?? (await nextGate({ docDir: dir, workdir }, workdir));
    if (!gate) {
      ctx.stdout.write(`${values.slug}: reported; nothing waits for the owner right now\n`);
      return ctx.EXIT.ok;
    }
    const body = await submission(gate, { ctx, request, project, workdir, dir });
    const review = await request("POST", `${values.slug}/reviews`, { json: body });
    ctx.stdout.write(`${values.slug}: ${gate} submitted for review (${review.status}); the owner decides on /admin/videos, then run review-pull\n`);
    return ctx.EXIT.ok;
  } catch (error) {
    return fail(error, ctx);
  }
}

export async function reviewPull(args, ctx) {
  const values = common(args);
  const dir = docDir(values.slug, ctx.root);
  const workdir = resolveWorkdir({ flag: values.workdir, env: ctx.env, slug: values.slug, root: ctx.root, home: ctx.home });
  try {
    const project = await client(ctx)("GET", values.slug);
    let waiting = 0;
    // Oldest first, so the newest decision on a gate is the one approvals.json ends with.
    for (const review of [...project.reviews].reverse()) {
      if (values.gate && review.gate !== values.gate) continue;
      if (review.status === "pending") {
        waiting += 1;
        ctx.stdout.write(`${review.gate}: waiting for the owner\n`);
      } else if (review.status === "rejected") {
        ctx.stdout.write(`${review.gate}: sent back — ${review.note ?? ""}\n`);
      } else if (review.status === "approved") {
        const message = await recordApproval(review, { dir, workdir, now: ctx.now() });
        ctx.stdout.write(`${review.gate}: ${message}\n`);
      }
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
  return `approval recorded${review.choice ? ` (outline ${review.choice})` : ""}`;
}
