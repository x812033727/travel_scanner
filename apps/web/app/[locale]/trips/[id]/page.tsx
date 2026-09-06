import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { OfflineTripCache } from "@/components/offline-trip-cache";
import { SiteHeader } from "@/components/site-header";
import { TodayView } from "@/components/today-view";
import { TripEditor } from "@/components/trip-editor";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("tripTitle"), description: t("tripDescription") };
}

export default async function TripPage({
  params,
  searchParams,
}: {
  params: Promise<{ id: string; locale: Locale }>;
  searchParams: Promise<{ view?: string }>;
}) {
  const { id } = await params;
  const { view } = await searchParams;
  // ?view=today is the day itself: one column, now and next, readable without a signal.
  if (view === "today") {
    return <><div className="hidden lg:block"><SiteHeader /></div><OfflineTripCache /><TodayView tripId={id} /></>;
  }
  return <><div className="hidden lg:block"><SiteHeader /></div><OfflineTripCache /><TripEditor tripId={id} /></>;
}
