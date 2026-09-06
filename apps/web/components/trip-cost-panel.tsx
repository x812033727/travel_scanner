"use client";

import { AlertTriangle, CircleDollarSign, Loader2, Plus, Sparkles, Trash2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import { currencies, currencyName, type Currency } from "@/lib/currency";
import { formatMoney } from "@/lib/locale-format";
import type { Trip, TripCost, TripExpenseCategory } from "@/lib/trip-types";

const categories: TripExpenseCategory[] = [
  "food",
  "transport",
  "lodging",
  "flight",
  "activity",
  "shopping",
  "other",
];

const field =
  "min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 text-sm text-[var(--ink)] outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]";

export function TripCostPanel({
  trip,
  days,
  activeDay,
  onSaveBudget,
  onSaveCurrency,
  onAdd,
  onDelete,
  onSeed,
}: {
  trip: Trip;
  days: string[];
  activeDay: string;
  onSaveBudget: (amount: string | null) => Promise<void>;
  onSaveCurrency: (currency: Currency) => Promise<void>;
  onAdd: (entry: { day_date: string; label: string; amount: string; category: TripExpenseCategory }) => Promise<void>;
  onDelete: (id: string, label: string) => Promise<void>;
  onSeed: () => Promise<number>;
}) {
  const t = useTranslations("trips");
  const cost: TripCost = trip.cost ?? {
    currency: "TWD",
    budget: null,
    total: "0",
    difference: null,
    by_day: {},
    by_category: {},
    items: [],
  };
  const currency = cost.currency;
  const [budget, setBudget] = useState(cost.budget ?? "");
  const [label, setLabel] = useState("");
  const [amount, setAmount] = useState("");
  const [day, setDay] = useState(activeDay || days[0] || "");
  const [category, setCategory] = useState<TripExpenseCategory>("food");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const [seeded, setSeeded] = useState<number>();

  // Once a real number is in the ledger the currency is frozen: nothing here
  // can restate 980 JPY as TWD, so relabelling it would be a lie.
  const locked = cost.items.length > 0;
  const difference = cost.difference === null ? null : Number(cost.difference);
  const money = (value: string | number) => formatMoney(Number(value), currency);

  async function run(action: () => Promise<void>) {
    setBusy(true);
    setError(false);
    try {
      await action();
    } catch {
      setError(true);
    } finally {
      setBusy(false);
    }
  }

  return (
    <div className="grid gap-4">
      <div className="grid gap-3 sm:grid-cols-2">
        <label className="text-sm font-semibold">
          {t("budgetLabel")}
          <input
            type="number"
            min="0"
            step="1"
            inputMode="decimal"
            value={budget}
            placeholder={t("budgetPlaceholder")}
            onChange={(event) => setBudget(event.target.value)}
            onBlur={() => {
              const next = budget.trim();
              if (next === (cost.budget ?? "")) return;
              void run(() => onSaveBudget(next || null));
            }}
            className={`mt-1.5 ${field}`}
          />
        </label>
        <label className="text-sm font-semibold">
          {t("currencyLabel")}
          <select
            aria-label={t("currencyLabel")}
            value={currency}
            disabled={locked}
            onChange={(event) => void run(() => onSaveCurrency(event.target.value as Currency))}
            className={`mt-1.5 ${field} disabled:opacity-60`}
          >
            {currencies.map((value) => (
              <option key={value} value={value}>{value} · {currencyName(value)}</option>
            ))}
          </select>
          {locked && <span className="mt-1 block text-xs font-normal text-[var(--muted)]">{t("currencyLocked")}</span>}
        </label>
      </div>

      <div className="rounded-2xl bg-[var(--paper)] p-3.5">
        <p className="flex flex-wrap items-baseline justify-between gap-2">
          <span className="text-sm font-semibold text-[var(--muted)]">{t("costTotal")}</span>
          <strong className="text-xl tabular-nums">{money(cost.total)}</strong>
        </p>
        {difference !== null && (
          <p className={`mt-2 flex items-center gap-2 text-sm font-semibold ${difference >= 0 ? "text-[var(--teal-dark)]" : "text-red-700"}`}>
            {difference >= 0 ? <CircleDollarSign size={16} /> : <AlertTriangle size={16} />}
            {difference >= 0
              ? t("costRemaining", { amount: money(difference) })
              : t("costOver", { amount: money(Math.abs(difference)) })}
          </p>
        )}
        {Object.keys(cost.by_category).length > 0 && (
          <dl className="mt-3 grid gap-1.5 border-t border-[var(--line)] pt-2.5 text-xs">
            {Object.entries(cost.by_category).map(([key, value]) => (
              <div key={key} className="flex justify-between gap-3">
                <dt>{t(`costCategories.${key}`)}</dt>
                <dd className="font-semibold tabular-nums">{money(value)}</dd>
              </div>
            ))}
          </dl>
        )}
      </div>

      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          disabled={busy}
          onClick={() => void run(async () => setSeeded(await onSeed()))}
          className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] bg-white px-4 text-sm font-semibold disabled:opacity-50"
        >
          {busy ? <Loader2 size={16} className="animate-spin" /> : <Sparkles size={16} />}
          {t("costSeed")}
        </button>
        {seeded !== undefined && (
          <span aria-live="polite" className="text-xs text-[var(--muted)]">
            {seeded > 0 ? t("costSeeded", { count: seeded }) : t("costSeedNone")}
          </span>
        )}
      </div>

      {cost.items.length === 0 ? (
        <p className="app-empty-state text-sm">{t("costEmpty")}</p>
      ) : (
        <ul className="grid gap-2">
          {cost.items.map((item) => (
            <li key={item.id} className="flex items-center gap-3 rounded-xl border border-[var(--line)] bg-white px-3 py-2.5">
              <span className="min-w-0 flex-1">
                <strong className="block truncate text-sm">{item.label}</strong>
                <span className="text-xs text-[var(--muted)]">
                  {item.day_date} · {t(`costCategories.${item.category}`)}
                </span>
              </span>
              <span className="shrink-0 text-sm font-semibold tabular-nums">{money(item.amount)}</span>
              <button
                type="button"
                aria-label={t("costDelete", { label: item.label })}
                disabled={busy}
                onClick={() => void run(() => onDelete(item.id, item.label))}
                className="grid h-11 w-11 shrink-0 place-items-center rounded-xl text-[var(--muted)] hover:bg-red-50 hover:text-red-700 disabled:opacity-50"
              >
                <Trash2 size={16} />
              </button>
            </li>
          ))}
        </ul>
      )}

      <form
        className="grid gap-2 rounded-2xl border border-dashed border-[var(--line)] p-3"
        onSubmit={(event) => {
          event.preventDefault();
          if (!label.trim() || !amount.trim() || !day) return;
          void run(async () => {
            await onAdd({ day_date: day, label: label.trim(), amount: amount.trim(), category });
            setLabel("");
            setAmount("");
          });
        }}
      >
        <div className="grid gap-2 sm:grid-cols-2">
          <label className="text-xs font-semibold">
            {t("costAddLabel")}
            <input value={label} maxLength={120} onChange={(event) => setLabel(event.target.value)} className={`mt-1 ${field}`} />
          </label>
          <label className="text-xs font-semibold">
            {t("costAddAmount")}
            <input type="number" min="0" step="0.01" inputMode="decimal" value={amount} onChange={(event) => setAmount(event.target.value)} className={`mt-1 ${field}`} />
          </label>
          <label className="text-xs font-semibold">
            {t("costAddDay")}
            <select value={day} onChange={(event) => setDay(event.target.value)} className={`mt-1 ${field}`}>
              {days.map((value) => <option key={value} value={value}>{value}</option>)}
            </select>
          </label>
          <label className="text-xs font-semibold">
            {t("costAddCategory")}
            <select value={category} onChange={(event) => setCategory(event.target.value as TripExpenseCategory)} className={`mt-1 ${field}`}>
              {categories.map((value) => <option key={value} value={value}>{t(`costCategories.${value}`)}</option>)}
            </select>
          </label>
        </div>
        <button
          type="submit"
          disabled={busy || !label.trim() || !amount.trim() || !day}
          className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white disabled:opacity-45"
        >
          {busy ? <Loader2 size={16} className="animate-spin" /> : <Plus size={16} />}
          {t("costAdd")}
        </button>
      </form>

      {error && <p role="alert" className="text-sm font-semibold text-red-700">{t("costFailed")}</p>}
    </div>
  );
}
