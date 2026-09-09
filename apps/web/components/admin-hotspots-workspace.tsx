"use client";

import { useLocale } from "next-intl";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import { useAdminWorkspaceNavigation, type AdminWorkspaceConfig } from "@/lib/admin-workspace-navigation";
import { AdminDomainWorkspace } from "./admin-domain-workspace";
import { AdminCatalogReviewPanel } from "./admin-catalog-review-panel";
import { AdminSettingsPanel } from "./admin-settings-panel";
import { AdminHotspotGuidesPanel } from "./admin-hotspot-guides-panel";
import { AdminHotspotIntrosPanel } from "./admin-hotspot-intros-panel";
import { AdminHotspotThemesPanel } from "./admin-hotspot-themes-panel";
import { AdminHotspotPlacesPanel } from "./admin-hotspot-places-panel";
import { AdminHotspotsPanel } from "./admin-hotspots-panel";

export const hotspotWorkspace: AdminWorkspaceConfig = {
  tabs: { catalog: ["catalog"], review: ["manual", "ai"], places: ["identity", "google"], content: ["guides", "themes", "intros"], settings: [] },
  defaultTab: "catalog",
  legacy: {
    candidates: { tab: "catalog" },
    places: { tab: "places", section: "google" },
    guides: { tab: "content", section: "guides" },
    themes: { tab: "content", section: "themes" },
    intros: { tab: "content", section: "intros" },
    restaurants: { tab: "nearby", section: "scans", pathname: "/admin/foods" },
    sources: { tab: "nearby", section: "sources", pathname: "/admin/foods" },
  },
};

export function AdminHotspotsWorkspace() {
  const copy = adminDomainsCopy(useLocale());
  const nav = useAdminWorkspaceNavigation(hotspotWorkspace);
  const tabs = ["catalog", "review", "places", "content", "settings"].map((key) => ({ key, label: copy[key as keyof typeof copy] }));
  const sections = hotspotWorkspace.tabs[nav.tab]?.map((key) => ({ key, label: copy[key as keyof typeof copy] })) ?? [];
  return <AdminDomainWorkspace id="hotspots" navigation={nav} tabs={tabs} sections={sections} settings={<AdminSettingsPanel scope="hotspots" provider={nav.query.get("provider") ?? undefined} field={nav.query.get("field") ?? undefined} />}>
    {nav.tab === "catalog" || nav.tab === "review" && nav.section === "manual" ? <AdminHotspotsPanel key={nav.tab} initialStatus={nav.tab === "review" ? "pending" : ""} locationEditing="link" /> : null}
    {nav.tab === "review" && nav.section === "ai" && <><p className="my-3 text-sm text-[var(--muted)]">{copy.reviewScope}</p><AdminCatalogReviewPanel scope="hotspots" /></>}
    {nav.tab === "places" && nav.section === "identity" && <AdminHotspotsPanel key={nav.query.get("hotspot_id") ?? "identity"} initialStatus="" initialHotspotId={nav.query.get("hotspot_id") ?? undefined} initialMissingLocation={nav.query.get("missing_location") === "true"} />}
    {nav.tab === "places" && nav.section === "google" && <AdminHotspotPlacesPanel />}
    {nav.tab === "content" && nav.section === "guides" && <AdminHotspotGuidesPanel />}
    {nav.tab === "content" && nav.section === "themes" && <AdminHotspotThemesPanel />}
    {nav.tab === "content" && nav.section === "intros" && <AdminHotspotIntrosPanel />}
  </AdminDomainWorkspace>;
}
