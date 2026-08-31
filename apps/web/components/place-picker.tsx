"use client";

import { Check, MapPin, Search } from "lucide-react";
import { useEffect, useRef, useState } from "react";
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
}: {
  value: string;
  confirmed: boolean;
  onTextChange: (value: string) => void;
  onSelect: (place: Place) => void;
  countryCodes?: string[];
  bias?: { latitude: number; longitude: number };
}) {
  const token = useRef(crypto.randomUUID());
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const [error, setError] = useState<string>();
  const canSearch = value.trim().length >= 2 && !confirmed;
  const visibleSuggestions = canSearch ? suggestions : [];
  const countryKey = countryCodes.map((code) => code.toLowerCase()).sort().join(",");
  const biasLatitude = bias?.latitude;
  const biasLongitude = bias?.longitude;

  useEffect(() => {
    if (!canSearch) return;
    let cancelled = false;
    const timeout = window.setTimeout(() => {
      setLoading(true);
      setError(undefined);
      const params = new URLSearchParams({ q: value.trim(), session_token: token.current });
      if (countryKey) params.set("country_codes", countryKey);
      if (biasLatitude != null && biasLongitude != null) {
        params.set("latitude", String(biasLatitude));
        params.set("longitude", String(biasLongitude));
      }
      api<Suggestion[]>(`/places/autocomplete?${params}`)
        .then((rows) => {
          if (cancelled) return;
          setSuggestions(rows);
          setOpen(true);
          if (!rows.length) setError("Google Maps 沒有符合的地點，請換一組關鍵字。");
        })
        .catch((reason: Error) => {
          if (cancelled) return;
          setSuggestions([]);
          setOpen(true);
          setError(reason.message);
        })
        .finally(() => { if (!cancelled) setLoading(false); });
    }, 320);
    return () => { cancelled = true; window.clearTimeout(timeout); };
  }, [biasLatitude, biasLongitude, canSearch, countryKey, value]);

  async function choose(suggestion: Suggestion) {
    setLoading(true);
    setError(undefined);
    try {
      const params = new URLSearchParams({ session_token: token.current });
      const place = await api<Place>(`/places/${suggestion.provider}/${encodeURIComponent(suggestion.place_id)}?${params}`);
      onSelect(place);
      setOpen(false);
      setSuggestions([]);
      token.current = crypto.randomUUID();
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : "Google Maps 地點詳細資料目前無法取得。");
    } finally {
      setLoading(false);
    }
  }

  return <div className="relative">
    <div className="flex items-center rounded-xl border border-[var(--line)] bg-white px-3 focus-within:border-[var(--teal)]">
      {confirmed ? <Check size={15} className="shrink-0 text-emerald-600" /> : <Search size={15} className="shrink-0 text-[var(--muted)]" />}
      <input value={value} onFocus={() => setOpen(true)} onChange={(event) => { setError(undefined); onTextChange(event.target.value); }} placeholder="搜尋景點、餐廳或車站" className="min-w-0 flex-1 bg-transparent px-2 py-2.5 text-sm outline-none" />
      {loading && <span className="text-xs text-[var(--muted)]">搜尋中</span>}
    </div>
    {open && visibleSuggestions.length > 0 && <div className="absolute z-30 mt-1 max-h-64 w-full overflow-auto rounded-xl border border-[var(--line)] bg-white p-1 shadow-[var(--shadow-lg)]">
      {visibleSuggestions.map((suggestion) => <button key={suggestion.place_id} type="button" onMouseDown={(event) => event.preventDefault()} onClick={() => choose(suggestion)} className="flex w-full items-start gap-2 rounded-lg px-3 py-2.5 text-left hover:bg-[var(--paper)]"><MapPin size={15} className="mt-0.5 shrink-0 text-[var(--teal)]" /><span><span className="block text-sm font-semibold">{suggestion.name}</span>{suggestion.address && <span className="mt-0.5 block text-xs text-[var(--muted)]">{suggestion.address}{suggestion.distance_meters != null ? ` · 約 ${Math.max(1, Math.round(suggestion.distance_meters / 1000))} 公里` : ""}</span>}</span></button>)}
      <p className="px-3 py-2 text-right text-[.65rem] font-semibold text-[var(--muted)]">地點資料：Google Maps</p>
    </div>}
    {error && canSearch && <p role="alert" className="mt-1 text-xs text-red-700">{error}</p>}
  </div>;
}
