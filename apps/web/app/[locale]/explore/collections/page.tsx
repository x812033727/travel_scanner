import { Suspense } from "react";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { DiscoveryCollections } from "@/components/discovery/collections";
/**
 * `noindex` here is not the "empty shell waiting for server rendering" kind that `/explore`
 * has just left behind, and it is not lifted by turning discovery on.
 *
 * This page is one reader's own saved items behind a sign-in prompt: there is no public
 * version of it to render on the server, and nothing an anonymous crawler could be shown that
 * would be worth showing. It belongs with `/account` and `/trips`, which are `noindex`
 * whatever the switches say. `app/sitemap.ts` leaves it out for the same reason.
 */
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("discoveryCollectionsTitle"), description: t("discoveryCollectionsDescription"), robots: { index: false, follow: true } };
}
export default function CollectionsPage() { return <><SiteHeader /><Suspense><DiscoveryCollections /></Suspense></>; }
