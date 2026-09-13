"use client";

import { useEffect, useRef } from "react";
import { adsbygoogleQueue } from "./adsense-loader";
import { isAdsensePublisherId, isAdsenseSlotId } from "@/lib/adsense";

/** Reserved before the ad arrives, so filling it shifts nothing below it. */
const RESERVED_HEIGHT = 280;

/**
 * One in-article unit, labelled and with its box reserved.
 *
 * The server decides whether this renders at all; when advertising is off the article emits
 * no slot and no reserved space, so a reader sees exactly the page they see today. The label
 * may only ever read "廣告" / "Advertisements": the programme policies forbid dressing an ad
 * up as a recommendation.
 */
export function ArticleAdSlot({ publisherId, slotId, label }: {
  publisherId: string;
  slotId: string;
  label: string;
}) {
  const ref = useRef<HTMLModElement>(null);
  useEffect(() => {
    const element = ref.current;
    if (!element) return;
    // React StrictMode runs this effect twice in development, and a second push for the same
    // <ins> is the "already have ads in this tag" error. The tag stamps this attribute on the
    // element it has claimed, which is the only reliable way to tell.
    if (element.getAttribute("data-adsbygoogle-status")) return;
    try {
      adsbygoogleQueue().push({});
    } catch {
      // A blocked or failed tag must never take the article down with it.
    }
  }, []);
  if (!isAdsensePublisherId(publisherId) || !isAdsenseSlotId(slotId)) return null;
  return (
    <aside aria-label={label} className="my-2">
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
