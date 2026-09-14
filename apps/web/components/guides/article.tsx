import { Fragment, type ReactNode } from "react";
import { GuideImage } from "./guide-image";
import { SeriesStart, SeriesEnd } from "./series-navigation";
import { SeriesNavigation as GeminiNavigation } from "./gemini-series-navigation";
import { GeminiSeriesIndex } from "./series-index";
import { geminiCopy, geminiSeries, seriesMember } from "@/lib/gemini-series";
import { ArticleAdSlot } from "@/components/ads/article-ad-slot";
import { ContentBlocks, ImageCreditLine, type ContentBlockLabels } from "@/components/content-blocks";
import { adsensePlacements, type AdsenseConfig } from "@/lib/adsense";
import { DestinationAffiliateOptions } from "@/components/destination-affiliate-options";
import { PartnerLink, type PartnerLinkLabels } from "@/components/guides/partner-link";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { contentBlockLink } from "@/lib/content-blocks";
import { guideAffiliateDestination, guideAffiliateModules, guideAffiliatePlacement } from "@/lib/guide-affiliate";
import {
  guideHeadings, guideHref, guideListHref, partnerClickPath, splitGuideBlocks,
  type GuideArticleState, type GuideKind,
} from "@/lib/guides";

/** One label per kind (the badge above the title) plus the update-date word, sources and
 *  the parts of the body the renderer cannot name itself. */
export type GuideArticleLabels = Record<GuideKind, string> & {
  updated: string;
  sources: string;
  checkedOn: string;
  destination: string;
  otherLanguages: string;
  /** The table of contents heading. */
  contents: string;
  /** Above an ad unit. Policy allows "廣告"/"Advertisements" and nothing softer. */
  adLabel: string;
  /** One line under the hero whenever the body itself carries partner buttons, so the
   *  disclosure comes before the first button rather than only inside the end panel. */
  disclosure: string;
  /** The same line when the body carries a partner link: worded for buying or subscribing,
   *  not only for booking, because a book or a hosting plan is not a booking. */
  partnerDisclosure: string;
  partner: PartnerLinkLabels;
  blocks: ContentBlockLabels;
};

/** Fewer level-2 headings than this and a table of contents is longer than the scroll it saves. */
export const CONTENTS_MIN_HEADINGS = 3;

/**
 * An article a reader can reach. Expiry is silent: an `intel` notice keeps its URL so
 * existing links do not break, and the reader is told nothing about dates — no first
 * publication, no expiry banner, no date it applied until. `expired` still decides one
 * thing, below: an expired notice carries no partner buttons.
 *
 * The body is drawn in slices around the editor's partner buttons (`offer` blocks) and partner
 * links (`partner_link` blocks), each a client island between two runs of the shared renderer.
 * The end of the article runs: end
 * panel (if any), `related`, topic chips, sources, other languages. `related` is whatever
 * the page fetched to hand the reader on and stays a plain node so this component remains
 * synchronous and renders directly under React Testing Library.
 */
export function GuideArticle({
  state, labels, related, readingTime, adsense, seriesHub, geminiEnabled = false,
}: {
  state: GuideArticleState & { document: NonNullable<GuideArticleState["document"]> };
  labels: GuideArticleLabels;
  related?: ReactNode;
  seriesHub?: ReactNode;
  geminiEnabled?: boolean;
  /** Already worded by the page ("about 5 min"); omitted when the page does not want it. */
  readingTime?: string | null;
  /** Disabled, or absent, means no slot AND no reserved space anywhere in the body. */
  adsense?: AdsenseConfig;
}) {
  const { document } = state;
  const geminiMember = geminiEnabled ? seriesMember(state.slug, state.locale, state.kind) : undefined;
  const isGeminiHub = geminiEnabled && state.kind === "life" && state.locale === geminiSeries.locale && state.slug === geminiSeries.hubSlug;
  // First publication is never drawn; it is only the date "updated" has to beat before it
  // means anything, since `modified_at` equals it until the article is republished.
  const published = document.published_at.slice(0, 10);
  const modified = document.modified_at ? document.modified_at.slice(0, 10) : null;
  const others = state.published_locales.filter((value) => value !== state.locale);
  const placement = guideAffiliatePlacement(state.kind);
  const segments = splitGuideBlocks(document.blocks);
  const headings = guideHeadings(document.blocks);

  // The editor's own buttons: each resolves its destination the way the end panel does
  // (its own city, else the article's; Kyoto folds into osaka-kyoto) and is dropped under
  // the same expiry rule. A block whose city is not in the catalog draws nothing.
  const islands = state.expired ? [] : segments.flatMap((segment) => {
    if (!segment.offer) return [];
    const destination = guideAffiliateDestination(segment.offer.destination_id ?? state.destination_id);
    return destination ? [{ segment, offer: segment.offer, destination }] : [];
  });
  const inlineModules = new Set(islands.map((island) => island.offer.module));

  // The editor's partner links, each drawn only when the API resolved it against the partner
  // registry: an unknown program, a foreign host or an expired notice leaves no link behind.
  const resolved = state.expired ? [] : state.partner_links ?? [];
  const partnerIslands = segments.flatMap((segment) => {
    const block = segment.partner;
    const link = block ? resolved.find((entry) => entry.partner === block.partner && entry.url === block.url) : undefined;
    return block && link ? [{ segment, block, link }] : [];
  });

  // Up to three in-article units, each kept clear of the hero (the LCP element), of every
  // partner button or partner link and of the end panel — `adsensePlacements` has the rules.
  // With advertising off every segment stays a single piece, so nothing is reserved anywhere.
  const pieces = adsense?.enabled
    ? adsensePlacements(segments, { hasHero: Boolean(document.hero) })
    : segments.map((segment) => [{ blocks: segment.blocks, headingStart: segment.headingStart }]);
  // The page-wide number of the first unit in each segment: every piece after a segment's
  // first is preceded by one.
  const firstAd = pieces.map((_, index) =>
    pieces.slice(0, index).reduce((count, segmentPieces) => count + segmentPieces.length - 1, 0));

  // Partner buttons only where they are contextual: a destination the article belongs to,
  // a module its topics point at, and a notice that still applies. An expired fare deal
  // with a "book flights" button underneath would read as bait. A module the editor already
  // placed mid-article is left out, so the same button never appears twice.
  //
  // A `life` article is the exception recorded in lib/guide-affiliate.ts: lifestyle topics
  // point at no module, so the destination the editor deliberately filled in is the only
  // contextual signal and the panel shows every module, exactly like the city page's own.
  // It is rendered non-contextual so its heading names the destination's partners rather
  // than inviting the reader to "keep exploring" a place the article was never about.
  const affiliateDestination = guideAffiliateDestination(state.destination_id);
  const affiliateModules = guideAffiliateModules(state.topics, state.kind)
    .filter((module) => !inlineModules.has(module));
  const showAffiliate = Boolean(affiliateDestination) && affiliateModules.length > 0 && !state.expired;

  return (
    <article className="space-y-6 break-words [overflow-wrap:anywhere]">
      {geminiMember ? <GeminiNavigation article={geminiMember} position="top" /> : null}
      <header>
        <p className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">
          <span className="rounded-full bg-[var(--line)] px-2 py-1 text-[var(--fg)]">
            {labels[state.kind]}
          </span>
          {state.destination_label ? (
            <Link className="underline" href={`/destinations/${state.destination_id}`}>
              {state.destination_label}
            </Link>
          ) : null}
        </p>
        <h1 className="mt-3 text-3xl font-bold">{document.title}</h1>
        <p className="mt-3 leading-7 text-[var(--muted)]">{document.description}</p>
        {isGeminiHub ? <a href="#series-directory" className="mt-3 inline-flex min-h-11 items-center text-[var(--teal)] underline">{geminiCopy.start}</a> : null}
        {(modified && modified > published) || readingTime ? (
          <p className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm text-[var(--muted)]">
            {modified && modified > published ? (
              <span>{labels.updated}: <time dateTime={modified}>{modified}</time></span>
            ) : null}
            {readingTime ? <span>{readingTime}</span> : null}
          </p>
        ) : null}
      </header>

      {document.hero ? (
        <figure>
          <GuideImage
            src={document.hero.src}
            alt={document.hero.alt}
            width={document.hero.width}
            height={document.hero.height}
            loading="eager"
            fetchPriority="high"
            decoding="async"
            className="h-auto w-full rounded-2xl"
          />
          {document.hero.credit ? (
            <figcaption className="mt-2 text-sm leading-6 text-[var(--muted)]">
              <ImageCreditLine credit={document.hero.credit} prefix={labels.blocks.imageCredit} />
            </figcaption>
          ) : null}
        </figure>
      ) : null}

      {islands.length || partnerIslands.length ? (
        <p role="note" className="text-sm leading-6 text-[var(--muted)]">
          {partnerIslands.length ? labels.partnerDisclosure : labels.disclosure}
        </p>
      ) : null}

      {state.series?.current ? <SeriesStart series={state.series} locale={state.locale} /> : null}
      {seriesHub}
      {isGeminiHub ? <GeminiSeriesIndex /> : null}
      {headings.length >= CONTENTS_MIN_HEADINGS && !state.series ? (
        <nav aria-label={labels.contents} className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] px-4 py-3">
          <p className="text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">{labels.contents}</p>
          <ol className="mt-2 space-y-1 leading-7">
            {headings.map((heading, index) => (
              <li key={heading.id}>
                <a href={`#${heading.id}`} className="underline">{index + 1}. {heading.text}</a>
              </li>
            ))}
          </ol>
        </nav>
      ) : null}
      {state.series?.current && headings.length >= CONTENTS_MIN_HEADINGS ? <details className="rounded-2xl border border-[var(--line)] p-4 lg:hidden">
        <summary className="min-h-11 cursor-pointer font-semibold">{labels.contents}</summary>
        <ol className="space-y-2">{headings.map(heading => <li key={heading.id}><a className="underline" href={`#${heading.id}`}>{heading.text}</a></li>)}</ol>
      </details> : null}

      {segments.map((segment, index) => {
        const island = islands.find((entry) => entry.segment === segment);
        const partnerIsland = partnerIslands.find((entry) => entry.segment === segment);
        return (
          <Fragment key={index}>
            {pieces[index].map((piece, pieceIndex) => (
              <Fragment key={pieceIndex}>
                {pieceIndex > 0 ? (
                  <ArticleAdSlot
                    publisherId={adsense?.publisher_id ?? ""}
                    slotId={adsense?.slot_id ?? ""}
                    label={labels.adLabel}
                    cmpEnabled={Boolean(adsense?.cmp_enabled)}
                    // Only the page's first unit asks for an ad as soon as it mounts; the rest
                    // wait until the reader scrolls near them.
                    lazy={firstAd[index] + pieceIndex - 1 > 0}
                  />
                ) : null}
                {piece.blocks.length ? (
                  <ContentBlocks blocks={piece.blocks} labels={labels.blocks} headingStart={piece.headingStart} articleLinks={state.article_links} locale={state.locale} />
                ) : null}
              </Fragment>
            ))}
            {partnerIsland ? (
              <PartnerLink
                link={partnerIsland.link}
                label={partnerIsland.block.label}
                note={partnerIsland.block.note}
                clickPath={partnerClickPath(state.kind, state.slug, state.locale, partnerIsland.link.key)}
                labels={labels.partner}
              />
            ) : null}
            {island ? (
              <section className="space-y-3">
                {island.offer.heading ? <h3 className="text-lg font-semibold">{island.offer.heading}</h3> : null}
                <DestinationAffiliateOptions
                  destinationId={island.destination}
                  modules={[island.offer.module]}
                  contextual={state.kind !== "life"}
                  destinationLabel={island.offer.destination_id ? undefined : state.destination_label ?? undefined}
                  placement={placement}
                />
              </section>
            ) : null}
          </Fragment>
        );
      })}

      {showAffiliate && affiliateDestination ? (
        <DestinationAffiliateOptions
          destinationId={affiliateDestination}
          modules={affiliateModules}
          contextual={state.kind !== "life"}
          destinationLabel={state.destination_label ?? undefined}
          placement={placement}
        />
      ) : null}

      {state.series?.current ? <SeriesEnd series={state.series} locale={state.locale} /> : null}
      {geminiMember ? <GeminiNavigation article={geminiMember} position="bottom" /> : null}
      {related}

      {state.topics.length ? (
        <ul className="flex flex-wrap gap-2 border-t border-[var(--line)] pt-6">
          {state.topics.map((topic) => (
            <li key={topic.slug}>
              <Link
                className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] px-3 py-1 text-sm text-[var(--muted)]"
                href={guideListHref(state.kind, topic.slug)}
              >
                {topic.label}
              </Link>
            </li>
          ))}
        </ul>
      ) : null}

      {document.sources.length ? (
        <section className="border-t border-[var(--line)] pt-6">
          <h2 className="text-lg font-semibold">{labels.sources}</h2>
          <ul className="mt-3 space-y-2">
            {document.sources.map((source, index) => {
              const href = contentBlockLink(source.url);
              return href ? (
                <li key={index} className="text-sm leading-6">
                  <a className="text-[var(--teal)] underline" href={href} target="_blank" rel="noopener noreferrer">
                    {source.title}
                  </a>
                  {source.checked_on ? (
                    <span className="text-[var(--muted)]">
                      {" "}· {labels.checkedOn}: <time dateTime={source.checked_on}>{source.checked_on}</time>
                    </span>
                  ) : null}
                </li>
              ) : null;
            })}
          </ul>
        </section>
      ) : null}

      {others.length ? (
        <section className="border-t border-[var(--line)] pt-6">
          <h2 className="text-lg font-semibold">{labels.otherLanguages}</h2>
          <ul className="mt-3 flex flex-wrap gap-3">
            {others.map((value) => (
              <li key={value}>
                <a
                  className="inline-flex min-h-11 items-center text-[var(--teal)] underline"
                  href={`/${value}${guideHref(state.kind, state.slug)}`}
                  hrefLang={value}
                >
                  {localeLabels[value as Locale]}
                </a>
              </li>
            ))}
          </ul>
        </section>
      ) : null}
    </article>
  );
}
