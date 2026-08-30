import { fireEvent, render, screen } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { destinationByAirport } from "@/lib/destinations";
import { SearchCriteriaEditor } from "./search-criteria-editor";

describe("SearchCriteriaEditor", () => {
  it("validates dates and returns updated Japan Korea Thailand criteria", () => {
    const onApply = vi.fn();
    render(<SearchCriteriaEditor
      criteria={{
        origin: "TPE",
        travelers: { adults: 2, children: 0, rooms: 1 },
        budget_twd: 60_000,
        hotel_max_nightly_twd: 5_000,
        interests: ["food"],
        avoid_red_eye: true,
        preferred_area: "普吉老城",
        pace: "balanced",
        include_airbnb: true,
      }}
      destination={destinationByAirport("HKT")}
      dates={["2026-11-10", "2026-11-15"]}
      onApply={onApply}
    />);

    fireEvent.click(screen.getByRole("button", { name: "修改搜尋條件" }));
    fireEvent.change(screen.getByLabelText("回程日期"), { target: { value: "2026-11-09" } });
    fireEvent.click(screen.getByRole("button", { name: "套用並重新規劃" }));
    expect(screen.getByRole("alert").textContent).toContain("回程日期必須晚於出發日期");
    expect(onApply).not.toHaveBeenCalled();

    fireEvent.change(screen.getByLabelText("回程日期"), { target: { value: "2026-11-16" } });
    fireEvent.change(screen.getByLabelText("總預算 TWD"), { target: { value: "85000" } });
    fireEvent.click(screen.getByRole("button", { name: "海灘／跳島" }));
    fireEvent.click(screen.getByRole("button", { name: "套用並重新規劃" }));

    expect(onApply).toHaveBeenCalledWith(expect.objectContaining({
      budget: 85_000,
      returnDate: "2026-11-16",
      interests: ["food", "beach"],
      preferredArea: "普吉老城",
      includeAirbnb: true,
    }));
  });
});
