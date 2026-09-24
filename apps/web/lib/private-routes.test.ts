import { afterEach, describe, expect, it } from "vitest";
import { hasThirdPartyScript, isPrivateRoute } from "./private-routes";
import { TRAVELPAYOUTS_DRIVE_SCRIPT_URL } from "./travelpayouts-drive";

describe("isPrivateRoute", () => {
  it.each([
    "/zh-TW/share/AbCdEfGhIjKlMnOpQrStUv",
    "/en/trips",
    "/ja/trips/550e8400-e29b-41d4-a716-446655440000",
    "/zh-TW/admin/users",
    "/zh-TW/account",
    "/ko/my",
    "/zh-CN/alerts",
    "/zh-TW/login",
    "/zh-TW/register",
    "/zh-TW/forgot-password",
    "/zh-TW/line/link",
    "/zh-TW/share-target",
    "/trips",
  ])("%s is private", (pathname) => {
    expect(isPrivateRoute(pathname)).toBe(true);
  });

  it.each([
    "/zh-TW",
    "/zh-TW/life/n8n-ai-automation-guide",
    "/en/guides/howto/tokyo-where-to-stay-first-trip",
    "/zh-TW/destinations/tokyo",
    "/zh-TW/hotspots",
    // A section name inside a slug or as a prefix of another word is not that section.
    "/zh-TW/life/share-your-trip-with-friends",
    "/zh-TW/tripsy",
    "/zh-TW/myths",
  ])("%s is public", (pathname) => {
    expect(isPrivateRoute(pathname)).toBe(false);
  });
});

describe("hasThirdPartyScript", () => {
  afterEach(() => {
    document.querySelectorAll("script").forEach((script) => script.remove());
  });

  function addScript(src: string) {
    const script = document.createElement("script");
    script.src = src;
    document.body.append(script);
  }

  it("sees Travelpayouts Drive and gtag.js, and nothing else", () => {
    addScript("/_next/static/chunks/app.js");
    addScript("https://emrldtp.cc.example.com/fake.js");
    expect(hasThirdPartyScript()).toBe(false);
    addScript(TRAVELPAYOUTS_DRIVE_SCRIPT_URL);
    expect(hasThirdPartyScript()).toBe(true);
  });

  it("sees GA4's tag", () => {
    addScript("https://www.googletagmanager.com/gtag/js?id=G-ABCD1234");
    expect(hasThirdPartyScript()).toBe(true);
  });
});
