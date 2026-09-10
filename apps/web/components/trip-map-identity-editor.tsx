"use client";

import { useEffect, useRef, useState } from "react";
import { useTranslations } from "next-intl";
import { PlacePicker } from "@/components/place-picker";
import { api } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";
import type { Trip, TripItem } from "@/lib/trip-types";

export function TripMapIdentityEditor({ tripId, version, item, canSave, onSaved, onBusy }: {
  tripId: string; version: number; item: TripItem; canSave: boolean;
  onSaved: (trip: Trip) => void;
  onBusy?: (busy: boolean) => void;
}) {
  const t = useTranslations("trips.editor.mapIdentities");
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [candidate, setCandidate] = useState<{ place_id: string; name: string; address?: string | null }>();
  const [confirmed, setConfirmed] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [key, setKey] = useState("");
  const mounted = useRef(true);
  useEffect(() => { mounted.current = true; return () => { mounted.current = false; }; }, []);
  async function save() {
    if (!candidate || !confirmed || !canSave || busy) return;
    setBusy(true); onBusy?.(true); setError("");
    const operationKey = key || crypto.randomUUID();
    setKey(operationKey);
    try {
      const trip = await api<Trip>(`/trips/${tripId}/items/${item.id}/map-identities`, {
        method: "POST", headers: { "Idempotency-Key": operationKey },
        body: JSON.stringify({ version, provider: "google_places", place_id: candidate.place_id, confirmed_same_place: true }),
      });
      if (mounted.current) { onSaved(trip); setOpen(false); }
    } catch (reason) { if (mounted.current) setError(reason instanceof Error ? reason.message : String(reason)); }
    finally { onBusy?.(false); if (mounted.current) setBusy(false); }
  }
  const identities = Object.values(item.map_identities || {});
  const links = item.location_map_links || identities.filter((identity) => identity.status === "verified" && identity.map_url)
    .map((identity) => ({ provider: identity.provider === "naver_maps" ? "naver" : "google", url: identity.map_url!, position_only: false }));
  return <section className="rounded-2xl border border-[var(--line)] p-4" aria-label={t("title")}>
    <h3 className="font-semibold">{t("title")}</h3>
    <div className="flex flex-wrap gap-2">
      {links.map((link) =>
        <a key={link.provider} href={safeExternalHref(link.url)} target="_blank" rel="noopener noreferrer"
          className="inline-flex min-h-11 items-center rounded-lg border border-[var(--line)] px-3 text-sm font-semibold">
          {link.provider === "google" ? "Google Maps" : "NAVER Maps"}{link.position_only ? ` · ${t("position")}` : ""}
        </a>)}
    </div>
    <p className="mt-2 text-xs leading-5 text-[var(--muted)]">{t("replaceHint")}</p>
    <button type="button" disabled={busy || !canSave} aria-expanded={open}
      className="mt-2 min-h-11 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold disabled:opacity-50"
      onClick={() => { setOpen(!open); setQuery(item.title); setCandidate(undefined); setConfirmed(false); setKey(""); setError(""); }}>{t("supplement")}</button>
    {!canSave && <p className="text-xs text-[var(--muted)]">{t("saveFirst")}</p>}
    {open && <fieldset disabled={busy} className="mt-3 grid gap-3">
      <PlacePicker provider="google_places" countryCodes={["kr"]} selectionContextKey={`identity:${item.id}`}
        label={t("search")} value={query} confirmed={Boolean(candidate)}
        bias={item.latitude != null && item.longitude != null ? { latitude: item.latitude, longitude: item.longitude } : undefined}
        onTextChange={(value) => { setQuery(value); setCandidate(undefined); setConfirmed(false); setKey(""); }}
        onSelect={(place) => { setCandidate(place); setQuery(place.name); setConfirmed(false); setKey(""); }} />
      {candidate && <div className="rounded-xl bg-[var(--paper)] p-3 text-sm"><p>{candidate.name}</p><p>{candidate.address}</p></div>}
      <label className="flex min-h-11 items-center gap-3 text-sm leading-5">
        <input type="checkbox" checked={confirmed} disabled={!candidate} onChange={(event) => setConfirmed(event.target.checked)} />{t("confirm")}
      </label>
      {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
      <button type="button" disabled={!candidate || !confirmed || !canSave || busy} onClick={() => void save()}
        className="min-h-12 rounded-xl bg-[var(--teal-fill)] px-4 font-semibold text-white disabled:opacity-50">{t("apply")}</button>
    </fieldset>}
  </section>;
}
