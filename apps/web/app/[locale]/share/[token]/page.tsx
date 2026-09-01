import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { SharedTripView } from "@/components/shared-trip-view";
import { SiteHeader } from "@/components/site-header";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("shareTitle"), description: t("shareDescription"), openGraph: { images: [] }, twitter: { images: [] } };
}

export default async function SharePage({
  params,
}: {
  params: Promise<{ token: string; locale: Locale }>;
}) {
  const { token } = await params;
  return <><SiteHeader /><SharedTripView token={token} /></>;
}
