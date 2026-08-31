"use client";

import { Check, MapPin, Search } from "lucide-react";
import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";

type Suggestion = { provider: string; place_id: string; name: string; address?: string | null };
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
}: {
  value: string;
  confirmed: boolean;
  onTextChange: (value: string) => void;
  onSelect: (place: Place) => void;
}) {
  const token = useRef(crypto.randomUUID());
  const [suggestions, setSuggestions] = useState<Suggestion[]>([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);
  const canSearch = value.trim().length >= 2 && !confirmed;
  const visibleSuggestions = canSearch ? suggestions : [];

  useEffect(() => {
    if (!canSearch) return;
    const timeout = window.setTimeout(() => {
      setLoading(true);
      api<Suggestion[]>(`/places/autocomplete?q=${encodeURIComponent(value)}&session_token=${token.current}`)
        .then((rows) => { setSuggestions(rows); setOpen(true); })
        .catch(() => setSuggestions([]))
        .finally(() => setLoading(false));
    }, 320);
    return () => window.clearTimeout(timeout);
  }, [canSearch, value]);

  async function choose(suggestion: Suggestion) {
    setLoading(true);
    try {
      const place = await api<Place>(`/places/${suggestion.provider}/${encodeURIComponent(suggestion.place_id)}`);
      onSelect(place);
      setOpen(false);
      setSuggestions([]);
      token.current = crypto.randomUUID();
    } finally {
      setLoading(false);
    }
  }

  return <div className="relative">
    <div className="flex items-center rounded-xl border border-[var(--line)] bg-white px-3 focus-within:border-[var(--teal)]">
      {confirmed ? <Check size={15} className="shrink-0 text-emerald-600" /> : <Search size={15} className="shrink-0 text-[var(--muted)]" />}
      <input value={value} onFocus={() => setOpen(true)} onChange={(event) => onTextChange(event.target.value)} placeholder="搜尋景點、餐廳或車站" className="min-w-0 flex-1 bg-transparent px-2 py-2.5 text-sm outline-none" />
      {loading && <span className="text-xs text-[var(--muted)]">搜尋中</span>}
    </div>
    {open && visibleSuggestions.length > 0 && <div className="absolute z-30 mt-1 max-h-64 w-full overflow-auto rounded-xl border border-[var(--line)] bg-white p-1 shadow-[var(--shadow-lg)]">
      {visibleSuggestions.map((suggestion) => <button key={suggestion.place_id} type="button" onMouseDown={(event) => event.preventDefault()} onClick={() => choose(suggestion)} className="flex w-full items-start gap-2 rounded-lg px-3 py-2.5 text-left hover:bg-[var(--paper)]"><MapPin size={15} className="mt-0.5 shrink-0 text-[var(--teal)]" /><span><span className="block text-sm font-semibold">{suggestion.name}</span>{suggestion.address && <span className="mt-0.5 block text-xs text-[var(--muted)]">{suggestion.address}</span>}</span></button>)}
    </div>}
  </div>;
}
