import { useState } from "react";
import { cleanup, fireEvent, render, screen } from "@testing-library/react";
import { afterEach, beforeEach, expect, it, vi } from "vitest";
import { SiteVisibilityProvider } from "@/components/site-visibility-provider";
import { openSiteVisibility } from "@/lib/site-features";
import type { CatalogPlace } from "@/lib/community/types";
import { PlacePicker, RelatedPlaces } from "./places";

const mock = vi.hoisted(() => ({ api: vi.fn() }));
vi.mock("@/lib/api", async (original) => ({ ...await original<typeof import("@/lib/api")>(), api: mock.api }));
vi.mock("@/components/header-session", () => ({ useHeaderSession: () => ({ user: { id: "member" } }) }));
const places: CatalogPlace[] = [
  { id: "pet", kind: "pet_place", name: "Dog cafe", names: { "zh-TW": "狗狗咖啡" }, destination: "Tokyo", href: "/pet-friendly/pet" },
  { id: "spot", kind: "hotspot", name: "Museum", destination: "Tokyo", href: "/hotspots?hotspot=spot" },
  { id: "merchant", kind: "merchant", name: "Restaurant", destination: "Tokyo", href: "/foods?merchant=merchant" },
];
beforeEach(() => mock.api.mockReset());
afterEach(cleanup);
function Picker({ initial = [] }: { initial?: CatalogPlace[] }) {
  const [value, setValue] = useState(initial);
  return <PlacePicker value={value} onChange={setValue} />;
}

it("searches typed catalog places, prevents duplicates and keeps selections after a failed search", async () => {
  mock.api.mockResolvedValueOnce({ items: places }).mockRejectedValueOnce(new Error("offline"))
    .mockResolvedValueOnce({ items: [] });
  render(<Picker />);
  fireEvent.change(screen.getByLabelText("搜尋關聯地點"), { target: { value: "Tokyo" } });
  fireEvent.keyDown(screen.getByLabelText("搜尋關聯地點"), { key: "Enter" });
  fireEvent.click(await screen.findByRole("button", { name: "加入 Dog cafe" }));
  expect(screen.getByRole("button", { name: "加入 Dog cafe" }).hasAttribute("disabled")).toBe(true);
  expect(screen.getByRole("button", { name: "移除 狗狗咖啡" })).toBeTruthy();
  fireEvent.change(screen.getByLabelText("搜尋關聯地點"), { target: { value: "Kyoto" } });
  fireEvent.click(screen.getByRole("button", { name: "搜尋" }));
  await screen.findByRole("alert");
  expect(screen.getByRole("button", { name: "移除 狗狗咖啡" })).toBeTruthy();
  fireEvent.click(screen.getByRole("button", { name: "重試" }));
  await screen.findByText("沒有符合的結果。");
  fireEvent.click(screen.getByRole("button", { name: "移除 狗狗咖啡" }));
  expect(screen.queryByRole("button", { name: "移除 狗狗咖啡" })).toBeNull();
  expect(mock.api.mock.calls[0][0]).toBe("/community/search/places?q=Tokyo&locale=zh-TW");
});

it("enforces the twenty-place UI limit and hides closed hotspot entry points", async () => {
  mock.api.mockResolvedValue({ items: places });
  const selected = Array.from({ length: 20 }, (_, index) => ({ ...places[0], id: String(index) }));
  const view = render(<Picker initial={selected} />);
  fireEvent.click(screen.getByRole("button", { name: "搜尋" }));
  expect((await screen.findByRole("button", { name: "加入 Restaurant" })).hasAttribute("disabled")).toBe(true);
  view.rerender(<SiteVisibilityProvider state={{ status: "ready", features: { ...openSiteVisibility, hotspots_enabled: false } }}>
    <RelatedPlaces places={places} />
  </SiteVisibilityProvider>);
  expect(screen.queryByRole("link", { name: "Museum" })).toBeNull();
  expect(screen.getByRole("link", { name: "狗狗咖啡" }).getAttribute("href")).toBe("/pet-friendly/pet");
  expect(screen.getByRole("link", { name: "Restaurant" }).getAttribute("href")).toBe("/foods?merchant=merchant");
});
