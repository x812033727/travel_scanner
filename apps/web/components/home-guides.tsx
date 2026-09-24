import { useTranslations } from "next-intl";
import { GuideCard } from "@/components/guides/card";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideTopicHref, type GuideSummary } from "@/lib/guides";
import { getGuideList } from "@/lib/guides.server";

const PER_BLOCK = 4;

export type HomeGuideBlock = { key: "travel" | "tech" | "money"; href: string; articles: GuideSummary[] };

/** The three reads, in parallel. A failed read is an empty block, never a thrown page. */
export async function loadHomeGuides(locale: Locale): Promise<HomeGuideBlock[]> {
  const [travel, tech, money] = await Promise.all([
    getGuideList(locale, { kind: "howto", sort: "curated" }, PER_BLOCK),
    getGuideList(locale, { kind: "life", topic: "ai", sort: "curated" }, PER_BLOCK),
    getGuideList(locale, { kind: "life", topic: "finance", sort: "curated" }, PER_BLOCK),
  ]);
  return [
    { key: "travel", href: "/guides", articles: travel.articles },
    { key: "tech", href: guideTopicHref("life", "ai"), articles: tech.articles },
    { key: "money", href: guideTopicHref("life", "finance"), articles: money.articles },
  ];
}

/**
 * What the site is, in its own words, and a way into each of its sections.
 *
 * The home page used to be the search form and the destination chips: a reviewer or a
 * crawler landing here saw a flight-comparison tool and none of the articles that make up
 * most of the site, which is how AdSense came to call it low-value content on 2026-09-23.
 * This sits outside `DiscoveryHomeGate`, so it is in the response whichever way discovery
 * is switched.
 *
 * A block whose read failed or came back empty is left out rather than shown as "nothing
 * here": the paragraph above it still stands on its own.
 */
export function HomeGuides({ blocks }: { blocks: HomeGuideBlock[] }) {
  const t = useTranslations("search.homeGuides");
  const common = useTranslations("common");
  const labels = { intel: common("guides.intel"), howto: common("guides.howto"), life: common("guides.life") };

  return (
    <section aria-labelledby="home-guides-title" className="mx-auto max-w-6xl px-5 pb-20 md:px-8">
      <p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p>
      <h2 id="home-guides-title" className="mt-1 text-2xl font-bold md:text-3xl">{t("title")}</h2>
      <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("intro")}</p>
      {blocks.filter((block) => block.articles.length).map((block) => (
        <div key={block.key} className="mt-8" data-testid={`home-guides-${block.key}`}>
          <div className="flex flex-wrap items-baseline justify-between gap-3">
            <h3 className="text-xl font-bold">{t(block.key)}</h3>
            <Link href={block.href} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">
              {t("seeAll")}
            </Link>
          </div>
          <ul className="mt-3 grid gap-3 sm:grid-cols-2">
            {block.articles.map((article) => (
              <GuideCard key={article.slug} article={article} labels={labels} variant="compact" />
            ))}
          </ul>
        </div>
      ))}
    </section>
  );
}
