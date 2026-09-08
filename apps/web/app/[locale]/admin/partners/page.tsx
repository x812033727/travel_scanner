import { Suspense } from "react";
import { getLocale } from "next-intl/server";
import { TravelServicesAdmin } from "@/components/travel-services/admin";
import { adminHotelsCopy } from "@/lib/admin-hotels-copy";

export default async function PartnersAdminPage() {
  const copy = adminHotelsCopy(await getLocale());
  return <main className="admin-page">
    <h1 className="text-3xl font-bold">{copy.partnersTitle}</h1>
    <p className="mt-3 text-[var(--muted)]">{copy.partnersIntro}</p>
    <Suspense><TravelServicesAdmin workspace="partners" /></Suspense>
  </main>;
}
