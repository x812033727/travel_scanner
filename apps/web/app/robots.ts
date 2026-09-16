import type { MetadataRoute } from "next";
import { siteUrl } from "@/lib/seo";

// Rendered per request rather than at build time, so `AI_CRAWLER_POLICY` takes effect on the
// next fetch of robots.txt and needs no rebuild.
export const dynamic = "force-dynamic";


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
 * AI crawlers, in two groups, because they make two different bargains.
 *
 * The training crawlers collect pages to train on or to resell as an answer and send nobody
 * back here. Refusing them costs nothing we want: `Google-Extended` and `Applebot-Extended`
 * are training-only tokens that Googlebot and Applebot do not consult when crawling or
 * ranking, so search is unaffected.
 *
 * The search crawlers fetch to answer a question and cite where the answer came from --
 * the same bargain a search engine offers, and the one the site wants (docs/seo.md,
 * "AI crawlers", 2026-09-15). `ChatGPT-User` and `OAI-SearchBot` are not listed at all:
 * they fetch on a person's behalf and were never refused.
 *
 * `AI_CRAWLER_POLICY` (read per request, so a change needs no rebuild) picks the line:
 * `allow-search` (the default) refuses the training group only, `block` refuses both,
 * `allow` refuses neither. This is a declaration, not a defence: it stops the crawlers
 * honest enough to read it. Volume from the rest is the per-source read limit's problem,
 * and that one does not care what a request calls itself.
 */
export const TRAINING_CRAWLERS = [
  "GPTBot",
  "anthropic-ai",
  "CCBot",
  "Google-Extended",
  "Applebot-Extended",
  "Bytespider",
  "Amazonbot",
  "meta-externalagent",
  "Diffbot",
];

export const SEARCH_CRAWLERS = ["PerplexityBot", "ClaudeBot"];

export const AI_CRAWLER_POLICIES = ["block", "allow-search", "allow"] as const;
export type AiCrawlerPolicy = (typeof AI_CRAWLER_POLICIES)[number];
export const DEFAULT_AI_CRAWLER_POLICY: AiCrawlerPolicy = "allow-search";

export function aiCrawlerPolicy(value = process.env.AI_CRAWLER_POLICY): AiCrawlerPolicy {
  const chosen = (value ?? "").trim().toLowerCase();
  return (AI_CRAWLER_POLICIES as readonly string[]).includes(chosen)
    ? (chosen as AiCrawlerPolicy)
    : DEFAULT_AI_CRAWLER_POLICY;
}

/** The user agents the current policy refuses. */
export function refusedCrawlers(policy: AiCrawlerPolicy = aiCrawlerPolicy()): string[] {
  if (policy === "allow") return [];
  if (policy === "block") return [...TRAINING_CRAWLERS, ...SEARCH_CRAWLERS];
  return [...TRAINING_CRAWLERS];
}

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
      ...refusedCrawlers().map((userAgent) => ({ userAgent, disallow: "/" })),
    ],
    sitemap: `${siteUrl}/sitemap.xml`,
  };
}
