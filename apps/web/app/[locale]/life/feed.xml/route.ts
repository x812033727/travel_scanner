import { getTranslations } from "next-intl/server";
import { NextResponse } from "next/server";
import { locales, type Locale } from "@/i18n/routing";
import { buildGuideAtomFeed } from "@/lib/guide-atom-feed";
import { NEWS_TOPICS, newsOrder } from "@/lib/guides";
import { loadGuideList } from "@/lib/guides.server";

export const dynamic = "force-dynamic";

const FEED_LIMIT = 25;
const isLocale = (value: string): value is Locale => (locales as readonly string[]).includes(value);

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ locale: string }> },
): Promise<NextResponse> {
  const { locale } = await params;
  if (!isLocale(locale)) {
    return new NextResponse("not found", { status: 404 });
  }

  const [lists, meta] = await Promise.all([
    Promise.all(
      NEWS_TOPICS.map((topic) =>
        loadGuideList(locale, { kind: "life", topic, sort: "news" }, FEED_LIMIT),
      ),
    ),
    getTranslations({ locale, namespace: "metadata" }),
  ]);

  if (lists.some((list) => !list.available)) {
    return new NextResponse("feed temporarily unavailable", {
      status: 503,
      headers: { "Retry-After": "600", "Content-Type": "text/plain; charset=utf-8" },
    });
  }

  const bySlug = new Map(
    lists
      .flatMap((list) => list.articles)
      .filter((article) => Boolean(article.news_date))
      .map((article) => [article.slug, article] as const),
  );
  const articles = [...bySlug.values()].sort(newsOrder).slice(0, FEED_LIMIT);

  const xml = buildGuideAtomFeed({
    locale,
    feedPath: "/life/feed.xml",
    hubPath: "/life",
    title: meta("lifeTitle"),
    subtitle: meta("lifeDescription"),
    articles,
  });

  return new NextResponse(xml, {
    headers: {
      "Content-Type": "application/atom+xml; charset=utf-8",
      "Cache-Control": "max-age=0, must-revalidate",
    },
  });
}
