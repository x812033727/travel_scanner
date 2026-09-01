import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import { SearchWorkbench } from "./search-workbench";

const { push } = vi.hoisted(() => ({ push: vi.fn() }));
vi.mock("@/i18n/navigation", () => ({ useRouter: () => ({ push }) }));

describe("SearchWorkbench", () => {
  beforeEach(() => {
    push.mockReset();
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => new Response(JSON.stringify(String(input).endsWith("/destinations") ? { items: [] } : {
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
    const discoveryCall = vi.mocked(fetch).mock.calls.find((call) => (call[1] as RequestInit | undefined)?.method === "POST")!;
    const request = JSON.parse(String((discoveryCall[1] as RequestInit).body));
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

  it("loads secondary destinations and offers only their configured extension cities", async () => {
    vi.stubGlobal("fetch", vi.fn(async (input: RequestInfo | URL) => {
      if (String(input).endsWith("/destinations")) {
        return new Response(JSON.stringify({ items: [
          { id: "kaohsiung", code: "KHH", city: "高雄", country_code: "TW", role: "secondary", parent_destination_id: null, gateway_codes: ["KHH"], primary_gateway: "KHH", areas: ["鹽埕"], recommended_days: { min: 3, max: 5 }, timezone: "Asia/Taipei", currency: "TWD", reason: "港都慢遊", searchable: true },
          { id: "tainan", code: "TNN", city: "台南", country_code: "TW", role: "extension", parent_destination_id: "kaohsiung", gateway_codes: ["KHH"], primary_gateway: "KHH", areas: ["中西區"], recommended_days: { min: 1, max: 2 }, timezone: "Asia/Taipei", currency: "TWD", reason: "府城延伸", searchable: false },
        ] }));
      }
      return new Response(JSON.stringify({ assumptions: [], recommendations: [{
        candidate_id: "KHH:2026-11-10:5", city: "高雄", airport: "KHH", country: "台灣", country_code: "TW", areas: ["鹽埕"], reason: "港都慢遊", departure_date: "2026-11-10", return_date: "2026-11-15", trip_length_days: 5, estimated_flight_twd: 3000, estimated_lodging_twd: 12000, estimated_total_twd: 20000, score: 90, matched_interests: [], relaxed_preferences: [],
      }] }));
    }));
    render(<SearchWorkbench />);
    fireEvent.click(screen.getByRole("button", { name: /台灣/ }));
    await screen.findByRole("option", { name: "高雄 · KHH" });
    fireEvent.change(screen.getByLabelText("指定城市"), { target: { value: "KHH" } });
    fireEvent.click(await screen.findByRole("checkbox", { name: "台南" }));
    for (let index = 0; index < 4; index += 1) fireEvent.click(screen.getByRole("button", { name: /下一步/ }));
    fireEvent.click(screen.getByRole("button", { name: /請 AI 推薦 3 組/ }));
    await screen.findByRole("heading", { name: "台灣・高雄" });
    fireEvent.click(screen.getByRole("button", { name: /用這組條件搜尋/ }));
    await waitFor(() => expect(push).toHaveBeenCalledOnce());
    const url = new URL(push.mock.calls[0][0], "https://travel.test");
    expect(url.searchParams.get("extension_destination_ids")).toBe("tainan");
  });
});
