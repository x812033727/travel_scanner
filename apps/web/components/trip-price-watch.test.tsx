import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { ApiError } from "@/lib/api";
import type { Trip, TripPricingItem } from "@/lib/trip-types";
import { TripPriceWatch } from "./trip-price-watch";

const apiMock = vi.fn();
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

function quote(offerId: string | null, role: string, kind: "flight" | "hotel" = "flight"): TripPricingItem {
  return {
    kind,
    role,
    item_id: `item-${role}`,
    offer_id: offerId,
    counted: true,
    total_price: "11500",
    currency: "TWD",
  };
}

function tripWith(items: TripPricingItem[]): Trip {
  return {
    id: "trip-1",
    name: "東京五天",
    mode: "balanced",
    total_price: 42000,
    currency: "TWD",
    data: {},
    version: 3,
    items: [],
    pricing: items.length
      ? { currency: "TWD", quoted_total: "23000", estimated_total: null, items, unsummed_currencies: [] }
      : null,
  };
}

describe("TripPriceWatch", () => {
  beforeEach(() => {
    apiMock.mockReset();
  });

  it("watches every quoted offer the trip holds, once each", async () => {
    apiMock.mockResolvedValue({});
    render(<TripPriceWatch trip={tripWith([
      quote("offer-out", "outbound_flight"),
      quote("offer-back", "return_flight"),
      // The same offer on two rows is one thing to watch, not two.
      quote("offer-out", "outbound_flight_duplicate"),
      quote("offer-stay", "primary_lodging", "hotel"),
      quote(null, "primary_lodging"),
    ])} />);

    fireEvent.click(screen.getByRole("button", { name: "追蹤這趟旅程的 3 筆報價" }));
    await screen.findByText("已追蹤 3 筆報價");
    expect(apiMock).toHaveBeenCalledTimes(3);
    // The hotel is watched as a hotel; a flight alert on its id would only 404.
    expect(apiMock.mock.calls.map(([, init]) => JSON.parse(String(init.body)))).toEqual([
      { resource_type: "flight", resource_id: "offer-out" },
      { resource_type: "flight", resource_id: "offer-back" },
      { resource_type: "hotel", resource_id: "offer-stay" },
    ]);
    expect(screen.getByRole("link", { name: "前往管理" }).getAttribute("href")).toBe("/alerts");
  });

  it("says there is nothing to watch until something is quoted", () => {
    render(<TripPriceWatch trip={tripWith([quote(null, "primary_lodging", "hotel")])} />);

    expect(screen.queryByRole("button")).toBeNull();
    expect(screen.getByText(/先查機票或住宿才能追蹤價格/)).toBeTruthy();
  });

  it("treats an offer that is already watched as watched", async () => {
    apiMock.mockRejectedValue(new ApiError("已建立過相同的價格通知", 409, "alert_exists"));
    render(<TripPriceWatch trip={tripWith([quote("offer-out", "outbound_flight")])} />);

    fireEvent.click(screen.getByRole("button", { name: /追蹤這趟旅程/ }));
    await screen.findByText("已追蹤 1 筆報價");
  });

  it("asks a signed-out visitor to log in and brings them back to the trip", async () => {
    apiMock.mockRejectedValue(new ApiError("請先登入", 401));
    render(<TripPriceWatch trip={tripWith([quote("offer-out", "outbound_flight")])} />);

    fireEvent.click(screen.getByRole("button", { name: /追蹤這趟旅程/ }));
    const back = await screen.findByRole("link", { name: "回到旅程" });
    expect(back.getAttribute("href")).toContain("next=%2Ftrips%2Ftrip-1");
    expect(screen.queryByText(/已追蹤/)).toBeNull();
  });

  it("keeps the alerts it did create when one of them fails", async () => {
    apiMock.mockImplementation(async (_path: string, init: RequestInit) =>
      JSON.parse(String(init.body)).resource_id === "offer-back"
        ? Promise.reject(new ApiError("服務暫時無法使用", 503))
        : {},
    );
    render(<TripPriceWatch trip={tripWith([
      quote("offer-out", "outbound_flight"),
      quote("offer-back", "return_flight"),
    ])} />);

    fireEvent.click(screen.getByRole("button", { name: /追蹤這趟旅程/ }));
    await screen.findByText("已追蹤 1 筆報價");
  });

  it("shows the failure when nothing could be watched", async () => {
    apiMock.mockRejectedValue(new ApiError("服務暫時無法使用", 503));
    render(<TripPriceWatch trip={tripWith([quote("offer-out", "outbound_flight")])} />);

    fireEvent.click(screen.getByRole("button", { name: /追蹤這趟旅程/ }));
    await waitFor(() => expect(screen.getByRole("alert").textContent).toContain("服務暫時無法使用"));
  });
});
