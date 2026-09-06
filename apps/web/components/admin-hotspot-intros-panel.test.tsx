import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import { AdminHotspotIntrosPanel } from "./admin-hotspot-intros-panel";

function introsBody() {
  return JSON.stringify({
    items: [
      {
        id: "intro-1",
        hotspot_id: "hotspot-1",
        hotspot_name: "淺草寺",
        locale: "zh-TW",
        body: "淺草寺是東京最古老的寺院。",
        status: "pending",
        source: "ai",
        ai_provider: "gemini",
        ai_model: "gemini-3.8-flash",
        updated_at: "2026-09-07T00:00:00Z",
      },
      {
        id: "intro-2",
        hotspot_id: "hotspot-2",
        hotspot_name: "秋葉原",
        locale: "ja",
        body: "電気街として知られています。",
        status: "pending",
        source: "manual",
        ai_provider: null,
        ai_model: null,
        updated_at: "2026-09-07T00:00:00Z",
      },
    ],
    total: 2,
    status_counts: { pending: 2, approved: 7 },
  });
}

describe("AdminHotspotIntrosPanel", () => {
  afterEach(() => vi.unstubAllGlobals());

  it("shows the pending queue with where each draft came from", async () => {
    vi.stubGlobal("fetch", vi.fn<typeof fetch>(async () => new Response(introsBody())));
    render(<AdminHotspotIntrosPanel />);

    expect(await screen.findByText("淺草寺")).toBeTruthy();
    expect(screen.getByText("待審 2・已核准 7")).toBeTruthy();
    expect(screen.getByText(/AI 草稿/)).toBeTruthy();
    expect(screen.getByText("手動")).toBeTruthy();
  });

  it("approves the drafts that were selected", async () => {
    const fetchMock = vi.fn<typeof fetch>(async (...args) =>
      (args[1] as RequestInit)?.method === "POST"
        ? new Response(JSON.stringify({ updated: 1, status: "approved" }))
        : new Response(introsBody()),
    );
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotIntrosPanel />);
    expect(await screen.findByText("淺草寺")).toBeTruthy();

    // Approve is unavailable until something is chosen.
    expect(screen.getByRole("button", { name: "核准" })).toHaveProperty("disabled", true);
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 淺草寺（zh-TW）" }));
    fireEvent.click(screen.getByRole("button", { name: "核准" }));

    await waitFor(() => {
      const post = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === "POST");
      expect(post).toBeTruthy();
      expect(String(post?.[0])).toContain("/admin/hotspots/intros/review");
      const body = JSON.parse(String((post?.[1] as RequestInit).body));
      expect(body).toEqual({ ids: ["intro-1"], action: "approve" });
    });
  });

  it("edits the wording before approving it", async () => {
    const fetchMock = vi.fn<typeof fetch>(async (...args) =>
      (args[1] as RequestInit)?.method === "PATCH" ? new Response("{}") : new Response(introsBody()),
    );
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotIntrosPanel />);
    expect(await screen.findByText("淺草寺")).toBeTruthy();

    const card = screen.getByText("淺草寺").closest("article") as HTMLElement;
    fireEvent.click(within(card).getByRole("button", { name: "編輯內容" }));
    fireEvent.change(within(card).getByLabelText("介紹內容"), {
      target: { value: "改寫過的介紹。" },
    });
    fireEvent.click(within(card).getByRole("button", { name: "儲存內容" }));

    await waitFor(() => {
      const patch = fetchMock.mock.calls.find(([, init]) => (init as RequestInit)?.method === "PATCH");
      expect(patch).toBeTruthy();
      expect(String(patch?.[0])).toContain("/admin/hotspots/intros/intro-1");
      expect(JSON.parse(String((patch?.[1] as RequestInit).body))).toEqual({ body: "改寫過的介紹。" });
    });
  });

  it("asks the server again when the status filter changes", async () => {
    const fetchMock = vi.fn<typeof fetch>(async () => new Response(introsBody()));
    vi.stubGlobal("fetch", fetchMock);
    render(<AdminHotspotIntrosPanel />);
    expect(await screen.findByText("淺草寺")).toBeTruthy();
    // The queue opens on what needs a decision.
    expect(String(fetchMock.mock.calls[0][0])).toContain("status=pending");

    fireEvent.change(screen.getByLabelText("狀態"), { target: { value: "approved" } });

    await waitFor(() =>
      expect(
        fetchMock.mock.calls.some(([input]) => String(input).includes("status=approved")),
      ).toBe(true),
    );
  });

  it("narrows the list as an editor types an attraction name", async () => {
    vi.stubGlobal("fetch", vi.fn<typeof fetch>(async () => new Response(introsBody())));
    render(<AdminHotspotIntrosPanel />);
    expect(await screen.findByText("淺草寺")).toBeTruthy();

    fireEvent.change(screen.getByLabelText("景點名稱"), { target: { value: "秋葉" } });

    expect(screen.queryByText("淺草寺")).toBeNull();
    expect(screen.getByText("秋葉原")).toBeTruthy();
  });
});
