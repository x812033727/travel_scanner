/**
 * The per-request decision: may THIS response carry an ad, and with which identifiers.
 *
 * Public only. Never forwards cookies, authorization, query strings or account state — the
 * API endpoint behind it is anonymous for the same reason article readers are.
 */
import { cache } from "react";
import { headers } from "next/headers";
import { disabledAdsense, isAdsenseArticlePath, isAdsenseOrigin, type AdsenseConfig } from "./adsense";
import { fetchAdsenseConfig } from "./adsense-config";

export async function loadAdsenseSlot(): Promise<AdsenseConfig> {
  const incoming = await headers();
  if (!isAdsenseOrigin(`https://${incoming.get("host") || ""}`)) return disabledAdsense;
  // The site's standing rule for third-party scripts: a browser asking not to be tracked
  // gets none of them, and no reserved space either.
  if (incoming.get("dnt") === "1" || incoming.get("sec-gpc") === "1") return disabledAdsense;
  // proxy.ts overwrites this header from NextRequest's actual URL, so it is the one
  // trustworthy statement of which page is being rendered.
  const path = incoming.get("x-travel-pathname") || "";
  if (!isAdsenseArticlePath(path)) return disabledAdsense;
  return fetchAdsenseConfig();
}

// The layout and its page must reach the same answer within one request: one of them
// deciding differently would reserve space nothing fills, or fill space nothing reserved.
export const getAdsenseSlot = cache(loadAdsenseSlot);
