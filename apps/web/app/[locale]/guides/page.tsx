import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { DestinationGroups } from "@/components/guides/destination-groups";
import { HubHero } from "@/components/guides/hub-hero";
import { TopicTiles } from "@/components/guides/topic-tiles";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideHref, guideListHref } from "@/lib/guides";
import { getDestinationFacets, getGuideList, getGuideTopics, hubIsEmpty } from "@/lib/guides.server";
import { breadcrumbs, itemList } from "@/lib/structured-data";

/** The same two reads the body makes, with the same arguments, so React's per-request cache
 *  answers both from one call to the API. */
const hubLists = (locale: Locale) => Promise.all([
  getGuideList(locale, { kind: "intel" }, 6),
  // "Featured guides" means it: the editor's order, not the last batch imported.
  getGuideList(locale, { kind: "howto", sort: "curated" }, 6),
]);

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const [t, lists] = await Promise.all([
    getTranslations({ locale, namespace: "metadata" }),
    hubLists(locale),
  ]);
  return {
    title: t("guidesTitle"),
    description: t("guidesDescription"),
    // Articles are published one language at a time. Until this one has any, the hub is a
    // heading over "nothing here yet" -- a soft 404 to Search Console and a page with no
    // content to Google. It stays `follow`, so the language switcher still leads to the
    // languages that do publish, and it returns to the index with the first article.
    ...(hubIsEmpty(...lists) ? { robots: { index: false, follow: true } } : {}),
  };
}

/**
 * The travel hub, top to bottom: what the section is and a search box scoped to it, the
 * topics as tiles, the editor's featured guides, the newest intel, and every destination
 * with something written, grouped by country.
 *
 * Series moved to the topic hubs and the figures line is gone, both for the reasons the
 * lifestyle hub gives -- the two hubs stay the same shape on purpose.
 */
export default async function GuidesHubPage({ params }: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params;
  const [[intel, howto], topics, facets, t, nav] = await Promise.all([
    hubLists(locale),
    getGuideTopics(locale, "travel"),
    getDestinationFacets(locale, "travel"),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  const cardLabels = {
    intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life"),
  };
  const sections = [
    { kind: "howto" as const, heading: t("guides.featuredHowto"), lead: t("guides.howtoLead"), rows: howto.articles },
    { kind: "intel" as const, heading: t("guides.latestIntel"), lead: t("guides.intelLead"), rows: intel.articles },
  ];
  const everything = [...howto.articles, ...intel.articles];

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [{ name: nav("home"), path: "/" }, { name: t("guides.hubTitle"), path: "/guides" }]),
          itemList(locale, everything.map((article) => ({ name: article.title, path: guideHref(article.kind, article.slug) }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <HubHero
          title={t("guides.hubTitle")}
          intro={t("guides.hubIntro")}
          section="travel"
          action={`/${locale}/search/articles`}
          labels={{ label: t("guides.searchLabel"), placeholder: t("guides.searchPlaceholder"), submit: t("guides.searchSubmit") }}
        />

        <TopicTiles
          section="travel"
          topics={topics}
          labels={{ heading: t("guides.browseTopics"), more: t("guides.subtopicsMore") }}
        />

        {sections.map((section) => (
          <section key={section.kind} className="mt-10">
            <div className="flex flex-wrap items-baseline justify-between gap-3">
              <h2 className="text-2xl font-bold tracking-tight">{section.heading}</h2>
              <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={guideListHref(section.kind)}>
                {t("guides.seeAll")}
              </Link>
            </div>
            <p className="mt-2 max-w-2xl leading-7 text-[var(--muted)]">{section.lead}</p>
            {section.rows.length ? (
              <ul className="mt-4 grid gap-3 sm:grid-cols-2">
                {section.rows.map((article, index) => (
                  <GuideCard
                    key={`${article.kind}:${article.slug}`}
                    article={article}
                    labels={cardLabels}
                    // The editor's first pick leads the hub as the one large card.
                    variant={section.kind === "howto" && index === 0 ? "featured" : "default"}
                  />
                ))}
              </ul>
            ) : (
              <p className="mt-4 leading-7 text-[var(--muted)]">{t("guides.empty")}</p>
            )}
          </section>
        ))}

        <DestinationGroups
          destinations={facets.destinations}
          labels={{
            heading: t("guides.browseDestinations"), lead: t("guides.destinationsLead"), countryAll: t("guides.countryAll"),
          }}
        />
      </main>
    </>
  );
}
