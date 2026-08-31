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
};

type RankingResponse = {
  scope: string;
  scope_key: string;
  observed_on: string | null;
  window_days: number;
  items: RankedHotspot[];
};

const cities = [
  ["", "全部城市"], ["NRT", "東京"], ["KIX", "大阪／京都"], ["FUK", "福岡"],
  ["CTS", "札幌"], ["OKA", "沖繩"], ["NGO", "名古屋"], ["ICN", "首爾"],
  ["PUS", "釜山"], ["CJU", "濟州"], ["BKK", "曼谷"], ["CNX", "清邁"],
  ["HKT", "普吉"], ["KBV", "喀比"],
] as const;

const categories = [
  ["", "所有類型"], ["culture", "文化古蹟"], ["food", "美食街區"],
  ["nature", "自然景觀"], ["beach", "海灘"], ["family", "親子"],
  ["viewpoint", "觀景地標"],
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
  const [city, setCity] = useState("");
  const [category, setCategory] = useState("");
  const [ranking, setRanking] = useState<RankingResponse | null>(null);
  const [sources, setSources] = useState<SourcesResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  async function load(nextQuery = query, nextCity = city, nextCategory = category) {
    setLoading(true);
    setError("");
    const params = new URLSearchParams({ limit: "30" });
    if (nextQuery.trim()) params.set("q", nextQuery.trim());
    if (nextCity) params.set("city_code", nextCity);
    if (nextCategory) params.set("category", nextCategory);
    try {
      setRanking(await api<RankingResponse>(`/hotspots/rankings?${params}`));
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    api<SourcesResponse>("/hotspots/sources").then(setSources).catch(() => undefined);
    api<RankingResponse>("/hotspots/rankings?limit=30")
      .then(setRanking)
      .catch((reason: Error) => setError(reason.message))
      .finally(() => setLoading(false));
  }, []);

  function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    void load();
  }

  return (
    <main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
      <section className="pb-7 pt-5 md:pb-9 md:pt-9">
        <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />旅遊熱點情報庫</p>
        <div className="mt-3 flex flex-wrap items-end justify-between gap-4">
          <div>
            <h1 className="text-3xl font-bold tracking-[-.035em] md:text-5xl">現在，大家在看哪裡？</h1>
            <p className="mt-3 max-w-2xl leading-7 text-[var(--muted)]">搜尋日本、韓國與泰國景點，查看最近 30 天關注度、升溫幅度與資料可信度。排行是行程候選訊號，不等同即時人潮。</p>
          </div>
          <div className="rounded-2xl border border-[var(--line)] bg-white px-4 py-3 text-sm text-[var(--muted)]">
            <span className="font-semibold text-[var(--ink)]">更新日期</span> {ranking?.observed_on || "等待首次蒐集"}
          </div>
        </div>
      </section>

      <form onSubmit={submit} aria-label="熱門景點搜尋" className="grid gap-3 rounded-[1.75rem] border border-[var(--line)] bg-white p-4 shadow-[var(--shadow-lg)] md:grid-cols-[1fr_11rem_11rem_auto] md:p-5">
        <label className="relative">
          <span className="sr-only">景點關鍵字</span>
          <Search className="pointer-events-none absolute left-4 top-3.5 text-[var(--muted)]" size={19} />
          <input value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜尋景點、別名或城市" className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-11 pr-4 outline-none focus:border-[var(--teal)]" />
        </label>
        <label>
          <span className="sr-only">城市</span>
          <select value={city} onChange={(event) => setCity(event.target.value)} className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3 outline-none focus:border-[var(--teal)]">
            {cities.map(([value, label]) => <option key={value} value={value}>{label}</option>)}
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
            <p className="text-sm text-[var(--muted)]">{ranking?.items.length ?? 0} 個結果</p>
          </div>
          {loading && <div className="rounded-3xl border border-[var(--line)] bg-white p-8 text-[var(--muted)]">正在整理最新排行…</div>}
          {!loading && error && <div role="alert" className="rounded-3xl border border-[var(--coral)] bg-[var(--coral-soft)] p-6">{error}</div>}
          {!loading && !error && ranking?.items.length === 0 && <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white/70 p-8 text-center"><h3 className="font-bold">目前沒有符合的景點</h3><p className="mt-2 text-sm text-[var(--muted)]">可清除關鍵字或切換城市；若顯示等待首次蒐集，請先執行熱點蒐集工作。</p></div>}
          {!loading && !error && ranking && ranking.items.length > 0 && <ol className="grid gap-4 md:grid-cols-2">{ranking.items.map((item) => (
            <li key={item.id} className="relative overflow-hidden rounded-3xl border border-[var(--line)] bg-white p-5">
              <div className="flex items-start justify-between gap-4">
                <div className="flex gap-3">
                  <span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-[var(--teal-soft)] text-lg font-bold text-[var(--teal-dark)]">{item.rank}</span>
                  <div><h3 className="text-lg font-bold">{item.name}</h3><p className="mt-1 flex items-center gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} />{item.city_name}・{categoryLabels[item.category] || item.category}</p></div>
                </div>
                <div className="text-right"><strong className="text-2xl text-[var(--teal)]">{Math.round(item.score)}</strong><p className="text-xs text-[var(--muted)]">熱門分數</p></div>
              </div>
              <div className="mt-5 grid grid-cols-2 gap-3 rounded-2xl bg-[var(--paper)] p-4 text-sm">
                <div><p className="text-[var(--muted)]">30 天瀏覽</p><p className="mt-1 font-semibold">{item.pageviews_30d?.toLocaleString("zh-TW") ?? "尚待蒐集"}</p></div>
                <div><p className="text-[var(--muted)]">相較前期</p><p className="mt-1 flex items-center gap-1 font-semibold">{trendIcon(item)}{percent(item.growth_rate)}</p></div>
              </div>
              <div className="mt-4 flex flex-wrap items-center gap-2">
                <span className={`rounded-full px-2.5 py-1 text-xs font-semibold ${item.is_estimate ? "bg-[var(--coral-soft)] text-[var(--coral)]" : "bg-[var(--teal-soft)] text-[var(--teal-dark)]"}`}>{item.is_estimate ? "冷啟動估算" : item.trend_label}</span>
                {item.sources.map((source) => <span key={source} className="rounded-full border border-[var(--line)] px-2.5 py-1 text-xs text-[var(--muted)]">{sourceLabels[source] || source}</span>)}
                {item.source_urls[0] && <a href={item.source_urls[0]} target="_blank" rel="noreferrer" className="ml-auto text-xs font-semibold text-[var(--teal)]">查看來源</a>}
              </div>
            </li>
          ))}</ol>}
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
