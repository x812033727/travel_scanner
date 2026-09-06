import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { TripPrintView } from "@/components/trip-print-view";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("tripTitle"), description: t("tripDescription"), robots: { index: false } };
}

/** The printable itinerary: no header, no map, no buttons — one day per page. */
export default async function TripPrintPage({
  params,
}: {
  params: Promise<{ id: string; locale: Locale }>;
}) {
  const { id } = await params;
  return <TripPrintView tripId={id} />;
}
