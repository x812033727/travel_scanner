import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import { AccountList } from "./account-list";

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

const alert = { id: "alert-1", resource_type: "flight", resource_id: "flight-1", title: "星宇航空", subtitle: "TPE → NRT", target_price: 14000, current_price: 15000, currency: "TWD", price_updated_at: "2026-08-31T08:00:00Z", active: true };
const usage = { remaining_uses: 3, reserved_uses: 0, available_uses: 3, limits: { saved_trips: 20, price_alerts: 20 }, counts: { saved_trips: 0, price_alerts: 1 } };

type Handler = (init?: RequestInit) => unknown;

/** Route the api mock by path so the capacity request never eats a queued response. */
function stub(routes: Record<string, Handler>) {
  apiMock.mockImplementation(async (path: string, init?: RequestInit) => {
    const key = `${init?.method || "GET"} ${path}`;
    const handler = routes[key];
    if (!handler) throw new Error(`unexpected api call ${key}`);
    return handler(init);
  });
}

describe("AccountList", () => {
  // Braces matter: a hook that returns the mock would have it called as a cleanup function.
  beforeEach(() => {
    apiMock.mockReset();
  });

  it("edits and pauses an alert", async () => {
    stub({
      "GET /alerts": () => [alert],
      "GET /usage": () => usage,
      "PATCH /alerts/alert-1": (init) => ({ ...alert, ...JSON.parse(String(init?.body)) }),
    });
    render(<AccountList kind="alerts" />);
    await screen.findByText("星宇航空");
    fireEvent.click(screen.getByRole("button", { name: "編輯 星宇航空" }));
    fireEvent.change(screen.getByLabelText("編輯 星宇航空 的目標價格"), { target: { value: "13000" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存價格" }));
    await waitFor(() => expect(apiMock).toHaveBeenCalledWith("/alerts/alert-1", { method: "PATCH", body: JSON.stringify({ target_price: 13000 }) }));
    fireEvent.click(screen.getByRole("button", { name: "暫停 星宇航空" }));
    await screen.findByText("已暫停");
  });

  it("shows how close the member is to the alert cap, from the server's count", async () => {
    stub({
      "GET /alerts": () => [alert],
      "GET /usage": () => ({ ...usage, counts: { saved_trips: 0, price_alerts: 20 } }),
    });
    render(<AccountList kind="alerts" />);
    expect(await screen.findByText(/追蹤中 20／20 筆價格通知/)).toBeTruthy();
    expect(screen.getByText(/已達價格通知上限/)).toBeTruthy();
  });

  it("keeps the list usable when the usage summary cannot be loaded", async () => {
    stub({
      "GET /alerts": () => [alert],
      "GET /usage": () => { throw new ApiError("服務暫時無法使用", 503); },
    });
    render(<AccountList kind="alerts" />);
    await screen.findByText("星宇航空");
    expect(screen.queryByText(/筆價格通知/)).toBeNull();
  });

  it("links a saved-trip alert back to the trip it watches", async () => {
    stub({
      "GET /alerts": () => [{
        ...alert,
        id: "alert-2",
        resource_type: "trip",
        resource_id: "trip-9",
        title: "京都五天",
        subtitle: "京都",
        monitoring_mode: "manual_only",
      }],
      "GET /usage": () => usage,
    });
    render(<AccountList kind="alerts" />);
    await screen.findByText("京都五天");
    expect(screen.getByRole("link", { name: "查看旅程" }).getAttribute("href")).toBe("/trips/trip-9");
  });

  it("does not remove an item when confirmed deletion fails", async () => {
    stub({
      "GET /alerts": () => [alert],
      "GET /usage": () => usage,
      "DELETE /alerts/alert-1": () => { throw new ApiError("服務暫時無法使用", 503); },
    });
    render(<AccountList kind="alerts" />);
    await screen.findByText("星宇航空");
    fireEvent.click(screen.getByRole("button", { name: "刪除通知" }));
    fireEvent.click(screen.getByRole("button", { name: "確定刪除" }));
    await screen.findByText(/操作失敗/);
    expect(screen.getByText("星宇航空")).toBeTruthy();
  });
});
