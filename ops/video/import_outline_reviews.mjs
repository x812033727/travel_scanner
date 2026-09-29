#!/usr/bin/env node
// One-time recovery of authored, unsubmitted outlines. Never calls a judge or a media stage.
// Before --apply, the operator must verify that the production worker has no <slug>/auto.json
// for ANY source below, and obtain approval for the exact bundle hash. Reporting a project does
// not create worker state. The receipt is local recovery evidence, not permission to overwrite.
// Report and submit are separate, unconditional API writes. The operator must have exclusive
// control of the target slugs: preflight detects existing collisions but cannot lock out a
// concurrent writer between GET and PUT/POST. This is a bounded recovery tool, not a sync job.
import { createHash } from "node:crypto";
import { existsSync, readFileSync, writeFileSync } from "node:fs";
import path from "node:path";
import { pathToFileURL } from "node:url";
import { parseArgs } from "node:util";

import { automationClient } from "../../tools/video/automation/client.mjs";
import { atomicWrite, ROOT, resolveWorkBase } from "../../tools/video/core/paths.mjs";
import { loadProject, pipelineStatus } from "../../tools/video/core/state.mjs";
import { checklistFrom, outlineOptions, sourceGuideOf } from "../../tools/video/review/sync.mjs";

export const SOURCES = Object.freeze([
  [867, "ai-agent-vs-chatbot"],
  [867, "ai-citation-check"],
  [868, "ai-coding-tools-same-task"],
  [868, "ai-bug-fix-pr-review"],
  [891, "ai-price-war-gpt-6-sol-vs-opus-5-5"],
  [891, "siri-ai-ios-27-how-to-get-it"],
  [891, "ai-agents-explained-what-they-cost"],
  [891, "google-vids-free-ai-video-omni-1-1"],
  [891, "vibe-coding-first-website-2026"],
  [891, "free-vs-paid-ai-plans-2026"],
]);
const KIND = "mokaair-authored-outline-recovery";
export const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const canonical = (value) => JSON.stringify(value, (_, item) => item && typeof item === "object" && !Array.isArray(item)
  ? Object.fromEntries(Object.keys(item).sort().map((key) => [key, item[key]])) : item);
const same = (left, right) => canonical(left) === canonical(right);
const encode = (value) => `${JSON.stringify(value, null, 2)}\n`;

/** The two developer briefs use level-two headings; keep their complete original text. */
export function optionsFor(brief) {
  const ordinary = outlineOptions(brief);
  if (ordinary.length) return ordinary;
  return [...brief.matchAll(/^## 大綱 ([A-Z])([^\r\n]*)\r?\n([\s\S]*?)(?=^## |$(?![\s\S]))/gm)]
    .map((match) => ({ key: match[1], title: `大綱 ${match[1]}${match[2].trim()}`, summary: match[3].trim() }));
}

function assertNoLocalWorker(workBase) {
  for (const [, slug] of SOURCES) {
    if (existsSync(path.join(workBase, slug, "auto.json"))) {
      throw new Error(`${slug}: local auto.json exists; coordinate with its worker before importing`);
    }
  }
}

/** Offline: existing pipeline helpers only read source/media state; no credentials are loaded. */
export async function prepareBundle(ctx = {}, workdir) {
  const root = ctx.root ?? ROOT;
  const workBase = resolveWorkBase({ flag: workdir, root, env: ctx.env, home: ctx.home });
  assertNoLocalWorker(workBase);
  const items = [];
  for (const [pr, slug] of SOURCES) {
    const dir = path.join(root, "docs", "videos", slug);
    const briefBytes = readFileSync(path.join(dir, "brief.md"));
    const videoBytes = readFileSync(path.join(dir, "video.json"));
    const brief = briefBytes.toString("utf8");
    const options = optionsFor(brief);
    if (options.length < 2 || options.length > 3 || new Set(options.map((option) => option.key)).size !== options.length) {
      throw new Error(`${slug}: expected two or three distinct authored outline options`);
    }
    const { doc } = loadProject({ slug, root });
    if (doc.slug !== slug || (doc.format && doc.format !== "slides") || doc.youtube?.video_id || doc.series || doc.compilation) {
      throw new Error(`${slug}: source is not an unpublished standalone tutorial`);
    }
    const status = await pipelineStatus({ slug, root, workdir: path.join(workBase, slug) });
    if (status.steps.some((step) => step.id.endsWith(" approved") && step.done)) {
      throw new Error(`${slug}: local approvals exist; reconcile them before manual recovery`);
    }
    const sourceGuide = sourceGuideOf(doc);
    if (!sourceGuide) throw new Error(`${slug}: source guide is missing`);
    const staleNarration = status.steps.some((step) => step.id === "narration synthesized" && step.note?.includes("older script"));
    const note = pr === 891
      ? "獨立查核與既有題目重疊仍待確認；檔案中的自查不代表獨立查核完成。"
      : pr === 867
        ? staleNarration
          ? "本機舊版媒體的旁白雜湊不符目前稿件；這次只送企劃，不送成片。"
          : "本機媒體仍需獨立核對；這次只送企劃，不送成片。"
        : "製作紀錄中的成片仍待找回與核對；這次只送企劃。";
    const source = { pr, brief_sha256: sha256(briefBytes), video_sha256: sha256(videoBytes) };
    items.push({
      slug,
      source,
      project: {
        title: doc.youtube?.title || slug,
        stage: status.next ? status.next.id.slice(0, 40) : "done",
        checklist: checklistFrom(status.steps),
        source_guide: sourceGuide,
        format: "slides",
      },
      review: {
        gate: "outline",
        content_sha256: source.brief_sha256,
        summary: `PR #${pr} 原始企劃待站主審核。${note}`,
        payload: { brief, options, import_source: { kind: KIND, ...source } },
        files: [],
      },
    });
  }
  return { schema_version: 1, kind: KIND, work_base: workBase, items };
}

/** Refuse edits, stale sources, changed local approvals/artifacts and arbitrary extra slugs. */
export async function validateBundle(bundle, ctx = {}) {
  if (bundle?.schema_version !== 1 || bundle.kind !== KIND || typeof bundle.work_base !== "string") {
    throw new Error("Not an authored-outline recovery bundle");
  }
  const current = await prepareBundle(ctx, bundle.work_base);
  if (!same(current, bundle)) throw new Error("Bundle differs from current source/state; prepare and review a new bundle");
  for (const { slug, review } of bundle.items) {
    if (Object.hasOwn(review.payload, "pick") || review.gate !== "outline" || review.files.length) {
      throw new Error(`${slug}: only manual outline reviews without files or a judge pick are allowed`);
    }
    if (Buffer.byteLength(JSON.stringify(review.payload), "utf8") > 256 * 1024) {
      throw new Error(`${slug}: review payload exceeds the server limit`);
    }
  }
}

function projectMatches(project, item) {
  return project?.slug === item.slug && project.title === item.project.title
    && project.source_guide === item.project.source_guide && (project.format ?? "slides") === "slides"
    && !project.series_slug && !project.episode_number && !project.dropped_at && !project.youtube_video_id
    && !project.locales_decided_at && !project.retry_request_id;
}

function exactReview(review, item) {
  return review.status === "pending" && !review.subject && review.gate === "outline"
    && review.content_sha256 === item.review.content_sha256 && review.summary === item.review.summary
    && same(review.payload, item.review.payload) && same(review.files, []);
}

/** Recognize only this exact pending review, or this run's recorded unfinished report. */
function disposition(project, item, receipt) {
  if (project === null) return "create";
  if (!projectMatches(project, item) || !Array.isArray(project.reviews)) throw new Error(`${item.slug}: existing project collision`);
  if (project.reviews.length === 1 && exactReview(project.reviews[0], item)) return "skip";
  const reported = receipt.reported[item.slug];
  if (project.reviews.length === 0 && reported
    && reported.last_synced_at === project.last_synced_at
    && reported.project_sha256 === sha256(canonical(item.project))
    && project.stage === item.project.stage && same(project.checklist, item.project.checklist)) return "submit";
  throw new Error(`${item.slug}: existing project/review differs; refusing to overwrite`);
}

/** All ten are read before any write; immediately recheck each slug before its first mutation. */
export async function applyBundle(bundle, { client, receipt, saveReceipt }) {
  const videos = await client.videos();
  if (!Array.isArray(videos)) throw new Error("Invalid site video inventory");
  const existing = [];
  for (const item of bundle.items) existing.push(await client.reviews(item.slug));
  const actions = existing.map((project, index) => {
    const item = bundle.items[index];
    if (project === null && videos.some((video) => video.slug === item.slug)) throw new Error(`${item.slug}: inventory changed; retry preflight`);
    return disposition(project, item, receipt);
  });
  const results = [];
  for (const [index, item] of bundle.items.entries()) {
    const fresh = await client.reviews(item.slug);
    if (disposition(fresh, item, receipt) !== actions[index]) throw new Error(`${item.slug}: changed after preflight; stopped`);
    if (actions[index] === "skip") {
      results.push({ slug: item.slug, status: "already_pending" });
      continue;
    }
    if (actions[index] === "create") {
      const reported = await client.report(item.slug, item.project);
      if (!projectMatches(reported, item) || !reported.last_synced_at || reported.reviews?.length) {
        throw new Error(`${item.slug}: unexpected report response; inspect the site before retrying`);
      }
      receipt.reported[item.slug] = { project_sha256: sha256(canonical(item.project)), last_synced_at: reported.last_synced_at };
      // Save before submit so a failed POST can resume without taking over an unrelated card.
      await saveReceipt(receipt);
    }
    const reviewed = await client.submit(item.slug, item.review);
    if (!exactReview(reviewed, item)) throw new Error(`${item.slug}: submission was not the expected pending review; inspect the site`);
    results.push({ slug: item.slug, status: "pending" });
  }
  return results;
}

/** Production host policy: sequential requests, at least one second between their starts. */
export function pacedClient(client, { intervalMs = 1000, now = Date.now, sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms)) } = {}) {
  let queue = Promise.resolve();
  let lastStarted = -Infinity;
  return Object.fromEntries(["videos", "reviews", "report", "submit"].map((method) => [method, (...args) => {
    const request = queue.then(async () => {
      const delay = intervalMs - (now() - lastStarted);
      if (delay > 0) await sleep(delay);
      lastStarted = now();
      return client[method](...args);
    });
    queue = request.catch(() => {});
    return request;
  }]));
}

export function summary(bundle, hash) {
  return {
    bundle_sha256: hash,
    projects: bundle.items.length,
    manual_outline_reviews: bundle.items.length,
    media_uploads: 0,
    model_calls: 0,
    remote_preflight_required: "Confirm no production worker <slug>/auto.json for all ten slugs before applying; keep the receipt for interrupted runs.",
    items: bundle.items.map(({ slug, source, project, review }) => ({ slug, pr: source.pr, title: project.title, source_guide: project.source_guide, brief_sha256: source.brief_sha256, summary: review.summary })),
  };
}

export async function main(args = process.argv.slice(2), ctx = {}) {
  const { values } = parseArgs({ args, strict: true, options: {
    prepare: { type: "string" }, input: { type: "string" }, apply: { type: "boolean" },
    "expected-sha256": { type: "string" }, workdir: { type: "string" }, receipt: { type: "string" },
  } });
  const out = ctx.stdout ?? process.stdout;
  if (Boolean(values.prepare) === Boolean(values.input)) throw new Error("Use --prepare OUTPUT or --input FILE [--apply --expected-sha256 HASH]");
  if (values.prepare) {
    if (values.apply || values["expected-sha256"] || values.receipt) throw new Error("--prepare cannot apply or use a receipt");
    const bundle = await prepareBundle(ctx, values.workdir);
    const bytes = encode(bundle);
    writeFileSync(values.prepare, bytes, { encoding: "utf8", flag: "wx" });
    out.write(encode(summary(bundle, sha256(bytes))));
    return 0;
  }
  if (values.workdir) throw new Error("--workdir belongs to --prepare; --input uses the bound work directory");
  const bytes = readFileSync(values.input);
  const hash = sha256(bytes);
  const bundle = JSON.parse(bytes.toString("utf8"));
  await validateBundle(bundle, ctx);
  if (!values.apply) {
    out.write(encode({ mode: "dry-run", ...summary(bundle, hash) }));
    return 0;
  }
  if (!/^[0-9a-f]{64}$/.test(values["expected-sha256"] ?? "") || values["expected-sha256"] !== hash) {
    throw new Error("--apply requires --expected-sha256 equal to the exact reviewed bundle bytes");
  }
  const receiptFile = path.resolve(values.receipt ?? `${values.input}.receipt.json`);
  if (receiptFile === path.resolve(values.input)) throw new Error("Receipt must not overwrite the bundle");
  const receipt = existsSync(receiptFile) ? JSON.parse(readFileSync(receiptFile, "utf8")) : { schema_version: 1, kind: KIND, bundle_sha256: hash, reported: {} };
  if (receipt.schema_version !== 1 || receipt.kind !== KIND || receipt.bundle_sha256 !== hash || !receipt.reported || typeof receipt.reported !== "object" || Array.isArray(receipt.reported)) {
    throw new Error("Receipt does not belong to this exact bundle");
  }
  // Credentials are loaded only after offline validation and hash confirmation.
  const client = ctx.client ?? pacedClient(automationClient(ctx));
  const results = await applyBundle(bundle, { client, receipt, saveReceipt: (value) => atomicWrite(receiptFile, encode(value)) });
  out.write(encode({ mode: "applied", bundle_sha256: hash, results }));
  return 0;
}

if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) {
  main().catch((error) => { process.stderr.write(`${error.message}\n`); process.exitCode = 1; });
}
