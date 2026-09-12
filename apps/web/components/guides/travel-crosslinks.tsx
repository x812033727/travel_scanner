import { GuideCard, type GuideCardLabels } from "@/components/guides/card";
import { Link } from "@/i18n/navigation";
import type { GuideSummary } from "@/lib/guides";

export type TravelCrosslinksLabels = {
  relatedTravel: string;
  relatedDestinations: string;
  card: GuideCardLabels;
};

/** Never more than this many destination links; past six the row stops being a pick. */
export const TRAVEL_CROSSLINK_CITY_LIMIT = 6;

/**
 * The on-site handover at the end of a lifestyle article: the newest travel guides and a
 * handful of destination pages.
 *
 * Ordinary internal links only -- no partner buttons and no disclosure -- so it never reads
 * as a second offer panel. It is its own section with a top border, which keeps it visibly
 * apart from the partner panel that may sit directly above it (docs/travel-services.md:
 * ordinary links are separated from commission-bearing offers). Synchronous and purely
 * presentational: the article page fetches, this only renders what it is handed.
 */
export function TravelCrosslinks({
  articles, cities, labels,
}: {
  articles: GuideSummary[];
  cities: { id: string; name: string }[];
  labels: TravelCrosslinksLabels;
}) {
  const shown = cities.slice(0, TRAVEL_CROSSLINK_CITY_LIMIT);
  if (!articles.length && !shown.length) return null;
  return (
    <section data-testid="travel-crosslinks" className="space-y-8 border-t border-[var(--line)] pt-6">
      {articles.length ? (
        <div>
          <h2 className="text-lg font-semibold">{labels.relatedTravel}</h2>
          <ul className="mt-3 grid gap-3 md:grid-cols-3">
            {articles.map((article) => (
              <GuideCard key={`${article.kind}:${article.slug}`} article={article} labels={labels.card} />
            ))}
          </ul>
        </div>
      ) : null}

      {shown.length ? (
        <div>
          <h2 className="text-lg font-semibold">{labels.relatedDestinations}</h2>
          <ul className="mt-3 flex flex-wrap gap-2">
            {shown.map((city) => (
              <li key={city.id}>
                <Link
                  className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] px-4 py-1 text-sm font-semibold"
                  href={`/destinations/${city.id}`}
                >
                  {city.name}
                </Link>
              </li>
            ))}
          </ul>
        </div>
      ) : null}
    </section>
  );
}
