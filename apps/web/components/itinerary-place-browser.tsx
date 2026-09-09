"use client";

import { Check, ChevronRight, Heart, Loader2, MapPin, Search, Undo2 } from "lucide-react";
import { useEffect, useId, useState } from "react";
import { useLocale } from "next-intl";
import { api } from "@/lib/api";
import { itineraryCopy, itineraryText } from "@/lib/itinerary-copy";
import { type TripItem } from "@/lib/trip-types";
import { PlacePicker } from "@/components/place-picker";
import { calmEditCopy } from "@/components/planner/calm-edit-copy";

export type PlaceOption = {
  key: string; id: string; kind: "hotspot" | "merchant"; title: string;
  subtitle: string; is_saved: boolean; distance_km?: number | null;
  item: Omit<TripItem, "id" | "position" | "day_date">;
};
type Result = { items: PlaceOption[]; next_offset: number | null; context: "nearby" | "destination" };
type Source = "discover" | "favorites" | "nearby" | "search";
export type PlaceBrowserState = {
  source: Source; query: string; kind: "all" | "hotspot" | "merchant"; allCities: boolean; radius: number;
};
export function createPlaceBrowserState(meal = false): PlaceBrowserState {
  return { source: "discover", query: "", kind: meal ? "merchant" : "all", allCities: false, radius: 3 };
}

export function ItineraryPlaceBrowser({
  tripId, reference, following, countryCodes, items, onAdd, onManual, onUndo,
  canUndo, meal = false, feedback, state, onStateChange,
}: {
  tripId: string; reference?: { latitude?: number | null; longitude?: number | null };
  following?: { latitude?: number | null; longitude?: number | null };
  countryCodes: string[]; items: TripItem[];
  onAdd: (item: PlaceOption["item"]) => boolean;
  onManual: () => void; onUndo: () => void; canUndo: boolean; meal?: boolean; feedback?: string;
  state?: PlaceBrowserState; onStateChange?: (state: PlaceBrowserState) => void;
}) {
  const locale = useLocale();
  const copy = itineraryCopy(locale);
  const editCopy = calmEditCopy(locale);
  const panelId = useId();
  const [localState, setLocalState] = useState(() => createPlaceBrowserState(meal));
  const currentState = state ?? localState;
  const { source, query, kind, allCities, radius } = currentState;
  function changeState(patch: Partial<PlaceBrowserState>) {
    const next = { ...currentState, ...patch };
    setLocalState(next); onStateChange?.(next);
  }
  const [reload, setReload] = useState(0);
  const [result, setResult] = useState<Result>();
  const [pending, setLoading] = useState(true);
  const [settledKey, setSettledKey] = useState<string>();
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState("");
  const lat = reference?.latitude;
  const lng = reference?.longitude;
  const nextLat = following?.latitude;
  const nextLng = following?.longitude;
  const contextKey = JSON.stringify([tripId, lat, lng, nextLat, nextLng]);
  const [pagination, setPagination] = useState({ contextKey, offset: 0 });
  // Reset during render so no request can combine the new insertion point with
  // the previous neighbourhood's page. Keep the result cards and focus intact.
  const offset = pagination.contextKey === contextKey ? pagination.offset : 0;
  const requestKey = JSON.stringify([contextKey, source, query, kind, allCities, radius, offset, reload]);
  // Keep cards/focus stable, but never let a result from the previous request
  // context be chosen during the debounce before its replacement starts.
  const loading = pending || settledKey !== requestKey;
  if (pagination.contextKey !== contextKey) setPagination({ contextKey, offset: 0 });
  function setOffset(nextOffset: number) {
    setPagination({ contextKey, offset: nextOffset });
  }

  useEffect(() => {
    if (source === "search") return;
    let cancelled = false;
    const controller = new AbortController();
    const timer = window.setTimeout(() => {
      setLoading(true);
      setError(undefined);
      const params = new URLSearchParams({
        source, q: query, kind, all_cities: String(allCities),
        radius_km: String(radius), offset: String(offset),
      });
      if (lat != null && lng != null) {
        params.set("latitude", String(lat)); params.set("longitude", String(lng));
      }
      if (nextLat != null && nextLng != null) {
        params.set("next_latitude", String(nextLat)); params.set("next_longitude", String(nextLng));
      }
      api<Result>(`/trips/${tripId}/place-options?${params}`, { signal: controller.signal })
        .then((value) => { if (!cancelled) setResult(value); })
        .catch(() => { if (!cancelled) { setResult(undefined); setError(navigator.onLine ? copy.unavailable : copy.offline); } })
        .finally(() => { if (!cancelled) { setSettledKey(requestKey); setLoading(false); } });
    }, query ? 250 : 0);
    return () => { cancelled = true; window.clearTimeout(timer); controller.abort(); };
  }, [tripId, source, query, kind, allCities, radius, offset, lat, lng, nextLat, nextLng, reload, copy, requestKey]);

  function switchSource(next: Source) {
    if (next === source) return;
    changeState({ source: next }); setOffset(0); setResult(undefined); setLoading(true); setError(undefined);
  }
  function add(option: PlaceOption) {
    if (onAdd(option.item)) setNotice(itineraryText(editCopy.chosen, { title: option.title }));
  }
  const data = result?.items || [];
  const saved = data.filter((item) => item.is_saved);
  const nearby = data.filter((item) => !item.is_saved);
  const groups = source === "discover"
    ? [{ title: copy.savedSection, rows: saved }, { title: result?.context === "nearby" ? copy.nearbySection : copy.citySection, rows: nearby }]
    : [{ title: source === "favorites" ? copy.savedSection : result?.context === "nearby" ? copy.nearbySection : copy.citySection, rows: data }];

  return <div className="itinerary-place-browser">
    <div className="itinerary-picker-actions itinerary-picker-actions-sticky">
      <button type="button" onClick={onManual}>{copy.manual}</button>
      {canUndo && <button type="button" onClick={() => { onUndo(); setNotice(""); }}><Undo2 size={16} />{copy.undo}</button>}
    </div>
    <div className="itinerary-source-tabs" role="tablist" aria-label={copy.addTitle}>
      {(["discover", "favorites", "nearby", "search"] as Source[]).map((value) => <button
        key={value} type="button" role="tab" aria-selected={source === value}
        id={`${panelId}-${value}`} aria-controls={panelId} tabIndex={source === value ? 0 : -1}
        onKeyDown={(event) => {
          const tabs: Source[] = ["discover", "favorites", "nearby", "search"];
          const index = tabs.indexOf(source);
          const next = event.key === "ArrowRight" ? tabs[(index + 1) % 4]
            : event.key === "ArrowLeft" ? tabs[(index + 3) % 4]
              : event.key === "Home" ? tabs[0] : event.key === "End" ? tabs[3] : undefined;
          if (next) {
            event.preventDefault(); switchSource(next);
            document.getElementById(`${panelId}-${next}`)?.focus();
          }
        }}
        onClick={() => switchSource(value)}
      >{value === "favorites" && <Heart size={15} />}{value === "search" && <Search size={15} />}{value === "search" ? editCopy.mapSearch : copy[value]}</button>)}
    </div>
    <div role="tabpanel" id={panelId} aria-labelledby={`${panelId}-${source}`} className="itinerary-place-panel">
    {source === "search" ? <div className="itinerary-search-place">
      <PlacePicker label={editCopy.searchLabel} placeholder={copy.searchHint} value={query} confirmed={false} selectionContextKey={contextKey}
        countryCodes={countryCodes} bias={lat != null && lng != null ? { latitude: lat, longitude: lng } : undefined}
        onTextChange={(query) => changeState({ query })} onSelect={(place) => {
          const added = onAdd({
            item_type: "custom", title: place.name, location_name: place.address || place.name,
            latitude: place.latitude, longitude: place.longitude, provider_place_id: place.place_id,
            location_source: "confirmed", location_provider: place.provider,
            duration_minutes: 60, fixed_time: false, locked: false, is_estimated: false,
            data: { source_mode: "manual", place_provider: place.provider,
              google_maps_url: place.google_maps_url, naver_maps_url: place.naver_maps_url || place.external_url,
              attribution: place.attribution, opening_hours: place.opening_hours || [],
              needs_place_confirmation: false, place_match_status: "confirmed" },
          });
          if (added) setNotice(itineraryText(editCopy.chosen, { title: place.name }));
        }} />
      <p className="itinerary-discovery-hint">{editCopy.mapHint}</p>
    </div> : <>
      <label className="itinerary-place-search"><Search size={18} aria-hidden="true" /><span className="sr-only">{editCopy.searchLabel}</span>
        <input value={query} placeholder={copy.searchHint} onChange={(event) => { changeState({ query: event.target.value }); setOffset(0); setLoading(true); }} />
      </label>
      <p className="itinerary-discovery-hint">{editCopy.catalogHint}</p>
      {!meal && <div className="itinerary-kind-filter" role="group" aria-label={copy.search}>
        {(["all", "hotspot", "merchant"] as const).map((value) => <button type="button" key={value}
          aria-pressed={kind === value} onClick={() => { changeState({ kind: value }); setOffset(0); setLoading(true); }}
        >{value === "all" ? copy.all : value === "hotspot" ? copy.attractions : copy.food}</button>)}
      </div>}
      {source === "favorites" && <label className="itinerary-other-cities">
        <input type="checkbox" checked={allCities} onChange={(event) => { changeState({ allCities: event.target.checked }); setOffset(0); setLoading(true); }} />{copy.allCities}
      </label>}
      <p className="itinerary-discovery-hint">{lat != null && lng != null ? copy.nearbyHint : copy.cityHint}</p>
      {loading && result && <p role="status" className="itinerary-discovery-hint">{copy.loading}</p>}
      {loading && !result ? <div className="itinerary-place-loading" role="status"><Loader2 size={20} className="animate-spin" />{copy.loading}</div>
        : error ? <div className="itinerary-place-empty" role="alert"><p>{error}</p><button type="button" onClick={() => setReload((value) => value + 1)}>{copy.retry}</button></div>
          : data.length === 0 ? <div className="itinerary-place-empty"><MapPin size={24} /><p>{source === "favorites" ? copy.emptySaved : query ? copy.emptySearch : copy.emptyNearby}</p>
            {source !== "favorites" && radius === 3 && lat != null && <button type="button" onClick={() => { changeState({ radius: 10 }); setOffset(0); setLoading(true); }}>{copy.expand}</button>}
            <button type="button" onClick={() => switchSource("search")}><Search size={16} />{editCopy.mapSearch}</button>
          </div> : groups.map((group) => group.rows.length > 0 && <section key={group.title} aria-label={group.title}>
            <h3 className="itinerary-place-section-title">{group.title}</h3>
            <div className="itinerary-place-results">{group.rows.map((option) => {
              const already = !meal && items.some((item) => {
                const selected = item.data.catalog_selection as { kind?: string; id?: string } | undefined;
                return selected?.kind === option.kind && selected?.id === option.id
                  || item.data[`${option.kind}_id`] === option.id
                  || Boolean(option.item.provider_place_id && item.provider_place_id === option.item.provider_place_id);
              });
              return <article className="itinerary-place-result" key={option.key}>
                <span className="itinerary-place-result-icon" aria-hidden="true">{option.is_saved ? <Heart size={20} /> : <MapPin size={20} />}</span>
                <div className="itinerary-place-result-content"><h4>{option.title}</h4><p>{option.subtitle}</p>
                  <div className="itinerary-place-meta">
                    {option.distance_km != null && <span>{itineraryText(copy.distance, { distance: option.distance_km.toFixed(1) })}</span>}
                    <span>{itineraryText(copy.duration, { minutes: option.item.duration_minutes || 60 })}</span>
                  </div>
                </div>
                <button type="button" className="itinerary-place-add" aria-disabled={already || loading} aria-label={`${already ? copy.already : editCopy.choose} ${option.title}`} onClick={() => { if (!already && !loading) add(option); }}>
                  {already ? <Check size={17} /> : <ChevronRight size={17} />}<span>{already ? copy.selected : editCopy.choose}</span>
                </button>
              </article>;
            })}</div>
          </section>)}
      {!loading && !error && (offset > 0 || result?.next_offset != null) && <div className="itinerary-pagination">
        <button type="button" disabled={offset === 0} aria-label={copy.previous} onClick={() => setOffset(Math.max(0, offset - 12))}>←</button>
        <span>{Math.floor(offset / 12) + 1}</span>
        <button type="button" disabled={result?.next_offset == null} aria-label={copy.next} onClick={() => setOffset(result?.next_offset || 0)}>→</button>
      </div>}
    </>}
    </div>
    {(feedback ?? notice) && <p className="itinerary-picker-notice" role="status"><Check size={16} />{feedback ?? notice}</p>}
  </div>;
}
