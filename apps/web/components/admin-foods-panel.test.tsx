import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminFoodsPanel } from "./admin-foods-panel";

const item = {
  id: "11111111-1111-4111-8111-111111111111",
  slug: "kr-bibimbap",
  country_code: "KR",
  local_name: "비빔밥",
  romanized_name: "Bibimbap",
  food_kind: "main",
  meal_types: ["lunch", "dinner"],
  ingredient_tags: ["rice"],
  dietary_notes: [],
  source_urls: ["https://english.visitkorea.or.kr/"],
  review_status: "pending",
  is_active: true,
  display_order: 1,
  localizations: [
    { locale: "zh-TW", name: "韓式拌飯", summary: "韓國代表料理。" },
    { locale: "zh-CN", name: "韩式拌饭", summary: "韩国代表料理。" },
    { locale: "en", name: "Bibimbap", summary: "A representative Korean rice dish." },
    { locale: "ja", name: "ビビンバ", summary: "韓国を代表するご飯料理。" },
    { locale: "ko", name: "비빔밥", summary: "한국을 대표하는 밥 요리입니다." },
  ],
  destination_ids: ["seoul"],
  hotspots: [{ id: "22222222-2222-4222-8222-222222222222", name: "廣藏市場" }],
};

describe("AdminFoodsPanel", () => {
  it("lists reviewed content and performs an audited batch action", async () => {
    const fetchMock = vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
      if (String(input).includes("/admin/foods/merchants?")) {
        return new Response(JSON.stringify({ items: [], total: 0, page: 1, pages: 0 }));
      }
      if (init?.method === "POST") {
        expect(JSON.parse(String(init.body))).toEqual({ ids: [item.id], action: "approve" });
        return new Response(JSON.stringify({ updated: 1, status: "approved" }));
      }
      return new Response(JSON.stringify({ items: [item], total: 1, page: 1, pages: 1 }));
    });
    vi.stubGlobal("fetch", fetchMock);

    render(<AdminFoodsPanel />);
    expect(await screen.findByText("韓式拌飯")).toBeTruthy();
    fireEvent.click(screen.getByRole("checkbox", { name: "選取 비빔밥" }));
    fireEvent.click(screen.getByRole("button", { name: "核准" }));

    expect(await screen.findByText("已更新 1 筆美食資料")).toBeTruthy();
    await waitFor(() => expect(fetchMock).toHaveBeenCalledTimes(3));
  });
});
