"use client";

import { useTranslations } from "next-intl";
import { type FormEvent, useCallback, useState } from "react";
import { AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { control, SLUG, useRefresh, useWhen } from "@/components/admin-video-review-card";
import { type Budget, type Cost, COST_CATEGORIES, type CostCategory, type Costs, dollars, message, type PeriodTotal } from "@/components/admin-video-shorts-data";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";

// The ledger of the Shorts tab (docs/videos/SHORTS.md, the section on spending): where the
// thirty days stand against the owner's limits, the three periods of the run, every line, and a
// form for what the site cannot see by itself (a subscription, a tool's fee). An amount nobody
// knows is entered as unknown, never as zero: it stops paid work until someone fills it in.
const statusTone: Record<Cost["status"], string> = { confirmed: "ok", reserved: "queued", unknown: "failed" };
const amountOf = (value: string) => (/^\d+(?:\.\d{1,4})?$/.test(value.trim()) ? value.trim() : null);

function BudgetSummary({ budget }: { budget: Budget }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  return <section aria-label={t("costs.budgetTitle")} className="grid gap-2 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4 text-sm leading-6">
    <h3 className="flex flex-wrap items-center gap-2 font-bold">{t("costs.budgetTitle")}
      <AdminStatusPill status={budget.paid_work_allowed ? "ok" : "failed"}>{budget.paid_work_allowed ? t("costs.allowed") : t("costs.stopped")}</AdminStatusPill>
    </h3>
    {budget.reason && <p className="text-red-800">{budget.reason}</p>}
    <p className="text-[var(--muted)]">{t("costs.period", { start: when(budget.period_start), end: when(budget.period_end) })}</p>
    <dl className="grid gap-1 md:grid-cols-2">
      <div><dt className="inline font-semibold">{t("costs.spent")}</dt><dd className="inline"> · NT${dollars(budget.spent_ntd)}</dd></div>
      <div><dt className="inline font-semibold">{t("costs.reserved")}</dt><dd className="inline"> · NT${dollars(budget.reserved_ntd)}</dd></div>
      <div><dt className="inline font-semibold">{t("costs.soft")}</dt><dd className="inline"> · NT${dollars(budget.soft_ntd)}</dd></div>
      <div><dt className="inline font-semibold">{t("costs.limit")}</dt><dd className="inline"> · NT${dollars(budget.limit_ntd)}</dd></div>
      <div><dt className="inline font-semibold">{t("costs.total")}</dt><dd className="inline"> · NT${dollars(budget.total_spent_ntd)}／NT${dollars(budget.total_limit_ntd)}</dd></div>
      <div><dt className="inline font-semibold">{t("costs.unknown")}</dt><dd className="inline"> · {budget.unknown}</dd></div>
    </dl>
  </section>;
}

function Periods({ periods }: { periods: PeriodTotal[] }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  if (periods.length === 0) return null;
  return <section aria-label={t("costs.periodsTitle")} className="grid gap-2">
    <h3 className="font-bold">{t("costs.periodsTitle")}</h3>
    <ul className="grid gap-3 md:grid-cols-3">{periods.map((period) => <li key={period.start} className="grid gap-1 rounded-2xl border border-[var(--line)] p-4 text-sm leading-6">
      <span className="text-[var(--muted)]">{t("costs.period", { start: when(period.start), end: when(period.end) })}</span>
      <span className="font-semibold">{t("costs.spent")} · NT${dollars(period.spent_ntd)}</span>
      <span>{t("costs.reserved")} · NT${dollars(period.reserved_ntd)}</span>
      <span className="flex flex-wrap items-center gap-2">{t("costs.periodLines", { count: period.lines })}
        {period.unknown > 0 && <AdminStatusPill status="failed">{t("costs.periodUnknown", { count: period.unknown })}</AdminStatusPill>}
      </span>
    </li>)}</ul>
  </section>;
}

/** A line the owner enters; an unknown one carries no amount. */
function AddCost({ onAdded }: { onAdded: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const [category, setCategory] = useState<CostCategory>("subscription");
  const [known, setKnown] = useState(true);
  const [amount, setAmount] = useState("");
  const [currency, setCurrency] = useState("TWD");
  const [rate, setRate] = useState("");
  const [slug, setSlug] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const currencyOk = /^[A-Z]{3}$/.test(currency);
  const rateOk = !rate.trim() || (amountOf(rate) !== null && Number(rate) > 0);
  const slugOk = !slug.trim() || SLUG.test(slug.trim());
  const ready = currencyOk && rateOk && slugOk && (!known || amountOf(amount) !== null);
  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!ready) return;
    setBusy(true);
    setError("");
    try {
      await api("/admin/video-shorts/costs", {
        method: "POST",
        body: JSON.stringify({
          category, status: known ? "confirmed" : "unknown", amount: known ? amountOf(amount) : undefined, currency,
          fx_rate: rate.trim() ? rate.trim() : undefined, project_slug: slug.trim() || undefined, note: note.trim() || undefined,
        }),
      });
      setAmount("");
      setNote("");
      setSlug("");
      onAdded();
    } catch (problem) {
      setError(t("costs.addError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <form onSubmit={(event) => void submit(event)} aria-label={t("costs.addTitle")} className="grid gap-3 rounded-2xl border border-[var(--line)] p-4 text-sm">
    <h3 className="text-base font-bold">{t("costs.addTitle")}</h3>
    <p className="leading-6 text-[var(--muted)]">{t("costs.addHelp")}</p>
    <div className="grid gap-3 md:grid-cols-3">
      <label className="grid gap-1 font-semibold">{t("costs.fields.category")}
        <select className={control} value={category} disabled={busy} onChange={(event) => setCategory(event.target.value as CostCategory)}>{COST_CATEGORIES.map((each) => <option key={each} value={each}>{t(`costs.categories.${each}`)}</option>)}</select>
      </label>
      <label className="grid gap-1 font-semibold">{t("costs.fields.amount")}
        <input className={control} inputMode="decimal" value={amount} disabled={busy || !known} aria-invalid={known && Boolean(amount) && amountOf(amount) === null} onChange={(event) => setAmount(event.target.value)} />
      </label>
      <label className="grid gap-1 font-semibold">{t("costs.fields.currency")}
        <input className={control} value={currency} maxLength={3} disabled={busy} aria-invalid={!currencyOk} onChange={(event) => setCurrency(event.target.value.toUpperCase())} />
      </label>
    </div>
    <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={!known} disabled={busy} onChange={(event) => setKnown(!event.target.checked)} />{t("costs.fields.unknown")}</label>
    <div className="grid gap-3 md:grid-cols-2">
      <label className="grid gap-1 font-semibold">{t("costs.fields.fxRate")}
        <input className={control} inputMode="decimal" value={rate} disabled={busy} aria-invalid={!rateOk} placeholder={t("costs.fields.fxRateHelp")} onChange={(event) => setRate(event.target.value)} />
      </label>
      <label className="grid gap-1 font-semibold">{t("costs.fields.projectSlug")}
        <input className={control} value={slug} disabled={busy} aria-invalid={!slugOk} onChange={(event) => setSlug(event.target.value)} />
      </label>
    </div>
    <label className="grid gap-1 font-semibold">{t("costs.fields.note")}
      <input className={control} value={note} maxLength={500} disabled={busy} onChange={(event) => setNote(event.target.value)} />
    </label>
    {error && <p role="alert" className="text-red-800">{error}</p>}
    <div><Button type="submit" disabled={busy || !ready}>{busy ? t("saving") : t("costs.add")}</Button></div>
  </form>;
}

/** A line of the ledger. An unknown one takes its amount here; one the owner entered can be removed. */
function CostRow({ cost, canManage, onChanged }: { cost: Cost; canManage: boolean; onChanged: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const [amount, setAmount] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const send = async (init: RequestInit, confirmText?: string) => {
    if (confirmText && !window.confirm(confirmText)) return;
    setBusy(true);
    setError("");
    try {
      await api(`/admin/video-shorts/costs/${cost.id}`, init);
      onChanged();
    } catch (problem) {
      setError(t("costs.changeError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const category = t.has(`costs.categories.${cost.category}`) ? t(`costs.categories.${cost.category}`) : cost.category;
  return <tr className="border-t border-[var(--line)] align-top">
    <td className="py-2 pr-3">{when(cost.occurred_at)}</td>
    <td className="py-2 pr-3">{category}{cost.project_slug && <span className="block font-mono text-xs text-[var(--muted)]">{cost.project_slug}</span>}</td>
    <td className="py-2 pr-3 font-mono">{cost.amount === null ? "—" : `${cost.amount} ${cost.currency}`}{cost.fx_rate !== null && cost.currency !== "TWD" && <span className="block text-xs text-[var(--muted)]">{t("costs.rate", { rate: cost.fx_rate })}</span>}</td>
    <td className="py-2 pr-3 font-mono">{cost.amount_ntd === null ? "—" : `NT$${dollars(cost.amount_ntd)}`}</td>
    <td className="py-2 pr-3"><span className="flex flex-wrap gap-1"><AdminStatusPill status={statusTone[cost.status]}>{t(`costs.statuses.${cost.status}`)}</AdminStatusPill><AdminStatusPill status="inactive">{t(`costs.sources.${cost.source}`)}</AdminStatusPill></span></td>
    <td className="py-2">
      {cost.note && <span className="block leading-6">{cost.note}</span>}
      {canManage && cost.status === "unknown" && <span className="mt-1 flex flex-wrap items-end gap-2">
        <label className="grid gap-1 text-xs font-semibold">{t("costs.fill", { currency: cost.currency })}<input className={control} inputMode="decimal" value={amount} disabled={busy} onChange={(event) => setAmount(event.target.value)} /></label>
        <Button secondary disabled={busy || amountOf(amount) === null} onClick={() => void send({ method: "PATCH", body: JSON.stringify({ status: "confirmed", amount: amountOf(amount) }) })}>{t("costs.fillButton")}</Button>
      </span>}
      {canManage && cost.source === "manual" && <span className="mt-1 block"><Button secondary disabled={busy} onClick={() => void send({ method: "DELETE" }, t("costs.deleteConfirm"))}>{t("costs.delete")}</Button></span>}
      {error && <span role="alert" className="block text-red-800">{error}</span>}
    </td>
  </tr>;
}

export function ShortsCosts({ canManage, onChanged }: { canManage: boolean; onChanged: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const [costs, setCosts] = useState<Costs | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<Costs>("/admin/video-shorts/costs").then((value) => { setCosts(value); setError(""); }).catch((problem: unknown) => setError(message(problem)));
  }, []);
  useRefresh(load);
  const changed = () => { load(); onChanged(); };
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!costs) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  return <section aria-label={t("views.costs")} className="grid gap-5">
    <BudgetSummary budget={costs.budget} />
    <Periods periods={costs.periods} />
    {canManage && <AddCost onAdded={changed} />}
    <section aria-label={t("costs.itemsTitle")} className="grid gap-2">
      <h3 className="font-bold">{t("costs.itemsTitle")}</h3>
      {costs.items.length === 0 ? <p className="text-sm text-[var(--muted)]">{t("costs.empty")}</p> : <div className="overflow-x-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
        <table className="w-full min-w-[48rem] text-left text-sm" aria-label={t("costs.itemsTitle")}>
          <thead><tr className="text-xs text-[var(--muted)]">{(["when", "category", "amount", "ntd", "status", "note"] as const).map((column) => <th key={column} scope="col" className="py-1 pr-3 font-semibold">{t(`costs.columns.${column}`)}</th>)}</tr></thead>
          <tbody>{costs.items.map((cost) => <CostRow key={cost.id} cost={cost} canManage={canManage} onChanged={changed} />)}</tbody>
        </table>
      </div>}
    </section>
  </section>;
}
