import { isValidElement, type ReactNode } from "react";
import { describe, expect, it, vi, beforeEach } from "vitest";

const { slot, incoming, original } = vi.hoisted(() => ({
  slot: vi.fn(),
  incoming: vi.fn(),
  original: vi.fn(),
}));
vi.mock("@/lib/adsense.server", () => ({ getAdsenseSlot: slot }));
vi.mock("next/headers", () => ({ headers: incoming }));
vi.mock("@/app/[locale]/layout", () => ({ default: original, generateMetadata: vi.fn(), generateStaticParams: vi.fn() }));
import AdsPublicLayout from "./layout";
import { AdsenseDocument } from "@/components/ads/adsense-loader";
import { disabledAdsense } from "@/lib/adsense";

/** Whether the page was handed to the ordinary layout marked as living in an ad document. */
function markedAsAdDocument(children: ReactNode): boolean {
  return isValidElement(children) && children.type === AdsenseDocument;
}

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
    expect(markedAsAdDocument(original.mock.calls[0][0].children)).toBe(false);
  });

  it("passes the configuration through, and marks the document, when advertising is on", async () => {
    await AdsPublicLayout({ children: <p>Article</p>, params });
    expect(original.mock.calls[0][0].ads).toEqual(enabled);
    // Pages reached later by client-side navigation read this: the root layout is not
    // rendered again, so it is the only record of whether the tag is in the document.
    expect(markedAsAdDocument(original.mock.calls[0][0].children)).toBe(true);
  });

  it("serves a URL with a query string as it is, with no ad tag to read its tags", async () => {
    // It used to be redirected to the bare path, which threw away every utm_* tag before
    // analytics could read it. `adsenseRequestGate` refuses the request first; this is the
    // layout's own copy of the rule, checked with the gate out of the way.
    incoming.mockResolvedValue(new Headers({
      "x-travel-pathname": "/zh-TW/life/ai-notes?utm_source=youtube&utm_medium=video&utm_campaign=ai-notes",
    }));
    await AdsPublicLayout({ children: <p>Article</p>, params });
    expect(original).toHaveBeenCalledTimes(1);
    expect(original.mock.calls[0][0].ads).toBeUndefined();
    expect(markedAsAdDocument(original.mock.calls[0][0].children)).toBe(false);
  });

  it.each(["codex-learning-hub", "claude-code-tutorials"])(
    "keeps the %s filter URL and omits ads for the document lifetime",
    async (slug) => {
      incoming.mockResolvedValue(new Headers({
        "x-travel-pathname": `/zh-TW/life/${slug}?q=AGENTS.md&unit=D`,
      }));
      await AdsPublicLayout({ children: <p>Tutorial directory</p>, params });
      expect(original).toHaveBeenCalledTimes(1);
      expect(original.mock.calls[0][0].ads).toBeUndefined();
      expect(markedAsAdDocument(original.mock.calls[0][0].children)).toBe(false);
    },
  );

  it.each(["codex-learning-hub", "claude-code-tutorials"])(
    "keeps the %s directory ad-free on its clean URL as well",
    async (slug) => {
      incoming.mockResolvedValue(new Headers({ "x-travel-pathname": `/zh-TW/life/${slug}` }));
      await AdsPublicLayout({ children: <p>Tutorial directory</p>, params });
      expect(original.mock.calls[0][0].ads).toBeUndefined();
      expect(markedAsAdDocument(original.mock.calls[0][0].children)).toBe(false);
    },
  );
});
