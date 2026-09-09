import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { DestinationAffiliateOptions } from "@/components/destination-affiliate-options";
import { ServiceCatalog } from "@/components/travel-services/catalog";
import {
  CITIES,
  KINDS,
  PUBLIC_DESTINATIONS,
  type Kind,
} from "@/components/travel-services/options";
import { Link } from "@/i18n/navigation";
import { locales, type Locale } from "@/i18n/routing";
import { serviceDiscoveryModules } from "@/lib/travel-service-discovery";

type Params = { locale: Locale; destinationId: string };
type DestinationItem = { id: string; city: string; country: string; role: string };
const SUPPORTED = new Set<string>([...PUBLIC_DESTINATIONS, ...CITIES]);

async function destinationCatalog(locale: Locale): Promise<DestinationItem[]> {
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  try {
    const response = await fetch(`${base}/api/v1/destinations`, {
      headers: { "x-travel-locale": locale },
      cache: "no-store",
    });
    if (!response.ok) return [];
    const value = (await response.json()) as { items?: DestinationItem[] };
    return value.items || [];
  } catch {
    return [];
  }
}

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { locale, destinationId } = await params;
  if (!SUPPORTED.has(destinationId)) notFound();
  const t = await getTranslations({ locale, namespace: "travelServices" });
  const destinations = await destinationCatalog(locale);
  const name =
    destinations.find((item) => item.id === destinationId)?.city ||
    (destinationId === "osaka" ? t("osaka") : destinationId === "kyoto" ? t("kyoto") : destinationId);
  const path = `/destinations/${destinationId}/services`;
  return {
    title: `${name} · ${t("title")}`,
    description: t("intro"),
    alternates: {
      canonical: `/${locale}${path}`,
      languages: Object.fromEntries(locales.map((l) => [l, `/${l}${path}`])),
    },
  };
}

export default async function DestinationServices({
  params,
  searchParams,
}: {
  params: Promise<Params>;
  searchParams: Promise<Record<string, string | undefined>>;
}) {
  const [{ locale, destinationId }, query, t] = await Promise.all([
    params,
    searchParams,
    getTranslations("travelServices"),
  ]);
  if (!SUPPORTED.has(destinationId)) notFound();
  const destinations = await destinationCatalog(locale);
  const selectedName =
    destinations.find((item) => item.id === destinationId)?.city ||
    (destinationId === "osaka" ? t("osaka") : destinationId === "kyoto" ? t("kyoto") : destinationId);
  const catalogCities =
    destinationId === "osaka-kyoto"
      ? ["osaka", "kyoto"]
      : CITIES.includes(destinationId as (typeof CITIES)[number])
        ? [destinationId]
        : [];
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
        <p className="text-sm font-bold tracking-widest text-[var(--teal)]">
          {selectedName}
        </p>
        <h1 className="mt-2 text-3xl font-bold sm:text-4xl">{t("title")}</h1>
        <p className="mb-6 mt-3 max-w-2xl leading-7 text-[var(--muted)]">
          {t("intro")}
        </p>
        <nav
          className="mb-7 flex flex-wrap gap-2"
          aria-label={t("destinationLink")}
        >
          {(destinations.length
            ? destinations
            : PUBLIC_DESTINATIONS.map((id) => ({ id, city: id, country: "", role: "" })))
            .map((city) => (
            <Link
              key={city.id}
              href={`/destinations/${city.id}/services`}
              aria-current={city.id === destinationId ? "page" : undefined}
              className="flex min-h-11 items-center rounded-full border border-[var(--line)] px-4 text-sm aria-[current=page]:bg-[var(--teal-soft)]"
            >
              {city.city}
            </Link>
          ))}
        </nav>
        {!catalogCities.length && <DestinationAffiliateOptions
          destinationId={
            destinationId === "osaka" || destinationId === "kyoto"
              ? "osaka-kyoto"
              : destinationId
          }
          destinationLabel={selectedName}
          modules={serviceDiscoveryModules(KINDS.includes(query.type as Kind) ? query.type as Kind : "all")}
          contextual
        />}
        {catalogCities.length ? (
          catalogCities.map((city, index) => (
            <ServiceCatalog
              key={city}
              destinationId={city}
              showDestinationDiscovery={index === 0}
              hotspotId={query.hotspot_id}
              initialKind={
                KINDS.includes(query.type as Kind)
                  ? (query.type as Kind)
                  : undefined
              }
              initialRadius={
                ["1", "3", "5"].includes(query.radius_km || "")
                  ? query.radius_km
                  : "3"
              }
              areaCode={query.area}
              initialFilters={query}
            />
          ))
        ) : (
          <p className="rounded-2xl border border-[var(--line)] bg-[var(--surface-raised)] p-5 text-sm text-[var(--muted)]">
            {t("destinationProductsPending")}
          </p>
        )}
      </main>
    </>
  );
}
