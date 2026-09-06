import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { ShareTargetView } from "@/components/share-target-view";
import { SiteHeader } from "@/components/site-header";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("tripTitle"), description: t("tripDescription"), robots: { index: false } };
}

/** Where Android's share sheet drops a place: text in, a trip's waiting list out. */
export default async function ShareTargetPage({
  searchParams,
}: {
  searchParams: Promise<{ text?: string; url?: string; title?: string }>;
}) {
  const shared = await searchParams;
  const lines = [shared.url, shared.text, shared.title].filter(Boolean) as string[];
  return <><SiteHeader /><ShareTargetView shared={[...new Set(lines)].join("\n")} /></>;
}
