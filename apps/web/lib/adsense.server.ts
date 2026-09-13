/**
 * The per-request decision: may THIS response carry an ad, and with which identifiers.
 *
 * Public only. Never forwards cookies, authorization, query strings or account state — the
 * API endpoint behind it is anonymous for the same reason article readers are.
 */
import { cache } from "react";
import { headers } from "next/headers";
import { adsenseRequestGate, disabledAdsense, type AdsenseConfig } from "./adsense";
import { fetchAdsenseConfig } from "./adsense-config";
import { getGuideArticle } from "./guides.server";
import { isLocale } from "@/i18n/routing";

export async function loadAdsenseSlot(): Promise<AdsenseConfig> {
  const incoming = await headers();
  // The same gate proxy.ts applies, so a request it refused cannot be accepted here and a
  // request it accepted cannot be silently refused. proxy.ts overwrites x-travel-pathname
  // from NextRequest's actual URL, so it is the one trustworthy statement of the page.
  const route = adsenseRequestGate({
    host: incoming.get("host"),
    dnt: incoming.get("dnt"),
    gpc: incoming.get("sec-gpc"),
    pathname: incoming.get("x-travel-pathname") || "",
  });
  if (!route || !isLocale(route.locale)) return disabledAdsense;
  const config = await fetchAdsenseConfig();
  if (!config.enabled) return disabledAdsense;
  // The URL having an article's shape is not the same as there being an article. A missing,
  // unpublished or untranslated slug renders the "article unavailable" screen, and Google's
  // policies forbid advertising on a no-content screen — so this asks before the document
  // loads the tag. `getGuideArticle` is React-cached, so the page's own call is the same
  // request, not a second one.
  const state = await getGuideArticle(route.kind, route.slug, route.locale);
  if (state.status !== "published" || !state.document) return disabledAdsense;
  return config;
}

// The layout and its page must reach the same answer within one request: one of them
// deciding differently would reserve space nothing fills, or fill space nothing reserved.
export const getAdsenseSlot = cache(loadAdsenseSlot);
