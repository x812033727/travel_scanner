import { Suspense } from "react";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { DiscoveryCollections } from "@/components/discovery/collections";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("discoveryCollectionsTitle"), description: t("discoveryCollectionsDescription"), robots: { index: false, follow: true } };
}
export default function CollectionsPage() { return <><SiteHeader /><Suspense><DiscoveryCollections /></Suspense></>; }
