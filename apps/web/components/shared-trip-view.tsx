"use client";

import { ShieldCheck } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { ItineraryTimeline } from "@/components/itinerary-timeline";
import { api } from "@/lib/api";
import type { Trip } from "@/lib/trip-types";

export function SharedTripView({ token }: { token: string }) {
  // The one page whose whole audience is people the owner sent a link to —
  // it used to greet them in Traditional Chinese regardless of /en, /ja, /ko.
  const t = useTranslations("trips");
  const locale = useLocale();
  const [trip, setTrip] = useState<Trip>();
  const [error, setError] = useState<string>();
  useEffect(() => {
    api<Trip>(`/shared-trips/${token}`).then(setTrip).catch((reason: Error) => setError(reason.message));
  }, [token]);
  if (error) return <main className="mx-auto max-w-4xl px-5 py-16"><p role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">{t("shareNotFound")}</p></main>;
  if (!trip) return <main className="mx-auto max-w-4xl px-5 py-16 text-[var(--muted)]">{t("shareLoading")}</main>;
  const updated = trip.updated_at
    ? t("shareUpdatedAt", {
        date: new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }).format(new Date(trip.updated_at)),
      })
    : t("shareUpdatedRecently");
  return <main className="mx-auto max-w-4xl px-5 pb-20 md:px-8"><section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8"><p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><ShieldCheck size={17} />{t("shareReadOnly")}</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{trip.name}</h1><p className="mt-3 text-[var(--muted)]">{trip.destination_name || t("shareFallbackDestination")} · {updated}</p><p className="mt-4 rounded-xl bg-[var(--teal-soft)] p-3 text-sm text-[var(--teal-dark)]">{t("shareDisclaimer")}</p></section><ItineraryTimeline items={trip.items} routes={trip.route_segments} timezone={trip.timezone} /></main>;
}
