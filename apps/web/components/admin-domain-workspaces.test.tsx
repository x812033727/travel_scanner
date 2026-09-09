import { useState } from "react";
import { act, fireEvent, render, screen } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotsWorkspace } from "./admin-hotspots-workspace";
import { AdminFoodsWorkspace } from "./admin-foods-workspace";

const probes = vi.hoisted(() => ({ coordinates: vi.fn(), scans: vi.fn(), replace: vi.fn() }));
vi.mock("next/navigation", () => ({ usePathname: () => window.location.pathname, useSearchParams: () => new URLSearchParams(window.location.search) }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ replace: probes.replace }) }));
vi.mock("./admin-hotspots-panel", () => ({ AdminHotspotsPanel: () => <p>hotspot-editor</p> }));
vi.mock("./admin-hotspot-places-panel", () => ({ AdminHotspotPlacesPanel: () => <p>place-data</p> }));
vi.mock("./admin-hotspot-guides-panel", () => ({ AdminHotspotGuidesPanel: () => <p>guide-editor</p> }));
vi.mock("./admin-hotspot-intros-panel", () => ({ AdminHotspotIntrosPanel: () => <p>intro-editor</p> }));
vi.mock("./admin-hotspot-themes-panel", () => ({ AdminHotspotThemesPanel: () => <p>theme-editor</p> }));
vi.mock("./admin-food-merchants-panel", () => ({ AdminFoodMerchantsPanel: ({ initialTaxonomy }: { initialTaxonomy: string }) => <p>merchant-editor:{initialTaxonomy}</p> }));
vi.mock("./admin-foods-panel", () => ({ AdminFoodsPanel: () => <p>dish-editor</p> }));
vi.mock("./admin-food-taxonomy-panel", () => ({ AdminFoodAreasPanel: () => <p>area-editor</p>, AdminFoodCategoriesPanel: () => <p>category-editor</p> }));
vi.mock("./admin-merchant-coordinate-queue", () => ({ AdminMerchantCoordinateQueue: () => { probes.coordinates(); return <p>coordinate-query</p>; } }));
vi.mock("./admin-restaurant-scans-panel", () => ({ AdminRestaurantScansPanel: () => { probes.scans(); return <p>restaurant-scans</p>; } }));
vi.mock("./admin-restaurant-sources-panel", () => ({ AdminRestaurantSourcesPanel: () => <p>restaurant-sources</p> }));
vi.mock("./admin-catalog-review-panel", () => ({ AdminCatalogReviewPanel: ({ scope }: { scope: string }) => <p>ai-review:{scope}</p> }));
vi.mock("./admin-settings-panel", () => ({ AdminSettingsPanel: function Settings({ scope }: { scope: string }) {
  const [value, setValue] = useState("");
  return <input aria-label={"settings-" + scope} value={value} onChange={(event) => setValue(event.target.value)} />;
} }));
beforeEach(() => { vi.clearAllMocks(); window.history.replaceState(null, "", "/zh-TW/admin/foods"); });

describe("domain workspaces", () => {
  it("does not mount paid coordinates, scans or AI on the default food catalog", () => {
    render(<AdminFoodsWorkspace />);
    expect(screen.getByText("merchant-editor:")).toBeTruthy();
    expect(probes.coordinates).not.toHaveBeenCalled();
    expect(probes.scans).not.toHaveBeenCalled();
    expect(screen.queryByText("ai-review:foods")).toBeNull();
    fireEvent.click(screen.getByRole("tab", { name: "資料補齊" }));
    expect(probes.coordinates).toHaveBeenCalled();
    fireEvent.click(screen.getByRole("tab", { name: "目錄" }));
    expect(screen.queryByText("coordinate-query")).toBeNull();
  });
  it("routes food AI to foods and preserves settings drafts between tabs", () => {
    render(<AdminFoodsWorkspace />);
    fireEvent.click(screen.getByRole("tab", { name: "設定" }));
    fireEvent.change(screen.getByLabelText("settings-foods"), { target: { value: "unsaved" } });
    fireEvent.click(screen.getByRole("tab", { name: "審核" }));
    fireEvent.click(screen.getByRole("tab", { name: "AI 審核" }));
    expect(screen.getByText("ai-review:foods")).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: "設定" }));
    expect((screen.getByLabelText("settings-foods") as HTMLInputElement).value).toBe("unsaved");
  });
  it("retains legacy taxonomy filters and applies changed filters on navigation", () => {
    window.history.replaceState(null, "", "/zh-TW/admin/foods?taxonomy=missing_area");
    render(<AdminFoodsWorkspace />);
    expect(screen.getByText("merchant-editor:missing_area")).toBeTruthy();
    act(() => {
      window.history.pushState(null, "", "/zh-TW/admin/foods?taxonomy=missing_category");
      window.dispatchEvent(new PopStateEvent("popstate"));
    });
    expect(screen.getByText("merchant-editor:missing_category")).toBeTruthy();
  });
  it("keeps hotspot content bookmarks and scopes AI independently", () => {
    window.history.replaceState(null, "", "/zh-TW/admin/hotspots#guides");
    render(<AdminHotspotsWorkspace />);
    expect(screen.getByText("guide-editor")).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: "審核" }));
    expect(screen.getByText("hotspot-editor")).toBeTruthy();
    fireEvent.click(screen.getByRole("tab", { name: "AI 審核" }));
    expect(screen.getByText("ai-review:hotspots")).toBeTruthy();
  });
  it("redirects old restaurant sources without mounting hotspot or costed panels", () => {
    window.history.replaceState(null, "", "/zh-TW/admin/hotspots#sources");
    render(<AdminHotspotsWorkspace />);
    expect(probes.replace).toHaveBeenCalledWith("/admin/foods?tab=nearby&section=sources");
    expect(screen.queryByText("hotspot-editor")).toBeNull();
    expect(probes.scans).not.toHaveBeenCalled();
    expect(probes.coordinates).not.toHaveBeenCalled();
  });
});
