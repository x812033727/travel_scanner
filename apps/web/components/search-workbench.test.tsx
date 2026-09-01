import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SearchWorkbench } from "./search-workbench";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push }) }));

describe("SearchWorkbench", () => {
  beforeEach(() => {
    push.mockReset();
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify({
      assumptions: ["推薦階段使用估算資料"],
      recommendations: [{
        candidate_id: "HKT:2026-11-10:5",
        city: "普吉",
        airport: "HKT",
        country: "泰國",
        country_code: "TH",
        areas: ["普吉老城", "卡塔"],
        reason: "海灘與度假選擇完整",
        departure_date: "2026-11-10",
        return_date: "2026-11-15",
        trip_length_days: 5,
        estimated_flight_twd: 21000,
        estimated_lodging_twd: 18000,
        estimated_total_twd: 55000,
        score: 92,
        matched_interests: ["beach"],
        relaxed_preferences: [],
      }],
    }), { status: 200 })));
  });

  it("sends structured options and continues with the selected recommendation", async () => {
    render(<SearchWorkbench />);
    fireEvent.click(screen.getByRole("button", { name: /泰國/ }));
    fireEvent.change(screen.getByLabelText("指定城市"), { target: { value: "HKT" } });
    fireEvent.change(screen.getByLabelText("兒童人數"), { target: { value: "2" } });
    fireEvent.change(screen.getByLabelText("第 2 位兒童年齡"), { target: { value: "12" } });
    fireEvent.click(screen.getByRole("button", { name: "兩種都接受" }));
    fireEvent.click(screen.getByRole("button", { name: "海灘／跳島" }));
    for (let index = 0; index < 4; index += 1) {
      fireEvent.click(screen.getByRole("button", { name: /下一步/ }));
    }
    fireEvent.click(screen.getByRole("button", { name: /請 AI 推薦 3 組/ }));

    await screen.findByRole("heading", { name: "泰國・普吉" });
    const request = JSON.parse(String((vi.mocked(fetch).mock.calls[0][1] as RequestInit).body));
    expect(request.destination_countries).toEqual(["JP", "TH"]);
    expect(request.destination_codes).toEqual(["HKT"]);
    expect(request.travelers.children_ages).toEqual([8, 12]);
    expect(request.lodging_preferences.accepted_property_types).toEqual(["hotel", "vacation_rental"]);

    fireEvent.change(screen.getByLabelText("偏好住宿區域"), { target: { value: "普吉老城" } });
    fireEvent.click(screen.getByRole("button", { name: /用這組條件搜尋/ }));
    await waitFor(() => expect(push).toHaveBeenCalledOnce());
    const url = new URL(push.mock.calls[0][0], "https://travel.test");
    expect(url.searchParams.get("destination")).toBe("HKT");
    expect(url.searchParams.get("children_ages")).toBe("8,12");
    expect(url.searchParams.get("interests")).toContain("beach");
    expect(url.searchParams.get("accepted_property_types")).toBe("hotel,vacation_rental");
    expect(url.searchParams.get("preferred_areas")).toBe("普吉老城");
    expect(url.searchParams.get("include_airbnb")).toBe("true");
  }, 10_000);
});
