"use client";

import { useCallback, useEffect, useState } from "react";
import { useTranslations } from "next-intl";
import { api } from "@/lib/api";
import { AdminFoodMerchantsPanel } from "./admin-food-merchants-panel";

const locales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
type Locale = (typeof locales)[number];
type Localization = { locale: Locale; name: string; summary: string };
type AdminFood = {
  id: string;
  slug: string;
  country_code: string;
  local_name: string;
  romanized_name: string;
  food_kind: "main" | "noodle_soup" | "street_food" | "dessert" | "drink";
  meal_types: string[];
  ingredient_tags: string[];
  dietary_notes: string[];
  source_urls: string[];
  review_status: "pending" | "approved" | "rejected" | "disabled";
  is_active: boolean;
  display_order: number;
  localizations: Localization[];
  destination_ids: string[];
  hotspots: { id: string; name: string }[];
};
type Response = {
  items: AdminFood[];
  total: number;
  page: number;
  pages: number;
};

function blankFood(): AdminFood {
  return {
    id: "",
    slug: "",
    country_code: "JP",
    local_name: "",
    romanized_name: "",
    food_kind: "main",
    meal_types: ["lunch", "dinner"],
    ingredient_tags: [],
    dietary_notes: [],
    source_urls: [],
    review_status: "pending",
    is_active: true,
    display_order: 100,
    localizations: locales.map((locale) => ({ locale, name: "", summary: "" })),
    destination_ids: [],
    hotspots: [],
  };
}

function completeLocalizations(food: AdminFood): AdminFood {
  return {
    ...food,
    localizations: locales.map(
      (locale) =>
        food.localizations.find((item) => item.locale === locale) ?? {
          locale,
          name: "",
          summary: "",
        },
    ),
  };
}

export function AdminFoodsPanel() {
  const t = useTranslations("foodAdmin");
  const [data, setData] = useState<Response | null>(null);
  const [country, setCountry] = useState("");
  const [destination, setDestination] = useState("");
  const [status, setStatus] = useState("");
  const [query, setQuery] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [editing, setEditing] = useState<AdminFood | null>(null);
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams({ limit: "100" });
    if (country) params.set("country_code", country);
    if (destination) params.set("destination_id", destination);
    if (status) params.set("status", status);
    if (query.trim()) params.set("q", query.trim());
    try {
      setData(await api<Response>(`/admin/foods?${params}`));
    } catch (reason) {
      setMessage((reason as Error).message);
    } finally {
      setLoading(false);
    }
  }, [country, destination, query, status]);

  useEffect(() => {
    const params = new URLSearchParams({ limit: "100" });
    if (country) params.set("country_code", country);
    if (destination) params.set("destination_id", destination);
    if (status) params.set("status", status);
    if (query.trim()) params.set("q", query.trim());
    void api<Response>(`/admin/foods?${params}`)
      .then(setData)
      .catch((reason: Error) => setMessage(reason.message))
      .finally(() => setLoading(false));
  }, [country, destination, query, status]);

  async function batch(action: "approve" | "reject" | "disable" | "activate") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/foods/batch", {
        method: "POST",
        body: JSON.stringify({ ids: [...selected], action }),
      });
      setMessage(t("batchUpdated", { count: selected.size }));
      setSelected(new Set());
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
      setLoading(false);
    }
  }

  async function save() {
    if (!editing) return;
    const payload = {
      ...(editing.id ? {} : { slug: editing.slug }),
      country_code: editing.country_code,
      local_name: editing.local_name,
      romanized_name: editing.romanized_name,
      food_kind: editing.food_kind,
      meal_types: editing.meal_types,
      ingredient_tags: editing.ingredient_tags,
      dietary_notes: editing.dietary_notes,
      source_urls: editing.source_urls,
      review_status: editing.review_status,
      is_active: editing.is_active,
      display_order: editing.display_order,
      localizations: editing.localizations,
      destination_ids: editing.destination_ids,
      hotspot_ids: editing.hotspots.map((item) => item.id).filter(Boolean),
    };
    setLoading(true);
    try {
      await api(editing.id ? `/admin/foods/${editing.id}` : "/admin/foods", {
        method: editing.id ? "PATCH" : "POST",
        body: JSON.stringify(payload),
      });
      setMessage(editing.id ? t("updated") : t("created"));
      setEditing(null);
      await load();
    } catch (reason) {
      setMessage((reason as Error).message);
      setLoading(false);
    }
  }

  function csv(value: string) {
    return value
      .split(",")
      .map((item) => item.trim())
      .filter(Boolean);
  }

  return (
    <>
      <section className="mt-8">
        <div className="grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-5">
          <input
            aria-label={t("search")}
            value={query}
            onChange={(event) => setQuery(event.target.value)}
            placeholder={t("searchPlaceholder")}
            className="h-11 rounded-xl border border-[var(--line)] px-3"
          />
          <select
            aria-label={t("country")}
            value={country}
            onChange={(event) => setCountry(event.target.value)}
            className="h-11 rounded-xl border border-[var(--line)] px-3"
          >
            <option value="">{t("allCountries")}</option>
            {["JP", "KR", "TH", "TW", "SG", "HK", "VN"].map((code) => (
              <option key={code}>{code}</option>
            ))}
          </select>
          <input
            aria-label={t("destinationId")}
            value={destination}
            onChange={(event) => setDestination(event.target.value)}
            placeholder={t("destinationId")}
            className="h-11 rounded-xl border border-[var(--line)] px-3"
          />
          <select
            aria-label={t("reviewStatus")}
            value={status}
            onChange={(event) => setStatus(event.target.value)}
            className="h-11 rounded-xl border border-[var(--line)] px-3"
          >
            <option value="">{t("allStatuses")}</option>
            <option value="pending">{t("statuses.pending")}</option>
            <option value="approved">{t("statuses.approved")}</option>
            <option value="rejected">{t("statuses.rejected")}</option>
            <option value="disabled">{t("statuses.disabled")}</option>
          </select>
          <button
            type="button"
            onClick={() => setEditing(blankFood())}
            className="h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white"
          >
            {t("add")}
          </button>
        </div>
        <div className="mt-4 flex flex-wrap items-center gap-2">
          <span className="mr-auto text-sm text-[var(--muted)]">
            {t("selectionCount", {
              total: data?.total ?? 0,
              selected: selected.size,
            })}
          </span>
          <button
            disabled={!selected.size || loading}
            onClick={() => void batch("approve")}
            className="rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-40"
          >
            {t("statuses.approved")}
          </button>
          <button
            disabled={!selected.size || loading}
            onClick={() => void batch("reject")}
            className="rounded-xl border border-[var(--coral)] px-4 py-2 text-sm font-semibold text-[var(--coral)] disabled:opacity-40"
          >
            {t("statuses.rejected")}
          </button>
          <button
            disabled={!selected.size || loading}
            onClick={() => void batch("disable")}
            className="rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:opacity-40"
          >
            {t("statuses.disabled")}
          </button>
          <button
            disabled={!selected.size || loading}
            onClick={() => void batch("activate")}
            className="rounded-xl border border-[var(--teal)] px-4 py-2 text-sm font-semibold text-[var(--teal)] disabled:opacity-40"
          >
            {t("activate")}
          </button>
        </div>
        {message && (
          <p role="status" className="mt-3 text-sm text-[var(--muted)]">
            {message}
          </p>
        )}
        <div className="mt-4 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white">
      <table className="admin-responsive-table admin-foods-table w-full min-w-[920px] text-left text-sm">
            <thead className="bg-[var(--paper)]">
              <tr>
                <th className="p-3">{t("table.select")}</th>
                <th className="p-3">{t("table.food")}</th>
                <th className="p-3">{t("table.kindMeal")}</th>
                <th className="p-3">{t("table.destinationArea")}</th>
                <th className="p-3">{t("table.status")}</th>
                <th className="p-3">{t("table.actions")}</th>
              </tr>
            </thead>
            <tbody>
              {data?.items.map((food) => (
                <tr key={food.id} className="border-t border-[var(--line)]">
                  <td className="p-3">
                    <input
                      type="checkbox"
                      checked={selected.has(food.id)}
                      aria-label={t("selectFood", { name: food.local_name })}
                      onChange={(event) =>
                        setSelected((current) => {
                          const next = new Set(current);
                          if (event.target.checked) next.add(food.id);
                          else next.delete(food.id);
                          return next;
                        })
                      }
                    />
                  </td>
                  <td className="p-3">
                    <strong>
                      {food.localizations.find(
                        (item) => item.locale === "zh-TW",
                      )?.name ?? food.romanized_name}
                    </strong>
                    <span className="block text-xs text-[var(--muted)]">
                      {food.local_name} · {food.slug}
                    </span>
                  </td>
                  <td className="p-3">
                    {t(`kinds.${food.food_kind}`)}
                    <span className="block text-xs text-[var(--muted)]">
                      {food.meal_types.join(" · ")}
                    </span>
                  </td>
                  <td className="p-3">
                    {food.destination_ids.join(" · ")}
                    <span className="block text-xs text-[var(--muted)]">
                      {food.hotspots.map((item) => item.name).join(" · ") ||
                        t("noFoodArea")}
                    </span>
                  </td>
                  <td className="p-3">
                    {t(`statuses.${food.review_status}`)}
                    <span className="block text-xs text-[var(--muted)]">
                      {food.is_active ? t("active") : t("inactive")}
                    </span>
                  </td>
                  <td className="p-3">
                    <button
                      type="button"
                      onClick={() => setEditing(completeLocalizations(food))}
                      className="min-h-10 rounded-xl border border-[var(--teal)] px-3 font-semibold text-[var(--teal)]"
                    >
                      {t("edit")}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!loading && data?.items.length === 0 && (
            <p className="p-8 text-center text-[var(--muted)]">{t("empty")}</p>
          )}
        </div>

        {editing && (
          <div
            className="fixed inset-0 z-[80] overflow-y-auto bg-slate-950/50 p-4 md:p-8"
            role="presentation"
          >
            <div
              role="dialog"
              aria-modal="true"
              aria-labelledby="food-editor-title"
              className="mx-auto max-w-4xl rounded-3xl bg-[var(--paper)] p-5 shadow-2xl md:p-7"
            >
              <div className="flex items-center justify-between gap-4">
                <h2 id="food-editor-title" className="text-2xl font-bold">
                  {editing.id
                    ? t("editTitle", { name: editing.local_name })
                    : t("add")}
                </h2>
                <button
                  type="button"
                  onClick={() => setEditing(null)}
                  className="min-h-11 rounded-xl border border-[var(--line)] px-4"
                >
                  {t("cancel")}
                </button>
              </div>
              <div className="mt-5 grid gap-4 md:grid-cols-3">
                <label className="text-sm font-semibold">
                  {t("fields.slug")}
                  <input
                    disabled={Boolean(editing.id)}
                    value={editing.slug}
                    onChange={(event) =>
                      setEditing({ ...editing, slug: event.target.value })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3 disabled:bg-slate-100"
                  />
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.countryCode")}
                  <input
                    value={editing.country_code}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        country_code: event.target.value.toUpperCase(),
                      })
                    }
                    maxLength={2}
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.kind")}
                  <select
                    value={editing.food_kind}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        food_kind: event.target.value as AdminFood["food_kind"],
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  >
                    <option value="main">{t("kinds.main")}</option>
                    <option value="noodle_soup">
                      {t("kinds.noodle_soup")}
                    </option>
                    <option value="street_food">
                      {t("kinds.street_food")}
                    </option>
                    <option value="dessert">{t("kinds.dessert")}</option>
                    <option value="drink">{t("kinds.drink")}</option>
                  </select>
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.localName")}
                  <input
                    value={editing.local_name}
                    onChange={(event) =>
                      setEditing({ ...editing, local_name: event.target.value })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.romanizedName")}
                  <input
                    value={editing.romanized_name}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        romanized_name: event.target.value,
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.displayOrder")}
                  <input
                    type="number"
                    value={editing.display_order}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        display_order: Number(event.target.value),
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
              </div>
              <div className="mt-4 grid gap-4 md:grid-cols-2">
                <label className="text-sm font-semibold">
                  {t("fields.meals")}
                  <input
                    value={editing.meal_types.join(", ")}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        meal_types: csv(event.target.value),
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.ingredients")}
                  <input
                    value={editing.ingredient_tags.join(", ")}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        ingredient_tags: csv(event.target.value),
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.dietaryNotes")}
                  <input
                    value={editing.dietary_notes.join(", ")}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        dietary_notes: csv(event.target.value),
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
                <label className="text-sm font-semibold">
                  {t("fields.destinations")}
                  <input
                    value={editing.destination_ids.join(", ")}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        destination_ids: csv(event.target.value),
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
                <label className="text-sm font-semibold md:col-span-2">
                  {t("fields.sources")}
                  <textarea
                    value={editing.source_urls.join("\n")}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        source_urls: event.target.value
                          .split("\n")
                          .map((item) => item.trim())
                          .filter(Boolean),
                      })
                    }
                    rows={3}
                    className="mt-1 w-full rounded-xl border p-3"
                  />
                </label>
                <label className="text-sm font-semibold md:col-span-2">
                  {t("fields.hotspots")}
                  <input
                    value={editing.hotspots.map((item) => item.id).join(", ")}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        hotspots: csv(event.target.value).map((id) => ({
                          id,
                          name: id,
                        })),
                      })
                    }
                    className="mt-1 h-11 w-full rounded-xl border px-3"
                  />
                </label>
              </div>
              <div className="mt-5 grid gap-4">
                {editing.localizations.map((localization, index) => (
                  <fieldset
                    key={localization.locale}
                    className="rounded-2xl border border-[var(--line)] bg-white p-4"
                  >
                    <legend className="px-2 font-bold">
                      {localization.locale}
                    </legend>
                    <input
                      aria-label={t("localizedName", {
                        locale: localization.locale,
                      })}
                      value={localization.name}
                      onChange={(event) => {
                        const next = [...editing.localizations];
                        next[index] = {
                          ...localization,
                          name: event.target.value,
                        };
                        setEditing({ ...editing, localizations: next });
                      }}
                      placeholder={t("fields.name")}
                      className="h-11 w-full rounded-xl border px-3"
                    />
                    <textarea
                      aria-label={t("localizedSummary", {
                        locale: localization.locale,
                      })}
                      value={localization.summary}
                      onChange={(event) => {
                        const next = [...editing.localizations];
                        next[index] = {
                          ...localization,
                          summary: event.target.value,
                        };
                        setEditing({ ...editing, localizations: next });
                      }}
                      placeholder={t("summaryPlaceholder")}
                      rows={3}
                      className="mt-3 w-full rounded-xl border p-3"
                    />
                  </fieldset>
                ))}
              </div>
              <div className="mt-5 flex flex-wrap items-center gap-4">
                <label className="flex items-center gap-2">
                  <input
                    type="checkbox"
                    checked={editing.is_active}
                    onChange={(event) =>
                      setEditing({
                        ...editing,
                        is_active: event.target.checked,
                      })
                    }
                  />
                  {t("active")}
                </label>
                <select
                  value={editing.review_status}
                  onChange={(event) =>
                    setEditing({
                      ...editing,
                      review_status: event.target
                        .value as AdminFood["review_status"],
                    })
                  }
                  className="h-11 rounded-xl border px-3"
                >
                  <option value="pending">{t("statuses.pending")}</option>
                  <option value="approved">{t("statuses.approved")}</option>
                  <option value="rejected">{t("statuses.rejected")}</option>
                  <option value="disabled">{t("statuses.disabled")}</option>
                </select>
                <button
                  type="button"
                  disabled={loading}
                  onClick={() => void save()}
                  className="ml-auto min-h-12 rounded-xl bg-[var(--teal)] px-6 font-semibold text-white disabled:opacity-40"
                >
                  {t("save")}
                </button>
              </div>
            </div>
          </div>
        )}
      </section>
      <AdminFoodMerchantsPanel />
    </>
  );
}
