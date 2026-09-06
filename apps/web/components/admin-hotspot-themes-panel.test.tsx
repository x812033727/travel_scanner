import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotThemesPanel } from "./admin-hotspot-themes-panel";

const NAMES = { "zh-TW": "賞櫻", "zh-CN": "赏樱", en: "Cherry Blossoms", ja: "桜", ko: "벚꽃" };

function themesBody() {
  return JSON.stringify({
    items: [
      {
        id: "theme-1",
        slug: "sakura",
        kind: "season",
        names: NAMES,
        months: [3, 4],
        display_order: 1,
        is_active: true,
        source: "seed",
        hotspot_count: 33,
      },
      {
        id: "theme-2",
        slug: "drugstore",
        kind: "shop",
        names: { ...NAMES, "zh-TW": "藥妝" },
        months: [],
        display_order: 11,
        is_active: true,
        source: "seed",
        hotspot_count: 2,
      },
    ],
    total: 2,
  });
}

describe("AdminHotspotThemesPanel", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("lists themes with their months and how many attractions carry them", async () => {
    vi.stubGlobal("fetch", vi.fn<typeof fetch>(async () => new Response(themesBody())));
    render(<AdminHotspotThemesPanel />);

    expect(await screen.findByText("賞櫻")).toBeTruthy();
    expect(screen.getByText("3月–4月")).toBeTruthy();
    expect(screen.getByText("33 個景點")).toBeTruthy();
    // A shop type has no season, and says so rather than showing an empty cell.
    expect(screen.getByText("藥妝")).toBeTruthy();
    expect(screen.getByText("—")).toBeTruthy();
  });

  it("filters to one kind", async () => {
    vi.stubGlobal("fetch", vi.fn<typeof fetch>(async () => new Response(themesBody())));
    render(<AdminHotspotThemesPanel />);
    expect(await screen.findByText("賞櫻")).toBeTruthy();

    fireEvent.click(within(screen.getByRole("group", { name: "主題類型" })).getByRole("button", { name: "購物類型" }));

    expect(screen.queryByText("賞櫻")).toBeNull();
    expect(screen.getByText("藥妝")).toBeTruthy();
  });

  it("refuses to save a season with no months, before asking the server", async () => {
    const fetchMock = vi.fn<typeof fetch>(async () => new Response(themesBody()));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotThemesPanel />);
    expect(await screen.findByText("賞櫻")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "新增主題" }));
    fireEvent.change(screen.getByLabelText(/代碼/), { target: { value: "hanami" } });
    for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
      fireEvent.change(screen.getByLabelText(`${locale} 名稱`), { target: { value: "花見" } });
    }
    fireEvent.click(screen.getByRole("button", { name: "儲存主題" }));

    expect(await screen.findByRole("alert")).toHaveProperty("textContent", "季節主題至少要選一個月份");
    expect(fetchMock.mock.calls.filter(([, init]) => (init as RequestInit)?.method === "POST")).toHaveLength(0);
  });

  it("creates a theme with the months that were toggled", async () => {
    const fetchMock = vi.fn<typeof fetch>(async (...args) =>
      (args[1] as RequestInit)?.method === "POST"
        ? new Response("{}", { status: 201 })
        : new Response(themesBody()),
    );
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotThemesPanel />);
    expect(await screen.findByText("賞櫻")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "新增主題" }));
    fireEvent.change(screen.getByLabelText(/代碼/), { target: { value: "hanami" } });
    for (const locale of ["zh-TW", "zh-CN", "en", "ja", "ko"]) {
      fireEvent.change(screen.getByLabelText(`${locale} 名稱`), { target: { value: "花見" } });
    }
    const months = screen.getByRole("group", { name: "適用月份" });
    fireEvent.click(within(months).getByRole("button", { name: "4月" }));
    fireEvent.click(within(months).getByRole("button", { name: "3月" }));
    fireEvent.click(screen.getByRole("button", { name: "儲存主題" }));

    await waitFor(() => {
      const post = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === "POST");
      expect(post).toBeTruthy();
      const body = JSON.parse(String((post?.[1] as RequestInit).body));
      expect(body.slug).toBe("hanami");
      expect(body.kind).toBe("season");
      // Toggled out of order, stored in order.
      expect(body.months).toEqual([3, 4]);
      expect(body.names["zh-TW"]).toBe("花見");
    });
  });
});
