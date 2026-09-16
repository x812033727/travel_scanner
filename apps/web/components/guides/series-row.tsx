import { Link } from "@/i18n/navigation";
import type { SeriesSummary } from "@/lib/guide-series";
import { guideHref } from "@/lib/guides";

export type SeriesRowLabels = {
  heading: string;
  lead: string;
  /** ICU-free: `{count}` is replaced here. */
  entries: string;
};

/** A registry row plus, optionally, the sentence the page wants under it instead of the hub
 *  article's description -- the Gemini series, whose visible lesson count the web decides. */
export type SeriesRowItem = SeriesSummary & { note?: string | null };

/**
 * The series and tutorial hubs a section offers, from `GET /guides/series`: one card per
 * hub published in this language, in registry order. One link per card, to the hub
 * article, so a page that counts links to a hub (the Gemini e2e does) sees exactly one.
 */
export function SeriesRow({ series, labels }: { series: readonly SeriesRowItem[]; labels: SeriesRowLabels }) {
  if (!series.length) return null;
  return (
    <section aria-labelledby="series-row-heading" className="mt-10" data-testid="series-row">
      <h2 id="series-row-heading" className="text-2xl font-bold tracking-tight">{labels.heading}</h2>
      <p className="mt-2 max-w-2xl leading-7 text-[var(--muted)]">{labels.lead}</p>
      <ul className="mt-4 grid gap-3 sm:grid-cols-2">
        {series.map((item) => {
          const note = item.note ?? item.hub.description;
          return (
            <li key={item.slug} className="rounded-2xl border border-[var(--teal)] bg-[var(--paper)] p-4">
              <h3 className="text-lg font-bold">
                <Link
                  className="inline-flex min-h-11 items-center text-[var(--teal)] underline-offset-4 hover:underline"
                  href={guideHref(item.hub.kind, item.hub.slug)}
                >
                  {item.hub.title}
                </Link>
              </h3>
              {note ? <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{note}</p> : null}
              {item.entries ? (
                <p className="mt-2 text-[length:var(--text-meta)] text-[var(--muted)]">
                  {labels.entries.replace("{count}", String(item.entries))}
                </p>
              ) : null}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
