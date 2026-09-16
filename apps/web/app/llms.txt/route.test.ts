import { beforeEach, describe, expect, it, vi } from "vitest";
import metadata from "@/messages/en/metadata.json";
import { locales } from "@/i18n/routing";
import { getDestinations } from "@/lib/destinations.server";
import { getDiscoveryStatus } from "@/lib/discovery-status.server";
import type { GuideTopic } from "@/lib/guides";
import { getGuideTopics, getSeriesIndex } from "@/lib/guides.server";
import { siteUrl } from "@/lib/seo";
import { closedSiteVisibility, openSiteVisibility } from "@/lib/site-features";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { GET, dynamic } from "./route";

/**
 * The real English catalogue, not `vitest.setup.tsx`'s.
 *
 * That shared mock carries zh-TW only, ignores the `locale` it is handed, and has no
 * `metadata` namespace at all -- so every annotation below would come back as its own key
 * ("guidesTitle"), and the assertions about stripping the brand suffix would pass without
 * ever seeing one. This route is the one place that asks for a locale other than the
 * reader's, so it has to resolve messages itself to be tested at all.
 */
vi.mock("next-intl/server", () => ({
  getTranslations: async ({ locale, namespace }: { locale: string; namespace: string }) => {
    if (locale !== "en" || namespace !== "metadata") throw new Error(`unexpected ${locale}/${namespace}`);
    return (key: string) => (metadata as Record<string, string>)[key] ?? key;
  },
}));

vi.mock("@/lib/site-visibility.server", () => ({ getSiteVisibility: vi.fn() }));
vi.mock("@/lib/discovery-status.server", () => ({ getDiscoveryStatus: vi.fn() }));
vi.mock("@/lib/destinations.server", () => ({ getDestinations: vi.fn() }));
// The topic vocabulary and the series registry, stubbed; the rest of the module is real.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(), getGuideTopics: vi.fn(), getSeriesIndex: vi.fn(),
}));
// `SITEMAP_ROUTES` comes from `app/sitemap.ts`, which imports the community module, and that one
// starts with `import "server-only"` -- a package only Next's own build resolves. Nothing here
// calls it, but Vite still has to resolve the import; app/sitemap.test.ts mocks it the same way.
vi.mock("@/lib/community/server", () => ({ getCommunityState: vi.fn() }));

const summary = (id: string, city: string, reason: string) => ({
  id, city, reason,
  localName: null, englishName: null, country: "Japan", countryCode: "JP",
  role: "primary" as const, parentDestinationId: null, extensionIds: [], areas: [],
  recommendedDays: null, timezone: "Asia/Tokyo", currency: "JPY", center: null,
});

async function body(): Promise<string> {
  return await (await GET()).text();
}

describe("llms.txt", () => {
  beforeEach(() => {
    vi.mocked(getSiteVisibility).mockReset().mockResolvedValue({ status: "ready", features: openSiteVisibility });
    vi.mocked(getDiscoveryStatus).mockReset().mockResolvedValue({ enabled: false });
    vi.mocked(getDestinations).mockReset().mockResolvedValue([
      summary("tokyo", "Tokyo", "Dense and legible for a first trip to Japan."),
    ]);
    vi.mocked(getGuideTopics).mockReset().mockResolvedValue([]);
    vi.mocked(getSeriesIndex).mockReset().mockResolvedValue([]);
  });

  it("is read per request, like the sitemap that reads the same switches", () => {
    expect(dynamic).toBe("force-dynamic");
  });

  it("serves plain text that a browser will show rather than download", async () => {
    const response = await GET();
    expect(response.headers.get("Content-Type")).toBe("text/plain; charset=utf-8");
    // The switches below are read no-store; caching the document that reports them would put
    // the two back out of step.
    expect(response.headers.get("Cache-Control")).toBe("no-store");
  });

  it("opens with the heading and blockquote the convention specifies", async () => {
    const lines = (await body()).split("\n");
    expect(lines[0]).toBe("# Mokaair");
    expect(lines[2].startsWith("> ")).toBe(true);
  });

  it("points at the sitemap as the complete list rather than claiming to be one", async () => {
    const text = await body();
    expect(text).toContain(`${siteUrl}/sitemap.xml`);
    expect(text).toContain(`${siteUrl}/robots.txt`);
  });

  it("annotates a destination with the catalogue's own reason", async () => {
    expect(await body()).toContain(
      `- [Tokyo](${siteUrl}/en/destinations/tokyo): Dense and legible for a first trip to Japan.`,
    );
  });

  it("keeps a destination listed, unannotated, when the catalogue read fails", async () => {
    vi.mocked(getDestinations).mockResolvedValue(null);
    const text = await body();
    // The page is still there; we just cannot say what it is this second. Dropping the section
    // would be a worse answer than a bare link.
    expect(text).toContain(`- [tokyo](${siteUrl}/en/destinations/tokyo)`);
    expect(text).not.toContain("Dense and legible");
  });

  it("lists every language's home page", async () => {
    const text = await body();
    for (const locale of locales) expect(text).toContain(`(${siteUrl}/${locale})`);
  });

  it("leaves out a page whose feature switch is closed, rather than listing it", async () => {
    vi.mocked(getSiteVisibility).mockResolvedValue({ status: "ready", features: closedSiteVisibility });
    const text = await body();
    // A link here is a page that answers today. `noindex` behind a closed switch means the
    // sitemap drops it too, and the two files must not disagree.
    expect(text).not.toContain(`${siteUrl}/en/hotspots`);
    expect(text).not.toContain(`${siteUrl}/en/pricing`);
    // /foods carries no switch, so it survives a full close.
    expect(text).toContain(`${siteUrl}/en/foods`);
  });

  it("lists /explore only while discovery is on", async () => {
    expect(await body()).not.toContain(`${siteUrl}/en/explore`);
    vi.mocked(getDiscoveryStatus).mockResolvedValue({ enabled: true });
    expect(await body()).toContain(`${siteUrl}/en/explore`);
  });

  it("names the guides and lifestyle hubs, which carry no switch", async () => {
    const text = await body();
    expect(text).toContain(`- [Travel intel and guides](${siteUrl}/en/guides): ${metadata.guidesDescription}`);
    expect(text).toContain(`- [Lifestyle](${siteUrl}/en/life): ${metadata.lifeDescription}`);
  });

  it("lists each top-level topic where its articles are, and every series hub once", async () => {
    vi.mocked(getGuideTopics).mockImplementation(async (_locale, section): Promise<GuideTopic[]> => section === "life"
      ? [
        { slug: "ai", label: "AI tools", section: "life", parent: null, description: "Tools, terms and news.", count: 2, counts: { en: 2, "zh-TW": 500 } },
        { slug: "ai-terms", label: "AI glossary", section: "life", parent: "ai", count: 0, counts: { "zh-TW": 80 } },
        { slug: "misc", label: "Miscellany", section: "life", parent: null, count: 0, counts: {} },
      ]
      : [{ slug: "transport", label: "Transport", section: "travel", parent: null, count: 3, counts: { en: 3, ja: 3 } }]);
    vi.mocked(getSeriesIndex).mockImplementation(async (locale) => locale === "zh-TW"
      ? [
        { slug: "claude-code", section: "life", hub: { kind: "life", slug: "claude-code-tutorials", title: "Claude Code 教學中心", description: "從安裝到進階" }, source: "api-series", topic: "claude-code", entries: 96 },
        { slug: "ai-terms", section: "life", hub: { kind: "life", slug: "ai-terms-index", title: "AI 名詞總索引" }, source: "catalogue", topic: "ai-terms", entries: null },
      ]
      : locale === "en" ? [{ slug: "ai-terms", section: "life", hub: { kind: "life", slug: "ai-terms-index", title: "AI glossary index" }, source: "catalogue", topic: "ai-terms", entries: null }] : []);
    const text = await body();
    // The hub in the language with the most under it; a sub-topic is not a line of its own;
    // a topic with nothing anywhere is left out.
    expect(text).toContain(`- [AI tools](${siteUrl}/zh-TW/life/topics/ai): 500 articles in 繁體中文: Tools, terms and news.`);
    // English wins a tie.
    expect(text).toContain(`- [Transport](${siteUrl}/en/guides/topics/transport): 3 articles in English`);
    expect(text).not.toContain("AI glossary](");
    expect(text).not.toContain("Miscellany");
    // Each hub once, under the first language (English first) that publishes it.
    expect(text).toContain(`- [AI glossary index](${siteUrl}/en/life/ai-terms-index): English`);
    expect(text).not.toContain("AI 名詞總索引");
    expect(text).toContain(`- [Claude Code 教學中心](${siteUrl}/zh-TW/life/claude-code-tutorials): 96 lessons, 繁體中文, 從安裝到進階`);
    expect(text.indexOf("### Topics")).toBeLessThan(text.indexOf("### Series"));
  });

  it("leaves the topic and series sub-sections out when the API answers nothing, keeping the hubs", async () => {
    const text = await body();
    expect(text).not.toContain("### Topics");
    expect(text).not.toContain("### Series");
    expect(text).toContain(`- [Travel intel and guides](${siteUrl}/en/guides)`);
  });

  it("strips the brand suffix the page titles need and a list label does not", async () => {
    const text = await body();
    // The catalogue really does carry it, so this is not passing on an unresolved key.
    expect(metadata.guidesTitle).toContain("| Mokaair");
    expect(text).not.toContain("| Mokaair");
  });

  it("answers in one language, the one x-default points at", async () => {
    const text = await body();
    expect(text).toContain(metadata.destinationsDescription.replace(" | Mokaair", ""));
  });
});
