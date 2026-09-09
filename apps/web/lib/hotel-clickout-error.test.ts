import { describe, expect, it } from "vitest";
import { hotelClickoutErrorPage } from "./hotel-clickout-error";
import { stay22AllezCopy } from "./stay22-allez-copy";

const path = "/api/travel/travel-services/1234/booking-options/5678/clickout";
const defaults = { requestUrl: `https://mokaair.test${path}?locale=ja&placement=trip`, referrer: "https://mokaair.test/ja/trips/abc?tab=stay", locale: "ja", status: 503, contentType: "application/x-www-form-urlencoded" };
const buffer = (value: string) => new TextEncoder().encode(value).buffer as ArrayBuffer;

describe("safe hotel clickout failure page", () => {
  it("keeps only bounded form fields and internal return link", async () => {
    const response = hotelClickoutErrorPage({ ...defaults, body: buffer("check_in=2030-11-01&check_out=2030-11-30&adults=2&children=1&aid=secret&link=https://evil.test") });
    const html = await response.text();
    expect(response.status).toBe(503);
    expect(response.headers.get("content-type")).toContain("text/html");
    expect(response.headers.get("cache-control")).toBe("no-store");
    expect(response.headers.get("referrer-policy")).toBe("same-origin");
    expect(response.headers.get("content-security-policy")).toContain("default-src 'none'");
    expect(html).toContain('value="2030-11-30"');
    expect(html).toContain('href="/ja/trips/abc?tab=stay"');
    expect(html).toContain(`action="${path}?locale=ja&amp;placement=trip&amp;return_to=`);
    expect(html).not.toMatch(/evil|secret|<script|<iframe/);
  });
  it.each(["https://evil.test/", "https://mokaair.test//evil.test", "javascript:alert(1)"])("never returns to %s", async (referrer) => {
    const html = await hotelClickoutErrorPage({ ...defaults, referrer }).text();
    expect(html).toContain('href="/ja"');
    expect(html).not.toContain('href="https:');
  });
  it("drops duplicate/unsafe fields and disallows an arbitrary action", async () => {
    const html = await hotelClickoutErrorPage({ ...defaults, requestUrl: "https://mokaair.test/api/delete", body: buffer("adults=2&adults=9&check_in=%22%3E%3Cscript%3E") }).text();
    expect(html).not.toContain("<form");
    expect(html).not.toContain("<script");
    expect(html).not.toContain('name="adults"');
  });
  it("retains a safe original page even with a no-referrer form", async () => {
    const html = await hotelClickoutErrorPage({ ...defaults, referrer: null,
      requestUrl: `${defaults.requestUrl}&return_to=${encodeURIComponent("/ja/trips/abc?tab=stay")}` }).text();
    expect(html).toContain('href="/ja/trips/abc?tab=stay"');
  });
  it.each(["zh-TW", "zh-CN", "en", "ja", "ko"])("localizes %s without upstream error leakage", async (locale) => {
    const html = await hotelClickoutErrorPage({ ...defaults, locale }).text();
    expect(html).toContain(stay22AllezCopy(locale).errorTitle);
    expect(html).toContain(`lang="${locale}"`);
  });
});
