/**
 * What `/ads.txt` says, kept apart from the Route Handler beside it: a `route.ts` may export
 * nothing but its handlers and segment config, and the e2e suite wants the fallback without
 * dragging a route module in.
 */

/**
 * The account the site was verified with, named whenever the configuration carries no id.
 *
 * Google crawls `/ads.txt` to verify the site, so an API that is down for longer than
 * `fetchAdsenseConfig` will cover, advertising being switched off, and an empty id must all
 * still produce a line: an outage must not un-verify the site. If the owner ever moves
 * AdSense accounts, change this too, so that a long outage names the right one.
 */
export const ADS_TXT_FALLBACK_PUBLISHER_ID = "ca-pub-4140966684432854";

/**
 * Google's own line for an AdSense publisher: the seller's domain, the publisher id without
 * the `ca-` prefix the back office stores it with, the direct relationship, and Google's
 * certification authority id, which is the same for every AdSense publisher.
 */
export function adsTxtLine(publisherId: string): string {
  return `google.com, ${publisherId.replace(/^ca-/, "")}, DIRECT, f08c47fec0942fa0`;
}
