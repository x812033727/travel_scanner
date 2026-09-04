"use client";

import { ArrowLeft, ArrowRight, BedDouble, Check, CircleAlert, ExternalLink, Loader2, MapPin, RefreshCw, Star } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";
import { hotelNightlyPrice, hotelStarRating, type HotelOfferView } from "@/components/hotel-offer-card";
import { api, formatCurrency } from "@/lib/api";
import { activeLocale } from "@/lib/locale-format";

export type StayArea = {
  code: string;
  name: string;
  latitude: number;
  longitude: number;
  radius_km: number;
  is_day_trip: boolean;
  score: number;
  item_count: number;
  dwell_minutes: number;
  day_count: number;
  sample_titles: string[];
  reasons: string[];
};

export type StayAreasResponse = {
  trip_id: string;
  version: number;
  destination_name?: string | null;
  city_code?: string | null;
  status: "recommended" | "low_evidence" | "no_evidence" | "unsupported";
  pricing: { available: boolean; provider?: string | null; mode?: string | null; message?: string | null };
  current_lodging_area_code?: string | null;
  located_item_count: number;
  unassigned_item_count: number;
  excluded_extension: Record<string, number>;
  warnings: string[];
  areas: StayArea[];
};

export type StayPartner = {
  partner: string;
  display_name: string;
  kind: "deep_link" | "hotel_search" | "area_search";
  cta?: string;
};

export type StayHotel = HotelOfferView & {
  hotel_id: string;
  hotel_name: string;
  provider: string;
  latitude: number;
  longitude: number;
  currency: string;
  nights: number;
  distance_km: number;
  in_area: boolean;
  is_current_lodging: boolean;
  preference_gaps: string[];
  partners: StayPartner[];
  offer_count?: number;
  price_estimate_unavailable?: boolean;
  original_currency?: string | null;
  original_total_price?: number | string | null;
};

export type StayHotelsResponse = {
  trip_id: string;
  version: number;
  area: { code: string; name: string; latitude: number; longitude: number; radius_km: number };
  check_in?: string | null;
  check_out?: string | null;
  nights: number;
  date_notes: string[];
  travelers?: { adults: number; children: number; rooms: number } | null;
  warnings: string[];
  pricing: {
    status: string;
    provider?: string | null;
    message?: string | null;
    retrieved_at?: string | null;
    expires_at?: string | null;
    cached?: boolean;
    is_fallback?: boolean;
  };
  filters: {
    applied: Record<string, unknown>;
    relaxed: Array<{ code: string; label: string }>;
    excluded_by_hard_filter: number;
  };
  hotels: StayHotel[];
  nearby: StayHotel[];
  area_partners: StayPartner[];
  disclosure: string;
};

export type StaySelectResult = "ok" | "expired" | "error";

type SortMode = "price" | "rating" | "distance";
type Tone = "neutral" | "teal" | "warn";

const PRICED_STATUSES = new Set(["live", "test", "mock"]);
const KNOWN_STATUSES = new Set(["live", "test", "mock", "not_configured", "unavailable", "timeout", "dates_missing", "dates_past", "empty"]);
const KNOWN_REASONS = new Set(["most_items", "most_days", "central", "day_trip_zone", "destination_default", "current_lodging"]);
const KNOWN_RELAXED = new Set(["breakfast", "refundable", "station_walk", "review_count", "review_score", "star_rating", "preferred_areas", "nightly_min", "nightly_max"]);
const KNOWN_DATE_NOTES = new Set(["checkin_moved_to_today", "assumed_one_night", "stay_truncated"]);
const KNOWN_WARNINGS = new Set(["children_ages_missing"]);
const CLOCK_TICK_MS = 15_000;

const toneClass: Record<Tone, string> = {
  neutral: "border-[var(--line)] bg-[var(--paper)] text-[var(--ink)]",
  teal: "border-transparent bg-[var(--teal-soft)] text-[var(--teal-dark)]",
  warn: "border-transparent bg-[var(--coral-soft)] text-[var(--coral)]",
};

function number(value: unknown) {
  const parsed = Number(value ?? 0);
  return Number.isFinite(parsed) ? parsed : 0;
}

function sortHotels(hotels: StayHotel[], mode: SortMode) {
  const price = (hotel: StayHotel) => hotelNightlyPrice(hotel);
  return [...hotels].sort((a, b) => {
    if (mode === "rating") {
      return (number(b.review_score) || number(b.rating)) - (number(a.review_score) || number(a.rating)) || price(a) - price(b);
    }
    if (mode === "distance") return a.distance_km - b.distance_km || price(a) - price(b);
    return Number(Boolean(a.price_estimate_unavailable)) - Number(Boolean(b.price_estimate_unavailable))
      || Number(a.preference_gaps.length > 0) - Number(b.preference_gaps.length > 0)
      || price(a) - price(b);
  });
}

function Notice({ tone = "neutral", children }: { tone?: Tone; children: ReactNode }) {
  return <div className={`flex items-start gap-2 rounded-2xl border px-4 py-3 text-sm leading-6 ${toneClass[tone]}`}><CircleAlert size={16} className="mt-1 shrink-0" />{children}</div>;
}

function Chip({ tone = "neutral", children }: { tone?: Tone; children: ReactNode }) {
  return <span className={`flex items-center gap-1 rounded-full border px-2.5 py-1 text-xs font-semibold ${toneClass[tone]}`}>{children}</span>;
}

function PartnerButton({ tripId, areaCode, partner, areaName, hotelId, disabled }: { tripId: string; areaCode: string; partner: StayPartner; areaName: string; hotelId?: string; disabled?: boolean }) {
  const t = useTranslations("stayAreas");
  const params = new URLSearchParams({ partner: partner.partner });
  if (hotelId) params.set("hotel_id", hotelId);
  return <form action={`/api/travel/trips/${tripId}/stay-areas/${areaCode}/clickout?${params.toString()}`} method="post" target="_blank" className="shrink-0">
    <button type="submit" disabled={disabled} className="flex min-h-11 items-center gap-1.5 rounded-xl border border-[var(--teal)] px-3 text-xs font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)] disabled:opacity-40">
      {t(`partner.${partner.kind}`, { partner: partner.display_name, area: areaName })}<ExternalLink size={13} />
    </button>
  </form>;
}

function StayHotelCard({ hotel, areaName, areaCode, tripId, busy, expired, onSelect }: { hotel: StayHotel; areaName: string; areaCode: string; tripId: string; busy: boolean; expired: boolean; onSelect: () => void }) {
  const t = useTranslations("stayAreas");
  const nightly = hotelNightlyPrice(hotel);
  const stars = hotelStarRating(hotel);
  const reviewScore = number(hotel.review_score);
  const reviewCount = number(hotel.review_count);
  const currency = hotel.currency || "TWD";
  const address = typeof hotel.address === "string" ? hotel.address : "";
  const gaps = hotel.preference_gaps.filter((code) => KNOWN_RELAXED.has(code));
  const roomCount = hotel.offer_count || 1;
  return <article className="planner-tool-card">
    <div className="flex items-start justify-between gap-3">
      <div className="min-w-0">
        <h4 className="text-base font-bold leading-snug">{hotel.hotel_name}</h4>
        {address && <p className="mt-1 flex items-start gap-1 text-xs text-[var(--muted)]"><MapPin size={13} className="mt-0.5 shrink-0" />{address}</p>}
      </div>
      <div className="shrink-0 text-right">
        <strong className="block text-lg">{formatCurrency(nightly, currency)}</strong>
        <span className="text-xs text-[var(--muted)]">{t("hotel.perNight")}</span>
        {hotel.price_estimate_unavailable && <span className="mt-1 block rounded-full bg-[var(--coral-soft)] px-2 py-0.5 text-[.68rem] font-semibold text-[var(--coral)]">{t("hotel.estimateUnavailable")}</span>}
        {hotel.original_currency && !hotel.price_estimate_unavailable && <span className="mt-1 block text-[.68rem] text-[var(--muted)]">{t("hotel.converted", { currency: hotel.original_currency })}</span>}
      </div>
    </div>
    <div className="mt-3 flex flex-wrap gap-2">
      {stars > 0 && <Chip><Star size={12} fill="currentColor" />{t("hotel.stars", { stars: stars.toFixed(0) })}</Chip>}
      {reviewScore > 0 && <Chip>{t("hotel.reviews", { score: reviewScore.toFixed(1) })}{reviewCount ? ` (${t("hotel.reviewCount", { count: reviewCount.toLocaleString(activeLocale()) })})` : ""}</Chip>}
      <Chip><MapPin size={12} />{t("hotel.distance", { area: areaName, km: hotel.distance_km.toFixed(1) })}</Chip>
      {hotel.breakfast_included && <Chip tone="teal"><Check size={12} />{t("hotel.breakfast")}</Chip>}
      <Chip tone={hotel.refundable ? "teal" : "neutral"}>{hotel.refundable ? t("hotel.refundable") : t("hotel.refundUnknown")}</Chip>
      {roomCount > 1 && <Chip><BedDouble size={12} />{t("hotel.moreRooms", { count: roomCount - 1 })}</Chip>}
    </div>
    {gaps.length > 0 && <p className="mt-2 text-xs font-semibold text-[var(--coral)]">{t("hotel.gaps", { labels: gaps.map((code) => t(`relaxed.${code}`)).join(", ") })}</p>}
    <div className="mt-3 flex flex-wrap gap-2">
      <button type="button" onClick={onSelect} disabled={busy || expired || hotel.is_current_lodging} className="planner-system-primary">
        {busy ? <Loader2 size={15} className="animate-spin" /> : <Check size={15} />}{hotel.is_current_lodging ? t("hotel.current") : t("hotel.choose")}
      </button>
      {hotel.partners.map((partner) => <PartnerButton key={partner.partner} tripId={tripId} areaCode={areaCode} partner={partner} areaName={areaName} hotelId={hotel.hotel_id} disabled={expired} />)}
    </div>
  </article>;
}

export function StayAreaFlow({ tripId, busy, onSelectHotel, onManualLodging }: {
  tripId: string;
  busy: boolean;
  onSelectHotel: (area: StayArea, hotel: StayHotel) => Promise<StaySelectResult>;
  onManualLodging: () => void;
}) {
  const t = useTranslations("stayAreas");
  const [areas, setAreas] = useState<StayAreasResponse>();
  const [areasError, setAreasError] = useState<string>();
  const [areasAttempt, setAreasAttempt] = useState(0);
  const [selected, setSelected] = useState<StayArea>();
  const [hotels, setHotels] = useState<StayHotelsResponse>();
  const [hotelsError, setHotelsError] = useState<string>();
  const [loadingHotels, setLoadingHotels] = useState(false);
  const [sort, setSort] = useState<SortMode>("price");
  const [onlyFullMatch, setOnlyFullMatch] = useState(false);
  const [flash, setFlash] = useState<string>();
  const [now, setNow] = useState(() => Date.now());
  const cacheRef = useRef(new Map<string, StayHotelsResponse>());
  const activeRef = useRef(true);

  useEffect(() => {
    activeRef.current = true;
    api<StayAreasResponse>(`/trips/${tripId}/stay-areas`)
      .then((value) => { if (activeRef.current) setAreas(value); })
      .catch((reason: Error) => { if (activeRef.current) setAreasError(reason.message); });
    return () => { activeRef.current = false; };
  }, [areasAttempt, tripId]);

  useEffect(() => {
    const timer = window.setInterval(() => setNow(Date.now()), CLOCK_TICK_MS);
    return () => window.clearInterval(timer);
  }, []);

  const loadHotels = useCallback(async (area: StayArea, refresh = false) => {
    const cached = refresh ? undefined : cacheRef.current.get(area.code);
    if (cached) {
      setHotels(cached);
      return;
    }
    setLoadingHotels(true);
    setHotelsError(undefined);
    try {
      const value = await api<StayHotelsResponse>(`/trips/${tripId}/stay-areas/${area.code}/hotels${refresh ? "?refresh=true" : ""}`);
      if (!activeRef.current) return;
      cacheRef.current.set(area.code, value);
      setHotels(value);
      setNow(Date.now());
    } catch (reason) {
      if (activeRef.current) setHotelsError(reason instanceof Error ? reason.message : t("compare.errorLoad"));
    } finally {
      if (activeRef.current) setLoadingHotels(false);
    }
  }, [t, tripId]);

  function retryAreas() {
    setAreas(undefined);
    setAreasError(undefined);
    setAreasAttempt((value) => value + 1);
  }

  function chooseArea(area: StayArea) {
    setSelected(area);
    setHotels(undefined);
    setHotelsError(undefined);
    setFlash(undefined);
    void loadHotels(area);
  }

  function backToAreas() {
    setSelected(undefined);
    setHotels(undefined);
    setHotelsError(undefined);
    setFlash(undefined);
  }

  async function selectHotel(hotel: StayHotel) {
    if (!selected) return;
    const result = await onSelectHotel(selected, hotel);
    if (result === "expired" && activeRef.current) {
      setFlash(t("notice.offerExpired"));
      await loadHotels(selected, true);
    }
  }

  const reasonLabel = (reason: string) => (KNOWN_REASONS.has(reason) ? t(`area.reason.${reason}`) : null);

  if (!selected) {
    return <div className="space-y-4">
      {areasError && <Notice tone="warn"><span className="flex-1">{areasError}</span><button type="button" onClick={retryAreas} className="shrink-0 font-bold underline">{t("retry")}</button></Notice>}
      {!areas && !areasError && <div aria-busy="true" className="space-y-3"><div className="h-24 animate-pulse rounded-2xl bg-[var(--paper)]" /><div className="h-24 animate-pulse rounded-2xl bg-[var(--paper)]" /><p className="text-center text-sm text-[var(--muted)]">{t("loadingAreas")}</p></div>}
      {areas && <>
        {areas.status === "unsupported" && <Notice tone="warn">{t("notice.unsupported")}</Notice>}
        {areas.status === "low_evidence" && <Notice>{t("notice.lowEvidence")}</Notice>}
        {areas.status === "no_evidence" && <Notice>{t("notice.noEvidence")}</Notice>}
        {areas.warnings.includes("consider_second_stay") && <Notice>{t("notice.secondStay")}</Notice>}
        {!areas.pricing.available && areas.status !== "unsupported" && <Notice>{t("notice.pricingUnavailable")}</Notice>}
        {areas.areas.length > 0 && <ul className="grid gap-3 sm:grid-cols-2" aria-label={t("title")}>
          {areas.areas.map((area) => {
            const stats = [
              area.item_count ? t("area.items", { count: area.item_count }) : "",
              area.dwell_minutes ? t("area.dwell", { hours: String(Math.round((area.dwell_minutes / 60) * 2) / 2) }) : "",
              area.day_count ? t("area.days", { count: area.day_count }) : "",
            ].filter(Boolean);
            const reasons = area.reasons.map(reasonLabel).filter((label): label is string => Boolean(label));
            return <li key={area.code}>
              <button type="button" onClick={() => chooseArea(area)} className="planner-tool-card w-full text-left transition hover:border-[var(--teal)]">
                <span className="flex flex-wrap items-center gap-2">
                  <strong className="text-base">{area.name}</strong>
                  {area.is_day_trip && <Chip tone="warn">{t("area.dayTrip")}</Chip>}
                  {areas.current_lodging_area_code === area.code && <Chip tone="teal">{t("area.current")}</Chip>}
                </span>
                {stats.length > 0 && <span className="mt-1 block text-xs text-[var(--muted)]">{stats.join(" · ")}</span>}
                {area.sample_titles.length > 0 && <span className="mt-1 block truncate text-xs text-[var(--muted)]">{area.sample_titles.join(" · ")}</span>}
                {reasons.length > 0 && <span className="mt-2 flex flex-wrap gap-1.5">{reasons.map((label) => <span key={label} className="rounded-full bg-[var(--paper)] px-2 py-1 text-[.68rem] font-semibold">{label}</span>)}</span>}
                <span className="mt-3 flex items-center gap-1 text-sm font-semibold text-[var(--teal)]">{t("area.pick")}<ArrowRight size={15} /></span>
              </button>
            </li>;
          })}
        </ul>}
      </>}
      <div className="flex flex-wrap items-center justify-between gap-3 border-t border-[var(--line)] pt-3 text-xs text-[var(--muted)]">
        <span>{t("noCharge")}</span>
        <button type="button" onClick={onManualLodging} className="min-h-11 rounded-xl border border-[var(--line)] px-4 font-semibold text-[var(--teal)]">{t("manualLodging")}</button>
      </div>
    </div>;
  }

  const status = hotels?.pricing.status || "";
  const priced = PRICED_STATUSES.has(status);
  const expiresAt = hotels?.pricing.expires_at ? Date.parse(hotels.pricing.expires_at) : Number.NaN;
  const expired = Number.isFinite(expiresAt) && expiresAt <= now;
  const visibleHotels = sortHotels(hotels?.hotels || [], sort).filter((hotel) => !onlyFullMatch || hotel.preference_gaps.length === 0);
  const notes = [
    ...(hotels?.date_notes || []).filter((note) => KNOWN_DATE_NOTES.has(note)).map((note) => t(`dateNote.${note}`)),
    ...(hotels?.warnings || []).filter((warning) => KNOWN_WARNINGS.has(warning)).map((warning) => t(`warning.${warning}`)),
  ];
  const validity = !hotels?.pricing.expires_at
    ? ""
    : expired
      ? t("compare.expired")
      : t("compare.validUntil", { time: new Date(hotels.pricing.expires_at).toLocaleTimeString(activeLocale(), { hour: "2-digit", minute: "2-digit" }) });

  return <div className="space-y-4">
    <div className="flex flex-wrap items-center justify-between gap-3">
      <button type="button" onClick={backToAreas} className="flex min-h-11 items-center gap-1.5 rounded-xl px-2 text-sm font-semibold text-[var(--teal)]"><ArrowLeft size={16} />{t("back")}</button>
      {hotels && !loadingHotels && <button type="button" onClick={() => void loadHotels(selected, true)} disabled={busy} className="flex min-h-11 items-center gap-1.5 rounded-xl border border-[var(--line)] px-3 text-xs font-semibold disabled:opacity-40"><RefreshCw size={14} />{t("refresh")}</button>}
    </div>
    <header>
      <h3 className="text-lg font-bold">{t("compare.title", { area: selected.name })}</h3>
      {hotels?.travelers && <p className="mt-1 text-xs text-[var(--muted)]">{t("compare.summary", { nights: hotels.nights, adults: hotels.travelers.adults, rooms: hotels.travelers.rooms })}{validity ? ` · ${validity}` : ""}</p>}
    </header>
    {flash && <Notice tone="teal">{flash}</Notice>}
    {loadingHotels && <div aria-busy="true" className="space-y-3"><div className="h-28 animate-pulse rounded-2xl bg-[var(--paper)]" /><div className="h-28 animate-pulse rounded-2xl bg-[var(--paper)]" /><p className="text-center text-sm text-[var(--muted)]">{t("compare.loading")}</p></div>}
    {hotelsError && <Notice tone="warn"><span className="flex-1">{hotelsError}</span><button type="button" onClick={() => void loadHotels(selected, true)} className="shrink-0 font-bold underline">{t("retry")}</button></Notice>}
    {hotels && !loadingHotels && <>
      {!priced && <Notice tone="warn"><span>{t(`status.${KNOWN_STATUSES.has(status) ? status : "unavailable"}`)}{hotels.pricing.message ? ` · ${hotels.pricing.message}` : ""}</span></Notice>}
      {notes.length > 0 && <p className="text-xs text-[var(--muted)]">{notes.join(" · ")}</p>}
      {hotels.filters.relaxed.length > 0 && <Notice tone="warn">{t("compare.relaxed", { labels: hotels.filters.relaxed.map((item) => (KNOWN_RELAXED.has(item.code) ? t(`relaxed.${item.code}`) : item.label)).join(", ") })}</Notice>}
      {hotels.hotels.length > 0 && <div className="flex flex-wrap items-center gap-2" role="group" aria-label={t("compare.sortLabel")}>
        {(["price", "rating", "distance"] as const).map((mode) => <button key={mode} type="button" aria-pressed={sort === mode} onClick={() => setSort(mode)} className={`min-h-9 rounded-full border px-3 text-xs font-semibold ${sort === mode ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-[var(--surface)]"}`}>{t(`compare.sort.${mode}`)}</button>)}
        <label className="ml-auto flex min-h-9 items-center gap-2 text-xs font-semibold"><input type="checkbox" checked={onlyFullMatch} onChange={(event) => setOnlyFullMatch(event.target.checked)} />{t("compare.onlyFullMatch")}</label>
      </div>}
      {priced && hotels.hotels.length === 0 && hotels.nearby.length === 0 && <Notice>{t("compare.empty")}</Notice>}
      {visibleHotels.length > 0 && <ul className="grid gap-3">{visibleHotels.map((hotel) => <li key={hotel.id}><StayHotelCard hotel={hotel} areaName={selected.name} areaCode={selected.code} tripId={tripId} busy={busy} expired={expired} onSelect={() => void selectHotel(hotel)} /></li>)}</ul>}
      {hotels.nearby.length > 0 && <section className="space-y-3">
        <h4 className="text-sm font-bold">{t("compare.nearbyTitle")}</h4>
        <ul className="grid gap-3">{hotels.nearby.map((hotel) => <li key={hotel.id}><StayHotelCard hotel={hotel} areaName={selected.name} areaCode={selected.code} tripId={tripId} busy={busy} expired={expired} onSelect={() => void selectHotel(hotel)} /></li>)}</ul>
      </section>}
      {hotels.filters.excluded_by_hard_filter > 0 && <p className="text-xs text-[var(--muted)]">{t("compare.hardFiltered", { count: hotels.filters.excluded_by_hard_filter })}</p>}
      {hotels.area_partners.length > 0 && <section className="rounded-2xl border border-[var(--line)] p-4">
        <p className="text-sm font-bold">{t("compare.partners")}</p>
        <div className="mt-2 flex flex-wrap gap-2">{hotels.area_partners.map((partner) => <PartnerButton key={partner.partner} tripId={tripId} areaCode={selected.code} partner={partner} areaName={selected.name} />)}</div>
      </section>}
      {hotels.disclosure && <p className="border-t border-[var(--line)] pt-3 text-xs text-[var(--muted)]">{hotels.disclosure}</p>}
    </>}
  </div>;
}
