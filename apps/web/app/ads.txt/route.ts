import { isAdsensePublisherId } from "@/lib/adsense";
import { fetchAdsenseConfig } from "@/lib/adsense-config";
import { ADS_TXT_FALLBACK_PUBLISHER_ID, adsTxtLine } from "./ads-txt";

/**
 * `/ads.txt` -- the one line that authorises the configured AdSense account to sell this
 * site's inventory.
 *
 * It used to be a checked-in file under `public/`, naming one publisher id at build time,
 * while the id itself is back-office configuration that changes without a redeploy. Nothing
 * kept the two in step: moving to another AdSense account gave a green admin card serving
 * inventory Google treats as unauthorised, and the only signal was a warning inside AdSense
 * that nobody here watches. Built from the same configuration the article pages read, the
 * two cannot disagree.
 *
 * Google crawls this file to verify the site, so it has to answer whether or not the API
 * does. `fetchAdsenseConfig` answers from a process-local cache, gives the API one second,
 * rides out a short outage on its last answer and reports "off" rather than throwing; and
 * "off" -- the API down for longer than that, advertising switched off, or no id configured
 * -- still names the account the site was verified with. Silence is the one answer this
 * must never give.
 *
 * Next has no file convention for this one, so it is a Route Handler in a dotted folder,
 * the pattern `app/llms.txt/route.ts` uses. `proxy.ts`'s matcher excludes any path with a
 * dot in it, so next-intl never sees the request and nothing redirects it to a locale. A
 * `public/ads.txt` would win over this route, which is why there is no longer one.
 */

// Read when a crawler asks, never while building: the Dockerfile's build stage has no API,
// so a prerendered file would carry the fallback until the next deploy -- exactly the drift
// this route exists to remove.
export const dynamic = "force-dynamic";

async function configuredPublisherId(): Promise<string | null> {
  try {
    const { publisher_id: id } = await fetchAdsenseConfig();
    return isAdsensePublisherId(id) ? id : null;
  } catch {
    // `fetchAdsenseConfig` already catches everything it can. This file answers regardless.
    return null;
  }
}

export async function GET(): Promise<Response> {
  const publisherId = (await configuredPublisherId()) ?? ADS_TXT_FALLBACK_PUBLISHER_ID;
  return new Response(`${adsTxtLine(publisherId)}\n`, {
    headers: {
      "Content-Type": "text/plain; charset=utf-8",
      // Google re-reads ads.txt about once a day, so an hour is nothing to a change of id and
      // everything to a crawl that lands during a blip: whatever sits between the crawler and
      // this server may serve its copy rather than wait on the API. The article pages read
      // the same configuration through a one-minute cache, so the two stay within an hour.
      "Cache-Control": "public, max-age=3600",
    },
  });
}
