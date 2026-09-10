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

  const [destination, all, places, merchants, nav] = await Promise.all([
    getDestination(locale, destinationId),
    getDestinations(locale),
    getGuidePlaces(locale, destinationId),
    getGuideMerchants(locale, destinationId),
    getTranslations({ locale, namespace: "navigation" }),
  ]);

  // A known destination with no record means the catalog could not be read. Throwing gives a 5xx,
  // which tells a crawler to come back; a 404 would invite it to drop a real page, and an empty
  // 200 would get the page indexed as thin content.
  if (!destination) throw new Error(`Destination catalog unavailable for ${destinationId}`);

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
