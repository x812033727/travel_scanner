import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { ServiceCatalog } from "@/components/travel-services/catalog";
import { CITIES, KINDS, type Kind } from "@/components/travel-services/options";
import { Link } from "@/i18n/navigation";
import { locales, type Locale } from "@/i18n/routing";

type Params = { locale: Locale; destinationId: string };

export async function generateMetadata({
  params,
}: {
  params: Promise<Params>;
}): Promise<Metadata> {
  const { locale, destinationId } = await params;
  if (!CITIES.includes(destinationId as (typeof CITIES)[number])) notFound();
  const t = await getTranslations({ locale, namespace: "travelServices" });
  const path = `/destinations/${destinationId}/services`;
  return {
    title: `${t(destinationId)} · ${t("title")}`,
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
  const [{ destinationId }, query, t] = await Promise.all([
    params,
    searchParams,
    getTranslations("travelServices"),
  ]);
  if (!CITIES.includes(destinationId as (typeof CITIES)[number])) notFound();
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-6xl px-4 py-8 sm:px-6 sm:py-12">
        <p className="text-sm font-bold tracking-widest text-[var(--teal)]">
          {t(destinationId)}
        </p>
        <h1 className="mt-2 text-3xl font-bold sm:text-4xl">{t("title")}</h1>
        <p className="mb-6 mt-3 max-w-2xl leading-7 text-[var(--muted)]">
          {t("intro")}
        </p>
        <nav
          className="mb-7 flex flex-wrap gap-2"
          aria-label={t("destinationLink")}
        >
          {CITIES.map((city) => (
            <Link
              key={city}
              href={`/destinations/${city}/services`}
              aria-current={city === destinationId ? "page" : undefined}
              className="flex min-h-11 items-center rounded-full border border-[var(--line)] px-4 text-sm aria-[current=page]:bg-[var(--teal-soft)]"
            >
              {t(city)}
            </Link>
          ))}
        </nav>
        <ServiceCatalog
          key={destinationId}
          destinationId={destinationId}
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
      </main>
    </>
  );
}
