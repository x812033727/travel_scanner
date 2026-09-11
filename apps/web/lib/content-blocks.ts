/**
 * The structured body shared by managed site documents and travel guides.
 *
 * Both come from the same Pydantic block union in `apps/api/app/site_pages/schemas.py`, so
 * they share one type, one link sanitizer and one renderer. The sanitizer in particular is
 * security-critical: a second copy is a second thing to get wrong.
 */

export type ContentBlock =
  | { type: "heading"; level: 2 | 3; text: string }
  | { type: "paragraph"; text: string }
  | { type: "list"; items: string[]; ordered: boolean }
  | { type: "link"; text: string; url: string };

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
