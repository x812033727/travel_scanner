import { beforeEach, describe, expect, it, vi } from "vitest";

const { incoming, article, config } = vi.hoisted(() => ({
  incoming: vi.fn(), article: vi.fn(), config: vi.fn(),
}));
vi.mock("next/headers", () => ({ headers: incoming }));
vi.mock("./guides.server", () => ({ getGuideArticle: article }));
vi.mock("./adsense-config", () => ({ fetchAdsenseConfig: config }));

import { loadAdsenseSlot } from "./adsense.server";
import { disabledAdsense } from "./adsense";

const enabled = {
  enabled: true, publisher_id: "ca-pub-4140966684432854", slot_id: "1234567890", cmp_enabled: false,
};
const published = { status: "published", document: { title: "東京 eSIM 怎麼選" } };
const articlePath = "/zh-TW/guides/howto/tokyo-esim";

function request(overrides: Record<string, string> = {}) {
  return new Headers({ host: "mokaair.com", "x-travel-pathname": articlePath, ...overrides });
}

describe("deciding whether this response may carry an ad", () => {
  beforeEach(() => {
    vi.clearAllMocks();
    incoming.mockResolvedValue(request());
    config.mockResolvedValue(enabled);
    article.mockResolvedValue(published);
  });

  it("serves a published article", async () => {
    expect(await loadAdsenseSlot()).toEqual(enabled);
    expect(article).toHaveBeenCalledWith("howto", "tokyo-esim", "zh-TW");
  });

  it.each([
    ["unavailable", { status: "unavailable", document: null }],
    ["not translated into this locale", { status: "unpublished", document: null }],
    ["published elsewhere but with no document here", { status: "published", document: null }],
  ])("refuses an article that is %s", async (_label, state) => {
    article.mockResolvedValue(state);
    // These render the "article unavailable" screen. Advertising on a no-content screen is
    // what Google's policies forbid, and the layout decides before the page gets to say so —
    // so the layout has to ask, or the tag loads on a page with nothing on it.
    expect(await loadAdsenseSlot()).toEqual(disabledAdsense);
  });

  it("never asks about the article when the request was already refused", async () => {
    incoming.mockResolvedValue(request({ "sec-gpc": "1" }));
    expect(await loadAdsenseSlot()).toEqual(disabledAdsense);
    expect(article).not.toHaveBeenCalled();
    expect(config).not.toHaveBeenCalled();
  });

  it("never asks about the article when advertising is switched off", async () => {
    config.mockResolvedValue(disabledAdsense);
    expect(await loadAdsenseSlot()).toEqual(disabledAdsense);
    // No point paying for a lookup whose answer cannot change the outcome.
    expect(article).not.toHaveBeenCalled();
  });

  it.each([
    ["DNT", { dnt: "1" }],
    ["GPC", { "sec-gpc": "1" }],
    ["a non-production host", { host: "localhost:3000" }],
    ["a hub rather than an article", { "x-travel-pathname": "/zh-TW/guides" }],
    ["a shared trip", { "x-travel-pathname": "/zh-TW/share/9f8e7d6c5b4a" }],
  ])("refuses %s", async (_label, headers) => {
    incoming.mockResolvedValue(request(headers));
    expect(await loadAdsenseSlot()).toEqual(disabledAdsense);
  });
});
