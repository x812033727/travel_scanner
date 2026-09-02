"use client";

import {
  ArrowDownRight,
  ArrowUpRight,
  BarChart3,
  BookOpenText,
  Building2,
  CalendarClock,
  Database,
  ExternalLink,
  FileText,
  MapPin,
  Minus,
  Play,
  Search,
  Sparkles,
  SlidersHorizontal,
  UtensilsCrossed,
  X,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import Image from "next/image";
import { FormEvent, KeyboardEvent, TouchEvent, useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import { HotspotRestaurantsPanel } from "@/components/hotspot-restaurants-panel";
import { TravelCardActions } from "@/components/travel-card-actions";

type SourceStatus = { id: string; name: string; status: string; purpose: string; persistence: string };
type MapLink = { provider: "google" | "naver"; label: string; url: string; primary: boolean };
type PlaceSummary = {
  status: "ready" | "pending_review" | "stale" | "unavailable";
  google_maps_url: string | null; map_links: MapLink[]; official_website_url: string | null;
  official_website_verified: boolean; has_details: boolean; updated_at: string | null;
};
type SourcesResponse = { collection_interval_seconds: number; sources: SourceStatus[] };
type RankedHotspot = {
  id: string; slug: string; rank: number; name: string; city_code: string; city_name: string;
  destination_id: string; destination_role: "primary" | "secondary" | "extension";
  parent_destination_id: string | null; is_cross_city: boolean;
  country_code: string; country_name: string; category: string; score: number;
  components: { interest: number; growth: number; quality: number; confidence: number };
  pageviews_30d: number | null; growth_rate: number | null; trend_label: string;
  sources: string[]; source_urls: string[]; signal_date: string | null; is_estimate: boolean;
  is_deep_travel: boolean; depth_kind: "urban_local" | "day_trip" | null;
  depth_score: number | null; depth_reason: string | null; local_name: string | null;
  access_minutes: number | null; recommended_duration_minutes: number | null;
  guide_counts: { article: number; video: number };
  map_links: MapLink[];
  place_summary: PlaceSummary;
};
type RankingResponse = { scope: string; scope_key: string; observed_on: string | null; window_days: number; total: number; has_more: boolean; next_cursor: number | null; items: RankedHotspot[] };
type FacetsResponse = {
  total: number;
  countries: { code: string; name: string; count: number }[];
  cities: { code: string; destination_id: string; name: string; country_code: string; count: number; destination_role: "primary" | "secondary" | "extension"; parent_destination_id: string | null; is_cross_city: boolean }[];
  categories: { code: string; count: number }[];
  styles: { code: "all" | "deep"; name: string; count: number }[];
};
type Guide = {
  id: string; type: "article" | "video"; provider: string; locale: string; title: string;
  creator_name: string; thumbnail_url: string | null; summary: string | null;
  published_at: string | null; duration_seconds: number | null; view_count: number | null;
  opens_30d: number; updated_at: string;
};
type GuidesResponse = {
  hotspot_id: string; hotspot_name: string; locale: string; videos: Guide[]; articles: Guide[];
  other_languages_available: boolean; updated_at: string | null;
};
type PlaceDetail = PlaceSummary & {
  hotspot_id: string; hotspot_name: string; address: string | null;
  opening_hours: { weekday_descriptions?: string[]; periods?: Array<Record<string, unknown>> };
  attribution: { provider: string | null; provider_url: string | null; third_party: Array<{ provider?: string; providerUri?: string }> };
};

const categoryCodes = ["", "culture", "food", "nature", "beach", "family", "viewpoint", "shopping", "nightlife"] as const;
const localeLabels: Record<string, string> = { en: "EN", ja: "日本語", ko: "한국어", "zh-TW": "繁中", "zh-CN": "简中" };

function trendIcon(item: RankedHotspot) {
  if (item.growth_rate === null) return <Minus size={15} />;
  if (item.growth_rate >= 0.15) return <ArrowUpRight size={15} />;
  if (item.growth_rate <= -0.15) return <ArrowDownRight size={15} />;
  return <Minus size={15} />;
}

function PlaceDetailsPanel({ hotspot, onClose }: { hotspot: RankedHotspot; onClose: () => void }) {
  const t = useTranslations("hotspots");
  const locale = useLocale();
  const [data, setData] = useState<GuidesResponse | null>(null);
  const [place, setPlace] = useState<PlaceDetail | null>(null);
  const [loading, setLoading] = useState(true);
  const [placeLoading, setPlaceLoading] = useState(true);
  const [error, setError] = useState(false);
  const [placeError, setPlaceError] = useState(false);
  const [otherLanguages, setOtherLanguages] = useState(false);
  const dialogRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const touchStart = useRef<number | null>(null);
  const number = new Intl.NumberFormat(locale);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();
    return () => { document.body.style.overflow = previousOverflow; };
  }, []);

  useEffect(() => {
    const closeOnEscape = (event: globalThis.KeyboardEvent) => {
      if (event.key === "Escape") onClose();
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => document.removeEventListener("keydown", closeOnEscape);
  }, [onClose]);

  useEffect(() => {
    api<GuidesResponse>(`/hotspots/${hotspot.id}/guides?limit_per_type=5&include_other_languages=${otherLanguages}`)
      .then(setData)
      .catch(() => setError(true))
      .finally(() => setLoading(false));
  }, [hotspot.id, otherLanguages]);

  useEffect(() => {
    api<PlaceDetail>(`/hotspots/${hotspot.id}/place`)
      .then(setPlace)
      .catch(() => setPlaceError(true))
      .finally(() => setPlaceLoading(false));
  }, [hotspot.id]);

  function trapFocus(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key !== "Tab") return;
    const nodes = dialogRef.current?.querySelectorAll<HTMLElement>("button:not([disabled]), a[href]");
    if (!nodes?.length) return;
    const first = nodes[0];
    const last = nodes[nodes.length - 1];
    if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last.focus(); }
    else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first.focus(); }
  }

  function touchStartHandler(event: TouchEvent) { touchStart.current = event.touches[0]?.clientY ?? null; }
  function touchEndHandler(event: TouchEvent) {
    const end = event.changedTouches[0]?.clientY;
    if (touchStart.current !== null && end !== undefined && end - touchStart.current > 90) onClose();
    touchStart.current = null;
  }

  function guideCard(guide: Guide) {
    const metric = guide.type === "video"
      ? t("youtubeViews", { count: number.format(guide.view_count || 0) })
      : t("articleOpens", { count: number.format(guide.opens_30d) });
    return <a
      key={guide.id}
      href={`/${locale}/out/guides/${guide.id}`}
      target="_blank"
      rel="noopener noreferrer"
      aria-label={`${guide.title} — ${t("openNew")}`}
      className="group grid grid-cols-[5rem_1fr_auto] gap-3 rounded-2xl border border-[var(--line)] bg-white p-3 transition hover:-translate-y-0.5 hover:border-[var(--teal)] hover:shadow-md"
    >
      <div className="relative grid h-20 place-items-center overflow-hidden rounded-xl bg-[var(--paper)]">
        {guide.thumbnail_url
          ? <div role="img" aria-label="" className="absolute inset-0 bg-cover bg-center" style={{ backgroundImage: `url(${JSON.stringify(guide.thumbnail_url)})` }} />
          : guide.type === "video" ? <Play className="text-[var(--teal)]" /> : <FileText className="text-[var(--teal)]" />}
        {guide.type === "video" && guide.thumbnail_url && <span className="relative grid h-8 w-8 place-items-center rounded-full bg-black/70 text-white"><Play size={14} fill="currentColor" /></span>}
      </div>
      <div className="min-w-0 self-center">
        <div className="mb-1 flex flex-wrap items-center gap-1.5 text-[11px] font-semibold">
          <span className="rounded-full bg-[var(--teal-soft)] px-2 py-0.5 text-[var(--teal-dark)]">{localeLabels[guide.locale] || guide.locale}</span>
          <span className="text-[var(--muted)]">{guide.provider === "youtube" ? "YouTube" : guide.creator_name}</span>
        </div>
        <h4 className="line-clamp-2 text-sm font-bold leading-5">{guide.title}</h4>
        <p className="mt-1 text-xs text-[var(--muted)]">{guide.creator_name} · {metric}</p>
      </div>
      <ExternalLink size={16} className="mt-1 text-[var(--muted)] transition group-hover:text-[var(--teal)]" />
    </a>;
  }

  const empty = !loading && !error && data && data.videos.length === 0 && data.articles.length === 0;
  const primaryMapLink = place?.map_links.find((link) => link.primary) ?? place?.map_links[0] ?? null;
  const openingHourLines = place?.opening_hours.weekday_descriptions ?? [];
  const showGoogleAttribution = Boolean(place?.attribution.provider === "Google Maps" && (place.address || openingHourLines.length));
  return <div className="fixed inset-0 z-[80] bg-slate-950/45 backdrop-blur-sm" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
    <div
      ref={dialogRef}
      role="dialog"
      aria-modal="true"
      aria-labelledby="place-panel-title"
      onKeyDown={trapFocus}
      onTouchStart={touchStartHandler}
      onTouchEnd={touchEndHandler}
      className="absolute inset-x-0 bottom-0 flex max-h-[94dvh] flex-col rounded-t-[2rem] bg-[var(--paper)] shadow-2xl md:inset-y-0 md:left-auto md:h-full md:max-h-none md:w-[34rem] md:rounded-none md:rounded-l-[2rem]"
    >
      <div className="mx-auto mt-2 h-1.5 w-11 rounded-full bg-slate-300 md:hidden" />
      <header className="flex items-start gap-3 border-b border-[var(--line)] px-5 pb-4 pt-4 md:px-7 md:pt-7">
        <div className="min-w-0 flex-1">
          <p className="text-xs font-bold uppercase tracking-[.16em] text-[var(--teal)]">{t("placeDetails")}</p>
          <h2 id="place-panel-title" className="mt-1 text-2xl font-bold tracking-tight">{t("guideTitle", { name: hotspot.name })}</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">{t("placeIntro")}</p>
        </div>
        <button ref={closeRef} type="button" onClick={onClose} aria-label={t("close")} className="grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[var(--line)] bg-white"><X /></button>
      </header>
      <div className="overflow-y-auto overscroll-contain px-5 pb-[calc(1.5rem+env(safe-area-inset-bottom))] pt-5 md:px-7">
        {placeLoading && <div className="rounded-2xl bg-white p-6 text-sm text-[var(--muted)]">{t("placeLoading")}</div>}
        {placeError && <div role="alert" className="rounded-2xl bg-[var(--coral-soft)] p-6 text-sm">{t("placeError")}</div>}
        {!placeLoading && !placeError && place && <section className="mb-7 grid gap-4" aria-label={t("placeDetails")}>
          {place.status !== "ready" && <p className={`rounded-2xl px-4 py-3 text-sm ${place.status === "pending_review" ? "bg-amber-50 text-amber-950" : place.status === "stale" ? "bg-sky-50 text-sky-950" : "bg-slate-100 text-slate-700"}`}>{t(place.status === "pending_review" ? "placeDataPending" : place.status === "stale" ? "placeDataStale" : "placeDataUnavailable")}</p>}
          {place.official_website_url && <a href={place.official_website_url} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-12 w-full items-center justify-center gap-2 rounded-xl border border-[var(--line)] bg-white px-4 text-sm font-semibold"><Building2 size={16} />{t("officialWebsite")}<ExternalLink size={13} /></a>}
          <div className="rounded-2xl bg-white p-4">
            {place.address && <section><h3 className="flex items-center gap-2 text-sm font-bold"><MapPin size={16} className="text-[var(--teal)]" />{t("address")}</h3>{primaryMapLink ? <a href={primaryMapLink.url} target="_blank" rel="noopener noreferrer" aria-label={`${place.address} — ${primaryMapLink.label} — ${t("openNew")}`} className="mt-2 flex min-h-11 items-center justify-between gap-3 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm font-semibold leading-6 text-[var(--teal-dark)] transition hover:bg-[var(--teal-soft)] hover:text-[var(--teal)]"><span>{place.address}</span><ExternalLink size={15} className="shrink-0" /></a> : <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{place.address}</p>}</section>}
            <section className={place.address ? "mt-4 border-t border-[var(--line)] pt-4" : ""}><h3 className="flex items-center gap-2 text-sm font-bold"><CalendarClock size={16} className="text-[var(--coral)]" />{t("openingHours")}</h3>{openingHourLines.length ? <ul className="mt-2 grid gap-1.5 text-sm text-[var(--muted)]">{openingHourLines.map((line) => <li key={line}>{line}</li>)}</ul> : <p className="mt-2 text-sm text-[var(--muted)]">{t("noOpeningHours")}</p>}</section>
            {showGoogleAttribution && <div className="mt-3 flex flex-wrap items-center gap-x-3 gap-y-1 border-t border-[var(--line)] pt-[10px] text-xs text-[#5e5e5e]"><span className="inline-flex px-[10px] pb-[5px]"><Image src="/google-maps-attribution-dark-gray.svg" alt="Google Maps" width={98} height={18} className="h-[18px] w-[98px]" /></span>{place.attribution.third_party.map((item) => item.providerUri ? <a key={`${item.provider}-${item.providerUri}`} href={item.providerUri} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-1 underline-offset-4 hover:underline">{item.provider || item.providerUri}<ExternalLink size={12} /></a> : item.provider ? <span key={item.provider}>{item.provider}</span> : null)}</div>}
          </div>
        </section>}
        <div className="mb-4 border-t border-[var(--line)] pt-5"><h3 className="flex items-center gap-2 text-lg font-bold"><BookOpenText size={18} className="text-[var(--teal)]" />{t("guides")}</h3><p className="mt-1 text-sm text-[var(--muted)]">{t("guideIntro")}</p></div>
        {loading && <div className="rounded-2xl bg-white p-6 text-sm text-[var(--muted)]">{t("guideLoading")}</div>}
        {error && <div role="alert" className="rounded-2xl bg-[var(--coral-soft)] p-6 text-sm">{t("guideError")}</div>}
        {empty && <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white p-7 text-center"><BookOpenText className="mx-auto text-[var(--teal)]" /><p className="mt-3 font-semibold">{t("strictEmpty")}</p></div>}
        {!loading && !error && data && <div className="grid gap-7">
          <section><h3 className="mb-3 flex items-center gap-2 text-lg font-bold"><Play size={18} className="text-red-600" />{t("videos")}</h3><div className="grid gap-3">{data.videos.length ? data.videos.map(guideCard) : <p className="rounded-2xl bg-white p-4 text-sm text-[var(--muted)]">{t("noVideos")}</p>}</div></section>
          <section><h3 className="mb-3 flex items-center gap-2 text-lg font-bold"><FileText size={18} className="text-[var(--teal)]" />{t("articles")}</h3><div className="grid gap-3">{data.articles.length ? data.articles.map(guideCard) : <p className="rounded-2xl bg-white p-4 text-sm text-[var(--muted)]">{t("noArticles")}</p>}</div></section>
          {data.other_languages_available && !otherLanguages && <button type="button" onClick={() => { setLoading(true); setError(false); setOtherLanguages(true); }} className="min-h-12 rounded-2xl border border-[var(--teal)] bg-white px-5 py-3 font-semibold text-[var(--teal)]">{t("otherLanguages")}<span className="mt-1 block text-xs font-normal text-[var(--muted)]">{t("otherLanguageNotice")}</span></button>}
        </div>}
      </div>
    </div>
  </div>;
}

export function HotspotExplorer() {
  const t = useTranslations("hotspots");
  const locale = useLocale();
  const [query, setQuery] = useState("");
  const [country, setCountry] = useState("");
  const [city, setCity] = useState("");
  const [role, setRole] = useState("");
  const [category, setCategory] = useState("");
  const [style, setStyle] = useState<"all" | "deep">("all");
  const [ranking, setRanking] = useState<RankingResponse | null>(null);
  const [sources, setSources] = useState<SourcesResponse | null>(null);
  const [facets, setFacets] = useState<FacetsResponse | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [filtersOpen, setFiltersOpen] = useState(false);
  const [selected, setSelected] = useState<RankedHotspot | null>(null);
  const detailTriggerRef = useRef<HTMLElement | null>(null);
  const [selectedRestaurants, setSelectedRestaurants] = useState<RankedHotspot | null>(null);
  const restaurantTriggerRef = useRef<HTMLElement | null>(null);
  const number = new Intl.NumberFormat(locale);

  async function load(append = false) {
    setLoading(true); setError("");
    const params = new URLSearchParams({ limit: "30", style });
    if (query.trim()) params.set("q", query.trim());
    if (country) params.set("country_code", country);
    if (city) params.set("destination_id", city);
    if (role) params.set("role", role);
    if (category) params.set("category", category);
    if (append && ranking?.next_cursor) params.set("after_rank", String(ranking.next_cursor));
    try {
      const result = await api<RankingResponse>(`/hotspots/rankings?${params}`);
      setRanking(append && ranking ? { ...result, items: [...ranking.items, ...result.items] } : result);
    } catch (reason) { setError((reason as Error).message); }
    finally { setLoading(false); }
  }

  useEffect(() => {
    const initial = new URLSearchParams(window.location.search);
    const initialCategory = initial.get("category") ?? "";
    const initialDestination = initial.get("destination_id") ?? "";
    const rankingParams = new URLSearchParams({ limit: "30" });
    if (initialCategory) {
      rankingParams.set("category", initialCategory);
    }
    if (initialDestination) {
      rankingParams.set("destination_id", initialDestination);
    }
    api<SourcesResponse>("/hotspots/sources").then(setSources).catch(() => undefined);
    api<FacetsResponse>("/hotspots/facets").then(setFacets).catch(() => undefined);
    api<RankingResponse>(`/hotspots/rankings?${rankingParams}`).then((result) => {
      setRanking(result);
      setCategory(initialCategory);
      setCity(initialDestination);
    }).catch((reason: Error) => setError(reason.message)).finally(() => setLoading(false));
  }, []);

  useEffect(() => {
    const closeOnBack = () => { setSelected(null); setSelectedRestaurants(null); };
    window.addEventListener("popstate", closeOnBack);
    return () => window.removeEventListener("popstate", closeOnBack);
  }, []);

  useEffect(() => {
    if (!selected && detailTriggerRef.current) {
      detailTriggerRef.current.focus();
      detailTriggerRef.current = null;
    }
  }, [selected]);

  useEffect(() => {
    if (!selectedRestaurants && restaurantTriggerRef.current) {
      restaurantTriggerRef.current.focus();
      restaurantTriggerRef.current = null;
    }
  }, [selectedRestaurants]);

  function openDetails(item: RankedHotspot) { detailTriggerRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null; window.history.pushState({ hotspotDetails: item.id }, ""); setSelected(item); }
  function closeDetails() {
    setSelected(null);
    if (window.history.state?.hotspotDetails) window.history.back();
  }
  function openRestaurants(item: RankedHotspot) { restaurantTriggerRef.current = document.activeElement instanceof HTMLElement ? document.activeElement : null; window.history.pushState({ hotspotRestaurants: item.id }, ""); setSelectedRestaurants(item); }
  function closeRestaurants() {
    setSelectedRestaurants(null);
    if (window.history.state?.hotspotRestaurants) window.history.back();
  }
  function percent(value: number | null) { return value === null ? t("noComparison") : `${value >= 0 ? "+" : ""}${Math.round(value * 100)}%`; }

  return <main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
    <section className="pb-7 pt-5 md:pb-9 md:pt-9">
      <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />{t("eyebrow")}</p>
      <div className="mt-3 flex flex-wrap items-end justify-between gap-4"><div><h1 className="text-3xl font-bold tracking-[-.035em] md:text-5xl">{t("title")}</h1><p className="mt-3 max-w-2xl leading-7 text-[var(--muted)]">{t("description")}</p></div><div className="rounded-2xl border border-[var(--line)] bg-white px-4 py-3 text-sm text-[var(--muted)]"><span className="font-semibold text-[var(--ink)]">{t("updated")}</span> {ranking?.observed_on || t("waiting")}</div></div>
    </section>
    <button type="button" onClick={() => setFiltersOpen(true)} className="mb-3 flex min-h-12 w-full items-center justify-between rounded-2xl border border-[var(--line)] bg-white px-4 font-semibold shadow-[var(--shadow-sm)] md:hidden"><span className="flex items-center gap-2"><SlidersHorizontal size={18} />{t("searchLabel")}</span><span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-1 text-xs text-[var(--teal-dark)]">{[country, city, role, category, style === "deep" ? style : ""].filter(Boolean).length}</span></button>
    {filtersOpen && <button type="button" aria-label={t("close")} onClick={() => setFiltersOpen(false)} className="fixed inset-0 z-[70] bg-slate-950/40 md:hidden" />}
    <form onSubmit={(event: FormEvent<HTMLFormElement>) => { event.preventDefault(); setFiltersOpen(false); void load(); }} aria-label={t("searchLabel")} className={`${filtersOpen ? "mobile-filter-sheet-open" : ""} mobile-filter-sheet grid gap-3 rounded-[1.75rem] border border-[var(--line)] bg-white p-4 shadow-[var(--shadow-lg)] md:grid-cols-[1fr_repeat(5,9rem)_auto] md:p-5`}>
      <div className="mb-1 flex items-center justify-between md:hidden"><strong>{t("searchLabel")}</strong><button type="button" onClick={() => setFiltersOpen(false)} aria-label={t("close")} className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]"><X size={19} /></button></div>
      <label className="relative"><span className="sr-only">{t("searchPlaceholder")}</span><Search className="pointer-events-none absolute left-4 top-3.5 text-[var(--muted)]" size={19} /><input value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t("searchPlaceholder")} className="h-12 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-11 pr-4 outline-none focus:border-[var(--teal)]" /></label>
      <select aria-label={t("allCountries")} value={country} onChange={(event) => { setCountry(event.target.value); setCity(""); }} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3"><option value="">{t("allCountries")}</option>{facets?.countries.map((item) => <option key={item.code} value={item.code}>{item.name} ({item.count})</option>)}</select>
      <select aria-label={t("allRoles")} value={role} onChange={(event) => { setRole(event.target.value); setCity(""); }} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3"><option value="">{t("allRoles")}</option><option value="primary">{t("primaryCities")}</option><option value="secondary">{t("secondaryCities")}</option><option value="extension">{t("extensionCities")}</option></select>
      <select aria-label={t("allStyles")} value={style} onChange={(event) => setStyle(event.target.value as "all" | "deep")} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3"><option value="all">{t("allStyles")}</option><option value="deep">{t("deepStyle")}</option></select>
      <select aria-label={t("allCities")} value={city} onChange={(event) => setCity(event.target.value)} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3"><option value="">{t("allCities")}</option>{(["primary", "secondary", "extension"] as const).map((groupRole) => { const cities = facets?.cities.filter((item) => (!country || item.country_code === country) && (!role || item.destination_role === role) && item.destination_role === groupRole) ?? []; return cities.length ? <optgroup key={groupRole} label={t(`${groupRole}Cities`)}>{cities.map((item) => <option key={item.destination_id} value={item.destination_id}>{item.name} ({item.count})</option>)}</optgroup> : null; })}</select>
      <select aria-label={t("allCategories")} value={category} onChange={(event) => setCategory(event.target.value)} className="h-12 rounded-xl border border-[var(--line)] bg-[var(--paper)] px-3">{categoryCodes.map((code) => <option key={code} value={code}>{code ? t(`categories.${code}`) : t("allCategories")}</option>)}</select>
      <button type="submit" className="h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white">{t("submit")}</button>
    </form>
    <div className="mt-7 grid gap-7 lg:grid-cols-[1fr_18rem]">
      <section aria-live="polite" aria-busy={loading}><div className="mb-4 flex items-center justify-between gap-4"><h2 className="flex items-center gap-2 text-xl font-bold"><BarChart3 size={20} className="text-[var(--coral)]" />{t("ranking")}</h2><p className="text-sm text-[var(--muted)]">{t("loaded", { shown: ranking?.items.length ?? 0, total: ranking?.total ?? 0 })}</p></div>
        {loading && <div className="rounded-3xl border border-[var(--line)] bg-white p-8 text-[var(--muted)]">{t("loading")}</div>}
        {!loading && error && <div role="alert" className="rounded-3xl bg-[var(--coral-soft)] p-6">{error}</div>}
        {!loading && !error && ranking?.items.length === 0 && <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white/70 p-8 text-center"><h3 className="font-bold">{t("emptyTitle")}</h3><p className="mt-2 text-sm text-[var(--muted)]">{t("emptyBody")}</p></div>}
        {!loading && !error && ranking && <ol className="grid gap-4 md:grid-cols-2">{ranking.items.map((item) => <li key={item.id} className={`travel-result-card travel-result-card-${item.category} relative overflow-hidden rounded-3xl border border-[var(--line)] bg-white p-5`}>
          <div className="flex items-start justify-between gap-4"><div className="flex gap-3"><span className="grid h-11 w-11 shrink-0 place-items-center rounded-2xl bg-[var(--teal-soft)] text-lg font-bold text-[var(--teal-dark)]">{item.rank}</span><div><h3 className="text-lg font-bold">{item.name}</h3>{item.local_name && item.local_name !== item.name && <p className="text-xs text-[var(--muted)]">{item.local_name}</p>}{item.map_links?.[0] ? <a href={item.map_links[0].url} target="_blank" rel="noopener noreferrer" aria-label={`${item.map_links[0].label}: ${item.name}`} className="mt-1 inline-flex min-h-11 items-center gap-1.5 text-sm font-semibold text-[var(--teal)] underline-offset-4 hover:underline"><MapPin size={14} />{item.city_name} · {t(`categories.${item.category}`)}<ExternalLink size={13} /></a> : <p className="mt-1 flex min-h-11 items-center gap-1.5 text-sm text-[var(--muted)]"><MapPin size={14} />{item.city_name} · {t(`categories.${item.category}`)}</p>}</div></div><div className="text-right"><strong className="text-2xl text-[var(--teal)]">{Math.round(item.score)}</strong><p className="text-xs text-[var(--muted)]">{t("score")}</p></div></div>
          <div className="mt-5 grid grid-cols-2 gap-3 rounded-2xl bg-[var(--paper)] p-4 text-sm"><div><p className="text-[var(--muted)]">{t("views30")}</p><p className="mt-1 font-semibold">{item.pageviews_30d === null ? t("pending") : number.format(item.pageviews_30d)}</p></div><div><p className="text-[var(--muted)]">{t("previous")}</p><p className="mt-1 flex items-center gap-1 font-semibold">{trendIcon(item)}{percent(item.growth_rate)}</p></div></div>
          <button type="button" onClick={() => openDetails(item)} className="mt-4 flex min-h-12 w-full items-center gap-3 rounded-2xl bg-[var(--teal)] px-4 py-3 text-left text-white shadow-sm transition hover:bg-[var(--teal-dark)]"><span className="grid h-8 w-8 place-items-center rounded-full bg-white/15"><BookOpenText size={17} /></span><span className="min-w-0 flex-1"><strong className="block text-sm">{t("placeDetails")}</strong><span className="block text-xs text-white/75">{t("guideCount", { articles: item.guide_counts?.article || 0, videos: item.guide_counts?.video || 0 })}</span></span><ExternalLink size={16} /></button>
          <button type="button" onClick={() => openRestaurants(item)} className="mt-2 flex min-h-12 w-full items-center gap-3 rounded-2xl border border-[var(--coral)] bg-[var(--coral-soft)] px-4 py-3 text-left text-[var(--ink)] transition hover:-translate-y-0.5 hover:shadow-sm"><span className="grid h-8 w-8 place-items-center rounded-full bg-white text-[var(--coral)]"><UtensilsCrossed size={17} /></span><span className="min-w-0 flex-1"><strong className="block text-sm">{t("nearbyRestaurants")}</strong><span className="block text-xs text-[var(--muted)]">{t("nearbyRestaurantsDetail")}</span></span><span className="text-xs font-bold text-[var(--coral)]">5–10 km</span></button>
          <TravelCardActions type="hotspot" id={item.id} title={item.name} selectionPath={`/hotspots/${item.id}/trip-selections`} />
          <div className="mt-4 flex flex-wrap items-center gap-2">{item.destination_role === "secondary" && <span className="rounded-full bg-sky-100 px-2.5 py-1 text-xs font-semibold text-sky-900">{t("secondaryTag")}</span>}{item.is_cross_city && <span className="rounded-full bg-violet-100 px-2.5 py-1 text-xs font-semibold text-violet-900">{t("crossCityTag")}</span>}{item.is_deep_travel && <span className="rounded-full bg-amber-100 px-2.5 py-1 text-xs font-semibold text-amber-900">{t("deep")}</span>}{item.depth_kind && <span className="rounded-full border border-amber-300 px-2.5 py-1 text-xs text-amber-900">{item.depth_kind === "day_trip" ? t("dayTrip") : t("urbanLocal")}</span>}{item.source_urls[0] && <a href={item.source_urls[0]} target="_blank" rel="noopener noreferrer" className="ml-auto text-xs font-semibold text-[var(--teal)]">{t("source")}</a>}</div>
          {item.is_deep_travel && item.access_minutes && item.recommended_duration_minutes && <p className="mt-3 rounded-xl bg-amber-50 px-3 py-2 text-xs text-amber-950">{t("depthDetail", { access: item.access_minutes, duration: item.recommended_duration_minutes })}</p>}
        </li>)}</ol>}
        {!loading && !error && ranking?.has_more && <div className="mt-6 text-center"><button type="button" onClick={() => void load(true)} className="rounded-xl border border-[var(--teal)] bg-white px-6 py-3 font-semibold text-[var(--teal)]">{t("loadMore")}</button></div>}
      </section>
      <aside className="h-fit rounded-3xl border border-[var(--line)] bg-white/80 p-5 lg:sticky lg:top-5"><h2 className="flex items-center gap-2 font-bold"><Database size={18} className="text-[var(--teal)]" />{t("sources")}</h2><div className="mt-4 grid gap-4">{sources?.sources.map((source) => <article key={source.id} className="border-b border-[var(--line)] pb-4 last:border-0"><div className="flex items-center justify-between gap-2"><h3 className="text-sm font-semibold">{t(`sourceNames.${source.id}`)}</h3><span className="rounded-full bg-[var(--paper)] px-2 py-1 text-[11px] text-[var(--muted)]">{source.status}</span></div></article>)}</div><p className="mt-5 border-t border-[var(--line)] pt-4 text-xs leading-5 text-[var(--muted)]">{t("plannerNote")}</p></aside>
    </div>
    {selected && <PlaceDetailsPanel hotspot={selected} onClose={closeDetails} />}
    {selectedRestaurants && <HotspotRestaurantsPanel hotspot={selectedRestaurants} onClose={closeRestaurants} />}
  </main>;
}
