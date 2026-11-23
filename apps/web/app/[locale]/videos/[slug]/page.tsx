import type { Metadata } from "next";
import { ArrowLeft, ExternalLink, FileText } from "lucide-react";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { Breadcrumb } from "@/components/guides/breadcrumb";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { VideoCard } from "@/components/videos/video-card";
import { VideoWatchPlayer } from "@/components/videos/video-watch-player";
import { Link } from "@/i18n/navigation";
import { routing, type Locale } from "@/i18n/routing";
import { getGuideArticle } from "@/lib/guides.server";
import { DISCOVER_ROBOTS, alternatesFor, localeUrl } from "@/lib/seo";
import { breadcrumbs, itemList, videoObject } from "@/lib/structured-data";
import { videoArticleHref, videoHref, videosHref, type PublicVideo } from "@/lib/videos";
import { getVideo } from "@/lib/videos.server";

type Params = { locale: Locale; slug: string };

async function loadCompanionArticle(locale: Locale, video: PublicVideo) {
  if (!video.source_guide || !video.source_guide_kind) return null;
  const article = await getGuideArticle(video.source_guide_kind, video.source_guide, locale);
  if (article.status !== "published" || !article.document) return null;
  return {
    title: article.document.title,
    description: article.document.description,
    href: videoArticleHref(video),
  };
}

export async function generateMetadata(
  { params }: { params: Promise<Params> },
): Promise<Metadata> {
  const { locale, slug } = await params;
  const [result, t] = await Promise.all([
    getVideo(locale, slug),
    getTranslations({ locale, namespace: "common" }),
  ]);

  if (result.status === "not_found") notFound();
  if (result.status === "unavailable") {
    return {
      title: `${t("videos.title")} | Mokaair`,
      description: t("videos.unavailable"),
      robots: { index: false, follow: true },
    };
  }

  const { video } = result;
  const companion = await loadCompanionArticle(locale, video);
  const path = videoHref(video.slug);
  const canonical = localeUrl(locale, path);
  const id = video.youtube_video_id;
  const thumbnail = `https://i.ytimg.com/vi/${id}/hqdefault.jpg`;
  const description = companion?.description || t("videos.intro");

  return {
    title: `${video.title} | Mokaair`,
    description,
    robots: DISCOVER_ROBOTS,
    alternates: alternatesFor(locale, path),
    openGraph: {
      type: "video.other",
      url: canonical,
      title: video.title,
      description,
      siteName: "Mokaair",
      locale: locale.replace("-", "_"),
      alternateLocale: routing.locales
        .filter((value) => value !== locale)
        .map((value) => value.replace("-", "_")),
      images: [{ url: thumbnail, width: 480, height: 360, alt: video.title }],
      videos: [
        {
          url: `https://www.youtube-nocookie.com/embed/${id}`,
          type: "text/html",
          width: 1280,
          height: 720,
        },
      ],
    },
    twitter: {
      card: "summary_large_image",
      title: video.title,
      description,
      images: [thumbnail],
    },
  };
}

/**
 * Dedicated watch page for a single published YouTube video.
 *
 * Google Video Search and Discover require a dedicated watch URL per video rather than a
 * gallery page with dozens of embeds. This page provides one canonical VideoObject, the
 * privacy-preserving embed player, a rich companion article handover, and related videos.
 */
export default async function VideoWatchPage(
  { params }: { params: Promise<Params> },
) {
  const { locale, slug } = await params;
  const [result, t, nav] = await Promise.all([
    getVideo(locale, slug),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  if (result.status === "not_found") notFound();

  if (result.status === "unavailable") {
    return (
      <>
        <SiteHeader />
        <main className="mx-auto max-w-3xl px-5 py-10 md:px-8">
          <div className="rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-6 shadow-[var(--shadow-sm)] md:p-8">
            <h1 className="text-3xl font-extrabold tracking-tight">{t("videos.title")}</h1>
            <p role="alert" className="mt-4 leading-7 text-[var(--muted)]">
              {t("videos.unavailable")}
            </p>
            <p className="mt-6">
              <Link
                href="/videos"
                className="inline-flex min-h-11 items-center gap-2 font-semibold text-[var(--teal)] underline underline-offset-4"
              >
                <ArrowLeft size={16} aria-hidden />
                {t("videos.backToVideos")}
              </Link>
            </p>
          </div>
        </main>
      </>
    );
  }

  const { video, related } = result;
  const companion = await loadCompanionArticle(locale, video);
  const articlePath = videoArticleHref(video);
  const pagePath = videoHref(video.slug);
  const date = new Intl.DateTimeFormat(locale, { year: "numeric", month: "short", day: "numeric" });
  const categoryLabel = (code: string | null) =>
    code && t.has(`videos.categories.${code}`) ? t(`videos.categories.${code}`) : null;
  const currentCategory = categoryLabel(video.category);
  const trail = [
    { name: nav("home"), path: "/" },
    { name: t("videos.title"), path: "/videos" },
  ];

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [...trail, { name: video.title, path: pagePath }]),
          videoObject(locale, {
            slug: video.slug,
            title: video.title,
            youtubeVideoId: video.youtube_video_id,
            publishedAt: video.published_at,
            description: companion?.description ?? t("videos.intro"),
            articlePath,
            pagePath,
          }),
          related.length
            ? itemList(
                locale,
                related.map((item) => ({ name: item.title, path: videoHref(item.slug) })),
                t("videos.relatedHeading"),
              )
            : null,
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-8 md:px-8 md:py-10">
        <Breadcrumb trail={trail} current={video.title} label={t("guides.breadcrumb")} />

        <article className="mt-4 rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] sm:p-8">
          <div className="flex flex-wrap items-center gap-3 text-sm">
            {currentCategory && video.category ? (
              <Link
                href={videosHref({ category: video.category })}
                className="inline-flex min-h-9 items-center rounded-full border border-[var(--teal)]/30 bg-[var(--teal-soft)] px-3.5 font-semibold text-[var(--teal)]"
              >
                {currentCategory}
              </Link>
            ) : null}
            <time dateTime={video.published_at} className="text-[var(--muted)]">
              {date.format(new Date(video.published_at))}
            </time>
          </div>

          <h1 className="mt-3 text-2xl font-extrabold tracking-tight sm:text-3xl md:text-4xl">
            {video.title}
          </h1>

          <div className="mt-6">
            <VideoWatchPlayer
              youtubeVideoId={video.youtube_video_id}
              title={video.title}
              kind={video.kind}
              playLabel={t("videos.play", { title: video.title })}
            />
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">{t("videos.privacy")}</p>
          </div>

          <div className="mt-5 flex flex-wrap items-center gap-4">
            <a
              href={`https://www.youtube.com/watch?v=${video.youtube_video_id}`}
              target="_blank"
              rel="noopener noreferrer"
              className="inline-flex min-h-11 items-center gap-2 rounded-full border border-[var(--line)] bg-[var(--paper)] px-4 text-sm font-semibold text-[var(--ink)] transition-colors hover:border-[var(--teal)] hover:text-[var(--teal)]"
            >
              <ExternalLink size={16} aria-hidden />
              {t("videos.watchOnYoutube")}
            </a>
            <Link
              href="/videos"
              className="inline-flex min-h-11 items-center gap-2 text-sm font-semibold text-[var(--teal)] underline underline-offset-4"
            >
              <ArrowLeft size={16} aria-hidden />
              {t("videos.backToVideos")}
            </Link>
          </div>

          {articlePath ? (
            <section
              aria-labelledby="companion-article-heading"
              className="mt-8 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-5"
            >
              <p
                id="companion-article-heading"
                className="flex items-center gap-2 text-xs font-extrabold uppercase tracking-wider text-[var(--teal)]"
              >
                <FileText size={15} aria-hidden />
                {t("videos.companionArticleHeading")}
              </p>
              {companion ? (
                <>
                  <h2 className="mt-2 text-xl font-bold tracking-tight">
                    <Link
                      href={articlePath}
                      className="underline-offset-4 hover:text-[var(--teal)] hover:underline"
                    >
                      {companion.title}
                    </Link>
                  </h2>
                  {companion.description ? (
                    <p className="mt-2 leading-7 text-[var(--muted)]">{companion.description}</p>
                  ) : null}
                </>
              ) : null}
              <p className="mt-3">
                <Link
                  href={articlePath}
                  className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline underline-offset-4"
                >
                  {t("videos.readArticle")}
                </Link>
              </p>
            </section>
          ) : null}
        </article>

        {related.length ? (
          <section aria-labelledby="related-videos-heading" className="mt-12">
            <h2
              id="related-videos-heading"
              className="portal-section-heading border-b border-[var(--line)] pb-3 text-2xl font-extrabold tracking-tight"
            >
              {t("videos.relatedHeading")}
            </h2>
            <ul className="mt-6 grid gap-5 sm:grid-cols-2 lg:grid-cols-3">
              {related.map((item) => (
                <VideoCard
                  key={item.slug}
                  video={item}
                  date={date.format(new Date(item.published_at))}
                  labels={{
                    play: t("videos.play", { title: item.title }),
                    watchOnYoutube: t("videos.watchOnYoutube"),
                    readArticle: t("videos.readArticle"),
                    category: categoryLabel(item.category),
                  }}
                />
              ))}
            </ul>
          </section>
        ) : null}
      </main>
    </>
  );
}
