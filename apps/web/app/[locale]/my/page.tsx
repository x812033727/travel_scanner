import { SiteHeader } from "@/components/site-header";
import { MyDirectory } from "@/components/community/home";
import { getTranslations } from "next-intl/server";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("mySpaceTitle"), description: t("mySpaceDescription"), robots: { index: false, follow: true } };
}
export default async function Page() { const t = await getTranslations("community"); return <><SiteHeader /><main className="mx-auto max-w-4xl px-5 py-10"><h1 className="mb-6 text-3xl font-bold">{t("my")}</h1><MyDirectory /></main></>; }
