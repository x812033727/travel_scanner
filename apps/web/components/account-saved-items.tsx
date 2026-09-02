"use client";

import {
  ExternalLink,
  Heart,
  LoaderCircle,
  MapPin,
  Trash2,
} from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { useSavedItems } from "@/components/saved-items-provider";
import { api } from "@/lib/api";

type SavedType = "hotspot" | "food" | "restaurant";
type SavedItem = {
  type: SavedType;
  id: string;
  title: string;
  subtitle: string;
  map_links: { url: string; label: string }[];
};
type Filter = "all" | SavedType;

const copy = {
  "zh-TW": {
    title: "我的收藏",
    description: "景點、美食與餐廳會同步到這個帳號。",
    loading: "正在載入收藏…",
    empty: "這個分類還沒有收藏。從景點或美食小卡按下愛心即可加入。",
    remove: "移除收藏",
    map: "開啟精準地圖",
    error: "收藏暫時無法載入",
    filters: { all: "全部", hotspot: "景點", food: "美食", restaurant: "餐廳" },
  },
  "zh-CN": {
    title: "我的收藏",
    description: "景点、美食与餐厅会同步到这个账号。",
    loading: "正在加载收藏…",
    empty: "这个分类还没有收藏。可从景点或美食卡片按下爱心加入。",
    remove: "移除收藏",
    map: "打开精确地图",
    error: "收藏暂时无法加载",
    filters: { all: "全部", hotspot: "景点", food: "美食", restaurant: "餐厅" },
  },
  en: {
    title: "Saved",
    description: "Places, foods, and restaurants stay synced to your account.",
    loading: "Loading saved items…",
    empty: "Nothing saved in this category yet.",
    remove: "Remove saved item",
    map: "Open exact map location",
    error: "Saved items are unavailable",
    filters: {
      all: "All",
      hotspot: "Places",
      food: "Food",
      restaurant: "Restaurants",
    },
  },
  ja: {
    title: "保存済み",
    description: "スポット、料理、レストランをアカウントに同期します。",
    loading: "保存済みを読み込み中…",
    empty: "このカテゴリにはまだ保存がありません。",
    remove: "保存から削除",
    map: "正確な地図を開く",
    error: "保存済みを読み込めません",
    filters: {
      all: "すべて",
      hotspot: "スポット",
      food: "料理",
      restaurant: "レストラン",
    },
  },
  ko: {
    title: "저장 목록",
    description: "명소, 음식, 식당을 계정에 동기화합니다.",
    loading: "저장 목록 불러오는 중…",
    empty: "이 분류에 저장된 항목이 없습니다.",
    remove: "저장 해제",
    map: "정확한 지도 열기",
    error: "저장 목록을 불러올 수 없습니다",
    filters: { all: "전체", hotspot: "명소", food: "음식", restaurant: "식당" },
  },
} as const;

export function AccountSavedItems() {
  const locale = useLocale() as keyof typeof copy;
  const text = copy[locale] ?? copy.en;
  const saved = useSavedItems();
  const [items, setItems] = useState<SavedItem[]>([]);
  const [filter, setFilter] = useState<Filter>("all");
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState("");

  useEffect(() => {
    api<{ items: SavedItem[] }>("/saved-items?limit=100")
      .then((result) => setItems(result.items))
      .catch((reason: Error) => setError(reason.message))
      .finally(() => setLoaded(true));
  }, []);

  const visible = useMemo(
    () =>
      filter === "all" ? items : items.filter((item) => item.type === filter),
    [filter, items],
  );
  const counts = useMemo(
    () => ({
      all: items.length,
      hotspot: items.filter((item) => item.type === "hotspot").length,
      food: items.filter((item) => item.type === "food").length,
      restaurant: items.filter((item) => item.type === "restaurant").length,
    }),
    [items],
  );

  async function remove(item: SavedItem) {
    const key = `${item.type}:${item.id}`;
    setBusy(key);
    setError("");
    try {
      await saved.setSaved(item.type, item.id, false);
      setItems((current) =>
        current.filter(
          (candidate) =>
            candidate.type !== item.type || candidate.id !== item.id,
        ),
      );
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setBusy("");
    }
  }

  return (
    <section className="app-surface mb-6 p-5 md:p-8">
      <div className="flex items-center gap-3">
        <span className="grid h-11 w-11 place-items-center rounded-2xl bg-[var(--coral-soft)] text-[var(--coral)]">
          <Heart size={20} fill="currentColor" />
        </span>
        <div>
          <h2 className="text-xl font-bold">{text.title}</h2>
          <p className="text-sm text-[var(--muted)]">{text.description}</p>
        </div>
      </div>
      <div className="app-chip-row mt-5" role="tablist" aria-label={text.title}>
        {(["all", "hotspot", "food", "restaurant"] as Filter[]).map((key) => (
          <button
            key={key}
            type="button"
            role="tab"
            aria-selected={filter === key}
            onClick={() => setFilter(key)}
            className={`app-filter-chip ${filter === key ? "app-filter-chip-active" : ""}`}
          >
            <span>{text.filters[key]}</span>
            <span className="app-filter-count">{counts[key]}</span>
          </button>
        ))}
      </div>
      {error && (
        <p
          role="alert"
          className="mt-4 rounded-2xl bg-red-50 p-4 text-sm text-red-800"
        >
          {text.error}：{error}
        </p>
      )}
      {!loaded ? (
        <div role="status" className="mt-5 grid gap-3 sm:grid-cols-2">
          <span className="app-skeleton h-20" />
          <span className="app-skeleton h-20" />
          <span className="sr-only">{text.loading}</span>
        </div>
      ) : visible.length === 0 ? (
        <div className="app-empty-state mt-5">
          <Heart size={24} />
          <p>{text.empty}</p>
        </div>
      ) : (
        <div className="mt-5 grid gap-3 sm:grid-cols-2">
          {visible.map((item) => {
            const map = item.map_links[0];
            const key = `${item.type}:${item.id}`;
            return (
              <article key={key} className="saved-item-card">
                <span className="grid h-10 w-10 shrink-0 place-items-center rounded-xl bg-[var(--teal-soft)] text-[var(--teal-dark)]">
                  <MapPin size={18} />
                </span>
                <div className="min-w-0 flex-1">
                  <strong className="block truncate text-sm">
                    {item.title}
                  </strong>
                  <span className="block truncate text-xs text-[var(--muted)]">
                    {item.subtitle}
                  </span>
                </div>
                {map && (
                  <a
                    href={map.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    aria-label={`${text.map}：${item.title}`}
                    className="app-icon-button"
                  >
                    <ExternalLink size={17} />
                  </a>
                )}
                <button
                  type="button"
                  disabled={busy === key}
                  onClick={() => void remove(item)}
                  aria-label={`${text.remove}：${item.title}`}
                  className="app-icon-button text-[var(--coral)]"
                >
                  {busy === key ? (
                    <LoaderCircle className="animate-spin" size={17} />
                  ) : (
                    <Trash2 size={17} />
                  )}
                </button>
              </article>
            );
          })}
        </div>
      )}
    </section>
  );
}
