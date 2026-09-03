import { fireEvent, render, screen, waitFor, within } from "@testing-library/react";
import { describe, expect, it, vi } from "vitest";
import { AdminFoodAreasPanel, AdminFoodCategoriesPanel } from "./admin-food-taxonomy-panel";

const area = {
  id: "area-1",
  slug: "seoul-myeongdong",
  destination_id: "seoul",
  destination_name: "首爾",
  country_code: "KR",
  name: "明洞",
  names: { "zh-TW": "明洞", "zh-CN": "明洞", en: "Myeongdong", ja: "明洞", ko: "명동" },
  match_terms: ["명동"],
  latitude: null,
  longitude: null,
  is_active: true,
  display_order: 1,
  source: "seed",
  merchant_count: 3,
};
const category = {
  id: "cat-1",
  slug: "ramen",
  name: "拉麵",
  names: { "zh-TW": "拉麵", "zh-CN": "拉面", en: "Ramen", ja: "ラーメン", ko: "라멘" },
  is_active: true,
  display_order: 3,
  source: "seed",
  merchant_count: 12,
};
const cities = {
  total_merchants: 3,
  countries: [
    {
      code: "KR",
      name: "韓國",
      merchant_count: 3,
      cities: [{ id: "seoul", name: "首爾", country_code: "KR", merchant_count: 3, area_count: 4 }],
    },
  ],
};
const euljiro = { "zh-TW": "乙支路", "zh-CN": "乙支路", en: "Euljiro", ja: "乙支路", ko: "을지로" };

function fillNames(values: Record<string, string>) {
  for (const [locale, value] of Object.entries(values)) {
    fireEvent.change(screen.getByLabelText(`${locale} 名稱`), { target: { value } });
  }
}

describe("AdminFoodAreasPanel", () => {
  it("lists areas, creates one with five names, and batch deactivates", async () => {
    const posts: Array<{ url: string; body: unknown }> = [];
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (url.includes("/foods/cities")) return new Response(JSON.stringify(cities));
        if (init?.method === "POST") {
          posts.push({ url, body: JSON.parse(String(init.body)) });
          const payload = url.includes("/batch")
            ? { updated: 1, status: "deactivate" }
            : { ...area, id: "area-2", slug: "seoul-euljiro", names: euljiro };
          return new Response(JSON.stringify(payload), { status: 201 });
        }
        return new Response(JSON.stringify({ items: [area], total: 1, page: 1, pages: 1 }));
      }),
    );

    render(<AdminFoodAreasPanel />);
    expect(await screen.findByText("明洞")).toBeTruthy();
    expect(screen.getByText("3 間店家")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "新增區域" }));
    const dialog = screen.getByRole("dialog");
    fireEvent.change(within(dialog).getByLabelText("Slug"), {
      target: { value: "seoul-euljiro" },
    });
    const destination = within(dialog).getByLabelText("所屬城市");
    await waitFor(() => expect(destination.querySelectorAll("option").length).toBe(2));
    fireEvent.change(destination, { target: { value: "seoul" } });
    fillNames(euljiro);
    fireEvent.change(screen.getByLabelText("排序"), { target: { value: "5" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存區域" }));

    expect(await screen.findByText("區域已新增")).toBeTruthy();
    expect(posts[0].url).toContain("/admin/foods/areas");
    expect(posts[0].body).toEqual({
      slug: "seoul-euljiro",
      destination_id: "seoul",
      names: euljiro,
      match_terms: [],
      latitude: null,
      longitude: null,
      display_order: 5,
      is_active: true,
    });

    fireEvent.click(screen.getByRole("checkbox", { name: "選取 明洞" }));
    fireEvent.click(screen.getByRole("button", { name: "停用" }));
    expect(await screen.findByText("已更新 1 個區域")).toBeTruthy();
    expect(posts[1].url).toContain("/admin/foods/areas/batch");
    expect(posts[1].body).toEqual({ ids: ["area-1"], action: "deactivate" });
  });
});

describe("AdminFoodCategoriesPanel", () => {
  it("creates a cuisine with five names", async () => {
    const posts: Array<{ url: string; body: unknown }> = [];
    vi.stubGlobal(
      "fetch",
      vi.fn(async (input: RequestInfo | URL, init?: RequestInit) => {
        const url = String(input);
        if (init?.method === "POST") {
          posts.push({ url, body: JSON.parse(String(init.body)) });
          return new Response(JSON.stringify({ ...category, id: "cat-2", slug: "izakaya" }), {
            status: 201,
          });
        }
        return new Response(JSON.stringify({ items: [category], total: 1, page: 1, pages: 1 }));
      }),
    );

    render(<AdminFoodCategoriesPanel />);
    expect(await screen.findByText("拉麵")).toBeTruthy();
    expect(screen.getByText("12 間店家")).toBeTruthy();

    fireEvent.click(screen.getByRole("button", { name: "新增分類" }));
    fireEvent.change(screen.getByLabelText("Slug"), { target: { value: "izakaya" } });
    fillNames({ "zh-TW": "居酒屋", "zh-CN": "居酒屋", en: "Izakaya", ja: "居酒屋", ko: "이자카야" });
    fireEvent.change(screen.getByLabelText("排序"), { target: { value: "20" } });
    fireEvent.click(screen.getByRole("button", { name: "儲存分類" }));

    expect(await screen.findByText("分類已新增")).toBeTruthy();
    expect(posts[0].url).toContain("/admin/foods/categories");
    expect(posts[0].body).toEqual({
      slug: "izakaya",
      names: { "zh-TW": "居酒屋", "zh-CN": "居酒屋", en: "Izakaya", ja: "居酒屋", ko: "이자카야" },
      display_order: 20,
      is_active: true,
    });
  });
});
