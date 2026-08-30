import { render, screen } from "@testing-library/react";
import { describe, expect, it } from "vitest";
import { BudgetBreakdown } from "./budget-breakdown";

describe("BudgetBreakdown", () => {
  it("shows remaining budget and separates quoted from estimated costs", () => {
    render(<BudgetBreakdown budget={60_000} cost={{
      confirmed_cost: "48000",
      estimated_cost: "4000",
      total_cost: "52000",
      components: [
        { category: "flight_base", label: "機票票價", amount: "30000", confidence: "confirmed" },
        { category: "local_transport", label: "當地交通估算", amount: "4000", confidence: "estimated" },
      ],
    }} />);

    expect(screen.getByText(/預算尚餘.*8,000/)).toBeTruthy();
    expect(screen.getByText(/報價項目.*48,000/)).toBeTruthy();
    expect(screen.getByText(/估算項目.*4,000/)).toBeTruthy();
    expect(screen.getByRole("img", { name: /已使用總預算的 87%/ })).toBeTruthy();
  });
});
