import { Link } from "@/i18n/navigation";
import { guideListHref, type DestinationFacet, type TravelGuideKind } from "@/lib/guides";

export type DestinationGroupLabels = { heading: string; lead: string; countryAll: string };

/** The catalog's country order is the display order; within a country, the API's order. */
export function groupByCountry(destinations: DestinationFacet[]) {
  const groups: { country: string; label: string; cities: DestinationFacet[]; count: number }[] = [];
  for (const facet of destinations) {
    if (facet.count <= 0) continue;
    let group = groups.find((item) => item.country === facet.country);
    if (!group) {
      group = { country: facet.country, label: facet.country_label, cities: [], count: 0 };
      groups.push(group);
    }
    group.cities.push(facet);
    group.count += facet.count;
  }
  return groups;
}

/**
 * "Browse by destination" on the travel hub: one block per country, its cities as pills,
 * each with how many articles this language has for it. Both links are the listing's own
 * filtered views (`?country=`, `?destination=`), which stay `noindex` as every filtered
 * listing does; the hub itself is what ranks.
 */
export function DestinationGroups({
  destinations, kind = "howto", labels,
}: {
  destinations: DestinationFacet[];
  kind?: TravelGuideKind;
  labels: DestinationGroupLabels;
}) {
  const groups = groupByCountry(destinations);
  if (!groups.length) return null;
  const listing = guideListHref(kind);
  return (
    <section className="mt-12 border-t border-[var(--line)] pt-8" data-testid="destination-groups">
      <h2 className="text-2xl font-bold tracking-tight">{labels.heading}</h2>
      <p className="mt-2 max-w-2xl leading-7 text-[var(--muted)]">{labels.lead}</p>
      <ul className="mt-4 grid gap-4 sm:grid-cols-2">
        {groups.map((group) => (
          <li key={group.country} className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4">
            <h3 className="text-lg font-semibold">
              <Link
                className="inline-flex min-h-11 items-center gap-2 text-[var(--teal)] underline underline-offset-4"
                href={`${listing}?country=${encodeURIComponent(group.country)}`}
              >
                {labels.countryAll.replace("{country}", group.label)}
              </Link>
            </h3>
            <ul className="mt-2 flex flex-wrap gap-2">
              {group.cities.map((city) => (
                <li key={city.id}>
                  <Link
                    className="app-filter-chip"
                    href={`${listing}?destination=${encodeURIComponent(city.id)}`}
                  >
                    {city.label}
                  </Link>
                </li>
              ))}
            </ul>
          </li>
        ))}
      </ul>
    </section>
  );
}
