"use client";

import Script from "next/script";
import { createContext, useContext } from "react";
import { ADSENSE_SCRIPT_ORIGIN, isAdsensePublisherId } from "@/lib/adsense";
import { AnchorAdOffset } from "./anchor-ad-offset";

declare global {
  interface Window {
    adsbygoogle?: AdsbygoogleQueue;
  }
}

export type AdsbygoogleQueue = Record<string, unknown>[] & { requestNonPersonalizedAds?: number };

/**
 * `cmpEnabled` is the only thing that may allow personalised ads.
 *
 * With a Google-certified consent message published, the tag loads it for readers in the EEA,
 * the UK and Switzerland and serves whatever they chose — forcing the flag here would
 * override that answer and make the consent message pointless. Without one, the flag is
 * mandatory: personalised ads in those regions require a certified CMP.
 *
 * The tag reads this off the same array the slots push into, so setting it in the same tick
 * as a push is enough however the two scripts interleave.
 */
export function adsbygoogleQueue(cmpEnabled: boolean): AdsbygoogleQueue {
  const queue: AdsbygoogleQueue = (window.adsbygoogle ??= []);
  if (!cmpEnabled) queue.requestNonPersonalizedAds = 1;
  return queue;
}

const AdsenseDocumentContext = createContext(false);

/**
 * Marks the pages under it as living in a document that loaded the tag.
 *
 * The page decides its units per request, but the root layout — and so the loader — is only
 * rendered for the request that opened the document. An article reached by client-side
 * navigation from a document that loaded no tag (a tutorial hub, or a URL with a query
 * string) would otherwise reserve boxes nothing will ever fill.
 */
export function AdsenseDocument({ children }: { children: React.ReactNode }) {
  return <AdsenseDocumentContext.Provider value>{children}</AdsenseDocumentContext.Provider>;
}

/** False outside an `AdsenseDocument`, so a unit fails closed wherever the tag is absent. */
export function useAdsenseDocument(): boolean {
  return useContext(AdsenseDocumentContext);
}

/**
 * Loads the AdSense tag once per document.
 *
 * Mount only in the isolated `(ads-public)` root, never in the private SPA root: removing a
 * React `<Script>` cannot retract observers and timers the vendor has already started, so a
 * document boundary — not unmounting — is what keeps this runtime out of account and trip
 * pages. See `docs/stay22-module-switch.md` for the precedent.
 */
export function AdsenseLoader({ publisherId, cmpEnabled }: {
  publisherId: string | null;
  cmpEnabled: boolean;
}) {
  if (!isAdsensePublisherId(publisherId)) return null;
  return (
    <>
      <Script
        id="adsbygoogle-init"
        src={`${ADSENSE_SCRIPT_ORIGIN}/pagead/js/adsbygoogle.js?client=${publisherId}`}
        strategy="afterInteractive"
        crossOrigin="anonymous"
        onReady={() => {
          adsbygoogleQueue(cmpEnabled);
        }}
      />
      {/* The same tag serves the account's Auto ads overlay formats (anchor, vignette) on
          whatever page loads it; this keeps the anchor off the site's own fixed chrome. */}
      <AnchorAdOffset />
    </>
  );
}
