import { cleanup, render, screen } from "@testing-library/react";
import { NextIntlClientProvider } from "next-intl";
import { afterEach, describe, expect, it, vi } from "vitest";
import type { ReservationLink } from "@/lib/foods";
import en from "@/messages/en/foods.json";
import ja from "@/messages/ja/foods.json";
import ko from "@/messages/ko/foods.json";
import zhCN from "@/messages/zh-CN/foods.json";
import zhTW from "@/messages/zh-TW/foods.json";
import { MerchantExternalLinks } from "./merchant-external-links";

vi.unmock("next-intl");
afterEach(cleanup);

const catalogs = { en, ja, ko, "zh-TW": zhTW, "zh-CN": zhCN };
const google = {
  provider: "google", label: "Google Maps", primary: false,
  url: "https://www.google.com/maps/search/?api=1&query=Sushi%20Sakai&query_place_id=ChIJ-sakai",
};
const naver = {
  provider: "naver", label: "Naver Map", primary: true,
  url: "https://map.naver.com/p/entry/place/123456",
};
const platforms: ReservationLink[] = [
  { provider: "tablecheck", label: "TableCheck", url: "https://www.tablecheck.com/en/shops/sushi-sakai/reserve" },
  { provider: "catchtable_global", label: "Catchtable Global", url: "https://www.catchtable.net/shop/reviewed-branch" },
  { provider: "eztable", label: "EZTABLE", url: "https://www.eztable.com/restaurant/1234" },
  { provider: "chope", label: "Chope", url: "https://www.chope.co/singapore-restaurants/restaurant/reviewed-branch" },
  { provider: "openrice", label: "OpenRice", url: "https://www.openrice.com/en/hongkong/r-reviewed-branch-r12345" },
  { provider: "hungry_hub", label: "Hungry Hub", url: "https://web.hungryhub.com/en/restaurants/reviewed-branch" },
  { provider: "pasgo", label: "PasGo", url: "https://pasgo.vn/nha-hang/reviewed-branch-1234" },
  { provider: "inline", label: "inline", url: "https://inline.app/booking/-Np4PbmnyNDdeWIZzRem:inline-live-3/-Np4PbzfZuNZ-afLExLd?language=zh-tw" },
  { provider: "maifood", label: "Maifood", url: "https://reservation.maifood.com.tw/qingtian76/qingtian76_1" },
  { provider: "sevenrooms", label: "SevenRooms", url: "https://www.sevenrooms.com/explore/candlenutsingapore/reservations/create/search" },
  { provider: "ikyu", label: "一休", url: "https://restaurant.ikyu.com/107953" },
  { provider: "myconcierge", label: "My Concierge Japan", url: "https://myconciergejapan.com/restaurants/ginza-kyubey" },
].map((item) => ({ ...item, verified_at: "2026-09-08T00:00:00Z", language_code: "en" } satisfies ReservationLink));
const merchant = {
  name: "鮨さかい", map_links: [google, naver], reservation_links: platforms,
  official_website_url: "https://sushi-sakai.example/branch",
};

function renderLinks(overrides: Partial<typeof merchant> = {}, locale: keyof typeof catalogs = "zh-TW", compact = false) {
  return render(
    <NextIntlClientProvider locale={locale} messages={{ foods: catalogs[locale] }} timeZone="UTC">
      <MerchantExternalLinks merchant={{ ...merchant, ...overrides }} compact={compact} />
    </NextIntlClientProvider>,
  );
}

describe("MerchantExternalLinks", () => {
  it("keeps exact map identities, primary order, every verified reservation and a separate official site", () => {
    renderLinks();
    const links = screen.getAllByRole("link");
    expect(links.map((link) => link.getAttribute("href"))).toEqual([
      naver.url, google.url, ...platforms.map((item) => item.url), merchant.official_website_url,
    ]);
    for (const link of links) {
      expect(link.getAttribute("target")).toBe("_blank");
      expect(link.getAttribute("rel")).toBe("noopener noreferrer");
      expect(link.getAttribute("aria-label")).toContain("鮨さかい");
      expect(link.getAttribute("aria-label")).toContain("另開新分頁");
      expect(link.classList.contains("min-h-11")).toBe(true);
    }
    expect(screen.getByRole("link", { name: /TableCheck/ }).textContent).toBe("查看 TableCheck 訂位資訊");
    expect(screen.getByRole("link", { name: /官方網站/ }).textContent).toBe("官方網站");
    expect(screen.queryByText(zhTW.noVerifiedReservation)).toBeNull();
  });

  it("shows each verified provider once across duplicate locale URLs without modifying inputs", () => {
    const first = platforms[0];
    const alternate = { ...first, url: "https://www.tablecheck.com/ja/shops/sushi-sakai/reserve" };
    const originalMaps = [google, naver, naver];
    const originalReservations = [first, { ...first }, alternate];
    renderLinks({ map_links: originalMaps, reservation_links: originalReservations });
    expect(originalMaps).toEqual([google, naver, naver]);
    expect(originalReservations).toEqual([first, { ...first }, alternate]);
    expect(screen.getAllByRole("link", { name: /TableCheck/ })).toHaveLength(1);
    expect(screen.getAllByRole("link", { name: /Naver Map/ })).toHaveLength(1);
  });

  it("keeps all twelve providers in fixed order regardless of the response order or label", () => {
    renderLinks({ reservation_links: [...platforms].reverse().map((link) => ({ ...link, label: "Sponsored first" })) });
    expect(screen.getAllByRole("link").slice(2, -1).map((link) => link.getAttribute("href"))).toEqual(platforms.map((link) => link.url));
    expect(screen.queryByRole("link", { name: /Sponsored first/ })).toBeNull();
  });

  it("skips invalid duplicates before selecting a reviewed provider", () => {
    renderLinks({ reservation_links: [{ ...platforms[0], url: "https://www.tablecheck.com/en/search" }, platforms[0]] });
    expect(screen.getAllByRole("link", { name: /TableCheck/ })).toHaveLength(1);
    expect(screen.getByRole("link", { name: /TableCheck/ }).getAttribute("href")).toBe(platforms[0].url);
  });

  it.each(Object.keys(catalogs) as (keyof typeof catalogs)[])("exposes reviewed dotted Catchtable links safely in %s", (locale) => {
    const url = "https://www.catchtable.net/zh-TW/shop/yosukgung.kr";
    renderLinks({ reservation_links: [{ ...platforms[1], url, language_code: "zh-TW" }] }, locale);
    const anchor = screen.getByRole("link", { name: /Catchtable Global/ });
    expect(anchor.getAttribute("href")).toBe(url);
    expect(anchor.getAttribute("target")).toBe("_blank");
    expect(anchor.getAttribute("rel")).toBe("noopener noreferrer");
    expect(screen.queryByText(catalogs[locale].noVerifiedReservation)).toBeNull();
  });

  it.each([
    { url: "https://www.catchtable.net/zh-TW/shop/yosukgung.kr", verified_at: "" },
    { url: "https://www.catchtable.net/zh-TW/shop/yosukgung%2ekr" },
    { url: "https://www.catchtable.net/zh-TW/shop/yosukgung.kr/../other" },
    { url: "https://www.catchtable.net.evil.test/zh-TW/shop/yosukgung.kr" },
  ])("does not expose unreviewed or unsafe dotted Catchtable links: %o", (overrides) => {
    renderLinks({ reservation_links: [{ ...platforms[1], ...overrides }] });
    expect(screen.queryByRole("link", { name: /Catchtable Global/ })).toBeNull();
    expect(screen.getByText(zhTW.noVerifiedReservation)).toBeTruthy();
  });

  it.each([
    "javascript:alert(1)", "data:text/html,unsafe", "http://www.tablecheck.com/en/shops/sushi-sakai/reserve",
    "https://user:pass@www.tablecheck.com/en/shops/sushi-sakai/reserve",
    "https://www.tablecheck.com:8443/en/shops/sushi-sakai/reserve",
    "https://127.0.0.1/branch", "https://10.0.0.1/branch", "https://2130706433/branch",
    "https://[::1]/branch", "https://[::ffff:127.0.0.1]/branch", "https://localhost/branch",
    "https://host.local/branch", "https://host.internal/branch", "https://www.tablecheck.com/\nbranch",
    "https://www.tablecheck.com\\@localhost/branch", "//www.tablecheck.com/en/shops/sushi-sakai/reserve",
  ])("never exposes unsafe supplied map, reservation or official URLs: %s", (url) => {
    renderLinks({ map_links: [{ ...google, url }], reservation_links: [{ ...platforms[0], url }], official_website_url: url });
    expect(screen.queryAllByRole("link")).toHaveLength(0);
    expect(screen.getByText(zhTW.noVerifiedReservation)).toBeTruthy();
  });

  it.each([
    { provider: "unknown" }, { provider: "toString" }, { provider: "__proto__" }, { provider: "constructor" },
    { url: "https://www.tablecheck.com.evil.example/en/shops/sushi-sakai/reserve" },
    { url: "https://www.catchtable.net/shop/reviewed-branch" }, { url: "https://www.tablecheck.com/" },
    { url: "https://www.tablecheck.com/en" }, { url: "https://www.tablecheck.com/en/search" },
    { url: "https://www.tablecheck.com/en/shops/search" },
    { url: "https://www.tablecheck.com/en/shops/sushi-sakai/reserve?redirect=https://evil.example" },
    { url: "https://www.tablecheck.com:443/en/shops/sushi-sakai/reserve" },
    { url: "https://www.tablecheck.com/%2e%2e/en/shops/sushi-sakai/reserve" },
    { url: "https://www.tablecheck.com/en/shops/sushi%2fsakai/reserve" },
    { verified_at: "" }, { verified_at: "invalid" }, { label: "" },
  ])("omits invalid reservation metadata and does not offer a homepage fallback: %o", (overrides) => {
    renderLinks({ reservation_links: [{ ...platforms[0], ...overrides }] });
    expect(screen.queryByRole("link", { name: /TableCheck/ })).toBeNull();
    expect(screen.getByText(zhTW.noVerifiedReservation)).toBeTruthy();
    expect(screen.getAllByRole("link")).toHaveLength(3);
  });

  it("does not invent a source-language hint when metadata is empty or missing", () => {
    renderLinks({ reservation_links: [{ ...platforms[0], language_code: "" }, { ...platforms[1], language_code: undefined }] });
    expect(screen.queryByText(/平台頁面語言/)).toBeNull();
    expect(screen.getByRole("link", { name: /TableCheck/ })).toBeTruthy();
    expect(screen.getByRole("link", { name: /Catchtable Global/ })).toBeTruthy();
  });

  it("handles older responses without additive reservation, map or website fields", () => {
    render(
      <NextIntlClientProvider locale="zh-TW" messages={{ foods: zhTW }} timeZone="UTC">
        <MerchantExternalLinks merchant={{ name: merchant.name, map_links: [] }} />
      </NextIntlClientProvider>,
    );
    expect(screen.queryAllByRole("link")).toHaveLength(0);
    expect(screen.getByText(zhTW.noVerifiedReservation)).toBeTruthy();
  });

  it.each(Object.keys(catalogs) as (keyof typeof catalogs)[])("uses translated labels and names the source language in %s", (locale) => {
    const reservation = { ...platforms[6], language_code: "vi" };
    renderLinks({ reservation_links: [reservation] }, locale);
    const messages = catalogs[locale];
    const language = new Intl.DisplayNames([locale], { type: "language" }).of("vi")!;
    expect(screen.getByText(messages.reservationLanguage.replace("{language}", language))).toBeTruthy();
    const label = messages.reserveAt.replace("{name}", merchant.name).replace("{provider}", "PasGo");
    expect(screen.getByRole("link", { name: messages.externalLinkLabel.replace("{label}", label) }).getAttribute("href")).toBe(reservation.url);
  });

  it.each(["zh-TW", "zh-Hant", "zh-HK"])("does not falsely warn about the same written language: %s", (language_code) => {
    renderLinks({ reservation_links: [{ ...platforms[2], language_code }] });
    expect(screen.queryByText(/平台頁面語言/)).toBeNull();
  });

  it("distinguishes Chinese scripts and keeps invalid language metadata from crashing", () => {
    renderLinks({ reservation_links: [{ ...platforms[2], language_code: "zh-CN" }, { ...platforms[0], language_code: "invalid_language" }] });
    expect(screen.getAllByText(/平台頁面語言/)).toHaveLength(1);
    expect(screen.getByText(/中文（中國）/)).toBeTruthy();
    expect(screen.getByRole("link", { name: /TableCheck/ })).toBeTruthy();
  });

  it("stacks compact mobile actions and allows wrapping desktop actions with theme colors", () => {
    renderLinks({}, "zh-TW", true);
    const map = screen.getByRole("link", { name: /Naver Map/ });
    expect(map.parentElement?.classList.contains("flex-col")).toBe(true);
    expect(map.parentElement?.classList.contains("sm:flex-wrap")).toBe(true);
    expect(map.className).toContain("bg-[var(--surface)]");
    expect(map.className).toContain("text-[var(--ink)]");
  });
});
