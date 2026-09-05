"use client";

import {
  CalendarPlus,
  CarTaxiFront,
  ChevronDown,
  Clock3,
  ExternalLink,
  Globe2,
  Heart,
  MapPinned,
  RefreshCw,
  ShieldCheck,
  Star,
  UtensilsCrossed,
  X,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import {
  KeyboardEvent,
  TouchEvent,
  useCallback,
  useEffect,
  useMemo,
  useRef,
  useState,
} from "react";
import { api, ApiError } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";
import { Link } from "@/i18n/navigation";

type RestaurantSort = "recommended" | "rating" | "reviews" | "distance";
type EditorialSource = {
  type: string;
  scope?: string;
  title: string;
  url: string;
  claims: string[];
  verified_at: string;
};
type Editorial = {
  name: string;
  local_name: string | null;
  address: string | null;
  official_website_url: string | null;
  uber_url: string | null;
  source_kind: "restaurant_editorial" | "food_merchant";
  sources: EditorialSource[];
  verified_at: string | null;
};
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
  primary_type: string | null;
  observed_at: string;
  editorial: Editorial | null;
};
type Coverage = {
  status:
    | "not_started"
    | "queued"
    | "running"
    | "quota_paused"
    | "partial"
    | "completed"
    | "failed";
  cells_completed: number;
  cells_total: number;
  candidate_count: number;
};
type RestaurantResponse = {
  items: Restaurant[];
  next_cursor: number | null;
  coverage: Coverage;
  attribution: string;
};
type TripOption = {
  trip_id: string;
  name: string;
  version: number;
  start_date: string;
  end_date: string;
};

const PREFERENCE_KEY = "travel-scanner:restaurant-preferences:v1";

function sortRestaurants(items: Restaurant[], sort: RestaurantSort) {
  return [...items].sort((left, right) => {
    if (sort === "rating") {
      return (
        right.rating - left.rating ||
        right.review_count - left.review_count ||
        left.distance_km - right.distance_km
      );
    }
    if (sort === "reviews") {
      return (
        right.review_count - left.review_count ||
        right.rating - left.rating ||
        left.distance_km - right.distance_km
      );
    }
    if (sort === "distance") {
      return left.distance_km - right.distance_km || right.recommendation_score - left.recommendation_score;
    }
    return (
      right.recommendation_score - left.recommendation_score ||
      right.review_count - left.review_count ||
      left.distance_km - right.distance_km
    );
  });
}

export function HotspotRestaurantsPanel({
  hotspot,
  loginHref,
  onClose,
}: {
  hotspot: { id: string; name: string };
  loginHref?: string;
  onClose: () => void;
}) {
  const t = useTranslations("restaurants");
  const locale = useLocale();
  const [radius, setRadius] = useState<5 | 10>(5);
  const [sort, setSort] = useState<RestaurantSort>("recommended");
  const [preferencesReady, setPreferencesReady] = useState(false);
  const [data, setData] = useState<RestaurantResponse | null>(null);
  const [items, setItems] = useState<Restaurant[]>([]);
  const [favorites, setFavorites] = useState<Set<string>>(new Set());
  const [loading, setLoading] = useState(true);
  const [loadingMore, setLoadingMore] = useState(false);
  const [error, setError] = useState("");
  const [authRequired, setAuthRequired] = useState(false);
  const [actionMessage, setActionMessage] = useState<{ text: string; tone: "success" | "error" } | null>(null);
  const [tripRestaurant, setTripRestaurant] = useState<Restaurant | null>(null);
  const [tripOptions, setTripOptions] = useState<TripOption[]>([]);
  const [tripId, setTripId] = useState("");
  const [tripDate, setTripDate] = useState("");
  const [mealRole, setMealRole] = useState<"lunch" | "dinner">("lunch");
  const [tripSaving, setTripSaving] = useState(false);
  const dialogRef = useRef<HTMLDivElement>(null);
  const closeRef = useRef<HTMLButtonElement>(null);
  const touchStart = useRef<number | null>(null);
  const initialPlaceIds = useRef<string[]>([]);
  const number = new Intl.NumberFormat(locale);
  const date = new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" });

  useEffect(() => {
    const timer = window.setTimeout(() => {
      try {
        const stored = JSON.parse(localStorage.getItem(PREFERENCE_KEY) || "{}") as {
          radius?: number;
          sort?: RestaurantSort;
        };
        if (stored.radius === 5 || stored.radius === 10) setRadius(stored.radius);
        if (["recommended", "rating", "reviews", "distance"].includes(stored.sort || "")) {
          setSort(stored.sort as RestaurantSort);
        }
      } catch {
        localStorage.removeItem(PREFERENCE_KEY);
      }
      setPreferencesReady(true);
    }, 0);
    return () => window.clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (!preferencesReady) return;
    localStorage.setItem(PREFERENCE_KEY, JSON.stringify({ radius, sort }));
  }, [preferencesReady, radius, sort]);

  const search = useCallback(
    async (cursor?: number) => {
      if (cursor === undefined) setLoading(true);
      else setLoadingMore(true);
      setError("");
      setAuthRequired(false);
      try {
        const result = await api<RestaurantResponse>(`/hotspots/${hotspot.id}/restaurant-searches`, {
          method: "POST",
          headers: { "Idempotency-Key": crypto.randomUUID() },
          body: JSON.stringify({
            radius_km: radius,
            sort: "recommended",
            ...(cursor === undefined
              ? {}
              : { cursor, exclude_place_ids: initialPlaceIds.current }),
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
        if (reason instanceof ApiError && reason.status === 401) {
          setAuthRequired(true);
        } else {
          setError((reason as Error).message);
        }
      } finally {
        setLoading(false);
        setLoadingMore(false);
      }
    },
    [hotspot.id, radius],
  );

  useEffect(() => {
    if (!preferencesReady) return;
    const timer = window.setTimeout(() => void search(), 0);
    return () => window.clearTimeout(timer);
  }, [preferencesReady, search]);

  useEffect(() => {
    void api<{ place_ids: string[] }>("/restaurants/favorites")
      .then((result) => setFavorites(new Set(result.place_ids)))
      .catch((reason) => {
        if (!(reason instanceof ApiError) || reason.status !== 401) {
          setActionMessage({ text: (reason as Error).message, tone: "error" });
        }
      });
  }, []);

  useEffect(() => {
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    closeRef.current?.focus();
    const closeOnEscape = (event: globalThis.KeyboardEvent) => {
      if (event.key === "Escape") {
        if (tripRestaurant) setTripRestaurant(null);
        else onClose();
      }
    };
    document.addEventListener("keydown", closeOnEscape);
    return () => {
      document.body.style.overflow = previousOverflow;
      document.removeEventListener("keydown", closeOnEscape);
    };
  }, [onClose, tripRestaurant]);

  function trapFocus(event: KeyboardEvent<HTMLDivElement>) {
    if (event.key !== "Tab") return;
    const nodes = dialogRef.current?.querySelectorAll<HTMLElement>(
      "button:not([disabled]), a[href], select:not([disabled]), input:not([disabled])",
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
    if (touchStart.current !== null && end !== undefined && end - touchStart.current > 90) {
      onClose();
    }
    touchStart.current = null;
  }

  async function toggleFavorite(restaurant: Restaurant) {
    const wasFavorite = favorites.has(restaurant.place_id);
    setActionMessage(null);
    setFavorites((current) => {
      const next = new Set(current);
      if (wasFavorite) next.delete(restaurant.place_id);
      else next.add(restaurant.place_id);
      return next;
    });
    try {
      await api(`/restaurants/favorites/${restaurant.place_id}`, {
        method: wasFavorite ? "DELETE" : "PUT",
      });
      setActionMessage({ text: t(wasFavorite ? "favoriteRemoved" : "favoriteSaved"), tone: "success" });
    } catch (reason) {
      setFavorites((current) => {
        const next = new Set(current);
        if (wasFavorite) next.add(restaurant.place_id);
        else next.delete(restaurant.place_id);
        return next;
      });
      setActionMessage({ text: (reason as Error).message, tone: "error" });
    }
  }

  async function openTripPicker(restaurant: Restaurant) {
    setActionMessage(null);
    try {
      const result = await api<{ items: TripOption[] }>("/restaurants/trip-options");
      setTripOptions(result.items);
      setTripRestaurant(restaurant);
      const first = result.items[0];
      setTripId(first?.trip_id || "");
      setTripDate(first?.start_date || "");
    } catch (reason) {
      setActionMessage({ text: (reason as Error).message, tone: "error" });
    }
  }

  async function saveToTrip() {
    const option = tripOptions.find((item) => item.trip_id === tripId);
    if (!tripRestaurant || !option || !tripDate) return;
    setTripSaving(true);
    try {
      await api(`/restaurants/${tripRestaurant.place_id}/trip-selections`, {
        method: "POST",
        body: JSON.stringify({
          trip_id: option.trip_id,
          version: option.version,
          day_date: tripDate,
          meal_role: mealRole,
        }),
      });
      setActionMessage({ text: t("tripSaved", { trip: option.name }), tone: "success" });
      setTripRestaurant(null);
    } catch (reason) {
      setActionMessage({ text: (reason as Error).message, tone: "error" });
    } finally {
      setTripSaving(false);
    }
  }

  const coveragePercent = data?.coverage.cells_total
    ? Math.min(100, Math.round((data.coverage.cells_completed / data.coverage.cells_total) * 100))
    : 0;
  const sortedItems = useMemo(() => sortRestaurants(items, sort), [items, sort]);

  return (
    <div className="fixed inset-0 z-[80] bg-slate-950/45 backdrop-blur-sm" role="presentation" onMouseDown={(event) => { if (event.target === event.currentTarget) onClose(); }}>
      <div ref={dialogRef} role="dialog" aria-modal="true" aria-labelledby="restaurant-panel-title" onKeyDown={trapFocus} onTouchStart={handleTouchStart} onTouchEnd={handleTouchEnd} className="absolute inset-x-0 bottom-0 flex h-[94dvh] flex-col rounded-t-[2rem] bg-[var(--paper)] shadow-2xl md:inset-y-0 md:left-auto md:h-full md:w-[38rem] md:rounded-none md:rounded-l-[2rem]">
        <div className="mx-auto mt-2 h-1.5 w-11 rounded-full bg-slate-300 md:hidden" />
        <header className="border-b border-[var(--line)] px-5 pb-4 pt-4 md:px-7 md:pt-7">
          <div className="flex items-start gap-3"><div className="min-w-0 flex-1"><p className="flex items-center gap-2 text-xs font-bold uppercase tracking-[.16em] text-[var(--coral)]"><UtensilsCrossed size={15} />{t("eyebrow")}</p><h2 id="restaurant-panel-title" className="mt-1 text-2xl font-bold tracking-tight">{t("title", { name: hotspot.name })}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t("threshold")}</p></div><button ref={closeRef} type="button" onClick={onClose} aria-label={t("close")} className="grid h-11 w-11 shrink-0 place-items-center rounded-full border border-[var(--line)] bg-white"><X /></button></div>
          <div className="mt-4 grid grid-cols-2 gap-2"><label className="text-xs font-semibold text-[var(--muted)]">{t("radius")}<select value={radius} onChange={(event) => setRadius(Number(event.target.value) as 5 | 10)} className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 text-sm text-[var(--ink)]"><option value={5}>{t("radiusOption", { radius: 5 })}</option><option value={10}>{t("radiusOption", { radius: 10 })}</option></select></label><label className="text-xs font-semibold text-[var(--muted)]">{t("sortLabel")}<select value={sort} onChange={(event) => setSort(event.target.value as RestaurantSort)} className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3 text-sm text-[var(--ink)]"><option value="recommended">{t("sort.recommended")}</option><option value="rating">{t("sort.rating")}</option><option value="reviews">{t("sort.reviews")}</option><option value="distance">{t("sort.distance")}</option></select></label></div>
          <p className="mt-2 text-[11px] leading-5 text-[var(--muted)]">{t("preferenceSaved")}</p>
        </header>
        <div className="overflow-y-auto overscroll-contain px-5 pb-[calc(1.5rem+env(safe-area-inset-bottom))] pt-5 md:px-7">
          {data && <section className="mb-4 rounded-2xl border border-[var(--line)] bg-white p-4 text-xs"><div className="flex items-center justify-between gap-3"><strong>{t("coverage.title")}</strong><span className="rounded-full bg-[var(--teal-soft)] px-2 py-1 font-semibold text-[var(--teal-dark)]">{t(`coverage.${data.coverage.status}`)}</span></div><div className="mt-3 h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-[var(--teal)]" style={{ width: `${coveragePercent}%` }} /></div><p className="mt-2 text-[var(--muted)]">{t("coverage.detail", { candidates: data.coverage.candidate_count, completed: data.coverage.cells_completed, total: data.coverage.cells_total })}</p></section>}
          {loading && <div className="rounded-2xl bg-white p-7 text-sm text-[var(--muted)]">{t("loading")}</div>}
          {!loading && authRequired && <div role="alert" className="rounded-2xl bg-[var(--coral-soft)] p-5 text-sm"><p className="font-bold">{t("loginRequiredTitle")}</p><p className="mt-2 leading-6">{t("loginRequiredBody")}</p><Link href={loginHref || "/login"} className="mt-3 inline-flex min-h-11 items-center rounded-xl bg-white px-4 font-semibold">{t("loginAction")}</Link></div>}
          {!loading && !authRequired && error && <div role="alert" className="rounded-2xl bg-[var(--coral-soft)] p-5 text-sm"><p>{error}</p><button type="button" onClick={() => void search()} className="mt-3 inline-flex min-h-11 items-center gap-2 rounded-xl bg-white px-4 font-semibold"><RefreshCw size={16} />{t("retry")}</button></div>}
          {!loading && !authRequired && !error && !items.length && <div className="rounded-3xl border border-dashed border-[var(--line)] bg-white p-8 text-center"><UtensilsCrossed className="mx-auto text-[var(--coral)]" /><h3 className="mt-3 font-bold">{t("emptyTitle")}</h3><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("emptyBody")}</p></div>}
          {!loading && !authRequired && !error && sortedItems.length > 0 && <ol className="grid gap-3">{sortedItems.map((restaurant, index) => {
            const ownedWebsite = restaurant.editorial?.official_website_url;
            const website = ownedWebsite || restaurant.official_website_url;
            return <li key={restaurant.place_id} className="rounded-3xl border border-[var(--line)] bg-white p-4 shadow-sm">
              <div className="flex items-start gap-3"><span className="grid h-9 w-9 shrink-0 place-items-center rounded-xl bg-[var(--coral-soft)] text-sm font-bold text-[var(--coral)]">{index + 1}</span><div className="min-w-0 flex-1"><h3 className="font-bold leading-5">{restaurant.editorial?.name || restaurant.name}</h3><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{restaurant.editorial?.address || restaurant.address}</p>{restaurant.editorial && <p className="mt-2 inline-flex items-center gap-1 rounded-full bg-emerald-50 px-2 py-1 text-[10px] font-semibold text-emerald-800"><ShieldCheck size={12} />{t("verifiedEditorial")}</p>}</div><span className="whitespace-nowrap rounded-full bg-amber-50 px-2.5 py-1 text-sm font-bold text-amber-800"><Star className="mr-1 inline" size={14} fill="currentColor" />{restaurant.rating.toFixed(1)}</span></div>
              <div className="mt-3 grid grid-cols-3 gap-2 text-center text-xs"><div className="rounded-xl bg-[var(--paper)] p-2"><strong className="block text-sm">{number.format(restaurant.review_count)}</strong><span className="text-[var(--muted)]">{t("reviews")}</span></div><div className="rounded-xl bg-[var(--paper)] p-2"><strong className="block text-sm">{restaurant.distance_km.toFixed(1)} km</strong><span className="text-[var(--muted)]">{t("distance")}</span></div><div className="rounded-xl bg-[var(--paper)] p-2"><strong className={restaurant.open_now === true ? "block text-sm text-emerald-700" : "block text-sm"}>{restaurant.open_now === null ? t("hoursUnknown") : restaurant.open_now ? t("openNow") : t("closedNow")}</strong><span className="text-[var(--muted)]">{t("liveStatus")}</span></div></div>
              {restaurant.opening_hours.length > 0 && <details className="mt-3 rounded-xl border border-[var(--line)] px-3 py-2 text-xs"><summary className="flex min-h-7 cursor-pointer list-none items-center gap-2 font-semibold"><Clock3 size={14} className="text-[var(--teal)]" />{t("openingHours")}<ChevronDown size={14} className="ml-auto" /></summary><div className="mt-2 grid gap-1 border-t border-[var(--line)] pt-2 text-[var(--muted)]">{restaurant.opening_hours.map((line) => <p key={line}>{line}</p>)}</div></details>}
              <div className="mt-3 rounded-xl bg-[var(--paper)] px-3 py-2 text-xs leading-5 text-[var(--muted)]"><p className="flex items-center gap-2 font-mono"><MapPinned size={14} />{restaurant.latitude.toFixed(5)}, {restaurant.longitude.toFixed(5)}</p></div>
              <div className="mt-3 grid grid-cols-2 gap-2"><button type="button" onClick={() => void toggleFavorite(restaurant)} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"><Heart size={16} fill={favorites.has(restaurant.place_id) ? "currentColor" : "none"} className={favorites.has(restaurant.place_id) ? "text-[var(--coral)]" : ""} />{t(favorites.has(restaurant.place_id) ? "favorited" : "favorite")}</button><button type="button" onClick={() => void openTripPicker(restaurant)} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"><CalendarPlus size={16} />{t("addToTrip")}</button>{restaurant.google_maps_url && <a href={safeExternalHref(restaurant.google_maps_url)} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-3 text-sm font-semibold text-white"><MapPinned size={16} />{t("openMap")}<ExternalLink size={13} /></a>}{restaurant.editorial?.uber_url && <a href={safeExternalHref(restaurant.editorial.uber_url)} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-3 text-sm font-semibold text-white"><CarTaxiFront size={16} />{t("openUber")}<ExternalLink size={13} /></a>}{website && <a href={safeExternalHref(website)} target="_blank" rel="noopener noreferrer" className="col-span-2 inline-flex min-h-11 items-center justify-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"><Globe2 size={16} />{t(ownedWebsite ? "verifiedWebsite" : "websiteLive")}<ExternalLink size={13} /></a>}</div>
              {restaurant.editorial?.sources.length ? <details className="mt-3 text-xs"><summary className="cursor-pointer font-semibold text-[var(--teal)]">{t("sourceEvidence", { count: restaurant.editorial.sources.length })}</summary><ul className="mt-2 grid gap-1">{restaurant.editorial.sources.map((source) => <li key={source.url}><a href={safeExternalHref(source.url)} target="_blank" rel="noopener noreferrer" className="inline-flex items-center gap-1 underline underline-offset-2">{source.title}<ExternalLink size={11} /></a></li>)}</ul></details> : null}
              <p className="mt-3 text-[10px] text-[var(--muted)]">{t("liveObserved", { time: date.format(new Date(restaurant.observed_at)) })}</p>
            </li>;
          })}</ol>}
          {actionMessage && <p role={actionMessage.tone === "error" ? "alert" : "status"} className={`sticky bottom-2 z-10 mt-3 rounded-xl px-4 py-3 text-sm shadow-lg ${actionMessage.tone === "error" ? "bg-red-50 text-red-800" : "bg-[var(--teal-soft)] text-[var(--teal-dark)]"}`}>{actionMessage.text}</p>}
          {!loading && !error && data?.next_cursor !== null && data?.next_cursor !== undefined && <button type="button" disabled={loadingMore} onClick={() => void search(data.next_cursor ?? undefined)} className="mt-4 flex min-h-12 w-full items-center justify-center gap-2 rounded-2xl border border-[var(--teal)] bg-white font-semibold text-[var(--teal)] disabled:opacity-50">{loadingMore && <RefreshCw size={16} className="animate-spin" />}{t("loadMore")}</button>}
          {data && <p className="mt-5 text-center text-xs leading-5 text-[var(--muted)]">{t("attributionPrefix")} <span translate="no" className="whitespace-nowrap font-normal">{data.attribution}</span><br />{t("storageNotice")}</p>}
        </div>
        {tripRestaurant && <div className="absolute inset-0 z-10 flex items-end bg-slate-950/35 p-3 md:items-center md:justify-center" role="dialog" aria-modal="true" aria-label={t("tripPickerTitle")}><div className="w-full rounded-[1.75rem] bg-white p-5 shadow-2xl md:max-w-md"><div className="flex items-center justify-between gap-3"><div><p className="text-xs font-bold text-[var(--teal)]">{t("addToTrip")}</p><h3 className="mt-1 text-xl font-bold">{tripRestaurant.editorial?.name || tripRestaurant.name}</h3></div><button type="button" onClick={() => setTripRestaurant(null)} className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]" aria-label={t("closeTripPicker")}><X size={18} /></button></div>{tripOptions.length ? <div className="mt-5 grid gap-3"><label className="text-sm font-semibold">{t("tripLabel")}<select value={tripId} onChange={(event) => { const next = tripOptions.find((item) => item.trip_id === event.target.value); setTripId(event.target.value); setTripDate(next?.start_date || ""); }} className="mt-1 h-12 w-full rounded-xl border border-[var(--line)] px-3">{tripOptions.map((item) => <option key={item.trip_id} value={item.trip_id}>{item.name}</option>)}</select></label><label className="text-sm font-semibold">{t("dateLabel")}<input type="date" value={tripDate} min={tripOptions.find((item) => item.trip_id === tripId)?.start_date} max={tripOptions.find((item) => item.trip_id === tripId)?.end_date} onChange={(event) => setTripDate(event.target.value)} className="mt-1 h-12 w-full rounded-xl border border-[var(--line)] px-3" /></label><label className="text-sm font-semibold">{t("mealLabel")}<select value={mealRole} onChange={(event) => setMealRole(event.target.value as "lunch" | "dinner")} className="mt-1 h-12 w-full rounded-xl border border-[var(--line)] px-3"><option value="lunch">{t("lunch")}</option><option value="dinner">{t("dinner")}</option></select></label><button type="button" disabled={tripSaving || !tripDate} onClick={() => void saveToTrip()} className="mt-2 min-h-12 rounded-xl bg-[var(--ink)] px-4 font-semibold text-white disabled:opacity-50">{tripSaving ? t("savingTrip") : t("confirmTrip")}</button></div> : <p className="mt-5 rounded-xl bg-[var(--paper)] p-4 text-sm text-[var(--muted)]">{t("noTrips")}</p>}</div></div>}
      </div>
    </div>
  );
}
