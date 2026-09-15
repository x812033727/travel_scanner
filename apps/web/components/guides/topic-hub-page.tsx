import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { GuideCard } from "@/components/guides/card";
import { TopicChips } from "@/components/guides/topic-chips";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import { locales, type Locale } from "@/i18n/routing";
import { guideHref, guideTopicHref, sectionHubHref, topicLocales, type GuideSection, type GuideTopic } from "@/lib/guides";
import { getGuideList, getGuideTopicList, hubIsEmpty } from "@/lib/guides.server";
import { HREFLANG_DEFAULT, localeUrl } from "@/lib/seo";
import { breadcrumbs, itemList } from "@/lib/structured-data";

export type TopicHubRoute = { locale: Locale; section: GuideSection; topic: string; cursor?: string };

const PAGE_SIZE = 24;

/** One listing read and one vocabulary read, shared by the metadata and the body through
 *  React's per-request cache: same arguments, one call each to the API. */
function reads({ locale, section, topic, cursor }: TopicHubRoute) {
  return Promise.all([
    getGuideTopicList(locale, section),
    getGuideList(locale, { section, topic, cursor }, PAGE_SIZE),
  ]);
}

/**
 * Resolves the route to a topic, or answers 404. An unknown slug is not a page; an
 * unreachable vocabulary is, and says so with `noindex` rather than claiming the topic is
 * gone -- the hub must survive an API outage the way the section hubs do.
 */
function resolve(topics: GuideTopic[], available: boolean, slug: string): GuideTopic | null {
  const found = topics.find((topic) => topic.slug === slug) ?? null;
  if (available && !found) notFound();
  return found;
}

export async function topicHubMetadata(route: TopicHubRoute): Promise<Metadata> {
  const [vocabulary, list] = await reads(route);
  const topic = resolve(vocabulary.topics, vocabulary.available, route.topic);
  const t = await getTranslations({ locale: route.locale, namespace: "metadata" });
  const label = topic?.label ?? route.topic;
  const path = guideTopicHref(route.section, route.topic);
  // Published-in-this-language decides the index, from the vocabulary's own counts; only when
  // an older API sends none does the listing's emptiness decide, and only a complete answer
  // may say empty (`hubIsEmpty`). A `?cursor=` page is the same collection further down.
  const empty = topic?.count !== undefined ? topic.count === 0 : hubIsEmpty(list);
  const noindex = !topic || empty || Boolean(route.cursor);
  const published = topic ? topicLocales(topic, locales) : [];
  return {
    title: t("topicHubTitle", { topic: label }),
    description: topic?.description || t("topicHubDescription", { topic: label }),
    alternates: {
      canonical: localeUrl(route.locale, path),
      // Only the languages with something under the topic, for the reason an article page
      // lists only its published translations: hreflang pointing at a `noindex` page is a
      // contradiction. `x-default` belongs to English only while English has the topic.
      ...(published.length
        ? {
            languages: {
              ...Object.fromEntries(published.map((locale) => [locale, localeUrl(locale, path)])),
              ...(published.includes(HREFLANG_DEFAULT) ? { "x-default": localeUrl(HREFLANG_DEFAULT, path) } : {}),
            },
          }
        : {}),
    },
    ...(noindex ? { robots: { index: false, follow: true } } : {}),
  };
}

export async function renderTopicHub(route: TopicHubRoute) {
  const { locale, section } = route;
  const [[vocabulary, list], t, nav] = await Promise.all([
    reads(route),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);
  const topic = resolve(vocabulary.topics, vocabulary.available, route.topic);
  const parent = topic?.parent ? vocabulary.topics.find((item) => item.slug === topic.parent) ?? null : null;
  const label = topic?.label ?? route.topic;
  const sectionTitle = section === "life" ? t("guides.lifeHubTitle") : t("guides.hubTitle");
  const sectionLead = section === "life" ? t("guides.lifeHubIntro") : t("guides.hubIntro");
  const lead = topic?.description || parent?.description || sectionLead;
  const path = guideTopicHref(section, route.topic);
  const cardLabels = { intel: t("guides.intel"), howto: t("guides.howto"), life: t("guides.life") };
  const chipLabels = {
    allTopics: t("guides.allTopics"), topicsLabel: t("guides.topicsLabel"), subtopics: t("guides.subtopics"),
    moreChips: t("guides.moreChips"), fewerChips: t("guides.fewerChips"),
  };
  const trail = [
    { name: nav("home"), path: "/" },
    { name: sectionTitle, path: sectionHubHref(section) },
    ...(parent ? [{ name: parent.label, path: guideTopicHref(section, parent.slug) }] : []),
    { name: label, path },
  ];

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, trail),
          itemList(locale, list.articles.map((article) => ({ name: article.title, path: guideHref(article.kind, article.slug) }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <nav aria-label={t("guides.breadcrumb")} className="text-[length:var(--text-meta)] text-[var(--muted)]">
          <ol className="flex flex-wrap items-center gap-1">
            {trail.slice(0, -1).map((crumb) => (
              <li key={crumb.path} className="flex items-center gap-1">
                <Link className="inline-flex min-h-11 items-center underline underline-offset-4" href={crumb.path}>{crumb.name}</Link>
                <span aria-hidden>›</span>
              </li>
            ))}
            <li aria-current="page" className="inline-flex min-h-11 items-center">{label}</li>
          </ol>
        </nav>
        <h1 className="text-4xl font-bold tracking-tight">{label}</h1>
        <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{lead}</p>
        {topic?.count !== undefined && topic.count > 0 ? (
          <p className="mt-2 text-[length:var(--text-meta)] text-[var(--muted)]">{t("guides.resultCount", { count: topic.count })}</p>
        ) : null}

        {!vocabulary.available ? (
          <p className="mt-6 leading-7 text-[var(--muted)]">{t("guides.topicUnavailable")}</p>
        ) : null}

        <TopicChips
          section={section}
          topics={vocabulary.topics}
          active={route.topic}
          allHref={sectionHubHref(section)}
          labels={chipLabels}
        />

        {list.articles.length ? (
          <ul className="mt-6 grid gap-3 sm:grid-cols-2">
            {list.articles.map((article) => (
              <GuideCard key={`${article.kind}:${article.slug}`} article={article} labels={cardLabels} />
            ))}
          </ul>
        ) : (
          <p className="mt-6 leading-7 text-[var(--muted)]">{t("guides.empty")}</p>
        )}

        {list.next_cursor ? (
          <p className="mt-8">
            <Link className="inline-flex min-h-11 items-center text-[var(--teal)] underline" href={`${path}?cursor=${encodeURIComponent(list.next_cursor)}`}>
              {t("guides.more")}
            </Link>
          </p>
        ) : null}
      </main>
    </>
  );
}
