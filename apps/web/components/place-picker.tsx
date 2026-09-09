"use client";

import { Check, MapPin, Search } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useId, useRef, useState } from "react";
import { api } from "@/lib/api";

type Suggestion = {
  provider: string;
  place_id: string;
  name: string;
  address?: string | null;
  distance_meters?: number | null;
  attribution?: string;
};
type Place = Suggestion & {
  latitude?: number | null;
  longitude?: number | null;
  google_maps_url?: string | null;
  naver_maps_url?: string | null;
  external_url?: string | null;
  opening_hours?: string[];
  attribution?: string;
};

export function PlacePicker({
  value,
  confirmed,
  onTextChange,
  onSelect,
  countryCodes = [],
  bias,
  inputId,
  label,
  descriptionId,
  kinds,
  placeholder,
  selectionContextKey,
}: {
  value: string;
  confirmed: boolean;
  onTextChange: (value: string) => void;
  onSelect: (place: Place) => void;
  countryCodes?: string[];
  bias?: { latitude: number; longitude: number };
  inputId?: string;
  label?: string;
  descriptionId?: string;
  kinds?: "cities";
  placeholder?: string;
  /** Identity of the draft/selection owner; changing it invalidates in-flight details. */
  selectionContextKey?: string;
}) {
  const t = useTranslations("common");
  const resolvedLabel = label ?? t("placePicker.destination");
  const resolvedPlaceholder = placeholder ?? t("placePicker.placeholder");
  // Read once per render so the search effect does not depend on `t` itself.
  const noMatchesMessage = t("placePicker.noMatches");
  const token = useRef(crypto.randomUUID());
  const generatedListboxId = useId();
  const listboxId = `place-suggestions-${generatedListboxId}`;
  const [suggestionResult, setSuggestions] = useState<{ scope: string; rows: Suggestion[] }>();
  const detailsGeneration = useRef(0);
  const detailsController = useRef<AbortController | undefined>(undefined);
  const autocompleteController = useRef<AbortController | undefined>(undefined);
  // Set when the reader closes the list themselves. The debounced search finishes
  // afterwards, and without this it would reopen what they just dismissed.
  const dismissed = useRef(false);
  const container = useRef<HTMLDivElement>(null);
  const [loadingScope, setLoadingScope] = useState<string>();
  const [open, setOpen] = useState(false);
  const [activeIndex, setActiveIndex] = useState(-1);
  const [errorState, setError] = useState<{ scope: string; message: string }>();
  const [searchAttempt, setSearchAttempt] = useState(0);
  const canSearch = value.trim().length >= 2 && !confirmed;
  const countryKey = countryCodes.map((code) => code.toLowerCase()).sort().join(",");
  const biasLatitude = bias?.latitude;
  const biasLongitude = bias?.longitude;

  const scope = JSON.stringify([selectionContextKey, value, confirmed, countryKey, kinds, biasLatitude, biasLongitude]);
  const suggestions = suggestionResult?.scope === scope ? suggestionResult.rows : [];
  const visibleSuggestions = canSearch ? suggestions : [];
  const loading = loadingScope === scope;
  const error = errorState?.scope === scope ? errorState.message : undefined;

  const invalidateDetails = useCallback(() => {
    detailsGeneration.current += 1;
    detailsController.current?.abort();
    detailsController.current = undefined;
  }, []);
  const dismissSuggestions = useCallback(() => {
    dismissed.current = true;
    autocompleteController.current?.abort();
    invalidateDetails();
    setLoadingScope(undefined);
    setOpen(false);
    setActiveIndex(-1);
  }, [invalidateDetails]);

  useEffect(() => () => {
    // Abort is best-effort; the generation also rejects adapters that resolve after abort.
    detailsGeneration.current += 1;
    detailsController.current?.abort();
    detailsController.current = undefined;
  }, [scope]);


  useEffect(() => {
    if (!canSearch) return;
    let cancelled = false;
    const controller = new AbortController();
    autocompleteController.current = controller;
    const timeout = window.setTimeout(() => {
      if (controller.signal.aborted) return;
      setLoadingScope(scope);
      setError(undefined);
      const params = new URLSearchParams({ q: value.trim(), session_token: token.current });
      if (countryKey) params.set("country_codes", countryKey);
      if (kinds) params.set("kinds", kinds);
      if (biasLatitude != null && biasLongitude != null) {
        params.set("latitude", String(biasLatitude));
        params.set("longitude", String(biasLongitude));
      }
      api<Suggestion[]>(`/places/autocomplete?${params}`, { signal: controller.signal })
        .then((rows) => {
          if (cancelled || controller.signal.aborted) return;
          setSuggestions({ scope, rows });
          if (!dismissed.current) setOpen(true);
          setActiveIndex(rows.length ? 0 : -1);
          if (!rows.length) setError({ scope, message: noMatchesMessage });
        })
        .catch((reason: Error) => {
          if (cancelled || controller.signal.aborted) return;
          setSuggestions({ scope, rows: [] });
          if (!dismissed.current) setOpen(true);
          setError({ scope, message: reason.message });
        })
        .finally(() => { if (!cancelled && !controller.signal.aborted) setLoadingScope(undefined); });
    }, 320);
    return () => { cancelled = true; window.clearTimeout(timeout); controller.abort(); };
  }, [biasLatitude, biasLongitude, canSearch, countryKey, kinds, noMatchesMessage, value, scope, searchAttempt]);

  async function choose(suggestion: Suggestion) {
    invalidateDetails();
    autocompleteController.current?.abort();
    const generation = detailsGeneration.current;
    const controller = new AbortController();
    detailsController.current = controller;
    setLoadingScope(scope);
    setError(undefined);
    try {
      const params = new URLSearchParams({ session_token: token.current });
      const place = await api<Place>('/places/' + suggestion.provider + '/' + encodeURIComponent(suggestion.place_id) + '?' + params, { signal: controller.signal });
      if (controller.signal.aborted || generation !== detailsGeneration.current) return;
      dismissed.current = true;
      setOpen(false);
      setSuggestions({ scope, rows: [] });
      setActiveIndex(-1);
      token.current = crypto.randomUUID();
      onSelect(place);
    } catch (reason) {
      if (controller.signal.aborted || generation !== detailsGeneration.current) return;
      setError({ scope, message: reason instanceof Error ? reason.message : t("placePicker.detailsUnavailable") });
    } finally {
      if (generation === detailsGeneration.current && !controller.signal.aborted) {
        detailsController.current = undefined;
        setLoadingScope(undefined);
      }
    }
  }

  useEffect(() => {
    if (!open) return;
    function closeOnOutsidePress(event: PointerEvent) {
      if (container.current?.contains(event.target as Node)) return;
      dismissSuggestions();
    }
    document.addEventListener("pointerdown", closeOnOutsidePress);
    return () => document.removeEventListener("pointerdown", closeOnOutsidePress);
  }, [open, dismissSuggestions]);

  function handleKeyDown(event: React.KeyboardEvent<HTMLInputElement>) {
    if (event.key === "Escape") {
      if (open || loading || (canSearch && !dismissed.current)) {
        event.preventDefault(); event.stopPropagation();
        dismissSuggestions();
      }
      return;
    }
    if (!visibleSuggestions.length) return;
    if (event.key === "ArrowDown") {
      event.preventDefault();
      dismissed.current = false;
      setOpen(true);
      setActiveIndex((current) => (current + 1) % visibleSuggestions.length);
    } else if (event.key === "ArrowUp") {
      event.preventDefault();
      dismissed.current = false;
      setOpen(true);
      setActiveIndex((current) => current <= 0 ? visibleSuggestions.length - 1 : current - 1);
    } else if (event.key === "Enter" && open && activeIndex >= 0) {
      event.preventDefault();
      void choose(visibleSuggestions[activeIndex]);
    }
  }

  return <div ref={container} className="relative">
    <div className="flex items-center rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 focus-within:border-[var(--teal)]">
      {confirmed ? <Check size={15} className="shrink-0 text-emerald-600" /> : <Search size={15} className="shrink-0 text-[var(--muted)]" />}
      <input id={inputId} aria-label={resolvedLabel} aria-describedby={descriptionId} role="combobox" aria-autocomplete="list" aria-expanded={open && visibleSuggestions.length > 0} aria-controls={listboxId} aria-activedescendant={open && activeIndex >= 0 ? `${listboxId}-option-${activeIndex}` : undefined} value={value} onFocus={() => {
        if (dismissed.current && autocompleteController.current?.signal.aborted && !visibleSuggestions.length) setSearchAttempt((attempt) => attempt + 1);
        dismissed.current = false; setOpen(true);
      }} onKeyDown={handleKeyDown} onChange={(event) => { invalidateDetails(); autocompleteController.current?.abort(); setLoadingScope(undefined); setError(undefined); setActiveIndex(-1); dismissed.current = false; onTextChange(event.target.value); }} placeholder={resolvedPlaceholder} className="min-w-0 flex-1 bg-transparent px-2 py-2.5 text-sm outline-none" />
      {loading && <span className="text-xs text-[var(--muted)]">{t("placePicker.searching")}</span>}
    </div>
    {open && visibleSuggestions.length > 0 && <div id={listboxId} role="listbox" aria-label={t("placePicker.suggestions", { label: resolvedLabel })} className="absolute z-30 mt-1 max-h-64 w-full overflow-auto rounded-xl border border-[var(--line)] bg-[var(--surface)] p-1 shadow-[var(--shadow-lg)]">
      {visibleSuggestions.map((suggestion, index) => <button id={`${listboxId}-option-${index}`} role="option" aria-selected={index === activeIndex} key={`${suggestion.provider}-${suggestion.place_id}`} type="button" onMouseDown={(event) => event.preventDefault()} onMouseEnter={() => setActiveIndex(index)} onClick={() => choose(suggestion)} className={`flex w-full items-start gap-2 rounded-lg px-3 py-2.5 text-left ${index === activeIndex ? "bg-[var(--paper)]" : "hover:bg-[var(--paper)]"}`}><MapPin size={15} className="mt-0.5 shrink-0 text-[var(--teal)]" /><span className="min-w-0 flex-1"><span className="flex items-center gap-2"><span className="block truncate text-sm font-semibold">{suggestion.name}</span><span className="shrink-0 rounded-full bg-[var(--paper)] px-2 py-0.5 text-xs font-bold text-[var(--muted)]">{suggestion.provider === "naver_local" ? "NAVER" : "Google"}</span></span>{suggestion.address && <span className="mt-0.5 block text-xs text-[var(--muted)]">{suggestion.address}{suggestion.distance_meters != null ? ` · ${t("placePicker.distanceKm", { km: Math.max(1, Math.round(suggestion.distance_meters / 1000)) })}` : ""}</span>}</span></button>)}
      <p className="px-3 py-2 text-right text-xs font-semibold text-[var(--muted)]">{t("placePicker.source", { providers: [...new Set(visibleSuggestions.map((row) => row.provider === "naver_local" ? "NAVER" : "Google Maps"))].join(t("placePicker.listSeparator")) })}</p>
    </div>}
    {error && canSearch && <p role="alert" className="mt-1 text-xs text-red-700">{error}</p>}
  </div>;
}
