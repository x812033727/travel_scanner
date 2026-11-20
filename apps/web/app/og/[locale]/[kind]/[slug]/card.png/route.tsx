import { NextResponse } from "next/server";
import { locales, type Locale } from "@/i18n/routing";
import { renderEditorialOgCard } from "@/lib/editorial-og-card";
import { isGuideKind } from "@/lib/guides";
import { getGuideArticle } from "@/lib/guides.server";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

const SLUG_PATTERN = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

/**
 * Dynamic 1200x630 editorial Open Graph / Google Discover card for published articles that do
 * not carry bespoke photography.
 */
export async function GET(
  _request: Request,
  { params }: { params: Promise<{ locale: string; kind: string; slug: string }> },
): Promise<Response> {
  const { locale, kind, slug } = await params;
  if (!(locales as readonly string[]).includes(locale) || !isGuideKind(kind) || !SLUG_PATTERN.test(slug)) {
    return new NextResponse("not found", { status: 404 });
  }

  const state = await getGuideArticle(kind, slug, locale as Locale);
  if (state.status !== "published" || !state.document) {
    return new NextResponse("not found", { status: 404 });
  }

  return renderEditorialOgCard({
    locale: locale as Locale,
    title: state.document.title,
    description: state.document.description,
    badge: state.topics[0]?.label?.trim() || (state.news_date ? "NEWS" : "MOKAAIR"),
    meta: state.news_date || state.document.published_at.slice(0, 10),
  });
}
