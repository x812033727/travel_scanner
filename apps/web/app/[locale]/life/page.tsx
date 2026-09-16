import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { GuideFilters } from "@/components/guides/filters";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { guideHref, guideListHref, guideTopicHref } from "@/lib/guides";
import { getGuideList, getGuideTopics, getGuideArticle, hubIsEmpty } from "@/lib/guides.server";
import { localeUrl } from "@/lib/seo";
import { seriesCopy } from "@/lib/guide-series-copy";
import { getGeminiHubReference, getVisibleGeminiSeries, filterGeminiArticleLinks } from "@/lib/gemini-series.server";
import { visibleGeminiHref } from "@/lib/gemini-series-projection";
import { breadcrumbs, itemList } from "@/lib/structured-data";
import { HUB_SLUG } from "@/lib/codex-learning";
import { learningCopy } from "@/lib/codex-learning/copy";

type Params = { locale: Locale };
type Search = { topic?: string; cursor?: string };

/** One listing read, shared by the metadata and the body through React's per-request cache:
 *  same arguments, one call to the API. The editor's order (featured, then `display_order`,
 *  then newest): the overview every other article links back to stays on page one however
 *  many batches follow it. */
const listFor = (locale: Locale, search: Search) =>
  getGuideList(locale, { kind: "life", topic: search.topic, cursor: search.cursor, sort: "curated" }, 24);

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
  // Only the unfiltered view asks: a filtered one is `noindex` already, and the extra read
  // would be a second API call per crawl of a URL whose answer cannot change.
  const empty = !filtered && hubIsEmpty(await listFor(locale, search));
  return {
    title: t("lifeTitle"),
    description: t("lifeDescription"),
    // A filtered view is the same collection in a different order. Let the unfiltered
    // section carry the ranking rather than competing with dozens of near-duplicates.
    // An empty section is out for a different reason: the lifestyle section has published
    // nothing in this language yet, so the page is a heading over one sentence. Both stay
    // `follow`, and the first article published here puts it back in the index.
    ...(filtered || empty ? { robots: { index: false, follow: true } } : {}),
    // The topic hub is the page that ranks for a topic; this older `?topic=` URL names it.
    ...(search.topic ? { alternates: { canonical: localeUrl(locale, guideTopicHref("life", search.topic)) } } : {}),
  };
}

export default async function LifeHubPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const [rawList, topics, t, nav] = await Promise.all([
    listFor(locale, search),
    getGuideTopics(locale, "life"),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  const listing = guideListHref("life", search.topic);
  // A `?cursor=` the API refused (minted under the old order, or hand-edited) must not
  // render as a 200 saying nothing is published; the first page is the honest answer.
  if (search.cursor && !rawList.available) redirect(listing);

  const cardLabels = {
    intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life"),
  };
  const tutorialHub = await getGuideArticle("life", "claude-code-tutorials", locale);
  const geminiReference = getGeminiHubReference(locale);
  const geminiHub = geminiReference ? await getGuideArticle("life", geminiReference.slug, locale) : null;
  const geminiSeries = getVisibleGeminiSeries({ locale, hubPublished: geminiHub?.status === "published" && Boolean(geminiHub.document) });
  const list = { ...rawList, articles: geminiReference ? filterGeminiArticleLinks(rawList.articles, geminiSeries) : rawList.articles };
  const tutorialCopy = seriesCopy(locale);
  const next = `${listing}${listing.includes("?") ? "&" : "?"}cursor=`;
  const learningHub = await getGuideArticle("life", HUB_SLUG, locale);
  const learning = learningCopy(locale);

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
        {learningHub.status === "published" && <aside className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5"><Link href={`/life/${HUB_SLUG}`} className="inline-flex min-h-11 items-center text-lg font-bold text-[var(--teal)] underline">{learning.title} →</Link><p className="leading-7">{learning.intro}</p></aside>}

        {geminiSeries ? <aside className="mt-6 rounded-2xl border border-[var(--teal)] bg-[var(--paper)] p-5">
          <a href={visibleGeminiHref(geminiSeries, geminiSeries.hubSlug)} className="text-xl font-semibold text-[var(--teal)] underline">{geminiSeries.title}</a>
          <p className="mt-2 leading-7">{t("geminiSeries.entry", { count: geminiSeries.articles.length })}</p>
        </aside> : null}

        <GuideFilters
          kind="life"
          topics={topics}
          active={search.topic ?? null}
          labels={{
            allTopics: t("guides.allTopics"), topicsLabel: t("guides.topicsLabel"), subtopics: t("guides.subtopics"),
            moreChips: t("guides.moreChips"), fewerChips: t("guides.fewerChips"),
          }}
        />
        {tutorialHub.status === "published" && tutorialHub.document ? <section className="mt-6 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5">
          <h2 className="text-xl font-bold"><Link className="text-[var(--teal)] underline" href="/life/claude-code-tutorials">{tutorialHub.document.title}</Link></h2>
          <p className="mt-2 leading-7 text-[var(--muted)]">{tutorialCopy.entry}</p>
        </section> : null}

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
