"use client";

import { Fragment, useCallback, useEffect, useRef, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { AdminMapIdentitiesPanel } from "./admin-map-identities-panel";
import { mapIdentityCopy } from "@/lib/map-identity-copy";
import { useSearchParams } from "next/navigation";
import { api } from "@/lib/api";
import { Link } from "@/i18n/navigation";
import { adminCatalogCopy, hotspotIdentityHref, hotspotIdentityListHref } from "@/lib/admin-catalog-copy";
import { hotspotReviewCopy } from "@/lib/hotspot-review-copy";
import { HOTSPOT_CATEGORY_CODES, isHotspotCategoryCode } from "@/lib/hotspot-categories";
import { safeExternalHref } from "@/lib/navigation";
import { naverMapSearchUrl } from "@/lib/naver-map";
import { FilterDisclosure, FilterPills } from "./admin-filter-pills";
import { AdminReadOnlyNotice, useAdminActionGuard } from "./admin-action-guard";
import { AdminHotspotIntroGenerator } from "./admin-hotspot-intro-generator";
import { AdminHotspotThemeEditor, type AssignedTheme } from "./admin-hotspot-theme-editor";

type Candidate = {
  id: string;
  name: string;
  themes?: AssignedTheme[];
  qid: string | null;
  updated_at?: string;
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

export function AdminHotspotsPanel({
  initialStatus = "pending", locationEditing = "inline", initialHotspotId,
  initialMissingLocation = false,
}: {
  initialStatus?: string;
  locationEditing?: "inline" | "link";
  initialHotspotId?: string;
  initialMissingLocation?: boolean;
}) {
  const manage = useAdminActionGuard("content.manage");
  const copy = adminCatalogCopy(useLocale());
  const reviewCopy = hotspotReviewCopy(useLocale());
  const mapCopy = mapIdentityCopy(useLocale());
  const search = useSearchParams();
  const t = useTranslations("hotspots");
  const tHotspotAdmin = useTranslations("hotspotAdmin");
  const ta = useTranslations("admin");
  const [data, setData] = useState<Response | null>(null);
  const [status, setStatus] = useState(initialStatus);
  const [city, setCity] = useState("");
  const [destinationId, setDestinationId] = useState("");
  const [role, setRole] = useState("");
  const [parentId, setParentId] = useState("");
  const [origin, setOrigin] = useState("");
  const [country, setCountry] = useState("");
  const [category, setCategory] = useState("");
  const [page, setPage] = useState(1);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const selectedVersions = useRef(new Map<string, string>());
  const [reviewReason, setReviewReason] = useState("");
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
  const [locationOriginal, setLocationOriginal] = useState<Candidate | null>(null);
  const [locationConflict, setLocationConflict] = useState(false);
  const [locationBusy, setLocationBusy] = useState(false);
  const [mapCandidate, setMapCandidate] = useState<MapCandidate | null>(null);
  const locationDirty = locationDraft !== null && JSON.stringify(locationDraft) !== JSON.stringify(locationOriginal);
  // List-filter requests finish independently of a save or candidate lookup.
  // Their loading state must never unlock an editor whose own request is pending.
  const actionBusy = loading || locationBusy;

  useEffect(() => {
    if (!locationDirty && !locationBusy) return;
    const warn = (event: BeforeUnloadEvent) => { event.preventDefault(); event.returnValue = ""; };
    const canLeave = () => !locationBusy && (!locationDirty || window.confirm(reviewCopy.discard));
    const beforeNavigate = (event: Event) => {
      const url = (event as CustomEvent<{ url?: string }>).detail?.url;
      if (!event.defaultPrevented && url && new URL(url, window.location.href).href !== window.location.href && !canLeave()) {
        event.preventDefault();
      }
    };
    const click = (event: MouseEvent) => {
      if (event.defaultPrevented || event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
      const anchor = event.target instanceof Element ? event.target.closest("a[href]") : null;
      if (!(anchor instanceof HTMLAnchorElement) || (anchor.target && anchor.target !== "_self") || anchor.hasAttribute("download")) return;
      if (anchor.href !== window.location.href && !canLeave()) { event.preventDefault(); event.stopPropagation(); }
    };
    window.addEventListener("beforeunload", warn);
    window.addEventListener("admin:before-navigate", beforeNavigate);
    document.addEventListener("click", click, true);
    return () => {
      window.removeEventListener("beforeunload", warn);
      window.removeEventListener("admin:before-navigate", beforeNavigate);
      document.removeEventListener("click", click, true);
    };
  }, [locationDirty, locationBusy, reviewCopy.discard]);

  function openLocationEditor(item: Candidate) {
    if (actionBusy) return;
    if (locationDirty && !window.confirm(reviewCopy.discard)) return;
    setLocationOriginal(item);
    setLocationDraft(item);
    setLocationConflict(false);
    setMapCandidate(null);
  }

  function closeLocationEditor() {
    if (actionBusy) return;
    if (locationDirty && !window.confirm(reviewCopy.discard)) return;
    setLocationDraft(null);
    setLocationOriginal(null);
    setLocationConflict(false);
    setMapCandidate(null);
  }

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams({ limit: String(PAGE_SIZE), page: String(page) });
    if (initialHotspotId) params.set("hotspot_id", initialHotspotId);
    if (initialMissingLocation) params.set("missing_location", "true");
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
  }, [category, city, country, destinationId, initialHotspotId, initialMissingLocation, origin, page, parentId, role, status]);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);

  function updateFilter(setter: (value: string) => void, value: string) {
    setter(value);
    setPage(1);
  }

  function toggleMany(ids: string[], checked: boolean) {
    for (const id of ids) {
      const version = data?.items.find((item) => item.id === id)?.updated_at;
      if (checked && version) selectedVersions.current.set(id, version);
      if (!checked) selectedVersions.current.delete(id);
    }
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
    if (!manage.allowed || !selected.size || actionBusy) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/review", {
        method: "POST",
        body: JSON.stringify({
          ids: [...selected], action,
          ...(reviewReason.trim() ? { reason: reviewReason.trim() } : {}),
          ...([...selected].every((id) => selectedVersions.current.has(id)) ? {
            expected_updated_ats: Object.fromEntries([...selected].map((id) => [id, selectedVersions.current.get(id)])),
          } : {}),
        }),
      });
      setMessage(ta("hotspotsPanel.reviewed", { count: selected.size }));
      setSelected(new Set());
      selectedVersions.current.clear();
      setReviewReason("");
      await load();
    } catch (error) {
      setMessage((error as Error).message);
      setLoading(false);
    }
  }

  async function updateDepth(isDeep: boolean) {
    if (!manage.allowed || !selected.size || actionBusy) return;
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
    if (!manage.allowed || !selected.size || !moveDestinationId.trim() || actionBusy) return;
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
    if (!manage.allowed || !locationDraft || locationDraft.country_code === "KR" || actionBusy) return;
    setLocationBusy(true);
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
      setLocationBusy(false);
    }
  }

  async function saveLocation() {
    if (!manage.allowed || !locationDraft || !locationOriginal || actionBusy || locationConflict) return;
    const identityChanged = locationDraft.category !== locationOriginal.category || locationDraft.qid !== locationOriginal.qid;
    if (identityChanged && !locationDraft.reason?.trim()) {
      setMessage(reviewCopy.required);
      return;
    }
    const changes: Record<string, unknown> = {};
    const editable = ["category", "reason", "latitude", "longitude", "coordinate_source_type", "coordinate_source_url", "google_place_id", "naver_map_url", "map_match_status"] as const;
    for (const key of editable) {
      if (locationDraft[key] !== locationOriginal[key]) changes[key] = locationDraft[key];
    }
    // The API validates coordinates as a pair even when only one changed.
    if ("latitude" in changes || "longitude" in changes) {
      changes.latitude = locationDraft.latitude;
      changes.longitude = locationDraft.longitude;
    }
    if (locationDraft.qid !== locationOriginal.qid) changes.wikidata_item_id = locationDraft.qid?.trim() || null;
    if (identityChanged) changes.reason = locationDraft.reason?.trim();
    setLocationBusy(true);
    setLoading(true);
    try {
      await api("/admin/hotspots/review", {
        method: "POST",
        body: JSON.stringify({
          ids: [locationDraft.id],
          action: "update",
          expected_updated_at: locationOriginal.updated_at,
          ...changes,
        }),
      });
      setMessage(ta("hotspotsPanel.locationSaved"));
      setLocationDraft(null);
      setLocationOriginal(null);
      setMapCandidate(null);
      await load();
    } catch (error) {
      if ((error as { code?: string }).code === "hotspot_review_conflict") setLocationConflict(true);
      setMessage((error as Error).message);
      setLoading(false);
    } finally {
      setLocationBusy(false);
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
      <AdminReadOnlyNotice capability="content.manage" className="mb-4" />
      {(initialHotspotId || initialMissingLocation) && <div className="mb-3 flex flex-wrap items-center gap-3 text-sm">
        <p role="status" className="text-[var(--muted)]">{initialHotspotId ? copy.filteredLocation : copy.missingLocation}</p>
        <Link href={hotspotIdentityListHref(search)} className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-3 font-semibold text-[var(--teal)] focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{copy.showAllLocations}</Link>
      </div>}
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
          disabled={!manage.allowed || !selected.size || actionBusy}
          onClick={() => void review("approve")}
          className="rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        >
          {ta("hotspotsPanel.approve")}
        </button>
        <button
          disabled={!manage.allowed || !selected.size || actionBusy}
          onClick={() => void review("reject")}
          className="rounded-xl border border-[var(--coral)] px-4 py-2 text-sm font-semibold text-[var(--coral)] disabled:opacity-40"
        >
          {ta("hotspotsPanel.reject")}
        </button>
        <button
          disabled={!manage.allowed || !selected.size || actionBusy}
          onClick={() => void review("disable")}
          className="rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-40"
        >
          {ta("hotspotsPanel.disable")}
        </button>
        </>}
      </div>
      {selected.size > 0 && <label className="mt-3 block text-sm font-semibold">
        {reviewCopy.batchReason}
        <textarea aria-label={reviewCopy.batchReason} value={reviewReason} maxLength={500} disabled={actionBusy || !manage.allowed}
          onChange={(event) => setReviewReason(event.target.value)}
          className="mt-1 min-h-20 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] p-3 text-[var(--ink)]" />
        <span className="block text-xs font-normal text-[var(--muted)]">{reviewCopy.reasonHint}</span>
      </label>}
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
          disabled={!manage.allowed || !selected.size || actionBusy || !moveDestinationId.trim()}
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
          disabled={!manage.allowed || !selected.size || actionBusy || !depthReason.trim()}
          onClick={() => void updateDepth(true)}
          className="rounded-xl bg-amber-700 px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
        >
          {ta("hotspotsPanel.setDepth")}
        </button>
        <button
          disabled={!manage.allowed || !selected.size || actionBusy}
          onClick={() => void updateDepth(false)}
          className="rounded-xl border border-amber-700 px-4 py-2 text-sm font-semibold text-amber-900 disabled:opacity-40"
        >
          {ta("hotspotsPanel.clearDepth")}
        </button>
      </div>
      </>}
      {locationDraft && (
        <form onSubmit={(event) => { event.preventDefault(); void saveLocation(); }}
          className="mt-4 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4 text-[var(--ink)]">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h3 className="font-bold">{ta("hotspotsPanel.locationTitle", { name: locationDraft.name })}</h3>
              <p className="text-xs text-[var(--muted)]">
                {ta("hotspotsPanel.locationHint")}
              </p>
            </div>
            <button
              type="button"
              onClick={closeLocationEditor}
              disabled={actionBusy}
              className="min-h-11 rounded-xl border px-3"
            >
              {ta("hotspotsPanel.close")}
            </button>
          </div>
          <fieldset disabled={!manage.allowed || actionBusy} className="mt-4 grid gap-3 md:grid-cols-2">
            <label className="text-sm font-semibold">
              {reviewCopy.category}
              <select value={locationDraft.category} autoFocus
                onChange={(event) => setLocationDraft({ ...locationDraft, category: event.target.value })}
                className="mt-1 min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3">
                {!isHotspotCategoryCode(locationDraft.category) && <option value={locationDraft.category}>{locationDraft.category}</option>}
                {HOTSPOT_CATEGORY_CODES.map((code) => <option key={code} value={code}>{categoryLabel(code)}</option>)}
              </select>
            </label>
            <label className="text-sm font-semibold">
              {reviewCopy.qid}
              <input value={locationDraft.qid ?? ""} readOnly={!!locationOriginal?.qid?.trim()}
                pattern="Q[1-9][0-9]*" maxLength={32} aria-describedby="hotspot-qid-hint"
                onChange={(event) => setLocationDraft({ ...locationDraft, qid: event.target.value || null })}
                className="mt-1 min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 read-only:text-[var(--muted)]" />
            </label>
            <p id="hotspot-qid-hint" className="text-xs text-[var(--muted)] md:col-span-2">{reviewCopy.qidHint}</p>
            <label className="text-sm font-semibold md:col-span-2">
              {reviewCopy.reason}
              <textarea aria-label={reviewCopy.reason} value={locationDraft.reason ?? ""} maxLength={500}
                onChange={(event) => setLocationDraft({ ...locationDraft, reason: event.target.value || null })}
                className="mt-1 min-h-20 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] p-3" />
              <span className="block text-xs font-normal text-[var(--muted)]">{reviewCopy.reasonHint}</span>
            </label>
          </fieldset>
          <fieldset disabled={!manage.allowed || actionBusy} className="mt-4 grid gap-3 md:grid-cols-2 lg:grid-cols-4">
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
            {(locationDraft.country_code === "KR" || locationDraft.naver_map_url) && (
              <div className="lg:col-span-2">
                <label className="text-xs font-semibold">
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
                <a
                  href={naverMapSearchUrl(
                    locationDraft.name,
                    locationDraft.destination_id,
                    locationDraft.city_name,
                  )}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="mt-2 inline-flex min-h-11 items-center rounded-xl border border-[var(--teal)] px-4 text-sm font-semibold text-[var(--teal)]"
                >
                  {ta("hotspotsPanel.openNaverSearch")}
                </a>
              </div>
            )}
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
            {locationDraft.country_code === "KR" && <p className="text-sm text-[var(--muted)] lg:col-span-2">{mapCopy.independent}</p>}
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
          </fieldset>
          <div className="mt-3 flex flex-wrap gap-2">
            <button
              type="button"
              disabled={!manage.allowed || locationDraft.country_code === "KR" || actionBusy}
              onClick={() => void searchMapCandidate()}
              className="min-h-11 rounded-xl border border-sky-700 px-4 font-semibold text-sky-900 disabled:opacity-40"
            >
              {ta("hotspotsPanel.searchGoogle")}
            </button>
            <button
              type="submit"
              disabled={!manage.allowed || actionBusy || locationConflict}
              className="ml-auto min-h-11 rounded-xl bg-sky-800 px-5 font-semibold text-white disabled:opacity-40"
            >
              {ta("hotspotsPanel.saveLocation")}
            </button>
          </div>
          {locationConflict && <div role="alert" className="mt-3 rounded-xl border border-[var(--coral)] p-3 text-sm">
            <p>{reviewCopy.conflict}</p>
            <button type="button" disabled={actionBusy} className="mt-2 min-h-11 rounded-xl border border-[var(--line)] px-3"
              onClick={async () => {
                if (actionBusy || !window.confirm(reviewCopy.discard)) return;
                setLocationBusy(true);
                setLoading(true);
                try {
                  const result = await api<Response>(`/admin/hotspots/candidates?hotspot_id=${locationDraft.id}&limit=1`);
                  const latest = result.items.find((item) => item.id === locationDraft.id);
                  if (latest) {
                    setLocationOriginal(latest); setLocationDraft(latest); setLocationConflict(false); setMapCandidate(null);
                  }
                } catch (error) { setMessage((error as Error).message); }
                finally { setLoading(false); setLocationBusy(false); }
              }}>{reviewCopy.refresh}</button>
          </div>}
          {mapCandidate && (
            <div className="mt-3 rounded-xl border border-[var(--line)] bg-[var(--surface)] p-3 text-sm">
              <strong>{mapCandidate.name}</strong>
              <p className="text-[var(--muted)]">{mapCandidate.address}</p>
              <p className="mt-1 text-xs">
                {ta("hotspotsPanel.temporaryCoordinates")}
                {mapCandidate.temporary_match_coordinates.latitude},{" "}
                {mapCandidate.temporary_match_coordinates.longitude}
              </p>
              <button
                type="button"
                disabled={actionBusy || !manage.allowed}
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
        </form>
      )}
      {locationEditing !== "link" && <AdminMapIdentitiesPanel initialKind="hotspot" canManage={manage.allowed} />}
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
                            <td data-label={ta("hotspotsPanel.thSelect")} className="p-3">
                              <input
                                type="checkbox"
                                checked={selected.has(item.id)}
                                aria-label={ta("hotspotsPanel.selectItem", { name: item.name })}
                                onChange={(e) => toggleMany([item.id], e.target.checked)}
                              />
                            </td>
                            <td data-label={ta("hotspotsPanel.thHotspot")} className="p-3 font-semibold">
                              {item.name}
                              <span className="block text-xs font-normal text-[var(--muted)]">
                                {item.qid || ta("hotspotsPanel.noQid")}
                              </span>
                            </td>
                            <td data-label={ta("hotspotsPanel.thCategoryCity")} className="p-3">
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
                                {manage.allowed && <AdminHotspotThemeEditor
                                  hotspotId={item.id}
                                  hotspotName={item.name}
                                  category={item.category}
                                  initial={item.themes}
                                />}
                              </div>
                              <div className="mt-2">
                                {manage.allowed && <AdminHotspotIntroGenerator
                                  hotspotId={item.id}
                                  hotspotName={item.name}
                                />}
                              </div>
                            </td>
                            <td data-label={ta("hotspotsPanel.thDepth")} className="p-3">
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
                            <td data-label={ta("hotspotsPanel.thDistance")} className="p-3">
                              {item.distance_km?.toFixed(1) ?? "—"} km
                            </td>
                            <td data-label={ta("hotspotsPanel.thViews")} className="p-3">
                              {item.pageviews_30d?.toLocaleString("zh-TW") ?? "—"}
                            </td>
                            <td data-label={ta("hotspotsPanel.thStatus")} className="p-3">
                              {item.status}
                              <span className="block text-xs text-[var(--muted)]">
                                {item.reason || "—"}
                              </span>
                            </td>
                            <td data-label={ta("hotspotsPanel.thMap")} className="p-3">
                              {item.map_match_status}
                              <span className="block text-xs text-[var(--muted)]">
                                {item.coordinate_source_type || ta("hotspotsPanel.coordinateSourceMissing")}
                              </span>
                              {locationEditing === "link" ? <Link
                                href={hotspotIdentityHref(item.id)}
                                className="mt-2 inline-flex min-h-11 items-center rounded-xl border border-sky-700 px-3 font-semibold text-sky-900"
                              >{copy.identityEditor}</Link> : <button
                                type="button"
                                disabled={!manage.allowed || actionBusy}
                                title={!manage.allowed ? manage.disabledReason : undefined}
                                onClick={() => openLocationEditor(item)}
                                className="mt-2 min-h-11 rounded-xl border border-sky-700 px-3 font-semibold text-sky-900"
                              >
                                {ta("hotspotsPanel.editLocation")}
                              </button>}
                            </td>
                            <td data-label={ta("hotspotsPanel.thSources")} className="p-3">
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
            disabled={page <= 1 || actionBusy}
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
            disabled={page >= data.pages || actionBusy}
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
