"use client";

import { ArrowDownRight, ArrowUpRight, BarChart3, Database, MapPin, Minus, Search, Sparkles } from "lucide-react";
import { FormEvent, useEffect, useState } from "react";
import { api } from "@/lib/api";

type SourceStatus = {
  id: string;
  name: string;
  status: string;
  purpose: string;
  persistence: string;
};

type SourcesResponse = {
  collection_interval_seconds: number;
  sources: SourceStatus[];
};

type RankedHotspot = {
  id: string;
  slug: string;
  rank: number;
  name: string;
  city_code: string;
  city_name: string;
  country_code: string;
  country_name: string;
  category: string;
  score: number;
  components: { interest: number; growth: number; quality: number; confidence: number };
  pageviews_30d: number | null;
  growth_rate: number | null;
  trend_label: string;
  sources: string[];
  source_urls: string[];
  signal_date: string | null;
  is_estimate: boolean;
  is_deep_travel: boolean;
  depth_kind: "urban_local" | "day_trip" | null;
  depth_score: number | null;
  depth_reason: string | null;
  local_name: string | null;
  access_minutes: number | null;
  recommended_duration_minutes: number | null;
};

type RankingResponse = {
  scope: string;
  scope_key: string;
  observed_on: string | null;
  window_days: number;
  total: number;
  has_more: boolean;
  next_cursor: number | null;
  items: RankedHotspot[];
};

type FacetsResponse = {
  total: number;
  countries: { code: string; name: string; count: number }[];
  cities: { code: string; name: string; country_code: string; count: number }[];
  categories: { code: string; count: number }[];
  styles: { code: "all" | "deep"; name: string; count: number }[];
};

const categories = [
  ["", "所有類型"], ["culture", "文化古蹟"], ["food", "美食街區"],
  ["nature", "自然景觀"], ["beach", "海灘"], ["family", "親子"],
  ["viewpoint", "觀景地標"], ["shopping", "購物"], ["nightlife", "夜生活"],
] as const;

const categoryLabels = Object.fromEntries(categories) as Record<string, string>;
const sourceLabels: Record<string, string> = {
  curated_catalog: "精選主檔",
  wikimedia_pageviews: "Wikimedia 趨勢",
};

function trendIcon(item: RankedHotspot) {
  if (item.growth_rate === null) return <Minus size={15} />;
  if (item.growth_rate >= 0.15) return <ArrowUpRight size={15} />;
  if (item.growth_rate <= -0.15) return <ArrowDownRight size={15} />;
  return <Minus size={15} />;
}

function percent(value: number | null) {
  if (value === null) return "尚無比較資料";
  return `${value >= 0 ? "+" : ""}${Math.round(value * 100)}%`;
}

export function HotspotExplorer() {
  const [query, setQuery] = useState("");
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");
  const [category, setCategory] = useState("");
  const [style, setStyle] = useState<"all" | "deep">("all");
  const [ranking, setRanking] = useState<RankingResponse | null>(null);
  const [sources, setSources] = useState<SourcesResponse | null>(null);
  const [facets, setFacets] = useState<FacetsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load(append = false) {
    setLoading(true);
    setError("");
    const params = new URLSearchParams({ limit: "30" });
    if (query.trim()) params.set("q", query.trim());
    if (country) params.set("country_code", country);
    if (city) params.set("city_code", city);
    if (category) params.set("category", category);
    params.set("style", style);
    if (append && ranking?.next_cursor) params.set("after_rank", String(ranking.next_cursor));
    try {
      const result = await api<RankingResponse>(`/hotspots/rankings?${params}`);
      setRanking(append && ranking ? { ...result, items: [...ranking.items, ...result.items] } : result);
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    api<SourcesResponse>("/hotspots/sources").then(setSources).catch(() => undefined);
    api<FacetsResponse>("/hotspots/facets").then(setFacets).catch(() => undefined);
    api<RankingResponse>("/hotspots/rankings?limit=30")
      .then(setRanking)
      .catch((reason: Error) => setError(reason.message))
      .finally(() => setLoading(false));
  }, []);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void load(false);
  }

  return (
    <main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
      <section className="pb-7 pt-5 md:pb-9 md:pt-9">
        <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />旅遊熱點情報庫</p>
        <div className="mt-3 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-[-.035em] md:text-5xl">現在，大家在看哪裡？</h1>
            <p className="mt-3 max-w-2xl leading-7 text-[var(--muted)]">搜尋日本、韓國、泰國、台灣、新加坡、香港與越南景點，查看最近 30 天關注度、升溫幅度與資料可信度。排行是行程候選訊號，不等同即時人潮。</p>
          </div>
          <div className="rounded-2xl border border-[var(--line)] bg-white px-4 py-3 text-sm text-[var(--muted)]">
            <span className="font-semibold text-[var(--ink)]">更新日期</span> {ranking?.observed_on || "等待首次蒐集"}
          </div>
        </div>
      </section>

      <form onSubmit={submit} aria-label="熱門景點搜尋" className="grid gap-3 rounded-[1.75rem] border border-[var(--line)] bg-white p-4 shadow-[var(--shadow-lg)] md:grid-cols-[1fr_9rem_10rem_10rem_9rem_auto] md:p-5">
        <label className="relative">
          <span className="sr-only">景點關鍵字</span>
          <Search className="pointer-events-none absolute left-4 top-3.5 text-[var(--muted)]" size={19} />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜尋景點、別名或城市" className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-11 pr-4 outline-none focus:border-[var(--teal)]" />
        </label>
        <label>
          <span className="sr-only">國家或地區</span>
          <select value={country} onChange={(event) => { setCountry(event.target.value); setCity(""); }} className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3 outline-none focus:border-[var(--teal)]">
            <option value="">全部國家</option>
            {facets?.countries?.map((item) => <option key={item.code} value={item.code}>{item.name} ({item.count})</option>)}
          </select>
        </label>
        <label>
          <span className="sr-only">旅遊風格</span>
          <select value={style} onChange={(event) => setStyle(event.target.value as "all" | "deep")} className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3 outline-none focus:border-[var(--teal)]">
            {(facets?.styles || [{ code: "all", name: "全部旅遊", count: facets?.total || 0 }, { code: "deep", name: "深度旅遊", count: 0 }]).map((item) => <option key={item.code} value={item.code}>{item.name} ({item.count})</option>)}
          </select>
        </label>
        <label>
          <span className="sr-only">城市</span>
          <select value={city} onChange={(event) => setCity(event.target.value)} className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3 outline-none focus:border-[var(--teal)]">
            <option value="">全部城市</option>
            {facets?.cities?.filter((item) => !country || item.country_code === country).map((item) => <option key={item.code} value={item.code}>{item.name} ({item.count})</option>)}
          </select>
        </label>
        <label>
          <span className="sr-only">景點類型</span>
          <select value={category} onChange={(event) => setCategory(event.target.value)} className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3 outline-none focus:border-[var(--teal)]">
            {categories.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
        </label>
        <button type="submit" className="h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white hover:bg-[var(--teal-dark)]">查看排行</button>
      </form>

      <div className="mt-7 grid gap-7 lg:grid-cols-[1fr_18rem]">
        <section aria-live="polite" aria-busy={loading}>
          <div className="mb-4 flex items-center justify-between gap-4">
            <h2 className="flex items-center gap-2 text-xl font-bold"><BarChart3 size={20} className="text-[var(--coral)]" />熱門排行榜</h2>
            <p className="text-sm text-[var(--muted)]">已載入 {ranking?.items.length ?? 0}／{ranking?.total ?? 0} 個結果</p>
          </div>
          {loading && <div className="rounded-3xl border border-[var(--line)] bg-white p-8 text-[var(--muted)]">正在整理最新排行…</div>}
          {!loading && error && <div role="alert" className="rounded-3xl border border-[var(--coral)] bg-[var(--coral-soft)] p-6">{error}</div>}
          {!loading && !error && ranking?.items.length === 0 && <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white/70 p-8 text-center"><h3 className="font-bold">目前沒有符合的景點</h3><p className="mt-2 text-sm text-[var(--muted)]">可清除關鍵字或切換城市；若顯示等待首次蒐集，請先執行熱點蒐集工作。</p></div>}
          {!loading && !error && ranking && ranking.items.length > 0 && <ol className="grid gap-4 md:grid-cols-2">{ranking.items.map((item) => (
            <li key={item.id} className="relative overflow-hidden rounded-3xl border border-[var(--line)] bg-white p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex gap-3">
                  <span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-[var(--teal-soft)] text-lg font-bold text-[var(--teal-dark)]">{item.rank}</span>
                  <div><h3 className="text-lg font-bold">{item.name}</h3>{item.local_name && item.local_name !== item.name && <p className="text-xs text-[var(--muted)]">{item.local_name}</p>}<p className="mt-1 flex items-center gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} />{item.city_name}・{categoryLabels[item.category] || item.category}</p></div>
                </div>
                <div className="text-right"><strong className="text-2xl text-[var(--teal)]">{Math.round(item.score)}</strong><p className="text-xs text-[var(--muted)]">熱門分數</p></div>
              </div>
              <div className="mt-5 grid grid-cols-2 gap-3 rounded-2xl bg-[var(--paper)] p-4 text-sm">
                <div><p className="text-[var(--muted)]">30 天瀏覽</p><p className="mt-1 font-semibold">{item.pageviews_30d?.toLocaleString("zh-TW") ?? "尚待蒐集"}</p></div>
                <div><p className="text-[var(--muted)]">相較前期</p><p className="mt-1 flex items-center gap-1 font-semibold">{trendIcon(item)}{percent(item.growth_rate)}</p></div>
              </div>
              <div className="mt-4 flex flex-wrap items-center gap-2">
                {item.is_deep_travel && <span className="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-900">深度旅遊</span>}
                {item.depth_kind && <span className="rounded-full border border-amber-300 px-2.5 py-1 text-xs text-amber-900">{item.depth_kind === "day_trip" ? "近郊" : "市區巷弄"}</span>}
                <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${item.is_estimate ? "bg-[var(--coral-soft)] text-[var(--coral)]" : "bg-[var(--teal-soft)] text-[var(--teal-dark)]"}`}>{item.is_estimate ? "冷啟動估算" : item.trend_label}</span>
                {item.sources.map((source) => <span key={source} className="rounded-full border border-[var(--line)] px-2.5 py-1 text-xs text-[var(--muted)]">{sourceLabels[source] || source}</span>)}
                {item.source_urls[0] && <a href={item.source_urls[0]} target="_blank" rel="noreferrer" className="ml-auto text-xs font-semibold text-[var(--teal)]">查看來源</a>}
              </div>
              {item.is_deep_travel && <div className="mt-3 rounded-2xl border border-amber-200 bg-amber-50 p-3 text-xs leading-5 text-amber-950"><p>{item.depth_reason}</p><p className="mt-1 font-semibold">交通約 {item.access_minutes} 分鐘・建議停留 {item.recommended_duration_minutes} 分鐘・深度分數 {Math.round(item.depth_score || 0)}</p></div>}
            </li>
          ))}</ol>}
          {!loading && !error && ranking?.has_more && <div className="mt-6 text-center"><button type="button" onClick={() => void load(true)} className="rounded-xl border border-[var(--teal)] bg-white px-6 py-3 font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)]">載入更多</button></div>}
        </section>

        <aside className="h-fit rounded-3xl border border-[var(--line)] bg-white/80 p-5 lg:sticky lg:top-5">
          <h2 className="flex items-center gap-2 font-bold"><Database size={18} className="text-[var(--teal)]" />資料來源狀態</h2>
          <div className="mt-4 grid gap-4">{sources?.sources.map((source) => (
            <article key={source.id} className="border-b border-[var(--line)] pb-4 last:border-0 last:pb-0">
              <div className="flex items-center justify-between gap-2"><h3 className="text-sm font-semibold">{source.name}</h3><span className="rounded-full bg-[var(--paper)] px-2 py-1 text-[11px] text-[var(--muted)]">{source.status}</span></div>
              <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{source.purpose}</p>
            </article>
          )) || <p className="text-sm text-[var(--muted)]">正在讀取來源狀態…</p>}</div>
          <p className="mt-5 border-t border-[var(--line)] pt-4 text-xs leading-5 text-[var(--muted)]">AI 規劃行程時會把這份排行當候選清單，再依日期、動線、興趣與營業時間篩選。</p>
        </aside>
      </div>
    </main>
  );
}
