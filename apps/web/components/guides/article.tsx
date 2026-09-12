import { Fragment, type ReactNode } from "react";
import { ContentBlocks, ImageCreditLine, type ContentBlockLabels } from "@/components/content-blocks";
import { DestinationAffiliateOptions } from "@/components/destination-affiliate-options";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { contentBlockLink } from "@/lib/content-blocks";
import { guideAffiliateDestination, guideAffiliateModules, guideAffiliatePlacement } from "@/lib/guide-affiliate";
import {
  guideHeadings, guideHref, guideListHref, splitGuideBlocks,
  type GuideArticleState, type GuideKind,
} from "@/lib/guides";

/** One label per kind (the badge above the title) plus the words around dates, sources and
 *  the parts of the body the renderer cannot name itself. */
export type GuideArticleLabels = Record<GuideKind, string> & {
  published: string;
  updated: string;
  expiredNotice: string;
  validUntil: string;
  sources: string;
  checkedOn: string;
  destination: string;
  otherLanguages: string;
  /** The table of contents heading. */
  contents: string;
  /** One line under the hero whenever the body itself carries partner buttons, so the
   *  disclosure comes before the first button rather than only inside the end panel. */
  disclosure: string;
  blocks: ContentBlockLabels;
};

/** Fewer level-2 headings than this and a table of contents is longer than the scroll it saves. */
export const CONTENTS_MIN_HEADINGS = 3;

/**
 * An article a reader can reach. Expiry is shown, not hidden: an `intel` notice keeps its
 * URL so existing links do not break, and says plainly what date it applied until.
 *
 * The body is drawn in slices around the editor's partner buttons (`offer` blocks), each a
 * client island between two runs of the shared renderer. The end of the article runs: end
 * panel (if any), `related`, topic chips, sources, other languages. `related` is whatever
 * the page fetched to hand the reader on and stays a plain node so this component remains
 * synchronous and renders directly under React Testing Library.
 */
export function GuideArticle({
  state, labels, related, readingTime,
}: {
  state: GuideArticleState & { document: NonNullable<GuideArticleState["document"]> };
  labels: GuideArticleLabels;
  related?: ReactNode;
  /** Already worded by the page ("about 5 min"); omitted when the page does not want it. */
  readingTime?: string | null;
}) {
  const { document } = state;
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
        <p className="mt-3 flex flex-wrap gap-x-4 gap-y-1 text-sm text-[var(--muted)]">
          <span>{labels.published}: <time dateTime={published}>{published}</time></span>
          {modified && modified > published ? (
            <span>{labels.updated}: <time dateTime={modified}>{modified}</time></span>
          ) : null}
          {readingTime ? <span>{readingTime}</span> : null}
        </p>
        {state.expired && state.valid_until ? (
          <p role="status" className="mt-4 rounded-2xl border border-[var(--line)] bg-[var(--line)] px-4 py-3 text-sm leading-6">
            {labels.expiredNotice} {labels.validUntil}: <time dateTime={state.valid_until}>{state.valid_until}</time>
          </p>
        ) : null}
      </header>

      {document.hero ? (
        <figure>
          <img
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

      {islands.length ? (
        <p role="note" className="text-sm leading-6 text-[var(--muted)]">{labels.disclosure}</p>
      ) : null}

      {headings.length >= CONTENTS_MIN_HEADINGS ? (
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

      {segments.map((segment, index) => {
        const island = islands.find((entry) => entry.segment === segment);
        return (
          <Fragment key={index}>
            {segment.blocks.length ? (
              <ContentBlocks blocks={segment.blocks} labels={labels.blocks} headingStart={segment.headingStart} />
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
