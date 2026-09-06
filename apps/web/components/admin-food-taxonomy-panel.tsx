"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";

export const nameLocales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
export type NameLocale = (typeof nameLocales)[number];
export type LocalizedNames = Record<NameLocale, string>;

export type FoodCity = {
  id: string;
  name: string;
  country_code: string;
  merchant_count: number;
  area_count: number;
};
type CitiesResponse = { countries: { code: string; name: string; cities: FoodCity[] }[] };

export type AdminArea = {
  id: string;
  slug: string;
  destination_id: string;
  destination_name: string;
  country_code: string;
  name: string;
  names: LocalizedNames;
  match_terms: string[];
  latitude: number | null;
  longitude: number | null;
  is_active: boolean;
  display_order: number;
  source: string;
  merchant_count: number;
};

export type AdminCategory = {
  id: string;
  slug: string;
  name: string;
  names: LocalizedNames;
  is_active: boolean;
  display_order: number;
  source: string;
  merchant_count: number;
};

type ListResponse<T> = { items: T[]; total: number; page: number; pages: number };

export function blankNames(): LocalizedNames {
  return { "zh-TW": "", "zh-CN": "", en: "", ja: "", ko: "" };
}

export function completeNames(names: Partial<LocalizedNames> | undefined): LocalizedNames {
  return { ...blankNames(), ...(names ?? {}) };
}

export async function loadCities(): Promise<FoodCity[]> {
  const response = await api<CitiesResponse>("/foods/cities");
  return (response.countries ?? []).flatMap((country) => country.cities ?? []);
}

function csv(value: string): string[] {
  return value
    .split(",")
    .map((item) => item.trim())
    .filter(Boolean);
}

function nullableNumber(value: string): number | null {
  return value.trim() ? Number(value) : null;
}

export function LocalizedNameFields({
  names,
  onChange,
  label,
  placeholders,
}: {
  names: LocalizedNames;
  onChange: (next: LocalizedNames) => void;
  label: (locale: string) => string;
  /** What each locale falls back to when its input is left empty. */
  placeholders?: Partial<LocalizedNames>;
}) {
  return (
    <div className="grid gap-3 md:grid-cols-2">
      {nameLocales.map((locale) => (
        <label key={locale} className="text-sm font-semibold">
          {label(locale)}
          <input
            value={names[locale]}
            placeholder={placeholders?.[locale]}
            onChange={(event) => onChange({ ...names, [locale]: event.target.value })}
            className="mt-1 h-11 w-full rounded-xl border px-3"
          />
        </label>
      ))}
    </div>
  );
}

function blankArea(destinationId = ""): AdminArea {
  return {
    id: "",
    slug: "",
    destination_id: destinationId,
    destination_name: "",
    country_code: "",
    name: "",
    names: blankNames(),
    match_terms: [],
    latitude: null,
    longitude: null,
    is_active: true,
    display_order: 100,
    source: "admin",
    merchant_count: 0,
  };
}

export function AdminFoodAreasPanel() {
  const t = useTranslations("foodAdmin");
  const [cities, setCities] = useState<FoodCity[]>([]);
  const [data, setData] = useState<ListResponse<AdminArea> | null>(null);
  const [destination, setDestination] = useState("");
  const [status, setStatus] = useState("");
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [editing, setEditing] = useState<AdminArea | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const listUrl = useMemo(() => {
    const params = new URLSearchParams({ limit: "200" });
    if (destination) params.set("destination_id", destination);
    if (status) params.set("status", status);
    if (query.trim()) params.set("q", query.trim());
    return `/admin/foods/areas?${params}`;
  }, [destination, query, status]);

  const load = useCallback(async () => {
    try {
      setData(await api<ListResponse<AdminArea>>(listUrl));
      setSelected(new Set());
    } catch (reason) {
      setMessage((reason as Error).message);
    }
  }, [listUrl]);

  useEffect(() => {
    api<ListResponse<AdminArea>>(listUrl)
      .then((response) => {
        setData(response);
        setSelected(new Set());
      })
      .catch((reason: Error) => setMessage(reason.message));
  }, [listUrl]);

  useEffect(() => {
    loadCities()
      .then(setCities)
      .catch((reason: Error) => setMessage(reason.message));
  }, []);

  async function batch(action: "activate" | "deactivate") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/foods/areas/batch", {
        method: "POST",
        body: JSON.stringify({ ids: [...selected], action }),
      });
      setMessage(t("areas.batchUpdated", { count: selected.size }));
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function save() {
    if (!editing) return;
    setLoading(true);
    const payload = {
      ...(editing.id ? {} : { slug: editing.slug }),
      destination_id: editing.destination_id,
      names: editing.names,
      match_terms: editing.match_terms,
      latitude: editing.latitude,
      longitude: editing.longitude,
      display_order: editing.display_order,
      is_active: editing.is_active,
    };
    try {
      await api(editing.id ? `/admin/foods/areas/${editing.id}` : "/admin/foods/areas", {
        method: editing.id ? "PATCH" : "POST",
        body: JSON.stringify(payload),
      });
      setMessage(editing.id ? t("areas.updated") : t("areas.created"));
      setEditing(null);
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mt-8" aria-labelledby="food-areas-title">
      <div className="flex flex-wrap items-end gap-3">
        <div className="mr-auto">
          <h2 id="food-areas-title" className="text-2xl font-bold">
            {t("areas.title")}
          </h2>
          <p className="mt-2 max-w-3xl text-sm text-[var(--muted)]">{t("areas.description")}</p>
        </div>
        <input
          aria-label={t("areas.search")}
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          placeholder={t("areas.searchPlaceholder")}
          className="h-11 rounded-xl border px-3"
        />
        <select
          aria-label={t("areas.destination")}
          value={destination}
          onChange={(event) => setDestination(event.target.value)}
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
          aria-label={t("areas.status")}
          value={status}
          onChange={(event) => setStatus(event.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">{t("areas.allStatuses")}</option>
          <option value="active">{t("active")}</option>
          <option value="disabled">{t("inactive")}</option>
        </select>
        <button
          type="button"
          onClick={() => setEditing(blankArea(destination))}
          className="h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white"
        >
          {t("areas.add")}
        </button>
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <span className="mr-auto text-sm text-[var(--muted)]">
          {t("selectionCount", { total: data?.total ?? 0, selected: selected.size })}
        </span>
        <button
          type="button"
          disabled={!selected.size || loading}
          onClick={() => void batch("activate")}
          className="rounded-xl border border-[var(--teal)] px-4 py-2 text-sm font-semibold text-[var(--teal)] disabled:opacity-40"
        >
          {t("areas.activate")}
        </button>
        <button
          type="button"
          disabled={!selected.size || loading}
          onClick={() => void batch("deactivate")}
          className="rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-40"
        >
          {t("areas.deactivate")}
        </button>
      </div>
      {message && (
        <p role="status" className="mt-3 text-sm text-[var(--muted)]">
          {message}
        </p>
      )}
      <div className="mt-4 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white">
        <table className="admin-responsive-table w-full min-w-[820px] text-left text-sm">
          <thead className="bg-[var(--paper)]">
            <tr>
              <th className="p-3">{t("areas.table.select")}</th>
              <th className="p-3">{t("areas.table.name")}</th>
              <th className="p-3">{t("areas.table.destination")}</th>
              <th className="p-3">{t("areas.table.order")}</th>
              <th className="p-3">{t("areas.table.merchants")}</th>
              <th className="p-3">{t("areas.table.status")}</th>
              <th className="p-3">{t("areas.table.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {data?.items?.map((area) => (
              <tr key={area.id} className="border-t">
                <td className="p-3">
                  <input
                    type="checkbox"
                    aria-label={t("areas.select", { name: area.name })}
                    checked={selected.has(area.id)}
                    onChange={() =>
                      setSelected((current) => {
                        const next = new Set(current);
                        if (next.has(area.id)) next.delete(area.id);
                        else next.add(area.id);
                        return next;
                      })
                    }
                    className="h-5 w-5 accent-[var(--teal)]"
                  />
                </td>
                <td className="p-3 font-semibold">
                  {area.name}
                  <span className="block text-xs font-normal text-[var(--muted)]">
                    {area.names.en} · {area.slug}
                  </span>
                </td>
                <td className="p-3">{area.destination_name}</td>
                <td className="p-3">{area.display_order}</td>
                <td className="p-3">{t("areas.merchantCount", { count: area.merchant_count })}</td>
                <td className="p-3">{area.is_active ? t("active") : t("inactive")}</td>
                <td className="p-3">
                  <button
                    type="button"
                    onClick={() => setEditing({ ...area, names: completeNames(area.names) })}
                    className="min-h-11 rounded-xl border border-[var(--teal)] px-3 font-semibold text-[var(--teal)]"
                  >
                    {t("edit")}
                  </button>
                </td>
              </tr>
            ))}
            {data && data.items?.length === 0 && (
              <tr>
                <td colSpan={7} className="p-6 text-center text-[var(--muted)]">
                  {t("areas.empty")}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {editing && (
        <div className="fixed inset-0 z-[90] overflow-y-auto bg-slate-950/50 p-4 md:p-8">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="food-area-editor-title"
            className="mx-auto max-w-3xl rounded-3xl bg-white p-6 shadow-2xl"
          >
            <div className="flex items-start justify-between gap-4">
              <h3 id="food-area-editor-title" className="text-2xl font-bold">
                {editing.id ? t("areas.editTitle", { name: editing.name }) : t("areas.createTitle")}
              </h3>
              <button
                type="button"
                onClick={() => setEditing(null)}
                className="min-h-11 rounded-xl border px-4"
              >
                {t("cancel")}
              </button>
            </div>
            <div className="mt-5 grid gap-4 md:grid-cols-2">
              <label className="text-sm font-semibold">
                {t("areas.slug")}
                <input
                  value={editing.slug}
                  disabled={Boolean(editing.id)}
                  onChange={(event) => setEditing({ ...editing, slug: event.target.value })}
                  className="mt-1 h-11 w-full rounded-xl border px-3 disabled:bg-[var(--paper)]"
                />
              </label>
              <label className="text-sm font-semibold">
                {t("areas.destination")}
                <select
                  value={editing.destination_id}
                  onChange={(event) =>
                    setEditing({ ...editing, destination_id: event.target.value })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                >
                  <option value="">{t("merchants.allDestinations")}</option>
                  {cities.map((city) => (
                    <option key={city.id} value={city.id}>
                      {city.name}
                    </option>
                  ))}
                </select>
              </label>
              <label className="text-sm font-semibold">
                {t("areas.latitude")}
                <input
                  type="number"
                  step="any"
                  value={editing.latitude ?? ""}
                  onChange={(event) =>
                    setEditing({ ...editing, latitude: nullableNumber(event.target.value) })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="text-sm font-semibold">
                {t("areas.longitude")}
                <input
                  type="number"
                  step="any"
                  value={editing.longitude ?? ""}
                  onChange={(event) =>
                    setEditing({ ...editing, longitude: nullableNumber(event.target.value) })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="text-sm font-semibold">
                {t("areas.matchTerms")}
                <input
                  value={editing.match_terms.join(", ")}
                  onChange={(event) =>
                    setEditing({ ...editing, match_terms: csv(event.target.value) })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
              <label className="text-sm font-semibold">
                {t("areas.displayOrder")}
                <input
                  type="number"
                  value={editing.display_order}
                  onChange={(event) =>
                    setEditing({ ...editing, display_order: Number(event.target.value) })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
            </div>
            <div className="mt-5">
              <LocalizedNameFields
                names={editing.names}
                onChange={(names) => setEditing({ ...editing, names })}
                label={(locale) => t("localizedName", { locale })}
              />
            </div>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <label className="flex items-center gap-2 text-sm font-semibold">
                <input
                  type="checkbox"
                  checked={editing.is_active}
                  onChange={(event) => setEditing({ ...editing, is_active: event.target.checked })}
                />
                {t("active")}
              </label>
              <button
                type="button"
                disabled={loading}
                onClick={() => void save()}
                className="ml-auto min-h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white disabled:opacity-40"
              >
                {t("areas.save")}
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

function blankCategory(): AdminCategory {
  return {
    id: "",
    slug: "",
    name: "",
    names: blankNames(),
    is_active: true,
    display_order: 100,
    source: "admin",
    merchant_count: 0,
  };
}

export function AdminFoodCategoriesPanel() {
  const t = useTranslations("foodAdmin");
  const [data, setData] = useState<ListResponse<AdminCategory> | null>(null);
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [editing, setEditing] = useState<AdminCategory | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(false);

  const load = useCallback(async () => {
    try {
      setData(await api<ListResponse<AdminCategory>>("/admin/foods/categories"));
      setSelected(new Set());
    } catch (reason) {
      setMessage((reason as Error).message);
    }
  }, []);

  useEffect(() => {
    api<ListResponse<AdminCategory>>("/admin/foods/categories")
      .then((response) => {
        setData(response);
        setSelected(new Set());
      })
      .catch((reason: Error) => setMessage(reason.message));
  }, []);

  async function batch(action: "activate" | "deactivate") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/foods/categories/batch", {
        method: "POST",
        body: JSON.stringify({ ids: [...selected], action }),
      });
      setMessage(t("categories.batchUpdated", { count: selected.size }));
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  async function save() {
    if (!editing) return;
    setLoading(true);
    const payload = {
      ...(editing.id ? {} : { slug: editing.slug }),
      names: editing.names,
      display_order: editing.display_order,
      is_active: editing.is_active,
    };
    try {
      await api(
        editing.id ? `/admin/foods/categories/${editing.id}` : "/admin/foods/categories",
        { method: editing.id ? "PATCH" : "POST", body: JSON.stringify(payload) },
      );
      setMessage(editing.id ? t("categories.updated") : t("categories.created"));
      setEditing(null);
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="mt-12 border-t border-[var(--line)] pt-8" aria-labelledby="food-categories-title">
      <div className="flex flex-wrap items-end gap-3">
        <div className="mr-auto">
          <h2 id="food-categories-title" className="text-2xl font-bold">
            {t("categories.title")}
          </h2>
          <p className="mt-2 max-w-3xl text-sm text-[var(--muted)]">
            {t("categories.description")}
          </p>
        </div>
        <button
          type="button"
          onClick={() => setEditing(blankCategory())}
          className="h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white"
        >
          {t("categories.add")}
        </button>
      </div>
      <div className="mt-4 flex flex-wrap items-center gap-2">
        <span className="mr-auto text-sm text-[var(--muted)]">
          {t("selectionCount", { total: data?.total ?? 0, selected: selected.size })}
        </span>
        <button
          type="button"
          disabled={!selected.size || loading}
          onClick={() => void batch("activate")}
          className="rounded-xl border border-[var(--teal)] px-4 py-2 text-sm font-semibold text-[var(--teal)] disabled:opacity-40"
        >
          {t("categories.activate")}
        </button>
        <button
          type="button"
          disabled={!selected.size || loading}
          onClick={() => void batch("deactivate")}
          className="rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-40"
        >
          {t("categories.deactivate")}
        </button>
      </div>
      {message && (
        <p role="status" className="mt-3 text-sm text-[var(--muted)]">
          {message}
        </p>
      )}
      <div className="mt-4 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white">
        <table className="admin-responsive-table w-full min-w-[720px] text-left text-sm">
          <thead className="bg-[var(--paper)]">
            <tr>
              <th className="p-3">{t("categories.table.select")}</th>
              <th className="p-3">{t("categories.table.name")}</th>
              <th className="p-3">{t("categories.table.order")}</th>
              <th className="p-3">{t("categories.table.merchants")}</th>
              <th className="p-3">{t("categories.table.status")}</th>
              <th className="p-3">{t("categories.table.actions")}</th>
            </tr>
          </thead>
          <tbody>
            {data?.items?.map((category) => (
              <tr key={category.id} className="border-t">
                <td className="p-3">
                  <input
                    type="checkbox"
                    aria-label={t("categories.select", { name: category.name })}
                    checked={selected.has(category.id)}
                    onChange={() =>
                      setSelected((current) => {
                        const next = new Set(current);
                        if (next.has(category.id)) next.delete(category.id);
                        else next.add(category.id);
                        return next;
                      })
                    }
                    className="h-5 w-5 accent-[var(--teal)]"
                  />
                </td>
                <td className="p-3 font-semibold">
                  {category.name}
                  <span className="block text-xs font-normal text-[var(--muted)]">
                    {category.names.en} · {category.slug}
                  </span>
                </td>
                <td className="p-3">{category.display_order}</td>
                <td className="p-3">
                  {t("categories.merchantCount", { count: category.merchant_count })}
                </td>
                <td className="p-3">{category.is_active ? t("active") : t("inactive")}</td>
                <td className="p-3">
                  <button
                    type="button"
                    onClick={() =>
                      setEditing({ ...category, names: completeNames(category.names) })
                    }
                    className="min-h-11 rounded-xl border border-[var(--teal)] px-3 font-semibold text-[var(--teal)]"
                  >
                    {t("edit")}
                  </button>
                </td>
              </tr>
            ))}
            {data && data.items?.length === 0 && (
              <tr>
                <td colSpan={6} className="p-6 text-center text-[var(--muted)]">
                  {t("categories.empty")}
                </td>
              </tr>
            )}
          </tbody>
        </table>
      </div>
      {editing && (
        <div className="fixed inset-0 z-[90] overflow-y-auto bg-slate-950/50 p-4 md:p-8">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="food-category-editor-title"
            className="mx-auto max-w-3xl rounded-3xl bg-white p-6 shadow-2xl"
          >
            <div className="flex items-start justify-between gap-4">
              <h3 id="food-category-editor-title" className="text-2xl font-bold">
                {editing.id
                  ? t("categories.editTitle", { name: editing.name })
                  : t("categories.createTitle")}
              </h3>
              <button
                type="button"
                onClick={() => setEditing(null)}
                className="min-h-11 rounded-xl border px-4"
              >
                {t("cancel")}
              </button>
            </div>
            <div className="mt-5 grid gap-4 md:grid-cols-2">
              <label className="text-sm font-semibold">
                {t("categories.slug")}
                <input
                  value={editing.slug}
                  disabled={Boolean(editing.id)}
                  onChange={(event) => setEditing({ ...editing, slug: event.target.value })}
                  className="mt-1 h-11 w-full rounded-xl border px-3 disabled:bg-[var(--paper)]"
                />
              </label>
              <label className="text-sm font-semibold">
                {t("categories.displayOrder")}
                <input
                  type="number"
                  value={editing.display_order}
                  onChange={(event) =>
                    setEditing({ ...editing, display_order: Number(event.target.value) })
                  }
                  className="mt-1 h-11 w-full rounded-xl border px-3"
                />
              </label>
            </div>
            <div className="mt-5">
              <LocalizedNameFields
                names={editing.names}
                onChange={(names) => setEditing({ ...editing, names })}
                label={(locale) => t("localizedName", { locale })}
              />
            </div>
            <div className="mt-5 flex flex-wrap items-center gap-3">
              <label className="flex items-center gap-2 text-sm font-semibold">
                <input
                  type="checkbox"
                  checked={editing.is_active}
                  onChange={(event) => setEditing({ ...editing, is_active: event.target.checked })}
                />
                {t("active")}
              </label>
              <button
                type="button"
                disabled={loading}
                onClick={() => void save()}
                className="ml-auto min-h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white disabled:opacity-40"
              >
                {t("categories.save")}
              </button>
            </div>
          </div>
        </div>
      )}
    </section>
  );
}
