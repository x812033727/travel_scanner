import { describe, expect, it } from "vitest";
import { reservationPlatformDefinitions, reservationPlatformHref, reservationPlatformIdentity } from "./reservation-platforms";

// URL-shape fixtures, not evidence of merchant approval or live availability.
const platformUrls = [
  ["tablecheck", "https://www.tablecheck.com/en/shops/sushi-sakai/reserve"],
  ["catchtable_global", "https://www.catchtable.net/shop/example"],
  ["eztable", "https://www.eztable.com/restaurant/example"],
  ["chope", "https://www.chope.co/singapore-restaurants/restaurant/song-fa"],
  ["openrice", "https://www.openrice.com/en/hongkong/p-yat-lok-p23206360"],
  ["hungry_hub", "https://web.hungryhub.com/en/restaurants/krua-apsorn/web"],
  ["pasgo", "https://pasgo.vn/nha-hang/example"],
  ["inline", "https://inline.app/booking/-Np4PbmnyNDdeWIZzRem:inline-live-3/-Np4PbzfZuNZ-afLExLd?language=zh-tw"],
  ["maifood", "https://reservation.maifood.com.tw/qingtian76/qingtian76_1"],
  ["sevenrooms", "https://www.sevenrooms.com/reservations/palmbeach"],
  ["ikyu", "https://restaurant.ikyu.com/107953"],
  ["myconcierge", "https://myconciergejapan.com/restaurants/ginza-kyubey"],
  ["tabelog", "https://tabelog.com/osaka/A2701/A270202/27001289"],
  ["hotpepper", "https://www.hotpepper.jp/strJ003560255"],
  ["gurunavi", "https://r.gnavi.co.jp/k001100"],
  ["autoreserve", "https://autoreserve.com/ja/restaurants/91FxEE6JLr2HE2owrKVL"],
  ["naver_booking", "https://booking.naver.com/booking/13/bizes/210459"],
] as const;

describe("reservation platforms", () => {
  it("exposes each known provider exactly once in a fixed order", () => {
    expect(reservationPlatformDefinitions.map((item) => item.provider)).toEqual(platformUrls.map(([provider]) => provider));
    expect(new Set(reservationPlatformDefinitions.map((item) => item.provider)).size).toBe(17);
  });

  it.each(platformUrls)("accepts the merchant-specific %s URL without dropping its identity", (provider, url) => {
    expect(reservationPlatformHref(provider, url)).toBe(url);
    expect(reservationPlatformIdentity(provider, url)).toBeTruthy();
  });

  it.each(["en", "ja", "ko", "zh-TW", "zh-CN"])("preserves dotted Catchtable venue identity in %s", (locale) => {
    // Format regression fixtures, not approval of unresearched language alternates.
    const url = `https://www.catchtable.net/${locale}/shop/yosukgung.kr`;
    expect(reservationPlatformHref("catchtable_global", url)).toBe(url);
    expect(reservationPlatformIdentity("catchtable_global", url)).toBe("catchtable_global:yosukgung.kr");
    expect(reservationPlatformIdentity("catchtable_global", url)).toBe(
      reservationPlatformIdentity("catchtable_global", "https://catchtable.net/restaurants/yosukgung.kr/"),
    );
  });

  it.each(["normal.brunch", "venue_1.branch-2.kr", "hani._.noodle"])("accepts Catchtable dot-separated ASCII IDs: %s", (id) => {
    const url = `https://www.catchtable.net/shop/${id}`;
    expect(reservationPlatformHref("catchtable_global", url)).toBe(url);
    expect(reservationPlatformIdentity("catchtable_global", url)).toBe(`catchtable_global:${id}`);
  });

  it("never drops a Catchtable dotted suffix when comparing branches", () => {
    const identities = ["yosukgung.kr", "yosukgung.jp", "yosukgung", "yosukgungkr"].map((id) =>
      reservationPlatformIdentity("catchtable_global", `https://www.catchtable.net/shop/${id}`));
    expect(identities.every(Boolean)).toBe(true);
    expect(new Set(identities).size).toBe(4);
  });

  it.each([
    ".", "..", ".venue", "venue.", "venue..kr", "venue...kr", "venue.-kr", "_venue.kr",
    "yosukgung%2ekr", "yosukgung%2Ekr", "yosukgung%252ekr", "%2e", ".%2e", "%2e%2e",
    "yosukgung.kr/..", "yosukgung.kr/../other", "../yosukgung.kr", "yosukgung.kr/.",
    "yosukgung.kr%2fother", "yosukgung.kr%5cother", "yosukgung.kr\\other",
    "yosukgung.kr%00", "yosukgung.kr%0a", "yosukgung.kr%7f", "yosukgung．kr", "yosukgung.Kr",
  ])("rejects unsafe or unsupported dotted Catchtable IDs: %s", (id) => {
    const url = `https://www.catchtable.net/zh-TW/shop/${id}`;
    expect(reservationPlatformHref("catchtable_global", url)).toBeUndefined();
    expect(reservationPlatformIdentity("catchtable_global", url)).toBeUndefined();
  });

  it.each([
    "http://www.catchtable.net/zh-TW/shop/yosukgung.kr",
    "https://www.catchtable.net.evil.test/zh-TW/shop/yosukgung.kr",
    "https://www.catchtable.net@evil.test/zh-TW/shop/yosukgung.kr",
    "https://user@www.catchtable.net/zh-TW/shop/yosukgung.kr",
    "https://www.catchtable.net:443/zh-TW/shop/yosukgung.kr",
    "https://127.0.0.1/zh-TW/shop/yosukgung.kr",
    "https://[::1]/zh-TW/shop/yosukgung.kr",
    "https://www.catchtable.net/zh-TW/shop/yosukgung.kr?redirect=https://evil.test",
    "https://www.catchtable.net/zh-TW/shop/yosukgung.kr#other",
  ])("retains authority and redirect guards with dotted IDs: %s", (url) => {
    expect(reservationPlatformHref("catchtable_global", url)).toBeUndefined();
    expect(reservationPlatformIdentity("catchtable_global", url)).toBeUndefined();
  });

  it.each([
    ["tablecheck", "https://www.tablecheck.com/en/shops/venue.kr/reserve"],
    ["eztable", "https://www.eztable.com/restaurant/venue.kr"],
    ["chope", "https://www.chope.co/singapore-restaurants/restaurant/venue.kr"],
    ["openrice", "https://www.openrice.com/en/hongkong/r-venue.kr-r123"],
    ["hungry_hub", "https://web.hungryhub.com/en/restaurants/venue.kr"],
    ["pasgo", "https://pasgo.vn/nha-hang/venue.kr"],
    ["inline", "https://inline.app/booking/company:live/venue.kr"],
    ["maifood", "https://reservation.maifood.com.tw/company/venue.kr"],
    ["sevenrooms", "https://www.sevenrooms.com/reservations/venue.kr"],
    ["ikyu", "https://restaurant.ikyu.com/123.456"],
    ["myconcierge", "https://myconciergejapan.com/restaurants/venue.kr"],
  ])("does not widen %s IDs when allowing Catchtable dots", (provider, url) => {
    expect(reservationPlatformHref(provider, url)).toBeUndefined();
  });

  it.each([
    ["tablecheck", "https://www.tablecheck.com/shops/sushi-sakai/reserve"],
    ["tablecheck", "https://www.tablecheck.com/zh-TW/sushi-sakai/reserve/message"],
    ["tablecheck", "https://www.tablecheck.com/en/sushi-sakai/reserve/landing"],
    ["catchtable_global", "https://catchtable.net/ko/restaurants/example"],
    ["eztable", "https://eztable.com/zh-TW/restaurants/1234"],
    ["hungry_hub", "https://hungryhub.com/restaurants/krua-apsorn"],
    ["sevenrooms", "https://www.sevenrooms.com/explore/candlenutsingapore/reservations/create/search"],
    ["myconcierge", "https://myconciergejapan.com/ja/restaurants/ginza-kyubey"],
    ["openrice", "https://www.openrice.com/zh-HK/hongkong/r-%E9%8F%9E%E8%A8%98-r23206360"],
  ])("recognizes documented alternate %s merchant page shapes", (provider, url) => {
    expect(reservationPlatformHref(provider, url)).toBe(url);
  });

  it.each([
    ["tabelog", "https://tabelog.com/en/tokyo/A1301/A130101/13226719", "tabelog:13226719"],
    ["tabelog", "https://tabelog.com/tw/tokyo/A1301/A130101/13226719", "tabelog:13226719"],
    ["tabelog", "https://tabelog.com/kr/tokyo/A1301/A130101/13226719", "tabelog:13226719"],
    ["gurunavi", "https://gurunavi.com/en/k001100/rst", "gurunavi:k001100"],
    ["gurunavi", "https://gurunavi.com/zh-hant/k001100/rst", "gurunavi:k001100"],
    ["gurunavi", "https://r.gnavi.co.jp/nmwubfx70000", "gurunavi:nmwubfx70000"],
    ["autoreserve", "https://autoreserve.com/zh-tw/restaurants/91FxEE6JLr2HE2owrKVL", "autoreserve:91FxEE6JLr2HE2owrKVL"],
    ["naver_booking", "https://m.booking.naver.com/booking/13/bizes/210459", "naver_booking:210459"],
  ])("keeps one branch identity across %s language and host variants", (provider, url, identity) => {
    expect(reservationPlatformHref(provider, url)).toBe(url);
    expect(reservationPlatformIdentity(provider, url)).toBe(identity);
  });

  it.each([
    // Area, ranking and review routes are not one shop.
    ["tabelog", "https://tabelog.com/osaka/A2701/A270202"],
    ["tabelog", "https://tabelog.com/tokyo/rstLst/RC0101"],
    ["tabelog", "https://tabelog.com/en/tokyo/A1301/A130101/13226719/dtlrvwlst"],
    ["tabelog", "https://tabelog.com/en/tokyo/A1301/A130101/1322671a"],
    // Tabelog has no Hong Kong directory; a site locale is not a Tabelog locale.
    ["tabelog", "https://tabelog.com/hk/tokyo/A1301/A130101/13226719"],
    ["tabelog", "https://tabelog.com/zh-tw/tokyo/A1301/A130101/13226719"],
    ["hotpepper", "https://www.hotpepper.jp/strJ00356025"],
    ["hotpepper", "https://www.hotpepper.jp/strJ003560255/yoyaku"],
    ["hotpepper", "https://www.hotpepper.jp/fukuoka"],
    ["gurunavi", "https://r.gnavi.co.jp/area"],
    ["gurunavi", "https://r.gnavi.co.jp/plan/r6pyrfvf0000/plan-reserve"],
    // Each Gurunavi route belongs to one host only.
    ["gurunavi", "https://r.gnavi.co.jp/en/k001100/rst"],
    ["gurunavi", "https://gurunavi.com/k001100/rst"],
    ["gurunavi", "https://gurunavi.com/en/k001100"],
    ["autoreserve", "https://autoreserve.com/ja/restaurants/91FxEE6JLr2HE2owrKV"],
    ["autoreserve", "https://autoreserve.com/restaurants/91FxEE6JLr2HE2owrKVL"],
    ["autoreserve", "https://autoreserve.com/ja/areas/osaka"],
    ["naver_booking", "https://booking.naver.com/booking/13/bizes"],
    ["naver_booking", "https://booking.naver.com/booking/13/bizes/210459/items/4567"],
    // Naver's map entry is a place page, not the reservation platform.
    ["naver_booking", "https://map.naver.com/p/entry/place/210459"],
  ])("rejects the %s page that is not one shop: %s", (provider, url) => {
    expect(reservationPlatformHref(provider, url)).toBeUndefined();
    expect(reservationPlatformIdentity(provider, url)).toBeUndefined();
  });

  it.each(platformUrls)("normalizes host casing and a trailing slash for %s", (provider, url) => {
    const parsed = new URL(url);
    const variant = `HTTPS://${parsed.host.toUpperCase()}${parsed.pathname}/${parsed.search}`;
    expect(reservationPlatformHref(provider, variant)).toBe(url);
  });

  it.each([
    ["tablecheck", "https://tablecheck.com/ja/sushi-sakai/reserve/message", "https://www.tablecheck.com/en/shops/sushi-sakai/reserve/"],
    ["catchtable_global", "https://catchtable.net/ko/shop/venue", "https://www.catchtable.net/en/restaurants/venue"],
    ["eztable", "https://eztable.com/zh-TW/restaurant/1234", "https://www.eztable.com/en/restaurants/1234"],
    ["chope", "https://chope.co/en/singapore-restaurants/restaurant/venue", "https://www.chope.co/zh-TW/singapore-restaurants/restaurant/venue"],
    ["openrice", "https://openrice.com/en/hongkong/r-venue-r1234", "https://www.openrice.com/zh-HK/hongkong/r-%E9%A4%90%E5%BB%B3-r1234"],
    ["hungry_hub", "https://web.hungryhub.com/en/restaurants/venue/web", "https://hungryhub.com/th/restaurants/venue"],
    ["inline", "https://inline.app/booking/-chain:live/-branch?language=zh-tw", "https://inline.app/booking/-chain:live/-branch?language=en"],
    ["sevenrooms", "https://sevenrooms.com/reservations/venue", "https://www.sevenrooms.com/explore/venue/reservations/create/search"],
    ["myconcierge", "https://myconciergejapan.com/restaurants/venue/", "https://www.myconciergejapan.com/ja/restaurants/venue"],
  ])("keeps the same %s venue identity across locales and accepted URL variants", (provider, first, second) => {
    expect(reservationPlatformIdentity(provider, first)).toBeTruthy();
    expect(reservationPlatformIdentity(provider, first)).toBe(reservationPlatformIdentity(provider, second));
  });

  it.each([
    ["tablecheck", "https://tablecheck.com/en/shops/venue/reserve", "https://tablecheck.com/ja/shops/other/reserve"],
    ["inline", "https://inline.app/booking/-chain:live/-branch", "https://inline.app/booking/-chain:live/-other"],
    ["inline", "https://inline.app/booking/-chain:live/-branch", "https://inline.app/booking/-other:live/-branch"],
    ["maifood", "https://reservation.maifood.com.tw/brand/branch_1", "https://reservation.maifood.com.tw/brand/branch_2"],
    ["openrice", "https://openrice.com/en/hongkong/r-venue-r1234", "https://openrice.com/en/macau/r-venue-r1234"],
    ["chope", "https://chope.co/singapore-restaurants/restaurant/venue", "https://chope.co/bangkok-restaurants/restaurant/venue"],
    ["sevenrooms", "https://sevenrooms.com/reservations/venue", "https://sevenrooms.com/reservations/other"],
    ["ikyu", "https://restaurant.ikyu.com/107953", "https://restaurant.ikyu.com/107954"],
  ])("does not conflate different %s branches or regions", (provider, first, second) => {
    expect(reservationPlatformIdentity(provider, first)).toBeTruthy();
    expect(reservationPlatformIdentity(provider, second)).toBeTruthy();
    expect(reservationPlatformIdentity(provider, first)).not.toBe(reservationPlatformIdentity(provider, second));
  });

  it.each(platformUrls)("rejects unsafe authority, traversal and hidden redirects for %s", (provider, url) => {
    const parsed = new URL(url);
    const base = `https://${parsed.host}`;
    const path = parsed.pathname;
    const attacks = [
      url.replace("https:", "http:"), `//${parsed.host}${path}`,
      `https://user:pass@${parsed.host}${path}`, `https://@${parsed.host}${path}`,
      `https://${parsed.host}:443${path}`, `https://${parsed.host}:8443${path}`,
      `https://${parsed.host}.${path}`, `https://${parsed.host}.evil.example${path}`,
      `https://${parsed.host}%2eevil.example${path}`, `https://${parsed.host}\\@evil.example${path}`,
      `https://127.0.0.1${path}`, `https://[::1]${path}`, `https://localhost${path}`,
      ` ${url}`, `${url}\t`, `${base}/\n${path.slice(1)}`,
      `${base}/discard/..${path}`, `${base}/.%2e${path}`, `${base}/%2e%2e${path}`,
      `${base}/.%252e${path}`, `${base}/%2f${path}`, `${base}/%5c${path}`,
      `${base}/%00${path}`, `${base}/%0a${path}`, `${base}/%7f${path}`,
      `${base}/%C2%85${path}`, `${base}/%FF${path}`, `${base}/%ZZ${path}`,
      `${base}/${path}`, `${base}${path}//`, `${base}${path}?redirect=https://evil.example`,
      `${base}${path}?venue=other`, `${base}${path}#other`, `${base}${path}#`,
    ];
    for (const attack of attacks) {
      expect(reservationPlatformHref(provider, attack), attack).toBeUndefined();
      expect(reservationPlatformIdentity(provider, attack), attack).toBeUndefined();
    }
  });

  it.each([
    ["tablecheck", "/en/shops/search/reserve"], ["tablecheck", "/random/shops/venue/reserve"],
    ["tablecheck", "/en/venue/reserve"], ["tablecheck", "/en/venue/reserve/pay"],
    ["catchtable_global", "/search/shop/venue"], ["catchtable_global", "/shop/venue/unrecognized"],
    ["eztable", "/restaurants/search"], ["chope", "/restaurant/venue"],
    ["openrice", "/en/hongkong/r-query1234"], ["openrice", "/en/hongkong/restaurants"],
    ["hungry_hub", "/en/restaurants/venue/payment"], ["pasgo", "/nha-hang/search"],
    ["inline", "/booking/chain/branch"], ["inline", "/booking/-chain:live"],
    ["maifood", "/branches"], ["maifood", "/brand/branches"], ["maifood", "/brand/search"],
    ["sevenrooms", "/explore/search"], ["sevenrooms", "/explore/venue/reservations"],
    ["ikyu", "/restaurants/107953"], ["ikyu", "/search"],
    ["myconcierge", "/restaurants/search"], ["myconcierge", "/restaurants/venue/book"],
  ])("rejects fuzzy or discovery-shaped %s paths: %s", (provider, path) => {
    const host = reservationPlatformDefinitions.find((item) => item.provider === provider)!.hosts[0];
    expect(reservationPlatformHref(provider, `https://${host}${path}`)).toBeUndefined();
  });

  it.each(reservationPlatformDefinitions)("does not expose $label homepages or generic owner forms", ({ provider, hosts }) => {
    for (const path of ["", "/", "/en", "/search", "/discovery", "/restaurants", "/owner/form/venue"]) {
      expect(reservationPlatformHref(provider, `https://${hosts[0]}${path}`)).toBeUndefined();
    }
  });

  it.each(["unknown", "owner_form", "__proto__", "constructor", "toString", "hasOwnProperty"])("rejects unknown or inherited provider keys: %s", (provider) => {
    expect(reservationPlatformHref(provider, platformUrls[0][1])).toBeUndefined();
    expect(reservationPlatformIdentity(provider, platformUrls[0][1])).toBeUndefined();
  });

  it.each(["Kyoto", "İstanbul", "ıstanbul", "ſushi"])("rejects Unicode lookalikes in ASCII-only restaurant slugs: %s", (slug) => {
    expect(reservationPlatformHref("tablecheck", `https://tablecheck.com/en/shops/${slug}/reserve`)).toBeUndefined();
    expect(reservationPlatformHref("tablecheck", `https://tablecheck.com/en/shops/${encodeURIComponent(slug)}/reserve`)).toBeUndefined();
  });

  it.each(["language=xx", "LANGUAGE=en", "language=en&language=ja", "language=en&redirect=https://evil.example", "language=%65n", "language=en%0a", "locale=en", "branch=other", ""])("only accepts one documented Inline language parameter: %s", (query) => {
    expect(reservationPlatformHref("inline", `https://inline.app/booking/-chain:live/-branch?${query}`)).toBeUndefined();
  });

  it("does not infer a valid URL from missing input", () => {
    expect(reservationPlatformHref("tablecheck", undefined)).toBeUndefined();
    expect(reservationPlatformHref("tablecheck", null)).toBeUndefined();
    expect(reservationPlatformHref("tablecheck", "")).toBeUndefined();
  });
});
