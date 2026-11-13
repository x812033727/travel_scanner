import { getTranslations } from "next-intl/server";
import { NextResponse } from "next/server";
import { locales, type Locale } from "@/i18n/routing";
import { buildGuideAtomFeed } from "@/lib/guide-atom-feed";
import { isNewsTopic } from "@/lib/guides";
import { loadGuideList, loadGuideTopicList } from "@/lib/guides.server";

export const dynamic = "force-dynamic";

const FEED_LIMIT = 25;
const isLocale = (value: string): value is Locale => (locales as readonly string[]).includes(value);

export async function GET(
  _request: Request,
  { params }: { params: Promise<{ locale: string; topic: string }> },
): Promise<NextResponse> {
  const { locale, topic } = await params;
  if (!isLocale(locale) || !isNewsTopic("life", topic)) {
    return new NextResponse("not found", { status: 404 });
  }

  const [list, topicList, meta] = await Promise.all([
    loadGuideList(locale, { kind: "life", topic, sort: "news" }, FEED_LIMIT),
    loadGuideTopicList(locale, "life"),
    getTranslations({ locale, namespace: "metadata" }),
  ]);

  if (!list.available || !topicList.available) {
    return new NextResponse("feed temporarily unavailable", {
      status: 503,
      headers: { "Retry-After": "600", "Content-Type": "text/plain; charset=utf-8" },
    });
  }

  const matched = topicList.topics.find((item) => item.slug === topic);
  const label = matched?.label ?? topic;
  const xml = buildGuideAtomFeed({
    locale,
    feedPath: `/life/topics/${encodeURIComponent(topic)}/feed.xml`,
    hubPath: `/life/topics/${encodeURIComponent(topic)}`,
    title: meta("topicHubTitle", { topic: label }),
    subtitle: matched?.description || meta("topicHubDescription", { topic: label }),
    articles: list.articles.filter((article) => Boolean(article.news_date)),
  });

  return new NextResponse(xml, {
    headers: {
      "Content-Type": "application/atom+xml; charset=utf-8",
      "Cache-Control": "max-age=0, must-revalidate",
    },
  });
}
