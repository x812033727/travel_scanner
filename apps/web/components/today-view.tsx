"use client";

import { CalendarDays, MapPin, Navigation } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";
import {
  formatTime,
  groupTripItems,
  isActiveRouteItem,
  originalItemName,
  type Trip,
  type TripItem,
} from "@/lib/trip-types";

function localDay(timezone?: string, now = new Date()): string {
  try {
    return new Intl.DateTimeFormat("en-CA", { timeZone: timezone || undefined }).format(now);
  } catch {
    return new Intl.DateTimeFormat("en-CA").format(now);
  }
}

/** The stop happening now, and the one after it. */
export function nowAndNext(stops: TripItem[], at = new Date()): { now?: TripItem; next?: TripItem } {
  const timed = stops.filter((item) => item.start_time);
  const moment = at.getTime();
  let current: TripItem | undefined;
  let upcoming: TripItem | undefined;
  for (const item of timed) {
    const start = new Date(item.start_time as string).getTime();
    const end = item.end_time ? new Date(item.end_time).getTime() : start;
    if (start <= moment && moment <= Math.max(end, start)) current = item;
    else if (start > moment && !upcoming) upcoming = item;
  }
  if (!current && !upcoming && timed.length) upcoming = timed[0];
  return { now: current, next: upcoming };
}

/**
 * The single column for the day itself: what is happening now, what is next, and the
 * rest of today. The editor is for planning; this is for standing on a platform.
 */
export function TodayView({ tripId }: { tripId: string }) {
  const t = useTranslations("trips.today");
  const locale = useLocale();
  const [trip, setTrip] = useState<Trip>();
  const [offline, setOffline] = useState(false);

  useEffect(() => {
    api<Trip>(`/trips/${tripId}`)
      .then(setTrip)
      .catch(() => setOffline(true));
  }, [tripId]);

  if (!trip) {
    return <main className="mx-auto max-w-xl px-5 py-16 text-[var(--muted)]">
      {offline ? t("unavailable") : t("loading")}
    </main>;
  }

  const today = localDay(trip.timezone);
  const days = new Map(groupTripItems(trip.items));
  const stops = (days.get(today) || []).filter(isActiveRouteItem);
  const { now, next } = nowAndNext(stops);

  const card = (item: TripItem, kind: "now" | "next") => <article
    key={item.id}
    className={`rounded-[1.75rem] border p-5 ${kind === "now" ? "border-[var(--teal)] bg-[var(--teal-soft)]" : "border-[var(--line)] bg-white"}`}
  >
    <p className="text-xs font-bold uppercase tracking-wide text-[var(--teal-dark)]">{t(kind)}</p>
    <h2 className="mt-2 text-2xl font-bold leading-snug">{item.title}</h2>
    {originalItemName(item) && <p className="text-sm text-[var(--muted)]" lang={item.names?.title?.original_locale}>{originalItemName(item)}</p>}
    <p className="mt-2 flex items-center gap-2 text-sm text-[var(--muted)]">
      <CalendarDays size={15} />{formatTime(item.start_time, locale, trip.timezone)}
      {item.location_name && <><MapPin size={15} />{item.location_name}</>}
    </p>
    {item.latitude != null && item.longitude != null && <a
      href={safeExternalHref(`https://www.google.com/maps/dir/?api=1&destination=${item.latitude},${item.longitude}`)}
      target="_blank"
      rel="noreferrer"
      className="mt-4 inline-flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white"
    >
      <Navigation size={16} />{t("navigate")}
    </a>}
  </article>;

  return <main className="mx-auto max-w-xl space-y-4 px-5 pb-24 pt-6">
    <header>
      <p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p>
      <h1 className="mt-1 text-2xl font-bold">{trip.name}</h1>
      <p className="mt-1 text-sm text-[var(--muted)]">{t("dayOf", { date: today })}</p>
    </header>

    {stops.length === 0 && <p className="rounded-2xl bg-[var(--paper)] p-5 text-[var(--muted)]">{t("nothingToday")}</p>}
    {now && card(now, "now")}
    {next && card(next, "next")}

    {stops.length > 0 && <section aria-label={t("rest")} className="rounded-[1.75rem] border border-[var(--line)] bg-white p-5">
      <h2 className="text-sm font-bold">{t("rest")}</h2>
      <ol className="mt-3 space-y-2">
        {stops.map((item) => <li key={item.id} className="flex items-baseline gap-3 text-sm">
          <span className="w-14 shrink-0 tabular-nums text-[var(--muted)]">{formatTime(item.start_time, locale, trip.timezone)}</span>
          <span className={item.id === now?.id ? "font-bold" : ""}>{item.title}</span>
        </li>)}
      </ol>
    </section>}

    <Link href={`/trips/${tripId}`} className="flex min-h-11 items-center justify-center rounded-xl border border-[var(--line)] bg-white text-sm font-semibold">
      {t("openPlanner")}
    </Link>
  </main>;
}
