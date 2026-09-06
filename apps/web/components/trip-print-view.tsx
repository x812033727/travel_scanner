"use client";

import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { api } from "@/lib/api";
import { activeLocale } from "@/lib/locale-format";
import {
  estimateLegMinutes,
  formatTime,
  groupTripItems,
  isActiveRouteItem,
  originalItemName,
  type RouteSegment,
  type TravelMode,
  type Trip,
  type TripItem,
} from "@/lib/trip-types";

/** The leg between two stops, whether or not anyone has routed it yet. */
function legFor(
  segments: RouteSegment[],
  from: TripItem,
  to: TripItem,
  mode: TravelMode,
): { minutes?: number; segment?: RouteSegment; estimated: boolean } {
  const segment = segments.find(
    (item) => item.from_item_id === from.id && item.to_item_id === to.id,
  );
  if (segment) return { minutes: segment.duration_minutes, segment, estimated: false };
  return { minutes: estimateLegMinutes(from, to, mode), estimated: true };
}

export function TripPrintView({ tripId }: { tripId: string }) {
  const t = useTranslations("trips");
  const [trip, setTrip] = useState<Trip>();
  const [error, setError] = useState<string>();
  useEffect(() => {
    api<Trip>(`/trips/${tripId}`).then(setTrip).catch((reason: Error) => setError(reason.message));
  }, [tripId]);

  if (error) return <main className="mx-auto max-w-3xl px-5 py-16"><p role="alert">{error}</p></main>;
  if (!trip) return <main className="mx-auto max-w-3xl px-5 py-16">{t("shareLoading")}</main>;

  const locale = activeLocale();
  const dayFormatter = new Intl.DateTimeFormat(locale, { month: "long", day: "numeric", weekday: "long" });
  const days = [...groupTripItems(trip.items)];
  const segments = trip.route_segments || [];
  const travelMode: TravelMode = "transit";

  return <main className="trip-print mx-auto max-w-3xl px-5 py-8 print:max-w-none print:px-0 print:py-0">
    <p className="trip-print-hint mb-6 rounded-2xl bg-[var(--paper)] p-4 text-sm text-[var(--muted)] print:hidden">
      {t("print.screenHint")}
    </p>

    <section className="trip-print-page">
      <p className="text-sm font-semibold text-[var(--teal)]">{t("print.eyebrow")}</p>
      <h1 className="mt-2 text-3xl font-bold">{trip.name}</h1>
      <dl className="mt-6 space-y-2 text-sm">
        {trip.destination_name && <div className="flex gap-3"><dt className="w-24 shrink-0 text-[var(--muted)]">{t("print.destination")}</dt><dd className="font-semibold">{trip.destination_name}</dd></div>}
        {trip.start_date && trip.end_date && <div className="flex gap-3"><dt className="w-24 shrink-0 text-[var(--muted)]">{t("print.dates")}</dt><dd className="font-semibold">{trip.start_date} – {trip.end_date}</dd></div>}
        <div className="flex gap-3"><dt className="w-24 shrink-0 text-[var(--muted)]">{t("print.days")}</dt><dd className="font-semibold">{t("print.dayCount", { count: days.length })}</dd></div>
      </dl>
      {trip.notes && <p className="mt-6 whitespace-pre-line text-sm leading-6">{trip.notes}</p>}
      <p className="mt-8 text-xs text-[var(--muted)]">{t("print.footer")}</p>
    </section>

    {days.map(([day, rows]) => {
      const stops = rows.filter(isActiveRouteItem);
      return <section key={day} className="trip-print-page">
        <header className="border-b border-[var(--line)] pb-2">
          <h2 className="text-xl font-bold">{dayFormatter.format(new Date(`${day}T00:00:00`))}</h2>
          <p className="mt-1 text-xs text-[var(--muted)]">{trip.name}{trip.day_notes?.[day] ? ` · ${trip.day_notes[day]}` : ""}</p>
        </header>
        {stops.length === 0
          ? <p className="mt-4 text-sm text-[var(--muted)]">{t("print.emptyDay")}</p>
          : <ol className="mt-4 space-y-3">
              {stops.map((item, index) => {
                const next = stops[index + 1];
                const leg = next ? legFor(segments, item, next, travelMode) : undefined;
                const ride = leg?.segment?.steps?.filter((step) => step.travel_mode === "TRANSIT") || [];
                const platform = leg?.segment?.steps?.find((step) => step.platform)?.platform;
                const exitName = leg?.segment?.steps?.find((step) => step.exit_name)?.exit_name;
                const car = leg?.segment?.steps?.find((step) => step.recommended_car)?.recommended_car;
                return <li key={item.id} className="trip-print-stop">
                  <div className="flex items-baseline gap-3">
                    <span className="w-14 shrink-0 text-sm font-semibold tabular-nums">{formatTime(item.start_time, locale, trip.timezone)}</span>
                    <div className="min-w-0 flex-1">
                      <h3 className="font-bold leading-snug">{item.title}</h3>
                      {originalItemName(item) && <p className="text-xs text-[var(--muted)]" lang={item.names?.title?.original_locale}>{originalItemName(item)}</p>}
                      {item.location_name && <p className="text-xs text-[var(--muted)]">{item.location_name}</p>}
                      {item.notes && <p className="mt-1 whitespace-pre-line text-xs leading-5">{item.notes}</p>}
                    </div>
                  </div>
                  {leg && leg.minutes !== undefined && <p className="mt-2 pl-[4.25rem] text-xs leading-5 text-[var(--muted)]">
                    {[
                      t(`print.mode.${leg.segment?.travel_mode || travelMode}`),
                      t("print.minutes", { minutes: leg.minutes }),
                      leg.estimated ? t("print.estimated") : undefined,
                      ride.length > 1 ? t("print.transfers", { count: ride.length - 1 }) : undefined,
                      ride.map((step) => step.line_short_name || step.line_name).filter(Boolean).join(" · ") || undefined,
                      leg.segment?.fare != null ? t("print.fare", { amount: `${leg.segment.currency || ""} ${leg.segment.fare}`.trim() }) : undefined,
                      platform ? t("print.platform", { value: platform }) : undefined,
                      exitName ? t("print.exit", { value: exitName }) : undefined,
                      car ? t("print.car", { value: car }) : undefined,
                    ].filter(Boolean).join(" · ")}
                  </p>}
                </li>;
              })}
            </ol>}
      </section>;
    })}
  </main>;
}
