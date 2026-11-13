import { NextResponse } from "next/server";
import { loadRecentNewsSitemap, renderNewsSitemapXml } from "@/lib/news-sitemap";

/**
 * `/sitemap-news.xml` -- standalone Google News Sitemap for stories published in the last 48 hours.
 *
 * Kept separate from `/sitemap.xml` so regular evergreen coverage reports and URL-count assertions
 * stay untouched while Search Console and news crawlers get a dedicated 48-hour news feed.
 */
export const dynamic = "force-dynamic";

export async function GET(): Promise<NextResponse> {
  const { available, entries } = await loadRecentNewsSitemap();
  if (!available) {
    return new NextResponse("news sitemap temporarily unavailable", {
      status: 503,
      headers: { "Retry-After": "600", "Content-Type": "text/plain; charset=utf-8" },
    });
  }

  return new NextResponse(renderNewsSitemapXml(entries), {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "max-age=0, must-revalidate",
    },
  });
}
