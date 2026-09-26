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
 * key, job_id?, seconds?, cost_usd, status (ready|failed|judged) }`.
 */
export function appendLedger(workdir, entry, now = new Date()) {
  const ledger = readLedger(workdir);
  ledger.entries.push({ at: now.toISOString(), ...entry });
  ledger.totals = totalsOf(ledger.entries);
  atomicWrite(ledgerFile(workdir), `${JSON.stringify(ledger, null, 2)}\n`);
  return ledger.totals;
}

export function ledgerTotals(workdir) {
  return totalsOf(readLedger(workdir).entries);
}

/** Why a generation costing `usd` may not be submitted now under the per-video cap, or null. */
export function capProblem(workdir, usd, cap) {
  if (!(cap > 0)) return null;
  const spent = ledgerTotals(workdir).usd;
  if (spent + usd <= cap) return null;
  return `this video has spent US$${spent.toFixed(2)} and the next generation costs about US$${usd.toFixed(2)}, past the per-video cap of US$${cap}; raise max_usd_per_video on /admin/videos or stop here`;
}
