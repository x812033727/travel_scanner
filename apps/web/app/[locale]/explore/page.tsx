import { SiteHeader } from "@/components/site-header";
import { TravelExplore } from "@/components/community/explore";
import { getTranslations } from "next-intl/server";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("exploreTitle"), description: t("exploreDescription"), robots: { index: false, follow: true } };
}
export default async function Page() { const t = await getTranslations("community"); return <><SiteHeader /><main className="mx-auto max-w-5xl px-5 py-10"><h1 className="mb-6 text-3xl font-bold">{t("exploreTravel")}</h1><TravelExplore /></main></>; }
