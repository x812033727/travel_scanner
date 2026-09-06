import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { ExploreSwitch } from "@/components/explore-switch";
import { HotspotExplorer } from "@/components/hotspot-explorer";
import { SiteHeader } from "@/components/site-header";
import { getInitialHotspots } from "@/lib/hotspots.server";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("hotspotsTitle"), description: t("hotspotsDescription") };
}

const first = (value: string | string[] | undefined) => (Array.isArray(value) ? value[0] : value) || "";

export default async function HotspotsPage({
  params,
  searchParams,
}: {
  params: Promise<{ locale: Locale }>;
  searchParams: Promise<Record<string, string | string[] | undefined>>;
}) {
  const [{ locale }, query] = await Promise.all([params, searchParams]);
  // The same three filters the explorer reads out of the address bar on mount, so
  // a shared link renders its own list rather than the global ranking.
  const filters = {
    category: first(query.category),
    destinationId: first(query.destination_id),
    area: first(query.area),
    theme: first(query.theme).trim(),
  };
  const initial = await getInitialHotspots(locale, filters);
  return (
    <>
      <SiteHeader />
      <ExploreSwitch />
      <HotspotExplorer initialRanking={initial.ranking} initialFacets={initial.facets} initialFilters={filters} />
    </>
  );
}
