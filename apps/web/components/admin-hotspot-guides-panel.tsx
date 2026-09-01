"use client";

import { ExternalLink, Languages, RefreshCw } from "lucide-react";
import { useTranslations } from "next-intl";
import { FormEvent, useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";

const locales = ["en", "ja", "ko", "zh-TW", "zh-CN"] as const;
type GuideCandidate = {
  id: string; hotspot_id: string; hotspot_name: string; type: "article" | "video";
  provider: string; locale: string; title: string; creator_name: string; url: string;
  thumbnail_url: string | null; view_count: number | null; language_confidence: number;
  status: string; reason: string | null; last_verified_at: string | null; metadata_expires_at: string | null;
};
type GuideResponse = { items: GuideCandidate[]; total: number; page: number; pages: number };
type CoverageItem = { id: string; name: string; complete: boolean; coverage: Record<string, { article: number; video: number }> };
type CoverageResponse = {
  items: CoverageItem[]; total: number; complete: number;
  quotas: { youtube: { used: number; automatic_limit: number; manual_limit: number }; brave: { used: number; limit: number } };
};

export function AdminHotspotGuidesPanel() {
  const t = useTranslations("hotspotAdmin");
  const [data, setData] = useState<GuideResponse | null>(null);
  const [coverage, setCoverage] = useState<CoverageResponse | null>(null);
  const [status, setStatus] = useState("pending");
  const [locale, setLocale] = useState("");
  const [type, setType] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [manual, setManual] = useState({ hotspot_id: "", locale: "zh-TW", content_type: "article", url: "", title: "", creator_name: "" });

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams({ limit: "50" });
    if (status) params.set("status", status);
    if (locale) params.set("locale", locale);
    if (type) params.set("type", type);
    try {
      const [guides, coverageResult] = await Promise.all([
        api<GuideResponse>(`/admin/hotspots/guides?${params}`),
        api<CoverageResponse>("/admin/hotspots/guides/coverage"),
      ]);
      setData(guides); setCoverage(coverageResult);
      if (coverageResult.items[0]) setManual((current) => current.hotspot_id ? current : ({ ...current, hotspot_id: coverageResult.items[0].id }));
    } catch (error) { setMessage((error as Error).message); }
    finally { setLoading(false); }
  }, [locale, status, type]);

  useEffect(() => {
    const params = new URLSearchParams({ limit: "50" });
    if (status) params.set("status", status);
    if (locale) params.set("locale", locale);
    if (type) params.set("type", type);
    Promise.all([
      api<GuideResponse>(`/admin/hotspots/guides?${params}`),
      api<CoverageResponse>("/admin/hotspots/guides/coverage"),
    ]).then(([guides, coverageResult]) => {
      setData(guides); setCoverage(coverageResult); setLoading(false);
      if (coverageResult.items[0]) setManual((current) => current.hotspot_id ? current : ({ ...current, hotspot_id: coverageResult.items[0].id }));
    }).catch((error: Error) => { setMessage(error.message); setLoading(false); });
  }, [locale, status, type]);

  async function review(action: "approve" | "reject" | "disable") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/guides/review", { method: "POST", body: JSON.stringify({ ids: [...selected], action, ...(locale ? { locale } : {}) }) });
      setSelected(new Set()); await load();
    } catch (error) { setMessage((error as Error).message); setLoading(false); }
  }

  async function discover(hotspotId: string) {
    setLoading(true);
    try {
      await api("/admin/hotspots/guides/discover", { method: "POST", body: JSON.stringify({ hotspot_ids: [hotspotId], locales }) });
      setMessage(t("discover")); await load();
    } catch (error) { setMessage((error as Error).message); setLoading(false); }
  }

  async function submitManual(event: FormEvent) {
    event.preventDefault(); setLoading(true);
    try {
      await api("/admin/hotspots/guides/manual", { method: "POST", body: JSON.stringify(manual) });
      setManual((current) => ({ ...current, url: "", title: "", creator_name: "" })); await load();
    } catch (error) { setMessage((error as Error).message); setLoading(false); }
  }

  return <section className="mt-10 border-t border-[var(--line)] pt-8">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]"><Languages size={17} />{t("title")}</p><h2 className="mt-2 text-2xl font-bold">{t("coverage")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("coverageSummary", { complete: coverage?.complete || 0, total: coverage?.total || 0 })}</p>{coverage?.quotas && <p className="mt-1 text-xs text-[var(--muted)]">YouTube {coverage.quotas.youtube.used}/{coverage.quotas.youtube.automatic_limit} · Brave {coverage.quotas.brave.used}/{coverage.quotas.brave.limit}</p>}</div><button type="button" onClick={() => void load()} className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] bg-white" aria-label="Refresh"><RefreshCw size={17} /></button></div>
    <div className="mt-4 grid gap-3 md:grid-cols-2 xl:grid-cols-3">{coverage?.items.slice(0, 12).map((item) => <article key={item.id} className="rounded-2xl border border-[var(--line)] bg-white p-4"><div className="flex items-start justify-between gap-3"><h3 className="font-bold">{item.name}</h3><span className={`rounded-full px-2 py-1 text-xs ${item.complete ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-900"}`}>{item.complete ? t("complete") : t("pending")}</span></div><div className="mt-3 grid grid-cols-5 gap-1 text-center text-[10px]">{locales.map((value) => <div key={value} className="rounded-lg bg-[var(--paper)] p-1.5"><strong>{value}</strong><span className="mt-1 block text-[var(--muted)]">{item.coverage[value].article}/{item.coverage[value].video}</span></div>)}</div><button type="button" onClick={() => void discover(item.id)} className="mt-3 w-full rounded-xl border border-[var(--teal)] px-3 py-2 text-xs font-semibold text-[var(--teal)]">{t("discover")}</button></article>)}</div>
    <div className="mt-7 grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-3"><select value={status} onChange={(event) => setStatus(event.target.value)} className="h-11 rounded-xl border px-3"><option value="pending">{t("pending")}</option><option value="approved">{t("approved")}</option><option value="rejected">{t("rejected")}</option><option value="disabled">{t("disabled")}</option><option value="">—</option></select><select value={locale} onChange={(event) => setLocale(event.target.value)} className="h-11 rounded-xl border px-3"><option value="">{t("allLanguages")}</option>{locales.map((value) => <option key={value}>{value}</option>)}</select><select value={type} onChange={(event) => setType(event.target.value)} className="h-11 rounded-xl border px-3"><option value="">{t("allTypes")}</option><option value="article">{t("article")}</option><option value="video">{t("video")}</option></select></div>
    <div className="mt-3 flex flex-wrap items-center gap-2"><span className="mr-auto text-sm text-[var(--muted)]">{t("selected", { count: selected.size })}</span><button disabled={!selected.size || loading} onClick={() => void review("approve")} className="rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-40">{t("approve")}</button><button disabled={!selected.size || loading} onClick={() => void review("reject")} className="rounded-xl border border-[var(--coral)] px-4 py-2 text-sm text-[var(--coral)] disabled:opacity-40">{t("reject")}</button><button disabled={!selected.size || loading} onClick={() => void review("disable")} className="rounded-xl border px-4 py-2 text-sm disabled:opacity-40">{t("disable")}</button></div>
    {message && <p role="status" className="mt-3 text-sm text-[var(--muted)]">{message}</p>}
    <div className="mt-3 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white"><table className="w-full min-w-[900px] text-left text-sm"><tbody>{data?.items.map((item) => <tr key={item.id} className="border-b border-[var(--line)]"><td className="p-3"><input type="checkbox" aria-label={item.title} checked={selected.has(item.id)} onChange={(event) => setSelected((current) => { const next = new Set(current); if (event.target.checked) next.add(item.id); else next.delete(item.id); return next; })} /></td><td className="p-3"><strong>{item.title}</strong><span className="block text-xs text-[var(--muted)]">{item.hotspot_name} · {item.creator_name}</span></td><td className="p-3">{item.locale} · {t(item.type)}</td><td className="p-3">{t("confidence")} {Math.round(item.language_confidence * 100)}%</td><td className="p-3"><a href={item.url} target="_blank" rel="noopener noreferrer" className="text-[var(--teal)]"><ExternalLink size={17} /></a></td></tr>)}</tbody></table>{!loading && !data?.items.length && <p className="p-7 text-center text-[var(--muted)]">{t("empty")}</p>}</div>
    <form onSubmit={submitManual} className="mt-7 grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 md:grid-cols-3"><h3 className="font-bold md:col-span-3">{t("manual")}</h3><select required value={manual.hotspot_id} onChange={(event) => setManual({ ...manual, hotspot_id: event.target.value })} className="h-11 rounded-xl border px-3">{coverage?.items.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select><select value={manual.locale} onChange={(event) => setManual({ ...manual, locale: event.target.value })} className="h-11 rounded-xl border px-3">{locales.map((value) => <option key={value}>{value}</option>)}</select><select value={manual.content_type} onChange={(event) => setManual({ ...manual, content_type: event.target.value })} className="h-11 rounded-xl border px-3"><option value="article">{t("article")}</option><option value="video">{t("video")}</option></select><input required type="url" value={manual.url} onChange={(event) => setManual({ ...manual, url: event.target.value })} placeholder={t("url")} className="h-11 rounded-xl border px-3 md:col-span-3" />{manual.content_type === "article" && <><input required value={manual.title} onChange={(event) => setManual({ ...manual, title: event.target.value })} placeholder={t("contentTitle")} className="h-11 rounded-xl border px-3" /><input required value={manual.creator_name} onChange={(event) => setManual({ ...manual, creator_name: event.target.value })} placeholder={t("creator")} className="h-11 rounded-xl border px-3" /></>}<button disabled={loading} className="h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-40">{t("save")}</button></form>
  </section>;
}
