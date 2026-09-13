import type { Metadata, ResolvingMetadata } from "next";
import { notFound } from "next/navigation";
import { guideArticleMetadata, renderGuideArticle } from "@/components/guides/article-page";
import type { Locale } from "@/i18n/routing";
import { isTravelGuideKind } from "@/lib/guides";

type Params = { locale: Locale; kind: string; slug: string };

/** `[kind]` holds the two travel kinds only. `/guides/life/{slug}` is a 404, not a second
 *  address for a lifestyle article, which lives at `/life/{slug}`. */
async function resolve(params: Promise<Params>) {
  const { locale, kind, slug } = await params;
  if (!isTravelGuideKind(kind)) notFound();
  return { locale, kind, slug };
}

export async function generateMetadata(
  { params }: { params: Promise<Params> }, parent?: ResolvingMetadata,
): Promise<Metadata> {
  // The layout's social defaults are handed through so an article with a hero can replace
  // only the image; Next replaces a whole top-level key, never merges inside it.
  return guideArticleMetadata(await resolve(params), parent);
}

export default async function GuideArticlePage({ params }: { params: Promise<Params> }) {
  // Awaited, not rendered as an element: the route hands back a finished tree, which is
  // what keeps both this page and its test looking at the same thing.
  return renderGuideArticle(await resolve(params));
}
