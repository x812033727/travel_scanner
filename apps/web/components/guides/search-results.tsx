import { Fragment } from "react";
import { GuideImage } from "./guide-image";
import { Link } from "@/i18n/navigation";
import { guideHref, highlight, visibleGuideHero, type GuideKind, type GuideSearchHit } from "@/lib/guides";

export type SearchResultLabels = Record<GuideKind, string>;

/** The runs of `text` that matched, wrapped in `<mark>`; the rest as plain text nodes. */
export function Highlighted({ text, terms }: { text: string; terms: readonly string[] }) {
  return (
    <>
      {highlight(text, terms).map((segment, index) =>
        segment.hit
          ? <mark key={index} className="rounded bg-[var(--teal-soft)] px-1 font-semibold text-[var(--teal-dark)]">{segment.text}</mark>
          : <Fragment key={index}>{segment.text}</Fragment>,
      )}
    </>
  );
}

/**
 * One result. Like a `GuideCard`, but the description gives way to the passage the match
 * was found in, and the words the reader typed are marked in the title and the passage so
 * they can see *why* this article answers. The hero is kept small: a results list is
 * scanned, not browsed.
 */
export function SearchResultCard({ hit, labels }: { hit: GuideSearchHit; labels: SearchResultLabels }) {
  const hero = visibleGuideHero(hit.hero);
  return (
    <li className="portal-card-surface group relative flex items-start gap-3.5 rounded-2xl p-4 sm:gap-4 sm:p-5">
      {hero ? (
        <GuideImage
          src={hero.src}
          alt=""
          width={hero.width}
          height={hero.height}
          loading="lazy"
          decoding="async"
          className="hidden h-20 w-24 flex-none rounded-xl object-cover ring-1 ring-black/5 min-[380px]:block sm:aspect-video sm:h-auto sm:w-36"
        />
      ) : null}
      <div className="min-w-0 flex-1">
        <p className="flex flex-wrap items-center gap-2 text-[length:var(--text-xs)] font-semibold uppercase tracking-wide text-[var(--muted)]">
          <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[var(--teal-dark)]">{labels[hit.kind]}</span>
          {hit.news_date ? (
            <time dateTime={hit.news_date} className="font-mono tabular-nums">
              {hit.news_date}
            </time>
          ) : null}
          {hit.destination_label ? <span>{hit.destination_label}</span> : null}
          {hit.topics.slice(0, 2).map((topic) => <span key={topic.slug}>{topic.label}</span>)}
        </p>
        <h3 className="mt-2 text-[1.0625rem] font-bold leading-snug tracking-tight sm:text-lg">
          <Link
            className="text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
            href={guideHref(hit.kind, hit.slug)}
          >
            <Highlighted text={hit.title} terms={hit.matched} />
          </Link>
        </h3>
        <p className="mt-1.5 text-sm leading-6 text-[var(--muted)] sm:mt-2">
          <Highlighted text={hit.snippet || hit.description} terms={hit.matched} />
        </p>
      </div>
    </li>
  );
}

export function SearchResults({ hits, labels }: { hits: GuideSearchHit[]; labels: SearchResultLabels }) {
  if (!hits.length) return null;
  return (
    <ol className="mt-6 grid gap-3.5">
      {hits.map((hit) => <SearchResultCard key={`${hit.kind}:${hit.slug}`} hit={hit} labels={labels} />)}
    </ol>
  );
}
