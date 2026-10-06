// Local protection for the approved-final batch only. The normal speech client and
// server budgets stay authoritative; this adapter never generates or approves audio.
import { createHash, randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, lstatSync, mkdirSync, openSync, readFileSync, readdirSync, unlinkSync, writeFileSync } from "node:fs";
import path from "node:path";
import { atomicWrite, stopRequested } from "../../../tools/video/core/paths.mjs";
import { parseWav } from "../../../tools/video/tts/wav.mjs";

const HASH = /^[a-f0-9]{64}$/;
const UUID = /^[a-f0-9]{8}(?:-[a-f0-9]{4}){3}-[a-f0-9]{12}$/i;
const SLUGS = new Set(["01-image-trust", "02-confident-errors", "03-machine-internet", "04-tasks-and-jobs", "05-uneven-abilities", "06-digital-yesman"].map((v) => `ai-real-world-${v}`));
const ROUTES = new Set(["/api/video/speech", "/api/video/speech/transcribe", "/api/video/speech/judge"]);
const MAX_RESPONSE_BYTES = 64 * 1024 * 1024;
const sha = (bytes) => createHash("sha256").update(bytes).digest("hex");
const canonical = (v) => Array.isArray(v) ? `[${v.map(canonical).join(",")}]` : v && typeof v === "object" ? `{${Object.keys(v).sort().map((k) => `${JSON.stringify(k)}:${canonical(v[k])}`).join(",")}}` : JSON.stringify(v);
const jsonCopy = (v) => JSON.parse(JSON.stringify(v));
const requireThat = (ok, detail) => { if (!ok) throw new Error(detail); };
const secretKey = /^(?:authorization|cookie|set-cookie|token|access_token|refresh_token|api_?key|secret|credentials?)$/i;
function tokenless(v) {
  if (typeof v === "string") requireThat(!/mkv_[A-Za-z0-9_-]{36,76}|Bearer\s+\S+/i.test(v), "secret material cannot enter a speech receipt");
  else if (Array.isArray(v)) v.forEach(tokenless);
  else if (v && typeof v === "object") for (const [key, value] of Object.entries(v)) { requireThat(!secretKey.test(key), "secret fields cannot enter a speech receipt"); tokenless(value); }
}
const pick = (v, names) => Object.fromEntries(names.map((name) => [name, v?.[name] ?? null]));

/** Stable, public configuration only: live usage counters and credentials are excluded. */
export function speechConfiguration(settings = {}, status = {}) {
  const configuration = {
    ...pick(settings, ["voice", "voice_options", "stage_models", "stage_instructions", "configured_providers", "durable_stage_runs", "monthly_token_budget_millions", "max_retake_rounds", "auto_approve_audio"]),
    speech: pick(status, ["configured", "region", "voices", "output_format", "max_request_characters", "monthly_limit", "gemini_configured", "gemini_models", "gemini_voices", "gemini_monthly_limit"]),
  };
  tokenless(configuration); return jsonCopy(configuration);
}

function checkedIdentity(value) {
  const v = jsonCopy(value); tokenless(v);
  requireThat(v.source_kind === "approved-final-body-range" && SLUGS.has(v.slug) && HASH.test(v.final_sha256 ?? "") && HASH.test(v.source_sha256 ?? "") && UUID.test(v.request_namespace ?? ""), "speech identity is not an approved-final batch source");
  requireThat(v.raw_source && ["script_sha256", "timeline_sha256", "lexicon_sha256"].every((k) => HASH.test(v.raw_source[k] ?? "")), "speech identity lacks exact raw source hashes");
  requireThat(v.choice && typeof v.choice === "object" && !Array.isArray(v.choice) && v.configuration && typeof v.configuration === "object" && !Array.isArray(v.configuration), "speech identity lacks owner choice or public configuration");
  return v;
}

function regular(file) { const stat = lstatSync(file); requireThat(stat.isFile() && !stat.isSymbolicLink(), "speech receipt is not a regular file"); return stat; }
function directory(file) { const stat = lstatSync(file); requireThat(stat.isDirectory() && !stat.isSymbolicLink(), "speech receipt directory cannot be a link"); }
function durableWrite(file, bytes) {
  atomicWrite(file, bytes);
  const fd = openSync(file, "r+"); try { fsyncSync(fd); } finally { closeSync(fd); }
  // Windows cannot open a directory for fsync. POSIX also commits the rename.
  if (process.platform !== "win32") { const dir = openSync(path.dirname(file), "r"); try { fsyncSync(dir); } finally { closeSync(dir); } }
}
function held() { return Response.json({ code: "video_speech_result_held", detail: "Speech request or saved result is held. Preserve its local receipt and inspect the existing result; no paid POST was retried." }, { status: 409 }); }
// The speech routes' own 502 `upstream_unavailable` (apps/web/app/api/video/speech/forward.ts) is an
// API they never reached; since #1272 a request the API took and lost answers 504
// `video_speech_answer_lost` (a host from before #1272 does not; production serves it since
// c12e159d0). Only this exact status and JSON code, as NEVER_REACHED in
// tools/video/tts/client.mjs: an HTML gateway 502, a 503 or any other code stays uncertain.
async function neverReached(response) {
  if (response.status !== 502) return false;
  try { return (await response.clone().json())?.code === "upstream_unavailable"; } catch { return false; }
}

function checkedRequest(route, body) {
  requireThat(ROUTES.has(route) && typeof body === "string", "paid speech requires its exact JSON wire body");
  const value = JSON.parse(body); tokenless(value);
  const keys = route.endsWith("/transcribe") ? ["audio", "terms", "language"] : route.endsWith("/judge") ? ["lines", "language"] : ["voice", "rate", "style", "model", "segments"];
  requireThat(value && typeof value === "object" && !Array.isArray(value) && Object.keys(value).every((k) => keys.includes(k)), "speech request contains fields outside its official route");
  if (route.endsWith("/transcribe")) requireThat(typeof value.audio === "string" && value.audio.length > 0, "transcription has no exact audio");
  else if (route.endsWith("/judge")) requireThat(Array.isArray(value.lines) && value.lines.length > 0, "judge has no lines");
  else requireThat(typeof value.voice === "string" && Array.isArray(value.segments) && value.segments.length > 0, "synthesis has no voice or segments");
  return { path: route, body_utf8: body, body_sha256: sha(Buffer.from(body)) };
}
function checkedHeaders(response, bytes) {
  const contentType = response.headers.get("content-type"), billable = response.headers.get("x-billable-characters"), length = response.headers.get("content-length");
  requireThat(length === null || /^\d+$/.test(length) && Number(length) === bytes.length, "speech response body is incomplete");
  requireThat(billable === null || /^\d+$/.test(billable) && Number.isSafeInteger(Number(billable)), "invalid billable speech header");
  const headers = {};
  if (contentType) { requireThat(/^(?:audio\/wav|application\/json)(?:\s*;\s*charset=utf-8)?$/i.test(contentType), "unexpected speech response content type"); headers["content-type"] = contentType; }
  if (billable !== null) headers["x-billable-characters"] = billable;
  if (response.headers.get("cache-control") === "no-store") headers["cache-control"] = "no-store";
  return headers;
}
function completePcmWav(bytes) {
  requireThat(bytes.length >= 44 && bytes.toString("ascii", 0, 4) === "RIFF" && bytes.toString("ascii", 8, 12) === "WAVE" && bytes.readUInt32LE(4) + 8 === bytes.length, "WAV has no exact complete RIFF length");
  let offset = 12, format = null, data = false;
  while (offset < bytes.length) {
    requireThat(offset + 8 <= bytes.length, "WAV has a partial chunk header");
    const id = bytes.toString("ascii", offset, offset + 4), declared = bytes.readUInt32LE(offset + 4), start = offset + 8;
    // The existing Azure/native streamed data convention uses a final data chunk.
    // A complete, exact outer RIFF size is still required; no oversized chunk is clamped.
    const streamed = id === "data" && (declared === 0 || declared === 0xffffffff), size = streamed ? bytes.length - start : declared;
    const end = start + size, next = end + (size % 2);
    requireThat(end <= bytes.length && next <= bytes.length, "WAV chunk exceeds its complete response");
    if (id === "fmt ") {
      requireThat(!format && !data && size >= 16, "WAV format chunk is missing, short or duplicated");
      const kind = bytes.readUInt16LE(start), channels = bytes.readUInt16LE(start + 2), rate = bytes.readUInt32LE(start + 4), byteRate = bytes.readUInt32LE(start + 8), align = bytes.readUInt16LE(start + 12), bits = bytes.readUInt16LE(start + 14);
      requireThat(channels === 1 && bits === 16 && align === 2 && rate >= 8000 && 48000 % rate === 0 && byteRate === rate * align, "WAV PCM frame format is inconsistent");
      if (kind === 1) requireThat(size === 16 || size === 18 && bytes.readUInt16LE(start + 16) === 0, "WAV PCM format extension is inconsistent");
      else requireThat(kind === 0xfffe && size === 40 && bytes.readUInt16LE(start + 16) === 22 && bytes.readUInt16LE(start + 18) === 16 && bytes.subarray(start + 24, start + 40).toString("hex") === "0100000000001000800000aa00389b71", "WAV extensible format is not complete 16-bit PCM");
      format = { align };
    } else if (id === "data") {
      requireThat(format && !data && size > 0 && size % format.align === 0 && (!streamed || next === bytes.length), "WAV data has incomplete PCM frames or multiple chunks");
      data = true;
    }
    offset = next;
  }
  requireThat(format && data && offset === bytes.length, "WAV is missing complete format/audio chunks");
}
function checkedAnswer(request, bytes) {
  requireThat(bytes.length > 0 && bytes.length <= MAX_RESPONSE_BYTES, "speech response size is invalid");
  if (request.path === "/api/video/speech") {
    completePcmWav(bytes);
    const wav = parseWav(bytes); requireThat(wav.samples.length > 0, "speech response has no actual PCM samples");
  } else {
    const answer = JSON.parse(bytes.toString("utf8")); tokenless(answer);
    if (request.path.endsWith("/transcribe")) requireThat(typeof answer.text === "string", "transcriber returned no actual text");
    else {
      const ids = JSON.parse(request.body_utf8).lines.map((v) => v.id);
      requireThat(new Set(ids).size === ids.length && Array.isArray(answer.results) && answer.results.length === ids.length && new Set(answer.results.map((v) => v.id)).size === ids.length && answer.results.every((v) => ids.includes(v.id) && typeof v.noul === "number" && Number.isFinite(v.noul) && v.noul >= 0 && v.noul <= 1), "judge returned incomplete or invalid actual results");
    }
  }
}
function responseBytes(dir, key, record) {
  const result = record.response;
  requireThat(result?.file === `responses/${key}.bin` && Number.isSafeInteger(result.bytes) && result.bytes > 0 && result.bytes <= MAX_RESPONSE_BYTES && HASH.test(result.sha256 ?? "") && result.status === 200 && result.headers && Object.keys(result.headers).every((k) => ["content-type", "x-billable-characters", "cache-control"].includes(k)), "saved speech response receipt is invalid");
  const { receipt_sha256, ...proof } = result;
  requireThat(receipt_sha256 === sha(canonical({ key, response: proof })), "saved speech response status or billable headers changed");
  const file = path.join(dir, result.file); regular(file); const bytes = readFileSync(file);
  requireThat(bytes.length === result.bytes && sha(bytes) === result.sha256, "saved speech response bytes changed");
  checkedHeaders(new Response(bytes, { status: result.status, headers: result.headers }), bytes); checkedAnswer(record.request, bytes);
  return bytes;
}

/** readIdentity rechecks current source/choice/settings before each paid boundary.
 * Local 409 holds stop the native client's internal retry loop without changing it; only the
 * route's never-reached 502 leaves no entry, so that loop's next attempt is journaled afresh.
 * The enclosing runner owns its batch/account lock; this lock also closes per-call races. */
export function createSpeechJournalFetch({ fetchImpl, site, workdir, readIdentity, now = () => new Date().toISOString(), write = durableWrite }) {
  const origin = new URL(site);
  requireThat(["https:", "http:"].includes(origin.protocol) && !origin.username && !origin.password && origin.pathname === "/" && !origin.search && !origin.hash && typeof fetchImpl === "function" && typeof readIdentity === "function", "speech journal requires exact site, fetch and fresh identity reader");
  const dir = path.join(workdir, "speech-journal"), file = path.join(dir, "journal.json");
  return async (input, init = {}) => {
    const url = new URL(typeof input === "string" || input instanceof URL ? input : input.url), method = String(init.method ?? input?.method ?? "GET").toUpperCase();
    if (method !== "POST" || !/^\/api(?:\/v1)?\/video\/speech(?:\/(?:transcribe|judge))?\/?$/.test(url.pathname)) return fetchImpl(input, init);
    let ownedLock = null, journal = null, record = null;
    try {
      requireThat(url.origin === origin.origin && ROUTES.has(url.pathname) && !url.search && !url.hash && !url.username && !url.password && !(input instanceof Request), "paid speech route differs from the exact site or native wire request");
      requireThat(new Headers(init.headers).get("content-type") === "application/json", "paid speech requires the native JSON content type");
      directory(workdir);
      const identity = checkedIdentity(await readIdentity());
      requireThat(!stopRequested(workdir), "STOP requested during the fresh speech identity probe");
      const request = checkedRequest(url.pathname, init.body), key = sha(canonical({ identity, request }));
      const fresh = !existsSync(dir); if (fresh) mkdirSync(dir); directory(dir);
      const lock = path.join(dir, "active.lock"), owner = randomUUID(), fd = openSync(lock, "wx");
      try { writeFileSync(fd, owner); fsyncSync(fd); ownedLock = { file: lock, owner, stat: lstatSync(lock, { bigint: true }) }; } finally { closeSync(fd); }
      if (!fresh) {
        regular(file); journal = JSON.parse(readFileSync(file, "utf8"));
        requireThat(journal.schema_version === 1 && canonical(journal.identity) === canonical(identity) && journal.entries && typeof journal.entries === "object" && !Array.isArray(journal.entries), "speech source, owner choice or configuration changed");
      } else journal = { schema_version: 1, identity, entries: {} };
      for (const [id, entry] of Object.entries(journal.entries)) {
        requireThat(HASH.test(id) && entry && checkedRequest(entry.request?.path, entry.request?.body_utf8).body_sha256 === entry.request.body_sha256 && id === sha(canonical({ identity, request: entry.request })) && ["pending", "unknown", "succeeded"].includes(entry.status), "speech journal is corrupt");
        if (entry.status === "succeeded") responseBytes(dir, id, entry);
      }
      const responseDir = path.join(dir, "responses");
      if (existsSync(responseDir)) { directory(responseDir); requireThat(readdirSync(responseDir).every((name) => HASH.test(name.replace(/\.bin$/, "")) && name === `${name.slice(0, 64)}.bin` && journal.entries[name.slice(0, 64)]), "orphan speech response requires inspection"); }
      requireThat(Object.values(journal.entries).every((v) => v.status === "succeeded"), "this video has an unresolved paid speech result");
      requireThat(!stopRequested(workdir), "STOP requested before the speech intent");
      if (journal.entries[key]) { const saved = journal.entries[key]; return new Response(responseBytes(dir, key, saved), { status: saved.response.status, headers: saved.response.headers }); }
      record = journal.entries[key] = { status: "pending", request, started_at: now() };
      write(file, `${JSON.stringify(journal, null, 2)}\n`);
      // Keep the native request's auth only in memory. It is never part of a receipt.
      requireThat(!stopRequested(workdir), "STOP requested before the paid speech POST");
      const response = await fetchImpl(input, { ...init, redirect: "error" });
      if (!response.ok) {
        if (await neverReached(response)) {
          // Nothing ran or was charged, so drop the intent and let the native client's bounded
          // retry pass every check above again. Save the journal without it before forgetting it:
          // if that write fails, the catch below still marks this entry unknown and holds.
          const next = { ...journal, entries: { ...journal.entries } }; delete next.entries[key];
          write(file, `${JSON.stringify(next, null, 2)}\n`);
          delete journal.entries[key]; record = null;
          return response;
        }
        // Preserve the server's owner/quota classification for this first response.
        // Any other failure, retryable or not, has no local authority to submit another POST.
        record.status = "unknown"; record.http_status = response.status; record.updated_at = now(); write(file, `${JSON.stringify(journal, null, 2)}\n`);
        return response;
      }
      requireThat(response.status === 200, "paid speech returned an unexpected success status");
      const bytes = Buffer.from(await response.arrayBuffer()), headers = checkedHeaders(response, bytes);
      if (request.path !== "/api/video/speech") tokenless(JSON.parse(bytes.toString("utf8")));
      requireThat(bytes.length > 0 && bytes.length <= MAX_RESPONSE_BYTES, "speech response size is invalid");
      if (!existsSync(responseDir)) mkdirSync(responseDir); directory(responseDir);
      const responseFile = path.join(responseDir, `${key}.bin`); requireThat(!existsSync(responseFile), "speech response cannot overwrite retained bytes");
      write(responseFile, bytes);
      record.response = { file: `responses/${key}.bin`, sha256: sha(bytes), bytes: bytes.length, status: response.status, headers };
      record.response.receipt_sha256 = sha(canonical({ key, response: record.response }));
      checkedAnswer(request, bytes);
      record.status = "succeeded"; record.updated_at = now(); write(file, `${JSON.stringify(journal, null, 2)}\n`);
      return new Response(bytes, { status: response.status, headers });
    } catch {
      if (record && journal) { record.status = "unknown"; record.updated_at = now(); try { write(file, `${JSON.stringify(journal, null, 2)}\n`); } catch { /* The earlier pending receipt remains a hold. */ } }
      return held();
    } finally {
      if (ownedLock) {
        try { const stat = lstatSync(ownedLock.file, { bigint: true }); if (stat.dev === ownedLock.stat.dev && stat.ino === ownedLock.stat.ino && readFileSync(ownedLock.file, "utf8") === ownedLock.owner) unlinkSync(ownedLock.file); } catch { /* An external/replaced lock remains held. */ }
      }
    }
  };
}
