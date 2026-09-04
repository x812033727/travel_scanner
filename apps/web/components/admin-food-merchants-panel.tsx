"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import {
  loadCities,
  type AdminArea,
  type AdminCategory,
  type FoodCity,
} from "./admin-food-taxonomy-panel";

type MerchantClaim =
  "display_name" | "address" | "official_website" | "coordinates";
type MerchantSource = {
  id?: string;
  source_type: "official_tourism" | "merchant_official" | "michelin_licensed";
  source_scope:
    | "destination_context"
    | "merchant_listing"
    | "merchant_website"
    | "coordinates";
  source_title: string;
  source_url: string;
  claims: MerchantClaim[];
  edition_year: number | null;
  distinction: string | null;
  is_current: boolean;
  last_verified_at?: string;
};

type Merchant = {
  id: string;
  slug: string;
  destination_id: string;
  country_code: string;
  name: string;
  local_name: string;
  address: string | null;
  latitude: number | null;
  longitude: number | null;
  coordinate_source_type: string | null;
  coordinate_source_url: string | null;
  coordinate_verified_at: string | null;
  google_place_id: string | null;
  naver_map_url: string | null;
  official_website_url: string | null;
  official_website_verified_at: string | null;
  map_match_status: "unverified" | "verified" | "ambiguous" | "disabled";
  review_status: "pending" | "approved" | "rejected" | "disabled";
  is_active: boolean;
  display_order: number;
  area: { id: string; slug: string; name: string; destination_id: string } | null;
  area_source: string | null;
  categories: { id: string; slug: string; name: string; is_primary: boolean; source: string }[];
  foods: { id: string; slug: string; name: string }[];
  sources: MerchantSource[];
};

export type MerchantTaxonomyFilter = "missing_area" | "missing_category";
type DishOption = { id: string; slug: string; local_name: string; country_code: string };
type MerchantResponse = { items: Merchant[]; total: number };
type MapCandidateResponse = {
  configured: boolean;
  reason: string;
  message?: string;
  candidates: {
    place_id: string;
    name: string;
    address: string;
    google_maps_url: string;
    temporary_match_coordinates: {
      latitude: number;
      longitude: number;
      expires_in_days: number;
      usage: "comparison_only";
    };
  }[];
};

type BatchCandidateResult = {
  merchant: Merchant;
  response: MapCandidateResponse | null;
  error?: string;
};

function nullableNumber(value: string): number | null {
  return value.trim() ? Number(value) : null;
}

function emptyDirectSource(): MerchantSource {
  return {
    source_type: "merchant_official",
    source_scope: "merchant_website",
    source_title: "",
    source_url: "",
    claims: ["display_name", "official_website"],
    edition_year: null,
    distinction: null,
    is_current: true,
  };
}

function withTaxonomyDefaults(merchant: Merchant): Merchant {
  return {
    ...merchant,
    display_order: merchant.display_order ?? 100,
    area: merchant.area ?? null,
    area_source: merchant.area_source ?? null,
    categories: merchant.categories ?? [],
    foods: merchant.foods ?? [],
  };
}

function normalise(response: MerchantResponse): MerchantResponse {
  return { ...response, items: (response.items ?? []).map(withTaxonomyDefaults) };
}

function blankMerchant(): Merchant {
  return {
    id: "",
    slug: "",
    destination_id: "",
    country_code: "",
    name: "",
    local_name: "",
    address: null,
    latitude: null,
    longitude: null,
    coordinate_source_type: null,
    coordinate_source_url: null,
    coordinate_verified_at: null,
    google_place_id: null,
    naver_map_url: null,
    official_website_url: null,
    official_website_verified_at: null,
    map_match_status: "unverified",
    review_status: "pending",
    is_active: false,
    display_order: 100,
    area: null,
    area_source: null,
    categories: [],
    foods: [],
    sources: [
      {
        source_type: "official_tourism",
        source_scope: "destination_context",
        source_title: "",
        source_url: "",
        claims: [],
        edition_year: null,
        distinction: null,
        is_current: true,
      },
    ],
  };
}

function orderedCategorySlugs(merchant: Merchant): string[] {
  const primary = merchant.categories.find((item) => item.is_primary);
  return [
    ...(primary ? [primary.slug] : []),
    ...merchant.categories.filter((item) => !item.is_primary).map((item) => item.slug),
  ];
}

export function AdminFoodMerchantsPanel({
  initialTaxonomy = "",
}: {
  initialTaxonomy?: MerchantTaxonomyFilter | "";
} = {}) {
  const t = useTranslations("foodAdmin");
  const [cities, setCities] = useState<FoodCity[]>([]);
  const [categories, setCategories] = useState<AdminCategory[]>([]);
  const [filterArea, setFilterArea] = useState("");
  const [filterCategory, setFilterCategory] = useState("");
  const [taxonomy, setTaxonomy] = useState<MerchantTaxonomyFilter | "">(initialTaxonomy);
  const [filterAreas, setFilterAreas] = useState<AdminArea[]>([]);
  const [editorAreas, setEditorAreas] = useState<AdminArea[]>([]);
  const [dishOptions, setDishOptions] = useState<DishOption[]>([]);
  const [data, setData] = useState<MerchantResponse | null>(null);
  const [destination, setDestination] = useState("");
  const [mapStatus, setMapStatus] = useState("");
  const [officialData, setOfficialData] = useState("");
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [batchCandidates, setBatchCandidates] = useState<
    BatchCandidateResult[]
  >([]);
  const [editing, setEditing] = useState<Merchant | null>(null);
  const [candidate, setCandidate] = useState<MapCandidateResponse | null>(null);
  // The page-level message banner sits behind the editor overlay, so the editor
  // reports the result of applying a candidate in its own notice instead.
  const [applyNotice, setApplyNotice] = useState("");
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    const params = new URLSearchParams({ limit: "100" });
    if (destination.trim()) params.set("destination_id", destination.trim());
    if (mapStatus) params.set("map_status", mapStatus);
    if (officialData) params.set("official_data", officialData);
    if (filterArea) params.set("area_slug", filterArea);
    if (filterCategory) params.set("category", filterCategory);
    if (taxonomy) params.set("taxonomy", taxonomy);
    if (query.trim()) params.set("q", query.trim());
    try {
      setData(normalise(await api<MerchantResponse>(`/admin/foods/merchants?${params}`)));
      setSelected(new Set());
      setBatchCandidates([]);
    } catch (reason) {
      setMessage((reason as Error).message);
    }
  }, [destination, filterArea, filterCategory, mapStatus, officialData, query, taxonomy]);

  useEffect(() => {
    const params = new URLSearchParams({ limit: "100" });
    if (destination.trim()) params.set("destination_id", destination.trim());
    if (mapStatus) params.set("map_status", mapStatus);
    if (officialData) params.set("official_data", officialData);
    if (filterArea) params.set("area_slug", filterArea);
    if (filterCategory) params.set("category", filterCategory);
    if (taxonomy) params.set("taxonomy", taxonomy);
    if (query.trim()) params.set("q", query.trim());
    void api<MerchantResponse>(`/admin/foods/merchants?${params}`)
      .then((response) => {
        setData(normalise(response));
        setSelected(new Set());
        setBatchCandidates([]);
      })
      .catch((reason: Error) => setMessage(reason.message));
  }, [destination, filterArea, filterCategory, mapStatus, officialData, query, taxonomy]);

  useEffect(() => {
    loadCities()
      .then(setCities)
      .catch((reason: Error) => setMessage(reason.message));
    api<{ items: AdminCategory[] }>("/admin/foods/categories")
      .then((response) => setCategories(response.items ?? []))
      .catch((reason: Error) => setMessage(reason.message));
  }, []);

  useEffect(() => {
    if (!destination) return;
    api<{ items: AdminArea[] }>(
      `/admin/foods/areas?destination_id=${encodeURIComponent(destination)}&limit=200`,
    )
      .then((response) => setFilterAreas(response.items ?? []))
      .catch((reason: Error) => setMessage(reason.message));
  }, [destination]);

  const editingDestination = editing?.destination_id ?? "";
  const editingCountry = editing?.country_code ?? "";

  useEffect(() => {
    if (!editingDestination) return;
    api<{ items: AdminArea[] }>(
      `/admin/foods/areas?destination_id=${encodeURIComponent(editingDestination)}&status=active&limit=200`,
    )
      .then((response) => setEditorAreas(response.items ?? []))
      .catch((reason: Error) => setMessage(reason.message));
  }, [editingDestination]);

  useEffect(() => {
    if (!editingCountry) return;
    api<{ items: DishOption[] }>(
      `/admin/foods?country_code=${encodeURIComponent(editingCountry)}&limit=100`,
    )
      .then((response) => setDishOptions(response.items ?? []))
      .catch((reason: Error) => setMessage(reason.message));
  }, [editingCountry]);

  const scopedFilterAreas = filterAreas.filter((area) => area.destination_id === destination);
  const scopedEditorAreas = editorAreas.filter(
    (area) => area.destination_id === editingDestination,
  );
  const scopedDishOptions = dishOptions.filter((dish) => dish.country_code === editingCountry);
  const visibleIds = data?.items.map((merchant) => merchant.id) ?? [];
  const allVisibleSelected =
    visibleIds.length > 0 && visibleIds.every((id) => selected.has(id));

  function toggleSelection(id: string) {
    setSelected((current) => {
      const next = new Set(current);
      if (next.has(id)) next.delete(id);
      else next.add(id);
      return next;
    });
  }

  function toggleAllVisible() {
    setSelected((current) => {
      const next = new Set(current);
      if (allVisibleSelected) visibleIds.forEach((id) => next.delete(id));
      else visibleIds.forEach((id) => next.add(id));
      return next;
    });
  }

  async function batchUpdate(action: "verify_activate" | "disable") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/foods/merchants/batch", {
        method: "POST",
        body: JSON.stringify({ ids: [...selected], action }),
      });
      setMessage(
        action === "verify_activate"
          ? `已將 ${selected.size} 間店家設為已驗證、核准並啟用。`
          : `已停用 ${selected.size} 間店家。`,
      );
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function searchBatchGoogleCandidates() {
    const merchants = (data?.items ?? []).filter(
      (merchant) => selected.has(merchant.id) && merchant.country_code !== "KR",
    );
    if (!merchants.length) {
      setMessage("所選項目沒有可使用 Google 候選搜尋的非韓國店家。");
      return;
    }
    setLoading(true);
    setBatchCandidates([]);
    const results: BatchCandidateResult[] = new Array(merchants.length);
    let cursor = 0;
    async function worker() {
      while (cursor < merchants.length) {
        const index = cursor++;
        const merchant = merchants[index];
        try {
          const response = await api<MapCandidateResponse>(
            "/admin/foods/merchants/map-candidates",
            {
              method: "POST",
              body: JSON.stringify({
                query: `${merchant.local_name} ${merchant.destination_id}`,
                country_code: merchant.country_code,
                latitude: merchant.latitude,
                longitude: merchant.longitude,
              }),
            },
          );
          results[index] = { merchant, response };
        } catch (reason) {
          results[index] = {
            merchant,
            response: null,
            error: (reason as Error).message,
          };
        }
      }
    }
    try {
      await Promise.all(
        Array.from({ length: Math.min(3, merchants.length) }, () => worker()),
      );
      setBatchCandidates(results);
      const found = results.filter(
        (result) => result.response?.candidates.length,
      ).length;
      const skipped = selected.size - merchants.length;
      setMessage(
        `已完成 ${merchants.length} 間 Google 候選搜尋，${found} 間有候選${skipped ? `；略過 ${skipped} 間韓國店家` : ""}。請逐筆比對後套用。`,
      );
    } finally {
      setLoading(false);
    }
  }

  async function applyBatchCandidate(merchant: Merchant, placeId: string) {
    setLoading(true);
    try {
      await api(`/admin/foods/merchants/${merchant.id}`, {
        method: "PATCH",
        body: JSON.stringify({
          google_place_id: placeId,
          map_match_status: "unverified",
        }),
      });
      setBatchCandidates((current) =>
        current.filter((result) => result.merchant.id !== merchant.id),
      );
      setData((current) =>
        current
          ? {
              ...current,
              items: current.items.map((item) =>
                item.id === merchant.id
                  ? {
                      ...item,
                      google_place_id: placeId,
                      map_match_status: "unverified",
                    }
                  : item,
              ),
            }
          : current,
      );
      setMessage(`${merchant.name} 已套用 Place ID，仍保留人工審核。`);
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  function applyCandidateToEditor(placeId: string) {
    if (!editing) return;
    if (editing.google_place_id === placeId) {
      setApplyNotice(t("merchants.applyUnchanged"));
      return;
    }
    setEditing({
      ...editing,
      google_place_id: placeId,
      map_match_status: "unverified",
    });
    setApplyNotice(t("merchants.applyFilled"));
  }

  async function searchGoogleCandidate() {
    if (!editing || editing.country_code === "KR") return;
    setApplyNotice("");
    setLoading(true);
    try {
      const result = await api<MapCandidateResponse>(
        "/admin/foods/merchants/map-candidates",
        {
          method: "POST",
          body: JSON.stringify({
            query: `${editing.local_name} ${editing.destination_id}`,
            country_code: editing.country_code,
            latitude: editing.latitude,
            longitude: editing.longitude,
          }),
        },
      );
      setCandidate(result);
      setMessage(
        result.message ??
          (result.candidates.length
            ? "找到候選；請比對名稱與地址後再套用 Place ID。"
            : "找不到唯一候選。"),
      );
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function save() {
    if (!editing) return;
    setLoading(true);
    try {
      await api(editing.id ? `/admin/foods/merchants/${editing.id}` : "/admin/foods/merchants", {
        method: editing.id ? "PATCH" : "POST",
        body: JSON.stringify({
          ...(editing.id ? {} : { slug: editing.slug }),
          area_slug: editing.area?.slug ?? null,
          category_slugs: orderedCategorySlugs(editing),
          food_ids: editing.foods.map((food) => food.id),
          display_order: editing.display_order,
          destination_id: editing.destination_id,
          country_code: editing.country_code,
          name: editing.name,
          local_name: editing.local_name,
          address: editing.address,
          latitude: editing.latitude,
          longitude: editing.longitude,
          coordinate_source_type: editing.coordinate_source_type,
          coordinate_source_url: editing.coordinate_source_url,
          google_place_id:
            editing.country_code === "KR" ? null : editing.google_place_id,
          naver_map_url:
            editing.country_code === "KR" ? editing.naver_map_url : null,
          official_website_url: editing.official_website_url,
          map_match_status: editing.map_match_status,
          review_status: editing.review_status,
          is_active: editing.is_active,
          sources: editing.sources.map((source) => ({
            source_type: source.source_type,
            source_scope: source.source_scope,
            source_title: source.source_title,
            source_url: source.source_url,
            claims: source.claims,
            edition_year: source.edition_year,
            distinction: source.distinction,
            is_current: source.is_current,
          })),
        }),
      });
      setMessage(editing.id ? "已儲存店家地點與來源資料。" : t("merchants.created"));
      setEditing(null);
      setCandidate(null);
      setApplyNotice("");
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  function updateSource(index: number, patch: Partial<MerchantSource>) {
    if (!editing) return;
    setEditing({
      ...editing,
      sources: editing.sources.map((source, sourceIndex) =>
        sourceIndex === index ? { ...source, ...patch } : source,
      ),
    });
  }

  function toggleCategory(category: AdminCategory) {
    if (!editing) return;
    const exists = editing.categories.some((item) => item.slug === category.slug);
    const next = exists
      ? editing.categories.filter((item) => item.slug !== category.slug)
      : [
          ...editing.categories,
          {
            id: category.id,
            slug: category.slug,
            name: category.name,
            is_primary: false,
            source: "admin",
          },
        ];
    if (next.length && !next.some((item) => item.is_primary)) {
      next[0] = { ...next[0], is_primary: true };
    }
    setEditing({ ...editing, categories: next });
  }

  function setPrimaryCategory(slug: string) {
    if (!editing) return;
    setEditing({
      ...editing,
      categories: editing.categories.map((item) => ({ ...item, is_primary: item.slug === slug })),
    });
  }

  function toggleDish(dish: DishOption) {
    if (!editing) return;
    const exists = editing.foods.some((food) => food.id === dish.id);
    setEditing({
      ...editing,
      foods: exists
        ? editing.foods.filter((food) => food.id !== dish.id)
        : [...editing.foods, { id: dish.id, slug: dish.slug, name: dish.local_name }],
    });
  }

  function toggleClaim(index: number, claim: MerchantClaim) {
    if (!editing) return;
    const source = editing.sources[index];
    updateSource(index, {
      claims: source.claims.includes(claim)
        ? source.claims.filter((item) => item !== claim)
        : [...source.claims, claim],
    });
  }

  return (
    <section className="mt-12 border-t border-[var(--line)] pt-8">
      <div className="flex flex-wrap items-end gap-3">
        <div className="mr-auto">
          <p className="text-sm font-semibold tracking-[.12em] text-[var(--teal)]">
            精準店家地點
          </p>
          <h2 className="mt-1 text-2xl font-bold">店家、地圖識別與永久座標</h2>
          <p className="mt-2 max-w-3xl text-sm text-[var(--muted)]">
            未驗證的啟動候選不會公開。Google Places
            座標僅用來比對，永久座標必須另附官方或人工查核來源。
          </p>
        </div>
        <input
          aria-label="店家搜尋"
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder="店名或 slug"
          className="h-11 rounded-xl border px-3"
        />
        <select
          aria-label={t("merchants.destination")}
          value={destination}
          onChange={(event) => {
            setDestination(event.target.value);
            setFilterArea("");
          }}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">{t("merchants.allDestinations")}</option>
          {cities.map((city) => (
            <option key={city.id} value={city.id}>
              {city.name}
            </option>
          ))}
        </select>
        <select
          aria-label={t("merchants.area")}
          value={filterArea}
          disabled={!destination}
          onChange={(event) => setFilterArea(event.target.value)}
          className="h-11 rounded-xl border px-3 disabled:opacity-50"
        >
          <option value="">{t("merchants.allAreas")}</option>
          {scopedFilterAreas.map((area) => (
            <option key={area.id} value={area.slug}>
              {area.name}
            </option>
          ))}
        </select>
        <select
          aria-label={t("merchants.category")}
          value={filterCategory}
          onChange={(event) => setFilterCategory(event.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">{t("merchants.allCategories")}</option>
          {categories.map((category) => (
            <option key={category.id} value={category.slug}>
              {category.name}
            </option>
          ))}
        </select>
        <select
          aria-label={t("merchants.taxonomyFilter")}
          value={taxonomy}
          onChange={(event) => setTaxonomy(event.target.value as MerchantTaxonomyFilter | "")}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">{t("merchants.allTaxonomy")}</option>
          <option value="missing_area">{t("merchants.missingArea")}</option>
          <option value="missing_category">{t("merchants.missingCategory")}</option>
        </select>
        <select
          aria-label="地圖比對狀態"
          value={mapStatus}
          onChange={(event) => setMapStatus(event.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">全部比對狀態</option>
          <option value="unverified">待驗證</option>
          <option value="verified">已驗證</option>
          <option value="ambiguous">模糊</option>
          <option value="disabled">已停用</option>
        </select>
        <select
          aria-label="官方資料狀態"
          value={officialData}
          onChange={(event) => setOfficialData(event.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">全部官方資料</option>
          <option value="filled">官方資料已填</option>
          <option value="missing">官方資料未填</option>
        </select>
        <button
          type="button"
          onClick={() => {
            setEditing(blankMerchant());
            setCandidate(null);
            setApplyNotice("");
          }}
          className="h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white"
        >
          {t("merchants.add")}
        </button>
      </div>
      {message && (
        <p
          role="status"
          className="mt-3 rounded-xl bg-[var(--paper)] px-4 py-3 text-sm text-[var(--muted)]"
        >
          {message}
        </p>
      )}
      <div className="mt-4 flex flex-wrap items-center gap-2 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-3">
        <button
          type="button"
          onClick={toggleAllVisible}
          disabled={!visibleIds.length}
          className="min-h-11 rounded-xl border bg-white px-4 font-semibold disabled:opacity-40"
        >
          {allVisibleSelected ? "取消全選" : "全選目前項目"}
        </button>
        <span className="text-sm text-[var(--muted)]">
          已選 {selected.size} 間
        </span>
        <button
          type="button"
          onClick={() => void searchBatchGoogleCandidates()}
          disabled={!selected.size || loading}
          className="min-h-11 rounded-xl border border-[var(--teal)] bg-white px-4 font-semibold text-[var(--teal)] disabled:opacity-40"
        >
          批次搜尋 Google 候選
        </button>
        <button
          type="button"
          onClick={() => void batchUpdate("verify_activate")}
          disabled={!selected.size || loading}
          className="min-h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-40"
        >
          批次設為已驗證並啟用
        </button>
        <button
          type="button"
          onClick={() => void batchUpdate("disable")}
          disabled={!selected.size || loading}
          className="min-h-11 rounded-xl border border-red-300 bg-white px-4 font-semibold text-red-700 disabled:opacity-40"
        >
          批次停用
        </button>
      </div>
      {batchCandidates.length > 0 && (
        <section className="mt-4 rounded-2xl border border-amber-300 bg-amber-50 p-4">
          <h3 className="font-bold">Google 候選人工比對</h3>
          <p className="mt-1 text-sm text-[var(--muted)]">
            候選座標只供比較，不會寫入永久座標。請確認店名與地址後逐筆套用 Place
            ID。
          </p>
          <div className="mt-3 grid gap-3">
            {batchCandidates.map(({ merchant, response, error }) => (
              <article
                key={merchant.id}
                className="rounded-xl border bg-white p-3"
              >
                <p className="font-semibold">
                  {merchant.name} · {merchant.destination_id}
                </p>
                {error && <p className="mt-1 text-sm text-red-700">{error}</p>}
                {!error && !response?.configured && (
                  <p className="mt-1 text-sm text-amber-800">
                    {response?.message ?? "Google Places 自動比對未設定。"}
                  </p>
                )}
                {response?.candidates.slice(0, 3).map((item) => (
                  <div
                    key={item.place_id}
                    className="mt-3 flex flex-wrap items-center gap-3 border-t pt-3"
                  >
                    <div className="min-w-0 flex-1">
                      <p className="font-semibold">{item.name}</p>
                      <p className="text-sm text-[var(--muted)]">
                        {item.address}
                      </p>
                    </div>
                    <button
                      type="button"
                      disabled={loading}
                      onClick={() =>
                        void applyBatchCandidate(merchant, item.place_id)
                      }
                      className="min-h-11 rounded-xl bg-amber-800 px-4 font-semibold text-white disabled:opacity-40"
                    >
                      套用 Place ID，保留人工審核
                    </button>
                  </div>
                ))}
                {response?.configured && response.candidates.length === 0 && (
                  <p className="mt-2 text-sm text-[var(--muted)]">沒有候選。</p>
                )}
              </article>
            ))}
          </div>
        </section>
      )}
      <div className="mt-4 overflow-x-auto rounded-2xl border bg-white">
        <table className="admin-responsive-table admin-merchants-table w-full min-w-[1120px] text-left text-sm">
          <thead className="bg-[var(--paper)]">
            <tr>
              <th className="p-3">選取</th>
              <th className="p-3">店家</th>
              <th className="p-3">目的地／料理</th>
              <th className="p-3">地圖識別</th>
              <th className="p-3">永久座標</th>
              <th className="p-3">官方資料</th>
              <th className="p-3">發布</th>
              <th className="p-3">操作</th>
            </tr>
          </thead>
          <tbody>
            {data?.items.map((merchant) => {
              const directSources = merchant.sources.filter(
                (source) => source.source_scope !== "destination_context",
              ).length;
              return (
                <tr key={merchant.id} className="border-t">
                  <td className="p-3">
                    <input
                      type="checkbox"
                      aria-label={`選取 ${merchant.name}`}
                      checked={selected.has(merchant.id)}
                      onChange={() => toggleSelection(merchant.id)}
                      className="h-5 w-5 accent-[var(--teal)]"
                    />
                  </td>
                  <td className="p-3 font-semibold">
                    {merchant.name}
                    <span className="block text-xs font-normal text-[var(--muted)]">
                      {merchant.local_name} · {merchant.slug}
                    </span>
                  </td>
                  <td className="p-3">
                    {merchant.destination_id}
                    {merchant.area ? ` · ${merchant.area.name}` : ""}
                    <span className="block text-xs text-[var(--muted)]">
                      {[
                        ...merchant.categories.map((category) => category.name),
                        ...merchant.foods.map((food) => food.name),
                      ].join("、")}
                    </span>
                  </td>
                  <td className="p-3">
                    {merchant.map_match_status}
                    <span className="block max-w-[260px] truncate text-xs text-[var(--muted)]">
                      {merchant.country_code === "KR"
                        ? merchant.naver_map_url
                        : merchant.google_place_id || "無精準識別"}
                    </span>
                  </td>
                  <td className="p-3">
                    {merchant.latitude ?? "—"}, {merchant.longitude ?? "—"}
                    <span className="block text-xs text-[var(--muted)]">
                      {merchant.coordinate_source_type || "座標來源待補"}
                    </span>
                  </td>
                  <td className="p-3">
                    {merchant.official_website_url ? "官網已填" : "官網待補"}
                    <span className="block text-xs text-[var(--muted)]">
                      直接佐證 {directSources} · 背景{" "}
                      {merchant.sources.length - directSources}
                    </span>
                  </td>
                  <td className="p-3">
                    {merchant.review_status}
                    <span className="block text-xs text-[var(--muted)]">
                      {merchant.is_active ? "啟用" : "停用"}
                    </span>
                  </td>
                  <td className="p-3">
                    <button
                      type="button"
                      onClick={() => {
                        setEditing({
                          ...merchant,
                          sources: merchant.sources.map((source) => ({
                            ...source,
                            claims: [...source.claims],
                          })),
                        });
                        setCandidate(null);
                        setApplyNotice("");
                      }}
                      className="min-h-11 rounded-xl border border-[var(--teal)] px-3 font-semibold text-[var(--teal)]"
                    >
                      編輯地點與來源
                    </button>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>

      {editing && (
        <div className="fixed inset-0 z-[90] overflow-y-auto bg-slate-950/50 p-4 md:p-8">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="merchant-map-title"
            className="mx-auto max-w-4xl rounded-3xl bg-white p-6 shadow-2xl"
          >
            <div className="flex items-start justify-between gap-4">
              <div>
                <h3 id="merchant-map-title" className="text-2xl font-bold">
                  {editing.id ? editing.name : t("merchants.createTitle")}
                </h3>
                <p className="text-sm text-[var(--muted)]">
                  {editing.destination_id} · {editing.country_code}
                </p>
              </div>
              <button
                type="button"
                onClick={() => setEditing(null)}
                className="min-h-11 rounded-xl border px-4"
              >
                關閉
              </button>
            </div>
            <div className="mt-5 grid gap-4 md:grid-cols-2">
              <label className="text-sm font-semibold">
                店名
                <input
                  value={editing.name}
                  onChange={(event) =>
                    setEditing({ ...editing, name: event.target.value })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="text-sm font-semibold">
                當地店名
                <input
                  value={editing.local_name}
                  onChange={(event) =>
                    setEditing({ ...editing, local_name: event.target.value })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              {!editing.id && (
                <label className="text-sm font-semibold">
                  {t("merchants.slug")}
                  <input
                    aria-label={t("merchants.slug")}
                    value={editing.slug}
                    onChange={(event) => setEditing({ ...editing, slug: event.target.value })}
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
              )}
              <label className="text-sm font-semibold">
                {t("merchants.destination")}
                <select
                  aria-label={t("merchants.destination")}
                  value={editing.destination_id}
                  onChange={(event) => {
                    const city = cities.find((item) => item.id === event.target.value);
                    const countryChanged = Boolean(city) && city?.country_code !== editing.country_code;
                    setEditing({
                      ...editing,
                      destination_id: event.target.value,
                      country_code: city?.country_code ?? editing.country_code,
                      area: null,
                      foods: countryChanged ? [] : editing.foods,
                    });
                  }}
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                >
                  <option value="">—</option>
                  {cities.map((city) => (
                    <option key={city.id} value={city.id}>
                      {city.name}
                    </option>
                  ))}
                </select>
              </label>
              <label className="text-sm font-semibold">
                {t("merchants.area")}
                <select
                  aria-label={t("merchants.area")}
                  value={editing.area?.slug ?? ""}
                  onChange={(event) => {
                    const area = scopedEditorAreas.find(
                      (item) => item.slug === event.target.value,
                    );
                    setEditing({
                      ...editing,
                      area: area
                        ? {
                            id: area.id,
                            slug: area.slug,
                            name: area.name,
                            destination_id: area.destination_id,
                          }
                        : null,
                    });
                  }}
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                >
                  <option value="">{t("merchants.noArea")}</option>
                  {scopedEditorAreas.map((area) => (
                    <option key={area.id} value={area.slug}>
                      {area.name}
                    </option>
                  ))}
                </select>
                <span className="mt-1 block text-xs font-normal text-[var(--muted)]">
                  {t("merchants.areaHelp")}
                </span>
              </label>
              <label className="text-sm font-semibold">
                {t("merchants.displayOrder")}
                <input
                  type="number"
                  aria-label={t("merchants.displayOrder")}
                  value={editing.display_order}
                  onChange={(event) =>
                    setEditing({ ...editing, display_order: Number(event.target.value) })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="text-sm font-semibold">
                緯度
                <input
                  type="number"
                  step="any"
                  value={editing.latitude ?? ""}
                  onChange={(event) =>
                    setEditing({
                      ...editing,
                      latitude: nullableNumber(event.target.value),
                    })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="text-sm font-semibold">
                經度
                <input
                  type="number"
                  step="any"
                  value={editing.longitude ?? ""}
                  onChange={(event) =>
                    setEditing({
                      ...editing,
                      longitude: nullableNumber(event.target.value),
                    })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="text-sm font-semibold">
                座標來源類型
                <select
                  value={editing.coordinate_source_type ?? ""}
                  onChange={(event) =>
                    setEditing({
                      ...editing,
                      coordinate_source_type: event.target.value || null,
                    })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                >
                  <option value="">待補</option>
                  <option value="official_tourism">官方觀光</option>
                  <option value="merchant_official">店家官方</option>
                  <option value="wikidata">Wikidata</option>
                  <option value="admin_verified">人工查核</option>
                </select>
              </label>
              <label className="text-sm font-semibold">
                座標來源網址
                <input
                  value={editing.coordinate_source_url ?? ""}
                  onChange={(event) =>
                    setEditing({
                      ...editing,
                      coordinate_source_url: event.target.value || null,
                    })
                  }
                  placeholder="https://"
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              {editing.country_code === "KR" ? (
                <label className="text-sm font-semibold md:col-span-2">
                  Naver 精準地點頁
                  <input
                    value={editing.naver_map_url ?? ""}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        naver_map_url: event.target.value || null,
                      })
                    }
                    placeholder="https://map.naver.com/p/entry/place/..."
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
              ) : (
                <label className="text-sm font-semibold md:col-span-2">
                  Google Place ID
                  <input
                    value={editing.google_place_id ?? ""}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        google_place_id: event.target.value || null,
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
              )}
            </div>
            <div className="mt-4 flex flex-wrap gap-2">
              <button
                type="button"
                disabled={loading || editing.country_code === "KR"}
                onClick={() => void searchGoogleCandidate()}
                className="min-h-11 rounded-xl border border-[var(--teal)] px-4 font-semibold text-[var(--teal)] disabled:opacity-40"
              >
                搜尋 Google 候選
              </button>
            </div>
            {candidate?.candidates[0] && (
              <div className="mt-4 rounded-2xl border border-amber-300 bg-amber-50 p-4">
                <p className="font-semibold">{candidate.candidates[0].name}</p>
                <p className="text-sm text-[var(--muted)]">
                  {candidate.candidates[0].address}
                </p>
                <p className="mt-2 text-xs">
                  暫存比對座標（不得作為永久來源）：
                  {candidate.candidates[0].temporary_match_coordinates.latitude}
                  ,{" "}
                  {
                    candidate.candidates[0].temporary_match_coordinates
                      .longitude
                  }
                </p>
                <button
                  type="button"
                  onClick={() =>
                    applyCandidateToEditor(candidate.candidates[0].place_id)
                  }
                  className="mt-3 min-h-11 rounded-xl bg-amber-800 px-4 font-semibold text-white"
                >
                  套用 Place ID，保留人工審核
                </button>
                {applyNotice && (
                  <p role="status" className="mt-3 text-sm font-semibold text-amber-900">
                    {applyNotice}
                  </p>
                )}
              </div>
            )}
            <fieldset className="mt-5 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
              <legend className="px-1 font-bold">{t("merchants.category")}</legend>
              <p className="text-xs text-[var(--muted)]">{t("merchants.categoriesHelp")}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {categories
                  .filter((category) => category.is_active)
                  .map((category) => {
                    const link = editing.categories.find((item) => item.slug === category.slug);
                    return (
                      <span
                        key={category.id}
                        className="inline-flex min-h-10 items-center gap-2 rounded-lg border bg-white px-3 text-xs"
                      >
                        <label className="inline-flex items-center gap-1">
                          <input
                            type="checkbox"
                            aria-label={category.name}
                            checked={Boolean(link)}
                            onChange={() => toggleCategory(category)}
                          />
                          {category.name}
                        </label>
                        {link && (
                          <label className="inline-flex items-center gap-1 text-[var(--muted)]">
                            <input
                              type="radio"
                              name="primary-category"
                              aria-label={`${t("merchants.primary")} ${category.name}`}
                              checked={link.is_primary}
                              onChange={() => setPrimaryCategory(category.slug)}
                            />
                            {t("merchants.primary")}
                          </label>
                        )}
                      </span>
                    );
                  })}
              </div>
            </fieldset>
            <fieldset className="mt-5 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
              <legend className="px-1 font-bold">{t("merchants.dishes")}</legend>
              <p className="text-xs text-[var(--muted)]">{t("merchants.dishesHelp")}</p>
              <div className="mt-3 flex flex-wrap gap-2">
                {scopedDishOptions.map((dish) => (
                  <label
                    key={dish.id}
                    className="inline-flex min-h-10 items-center gap-2 rounded-lg border bg-white px-3 text-xs"
                  >
                    <input
                      type="checkbox"
                      aria-label={dish.local_name}
                      checked={editing.foods.some((food) => food.id === dish.id)}
                      onChange={() => toggleDish(dish)}
                    />
                    {dish.local_name}
                  </label>
                ))}
              </div>
            </fieldset>
            <section className="mt-5 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
              <div className="flex flex-wrap items-start justify-between gap-3">
                <div>
                  <h4 className="font-bold">店家官網與官方佐證</h4>
                  <p className="mt-1 text-xs leading-5 text-[var(--muted)]">
                    區域政府觀光頁只屬於目的地背景；只有直接列出店家或店家自己的官網，才能佐證店名、地址、官網與叫車座標。
                  </p>
                </div>
                <button
                  type="button"
                  onClick={() =>
                    setEditing({
                      ...editing,
                      sources: [...editing.sources, emptyDirectSource()],
                    })
                  }
                  className="min-h-10 rounded-xl border bg-white px-3 text-sm font-semibold"
                >
                  新增直接來源
                </button>
              </div>
              <label className="mt-4 block text-sm font-semibold">
                店家官方網站
                <input
                  value={editing.official_website_url ?? ""}
                  onChange={(event) =>
                    setEditing({
                      ...editing,
                      official_website_url: event.target.value || null,
                    })
                  }
                  placeholder="https://"
                  className="mt-1 h-11 w-full rounded-xl border bg-white px-3"
                />
              </label>
              <div className="mt-4 grid gap-3">
                {editing.sources.map((source, index) => (
                  <fieldset
                    key={source.id ?? index}
                    className="rounded-2xl border bg-white p-4"
                  >
                    <div className="flex items-center justify-between gap-3">
                      <legend className="font-semibold">
                        來源 {index + 1}
                      </legend>
                      {editing.sources.length > 1 && (
                        <button
                          type="button"
                          onClick={() =>
                            setEditing({
                              ...editing,
                              sources: editing.sources.filter(
                                (_, sourceIndex) => sourceIndex !== index,
                              ),
                            })
                          }
                          className="min-h-9 rounded-lg border px-3 text-xs"
                        >
                          移除
                        </button>
                      )}
                    </div>
                    <div className="mt-3 grid gap-3 md:grid-cols-2">
                      <label className="text-xs font-semibold">
                        來源類型
                        <select
                          value={source.source_type}
                          onChange={(event) =>
                            updateSource(index, {
                              source_type: event.target
                                .value as MerchantSource["source_type"],
                            })
                          }
                          className="mt-1 h-11 w-full rounded-xl border px-3"
                        >
                          <option value="merchant_official">店家官方</option>
                          <option value="official_tourism">
                            政府／官方觀光
                          </option>
                          {source.source_type === "michelin_licensed" && (
                            <option value="michelin_licensed">
                              授權米其林
                            </option>
                          )}
                        </select>
                      </label>
                      <label className="text-xs font-semibold">
                        佐證範圍
                        <select
                          value={source.source_scope}
                          onChange={(event) => {
                            const scope = event.target
                              .value as MerchantSource["source_scope"];
                            updateSource(index, {
                              source_scope: scope,
                              claims:
                                scope === "destination_context"
                                  ? []
                                  : source.claims,
                            });
                          }}
                          className="mt-1 h-11 w-full rounded-xl border px-3"
                        >
                          <option value="destination_context">
                            目的地背景（不佐證店家）
                          </option>
                          <option value="merchant_listing">官方店家名錄</option>
                          <option value="merchant_website">店家官網</option>
                          <option value="coordinates">永久座標來源</option>
                        </select>
                      </label>
                      <label className="text-xs font-semibold">
                        來源標題
                        <input
                          value={source.source_title}
                          onChange={(event) =>
                            updateSource(index, {
                              source_title: event.target.value,
                            })
                          }
                          className="mt-1 h-11 w-full rounded-xl border px-3"
                        />
                      </label>
                      <label className="text-xs font-semibold">
                        HTTPS 來源網址
                        <input
                          value={source.source_url}
                          onChange={(event) =>
                            updateSource(index, {
                              source_url: event.target.value,
                            })
                          }
                          placeholder="https://"
                          className="mt-1 h-11 w-full rounded-xl border px-3"
                        />
                      </label>
                    </div>
                    <div className="mt-3 flex flex-wrap gap-2">
                      {(
                        [
                          "display_name",
                          "address",
                          "official_website",
                          "coordinates",
                        ] as MerchantClaim[]
                      ).map((claim) => (
                        <label
                          key={claim}
                          className={`inline-flex min-h-10 items-center gap-2 rounded-lg border px-3 text-xs ${source.source_scope === "destination_context" ? "opacity-50" : ""}`}
                        >
                          <input
                            type="checkbox"
                            disabled={
                              source.source_scope === "destination_context"
                            }
                            checked={source.claims.includes(claim)}
                            onChange={() => toggleClaim(index, claim)}
                          />
                          {
                            {
                              display_name: "店名",
                              address: "地址",
                              official_website: "官網",
                              coordinates: "座標",
                            }[claim]
                          }
                        </label>
                      ))}
                    </div>
                  </fieldset>
                ))}
              </div>
            </section>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <select
                aria-label={t("merchants.mapMatchStatus")}
                value={editing.map_match_status}
                onChange={(event) =>
                  setEditing({
                    ...editing,
                    map_match_status: event.target
                      .value as Merchant["map_match_status"],
                  })
                }
                className="h-11 rounded-xl border px-3"
              >
                <option value="unverified">待驗證</option>
                <option value="verified">已驗證</option>
                <option value="ambiguous">模糊</option>
                <option value="disabled">地圖停用</option>
              </select>
              <select
                aria-label={t("merchants.reviewStatus")}
                value={editing.review_status}
                onChange={(event) =>
                  setEditing({
                    ...editing,
                    review_status: event.target
                      .value as Merchant["review_status"],
                  })
                }
                className="h-11 rounded-xl border px-3"
              >
                <option value="pending">待審</option>
                <option value="approved">核准</option>
                <option value="rejected">拒絕</option>
                <option value="disabled">停用</option>
              </select>
              <label className="flex items-center gap-2">
                <input
                  type="checkbox"
                  checked={editing.is_active}
                  onChange={(event) =>
                    setEditing({ ...editing, is_active: event.target.checked })
                  }
                />
                啟用
              </label>
              <button
                type="button"
                disabled={loading}
                onClick={() => void save()}
                className="ml-auto min-h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white disabled:opacity-40"
              >
                儲存店家地點
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
