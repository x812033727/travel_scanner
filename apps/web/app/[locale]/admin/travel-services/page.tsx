import { Suspense } from "react";
import { getLocale, getTranslations } from "next-intl/server";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import { TravelServicesAdmin } from "@/components/travel-services/admin";

export default async function TravelServicesAdminPage() {
  const t = await getTranslations("travelServices");
  const copy = adminDomainsCopy(await getLocale());
  return <main className="admin-page"><h1 className="text-3xl font-bold">{copy.otherServices}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("adminIntro")}</p><Suspense fallback={<p>{copy.loading}</p>}><TravelServicesAdmin /></Suspense></main>;
}
