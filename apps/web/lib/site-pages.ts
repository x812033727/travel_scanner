import { contentBlockLink, isContentBlockList, type ContentBlock } from "./content-blocks";

export const sitePageSlugs = ["privacy", "terms", "about", "contact"] as const;
export type SitePageSlug = typeof sitePageSlugs[number];
export const sitePageLocales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
export type SitePageLocale = typeof sitePageLocales[number];
export const requirementKeys = ["operator", "location", "contact", "retention", "legal"] as const;
export type RequirementKey = typeof requirementKeys[number];
// The block union and its link sanitizer are shared with travel guides; both bodies come
// from the same Pydantic union in apps/api/app/site_pages/schemas.py. One definition, so a
// tightened rule cannot reach one surface and miss the other.
export type SitePageBlock = ContentBlock;
export type SitePageDocument = {
  title: string;
  description: string;
  blocks: SitePageBlock[];
  effective_date: string | null;
  requirements: Record<RequirementKey, string>;
};
export type PublishedSitePage = SitePageDocument & { version: number; published_at: string };
export type SitePageRevision = { id: string; version: number; action: string; created_at: string; created_by_user_id: string | null };
export type SitePageDetail = {
  slug: SitePageSlug; locale: SitePageLocale; version: number;
  draft: SitePageDocument; published: PublishedSitePage | null;
  pending_requirements: string[];
  revisions: SitePageRevision[];
  audit: Array<{ id: string; action: string; created_at: string; actor_user_id: string | null }>;
};
export type SitePagePublicState = {
  slug: SitePageSlug; locale: string;
  status: "published" | "unpublished" | "unavailable";
  document: PublishedSitePage | null;
};

export const sitePageLink = contentBlockLink;

export function isSitePageDocument(value: unknown): value is SitePageDocument {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  if (typeof row.title !== "string" || typeof row.description !== "string"
      || !(row.effective_date === null || typeof row.effective_date === "string")
      || !row.requirements || typeof row.requirements !== "object"
      || !requirementKeys.every((key) => typeof (row.requirements as Record<string, unknown>)[key] === "string")
      || !isContentBlockList(row.blocks)) return false;
  return true;
}
