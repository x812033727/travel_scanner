import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminRestaurantScansPanel } from "./admin-restaurant-scans-panel";
import { adminCatalogCopy } from "@/lib/admin-catalog-copy";

const usage = { used: 0, feature_used: 0, budget: 100, percentage: 0, projected_month_end: 0, projected_percentage: 0, alert: "normal" };
const coverage = {
  total: 1, completed: 0, automation_enabled: true,
  items: [{ hotspot_id: "hotspot-1", name: "測試景點", city_name: "東京", country_code: "JP", candidate_count: 0, status: "failed", run_id: null, updated_at: null, usage: { aggregate_calls: 0, details_calls: 0, total_paid_calls: 0 } }],
  usage: { period: "2026-09", available: true, skus: [], operations: {
    aggregate: usage, nearby: usage, details: usage,
    ids_only: { used: 0, billing: "no_charge", budget: null, operations: { text_search: 0, place_id_refresh: 0 } },
  } },
};

describe("AdminRestaurantScansPanel", () => {
  it.each([true, false])("routes automation %s settings to their owner without a duplicate toggle", async (enabled) => {
    const fetchMock = vi.fn<(input: RequestInfo | URL, init?: RequestInit) => Promise<Response>>(async () => new Response(JSON.stringify({ ...coverage, automation_enabled: enabled })));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminRestaurantScansPanel />);
    await screen.findByText(enabled ? "餐廳自動掃描已啟用" : "餐廳自動掃描已暫停");
    expect(screen.getByRole("link", { name: "前往美食設定管理自動掃描" }).getAttribute("href")).toBe("/admin/foods?tab=settings&provider=google_maps&field=restaurant_scan_enabled");
    expect(screen.queryByRole("button", { name: /自動掃描/ })).toBeNull();
    expect(fetchMock.mock.calls.every(([, init]) => !init?.method || init.method === "GET")).toBe(true);
    expect((screen.getByRole("button", { name: "掃描 10 公里" }) as HTMLButtonElement).disabled).toBe(!enabled);
  });

  it.each([true, false])("keeps explicit %s scan/retry operations", async (bulk) => {
    const fetchMock = vi.fn(async (_input: RequestInfo | URL, init?: RequestInit) => new Response(JSON.stringify(init?.method === "POST" ? { status: "queued", runs: [{ run_id: "run-1" }] } : coverage)));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminRestaurantScansPanel />);
    await screen.findByText("測試景點");
    fireEvent.click(screen.getByRole("button", { name: bulk ? "掃描尚未覆蓋景點" : "掃描 10 公里" }));
    await waitFor(() => expect(fetchMock.mock.calls.some(([, init]) => init?.method === "POST")).toBe(true));
    const [url, request] = fetchMock.mock.calls.find(([, init]) => init?.method === "POST")!;
    expect(String(url)).toContain("/restaurants/scans");
    expect(JSON.parse(String(request?.body))).toEqual({ hotspot_ids: bulk ? [] : ["hotspot-1"], all_missing: bulk });
    expect(fetchMock.mock.calls.some(([, init]) => init?.method === "PATCH")).toBe(false);
  });

  it("has complete isolated copy in every supported locale", () => {
    const keys = Object.keys(adminCatalogCopy("en"));
    for (const locale of ["zh-TW", "zh-CN", "ja", "ko"]) {
      const copy = adminCatalogCopy(locale);
      expect(Object.keys(copy)).toEqual(keys);
      expect(Object.values(copy).every((value) => value.trim())).toBe(true);
      expect(copy.identityEditor).not.toBe(adminCatalogCopy("en").identityEditor);
    }
  });
});
