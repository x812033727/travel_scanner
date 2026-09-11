import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { GuideFilters } from "@/components/guides/filters";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideHref, isGuideKind } from "@/lib/guides";
import { getGuideList, getGuideTopics } from "@/lib/guides.server";
import { breadcrumbs, itemList } from "@/lib/structured-data";

type Params = { locale: Locale; kind: string };
type Search = { topic?: string; destination?: string; cursor?: string };

/** `[kind]` holds exactly two literal values; anything else is a 404, not a 500. */
async function resolve(params: Promise<Params>) {
  const { locale, kind } = await params;
  if (!isGuideKind(kind)) notFound();
  return { locale, kind };
}

export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale, kind }, search] = await Promise.all([resolve(params), searchParams]);
  const t = await getTranslations({ locale, namespace: "common" });
  const filtered = Boolean(search.topic || search.destination || search.cursor);
  return {
    title: kind === "intel" ? t("guides.intelTitle") : t("guides.howtoTitle"),
    description: kind === "intel" ? t("guides.intelLead") : t("guides.howtoLead"),
    // A filtered view is the same collection in a different order. Let the unfiltered
    // section carry the ranking rather than competing with dozens of near-duplicates.
    ...(filtered ? { robots: { index: false, follow: true } } : {}),
  };
}

export default async function GuideListPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale, kind }, search] = await Promise.all([resolve(params), searchParams]);
  const [list, topics, t, nav] = await Promise.all([
    getGuideList(locale, { kind, topic: search.topic, destination: search.destination, cursor: search.cursor }, 24),
    getGuideTopics(locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  const heading = kind === "intel" ? t("guides.intelTitle") : t("guides.howtoTitle");
  const lead = kind === "intel" ? t("guides.intelLead") : t("guides.howtoLead");
  const cardLabels = {
    intel: t("guides.intel"), howto: t("guides.howto"), expired: t("guides.expired"),
    validUntil: t("guides.validUntil"), published: t("guides.published"),
  };
  const next = search.topic
    ? `/guides/${kind}?topic=${encodeURIComponent(search.topic)}&cursor=`
    : `/guides/${kind}?cursor=`;

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [
            { name: nav("home"), path: "/" },
            { name: t("guides.hubTitle"), path: "/guides" },
            { name: heading, path: `/guides/${kind}` },
          ]),
          itemList(locale, list.articles.map((article) => ({ name: article.title, path: guideHref(article.kind, article.slug) }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <h1 className="text-4xl font-bold tracking-tight">{heading}</h1>
        <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{lead}</p>

        <GuideFilters
          kind={kind}
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
