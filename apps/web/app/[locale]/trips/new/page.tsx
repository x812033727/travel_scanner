import { NewTripAuthGate } from "@/components/new-trip-auth-gate";
import { SiteHeader } from "@/components/site-header";
import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("newTripTitle"), description: t("newTripDescription") };
}


export default async function NewTripPage({ searchParams }: { searchParams: Promise<{ resume_plan?: string }> }) {
  const query = await searchParams;
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 pb-20 pt-4 md:px-8"><NewTripAuthGate resumePlanning={query.resume_plan === "1"} /></main></>;
}
