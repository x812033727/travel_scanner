import type { Metadata } from "next";
import { notFound, redirect } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { ListingEmpty, ListingToolbar } from "@/components/guides/listing-toolbar";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import {
  guideHref, guideListHref, guideTopicHref, isGuideListSort, isTravelGuideKind, type GuideListSort, type TravelGuideKind,
} from "@/lib/guides";
import { getGuideList, getGuideTopics, hubIsEmpty } from "@/lib/guides.server";
import { localeUrl } from "@/lib/seo";
import { breadcrumbs, itemList } from "@/lib/structured-data";

type Params = { locale: Locale; kind: string };
type Search = { topic?: string; destination?: string; country?: string; cursor?: string; sort?: string };

/** `[kind]` holds the two travel kinds; anything else is a 404, not a 500. That includes
 *  `life`, whose articles list at `/life`, so no listing ever answers at two addresses. */
async function resolve(params: Promise<Params>) {
  const { locale, kind } = await params;
  if (!isTravelGuideKind(kind)) notFound();
  return { locale, kind };
}

/** How-to guides list in the editor's order (featured, then `display_order`), so the core
 *  airport and transit guides lead however many batches follow; intel stays newest first,
 *  because a notice is dated. `?sort=` is the reader's override of either. */
const defaultSort = (kind: TravelGuideKind): GuideListSort => (kind === "howto" ? "curated" : "latest");
const sortOf = (kind: TravelGuideKind, search: Search): GuideListSort =>
  (isGuideListSort(search.sort) && search.sort !== "news" ? search.sort : defaultSort(kind));

/** One listing read, shared by the metadata and the body through React's per-request cache:
 *  same arguments, one call to the API. */
const listFor = (locale: Locale, kind: TravelGuideKind, search: Search) =>
  getGuideList(locale, {
    kind, topic: search.topic, destination: search.destination, country: search.country, cursor: search.cursor,
    sort: sortOf(kind, search),
  }, 24);

/** The listing's URL for an order, keeping the filters and dropping the cursor. The kind's
 *  own default order is the canonical address and carries no `sort`. */
function viewHref(kind: TravelGuideKind, search: Search, sort: GuideListSort): string {
  const params = new URLSearchParams();
  for (const key of ["topic", "destination", "country"] as const) {
    const value = search[key];
    if (value) params.set(key, value);
  }
  if (sort !== defaultSort(kind)) params.set("sort", sort);
  const query = params.toString();
  return query ? `${guideListHref(kind)}?${query}` : guideListHref(kind);
}

export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale, kind }, search] = await Promise.all([resolve(params), searchParams]);
  const t = await getTranslations({ locale, namespace: "common" });
  const filtered = Boolean(search.topic || search.destination || search.country || search.cursor || search.sort);
  // Only the unfiltered view asks: a filtered one is `noindex` already, and the extra read
  // would be a second API call per crawl of a URL whose answer cannot change.
  const empty = !filtered && hubIsEmpty(await listFor(locale, kind, search));
  return {
    title: kind === "intel" ? t("guides.intelTitle") : t("guides.howtoTitle"),
    description: kind === "intel" ? t("guides.intelLead") : t("guides.howtoLead"),
    // A filtered or reordered view is the same collection in a different order. Let the
    // unfiltered section carry the ranking rather than competing with dozens of
    // near-duplicates. An empty language is out for a different reason: there is nothing
    // on the page at all until this section publishes its first article here. Both stay
    // `follow`.
    ...(filtered || empty ? { robots: { index: false, follow: true } } : {}),
    // A `?topic=` view is the topic hub's collection under an older URL: the hub is the page
    // that ranks, so this one names it as canonical rather than competing with it.
    ...(search.topic ? { alternates: { canonical: localeUrl(locale, guideTopicHref("travel", search.topic)) } } : {}),
  };
}

export default async function GuideListPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale, kind }, search] = await Promise.all([resolve(params), searchParams]);
  const [list, topics, t, nav] = await Promise.all([
    listFor(locale, kind, search),
    getGuideTopics(locale, "travel"),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  const sort = sortOf(kind, search);
  const listing = viewHref(kind, search, sort);
  // A `?cursor=` the API refused -- a "see more" link minted before the listing changed its
  // order, or a hand-edited one -- must not render as a 200 saying nothing is published.
  // The first page is the honest answer, and it is one click from where the reader was.
  if (search.cursor && !list.available) redirect(listing);

  const heading = kind === "intel" ? t("guides.intelTitle") : t("guides.howtoTitle");
  const lead = kind === "intel" ? t("guides.intelLead") : t("guides.howtoLead");
  const cardLabels = {
    intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life"),
  };
  const searchLabels = { label: t("guides.searchLabel"), placeholder: t("guides.searchPlaceholder"), submit: t("guides.searchSubmit") };
  const next = `${listing}${listing.includes("?") ? "&" : "?"}cursor=`;

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [
            { name: nav("home"), path: "/" },
            { name: t("guides.hubTitle"), path: "/guides" },
            { name: heading, path: guideListHref(kind) },
          ]),
          itemList(locale, list.articles.map((article) => ({ name: article.title, path: guideHref(article.kind, article.slug) }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <h1 className="text-4xl font-bold tracking-tight">{heading}</h1>
        <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{lead}</p>

        <ListingToolbar
          section="travel"
          topics={topics}
          active={search.topic ?? null}
          allHref={guideListHref(kind)}
          sort={{ current: sort, hrefs: { curated: viewHref(kind, search, "curated"), latest: viewHref(kind, search, "latest") } }}
          labels={{
            allTopics: t("guides.allTopics"), topicsLabel: t("guides.topicsLabel"), subtopics: t("guides.subtopics"),
            moreChips: t("guides.moreChips"), fewerChips: t("guides.fewerChips"),
            sortLabel: t("guides.sortLabel"), sortCurated: t("guides.sortCurated"), sortLatest: t("guides.sortLatest"),
          }}
        />

        {list.articles.length ? (
          <ul className="mt-6 grid gap-3 sm:grid-cols-2">
            {list.articles.map((article) => (
              <GuideCard key={article.slug} article={article} labels={cardLabels} />
            ))}
          </ul>
        ) : (
          <ListingEmpty
            section="travel"
            action={`/${locale}/search/articles`}
            labels={{ ...searchLabels, empty: t("guides.empty"), hint: t("guides.emptyHint") }}
          />
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
