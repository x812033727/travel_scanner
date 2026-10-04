"use client";

import { ExternalLink, HandCoins } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { api } from "@/lib/api";
import type { AffiliateModule } from "@/components/affiliate-partner-options";
import type { HotelBookingPlacement } from "@/lib/hotel-booking-placement";
import { klookAffiliateCopy } from "@/lib/klook-affiliate-copy";

type DestinationOption = {
  id: string;
  brand: string;
  display_name: string;
  destination_id: string;
  module: AffiliateModule;
  cta: string;
  clickout_url: string;
};

type DestinationResponse = {
  destination_id: string;
  module: AffiliateModule;
  disclosure: string;
  options: DestinationOption[];
};

const MODULES: AffiliateModule[] = [
  "flight",
  "hotel",
  "activities",
  "transport",
  "connectivity",
];

const LABEL_KEYS: Record<AffiliateModule, string> = {
  flight: "affiliateFlight",
  hotel: "affiliateHotel",
  activities: "affiliateActivities",
  transport: "affiliateTransport",
  connectivity: "affiliateConnectivity",
};

/** The clickout URL the API built, plus the article that placed the button when there is
 *  one. The API keeps the slug only when it is shaped like one of ours and drops it
 *  otherwise; nothing else about the click, its `sub_id` included, depends on it. */
function clickoutUrl(url: string, locale: string, article?: string): string {
  const suffix = `locale=${encodeURIComponent(locale)}${article ? `&article=${encodeURIComponent(article)}` : ""}`;
  return `${url}${url.includes("?") ? "&" : "?"}${suffix}`;
}

/** Fetch before a reader reaches the panel, without loading every below-fold placement. */
export const AFFILIATE_PREFETCH_MARGIN = "0px 0px 1200px 0px";

export function DestinationAffiliateOptions({
  destinationId,
  modules = MODULES,
  contextual = false,
  destinationLabel,
  placement = "destination",
  article,
}: {
  destinationId: string;
  modules?: AffiliateModule[];
  contextual?: boolean;
  destinationLabel?: string;
  /** Which public surface renders the buttons. The API decides per placement whether
   *  offers may show at all, and records it on every click. */
  placement?: HotelBookingPlacement;
  /** The slug of the article whose page renders the buttons, recorded on every click so
   *  the report can say which article placed them. Not part of the request identity. */
  article?: string;
}) {
  const t = useTranslations("travelServices");
  const locale = useLocale();
  const copy = klookAffiliateCopy(locale);
  const moduleKey = [...new Set(modules)].filter((module) => MODULES.includes(module)).join(",");
  const requestKey = `${destinationId}:${moduleKey}:${locale}:${placement}`;
  const sentinel = useRef<HTMLSpanElement>(null);
  const [snapshot, setSnapshot] = useState<{ key: string; responses: DestinationResponse[] }>();
  const responses = snapshot?.key === requestKey ? snapshot.responses : [];

  useEffect(() => {
    if (!destinationId || !moduleKey) return;
    const controller = new AbortController();
    let requested = false;
    let observer: IntersectionObserver | undefined;
    let pendingFrame: number | undefined;
    const stopWaiting = () => {
      observer?.disconnect();
      window.removeEventListener("scroll", checkPassed);
      if (pendingFrame !== undefined) {
        window.cancelAnimationFrame(pendingFrame);
        pendingFrame = undefined;
      }
    };
    function checkPassed() {
      if (requested || controller.signal.aborted || pendingFrame !== undefined) return;
      pendingFrame = window.requestAnimationFrame(() => {
        pendingFrame = undefined;
        if (controller.signal.aborted) return;
        if (sentinel.current && sentinel.current.getBoundingClientRect().bottom < 0) load();
      });
    }
    const load = () => {
      if (requested || controller.signal.aborted) return;
      requested = true;
      stopWaiting();
      void Promise.all(
        (moduleKey.split(",") as AffiliateModule[]).map((module) =>
          api<DestinationResponse>(
            `/affiliates/destination-offers?destination_id=${encodeURIComponent(destinationId)}&module=${module}&placement=${placement}`,
            { signal: controller.signal, headers: { "X-Travel-Locale": locale } },
          ).catch(() => ({
            destination_id: destinationId,
            module,
            disclosure: "",
            options: [],
          })),
        ),
      ).then((values) => {
        if (!controller.signal.aborted) setSnapshot({ key: requestKey, responses: values.filter((value) => value?.options?.length) });
      });
    };
    if (typeof IntersectionObserver === "undefined" || !sentinel.current) {
      load();
    } else {
      observer = new IntersectionObserver((entries) => {
        // Reload and history navigation can restore scroll below the marker. Load a
        // passed placement too, rather than requiring the reader to scroll back up.
        if (entries.some((entry) => entry.isIntersecting || entry.boundingClientRect.bottom < 0)) load();
      }, { rootMargin: AFFILIATE_PREFETCH_MARGIN });
      // A jump from below the prefetch window to above it can keep intersection false,
      // so the observer may never report that the marker has been passed.
      window.addEventListener("scroll", checkPassed, { passive: true });
      observer.observe(sentinel.current);
    }
    return () => {
      controller.abort();
      stopWaiting();
    };
  }, [destinationId, locale, moduleKey, placement, requestKey]);

  if (!destinationId || !moduleKey || (snapshot?.key === requestKey && !responses.length)) return null;
  if (!responses.length) return (
    // An invisible measurable target, with no card or height reserved for disabled offers.
    // Inline margin overrides article space-y rules while this zero-height wrapper waits.
    <span aria-hidden="true" style={{ display: "block", position: "relative", height: 0, margin: 0 }}>
      <span ref={sentinel} style={{ position: "absolute", top: 0, left: 0, width: "100%", height: 1, opacity: 0, pointerEvents: "none" }} />
    </span>
  );
  const disclosure = responses.find((response) => response.disclosure)?.disclosure;
  return (
    <section
      aria-label={`${contextual ? copy.discover : t("destinationOffersTitle")}${destinationLabel ? ` · ${destinationLabel}` : ""}`}
      className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-4 sm:p-5"
    >
      <div className="flex items-start gap-3">
        <span className="shrink-0 rounded-xl bg-[var(--coral-soft)] p-2 text-[var(--coral)]">
          <HandCoins size={19} />
        </span>
        <div className="min-w-0 break-words">
          <h2 className="font-bold">{contextual ? copy.discover : t("destinationOffersTitle")}{destinationLabel && <span className="ml-2 text-[var(--teal)]">{destinationLabel}</span>}</h2>
          <p className="mt-1 text-xs leading-5 text-[var(--muted)]">
            {contextual ? copy.discoveryHint : t("destinationOffersHint")}
          </p>
        </div>
      </div>
      <div className="mt-4 space-y-4">
        {responses.map((response) => (
          <div key={response.module}>
            <p className="mb-2 text-xs font-bold text-[var(--teal-dark)]">
              {t(LABEL_KEYS[response.module])}
            </p>
            <div className="grid min-w-0 gap-2 sm:grid-cols-2">
              {/* `noopener` only: a `noreferrer` form POST goes out with `Origin: null`, and the
                  BFF's same-origin guard answers that with a 403 instead of the partner page.
                  The 303 onward already carries `Referrer-Policy: no-referrer`. */}
              {response.options.map((option) => (
                <form
                  key={option.id}
                  action={clickoutUrl(option.clickout_url, locale, article)}
                  method="post"
                  target="_blank"
                  rel="noopener"
                  className="min-w-0"
                >
                  <button
                    type="submit"
                    aria-label={`${option.cta} · ${t("newTab")}`}
                    className="flex min-h-11 w-full min-w-0 items-center justify-between gap-2 rounded-xl border border-[var(--teal)] bg-[var(--surface-raised)] px-4 py-3 text-left text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)]"
                  >
                    <span className="min-w-0 break-words [overflow-wrap:anywhere]">{option.cta}</span>
                    <ExternalLink size={15} className="shrink-0" aria-hidden="true" />
                  </button>
                </form>
              ))}
            </div>
          </div>
        ))}
      </div>
      {disclosure && (
        <p className="mt-4 border-t border-[var(--line)] pt-3 text-xs text-[var(--muted)]">
          {disclosure}
        </p>
      )}
    </section>
  );
}
