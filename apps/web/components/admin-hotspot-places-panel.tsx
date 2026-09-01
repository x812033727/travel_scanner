"use client";

import { CheckCircle2, ExternalLink, LoaderCircle, MapPinned, Pencil, Play, RefreshCw, ShieldCheck } from "lucide-react";
import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";

type PlaceItem = {
  hotspot_id: string; name: string; city_name: string; country_code: string;
  google_place_id: string | null; place_id_source: string; match_status: string;
  match_confidence: number | null; candidate: { place_id: string; name: string; address: string | null } | null;
  website_review_status: string; provider_website_url: string | null;
  manual_official_website_url: string | null; address: string | null;
  refresh_after: string | null; expires_at: string | null;
  summary: { google_maps_url: string | null; official_website_url: string | null; status: string };
};
type UsageSku = { sku: string; used: number; free_limit: number; percentage: number };
type Overview = {
  configured: boolean; total: number; ready: number; pending: number; unmatched: number;
  failed: number; expired: number; missing_place_ids: number; usage: { period: string; used: number | null; free_remaining: number | null; available: boolean; sku_usage: UsageSku[] };
};
type ProfilesResponse = { items: PlaceItem[]; total: number; page: number; pages: number; overview: Overview };
type EnrichmentRun = {
  run_id: string; status: "queued" | "running" | "partial" | "completed" | "failed";
  progress: number; counts: { total: number; processed: number; published: number; pending: number; unmatched: number; failed: number };
  usage: { estimated_google_calls: number; actual_google_calls: number };
};
type EditDraft = { hotspotId: string; name: string; googlePlaceId: string; website: string; websiteSource: string };

const statusLabels: Record<string, string> = {
  missing: "尚未擷取", unmatched: "找不到配對", pending: "待人工確認",
  auto_approved: "自動核准", approved: "人工核准", rejected: "已拒絕", failed: "擷取失敗",
};

export function AdminHotspotPlacesPanel() {
  const [data, setData] = useState<ProfilesResponse | null>(null);
  const [status, setStatus] = useState("");
  const [country, setCountry] = useState("");
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [confirmed, setConfirmed] = useState(false);
  const [force, setForce] = useState(false);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");
  const [run, setRun] = useState<EnrichmentRun | null>(null);
  const [edit, setEdit] = useState<EditDraft | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams({ limit: "100", page: String(page) });
    if (status) params.set("status", status);
    if (country) params.set("country_code", country);
    if (query.trim()) params.set("q", query.trim());
    try { setData(await api<ProfilesResponse>(`/admin/hotspots/place-profiles?${params}`)); }
    catch (error) { setMessage((error as Error).message); }
    finally { setLoading(false); }
  }, [country, page, query, status]);

  useEffect(() => { const timer = window.setTimeout(() => void load(), 0); return () => window.clearTimeout(timer); }, [load]);
  useEffect(() => {
    if (!run || !["queued", "running"].includes(run.status)) return;
    const timer = window.setInterval(() => void api<EnrichmentRun>(`/admin/hotspots/place-enrichment/runs/${run.run_id}`).then((next) => {
      setRun(next);
      if (!["queued", "running"].includes(next.status)) void load();
    }).catch((error: Error) => setMessage(error.message)), 1500);
    return () => window.clearInterval(timer);
  }, [load, run]);

  const estimated = useMemo(() => {
    if (!data) return 0;
    return data.overview.total + data.overview.missing_place_ids;
  }, [data]);
  const enterprise = data?.overview.usage.sku_usage.find((item) => item.sku === "place_details_enterprise");
  const locate = data?.overview.usage.sku_usage.find((item) => item.sku === "text_search_pro");

  async function startRun() {
    if (!confirmed) return;
    setLoading(true); setMessage("");
    try {
      const result = await api<EnrichmentRun>("/admin/hotspots/place-enrichment/runs", {
        method: "POST", headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({ scope: country ? "country" : "all", country_code: country || null, mode: force ? "force" : "missing_or_expired", confirm_usage: true }),
      });
      setRun(result); setMessage("已建立 Google 地點資料更新工作");
    } catch (error) { setMessage((error as Error).message); }
    finally { setLoading(false); }
  }

  async function review(action: "approve" | "reject") {
    if (!selected.size) return;
    setLoading(true);
    try {
      const result = await api<{ run: EnrichmentRun | null }>("/admin/hotspots/place-profiles/review", { method: "POST", body: JSON.stringify({ ids: [...selected], action }) });
      if (result.run) setRun(result.run);
      setSelected(new Set()); await load();
    } catch (error) { setMessage((error as Error).message); setLoading(false); }
  }

  async function saveEdit(event: FormEvent) {
    event.preventDefault();
    if (!edit) return;
    setLoading(true);
    try {
      const result = await api<{ run: EnrichmentRun | null }>(`/admin/hotspots/${edit.hotspotId}/place-profile`, {
        method: "PATCH", body: JSON.stringify({ action: "save", google_place_id: edit.googlePlaceId || null, official_website_url: edit.website || null, official_website_source_url: edit.websiteSource || null }),
      });
      if (result.run) setRun(result.run);
      setEdit(null); await load();
    } catch (error) { setMessage((error as Error).message); setLoading(false); }
  }

  async function refresh(item: PlaceItem) {
    setLoading(true);
    try {
      const result = await api<{ run: EnrichmentRun | null }>(`/admin/hotspots/${item.hotspot_id}/place-profile`, { method: "PATCH", body: JSON.stringify({ action: "refresh" }) });
      if (result.run) setRun(result.run);
    } catch (error) { setMessage((error as Error).message); }
    finally { setLoading(false); }
  }

  return <section className="mt-10 border-t border-[var(--line)] pt-8">
    <div className="flex flex-wrap items-end justify-between gap-4"><div><p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]"><MapPinned size={17} />Google 地點資料</p><h2 className="mt-2 text-2xl font-bold">地圖、營業時間與官方網站</h2><p className="mt-1 text-sm text-[var(--muted)]">Place ID 長期保存，其他 Google 欄位最長快取 30 天。</p></div><button type="button" onClick={() => void load()} aria-label="重新整理地點資料" className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] bg-white"><RefreshCw size={17} className={loading ? "animate-spin" : ""} /></button></div>
    <div className="mt-5 grid gap-3 sm:grid-cols-2 lg:grid-cols-6">{[["總景點", data?.overview.total], ["可公開", data?.overview.ready], ["待審", data?.overview.pending], ["未配對", data?.overview.unmatched], ["失敗", data?.overview.failed], ["已過期", data?.overview.expired]].map(([label, value]) => <div key={String(label)} className="rounded-2xl border border-[var(--line)] bg-white p-4"><p className="text-xs text-[var(--muted)]">{label}</p><strong className="mt-1 block text-2xl">{value ?? 0}</strong></div>)}</div>
    <div className="mt-4 rounded-2xl border border-sky-200 bg-sky-50 p-4"><div className="flex flex-wrap items-center gap-3"><ShieldCheck className="text-sky-700" /><div className="mr-auto"><p className="font-bold">本月 Place Details Enterprise {enterprise?.used ?? 0}／{enterprise?.free_limit ?? 0} · Text Search Pro {locate?.used ?? 0}／{locate?.free_limit ?? 0}</p><p className="text-xs text-sky-900">首輪約 {estimated} 次呼叫；實際數量依既有 Place ID 而定。</p></div><span className={`rounded-full px-3 py-1 text-xs font-bold ${data?.overview.configured ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-900"}`}>{data?.overview.configured ? "Google 已設定" : "Google 未設定"}</span></div>
      <div className="mt-4 grid gap-3 md:grid-cols-[1fr_1fr_auto]"><label className="flex min-h-11 items-center gap-3 rounded-xl bg-white px-3 text-sm"><input type="checkbox" checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} /><span>我已確認預估 Google API 用量</span></label><label className="flex min-h-11 items-center gap-3 rounded-xl bg-white px-3 text-sm"><input type="checkbox" checked={force} onChange={(event) => setForce(event.target.checked)} /><span>強制更新尚未過期資料</span></label><button type="button" onClick={() => void startRun()} disabled={!confirmed || !data?.overview.configured || loading} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-5 text-sm font-semibold text-white disabled:opacity-40"><Play size={16} />開始補齊</button></div>
    </div>
    {run && <div className="mt-4 rounded-2xl border border-violet-200 bg-violet-50 p-4" aria-live="polite"><div className="flex items-center justify-between gap-4"><p className="flex items-center gap-2 font-bold">{["queued", "running"].includes(run.status) ? <LoaderCircle size={17} className="animate-spin" /> : <CheckCircle2 size={17} />}更新狀態：{run.status}</p><span>{run.progress}%</span></div><div className="mt-2 h-2 overflow-hidden rounded-full bg-white"><div className="h-full rounded-full bg-violet-600 transition-[width] motion-reduce:transition-none" style={{ width: `${run.progress}%` }} /></div><p className="mt-2 text-xs text-violet-900">完成 {run.counts.processed}/{run.counts.total} · 公開 {run.counts.published} · 待審 {run.counts.pending} · 無配對 {run.counts.unmatched} · 失敗 {run.counts.failed} · Google {run.usage.actual_google_calls}/{run.usage.estimated_google_calls}</p></div>}
    <form onSubmit={(event) => { event.preventDefault(); setPage(1); void load(); }} className="mt-5 grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-[1fr_9rem_11rem_auto]"><input aria-label="搜尋景點" value={query} onChange={(event) => { setQuery(event.target.value); setPage(1); }} placeholder="搜尋景點" className="h-11 rounded-xl border px-3" /><input aria-label="國家代碼" value={country} onChange={(event) => { setCountry(event.target.value.toUpperCase()); setPage(1); }} maxLength={2} placeholder="國家，例如 JP" className="h-11 rounded-xl border px-3" /><select aria-label="配對狀態" value={status} onChange={(event) => { setStatus(event.target.value); setPage(1); }} className="h-11 rounded-xl border px-3"><option value="">全部狀態</option><option value="missing">尚未擷取</option><option value="pending">待審</option><option value="auto_approved">自動核准</option><option value="approved">人工核准</option><option value="unmatched">無配對</option><option value="failed">失敗</option></select><button className="min-h-11 rounded-xl border border-[var(--teal)] px-4 text-sm font-semibold text-[var(--teal)]">套用篩選</button></form>
    <div className="mt-3 flex flex-wrap items-center gap-2"><span className="mr-auto text-sm text-[var(--muted)]">共 {data?.total ?? 0} 筆，已選 {selected.size} 筆</span><button type="button" disabled={!selected.size || loading} onClick={() => void review("approve")} className="min-h-11 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white disabled:opacity-40">核准配對</button><button type="button" disabled={!selected.size || loading} onClick={() => void review("reject")} className="min-h-11 rounded-xl border border-[var(--coral)] px-4 text-sm font-semibold text-[var(--coral)] disabled:opacity-40">拒絕</button></div>
    {message && <p role="status" className="mt-3 rounded-xl bg-[var(--paper)] px-4 py-3 text-sm text-[var(--muted)]">{message}</p>}
    <div className="mt-4 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white"><table className="w-full min-w-[980px] text-left text-sm"><thead className="bg-[var(--paper)]"><tr><th className="p-3">選取</th><th className="p-3">景點</th><th className="p-3">配對</th><th className="p-3">地址／官網</th><th className="p-3">效期</th><th className="p-3">操作</th></tr></thead><tbody>{data?.items.map((item) => <tr key={item.hotspot_id} className="border-t border-[var(--line)] align-top"><td className="p-3"><input type="checkbox" aria-label={`選取 ${item.name}`} checked={selected.has(item.hotspot_id)} onChange={(event) => setSelected((current) => { const next = new Set(current); if (event.target.checked) next.add(item.hotspot_id); else next.delete(item.hotspot_id); return next; })} /></td><td className="p-3 font-semibold">{item.name}<span className="block text-xs font-normal text-[var(--muted)]">{item.city_name} · {item.country_code}</span></td><td className="p-3"><span className="rounded-full bg-[var(--paper)] px-2 py-1 text-xs">{statusLabels[item.match_status] || item.match_status}</span><span className="mt-2 block text-xs text-[var(--muted)]">{item.google_place_id || item.candidate?.place_id || "無 Place ID"}</span>{item.candidate && <span className="mt-1 block text-xs text-amber-800">候選：{item.candidate.name}</span>}</td><td className="max-w-xs p-3 text-xs"><span className="line-clamp-2">{item.address || item.candidate?.address || "—"}</span>{item.summary.official_website_url && <a href={item.summary.official_website_url} target="_blank" rel="noopener noreferrer" className="mt-2 inline-flex items-center gap-1 font-semibold text-[var(--teal)]">官方網站<ExternalLink size={12} /></a>}</td><td className="p-3 text-xs text-[var(--muted)]">{item.expires_at ? new Date(item.expires_at).toLocaleDateString("zh-TW") : "—"}<span className="block">官網：{statusLabels[item.website_review_status] || item.website_review_status}</span></td><td className="p-3"><div className="flex gap-2"><button type="button" onClick={() => setEdit({ hotspotId: item.hotspot_id, name: item.name, googlePlaceId: item.google_place_id || item.candidate?.place_id || "", website: item.manual_official_website_url || item.provider_website_url || "", websiteSource: "" })} className="grid h-11 w-11 place-items-center rounded-xl border" aria-label={`編輯 ${item.name}`}><Pencil size={15} /></button><button type="button" onClick={() => void refresh(item)} disabled={!item.google_place_id || loading} className="grid h-11 w-11 place-items-center rounded-xl border disabled:opacity-40" aria-label={`重新查詢 ${item.name}`}><RefreshCw size={15} /></button></div></td></tr>)}</tbody></table>{!loading && data?.items.length === 0 && <p className="p-8 text-center text-[var(--muted)]">沒有符合條件的地點資料</p>}</div>
    {data && data.pages > 1 && <nav aria-label="Google 地點資料分頁" className="mt-4 flex items-center justify-end gap-3"><button type="button" disabled={page <= 1 || loading} onClick={() => setPage((current) => Math.max(1, current - 1))} className="min-h-11 rounded-xl border px-4 text-sm font-semibold disabled:opacity-40">上一頁</button><span className="text-sm text-[var(--muted)]">第 {page}／{data.pages} 頁</span><button type="button" disabled={page >= data.pages || loading} onClick={() => setPage((current) => Math.min(data.pages, current + 1))} className="min-h-11 rounded-xl border px-4 text-sm font-semibold disabled:opacity-40">下一頁</button></nav>}
    {edit && <form onSubmit={saveEdit} className="mt-4 rounded-2xl border border-[var(--teal)] bg-white p-4"><div className="flex items-center justify-between"><h3 className="font-bold">編輯 {edit.name}</h3><button type="button" onClick={() => setEdit(null)} className="min-h-11 px-3 text-sm">取消</button></div><div className="mt-3 grid gap-3 md:grid-cols-3"><label className="text-sm font-semibold">Google Place ID<input value={edit.googlePlaceId} onChange={(event) => setEdit({ ...edit, googlePlaceId: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3 font-normal" /></label><label className="text-sm font-semibold">官方網站<input type="url" value={edit.website} onChange={(event) => setEdit({ ...edit, website: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3 font-normal" /></label><label className="text-sm font-semibold">官方來源<input type="url" value={edit.websiteSource} onChange={(event) => setEdit({ ...edit, websiteSource: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3 font-normal" /></label></div><button type="submit" disabled={loading} className="mt-4 min-h-11 rounded-xl bg-[var(--teal)] px-5 text-sm font-semibold text-white disabled:opacity-40">儲存並更新</button></form>}
  </section>;
}
