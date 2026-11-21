import { NextResponse } from "next/server";
import { getTranslations } from "next-intl/server";
import { locales, type Locale } from "@/i18n/routing";
import { renderEditorialOgCard } from "@/lib/editorial-og-card";
import { guideSections, isNewsTopic, type GuideSection } from "@/lib/guides";
import { getGuideTopicList } from "@/lib/guides.server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const SLUG_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/**
 * Dynamic 1200x630 editorial Open Graph / Google Discover card for a published topic hub.
 * Reads the topic vocabulary from the API so arbitrary strings cannot be rendered on this origin.
 */
export async function GET(
  _request: Request,
  { params }: { params: Promise<{ locale: string; section: string; topic: string }> },
): Promise<Response> {
  const { locale, section, topic: topicSlug } = await params;
  if (
    !(locales as readonly string[]).includes(locale)
    || !(guideSections as readonly string[]).includes(section)
    || !SLUG_PATTERN.test(topicSlug)
  ) {
    return new NextResponse("not found", { status: 404 });
  }

  const typedLocale = locale as Locale;
  const typedSection = section as GuideSection;
  const [vocabulary, metaT, commonT] = await Promise.all([
    getGuideTopicList(typedLocale, typedSection),
    getTranslations({ locale: typedLocale, namespace: "metadata" }),
    getTranslations({ locale: typedLocale, namespace: "common" }),
  ]);

  const found = vocabulary.topics.find((item) => item.slug === topicSlug);
  if (!found || (found.count !== undefined && found.count === 0)) {
    return new NextResponse("not found", { status: 404 });
  }

  const news = isNewsTopic(typedSection, topicSlug);
  const title = metaT(news ? `newsTopic-${topicSlug}-title` : "topicHubTitle", { topic: found.label })
    .replace(/\s*\|\s*Mokaair$/, "");
  const description = found.description || (news
    ? metaT(`newsTopic-${topicSlug}-description`)
    : metaT("topicHubDescription", { topic: found.label }));
  const badge = typedSection === "travel" ? commonT("guides.hubTitle") : commonT("guides.lifeHubTitle");

  return renderEditorialOgCard({
    locale: typedLocale,
    title,
    description,
    badge,
    meta: found.label,
  });
}
