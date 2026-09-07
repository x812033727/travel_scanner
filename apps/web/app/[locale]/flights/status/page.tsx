import type { Metadata } from "next";
import { Suspense } from "react";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { FlightStatusSearch } from "@/components/flight-status-search";
import { SiteHeader } from "@/components/site-header";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("flightStatusTitle"), description: t("flightStatusDescription") };
}

export default function FlightStatusPage() {
  // The component reads `trip_id`/`flight_number` from the query string, which needs
  // a boundary or the whole route opts out of static rendering.
  return <><SiteHeader /><Suspense><FlightStatusSearch /></Suspense></>;
}
