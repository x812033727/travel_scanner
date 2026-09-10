import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { Link } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { countryKeys, destinationSeeds } from "@/lib/destinations";
import { destinationsCopy } from "@/lib/destinations-copy";
import { getDestinations, type DestinationSummary } from "@/lib/destinations.server";
import { breadcrumbs, itemList } from "@/lib/structured-data";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("destinationsTitle"), description: t("destinationsDescription") };
}

/** The offline catalog carries 19 of the 33 destinations and its names live in `search.catalog`.
 *  Fewer cities beats an empty page while the API is unreachable. */
function offline(t: (key: string) => string): DestinationSummary[] {
  const order = new Map(countryKeys.map((code, index) => [code, index]));
  return [...destinationSeeds]
    .sort((left, right) => (order.get(left.country) ?? 0) - (order.get(right.country) ?? 0))
    .map((seed) => ({
      id: seed.id,
      city: t(`cities.${seed.id}.name`),
      localName: null,
      englishName: null,
      country: seed.country,
      countryCode: seed.country,
      role: "primary" as const,
      parentDestinationId: null,
      extensionIds: [],
      areas: seed.areas,
      recommendedDays: seed.recommendedDays,
      timezone: seed.timezone,
      currency: seed.currency,
      center: null,
      reason: t(`cities.${seed.id}.summary`),
    }));
}

export default async function DestinationsPage({ params }: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params;
  const [rows, nav, catalog] = await Promise.all([
    getDestinations(locale),
    getTranslations({ locale, namespace: "navigation" }),
    getTranslations({ locale, namespace: "search.catalog" }),
  ]);
  const copy = destinationsCopy(locale);
  const destinations = rows ?? offline(catalog);

  // Group under the localized country label the API already returned; the offline copy only has
  // the two-letter code, which is still a stable grouping key.
  const groups = new Map<string, DestinationSummary[]>();
  for (const destination of destinations) {
    const key = destination.country || destination.countryCode;
    groups.set(key, [...(groups.get(key) ?? []), destination]);
  }

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [{ name: nav("home"), path: "/" }, { name: copy.breadcrumb, path: "/destinations" }]),
          itemList(locale, destinations.map((destination) => ({ name: destination.city, path: `/destinations/${destination.id}` }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-10 md:px-8">
        <h1 className="text-4xl font-bold tracking-tight">{copy.indexTitle}</h1>
        <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{copy.indexIntro}</p>
        {[...groups].map(([country, items]) => (
          <section key={country} className="mt-10">
            <h2 className="text-2xl font-bold tracking-tight">{country}</h2>
            <ul className="mt-4 grid gap-3 sm:grid-cols-2">
              {items.map((destination) => (
                <li key={destination.id} className="rounded-2xl border border-[var(--line)] p-4">
                  <h3 className="text-lg font-bold">
                    <Link className="text-[var(--teal)] underline" href={`/destinations/${destination.id}`}>
                      {destination.city}
                    </Link>
                  </h3>
                  {destination.reason ? <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{destination.reason}</p> : null}
                  {destination.recommendedDays.min ? (
                    <p className="mt-2 text-xs font-semibold uppercase tracking-wide text-[var(--muted)]">
                      {copy.factsDays}: {destination.recommendedDays.min}–{destination.recommendedDays.max} {copy.daysUnit}
                    </p>
                  ) : null}
                </li>
              ))}
            </ul>
          </section>
        ))}
      </main>
    </>
  );
}
