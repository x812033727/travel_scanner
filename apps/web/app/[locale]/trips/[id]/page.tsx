import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { SiteHeader } from "@/components/site-header";
import { TripEditor } from "@/components/trip-editor";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("tripTitle"), description: t("tripDescription") };
}

export default async function TripPage({
  params,
}: {
  params: Promise<{ id: string; locale: Locale }>;
}) {
  const { id } = await params;
  return <><div className="hidden lg:block"><SiteHeader /></div><TripEditor tripId={id} /></>;
}
