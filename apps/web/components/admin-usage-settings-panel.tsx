"use client";

import { Archive, BadgePlus, Check, Loader2, Pencil, RotateCcw } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { usageOperations, type UsageOperation } from "@/lib/usage-catalog";

const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
type Locale = (typeof locales)[number];
type Tab = "trial" | "packages" | "costs" | "audit";

type UsagePackage = {
  id: string;
  code: string;
  localized_names: Record<Locale, string>;
  uses: number;
  price_twd: number;
  display_order: number;
  is_active: boolean;
  is_featured: boolean;
};

type Snapshot = {
  trial_uses: number;
  packages: UsagePackage[];
  operation_costs: Array<{ operation: UsageOperation; uses: number; source: "default" | "database" }>;
  audit: Array<{
    id: string;
    actor_user_id: string | null;
    action: string;
    target: string;
    metadata: Record<string, unknown>;
    created_at: string;
  }>;
};

type PackageDraft = Omit<UsagePackage, "id" | "code">;

function emptyPackage(): PackageDraft {
  return {
    localized_names: { "zh-TW": "", "zh-CN": "", en: "", ja: "", ko: "" },
    uses: 10,
    price_twd: 0,
    display_order: 100,
    is_active: true,
    is_featured: false,
  };
}

export function AdminUsageSettingsPanel() {
  const t = useTranslations("admin.usage");
  const locale = useLocale();
  const [snapshot, setSnapshot] = useState<Snapshot>();
  const [tab, setTab] = useState<Tab>("trial");
  const [trialUses, setTrialUses] = useState(3);
  const [costs, setCosts] = useState<Record<string, number>>({});
  const [editing, setEditing] = useState<UsagePackage | "new" | null>(null);
  const [draft, setDraft] = useState<PackageDraft>(emptyPackage());
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");

  function applySnapshot(value: Snapshot) {
    setSnapshot(value);
    setTrialUses(value.trial_uses);
    setCosts(Object.fromEntries(value.operation_costs.map((item) => [item.operation, item.uses])));
  }

  useEffect(() => {
    api<Snapshot>("/admin/usage-settings")
      .then(applySnapshot)
      .catch((reason: Error) => setError(reason.message));
  }, []);

  const tabs = useMemo<Array<{ key: Tab; label: string }>>(() => [
    { key: "trial", label: t("tabs.trial") },
    { key: "packages", label: t("tabs.packages") },
    { key: "costs", label: t("tabs.costs") },
    { key: "audit", label: t("tabs.audit") },
  ], [t]);

  async function saveTrial() {
    setBusy(true); setError(""); setNotice("");
    try {
      applySnapshot(await api<Snapshot>("/admin/usage-settings/trial", {
        method: "PUT",
        body: JSON.stringify({ uses: trialUses }),
      }));
      setNotice(t("trial.saved"));
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  async function saveCosts() {
    setBusy(true); setError(""); setNotice("");
    try {
      applySnapshot(await api<Snapshot>("/admin/usage-settings/operation-costs", {
        method: "PUT",
        body: JSON.stringify({ costs }),
      }));
      setNotice(t("costs.saved"));
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  function beginEdit(item: UsagePackage | "new") {
    setEditing(item);
    setDraft(item === "new" ? emptyPackage() : {
      localized_names: { ...item.localized_names },
      uses: item.uses,
      price_twd: item.price_twd,
      display_order: item.display_order,
      is_active: item.is_active,
      is_featured: item.is_featured,
    });
  }

  async function savePackage() {
    setBusy(true); setError(""); setNotice("");
    try {
      const path = editing === "new" ? "/admin/usage-settings/packages" : `/admin/usage-settings/packages/${editing?.id}`;
      applySnapshot(await api<Snapshot>(path, {
        method: editing === "new" ? "POST" : "PUT",
        body: JSON.stringify(draft),
      }));
      setEditing(null);
      setNotice(t("packages.saved"));
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  async function togglePackage(item: UsagePackage) {
    if (item.is_active && !window.confirm(t("packages.archiveConfirm", { name: item.localized_names["zh-TW"] }))) return;
    setBusy(true); setError(""); setNotice("");
    try {
      applySnapshot(await api<Snapshot>(`/admin/usage-settings/packages/${item.id}`, {
        method: "PUT",
        body: JSON.stringify({
          localized_names: item.localized_names,
          uses: item.uses,
          price_twd: item.price_twd,
          display_order: item.display_order,
          is_active: !item.is_active,
          is_featured: item.is_active ? false : item.is_featured,
        }),
      }));
      setNotice(item.is_active ? t("packages.archived") : t("packages.restored"));
    } catch (reason) { setError((reason as Error).message); }
    finally { setBusy(false); }
  }

  if (!snapshot) return <div className={`mt-6 flex items-center gap-2 rounded-2xl border p-6 text-sm ${error ? "border-red-200 bg-red-50 text-red-800" : "border-[var(--line)] bg-white text-[var(--muted)]"}`} role={error ? "alert" : "status"}>{error || <><Loader2 className="animate-spin" size={18} />{t("loading")}</>}</div>;

  return <section className="mt-6">
    <div className="hidden gap-2 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white p-2 sm:flex" role="tablist" aria-label={t("tabs.label")}>
      {tabs.map((item) => <button key={item.key} role="tab" aria-selected={tab === item.key} onClick={() => setTab(item.key)} className={`min-h-11 shrink-0 rounded-xl px-4 text-sm font-semibold ${tab === item.key ? "bg-[var(--ink)] text-white" : "hover:bg-[var(--paper)]"}`}>{item.label}</button>)}
    </div>
    <label className="block sm:hidden"><span className="mb-2 block text-sm font-semibold">{t("tabs.mobileLabel")}</span><select value={tab} onChange={(event) => setTab(event.target.value as Tab)} className="min-h-12 w-full rounded-xl border border-[var(--line)] bg-white px-3">{tabs.map((item) => <option key={item.key} value={item.key}>{item.label}</option>)}</select></label>
    {(error || notice) && <div className={`mt-4 rounded-xl px-4 py-3 text-sm ${error ? "bg-red-50 text-red-800" : "bg-emerald-50 text-emerald-800"}`} role={error ? "alert" : "status"}>{error || notice}</div>}

    {tab === "trial" && <div className="mt-5 max-w-2xl rounded-2xl border border-[var(--line)] bg-white p-6"><h2 className="text-xl font-bold">{t("trial.title")}</h2><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("trial.help")}</p><label className="mt-5 block text-sm font-semibold">{t("trial.uses")}<input type="number" min={1} max={10000} value={trialUses} onChange={(event) => setTrialUses(Number(event.target.value))} className="mt-2 min-h-12 w-full rounded-xl border border-[var(--line)] px-3" /></label><button type="button" disabled={busy || trialUses < 1 || trialUses > 10000} onClick={() => void saveTrial()} className="mt-5 flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-5 font-semibold text-white disabled:opacity-45">{busy && <Loader2 size={17} className="animate-spin" />}{t("save")}</button></div>}

    {tab === "packages" && <div className="mt-5 space-y-5"><div className="flex items-center justify-between gap-3"><div><h2 className="text-xl font-bold">{t("packages.title")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("packages.help")}</p></div><button type="button" onClick={() => beginEdit("new")} className="flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white"><BadgePlus size={17} />{t("packages.add")}</button></div>
      {editing && <div className="rounded-2xl border border-[var(--teal)] bg-white p-6"><h3 className="text-lg font-bold">{editing === "new" ? t("packages.createTitle") : t("packages.editTitle")}</h3><div className="mt-4 grid gap-4 md:grid-cols-2">{locales.map((nameLocale) => <label key={nameLocale} className="text-sm font-semibold">{t(`locales.${nameLocale}`)}<input value={draft.localized_names[nameLocale]} maxLength={100} onChange={(event) => setDraft((current) => ({ ...current, localized_names: { ...current.localized_names, [nameLocale]: event.target.value } }))} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3" /></label>)}<label className="text-sm font-semibold">{t("packages.uses")}<input type="number" min={1} max={100000} value={draft.uses} onChange={(event) => setDraft((current) => ({ ...current, uses: Number(event.target.value) }))} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3" /></label><label className="text-sm font-semibold">{t("packages.price")}<input type="number" min={0} max={10000000} value={draft.price_twd} onChange={(event) => setDraft((current) => ({ ...current, price_twd: Number(event.target.value) }))} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3" /></label><label className="text-sm font-semibold">{t("packages.order")}<input type="number" min={0} max={10000} value={draft.display_order} onChange={(event) => setDraft((current) => ({ ...current, display_order: Number(event.target.value) }))} className="mt-2 min-h-11 w-full rounded-xl border border-[var(--line)] px-3" /></label><div className="flex flex-wrap items-end gap-4"><label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={draft.is_active} onChange={(event) => setDraft((current) => ({ ...current, is_active: event.target.checked, is_featured: event.target.checked ? current.is_featured : false }))} />{t("packages.active")}</label><label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={draft.is_featured} disabled={!draft.is_active} onChange={(event) => setDraft((current) => ({ ...current, is_featured: event.target.checked }))} />{t("packages.featured")}</label></div></div><div className="mt-5 flex gap-3"><button type="button" onClick={() => setEditing(null)} className="min-h-11 rounded-xl border border-[var(--line)] px-5 font-semibold">{t("cancel")}</button><button type="button" onClick={() => void savePackage()} disabled={busy || locales.some((nameLocale) => !draft.localized_names[nameLocale].trim())} className="flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-5 font-semibold text-white disabled:opacity-45">{busy && <Loader2 size={17} className="animate-spin" />}{t("save")}</button></div></div>}
      <div className="overflow-x-auto rounded-2xl border border-[var(--line)] bg-white"><table className="min-w-full text-left text-sm"><thead className="bg-[var(--paper)] text-[var(--muted)]"><tr><th className="px-4 py-3">{t("packages.name")}</th><th className="px-4 py-3">{t("packages.uses")}</th><th className="px-4 py-3">{t("packages.price")}</th><th className="px-4 py-3">{t("packages.order")}</th><th className="px-4 py-3">{t("packages.status")}</th><th className="px-4 py-3">{t("packages.actions")}</th></tr></thead><tbody>{snapshot.packages.map((item) => <tr key={item.id} className="border-t border-[var(--line)]"><td className="px-4 py-3"><strong>{item.localized_names[(locale as Locale)] || item.localized_names["zh-TW"]}</strong><span className="mt-1 block text-xs text-[var(--muted)]">{item.code}{item.is_featured ? ` · ${t("packages.featured")}` : ""}</span></td><td className="px-4 py-3">{item.uses}</td><td className="px-4 py-3">NT${item.price_twd.toLocaleString()}</td><td className="px-4 py-3">{item.display_order}</td><td className="px-4 py-3">{item.is_active ? t("packages.enabled") : t("packages.archivedStatus")}</td><td className="px-4 py-3"><div className="flex gap-2"><button type="button" aria-label={t("packages.editNamed", { name: item.localized_names["zh-TW"] })} onClick={() => beginEdit(item)} className="grid min-h-10 min-w-10 place-items-center rounded-lg border border-[var(--line)]"><Pencil size={16} /></button><button type="button" aria-label={item.is_active ? t("packages.archiveNamed", { name: item.localized_names["zh-TW"] }) : t("packages.restoreNamed", { name: item.localized_names["zh-TW"] })} disabled={busy} onClick={() => void togglePackage(item)} className="grid min-h-10 min-w-10 place-items-center rounded-lg border border-[var(--line)]">{item.is_active ? <Archive size={16} /> : <RotateCcw size={16} />}</button></div></td></tr>)}</tbody></table></div></div>}

    {tab === "costs" && <div className="mt-5"><h2 className="text-xl font-bold">{t("costs.title")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("costs.help")}</p><div className="mt-5 grid gap-4 md:grid-cols-2 xl:grid-cols-3">{usageOperations.map((operation) => <label key={operation} className="rounded-2xl border border-[var(--line)] bg-white p-5"><span className="font-semibold">{t(`operations.${operation}.label`)}</span><span className="mt-1 block min-h-10 text-xs leading-5 text-[var(--muted)]">{t(`operations.${operation}.help`)}</span><span className="mt-4 flex items-center gap-2"><input aria-label={t(`operations.${operation}.label`)} type="number" min={0} max={100} value={costs[operation] ?? 1} onChange={(event) => setCosts((current) => ({ ...current, [operation]: Number(event.target.value) }))} className="min-h-11 w-28 rounded-xl border border-[var(--line)] px-3" /><span className="text-sm">{t("costs.unit")}</span></span></label>)}</div><button type="button" disabled={busy || usageOperations.some((operation) => !Number.isInteger(costs[operation]) || costs[operation] < 0 || costs[operation] > 100)} onClick={() => void saveCosts()} className="mt-5 flex min-h-12 items-center gap-2 rounded-xl bg-[var(--teal)] px-5 font-semibold text-white disabled:opacity-45">{busy ? <Loader2 size={17} className="animate-spin" /> : <Check size={17} />}{t("costs.save")}</button></div>}

    {tab === "audit" && <div className="mt-5"><h2 className="text-xl font-bold">{t("audit.title")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("audit.help")}</p><div className="mt-5 space-y-3">{snapshot.audit.length ? snapshot.audit.map((item) => <article key={item.id} className="rounded-2xl border border-[var(--line)] bg-white p-5"><div className="flex flex-wrap items-center justify-between gap-2"><strong>{t(`auditActions.${item.action}`)}</strong><time className="text-xs text-[var(--muted)]">{new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }).format(new Date(item.created_at))}</time></div><p className="mt-2 text-sm text-[var(--muted)]">{item.target}</p><pre className="mt-3 overflow-x-auto rounded-xl bg-[var(--paper)] p-3 text-xs">{JSON.stringify(item.metadata, null, 2)}</pre></article>) : <p className="rounded-2xl border border-[var(--line)] bg-white p-6 text-sm text-[var(--muted)]">{t("audit.empty")}</p>}</div></div>}
  </section>;
}
