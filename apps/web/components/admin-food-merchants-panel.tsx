"use client";

import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";

type Merchant = {
  id: string;
  slug: string;
  destination_id: string;
  country_code: string;
  name: string;
  local_name: string;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  plus_code_global: string | null;
  coordinate_source_type: string | null;
  coordinate_source_url: string | null;
  coordinate_verified_at: string | null;
  google_place_id: string | null;
  naver_map_url: string | null;
  map_match_status: "unverified" | "verified" | "ambiguous" | "disabled";
  review_status: "pending" | "approved" | "rejected" | "disabled";
  is_active: boolean;
  foods: { id: string; slug: string; name: string }[];
  sources: { source_type: string; source_title: string; source_url: string }[];
};

type MerchantResponse = { items: Merchant[]; total: number };
type MapCandidateResponse = {
  configured: boolean;
  reason: string;
  message?: string;
  candidates: {
    place_id: string;
    name: string;
    address: string;
    google_maps_url: string;
    temporary_match_coordinates: {
      latitude: number;
      longitude: number;
      plus_code_global: string;
      expires_in_days: number;
      usage: "comparison_only";
    };
  }[];
};

function nullableNumber(value: string): number | null {
  return value.trim() ? Number(value) : null;
}

export function AdminFoodMerchantsPanel() {
  const [data, setData] = useState<MerchantResponse | null>(null);
  const [destination, setDestination] = useState("");
  const [mapStatus, setMapStatus] = useState("");
  const [query, setQuery] = useState("");
  const [editing, setEditing] = useState<Merchant | null>(null);
  const [candidate, setCandidate] = useState<MapCandidateResponse | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    const params = new URLSearchParams({ limit: "100" });
    if (destination.trim()) params.set("destination_id", destination.trim());
    if (mapStatus) params.set("map_status", mapStatus);
    if (query.trim()) params.set("q", query.trim());
    try {
      setData(await api<MerchantResponse>(`/admin/foods/merchants?${params}`));
    } catch (reason) {
      setMessage((reason as Error).message);
    }
  }, [destination, mapStatus, query]);

  useEffect(() => {
    const params = new URLSearchParams({ limit: "100" });
    if (destination.trim()) params.set("destination_id", destination.trim());
    if (mapStatus) params.set("map_status", mapStatus);
    if (query.trim()) params.set("q", query.trim());
    void api<MerchantResponse>(`/admin/foods/merchants?${params}`)
      .then(setData)
      .catch((reason: Error) => setMessage(reason.message));
  }, [destination, mapStatus, query]);

  async function previewPlusCode() {
    if (!editing || editing.latitude === null || editing.longitude === null) return;
    try {
      const result = await api<{ plus_code_global: string }>(
        "/admin/foods/merchants/plus-code-preview",
        { method: "POST", body: JSON.stringify({ latitude: editing.latitude, longitude: editing.longitude }) },
      );
      setEditing({ ...editing, plus_code_global: result.plus_code_global });
    } catch (reason) {
      setMessage((reason as Error).message);
    }
  }

  async function searchGoogleCandidate() {
    if (!editing || editing.country_code === "KR") return;
    setLoading(true);
    try {
      const result = await api<MapCandidateResponse>("/admin/foods/merchants/map-candidates", {
        method: "POST",
        body: JSON.stringify({
          query: `${editing.local_name} ${editing.destination_id}`,
          country_code: editing.country_code,
          latitude: editing.latitude,
          longitude: editing.longitude,
        }),
      });
      setCandidate(result);
      setMessage(result.message ?? (result.candidates.length ? "找到候選；請比對名稱與地址後再套用 Place ID。" : "找不到唯一候選。"));
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function save() {
    if (!editing) return;
    setLoading(true);
    try {
      await api(`/admin/foods/merchants/${editing.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          destination_id: editing.destination_id,
          country_code: editing.country_code,
          name: editing.name,
          local_name: editing.local_name,
          address: editing.address,
          latitude: editing.latitude,
          longitude: editing.longitude,
          coordinate_source_type: editing.coordinate_source_type,
          coordinate_source_url: editing.coordinate_source_url,
          google_place_id: editing.country_code === "KR" ? null : editing.google_place_id,
          naver_map_url: editing.country_code === "KR" ? editing.naver_map_url : null,
          map_match_status: editing.map_match_status,
          review_status: editing.review_status,
          is_active: editing.is_active,
        }),
      });
      setMessage("已儲存店家地點；Plus Code 由伺服器根據座標重新計算。");
      setEditing(null);
      setCandidate(null);
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return <section className="mt-12 border-t border-[var(--line)] pt-8">
    <div className="flex flex-wrap items-end gap-3">
      <div className="mr-auto"><p className="text-sm font-semibold tracking-[.12em] text-[var(--teal)]">精準店家地點</p><h2 className="mt-1 text-2xl font-bold">店家、地圖識別與永久座標</h2><p className="mt-2 max-w-3xl text-sm text-[var(--muted)]">未驗證的啟動候選不會公開。Google Places 座標僅用來比對，永久座標必須另附官方或人工查核來源。</p></div>
      <input aria-label="店家搜尋" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="店名或 slug" className="h-11 rounded-xl border px-3" />
      <input aria-label="店家目的地" value={destination} onChange={(event) => setDestination(event.target.value)} placeholder="目的地 ID" className="h-11 rounded-xl border px-3" />
      <select aria-label="地圖比對狀態" value={mapStatus} onChange={(event) => setMapStatus(event.target.value)} className="h-11 rounded-xl border px-3"><option value="">全部比對狀態</option><option value="unverified">待驗證</option><option value="verified">已驗證</option><option value="ambiguous">模糊</option><option value="disabled">已停用</option></select>
    </div>
    {message && <p role="status" className="mt-3 rounded-xl bg-[var(--paper)] px-4 py-3 text-sm text-[var(--muted)]">{message}</p>}
    <div className="mt-4 overflow-x-auto rounded-2xl border bg-white"><table className="w-full min-w-[980px] text-left text-sm"><thead className="bg-[var(--paper)]"><tr><th className="p-3">店家</th><th className="p-3">目的地／料理</th><th className="p-3">地圖識別</th><th className="p-3">座標／Plus Code</th><th className="p-3">發布</th><th className="p-3">操作</th></tr></thead><tbody>{data?.items.map((merchant) => <tr key={merchant.id} className="border-t"><td className="p-3 font-semibold">{merchant.name}<span className="block text-xs font-normal text-[var(--muted)]">{merchant.local_name} · {merchant.slug}</span></td><td className="p-3">{merchant.destination_id}<span className="block text-xs text-[var(--muted)]">{merchant.foods.map((food) => food.name).join("、")}</span></td><td className="p-3">{merchant.map_match_status}<span className="block max-w-[260px] truncate text-xs text-[var(--muted)]">{merchant.country_code === "KR" ? merchant.naver_map_url : merchant.google_place_id || "無精準識別"}</span></td><td className="p-3">{merchant.latitude ?? "—"}, {merchant.longitude ?? "—"}<span className="block text-xs text-[var(--muted)]">{merchant.plus_code_global || "待計算"}</span></td><td className="p-3">{merchant.review_status}<span className="block text-xs text-[var(--muted)]">{merchant.is_active ? "啟用" : "停用"}</span></td><td className="p-3"><button type="button" onClick={() => { setEditing({ ...merchant }); setCandidate(null); }} className="min-h-11 rounded-xl border border-[var(--teal)] px-3 font-semibold text-[var(--teal)]">編輯地點</button></td></tr>)}</tbody></table></div>

    {editing && <div className="fixed inset-0 z-[90] overflow-y-auto bg-slate-950/50 p-4 md:p-8"><div role="dialog" aria-modal="true" aria-labelledby="merchant-map-title" className="mx-auto max-w-4xl rounded-3xl bg-white p-6 shadow-2xl"><div className="flex items-start justify-between gap-4"><div><h3 id="merchant-map-title" className="text-2xl font-bold">{editing.name}</h3><p className="text-sm text-[var(--muted)]">{editing.destination_id} · {editing.country_code}</p></div><button type="button" onClick={() => setEditing(null)} className="min-h-11 rounded-xl border px-4">關閉</button></div>
      <div className="mt-5 grid gap-4 md:grid-cols-2"><label className="text-sm font-semibold">店名<input value={editing.name} onChange={(event) => setEditing({ ...editing, name: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold">當地店名<input value={editing.local_name} onChange={(event) => setEditing({ ...editing, local_name: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold">緯度<input type="number" step="any" value={editing.latitude ?? ""} onChange={(event) => setEditing({ ...editing, latitude: nullableNumber(event.target.value) })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold">經度<input type="number" step="any" value={editing.longitude ?? ""} onChange={(event) => setEditing({ ...editing, longitude: nullableNumber(event.target.value) })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold">座標來源類型<select value={editing.coordinate_source_type ?? ""} onChange={(event) => setEditing({ ...editing, coordinate_source_type: event.target.value || null })} className="mt-1 h-11 w-full rounded-xl border px-3"><option value="">待補</option><option value="official_tourism">官方觀光</option><option value="merchant_official">店家官方</option><option value="wikidata">Wikidata</option><option value="admin_verified">人工查核</option></select></label><label className="text-sm font-semibold">座標來源網址<input value={editing.coordinate_source_url ?? ""} onChange={(event) => setEditing({ ...editing, coordinate_source_url: event.target.value || null })} placeholder="https://" className="mt-1 h-11 w-full rounded-xl border px-3" /></label>{editing.country_code === "KR" ? <label className="text-sm font-semibold md:col-span-2">Naver 精準地點頁<input value={editing.naver_map_url ?? ""} onChange={(event) => setEditing({ ...editing, naver_map_url: event.target.value || null })} placeholder="https://map.naver.com/p/entry/place/..." className="mt-1 h-11 w-full rounded-xl border px-3" /></label> : <label className="text-sm font-semibold md:col-span-2">Google Place ID<input value={editing.google_place_id ?? ""} onChange={(event) => setEditing({ ...editing, google_place_id: event.target.value || null })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label>}</div>
      <div className="mt-4 flex flex-wrap gap-2"><button type="button" disabled={loading || editing.country_code === "KR"} onClick={() => void searchGoogleCandidate()} className="min-h-11 rounded-xl border border-[var(--teal)] px-4 font-semibold text-[var(--teal)] disabled:opacity-40">搜尋 Google 候選</button><button type="button" onClick={() => void previewPlusCode()} className="min-h-11 rounded-xl border px-4 font-semibold">預覽 Plus Code</button><span className="inline-flex min-h-11 items-center rounded-xl bg-[var(--paper)] px-4 font-mono text-sm">{editing.plus_code_global || "尚未計算"}</span></div>
      {candidate?.candidates[0] && <div className="mt-4 rounded-2xl border border-amber-300 bg-amber-50 p-4"><p className="font-semibold">{candidate.candidates[0].name}</p><p className="text-sm text-[var(--muted)]">{candidate.candidates[0].address}</p><p className="mt-2 text-xs">暫存比對座標（不得作為永久來源）：{candidate.candidates[0].temporary_match_coordinates.latitude}, {candidate.candidates[0].temporary_match_coordinates.longitude}</p><button type="button" onClick={() => setEditing({ ...editing, google_place_id: candidate.candidates[0].place_id })} className="mt-3 min-h-11 rounded-xl bg-amber-800 px-4 font-semibold text-white">套用 Place ID，保留人工審核</button></div>}
      <div className="mt-5 flex flex-wrap items-center gap-3"><select value={editing.map_match_status} onChange={(event) => setEditing({ ...editing, map_match_status: event.target.value as Merchant["map_match_status"] })} className="h-11 rounded-xl border px-3"><option value="unverified">待驗證</option><option value="verified">已驗證</option><option value="ambiguous">模糊</option><option value="disabled">地圖停用</option></select><select value={editing.review_status} onChange={(event) => setEditing({ ...editing, review_status: event.target.value as Merchant["review_status"] })} className="h-11 rounded-xl border px-3"><option value="pending">待審</option><option value="approved">核准</option><option value="rejected">拒絕</option><option value="disabled">停用</option></select><label className="flex items-center gap-2"><input type="checkbox" checked={editing.is_active} onChange={(event) => setEditing({ ...editing, is_active: event.target.checked })} />啟用</label><button type="button" disabled={loading} onClick={() => void save()} className="ml-auto min-h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white disabled:opacity-40">儲存並重算 Plus Code</button></div>
    </div></div>}
  </section>;
}
