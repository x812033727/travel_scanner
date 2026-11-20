import type { Metadata } from "next";
import { redirect } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { VideoCard } from "@/components/videos/video-card";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { breadcrumbs, videoItemList } from "@/lib/structured-data";
import { isVideoKind, videoArticleHref, videosHref, type VideoKind } from "@/lib/videos";
import { getVideos } from "@/lib/videos.server";

type Params = { locale: Locale };
type Search = { category?: string; kind?: string; cursor?: string };

const filtersOf = (search: Search) => ({
  category: search.category || undefined,
  kind: isVideoKind(search.kind) ? search.kind : undefined,
  cursor: search.cursor || undefined,
});

export async function generateMetadata(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
): Promise<Metadata> {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const filtered = Boolean(search.category || search.kind || search.cursor);
  const [t, list] = await Promise.all([
    getTranslations({ locale, namespace: "metadata" }),
    filtered ? Promise.resolve(null) : getVideos(locale, {}),
  ]);
  const empty = Boolean(list && list.available && list.videos.length === 0);
  return {
    title: t("videosTitle"),
    description: t("videosDescription"),
    // A filtered or paged view is the same library cut differently, and a locale with no
    // published videos yet is a soft 404 until its first video ships; both stay `follow`.
    ...(filtered || empty ? { robots: { index: false, follow: true } } : {}),
  };
}

/**
 * The video library: every video the site has published on YouTube, newest first, with a
 * row for long videos or Shorts and a row of the categories that have something in them.
 * Each card plays in place and links to the article it retells.
 */
export default async function VideosPage(
  { params, searchParams }: { params: Promise<Params>; searchParams: Promise<Search> },
) {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const filters = filtersOf(search);
  const [page, t, nav] = await Promise.all([
    getVideos(locale, filters),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);
  // A cursor the API no longer honours must not render as "no videos"; start over instead.
  if (filters.cursor && page.available && !page.videos.length) redirect(`/${locale}${videosHref({ ...filters, cursor: null })}`);
  const date = new Intl.DateTimeFormat(locale, { year: "numeric", month: "short", day: "numeric" });
  const categoryLabel = (code: string | null) => (code && t.has(`videos.categories.${code}`) ? t(`videos.categories.${code}`) : null);
  const chip = (active: boolean) => `app-filter-chip ${active ? "app-filter-chip-active" : ""}`;
  const kinds: (VideoKind | null)[] = [null, "long", "shorts"];

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [{ name: nav("home"), path: "/" }, { name: t("videos.title"), path: "/videos" }]),
          videoItemList(
            locale,
            page.videos.map((video) => ({
              slug: video.slug,
              title: video.title,
              youtube_video_id: video.youtube_video_id,
              articlePath: videoArticleHref(video),
            })),
          ),
        ]}
      />
      <main className="mx-auto max-w-6xl px-5 py-6 sm:py-10 md:px-8">
        <nav aria-label={t("guides.breadcrumb")} className="flex flex-wrap items-center gap-x-1.5 gap-y-0.5 text-[length:var(--text-meta)] text-[var(--muted)]">
          <Link className="inline-flex min-h-11 items-center underline decoration-[var(--line)] underline-offset-4 transition-colors hover:text-[var(--teal)] hover:decoration-[var(--teal)]" href="/">
            {nav("home")}
          </Link>
          <span aria-hidden>›</span>
          <span aria-current="page" className="py-1.5 font-medium text-[var(--ink)]">{t("videos.title")}</span>
        </nav>

        <header className="portal-hero-shell mt-2 rounded-3xl p-6 md:p-10">
          <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl md:text-5xl">{t("videos.title")}</h1>
          <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{t("videos.intro")}</p>
          <p className="mt-2 max-w-2xl text-sm leading-6 text-[var(--muted)]">{t("videos.privacy")}</p>
        </header>

        <nav aria-label={t("videos.kinds")} className="mt-6 flex flex-wrap gap-2">
          {kinds.map((kind) => (
            <Link key={kind ?? "all"} href={videosHref({ category: filters.category, kind })} aria-current={(filters.kind ?? null) === kind ? "page" : undefined} className={chip((filters.kind ?? null) === kind)}>
              {kind ? t(`videos.${kind}`) : t("videos.all")}
            </Link>
          ))}
        </nav>
        {page.categories.length > 1 ? (
          <nav aria-label={t("videos.categoriesLabel")} className="mt-3 flex flex-wrap gap-2">
            {[null, ...page.categories].map((code) => (
              <Link key={code ?? "all"} href={videosHref({ kind: filters.kind, category: code })} aria-current={(filters.category ?? null) === code ? "page" : undefined} className={chip((filters.category ?? null) === code)}>
                {code ? categoryLabel(code) ?? code : t("videos.all")}
              </Link>
            ))}
          </nav>
        ) : null}

        {!page.available ? (
          <p className="mt-8 leading-7 text-[var(--muted)]">{t("videos.unavailable")}</p>
        ) : page.videos.length ? (
          <ul className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
            {page.videos.map((video) => (
              <VideoCard
                key={video.slug}
                video={video}
                date={date.format(new Date(video.published_at))}
                labels={{
                  play: t("videos.play", { title: video.title }),
                  watchOnYoutube: t("videos.watchOnYoutube"),
                  readArticle: t("videos.readArticle"),
                  category: categoryLabel(video.category),
                }}
              />
            ))}
          </ul>
        ) : (
          <p className="mt-8 leading-7 text-[var(--muted)]">{t("videos.empty")}</p>
        )}

        {page.next_cursor ? (
          <p className="mt-8">
            <Link
              className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] bg-[var(--surface)] px-5 py-2 text-sm font-semibold text-[var(--teal)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)]"
              href={videosHref({ ...filters, cursor: page.next_cursor })}
            >
              {t("videos.more")}
            </Link>
          </p>
        ) : null}
      </main>
    </>
  );
}
