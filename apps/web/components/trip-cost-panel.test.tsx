import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import type { Trip, TripCost } from "@/lib/trip-types";
import { TripCostPanel } from "./trip-cost-panel";

const days = ["2026-11-10", "2026-11-11"];

function trip(cost: Partial<TripCost> = {}): Trip {
  return {
    id: "trip-1",
    name: "東京五日",
    mode: "manual",
    total_price: 0,
    currency: "TWD",
    data: {},
    version: 3,
    items: [],
    cost: {
      currency: "JPY",
      budget: null,
      total: "0",
      difference: null,
      by_day: {},
      by_category: {},
      items: [],
      ...cost,
    },
  } as Trip;
}

function panel(value: Trip, overrides: Partial<Parameters<typeof TripCostPanel>[0]> = {}) {
  return (
    <TripCostPanel
      trip={value}
      days={days}
      activeDay="2026-11-10"
      onSaveBudget={vi.fn(async () => undefined)}
      onSaveCurrency={vi.fn(async () => undefined)}
      onAdd={vi.fn(async () => undefined)}
      onDelete={vi.fn(async () => undefined)}
      onSeed={vi.fn(async () => 0)}
      {...overrides}
    />
  );
}

describe("trip cost panel", () => {
  it("shows the total in the ledger's own currency, not TWD", () => {
    render(panel(trip({ total: "1780", by_category: { food: "980", transport: "800" } })));

    // JPY has no minor unit, so no decimals — and it must not say NT$.
    expect(screen.getByText("¥1,780")).toBeTruthy();
    expect(screen.queryByText(/NT\$/)).toBeNull();
  });

  it("says how far over budget the trip is, with the sign", () => {
    render(panel(trip({ total: "1200", budget: "1000", difference: "-200" })));
    expect(screen.getByText("超出預算 ¥200")).toBeTruthy();
  });

  it("says what is left when the trip is under budget", () => {
    render(panel(trip({ total: "400", budget: "1000", difference: "600" })));
    expect(screen.getByText("預算尚餘 ¥600")).toBeTruthy();
  });

  it("freezes the currency once the ledger holds real numbers", () => {
    render(
      panel(
        trip({
          total: "980",
          items: [
            { id: "e1", day_date: "2026-11-10", label: "一蘭拉麵", amount: "980", category: "food", source: "manual", source_key: null, position: 0 },
          ],
        }),
      ),
    );

    // Nothing here can restate 980 JPY as TWD, so the control is disabled
    // rather than silently relabelling the number.
    expect((screen.getByLabelText("記帳幣別") as HTMLSelectElement).disabled).toBe(true);
    expect(screen.getByText("已有帳目，要換幣別請先清空")).toBeTruthy();
  });

  it("adds a line and clears the form for the next one", async () => {
    const onAdd = vi.fn(async () => undefined);
    render(panel(trip(), { onAdd }));

    fireEvent.change(screen.getByLabelText("項目"), { target: { value: "一蘭拉麵" } });
    fireEvent.change(screen.getByLabelText("金額"), { target: { value: "980" } });
    fireEvent.click(screen.getByRole("button", { name: "新增一筆" }));

    await waitFor(() =>
      expect(onAdd).toHaveBeenCalledWith({
        day_date: "2026-11-10",
        label: "一蘭拉麵",
        amount: "980",
        category: "food",
      }),
    );
    expect((screen.getByLabelText("項目") as HTMLInputElement).value).toBe("");
  });

  it("reports when there was nothing to seed", async () => {
    render(panel(trip(), { onSeed: vi.fn(async () => 0) }));
    fireEvent.click(screen.getByRole("button", { name: "帶入已知價格" }));
    expect(await screen.findByText("沒有可帶入的價格")).toBeTruthy();
  });

  it("surfaces a failed write instead of pretending it worked", async () => {
    render(
      panel(trip(), {
        onSeed: vi.fn(async () => {
          throw new Error("offline");
        }),
      }),
    );
    fireEvent.click(screen.getByRole("button", { name: "帶入已知價格" }));
    expect(await screen.findByRole("alert")).toBeTruthy();
  });
});
