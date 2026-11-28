/**
 * Per-episode credit ledger, series budget hard cap enforcement, and
 * single-use SHA-256 bound `confirm_token` approvals.
 *
 * Supports both uniform per-clip credits (explainers) and variable per-shot
 * credits (AI dramas mixing 4s/6s/8s/10s Omni 1.2 Flash, Veo 3.1, and Extend).
 */

import { createHash, randomBytes } from "node:crypto";
import fs from "node:fs";
import path from "node:path";
import { DEFAULT_CLIP_CREDITS, DEFAULT_VIDEO_MODEL, getSeriesPreset } from "../config.mjs";

const DEFAULT_TOKEN_TTL_MS = 30 * 60 * 1000;

export function atomicWriteJson(filePath, data) {
  fs.mkdirSync(path.dirname(filePath), { recursive: true });
  const tmpPath = `${filePath}.${process.pid}.${randomBytes(4).toString("hex")}.tmp`;
  fs.writeFileSync(tmpPath, `${JSON.stringify(data, null, 2)}\n`, "utf8");
  fs.renameSync(tmpPath, filePath);
}

export function readJsonSafe(filePath, fallback) {
  if (!fs.existsSync(filePath)) return fallback;
  return JSON.parse(fs.readFileSync(filePath, "utf8"));
}

export function loadCreditLedger(ledgerFile, { slug, series = "curio" } = {}) {
  const preset = getSeriesPreset(series);
  const existing = readJsonSafe(ledgerFile, null);
  if (existing && typeof existing === "object") {
    return existing;
  }
  return {
    schemaVersion: 1,
    slug: slug || null,
    series: preset.id,
    budgetSoftCap: preset.budgetSoftCap,
    budgetHardCap: preset.budgetHardCap,
    totalSpentCredits: 0,
    totalMaybeCredits: 0,
    entries: [],
  };
}

export function recalculateLedgerTotals(ledger) {
  ledger.totalSpentCredits = (ledger.entries || [])
    .filter((e) => e.charged === "yes")
    .reduce((sum, e) => sum + (Number(e.credits) || 0), 0);
  ledger.totalMaybeCredits = (ledger.entries || [])
    .filter((e) => e.charged === "maybe")
    .reduce((sum, e) => sum + (Number(e.credits) || 0), 0);
  return ledger;
}

export function recordCreditEvent(
  ledgerFile,
  {
    slug,
    series = "curio",
    shotId,
    model = DEFAULT_VIDEO_MODEL,
    credits = DEFAULT_CLIP_CREDITS,
    charged = "yes", // "yes" | "maybe" | "no"
    mediaId = null,
    operation = "clip", // "clip" | "extend" | "reconcile"
    take = null,
    note = "",
    timestamp = new Date().toISOString(),
  },
) {
  const ledger = loadCreditLedger(ledgerFile, { slug, series });
  const normalizedCharged = ["yes", "maybe", "no"].includes(charged) ? charged : "maybe";
  const amount = Number(credits) || 0;

  ledger.entries.push({
    timestamp,
    shotId,
    operation,
    take,
    model,
    credits: amount,
    charged: normalizedCharged,
    mediaId,
    note,
  });

  recalculateLedgerTotals(ledger);
  atomicWriteJson(ledgerFile, ledger);
  return ledger;
}

function hashApprovalPayload({ slug, shotIds, model, plannedCredits }) {
  const canonical = JSON.stringify({
    slug,
    shotIds: [...shotIds].map(String).sort(),
    model: String(model),
    plannedCredits: Number(plannedCredits),
  });
  return createHash("sha256").update(canonical).digest("hex");
}

/**
 * Evaluates a clip/extend generation plan against series caps, existing spend,
 * and optional live account balance. Mints a single-use `confirm_token`.
 */
export function planClipBudget({
  episodePaths,
  series = "curio",
  shotIds,
  shotPlans = null, // optional [{ shotId, model, durationSec, credits }]
  model = DEFAULT_VIDEO_MODEL,
  creditsPerClip = DEFAULT_CLIP_CREDITS,
  accountCredits = null,
  budgetHardCapOverride = null,
  ttlMs = DEFAULT_TOKEN_TTL_MS,
  now = Date.now(),
}) {
  const preset = getSeriesPreset(series);
  const cleanShotIds = [...new Set((shotIds || []).map(String).filter(Boolean))];

  if (cleanShotIds.length === 0) {
    return {
      ok: false,
      reason: "no_shots_selected",
      message: "No approved clip shots were provided to plan.",
    };
  }

  const ledger = loadCreditLedger(episodePaths.ledgerFile, {
    slug: episodePaths.slug,
    series: preset.id,
  });

  const committedCredits = ledger.totalSpentCredits + ledger.totalMaybeCredits;
  const plannedCredits = Array.isArray(shotPlans) && shotPlans.length > 0
    ? shotPlans.reduce((sum, p) => sum + (Number(p.credits) || 0), 0)
    : cleanShotIds.length * creditsPerClip;
  const projectedTotal = committedCredits + plannedCredits;
  const hardCap =
    budgetHardCapOverride != null ? Number(budgetHardCapOverride) : preset.budgetHardCap;
  const softCap = Math.min(preset.budgetSoftCap, hardCap);

  if (projectedTotal > hardCap) {
    return {
      ok: false,
      reason: "budget_exceeded",
      series: preset.id,
      shotCount: cleanShotIds.length,
      creditsPerClip,
      shotPlans: shotPlans || null,
      alreadyCommittedCredits: committedCredits,
      plannedCredits,
      projectedTotal,
      budgetSoftCap: softCap,
      budgetHardCap: hardCap,
      message: `Refused: projected episode spend (${projectedTotal} credits = ${committedCredits} committed + ${plannedCredits} planned) exceeds ${preset.label} hard cap of ${hardCap} credits.`,
    };
  }

  if (accountCredits != null && Number.isFinite(Number(accountCredits)) && plannedCredits > Number(accountCredits)) {
    return {
      ok: false,
      reason: "insufficient_account_credits",
      series: preset.id,
      shotCount: cleanShotIds.length,
      plannedCredits,
      accountCredits: Number(accountCredits),
      message: `Refused: planned batch needs ${plannedCredits} credits, but account balance is ${accountCredits}.`,
    };
  }

  const token = `mflow_${randomBytes(12).toString("hex")}`;
  const payloadHash = hashApprovalPayload({
    slug: episodePaths.slug,
    shotIds: cleanShotIds,
    model,
    plannedCredits,
  });
  const expiresAt = new Date(now + ttlMs).toISOString();

  const store = readJsonSafe(episodePaths.pendingApprovalsFile, { approvals: {} });
  for (const [key, entry] of Object.entries(store.approvals || {})) {
    if (!entry.expiresAt || Date.parse(entry.expiresAt) <= now) {
      delete store.approvals[key];
    }
  }
  store.approvals[token] = {
    payloadHash,
    slug: episodePaths.slug,
    shotIds: cleanShotIds,
    model,
    plannedCredits,
    shotPlans: shotPlans || null,
    createdAt: new Date(now).toISOString(),
    expiresAt,
    consumedAt: null,
  };
  atomicWriteJson(episodePaths.pendingApprovalsFile, store);

  return {
    ok: true,
    series: preset.id,
    model,
    shotIds: cleanShotIds,
    shotCount: cleanShotIds.length,
    creditsPerClip,
    shotPlans: shotPlans || null,
    alreadyCommittedCredits: committedCredits,
    plannedCredits,
    projectedTotal,
    remainingAfterBatch: hardCap - projectedTotal,
    budgetSoftCap: softCap,
    budgetHardCap: hardCap,
    softCapWarning: projectedTotal > softCap
      ? `Projected spend (${projectedTotal}) exceeds soft cap (${softCap}) but is within hard cap (${hardCap}).`
      : null,
    accountCredits: accountCredits != null ? Number(accountCredits) : null,
    confirm_token: token,
    expiresAt,
    ownerPrompt: `Confirm spending ${plannedCredits} Flow credits (${cleanShotIds.length} shot(s), model=${model}; episode total ${projectedTotal}/${hardCap}) before calling flow_generate_clips / flow_extend_clip with confirm_token.`,
  };
}

/**
 * Validates and atomically consumes a single-use `confirm_token`.
 */
export function verifyAndConsumeConfirmToken({
  episodePaths,
  token,
  shotIds,
  model = DEFAULT_VIDEO_MODEL,
  creditsPerClip = DEFAULT_CLIP_CREDITS,
  plannedCreditsOverride = null,
  now = Date.now(),
}) {
  if (!token || typeof token !== "string") {
    return {
      ok: false,
      reason: "missing_confirm_token",
      message: "Paid generation requires a confirm_token from flow_plan_clips after owner approval.",
    };
  }

  const store = readJsonSafe(episodePaths.pendingApprovalsFile, { approvals: {} });
  const record = store.approvals?.[token];
  if (!record) {
    return {
      ok: false,
      reason: "unknown_confirm_token",
      message: "confirm_token was not found. Call flow_plan_clips to generate a fresh approval token.",
    };
  }
  if (record.consumedAt) {
    return {
      ok: false,
      reason: "token_already_consumed",
      message: `confirm_token was already used at ${record.consumedAt}. Call flow_plan_clips for a new batch.`,
    };
  }
  if (Date.parse(record.expiresAt) <= now) {
    return {
      ok: false,
      reason: "token_expired",
      message: `confirm_token expired at ${record.expiresAt}. Call flow_plan_clips to refresh.`,
    };
  }

  const cleanShotIds = [...new Set((shotIds || []).map(String).filter(Boolean))];
  const plannedCredits =
    plannedCreditsOverride != null
      ? Number(plannedCreditsOverride)
      : cleanShotIds.length * creditsPerClip;
  const expectedHash = hashApprovalPayload({
    slug: episodePaths.slug,
    shotIds: cleanShotIds,
    model,
    plannedCredits,
  });

  if (record.payloadHash !== expectedHash) {
    return {
      ok: false,
      reason: "token_payload_mismatch",
      message: "confirm_token does not match the requested shot_ids / model / planned credits. Re-run flow_plan_clips.",
    };
  }

  record.consumedAt = new Date(now).toISOString();
  atomicWriteJson(episodePaths.pendingApprovalsFile, store);

  return {
    ok: true,
    approval: record,
  };
}
