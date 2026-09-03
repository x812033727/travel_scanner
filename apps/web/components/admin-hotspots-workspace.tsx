"use client";

import { useTranslations } from "next-intl";
import { AdminHotspotGuidesPanel } from "./admin-hotspot-guides-panel";
import { AdminHotspotPlacesPanel } from "./admin-hotspot-places-panel";
import { AdminHotspotsPanel } from "./admin-hotspots-panel";
import { AdminRestaurantScansPanel } from "./admin-restaurant-scans-panel";
import { AdminRestaurantSourcesPanel } from "./admin-restaurant-sources-panel";
import { AdminTabPanel, AdminTabs, useHashTab } from "./admin-tabs";

const tabKeys = ["candidates", "places", "guides", "restaurants", "sources"] as const;

export function AdminHotspotsWorkspace() {
  const t = useTranslations("admin");
  const [active, select] = useHashTab(tabKeys, "candidates");
  const tabs = tabKeys.map((key) => ({ key, label: t(`hotspotTabs.${key}`) }));

  return (
    <div className="mt-6">
      <AdminTabs
        idPrefix="hotspots"
        label={t("hotspotTabs.label")}
        mobileLabel={t("hotspotTabs.mobileLabel")}
        tabs={tabs}
        active={active}
        onSelect={select}
      />
      <AdminTabPanel idPrefix="hotspots" tabKey="candidates" active={active}>
        <AdminHotspotsPanel />
      </AdminTabPanel>
      <AdminTabPanel idPrefix="hotspots" tabKey="places" active={active}>
        <AdminHotspotPlacesPanel />
      </AdminTabPanel>
      <AdminTabPanel idPrefix="hotspots" tabKey="guides" active={active}>
        <AdminHotspotGuidesPanel />
      </AdminTabPanel>
      <AdminTabPanel idPrefix="hotspots" tabKey="restaurants" active={active}>
        <AdminRestaurantScansPanel />
      </AdminTabPanel>
      <AdminTabPanel idPrefix="hotspots" tabKey="sources" active={active}>
        <AdminRestaurantSourcesPanel />
      </AdminTabPanel>
    </div>
  );
}
