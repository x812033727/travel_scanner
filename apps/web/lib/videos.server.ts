import { cache } from "react";
import { publicServerHeaders } from "@/lib/public-server-fetch";
import {
  isPublicVideo,
  type PublicVideo,
  type PublicVideoDetailResult,
  type PublicVideoPage,
  type VideoKind,
} from "@/lib/videos";

function apiBase() {
  return (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
}

export type VideoFilters = { category?: string; kind?: VideoKind; guide?: string; cursor?: string };

/** One page of published videos; an unreachable API is `available: false`, never a throw. */
async function loadVideos(locale: string, filters: VideoFilters, limit = 24): Promise<PublicVideoPage> {
  const params = new URLSearchParams({ limit: String(limit) });
  for (const [key, value] of Object.entries(filters)) if (value) params.set(key, value);
  try {
    const response = await fetch(`${apiBase()}/api/v1/videos?${params}`, {
      cache: "no-store",
      signal: AbortSignal.timeout(3000),
      headers: await publicServerHeaders(locale),
    });
    const body = (await response.json().catch(() => null)) as Record<string, unknown> | null;
    if (!response.ok || !body || !Array.isArray(body.videos)) throw new Error("unavailable");
    return {
      videos: body.videos.filter(isPublicVideo),
      next_cursor: typeof body.next_cursor === "string" ? body.next_cursor : null,
      categories: Array.isArray(body.categories) ? body.categories.filter((item): item is string => typeof item === "string") : [],
      available: true,
    };
  } catch {
    return { videos: [], next_cursor: null, categories: [], available: false };
  }
}

export const getVideos = cache(loadVideos);

/** One published video and its related picks for `/videos/[slug]`. */
async function loadVideo(locale: string, slug: string): Promise<PublicVideoDetailResult> {
  try {
    const response = await fetch(`${apiBase()}/api/v1/videos/${encodeURIComponent(slug)}`, {
      cache: "no-store",
      signal: AbortSignal.timeout(3000),
      headers: await publicServerHeaders(locale),
    });
    if (response.status === 404) return { status: "not_found" };
    const body = (await response.json().catch(() => null)) as Record<string, unknown> | null;
    if (!response.ok || !body || !isPublicVideo(body.video)) return { status: "unavailable" };
    const related = Array.isArray(body.related) ? body.related.filter(isPublicVideo) : [];
    return { status: "found", video: body.video, related };
  } catch {
    return { status: "unavailable" };
  }
}

export const getVideo = cache(loadVideo);

/** Walks published video pages up to `maxPages` (max 480 videos) for `/sitemap-videos.xml`. */
export async function getAllPublishedVideos(
  locale: string,
  maxPages = 10,
): Promise<{ available: boolean; videos: PublicVideo[] }> {
  const videos: PublicVideo[] = [];
  const seen = new Set<string>();
  let cursor: string | undefined;

  for (let page = 0; page < maxPages; page += 1) {
    const result = await loadVideos(locale, { cursor }, 48);
    if (!result.available) return { available: false, videos: [] };
    for (const item of result.videos) {
      if (seen.has(item.slug)) continue;
      seen.add(item.slug);
      videos.push(item);
    }
    if (!result.next_cursor || result.next_cursor === cursor) break;
    cursor = result.next_cursor;
  }

  return { available: true, videos };
}
