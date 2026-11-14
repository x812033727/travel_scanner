import { cleanup, render, screen, within } from "@testing-library/react";
import { beforeEach, describe, expect, it, vi } from "vitest";
import DestinationsPage, { generateMetadata } from "./page";

const mocks = vi.hoisted(() => ({ getDestinations: vi.fn() }));
vi.mock("@/components/site-header", () => ({ SiteHeader: () => null }));
vi.mock("@/lib/destinations.server", () => ({ getDestinations: mocks.getDestinations }));

const tokyo = {
  id: "tokyo",
  city: "東京",
  localName: "東京",
  englishName: "Tokyo",
  country: "日本",
  countryCode: "JP",
  role: "primary" as const,
  parentDestinationId: null,
  extensionIds: [],
  areas: ["新宿", "上野／淺草", "東京站／銀座", "澀谷"],
  recommendedDays: { min: 4, max: 6 },
  timezone: "Asia/Tokyo",
  currency: "JPY",
  center: null,
  reason: "第一次去日本最容易排線的首都圈城市。",
};

const seoul = {
  id: "seoul",
  city: "首爾",
  localName: "서울",
  englishName: "Seoul",
  country: "韓國",
  countryCode: "KR",
  role: "primary" as const,
  parentDestinationId: null,
  extensionIds: [],
  areas: ["明洞", "弘大", "聖水"],
  recommendedDays: { min: 4, max: 6 },
  timezone: "Asia/Seoul",
  currency: "KRW",
  center: null,
  reason: "美食、逛街與地鐵動線成熟的韓國首站。",
};

beforeEach(() => {
  cleanup();
  vi.clearAllMocks();
  mocks.getDestinations.mockResolvedValue([tokyo, seoul]);
});

describe("the destinations index", () => {
  it("is indexable with localized metadata", async () => {
    const metadata = await generateMetadata({ params: Promise.resolve({ locale: "zh-TW" }) });
    expect(metadata.title).toBeTruthy();
    expect(metadata.description).toBeTruthy();
    expect(metadata.robots).toBeUndefined();
  });

  it("emits BreadcrumbList and ItemList JSON-LD alongside a visible breadcrumb trail", async () => {
    const { container } = render(await DestinationsPage({ params: Promise.resolve({ locale: "zh-TW" }) }));
    const graphs = [...container.querySelectorAll('script[type="application/ld+json"]')]
      .flatMap((node) => JSON.parse(node.textContent ?? "[]"));
    expect(graphs.map((graph) => graph["@type"])).toEqual(["BreadcrumbList", "ItemList"]);
    const list = graphs.find((graph) => graph["@type"] === "ItemList");
    expect(list.itemListElement.map((item: { url: string }) => item.url)).toEqual([
      "http://localhost:3000/zh-TW/destinations/tokyo",
      "http://localhost:3000/zh-TW/destinations/seoul",
    ]);

    const crumb = screen.getByRole("navigation", { name: "頁面路徑" });
    expect(within(crumb).getByRole("link", { name: "首頁" }).getAttribute("href")).toBe("/");
    expect(within(crumb).getByText("目的地").getAttribute("aria-current")).toBe("page");
  });

  it("renders country quick-jump anchors, suggested stay badges, and up to three area preview chips", async () => {
    const { container } = render(await DestinationsPage({ params: Promise.resolve({ locale: "zh-TW" }) }));

    const jumpNav = screen.getByTestId("destinations-country-nav");
    const jpJump = within(jumpNav).getByRole("link", { name: /日本/ });
    const krJump = within(jumpNav).getByRole("link", { name: /韓國/ });
    expect(jpJump.getAttribute("href")).toBe("#country-jp");
    expect(krJump.getAttribute("href")).toBe("#country-kr");
    expect(container.querySelector("section#country-jp")).not.toBeNull();
    expect(container.querySelector("section#country-kr")).not.toBeNull();

    const cards = screen.getAllByRole("listitem");
    expect(cards).toHaveLength(2);
    expect(within(cards[0]).getByRole("link", { name: "東京" }).getAttribute("href")).toBe("/destinations/tokyo");
    expect(within(cards[0]).getByText(/4–6/)).toBeTruthy();
    expect(within(cards[0]).getByText("新宿")).toBeTruthy();
    expect(within(cards[0]).getByText("上野／淺草")).toBeTruthy();
    expect(within(cards[0]).getByText("東京站／銀座")).toBeTruthy();
    expect(within(cards[0]).queryByText("澀谷")).toBeNull();
  });

  it("degrades to the localized offline seed catalog without leaking zh-TW area names into non-zh-TW locales", async () => {
    mocks.getDestinations.mockResolvedValueOnce(null);
    const { container } = render(await DestinationsPage({ params: Promise.resolve({ locale: "zh-TW" }) }));

    expect(screen.getByRole("heading", { level: 2, name: "日本" })).toBeTruthy();
    expect(screen.getByRole("link", { name: "東京" }).getAttribute("href")).toBe("/destinations/tokyo");
    expect(container.querySelector("section#country-jp")).not.toBeNull();
    expect(screen.getByText("新宿")).toBeTruthy();

    cleanup();
    mocks.getDestinations.mockResolvedValueOnce(null);
    render(await DestinationsPage({ params: Promise.resolve({ locale: "en" }) }));
    expect(screen.queryByText("新宿")).toBeNull();
  });
});
