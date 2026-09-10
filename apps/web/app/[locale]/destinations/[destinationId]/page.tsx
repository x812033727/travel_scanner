import type { Metadata } from "next";
import { notFound } from "next/navigation";
import { getTranslations } from "next-intl/server";
import { DestinationGuide } from "@/components/destination-guide";
import { SiteHeader } from "@/components/site-header";
import { StructuredData } from "@/components/structured-data";
import { PUBLIC_DESTINATIONS } from "@/components/travel-services/options";
import type { Locale } from "@/i18n/routing";
import { destinationsCopy } from "@/lib/destinations-copy";
import { getDestination, getDestinations, getGuideMerchants, getGuidePlaces } from "@/lib/destinations.server";
import { breadcrumbs, touristDestination } from "@/lib/structured-data";

type Params = { locale: Locale; destinationId: string };

const known = (id: string) => (PUBLIC_DESTINATIONS as readonly string[]).includes(id);

export async function generateMetadata({ params }: { params: Promise<Params> }): Promise<Metadata> {
  const { locale, destinationId } = await params;
  if (!known(destinationId)) return {};
  const destination = await getDestination(locale, destinationId);
  if (!destination) return {};
  const copy = destinationsCopy(locale);
  return {
    title: `${destination.city} | Mokaair`,
    description: destination.reason || copy.indexIntro,
  };
}

export default async function DestinationGuidePage({ params }: { params: Promise<Params> }) {
  const { locale, destinationId } = await params;
  if (!known(destinationId)) notFound();

  const [all, places, merchants, nav] = await Promise.all([
    getDestinations(locale),
    getGuidePlaces(locale, destinationId),
    getGuideMerchants(locale, destinationId),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  // Two different failures, two different answers. A catalog that could not be read at all is an
  // outage: throwing gives a 5xx, which tells a crawler to come back, where a 404 would invite it
  // to drop a real page and an empty 200 would get one indexed as thin content. A catalog that
  // loaded but does not carry this slug is drift between PUBLIC_DESTINATIONS and the API, and
  // then the destination really is absent, so 404 is the honest answer.
  if (all === null) throw new Error(`Destination catalog unavailable for ${destinationId}`);
  const destination = all.find((row) => row.id === destinationId);
  if (!destination) notFound();

  const copy = destinationsCopy(locale);
  const byId = new Map((all ?? []).map((row) => [row.id, row]));
  const related = [destination.parentDestinationId, ...destination.extensionIds]
    .filter((id): id is string => Boolean(id))
    .map((id) => byId.get(id))
    .filter((row) => row !== undefined);

  return (
    <>
      <SiteHeader />
      <StructuredData
        data={[
          breadcrumbs(locale, [
            { name: nav("home"), path: "/" },
            { name: copy.breadcrumb, path: "/destinations" },
            { name: destination.city, path: `/destinations/${destination.id}` },
          ]),
          touristDestination(locale, {
            name: destination.city,
            path: `/destinations/${destination.id}`,
            description: destination.reason,
            country: destination.country,
            alternateName: [destination.localName, destination.englishName].filter((value): value is string => Boolean(value)),
            center: destination.center,
          }),
        ]}
      />
      <DestinationGuide locale={locale} destination={destination} places={places} merchants={merchants} related={related} />
    </>
  );
}
