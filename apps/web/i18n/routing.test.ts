import { afterEach, describe, expect, it, vi } from "vitest";
import { defaultLocale, isLocale, normalizeLocale } from "./routing";

describe("locale cookie", () => {
  afterEach(() => { vi.unstubAllEnvs(); vi.resetModules(); });

  // `routing` is built once when the module loads, so each case loads a fresh copy.
  async function load(env: string) {
    vi.stubEnv("NODE_ENV", env);
    vi.resetModules();
    return import("./routing");
  }

  it("is Secure in production for next-intl and the browser writes alike", async () => {
    const { localeCookieAttributes, localeCookieString, routing } = await load("production");
    expect(localeCookieAttributes()).toEqual({ path: "/", maxAge: 31_536_000, sameSite: "lax", secure: true });
    expect(routing.localeCookie).toMatchObject({ name: "travel_locale", sameSite: "lax", secure: true });
    expect(localeCookieString("ja")).toBe("travel_locale=ja; path=/; max-age=31536000; samesite=lax; secure");
  });

  it("names no Secure attribute at all outside production", async () => {
    const { localeCookieAttributes, localeCookieString, routing } = await load("development");
    // next-intl's browser writer prints a boolean attribute's name even when it is false, so the
    // key itself has to be absent for a development server over plain HTTP to keep the cookie.
    expect(localeCookieAttributes()).not.toHaveProperty("secure");
    expect(routing.localeCookie).toMatchObject({ name: "travel_locale", sameSite: "lax" });
    expect(routing.localeCookie).not.toHaveProperty("secure");
    expect(localeCookieString("ja")).toBe("travel_locale=ja; path=/; max-age=31536000; samesite=lax");
  });
});

describe("locale routing", () => {
  it.each([
    ["en-US", "en"],
    ["ja-JP", "ja"],
    ["ko-KR", "ko"],
    ["zh-Hant", "zh-TW"],
    ["zh-HK", "zh-TW"],
    ["zh-MO", "zh-TW"],
    ["zh-Hans", "zh-CN"],
    ["zh-CN", "zh-CN"],
    ["zh-SG", "zh-CN"],
    ["fr-FR", "zh-TW"],
  ])("maps %s to %s", (input, expected) => {
    expect(normalizeLocale(input)).toBe(expected);
  });

  it("keeps the supported locale whitelist strict", () => {
    expect(defaultLocale).toBe("zh-TW");
    expect(isLocale("ko")).toBe(true);
    expect(isLocale("zh-Hant")).toBe(false);
  });
});
