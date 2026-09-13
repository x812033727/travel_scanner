"use client";

import Script from "next/script";
import { ADSENSE_SCRIPT_ORIGIN, isAdsensePublisherId } from "@/lib/adsense";

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
    <Script
      id="adsbygoogle-init"
      src={`${ADSENSE_SCRIPT_ORIGIN}/pagead/js/adsbygoogle.js?client=${publisherId}`}
      strategy="afterInteractive"
      crossOrigin="anonymous"
      onReady={() => {
        adsbygoogleQueue(cmpEnabled);
      }}
    />
  );
}
