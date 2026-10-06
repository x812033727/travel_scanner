// Stage requests and answers live outside Git until the worker has saved the unit's artifacts.
// The request key is durable before the first HTTP request; losing an answer never buys a new run.
import { createHash, randomUUID } from "node:crypto";
import { closeSync, existsSync, fsyncSync, mkdirSync, openSync, readFileSync, readdirSync, renameSync, unlinkSync, writeFileSync } from "node:fs";
import path from "node:path";

import { resolveWorkdir } from "../core/paths.mjs";

export const RUN_RECEIPTS_DIR = "run-receipts";
export const POLICY_HOLD_CODE = "video_ai_drama_disabled";
export const policyHeld = (record) => record.receipt?.status === "failed" && record.receipt.error_code === POLICY_HOLD_CODE
  || record.policy_rejection?.error_code === POLICY_HOLD_CODE;
const HASH = /^[a-f0-9]{64}$/;
const UUID = /^[a-f0-9]{8}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{4}-[a-f0-9]{12}$/i;
const STATUSES = new Set(["queued", "running", "succeeded", "failed", "uncertain"]);

export class RunReceiptError extends Error {}
export const INPUT_CHANGED_CODE = "video_ai_receipt_input_changed";
export const INPUT_CHANGED_MESSAGE = "stage inputs changed while a saved run is unfinished; restore its exact inputs or inspect the receipt before an owner retry";
const inputChanged = () => Object.assign(new RunReceiptError(INPUT_CHANGED_MESSAGE), { code: INPUT_CHANGED_CODE });
// What archive() writes for a stale journal it may close on its own: the run is over (or never
// reached the server), so no owner retry is needed and no request id is consumed.
export const AUTO_ARCHIVE_REASON = "inputs changed; the saved run is terminal";
// The same when the server answered the job lookup with a settled 4xx (`gone`): no job under
// this token (404 after a re-pair), not the receipt's job (409 input hash), a malformed identity.
export const jobGoneReason = (gone) => `the server no longer has this job (${gone.status}${gone.code ? ` ${gone.code}` : ""})`;
// The kind of block (flow.mjs `blocked_kind`, `job_gone:<stage>`) of a video whose running
// journal met that answer outside a retry: the owner's retry of it is what may archive the journal.
export const JOB_GONE_KIND = "job_gone:";
const validGone = (gone) => object(gone) && Number.isInteger(gone.status) && gone.status >= 400 && gone.status < 500 && typeof gone.code === "string";
const requireThat = (condition, message) => { if (!condition) throw new RunReceiptError(message); };
const object = (value) => value !== null && typeof value === "object" && !Array.isArray(value);

/** JSON on the wire, with object keys sorted recursively. Reject lossy non-JSON values. */
export function canonicalJson(value) {
  if (value === null || typeof value === "string" || typeof value === "boolean") return JSON.stringify(value);
  if (typeof value === "number") {
    requireThat(Number.isFinite(value), "stage inputs must contain finite JSON numbers");
    return JSON.stringify(value);
  }
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  requireThat(object(value), "stage inputs must contain only JSON values");
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`).join(",")}}`;
}

export const sourceHash = (request) => createHash("sha256").update(canonicalJson(request), "utf8").digest("hex");
// The request already running keeps its frozen date and pronunciation context. Another lane
// adding a lexicon term, or midnight passing, must not buy a second copy of that same unit.
function unitSource(request) {
  const payload = { ...request.payload };
  delete payload.today;
  delete payload.lexicon;
  return canonicalJson({ ...request, payload });
}

export function normalizeRun(request) {
  requireThat(object(request) && /^[a-z0-9][a-z0-9-]{0,79}$/.test(request.slug ?? ""), "invalid stage slug for its durable journal");
  requireThat(typeof request.stage === "string" && typeof request.instructions === "string" && object(request.payload), "invalid stage request");
  const normalized = { stage: request.stage, slug: request.slug, instructions: request.instructions, payload: request.payload,
    max_output_tokens: request.max_output_tokens ?? 16_000, format: request.format ?? "slides", variant: request.variant ?? null };
  // Preserve JSON's ordinary omission of optional undefined properties, then snapshot the
  // actual wire values. A caller's later mutation cannot change the request already sent.
  const wire = JSON.stringify(normalized, (_key, value) => {
    if (typeof value === "number") requireThat(Number.isFinite(value), "stage inputs must contain finite JSON numbers");
    return value;
  });
  return JSON.parse(canonicalJson(JSON.parse(wire)));
}

/** Keep the first receipt's server identities unchanged, including its selected provider/model. */
export function validateRunReceipt(receipt, record) {
  requireThat(object(receipt) && UUID.test(receipt.id ?? "") && receipt.request_key === record.request_key
    && HASH.test(receipt.request_hash ?? "") && HASH.test(receipt.input_hash ?? "")
    && typeof receipt.provider === "string" && receipt.provider.length > 0 && typeof receipt.model === "string" && receipt.model.length > 0
    && STATUSES.has(receipt.status), "stage receipt has missing or mismatched identities");
  const earlier = record.receipt;
  if (earlier) for (const key of ["id", "request_key", "request_hash", "input_hash", "provider", "model"]) {
    requireThat(receipt[key] === earlier[key], `stage receipt changed its ${key}`);
  }
  requireThat(receipt.status === "succeeded" ? object(receipt.result) && typeof receipt.result.text === "string"
    && receipt.result.provider === receipt.provider && typeof receipt.result.model === "string" && receipt.result.model.length > 0
    && Number.isSafeInteger(receipt.result.input_tokens) && Number.isSafeInteger(receipt.result.output_tokens) && object(receipt.result.usage)
    : receipt.result === null, "stage receipt has an invalid result");
  requireThat(!earlier || !["succeeded", "failed", "uncertain"].includes(earlier.status)
    || earlier.status === "uncertain" && receipt.status === "succeeded"
    || receipt.status === earlier.status && canonicalJson(receipt) === canonicalJson(earlier), "a settled stage receipt changed");
  return structuredClone(receipt);
}

// Windows can briefly refuse to replace or move a journal that another process holds open (the
// cause seen once in a local run is unknown). Retry only that rename, on Windows only, with the
// schedule of core/paths.mjs atomicWrite: at most 630 ms of waiting before the original error.
const RENAME_RETRY_MS = [10, 20, 40, 80, 160, 320];
const TRANSIENT_RENAME_CODES = new Set(["EPERM", "EACCES", "EBUSY"]);
const renameWaitCell = new Int32Array(new SharedArrayBuffer(4));
const RENAME_IO = { platform: process.platform, rename: renameSync, wait: (ms) => Atomics.wait(renameWaitCell, 0, 0, ms) };

function renameJournal(from, to, io) {
  for (let attempt = 0; ; attempt++) {
    try { return io.rename(from, to); }
    catch (error) {
      if (io.platform !== "win32" || !TRANSIENT_RENAME_CODES.has(error?.code) || attempt >= RENAME_RETRY_MS.length) throw error;
      io.wait(RENAME_RETRY_MS[attempt]);
    }
  }
}

function save(file, value, io) {
  const temporary = `${file}.${randomUUID()}.tmp`;
  const fd = openSync(temporary, "wx", 0o600);
  try {
    try { writeFileSync(fd, `${JSON.stringify(value, null, 2)}\n`); fsyncSync(fd); }
    finally { closeSync(fd); }
    renameJournal(temporary, file, io);
  } catch (error) {
    // The journal was never replaced. Remove only this save's own temporary bytes.
    try { unlinkSync(temporary); } catch { /* the original error is the one to report */ }
    throw error;
  }
}

/** One source hash per slug; malformed or changed journal bytes fail closed. Tests may pass
 * `ctx.receiptIo` ({ platform, rename, wait }) to simulate a refused rename. */
export function runReceiptStore(ctx, site) {
  const consumed = new Map();
  const io = { ...RENAME_IO, ...ctx.receiptIo };
  function directory(slug) {
    requireThat(/^[a-z0-9][a-z0-9-]{0,79}$/.test(slug ?? ""), "invalid stage slug for its durable journal");
    return path.join(resolveWorkdir({ env: ctx.env, root: ctx.root, home: ctx.home, slug }), RUN_RECEIPTS_DIR);
  }
  function read(file) {
    let record;
    try { record = JSON.parse(readFileSync(file, "utf8")); }
    catch { throw new RunReceiptError("stage journal is unreadable; preserve it and inspect the saved request before retrying"); }
    requireThat(record?.schema_version === 1 && record.site === site && UUID.test(record.request_key ?? "")
      && HASH.test(record.source_hash ?? "") && record.source_hash === sourceHash(normalizeRun(record.request))
      && canonicalJson(record.request) === canonicalJson(normalizeRun(record.request))
      && path.basename(file) === `${record.source_hash}.json`, "stage journal has changed identities or source bytes");
    if (record.receipt) {
      validateRunReceipt(record.receipt, { ...record, receipt: null });
      requireThat(record.receipt_hash === sourceHash(record.receipt), "stage journal has changed receipt bytes");
    }
    if (record.policy_rejection) requireThat(record.receipt === null && record.policy_rejection.error_code === POLICY_HOLD_CODE
      && record.policy_rejection.error_status === 409 && typeof record.policy_rejection.error_detail === "string",
    "invalid saved policy rejection");
    requireThat(record.adopted === undefined || typeof record.adopted === "boolean" && (!record.adopted || record.receipt?.status === "succeeded"), "only a successful stage receipt can be adopted");
    if (record.adopted) requireThat(Array.isArray(record.adoption?.artifacts) && record.adoption.artifacts.length > 0
      && record.adoption.artifacts.every((item) => typeof item?.path === "string" && path.isAbsolute(item.path) && HASH.test(item.sha256 ?? "")), "adopted stage receipt has no saved artifact proofs");
    return record;
  }
  return {
    /**
     * The journal of this exact request, or of the same unit with only derived drift (unitSource);
     * else, with `stale: true`, an unfinished journal of the same stage and variant whose inputs
     * differ (a deploy changed the prompt, the owner edited a setting or the source). The caller
     * reconciles a stale journal with the server (client.mjs) and archives or removes it; it is
     * never a match, and `prepare` refuses to create a new journal beside it.
     */
    find(request) {
      const normalized = normalizeRun(request), hash = sourceHash(normalized), file = path.join(directory(normalized.slug), `${hash}.json`);
      if (existsSync(file)) return { file, record: read(file) };
      const dir = path.dirname(file);
      if (!existsSync(dir)) return null;
      let stale = null;
      for (const name of readdirSync(dir).filter((name) => name.endsWith(".json"))) {
        const otherFile = path.join(dir, name), record = read(otherFile);
        if (record.request.stage === normalized.stage && record.request.variant === normalized.variant
          && !record.adopted && !consumed.has(otherFile)) {
          if (unitSource(record.request) === unitSource(normalized)) return { file: otherFile, record };
          stale ??= { file: otherFile, record, stale: true };
        }
      }
      return stale;
    },
    prepare(request) {
      const previous = this.find(request);
      if (previous?.stale) throw inputChanged();
      if (previous) return previous;
      const normalized = normalizeRun(request), hash = sourceHash(normalized), file = path.join(directory(normalized.slug), `${hash}.json`);
      mkdirSync(path.dirname(file), { recursive: true });
      const record = { schema_version: 1, site, source_hash: hash, request_key: randomUUID(), request: normalized, receipt: null };
      let fd;
      try { fd = openSync(file, "wx", 0o600); }
      catch (error) { if (error.code === "EEXIST") return { file, record: read(file) }; throw error; }
      try { writeFileSync(fd, `${JSON.stringify(record, null, 2)}\n`); fsyncSync(fd); }
      finally { closeSync(fd); }
      return { file, record };
    },
    receive(entry, receipt) {
      const current = read(entry.file);
      requireThat(current.request_key === entry.record.request_key, "stage journal changed during its request");
      const verified = validateRunReceipt(receipt, current);
      const next = { ...current, receipt: verified, receipt_hash: sourceHash(verified) };
      save(entry.file, next, io);
      entry.record = next;
      return next.receipt;
    },
    consume(entry) { consumed.set(entry.file, entry.record.request_key); },
    hold(entry, rejection) {
      const current = read(entry.file);
      requireThat(current.request_key === entry.record.request_key && current.receipt === null
        && rejection.error_code === POLICY_HOLD_CODE && rejection.error_status === 409,
      "only an undispatched policy refusal may be saved without a job receipt");
      const next = { ...current, policy_rejection: structuredClone(rejection) };
      save(entry.file, next, io);
      entry.record = next;
    },
    adopt(slug, proof) {
      let verified = null;
      for (const [file, key] of consumed) {
        const current = read(file);
        if (current.request.slug !== slug || current.adopted) continue;
        requireThat(current.request_key === key && current.receipt?.status === "succeeded", "only a consumed successful stage may be adopted");
        if (!verified) {
          requireThat(Array.isArray(proof?.artifacts) && proof.artifacts.length > 0
            && new Set(proof.artifacts.map((item) => item.path)).size === proof.artifacts.length, "adopting a stage result needs its saved artifact proofs");
          for (const item of proof.artifacts) {
            requireThat(typeof item?.path === "string" && path.isAbsolute(item.path) && HASH.test(item.sha256 ?? ""), "invalid saved artifact proof");
            requireThat(existsSync(item.path) && createHash("sha256").update(readFileSync(item.path)).digest("hex") === item.sha256, "saved artifact bytes changed before stage adoption");
          }
          verified = structuredClone(proof.artifacts);
        }
        save(file, { ...current, adopted: true, adoption: { artifacts: verified, recorded_at: (ctx.now?.() ?? new Date()).toISOString() } }, io);
      }
    },
    removeFailed(entry) {
      const current = read(entry.file);
      requireThat(current.request_key === entry.record.request_key && current.receipt?.status === "failed", "only a definitively failed stage may be cleared");
      requireThat(!policyHeld(current), "a policy refusal must be retained until a validated owner retry");
      unlinkSync(entry.file);
    },
    settle(slugs = null) {
      const selected = slugs === null ? null : new Set(Array.isArray(slugs) ? slugs : [slugs]);
      for (const [file, key] of consumed) {
        const record = read(file);
        if (selected !== null && !selected.has(record.request.slug)) continue;
        requireThat(record.request_key === key && record.receipt?.status === "succeeded", "only a consumed successful stage may be settled");
        unlinkSync(file);
        consumed.delete(file);
      }
      if (selected) for (const slug of selected) {
        const dir = directory(slug);
        if (!existsSync(dir)) continue;
        for (const name of readdirSync(dir).filter((name) => name.endsWith(".json"))) {
          const file = path.join(dir, name), current = read(file);
          if (current.adopted && current.receipt?.status === "succeeded") unlinkSync(file);
        }
      }
    },
    /**
     * Move a journal aside, keeping its bytes: an uncertain run the owner retries, a changed-input
     * success the owner retries (`requestId`, `reason`), a validated policy retry, or
     * (`autoArchive`) a stale journal the worker reconciled itself: its run succeeded and was
     * never adopted, it never reached the server (no receipt, no policy hold), or the server
     * answered its lookup with a settled 4xx (`gone: { status, code }`; not a policy hold).
     */
    archive(entry, { requestId = null, reason = "", policyValidated = false, autoArchive = false, gone = null } = {}) {
      const current = read(entry.file);
      requireThat(current.request_key === entry.record.request_key, "stage journal changed before owner retry");
      const successfulSourceChange = current.receipt?.status === "succeeded" && !current.adopted
        && UUID.test(requestId ?? "") && typeof reason === "string" && reason.includes("inputs changed");
      const policyRetry = policyHeld(current) && UUID.test(requestId ?? "") && policyValidated === true
        && (!current.receipt || current.receipt.dispatched_at === null);
      const jobGone = autoArchive === true && validGone(gone) && current.receipt !== null && !current.adopted && !policyHeld(current);
      const terminal = autoArchive === true && (current.receipt?.status === "succeeded" && !current.adopted
        || current.receipt === null && !policyHeld(current)) || jobGone;
      requireThat(current.receipt?.status === "uncertain" || successfulSourceChange || policyRetry || terminal,
        "only a confirmed uncertain run, authorized changed input, validated policy retry or terminal stale run can be archived");
      if (terminal) { requestId = null; reason = jobGone ? jobGoneReason(gone) : AUTO_ARCHIVE_REASON; }
      const archiveDir = path.join(path.dirname(entry.file), "archive");
      mkdirSync(archiveDir, { recursive: true });
      if (policyRetry) for (const name of readdirSync(archiveDir).filter((name) => name.endsWith(".json"))) {
        let previous;
        try { previous = JSON.parse(readFileSync(path.join(archiveDir, name), "utf8")); }
        catch { throw new RunReceiptError("an owner retry archive is unreadable; preserve it before resuming"); }
        requireThat(previous.owner_retry?.request_id !== requestId, "this owner retry was already used; a new request is required");
      }
      const target = path.join(archiveDir, `${current.source_hash}-${current.request_key}.json`);
      requireThat(!existsSync(target), "the owner retry archive already exists; preserve both journals and inspect it");
      save(entry.file, { ...current, owner_retry: { request_id: requestId, reason, archived_at: (ctx.now?.() ?? new Date()).toISOString() } }, io);
      renameJournal(entry.file, target, io);
      consumed.delete(entry.file);
    },
    retry(slug) {
      const dir = directory(slug);
      if (!existsSync(dir)) return;
      for (const name of readdirSync(dir).filter((name) => name.endsWith(".json"))) {
        const file = path.join(dir, name), record = read(file);
        if (record.receipt?.status === "uncertain") this.archive({ file, record });
      }
    },
    /**
     * What an owner retry may touch; a plain failed journal is listed so the retry can clear it.
     * `kind` is what blocked the video: for `job_gone:<stage>` (the lookup of that stage's saved
     * job answered that the server no longer has it) the stage's queued or running journal is
     * listed too, under the owner's request id only, so the retry can look it up once more and
     * archive it as gone. Nothing else may touch a journal whose job might still be running.
     */
    retryCandidates(slug, { requestId = null, reason = "", kind = null } = {}) {
      const dir = directory(slug);
      if (!existsSync(dir)) return [];
      const goneStage = UUID.test(requestId ?? "") && typeof kind === "string" && kind.startsWith(JOB_GONE_KIND) ? kind.slice(JOB_GONE_KIND.length) : null;
      return readdirSync(dir).filter((name) => name.endsWith(".json")).map((name) => {
        const file = path.join(dir, name);
        return { file, record: read(file) };
      }).filter((entry) => entry.record.receipt?.status === "uncertain" || entry.record.receipt?.status === "failed" && !policyHeld(entry.record)
        || UUID.test(requestId ?? "") && policyHeld(entry.record) || UUID.test(requestId ?? "")
        && typeof reason === "string" && reason.includes("inputs changed")
        && ["queued", "running", "succeeded"].includes(entry.record.receipt?.status) && !entry.record.adopted
        || goneStage !== null && goneStage !== "" && entry.record.request.stage === goneStage
        && ["queued", "running"].includes(entry.record.receipt?.status) && !entry.record.adopted);
    },
  };
}
