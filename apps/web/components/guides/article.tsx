import type { ReactNode } from "react";
import { ContentBlocks } from "@/components/content-blocks";
import { DestinationAffiliateOptions } from "@/components/destination-affiliate-options";
import { Link } from "@/i18n/navigation";
import { localeLabels, type Locale } from "@/i18n/routing";
import { contentBlockLink } from "@/lib/content-blocks";
import { guideAffiliateDestination, guideAffiliateModules, guideAffiliatePlacement } from "@/lib/guide-affiliate";
import { guideHref, guideListHref, type GuideArticleState, type GuideKind } from "@/lib/guides";

/** One label per kind (the badge above the title) plus the words around dates and sources. */
export type GuideArticleLabels = Record<GuideKind, string> & {
  published: string;
  updated: string;
  expiredNotice: string;
  validUntil: string;
  sources: string;
  checkedOn: string;
  destination: string;
  otherLanguages: string;
};

/**
 * An article a reader can reach. Expiry is shown, not hidden: an `intel` notice keeps its
 * URL so existing links do not break, and says plainly what date it applied until.
 *
 * The end of the article runs: body, partner panel (if any), `related`, topic chips,
 * sources, other languages. `related` is whatever the page fetched to hand the reader on --
 * for a lifestyle article the travel crosslinks -- and stays a plain node so this component
 * remains synchronous and renders directly under React Testing Library.
 */
export function GuideArticle({
  state, labels, related,
}: {
  state: GuideArticleState & { document: NonNullable<GuideArticleState["document"]> };
  labels: GuideArticleLabels;
  related?: ReactNode;
}) {
  const { document } = state;
  const published = document.published_at.slice(0, 10);
  const others = state.published_locales.filter((value) => value !== state.locale);
  // Partner buttons only where they are contextual: a destination the article belongs to,
  // a module its topics point at, and a notice that still applies. An expired fare deal
  // with a "book flights" button underneath would read as bait.
  //
  // A `life` article is the exception recorded in lib/guide-affiliate.ts: lifestyle topics
  // point at no module, so the destination the editor deliberately filled in is the only
  // contextual signal and the panel shows every module, exactly like the city page's own.
  // It is rendered non-contextual so its heading names the destination's partners rather
  // than inviting the reader to "keep exploring" a place the article was never about.
  const affiliateDestination = guideAffiliateDestination(state.destination_id);
  const affiliateModules = guideAffiliateModules(state.topics, state.kind);
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
        <p className="mt-3 text-sm text-[var(--muted)]">
          {labels.published}: <time dateTime={published}>{published}</time>
        </p>
        {state.expired && state.valid_until ? (
          <p role="status" className="mt-4 rounded-2xl border border-[var(--line)] bg-[var(--line)] px-4 py-3 text-sm leading-6">
            {labels.expiredNotice} {labels.validUntil}: <time dateTime={state.valid_until}>{state.valid_until}</time>
          </p>
        ) : null}
      </header>

      <ContentBlocks blocks={document.blocks} />

      {showAffiliate && affiliateDestination ? (
        <DestinationAffiliateOptions
          destinationId={affiliateDestination}
          modules={affiliateModules}
          contextual={state.kind !== "life"}
          destinationLabel={state.destination_label ?? undefined}
          placement={guideAffiliatePlacement(state.kind)}
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
