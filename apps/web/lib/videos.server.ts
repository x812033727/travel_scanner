import { cache } from "react";
import { publicServerHeaders } from "@/lib/public-server-fetch";
import { isPublicVideo, type PublicVideoPage, type VideoKind } from "@/lib/videos";

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
