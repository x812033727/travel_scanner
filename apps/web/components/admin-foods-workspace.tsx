"use client";

import { useMemo, useState, useSyncExternalStore } from "react";
import { useTranslations } from "next-intl";
import { AdminFoodMerchantsPanel, type MerchantTaxonomyFilter } from "./admin-food-merchants-panel";
import { AdminFoodsPanel } from "./admin-foods-panel";
import { AdminFoodAreasPanel, AdminFoodCategoriesPanel } from "./admin-food-taxonomy-panel";

type Tab = "merchants" | "taxonomy" | "dishes";
const tabKeys: Tab[] = ["merchants", "taxonomy", "dishes"];
const taxonomyFilters: MerchantTaxonomyFilter[] = ["missing_area", "missing_category"];

const subscribeToNothing = () => () => {};

// The query string only exists in the browser; reading it through useSyncExternalStore keeps
// server rendering and hydration consistent without a mount effect.
function useClientSearch(): string | null {
  return useSyncExternalStore(
    subscribeToNothing,
    () => window.location.search,
    () => null,
  );
}

function readInitialState(search: string | null): {
  tab: Tab;
  taxonomy: MerchantTaxonomyFilter | "";
} {
  if (search === null) return { tab: "merchants", taxonomy: "" };
  const params = new URLSearchParams(search);
  const tab = params.get("tab");
  const taxonomy = params.get("taxonomy");
  return {
    tab: tabKeys.includes(tab as Tab) ? (tab as Tab) : "merchants",
    taxonomy: taxonomyFilters.includes(taxonomy as MerchantTaxonomyFilter)
      ? (taxonomy as MerchantTaxonomyFilter)
      : "",
  };
}

export function AdminFoodsWorkspace() {
  const t = useTranslations("foodAdmin");
  const search = useClientSearch();
  const initial = useMemo(() => readInitialState(search), [search]);
  const [tabOverride, setTab] = useState<Tab | null>(null);
  const tab = tabOverride ?? initial.tab;
  const initialTaxonomy = initial.taxonomy;
  const ready = search !== null;

  const tabs = useMemo<Array<{ key: Tab; label: string }>>(
    () => [
      { key: "merchants", label: t("tabs.merchants") },
      { key: "taxonomy", label: t("tabs.taxonomy") },
      { key: "dishes", label: t("tabs.dishes") },
    ],
    [t],
  );

  return (
    <div className="mt-8">
      <div
        className="hidden gap-2 overflow-x-auto rounded-2xl border border-[var(--line)] bg-white p-2 sm:flex"
        role="tablist"
        aria-label={t("tabs.label")}
      >
        {tabs.map((item) => (
          <button
            key={item.key}
            type="button"
            role="tab"
            aria-selected={tab === item.key}
            onClick={() => setTab(item.key)}
            className={`min-h-11 shrink-0 rounded-xl px-4 text-sm font-semibold ${tab === item.key ? "bg-[var(--ink)] text-white" : "hover:bg-[var(--paper)]"}`}
          >
            {item.label}
          </button>
        ))}
      </div>
      <label className="block sm:hidden">
        <span className="mb-2 block text-sm font-semibold">{t("tabs.mobileLabel")}</span>
        <select
          value={tab}
          onChange={(event) => setTab(event.target.value as Tab)}
          className="min-h-12 w-full rounded-xl border border-[var(--line)] bg-white px-3"
        >
          {tabs.map((item) => (
            <option key={item.key} value={item.key}>
              {item.label}
            </option>
          ))}
        </select>
      </label>
      {ready && tab === "merchants" && (
        <AdminFoodMerchantsPanel initialTaxonomy={initialTaxonomy} />
      )}
      {ready && tab === "taxonomy" && (
        <>
          <AdminFoodAreasPanel />
          <AdminFoodCategoriesPanel />
        </>
      )}
      {ready && tab === "dishes" && <AdminFoodsPanel />}
    </div>
  );
}
