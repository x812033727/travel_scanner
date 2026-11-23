"use client";

import { ExternalLink, Play, Plus, Save, Trash2 } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { geminiPoolCopy } from "@/lib/gemini-pool-copy";

export type GeminiPoolKey = {
  slot?: string;
  configured?: boolean;
  fingerprint_tail: string;
  position: number;
  site_key: boolean;
  active: boolean;
  is_turn?: boolean;
  resting: string | null;
  rest_seconds: number;
  month_usd: number;
  budget_usd: number | null;
};

export type GeminiPoolSnapshot = {
  keys: GeminiPoolKey[];
  current_turn_slot?: string | null;
  slot_count?: number;
  redis_ok: boolean;
};

const ENDPOINT = "/admin/provider-settings/ai_vendors/gemini-pool";
const BILLING_URL = "https://aistudio.google.com/billing";
const SLOT_LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split("");
const DEFAULT_SLOT_COUNT = 4;

function usd(value: number) {
  return `US$${value.toFixed(2)}`;
}

function slotOf(key: GeminiPoolKey): string {
  if (key.slot) return key.slot;
  return key.site_key ? "SITE" : (SLOT_LETTERS[key.position] ?? String(key.position + 1));
}

/**
 * Per-slot Google AI Ultra Gemini key pool (A, B, C, D... expandable up to Z):
 * - Save or clear each account slot's API key and monthly budget individually.
 * - Circular turn rotation (A -> B -> C -> ... -> A) when the active slot runs out of credit or
 *   reaches its limit.
 * - Shows which slot is currently in turn and lets the owner click "Start here" on any configured
 *   slot to switch the rotation starting point immediately.
 */
export function AdminGeminiPool({ canManage = true }: { canManage?: boolean }) {
  const locale = useLocale();
  const copy = geminiPoolCopy(locale).panel;
  const dateTime = useMemo(
    () => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }),
    [locale],
  );
  const [snapshot, setSnapshot] = useState<GeminiPoolSnapshot | null>(null);
  const [loadedAt, setLoadedAt] = useState(0);
  const [failed, setFailed] = useState(false);
  const [extraCount, setExtraCount] = useState(DEFAULT_SLOT_COUNT);
  const [keyDrafts, setKeyDrafts] = useState<Record<string, string>>({});
  const [budgetDrafts, setBudgetDrafts] = useState<Record<string, string>>({});
  const [busySlot, setBusySlot] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [actionError, setActionError] = useState<string | null>(null);

  function applyResult(result: GeminiPoolSnapshot) {
    setSnapshot(result);
    setLoadedAt(Date.now());
    const configuredSlots = result.keys
      .filter((k) => !k.site_key)
      .map((k) => slotOf(k))
      .filter((s) => SLOT_LETTERS.includes(s));
    const highest = configuredSlots.reduce(
      (max, s) => Math.max(max, SLOT_LETTERS.indexOf(s) + 1),
      0,
    );
    setExtraCount((prev) => Math.max(prev, result.slot_count ?? DEFAULT_SLOT_COUNT, highest));
    const nextBudgets: Record<string, string> = {};
    for (const k of result.keys) {
      const s = slotOf(k);
      nextBudgets[s] = k.budget_usd !== null && k.budget_usd > 0 ? String(k.budget_usd) : "";
    }
    setBudgetDrafts((prev) => ({ ...prev, ...nextBudgets }));
  }

  useEffect(() => {
    let live = true;
    api<GeminiPoolSnapshot>(ENDPOINT)
      .then((result) => {
        if (!live) return;
        applyResult(result);
      })
      .catch(() => {
        if (live) setFailed(true);
      });
    return () => {
      live = false;
    };
  }, []);

  function stateText(key: GeminiPoolKey | undefined) {
    if (!key || (key.configured === false && !key.fingerprint_tail)) return copy.unconfigured;
    const until = dateTime.format(new Date(loadedAt + key.rest_seconds * 1000));
    if (key.resting === "exhausted") return `${copy.exhausted} ${until}`;
    if (key.resting === "busy") return `${copy.busy} ${until}`;
    if (key.budget_usd !== null && key.month_usd >= key.budget_usd) return copy.over;
    return key.active ? copy.active : copy.ready;
  }

  async function saveSlot(slot: string) {
    if (!canManage) return;
    setBusySlot(slot);
    setNotice(null);
    setActionError(null);
    const rawKey = (keyDrafts[slot] ?? "").trim();
    const rawBudget = (budgetDrafts[slot] ?? "").trim();
    const budgetValue = rawBudget === "" ? null : Number(rawBudget);
    try {
      const updated = await api<GeminiPoolSnapshot>(`${ENDPOINT}/slots/${slot}`, {
        method: "PUT",
        body: JSON.stringify({
          ...(rawKey ? { api_key: rawKey } : {}),
          budget_usd: budgetValue !== null && !Number.isNaN(budgetValue) && budgetValue > 0 ? budgetValue : null,
        }),
      });
      setKeyDrafts((prev) => ({ ...prev, [slot]: "" }));
      applyResult(updated);
      setNotice(`${copy.savedNotice} ${slot}`);
    } catch (err) {
      setActionError((err as Error).message);
    } finally {
      setBusySlot(null);
    }
  }

  async function clearSlot(slot: string) {
    if (!canManage) return;
    setBusySlot(slot);
    setNotice(null);
    setActionError(null);
    try {
      const updated = await api<GeminiPoolSnapshot>(`${ENDPOINT}/slots/${slot}`, {
        method: "PUT",
        body: JSON.stringify({ clear: true }),
      });
      setKeyDrafts((prev) => ({ ...prev, [slot]: "" }));
      setBudgetDrafts((prev) => ({ ...prev, [slot]: "" }));
      applyResult(updated);
      setNotice(`${copy.savedNotice} ${slot}`);
    } catch (err) {
      setActionError((err as Error).message);
    } finally {
      setBusySlot(null);
    }
  }

  async function startFromSlot(slot: string) {
    if (!canManage) return;
    setBusySlot(slot);
    setNotice(null);
    setActionError(null);
    try {
      const updated = await api<GeminiPoolSnapshot>(`${ENDPOINT}/turn`, {
        method: "POST",
        body: JSON.stringify({ slot }),
      });
      applyResult(updated);
      setNotice(`${copy.turnNotice} ${slot}`);
    } catch (err) {
      setActionError((err as Error).message);
    } finally {
      setBusySlot(null);
    }
  }

  const configuredBySlot = useMemo(() => {
    const map = new Map<string, GeminiPoolKey>();
    for (const k of snapshot?.keys ?? []) {
      map.set(slotOf(k), k);
    }
    return map;
  }, [snapshot]);

  const activeKey = useMemo(
    () => snapshot?.keys.find((k) => k.active),
    [snapshot],
  );
  const currentTurnSlot =
    snapshot?.current_turn_slot ??
    (activeKey ? slotOf(activeKey) : null);

  const visibleUltraSlots = SLOT_LETTERS.slice(0, Math.min(SLOT_LETTERS.length, extraCount));
  const siteKeyEntry = configuredBySlot.get("SITE");

  return (
    <section className="mt-6 rounded-2xl bg-[var(--paper)] p-4" data-testid="gemini-pool">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <div className="flex flex-wrap items-center gap-3">
          <h3 className="text-sm font-bold">{copy.title}</h3>
          {snapshot && currentTurnSlot && (
            <span
              data-testid="gemini-pool-current-turn"
              className="rounded-full bg-emerald-100 px-3 py-1 text-xs font-bold text-emerald-900"
            >
              {copy.currentTurn}：{currentTurnSlot === "SITE" ? copy.siteKey : `${copy.slotLabel} ${currentTurnSlot}`}
              {activeKey?.fingerprint_tail ? ` (…${activeKey.fingerprint_tail})` : ""}
            </span>
          )}
        </div>
        <a
          href={BILLING_URL}
          target="_blank"
          rel="noreferrer"
          className="inline-flex min-h-11 items-center gap-1 text-xs font-semibold text-[var(--teal)] underline"
        >
          {copy.billing}
          <ExternalLink size={13} aria-hidden />
        </a>
      </div>
      <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{copy.intro}</p>
      {failed && (
        <p role="alert" className="mt-3 text-sm text-red-700">
          {copy.error}
        </p>
      )}
      {notice && (
        <p role="status" className="mt-3 rounded-xl bg-emerald-50 px-3 py-2 text-xs font-semibold text-emerald-800">
          {notice}
        </p>
      )}
      {actionError && (
        <p role="alert" className="mt-3 rounded-xl bg-red-50 px-3 py-2 text-xs font-semibold text-red-800">
          {actionError}
        </p>
      )}
      {snapshot && snapshot.keys.length < 2 && (
        <p className="mt-3 text-sm text-[var(--muted)]">{copy.single}</p>
      )}
      {snapshot && (
        <div className="mt-3 overflow-x-auto">
          <table className="w-full text-left text-sm">
            <thead className="text-xs text-[var(--muted)]">
              <tr>
                <th className="py-2 pr-3">{copy.order}</th>
                <th className="py-2 pr-3">{copy.key}</th>
                <th className="py-2 pr-3">{copy.spent}</th>
                <th className="py-2 pr-3">{copy.budget}</th>
                <th className="py-2 pr-3">{copy.state}</th>
                <th className="py-2">{copy.actions}</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-[var(--line)]">
              {visibleUltraSlots.map((slot) => {
                const entry = configuredBySlot.get(slot);
                const isConfigured = Boolean(entry && entry.fingerprint_tail);
                const isActive = Boolean(entry?.active);
                const isTurn = currentTurnSlot === slot;
                const isBusy = busySlot === slot;
                const keyInput = keyDrafts[slot] ?? "";
                const budgetInput =
                  budgetDrafts[slot] ??
                  (entry?.budget_usd !== null && entry?.budget_usd !== undefined
                    ? String(entry.budget_usd)
                    : "");

                return (
                  <tr
                    key={slot}
                    data-testid={`gemini-slot-row-${slot}`}
                    className={isActive ? "bg-emerald-50/60 font-semibold" : undefined}
                  >
                    <td className="py-2.5 pr-3 whitespace-nowrap">
                      <span className="inline-flex h-6 w-6 items-center justify-center rounded-full bg-[var(--ink)] text-xs font-bold text-white">
                        {slot}
                      </span>
                      {entry && (
                        <span className="ml-2 text-xs text-[var(--muted)]">{entry.position + 1}</span>
                      )}
                    </td>
                    <td className="py-2.5 pr-3">
                      <div className="flex flex-col gap-1.5 sm:flex-row sm:items-center">
                        {isConfigured && (
                          <span className="font-mono text-xs">…{entry!.fingerprint_tail}</span>
                        )}
                        <input
                          type="password"
                          autoComplete="off"
                          disabled={!canManage || isBusy}
                          data-testid={`gemini-slot-key-${slot}`}
                          value={keyInput}
                          onChange={(e) =>
                            setKeyDrafts((prev) => ({ ...prev, [slot]: e.target.value }))
                          }
                          placeholder={
                            isConfigured ? copy.keyConfiguredPlaceholder : copy.keyPlaceholder
                          }
                          className="w-full min-w-[13rem] rounded-lg border border-[var(--line)] bg-white px-2.5 py-1.5 font-mono text-xs font-normal"
                        />
                      </div>
                    </td>
                    <td className="py-2.5 pr-3 whitespace-nowrap">
                      {isConfigured ? usd(entry!.month_usd) : "—"}
                    </td>
                    <td className="py-2.5 pr-3">
                      <div className="flex items-center gap-1.5">
                        {isConfigured && entry!.budget_usd !== null && (
                          <span className="text-xs text-[var(--muted)]">
                            {usd(entry!.budget_usd)}
                          </span>
                        )}
                        {isConfigured && entry!.budget_usd === null && (
                          <span className="text-xs text-[var(--muted)]">{copy.none}</span>
                        )}
                        <input
                          type="number"
                          min="0"
                          step="any"
                          disabled={!canManage || isBusy}
                          data-testid={`gemini-slot-budget-${slot}`}
                          value={budgetInput}
                          onChange={(e) =>
                            setBudgetDrafts((prev) => ({ ...prev, [slot]: e.target.value }))
                          }
                          placeholder={copy.budgetPlaceholder}
                          className="w-20 rounded-lg border border-[var(--line)] bg-white px-2 py-1.5 text-xs font-normal"
                        />
                      </div>
                    </td>
                    <td className="py-2.5 pr-3 whitespace-nowrap">{stateText(entry)}</td>
                    <td className="py-2.5 whitespace-nowrap">
                      <div className="flex flex-wrap items-center gap-1.5">
                        <button
                          type="button"
                          data-testid={`gemini-slot-save-${slot}`}
                          disabled={!canManage || isBusy || (!keyInput.trim() && !isConfigured)}
                          onClick={() => saveSlot(slot)}
                          className="inline-flex items-center gap-1 rounded-lg bg-[var(--teal)] px-2.5 py-1.5 text-xs font-semibold text-white disabled:opacity-40"
                        >
                          <Save size={12} />
                          {copy.saveSlot} {slot}
                        </button>
                        {isConfigured && (
                          <button
                            type="button"
                            data-testid={`gemini-slot-turn-${slot}`}
                            disabled={!canManage || isBusy || (isTurn && !entry?.resting)}
                            onClick={() => startFromSlot(slot)}
                            className="inline-flex items-center gap-1 rounded-lg border border-[var(--line)] bg-white px-2.5 py-1.5 text-xs font-semibold text-[var(--ink)] disabled:opacity-40"
                          >
                            <Play size={12} />
                            {copy.startHere}
                          </button>
                        )}
                        {isConfigured && (
                          <button
                            type="button"
                            data-testid={`gemini-slot-clear-${slot}`}
                            disabled={!canManage || isBusy}
                            onClick={() => clearSlot(slot)}
                            className="inline-flex items-center gap-1 rounded-lg border border-red-200 bg-white px-2 py-1.5 text-xs font-semibold text-red-700 disabled:opacity-40"
                          >
                            <Trash2 size={12} />
                            {copy.clearSlot}
                          </button>
                        )}
                      </div>
                    </td>
                  </tr>
                );
              })}
              {siteKeyEntry && (
                <tr className={siteKeyEntry.active ? "font-semibold" : undefined}>
                  <td className="py-2.5 pr-3">{siteKeyEntry.position + 1}</td>
                  <td className="py-2.5 pr-3 font-mono">
                    …{siteKeyEntry.fingerprint_tail}
                    <span className="ml-2 font-sans text-xs text-[var(--muted)]">
                      {copy.siteKey}
                    </span>
                  </td>
                  <td className="py-2.5 pr-3">{usd(siteKeyEntry.month_usd)}</td>
                  <td className="py-2.5 pr-3">
                    {siteKeyEntry.budget_usd === null
                      ? copy.none
                      : usd(siteKeyEntry.budget_usd)}
                  </td>
                  <td className="py-2.5 pr-3">{stateText(siteKeyEntry)}</td>
                  <td className="py-2.5 text-xs text-[var(--muted)]">—</td>
                </tr>
              )}
            </tbody>
          </table>
          {extraCount < SLOT_LETTERS.length && (
            <div className="mt-3">
              <button
                type="button"
                data-testid="gemini-slot-add"
                disabled={!canManage}
                onClick={() => setExtraCount((c) => Math.min(SLOT_LETTERS.length, c + 1))}
                className="inline-flex items-center gap-1.5 rounded-xl border border-[var(--line)] bg-white px-3 py-2 text-xs font-semibold text-[var(--ink)] hover:border-[var(--teal)] disabled:opacity-40"
              >
                <Plus size={14} />
                {copy.addSlot} ({SLOT_LETTERS[extraCount]})
              </button>
            </div>
          )}
        </div>
      )}
    </section>
  );
}
