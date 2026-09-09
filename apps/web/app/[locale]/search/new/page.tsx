import { getLocale, getTranslations } from "next-intl/server";
import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";
import { SiteHeader } from "@/components/site-header";
import { SearchWorkbench } from "@/components/search-workbench";
import { frontendCopy } from "@/lib/frontend-navigation";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("newSearchTitle"), description: t("newSearchDescription") };
}

export default async function SearchNewPage() {
  const copy = frontendCopy(await getLocale());
  return <><SiteHeader /><main className="mx-auto max-w-4xl px-5 pb-28 pt-7 md:pt-12">
    <h1 className="mb-6 text-3xl font-bold">{copy.searchTitle}</h1>
    <SearchWorkbench compact />
  </main></>;
}
