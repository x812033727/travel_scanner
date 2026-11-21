import { NextResponse } from "next/server";
import { loadVideoSitemap, renderVideoSitemapXml } from "@/lib/video-sitemap";

/**
 * `/sitemap-videos.xml` -- standalone Google Video Sitemap for dedicated video watch pages.
 *
 * Returns 503 with Retry-After when the upstream API is unreachable so crawlers never mistake
 * an outage for a deleted video library.
 */
export const dynamic = "force-dynamic";

export async function GET(): Promise<NextResponse> {
  const { available, entries } = await loadVideoSitemap();
  if (!available) {
    return new NextResponse("video sitemap temporarily unavailable", {
      status: 503,
      headers: { "Retry-After": "600", "Content-Type": "text/plain; charset=utf-8" },
    });
  }

  return new NextResponse(renderVideoSitemapXml(entries), {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      "Cache-Control": "max-age=0, must-revalidate",
    },
  });
}
