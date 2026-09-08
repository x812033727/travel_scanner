import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotsWorkspace } from "./admin-hotspots-workspace";

vi.mock("next/navigation", () => ({
  usePathname: () => window.location.pathname,
  useSearchParams: () => new URLSearchParams(window.location.search),
}));

function stubFetch() {
  const fetchMock = vi.fn(async (input: RequestInfo | URL) => {
    const url = new URL(String(input), window.location.origin);
    if (url.pathname.endsWith("/admin/provider-settings")) {
      return new Response(JSON.stringify({ providers: [], audit: [], encryption_source: "test" }));
    }
    if (url.pathname.endsWith("/admin/hotspots/candidates")) {
      return new Response(JSON.stringify({ items: [], total: 0, page: 1, pages: 0, facets: { countries: [], categories: [] } }));
    }
    throw new Error(`Unexpected API request: ${url.pathname}`);
  });
  vi.stubGlobal("fetch", fetchMock);
  return fetchMock;
}

function candidateRequests(fetchMock: ReturnType<typeof stubFetch>) {
  return fetchMock.mock.calls.map(([input]) => new URL(String(input), window.location.origin)).filter((url) => url.pathname.endsWith("/admin/hotspots/candidates"));
}

afterEach(() => { vi.unstubAllGlobals(); window.history.replaceState({}, "", "/"); });

describe("AdminHotspotsWorkspace", () => {
  it.each(["", "?tab=catalog", "#candidates"])("keeps the complete catalog query for the current or legacy entry %s", async (suffix) => {
    const fetchMock = stubFetch();
    window.history.replaceState({}, "", `/zh-TW/admin/hotspots${suffix}`);
    render(<AdminHotspotsWorkspace />);
    expect(await screen.findByRole("tab", { name: "目錄", selected: true })).toBeTruthy();
    await waitFor(() => expect(candidateRequests(fetchMock).length).toBeGreaterThan(0));
    expect(candidateRequests(fetchMock).every((url) => !url.searchParams.has("status"))).toBe(true);
    expect(window.location.pathname).toBe("/zh-TW/admin/hotspots");
    expect(window.location.hash).toBe("");
    expect(fetchMock.mock.calls.every(([input]) => /\/admin\/(?:hotspots\/candidates|provider-settings)/.test(String(input)))).toBe(true);
    expect(screen.queryByText("無法開啟管理後台")).toBeNull();
  });

  it("switches to pending manual review and returns to all catalog statuses", async () => {
    const fetchMock = stubFetch();
    window.history.replaceState({}, "", "/zh-TW/admin/hotspots?tab=review&section=manual");
    render(<AdminHotspotsWorkspace />);
    expect(await screen.findByRole("tab", { name: "審核", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "人工審核", selected: true })).toBeTruthy();
    await waitFor(() => expect(candidateRequests(fetchMock).at(-1)?.searchParams.get("status")).toBe("pending"));
    fireEvent.click(screen.getByRole("tab", { name: "目錄" }));
    await waitFor(() => expect(candidateRequests(fetchMock).at(-1)?.searchParams.get("status")).toBeNull());
    expect(screen.queryByRole("tab", { name: "AI 審核" })).toBeNull();
  });

  it("preserves exact identity and missing-location constraints from dashboard deep links", async () => {
    const fetchMock = stubFetch();
    const id = "11111111-1111-4111-8111-111111111111";
    window.history.replaceState({}, "", `/zh-TW/admin/hotspots?tab=places&section=identity&hotspot_id=${id}&missing_location=true`);
    render(<AdminHotspotsWorkspace />);
    expect(await screen.findByRole("tab", { name: "地點資料", selected: true })).toBeTruthy();
    expect(screen.getByRole("tab", { name: "地圖身分與座標", selected: true })).toBeTruthy();
    await waitFor(() => expect(candidateRequests(fetchMock).length).toBeGreaterThan(0));
    const query = candidateRequests(fetchMock).at(-1)!.searchParams;
    expect(query.get("hotspot_id")).toBe(id);
    expect(query.get("missing_location")).toBe("true");
    expect(query.get("status")).toBeNull();
    expect(new URLSearchParams(window.location.search).get("hotspot_id")).toBe(id);
  });
});
