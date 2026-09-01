"use client";

import {
  BadgeCheck,
  ExternalLink,
  FileCheck2,
  Link2,
  MapPinned,
  Plus,
  RefreshCw,
  Save,
  Search,
  Trash2,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";

type HotspotOption = { hotspot_id: string; name: string; city_name: string };
type ImportCandidate = { place_id: string; maps_url: string };
type CoverageItem = {
  place_id: string;
  maps_url: string;
  identity_status: "unknown" | "active" | "moved" | "not_found";
  identity_checked_at: string | null;
  review_status: "missing" | "pending" | "approved" | "rejected" | "disabled";
  display_name: string | null;
  official_website_url: string | null;
  has_ride_coordinates: boolean;
  source_count: number;
};
type EditorialCoverage = {
  items: CoverageItem[];
  restaurant_places: { listed: number; approved: number; missing: number };
  food_merchants: {
    total: number;
    destination_context: number;
    direct_merchant_evidence: number;
    official_website: number;
    by_country: Array<{
      country_code: "HK" | "JP" | "KR" | "SG" | "TH" | "TW" | "VN";
      total: number;
      destination_context: number;
      direct_merchant_evidence: number;
      official_website: number;
    }>;
    disclosure: string;
  };
};
type Claim = "display_name" | "address" | "official_website" | "coordinates";
type FormSource = {
  source_type: "merchant_official" | "official_tourism";
  source_title: string;
  source_url: string;
  claims: Claim[];
};
type EditorialForm = {
  display_name: string;
  local_name: string;
  address: string;
  official_website_url: string;
  ride_latitude: string;
  ride_longitude: string;
  review_status: "pending" | "approved" | "rejected" | "disabled";
  sources: FormSource[];
};

const emptySource = (): FormSource => ({
  source_type: "merchant_official",
  source_title: "",
  source_url: "",
  claims: ["display_name"],
});
const emptyForm = (): EditorialForm => ({
  display_name: "",
  local_name: "",
  address: "",
  official_website_url: "",
  ride_latitude: "",
  ride_longitude: "",
  review_status: "pending",
  sources: [emptySource()],
});

export function AdminRestaurantSourcesPanel() {
  const t = useTranslations("restaurants.adminSources");
  const [hotspots, setHotspots] = useState<HotspotOption[]>([]);
  const [hotspotId, setHotspotId] = useState("");
  const [mapsValue, setMapsValue] = useState("");
  const [fallbackQuery, setFallbackQuery] = useState("");
  const [candidates, setCandidates] = useState<ImportCandidate[]>([]);
  const [coverage, setCoverage] = useState<EditorialCoverage | null>(null);
  const [selectedPlaceId, setSelectedPlaceId] = useState("");
  const [form, setForm] = useState<EditorialForm>(emptyForm);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [scanCoverage, sourceCoverage] = await Promise.all([
        api<{ items: HotspotOption[] }>("/admin/hotspots/restaurants/coverage"),
        api<EditorialCoverage>("/admin/hotspots/restaurants/editorial-coverage?limit=200"),
      ]);
      setHotspots(scanCoverage.items);
      setHotspotId((current) => current || scanCoverage.items[0]?.hotspot_id || "");
      setCoverage(sourceCoverage);
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  async function previewImport() {
    setSaving(true);
    setMessage("");
    try {
      const result = await api<{ candidates: ImportCandidate[]; pricing: { billing: string } }>(
        "/admin/hotspots/restaurants/imports/preview",
        {
          method: "POST",
          body: JSON.stringify({
            value: mapsValue,
            hotspot_id: hotspotId || null,
            query: fallbackQuery || null,
          }),
        },
      );
      setCandidates(result.candidates);
      setMessage(t("previewReady", { count: result.candidates.length }));
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }

  async function commitImport(candidate: ImportCandidate) {
    if (!hotspotId) return;
    setSaving(true);
    setMessage("");
    try {
      await api("/admin/hotspots/restaurants/imports", {
        method: "POST",
        headers: { "Idempotency-Key": crypto.randomUUID() },
        body: JSON.stringify({ hotspot_id: hotspotId, place_id: candidate.place_id }),
      });
      setMessage(t("imported"));
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }

  async function editPlace(placeId: string) {
    setSaving(true);
    setMessage("");
    try {
      const result = await api<{
        profile: null | {
          display_name: string;
          local_name: string | null;
          address: string | null;
          official_website_url: string | null;
          ride_latitude: number | null;
          ride_longitude: number | null;
          review_status: EditorialForm["review_status"];
          sources: FormSource[];
        };
      }>(`/admin/hotspots/restaurants/places/${placeId}/editorial`);
      setSelectedPlaceId(placeId);
      setForm(
        result.profile
          ? {
              display_name: result.profile.display_name,
              local_name: result.profile.local_name || "",
              address: result.profile.address || "",
              official_website_url: result.profile.official_website_url || "",
              ride_latitude: result.profile.ride_latitude?.toString() || "",
              ride_longitude: result.profile.ride_longitude?.toString() || "",
              review_status: result.profile.review_status,
              sources: result.profile.sources.length ? result.profile.sources : [emptySource()],
            }
          : emptyForm(),
      );
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }

  function updateSource(index: number, value: Partial<FormSource>) {
    setForm((current) => ({
      ...current,
      sources: current.sources.map((source, sourceIndex) =>
        sourceIndex === index ? { ...source, ...value } : source,
      ),
    }));
  }

  function toggleClaim(index: number, claim: Claim) {
    const source = form.sources[index];
    updateSource(index, {
      claims: source.claims.includes(claim)
        ? source.claims.filter((item) => item !== claim)
        : [...source.claims, claim],
    });
  }

  async function saveEditorial() {
    if (!selectedPlaceId) return;
    setSaving(true);
    setMessage("");
    try {
      await api(`/admin/hotspots/restaurants/places/${selectedPlaceId}/editorial`, {
        method: "PUT",
        body: JSON.stringify({
          display_name: form.display_name,
          local_name: form.local_name || null,
          address: form.address || null,
          official_website_url: form.official_website_url || null,
          ride_latitude: form.ride_latitude ? Number(form.ride_latitude) : null,
          ride_longitude: form.ride_longitude ? Number(form.ride_longitude) : null,
          review_status: form.review_status,
          sources: form.sources,
        }),
      });
      setMessage(t("saved"));
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }

  async function refreshIdentity(placeId: string) {
    setSaving(true);
    setMessage("");
    try {
      const result = await api<{ status: string }>(
        `/admin/hotspots/restaurants/places/${placeId}/refresh-identity`,
        { method: "POST" },
      );
      setMessage(t("identityResult", { status: result.status }));
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setSaving(false);
    }
  }

  return <section className="mt-10 border-t border-[var(--line)] pt-8">
    <div><p className="flex items-center gap-2 text-sm font-bold text-[var(--coral)]"><FileCheck2 size={17} />{t("eyebrow")}</p><h2 className="mt-2 text-2xl font-bold">{t("title")}</h2><p className="mt-1 max-w-4xl text-sm leading-6 text-[var(--muted)]">{t("description")}</p></div>
    {message && <p role="status" className="mt-4 rounded-xl bg-[var(--teal-soft)] px-4 py-3 text-sm text-[var(--teal-dark)]">{message}</p>}
    <div className="mt-5 grid gap-5 xl:grid-cols-2">
      <article className="rounded-3xl border border-[var(--line)] bg-white p-5"><div className="flex items-center gap-2"><Link2 className="text-[var(--teal)]" size={19} /><h3 className="font-bold">{t("importTitle")}</h3></div><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("importDescription")}</p><div className="mt-4 grid gap-3"><label className="text-sm font-semibold">{t("hotspot")}<select value={hotspotId} onChange={(event) => setHotspotId(event.target.value)} className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] px-3">{hotspots.map((item) => <option key={item.hotspot_id} value={item.hotspot_id}>{item.name} · {item.city_name}</option>)}</select></label><label className="text-sm font-semibold">{t("mapsInput")}<input value={mapsValue} onChange={(event) => setMapsValue(event.target.value)} placeholder="Place ID / https://maps.app.goo.gl/..." className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] px-3" /></label><label className="text-sm font-semibold">{t("fallbackQuery")}<input value={fallbackQuery} onChange={(event) => setFallbackQuery(event.target.value)} placeholder={t("fallbackPlaceholder")} className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] px-3" /></label><button type="button" disabled={saving || !mapsValue || !hotspotId} onClick={() => void previewImport()} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-4 font-semibold text-white disabled:opacity-40"><Search size={16} />{t("preview")}</button></div><p className="mt-3 rounded-xl bg-emerald-50 p-3 text-xs leading-5 text-emerald-900">{t("idsOnlyNotice")}</p>{candidates.length > 0 && <div className="mt-4 grid gap-2">{candidates.map((candidate) => <div key={candidate.place_id} className="rounded-xl border border-[var(--line)] p-3"><code className="break-all text-xs">{candidate.place_id}</code><div className="mt-3 flex gap-2"><a href={candidate.maps_url} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-10 items-center gap-1 rounded-lg border px-3 text-xs font-semibold"><MapPinned size={14} />{t("openMap")}<ExternalLink size={11} /></a><button type="button" disabled={saving} onClick={() => void commitImport(candidate)} className="min-h-10 rounded-lg bg-[var(--teal)] px-3 text-xs font-semibold text-white">{t("confirmImport")}</button></div></div>)}</div>}</article>
      <article className="rounded-3xl border border-[var(--line)] bg-white p-5"><div className="flex items-center gap-2"><BadgeCheck className="text-[var(--teal)]" size={19} /><h3 className="font-bold">{t("coverageTitle")}</h3></div>{coverage && <><div className="mt-4 grid grid-cols-3 gap-2 text-center text-xs"><div className="rounded-xl bg-[var(--paper)] p-3"><strong className="block text-lg">{coverage.restaurant_places.approved}</strong>{t("approved")}</div><div className="rounded-xl bg-[var(--paper)] p-3"><strong className="block text-lg">{coverage.restaurant_places.missing}</strong>{t("missing")}</div><div className="rounded-xl bg-[var(--paper)] p-3"><strong className="block text-lg">{coverage.food_merchants.destination_context}/{coverage.food_merchants.total}</strong>{t("governmentContext")}</div></div><p className="mt-3 rounded-xl bg-amber-50 p-3 text-xs leading-5 text-amber-900">{t("contextDisclosure", { direct: coverage.food_merchants.direct_merchant_evidence })}</p><div className="mt-4 grid gap-2 sm:grid-cols-2">{coverage.food_merchants.by_country.map((country) => { const percent = country.total ? Math.round((country.direct_merchant_evidence / country.total) * 100) : 0; return <div key={country.country_code} className="rounded-2xl border border-[var(--line)] p-3"><div className="flex items-center justify-between gap-3 text-xs"><strong>{t(`country.${country.country_code}`)}</strong><span className="font-semibold text-[var(--teal-dark)]">{country.direct_merchant_evidence}/{country.total}</span></div><div className="mt-2 h-1.5 overflow-hidden rounded-full bg-slate-100"><div className="h-full rounded-full bg-[var(--teal)]" style={{ width: `${percent}%` }} /></div><p className="mt-2 text-[11px] text-[var(--muted)]">{t("countryCoverage", { direct: country.direct_merchant_evidence, websites: country.official_website })}</p></div>; })}</div></>}</article>
    </div>
    <div className="mt-5 overflow-hidden rounded-2xl border border-[var(--line)] bg-white"><div className="max-h-[30rem] divide-y divide-[var(--line)] overflow-y-auto">{coverage?.items.map((item) => <article key={item.place_id} className="grid gap-3 p-4 md:grid-cols-[1fr_auto] md:items-center"><div><div className="flex flex-wrap items-center gap-2"><h3 className="font-semibold">{item.display_name || item.place_id}</h3><span className="rounded-full bg-[var(--paper)] px-2 py-1 text-[10px] font-semibold">{t(`status.${item.review_status}`)}</span><span className="rounded-full bg-[var(--paper)] px-2 py-1 text-[10px] font-semibold">ID: {item.identity_status}</span></div><p className="mt-1 text-xs text-[var(--muted)]">{t("itemCoverage", { sources: item.source_count, website: item.official_website_url ? t("yes") : t("no"), ride: item.has_ride_coordinates ? t("yes") : t("no") })}</p></div><div className="flex gap-2"><button type="button" disabled={saving} onClick={() => void refreshIdentity(item.place_id)} className="grid h-10 w-10 place-items-center rounded-lg border" aria-label={t("refreshIdentity")}><RefreshCw size={15} /></button><button type="button" disabled={saving} onClick={() => void editPlace(item.place_id)} className="min-h-10 rounded-lg border border-[var(--teal)] px-3 text-xs font-semibold text-[var(--teal)]">{t("editSources")}</button></div></article>)}</div>{!loading && !coverage?.items.length && <p className="p-7 text-center text-sm text-[var(--muted)]">{t("empty")}</p>}</div>
    {selectedPlaceId && <article className="mt-5 rounded-3xl border-2 border-[var(--teal)] bg-white p-5"><div className="flex flex-wrap items-center justify-between gap-3"><div><p className="text-xs font-bold text-[var(--teal)]">{t("editing")}</p><code className="text-xs">{selectedPlaceId}</code></div><select value={form.review_status} onChange={(event) => setForm({ ...form, review_status: event.target.value as EditorialForm["review_status"] })} className="h-11 rounded-xl border px-3"><option value="pending">{t("status.pending")}</option><option value="approved">{t("status.approved")}</option><option value="rejected">{t("status.rejected")}</option><option value="disabled">{t("status.disabled")}</option></select></div><div className="mt-5 grid gap-3 md:grid-cols-2"><label className="text-sm font-semibold">{t("displayName")}<input value={form.display_name} onChange={(event) => setForm({ ...form, display_name: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold">{t("localName")}<input value={form.local_name} onChange={(event) => setForm({ ...form, local_name: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold md:col-span-2">{t("address")}<input value={form.address} onChange={(event) => setForm({ ...form, address: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold md:col-span-2">{t("officialWebsite")}<input value={form.official_website_url} onChange={(event) => setForm({ ...form, official_website_url: event.target.value })} placeholder="https://" className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold">{t("latitude")}<input type="number" step="any" value={form.ride_latitude} onChange={(event) => setForm({ ...form, ride_latitude: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label><label className="text-sm font-semibold">{t("longitude")}<input type="number" step="any" value={form.ride_longitude} onChange={(event) => setForm({ ...form, ride_longitude: event.target.value })} className="mt-1 h-11 w-full rounded-xl border px-3" /></label></div><div className="mt-5 grid gap-3">{form.sources.map((source, index) => <fieldset key={index} className="rounded-2xl border border-[var(--line)] p-4"><div className="flex items-center justify-between"><legend className="font-semibold">{t("sourceNumber", { number: index + 1 })}</legend>{form.sources.length > 1 && <button type="button" onClick={() => setForm({ ...form, sources: form.sources.filter((_, itemIndex) => itemIndex !== index) })} className="grid h-9 w-9 place-items-center rounded-lg border" aria-label={t("removeSource")}><Trash2 size={14} /></button>}</div><div className="mt-3 grid gap-3 md:grid-cols-2"><select value={source.source_type} onChange={(event) => updateSource(index, { source_type: event.target.value as FormSource["source_type"] })} className="h-11 rounded-xl border px-3"><option value="merchant_official">{t("merchantOfficial")}</option><option value="official_tourism">{t("officialTourism")}</option></select><input value={source.source_title} onChange={(event) => updateSource(index, { source_title: event.target.value })} placeholder={t("sourceTitle")} className="h-11 rounded-xl border px-3" /><input value={source.source_url} onChange={(event) => updateSource(index, { source_url: event.target.value })} placeholder="https://" className="h-11 rounded-xl border px-3 md:col-span-2" /></div><div className="mt-3 flex flex-wrap gap-2">{(["display_name", "address", "official_website", "coordinates"] as Claim[]).map((claim) => <label key={claim} className="inline-flex min-h-10 items-center gap-2 rounded-lg border px-3 text-xs"><input type="checkbox" checked={source.claims.includes(claim)} onChange={() => toggleClaim(index, claim)} />{t(`claim.${claim}`)}</label>)}</div></fieldset>)}</div><div className="mt-4 flex flex-wrap gap-2"><button type="button" onClick={() => setForm({ ...form, sources: [...form.sources, emptySource()] })} className="inline-flex min-h-11 items-center gap-2 rounded-xl border px-4 text-sm font-semibold"><Plus size={15} />{t("addSource")}</button><button type="button" disabled={saving || !form.display_name || form.sources.some((source) => !source.source_title || !source.source_url || !source.claims.length)} onClick={() => void saveEditorial()} className="ml-auto inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--ink)] px-5 text-sm font-semibold text-white disabled:opacity-40"><Save size={15} />{t("save")}</button></div></article>}
  </section>;
}
