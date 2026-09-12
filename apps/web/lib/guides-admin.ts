import type { GuideDocument, GuideKind, GuideTopic } from "@/lib/guides";
import type { SitePageLocale } from "@/lib/site-pages";

/** The editor-facing state the API computes once per article (`app/guides/publication.py`). */
export const articleStatuses = ["published", "draft", "hidden", "expired"] as const;
export type ArticleStatus = typeof articleStatuses[number];

export function isArticleStatus(value: unknown): value is ArticleStatus {
  return typeof value === "string" && (articleStatuses as readonly string[]).includes(value);
}

export type LocaleState = {
  locale: SitePageLocale;
  version: number;
  published_version: number | null;
  published_at: string | null;
  title: string;
  updated_at: string;
};

export type Revision = { id: string; version: number; action: string; created_at: string };

export type ArticleSummary = {
  id: string;
  slug: string;
  kind: GuideKind;
  destination_id: string | null;
  destination_label: string | null;
  topics: GuideTopic[];
  valid_until: string | null;
  expired: boolean;
  featured: boolean;
  display_order: number;
  is_active: boolean;
  status: ArticleStatus;
  version: number;
  locales: LocaleState[];
  updated_at: string;
};

export type ArticleDetail = ArticleSummary & {
  locale: SitePageLocale;
  draft: GuideDocument;
  published: (GuideDocument & { version: number; published_at: string }) | null;
  revisions: Revision[];
};

export type FacetCount = { code: string; count: number };

export type ArticleList = {
  articles: ArticleSummary[];
  total: number;
  page: number;
  pages: number;
  facets: { status: FacetCount[]; kind: FacetCount[] };
};

export type BatchVisibilityResult = {
  updated: number;
  skipped: number;
  status: "hidden" | "active";
  articles: ArticleSummary[];
};

/** `?article=` carries an id, and only an id: anything else falls back to the list. */
export function isUuid(value: string): boolean {
  return /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(value);
}

export function isPageNumber(value: string): boolean {
  return /^[1-9][0-9]{0,4}$/.test(value);
}
