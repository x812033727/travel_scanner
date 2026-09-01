import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { HotspotExplorer } from "@/components/hotspot-explorer";
import { SiteHeader } from "@/components/site-header";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("hotspotsTitle"), description: t("hotspotsDescription") };
}

export default function HotspotsPage() {
  return <><SiteHeader /><HotspotExplorer /></>;
}
