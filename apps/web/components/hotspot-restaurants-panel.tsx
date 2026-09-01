"use client";

import {
  ChevronDown,
  Clock3,
  ExternalLink,
  Globe2,
  MapPinned,
  RefreshCw,
  Star,
  UtensilsCrossed,
  X,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { KeyboardEvent, TouchEvent, useCallback, useEffect, useMemo, useRef, useState } from "react";
import { api } from "@/lib/api";

type RestaurantSort = "recommended" | "rating" | "reviews" | "distance";
type Restaurant = {
  place_id: string;
  name: string;
  address: string | null;
  latitude: number;
  longitude: number;
  distance_km: number;
  rating: number;
  review_count: number;
  recommendation_score: number;
  opening_hours: string[];
  open_now: boolean | null;
  official_website_url: string | null;
  google_maps_url: string | null;
  plus_code: string | null;
  primary_type: string | null;
  observed_at: string;
};
type Coverage = {
  status: "not_started" | "queued" | "running" | "quota_paused" | "partial" | "completed" | "failed";
  cells_completed: number;
  cells_total: number;
  candidate_count: number;
};
type RestaurantResponse = {
  hotspot_id: string;
  hotspot_name: string;
  radius_km: 5 | 10;
  sort: RestaurantSort;
  filters: { min_rating: number; min_review_count: number };
  items: Restaurant[];
  next_cursor: number | null;
  coverage: Coverage;
  observed_at: string;
  attribution: string;
  persistence: {
    place_id: "durable";
    generated_maps_url: "durable";
    location_cache_ttl_days: number;
    other_google_fields: "live_only";
  };
};

function sortRestaurants(items: Restaurant[], sort: RestaurantSort) {
  return [...items].sort((left, right) => {
    if (sort === "rating") return right.rating - left.rating || right.review_count - left.review_count || left.distance_km - right.distance_km;
    if (sort === "reviews") return right.review_count - left.review_count || right.rating - left.rating || left.distance_km - right.distance_km;
    if (sort === "distance") return left.distance_km - right.distance_km || right.recommendation_score - left.recommendation_score;
    return right.recommendation_score - left.recommendation_score || right.review_count - left.review_count || left.distance_km - right.distance_km;
  });
}

export function HotspotRestaurantsPanel({
  hotspot,
  onClose,
}: {
  hotspot: { id: string; name: string };
  onClose: () => void;
}) {
  const t = useTranslations("restaurants");
  const locale = useLocale();
  const [radius, setRadius] = useState<5 | 10>(5);
  const [sort, setSort] = useState<RestaurantSort>("recommended");
  const [data, setData] = useState<RestaurantResponse | null>(null);
  const [items, setItems] = useState<Restaurant[]>([]);
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState("");
  const dialogRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const touchStart = useRef<number | null>(null);
  const initialPlaceIds = useRef<string[]>([]);
  const number = new Intl.NumberFormat(locale);
  const date = new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" });

  const search = useCallback(async (cursor?: number) => {
    if (cursor === undefined) setLoading(true);
    else setLoadingMore(true);
    setError("");
    try {
      const result = await api<RestaurantResponse>(`/hotspots/${hotspot.id}/restaurant-searches`, {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({
          radius_km: radius,
          sort: "recommended",
          ...(cursor === undefined ? {} : { cursor, exclude_place_ids: initialPlaceIds.current }),
        }),
      });
      setData(result);
      if (cursor === undefined) initialPlaceIds.current = result.items.map((item) => item.place_id);
      setItems((current) => {
        if (cursor === undefined) return result.items;
        const merged = new Map(current.map((item) => [item.place_id, item]));
        result.items.forEach((item) => merged.set(item.place_id, item));
        return [...merged.values()];
      });
    } catch (reason) {
      setError((reason as Error).message);
    } finally {
      setLoading(false);
      setLoadingMore(false);
    }
  }, [hotspot.id, radius]);

  useEffect(() => {
    const timer = window.setTimeout(() => void search(), 0);
    return () => window.clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();
    const closeOnEscape = (event: globalThis.KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, [onClose]);

  function trapFocus(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key !== "Tab") return;
    const nodes = dialogRef.current?.querySelectorAll<HTMLElement>(
      "button:not([disabled]), a[href], select:not([disabled])",
    );
    if (!nodes?.length) return;
    const first = nodes[0];
    const last = nodes[nodes.length - 1];
    if (event.shiftKey && document.activeElement === first) {
      event.preventDefault();
      last.focus();
    } else if (!event.shiftKey && document.activeElement === last) {
      event.preventDefault();
      first.focus();
    }
  }

  function handleTouchStart(event: TouchEvent) {
    touchStart.current = event.touches[0]?.clientY ?? null;
  }

  function handleTouchEnd(event: TouchEvent) {
    const end = event.changedTouches[0]?.clientY;
    if (touchStart.current !== null && end !== undefined && end - touchStart.current > 90) onClose();
    touchStart.current = null;
  }

  const coveragePercent = data?.coverage.cells_total
    ? Math.min(100, Math.round(data.coverage.cells_completed / data.coverage.cells_total * 100))
    : 0;
  const nextCursor = data?.next_cursor;
  const sortedItems = useMemo(() => sortRestaurants(items, sort), [items, sort]);

  return <div
    className="fixed inset-0 z-[80] bg-slate-950/45 backdrop-blur-sm"
    role="presentation"
    onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}
  >
    <div
      ref={dialogRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="restaurant-panel-title"
      onKeyDown={trapFocus}
      onTouchStart={handleTouchStart}
      onTouchEnd={handleTouchEnd}
      className="absolute inset-x-0 bottom-0 flex h-[94dvh] flex-col rounded-t-[2rem] bg-[var(--paper)] shadow-2xl md:inset-y-0 md:left-auto md:h-full md:w-[38rem] md:rounded-none md:rounded-l-[2rem]"
    >
      <div className="mx-auto mt-2 h-1.5 w-11 rounded-full bg-slate-300 md:hidden" />
      <header className="border-b border-[var(--line)] px-5 pb-4 pt-4 md:px-7 md:pt-7">
        <div className="flex items-start gap-3">
          <div className="min-w-0 flex-1">
            <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[.16em] text-[var(--coral)]"><UtensilsCrossed size={15} />{t("eyebrow")}</p>
            <h2 id="restaurant-panel-title" className="mt-1 text-2xl font-bold tracking-tight">{t("title", { name: hotspot.name })}</h2>
            <p className="mt-1 text-sm text-[var(--muted)]">{t("threshold")}</p>
          </div>
          <button ref={closeRef} type="button" onClick={onClose} aria-label={t("close")} className="grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[var(--line)] bg-white"><X /></button>
        </div>
        <div className="mt-4 grid grid-cols-2 gap-2">
          <label className="text-xs font-semibold text-[var(--muted)]">{t("radius")}
            <select value={radius} onChange={(event) => setRadius(Number(event.target.value) as 5 | 10)} className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 text-sm text-[var(--ink)]">
              <option value={5}>{t("radiusOption", { radius: 5 })}</option>
              <option value={10}>{t("radiusOption", { radius: 10 })}</option>
            </select>
          </label>
          <label className="text-xs font-semibold text-[var(--muted)]">{t("sortLabel")}
            <select value={sort} onChange={(event) => setSort(event.target.value as RestaurantSort)} className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 text-sm text-[var(--ink)]">
              <option value="recommended">{t("sort.recommended")}</option>
              <option value="rating">{t("sort.rating")}</option>
              <option value="reviews">{t("sort.reviews")}</option>
              <option value="distance">{t("sort.distance")}</option>
            </select>
          </label>
        </div>
        <p className="mt-2 text-[11px] leading-5 text-[var(--muted)]">{t("recommendationNote")}</p>
      </header>
      <div className="overflow-y-auto overscroll-contain px-5 pb-[calc(1.5rem+env(safe-area-inset-bottom))] pt-5 md:px-7">
        {data && <section className="mb-4 rounded-2xl border border-[var(--line)] bg-white p-4 text-xs">
          <div className="flex items-center justify-between gap-3"><strong>{t("coverage.title")}</strong><span className="rounded-full bg-[var(--teal-soft)] px-2 py-1 font-semibold text-[var(--teal-dark)]">{t(`coverage.${data.coverage.status}`)}</span></div>
          <div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-[var(--teal)]" style={{ width: `${coveragePercent}%` }} /></div>
          <p className="mt-2 text-[var(--muted)]">{t("coverage.detail", { candidates: data.coverage.candidate_count, completed: data.coverage.cells_completed, total: data.coverage.cells_total })}</p>
        </section>}
        {loading && <div className="rounded-2xl bg-white p-7 text-sm text-[var(--muted)]">{t("loading")}</div>}
        {!loading && error && <div role="alert" className="rounded-2xl bg-[var(--coral-soft)] p-5 text-sm"><p>{error}</p><button type="button" onClick={() => void search()} className="mt-3 inline-flex min-h-11 items-center gap-2 rounded-xl bg-white px-4 font-semibold"><RefreshCw size={16} />{t("retry")}</button></div>}
        {!loading && !error && !items.length && <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white p-8 text-center"><UtensilsCrossed className="mx-auto text-[var(--coral)]" /><h3 className="mt-3 font-bold">{t("emptyTitle")}</h3><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("emptyBody")}</p></div>}
        {!loading && !error && sortedItems.length > 0 && <ol className="grid gap-3">{sortedItems.map((restaurant, index) => <li key={restaurant.place_id} className="rounded-3xl border border-[var(--line)] bg-white p-4 shadow-sm">
          <div className="flex items-start gap-3"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-[var(--coral-soft)] text-sm font-bold text-[var(--coral)]">{index + 1}</span><div className="min-w-0 flex-1"><h3 className="font-bold leading-5">{restaurant.name}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{restaurant.address}</p></div><span className="whitespace-nowrap rounded-full bg-amber-50 px-2.5 py-1 text-sm font-bold text-amber-800"><Star className="mr-1 inline" size={14} fill="currentColor" />{restaurant.rating.toFixed(1)}</span></div>
          <div className="mt-3 grid grid-cols-3 gap-2 text-center text-xs"><div className="rounded-xl bg-[var(--paper)] p-2"><strong className="block text-sm">{number.format(restaurant.review_count)}</strong><span className="text-[var(--muted)]">{t("reviews")}</span></div><div className="rounded-xl bg-[var(--paper)] p-2"><strong className="block text-sm">{restaurant.distance_km.toFixed(1)} km</strong><span className="text-[var(--muted)]">{t("distance")}</span></div><div className="rounded-xl bg-[var(--paper)] p-2"><strong className={restaurant.open_now === true ? "block text-sm text-emerald-700" : "block text-sm"}>{restaurant.open_now === null ? t("hoursUnknown") : restaurant.open_now ? t("openNow") : t("closedNow")}</strong><span className="text-[var(--muted)]">{t("liveStatus")}</span></div></div>
          {restaurant.opening_hours.length > 0 && <details className="mt-3 rounded-xl border border-[var(--line)] px-3 py-2 text-xs"><summary className="flex min-h-7 cursor-pointer list-none items-center gap-2 font-semibold"><Clock3 size={14} className="text-[var(--teal)]" />{t("openingHours")}<ChevronDown size={14} className="ml-auto" /></summary><div className="mt-2 grid gap-1 border-t border-[var(--line)] pt-2 text-[var(--muted)]">{restaurant.opening_hours.map((line) => <p key={line}>{line}</p>)}</div></details>}
          {(restaurant.plus_code || restaurant.latitude) && <div className="mt-3 rounded-xl bg-[var(--paper)] px-3 py-2 text-xs leading-5 text-[var(--muted)]"><p className="flex items-center gap-2"><MapPinned size={14} />{restaurant.plus_code || t("plusCodeUnknown")}</p><p className="pl-[22px] font-mono">{restaurant.latitude.toFixed(5)}, {restaurant.longitude.toFixed(5)}</p></div>}
          <div className={`mt-3 grid gap-2 ${restaurant.official_website_url ? "grid-cols-2" : "grid-cols-1"}`}>
            {restaurant.google_maps_url && <a href={restaurant.google_maps_url} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-3 text-sm font-semibold text-white"><MapPinned size={16} />{t("openMap")}<ExternalLink size={13} /></a>}
            {restaurant.official_website_url && <a href={restaurant.official_website_url} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"><Globe2 size={16} />{t("website")}<ExternalLink size={13} /></a>}
          </div>
          <p className="mt-3 text-[10px] text-[var(--muted)]">{t("liveObserved", { time: date.format(new Date(restaurant.observed_at)) })}</p>
        </li>)}</ol>}
        {!loading && !error && nextCursor !== undefined && nextCursor !== null && <button type="button" disabled={loadingMore} onClick={() => void search(nextCursor)} className="mt-4 flex min-h-12 w-full items-center justify-center gap-2 rounded-2xl border border-[var(--teal)] bg-white font-semibold text-[var(--teal)] disabled:opacity-50">{loadingMore && <RefreshCw size={16} className="animate-spin" />}{t("loadMore")}</button>}
        {data && <p className="mt-5 text-center text-xs leading-5 text-[var(--muted)]">{t("attributionPrefix")} <span translate="no" className="whitespace-nowrap font-normal">{data.attribution}</span><br />{t("storageNotice")}</p>}
      </div>
    </div>
  </div>;
}
