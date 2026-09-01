import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { FlightDateOptions, type FlightDateOption } from "./flight-date-options";

const options: FlightDateOption[] = [
  { shift_days: 0, departure_date: "2026-11-10", return_date: "2026-11-15", lowest_price: 15000, currency: "TWD", provider: "skyscanner", source_mode: "live", is_current: true, offer_count: 4 },
  { shift_days: 2, departure_date: "2026-11-12", return_date: "2026-11-17", lowest_price: 12800, currency: "TWD", provider: "skyscanner", source_mode: "estimate", is_current: false, offer_count: 2 },
];

describe("FlightDateOptions", () => {
  it("selects an estimate without applying it, then requires explicit confirmation", () => {
    const select = vi.fn();
    const apply = vi.fn();
    const { rerender } = render(<FlightDateOptions options={options} onSelect={select} onApply={apply} />);
    fireEvent.click(screen.getByRole("button", { name: /晚 2 日/ }));
    expect(select).toHaveBeenCalledWith(options[1]);
    expect(apply).not.toHaveBeenCalled();

    rerender(<FlightDateOptions options={options} selected={options[1]} onSelect={select} onApply={apply} />);
    expect(screen.getAllByText(/消耗 1 次/)).toHaveLength(2);
    fireEvent.click(screen.getByRole("button", { name: /^套用並重新搜尋整趟/ }));
    expect(apply).toHaveBeenCalledWith(options[1]);
  });
});
