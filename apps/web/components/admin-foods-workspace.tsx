"use client";

import { useSyncExternalStore } from "react";
import { useTranslations } from "next-intl";
import { AdminFoodMerchantsPanel, type MerchantTaxonomyFilter } from "./admin-food-merchants-panel";
import { AdminFoodsPanel } from "./admin-foods-panel";
import { AdminFoodAreasPanel, AdminFoodCategoriesPanel } from "./admin-food-taxonomy-panel";
import { AdminTabPanel, AdminTabs, useHashTab } from "./admin-tabs";

const tabKeys = ["merchants", "taxonomy", "dishes"] as const;
const taxonomyFilters: MerchantTaxonomyFilter[] = ["missing_area", "missing_category"];

const subscribeToNothing = () => () => {};

/**
 * Reads the `?taxonomy=` deep link the admin dashboard uses for its
 * "categorise merchants" quick action. The query string only exists in the
 * browser, so the server snapshot is `null`; the merchants panel seeds its
 * filter state once and must not mount before the real value is known.
 */
function useTaxonomyParam(): MerchantTaxonomyFilter | "" | null {
  return useSyncExternalStore(
    subscribeToNothing,
    () => {
      const value = new URLSearchParams(window.location.search).get("taxonomy");
      return taxonomyFilters.includes(value as MerchantTaxonomyFilter)
        ? (value as MerchantTaxonomyFilter)
        : "";
    },
    () => null,
  );
}

export function AdminFoodsWorkspace() {
  const t = useTranslations("foodAdmin");
  const [active, select] = useHashTab(tabKeys, "merchants");
  const taxonomy = useTaxonomyParam();
  const tabs = tabKeys.map((key) => ({ key, label: t(`tabs.${key}`) }));

  return (
    <div className="mt-6">
      <AdminTabs
        idPrefix="foods"
        label={t("tabs.label")}
        mobileLabel={t("tabs.mobileLabel")}
        tabs={tabs}
        active={active}
        onSelect={select}
      />
      <AdminTabPanel idPrefix="foods" tabKey="merchants" active={active}>
        {taxonomy !== null && <AdminFoodMerchantsPanel initialTaxonomy={taxonomy} />}
      </AdminTabPanel>
      <AdminTabPanel idPrefix="foods" tabKey="taxonomy" active={active}>
        <AdminFoodAreasPanel />
        <AdminFoodCategoriesPanel />
      </AdminTabPanel>
      <AdminTabPanel idPrefix="foods" tabKey="dishes" active={active}>
        <AdminFoodsPanel />
      </AdminTabPanel>
    </div>
  );
}
