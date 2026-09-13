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
 * Non-personalised ads only, and deliberately not a setting: serving personalised ads in the
 * EEA, the UK or Switzerland requires a certified CMP and a different privacy policy, so
 * changing this has to be a code change reviewed alongside that text.
 *
 * The tag reads this flag off the same array the slots push into, so setting it in the same
 * tick as a push is enough however the two scripts interleave.
 */
export function adsbygoogleQueue(): AdsbygoogleQueue {
  const queue: AdsbygoogleQueue = (window.adsbygoogle ??= []);
  queue.requestNonPersonalizedAds = 1;
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
export function AdsenseLoader({ publisherId }: { publisherId: string | null }) {
  if (!isAdsensePublisherId(publisherId)) return null;
  return (
    <Script
      id="adsbygoogle-init"
      src={`${ADSENSE_SCRIPT_ORIGIN}/pagead/js/adsbygoogle.js?client=${publisherId}`}
      strategy="afterInteractive"
      crossOrigin="anonymous"
      onReady={() => {
        adsbygoogleQueue();
      }}
    />
  );
}
