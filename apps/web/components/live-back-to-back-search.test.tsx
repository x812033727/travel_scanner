import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { LiveBackToBackSearch } from "./live-back-to-back-search";

const apiMock = vi.fn();
vi.mock("next/navigation", () => ({ useRouter: () => ({ push: vi.fn() }) }));
vi.mock("@/lib/api", async () => {
  const actual = await vi.importActual<typeof import("@/lib/api")>("@/lib/api");
  return { ...actual, api: (...args: unknown[]) => apiMock(...args) };
});

describe("LiveBackToBackSearch", () => {
  it("submits five-ticket live comparison inputs and renders both modes", async () => {
    apiMock.mockResolvedValue({
      provider: "skyscanner",
      warnings: [],
      comparisons: [
        {
          mode: "mixed_airlines",
          conventional: null,
          back_to_back: null,
          savings: null,
          verdict: "comparison_unavailable",
          detail: "缺少必要票價",
        },
        {
          mode: "same_airline",
          conventional: null,
          back_to_back: null,
          savings: null,
          verdict: "comparison_unavailable",
          detail: "缺少必要票價",
        },
      ],
    });
    render(<LiveBackToBackSearch />);
    fireEvent.change(screen.getByLabelText("成人"), { target: { value: "2" } });
    fireEvent.click(screen.getByRole("button", { name: "開始即時比較" }));

    await waitFor(() => expect(apiMock).toHaveBeenCalled());
    const [path, init] = apiMock.mock.calls[0];
    expect(path).toBe("/flights/back-to-back");
    const payload = JSON.parse(init.body);
    expect(payload.first_destination).toBe("NRT");
    expect(payload.second_destination).toBe("KIX");
    expect(payload.travelers.adults).toBe(2);
    expect(screen.getByRole("heading", { name: "最低混搭" })).toBeTruthy();
    expect(screen.getByRole("heading", { name: "最低同航空公司" })).toBeTruthy();
    expect(screen.getByText(/Powered by/)).toBeTruthy();
  });
});
