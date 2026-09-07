import { getTranslations } from "next-intl/server";
import { TravelServicesAdmin } from "@/components/travel-services/admin";

export default async function TravelServicesAdminPage() {
  const t = await getTranslations("travelServices");
  return <main className="admin-page"><h1 className="text-3xl font-bold">{t("adminTitle")}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("adminIntro")}</p><TravelServicesAdmin /></main>;
}
