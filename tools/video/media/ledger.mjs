// The cost ledger: every generation and judge call a video paid for, and the running totals.
//
// The server enforces the month's budgets; this is the per-video view the stages use to refuse
// a generation that would pass the owner's per-video cap (`max_usd_per_video` from
// `media-status`) before it is submitted, and what `media-status` prints.
import path from "node:path";

import { atomicWrite, readJson } from "../core/paths.mjs";
import { ARTIFACTS } from "../core/state.mjs";

export const ledgerFile = (workdir) => path.join(workdir, ARTIFACTS.mediaLedger);

const EMPTY = () => ({ entries: [], totals: { usd: 0, images: 0, clip_seconds: 0, music: 0, judge_calls: 0 } });

export function readLedger(workdir) {
  return readJson(ledgerFile(workdir), EMPTY());
}

const round = (value) => Math.round(value * 10_000) / 10_000;

/** Recompute the totals from the entries, so a hand edit or a lost write cannot skew them. */
export function totalsOf(entries) {
  const totals = EMPTY().totals;
  for (const entry of entries) {
    totals.usd = round(totals.usd + Number(entry.cost_usd || 0));
    if (entry.kind === "image") totals.images += 1;
    else if (entry.kind === "clip") totals.clip_seconds += Number(entry.seconds || 0);
    else if (entry.kind === "music") totals.music += 1;
    else if (entry.kind === "judge") totals.judge_calls += 1;
  }
  return totals;
}

/**
 * Append one entry: `{ stage, kind (image|clip|music|judge), id (shot or character), provider, model,
 * key, job_id?, seconds?, cost_usd, status (ready|failed|judged|cut|imported) }`.
 */
export function appendLedger(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  ledger.entries.push({ at: now.toISOString(), ...entry });
  ledger.totals = totalsOf(ledger.entries);
  atomicWrite(ledgerFile(workdir), `${JSON.stringify(ledger, null, 2)}\n`);
  return ledger.totals;
}

/** Reconcile a server job, whose id survives both retries and idempotent resubmissions. */
export function bookJob(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  const index = ledger.entries.findIndex((previous) => previous.job_id === entry.job_id);
  const recorded = { at: now.toISOString(), ...entry };
  if (index < 0) ledger.entries.push(recorded);
  else {
    // A failed attempt can cost zero and later succeed under the same id. Conversely,
    // a later failure must not erase a charge already observed for this job.
    recorded.cost_usd = Math.max(Number(ledger.entries[index].cost_usd || 0), Number(entry.cost_usd || 0));
    ledger.entries[index] = recorded;
  }
  ledger.totals = totalsOf(ledger.entries);
  atomicWrite(ledgerFile(workdir), `${JSON.stringify(ledger, null, 2)}\n`);
  return ledger.totals;
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
  ledger.totals = totalsOf(ledger.entries);
  atomicWrite(ledgerFile(workdir), `${JSON.stringify(ledger, null, 2)}\n`);
  return ledger.totals;
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
 * Keyed by the shot and the file, so importing the same file again replaces the entry.
 */
export function bookImport(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  const recorded = { at: now.toISOString(), ...entry, kind: "clip", status: "imported" };
  const index = ledger.entries.findIndex((previous) => previous.status === "imported" && previous.id === entry.id && previous.sha256 === entry.sha256);
  if (index < 0) ledger.entries.push(recorded);
  else ledger.entries[index] = recorded;
  ledger.totals = totalsOf(ledger.entries);
  atomicWrite(ledgerFile(workdir), `${JSON.stringify(ledger, null, 2)}\n`);
  return ledger.totals;
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

/** Why a generation costing `usd` may not be submitted now under the per-video cap, or null. */
export function capProblem(workdir, usd, cap) {
  if (!(cap > 0)) return null;
  const spent = ledgerTotals(workdir).usd;
  if (spent + usd <= cap) return null;
  return `this video has spent US$${spent.toFixed(2)} and the next generation costs about US$${usd.toFixed(2)}, past the per-video cap of US$${cap}; raise max_usd_per_video on /admin/videos or stop here`;
}
