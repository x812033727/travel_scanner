import { Calendar, Clock, RefreshCw } from "lucide-react";
import { Fragment, type ReactNode } from "react";
import { GuideImage } from "./guide-image";
import { SeriesStart, SeriesEnd } from "./series-navigation";
import { SeriesNavigation as GeminiNavigation } from "./gemini-series-navigation";
import { GeminiSeriesIndex } from "./series-index";
import { geminiSeriesCopy as geminiCopy } from "@/lib/gemini-series-copy";
import { visibleGeminiMember, type VisibleGeminiSeries } from "@/lib/gemini-series-projection";
import { ArticleAdSlot } from "@/components/ads/article-ad-slot";
import { ContentBlocks, FaqSection, ImageCreditLine, SummaryCard, type ContentBlockLabels } from "@/components/content-blocks";
import { adsensePlacements, type AdsenseConfig } from "@/lib/adsense";
import { DestinationAffiliateOptions } from "@/components/destination-affiliate-options";
import { ArticleShareBar, type ArticleShareLabels } from "@/components/guides/article-share-bar";
import { PartnerLink, type PartnerLinkLabels } from "@/components/guides/partner-link";
import { SupportLink, type SupportLinkLabels } from "@/components/guides/support-link";
import type { TermLinkLabels } from "@/components/guides/term-link";
import { Link } from "@/i18n/navigation";
import { contentBlockLink } from "@/lib/content-blocks";
import { guideAffiliateDestination, guideAffiliateModules, guideAffiliatePlacement } from "@/lib/guide-affiliate";
import {
  guideHeadings, guideListHref, isSyntheticNewsBlock, partnerClickPath, splitGuideBlocks,
  type GuideArticleState, type GuideKind,
  splitArticleExtras, visibleGuideHero,
} from "@/lib/guides";

/** One label per kind (the badge above the title) plus the update-date word, sources and
 *  the parts of the body the renderer cannot name itself. */
export type GuideArticleLabels = Record<GuideKind, string> & {
  publishedOn?: string;
  updated: string;
  sources: string;
  checkedOn: string;
  sourcesProvenance?: string;
  destination: string;
  /** The table of contents heading. */
  contents: string;
  /** Above an ad unit. */
  adLabel: string;
  /** One line under the hero whenever the body itself carries partner buttons, so the
   *  disclosure comes before the first button rather than only inside the end panel. */
  disclosure: string;
  /** The same line when the body carries a partner link: worded for buying or subscribing,
   *  not only for booking, because a book or a hosting plan is not a booking. */
  partnerDisclosure: string;
  partner: PartnerLinkLabels;
  blocks: ContentBlockLabels;
  /** The definition card under a term link; without it a term is a plain link. */
  term?: TermLinkLabels;
  /** The heading over the summary card and over the FAQ section. */
  summary?: string;
  faq?: string;
  /** The line under the sources that links the owner's tip page, when one is set. */
  support?: SupportLinkLabels;
};

/** Fewer level-2 headings than this and a table of contents is longer than the scroll it saves. */
export const CONTENTS_MIN_HEADINGS = 3;

/**
 * An article a reader can reach. Expiry is silent: an `intel` notice keeps its URL so
 * existing links do not break, and the reader is told nothing about dates -- no first
 * publication, no expiry banner, no date it applied until. `expired` still decides one
 * thing, below: an expired notice carries no partner buttons.
 *
 * The body is drawn in slices around the editor's partner buttons (`offer` blocks) and partner
 * links (`partner_link` blocks), each a client island between two runs of the shared renderer.
 * The end of the article runs: end
 * panel (if any), `related`, topic chips, sources. A translation of the article is not
 * offered in the body: the published set is declared in `alternates.languages` for search
 * engines, and the reader switches language from the header. `related` is whatever
 * the page fetched to hand the reader on and stays a plain node so this component remains
 * synchronous and renders directly under React Testing Library.
 */
export function GuideArticle({
  state,
  labels,
  related,
  readingTime,
  adsense,
  seriesHub,
  geminiSeries = null,
  sidebarToc = false,
  constrainDiagrams = false,
  share,
}: {
  state: GuideArticleState & { document: NonNullable<GuideArticleState["document"]> };
  labels: GuideArticleLabels;
  related?: ReactNode;
  seriesHub?: ReactNode;
  geminiSeries?: VisibleGeminiSeries | null;
  /** Already worded by the page ("about 5 min"); omitted when the page does not want it. */
  readingTime?: string | null;
  /** Disabled, or absent, means no slot AND no reserved space anywhere in the body. */
  adsense?: AdsenseConfig;
  /** Set when the surrounding page provides a sticky desktop TOC rail, folding the mobile TOC. */
  sidebarToc?: boolean;
  /** Keeps wide SVG diagrams inside their own scroller when rendered inside an elevated sheet. */
  constrainDiagrams?: boolean;
  /** Optional zero-script share actions rendered in the article header. */
  share?: { url: string; labels: ArticleShareLabels };
}) {
  const { document } = state;
  const visibleHero = visibleGuideHero(document.hero);
  const authoredBlocks = document.blocks.filter((block) => !isSyntheticNewsBlock(block));
  const geminiMember = geminiSeries ? visibleGeminiMember(geminiSeries, state.slug, state.locale, state.kind) : undefined;
  const isGeminiHub = geminiSeries && state.kind === "life" && state.locale === geminiSeries.locale && state.slug === geminiSeries.hubSlug;
  // First publication is never drawn; it is only the date "updated" has to beat before it
  // means anything, since `modified_at` equals it until the article is republished.
  const published = document.published_at.slice(0, 10);
  const modified = document.modified_at ? document.modified_at.slice(0, 10) : null;
  const placement = guideAffiliatePlacement(state.kind);
  // The summary goes under the description. FAQ answers stay in the author's body order;
  // hoisting them used to leave an empty heading and a misleading contents link behind.
  const extras = splitArticleExtras(authoredBlocks);
  const segments = splitGuideBlocks(extras.blocks);
  const headings = guideHeadings(extras.blocks);
  const faqSections = new Map<number, { id: string; heading?: string }>();
  let faqCount = 0;
  let sectionHeading = "";
  const faqLabel = labels.faq?.normalize("NFKC").trim().toLocaleLowerCase(state.locale);
  for (const [index, block] of extras.blocks.entries()) {
    if (block.type === "heading" && block.level === 2) sectionHeading = block.text;
    if (block.type !== "faq") continue;
    faqCount += 1;
    const preceding = extras.blocks[index - 1];
    // An immediately preceding H2 is the author's heading, whatever its language or wording.
    // A localized FAQ heading may also introduce a paragraph before the answers. Keep that
    // prose and heading; a genuinely separate section still gets the localized FAQ label.
    const authoredHeading = (preceding?.type === "heading" && preceding.level === 2)
      || Boolean(faqLabel && sectionHeading.normalize("NFKC").trim().toLocaleLowerCase(state.locale) === faqLabel);
    faqSections.set(index, {
      id: faqCount === 1 ? "article-faq" : `article-faq-${faqCount}`,
      heading: authoredHeading ? undefined : labels.faq,
    });
  }
  const segmentOffsets = segments.map((_, index) => segments.slice(0, index).reduce(
    (offset, segment) => offset + segment.blocks.length + Number(Boolean(segment.offer || segment.partner)), 0));

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
  // partner button or partner link and of the end panel -- `adsensePlacements` has the rules.
  // With advertising off every segment stays a single piece, so nothing is reserved anywhere.
  const pieces = adsense?.enabled
    ? adsensePlacements(segments, { hasHero: Boolean(visibleHero) })
    : segments.map((segment) => [{ blocks: segment.blocks, headingStart: segment.headingStart }]);
  // The page-wide number of the first unit in each segment: every piece after a segment's
  // first is preceded by one.
  const firstAd = pieces.map((_, index) =>
    pieces.slice(0, index).reduce((count, segmentPieces) => count + segmentPieces.length - 1, 0));
  // The level-3 headings already drawn in the section each piece opens inside. A unit or a
  // partner slice can fall between two subsections, and a count restarted at every piece
  // would give the second one the first one's anchor.
  const subsectionStarts: number[][] = [];
  let openSubsections = 0;
  for (const segmentPieces of pieces) {
    const starts: number[] = [];
    for (const piece of segmentPieces) {
      starts.push(openSubsections);
      for (const block of piece.blocks) {
        if (block.type === "heading") openSubsections = block.level === 3 ? openSubsections + 1 : 0;
      }
    }
    subsectionStarts.push(starts);
  }

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
      {geminiMember && geminiSeries ? <GeminiNavigation series={geminiSeries} number={geminiMember.number} position="top" /> : null}
      <header>
        <p className="flex flex-wrap items-center gap-2 text-[length:var(--text-xs)] font-semibold uppercase tracking-wide text-[var(--muted)]">
          <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[var(--teal-dark)]">
            {labels[state.kind]}
          </span>
          {state.destination_label ? (
            <Link className="underline underline-offset-4 hover:text-[var(--teal)]" href={`/destinations/${state.destination_id}`}>
              {state.destination_label}
            </Link>
          ) : null}
        </p>
        <h1 className="mt-3 text-2xl font-extrabold leading-[1.28] tracking-tight sm:mt-3.5 sm:text-3xl md:text-4xl md:leading-[1.2]">{document.title}</h1>
        <p className="mt-3 text-base leading-7 text-[var(--muted)] sm:mt-3.5 sm:text-lg sm:leading-8">{document.description}</p>
        {isGeminiHub ? <a href="#series-directory" className="mt-3 inline-flex min-h-11 items-center text-[var(--teal)] underline">{geminiCopy.start}</a> : null}
        {state.news_date || (modified && modified > published) || readingTime ? (
          <p className="mt-4 flex flex-wrap items-center gap-x-4 gap-y-1.5 border-y border-[var(--line)] py-2.5 text-sm text-[var(--muted)]">
            {state.news_date ? (
              <span className="inline-flex items-center gap-1.5">
                <Calendar size={14} className="shrink-0 text-[var(--teal)]" aria-hidden />
                <span>{labels.publishedOn ? `${labels.publishedOn}: ` : ""}<time dateTime={state.news_date} className="font-mono tabular-nums">{state.news_date}</time></span>
              </span>
            ) : null}
            {modified && modified > published ? (
              <span className="inline-flex items-center gap-1.5">
                <RefreshCw size={14} className="shrink-0 text-[var(--muted)]" aria-hidden />
                <span>{labels.updated}: <time dateTime={modified} className="font-mono tabular-nums">{modified}</time></span>
              </span>
            ) : null}
            {readingTime ? (
              <span className="inline-flex items-center gap-1.5">
                <Clock size={14} className="shrink-0 text-[var(--muted)]" aria-hidden />
                <span>{readingTime}</span>
              </span>
            ) : null}
          </p>
        ) : null}
        {share && !isGeminiHub ? (
          <ArticleShareBar url={share.url} title={document.title} labels={share.labels} />
        ) : null}
      </header>

      {extras.summary ? <SummaryCard id="article-summary" items={extras.summary.items} heading={labels.summary} /> : null}

      {visibleHero ? (
        <figure>
          <GuideImage
            src={visibleHero.src}
            alt={visibleHero.alt}
            width={visibleHero.width}
            height={visibleHero.height}
            loading="eager"
            fetchPriority="high"
            decoding="async"
            className="h-auto w-full rounded-2xl border border-[var(--line)] shadow-[var(--shadow-sm)]"
          />
          {visibleHero.credit ? (
            <figcaption className="mt-2 text-sm leading-6 text-[var(--muted)]">
              <ImageCreditLine credit={visibleHero.credit} prefix={labels.blocks.imageCredit} />
            </figcaption>
          ) : null}
        </figure>
      ) : null}

      {islands.length || partnerIslands.length ? (
        <p role="note" className="text-sm leading-6 text-[var(--muted)]">
          {partnerIslands.length ? labels.partnerDisclosure : labels.disclosure}
        </p>
      ) : null}

      {state.series?.current && !geminiMember ? <SeriesStart series={state.series} locale={state.locale} /> : null}
      {seriesHub}
      {isGeminiHub && geminiSeries ? <GeminiSeriesIndex series={geminiSeries} /> : null}
      {!sidebarToc && headings.length >= CONTENTS_MIN_HEADINGS && !state.series ? (
        <nav aria-label={labels.contents} className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-5 py-4 shadow-[var(--shadow-sm)]">
          <p className="text-[length:var(--text-xs)] font-extrabold uppercase tracking-wider text-[var(--teal-dark)]">{labels.contents}</p>
          <ol className="mt-2.5 space-y-1.5 leading-7">
            {headings.map((heading, index) => (
              <li key={heading.id}>
                <a href={`#${heading.id}`} className="text-[var(--ink)] underline decoration-[var(--line)] underline-offset-4 transition-colors hover:text-[var(--teal)] hover:decoration-[var(--teal)]">{index + 1}. {heading.text}</a>
              </li>
            ))}
          </ol>
        </nav>
      ) : null}
      {(sidebarToc || state.series?.current) && headings.length >= CONTENTS_MIN_HEADINGS ? (
        <details open={!state.series?.current} className="group rounded-2xl border border-[var(--line)] bg-[color-mix(in_srgb,var(--teal-soft)_38%,var(--surface))] px-4 py-2.5 shadow-[var(--shadow-sm)] sm:px-5 sm:py-3 lg:hidden">
          <summary className="flex min-h-11 cursor-pointer list-none items-center justify-between gap-2 font-bold text-[var(--teal-dark)] after:shrink-0 after:font-mono after:text-base after:text-[var(--muted)] after:content-['+'] group-open:after:content-['−'] [&::-webkit-details-marker]:hidden">{labels.contents}</summary>
          <ol className="mt-1.5 space-y-1.5 border-t border-[var(--line)] pb-1.5 pt-2.5 text-sm leading-6">
            {headings.map((heading, index) => (
              <li key={heading.id}>
                <a className="inline-block py-1 text-[var(--ink)] underline decoration-[var(--line)] underline-offset-4 hover:text-[var(--teal)]" href={`#${heading.id}`}>
                  <span className="mr-1 font-mono text-[length:var(--text-xs)] font-semibold text-[var(--muted)]">{index + 1}.</span> {heading.text}
                </a>
              </li>
            ))}
          </ol>
        </details>
      ) : null}

      {segments.map((segment, index) => {
        const island = islands.find((entry) => entry.segment === segment);
        const partnerIsland = partnerIslands.find((entry) => entry.segment === segment);
        return (
          <Fragment key={index}>
            {pieces[index].map((piece, pieceIndex) => {
              const offset = segmentOffsets[index] + pieces[index].slice(0, pieceIndex)
                .reduce((count, preceding) => count + preceding.blocks.length, 0);
              return (
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
                    <ContentBlocks
                      blocks={piece.blocks} labels={labels.blocks} headingStart={piece.headingStart}
                      subsectionStart={subsectionStarts[index][pieceIndex]}
                      articleLinks={state.article_links} locale={state.locale} termLabels={labels.term}
                      constrainDiagrams={constrainDiagrams}
                      renderFaq={(block, blockIndex) => <FaqSection items={block.items} {...faqSections.get(offset + blockIndex)} />}
                    />
                  ) : null}
                </Fragment>
              );
            })}
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
                  article={state.slug}
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
          article={state.slug}
        />
      ) : null}

      {share && !isGeminiHub ? (
        <ArticleShareBar url={share.url} title={document.title} labels={share.labels} variant="callout" />
      ) : null}

      {state.series?.current && !geminiMember ? <SeriesEnd series={state.series} locale={state.locale} /> : null}
      {geminiMember && geminiSeries ? <GeminiNavigation series={geminiSeries} number={geminiMember.number} position="bottom" /> : null}
      {related}

      {state.topics.length ? (
        <ul className="flex flex-wrap gap-2 border-t border-[var(--line)] pt-6">
          {state.topics.map((topic) => (
            <li key={topic.slug}>
              <Link
                className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] bg-[var(--surface)] px-3.5 py-1 text-sm font-medium text-[var(--ink)] shadow-[var(--shadow-sm)] transition-colors hover:border-[var(--teal)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"
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
          <div className="rounded-2xl border border-[var(--line)] bg-[var(--surface-tint)]/45 p-4 md:p-5">
            <h2 className="portal-section-heading text-base font-bold tracking-tight text-[var(--ink)]">{labels.sources}</h2>
            <ul className="mt-2.5 divide-y divide-[var(--line)]">
              {document.sources.map((source, index) => {
                const href = contentBlockLink(source.url);
                return href ? (
                  <li key={index} className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1 py-2 text-sm leading-6 first:pt-0 last:pb-0">
                    <a className="font-medium text-[var(--teal)] underline underline-offset-4 hover:text-[var(--teal-dark)]" href={href} target="_blank" rel="noopener noreferrer">
                      {source.title}
                    </a>
                    {source.checked_on ? (
                      <span className="font-mono text-[length:var(--text-xs)] tabular-nums text-[var(--muted)]">
                        {labels.checkedOn}: <time dateTime={source.checked_on}>{source.checked_on}</time>
                      </span>
                    ) : null}
                  </li>
                ) : null;
              })}
            </ul>
            {labels.sourcesProvenance ? (
              <p className="mt-3 border-t border-[var(--line)] pt-2.5 text-[length:var(--text-xs)] leading-6 text-[var(--muted)]">
                {labels.sourcesProvenance}
              </p>
            ) : null}
          </div>
        </section>
      ) : null}

      {labels.support ? <SupportLink labels={labels.support} /> : null}
    </article>
  );
}
