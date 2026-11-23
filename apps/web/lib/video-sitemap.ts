import { defaultLocale } from "@/i18n/routing";
import { localeUrl } from "@/lib/seo";
import { videoHref, type PublicVideo } from "@/lib/videos";
import { getAllPublishedVideos } from "@/lib/videos.server";

const escapeXml = (value: string) =>
  value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&apos;");

function toIso(value: string): string | null {
  const parsed = new Date(value);
  return Number.isNaN(parsed.getTime()) ? null : parsed.toISOString();
}

export type VideoSitemapEntry = {
  url: string;
  thumbnailUrl: string;
  title: string;
  description: string;
  playerUrl: string;
  publicationDate: string;
};

/**
 * Renders a standards-compliant Google Video Sitemap (`sitemap-video/1.1`).
 * Each entry points at the dedicated canonical watch page (`/${defaultLocale}/videos/[slug]`)
 * with its YouTube thumbnail, nocookie embed player and publication timestamp.
 */
export function renderVideoSitemapXml(entries: readonly VideoSitemapEntry[]): string {
  const body = entries.map((entry) => [
    "  <url>",
    `    <loc>${escapeXml(entry.url)}</loc>`,
    "    <video:video>",
    `      <video:thumbnail_loc>${escapeXml(entry.thumbnailUrl)}</video:thumbnail_loc>`,
    `      <video:title>${escapeXml(entry.title)}</video:title>`,
    `      <video:description>${escapeXml(entry.description)}</video:description>`,
    `      <video:player_loc>${escapeXml(entry.playerUrl)}</video:player_loc>`,
    `      <video:publication_date>${entry.publicationDate}</video:publication_date>`,
    "      <video:family_friendly>yes</video:family_friendly>",
    "    </video:video>",
    "  </url>",
  ].join("\n"));

  return [
    '<?xml version="1.0" encoding="UTF-8"?>',
    '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:video="http://www.google.com/schemas/sitemap-video/1.1">',
    ...body,
    "</urlset>",
    "",
  ].join("\n");
}

export function videoToSitemapEntry(video: PublicVideo): VideoSitemapEntry | null {
  const publicationDate = toIso(video.published_at);
  if (!publicationDate) return null;
  const id = video.youtube_video_id;
  return {
    url: localeUrl(defaultLocale, videoHref(video.slug)),
    thumbnailUrl: `https://i.ytimg.com/vi/${id}/hqdefault.jpg`,
    title: video.title,
    description: video.title,
    playerUrl: `https://www.youtube-nocookie.com/embed/${id}`,
    publicationDate,
  };
}

export async function loadVideoSitemap(): Promise<{
  available: boolean;
  entries: VideoSitemapEntry[];
}> {
  const result = await getAllPublishedVideos(defaultLocale);
  if (!result.available) return { available: false, entries: [] };
  const entries = result.videos
    .map(videoToSitemapEntry)
    .filter((entry): entry is VideoSitemapEntry => entry !== null);
  return { available: true, entries };
}
