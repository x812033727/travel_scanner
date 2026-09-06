"use client";

import { Fragment, useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import { HOTSPOT_CATEGORY_CODES, isHotspotCategoryCode } from "@/lib/hotspot-categories";
import { safeExternalHref } from "@/lib/navigation";
import { FilterDisclosure, FilterPills } from "./admin-filter-pills";
import { AdminHotspotThemeEditor, type AssignedTheme } from "./admin-hotspot-theme-editor";

type Candidate = {
  id: string;
  name: string;
  themes?: AssignedTheme[];
  qid: string | null;
  destination_id: string;
  city_code: string;
  city_name: string;
  country_code: string;
  country_name?: string;
  destination_role: "primary" | "secondary" | "extension";
  parent_destination_id: string | null;
  category: string;
  area_code?: string | null;
  area_name?: string | null;
  origin: string;
  status: string;
  reason: string | null;
  distance_km: number | null;
  pageviews_30d: number | null;
  source_urls: string[];
  is_active: boolean;
  is_deep_travel: boolean;
  depth_kind: "urban_local" | "day_trip" | null;
  depth_score: number | null;
  depth_reason: string | null;
  access_minutes: number | null;
  recommended_duration_minutes: number | null;
  latitude: number | null;
  longitude: number | null;
  coordinate_source_type: string | null;
  coordinate_source_url: string | null;
  google_place_id: string | null;
  naver_map_url: string | null;
  map_match_status: "unverified" | "verified" | "ambiguous" | "disabled";
};
type Facets = {
  countries: { code: string; name: string; count: number }[];
  categories: { code: string; count: number }[];
};
type Response = {
  items: Candidate[];
  total: number;
  page: number;
  pages: number;
  facets?: Facets;
};
type DestinationGroup = {
  destinationId: string;
  cityName: string;
  cityCode: string;
  role: Candidate["destination_role"];
  parentId: string | null;
  items: Candidate[];
};
type CountryGroup = {
  countryCode: string;
  countryName: string;
  destinations: DestinationGroup[];
  count: number;
};

const PAGE_SIZE = 50;
type Translator = ReturnType<typeof useTranslations>;

function roleLabel(ta: Translator, role: Candidate["destination_role"], parentId: string | null) {
  if (role === "extension") return ta("hotspotsPanel.roleExtension", { parentId: parentId ?? "" });
  return role === "secondary" ? ta("hotspotsPanel.roleSecondary") : ta("hotspotsPanel.rolePrimary");
}

// The API already orders rows by country, then destination, so grouping only
// needs to split the page wherever those keys change.
function groupCandidates(items: Candidate[]): CountryGroup[] {
  const groups: CountryGroup[] = [];
  for (const item of items) {
    let country = groups[groups.length - 1];
    if (!country || country.countryCode !== item.country_code) {
      country = {
        countryCode: item.country_code,
        countryName: item.country_name || item.country_code,
        destinations: [],
        count: 0,
      };
      groups.push(country);
    }
    let destination = country.destinations[country.destinations.length - 1];
    if (!destination || destination.destinationId !== item.destination_id) {
      destination = {
        destinationId: item.destination_id,
        cityName: item.city_name,
        cityCode: item.city_code,
        role: item.destination_role,
        parentId: item.parent_destination_id,
        items: [],
      };
      country.destinations.push(destination);
    }
    destination.items.push(item);
    country.count += 1;
  }
  return groups;
}

function sumCounts(rows: { count: number }[]) {
  return rows.reduce((sum, row) => sum + row.count, 0);
}
type MapCandidate = {
  place_id: string;
  name: string;
  address: string;
  temporary_match_coordinates: {
    latitude: number;
    longitude: number;
    usage: string;
  };
};

export function AdminHotspotsPanel() {
  const t = useTranslations("hotspots");
  const tHotspotAdmin = useTranslations("hotspotAdmin");
  const ta = useTranslations("admin");
  const [data, setData] = useState<Response | null>(null);
  const [status, setStatus] = useState("pending");
  const [city, setCity] = useState("");
  const [destinationId, setDestinationId] = useState("");
  const [role, setRole] = useState("");
  const [parentId, setParentId] = useState("");
  const [origin, setOrigin] = useState("");
  const [country, setCountry] = useState("");
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [depthKind, setDepthKind] = useState<"urban_local" | "day_trip">(
    "urban_local",
  );
  const [depthReason, setDepthReason] = useState("");
  const [accessMinutes, setAccessMinutes] = useState(30);
  const [durationMinutes, setDurationMinutes] = useState(120);
  const [moveDestinationId, setMoveDestinationId] = useState("");
  const [scores, setScores] = useState({
    locality: 85,
    distinctiveness: 85,
    feasibility: 85,
    evidence: 90,
  });
  const [locationDraft, setLocationDraft] = useState<Candidate | null>(null);
  const [mapCandidate, setMapCandidate] = useState<MapCandidate | null>(null);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams({ limit: String(PAGE_SIZE), page: String(page) });
    if (status) params.set("status", status);
    if (city) params.set("city_code", city);
    if (destinationId) params.set("destination_id", destinationId);
    if (role) params.set("role", role);
    if (parentId) params.set("parent_id", parentId);
    if (origin) params.set("origin", origin);
    if (country) params.set("country_code", country);
    if (category) params.set("category", category);
    try {
      const result = await api<Response>(`/admin/hotspots/candidates?${params}`);
      setData(result);
      // A batch action can empty the last page; fall back to the new last page.
      if (result.pages > 0 && page > result.pages) setPage(result.pages);
    } catch (error) {
      setMessage((error as Error).message);
    } finally {
      setLoading(false);
    }
  }, [category, city, country, destinationId, origin, page, parentId, role, status]);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  function updateFilter(setter: (value: string) => void, value: string) {
    setter(value);
    setPage(1);
  }

  function toggleMany(ids: string[], checked: boolean) {
    setSelected((current) => {
      const next = new Set(current);
      for (const id of ids) {
        if (checked) next.add(id);
        else next.delete(id);
      }
      return next;
    });
  }

  function categoryLabel(code: string) {
    return isHotspotCategoryCode(code) ? t(`categories.${code}`) : code;
  }

  async function review(action: "approve" | "reject" | "disable") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/review", {
        method: "POST",
        body: JSON.stringify({ ids: [...selected], action }),
      });
      setMessage(ta("hotspotsPanel.reviewed", { count: selected.size }));
      setSelected(new Set());
      await load();
    } catch (error) {
      setMessage((error as Error).message);
      setLoading(false);
    }
  }

  async function updateDepth(isDeep: boolean) {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/review", {
        method: "POST",
        body: JSON.stringify({
          ids: [...selected],
          action: "update",
          is_deep_travel: isDeep,
          ...(isDeep
            ? {
                depth_kind: depthKind,
                depth_reason: depthReason,
                access_minutes: accessMinutes,
                recommended_duration_minutes: durationMinutes,
                locality_score: scores.locality,
                distinctiveness_score: scores.distinctiveness,
                feasibility_score: scores.feasibility,
                evidence_score: scores.evidence,
              }
            : {}),
        }),
      });
      setMessage(
        isDeep
          ? ta("hotspotsPanel.depthSet", { count: selected.size })
          : ta("hotspotsPanel.depthCleared", { count: selected.size }),
      );
      setSelected(new Set());
      await load();
    } catch (error) {
      setMessage((error as Error).message);
      setLoading(false);
    }
  }

  async function moveDestination() {
    if (!selected.size || !moveDestinationId.trim()) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/review", {
        method: "POST",
        body: JSON.stringify({
          ids: [...selected],
          action: "update",
          destination_id: moveDestinationId.trim(),
        }),
      });
      setMessage(
        ta("hotspotsPanel.moved", { count: selected.size, destination: moveDestinationId.trim() }),
      );
      setSelected(new Set());
      await load();
    } catch (error) {
      setMessage((error as Error).message);
      setLoading(false);
    }
  }

  async function searchMapCandidate() {
    if (!locationDraft || locationDraft.country_code === "KR") return;
    setLoading(true);
    try {
      const result = await api<{
        configured: boolean;
        candidates: MapCandidate[];
        message?: string;
      }>("/admin/hotspots/map-candidates", {
        method: "POST",
        body: JSON.stringify({
          query: `${locationDraft.name} ${locationDraft.city_name}`,
          country_code: locationDraft.country_code,
          latitude: locationDraft.latitude,
          longitude: locationDraft.longitude,
        }),
      });
      setMapCandidate(result.candidates[0] ?? null);
      setMessage(
        result.message ??
          (result.candidates.length
            ? ta("hotspotsPanel.candidateFound")
            : ta("hotspotsPanel.candidateNone")),
      );
    } catch (error) {
      setMessage((error as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function saveLocation() {
    if (!locationDraft) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/review", {
        method: "POST",
        body: JSON.stringify({
          ids: [locationDraft.id],
          action: "update",
          latitude: locationDraft.latitude,
          longitude: locationDraft.longitude,
          coordinate_source_type: locationDraft.coordinate_source_type,
          coordinate_source_url: locationDraft.coordinate_source_url,
          google_place_id:
            locationDraft.country_code === "KR"
              ? null
              : locationDraft.google_place_id,
          naver_map_url:
            locationDraft.country_code === "KR"
              ? locationDraft.naver_map_url
              : null,
          map_match_status: locationDraft.map_match_status,
        }),
      });
      setMessage(ta("hotspotsPanel.locationSaved"));
      setLocationDraft(null);
      setMapCandidate(null);
      await load();
    } catch (error) {
      setMessage((error as Error).message);
      setLoading(false);
    }
  }

  const facets = data?.facets;
  const countryOptions = (facets?.countries ?? []).map((item) => ({
    code: item.code,
    label: item.name,
    count: item.count,
  }));
  if (country && !countryOptions.some((item) => item.code === country)) {
    countryOptions.push({ code: country, label: country, count: 0 });
  }
  const categoryCounts = new Map(
    (facets?.categories ?? []).map((item) => [item.code, item.count]),
  );
  const categoryCodes: string[] = [...HOTSPOT_CATEGORY_CODES];
  for (const code of [...categoryCounts.keys(), category]) {
    if (code && !categoryCodes.includes(code)) categoryCodes.push(code);
  }
  const categoryOptions = categoryCodes.map((code) => ({
    code,
    label: categoryLabel(code),
    count: facets ? (categoryCounts.get(code) ?? 0) : undefined,
  }));
  const groups = groupCandidates(data?.items ?? []);

  const statusSummary = status
    ? ta(`hotspotsPanel.status${status.replace(/(^|_)([a-z])/g, (_all, _lead, letter: string) => letter.toUpperCase())}`)
    : ta("hotspotsPanel.statusAll");
  const filterSummary = [
    statusSummary,
    country
      ? (countryOptions.find((item) => item.code === country)?.label ?? country)
      : t("allCountries"),
    category ? categoryLabel(category) : t("allCategories"),
  ].join(" · ");

  return (
    <section className="mt-8">
      <FilterDisclosure
        label={ta("hotspotsPanel.filtersLabel")}
        summary={filterSummary}
        showLabel={ta("hotspotsPanel.filtersShow")}
        hideLabel={ta("hotspotsPanel.filtersHide")}
        storageKey="mokaair-admin-hotspot-filters"
      >
      <div className="grid gap-2">
        <FilterPills
          label={ta("hotspotsPanel.filterCountry")}
          allLabel={t("allCountries")}
          allCount={facets ? sumCounts(facets.countries) : undefined}
          options={countryOptions}
          value={country}
          onChange={(code) => updateFilter(setCountry, code)}
        />
        <FilterPills
          label={ta("hotspotsPanel.filterCategory")}
          allLabel={t("allCategories")}
          allCount={facets ? sumCounts(facets.categories) : undefined}
          options={categoryOptions}
          value={category}
          onChange={(code) => updateFilter(setCategory, code)}
        />
      </div>
      <div className="mt-3 grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-3 lg:grid-cols-6">
        <select
          aria-label={ta("hotspotsPanel.statusFilter")}
          value={status}
          onChange={(e) => updateFilter(setStatus, e.target.value)}
          className="h-11 rounded-xl border border-[var(--line)] px-3"
        >
          <option value="pending">{ta("hotspotsPanel.statusPending")}</option>
          <option value="approved">{ta("hotspotsPanel.statusApproved")}</option>
          <option value="auto_approved">{ta("hotspotsPanel.statusAutoApproved")}</option>
          <option value="rejected">{ta("hotspotsPanel.statusRejected")}</option>
          <option value="disabled">{ta("hotspotsPanel.statusDisabled")}</option>
          <option value="">{ta("hotspotsPanel.statusAll")}</option>
        </select>
        <input
          aria-label={ta("hotspotsPanel.cityCode")}
          value={city}
          onChange={(e) => updateFilter(setCity, e.target.value.toUpperCase())}
          maxLength={3}
          placeholder={ta("hotspotsPanel.cityCodePlaceholder")}
          className="h-11 rounded-xl border border-[var(--line)] px-3"
        />
        <input
          aria-label={ta("hotspotsPanel.destinationId")}
          value={destinationId}
          onChange={(e) => updateFilter(setDestinationId, e.target.value)}
          placeholder={ta("hotspotsPanel.destinationId")}
          className="h-11 rounded-xl border border-[var(--line)] px-3"
        />
        <select
          aria-label={ta("hotspotsPanel.roleFilter")}
          value={role}
          onChange={(e) => updateFilter(setRole, e.target.value)}
          className="h-11 rounded-xl border border-[var(--line)] px-3"
        >
          <option value="">{ta("hotspotsPanel.roleAll")}</option>
          <option value="primary">{ta("hotspotsPanel.rolePrimary")}</option>
          <option value="secondary">{ta("hotspotsPanel.roleSecondary")}</option>
          <option value="extension">{ta("hotspotsPanel.roleExtensionOption")}</option>
        </select>
        <input
          aria-label={ta("hotspotsPanel.parentId")}
          value={parentId}
          onChange={(e) => updateFilter(setParentId, e.target.value)}
          placeholder={ta("hotspotsPanel.parentId")}
          className="h-11 rounded-xl border border-[var(--line)] px-3"
        />
        <select
          aria-label={ta("hotspotsPanel.originFilter")}
          value={origin}
          onChange={(e) => updateFilter(setOrigin, e.target.value)}
          className="h-11 rounded-xl border border-[var(--line)] px-3"
        >
          <option value="">{ta("hotspotsPanel.originAll")}</option>
          <option value="curated">{ta("hotspotsPanel.originCurated")}</option>
          <option value="wikimedia_discovery">{ta("hotspotsPanel.originWikimedia")}</option>
        </select>
      </div>
      </FilterDisclosure>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <span className="mr-auto text-sm text-[var(--muted)]">
          {ta("hotspotsPanel.totals", { total: data?.total ?? 0, selected: selected.size })}
        </span>
        {selected.size > 0 && <>
        <button
          disabled={!selected.size || loading}
          onClick={() => void review("approve")}
          className="rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        >
          {ta("hotspotsPanel.approve")}
        </button>
        <button
          disabled={!selected.size || loading}
          onClick={() => void review("reject")}
          className="rounded-xl border border-[var(--coral)] px-4 py-2 text-sm font-semibold text-[var(--coral)] disabled:opacity-40"
        >
          {ta("hotspotsPanel.reject")}
        </button>
        <button
          disabled={!selected.size || loading}
          onClick={() => void review("disable")}
          className="rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-40"
        >
          {ta("hotspotsPanel.disable")}
        </button>
        </>}
      </div>
      {/* Nothing here can act on an empty selection, and all of it used to sit between the
          reviewer and the first candidate. */}
      {selected.size > 0 && <>
      <div className="mt-3 flex flex-wrap gap-2">
        <input
          aria-label={ta("hotspotsPanel.moveTo")}
          value={moveDestinationId}
          onChange={(e) => setMoveDestinationId(e.target.value)}
          placeholder={ta("hotspotsPanel.moveToPlaceholder")}
          className="h-10 rounded-xl border border-[var(--line)] px-3"
        />
        <button
          disabled={!selected.size || loading || !moveDestinationId.trim()}
          onClick={() => void moveDestination()}
          className="rounded-xl border border-[var(--teal)] px-4 py-2 text-sm font-semibold text-[var(--teal)] disabled:opacity-40"
        >
          {ta("hotspotsPanel.moveButton")}
        </button>
      </div>
      <div className="mt-4 grid gap-3 rounded-2xl border border-amber-200 bg-amber-50 p-4 md:grid-cols-4">
        <select
          aria-label={ta("hotspotsPanel.depthKind")}
          value={depthKind}
          onChange={(e) =>
            setDepthKind(e.target.value as "urban_local" | "day_trip")
          }
          className="h-10 rounded-xl border px-3"
        >
          <option value="urban_local">{ta("hotspotsPanel.depthUrbanLocal")}</option>
          <option value="day_trip">{ta("hotspotsPanel.depthDayTrip")}</option>
        </select>
        <input
          aria-label={ta("hotspotsPanel.accessMinutes")}
          type="number"
          min={1}
          max={depthKind === "urban_local" ? 45 : 90}
          value={accessMinutes}
          onChange={(e) => setAccessMinutes(Number(e.target.value))}
          className="h-10 rounded-xl border px-3"
        />
        <input
          aria-label={ta("hotspotsPanel.durationMinutes")}
          type="number"
          min={30}
          max={480}
          value={durationMinutes}
          onChange={(e) => setDurationMinutes(Number(e.target.value))}
          className="h-10 rounded-xl border px-3"
        />
        <input
          aria-label={ta("hotspotsPanel.depthReason")}
          value={depthReason}
          onChange={(e) => setDepthReason(e.target.value)}
          placeholder={ta("hotspotsPanel.depthReasonPlaceholder")}
          className="h-10 rounded-xl border px-3"
        />
        {Object.entries(scores).map(([key, value]) => (
          <label key={key} className="text-xs font-semibold">
            {tHotspotAdmin(`depthScores.${key}`)}
            <input
              type="number"
              min={0}
              max={100}
              value={value}
              onChange={(e) =>
                setScores((current) => ({
                  ...current,
                  [key]: Number(e.target.value),
                }))
              }
              className="mt-1 h-9 w-full rounded-xl border px-3"
            />
          </label>
        ))}
        <button
          disabled={!selected.size || loading || !depthReason.trim()}
          onClick={() => void updateDepth(true)}
          className="rounded-xl bg-amber-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        >
          {ta("hotspotsPanel.setDepth")}
        </button>
        <button
          disabled={!selected.size || loading}
          onClick={() => void updateDepth(false)}
          className="rounded-xl border border-amber-700 px-4 py-2 text-sm font-semibold text-amber-900 disabled:opacity-40"
        >
          {ta("hotspotsPanel.clearDepth")}
        </button>
      </div>
      </>}
      {locationDraft && (
        <div className="mt-4 rounded-2xl border border-sky-200 bg-sky-50 p-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h3 className="font-bold">{ta("hotspotsPanel.locationTitle", { name: locationDraft.name })}</h3>
              <p className="text-xs text-[var(--muted)]">
                {ta("hotspotsPanel.locationHint")}
              </p>
            </div>
            <button
              type="button"
              onClick={() => setLocationDraft(null)}
              className="min-h-11 rounded-xl border px-3"
            >
              {ta("hotspotsPanel.close")}
            </button>
          </div>
          <div className="mt-4 grid gap-3 md:grid-cols-2 lg:grid-cols-4">
            <label className="text-xs font-semibold">
              {ta("hotspotsPanel.latitude")}
              <input
                type="number"
                step="any"
                value={locationDraft.latitude ?? ""}
                onChange={(e) =>
                  setLocationDraft({
                    ...locationDraft,
                    latitude: e.target.value ? Number(e.target.value) : null,
                  })
                }
                className="mt-1 h-10 w-full rounded-xl border px-3"
              />
            </label>
            <label className="text-xs font-semibold">
              {ta("hotspotsPanel.longitude")}
              <input
                type="number"
                step="any"
                value={locationDraft.longitude ?? ""}
                onChange={(e) =>
                  setLocationDraft({
                    ...locationDraft,
                    longitude: e.target.value ? Number(e.target.value) : null,
                  })
                }
                className="mt-1 h-10 w-full rounded-xl border px-3"
              />
            </label>
            <label className="text-xs font-semibold">
              {ta("hotspotsPanel.coordinateSourceType")}
              <select
                value={locationDraft.coordinate_source_type ?? ""}
                onChange={(e) =>
                  setLocationDraft({
                    ...locationDraft,
                    coordinate_source_type: e.target.value || null,
                  })
                }
                className="mt-1 h-10 w-full rounded-xl border px-3"
              >
                <option value="">{ta("hotspotsPanel.coordinateSourcePending")}</option>
                <option value="wikidata">Wikidata</option>
                <option value="official_tourism">{ta("hotspotsPanel.coordinateSourceOfficialTourism")}</option>
                <option value="admin_verified">{ta("hotspotsPanel.coordinateSourceAdminVerified")}</option>
                <option value="curated">{ta("hotspotsPanel.coordinateSourceCurated")}</option>
              </select>
            </label>
            <label className="text-xs font-semibold">
              {ta("hotspotsPanel.coordinateSourceUrl")}
              <input
                value={locationDraft.coordinate_source_url ?? ""}
                onChange={(e) =>
                  setLocationDraft({
                    ...locationDraft,
                    coordinate_source_url: e.target.value || null,
                  })
                }
                placeholder="https://"
                className="mt-1 h-10 w-full rounded-xl border px-3"
              />
            </label>
            {locationDraft.country_code === "KR" ? (
              <label className="text-xs font-semibold lg:col-span-2">
                {ta("hotspotsPanel.naverUrl")}
                <input
                  value={locationDraft.naver_map_url ?? ""}
                  onChange={(e) =>
                    setLocationDraft({
                      ...locationDraft,
                      naver_map_url: e.target.value || null,
                    })
                  }
                  placeholder="https://map.naver.com/p/entry/place/..."
                  className="mt-1 h-10 w-full rounded-xl border px-3"
                />
              </label>
            ) : (
              <label className="text-xs font-semibold lg:col-span-2">
                Google Place ID
                <input
                  value={locationDraft.google_place_id ?? ""}
                  onChange={(e) =>
                    setLocationDraft({
                      ...locationDraft,
                      google_place_id: e.target.value || null,
                    })
                  }
                  className="mt-1 h-10 w-full rounded-xl border px-3"
                />
              </label>
            )}
            <label className="text-xs font-semibold">
              {ta("hotspotsPanel.matchStatus")}
              <select
                value={locationDraft.map_match_status}
                onChange={(e) =>
                  setLocationDraft({
                    ...locationDraft,
                    map_match_status: e.target
                      .value as Candidate["map_match_status"],
                  })
                }
                className="mt-1 h-10 w-full rounded-xl border px-3"
              >
                <option value="unverified">{ta("hotspotsPanel.matchUnverified")}</option>
                <option value="verified">{ta("hotspotsPanel.matchVerified")}</option>
                <option value="ambiguous">{ta("hotspotsPanel.matchAmbiguous")}</option>
                <option value="disabled">{ta("hotspotsPanel.matchDisabled")}</option>
              </select>
            </label>
          </div>
          <div className="mt-3 flex flex-wrap gap-2">
            <button
              type="button"
              disabled={locationDraft.country_code === "KR" || loading}
              onClick={() => void searchMapCandidate()}
              className="min-h-11 rounded-xl border border-sky-700 px-4 font-semibold text-sky-900 disabled:opacity-40"
            >
              {ta("hotspotsPanel.searchGoogle")}
            </button>
            <button
              type="button"
              disabled={loading}
              onClick={() => void saveLocation()}
              className="ml-auto min-h-11 rounded-xl bg-sky-800 px-5 font-semibold text-white disabled:opacity-40"
            >
              {ta("hotspotsPanel.saveLocation")}
            </button>
          </div>
          {mapCandidate && (
            <div className="mt-3 rounded-xl border border-sky-300 bg-white p-3 text-sm">
              <strong>{mapCandidate.name}</strong>
              <p className="text-[var(--muted)]">{mapCandidate.address}</p>
              <p className="mt-1 text-xs">
                {ta("hotspotsPanel.temporaryCoordinates")}
                {mapCandidate.temporary_match_coordinates.latitude},{" "}
                {mapCandidate.temporary_match_coordinates.longitude}
              </p>
              <button
                type="button"
                onClick={() =>
                  setLocationDraft({
                    ...locationDraft,
                    google_place_id: mapCandidate.place_id,
                  })
                }
                className="mt-2 min-h-11 rounded-xl bg-sky-700 px-4 font-semibold text-white"
              >
                {ta("hotspotsPanel.applyPlaceId")}
              </button>
            </div>
          )}
        </div>
      )}
      {message && (
        <p role="status" className="mt-3 text-sm text-[var(--muted)]">
          {message}
        </p>
      )}
      <div className="mt-4 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white">
      <table className="admin-responsive-table admin-hotspots-table w-full min-w-[1100px] text-left text-sm">
          <thead className="bg-[var(--paper)]">
            <tr>
              <th className="p-3">{ta("hotspotsPanel.thSelect")}</th>
              <th className="p-3">{ta("hotspotsPanel.thHotspot")}</th>
              <th className="p-3">{ta("hotspotsPanel.thCategoryCity")}</th>
              <th className="p-3">{ta("hotspotsPanel.thDepth")}</th>
              <th className="p-3">{ta("hotspotsPanel.thDistance")}</th>
              <th className="p-3">{ta("hotspotsPanel.thViews")}</th>
              <th className="p-3">{ta("hotspotsPanel.thStatus")}</th>
              <th className="p-3">{ta("hotspotsPanel.thMap")}</th>
              <th className="p-3">{ta("hotspotsPanel.thSources")}</th>
            </tr>
          </thead>
          <tbody>
            {groups.map((countryGroup) => {
              const countryIds = countryGroup.destinations.flatMap((group) =>
                group.items.map((item) => item.id),
              );
              return (
                <Fragment key={countryGroup.countryCode}>
                  <tr className="admin-group-row admin-group-row-country">
                    <th colSpan={9} scope="colgroup">
                      <input
                        type="checkbox"
                        aria-label={ta("hotspotsPanel.selectAllGroup", { name: countryGroup.countryName, code: countryGroup.countryCode })}
                        checked={countryIds.every((id) => selected.has(id))}
                        onChange={(e) => toggleMany(countryIds, e.target.checked)}
                      />
                      {countryGroup.countryName} ({countryGroup.countryCode}) · {ta("hotspotsPanel.pageCount", { count: countryGroup.count })}
                    </th>
                  </tr>
                  {countryGroup.destinations.map((group) => {
                    const ids = group.items.map((item) => item.id);
                    return (
                      <Fragment key={group.destinationId}>
                        <tr className="admin-group-row">
                          <th colSpan={9} scope="colgroup">
                            <input
                              type="checkbox"
                              aria-label={ta("hotspotsPanel.selectAllGroup", { name: group.cityName, code: group.cityCode })}
                              checked={ids.every((id) => selected.has(id))}
                              onChange={(e) => toggleMany(ids, e.target.checked)}
                            />
                            {group.cityName} ({group.cityCode}) · {group.destinationId} ·{" "}
                            {roleLabel(ta, group.role, group.parentId)} · {ta("hotspotsPanel.pageCount", { count: ids.length })}
                          </th>
                        </tr>
                        {group.items.map((item) => (
                          <tr key={item.id} className="border-t border-[var(--line)]">
                            <td className="p-3">
                              <input
                                type="checkbox"
                                checked={selected.has(item.id)}
                                aria-label={ta("hotspotsPanel.selectItem", { name: item.name })}
                                onChange={(e) =>
                                  setSelected((current) => {
                                    const next = new Set(current);
                                    if (e.target.checked) next.add(item.id);
                                    else next.delete(item.id);
                                    return next;
                                  })
                                }
                              />
                            </td>
                            <td className="p-3 font-semibold">
                              {item.name}
                              <span className="block text-xs font-normal text-[var(--muted)]">
                                {item.qid || ta("hotspotsPanel.noQid")}
                              </span>
                            </td>
                            <td className="p-3">
                              {categoryLabel(item.category)}
                              <span className="block text-xs text-[var(--muted)]">
                                {item.city_name} ({item.city_code})
                              </span>
                              <span className="block text-xs text-[var(--muted)]">
                                {item.destination_id} ·{" "}
                                {roleLabel(ta, item.destination_role, item.parent_destination_id)}
                              </span>
                              {item.area_name && (
                                <span className="block text-xs text-[var(--muted)]">
                                  {ta("hotspotsPanel.area", { name: item.area_name })}
                                </span>
                              )}
                              <div className="mt-2">
                                <AdminHotspotThemeEditor
                                  hotspotId={item.id}
                                  hotspotName={item.name}
                                  category={item.category}
                                  initial={item.themes}
                                />
                              </div>
                            </td>
                            <td className="p-3">
                              {item.is_deep_travel ? (
                                <>
                                  <span className="rounded-full bg-amber-100 px-2 py-1 text-xs">
                                    {item.depth_kind === "day_trip" ? ta("hotspotsPanel.depthDayTrip") : ta("hotspotsPanel.depthUrbanLocal")} ·{" "}
                                    {Math.round(item.depth_score || 0)}
                                  </span>
                                  <span className="mt-1 block text-xs text-[var(--muted)]">
                                    {ta("hotspotsPanel.depthLine", { access: item.access_minutes ?? 0, duration: item.recommended_duration_minutes ?? 0 })}
                                  </span>
                                </>
                              ) : (
                                "—"
                              )}
                            </td>
                            <td className="p-3">
                              {item.distance_km?.toFixed(1) ?? "—"} km
                            </td>
                            <td className="p-3">
                              {item.pageviews_30d?.toLocaleString("zh-TW") ?? "—"}
                            </td>
                            <td className="p-3">
                              {item.status}
                              <span className="block text-xs text-[var(--muted)]">
                                {item.reason || "—"}
                              </span>
                            </td>
                            <td className="p-3">
                              {item.map_match_status}
                              <span className="block text-xs text-[var(--muted)]">
                                {item.coordinate_source_type || ta("hotspotsPanel.coordinateSourceMissing")}
                              </span>
                              <button
                                type="button"
                                onClick={() => {
                                  setLocationDraft({ ...item });
                                  setMapCandidate(null);
                                }}
                                className="mt-2 min-h-10 rounded-xl border border-sky-700 px-3 font-semibold text-sky-900"
                              >
                                {ta("hotspotsPanel.editLocation")}
                              </button>
                            </td>
                            <td className="p-3">
                              {item.source_urls.map((url, index) => (
                                <a
                                  key={url}
                                  href={safeExternalHref(url)}
                                  target="_blank"
                                  rel="noreferrer"
                                  className="mr-2 font-semibold text-[var(--teal)]"
                                >
                                  {ta("hotspotsPanel.sourceN", { index: index + 1 })}
                                </a>
                              ))}
                            </td>
                          </tr>
                        ))}
                      </Fragment>
                    );
                  })}
                </Fragment>
              );
            })}
          </tbody>
        </table>
        {!loading && data?.items?.length === 0 && (
          <p className="p-8 text-center text-[var(--muted)]">
            {ta("hotspotsPanel.empty")}
          </p>
        )}
      </div>
      {data && data.pages > 1 && (
        <nav aria-label={ta("hotspotsPanel.paginationLabel")} className="mt-4 flex items-center justify-end gap-3">
          <button
            type="button"
            disabled={page <= 1 || loading}
            onClick={() => setPage((current) => Math.max(1, current - 1))}
            className="min-h-11 rounded-xl border px-4 text-sm font-semibold disabled:opacity-40"
          >
            {ta("hotspotsPanel.previous")}
          </button>
          <span className="text-sm text-[var(--muted)]">
            {ta("hotspotsPanel.pageOf", { page, pages: data.pages })}
          </span>
          <button
            type="button"
            disabled={page >= data.pages || loading}
            onClick={() => setPage((current) => Math.min(data.pages, current + 1))}
            className="min-h-11 rounded-xl border px-4 text-sm font-semibold disabled:opacity-40"
          >
            {ta("hotspotsPanel.next")}
          </button>
        </nav>
      )}
    </section>
  );
}
