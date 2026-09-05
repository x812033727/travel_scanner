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

describe("AccountList", () => {
  beforeEach(() => apiMock.mockReset());

  it("edits and pauses an alert", async () => {
    apiMock.mockResolvedValueOnce([alert]);
    apiMock.mockResolvedValueOnce({ ...alert, target_price: 13000 });
    apiMock.mockResolvedValueOnce({ ...alert, target_price: 13000, active: false });
    render(<AccountList kind="alerts" />);
    await screen.findByText("星宇航空");
    fireEvent.click(screen.getByRole("button", { name: "編輯 星宇航空" }));
    fireEvent.change(screen.getByLabelText("編輯 星宇航空 的目標價格"), { target: { value: "13000" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存價格" }));
    await waitFor(() => expect(apiMock).toHaveBeenCalledWith("/alerts/alert-1", { method: "PATCH", body: JSON.stringify({ target_price: 13000 }) }));
    fireEvent.click(screen.getByRole("button", { name: "暫停 星宇航空" }));
    await screen.findByText("已暫停");
  });

  it("links a saved-trip alert back to the trip it watches", async () => {
    apiMock.mockResolvedValueOnce([{
      ...alert,
      id: "alert-2",
      resource_type: "trip",
      resource_id: "trip-9",
      title: "京都五天",
      subtitle: "京都",
      monitoring_mode: "manual_only",
    }]);
    render(<AccountList kind="alerts" />);
    await screen.findByText("京都五天");
    expect(screen.getByRole("link", { name: "查看旅程" }).getAttribute("href")).toBe("/trips/trip-9");
  });

  it("does not remove an item when confirmed deletion fails", async () => {
    apiMock.mockResolvedValueOnce([alert]);
    apiMock.mockRejectedValueOnce(new ApiError("服務暫時無法使用", 503));
    render(<AccountList kind="alerts" />);
    await screen.findByText("星宇航空");
    fireEvent.click(screen.getByRole("button", { name: "刪除通知" }));
    fireEvent.click(screen.getByRole("button", { name: "確定刪除" }));
    await screen.findByText(/操作失敗/);
    expect(screen.getByText("星宇航空")).toBeTruthy();
  });
});
