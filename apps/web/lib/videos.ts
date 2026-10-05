import { guideHref, type GuideKind } from "@/lib/guides";

export const videoKinds = ["long", "shorts"] as const;
export type VideoKind = (typeof videoKinds)[number];

/** One published video, as `GET /videos` sends it. */
export type PublicVideo = {
  slug: string;
  title: string;
  youtube_video_id: string;
  category: string | null;
  kind: VideoKind;
  source_guide: string | null;
  source_guide_kind: GuideKind | null;
  published_at: string;
};

export type PublicVideoPage = {
  videos: PublicVideo[];
  next_cursor: string | null;
  categories: string[];
  /** False when the API did not answer: the page says so instead of claiming there is nothing. */
  available: boolean;
};

const YOUTUBE_ID = /^[A-Za-z0-9_-]{11}$/;
const GUIDE_KINDS = new Set(["intel", "howto", "life"]);

export function isPublicVideo(value: unknown): value is PublicVideo {
  const row = value as Record<string, unknown> | null;
  return Boolean(row)
    && typeof row!.slug === "string"
    && typeof row!.title === "string"
    && typeof row!.youtube_video_id === "string" && YOUTUBE_ID.test(row!.youtube_video_id)
    && (row!.kind === "long" || row!.kind === "shorts")
    && typeof row!.published_at === "string";
}

export function isVideoKind(value: unknown): value is VideoKind {
  return value === "long" || value === "shorts";
}

/** The article a video retells, or null when the API could not vouch for it. */
export function videoArticleHref(video: PublicVideo): string | null {
  return video.source_guide && video.source_guide_kind && GUIDE_KINDS.has(video.source_guide_kind)
    ? guideHref(video.source_guide_kind, video.source_guide)
    : null;
}

/** A listing address. Every `/videos` link comes from here so the filters compose one way. */
export function videosHref(filters: { category?: string | null; kind?: VideoKind | null; cursor?: string | null } = {}): string {
  const params = new URLSearchParams();
  if (filters.kind) params.set("kind", filters.kind);
  if (filters.category) params.set("category", filters.category);
  if (filters.cursor) params.set("cursor", filters.cursor);
  const query = params.toString();
  return query ? `/videos?${query}` : "/videos";
}
