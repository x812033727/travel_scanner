import type { Metadata } from "next";
import { guideArticleMetadata, renderGuideArticle } from "@/components/guides/article-page";
import type { Locale } from "@/i18n/routing";

type Params = { locale: Locale; slug: string };

/** A lifestyle article. The kind is fixed by the route, so no `[kind]` segment to validate. */
export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { locale, slug } = await params;
  return guideArticleMetadata({ locale, kind: "life", slug });
}

export default async function LifeArticlePage({ params }: { params: Promise<Params> }) {
  const { locale, slug } = await params;
  return renderGuideArticle({ locale, kind: "life", slug });
}
