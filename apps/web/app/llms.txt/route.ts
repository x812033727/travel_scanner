import { getTranslations } from "next-intl/server";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import { locales, localeLabels } from "@/i18n/routing";
import { getDestinations } from "@/lib/destinations.server";
import { getDiscoveryStatus } from "@/lib/discovery-status.server";
import { HREFLANG_DEFAULT, localeUrl, siteUrl } from "@/lib/seo";
import { featureEnabled } from "@/lib/site-features";
import { getSiteVisibility } from "@/lib/site-visibility.server";
import { SITEMAP_ROUTES } from "../sitemaps/sitemap";

/**
 * `/llms.txt` -- the short, annotated map of what this site authoritatively covers.
 *
 * The sitemap is the complete list and stays the one to crawl; it is hundreds of bare URLs with
 * no titles. This file is the other half: what each section *is*, in one line each, in the shape
 * llmstxt.org describes (an H1, a blockquote, then H2 sections of annotated links).
 *
 * What it is not: a promise. Three of the agents that advertise reading this file -- GPTBot,
 * ClaudeBot and PerplexityBot -- are refused in `app/robots.ts` and will never fetch it, and the
 * convention has no registered discovery directive. The readers it actually has are the agents
 * that fetch on a person's behalf and cite what they found (`ChatGPT-User`, `OAI-SearchBot`),
 * ordinary search crawlers, and tooling. That is worth one file; it is not worth reopening the
 * refusal list over, and a flat metric here is not evidence that it should be.
 *
 * Next has no file convention for this one, so it is a Route Handler in a dotted folder --
 * the pattern its own docs name ("app/rss.xml/route.ts creates a Route Handler for rss.xml").
 * `proxy.ts`'s matcher already excludes any path containing a dot, so next-intl never sees it
 * and no locale is inferred: everything below names its locale explicitly.
 */

// Same reason as `app/sitemap.ts`: read the public switches per request, not while building
// without the API. The Dockerfile's build stage has no API_INTERNAL_URL, so a prerendered file
// would be baked with no destinations at all until the next deploy.
export const dynamic = "force-dynamic";

/** The list labels read better without the brand the `<title>` needs. */
const plain = (value: string) => value.replace(/\s*\|\s*Mokaair$/, "");

/** `- [name](url): note`, the line shape llmstxt.org specifies. A note is optional; a link
 *  with nothing to say about it is still worth listing. */
function entry(name: string, url: string, note?: string | null): string {
  return note ? `- [${name}](${url}): ${note}` : `- [${name}](${url})`;
}

/**
 * The pages that are public *right now*.
 *
 * Reusing `SITEMAP_ROUTES` rather than restating the list is the whole point: the gating is
 * four feature switches plus the discovery switch, and a second file re-deriving "which pages
 * exist" would advertise a `noindex` page the first time a route changed on one side only.
 * A route module importing another route module is unusual here; drifting from the sitemap
 * would be worse, and `app/sitemap.test.ts` already treats this export as a shared constant.
 */
function openPaths(
  visibility: Awaited<ReturnType<typeof getSiteVisibility>>,
  discovery: Awaited<ReturnType<typeof getDiscoveryStatus>>,
): Set<string> {
  return new Set(
    SITEMAP_ROUTES
      .filter((route) => (!route.feature || featureEnabled(visibility, route.feature))
        && (!route.discovery || discovery.enabled))
      .map((route) => route.path),
  );
}

export async function GET(): Promise<Response> {
  const [visibility, discovery, t] = await Promise.all([
    getSiteVisibility(),
    getDiscoveryStatus(),
    getTranslations({ locale: HREFLANG_DEFAULT, namespace: "metadata" }),
  ]);
  // The catalogue read the destination index already makes. `null` on an outage, and the
  // section then lists the same URLs with no annotation rather than disappearing -- those
  // pages are still there, we just cannot say what they are this second.
  const catalogue = await getDestinations(HREFLANG_DEFAULT);
  const open = openPaths(visibility, discovery);
  const url = (path: string) => localeUrl(HREFLANG_DEFAULT, path);
  const lines: string[] = [
    "# Mokaair",
    "",
    `> ${plain(t("description"))} Every travel guide, intel notice and lifestyle article here is`,
    "> written first-party, and each one lists the sources it was checked against and the date",
    "> it was checked.",
    "",
    `- Every public page carries a language prefix: ${locales.map((locale) => `/${locale}`).join(", ")}.`,
    "- An article exists only in the languages it was genuinely published in; nothing here",
    "  advertises a translation that was never written.",
    "- A page behind a closed feature switch is left out of this file rather than listed, so a",
    "  link below is a page that answers today.",
    `- ${siteUrl}/sitemap.xml is the complete list and the one to crawl. This file is the map.`,
    "",
    "## Destinations",
    "",
    plain(t("destinationsDescription")),
    "",
  ];

  const byId = new Map((catalogue ?? []).map((row) => [row.id, row]));
  for (const id of PUBLIC_DESTINATIONS) {
    const row = byId.get(id);
    lines.push(entry(row?.city ?? id, url(`/destinations/${id}`), row?.reason ?? null));
  }

  lines.push("", "## Guides and lifestyle", "");
  for (const [path, title, note] of [
    ["/guides", "guidesTitle", "guidesDescription"],
    ["/life", "lifeTitle", "lifeDescription"],
  ] as const) {
    if (open.has(path)) lines.push(entry(plain(t(title)), url(path), plain(t(note))));
  }

  lines.push("", "## Tools", "");
  for (const [path, title, note] of [
    ["/foods", "foodsTitle", "foodsDescription"],
    ["/hotspots", "hotspotsTitle", "hotspotsDescription"],
    ["/flights/status", "flightStatusTitle", "flightStatusDescription"],
    ["/labs/airlines", "airlinesTitle", "airlinesDescription"],
    ["/pricing", "pricingTitle", "pricingDescription"],
    ["/explore", "exploreTitle", "exploreDescription"],
  ] as const) {
    if (open.has(path)) lines.push(entry(plain(t(title)), url(path), plain(t(note))));
  }

  lines.push("", "## Languages", "");
  for (const locale of locales) {
    lines.push(entry(localeLabels[locale], localeUrl(locale, "/")));
  }

  lines.push(
    "",
    "## Optional",
    "",
    entry("Sitemap", `${siteUrl}/sitemap.xml`, "every indexable URL, with hreflang and article lastmod"),
    entry("robots.txt", `${siteUrl}/robots.txt`, "which agents may fetch what, and why"),
    "",
  );

  return new Response(lines.join("\n"), {
    headers: {
      // `text/plain` rather than `text/markdown`: the convention names the file `.txt`, every
      // client fetches it as text, and `text/markdown` makes a browser download it instead of
      // showing it. The charset is explicit because destination names are not all ASCII.
      "Content-Type": "text/plain; charset=utf-8",
      // The switches above are read with `no-store` for a reason; caching the document that
      // reports them would put the two back out of step.
      "Cache-Control": "no-store",
    },
  });
}
