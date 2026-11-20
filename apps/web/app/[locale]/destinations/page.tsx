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
function offline(t: (key: string) => string, locale: Locale): DestinationSummary[] {
  const order = new Map(countryKeys.map((code, index) => [code, index]));
  return [...destinationSeeds]
    .sort((left, right) => (order.get(left.country) ?? 0) - (order.get(right.country) ?? 0))
    .map((seed) => ({
      id: seed.id,
      city: t(`cities.${seed.id}.name`),
      localName: null,
      englishName: null,
      country: t(`countries.${seed.country}.name`),
      countryCode: seed.country,
      role: "primary" as const,
      parentDestinationId: null,
      extensionIds: [],
      areas: locale === "zh-TW" ? seed.areas : [],
      recommendedDays: seed.recommendedDays,
      timezone: seed.timezone,
      currency: seed.currency,
      center: null,
      reason: t(`cities.${seed.id}.summary`),
    }));
}

export default async function DestinationsPage({ params }: { params: Promise<{ locale: Locale }> }) {
  const { locale } = await params;
  const [rows, common, nav, catalog] = await Promise.all([
    getDestinations(locale),
    getTranslations({ locale, namespace: "common" }),
    getTranslations({ locale, namespace: "navigation" }),
    getTranslations({ locale, namespace: "search.catalog" }),
  ]);
  const copy = destinationsCopy(locale);
  const destinations = rows ?? offline(catalog, locale);

  // Group under the localized country label the API already returned; the offline copy translates
  // country names via `search.catalog` and preserves the two-letter `countryCode` for anchor IDs.
  const groups = new Map<string, DestinationSummary[]>();
  for (const destination of destinations) {
    // `country` is the localized label; the code is the fallback grouping key, and it also becomes
    // the visible <h2>, so blanks must not get through.
    const key = destination.country || destination.countryCode || copy.indexTitle;
    groups.set(key, [...(groups.get(key) ?? []), destination]);
  }
  const countrySections = [...groups].map(([country, items], index) => {
    const rawCode = items[0]?.countryCode?.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/^-|-$/g, "");
    const sectionId = rawCode ? `country-${rawCode}` : `country-${index + 1}`;
    return { country, items, sectionId };
  });

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [{ name: nav("home"), path: "/" }, { name: copy.breadcrumb, path: "/destinations" }]),
          itemList(locale, destinations.map((destination) => ({ name: destination.city, path: `/destinations/${destination.id}` }))),
        ]}
      />
      <main className="mx-auto max-w-5xl px-5 py-6 sm:py-10 md:px-8">
        <nav aria-label={common("guides.breadcrumb")} className="flex flex-wrap items-center gap-x-1.5 gap-y-0.5 text-[length:var(--text-meta)] text-[var(--muted)]">
          <Link className="inline-flex min-h-11 items-center underline decoration-[var(--line)] underline-offset-4 transition-colors hover:text-[var(--teal)] hover:decoration-[var(--teal)]" href="/">
            {nav("home")}
          </Link>
          <span aria-hidden>›</span>
          <span aria-current="page" className="py-1.5 font-medium text-[var(--ink)]">{copy.breadcrumb}</span>
        </nav>

        <header className="portal-hero-shell mt-2 rounded-3xl p-6 sm:p-8 md:p-10">
          <h1 className="text-3xl font-extrabold tracking-tight sm:text-4xl md:text-5xl">{copy.indexTitle}</h1>
          <p className="mt-4 max-w-2xl text-lg leading-8 text-[var(--muted)]">{copy.indexIntro}</p>
          {countrySections.length > 1 ? (
            <nav
              aria-label={copy.indexTitle}
              data-testid="destinations-country-nav"
              className="portal-scroll-strip mt-5 flex items-center gap-2 sm:flex-wrap sm:overflow-visible"
            >
              {countrySections.map(({ country, items, sectionId }) => (
                <a key={sectionId} href={`#${sectionId}`} className="app-filter-chip shrink-0">
                  <span>{country}</span>
                  <span className="text-[length:var(--text-xs)] text-[var(--muted)]">({items.length})</span>
                </a>
              ))}
            </nav>
          ) : null}
        </header>

        {countrySections.map(({ country, items, sectionId }) => (
          <section key={country} id={sectionId} className="mt-10 scroll-mt-24">
            <h2 className="portal-section-heading text-2xl font-extrabold tracking-tight">{country}</h2>
            <ul className="mt-4 grid gap-4 sm:grid-cols-2">
              {items.map((destination) => (
                <li
                  key={destination.id}
                  className="portal-card-surface group relative flex flex-col justify-between rounded-2xl p-4 sm:p-5"
                >
                  <div>
                    <div className="flex flex-wrap items-start justify-between gap-2">
                      <h3 className="text-lg font-bold tracking-tight">
                        <Link
                          className="text-[var(--ink)] underline-offset-4 after:absolute after:inset-0 after:content-[''] group-hover:text-[var(--teal)] group-hover:underline"
                          href={`/destinations/${destination.id}`}
                        >
                          {destination.city}
                        </Link>
                      </h3>
                      {destination.recommendedDays ? (
                        <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-0.5 text-[length:var(--text-xs)] font-semibold text-[var(--teal)]">
                          {copy.factsDays}: {destination.recommendedDays.min}–{destination.recommendedDays.max} {copy.daysUnit}
                        </span>
                      ) : null}
                    </div>
                    {destination.reason ? (
                      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{destination.reason}</p>
                    ) : null}
                  </div>
                  {destination.areas.length ? (
                    <div className="mt-auto flex flex-wrap gap-1.5 pt-3">
                      {destination.areas.slice(0, 3).map((area) => (
                        <span
                          key={area}
                          className="rounded-full border border-[var(--line)] bg-[var(--paper)] px-2.5 py-0.5 text-[length:var(--text-xs)] text-[var(--muted)]"
                        >
                          {area}
                        </span>
                      ))}
                    </div>
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
