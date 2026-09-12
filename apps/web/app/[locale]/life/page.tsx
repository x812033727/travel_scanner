import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { GuideFilters } from "@/components/guides/filters";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideHref, guideListHref } from "@/lib/guides";
import { getGuideList, getGuideTopics } from "@/lib/guides.server";
import { breadcrumbs, itemList } from "@/lib/structured-data";

type Params = { locale: Locale };
type Search = { topic?: string; cursor?: string };

/**
 * The lifestyle section: the same article system as `/guides`, with its own hub, its own
 * topic vocabulary and no kind segment, because `life` is the only kind that lists here.
 */
export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const t = await getTranslations({ locale, namespace: "metadata" });
  const filtered = Boolean(search.topic || search.cursor);
  return {
    title: t("lifeTitle"),
    description: t("lifeDescription"),
    // A filtered view is the same collection in a different order. Let the unfiltered
    // section carry the ranking rather than competing with dozens of near-duplicates.
    ...(filtered ? { robots: { index: false, follow: true } } : {}),
  };
}

export default async function LifeHubPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const [list, topics, t, nav] = await Promise.all([
    getGuideList(locale, { kind: "life", topic: search.topic, cursor: search.cursor }, 24),
    getGuideTopics(locale, "life"),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  const cardLabels = {
    intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life"),
    expired: t("guides.expired"), validUntil: t("guides.validUntil"), published: t("guides.published"),
  };
  const listing = guideListHref("life", search.topic);
  const next = `${listing}${listing.includes("?") ? "&" : "?"}cursor=`;

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [
            { name: nav("home"), path: "/" },
            { name: t("guides.lifeHubTitle"), path: "/life" },
          ]),
          itemList(locale, list.articles.map((article) => ({ name: article.title, path: guideHref(article.kind, article.slug) }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <h1 className="text-4xl font-bold tracking-tight">{t("guides.lifeHubTitle")}</h1>
        <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{t("guides.lifeHubIntro")}</p>

        <GuideFilters
          kind="life"
          topics={topics}
          active={search.topic ?? null}
          labels={{ allTopics: t("guides.allTopics"), topicsLabel: t("guides.topicsLabel") }}
        />

        {list.articles.length ? (
          <ul className="mt-6 grid gap-3 sm:grid-cols-2">
            {list.articles.map((article) => (
              <GuideCard key={article.slug} article={article} labels={cardLabels} />
            ))}
          </ul>
        ) : (
          <p className="mt-6 leading-7 text-[var(--muted)]">{t("guides.empty")}</p>
        )}

        {list.next_cursor ? (
          <p className="mt-8">
            <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`${next}${encodeURIComponent(list.next_cursor)}`}>
              {t("guides.more")}
            </Link>
          </p>
        ) : null}
      </main>
    </>
  );
}
