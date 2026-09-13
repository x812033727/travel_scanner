import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideHref, guideListHref } from "@/lib/guides";
import { getGuideList, getGuideTopics, hubIsEmpty } from "@/lib/guides.server";
import { breadcrumbs, itemList } from "@/lib/structured-data";

/** The same two reads the body makes, with the same arguments, so React's per-request cache
 *  answers both from one call to the API. */
const hubLists = (locale: Locale) => Promise.all([
  getGuideList(locale, { kind: "intel" }, 6),
  getGuideList(locale, { kind: "howto" }, 6),
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

export default async function GuidesHubPage({ params }: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params;
  const [[intel, howto], topics, t, nav] = await Promise.all([
    hubLists(locale),
    getGuideTopics(locale, "travel"),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  const cardLabels = {
    intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life"),
  };
  const sections = [
    { kind: "intel" as const, heading: t("guides.latestIntel"), lead: t("guides.intelLead"), rows: intel.articles },
    { kind: "howto" as const, heading: t("guides.featuredHowto"), lead: t("guides.howtoLead"), rows: howto.articles },
  ];
  const everything = [...intel.articles, ...howto.articles];

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
        <h1 className="text-4xl font-bold tracking-tight">{t("guides.hubTitle")}</h1>
        <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{t("guides.hubIntro")}</p>

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
                {section.rows.map((article) => (
                  <GuideCard key={`${article.kind}:${article.slug}`} article={article} labels={cardLabels} />
                ))}
              </ul>
            ) : (
              <p className="mt-4 leading-7 text-[var(--muted)]">{t("guides.empty")}</p>
            )}
          </section>
        ))}

        {topics.length ? (
          <section className="mt-12 border-t border-[var(--line)] pt-8">
            <h2 className="text-2xl font-bold tracking-tight">{t("guides.browseTopics")}</h2>
            <ul className="mt-4 flex flex-wrap gap-2">
              {topics.map((topic) => (
                <li key={topic.slug}>
                  <Link
                    className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] px-3 py-1 text-sm text-[var(--muted)]"
                    href={guideListHref("howto", topic.slug)}
                  >
                    {topic.label}
                  </Link>
                </li>
              ))}
            </ul>
          </section>
        ) : null}
      </main>
    </>
  );
}
