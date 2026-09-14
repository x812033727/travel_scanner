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
  /**
   * A Google-certified consent message ("Privacy & messaging") is published in the AdSense
   * account, so the reader's own answer decides personalisation. False means the loader must
   * force non-personalised ads: serving personalised ads in the EEA, the UK or Switzerland
   * without a certified CMP is exactly what the programme policies forbid.
   */
  cmp_enabled: boolean;
};

export const disabledAdsense: AdsenseConfig = {
  enabled: false, publisher_id: null, slot_id: null, cmp_enabled: false,
};

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
    && typeof config.cmp_enabled === "boolean"
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
  return adsenseArticleRoute(pathname) !== null;
}

/**
 * The locale, kind and slug of an article URL, or `null` when the path is not one.
 *
 * Matching the shape is NOT enough to carry an ad: a URL of this shape whose article is
 * missing, unpublished or untranslated renders the "article unavailable" screen, and putting
 * advertising on that is the no-content-screen policy. The caller has to check.
 */
export function adsenseArticleRoute(
  pathname: string,
): { locale: string; kind: "intel" | "howto" | "life"; slug: string } | null {
  const path = pathname.split("?")[0].split("#")[0].replace(/\/+$/, "");
  const match = /^\/(en|ja|ko|zh-TW|zh-CN)\/(?:guides\/(intel|howto)|(life))\/([^/]+)$/.exec(path);
  if (!match) return null;
  const kind = (match[2] ?? match[3]) as "intel" | "howto" | "life";
  return { locale: match[1], kind, slug: match[4] };
}

/**
 * Everything about a request that can be decided from the request alone.
 *
 * `proxy.ts` and `lib/adsense.server.ts` both go through this so they cannot drift: a
 * request the renderer will refuse must not still get the relaxed policy. The renderer adds
 * one more condition on top — that the article actually exists — which needs an API read and
 * so cannot happen in the proxy.
 */
export function adsenseRequestGate(signals: {
  host: string | null;
  dnt: string | null;
  gpc: string | null;
  pathname: string;
}): { locale: string; kind: "intel" | "howto" | "life"; slug: string } | null {
  if (!isAdsenseOrigin(`https://${signals.host || ""}`)) return null;
  // The site's standing rule for third-party scripts: a browser asking not to be tracked gets
  // none of them — and therefore has no reason to be handed a loosened policy either.
  if (signals.dnt === "1" || signals.gpc === "1") return null;
  return adsenseArticleRoute(signals.pathname);
}

/**
 * Where the in-article units go: every segment of the body cut into pieces, with one unit
 * between each pair of pieces. A segment that carries no ad comes back as a single piece.
 *
 * The caller passes `splitGuideBlocks`' segments. Every boundary between two of them is an
 * editor's partner button or partner link, and the end of the body is followed by the
 * automatic partner panel, so those three places are what the clearance below is kept from.
 *
 * Constraints, in the order they bite:
 *   - Never above the hero, which is the LCP element: the first unit is no earlier than after
 *     the first level-2 heading and its first paragraph. An article with no hero has far less
 *     above that point, so it needs `MIN_BLOCKS_BEFORE_WITHOUT_HERO` of body instead.
 *   - Never beside a partner button: the programme policies forbid placing an ad next to an
 *     interactive element, and those buttons are the affiliate revenue this must not eat.
 *     `AD_CLEARANCE_BLOCKS` of body separate a unit from a button on either side of it, and
 *     from the end of the article.
 *   - Only after prose — a paragraph or a list — so a unit never splits a heading from its
 *     section or sits directly under an image or a table it could be mistaken for part of.
 *   - Never on a thin article. `MIN_BLOCKS_AFTER` blocks must follow the first unit.
 *   - Content first: `MIN_BLOCKS_BETWEEN` blocks between two units, and one unit per
 *     `BLOCKS_PER_AD` blocks of body up to `MAX_ADS`.
 *
 * Each piece's `headingStart` continues the level-2 numbering across every cut so
 * `ContentBlocks` keeps giving the table of contents the heading ids it already points at.
 */
export const MIN_BLOCKS_AFTER = 6;
/**
 * A hero is optional, and it is most of what separates the headline from the first section.
 * Without one the first unit can land inside the opening viewport, so the reader meets the ad
 * before they have met the article. Require this much body above it instead.
 */
export const MIN_BLOCKS_BEFORE_WITHOUT_HERO = 3;
export const AD_CLEARANCE_BLOCKS = 3;
export const MIN_BLOCKS_BETWEEN = 10;
export const BLOCKS_PER_AD = 12;
export const MAX_ADS = 3;

const PARAGRAPHS = new Set(["paragraph", "rich_paragraph"]);
const PROSE = new Set([...PARAGRAPHS, "list"]);

export type AdsensePiece<T> = { blocks: T[]; headingStart: number };

export function adsensePlacements<T extends { type: string; level?: number }>(
  segments: readonly { blocks: readonly T[]; headingStart: number }[],
  { hasHero = true }: { hasHero?: boolean } = {},
): AdsensePiece<T>[][] {
  const flat = segments.flatMap((segment) => segment.blocks);
  const cuts = segments.map((): number[] => []);
  const firstHeading = flat.findIndex((block) => block.type === "heading" && block.level === 2);
  const firstParagraph = firstHeading < 0
    ? -1
    : flat.findIndex((block, index) => index > firstHeading && PARAGRAPHS.has(block.type));
  if (firstParagraph >= 0) {
    const earliest = hasHero
      ? firstParagraph + 1
      : Math.max(firstParagraph + 1, MIN_BLOCKS_BEFORE_WITHOUT_HERO);
    const limit = Math.min(MAX_ADS, Math.max(1, Math.floor(flat.length / BLOCKS_PER_AD)));
    let placed = 0;
    let last = -Infinity;
    let offset = 0;
    segments.forEach((segment, segmentIndex) => {
      const { length } = segment.blocks;
      // `cut` is the index the unit goes before; 0 would put it straight after a button.
      for (let cut = 1; cut < length && placed < limit; cut += 1) {
        const position = offset + cut;
        if (position < earliest || position - last < MIN_BLOCKS_BETWEEN) continue;
        if (!PROSE.has(segment.blocks[cut - 1].type)) continue;
        if (segmentIndex > 0 && cut < AD_CLEARANCE_BLOCKS) continue;
        if (length - cut < AD_CLEARANCE_BLOCKS) continue;
        if (placed === 0 && flat.length - position < MIN_BLOCKS_AFTER) continue;
        cuts[segmentIndex].push(cut);
        placed += 1;
        last = position;
      }
      offset += length;
    });
  }
  return segments.map((segment, segmentIndex) => {
    const pieces: AdsensePiece<T>[] = [];
    let start = 0;
    let headingStart = segment.headingStart;
    for (const end of [...cuts[segmentIndex], segment.blocks.length]) {
      const blocks = segment.blocks.slice(start, end);
      pieces.push({ blocks, headingStart });
      headingStart += blocks.filter((block) => block.type === "heading" && block.level === 2).length;
      start = end;
    }
    return pieces;
  });
}
