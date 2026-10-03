import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { afterEach, describe, expect, it, vi } from "vitest";
import * as nextIntl from "next-intl";
import { fareLabCopy, fareLabText } from "@/lib/fare-lab-copy";
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
      warnings: ["live_fare_failed?role=middle_two_segment"],
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
    fireEvent.click(screen.getByRole("button", { name: /^開始即時比較/ }));

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
    // The API sends a code; the reader sees the ticket named in their language.
    expect(screen.getByText("外站始發兩段票：即時票價查詢失敗")).toBeTruthy();
  });
});

afterEach(() => vi.restoreAllMocks());

describe("localized live comparison details", () => {
  it.each(["en", "ja", "ko", "zh-CN", "zh-TW"])("renders complete and missing-role details in %s", async (locale) => {
    vi.spyOn(nextIntl, "useLocale").mockReturnValue(locale);
    apiMock.mockReset();
    const copy = fareLabCopy(locale);
    const labels: Record<string, string> = copy;
    const missingDetail = "live_comparison_missing?roles=middle_two_segment%2Ctail_one_way";
    apiMock.mockResolvedValue({
      provider: "skyscanner", warnings: [],
      comparisons: [
        { mode: "mixed_airlines", conventional: null, back_to_back: null, savings: null, verdict: "comparison_unavailable", detail: missingDetail },
        { mode: "same_airline", conventional: { components: [], total_price: "22000", currency: "TWD" }, back_to_back: { components: [], total_price: "16000", currency: "TWD" }, savings: "6000", verdict: "back_to_back_cheaper", detail: "live_comparison_complete" },
      ],
    });
    render(<LiveBackToBackSearch />);
    fireEvent.click(screen.getByRole("button", { name: new RegExp("^" + copy["live.search"].split("{charge}")[0]) }));
    await screen.findByRole("heading", { name: copy["mode.mixed_airlines"] });
    expect(screen.queryByText(missingDetail)).toBeNull();
    expect(screen.queryByText("live_comparison_complete")).toBeNull();
    const roles = copy["liveRole.middle_two_segment"] + copy["b2b.listSeparator"] + copy["liveRole.tail_one_way"];
    expect(await screen.findByText(fareLabText(labels["warning.live_comparison_missing"], { roles }))).toBeTruthy();
    expect(screen.getByText(labels["warning.live_comparison_complete"])).toBeTruthy();
    expect(screen.queryByText(missingDetail)).toBeNull();
    expect(screen.queryByText("live_comparison_complete")).toBeNull();
    expect(apiMock).toHaveBeenCalledTimes(1);
    expect(apiMock.mock.calls[0][0]).toBe("/flights/back-to-back");
  });
});