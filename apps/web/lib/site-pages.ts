export const sitePageSlugs = ["privacy", "terms", "about", "contact"] as const;
export type SitePageSlug = typeof sitePageSlugs[number];
export const sitePageLocales = ["zh-TW", "zh-CN", "en", "ja", "ko"] as const;
export type SitePageLocale = typeof sitePageLocales[number];
export const requirementKeys = ["operator", "location", "contact", "retention", "legal"] as const;
export type RequirementKey = typeof requirementKeys[number];
export type SitePageBlock =
  | { type: "heading"; level: 2 | 3; text: string }
  | { type: "paragraph"; text: string }
  | { type: "list"; items: string[]; ordered: boolean }
  | { type: "link"; text: string; url: string };
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

export function sitePageLink(raw: unknown): string | null {
  if (typeof raw !== "string" || !raw.trim() || /[\s\\\u0000-\u001f\u007f-\u009f]/.test(raw)) return null;
  try {
    const url = new URL(raw);
    if (url.username || url.password) return null;
    if (url.protocol === "mailto:") {
      const address = decodeURIComponent(url.pathname);
      return !url.search && !url.hash && !url.host && !/[\u0000-\u001f\u007f-\u009f]/.test(address)
        && /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(address) ? url.href : null;
    }
    return ["https:", "http:"].includes(url.protocol) && url.hostname ? url.href : null;
  } catch { return null; }
}

export function isSitePageDocument(value: unknown): value is SitePageDocument {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  if (typeof row.title !== "string" || typeof row.description !== "string"
      || !(row.effective_date === null || typeof row.effective_date === "string")
      || !row.requirements || typeof row.requirements !== "object"
      || !requirementKeys.every((key) => typeof (row.requirements as Record<string, unknown>)[key] === "string")
      || !Array.isArray(row.blocks)) return false;
  return row.blocks.every((block: unknown) => {
    if (!block || typeof block !== "object") return false;
    const entry = block as Record<string, unknown>;
    if (entry.type === "list") return typeof entry.ordered === "boolean" && Array.isArray(entry.items) && entry.items.every((text) => typeof text === "string");
    if (typeof entry.text !== "string") return false;
    if (entry.type === "heading") return entry.level === 2 || entry.level === 3;
    if (entry.type === "link") return sitePageLink(entry.url) !== null;
    return entry.type === "paragraph";
  });
}
