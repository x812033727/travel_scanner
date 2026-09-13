import { Suspense } from "react";
import { getTranslations } from "next-intl/server";
import { SiteHeader } from "@/components/site-header";
import { DiscoveryExplorer } from "@/components/discovery/explorer";
import { getDiscoveryStatus } from "@/lib/discovery-status.server";
import { discoveryFeedPath, getInitialDiscoveryFeed, type DiscoverySearchParams } from "@/lib/discovery.server";
import type { Locale } from "@/i18n/routing";

type Props = { params: Promise<{ locale: Locale }>; searchParams: Promise<DiscoverySearchParams> };

/**
 * Indexable only while discovery is on, which is the same rule the rest of the site applies to
 * a closed feature. With the switch off this page is the fallback link grid -- a handful of
 * links to pages that are in the sitemap in their own right, and nothing of its own to rank.
 * With it on, the body below carries the feed's first page in the response.
 */
export async function generateMetadata({ params, searchParams }: Props) {
  const [{ locale }, search, t, discovery] = await Promise.all([
    params, searchParams, getTranslations("metadata"), getDiscoveryStatus(),
  ]);
  const feed = await getInitialDiscoveryFeed(locale, discoveryFeedPath(search, discovery.enabled));
  // `feed` is null for a searched or signed-in view, for an unreachable API, and for a feed
  // with no rows in it. In every one of those the response body is the skeleton or an empty
  // page, so there is nothing here to index.
  const indexable = discovery.enabled && Boolean(feed);
  return {
    title: t("exploreTitle"),
    description: t("exploreDescription"),
    ...(indexable ? {} : { robots: { index: false, follow: true } }),
  };
}

export default async function ExplorePage({ params, searchParams }: Props) {
  const [{ locale }, search, discovery] = await Promise.all([params, searchParams, getDiscoveryStatus()]);
  // The same path as the metadata above, so React's per-request cache answers both from one
  // call to the API rather than fetching the feed twice per request.
  const feed = await getInitialDiscoveryFeed(locale, discoveryFeedPath(search, discovery.enabled));
  return (
    <>
      <SiteHeader />
      <Suspense>
        <DiscoveryExplorer initialEnabled={discovery.enabled} initialFeed={feed} />
      </Suspense>
    </>
  );
}
