import { Suspense } from "react";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { DiscoveryExplorer } from "@/components/discovery/explorer";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("exploreTitle"), description: t("exploreDescription"), robots: { index: false, follow: true } };
}
export default function ExplorePage() { return <><SiteHeader /><Suspense><DiscoveryExplorer /></Suspense></>; }
