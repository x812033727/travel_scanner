import type { AffiliateModule } from "@/components/affiliate-partner-options";
import {
  contentBlockLink,
  contentImageSrc,
  isImageCredit,
  isImageSize,
  isRichContentBlock,
  type FaqBlock,
  type ImageCredit,
  type RichContentBlock,
  type SummaryBlock,
} from "./content-blocks";
import type { Locale } from "@/i18n/routing";
import type { ArticleReference, SeriesNavigation } from "./guide-series";

export const guideKinds = ["intel", "howto", "life"] as const;
export type GuideKind = typeof guideKinds[number];

/** The two kinds that live under `/guides`; `life` has its own section at `/life`. */
export const travelGuideKinds = ["intel", "howto"] as const;
export type TravelGuideKind = typeof travelGuideKinds[number];

export const guideSections = ["travel", "life"] as const;
export type GuideSection = typeof guideSections[number];

export function isGuideKind(value: unknown): value is GuideKind {
  return typeof value === "string" && (guideKinds as readonly string[]).includes(value);
}

export function isTravelGuideKind(value: unknown): value is TravelGuideKind {
  return typeof value === "string" && (travelGuideKinds as readonly string[]).includes(value);
}

export function isGuideSection(value: unknown): value is GuideSection {
  return typeof value === "string" && (guideSections as readonly string[]).includes(value);
}

/** Which public section a kind belongs to: intel and howto are travel, life is its own. */
export function guideSection(kind: GuideKind): GuideSection {
  return kind === "life" ? "life" : "travel";
}

/**
 * Kind fixes the URL: travel articles live at `/guides/{kind}/{slug}`, lifestyle articles at
 * `/life/{slug}`. An article never has two URLs, and `/guides/life/...` is a 404.
 */
export function guideHref(kind: GuideKind, slug: string): string {
  return kind === "life" ? `/life/${slug}` : `/guides/${kind}/${slug}`;
}

/** The listing a kind belongs to, optionally filtered by topic. Every listing URL comes from here. */
export function guideListHref(kind: GuideKind, topic?: string | null): string {
  const base = kind === "life" ? "/life" : `/guides/${kind}`;
  return topic ? `${base}?topic=${encodeURIComponent(topic)}` : base;
}

/**
 * The hub page of one topic: `/guides/topics/{topic}` for the travel vocabulary and
 * `/life/topics/{topic}` for the lifestyle one. A `?topic=` listing is the same collection
 * and canonicalizes here; a chip links here directly.
 */
export function guideTopicHref(section: GuideSection, topic: string): string {
  return `${section === "life" ? "/life" : "/guides"}/topics/${encodeURIComponent(topic)}`;
}

/** The section hub a topic hub sits under, for its breadcrumb and its "all topics" chip. */
export function sectionHubHref(section: GuideSection): string {
  return section === "life" ? "/life" : "/guides";
}

/**
 * `section` is optional on the wire so a catalogue served by an older API still parses; so
 * are the two-level fields. `parent` names the parent topic of a sub-topic; `count` is how
 * many articles the request locale publishes under the topic (a parent counts its children's
 * too) and `counts` the same per locale, which is what a hub page decides its hreflang from.
 */
export type GuideTopic = {
  slug: string;
  label: string;
  section?: GuideSection;
  parent?: string | null;
  description?: string | null;
  count?: number;
  counts?: Record<string, number>;
};

/** One destination with at least one published article, for the travel hub's country groups. */
export type DestinationFacet = {
  id: string;
  label: string;
  country: string;
  country_label: string;
  count: number;
};

export function isDestinationFacet(value: unknown): value is DestinationFacet {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  return typeof row.id === "string" && typeof row.label === "string"
    && typeof row.country === "string" && typeof row.country_label === "string"
    && Number.isInteger(row.count) && Number(row.count) >= 0;
}

/** The locales a topic publishes in, in the site's own order, from the API's per-locale counts. */
export function topicLocales(topic: Pick<GuideTopic, "counts">, all: readonly Locale[]): Locale[] {
  const counts = topic.counts ?? {};
  return all.filter((locale) => (counts[locale] ?? 0) > 0);
}

export type GuideSource = { title: string; url: string; checked_on: string | null };

// --- the guide-only blocks ---------------------------------------------------------------

/** The partner modules an editor may place mid-article: the catalog's own five. */
export const offerModules = ["flight", "hotel", "activities", "transport", "connectivity"] as const;

/**
 * A partner button placed by the editor next to the paragraph that earns it. Which brands
 * show is still the catalog's decision; `destination_id` overrides the article's own so a
 * cross-destination notice can point each section at its city.
 */
export type OfferBlock = {
  type: "offer";
  module: AffiliateModule;
  destination_id: string | null;
  heading?: string;
};

/**
 * A link to a non-travel affiliate program (hosting, books, courses, software), placed by the
 * editor. Only the shape is checked here. Whether the partner is known and the URL is its own
 * is the API's call (`apps/api/app/affiliates/content_links.py`), delivered as the article's
 * `partner_links`; a block with no matching entry draws nothing, so the web never keeps a
 * second copy of the partner list.
 */
export type PartnerLinkBlock = { type: "partner_link"; partner: string; url: string; label: string; note?: string };

/** One partner link the API resolved for this article; `key` names it for the click count. */
export type GuidePartnerLink = { key: string; partner: string; display_name: string; url: string };

/** A partner program an editor may pick, as `GET /admin/guides/partners` lists it. */
export type ContentPartnerOption = { code: string; display_name: string; category: string; hosts: string[] };

export type GuideBlock = RichContentBlock | OfferBlock | PartnerLinkBlock;

/** The article's own picture: a self-hosted raster, because it doubles as the social card. */
export type GuideHero = { src: string; alt: string; width: number; height: number; credit: ImageCredit | null };

export function isOfferBlock(value: unknown): value is OfferBlock {
  if (!value || typeof value !== "object") return false;
  const entry = value as Record<string, unknown>;
  return entry.type === "offer"
    && (offerModules as readonly string[]).includes(entry.module as string)
    && (entry.destination_id === null || entry.destination_id === undefined || typeof entry.destination_id === "string")
    && (entry.heading === undefined || typeof entry.heading === "string");
}

/** An https link, the same rule the API applies to both the block and the resolved entry. */
function httpsLink(raw: unknown): string | null {
  const href = contentBlockLink(raw);
  return href?.startsWith("https:") ? href : null;
}

export function isPartnerLinkBlock(value: unknown): value is PartnerLinkBlock {
  if (!value || typeof value !== "object") return false;
  const entry = value as Record<string, unknown>;
  // Any code-shaped partner passes: a program since removed from the registry must leave the
  // document readable and simply find no entry in `partner_links`.
  return entry.type === "partner_link" && typeof entry.partner === "string"
    && httpsLink(entry.url) !== null && typeof entry.label === "string"
    && (entry.note === undefined || typeof entry.note === "string");
}

const PARTNER_LINK_KEY = /^[0-9a-f]{16}$/;

export function isGuidePartnerLink(value: unknown): value is GuidePartnerLink {
  if (!value || typeof value !== "object") return false;
  const entry = value as Record<string, unknown>;
  return typeof entry.key === "string" && PARTNER_LINK_KEY.test(entry.key)
    && typeof entry.partner === "string" && typeof entry.display_name === "string"
    && httpsLink(entry.url) !== null;
}

/** Where a partner-link click is counted: through the BFF, so it carries this site's Origin. */
export function partnerClickPath(kind: GuideKind, slug: string, locale: string, key: string): string {
  return `/api/travel/guides/${kind}/${encodeURIComponent(slug)}/partner-links/${key}/click?locale=${encodeURIComponent(locale)}`;
}

export function isGuideBlock(value: unknown): value is GuideBlock {
  return isRichContentBlock(value) || isOfferBlock(value) || isPartnerLinkBlock(value);
}

export function isGuideBlockList(value: unknown): value is GuideBlock[] {
  return Array.isArray(value) && value.every(isGuideBlock);
}

const HERO_SRC = /\.(?:webp|jpg|png)$/;

export function isGuideHero(value: unknown): value is GuideHero {
  if (!value || typeof value !== "object") return false;
  const hero = value as Record<string, unknown>;
  const src = contentImageSrc(hero.src);
  return src !== null && HERO_SRC.test(src) && typeof hero.alt === "string"
    && isImageSize(hero.width) && isImageSize(hero.height)
    && (hero.credit === null || hero.credit === undefined || isImageCredit(hero.credit));
}

/** Absent from the wire (an older API) and explicitly null both mean "no artwork". */
function isOptionalHero(value: unknown): boolean {
  return value === undefined || value === null || isGuideHero(value);
}

export type GuideDocument = {
  title: string;
  description: string;
  hero?: GuideHero | null;
  blocks: GuideBlock[];
  sources: GuideSource[];
};

export type PublishedGuide = GuideDocument & {
  version: number;
  published_at: string;
  /** When the version readers see went live; moves on republication where `published_at`
   *  does not. Optional so a document from an older API still renders. */
  modified_at?: string | null;
};

export type GuideSummary = {
  slug: string;
  kind: GuideKind;
  destination_id: string | null;
  destination_label: string | null;
  topics: GuideTopic[];
  title: string;
  description: string;
  hero?: GuideHero | null;
  published_at: string;
  valid_until: string | null;
  featured: boolean;
};

export type GuideList = { articles: GuideSummary[]; next_cursor: string | null };

/** One search result: the card fields plus the passage the match was found in, and the
 *  folded terms the API matched so the card can mark them. */
export type GuideSearchHit = GuideSummary & { snippet: string; matched: string[] };

export type GuideSearchResult = {
  query: string;
  total: number;
  offset: number;
  limit: number;
  results: GuideSearchHit[];
  /** The article whose alias or title *is* the query; shown above the list, never in it. */
  best_match: GuideSummary | null;
  next_offset: number | null;
};

export type ArticleSearchOptions = { section?: GuideSection | null; offset?: number | null };

/** The results page URL. Only what changes the result set goes in: the query, the section
 *  and the offset, so two readers searching the same thing land on the same address. */
export function articleSearchHref(q: string, options: ArticleSearchOptions = {}): string {
  const params = new URLSearchParams();
  const query = q.trim();
  if (query) params.set("q", query);
  if (options.section) params.set("section", options.section);
  if (options.offset) params.set("offset", String(options.offset));
  const suffix = params.toString();
  return suffix ? `/search/articles?${suffix}` : "/search/articles";
}

export type HighlightSegment = { text: string; hit: boolean };

/** The same fold the API applies to both the index and the query (NFKC, casefold). */
function foldForMatch(text: string): string {
  return text.normalize("NFKC").toLowerCase();
}

/**
 * `text` folded character by character, with each folded position mapped back to the
 * original character it came from. NFKC is not length-preserving -- an ellipsis becomes
 * three periods, a ligature two letters -- so a match found in the folded copy has to be
 * carried back through this map rather than by index.
 */
function foldWithMap(text: string): { folded: string; starts: number[]; stops: number[] } {
  let folded = "";
  const starts: number[] = [];
  const stops: number[] = [];
  let index = 0;
  for (const char of text) {
    const piece = foldForMatch(char) || char;
    for (let offset = 0; offset < piece.length; offset += 1) {
      starts.push(index);
      stops.push(index + char.length);
    }
    folded += piece;
    index += char.length;
  }
  return { folded, starts, stops };
}

/**
 * Splits `text` into the runs that match one of `terms` and the runs between them, so a
 * card can wrap the hits in `<mark>` without ever building HTML from a string. The match is
 * made on the folded copy, so `ＡＩ` marks for `ai` and `JR PASS` for `jr pass`, and the
 * runs are sliced from the original so the reader sees their own text. A term that lands
 * inside one original character (a period inside an ellipsis) marks that character once.
 */
export function highlight(text: string, terms: readonly string[]): HighlightSegment[] {
  if (!text) return [];
  const needles = [...new Set(terms.map(foldForMatch).filter(Boolean))].sort((a, b) => b.length - a.length);
  if (!needles.length) return [{ text, hit: false }];
  const { folded, starts, stops } = foldWithMap(text);
  const segments: HighlightSegment[] = [];
  let foldCursor = 0;
  let cursor = 0;
  while (foldCursor < folded.length) {
    let nextIndex = -1;
    let nextLength = 0;
    for (const needle of needles) {
      const index = folded.indexOf(needle, foldCursor);
      if (index >= 0 && (nextIndex < 0 || index < nextIndex)) { nextIndex = index; nextLength = needle.length; }
    }
    if (nextIndex < 0) break;
    const from = Math.max(starts[nextIndex], cursor);
    const to = stops[nextIndex + nextLength - 1];
    if (to > from) {
      if (from > cursor) segments.push({ text: text.slice(cursor, from), hit: false });
      segments.push({ text: text.slice(from, to), hit: true });
      cursor = to;
    }
    foldCursor = nextIndex + nextLength;
  }
  if (cursor < text.length) segments.push({ text: text.slice(cursor), hit: false });
  return segments;
}


export type GuideArticleState = {
  slug: string;
  kind: GuideKind;
  locale: string;
  status: "published" | "unpublished" | "unavailable";
  destination_id: string | null;
  destination_label: string | null;
  topics: GuideTopic[];
  valid_until: string | null;
  expired: boolean;
  document: PublishedGuide | null;
  /** Only the locales genuinely published. The article page turns this into hreflang, so an
   *  unwritten translation is never advertised as one. */
  published_locales: Locale[];
  /** The partner links the API resolved against its registry. Optional so an article from an
   *  older API, or a state built without one, simply draws no partner link. */
  partner_links?: GuidePartnerLink[];
  article_links?: ArticleReference[];
  series?: SeriesNavigation | null;
  /** Further reading (the editor's picks, then the nearest neighbours), the articles whose
   *  text links here, and the other names this article answers to. All optional, so an
   *  article from an older API simply draws none of them. */
  related?: ArticleReference[];
  backlinks?: ArticleReference[];
  aliases?: string[];
  /** The glossary this article is an entry of, when it is one: the page marks it up as a
   *  DefinedTerm in that set. */
  term_set?: ArticleReference | null;
};

export function isGuideTopic(value: unknown): value is GuideTopic {
  const topic = value as Record<string, unknown> | null;
  if (!topic || typeof topic.slug !== "string" || typeof topic.label !== "string") return false;
  if (topic.section !== undefined && !isGuideSection(topic.section)) return false;
  if (topic.parent !== undefined && topic.parent !== null && typeof topic.parent !== "string") return false;
  if (topic.description !== undefined && topic.description !== null && typeof topic.description !== "string") return false;
  if (topic.count !== undefined && !Number.isInteger(topic.count)) return false;
  if (topic.counts !== undefined) {
    if (!topic.counts || typeof topic.counts !== "object") return false;
    if (!Object.values(topic.counts as Record<string, unknown>).every(Number.isInteger)) return false;
  }
  return true;
}

function isTopicList(value: unknown): value is GuideTopic[] {
  return Array.isArray(value) && value.every(isGuideTopic);
}

function isSourceList(value: unknown): value is GuideSource[] {
  return Array.isArray(value) && value.every((row) => {
    const source = row as Record<string, unknown> | null;
    return !!source && typeof source.title === "string" && typeof source.url === "string"
      && (source.checked_on === null || typeof source.checked_on === "string");
  });
}

export function isPublishedGuide(value: unknown): value is PublishedGuide {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  return typeof row.title === "string" && typeof row.description === "string"
    && typeof row.version === "number" && typeof row.published_at === "string"
    && (row.modified_at === undefined || row.modified_at === null || typeof row.modified_at === "string")
    && isOptionalHero(row.hero)
    && isGuideBlockList(row.blocks) && isSourceList(row.sources);
}

export function isGuideSummary(value: unknown): value is GuideSummary {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  return typeof row.slug === "string" && isGuideKind(row.kind)
    && typeof row.title === "string" && typeof row.description === "string"
    && typeof row.published_at === "string" && typeof row.featured === "boolean"
    && (row.destination_id === null || typeof row.destination_id === "string")
    && (row.destination_label === null || typeof row.destination_label === "string")
    && (row.valid_until === null || typeof row.valid_until === "string")
    && isOptionalHero(row.hero)
    && isTopicList(row.topics);
}

export function isGuideSearchHit(value: unknown): value is GuideSearchHit {
  if (!isGuideSummary(value)) return false;
  const row = value as unknown as Record<string, unknown>;
  return typeof row.snippet === "string"
    && Array.isArray(row.matched) && row.matched.every((term) => typeof term === "string");
}

export function isGuideSearchResult(value: unknown): value is GuideSearchResult {
  if (!value || typeof value !== "object") return false;
  const row = value as Record<string, unknown>;
  return typeof row.query === "string" && Number.isInteger(row.total) && Number.isInteger(row.offset)
    && Number.isInteger(row.limit)
    && Array.isArray(row.results) && row.results.every(isGuideSearchHit)
    && (row.best_match === null || row.best_match === undefined || isGuideSummary(row.best_match))
    && (row.next_offset === null || row.next_offset === undefined || Number.isInteger(row.next_offset));
}

/** An `intel` notice past its own validity. It keeps its page; it just stops being current. */
export function isExpired(validUntil: string | null, today: Date = new Date()): boolean {
  if (!validUntil) return false;
  const cutoff = new Date(`${validUntil}T23:59:59Z`);
  return Number.isFinite(cutoff.getTime()) && cutoff.getTime() < today.getTime();
}

// --- reading the body ------------------------------------------------------------------

/**
 * The body cut at every partner button and partner link, so a page can draw each slice with
 * the shared renderer and put an island between them. A segment ends in at most one of the
 * two. `headingStart` is the number of level-2 headings before the slice: heading ids are
 * numbered across the whole article, and a renderer that restarted at each slice would give
 * two sections the same anchor.
 *
 * A partner link never stays inside `blocks`: the shared renderer would draw its URL as an
 * ordinary, unqualified link.
 */
/** The summary and the FAQ are drawn in fixed places -- the answer under the description, the
 *  questions before the sources -- so the body is rendered without them. The API allows one
 *  of each; a document from an older draft that somehow carries two keeps the first. */
export function splitArticleExtras(blocks: readonly GuideBlock[]): {
  summary: SummaryBlock | null;
  faq: FaqBlock | null;
  blocks: GuideBlock[];
} {
  let summary: SummaryBlock | null = null;
  let faq: FaqBlock | null = null;
  const rest: GuideBlock[] = [];
  for (const block of blocks) {
    if (block.type === "summary" && !summary) summary = block;
    else if (block.type === "faq" && !faq) faq = block;
    else rest.push(block);
  }
  return { summary, faq, blocks: rest };
}

export type GuideSegment = {
  blocks: RichContentBlock[];
  headingStart: number;
  offer: OfferBlock | null;
  partner: PartnerLinkBlock | null;
};

export function splitGuideBlocks(blocks: readonly GuideBlock[]): GuideSegment[] {
  const segments: GuideSegment[] = [];
  let current: RichContentBlock[] = [];
  let start = 0;
  let seen = 0;
  for (const block of blocks) {
    if (block.type === "offer" || block.type === "partner_link") {
      segments.push({
        blocks: current,
        headingStart: start,
        offer: block.type === "offer" ? block : null,
        partner: block.type === "partner_link" ? block : null,
      });
      current = [];
      start = seen;
      continue;
    }
    if (block.type === "heading" && block.level === 2) seen += 1;
    current.push(block);
  }
  segments.push({ blocks: current, headingStart: start, offer: null, partner: null });
  return segments;
}

export type GuideHeading = { id: string; text: string };

/** The level-2 headings with the ids `ContentBlocks` gives them, for a table of contents. */
export function guideHeadings(blocks: readonly GuideBlock[]): GuideHeading[] {
  const headings: GuideHeading[] = [];
  for (const block of blocks) {
    if (block.type === "heading" && block.level === 2) {
      headings.push({ id: `section-${headings.length + 1}`, text: block.text });
    }
  }
  return headings;
}

const CJK = /[\p{Script=Han}\p{Script=Hiragana}\p{Script=Katakana}\p{Script=Hangul}]/gu;

/** Roughly how long the body takes to read: CJK by character, everything else by word. Never
 *  below one minute, so a short notice does not claim to take none. */
export function readingMinutes(document: GuideDocument): number {
  const parts: string[] = [];
  for (const block of document.blocks) {
    if (block.type === "heading" || block.type === "paragraph" || block.type === "link") parts.push(block.text);
    if (block.type === "callout") parts.push(block.title ?? "", block.text);
    if (block.type === "list") parts.push(...block.items);
    if (block.type === "table") parts.push(...block.header, ...block.rows.flat());
    if (block.type === "image") parts.push(block.caption ?? "");
    if (block.type === "rich_paragraph") parts.push(...block.inlines.map(node => node.text));
    if (block.type === "summary") parts.push(...block.items);
    if (block.type === "faq") parts.push(...block.items.flatMap((item) => [item.question, item.answer]));
  }
  const text = parts.join(" ");
  const characters = (text.match(CJK) ?? []).length;
  const words = text.replace(CJK, " ").split(/\s+/).filter(Boolean).length;
  return Math.max(1, Math.ceil(characters / 400 + words / 200));
}
