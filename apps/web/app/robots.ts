import type { MetadataRoute } from "next";
import { siteUrl } from "@/lib/seo";


/**
 * Disallow is not a way to remove a page from an index: a blocked URL is never fetched, so the
 * crawler never reads its `noindex` and the page can persist as a URL-only result. So this list
 * holds only machine endpoints and unguessable token URLs, none of which were ever meant to be
 * indexed. Member pages (/login, /account, /trips, /alerts, /search, /my) are kept crawlable and
 * carry `noindex` instead, which is what actually removes them.
 *
 * /admin is in both places on purpose: it has no index entry to clear and blocking it at the
 * door saves crawl budget.
 *
 * Every route is locale-prefixed (`localePrefix: "always"`), so there is no unprefixed form to
 * match -- hence the `/*\/` wildcards, which Google and Bing both support.
 */
export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      {
        userAgent: "*",
        allow: "/",
        disallow: [
          "/api/",
          "/*/admin",
          "/*/out/",
          "/*/share/",
          "/*/share-target",
          "/*/line/",
          "/*/account/confirm",
        ],
      },
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
