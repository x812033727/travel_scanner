"use client";

import { useTranslations } from "next-intl";
import { AdminFoodMerchantsPanel } from "./admin-food-merchants-panel";
import { AdminFoodsPanel } from "./admin-foods-panel";
import { AdminTabPanel, AdminTabs, useHashTab } from "./admin-tabs";

const tabKeys = ["catalog", "merchants"] as const;

export function AdminFoodsWorkspace() {
  const t = useTranslations("foodAdmin");
  const [active, select] = useHashTab(tabKeys, "catalog");
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
      <AdminTabPanel idPrefix="foods" tabKey="catalog" active={active}>
        <AdminFoodsPanel />
      </AdminTabPanel>
      <AdminTabPanel idPrefix="foods" tabKey="merchants" active={active}>
        <AdminFoodMerchantsPanel />
      </AdminTabPanel>
    </div>
  );
}
