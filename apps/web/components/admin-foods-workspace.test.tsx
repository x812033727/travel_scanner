import { act, fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { AdminFoodsWorkspace } from "./admin-foods-workspace";

vi.mock("next/navigation", () => ({
  usePathname: () => window.location.pathname,
  useSearchParams: () => new URLSearchParams(window.location.search),
}));

function stubFetch() {
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
      const url = String(input);
      // The retained settings panel requests metadata only, never connection tests.
      if (url.includes("/admin/provider-settings")) {
        return new Response(JSON.stringify({ providers: [], audit: [], encryption_source: "test" }));
      }
      if (url.includes("/foods/cities")) {
        return new Response(JSON.stringify({ total_merchants: 0, countries: [] }));
      }
      if (/coordinate|map-candidates|restaurant-scans|catalog-review/.test(url)) throw new Error(`Unexpected paid request: ${url}`);
      return new Response(JSON.stringify({ items: [], total: 0, page: 1, pages: 0 }));
    });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

function requests(fetchMock: ReturnType<typeof stubFetch>, path: string) {
  return fetchMock.mock.calls.map(([input]) => new URL(String(input), window.location.origin)).filter((url) => url.pathname.endsWith(path));
}

beforeEach(() => window.history.replaceState({}, "", "/zh-TW/admin/foods"));
afterEach(() => { vi.unstubAllGlobals(); window.history.replaceState({}, "", "/"); });

describe("AdminFoodsWorkspace", () => {
  it("opens all merchants in Catalog without loading paid completion or AI panels", async () => {
    const fetchMock = stubFetch();
    render(<AdminFoodsWorkspace />);

    const workspace = await screen.findByRole("tablist", { name: "管理工作區" });
    expect(within(workspace).getAllByRole("tab").map((tab) => tab.textContent)).toEqual(["目錄", "審核", "資料補齊", "周邊餐廳", "設定"]);
    expect(screen.getByRole("tab", { name: "目錄", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "精選店家", selected: true })).toBeTruthy();
    expect(
      await screen.findByRole("heading", { name: "店家、地圖識別與永久座標" }),
    ).toBeTruthy();
    expect(screen.getByRole("button", { name: "新增店家" })).toBeTruthy();
    await waitFor(() => expect(requests(fetchMock, "/admin/foods/merchants").length).toBeGreaterThan(0));
    expect(requests(fetchMock, "/admin/foods/merchants").every((url) => !url.searchParams.has("status"))).toBe(true);
    await waitFor(() => expect(requests(fetchMock, "/admin/provider-settings")).toHaveLength(1));
    expect(fetchMock.mock.calls.some(([input]) => /coordinate|map-candidates|restaurant-scans|catalog-review/.test(String(input)))).toBe(false);
    expect(screen.queryByText("無法開啟管理後台")).toBeNull();
  });

  it("opens the areas and cuisines tab from the URL hash", async () => {
    const fetchMock = stubFetch();
    window.history.replaceState({}, "", "/zh-TW/admin/foods#taxonomy");
    render(<AdminFoodsWorkspace />);

    expect(await screen.findByRole("heading", { name: "區域（商圈）" })).toBeTruthy();
    expect(await screen.findByRole("heading", { name: "美食分類" })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "區域與分類", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "資料補齊", selected: true })).toBeTruthy();
    expect(screen.getByRole("button", { name: "新增區域" })).toBeTruthy();
    expect(screen.getByRole("button", { name: "新增分類" })).toBeTruthy();
    await waitFor(() => expect(requests(fetchMock, "/admin/foods/areas").length).toBeGreaterThan(0));
    expect(requests(fetchMock, "/admin/foods/categories").length).toBeGreaterThan(0);
    expect(new URLSearchParams(window.location.search).get("tab")).toBe("completion");
    expect(new URLSearchParams(window.location.search).get("section")).toBe("taxonomy");
    expect(window.location.hash).toBe("");
    expect(window.location.pathname).toBe("/zh-TW/admin/foods");
  });

  it.each(["/zh-TW/admin/foods?taxonomy=missing_area", "/zh-TW/admin/foods?tab=catalog&section=merchants&taxonomy=missing_area"])("applies the dashboard taxonomy deep link %s", async (url) => {
    const fetchMock = stubFetch();
    window.history.replaceState({}, "", url);
    render(<AdminFoodsWorkspace />);

    expect(await screen.findByRole("tab", { name: "精選店家", selected: true })).toBeTruthy();
    await waitFor(() => expect(requests(fetchMock, "/admin/foods/merchants").some((request) => request.searchParams.get("taxonomy") === "missing_area")).toBe(true));
    expect(new URLSearchParams(window.location.search).get("taxonomy")).toBe("missing_area");
  });

  it("filters pending merchants and dishes in Review and restores the full Catalog query", async () => {
    const fetchMock = stubFetch();
    render(<AdminFoodsWorkspace />);
    fireEvent.click(await screen.findByRole("tab", { name: "審核" }));
    await waitFor(() => expect(requests(fetchMock, "/admin/foods/merchants").at(-1)?.searchParams.get("status")).toBe("pending"));
    fireEvent.click(screen.getByRole("tab", { name: "料理" }));
    expect(await screen.findByRole("button", { name: "新增美食" })).toBeTruthy();
    await waitFor(() => expect(requests(fetchMock, "/admin/foods").at(-1)?.searchParams.get("status")).toBe("pending"));
    fireEvent.click(screen.getByRole("tab", { name: "目錄" }));
    await waitFor(() => expect(requests(fetchMock, "/admin/foods/merchants").at(-1)?.searchParams.get("status")).toBeNull());
    expect(screen.getByRole("tab", { name: "精選店家", selected: true })).toBeTruthy();
  });

  it("keeps the legacy dishes hash as the full catalog, not the pending queue", async () => {
    const fetchMock = stubFetch();
    window.history.replaceState({}, "", "/zh-TW/admin/foods#dishes");
    render(<AdminFoodsWorkspace />);
    expect(await screen.findByRole("tab", { name: "料理", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "目錄", selected: true })).toBeTruthy();
    expect(await screen.findByRole("button", { name: "新增美食" })).toBeTruthy();
    await waitFor(() => expect(requests(fetchMock, "/admin/foods").length).toBeGreaterThan(0));
    expect(requests(fetchMock, "/admin/foods").every((url) => !url.searchParams.has("status"))).toBe(true);
  });

  it("reloads the merchant filter on Back/Forward taxonomy navigation", async () => {
    const fetchMock = stubFetch();
    window.history.replaceState({}, "", "/zh-TW/admin/foods?taxonomy=missing_area");
    render(<AdminFoodsWorkspace />);
    await waitFor(() => expect(requests(fetchMock, "/admin/foods/merchants").at(-1)?.searchParams.get("taxonomy")).toBe("missing_area"));
    act(() => {
      window.history.pushState({}, "", "/zh-TW/admin/foods?tab=catalog&section=merchants&taxonomy=missing_category");
      window.dispatchEvent(new PopStateEvent("popstate"));
    });
    await waitFor(() => expect(requests(fetchMock, "/admin/foods/merchants").at(-1)?.searchParams.get("taxonomy")).toBe("missing_category"));
    expect(screen.getByRole("tab", { name: "目錄", selected: true })).toBeTruthy();
  });
});
