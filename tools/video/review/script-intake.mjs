// Import an owner-approved Markdown script as a *pending*, hand-pushed review.
// This deliberately does not call review-push: that command regenerates script.md
// from video.json, while this gate must stay bound to the approved file bytes.
import { createHash } from "node:crypto";
import { readFileSync, realpathSync } from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

import { readCredentials, validSite } from "../tts/credentials.mjs";

export const DEFAULT_MANIFEST = "docs/videos/brand-stories-everyday-reversals-20261020/approved-scripts.json";
const SHA = /^[a-f0-9]{64}$/;
const ID = /^C(0[1-9]|1[0-9]|20)$/;
const SLUG = /^story-everyday-[a-z0-9-]+-c(0[1-9]|1[0-9]|20)$/;
const SERIES = "brand-stories-everyday-reversals";
const APPROVED_IDS = ["C03", "C04", "C05", "C06", "C07", "C08", "C09", "C10", "C11", "C14", "C15", "C19"];
const C08_SHORT_SLUG = "story-everyday-kikkoman-c08-short-v8";
const C08_SHORT_SCRIPT_SHA256 = "07cc18d1d90e6eba679a699f0243d977717f896b924158ab251fb390a308c0b9";
const C08_SHORT_SOURCE_SHA256 = "040d9a499ddb864f62ebf0edcc948cc58439ffa13d0dae0ce5a9475297ee5d69";
const C08_SHORT_SOURCE_PATH = "docs/videos/story-everyday-kikkoman-c08/reviews/v8-short-narration-candidate-20261024.md";
const hash = (bytes) => createHash("sha256").update(bytes).digest("hex");
const insist = (ok, message) => { if (!ok) throw new Error(message); };

function columns(line) {
  if (!line.startsWith("|") || !line.endsWith("|")) return null;
  const cells = line.slice(1, -1).split("|").map((cell) => cell.trim());
  return cells.length === 3 ? cells : null;
}

function tableScenes(markdown, id) {
  const lines = markdown.split(/\r?\n/);
  const scenes = [];
  const seen = new Set();
  let chapter = null;
  let inTable = false;
  let expectingDivider = false;
  let lastChapter = 0;
  const prefix = id.toLowerCase();
  for (let index = 0; index < lines.length; index++) {
    const line = lines[index].trim();
    const heading = /^## ([1-6])(?:\.|\s|｜)(.+)$/.exec(line);
    if (heading) {
      chapter = { number: Number(heading[1]), title: heading[2].trim() };
      insist(chapter.number === lastChapter + 1, `chapter order at line ${index + 1}`);
      lastChapter = chapter.number;
      insist(chapter.title, `empty chapter at line ${index + 1}`);
      inTable = false;
      expectingDivider = false;
      continue;
    }
    if (line.startsWith("| ID |")) {
      const cells = columns(line);
      insist(chapter && cells && cells[0] === "ID" && cells[1].startsWith("旁白"), `invalid table header at line ${index + 1}`);
      inTable = true;
      expectingDivider = true;
      continue;
    }
    if (!inTable) continue;
    if (!line) { inTable = false; continue; }
    const cells = columns(line);
    insist(cells, `malformed table row at line ${index + 1}`);
    if (expectingDivider) {
      insist(cells.every((cell) => /^:?-{3,}:?$/.test(cell)), `missing table divider at line ${index + 1}`);
      expectingDivider = false;
      continue;
    }
    const [lineId, narration] = cells;
    // C05 uses H01/O01/... chapter IDs; the other table scripts use cNNNNNN.
    insist(new RegExp(`^(?:${prefix}[0-9]{4}|[A-Z][0-9]{2})$`).test(lineId), `invalid narration ID at line ${index + 1}`);
    insist(narration && !seen.has(lineId), `empty or duplicate narration ID ${lineId}`);
    seen.add(lineId);
    scenes.push({ id: lineId, chapter: chapter.title, template: "shot", prompt: null,
      lines: [{ id: lineId, speaker: "narrator", name: null, text: narration, emotion: null }] });
  }
  insist(!expectingDivider, "script ends before table divider");
  insist(scenes.length > 0, "no strict narration rows found");
  insist(lastChapter === 6 && new Set(scenes.map((scene) => scene.chapter)).size === 6, "expected six chapter tables");
  return scenes;
}

function c08ShortScenes(markdown) {
  const scenes = [];
  const seen = new Set();
  let chapter = null;
  let lastChapter = 0;
  for (const [index, raw] of markdown.split(/\r?\n/).entries()) {
    const line = raw.trim();
    if (line.startsWith("## ")) {
      const heading = /^## ([1-6]) (.+)$/.exec(line);
      insist(heading && Number(heading[1]) === lastChapter + 1, `C08 short-v8 chapter order at line ${index + 1}`);
      chapter = heading[2].trim();
      insist(chapter, `C08 short-v8 empty chapter at line ${index + 1}`);
      lastChapter++;
      continue;
    }
    if (!line.startsWith("-")) continue;
    const bullet = /^- (v7[a-z]{1,2}[0-9]{2}) (.+)$/.exec(line);
    insist(chapter && bullet && bullet[2].trim() && !seen.has(bullet[1]), `C08 short-v8 malformed or duplicate narration at line ${index + 1}`);
    seen.add(bullet[1]);
    scenes.push({ id: bullet[1], chapter, template: "shot", prompt: null,
      lines: [{ id: bullet[1], speaker: "narrator", name: null, text: bullet[2].trim(), emotion: null }] });
  }
  insist(lastChapter === 6 && scenes.length === 36 && new Set(scenes.map((scene) => scene.chapter)).size === 6,
    "C08 short-v8 requires six chapters and 36 narration lines");
  return scenes;
}

function bulletScenes(markdown) {
  const lines = markdown.split(/\r?\n/);
  const chapters = ["第一", "第二", "第三", "第四", "第五", "第六"];
  const scenes = [];
  const seen = new Set();
  let chapter = null;
  let lastChapter = 0;
  for (let index = 0; index < lines.length; index++) {
    const line = lines[index].trim();
    const heading = /^## (第[一二三四五六]章)｜(.+)$/.exec(line);
    if (heading) {
      insist(heading[1] === `${chapters[lastChapter]}章`, `chapter order at line ${index + 1}`);
      chapter = heading[2].trim();
      lastChapter++;
      continue;
    }
    if (line.startsWith("## ")) { chapter = null; continue; }
    if (!chapter || !line.startsWith("- ")) continue;
    const match = /^- \*\*([A-Z][0-9]{2})\*\* (.+?)〔([^〕]+)〕$/.exec(line);
    insist(match, `malformed narration bullet at line ${index + 1}`);
    insist(!seen.has(match[1]) && match[2].trim(), `duplicate or empty narration at line ${index + 1}`);
    seen.add(match[1]);
    scenes.push({ id: match[1], chapter, template: "shot", prompt: null,
      lines: [{ id: match[1], speaker: "narrator", name: null, text: match[2].trim(), emotion: null }] });
  }
  insist(lastChapter === 6 && new Set(scenes.map((scene) => scene.chapter)).size === 6, "expected six narration bullet chapters");
  return scenes;
}

function screenplayScenes(markdown, id) {
  const lines = markdown.split(/\r?\n/);
  const scenes = [];
  const seen = new Set();
  let chapter = null;
  let current = null;
  for (let index = 0; index < lines.length; index++) {
    const line = lines[index].trim();
    if (line.startsWith("### ")) { chapter = line.slice(4).trim(); current = null; continue; }
    const heading = /^#### (\d+)\. (c\d{2}-[a-z0-9-]+)(?:（([^）]+)）)?$/.exec(line);
    if (heading) {
      insist(chapter && heading[2].startsWith(`${id.toLowerCase()}-`), `wrong scene chapter or ID at line ${index + 1}`);
      insist(Number(heading[1]) === scenes.length + 1 && !seen.has(heading[2]), `scene order/duplicate at line ${index + 1}`);
      seen.add(heading[2]);
      current = { id: heading[2], chapter, template: heading[3] || "shot", prompt: null, lines: [] };
      scenes.push(current);
      continue;
    }
    if (!current || !line) continue;
    const narration = /^旁白(?:（([^）]+)）)?：(.+)$/.exec(line);
    if (narration) {
      insist(current.lines.length === 0, `multiple narration lines in ${current.id}`);
      current.lines.push({ id: current.id, speaker: "narrator", name: null,
        text: narration[2].trim(), emotion: narration[1] || null });
    } else if (line.startsWith("旁白") || line.startsWith("【")) {
      throw new Error(`unsupported screenplay line at ${index + 1}`);
    }
  }
  insist(scenes.length > 0 && scenes.every((scene) => scene.lines.length === 1 && scene.lines[0].text), "every screenplay scene must have one narration line");
  insist(new Set(scenes.map((scene) => scene.chapter)).size === 6, "expected six screenplay chapters");
  return scenes;
}

export function parseScript(markdown, id) {
  insist(typeof markdown === "string" && ID.test(id), "invalid script or episode ID");
  const hasTables = /^\| ID \|/m.test(markdown);
  const hasScenes = /^#### 1\. /m.test(markdown);
  const hasBullets = /^## 第一章｜/m.test(markdown) && /^- \*\*[A-Z][0-9]{2}\*\*/m.test(markdown);
  const hasC08Short = id === "C08" && /^# C08 龜甲萬｜短版 v8 核准旁白投影$/m.test(markdown);
  insist(Number(hasTables) + Number(hasScenes) + Number(hasBullets) + Number(hasC08Short) === 1,
    "script must use exactly one supported line format");
  return hasTables ? tableScenes(markdown, id) : hasScenes ? screenplayScenes(markdown, id)
    : hasBullets ? bulletScenes(markdown) : c08ShortScenes(markdown);
}

export function loadIntake(manifestPath, { root = process.cwd(), ids = [] } = {}) {
  const source = JSON.parse(readFileSync(path.resolve(root, manifestPath), "utf8"));
  insist(source.schema_version === 1 && source.series_slug === SERIES && Array.isArray(source.entries), "unsupported approval manifest");
  insist(source.entries.length === APPROVED_IDS.length, "approval manifest must contain every owner-approved script");
  const wanted = new Set(ids.map((value) => value.toUpperCase()));
  insist([...wanted].every((value) => ID.test(value)), "invalid --id value");
  const allIds = new Set();
  const allNumbers = new Set();
  const entries = source.entries.map((entry) => {
    insist(entry && ID.test(entry.id) && !allIds.has(entry.id), "invalid or duplicate approval ID");
    allIds.add(entry.id);
    insist(Number.isInteger(entry.number) && entry.number === Number(entry.id.slice(1)) && !allNumbers.has(entry.number), `invalid episode number for ${entry.id}`);
    allNumbers.add(entry.number);
    const c08Short = entry.id === "C08" && entry.slug === C08_SHORT_SLUG;
    insist(c08Short || (SLUG.test(entry.slug) && entry.slug.endsWith(`-${entry.id.toLowerCase()}`)), `invalid slug for ${entry.id}`);
    if (c08Short) {
      insist(entry.script_sha256 === C08_SHORT_SCRIPT_SHA256 && entry.expected_lines === 36,
        "C08 short-v8 approval hash/count differs from the frozen owner-approved projection");
      insist(hash(readFileSync(path.resolve(root, C08_SHORT_SOURCE_PATH))) === C08_SHORT_SOURCE_SHA256,
        "C08 short-v8 approved source SHA256 mismatch");
    }
    const expectedPath = `docs/videos/${entry.slug}/script.md`;
    insist(entry.script_path === expectedPath, `wrong script path for ${entry.id}`);
    insist(SHA.test(entry.script_sha256) && Number.isInteger(entry.expected_lines) && entry.expected_lines > 0, `missing exact hash/count for ${entry.id}`);
    insist(Number.isInteger(entry.approval_pr) && entry.approval_pr > 0 && typeof entry.approval_basis === "string" && entry.approval_basis.trim(), `missing owner approval provenance for ${entry.id}`);
    insist(typeof entry.title === "string" && entry.title.trim(), `missing title for ${entry.id}`);
    const file = path.resolve(root, expectedPath);
    insist(file.startsWith(path.resolve(root) + path.sep), `script escapes repository: ${entry.id}`);
    insist(realpathSync(file).startsWith(realpathSync(root) + path.sep), `script symlink escapes repository: ${entry.id}`);
    const bytes = readFileSync(file);
    const actual = hash(bytes);
    insist(actual === entry.script_sha256, `${entry.id} script SHA256 mismatch: expected ${entry.script_sha256}, got ${actual}`);
    const source_md = bytes.toString("utf8");
    insist(Buffer.from(source_md, "utf8").equals(bytes), `${entry.id} script is not valid UTF-8`);
    const scenes = parseScript(source_md, entry.id);
    insist(scenes.length === entry.expected_lines, `${entry.id} narration count mismatch: expected ${entry.expected_lines}, got ${scenes.length}`);
    if (c08Short) {
      const project = JSON.parse(readFileSync(path.resolve(root, `docs/videos/${entry.slug}/video.json`), "utf8"));
      insist(project.slug === entry.slug && project.series?.slug === SERIES && project.series.episode === 8,
        "C08 short-v8 canonical project identity mismatch");
      const projected = project.scenes?.flatMap((scene) => scene.lines ?? []);
      insist(projected?.length === scenes.length && projected.every((line, index) =>
        line.id === scenes[index].id && line.text === scenes[index].lines[0].text),
      "C08 short-v8 canonical narration differs from the approved script");
    }
    return { ...entry, scenes, source_md };
  });
  insist(APPROVED_IDS.every((id) => allIds.has(id)), "approval manifest ID set differs from the owner's approvals");
  insist([...wanted].every((value) => allIds.has(value)), "requested ID is absent from approval manifest");
  return { series_slug: source.series_slug, entries: wanted.size ? entries.filter((entry) => wanted.has(entry.id)) : entries };
}

function validateContext(context, manifest, entry) {
  insist(context?.series?.slug === manifest.series_slug && context.series.kind === "story", `${entry.id}: wrong backend series`);
  insist(context.series.status === "paused", `${entry.id}: series is not paused`);
  insist(context.episode?.number === entry.number && context.episode.slug === entry.slug, `${entry.id}: backend episode/slug mismatch`);
  insist(context.episode?.status === "planned", `${entry.id}: backend episode is not planned`);
}

const stableJson = (value) => JSON.stringify(value, (_key, item) => item && !Array.isArray(item) && typeof item === "object"
  ? Object.fromEntries(Object.keys(item).sort().map((key) => [key, item[key]])) : item);

function checkProject(project, manifest, entry) {
  if (!project) return "create";
  insist(project.slug === entry.slug && project.series_slug === manifest.series_slug && project.episode_number === entry.number && project.format === "drama" && !project.shorts_line && !project.dropped_at, `${entry.id}: existing project identity conflicts`);
  const reviews = (project.reviews ?? []).filter((review) => review.gate === "script" && review.subject == null);
  const same = reviews.find((review) => review.content_sha256 === entry.script_sha256 && (review.status === "pending" || review.status === "approved"));
  if (same) {
    const expected = reviewBody(entry);
    const currentFormat = same.summary === expected.summary && stableJson(same.payload) === stableJson(expected.payload);
    // C03 reached the site before this intake format existed. Keep its existing
    // owner-approved card only when the exact approved source hash and every
    // narration ID/text match; submitting it again would supersede an approval.
    const legacyC03 = entry.id === "C03" && same.status === "approved" && same.payload?.hand_pushed === true
      && Array.isArray(same.payload.scenes) && same.payload.scenes.length === entry.scenes.length
      && same.payload.scenes.every((scene, index) => {
        const legacyId = /^c03-p(\d{2})-s(\d{2})$/.exec(scene?.id ?? "");
        return scene?.id === entry.scenes[index].id
          && Array.isArray(scene.lines) && scene.lines.length === 1
          // C03's earlier card kept the original narration-row ID, while this
          // intake assigns the scene ID to its single narration line.
          && (scene.lines[0]?.id === entry.scenes[index].lines[0].id
            || (legacyId && scene.lines[0]?.id === `c03${legacyId[1]}${legacyId[2]}`))
          && scene.lines[0]?.text === entry.scenes[index].lines[0].text;
      });
    insist(currentFormat || legacyC03, `${entry.id}: same-hash review payload differs from approved source`);
    return "already-present";
  }
  insist(!reviews.some((review) => review.content_sha256 === entry.script_sha256), `${entry.id}: same-hash script review was rejected or superseded`);
  insist(!reviews.some((review) => review.status === "pending" || review.status === "approved"), `${entry.id}: a different live script review exists`);
  return "submit";
}

function reviewBody(entry) {
  return { gate: "script", content_sha256: entry.script_sha256, subject: null,
    summary: `${entry.id} 站主已核准劇本；PR #${entry.approval_pr}；${entry.expected_lines} 句；原稿 ${entry.script_path}；SHA-256 ${entry.script_sha256}。`,
    payload: { hand_pushed: true, source_kind: "owner-approved-markdown", source_path: entry.script_path,
      source_sha256: entry.script_sha256, approval_pr: entry.approval_pr,
      approval_basis: entry.approval_basis, source_md: entry.source_md, scenes: entry.scenes }, files: [] };
}

/** `request(method, apiPath, {json}?)` is injected so dry-run never needs credentials. */
export async function runIntake({ manifestPath = DEFAULT_MANIFEST, root = process.cwd(), ids = [], apply = false, request } = {}) {
  const manifest = loadIntake(manifestPath, { root, ids });
  if (!apply) return manifest.entries.map((entry) => ({ id: entry.id, slug: entry.slug, sha256: entry.script_sha256, lines: entry.scenes.length, action: "dry-run-local-only" }));
  insist(typeof request === "function", "--apply requires an authenticated request transport");
  // Finish every remote read before the first write. A mismatch in any selected
  // episode stops the entire batch instead of leaving a partial import.
  const plans = [];
  for (const entry of manifest.entries) {
    const context = await request("GET", `/api/video/automation/series/${manifest.series_slug}/context?episode=${entry.number}`);
    validateContext(context, manifest, entry);
    let project;
    try { project = await request("GET", `/api/video/reviews/${entry.slug}`); }
    catch (error) { if (error?.status !== 404) throw error; project = null; }
    plans.push({ entry, action: checkProject(project, manifest, entry) });
  }
  const results = [];
  for (const { entry, action } of plans) {
    if (action === "already-present") { results.push({ id: entry.id, action, sha256: entry.script_sha256 }); continue; }
    // Recheck immediately before mutation. The endpoints do not expose an
    // atomic paused precondition; these calls themselves never start a worker.
    const context = await request("GET", `/api/video/automation/series/${manifest.series_slug}/context?episode=${entry.number}`);
    validateContext(context, manifest, entry);
    if (action === "create") {
      // PUT is an upsert, so a project that appeared after preflight must not
      // have its metadata overwritten. The API has no atomic create-only form.
      try {
        const appeared = await request("GET", `/api/video/reviews/${entry.slug}`);
        throw new Error(`${entry.id}: project appeared during preflight (${checkProject(appeared, manifest, entry)}); rerun intake`);
      } catch (error) {
        if (error?.status !== 404) throw error;
      }
      const created = await request("PUT", `/api/video/reviews/${entry.slug}`, { json: {
        title: entry.title, stage: "script review", checklist: [], category: "story", format: "drama",
        series_slug: manifest.series_slug, episode_number: entry.number,
      } });
      insist(created?.slug === entry.slug && created?.series_slug === manifest.series_slug && created?.episode_number === entry.number && created?.format === "drama", `${entry.id}: project creation readback mismatch`);
    } else {
      const current = await request("GET", `/api/video/reviews/${entry.slug}`);
      const state = checkProject(current, manifest, entry);
      insist(state === "submit" || state === "already-present", `${entry.id}: project changed during import`);
      if (state === "already-present") { results.push({ id: entry.id, action: state, sha256: entry.script_sha256 }); continue; }
    }
    const sent = await request("POST", `/api/video/reviews/${entry.slug}/reviews`, { json: reviewBody(entry) });
    insist(sent?.gate === "script" && sent?.content_sha256 === entry.script_sha256 && sent?.status === "pending" && sent?.payload?.hand_pushed === true, `${entry.id}: review submission did not return a pending manual card for the exact hash`);
    const readback = await request("GET", `/api/video/reviews/${entry.slug}`);
    const expected = reviewBody(entry);
    insist(readback?.reviews?.some((review) => review.id === sent.id && review.status === "pending"
      && review.content_sha256 === entry.script_sha256 && review.summary === expected.summary
      && stableJson(review.payload) === stableJson(expected.payload)),
    `${entry.id}: pending review readback missing or altered`);
    results.push({ id: entry.id, action: "submitted", sha256: entry.script_sha256, review_id: sent.id });
  }
  return results;
}

export function makeRequest({ env = process.env, home, fetchImpl = globalThis.fetch } = {}) {
  const { site, token } = readCredentials({ env, home });
  insist(token && validSite(`${site}/`), "video tool credentials unavailable or site invalid; run video login");
  return async (method, route, { json } = {}) => {
    const response = await fetchImpl(`${site}${route}`, { method,
      headers: { Authorization: `Bearer ${token}`, Accept: "application/json", ...(json ? { "Content-Type": "application/json" } : {}) },
      ...(json ? { body: JSON.stringify(json) } : {}) });
    const body = await response.json().catch(() => ({}));
    if (!response.ok) {
      const error = new Error(`video API ${response.status}: ${typeof body.detail === "string" ? body.detail : "request failed"}`);
      error.status = response.status;
      throw error;
    }
    return body;
  };
}

if (process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  const args = process.argv.slice(2);
  const ids = [];
  let apply = false;
  for (let index = 0; index < args.length; index++) {
    if (args[index] === "--apply") apply = true;
    else if (args[index] === "--id" && args[index + 1]) ids.push(args[++index]);
    else throw new Error(`unknown argument: ${args[index]}`);
  }
  runIntake({ ids, apply, request: apply ? makeRequest() : undefined })
    .then((result) => console.log(JSON.stringify(result, null, 2)))
    .catch((error) => { console.error(error.message); process.exitCode = 1; });
}
