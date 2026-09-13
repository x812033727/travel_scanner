/**
 * Google AdSense on article pages, and nowhere else.
 *
 * The split mirrors `lib/stay22-script.ts` / `lib/stay22-script.server.ts`: everything here
 * is pure and isomorphic so `proxy.ts` can import it, which rules out `next/headers`. The
 * per-request decision that needs request headers lives in `lib/adsense.server.ts`.
 */

export const ADSENSE_SCRIPT_ORIGIN = "https://pagead2.googlesyndication.com";

export type AdsenseConfig = {
  enabled: boolean;
  publisher_id: string | null;
  slot_id: string | null;
};

export const disabledAdsense: AdsenseConfig = { enabled: false, publisher_id: null, slot_id: null };

/** Google's shapes: `ca-pub-` plus 16 digits, and a 10-digit ad unit slot. */
export function isAdsensePublisherId(value: unknown): value is string {
  return typeof value === "string" && /^ca-pub-\d{16}$/.test(value);
}

export function isAdsenseSlotId(value: unknown): value is string {
  return typeof value === "string" && /^\d{10}$/.test(value);
}

export function validAdsenseConfig(value: unknown): value is AdsenseConfig {
  if (!value || typeof value !== "object") return false;
  const config = value as Partial<AdsenseConfig>;
  return typeof config.enabled === "boolean"
    && (config.publisher_id === null || isAdsensePublisherId(config.publisher_id))
    && (config.slot_id === null || isAdsenseSlotId(config.slot_id))
    && (!config.enabled || (isAdsensePublisherId(config.publisher_id) && isAdsenseSlotId(config.slot_id)));
}

export function isAdsenseOrigin(value: string): boolean {
  try {
    const url = new URL(value);
    return !url.username && !url.password
      && ["https://mokaair.com", "https://www.mokaair.com"].includes(url.origin);
  } catch { return false; }
}

/**
 * The only two page shapes that may carry an ad: a travel guide article and a life article.
 *
 * Everything else is excluded on purpose, and each for its own reason. Hubs and listings are
 * "no content" screens in the non-zh-TW locales, which the programme policies forbid. A shared
 * trip URL *is* its secret token, which a third-party script in the same document can read.
 * Community is behind a master switch and noindex. Account and trip pages are private.
 */
export function isAdsenseArticlePath(pathname: string): boolean {
  const path = pathname.split("?")[0].split("#")[0].replace(/\/+$/, "");
  return /^\/(?:en|ja|ko|zh-TW|zh-CN)\/(?:guides\/(?:intel|howto)|life)\/[^/]+$/.test(path);
}

/**
 * Where the in-article unit goes inside one run of body blocks, or `null` for no ad here.
 *
 * The caller passes the article's first segment — the blocks before the editor's first
 * partner button — so this never has to reason about `offer` blocks itself.
 *
 * Constraints, in the order they bite:
 *   - Never above the fold: the hero image is the LCP element, and a slot above it moves it.
 *     The cut is therefore after the first level-2 heading and its first paragraph.
 *   - Never beside a partner button: the programme policies forbid placing an ad next to an
 *     interactive element, and those buttons are the affiliate revenue this must not eat.
 *   - Never on a thin article. `MIN_BLOCKS_AFTER` blocks of real content must follow the
 *     slot in this same segment, which doubles as the clearance before the partner button
 *     that ends it: a short segment simply gets no ad.
 *
 * `headingStart` continues the level-2 numbering across the split so `ContentBlocks` keeps
 * giving the table of contents the heading ids it already points at.
 */
export const MIN_BLOCKS_AFTER = 6;

export function adsenseSplit<T extends { type: string; level?: number }>(
  blocks: readonly T[],
): { before: T[]; after: T[]; headingStart: number } | null {
  const firstHeading = blocks.findIndex((block) => block.type === "heading" && block.level === 2);
  if (firstHeading < 0) return null;
  const firstParagraph = blocks.findIndex(
    (block, index) => index > firstHeading && block.type === "paragraph",
  );
  if (firstParagraph < 0) return null;
  const cut = firstParagraph + 1;
  if (blocks.length - cut < MIN_BLOCKS_AFTER) return null;
  const before = blocks.slice(0, cut);
  return {
    before,
    after: blocks.slice(cut),
    headingStart: before.filter((b) => b.type === "heading" && b.level === 2).length,
  };
}
