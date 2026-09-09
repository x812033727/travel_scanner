import { describe, expect, it } from "vitest";
import { disabledStay22Script, isOriginalHotelUrl, isSafeStay22Referrer, isStay22LmaId, isStay22ScriptOrigin, privacyBlocksStay22, validStay22ScriptConfig } from "./stay22-script";
import { stay22ScriptCopy } from "./stay22-script-copy";
const STAY22_SCRIPT_LMA_ID = "6aa15a455ff1d17f658d1692";

describe("Stay22 public script policy", () => {
  it("only accepts the HTTPS project production origins", () => {
    expect(isStay22ScriptOrigin("https://mokaair.com/path")).toBe(true);
    expect(isStay22ScriptOrigin("https://www.mokaair.com")).toBe(true);
    for (const origin of ["http://mokaair.com", "http://localhost:3000", "https://preview.mokaair.com", "https://mokaair.com.evil.test", "https://user:pass@mokaair.com", "invalid"]) expect(isStay22ScriptOrigin(origin)).toBe(false);
  });
  it("requires a validated script identity and effective script mode", () => {
    expect(validStay22ScriptConfig(disabledStay22Script)).toBe(true);
    expect(validStay22ScriptConfig({ enabled: true, integration_mode: "script", lma_id: STAY22_SCRIPT_LMA_ID })).toBe(true);
    expect(isStay22LmaId("6aa15a455ff1d17f658d1693")).toBe(true);
    for (const value of [null, {}, { enabled: "true" }, { enabled: true, integration_mode: "allez", lma_id: STAY22_SCRIPT_LMA_ID }, { enabled: true, integration_mode: "script", lma_id: "different" }]) expect(validStay22ScriptConfig(value)).toBe(false);
  });
  it("respects privacy opt-out and excludes already-wrapped or unsafe links", () => {
    expect(privacyBlocksStay22({ doNotTrack: "1" })).toBe(true);
    expect(privacyBlocksStay22({ globalPrivacyControl: true })).toBe(true);
    expect(privacyBlocksStay22({ doNotTrack: "0" })).toBe(false);
    expect(isOriginalHotelUrl("https://www.booking.com/hotel/jp/example.html")).toBe(true);
    for (const url of ["javascript:alert(1)", "http://example.com", "https://stay22.com/allez/booking", "https://www.stay22.com/allez/booking", "https://user:pass@booking.com/hotel/x", "https://booking.com/hotel/x?aid=1", "https://booking.com/hotel/x#private"]) expect(isOriginalHotelUrl(url)).toBe(false);
  });
  it("allows only empty or exact-origin clean public referrers", () => {
    for (const referrer of ["", "https://mokaair.com/", "https://mokaair.com/zh-TW", "https://mokaair.com/en/destinations/tokyo/services"]) expect(isSafeStay22Referrer(referrer, "https://mokaair.com")).toBe(true);
    for (const referrer of ["https://mokaair.com/zh-TW/trips/private-id", "https://mokaair.com/zh-TW/account", "https://mokaair.com/zh-TW/admin", "https://mokaair.com/zh-TW?secret=1", "https://mokaair.com/en/destinations/tokyo/services?trip=private", "https://mokaair.com/zh-TW#private", "https://www.mokaair.com/zh-TW", "https://other.example/", "https://user:pass@mokaair.com/", "not-a-url"]) expect(isSafeStay22Referrer(referrer, "https://mokaair.com")).toBe(false);
  });
  it.each(["en", "zh-TW", "zh-CN", "ja", "ko"])("supplies every public-copy field in %s", (locale) => {
    const copy = stay22ScriptCopy(locale);
    expect(Object.keys(copy).sort()).toEqual(Object.keys(stay22ScriptCopy("en")).sort());
    expect(Object.values(copy).every((text) => text.trim().length > 0)).toBe(true);
    expect(copy.disclosure).toContain("Stay22");
    expect(copy.disclosure).toContain("Spark");
    expect(copy.disclosure).toContain("Nova");
  });
});
