"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";

type Candidate = {
  id: string; name: string; qid: string | null; city_code: string; city_name: string;
  category: string; origin: string; status: string; reason: string | null;
  distance_km: number | null; pageviews_30d: number | null; source_urls: string[]; is_active: boolean;
  is_deep_travel: boolean; depth_kind: "urban_local" | "day_trip" | null; depth_score: number | null;
  depth_reason: string | null; access_minutes: number | null; recommended_duration_minutes: number | null;
};
type Response = { items: Candidate[]; total: number; page: number; pages: number };

export function AdminHotspotsPanel() {
  const [data, setData] = useState<Response | null>(null);
  const [status, setStatus] = useState("pending");
  const [city, setCity] = useState("");
  const [origin, setOrigin] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [depthKind, setDepthKind] = useState<"urban_local" | "day_trip">("urban_local");
  const [depthReason, setDepthReason] = useState("");
  const [accessMinutes, setAccessMinutes] = useState(30);
  const [durationMinutes, setDurationMinutes] = useState(120);
  const [scores, setScores] = useState({ locality: 85, distinctiveness: 85, feasibility: 85, evidence: 90 });

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams({ limit: "100" });
    if (status) params.set("status", status);
    if (city) params.set("city_code", city);
    if (origin) params.set("origin", origin);
    try { setData(await api<Response>(`/admin/hotspots/candidates?${params}`)); }
    catch (error) { setMessage((error as Error).message); }
    finally { setLoading(false); }
  }, [city, origin, status]);

  useEffect(() => {
    const params = new URLSearchParams({ limit: "100" });
    if (status) params.set("status", status);
    if (city) params.set("city_code", city);
    if (origin) params.set("origin", origin);
    void api<Response>(`/admin/hotspots/candidates?${params}`)
      .then(setData)
      .catch((error: Error) => setMessage(error.message))
      .finally(() => setLoading(false));
  }, [city, origin, status]);

  async function review(action: "approve" | "reject" | "disable") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/review", { method: "POST", body: JSON.stringify({ ids: [...selected], action }) });
      setMessage(`已更新 ${selected.size} 筆景點候選`);
      setSelected(new Set());
      await load();
    } catch (error) { setMessage((error as Error).message); setLoading(false); }
  }

  async function updateDepth(isDeep: boolean) {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/review", { method: "POST", body: JSON.stringify({
        ids: [...selected], action: "update", is_deep_travel: isDeep,
        ...(isDeep ? { depth_kind: depthKind, depth_reason: depthReason, access_minutes: accessMinutes,
          recommended_duration_minutes: durationMinutes, locality_score: scores.locality,
          distinctiveness_score: scores.distinctiveness, feasibility_score: scores.feasibility,
          evidence_score: scores.evidence } : {}),
      }) });
      setMessage(isDeep ? `已設定 ${selected.size} 筆深度景點` : `已移除 ${selected.size} 筆深度標記`);
      setSelected(new Set()); await load();
    } catch (error) { setMessage((error as Error).message); setLoading(false); }
  }

  return <section className="mt-8">
    <div className="grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-3">
      <select aria-label="審核狀態" value={status} onChange={(e) => setStatus(e.target.value)} className="h-11 rounded-xl border border-[var(--line)] px-3"><option value="pending">待審</option><option value="approved">人工核准</option><option value="auto_approved">自動核准</option><option value="rejected">已拒絕</option><option value="disabled">已停用</option><option value="">全部狀態</option></select>
      <input aria-label="城市代碼" value={city} onChange={(e) => setCity(e.target.value.toUpperCase())} maxLength={3} placeholder="城市代碼，例如 TPE" className="h-11 rounded-xl border border-[var(--line)] px-3" />
      <select aria-label="資料來源" value={origin} onChange={(e) => setOrigin(e.target.value)} className="h-11 rounded-xl border border-[var(--line)] px-3"><option value="">全部來源</option><option value="curated">人工啟動資料</option><option value="wikimedia_discovery">Wikimedia 探索</option></select>
    </div>
    <div className="mt-4 flex flex-wrap items-center gap-2"><span className="mr-auto text-sm text-[var(--muted)]">共 {data?.total ?? 0} 筆，已選 {selected.size} 筆</span><button disabled={!selected.size || loading} onClick={() => void review("approve")} className="rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-40">核准</button><button disabled={!selected.size || loading} onClick={() => void review("reject")} className="rounded-xl border border-[var(--coral)] px-4 py-2 text-sm font-semibold text-[var(--coral)] disabled:opacity-40">拒絕</button><button disabled={!selected.size || loading} onClick={() => void review("disable")} className="rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-40">停用</button></div>
    <div className="mt-4 grid gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4 md:grid-cols-4">
      <select aria-label="深度類型" value={depthKind} onChange={(e) => setDepthKind(e.target.value as "urban_local" | "day_trip")} className="h-10 rounded-xl border px-3"><option value="urban_local">市區巷弄</option><option value="day_trip">近郊</option></select>
      <input aria-label="交通分鐘" type="number" min={1} max={depthKind === "urban_local" ? 45 : 90} value={accessMinutes} onChange={(e) => setAccessMinutes(Number(e.target.value))} className="h-10 rounded-xl border px-3" />
      <input aria-label="停留分鐘" type="number" min={30} max={480} value={durationMinutes} onChange={(e) => setDurationMinutes(Number(e.target.value))} className="h-10 rounded-xl border px-3" />
      <input aria-label="深度理由" value={depthReason} onChange={(e) => setDepthReason(e.target.value)} placeholder="深度旅遊理由" className="h-10 rounded-xl border px-3" />
      {Object.entries(scores).map(([key, value]) => <label key={key} className="text-xs font-semibold">{key}<input type="number" min={0} max={100} value={value} onChange={(e) => setScores((current) => ({ ...current, [key]: Number(e.target.value) }))} className="mt-1 h-9 w-full rounded-xl border px-3" /></label>)}
      <button disabled={!selected.size || loading || !depthReason.trim()} onClick={() => void updateDepth(true)} className="rounded-xl bg-amber-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40">設定深度景點</button>
      <button disabled={!selected.size || loading} onClick={() => void updateDepth(false)} className="rounded-xl border border-amber-700 px-4 py-2 text-sm font-semibold text-amber-900 disabled:opacity-40">移除深度標記</button>
    </div>
    {message && <p role="status" className="mt-3 text-sm text-[var(--muted)]">{message}</p>}
    <div className="mt-4 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white"><table className="w-full min-w-[1000px] text-left text-sm"><thead className="bg-[var(--paper)]"><tr><th className="p-3">選取</th><th className="p-3">景點</th><th className="p-3">分類／城市</th><th className="p-3">深度設定</th><th className="p-3">距離</th><th className="p-3">30 天瀏覽</th><th className="p-3">狀態／原因</th><th className="p-3">來源</th></tr></thead><tbody>{data?.items.map((item) => <tr key={item.id} className="border-t border-[var(--line)]"><td className="p-3"><input type="checkbox" checked={selected.has(item.id)} aria-label={`選取 ${item.name}`} onChange={(e) => setSelected((current) => { const next = new Set(current); if (e.target.checked) next.add(item.id); else next.delete(item.id); return next; })} /></td><td className="p-3 font-semibold">{item.name}<span className="block text-xs font-normal text-[var(--muted)]">{item.qid || "無 QID"}</span></td><td className="p-3">{item.category}<span className="block text-xs text-[var(--muted)]">{item.city_name} ({item.city_code})</span></td><td className="p-3">{item.is_deep_travel ? <><span className="rounded-full bg-amber-100 px-2 py-1 text-xs">{item.depth_kind === "day_trip" ? "近郊" : "市區巷弄"} · {Math.round(item.depth_score || 0)}</span><span className="mt-1 block text-xs text-[var(--muted)]">交通 {item.access_minutes}／停留 {item.recommended_duration_minutes} 分</span></> : "—"}</td><td className="p-3">{item.distance_km?.toFixed(1) ?? "—"} km</td><td className="p-3">{item.pageviews_30d?.toLocaleString("zh-TW") ?? "—"}</td><td className="p-3">{item.status}<span className="block text-xs text-[var(--muted)]">{item.reason || "—"}</span></td><td className="p-3">{item.source_urls.map((url, index) => <a key={url} href={url} target="_blank" rel="noreferrer" className="mr-2 font-semibold text-[var(--teal)]">來源 {index + 1}</a>)}</td></tr>)}</tbody></table>{!loading && data?.items.length === 0 && <p className="p-8 text-center text-[var(--muted)]">沒有符合條件的候選景點</p>}</div>
  </section>;
}
