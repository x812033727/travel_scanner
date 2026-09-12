"use client";

import { ExternalLink, HandCoins } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
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

export function DestinationAffiliateOptions({
  destinationId,
  modules = MODULES,
  contextual = false,
  destinationLabel,
  placement = "destination",
}: {
  destinationId: string;
  modules?: AffiliateModule[];
  contextual?: boolean;
  destinationLabel?: string;
  /** Which public surface renders the buttons. The API decides per placement whether
   *  offers may show at all, and records it on every click. */
  placement?: HotelBookingPlacement;
}) {
  const t = useTranslations("travelServices");
  const locale = useLocale();
  const copy = klookAffiliateCopy(locale);
  const moduleKey = [...new Set(modules)].filter((module) => MODULES.includes(module)).join(",");
  const requestKey = `${destinationId}:${moduleKey}:${locale}:${placement}`;
  const [snapshot, setSnapshot] = useState<{ key: string; responses: DestinationResponse[] }>();
  const responses = snapshot?.key === requestKey ? snapshot.responses : [];

  useEffect(() => {
    const controller = new AbortController();
    Promise.all(
      (moduleKey.split(",").filter(Boolean) as AffiliateModule[]).map((module) =>
        api<DestinationResponse>(
          `/affiliates/destination-offers?destination_id=${encodeURIComponent(destinationId)}&module=${module}&placement=${placement}`,
          { signal: controller.signal },
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
    return () => {
      controller.abort();
    };
  }, [destinationId, moduleKey, placement, requestKey]);

  if (!responses.length) return null;
  const disclosure = responses.find((response) => response.disclosure)?.disclosure;
  return (
    <section
      aria-label={`${contextual ? copy.discover : t("destinationOffersTitle")}${destinationLabel ? ` · ${destinationLabel}` : ""}`}
      className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-4 sm:p-5"
    >
      <div className="flex items-start gap-3">
        <span className="rounded-xl bg-[var(--coral-soft)] p-2 text-[var(--coral)]">
          <HandCoins size={19} />
        </span>
        <div>
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
            <div className="flex gap-2 overflow-x-auto pb-1">
              {response.options.map((option) => (
                <form
                  key={option.id}
                  action={option.clickout_url}
                  method="post"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="shrink-0"
                >
                  <button
                    type="submit"
                    aria-label={`${option.cta} · ${t("newTab")}`}
                    className="flex min-h-11 items-center gap-2 rounded-xl border border-[var(--teal)] bg-[var(--surface-raised)] px-4 py-3 text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)]"
                  >
                    {option.cta}
                    <ExternalLink size={15} />
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
