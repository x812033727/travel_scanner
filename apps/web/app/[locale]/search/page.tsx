import { Suspense } from "react";
import { getTranslations } from "next-intl/server";
import { SearchExperience } from "@/components/search-experience";
import { SiteHeader } from "@/components/site-header";

export default async function SearchPage() {
  const t = await getTranslations("search");
  return <><SiteHeader /><Suspense fallback={<main className="mx-auto max-w-6xl px-5">{t("understanding")}</main>}><SearchExperience /></Suspense></>;
}
