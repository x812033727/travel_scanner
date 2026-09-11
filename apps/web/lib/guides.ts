import { isContentBlockList, type ContentBlock } from "./content-blocks";
import type { Locale } from "@/i18n/routing";

export const guideKinds = ["intel", "howto"] as const;
export type GuideKind = typeof guideKinds[number];

export function isGuideKind(value: unknown): value is GuideKind {
  return typeof value === "string" && (guideKinds as readonly string[]).includes(value);
}

/** Kind is part of the URL, so an article never moves between the two sections. */
export function guideHref(kind: GuideKind, slug: string): string {
  return `/guides/${kind}/${slug}`;
}

export type GuideTopic = { slug: string; label: string };

export type GuideSource = { title: string; url: string; checked_on: string | null };

export type GuideDocument = {
  title: string;
  description: string;
  blocks: ContentBlock[];
  sources: GuideSource[];
};

export type PublishedGuide = GuideDocument & { version: number; published_at: string };

export type GuideSummary = {
  slug: string;
  kind: GuideKind;
  destination_id: string | null;
  destination_label: string | null;
  topics: GuideTopic[];
  title: string;
  description: string;
  published_at: string;
  valid_until: string | null;
  featured: boolean;
};

export type GuideList = { articles: GuideSummary[]; next_cursor: string | null };

export type GuideArticleState = {
  slug: string;
  kind: GuideKind;
  locale: string;
  status: "published" | "unpublished" | "unavailable";
  destination_id: string | null;
  destination_label: string | null;
  topics: GuideTopic[];
  valid_until: string | null;
  expired: boolean;
  document: PublishedGuide | null;
  /** Only the locales genuinely published. The article page turns this into hreflang, so an
   *  unwritten translation is never advertised as one. */
  published_locales: Locale[];
};

function isTopicList(value: unknown): value is GuideTopic[] {
  return Array.isArray(value) && value.every((row) => {
    const topic = row as Record<string, unknown> | null;
    return !!topic && typeof topic.slug === "string" && typeof topic.label === "string";
  });
}

function isSourceList(value: unknown): value is GuideSource[] {
  return Array.isArray(value) && value.every((row) => {
    const source = row as Record<string, unknown> | null;
    return !!source && typeof source.title === "string" && typeof source.url === "string"
      && (source.checked_on === null || typeof source.checked_on === "string");
  });
}

export function isPublishedGuide(value: unknown): value is PublishedGuide {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  return typeof row.title === "string" && typeof row.description === "string"
    && typeof row.version === "number" && typeof row.published_at === "string"
    && isContentBlockList(row.blocks) && isSourceList(row.sources);
}

export function isGuideSummary(value: unknown): value is GuideSummary {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  return typeof row.slug === "string" && isGuideKind(row.kind)
    && typeof row.title === "string" && typeof row.description === "string"
    && typeof row.published_at === "string" && typeof row.featured === "boolean"
    && (row.destination_id === null || typeof row.destination_id === "string")
    && (row.destination_label === null || typeof row.destination_label === "string")
    && (row.valid_until === null || typeof row.valid_until === "string")
    && isTopicList(row.topics);
}

/** An `intel` notice past its own validity. It keeps its page; it just stops being current. */
export function isExpired(validUntil: string | null, today: Date = new Date()): boolean {
  if (!validUntil) return false;
  const cutoff = new Date(`${validUntil}T23:59:59Z`);
  return Number.isFinite(cutoff.getTime()) && cutoff.getTime() < today.getTime();
}
