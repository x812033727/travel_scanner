/**
 * The structured bodies the site renders.
 *
 * `ContentBlock` is the union managed site documents and travel guides share; it comes from
 * the same Pydantic block union in `apps/api/app/site_pages/schemas.py`, so both have one
 * type, one link sanitizer and one renderer. The sanitizer in particular is
 * security-critical: a second copy is a second thing to get wrong.
 *
 * `RichContentBlock` adds the guide-only blocks (`apps/api/app/guides/schemas.py`): a
 * self-hosted image with its licence, a table and a callout. They are a superset on purpose:
 * the renderer draws all of them, but a legal page's document is typed to the four shared
 * blocks and its editor never meets the rest.
 */

export type ContentBlock =
  | { type: "heading"; level: 2 | 3; text: string }
  | { type: "paragraph"; text: string }
  | { type: "list"; items: string[]; ordered: boolean }
  | { type: "link"; text: string; url: string };

export type ImageCredit = { author: string; license: string; source_url: string | null };
export type ImageBlock = {
  type: "image";
  src: string;
  alt: string;
  width: number;
  height: number;
  caption?: string;
  credit?: ImageCredit | null;
};
export type TableBlock = { type: "table"; header: string[]; rows: string[][]; caption?: string };
export const calloutTones = ["tip", "warning", "info"] as const;
export type CalloutTone = typeof calloutTones[number];
export type CalloutBlock = { type: "callout"; tone: CalloutTone; title?: string; text: string };

export type RichContentBlock = ContentBlock | ImageBlock | TableBlock | CalloutBlock;

export function contentBlockLink(raw: unknown): string | null {
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

/**
 * Self-hosted only: `/guides/<slug>/<name>.<ext>` under the web app's own `public/` folder,
 * the same grammar the API enforces on write. A path rather than a URL means an article can
 * never make a reader's browser fetch a picture from a third party.
 */
const IMAGE_SRC = /^\/guides\/[a-z0-9]+(?:-[a-z0-9]+)*\/[a-z0-9]+(?:-[a-z0-9]+)*\.(?:webp|jpg|png|svg)$/;

export function contentImageSrc(raw: unknown): string | null {
  return typeof raw === "string" && IMAGE_SRC.test(raw) ? raw : null;
}

/** The licence page a credit can link to, for the Creative Commons family only. Anything
 *  else ("© Mokaair", "Public domain") is shown as text. */
export function licenseUrl(license: string): string | null {
  const trimmed = license.trim();
  if (/^CC0 1\.0$/i.test(trimmed)) return "https://creativecommons.org/publicdomain/zero/1.0/";
  const cc = /^CC (BY(?:-SA|-NC|-ND|-NC-SA|-NC-ND)?) ([1-4]\.0)$/i.exec(trimmed);
  return cc ? `https://creativecommons.org/licenses/${cc[1].toLowerCase()}/${cc[2]}/` : null;
}

/** A stored side length: the API caps both dimensions so a typo cannot reserve a mile of page. */
export function isImageSize(value: unknown): value is number {
  return typeof value === "number" && Number.isInteger(value) && value >= 1 && value <= 4000;
}

function isOptionalText(value: unknown): boolean {
  return value === undefined || typeof value === "string";
}

export function isImageCredit(value: unknown): value is ImageCredit {
  if (!value || typeof value !== "object") return false;
  const credit = value as Record<string, unknown>;
  if (typeof credit.author !== "string" || typeof credit.license !== "string") return false;
  if (credit.source_url === null || credit.source_url === undefined) return true;
  const href = contentBlockLink(credit.source_url);
  return href !== null && !href.startsWith("mailto:");
}

export function isContentBlock(block: unknown): block is ContentBlock {
  if (!block || typeof block !== "object") return false;
  const entry = block as Record<string, unknown>;
  if (entry.type === "list") {
    return typeof entry.ordered === "boolean" && Array.isArray(entry.items)
      && entry.items.every((text) => typeof text === "string");
  }
  if (typeof entry.text !== "string") return false;
  if (entry.type === "heading") return entry.level === 2 || entry.level === 3;
  if (entry.type === "link") return contentBlockLink(entry.url) !== null;
  return entry.type === "paragraph";
}

export function isContentBlockList(value: unknown): value is ContentBlock[] {
  return Array.isArray(value) && value.every(isContentBlock);
}

export function isRichContentBlock(block: unknown): block is RichContentBlock {
  if (isContentBlock(block)) return true;
  if (!block || typeof block !== "object") return false;
  const entry = block as Record<string, unknown>;
  if (entry.type === "image") {
    return contentImageSrc(entry.src) !== null && typeof entry.alt === "string"
      && isImageSize(entry.width) && isImageSize(entry.height) && isOptionalText(entry.caption)
      && (entry.credit === null || entry.credit === undefined || isImageCredit(entry.credit));
  }
  if (entry.type === "table") {
    const header = entry.header;
    if (!Array.isArray(header) || !header.length || !header.every((cell) => typeof cell === "string")) return false;
    return Array.isArray(entry.rows) && isOptionalText(entry.caption)
      && entry.rows.every((row) => Array.isArray(row) && row.length === header.length
        && row.every((cell) => typeof cell === "string"));
  }
  if (entry.type === "callout") {
    return (calloutTones as readonly string[]).includes(entry.tone as string)
      && typeof entry.text === "string" && isOptionalText(entry.title);
  }
  return false;
}

export function isRichContentBlockList(value: unknown): value is RichContentBlock[] {
  return Array.isArray(value) && value.every(isRichContentBlock);
}
