import { Fragment } from "react";
import { GuideImage } from "./guide-image";
import { Link } from "@/i18n/navigation";
import { guideHref, highlight, type GuideKind, type GuideSearchHit } from "@/lib/guides";

export type SearchResultLabels = Record<GuideKind, string>;

/** The runs of `text` that matched, wrapped in `<mark>`; the rest as plain text nodes. */
export function Highlighted({ text, terms }: { text: string; terms: readonly string[] }) {
  return (
    <>
      {highlight(text, terms).map((segment, index) =>
        segment.hit
          ? <mark key={index} className="rounded bg-[var(--teal-soft)] px-0.5 text-inherit">{segment.text}</mark>
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
  return (
    <li className="flex gap-4 rounded-2xl border border-[var(--line)] p-4">
      {hit.hero ? (
        <GuideImage
          src={hit.hero.src}
          alt=""
          width={hit.hero.width}
          height={hit.hero.height}
          loading="lazy"
          decoding="async"
          className="hidden aspect-video w-32 flex-none rounded-xl object-cover sm:block"
        />
      ) : null}
      <div className="min-w-0 flex-1">
        <p className="flex flex-wrap items-center gap-2 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">
          <span className="rounded-full bg-[var(--line)] px-2 py-1 text-[var(--fg)]">{labels[hit.kind]}</span>
          {hit.destination_label ? <span>{hit.destination_label}</span> : null}
          {hit.topics.slice(0, 2).map((topic) => <span key={topic.slug}>{topic.label}</span>)}
        </p>
        <h3 className="mt-2 text-lg font-bold">
          <Link className="text-[var(--teal)] underline" href={guideHref(hit.kind, hit.slug)}>
            <Highlighted text={hit.title} terms={hit.matched} />
          </Link>
        </h3>
        <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
          <Highlighted text={hit.snippet || hit.description} terms={hit.matched} />
        </p>
      </div>
    </li>
  );
}

export function SearchResults({ hits, labels }: { hits: GuideSearchHit[]; labels: SearchResultLabels }) {
  if (!hits.length) return null;
  return (
    <ol className="mt-6 grid gap-3">
      {hits.map((hit) => <SearchResultCard key={`${hit.kind}:${hit.slug}`} hit={hit} labels={labels} />)}
    </ol>
  );
}
