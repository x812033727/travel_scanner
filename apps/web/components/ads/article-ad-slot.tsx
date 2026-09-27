"use client";

import { useEffect, useRef } from "react";
import { adsbygoogleQueue, useAdsenseDocument } from "./adsense-loader";
import { isAdsensePublisherId, isAdsenseSlotId } from "@/lib/adsense";

/** Reserved before the ad arrives, so filling it shifts nothing below it. */
const RESERVED_HEIGHT = 280;

/**
 * How far below the viewport a lazy unit starts asking for its ad: about one phone screen,
 * so the ad has arrived by the time the reader gets there.
 */
export const LAZY_ROOT_MARGIN = "0px 0px 800px 0px";

/**
 * One in-article unit, labelled and with its box reserved.
 *
 * The server decides whether this renders at all; when advertising is off the article emits
 * no slot and no reserved space, so a reader sees exactly the page they see today. It also
 * renders nothing outside an `AdsenseDocument`: without the tag in the document there is
 * nothing to fill the box. The label
 * may only ever read "廣告" / "Advertisements": the programme policies forbid dressing an ad
 * up as a recommendation.
 *
 * A `lazy` unit waits until it is near the viewport before requesting an ad. An impression
 * nobody scrolls to still counts against the page's viewability, and a lower viewability is
 * a lower bid on every unit, the ones that are seen included. A unit Google leaves unfilled
 * is collapsed by `globals.css` rather than left as an empty box.
 */
export function ArticleAdSlot({ publisherId, slotId, label, cmpEnabled, lazy = false }: {
  publisherId: string;
  slotId: string;
  label: string;
  /** Passed through to the queue: see `adsbygoogleQueue`. */
  cmpEnabled: boolean;
  lazy?: boolean;
}) {
  const ref = useRef<HTMLModElement>(null);
  const tagLoaded = useAdsenseDocument();
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    const request = () => {
      // React StrictMode runs this effect twice in development, and a second push for the same
      // <ins> is the "already have ads in this tag" error. The tag stamps this attribute on the
      // element it has claimed, which is the only reliable way to tell.
      if (element.getAttribute("data-adsbygoogle-status")) return;
      try {
        adsbygoogleQueue(cmpEnabled).push({});
      } catch {
        // A blocked or failed tag must never take the article down with it.
      }
    };
    if (!lazy || typeof IntersectionObserver === "undefined") {
      request();
      return;
    }
    const observer = new IntersectionObserver((entries) => {
      if (!entries.some((entry) => entry.isIntersecting)) return;
      observer.disconnect();
      request();
    }, { rootMargin: LAZY_ROOT_MARGIN });
    observer.observe(element);
    return () => observer.disconnect();
  }, [cmpEnabled, lazy]);
  if (!tagLoaded || !isAdsensePublisherId(publisherId) || !isAdsenseSlotId(slotId)) return null;
  return (
    <aside aria-label={label} className="article-ad-slot my-2">
      <p className="mb-1 text-xs uppercase tracking-wide text-[var(--muted)]">{label}</p>
      <div style={{ minHeight: RESERVED_HEIGHT }} className="overflow-hidden">
        <ins
          ref={ref}
          className="adsbygoogle"
          style={{ display: "block", minHeight: RESERVED_HEIGHT }}
          data-ad-client={publisherId}
          data-ad-slot={slotId}
          data-ad-format="fluid"
          data-ad-layout="in-article"
        />
      </div>
    </aside>
  );
}
