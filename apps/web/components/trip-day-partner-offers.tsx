"use client";

import { HandCoins, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useState } from "react";
import type { AffiliateModule } from "@/components/affiliate-partner-options";
import { DestinationAffiliateOptions } from "@/components/destination-affiliate-options";
import type { DayPartnerKind } from "@/lib/trip-partner-offers";

/**
 * The partner block at the end of a planner day.
 *
 * Closed by default and, unlike a plain `<details>`, its body does not exist until the
 * member opens it: the calm-planner rule is that the first paint of a trip makes no
 * partner request, and mounting the panel is what makes the request. Closing unmounts
 * it again, which aborts anything in flight.
 */
export function TripDayPartnerOffers({
  destinationId, modules, kind, destinationLabel,
}: {
  destinationId: string;
  modules: AffiliateModule[];
  kind: DayPartnerKind;
  destinationLabel?: string;
}) {
  const te = useTranslations("trips.editor");
  const [open, setOpen] = useState(false);
  if (!modules.length) return null;
  return (
    <details className="premium-planning-notes calm-day-review calm-day-partner" onToggle={(event) => setOpen(event.currentTarget.open)}>
      <summary><HandCoins size={16} /><span>{te(`partnerDay.${kind}`)}</span></summary>
      {open && (
        <div className="pt-3">
          <DestinationAffiliateOptions destinationId={destinationId} modules={modules} contextual destinationLabel={destinationLabel} placement="trip" />
        </div>
      )}
    </details>
  );
}

/**
 * Shown once, right after an AI plan is applied: the member just asked for stops, so
 * offering tickets and transport for them is an answer, not an interruption. Mounts the
 * panel immediately (the request is member-initiated) and goes away on dismiss.
 */
export function TripPartnerNextSteps({
  destinationId, modules, destinationLabel, onDismiss,
}: {
  destinationId: string;
  modules: AffiliateModule[];
  destinationLabel?: string;
  onDismiss: () => void;
}) {
  const te = useTranslations("trips.editor");
  const tCommon = useTranslations("common");
  if (!modules.length) return null;
  return (
    <section aria-label={te("partnerDay.afterAi")} className="calm-day-partner-next rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
      <div className="flex items-start justify-between gap-3">
        <div>
          <h3 className="font-bold">{te("partnerDay.afterAi")}</h3>
          <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{te("partnerDay.afterAiHint")}</p>
        </div>
        <button type="button" onClick={onDismiss} aria-label={tCommon("close")} className="grid h-9 w-9 shrink-0 place-items-center rounded-full hover:bg-[var(--paper)]">
          <X size={16} />
        </button>
      </div>
      <div className="mt-3">
        <DestinationAffiliateOptions destinationId={destinationId} modules={modules} contextual destinationLabel={destinationLabel} placement="trip" />
      </div>
    </section>
  );
}
