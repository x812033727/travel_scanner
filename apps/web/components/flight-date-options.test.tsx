import { fireEvent, render, screen } from "@testing-library/react";
import "@testing-library/jest-dom/vitest";
import { describe, expect, it, vi } from "vitest";
import { FlightDateOptions, type FlightDateOption } from "./flight-date-options";
import { UsageCatalogProvider } from "./usage-catalog-provider";
import { defaultUsageCatalog, searchUsageOperation } from "@/lib/usage-catalog";

const options: FlightDateOption[] = [
  { shift_days: 0, departure_date: "2026-11-10", return_date: "2026-11-15", lowest_price: 15000, currency: "TWD", provider: "skyscanner", source_mode: "live", is_current: true, offer_count: 4 },
  { shift_days: 2, departure_date: "2026-11-12", return_date: "2026-11-17", lowest_price: 12800, currency: "TWD", provider: "skyscanner", source_mode: "estimate", is_current: false, offer_count: 2 },
];

describe("FlightDateOptions", () => {
  it("selects an estimate without applying it, then requires explicit confirmation", () => {
    const select = vi.fn();
    const apply = vi.fn();
    const { rerender } = render(<FlightDateOptions options={options} operation="full_trip_search" onSelect={select} onApply={apply} />);
    fireEvent.click(screen.getByRole("button", { name: /晚 2 日/ }));
    expect(select).toHaveBeenCalledWith(options[1]);
    expect(apply).not.toHaveBeenCalled();

    rerender(<FlightDateOptions options={options} selected={options[1]} operation="full_trip_search" onSelect={select} onApply={apply} />);
    expect(screen.getAllByText(/消耗 1 次/)).toHaveLength(2);
    fireEvent.click(screen.getByRole("button", { name: /^套用並重新搜尋整趟/ }));
    expect(apply).toHaveBeenCalledWith(options[1]);
  });

  it("quotes the operation its caller derived from the payload, not a full trip of its own", () => {
    // Priced apart on purpose: with every operation at one use, a label naming the wrong
    // operation still shows the right number, which is how a hard-coded one went unseen.
    const catalog = {
      ...defaultUsageCatalog,
      operation_costs: { ...defaultUsageCatalog.operation_costs, full_trip_search: 3, flexible_flight_search: 2 },
    };
    // A flight-only search with flexible dates is a flexible_flight_search on the server.
    const operation = searchUsageOperation({ modules: ["flight"], flexibleDates: true });
    render(
      <UsageCatalogProvider state={{ status: "ready", catalog }}>
        <FlightDateOptions options={options} selected={options[1]} operation={operation} onSelect={vi.fn()} onApply={vi.fn()} />
      </UsageCatalogProvider>,
    );

    expect(operation).toBe("flexible_flight_search");
    expect(screen.getByRole("button", { name: /^套用並重新搜尋整趟/ })).toHaveTextContent("消耗 2 次");
    expect(screen.queryByText(/消耗 3 次/)).toBeNull();
  });
});
