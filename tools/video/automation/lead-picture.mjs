// The lead story's official picture for a daily brief's thumbnail (ticket
// 2026-10-30-daily-brief-thumbnails-carry-the-lead). The thumbnail's picture box on the right
// went out empty on the first briefs; the owner asked for the product's own announcement image
// there, credited (SKILL.md rule 6 allows a product's official page or image as the subject of a
// news commentary, with the source named).
import { EDITORIAL_USER_AGENT } from "./fetch.mjs";

export const LEAD_PICTURE_FILE = "lead.jpg";
export const LEAD_PICTURE_LICENSE = "Official announcement image of the product, quoted as the subject of a news commentary thumbnail with the source credited";
const MAX_PAGE_BYTES = 3 * 1024 * 1024;
const MAX_IMAGE_BYTES = 10 * 1024 * 1024;
const TIMEOUT_MS = 20_000;
// The thumbnail's picture box is the right 60% of a 1280×720 frame (theme.css .thumb-subject),
// drawn here at twice that so it stays sharp. A wide announcement image is fitted whole over a
// blurred copy of itself, so its wordmark is not cropped by the box's object-fit: cover.
const BOX = { width: 1536, height: 1440 };
export const PAD_FILTER = `[0]format=rgb24,split[a][b];[a]scale=${BOX.width}:${BOX.height}:force_original_aspect_ratio=increase,crop=${BOX.width}:${BOX.height},boxblur=40:4[bg];[b]scale=${BOX.width}:${BOX.height}:force_original_aspect_ratio=decrease[fg];[bg][fg]overlay=(W-w)/2:(H-h)/2`;

const attr = (tag, name) => tag.match(new RegExp(`\\b${name}\\s*=\\s*(?:"([^"]*)"|'([^']*)')`, "i"))?.slice(1).find((value) => value !== undefined) ?? null;
const decode = (text) => text.replaceAll("&amp;", "&").replaceAll("&quot;", '"').replaceAll("&#39;", "'").replaceAll("&lt;", "<").replaceAll("&gt;", ">");

/** The page's og:image (or twitter:image), as an absolute https URL, or null. */
export function pageImage(html, base) {
  const found = {};
  for (const tag of String(html ?? "").match(/<meta\b[^>]*>/gi) ?? []) {
    const key = (attr(tag, "property") ?? attr(tag, "name") ?? "").toLowerCase();
    const content = attr(tag, "content");
    if (content && ["og:image", "og:image:url", "og:image:secure_url", "twitter:image", "twitter:image:src"].includes(key) && !found[key]) found[key] = decode(content.trim());
  }
  const raw = found["og:image:secure_url"] ?? found["og:image"] ?? found["og:image:url"] ?? found["twitter:image"] ?? found["twitter:image:src"];
  if (!raw) return null;
  try {
    const url = new URL(raw, base);
    return url.protocol === "https:" ? url.href : null;
  } catch {
    return null;
  }
}

/**
 * The source a brief's lead story is told from: the first of `video.sources` that is not this
 * site's own article (the brief's stories are the site's articles; its sources are the official
 * pages they rest on). Null when there is none.
 */
export function leadSource(video) {
  for (const source of Array.isArray(video?.sources) ? video.sources : []) {
    try {
      const url = new URL(source?.url);
      if (url.protocol === "https:" && !/(^|\.)mokaair\.com$/i.test(url.hostname)) return { url: url.href, title: String(source.title ?? "") };
    } catch {
      // Not a URL; the next one.
    }
  }
  return null;
}

async function fetchBytes(fetchImpl, url, accept, limit) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const response = await fetchImpl(url, { headers: { "User-Agent": EDITORIAL_USER_AGENT, Accept: accept }, redirect: "follow", signal: controller.signal });
    if (!response.ok) throw new Error(`HTTP ${response.status} from ${url}`);
    const bytes = new Uint8Array(await response.arrayBuffer());
    if (bytes.length > limit) throw new Error(`${url} is larger than ${Math.round(limit / 1024 / 1024)} MB`);
    return { bytes, type: response.headers.get("content-type") ?? "", url: response.url || url };
  } catch (error) {
    throw new Error(error.name === "AbortError" ? `${url} timed out` : error.message);
  } finally {
    clearTimeout(timer);
  }
}

/**
 * Find and download the lead source's picture: { page, image, bytes }. Throws with the reason
 * when there is no picture to use.
 */
export async function findLeadPicture(fetchImpl, video) {
  const lead = leadSource(video);
  if (!lead) throw new Error("the script names no official source");
  const page = await fetchBytes(fetchImpl, lead.url, "text/html,application/xhtml+xml;q=0.9,*/*;q=0.5", MAX_PAGE_BYTES);
  if (!/html/i.test(page.type)) throw new Error(`${lead.url} is not an HTML page (${page.type || "no type"})`);
  const image = pageImage(new TextDecoder("utf-8").decode(page.bytes), page.url);
  if (!image) throw new Error(`${lead.url} has no og:image`);
  const file = await fetchBytes(fetchImpl, image, "image/png,image/jpeg,image/webp;q=0.9", MAX_IMAGE_BYTES);
  if (!/^image\/(png|jpe?g|webp)\b/i.test(file.type)) throw new Error(`${image} is not a PNG, JPEG or WebP image (${file.type || "no type"})`);
  return { page: lead.url, image, bytes: file.bytes };
}
