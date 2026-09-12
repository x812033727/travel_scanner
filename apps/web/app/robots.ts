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
/**
 * Crawlers that collect pages to train on, or to resell as an answer, rather than to send
 * a reader back here. Refusing them costs nothing we want: `Google-Extended` and
 * `Applebot-Extended` are training-only tokens that Googlebot and Applebot do not consult
 * when crawling or ranking, so search is unaffected. `ChatGPT-User` and `OAI-SearchBot` are
 * deliberately absent -- those fetch on a person's behalf and cite where the answer came
 * from, which is the same bargain a search engine offers.
 *
 * This is a declaration, not a defence: it stops the crawlers honest enough to read it.
 * Volume from the rest is the per-source read limit's problem, and that one does not care
 * what a request calls itself.
 */
const CONTENT_HARVESTERS = [
  "GPTBot",
  "ClaudeBot",
  "anthropic-ai",
  "CCBot",
  "Google-Extended",
  "Applebot-Extended",
  "Bytespider",
  "Amazonbot",
  "meta-externalagent",
  "PerplexityBot",
  "Diffbot",
];

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      // Keep this first. The rules are read positionally in tests and by eye; the group that
      // decides what an ordinary crawler may fetch is the one that belongs at the top.
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
      ...CONTENT_HARVESTERS.map((userAgent) => ({ userAgent, disallow: "/" })),
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
