import { Link } from "@/i18n/navigation";
import type { SeriesSummary } from "@/lib/guide-series";
import { guideHref } from "@/lib/guides";

export type SeriesRowLabels = {
  heading: string;
  lead: string;
};

/** A registry row plus, optionally, the sentence the page wants under it instead of the hub
 *  article's description. */
export type SeriesRowItem = SeriesSummary & { note?: string | null };

/**
 * The series and tutorial hubs a topic offers, from `GET /guides/series`: one card per hub
 * published in this language, in registry order. One link per card, to the hub article, so
 * a page that counts links to a hub (the Gemini e2e does) sees exactly one.
 *
 * This sits on the topic hubs rather than the section hub. A series belongs to one topic
 * (`SeriesSummary.topic`), so the reader who has chosen that topic is the one it answers;
 * on the section hub it competed with the topics themselves for the same attention.
 *
 * No lesson count: a series gains articles, so the figure aged into a lie between deploys.
 */
export function SeriesRow({ series, labels }: { series: readonly SeriesRowItem[]; labels: SeriesRowLabels }) {
  if (!series.length) return null;
  return (
    <section aria-labelledby="series-row-heading" className="mt-10" data-testid="series-row">
      <h2 id="series-row-heading" className="text-2xl font-extrabold tracking-tight">{labels.heading}</h2>
      <p className="mt-2 max-w-2xl leading-7 text-[var(--muted)]">{labels.lead}</p>
      <ul className="mt-4 grid gap-4 sm:grid-cols-2">
        {series.map((item) => {
          const note = item.note ?? item.hub.description;
          return (
            <li
              key={item.slug}
              className="group relative rounded-2xl border border-[var(--line)] border-l-4 border-l-[var(--teal)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] transition-all duration-200 hover:-translate-y-0.5 hover:border-[var(--teal)] hover:shadow-[var(--shadow-md)]"
            >
              <h3 className="text-lg font-bold tracking-tight">
                <Link
                  className="inline-flex min-h-11 items-center text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
                  href={guideHref(item.hub.kind, item.hub.slug)}
                >
                  {item.hub.title}
                </Link>
              </h3>
              {note ? <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{note}</p> : null}
            </li>
          );
        })}
      </ul>
    </section>
  );
}
