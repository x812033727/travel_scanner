"use client";

import { useLocale } from "next-intl";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import { useAdminWorkspaceNavigation, type AdminWorkspaceConfig } from "@/lib/admin-workspace-navigation";
import { AdminDomainWorkspace } from "./admin-domain-workspace";
import { AdminCatalogReviewPanel } from "./admin-catalog-review-panel";
import { AdminSettingsPanel } from "./admin-settings-panel";
import { AdminFoodMerchantsPanel, type MerchantTaxonomyFilter } from "./admin-food-merchants-panel";
import { AdminFoodsPanel } from "./admin-foods-panel";
import { AdminFoodAreasPanel, AdminFoodCategoriesPanel } from "./admin-food-taxonomy-panel";
import { AdminMerchantCoordinateQueue } from "./admin-merchant-coordinate-queue";
import { AdminRestaurantScansPanel } from "./admin-restaurant-scans-panel";
import { AdminRestaurantSourcesPanel } from "./admin-restaurant-sources-panel";

export const foodWorkspace: AdminWorkspaceConfig = {
  tabs: { catalog: ["merchants", "dishes"], review: ["merchants", "dishes", "ai"], completion: ["coordinates", "taxonomy"], nearby: ["scans", "sources"], settings: [] },
  defaultTab: "catalog",
  legacy: {
    merchants: { tab: "catalog", section: "merchants" },
    dishes: { tab: "catalog", section: "dishes" },
    coordinates: { tab: "completion", section: "coordinates" },
    taxonomy: { tab: "completion", section: "taxonomy" },
    restaurants: { tab: "nearby", section: "scans" },
    sources: { tab: "nearby", section: "sources" },
  },
};

export function AdminFoodsWorkspace() {
  const copy = adminDomainsCopy(useLocale());
  const nav = useAdminWorkspaceNavigation(foodWorkspace);
  const taxonomyValue = nav.query.get("taxonomy");
  const taxonomy: MerchantTaxonomyFilter | "" = taxonomyValue === "missing_area" || taxonomyValue === "missing_category" ? taxonomyValue : "";
  const tabs = ["catalog", "review", "completion", "nearby", "settings"].map((key) => ({ key, label: copy[key as keyof typeof copy] }));
  const sections = foodWorkspace.tabs[nav.tab]?.map((key) => ({ key, label: copy[key as keyof typeof copy] })) ?? [];
  return <AdminDomainWorkspace id="foods" navigation={nav} tabs={tabs} sections={sections} settings={<AdminSettingsPanel scope="foods" provider={nav.query.get("provider") ?? undefined} field={nav.query.get("field") ?? undefined} />}>
    {(nav.tab === "catalog" || nav.tab === "review") && nav.section === "merchants" && <AdminFoodMerchantsPanel key={nav.tab + taxonomy} initialTaxonomy={taxonomy} initialStatus={nav.tab === "review" ? "pending" : ""} />}
    {(nav.tab === "catalog" || nav.tab === "review") && nav.section === "dishes" && <AdminFoodsPanel key={nav.tab} initialStatus={nav.tab === "review" ? "pending" : ""} />}
    {nav.tab === "review" && nav.section === "ai" && <><p className="my-3 text-sm text-[var(--muted)]">{copy.reviewScope}</p><AdminCatalogReviewPanel scope="foods" /></>}
    {/* Each coordinate queue page costs Google calls: never mount it in an inactive panel. */}
    {nav.tab === "completion" && nav.section === "coordinates" && <AdminMerchantCoordinateQueue />}
    {nav.tab === "completion" && nav.section === "taxonomy" && <><AdminFoodAreasPanel /><AdminFoodCategoriesPanel /></>}
    {nav.tab === "nearby" && <p className="my-3 text-sm text-[var(--muted)]">{copy.sourceScope}</p>}
    {nav.tab === "nearby" && nav.section === "scans" && <AdminRestaurantScansPanel />}
    {nav.tab === "nearby" && nav.section === "sources" && <AdminRestaurantSourcesPanel />}
  </AdminDomainWorkspace>;
}
