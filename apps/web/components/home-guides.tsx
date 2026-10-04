import { ArrowRight } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { GuideCard } from "@/components/guides/card";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideTopicHref, type GuideSummary } from "@/lib/guides";
import { getGuideList } from "@/lib/guides.server";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";

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
 * This sits before and outside `DiscoveryHomeGate`, so the introduction and article
 * links are present in the server response whichever way discovery is switched.
 *
 * A block whose read failed or came back empty is left out rather than shown as "nothing
 * here": the paragraph above it still stands on its own.
 */
export function HomeGuides({ blocks }: { blocks: HomeGuideBlock[] }) {
  const t = useTranslations("search.homeGuides");
  const common = useTranslations("common");
  const flow = getFrontendFlowCopy(useLocale());
  const labels = { intel: common("guides.intel"), howto: common("guides.howto"), life: common("guides.life") };

  return (
    <section aria-labelledby="home-guides-title" className="mx-auto max-w-6xl px-5 pb-10 pt-6 md:px-8 md:pt-10">
      <div className="flex flex-wrap items-center justify-between gap-4">
        <div className="min-w-0">
          <p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p>
          <h2 id="home-guides-title" className="mt-1 text-2xl font-bold md:text-3xl">{t("title")}</h2>
        </div>
        <Link href="/search/new" className="inline-flex min-h-11 items-center gap-2 rounded-full border border-[var(--teal)] px-4 py-2 text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)]">
          {flow.searchTrips}<ArrowRight size={17} className="shrink-0" aria-hidden />
        </Link>
      </div>
      <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("intro")}</p>
      <div className="mt-6 grid gap-6 lg:grid-cols-3">
        {blocks.filter((block) => block.articles.length).map((block) => (
          <div key={block.key} className="min-w-0" data-testid={`home-guides-${block.key}`}>
            <div className="flex flex-wrap items-baseline justify-between gap-3">
              <h3 className="text-xl font-bold">{t(block.key)}</h3>
              <Link href={block.href} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">
                {t("seeAll")}
              </Link>
            </div>
            <ul className="mt-3 grid gap-3 sm:grid-cols-2 lg:grid-cols-1">
              {block.articles.map((article) => (
                <GuideCard key={article.slug} article={article} labels={labels} variant="compact" />
              ))}
            </ul>
          </div>
        ))}
      </div>
    </section>
  );
}
