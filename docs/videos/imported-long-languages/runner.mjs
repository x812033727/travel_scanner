#!/usr/bin/env node
// A bounded, explicitly scoped continuation for the six imported long cuts. This never
// invokes auto.step, assemble, package, project PUT, publish, or a YouTube endpoint.
import { createHash, randomUUID } from "node:crypto";
import { request as httpRequest } from "node:http";
import { appendFileSync, closeSync, copyFileSync, existsSync, fsyncSync, mkdirSync, openSync, readFileSync, readSync, statSync } from "node:fs";
import path from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import { parseArgs } from "node:util";
import { Automation } from "../../../tools/video/automation/flow.mjs";
import { main as videoMain, EXIT } from "../../../tools/video/cli.mjs";
import { approvalState, sha256File } from "../../../tools/video/core/approvals.mjs";
import { atomicWrite, isInside, readJson, stopRequested } from "../../../tools/video/core/paths.mjs";
import { dubsForUpload, writeLanguages } from "../../../tools/video/core/stages.mjs";
import { loadProject } from "../../../tools/video/core/state.mjs";
import { speechHash } from "../../../tools/video/core/timeline.mjs";
import { presentationTimeline, readBranding } from "../../../tools/video/core/branding.mjs";
import { bindManualLanguageSubmission, fileInventory, readManualLanguageSource } from "../../../tools/video/review/renewal-handoff.mjs";
import { mergeSheet } from "../../../tools/video/i18n/cli.mjs";
import { composeMetadata } from "../../../tools/video/package/metadata.mjs";
import { ledgerTotals } from "../../../tools/video/media/ledger.mjs";
import { readCredentials } from "../../../tools/video/tts/credentials.mjs";
import { USER_AGENT } from "../../../tools/video/tts/client.mjs";
import { speechStatus } from "../../../tools/video/tts/client.mjs";
import { createSpeechJournalFetch, speechConfiguration } from "./speech-journal.mjs";

export const SLUGS = ["01-image-trust", "02-confident-errors", "03-machine-internet", "04-tasks-and-jobs", "05-uneven-abilities", "06-digital-yesman"].map((id) => `ai-real-world-${id}`);
const LOCALES = ["en", "ja", "ko", "zh-CN"];
const PARTS = ["metadata", "captions", "dub"];
const COMMANDS = new Set(["review-pull", "i18n-sheet", "i18n-merge", "dub", "check-audio", "captions"]);
const CHUNK_BYTES = 4 * 1024 * 1024;
export const DIRECT_STAGE_TIMEOUT_MS = (900 + 60 + 60) * 1000;
const DIRECT_STAGE_MAX_BYTES = 16 * 1024 * 1024;
const DIRECT_STAGE_REQUEST_MAX_BYTES = 4 * 1024 * 1024;
export class HardStop extends Error {}
export class VideoStop extends Error {}
const digest = (value) => createHash("sha256").update(value).digest("hex");
export function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value && typeof value === "object") return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  return JSON.stringify(value);
}
const clean = (message) => String(message).replace(/mkv_[A-Za-z0-9_-]+/g, "[redacted]").replace(/Bearer\s+\S+/gi, "Bearer [redacted]");
const save = (file, value) => atomicWrite(file, `${JSON.stringify(value, null, 2)}\n`);
function savePaidStage(file, value) {
  save(file, value);
  const fd = openSync(file, "r+"); try { fsyncSync(fd); } finally { closeSync(fd); }
  if (process.platform !== "win32") { const dir = openSync(path.dirname(file), "r"); try { fsyncSync(dir); } finally { closeSync(dir); } }
}
const fileEntry = async (file, role, content_type) => ({ path: file, role, content_type, size: statSync(file).size, sha256: await sha256File(file) });
const partStatus = (value) => typeof value === "string" ? value : value?.status;
const ordered = (reviews = []) => [...reviews].sort((a, b) => String(a.created_at).localeCompare(String(b.created_at)));

export function missingPhaseParts(project, phase) {
  return Object.entries(project.locales ?? {}).flatMap(([locale, choice]) => PARTS
    .filter((part) => choice[part] && (phase === "all" || (phase === "dubs" ? part === "dub" : part !== "dub")))
    .filter((part) => !["ready", "skipped", "uploaded"].includes(project.languages?.[locale]?.[part]?.state))
    .map((part) => `${locale}/${part}`));
}

function currentLanguageProject(project, entry) {
  if (!entry.renewal_source || readJson(path.join(entry.workdir, entry.renewal_source.file)).source?.kind !== "approved-final-body-range") return project;
  const final = assertProject(project, entry), reviews = project.reviews.filter((review) => review.gate === "languages" && ["pending", "approved"].includes(review.status) && review.payload?.final_review_id === final.id), languages = structuredClone(project.languages ?? {});
  for (const [locale, parts] of Object.entries(languages)) for (const part of PARTS) {
    if (!["ready", "skipped", "uploaded"].includes(parts?.[part]?.state)) continue;
    const role = `${part === "metadata" ? "description" : part}_${locale}`;
    const bound = reviews.some((review) => {
      const status = partStatus(review.payload?.locales?.[locale]?.[part]);
      return status === "skipped" && part === "dub" || status === "ready" && review.files?.some((file) => file.role === role && /^[a-f0-9]{64}$/.test(file.sha256));
    });
    if (!bound) parts[part] = { ...parts[part], state: "working" };
  }
  return { ...project, languages };
}

export function assertAllowedSlug(slug) {
  if (!SLUGS.includes(slug)) throw new VideoStop(`slug is outside the six-video allowlist: ${slug}`);
}
export function assertProject(project, entry, choices = undefined) {
  assertAllowedSlug(entry.slug);
  if (!project || project.slug !== entry.slug || project.dropped_at || project.shorts_line || (project.format && project.format !== "slides")) throw new VideoStop(`${entry.slug}: missing, dropped, or not an imported long slides video`);
  const latest = ordered(project.reviews).filter((review) => review.gate === "final" && review.status !== "superseded").at(-1);
  if (latest?.status !== "approved" || latest.content_sha256 !== entry.final_sha256) throw new VideoStop(`${entry.slug}: latest final approval does not match the imported file`);
  if (!project.locales_decided_at) throw new VideoStop(`${entry.slug}: the owner has not chosen languages`);
  for (const [locale, parts] of Object.entries(project.locales ?? {})) {
    if (!LOCALES.includes(locale) || Object.keys(parts).some((key) => !PARTS.includes(key)) || Object.values(parts).some((value) => typeof value !== "boolean")) throw new VideoStop(`${entry.slug}: unsupported language choice`);
    if (parts.dub && !parts.captions) throw new VideoStop(`${entry.slug}: a dub requires captions`);
  }
  if (choices !== undefined && canonical(project.locales ?? {}) !== canonical(choices)) throw new VideoStop(`${entry.slug}: owner language choice changed; rerun from a fresh snapshot`);
  return latest;
}

/** Preserve every part of live prior batches: a new pending review supersedes the old pending
 * review. Previously approved dub tracks are omitted so their old approval remains uploaded. */
export function cumulativeSnapshot(project, additions = { locales: {}, files: [] }) {
  const locales = {};
  const files = new Map();
  for (const review of ordered(project.reviews).filter((item) => item.gate === "languages" && ["pending", "approved"].includes(item.status))) {
    for (const [locale, entry] of Object.entries(review.payload?.locales ?? {})) locales[locale] = { ...locales[locale], ...entry };
    for (const file of review.files ?? []) files.set(file.role, file);
  }
  const priorFiles = new Map(files);
  for (const [locale, entry] of Object.entries(additions.locales)) locales[locale] = { ...locales[locale], ...entry };
  for (const file of additions.files) files.set(file.role, file);
  const kept = {};
  const roles = new Set();
  for (const locale of LOCALES) {
    const chosen = project.locales?.[locale] ?? {};
    const source = locales[locale] ?? {};
    const entry = {};
    for (const part of PARTS) {
      if (!chosen[part] || !["ready", "skipped"].includes(partStatus(source[part]))) continue;
      const role = `${part === "metadata" ? "description" : part}_${locale}`;
      if (part === "dub" && project.languages?.[locale]?.dub?.state === "uploaded" && (!additions.locales?.[locale]?.dub || priorFiles.get(role)?.sha256 === files.get(role)?.sha256)) continue;
      if (partStatus(source[part]) === "ready" && !files.has(role)) throw new VideoStop(`ready ${locale}/${part} has no hash-bound file`);
      entry[part] = source[part];
      if (partStatus(source[part]) === "ready") roles.add(role);
      if (part === "dub" && partStatus(source[part]) === "ready") {
        const file = files.get(role);
        Object.assign(entry, { file_role: role, sha256: file.sha256, format: "m4a", file: `${locale}.m4a`, tempo_max: source.tempo_max ?? 1 });
      }
    }
    if (Object.keys(entry).length) kept[locale] = entry;
  }
  return { locales: kept, files: [...roles].sort().map((role) => files.get(role)) };
}

/** Explicit, host-only transport for long subscription stages. No public/custom origin is
 * accepted: this carries the same existing bearer token over the Compose network. */
export function directStageOrigin(env, site) {
  const origin = env?.VIDEO_LANGUAGE_API_ORIGIN;
  if (!origin) return null;
  if (env.MOKAAIR_SITE !== "http://web:3000" || site !== "http://web:3000" || origin !== "http://api:8000") throw new HardStop("VIDEO_LANGUAGE_API_ORIGIN requires the exact internal origins http://web:3000 and http://api:8000");
  return origin;
}

/** Native HTTP avoids fetch/Undici's default five-minute response-header deadline. The
 * total deadline includes waiting for headers and reading the complete bounded response.
 * No redirects or retries are followed here. Test overrides affect transport only. */
export function nativeStageRequest(url, init, { requestImpl = httpRequest, timeoutMs = DIRECT_STAGE_TIMEOUT_MS, maxBytes = DIRECT_STAGE_MAX_BYTES } = {}) {
  return new Promise((resolve, reject) => {
    let finished = false;
    let request;
    let timer;
    const finish = (error, response) => {
      if (finished) return;
      finished = true;
      clearTimeout(timer);
      if (error) reject(error); else resolve(response);
    };
    try {
      const body = init.body ?? "";
      if (Buffer.byteLength(body) > DIRECT_STAGE_REQUEST_MAX_BYTES) throw new VideoStop("Direct language-stage request exceeds the byte limit");
      request = requestImpl(url, { method: init.method, headers: { ...init.headers, "Content-Length": Buffer.byteLength(body) }, agent: false }, (response) => {
        const chunks = [];
        let size = 0;
        response.on("data", (chunk) => {
          size += chunk.length;
          if (size > maxBytes) {
            const error = new VideoStop("Direct language-stage response exceeds the byte limit");
            finish(error);
            response.destroy(error);
            request.destroy(error);
          } else chunks.push(Buffer.from(chunk));
        });
        response.on("error", (error) => finish(error));
        response.on("aborted", () => finish(new VideoStop("Direct language-stage response was interrupted")));
        response.on("end", () => {
          if (finished) return;
          const status = response.statusCode ?? 502;
          finish(null, new Response([204, 205, 304].includes(status) ? null : Buffer.concat(chunks), { status, headers: { "Content-Type": "application/json" } }));
        });
      });
      request.on("error", (error) => finish(error));
      timer = setTimeout(() => {
        const error = new VideoStop(`Direct language stage exceeded the ${timeoutMs / 1000}s total deadline`);
        finish(error);
        request.destroy(error);
      }, timeoutMs);
      request.end(body);
    } catch (error) { finish(error); request?.destroy(); }
  });
}

/** No call in this client can change owner choices, project fields, approvals, or YouTube. */
export function createSiteClient(ctx) {
  const { site, token } = readCredentials({ env: ctx.env, home: ctx.home });
  if (!token) throw new HardStop("No video tool token; pair the existing video CLI first.");
  const direct = directStageOrigin(ctx.env, site);
  const request = async (method, route, body, binary = false) => {
    const attempts = ["GET", "PUT"].includes(method) ? 2 : 1;
    const uncertain = method === "POST" ? "; POST was not retried because the work may already have completed; inspect its result before resuming" : "";
    for (let attempt = 0; attempt < attempts; attempt++) {
      let response;
      try {
        const init = {
          method, headers: { Authorization: `Bearer ${token}`, "User-Agent": USER_AGENT, "Accept-Language": "zh-TW", ...(body !== undefined ? { "Content-Type": binary ? "application/octet-stream" : "application/json" } : {}) },
          body: body === undefined ? undefined : binary ? body : JSON.stringify(body),
        };
        response = direct && method === "POST" && route === "automation/run"
          ? await (ctx.nativeStageRequest ?? nativeStageRequest)(`${direct}/api/v1/video/automation/run`, init)
          : await ctx.fetch(`${site}/api/video/${route}`, init);
      } catch (error) {
        if (error instanceof HardStop) throw error;
        if (attempt === attempts - 1) throw new VideoStop(`${clean(error.message)}${uncertain}`);
        await ctx.sleep(1000);
        continue;
      }
      const result = await response.json().catch(() => ({}));
      if (response.ok) return result;
      const message = clean(result.detail ?? result.title ?? `HTTP ${response.status}`);
      if ([401, 403, 429].includes(response.status) || /budget|quota|subscription_paused|token_invalid|provider_not_configured/.test(result.code ?? "")) throw new HardStop(message);
      if (response.status < 500 || attempt === attempts - 1) throw new VideoStop(`${message}${response.status >= 500 ? uncertain : ""}`);
      await ctx.sleep(1000);
    }
    throw new VideoStop("Request did not finish");
  };
  return {
    settings: () => request("GET", "automation/settings"),
    reviews: (slug) => { assertAllowedSlug(slug); return request("GET", `reviews/${slug}`); },
    run: (stage, slug, instructions, payload, max_output_tokens, format, variant = null) => {
      assertAllowedSlug(slug);
      if (!["translator", "caption_reviewer"].includes(stage)) throw new VideoStop(`stage is not permitted: ${stage}`);
      return request("POST", "automation/run", { stage, slug, instructions, payload, max_output_tokens, format, ...(variant ? { variant } : {}) });
    },
    submit: (slug, body) => {
      assertAllowedSlug(slug);
      if (body.gate !== "languages") throw new VideoStop("Only a languages review is permitted");
      return request("POST", `reviews/${slug}/reviews`, body);
    },
    upload: async (slug, entry) => {
      assertAllowedSlug(slug);
      const current = await fileEntry(entry.path, entry.role, entry.content_type);
      if (current.sha256 !== entry.sha256 || current.size !== entry.size) throw new VideoStop("An output changed before upload");
      const parts = Math.max(1, Math.ceil(entry.size / CHUNK_BYTES));
      const handle = openSync(entry.path, "r");
      let complete = false;
      try {
        for (let part = 0; part < parts; part++) {
          const bytes = Buffer.alloc(Math.min(CHUNK_BYTES, entry.size - part * CHUNK_BYTES));
          readSync(handle, bytes, 0, bytes.length, part * CHUNK_BYTES);
          const query = new URLSearchParams({ part: String(part), parts: String(parts), size: String(entry.size) });
          const result = await request("PUT", `reviews/${slug}/files/${entry.sha256}?${query}`, bytes, true);
          if (result.complete) { complete = true; break; }
        }
      } finally { closeSync(handle); }
      if (!complete) throw new VideoStop("The review store did not confirm the complete file");
      const { path: omitted, ...record } = entry;
      return record;
    },
  };
}

const sheetSource = (sheet) => ({
  slug: sheet.slug, locale: sheet.locale, parts: sheet.parts,
  lines: sheet.lines?.map(({ id, scene, source, max_chars }) => ({ id, scene, source, max_chars })),
  chapters: sheet.chapters?.map(({ scene, source }) => ({ scene, source })),
  ...Object.fromEntries(["title", "description", "tags"].map((key) => [key, sheet[key] === null ? null : { source: sheet[key]?.source }])),
});

/** Source validation is not a review or a merge: an interrupted translator's worksheet
 * is reusable only against the exact current identity, parts, sources and dub budgets. */
export function validateResumeSheet(sheet, fresh, doc, previous) {
  if (canonical(sheetSource(sheet)) !== canonical(sheetSource(fresh))) throw new VideoStop(`${fresh.locale}: saved worksheet identity, source, or dub budget differs from the current sheet; preserved for inspection`);
  const { problems } = mergeSheet(doc, sheet, previous);
  if (problems.length) throw new VideoStop(`${fresh.locale}: saved worksheet is incomplete or invalid: ${problems.join("; ")}`);
}

/** Reuse paid translation bytes after an interrupted reviewer, never its missing review.
 * The standard sheet command still determines the current sources and character budgets. */
export async function translateLocaleResuming(automation, ctx, entry, state, locale, parts, project, event = () => {}) {
  const file = path.join(entry.workdir, "i18n", `${locale}.todo.json`);
  const saved = existsSync(file) ? readFileSync(file, "utf8") : null;
  const worksheet = saved === null ? null : JSON.parse(saved);
  const filled = (value) => typeof value === "string" ? value.trim().length > 0 : Array.isArray(value) && value.length > 0;
  const hasTranslation = worksheet && [...(worksheet.lines ?? []), ...(worksheet.chapters ?? []), worksheet.title, worksheet.description, worksheet.tags].some((item) => filled(item?.text));
  if (!hasTranslation) {
    // The shared flow accepts an absent reviewer worksheet and then merges the translator's
    // copy. This isolated lane requires both actual outputs to pass the source/completeness
    // guard; keeping its existing flow preserves prompts, accounting and failure handling.
    const stage = automation.stage;
    automation.stage = async (...args) => {
      const answer = await stage.call(automation, ...args);
      if (!["translator", "caption_reviewer"].includes(args[0])) return answer;
      const fresh = args[2].worksheet;
      if (!Array.isArray(answer.worksheet?.lines)) throw new VideoStop(`${locale}: ${args[0]} returned no worksheet`);
      const checked = { locale, slug: fresh.slug, parts: fresh.parts, ...answer.worksheet };
      validateResumeSheet(checked, fresh, args[2].video ?? project.doc, project.translations[locale]);
      return { ...answer, worksheet: checked };
    };
    try { return await automation.translateLocale(state, locale, parts, project.doc); }
    finally { automation.stage = stage; }
  }

  const savedHash = digest(saved);
  const backup = path.join(entry.workdir, "i18n", `${locale}.todo.resume-${savedHash}.json`);
  if (!existsSync(backup)) atomicWrite(backup, saved);
  let fresh;
  try {
    const result = await ctx.runCommand(["i18n-sheet", "--slug", state.slug, "--locale", locale, "--parts", parts.join(",")]);
    if (result.code !== 0) throw new VideoStop(`${locale}: could not validate the saved worksheet against a fresh sheet: ${result.out}`);
    fresh = readJson(file, null);
    if (!fresh) throw new VideoStop(`${locale}: no fresh worksheet was produced`);
  } finally { atomicWrite(file, saved); }
  validateResumeSheet(worksheet, fresh, project.doc, project.translations[locale]);
  event({ slug: state.slug, type: "translation-resumed", locale, worksheet_sha256: savedHash, stage: "caption_reviewer" });
  const reviewed = await automation.stage("caption_reviewer", state.slug, { locale, parts, worksheet, video: project.doc }, 32_000, state.format);
  if (!Array.isArray(reviewed.worksheet?.lines)) throw new VideoStop(`${locale}: caption reviewer returned no worksheet; original translation retained`);
  // The model may omit identity, as in the standard flow, but cannot replace it.
  const checked = { locale, slug: fresh.slug, parts: fresh.parts, ...reviewed.worksheet };
  validateResumeSheet(checked, fresh, project.doc, project.translations[locale]);
  save(file, checked);
  const merged = await ctx.runCommand(["i18n-merge", "--slug", state.slug, "--locale", locale]);
  if (merged.code !== 0) throw new VideoStop(`${locale}: reviewed worksheet did not merge: ${merged.out}`);
  automation.cleared(state, "translator");
  automation.persist(state);
  return `${state.slug}: saved ${locale} translation independently reviewed and merged`;
}

export function resolveManifest(raw, base) {
  const resolve = (value) => path.resolve(base, raw.portable ? value.replaceAll("\\", "/") : value);
  if (raw.portable && (!raw.relative_paths?.root || !raw.relative_paths?.work_base || !isInside(resolve(raw.relative_paths.root), base) || !isInside(resolve(raw.relative_paths.work_base), base))) throw new VideoStop("Portable root and work paths must stay inside the batch");
  return { ...raw, base, root: resolve(raw.relative_paths?.root ?? raw.root), work_base: resolve(raw.relative_paths?.work_base ?? raw.work_base), videos: raw.videos?.map((entry) => ({
    ...entry, doc_file: resolve(entry.relative_paths?.doc_file ?? entry.doc_file), workdir: resolve(entry.relative_paths?.workdir ?? entry.workdir), provenance_file: entry.provenance_file ? resolve(entry.relative_paths?.provenance_file ?? entry.provenance_file) : undefined,
    source: raw.portable ? entry.source : Object.fromEntries(Object.entries(entry.source ?? {}).map(([key, value]) => [key, resolve(value)])),
    source_files: raw.portable ? entry.source_files : entry.source_files?.map((file) => ({ ...file, path: resolve(file.path) })),
  })) };
}

/** Freeze a NEW portable language batch around exact owner-approved replacements. Original
 * batch, progress, worksheets and uncertain API receipts stay intact. Output remains stopped;
 * preparation neither generates a language nor authorizes retrying an interrupted paid POST. */
export async function prepareRenewedBatch({ manifestFile, handoffs, out, readRemote, runtimeRoot = fileURLToPath(new URL("../../..", import.meta.url)) }) {
  const base = path.dirname(path.resolve(manifestFile)), raw = readJson(manifestFile);
  if (!raw.portable || typeof readRemote !== "function" || existsSync(out) || isInside(out, base) || isInside(base, out)) throw new VideoStop("Renewed language preparation requires a fresh separate portable batch and owner-state probe");
  const manifest = resolveManifest(raw, base), prepared = structuredClone(raw);
  const sources = new Map(handoffs.map((v) => [v.slug, v.workdir]));
  if (!sources.size || sources.size !== handoffs.length) throw new VideoStop("No or duplicate renewed language handoffs");
  for (const slug of sources.keys()) assertAllowedSlug(slug);
  for (const slug of sources.keys()) if (!manifest.videos.some((v) => v.slug === slug)) throw new VideoStop(`${slug}: renewed handoff is outside the original batch`);
  for (const entry of manifest.videos) await verifyLocal(manifest, entry);
  const exclusions = ["runner.lock", `${raw.relative_paths.root.replaceAll("\\", "/").replace(/\/$/, "")}/node_modules`];
  const before = await fileInventory(base, { exclude: exclusions });
  mkdirSync(out, { recursive: false });
  atomicWrite(path.join(out, "STOP"), "Preparing renewed language sources; retain STOP on every failure.\n");
  for (const [name, proof] of Object.entries(before)) {
    const target = path.join(out, name); mkdirSync(path.dirname(target), { recursive: true }); copyFileSync(path.join(base, name), target);
    if (await sha256File(target) !== proof.sha256) throw new VideoStop("Original language batch changed while copying; output remains held");
  }
  atomicWrite(path.join(out, "STOP"), "Prepared renewed language sources; inspect previous paid request receipts before owner-authorized continuation.\n");
  if (existsSync(path.join(out, "progress.json"))) {
    mkdirSync(path.join(out, "retained-source"), { recursive: true }); copyFileSync(path.join(out, "progress.json"), path.join(out, "retained-source/previous-progress.json"));
    save(path.join(out, "progress.json"), { videos: {}, renewal_source_preparation: true, previous_progress_preserved: "retained-source/previous-progress.json" });
  }
  // The previous batch's isolated runtime cannot consume this new contract. Freeze the
  // current reviewed code in the NEW batch and retain every replaced code byte separately.
  const codeNames = ["tools/video", ".agents/skills/youtube-video"], runtimeFiles = [];
  for (const name of codeNames) {
    for (const [relative, proof] of Object.entries(await fileInventory(path.join(runtimeRoot, name)))) runtimeFiles.push({ name: `${name}/${relative}`, source: path.join(runtimeRoot, name, relative), proof });
  }
  for (const name of ["runner.mjs", "prepare.mjs", "preflight.mjs", "speech-journal.mjs"]) {
    const source = path.join(runtimeRoot, "docs/videos/imported-long-languages", name);
    runtimeFiles.push({ name: `docs/videos/imported-long-languages/${name}`, source, proof: { sha256: await sha256File(source), size: statSync(source).size } });
  }
  const shared = new Map((prepared.shared_generated_files ?? []).map((v) => [v.relative_path.replaceAll("\\", "/"), v]));
  for (const { name, source, proof } of runtimeFiles) {
    const target = path.resolve(out, raw.relative_paths.root, name);
    if (!isInside(target, out)) throw new VideoStop("Runtime path escapes the new portable batch");
    if (existsSync(target)) { const old = path.join(out, "retained-source/runtime", name); mkdirSync(path.dirname(old), { recursive: true }); copyFileSync(target, old); }
    mkdirSync(path.dirname(target), { recursive: true }); copyFileSync(source, target);
    if (await sha256File(target) !== proof.sha256 || await sha256File(source) !== proof.sha256) throw new VideoStop("Runtime changed during freeze; output remains stopped");
    const relative_path = path.relative(out, target).split(path.sep).join("/");
    shared.set(relative_path, { role: "renewed-language-runtime", relative_path, bytes: proof.size, sha256: proof.sha256 });
  }
  prepared.shared_generated_files = [...shared.values()];
  if (existsSync(path.join(out, "runtime-receipt.json"))) { mkdirSync(path.join(out, "retained-source"), { recursive: true }); copyFileSync(path.join(out, "runtime-receipt.json"), path.join(out, "retained-source/previous-runtime-receipt.json")); }
  save(path.join(out, "runtime-receipt.json"), { kind: "renewed-language-runtime", files: runtimeFiles.map(({ name, proof }) => ({ path: `${raw.relative_paths.root}/${name}`, sha256: proof.sha256 })) });
  for (const entry of prepared.videos) {
    if (!sources.has(entry.slug)) continue;
    const sourceWorkdir = sources.get(entry.slug), remote = await readRemote(entry.slug), contract = await readManualLanguageSource({ workdir: sourceWorkdir, remote });
    if (contract.source.kind === "approved-final-body-range" || contract.source.original_final.content_sha256 !== entry.final_sha256 || !contract.adapter) throw new VideoStop(`${entry.slug}: renewal lacks the old batch's real retained source adapter`);
    const oldProject = loadProject({ slug: entry.slug, root: manifest.root });
    if (contract.adapter.doc_sha256 !== digest(JSON.stringify(oldProject.doc)) || contract.adapter.lexicon_sha256 !== digest(JSON.stringify(oldProject.lexicon))) throw new VideoStop(`${entry.slug}: renewal adapter does not match the retained language source script/lexicon`);
    const workdir = path.resolve(out, entry.relative_paths.workdir);
    if (!isInside(workdir, out)) throw new VideoStop("Renewed work path escapes the new portable batch");
    const keep = path.join(workdir, "retained-source/adapter-original-final.mp4"); mkdirSync(path.dirname(keep), { recursive: true }); copyFileSync(path.join(workdir, "final.mp4"), keep);
    const sourceFiles = await fileInventory(sourceWorkdir, { exclude: ["STOP"] });
    for (const [name, proof] of Object.entries(sourceFiles)) {
      const target = path.join(workdir, name); mkdirSync(path.dirname(target), { recursive: true }); copyFileSync(path.join(sourceWorkdir, name), target);
      if (await sha256File(target) !== proof.sha256) throw new VideoStop("Renewal handoff changed while copying; output remains held");
    }
    copyFileSync(path.join(workdir, contract.adapter.timeline_file), path.join(workdir, "timeline.json"));
    entry.final_sha256 = contract.source.final.content_sha256;
    entry.renewal_source = { file: "renewal-language-source.json", sha256: await sha256File(path.join(workdir, "renewal-language-source.json")) };
    const changed = new Map((entry.generated_files ?? []).map((v) => [v.relative_path.replaceAll("\\", "/"), v]));
    for (const name of ["final.mp4", "timeline.json", ...Object.keys(sourceFiles).filter((v) => v !== "renewal-handoff.json" && !v.startsWith("review/") && !v.startsWith("language-package/"))]) {
      const file = path.join(workdir, name), relative_path = path.relative(out, file).split(path.sep).join("/");
      changed.set(relative_path, { role: "renewed-source", relative_path, bytes: statSync(file).size, sha256: await sha256File(file) });
    }
    entry.generated_files = [...changed.values()];
  }
  if (canonical(before) !== canonical(await fileInventory(base, { exclude: exclusions }))) throw new VideoStop("Original language batch changed during prepare; do not run the new batch");
  save(path.join(out, "manifest.json"), prepared);
  const current = resolveManifest(prepared, out);
  for (const entry of current.videos) { await verifyLocal(current, entry); if (entry.renewal_source) await readManualLanguageSource({ workdir: entry.workdir, remote: await readRemote(entry.slug) }); }
  return { manifest: path.join(out, "manifest.json"), status: "prepared-held", renewed: [...sources.keys()], paid_generation: false };
}

/** An exit code alone is insufficient: STOP also returns zero. Require a new completed
 * check run, matching flags/timeline, and transcripts for the exact clips being packaged. */
export async function prepareApprovedFinalBatch({ manifestFile, handoffs, out, readRemote, runtimeRoot = fileURLToPath(new URL("../../..", import.meta.url)) }) {
  const base = path.dirname(path.resolve(manifestFile)), raw = readJson(manifestFile);
  if (!raw.portable || typeof readRemote !== "function" || existsSync(out) || isInside(out, base) || isInside(base, out)) throw new VideoStop("Current approved source preparation requires a new separate portable batch");
  const old = resolveManifest(raw, base), sources = new Map(handoffs.map((v) => [v.slug, v.workdir]));
  if (!sources.size || sources.size !== handoffs.length) throw new VideoStop("Missing or duplicate current approved sources");
  for (const slug of sources.keys()) { assertAllowedSlug(slug); if (!old.videos.some((v) => v.slug === slug)) throw new VideoStop(`${slug}: current source is outside the retained batch`); }
  for (const entry of old.videos) await verifyLocal(old, entry);
  const exclusions = ["runner.lock", `${raw.relative_paths.root.replaceAll("\\", "/").replace(/\/$/, "")}/node_modules`], before = await fileInventory(base, { exclude: exclusions });
  // Credentials/site home are never archival source material. Refuse rather than
  // silently copy a secret, even when an operator supplied a broader old directory.
  if (Object.keys(before).some((v) => /(?:^|\/)(?:\.env(?:\..*)?|tokens?\.json|credentials\.json|site-home)(?:\/|$)/i.test(v))) throw new VideoStop("The retained batch includes credentials/site home; isolate artifacts first");
  mkdirSync(out); atomicWrite(path.join(out, "STOP"), "New approved-final source batch; no paid continuation until owner review.\n");
  const retained = "retained-source/original-batch";
  for (const [name, proof] of Object.entries(before)) {
    const target = path.join(out, retained, name); mkdirSync(path.dirname(target), { recursive: true }); copyFileSync(path.join(base, name), target);
    if (await sha256File(target) !== proof.sha256 || await sha256File(path.join(base, name)) !== proof.sha256) throw new VideoStop("Retained old source changed while archiving; new batch stays held");
  }
  const prepared = { ...structuredClone(raw), portable: true, root: "root", work_base: "work", relative_paths: { root: "root", work_base: "work" }, source_kind: "approved-final-body-range", request_namespace: randomUUID(), retained_source: { manifest: `${retained}/manifest.json`, inventory: before, paid_requests: "retained unchanged; uncertain old requests are never resumed by this new source", budget_policy: "Prior spend and unknown-call accounting remain charged; remote budgets/settings are unchanged." }, shared_generated_files: [], videos: [] };
  const shared = [], runtimeFiles = [];
  for (const name of ["tools/video", ".agents/skills/youtube-video"]) for (const [relative, proof] of Object.entries(await fileInventory(path.join(runtimeRoot, name)))) runtimeFiles.push({ name: `${name}/${relative}`, source: path.join(runtimeRoot, name, relative), proof });
  for (const name of ["runner.mjs", "prepare.mjs", "preflight.mjs", "speech-journal.mjs"]) {
    const source = path.join(runtimeRoot, "docs/videos/imported-long-languages", name); runtimeFiles.push({ name: `docs/videos/imported-long-languages/${name}`, source, proof: { sha256: await sha256File(source), size: statSync(source).size } });
  }
  for (const { name, source, proof } of runtimeFiles) {
    const target = path.join(out, "root", name); mkdirSync(path.dirname(target), { recursive: true }); copyFileSync(source, target);
    if (await sha256File(target) !== proof.sha256 || await sha256File(source) !== proof.sha256) throw new VideoStop("Current runtime changed during freeze; new source stays held");
    shared.push({ role: "current-source-runtime", relative_path: `root/${name}`, bytes: proof.size, sha256: proof.sha256 });
  }
  const lexicons = [];
  for (const [slug, sourceWorkdir] of sources) {
    const remote = await readRemote(slug), contract = await readManualLanguageSource({ workdir: sourceWorkdir, remote });
    if (contract.source.kind !== "approved-final-body-range" || !contract.adapter) throw new VideoStop(`${slug}: new-source batch requires a current approved final-range adapter`);
    const project = readJson(path.join(sourceWorkdir, contract.adapter.project_file)); lexicons.push(canonical(project.lexicon));
    if (lexicons.some((v) => v !== lexicons[0])) throw new VideoStop("Current source lexicons differ; do not merge or silently replace source spelling");
    const workdir = path.join(out, "work", slug), docFile = path.join(out, "root/docs/videos", slug, "video.json");
    const incoming = await fileInventory(sourceWorkdir, { exclude: ["STOP"] });
    if (Object.keys(incoming).some((v) => /^(?:dubs|captions|i18n|review|language-package|automation)\//.test(v))) throw new VideoStop("Current handoff contains prior active paid/language outputs; prepare a clean source snapshot");
    for (const [name, proof] of Object.entries(incoming)) {
      const target = path.join(workdir, name); mkdirSync(path.dirname(target), { recursive: true }); copyFileSync(path.join(sourceWorkdir, name), target);
      if (await sha256File(target) !== proof.sha256 || await sha256File(path.join(sourceWorkdir, name)) !== proof.sha256) throw new VideoStop("Current source changed during batch copy");
    }
    save(docFile, project.doc); save(path.join(out, "root/docs/videos/lexicon.json"), project.lexicon);
    // Editorial brief is retained context only, never old script/translation authority.
    const brief = path.join(old.root, "docs/videos", slug, "brief.md"), briefFile = path.join(path.dirname(docFile), "brief.md");
    if (!existsSync(brief)) throw new VideoStop(`${slug}: retained editorial brief is missing`);
    copyFileSync(brief, briefFile);
    copyFileSync(path.join(workdir, contract.adapter.timeline_file), path.join(workdir, "timeline.json"));
    const oldEntry = old.videos.find((v) => v.slug === slug), ledger = path.join(oldEntry.workdir, "media/ledger.json");
    // Copy the authoritative per-project ledger, without its old dispatch/cache state.
    // Native ledgerTotals must continue to charge prior entries in the NEW workdir.
    if (existsSync(ledger)) { const target = path.join(workdir, "media/ledger.json"); mkdirSync(path.dirname(target), { recursive: true }); copyFileSync(ledger, target); }
    const oldTotals = ledgerTotals(oldEntry.workdir);
    if (canonical(oldTotals) !== canonical(ledgerTotals(workdir))) throw new VideoStop("Current source would reset its inherited media budget");
    save(path.join(workdir, "source-accounting.json"), { schema_version: 1, source_kind: contract.source.kind, inherited_media_ledger: existsSync(ledger) ? { file: "media/ledger.json", sha256: await sha256File(ledger), totals: oldTotals } : null, inherited_media_totals: oldTotals, monthly_subscription_authority: "Existing backend account/slugs and monthly token/speech budgets; this prepare creates no budget or refund.", retained_paid_progress: `${retained}/progress.json`, retained_paid_source: `${retained}/${path.relative(base, oldEntry.workdir).split(path.sep).join("/")}`, uncertain_request_policy: "Old worksheets/results/request receipts remain retained; unknown paid outcomes are not retried, cleared or credited by this new source." });
    atomicWrite(path.join(workdir, "STOP"), "Current source prepared; no generation authorized by preparation.\n");
    // review-pull/writeLanguages refresh synced_at. Owner choices remain pinned by
    // the contract and fresh remote reads; that mutable local mirror is not source evidence.
    const generated = Object.entries(await fileInventory(workdir, { exclude: ["STOP", "languages.json"] })).map(([name, proof]) => ({ role: "current-approved-source", relative_path: `work/${slug}/${name}`, bytes: proof.size, sha256: proof.sha256 }));
    generated.push({ role: "current-approved-script", relative_path: `root/docs/videos/${slug}/video.json`, bytes: statSync(docFile).size, sha256: await sha256File(docFile) });
    generated.push({ role: "retained-editorial-context", relative_path: `root/docs/videos/${slug}/brief.md`, bytes: statSync(briefFile).size, sha256: await sha256File(briefFile) });
    prepared.videos.push({ slug, doc_file: `root/docs/videos/${slug}/video.json`, workdir: `work/${slug}`, relative_paths: { doc_file: `root/docs/videos/${slug}/video.json`, workdir: `work/${slug}` }, final_sha256: contract.source.final.content_sha256, source: { final: contract.source.final.content_sha256 }, source_files: Object.values(contract.evidence).map((v) => ({ role: v.role, sha256: v.sha256, bytes: v.size, path: `work/${slug}/${v.file}` })), generated_files: generated, renewal_source: { file: "renewal-language-source.json", sha256: await sha256File(path.join(workdir, "renewal-language-source.json")) }, previous_source_retained: `${retained}/work/${slug}`, choice: contract.choice });
  }
  const lexicon = path.join(out, "root/docs/videos/lexicon.json"); shared.push({ role: "current-approved-lexicon", relative_path: "root/docs/videos/lexicon.json", bytes: statSync(lexicon).size, sha256: await sha256File(lexicon) }); prepared.shared_generated_files = shared;
  save(path.join(out, "runtime-receipt.json"), { kind: "approved-final-language-runtime", request_namespace: prepared.request_namespace, files: runtimeFiles.map(({ name, proof }) => ({ path: `root/${name}`, sha256: proof.sha256 })) });
  save(path.join(out, "progress.json"), { videos: {}, request_namespace: prepared.request_namespace, retained_paid_accounting: `${retained}/progress.json`, previous_translations_stale: true });
  if (canonical(before) !== canonical(await fileInventory(base, { exclude: exclusions }))) throw new VideoStop("Retained original batch changed during preparation");
  save(path.join(out, "manifest.json"), prepared);
  const current = resolveManifest(prepared, out);
  for (const entry of current.videos) { await verifyLocal(current, entry); await readManualLanguageSource({ workdir: entry.workdir, remote: await readRemote(entry.slug) }); }
  return { manifest: path.join(out, "manifest.json"), status: "prepared-held", source_kind: prepared.source_kind, renewed: [...sources.keys()], paid_generation: false };
}

export async function checkedDubReceipt(entry, locale, beforeRuns) {
  const runs = readJson(path.join(entry.workdir, "state.json"), { runs: [] }).runs;
  const check = runs.slice(beforeRuns).filter((item) => item.stage === "check-audio" && item.locale === locale).at(-1);
  const timeline = readJson(path.join(entry.workdir, "dubs", locale, "timeline.json"), null);
  const flags = readJson(path.join(entry.workdir, "review", `check-flags.${locale}.json`), null);
  const cache = readJson(path.join(entry.workdir, "review", `check.${locale}.json`), null);
  const translationFile = path.join(path.dirname(entry.doc_file), "i18n", `${locale}.json`);
  const translation = readJson(translationFile, null);
  const expected = timeline?.lines?.length ?? 0;
  if (!check || !expected || check.lines !== expected || check.unchecked !== 0 || check.flagged !== 0 || flags?.locale !== locale || flags.speech_hash !== timeline.speech_hash || flags.translation_hash !== timeline.translation_hash || !Array.isArray(flags.flags) || flags.flags.length) throw new VideoStop(`${locale}: no new, complete audio check for this dub`);
  for (const line of timeline.lines) {
    const checked = cache?.lines?.[line.id];
    const clip = path.join(entry.workdir, "dubs", locale, "audio", `${line.id}.wav`);
    if (!checked || typeof checked.heard !== "string" || checked.intended !== translation?.lines?.[line.id]?.text || checked.clip !== (await sha256File(clip)).slice(0, 16)) throw new VideoStop(`${locale}: audio check does not cover the current clip ${line.id}`);
  }
  return { sha256: await sha256File(path.join(entry.workdir, "dubs", `${locale}.m4a`)), speech_hash: timeline.speech_hash, translation_hash: timeline.translation_hash, translation_sha256: await sha256File(translationFile), check_at: check.at };
}

export async function verifyLocal(manifest, entry) {
  assertAllowedSlug(entry.slug);
  if (path.resolve(entry.doc_file) !== path.join(path.resolve(manifest.root), "docs", "videos", entry.slug, "video.json") || path.resolve(entry.workdir) !== path.join(path.resolve(manifest.work_base), entry.slug) || isInside(manifest.work_base, manifest.root)) throw new VideoStop("Manifest paths do not match the isolated workspace");
  const localFinal = path.join(entry.workdir, "final.mp4");
  if (await sha256File(localFinal) !== entry.final_sha256 || (!manifest.portable && await sha256File(entry.source.final) !== entry.final_sha256)) throw new VideoStop(`${entry.slug}: original or working final changed`);
  if (!Array.isArray(entry.source_files) || !entry.source_files.length) throw new VideoStop("Missing source provenance hashes");
  const files = manifest.portable ? [...(manifest.shared_generated_files ?? []), ...(entry.generated_files ?? [])] : entry.source_files;
  if (!files.length) throw new VideoStop("Missing portable artifact hashes");
  for (const file of files) {
    const target = manifest.portable ? path.resolve(manifest.base, file.relative_path.replaceAll("\\", "/")) : file.path;
    if (manifest.portable && !isInside(target, manifest.base)) throw new VideoStop("Portable artifact escapes the batch");
    if (statSync(target).size !== file.bytes || await sha256File(target) !== file.sha256) throw new VideoStop(`${entry.slug}: source changed: ${file.role ?? file.relative_path}`);
  }
  const project = loadProject({ slug: entry.slug, root: manifest.root });
  const timeline = readJson(path.join(entry.workdir, "timeline.json"));
  if (project.doc.slug !== entry.slug || timeline.speech_hash !== speechHash(project.doc, project.lexicon)) throw new VideoStop(`${entry.slug}: adapter timeline is stale`);
  if (entry.renewal_source) {
    const file = path.resolve(entry.workdir, entry.renewal_source.file);
    if (!isInside(file, entry.workdir) || await sha256File(file) !== entry.renewal_source.sha256) throw new VideoStop(`${entry.slug}: renewed language source contract changed`);
    const contract = readJson(file);
    if ((manifest.source_kind === "approved-final-body-range") !== (contract.source?.kind === "approved-final-body-range")) throw new VideoStop(`${entry.slug}: batch source kind differs from its pinned source contract`);
    if (contract.source?.final?.content_sha256 !== entry.final_sha256 || !contract.adapter || contract.adapter.timeline_sha256 !== await sha256File(path.join(entry.workdir, "timeline.json"))) throw new VideoStop(`${entry.slug}: renewed source lacks its real retained timing adapter`);
  }
  return project;
}

async function localAdditions(entry, project, progress, choices) {
  const timeline = readJson(path.join(entry.workdir, "timeline.json"));
  const captions = readJson(path.join(entry.workdir, "captions", "manifest.json"), null);
  const result = { locales: {}, files: [], problems: [] };
  const { dubs, skipped } = dubsForUpload(project, entry.workdir, timeline.speech_hash, LOCALES.filter((locale) => choices[locale]?.dub));
  for (const locale of LOCALES) {
    const choice = choices[locale];
    if (!choice) continue;
    const fields = {};
    const translation = path.join(project.dir, "i18n", `${locale}.json`);
    const ready = existsSync(translation) && progress.translations?.[locale] === await sha256File(translation);
    if (ready && choice.metadata) {
      const composed = composeMetadata({ doc: project.doc, timeline: entry.renewal_source ? presentationTimeline(timeline, { hash: readBranding(entry.workdir).hash, intro_frames: readBranding(entry.workdir).intro.frames, outro_frames: readBranding(entry.workdir).outro.frames, body_frames: timeline.total_frames }) : timeline, translations: project.translations, pack: project.pack ?? null, locales: [locale] });
      result.problems.push(...composed.problems);
      if (!composed.problems.length && composed.metadata.localizations[locale]) {
        const localized = composed.metadata.localizations[locale];
        const file = path.join(entry.workdir, "language-package", `description.${locale}.txt`);
        atomicWrite(file, `${localized.title}\n\n${localized.description}\n`);
        result.files.push(await fileEntry(file, `description_${locale}`, "text/plain"));
        fields.metadata = "ready";
      }
    }
    if (ready && choice.captions && captions?.speech_hash === timeline.speech_hash && captions.locales?.[locale]?.cues > 0 && !captions.locales[locale].problems.length) {
      result.files.push(await fileEntry(path.join(entry.workdir, "captions", `${locale}.srt`), `captions_${locale}`, "text/plain"));
      fields.captions = "ready";
    }
    if (ready && choice.captions) result.problems.push(...(captions?.locales?.[locale]?.problems ?? []).map((problem) => `${locale}: ${problem}`));
    const dub = dubs.find((item) => item.locale === locale);
    if (choice.dub && dub?.format === "m4a" && progress.checked_dubs?.[locale]?.speech_hash === timeline.speech_hash && progress.checked_dubs[locale].sha256 === await sha256File(dub.file) && progress.checked_dubs[locale].translation_sha256 === (existsSync(translation) ? await sha256File(translation) : null)) {
      result.files.push(await fileEntry(dub.file, `dub_${locale}`, "audio/mp4"));
      fields.dub = "ready";
      fields.tempo_max = dub.tempo_max;
    } else if (choice.dub && skipped[locale] !== undefined && progress.skipped_dubs?.[locale] === skipped[locale]) fields.dub = { status: "skipped", reason: skipped[locale] };
    if (Object.keys(fields).length) result.locales[locale] = fields;
  }
  return result;
}

export async function submitSnapshot(api, project, entry, additions, choices, now) {
  const fresh = await api.reviews(entry.slug);
  const approved = assertProject(fresh, entry, choices);
  // Approval/choice drift is checked again immediately before the mutating request. The
  // review API has no conditional-write token; this is an operator-scoped run, not a queue.
  const contract = entry.renewal_source ? await readManualLanguageSource({ workdir: entry.workdir, remote: fresh }) : null;
  const currentSource = contract?.source.kind === "approved-final-body-range";
  const snapshot = cumulativeSnapshot(currentSource ? { ...fresh, reviews: fresh.reviews.filter((r) => r.gate !== "languages" || r.payload?.final_review_id === approved.id) } : fresh, additions);
  if (!Object.keys(snapshot.locales).length) return { status: "nothing-ready" };
  if (approved.payload?._final_renewal) {
    if (!entry.renewal_source) throw new VideoStop(`${entry.slug}: renewed final requires an explicit source-bound language handoff; old adapter cannot be relabelled`);
    await readManualLanguageSource({ workdir: entry.workdir, remote: fresh });
    for (const file of snapshot.files) if (file.path) await api.upload(entry.slug, file);
    const body = await bindManualLanguageSubmission({ body: { gate: "languages", content_sha256: digest("source-bound manifest pending"), summary: `匯入長片新版語言批次：${Object.keys(snapshot.locales).join("、")}；配音上傳另由站主確認。`, payload: { locales: snapshot.locales }, files: snapshot.files.map(({ path: omitted, ...file }) => file) }, remote: fresh, workdir: entry.workdir, project, upload: async (_request, slug, file, role, type) => {
      const entry = await fileEntry(file, role, type); await api.upload(slug, entry); const { path: omitted, ...ref } = entry; return ref;
    } });
    const current = await api.reviews(entry.slug); assertProject(current, entry, choices);
    await readManualLanguageSource({ workdir: entry.workdir, remote: current });
    if (canonical(current.reviews.filter((r) => ["publish", "languages"].includes(r.gate))) !== canonical(fresh.reviews.filter((r) => ["publish", "languages"].includes(r.gate)))) throw new VideoStop("Another publish/language review changed during staging; reread the source before submission");
    const existing = current.reviews.find((r) => r.gate === "languages" && r.content_sha256 === body.content_sha256);
    if (existing && ["approved", "pending"].includes(existing.status)) return { status: "already-submitted", review_id: existing.id, content_sha256: body.content_sha256 };
    if (existing) throw new VideoStop("This exact renewed language batch was rejected/superseded; inspect it before resubmitting");
    const receiptFile = path.join(entry.workdir, "language-package", "last-renewal-submission.json"), previous = readJson(receiptFile, null);
    if (previous?.status === "submitting" && previous.request?.content_sha256 === body.content_sha256) throw new VideoStop("Renewed language submission lost its answer; preserve its receipt and inspect site state before retrying");
    save(receiptFile, { status: "submitting", submitted_at: now(), request: body });
    const review = await api.submit(entry.slug, body);
    const confirmed = await api.reviews(entry.slug);
    assertProject(confirmed, entry, choices);
    if (!review?.id || review.gate !== "languages" || review.content_sha256 !== body.content_sha256 || !confirmed.reviews.some((v) => v.id === review.id && v.gate === "languages" && v.content_sha256 === body.content_sha256)) throw new VideoStop("Renewed language response was not confirmed; preserve the submission receipt without retrying");
    save(receiptFile, { status: "confirmed", submitted_at: now(), request: body, response: review });
    return { status: review.status, review_id: review.id, content_sha256: body.content_sha256 };
  }
  const refs = snapshot.files.map(({ path: omitted, ...file }) => file);
  const provenance = { final_sha256: entry.final_sha256, final_review_id: approved.id, final_decided_at: approved.decided_at, producer: "imported-long-languages", original_narration: "Windows Microsoft Hanhan Desktop; unchanged", target_dub_voice: "per prepared adapter" };
  const manifest = { schema_version: 1, provenance, locales_decided_at: fresh.locales_decided_at, locales: snapshot.locales, files: refs };
  const content_sha256 = digest(`${canonical(manifest)}\n`);
  const existing = fresh.reviews.find((review) => review.gate === "languages" && review.content_sha256 === content_sha256);
  if (existing && ["approved", "pending"].includes(existing.status)) return { status: "already-submitted", review_id: existing.id, content_sha256 };
  if (existing) throw new VideoStop("This exact language batch was rejected or superseded; inspect it before resubmitting");
  for (const file of snapshot.files) if (file.path) await api.upload(entry.slug, file);
  const latest = await api.reviews(entry.slug);
  assertProject(latest, entry, choices);
  if (canonical(latest.reviews.filter((review) => review.gate === "languages")) !== canonical(fresh.reviews.filter((review) => review.gate === "languages"))) throw new VideoStop("Another language review changed during upload; retry from the new snapshot");
  save(path.join(entry.workdir, "language-package", `${content_sha256}.json`), manifest);
  const body = { gate: "languages", content_sha256, summary: `匯入長片語言批次：${Object.keys(snapshot.locales).join("、")}；僅含已完成部件，配音上傳另由站主確認。`, payload: { locales: snapshot.locales, provenance }, files: refs };
  const review = await api.submit(entry.slug, body);
  save(path.join(entry.workdir, "language-package", "last-submission.json"), { submitted_at: now(), request: body, response: review });
  return { status: review.status, review_id: review.id, content_sha256 };
}

/** Sync subscription calls have no remote idempotency key. Persist before dispatch,
 * retain exact successful answers, and hold every unresolved attempt across restarts. */
export function journaledStageClient(api, manifest, entries, now, { settings = {}, choices = {}, readCurrent } = {}) {
  return { ...api, run: async (...args) => {
    const [stage, slug] = args, entry = entries.find((item) => item.slug === slug);
    if (!entry || !["translator", "caption_reviewer"].includes(stage)) throw new VideoStop("Stage is outside the isolated language scope");
    const checkStageStop = () => {
      if (manifest.source_kind !== "approved-final-body-range") return;
      if (!path.isAbsolute(manifest.work_base ?? "")) throw new VideoStop("Approved-final stage has no isolated batch STOP boundary");
      if (stopRequested(path.dirname(manifest.work_base)) || stopRequested(entry.workdir)) throw new HardStop("STOP requested before the approved-final language stage");
    };
    checkStageStop();
    const configuration = (value) => ({ durable_stage_runs: value.durable_stage_runs ?? null, stage_models: Object.fromEntries(["translator", "caption_reviewer"].map((name) => [name, value.stage_models?.[name] ?? null])), instructions: Object.fromEntries(["translator", "caption_reviewer"].map((name) => [name, value.stage_instructions?.[name] ?? null])) });
    const identity = { slug, final_sha256: entry.final_sha256, source_sha256: entry.renewal_source?.sha256 ?? null, namespace: manifest.request_namespace ?? null, choice: choices[slug] ?? entry.choice ?? null, configuration: configuration(settings) };
    if (manifest.source_kind === "approved-final-body-range") {
      if (typeof readCurrent !== "function") throw new VideoStop("Approved-final stage needs a fresh source, choice and settings reader");
      checkStageStop(); const current = await readCurrent(entry, stage); checkStageStop();
      if (!current || !current.settings || typeof current.settings !== "object" || Array.isArray(current.settings) || canonical(current.choice) !== canonical(identity.choice) || canonical(configuration(current.settings)) !== canonical(identity.configuration)) throw new VideoStop(`${slug}: current owner choice or stage configuration changed; preserve existing paid answers`);
    }
    // JSON roundtrip matches the actual wire body, including omitted optional properties.
    const request = JSON.parse(JSON.stringify({ stage, slug, instructions: args[2], payload: args[3], max_output_tokens: args[4], format: args[5], variant: args[6] ?? null }));
    const key = digest(canonical({ identity, request })), file = path.join(entry.workdir, "language-stage-journal.json");
    const logicalKey = (value) => value.variant ? null : digest(canonical(JSON.parse(JSON.stringify({ stage: value.stage, slug, locale: value.payload?.locale ?? null, parts: value.payload?.parts ?? null, worksheet: value.payload?.worksheet ? sheetSource(value.payload.worksheet) : null }))));
    const journal = readJson(file, { schema_version: 1, identity, entries: {} });
    if (journal.schema_version !== 1 || canonical(journal.identity) !== canonical(identity) || !journal.entries || typeof journal.entries !== "object" || Array.isArray(journal.entries)) throw new VideoStop(`${slug}: language stage journal source identity changed; preserve and inspect it`);
    for (const [id, record] of Object.entries(journal.entries)) {
      if (!record || id !== digest(canonical({ identity, request: record.request })) || !["dispatching", "unknown", "succeeded"].includes(record.status) || (record.status === "succeeded" && (!record.result || digest(canonical(record.result)) !== record.result_sha256))) throw new VideoStop(`${slug}: language stage journal is malformed; no new request was sent`);
    }
    const unresolved = Object.values(journal.entries).find((record) => record.status !== "succeeded");
    if (unresolved) throw new VideoStop(`${slug}: ${unresolved.request.stage} has an unknown paid result; preserve its stage journal and inspect the existing result before any retry`);
    if (journal.entries[key]) return structuredClone(journal.entries[key].result);
    if (logicalKey(request) && Object.values(journal.entries).some((record) => logicalKey(record.request) === logicalKey(request))) throw new VideoStop(`${slug}: exact stage request changed for a recorded language unit; preserve its answer and inspect before retrying`);
    const startedAt = now(); checkStageStop();
    const record = journal.entries[key] = { status: "dispatching", request, started_at: startedAt };
    savePaidStage(file, journal); // A crash from this point onward cannot authorize a second POST.
    let result;
    try { checkStageStop(); result = JSON.parse(JSON.stringify(await api.run(...args))); }
    catch (error) { record.status = "unknown"; record.error = clean(error.message); record.updated_at = now(); savePaidStage(file, journal); throw error; }
    record.status = "succeeded"; record.result = result; record.result_sha256 = digest(canonical(result)); record.updated_at = now(); savePaidStage(file, journal);
    return structuredClone(result);
  } };
}

export async function run(options, dependencies = {}) {
  const base = path.dirname(path.resolve(options.manifest));
  const manifest = resolveManifest(readJson(path.resolve(options.manifest)), base);
  const phase = options.phase ?? "all";
  if (!["translations", "dubs", "all"].includes(phase)) throw new VideoStop("phase must be translations, dubs, or all");
  const limit = Number(options.maxUnits ?? 12);
  if (!Number.isInteger(limit) || limit < 1 || limit > 100) throw new VideoStop("max-units must be 1..100");
  const requested = options.slugs ?? SLUGS;
  for (const slug of requested) assertAllowedSlug(slug);
  if (!Array.isArray(manifest.videos) || new Set(manifest.videos.map((entry) => entry.slug)).size !== manifest.videos.length) throw new VideoStop("Invalid or duplicate manifest videos");
  for (const entry of manifest.videos) assertAllowedSlug(entry.slug);
  const entries = requested.map((slug) => manifest.videos.find((entry) => entry.slug === slug));
  if (entries.some((entry) => !entry)) throw new VideoStop("A requested video is absent from the prepared manifest");
  const dry = options.dryRun !== false;
  const now = () => (dependencies.now?.() ?? new Date()).toISOString();
  const checkBatchStop = () => {
    if (manifest.source_kind === "approved-final-body-range" && stopRequested(base)) throw new HardStop("STOP requested in the approved-final batch");
  };
  const freshProbe = async (read) => { checkBatchStop(); const value = await read(); checkBatchStop(); return value; };
  let fatal = null;
  const rawFetch = dependencies.fetch ?? globalThis.fetch;
  const guardedFetch = async (...args) => {
    if (fatal) throw fatal;
    if (!dry && args[1]?.method === "POST") checkBatchStop();
    const response = await rawFetch(...args);
    if (!response.ok) {
      const error = await response.clone().json().catch(() => ({}));
      if ([401, 403, 429].includes(response.status) || /budget|quota|subscription_paused|token_invalid|provider_not_configured/.test(error.code ?? "")) {
        fatal = new HardStop(clean(error.detail ?? error.title ?? `HTTP ${response.status}`));
        throw fatal;
      }
    }
    return response;
  };
  const ctx = { root: manifest.root, env: { ...(dependencies.env ?? process.env), VIDEO_WORKDIR: manifest.work_base }, home: dependencies.home, EXIT, now: () => new Date(now()), fetch: guardedFetch, sleep: async (ms) => { if (fatal) throw fatal; await (dependencies.sleep ?? ((delay) => new Promise((resolve) => setTimeout(resolve, delay))))(Math.min(ms, 5000)); }, stdout: { write: () => {} }, stderr: { write: () => {} } };
  const api = dependencies.api ?? createSiteClient(ctx);
  const progressFile = path.join(base, "progress.json");
  const progress = readJson(progressFile, { schema_version: 1, videos: {} });
  const event = (value) => {
    if (dry) return;
    appendFileSync(path.join(base, "events.jsonl"), `${JSON.stringify({ at: now(), ...value })}\n`);
    progress.updated_at = now();
    save(progressFile, progress);
  };
  const projects = new Map();
  for (const entry of entries) {
    await verifyLocal(manifest, entry);
    const remote = await api.reviews(entry.slug);
    assertProject(remote, entry);
    if (remote.reviews.some((r) => r.gate === "final" && r.status === "approved" && r.payload?._final_renewal)) {
      if (!entry.renewal_source) throw new VideoStop(`${entry.slug}: owner-approved replacement has no source-bound language handoff`);
      await readManualLanguageSource({ workdir: entry.workdir, remote });
    }
    projects.set(entry.slug, remote);
  }
  if (dry) return { status: "dry-run", phase, max_units: limit, videos: entries.map((entry) => ({ slug: entry.slug, final_sha256: entry.final_sha256, locales: projects.get(entry.slug).locales })) };
  // One exclusive runner per isolated batch. An interrupted process leaves a lock requiring
  // explicit inspection/removal, rather than allowing duplicate paid jobs to overlap.
  const lock = path.join(base, "runner.lock");
  const { unlinkSync } = await import("node:fs");
  // Exact-lexicon sibling batches share one owner lock so only one producer can
  // consume the account's subscription budget at a time. A crash keeps this lock too.
  const ownerLock = manifest.source_kind === "approved-final-body-range" ? path.join(path.dirname(base), ".approved-final-language-runner.lock") : null;
  if (ownerLock) closeSync(openSync(ownerLock, "wx"));
  try { closeSync(openSync(lock, "wx")); }
  catch (error) { if (ownerLock) unlinkSync(ownerLock); throw error; }
  try {
    const settings = await api.settings();
    const noReport = { ...journaledStageClient(api, manifest, entries, now, { settings, choices: Object.fromEntries([...projects].map(([slug, project]) => [slug, project.locales])), readCurrent: async (entry) => {
      await freshProbe(() => verifyLocal(manifest, entry));
      const current = await freshProbe(() => api.reviews(entry.slug)); assertProject(current, entry, projects.get(entry.slug).locales);
      await freshProbe(() => readManualLanguageSource({ workdir: entry.workdir, remote: current }));
      const currentSettings = await freshProbe(() => api.settings());
      return { settings: currentSettings, choice: current.locales };
    } }), report: async (slug) => { assertAllowedSlug(slug); return projects.get(slug); } };
    const Auto = dependencies.AutomationClass ?? Automation;
    const automation = new Auto(ctx, noReport, settings);
    const runMain = dependencies.runMain ?? videoMain;
    let audioPassed = new Map();
    ctx.runCommand = async (args) => {
      const slug = args[args.indexOf("--slug") + 1];
      assertAllowedSlug(slug);
      if (!requested.includes(slug) || !COMMANDS.has(args[0]) || args.includes("--file") || args.includes("--workdir") || (args[0] === "review-pull" && args[args.indexOf("--gate") + 1] !== "final")) throw new VideoStop("Command is outside the language-only scope");
      if (fatal) throw fatal;
      checkBatchStop();
      let out = "";
      const sink = { write: (text) => { out += text; } };
      const entry = entries.find((item) => item.slug === slug);
      if (entry.renewal_source) {
        await verifyLocal(manifest, entry);
        const remote = await api.reviews(slug); assertProject(remote, entry);
        await readManualLanguageSource({ workdir: entry.workdir, remote });
      }
      checkBatchStop();
      const beforeRuns = readJson(path.join(entry.workdir, "state.json"), { runs: [] }).runs.length;
      let commandFetch = ctx.fetch;
      if (manifest.source_kind === "approved-final-body-range") {
        const credentials = readCredentials({ env: ctx.env, home: ctx.home });
        commandFetch = createSpeechJournalFetch({ fetchImpl: ctx.fetch, site: credentials.site, workdir: entry.workdir, now, readIdentity: async () => {
          await freshProbe(() => verifyLocal(manifest, entry));
          const current = await freshProbe(() => api.reviews(slug)); assertProject(current, entry, projects.get(slug).locales);
          const contract = await freshProbe(() => readManualLanguageSource({ workdir: entry.workdir, remote: current }));
          const currentSettings = await freshProbe(() => api.settings());
          const status = await freshProbe(() => speechStatus({ site: credentials.site, token: credentials.token, fetchImpl: ctx.fetch, sleep: ctx.sleep }));
          checkBatchStop();
          return { source_kind: contract.source.kind, slug, final_sha256: entry.final_sha256, source_sha256: entry.renewal_source.sha256, raw_source: { script_sha256: contract.evidence.evidence_script.sha256, timeline_sha256: contract.evidence.evidence_body_timeline.sha256, lexicon_sha256: contract.adapter.raw_lexicon?.sha256 ?? contract.adapter.lexicon_sha256 }, request_namespace: manifest.request_namespace, choice: contract.choice, configuration: speechConfiguration(currentSettings, status) };
        } });
      }
      const code = await runMain(args, { ...ctx, fetch: commandFetch, stdout: sink, stderr: sink });
      if (fatal) throw fatal;
      out = clean(out);
      if (code === EXIT.owner || /quota|budget.exhaust|subscription.paused|token.invalid/i.test(out)) throw new HardStop(out || "The language tool needs owner credentials or budget");
      if (args[0] === "check-audio" && code === 0) {
        const locale = args[args.indexOf("--locale") + 1];
        audioPassed.set(`${slug}/${locale}`, await checkedDubReceipt(entry, locale, beforeRuns));
      }
      event({ slug, type: "command", command: args[0], code, detail: out.slice(-4000) });
      return { code, out };
    };
    const paused = new Set();
    let units = 0;
    for (const entry of entries) {
      const remote = projects.get(entry.slug);
      const previous = progress.videos[entry.slug];
      if (previous && previous.final_sha256 !== entry.final_sha256) throw new VideoStop("Progress belongs to a different final cut");
      progress.videos[entry.slug] ??= { final_sha256: entry.final_sha256, translations: {}, checked_dubs: {}, skipped_dubs: {} };
      const result = await ctx.runCommand(["review-pull", "--slug", entry.slug, "--gate", "final"]);
      if (result.code !== 0 || (await approvalState({ gate: "final", docDir: path.dirname(entry.doc_file), workdir: entry.workdir })).status !== "approved") throw new VideoStop(`${entry.slug}: exact final approval was not pulled`);
      writeLanguages(entry.workdir, { locales: remote.locales, decided_at: remote.locales_decided_at, synced_at: now() });
    }
    while (units < limit) {
      let moved = false;
      for (const entry of entries) {
        if (units >= limit) break;
        if (paused.has(entry.slug)) continue;
        if (stopRequested(entry.workdir)) throw new HardStop("STOP requested in the isolated batch");
        const record = progress.videos[entry.slug];
        try {
          let remote = currentLanguageProject(await api.reviews(entry.slug), entry);
          const choices = projects.get(entry.slug).locales ?? {};
          assertProject(remote, entry, choices);
          let project = await verifyLocal(manifest, entry);
          const state = readJson(path.join(entry.workdir, "auto.json"), { slug: entry.slug, title: remote.title, format: "slides", status: "imported_languages", created_at: now(), notes: [], failures: {} });
          if (state.status === "blocked") throw new VideoStop(`Language stage is blocked: ${state.blocked}`);
          let action = null;
          for (const locale of LOCALES) {
            const choice = choices[locale];
            if (!choice) continue;
            const needed = ["metadata", "captions"].filter((part) => choice[part] && (!remote.languages?.[locale]?.[part] || remote.languages[locale][part].state === "working"));
            const translation = path.join(project.dir, "i18n", `${locale}.json`);
            if (phase !== "dubs" && needed.length && !(existsSync(translation) && record.translations[locale] === await sha256File(translation))) { action = { kind: "translate", locale, parts: needed }; break; }
          }
          if (!action && phase !== "translations") {
            for (const locale of LOCALES) {
              if (!choices[locale]?.dub || ["ready", "skipped", "uploaded"].includes(remote.languages?.[locale]?.dub?.state)) continue;
              const translation = path.join(project.dir, "i18n", `${locale}.json`);
              if (!existsSync(translation) || record.translations[locale] !== await sha256File(translation)) continue;
              const additions = await localAdditions(entry, project, record, choices);
              if (!additions.locales[locale]?.dub) { action = { kind: "dub", locale }; break; }
            }
          }
          automation.halted = false;
          // A unit the automation sets aside for later (defer(): a held speech result, a busy
          // service) is a stop for this round too, with its own reason, not a missing track.
          automation.skipped?.delete(entry.slug);
          audioPassed = new Map();
          if (action) {
            units++;
            moved = true;
            record.status = "running";
            record.active_unit = { phase, kind: action.kind, locale: action.locale, started_at: now() };
            event({ slug: entry.slug, type: "unit-start", ...record.active_unit });
            const line = action.kind === "translate" ? await translateLocaleResuming(automation, ctx, entry, state, action.locale, action.parts, project, event) : await automation.makeDub(state, action.locale);
            event({ slug: entry.slug, type: action.kind, locale: action.locale, detail: clean(line ?? "already current") });
            if (automation.halted || state.status === "blocked" || automation.skipped?.has(entry.slug)) throw new VideoStop(clean(line ?? "Stage stopped; resume in a later invocation"));
            const translation = path.join(project.dir, "i18n", `${action.locale}.json`);
            if (action.kind === "translate" || existsSync(translation)) record.translations[action.locale] = await sha256File(translation);
            project = loadProject({ slug: entry.slug, root: manifest.root });
            if (action.kind === "dub") {
              const { dubs, skipped } = dubsForUpload(project, entry.workdir, speechHash(project.doc, project.lexicon), [action.locale]);
              if (audioPassed.has(`${entry.slug}/${action.locale}`) && dubs[0]) record.checked_dubs[action.locale] = audioPassed.get(`${entry.slug}/${action.locale}`);
              else if (skipped[action.locale] !== undefined) record.skipped_dubs[action.locale] = skipped[action.locale];
              else throw new VideoStop("Dub did not produce a checked track or an explicit skip reason");
            }
          }
          // The general caption command follows any current dub, even one whose audio check
          // failed. Only checked, non-skipped tracks may set the caption timing in this lane.
          const checked = await localAdditions(entry, project, record, choices);
          const captionChoices = Object.fromEntries(Object.entries(choices).map(([locale, choice]) => [locale, { ...choice, dub: partStatus(checked.locales[locale]?.dub) === "ready" }]));
          writeLanguages(entry.workdir, { locales: captionChoices, decided_at: remote.locales_decided_at });
          let captions;
          try { captions = await ctx.runCommand(["captions", "--slug", entry.slug]); }
          finally { writeLanguages(entry.workdir, { locales: choices, decided_at: remote.locales_decided_at }); }
          if (captions.code !== 0) throw new VideoStop(captions.out || "Caption validation failed");
          await verifyLocal(manifest, entry);
          const additions = await localAdditions(entry, project, record, choices);
          const sent = await submitSnapshot(api, remote, entry, additions, choices, now);
          record.last_submission = sent;
          record.problems = additions.problems;
          delete record.active_unit;
          if (!action) {
            const current = currentLanguageProject(await api.reviews(entry.slug), entry);
            assertProject(current, entry, choices);
            const missing = missingPhaseParts(current, phase);
            if (missing.length) throw new VideoStop(`Phase still missing ${missing.join(", ")}${additions.problems.length ? `: ${additions.problems.join("; ")}` : ""}`);
          }
          record.status = action ? "progress" : "phase-complete";
          event({ slug: entry.slug, type: "submission", ...sent });
          if (!action) paused.add(entry.slug);
        } catch (error) {
          record.status = error instanceof HardStop ? "hard-stop" : "paused";
          record.error = clean(error.message);
          event({ slug: entry.slug, type: "error", detail: record.error });
          if (error instanceof HardStop || fatal) throw fatal ?? error;
          paused.add(entry.slug);
        }
      }
      if (!moved) break;
    }
    const failed = entries.filter((entry) => ["paused", "hard-stop"].includes(progress.videos[entry.slug]?.status));
    progress.status = failed.length ? "paused" : paused.size === entries.length ? "phase-complete" : "unit-limit";
    event({ type: "round-ended", units, phase });
    return { status: progress.status, units, videos: progress.videos };
  } catch (error) {
    progress.status = error instanceof HardStop ? "hard-stop" : "failed";
    event({ type: "run-stopped", detail: clean(error.message) });
    throw error;
  } finally { try { unlinkSync(lock); } finally { if (ownerLock) unlinkSync(ownerLock); } }
}

export async function main(args = process.argv.slice(2)) {
  const { values } = parseArgs({ args, strict: true, options: { manifest: { type: "string" }, slug: { type: "string" }, phase: { type: "string", default: "all" }, "max-units": { type: "string", default: "12" }, "dry-run": { type: "boolean" }, apply: { type: "boolean" } } });
  if (!values.manifest || (values.apply && values["dry-run"])) throw new VideoStop("Use --manifest <prepared manifest> with --dry-run or --apply");
  const result = await run({ manifest: values.manifest, slugs: values.slug?.split(","), phase: values.phase, maxUnits: Number(values["max-units"]), dryRun: !values.apply });
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.status === "paused") process.exitCode = 1;
}
if (process.argv[1] && import.meta.url === pathToFileURL(path.resolve(process.argv[1])).href) main().catch((error) => { process.stderr.write(`${clean(error.message)}\n`); process.exitCode = 1; });
