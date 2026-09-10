import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminMapIdentitiesPanel } from "./admin-map-identities-panel";
import { mapIdentityCopy } from "@/lib/map-identity-copy";
import { availableMapLinks } from "@/lib/map-identities";

const { request } = vi.hoisted(() => ({ request: vi.fn() }));
vi.mock("@/lib/api", () => ({ api: request }));
const copy = mapIdentityCopy("zh-TW");
const row = {
  kind: "merchant",
  id: "merchant-1",
  name: "명동 음식점",
  local_name: "명동 음식점 본점",
  address: "서울특별시 중구 명동길 1",
  destination_id: "seoul",
  country_code: "KR",
  revision: 3,
  canonical_fingerprint: "canonical-sha",
  google_place_id: null,
  map_identities: {
    naver_maps: {
      provider: "naver_maps",
      place_id: "123",
      map_url: "https://map.naver.com/p/entry/place/123",
      status: "verified",
      verified_at: "2026-09-10T00:00:00Z",
    },
    google_places: {
      provider: "google_places",
      place_id: null,
      map_url: null,
      status: "unverified",
    },
  },
};
const candidates = {
  item: row,
  snapshot_id: "snapshot-1",
  expires_at: "2099-09-10T00:00:00Z",
  candidates: [
    {
      place_id: "ChIJ-branch",
      name: "명동 음식점 (본점)",
      address: row.address,
      country_code: "KR",
      google_maps_url:
        "https://www.google.com/maps/search/?api=1&query_place_id=ChIJ-branch&query=place",
    },
  ],
};
const listing = {
  items: [row],
  total: 1,
  capabilities: { google_places_configured: true },
};

function openPanel() {
  const details = screen.getByText(copy.title).closest("details")!;
  details.open = true;
  fireEvent(details, new Event("toggle"));
}

afterEach(() => {
  vi.clearAllMocks();
});

describe("AdminMapIdentitiesPanel", () => {
  it("does not fetch until expanded, filters city/type/review and starts only selected targets", async () => {
    request.mockImplementation(async (path: string, init?: RequestInit) => {
      if (init?.method === "POST")
        return {
          id: "batch-1",
          total: 1,
          processed: 1,
          status: "completed",
          results: [],
          created_at: "2026-09-10T00:00:00Z",
        };
      return listing;
    });
    render(<AdminMapIdentitiesPanel initialKind="merchant" />);
    expect(request).not.toHaveBeenCalled();
    openPanel();
    await screen.findByRole("checkbox", { name: `${copy.select} ${row.name}` });
    fireEvent.change(screen.getByLabelText(copy.city), {
      target: { value: "seoul" },
    });
    fireEvent.change(screen.getByLabelText(copy.missing), {
      target: { value: "missing" },
    });
    fireEvent.click(screen.getByRole("button", { name: copy.filter }));
    await waitFor(() =>
      expect(request).toHaveBeenCalledWith(
        expect.stringContaining("destination_id=seoul"),
      ),
    );
    expect(request.mock.calls.at(-1)?.[0]).toContain("missing_status=missing");
    expect(request.mock.calls.at(-1)?.[0]).toContain("limit=50");
    fireEvent.click(
      screen.getByRole("checkbox", { name: `${copy.select} ${row.name}` }),
    );
    fireEvent.click(screen.getByRole("button", { name: copy.batch }));
    await screen.findByText(/1\/1/);
    const [path, init] = request.mock.calls.find(
      ([, init]) => init?.method === "POST",
    )!;
    expect(path).toBe("/admin/map-identities/batches");
    expect(JSON.parse(init.body)).toEqual({
      targets: [{ kind: "merchant", id: row.id }],
    });
    expect(init.headers["Idempotency-Key"]).toBeTruthy();
  });

  it("requires explicit single-branch comparison and retains evidence on a version conflict", async () => {
    request.mockImplementation(async (path: string, init?: RequestInit) => {
      if (init?.method === "POST") throw new Error("資料已被修改，請重新載入");
      if (path.endsWith("/candidates")) return candidates;
      return listing;
    });
    render(<AdminMapIdentitiesPanel initialKind="merchant" />);
    openPanel();
    const trigger = await screen.findByRole("button", {
      name: `${copy.review} ${row.name}`,
    });
    fireEvent.click(trigger);
    await screen.findByRole("radio");
    expect(screen.getByRole("button", { name: copy.confirm })).toBeDisabled();
    expect(screen.getAllByText(row.address)).toHaveLength(2);
    fireEvent.click(screen.getByRole("radio"));
    fireEvent.change(screen.getByLabelText(copy.note), {
      target: {
        value: "韓文名稱、明洞本店及完整地址一致，已核對 NAVER 店頁。",
      },
    });
    expect(screen.getByRole("button", { name: copy.confirm })).toBeDisabled();
    fireEvent.click(screen.getByLabelText(copy.checked));
    fireEvent.click(screen.getByRole("button", { name: copy.confirm }));
    await screen.findByRole("alert");
    expect(screen.getByLabelText(copy.note)).toHaveValue(
      "韓文名稱、明洞本店及完整地址一致，已核對 NAVER 店頁。",
    );
    const [, init] = request.mock.calls.find(
      ([, init]) => init?.method === "POST",
    )!;
    expect(JSON.parse(init.body)).toEqual({
      action: "confirm",
      expected_revision: 3,
      expected_fingerprint: "canonical-sha",
      snapshot_id: "snapshot-1",
      place_id: "ChIJ-branch",
      note: "韓文名稱、明洞本店及完整地址一致，已核對 NAVER 店頁。",
    });
    expect(init.body).not.toContain("latitude");
    expect(init.body).not.toContain("naver_map_url");
    fireEvent.click(screen.getByRole("button", { name: copy.close }));
    expect(trigger).toHaveFocus();
  });

  it("does not confirm expired snapshots or unavailable Google service", async () => {
    request.mockImplementation(async (path: string) =>
      path.endsWith("/candidates")
        ? { ...candidates, expires_at: "2000-01-01T00:00:00Z" }
        : listing,
    );
    render(<AdminMapIdentitiesPanel initialKind="merchant" />);
    openPanel();
    fireEvent.click(
      await screen.findByRole("button", { name: `${copy.review} ${row.name}` }),
    );
    fireEvent.click(await screen.findByRole("radio"));
    fireEvent.click(screen.getByLabelText(copy.checked));
    fireEvent.change(screen.getByLabelText(copy.note), {
      target: { value: "review" },
    });
    fireEvent.click(screen.getByRole("button", { name: copy.confirm }));
    await screen.findByText(copy.expired);
    expect(request.mock.calls.some(([, init]) => init?.method === "POST")).toBe(
      false,
    );
  });

  it.each([false, true])(
    "disables mutation when permission or provider is unavailable (%s)",
    async (canManage) => {
      request.mockResolvedValue({
        ...listing,
        capabilities: { google_places_configured: !canManage },
      });
      render(
        <AdminMapIdentitiesPanel
          initialKind="merchant"
          canManage={canManage}
        />,
      );
      openPanel();
      fireEvent.click(
        await screen.findByRole("checkbox", {
          name: `${copy.select} ${row.name}`,
        }),
      );
      expect(screen.getByRole("button", { name: copy.batch })).toBeDisabled();
      const reviewButton = screen.getByRole("button", {
        name: `${copy.review} ${row.name}`,
      });
      expect(reviewButton).toBeDisabled();
      fireEvent.click(reviewButton);
      fireEvent.click(screen.getByRole("button", { name: copy.batch }));
      expect(request.mock.calls.some(([path]) => path.endsWith("/candidates"))).toBe(false);
      expect(request.mock.calls.some(([, init]) => init?.method === "POST")).toBe(false);
    },
  );

  it("keeps both server links, labels a coordinate link as reference and removes unsafe/duplicate URLs", () => {
    const links = availableMapLinks([
      {
        provider: "google",
        label: "Google 位置導航",
        kind: "position",
        url: "https://www.google.com/maps/search/?api=1&query=37.58,126.98",
        primary: false,
      },
      {
        provider: "naver",
        label: "NAVER Maps",
        url: "https://map.naver.com/p/entry/place/123",
        primary: true,
      },
      {
        provider: "naver",
        label: "duplicate",
        url: "https://map.naver.com/p/entry/place/123",
        primary: false,
      },
      {
        provider: "google",
        label: "unsafe",
        url: "javascript:alert(1)",
        primary: false,
      },
    ]);
    expect(links.map((link) => link.provider)).toEqual(["naver", "google"]);
    expect(links[1].label).toBe("Google 位置導航");
    expect(availableMapLinks(undefined)).toEqual([]);
  });

  it("limits even an oversized response to fifty selected records and replays an uncertain batch submission", async () => {
    const rows = Array.from({ length: 51 }, (_, index) => ({
      ...row,
      id: `merchant-${index}`,
      name: `식당 ${index}`,
    }));
    let attempts = 0;
    request.mockImplementation(async (_path: string, init?: RequestInit) => {
      if (init?.method === "POST") {
        attempts += 1;
        if (attempts === 1) throw new Error("服務暫時中斷");
        return {
          id: "batch-1",
          status: "completed",
          total: 50,
          processed: 50,
          results: [],
          created_at: "2026-09-10T00:00:00Z",
        };
      }
      return { items: rows, total: rows.length };
    });
    render(<AdminMapIdentitiesPanel initialKind="merchant" />);
    openPanel();
    await screen.findByRole("checkbox", { name: `${copy.select} 식당 50` });
    fireEvent.click(screen.getByRole("button", { name: copy.selectAll }));
    expect(
      screen.getByRole("checkbox", { name: `${copy.select} 식당 50` }),
    ).toBeDisabled();
    fireEvent.click(screen.getByRole("button", { name: copy.batch }));
    await screen.findByText("服務暫時中斷");
    fireEvent.click(screen.getByRole("button", { name: copy.batch }));
    await screen.findByText(/50\/50/);
    const calls = request.mock.calls.filter(
      ([, init]) => init?.method === "POST",
    );
    expect(calls).toHaveLength(2);
    expect(calls[0][1].headers["Idempotency-Key"]).toBe(
      calls[1][1].headers["Idempotency-Key"],
    );
    expect(JSON.parse(calls[1][1].body).targets).toHaveLength(50);
  });

  it("updates only the confirmed Google identity and keeps the NAVER review visible", async () => {
    request.mockImplementation(async (path: string, init?: RequestInit) => {
      if (init?.method === "POST")
        return {
          ...row,
          revision: 4,
          google_place_id: "ChIJ-branch",
          map_identities: {
            ...row.map_identities,
            google_places: {
              provider: "google_places",
              place_id: "ChIJ-branch",
              map_url: candidates.candidates[0].google_maps_url,
              status: "verified",
            },
          },
        };
      if (path.endsWith("/candidates")) return candidates;
      return listing;
    });
    render(<AdminMapIdentitiesPanel initialKind="merchant" />);
    openPanel();
    fireEvent.click(
      await screen.findByRole("button", { name: `${copy.review} ${row.name}` }),
    );
    fireEvent.click(await screen.findByRole("radio"));
    fireEvent.click(screen.getByLabelText(copy.checked));
    fireEvent.change(screen.getByLabelText(copy.note), {
      target: { value: "韓文名稱、分館與完整地址均一致。" },
    });
    fireEvent.click(screen.getByRole("button", { name: copy.confirm }));
    await screen.findByText(copy.success);
    expect(screen.getByText(/NAVER · 已確認/)).toBeTruthy();
    expect(screen.getByText(/Google · 已確認/)).toBeTruthy();
    expect(screen.queryByRole("radio")).toBeNull();
  });
});
