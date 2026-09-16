import { describe, expect, it, vi } from "vitest";
import { guideSitemapSummary } from "@/lib/guides.server";
import { siteUrl } from "@/lib/seo";
import { SITEMAP_CHILDREN } from "../sitemaps/sitemap";
import { dynamic, GET } from "./route";

// The summary is stubbed; the slice size the children are cut by stays the real constant.
vi.mock("@/lib/guides.server", async (original) => ({
  ...await original<typeof import("@/lib/guides.server")>(), guideSitemapSummary: vi.fn(),
}));

const children = (xml: string) =>
  [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((match) => new URL(match[1]).pathname);

describe("/sitemap.xml, the index", () => {
  it("is a sitemap index of the children that have something, read at request time", async () => {
    expect(dynamic).toBe("force-dynamic");
    vi.mocked(guideSitemapSummary).mockResolvedValue({
      counts: [
        { kind: "intel", locale: "zh-TW", count: 2 },
        { kind: "howto", locale: "en", count: 1 },
        { kind: "life", locale: "zh-TW", count: 40 },
        { kind: "life", locale: "ko", count: 0 },
      ],
      available: true,
    });
    const response = await GET();
    expect(response.headers.get("content-type")).toContain("application/xml");
    expect(response.headers.get("cache-control")).toBe("max-age=0, must-revalidate");
    const xml = await response.text();
    expect(xml.startsWith('<?xml version="1.0" encoding="UTF-8"?>\n<sitemapindex')).toBe(true);
    expect(xml).not.toContain("<urlset");
    // The static child always; a section child only where a kind of it publishes.
    expect(children(xml)).toEqual([
      "/sitemaps/sitemap/static.xml", "/sitemaps/sitemap/travel-en.xml",
      "/sitemaps/sitemap/travel-zh-TW.xml", "/sitemaps/sitemap/life-zh-TW.xml",
    ]);
    for (const loc of xml.matchAll(/<loc>([^<]+)<\/loc>/g)) expect(loc[1].startsWith(`${siteUrl}/`)).toBe(true);
  });

  it("lists a numbered child per further 5,000 rows, so a section that outgrows one file gets a second at once", async () => {
    vi.mocked(guideSitemapSummary).mockResolvedValue({
      counts: [
        { kind: "life", locale: "zh-TW", count: 5_001 },
        { kind: "howto", locale: "en", count: 5_000 },
      ],
      available: true,
    });
    expect(children(await (await GET()).text())).toEqual([
      "/sitemaps/sitemap/static.xml", "/sitemaps/sitemap/travel-en.xml",
      "/sitemaps/sitemap/life-zh-TW.xml", "/sitemaps/sitemap/life-zh-TW-2.xml",
    ]);
  });

  it("lists every child when the summary cannot be read, because an outage is not an empty section", async () => {
    vi.mocked(guideSitemapSummary).mockResolvedValue({ counts: [], available: false });
    const xml = await (await GET()).text();
    expect(children(xml)).toEqual(SITEMAP_CHILDREN.map((id) => `/sitemaps/sitemap/${id}.xml`));
  });

  it("lists only the static child when nothing at all is published", async () => {
    vi.mocked(guideSitemapSummary).mockResolvedValue({ counts: [], available: true });
    expect(children(await (await GET()).text())).toEqual(["/sitemaps/sitemap/static.xml"]);
  });
});
