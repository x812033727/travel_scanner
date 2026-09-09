import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
const { incoming } = vi.hoisted(() => ({ incoming: vi.fn() }));
vi.mock("next/headers", () => ({ headers: incoming }));
import { loadStay22ScriptConfig } from "./stay22-script.server";
import { disabledStay22Script } from "./stay22-script";

const STAY22_SCRIPT_LMA_ID = "6aa15a455ff1d17f658d1692";
const enabled = { enabled: true, integration_mode: "script", lma_id: STAY22_SCRIPT_LMA_ID };
describe("public server script configuration", () => {
  beforeEach(() => {
    vi.stubEnv("NEXT_PUBLIC_SITE_URL", "https://mokaair.com");
    vi.stubEnv("API_INTERNAL_URL", "http://api.internal:8000");
    incoming.mockResolvedValue(new Headers({ host: "mokaair.com", "x-travel-pathname": "/zh-TW/destinations/tokyo/services", cookie: "private=session", authorization: "Bearer private" }));
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue(new Response(JSON.stringify(enabled))));
  });
  afterEach(() => { vi.unstubAllGlobals(); vi.unstubAllEnvs(); vi.clearAllMocks(); });
  it("fetches only bounded public config without forwarding credentials", async () => {
    expect(await loadStay22ScriptConfig()).toEqual(enabled);
    const [url, init] = vi.mocked(fetch).mock.calls[0];
    expect(url).toBe("http://api.internal:8000/api/v1/travel-services/stay22-script-config");
    expect(init?.headers).toEqual({ Accept: "application/json" });
    expect(init?.cache).toBe("no-store");
    expect(init?.signal).toBeInstanceOf(AbortSignal);
  });
  it.each([{ host: "localhost:3000" }, { host: "mokaair.com", dnt: "1" }, { host: "mokaair.com", "sec-gpc": "1" }])("does not fetch for opt-out or local headers %j", async (values) => {
    incoming.mockResolvedValue(new Headers(Object.entries(values).filter((entry): entry is [string, string] => typeof entry[1] === "string")));
    expect(await loadStay22ScriptConfig()).toEqual(disabledStay22Script);
    expect(fetch).not.toHaveBeenCalled();
  });
  it("does not fetch for preview hostname even with a production site URL", async () => {
    incoming.mockResolvedValue(new Headers({ host: "preview.mokaair.com" }));
    expect(await loadStay22ScriptConfig()).toEqual(disabledStay22Script);
    expect(fetch).not.toHaveBeenCalled();
  });
  it.each(["tour", "transfer", "esim", "all", "hotel&type=tour"])("preserves original non-hotel catalogue for %s", async (kind) => {
    incoming.mockResolvedValue(new Headers({ host: "mokaair.com", "x-travel-pathname": `/zh-TW/destinations/tokyo/services?type=${kind}` }));
    expect(await loadStay22ScriptConfig()).toEqual(disabledStay22Script);
    expect(fetch).not.toHaveBeenCalled();
  });
  it("allows the hotel view while the root removes URL conditions before SDK load", async () => {
    incoming.mockResolvedValue(new Headers({ host: "mokaair.com", "x-travel-pathname": "/zh-TW/destinations/tokyo/services?type=hotel&start_date=2027-01-01" }));
    expect(await loadStay22ScriptConfig()).toEqual(enabled);
    expect(fetch).toHaveBeenCalledTimes(1);
  });
  it.each(["fukuoka", "singapore", "bangkok", "invalid"])("preserves non-catalogue destination %s", async (destination) => {
    incoming.mockResolvedValue(new Headers({ host: "mokaair.com", "x-travel-pathname": `/zh-TW/destinations/${destination}/services` }));
    expect(await loadStay22ScriptConfig()).toEqual(disabledStay22Script);
    expect(fetch).not.toHaveBeenCalled();
  });
  it("allows the combined Osaka and Kyoto hotel catalogue", async () => {
    incoming.mockResolvedValue(new Headers({ host: "mokaair.com", "x-travel-pathname": "/zh-TW/destinations/osaka-kyoto/services" }));
    expect(await loadStay22ScriptConfig()).toEqual(enabled);
  });
  it.each(["status", "invalid", "network"])("fails off for %s", async (failure) => {
    if (failure === "network") vi.mocked(fetch).mockRejectedValue(new Error("unavailable"));
    else vi.mocked(fetch).mockResolvedValue(new Response(failure === "invalid" ? "{}" : "unavailable", { status: failure === "status" ? 503 : 200 }));
    expect(await loadStay22ScriptConfig()).toEqual(disabledStay22Script);
  });
});
