import { describe, expect, it, vi, beforeEach } from "vitest";

const { slot, incoming, original, redirect } = vi.hoisted(() => ({
  slot: vi.fn(),
  incoming: vi.fn(),
  original: vi.fn(),
  redirect: vi.fn((url: string) => { throw new Error(`redirect:${url}`); }),
}));
vi.mock("@/lib/adsense.server", () => ({ getAdsenseSlot: slot }));
vi.mock("next/headers", () => ({ headers: incoming }));
vi.mock("next/navigation", () => ({ redirect }));
vi.mock("@/app/[locale]/layout", () => ({ default: original, generateMetadata: vi.fn(), generateStaticParams: vi.fn() }));
import AdsPublicLayout from "./layout";
import { disabledAdsense } from "@/lib/adsense";

const enabled = { enabled: true, publisher_id: "ca-pub-4140966684432854", slot_id: "1234567890", cmp_enabled: false };
const params = Promise.resolve({ locale: "zh-TW" });

describe("the article document root", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    slot.mockResolvedValue(enabled);
    incoming.mockResolvedValue(new Headers({ "x-travel-pathname": "/zh-TW/guides/howto/tokyo-esim" }));
    original.mockImplementation(() => null);
  });

  it("hands the ordinary layout nothing of its own when advertising is off", async () => {
    slot.mockResolvedValue(disabledAdsense);
    await AdsPublicLayout({ children: <p>Article</p>, params });
    // Byte-for-byte today's page: the boundary exists, the behaviour does not change.
    expect(original).toHaveBeenCalledTimes(1);
    expect(original.mock.calls[0][0].ads).toBeUndefined();
    expect(redirect).not.toHaveBeenCalled();
  });

  it("passes the configuration through when advertising is on", async () => {
    await AdsPublicLayout({ children: <p>Article</p>, params });
    expect(original.mock.calls[0][0].ads).toEqual(enabled);
  });

  it("strips a query string before the ad tag can read location.href", async () => {
    incoming.mockResolvedValue(new Headers({ "x-travel-pathname": "/zh-TW/life/ai-notes?utm_campaign=private" }));
    await expect(AdsPublicLayout({ children: <p>Article</p>, params }))
      .rejects.toThrow("redirect:/zh-TW/life/ai-notes");
    expect(original).not.toHaveBeenCalled();
  });

  it("leaves the query alone when advertising is off, since no vendor can read it", async () => {
    slot.mockResolvedValue(disabledAdsense);
    incoming.mockResolvedValue(new Headers({ "x-travel-pathname": "/zh-TW/life/ai-notes?topic=ai" }));
    await AdsPublicLayout({ children: <p>Article</p>, params });
    expect(redirect).not.toHaveBeenCalled();
    expect(original).toHaveBeenCalledTimes(1);
  });
});
