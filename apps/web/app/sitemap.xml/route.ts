import { NextResponse } from "next/server";
import { guideSitemapSummary } from "@/lib/guides.server";
import { siteUrl } from "@/lib/seo";
import { listedSitemapChildren, sitemapChildPath } from "../sitemaps/sitemap";

/**
 * `/sitemap.xml` is a sitemap index: one child for the static routes and, per section and
 * locale, one child per `SITEMAP_CHILD_LIMIT` articles for the articles and their topic
 * hubs (`app/sitemaps/sitemap.ts`, `generateSitemaps`, served at
 * `/sitemaps/sitemap/<id>.xml`). Nothing here caps a section: a sixth thousand rows means a
 * second child, listed the next time a crawler asks.
 *
 * Next writes the children but never an index, and it refuses a `sitemap.ts` beside a
 * `sitemap.xml/route.ts` as the same route declared twice -- so this handler is what keeps
 * the address `robots.ts`, `/llms.txt` and Search Console already know, and the children
 * live one folder down. Same
 * request-time evaluation as the children: the public switches and the publication picture
 * are read when a crawler asks, not while building without the API.
 *
 * A child is listed only while something is published under it, from the same summary the
 * static child's hub rule reads; an empty child would be a valid but pointless file. When
 * the summary cannot be read every child is listed, because an outage is not an empty
 * section, and a child that then answers with no rows costs one fetch rather than a hidden
 * section.
 */
export const dynamic = "force-dynamic";

const escape = (value: string) => value.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");

export async function GET(): Promise<NextResponse> {
  const children = listedSitemapChildren(await guideSitemapSummary());
  const body = [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<sitemapindex xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
    ...children.map((id) => `  <sitemap><loc>${escape(`${siteUrl}${sitemapChildPath(id)}`)}</loc></sitemap>`),
    "</sitemapindex>",
    "",
  ].join("\n");
  return new NextResponse(body, {
    headers: {
      "Content-Type": "application/xml; charset=utf-8",
      // The same freshness the children's generated handler declares: a crawler always
      // re-asks, and a child added by the first article in a new language shows up at once.
      "Cache-Control": "max-age=0, must-revalidate",
    },
  });
}
