// The cost ledger: every generation and judge call a video paid for, and the running totals.
//
// The server enforces the month's budgets; this is the per-video view the stages use to refuse
// a generation that would pass the owner's per-video cap (`max_usd_per_video` from
// `media-status`) before it is submitted, and what `media-status` prints.
//
// Money is held before it is spent: a stage writes a `reserved` row at list price under the
// request's key before it submits, so the cap counts work in flight, and the row is replaced by
// what the server charged (`bookJob`, `bookImport`) or dropped when nothing was submitted
// (`release`). A run that dies between submit and reconcile leaves its `reserved` row in the
// ledger, where `media-status` and the estimate show it, until the next run picks the job up by
// its key and books it. A ledger written before reservations existed has no such rows and reads
// as before: `totals.reserved` is simply zero.
import path from "node:path";

import { atomicWrite, readJson } from "../core/paths.mjs";
import { ARTIFACTS } from "../core/state.mjs";

export const ledgerFile = (workdir) => path.join(workdir, ARTIFACTS.mediaLedger);

const EMPTY = () => ({ entries: [], totals: { usd: 0, images: 0, clip_seconds: 0, music: 0, judge_calls: 0, reserved: 0, reservations: 0 } });

export function readLedger(workdir) {
  return readJson(ledgerFile(workdir), EMPTY());
}

const round = (value) => Math.round(value * 10_000) / 10_000;

/**
 * Recompute the totals from the entries, so a hand edit or a lost write cannot skew them.
 * `usd` is every dollar this video has committed: what the server charged plus what is still
 * held by `reserved` rows, which `reserved` and `reservations` report apart. A reserved row
 * counts its kind (an image, its clip seconds) the way a failed job's row does: it is replaced,
 * not added to, when the job is booked.
 */
export function totalsOf(entries) {
  const totals = EMPTY().totals;
  for (const entry of entries) {
    totals.usd = round(totals.usd + Number(entry.cost_usd || 0));
    if (entry.status === "reserved") {
      totals.reserved = round(totals.reserved + Number(entry.cost_usd || 0));
      totals.reservations += 1;
    }
    if (entry.kind === "image") totals.images += 1;
    else if (entry.kind === "clip") totals.clip_seconds += Number(entry.seconds || 0);
    else if (entry.kind === "music") totals.music += 1;
    else if (entry.kind === "judge") totals.judge_calls += 1;
  }
  return totals;
}

function save(workdir, ledger) {
  ledger.totals = totalsOf(ledger.entries);
  atomicWrite(ledgerFile(workdir), `${JSON.stringify(ledger, null, 2)}\n`);
  return ledger.totals;
}

/** The index of the `reserved` row held under `key`, or -1 (a row without a key never matches). */
const reservedIndex = (entries, key) => (key ? entries.findIndex((entry) => entry.status === "reserved" && entry.key === key) : -1);

/** The `reserved` rows: `[{ at, stage, kind, id, key, seconds, cost_usd, ... }]`, oldest first. */
export const reservedEntries = (entries) => entries.filter((entry) => entry.status === "reserved");

/**
 * Append one entry: `{ stage, kind (image|clip|music|judge), id (shot or character), provider, model,
 * key, job_id?, seconds?, cost_usd, status (ready|failed|judged|cut|imported) }`.
 */
export function appendLedger(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  ledger.entries.push({ at: now.toISOString(), ...entry });
  return save(workdir, ledger);
}

/**
 * Hold money for a request about to be submitted: `{ stage, kind, id, provider, model, key,
 * seconds?, cost_usd }` at list price, as a `reserved` row under its `key`. The row counts
 * toward the per-video cap until `bookJob` or `bookImport` replaces it with what was actually
 * charged, or `release` drops it. Reserving the same key again replaces the row, so a run that
 * repeats a submission after a lost answer holds the money once.
 */
export function reserve(workdir, entry, now = new Date()) {
  if (!entry.key) throw new TypeError("a reservation needs the request key it will be reconciled under");
  const ledger = readLedger(workdir);
  const recorded = { at: now.toISOString(), ...entry, status: "reserved" };
  const index = reservedIndex(ledger.entries, entry.key);
  if (index < 0) ledger.entries.push(recorded);
  else ledger.entries[index] = recorded;
  return save(workdir, ledger);
}

/** Drop the reservation held under `key` because nothing was submitted for it; returns the totals. */
export function release(workdir, key) {
  const ledger = readLedger(workdir);
  const index = reservedIndex(ledger.entries, key);
  if (index < 0) return totalsOf(ledger.entries);
  ledger.entries.splice(index, 1);
  return save(workdir, ledger);
}

/**
 * Reconcile a server job, whose id survives both retries and idempotent resubmissions. A job
 * seen for the first time replaces the `reserved` row held under its request `key`, so the
 * estimate gives way to the server's charge; a job seen before updates its own row, and the
 * hold a resubmission took out under the key goes with it, since the job's row carries the charge.
 */
export function bookJob(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  const recorded = { at: now.toISOString(), ...entry };
  const index = entry.job_id ? ledger.entries.findIndex((previous) => previous.job_id === entry.job_id) : -1;
  const held = reservedIndex(ledger.entries, entry.key);
  if (index >= 0) {
    // A failed attempt can cost zero and later succeed under the same id. Conversely,
    // a later failure must not erase a charge already observed for this job.
    recorded.cost_usd = Math.max(Number(ledger.entries[index].cost_usd || 0), Number(entry.cost_usd || 0));
    ledger.entries[index] = recorded;
    if (held >= 0) ledger.entries.splice(held, 1);
  } else if (held >= 0) ledger.entries[held] = recorded;
  else ledger.entries.push(recorded);
  return save(workdir, ledger);
}

export function ledgerTotals(workdir) {
  return totalsOf(readLedger(workdir).entries);
}

/**
 * Record a shot cut from another shot's clip (docs/videos/DRAMA.md): nothing was bought, and
 * the entry says what the cut would have cost (`saved_seconds`, `saved_usd`). Keyed by the
 * shot, so a rerun of the stage replaces it instead of counting the saving twice.
 */
export function bookReuse(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  const recorded = { at: now.toISOString(), ...entry, kind: "clip", status: "cut", seconds: 0, cost_usd: 0 };
  const index = ledger.entries.findIndex((previous) => previous.status === "cut" && previous.id === entry.id);
  if (index < 0) ledger.entries.push(recorded);
  else ledger.entries[index] = recorded;
  return save(workdir, ledger);
}

/** What the cuts from other shots' clips saved: { clip_seconds, usd, cuts }. */
export function savedTotals(entries) {
  const saved = { clip_seconds: 0, usd: 0, cuts: 0 };
  for (const entry of entries) {
    if (entry.status !== "cut") continue;
    saved.cuts += 1;
    saved.clip_seconds += Number(entry.saved_seconds || 0);
    saved.usd = round(saved.usd + Number(entry.saved_usd || 0));
  }
  return saved;
}

/**
 * Record a clip made outside the pipeline and brought in by `clips import` (a Hailuo web plan,
 * Kling's MCP): `{ stage, id, provider, plan, credits, seconds, cost_usd, file, sha256 }`. Its
 * seconds count as clip seconds; its cost is what the operator priced the credits at, or zero.
 * Keyed by the shot and the file, so importing the same file again replaces the entry. A `key`
 * names the reservation the import held while it was checked; the row replaces that
 * reservation and does not carry the key.
 */
export function bookImport(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  const { key = null, ...fields } = entry;
  const recorded = { at: now.toISOString(), ...fields, kind: "clip", status: "imported" };
  const held = reservedIndex(ledger.entries, key);
  const index = ledger.entries.findIndex((previous) => previous.status === "imported" && previous.id === entry.id && previous.sha256 === entry.sha256);
  if (index >= 0) {
    ledger.entries[index] = recorded;
    if (held >= 0) ledger.entries.splice(held, 1);
  } else if (held >= 0) ledger.entries[held] = recorded;
  else ledger.entries.push(recorded);
  return save(workdir, ledger);
}

/** What was imported rather than bought: { clips, clip_seconds, credits, usd }. */
export function importedTotals(entries) {
  const imported = { clips: 0, clip_seconds: 0, credits: 0, usd: 0 };
  for (const entry of entries) {
    if (entry.status !== "imported") continue;
    imported.clips += 1;
    imported.clip_seconds += Number(entry.seconds || 0);
    imported.credits += Number(entry.credits || 0);
    imported.usd = round(imported.usd + Number(entry.cost_usd || 0));
  }
  return imported;
}

/**
 * Why spending `usd` on `what` (a generation, a judge call, an import) may not go ahead now under
 * the per-video cap, or null. What the video has committed is what the server charged plus what
 * its `reserved` rows still hold, so work in flight and work left by a dead run count too.
 */
export function capProblem(workdir, usd, cap, what = "generation") {
  if (!(cap > 0)) return null;
  const totals = ledgerTotals(workdir);
  const spent = totals.usd;
  if (round(spent + usd) <= cap) return null;
  const held = totals.reserved > 0 ? ` (US$${totals.reserved.toFixed(2)} of it reserved for ${totals.reservations} ${totals.reservations === 1 ? "request" : "requests"} not yet reconciled)` : "";
  return `this video has spent US$${spent.toFixed(2)}${held} and the next ${what} costs about US$${usd.toFixed(2)}, past the per-video cap of US$${cap}; raise max_usd_per_video on /admin/videos or stop here`;
}
