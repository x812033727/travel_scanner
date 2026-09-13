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
 * Where the in-article unit goes inside one run of body blocks, or `null` for no ad here.
 *
 * The caller passes the article's first segment — the blocks before the editor's first
 * partner button — so this never has to reason about `offer` blocks itself.
 *
 * Constraints, in the order they bite:
 *   - Never above the hero, which is the LCP element: the cut is after the first level-2
 *     heading and its first paragraph. An article with no hero has far less above that
 *     point, so it needs `MIN_BLOCKS_BEFORE_WITHOUT_HERO` of body instead.
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
/**
 * A hero is optional, and it is most of what separates the headline from the first section.
 * Without one the cut below can land inside the opening viewport, so the reader meets the ad
 * before they have met the article. Require this much body above it instead.
 */
export const MIN_BLOCKS_BEFORE_WITHOUT_HERO = 3;

export function adsenseSplit<T extends { type: string; level?: number }>(
  blocks: readonly T[],
  { hasHero = true }: { hasHero?: boolean } = {},
): { before: T[]; after: T[]; headingStart: number } | null {
  const firstHeading = blocks.findIndex((block) => block.type === "heading" && block.level === 2);
  if (firstHeading < 0) return null;
  const firstParagraph = blocks.findIndex(
    (block, index) => index > firstHeading && block.type === "paragraph",
  );
  if (firstParagraph < 0) return null;
  const cut = hasHero
    ? firstParagraph + 1
    : Math.max(firstParagraph + 1, MIN_BLOCKS_BEFORE_WITHOUT_HERO);
  if (blocks.length - cut < MIN_BLOCKS_AFTER) return null;
  const before = blocks.slice(0, cut);
  return {
    before,
    after: blocks.slice(cut),
    headingStart: before.filter((b) => b.type === "heading" && b.level === 2).length,
  };
}
