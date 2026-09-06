"use client";

import { Copy, ShieldCheck, Sparkles } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import Image from "next/image";
import QRCode from "qrcode";
import { useEffect, useState } from "react";
import { ItineraryTimeline } from "@/components/itinerary-timeline";
import { Link, useRouter } from "@/i18n/navigation";
import { api, ApiError } from "@/lib/api";
import type { SharedTrip, Trip } from "@/lib/trip-types";

export function SharedTripView({ token }: { token: string }) {
  // The one page whose whole audience is people the owner sent a link to —
  // it used to greet them in Traditional Chinese regardless of /en, /ja, /ko.
  const t = useTranslations("trips");
  const locale = useLocale();
  const router = useRouter();
  const [trip, setTrip] = useState<SharedTrip>();
  const [error, setError] = useState<string>();
  const [forking, setForking] = useState(false);
  const [forkError, setForkError] = useState<string>();
  // Drawn in the browser from the address bar: a QR service would learn every
  // share link anyone ever opened.
  const [qrCode, setQrCode] = useState<string>();
  useEffect(() => {
    if (typeof window === "undefined") return;
    QRCode.toDataURL(window.location.href, { margin: 1, width: 220 })
      .then(setQrCode)
      .catch(() => setQrCode(undefined));
  }, []);

  async function saveAsMyTrip() {
    setForking(true);
    setForkError(undefined);
    try {
      const copy = await api<Trip>(`/shared-trips/${token}/fork`, { method: "POST" });
      router.push(`/trips/${copy.id}`);
    } catch (reason) {
      if (reason instanceof ApiError && reason.status === 401) {
        router.push(`/login?next=${encodeURIComponent(`/share/${token}`)}`);
        return;
      }
      setForkError(reason instanceof Error ? reason.message : t("shared.forkFailed"));
      setForking(false);
    }
  }
  useEffect(() => {
    api<SharedTrip>(`/shared-trips/${token}`).then(setTrip).catch((reason: Error) => setError(reason.message));
  }, [token]);
  if (error) return <main className="mx-auto max-w-4xl px-5 py-16"><p role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">{t("shareNotFound")}</p></main>;
  if (!trip) return <main className="mx-auto max-w-4xl px-5 py-16 text-[var(--muted)]">{t("shareLoading")}</main>;
  const updated = trip.updated_at
    ? t("shareUpdatedAt", {
        date: new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }).format(new Date(trip.updated_at)),
      })
    : t("shareUpdatedRecently");
  return <main className="mx-auto max-w-4xl px-5 pb-20 md:px-8"><section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:p-8"><p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><ShieldCheck size={17} />{t("shareReadOnly")}</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{trip.name}</h1><p className="mt-3 text-[var(--muted)]">{trip.destination_name || t("shareFallbackDestination")} · {updated}</p><p className="mt-4 rounded-xl bg-[var(--teal-soft)] p-3 text-sm text-[var(--teal-dark)]">{t("shareDisclaimer")}</p></section><ItineraryTimeline items={trip.items} routes={trip.route_segments} timezone={trip.timezone} />
    {/* The share page used to end here with no way onward; a recipient could only leave. */}
    <section className="mt-8 grid gap-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 shadow-[var(--shadow-lg)] md:grid-cols-[1fr_auto] md:p-8">
      <div>
        <h2 className="text-xl font-bold">{t("shared.forkTitle")}</h2>
        <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("shared.forkHint")}</p>
        <button type="button" onClick={() => void saveAsMyTrip()} disabled={forking} className="mt-4 inline-flex min-h-12 items-center gap-2 rounded-2xl bg-[var(--teal)] px-6 font-bold text-white disabled:opacity-60"><Copy size={17} />{forking ? t("shared.forkBusy") : t("shared.forkButton")}</button>
        {forkError && <p role="alert" className="mt-3 text-sm font-semibold text-red-700">{forkError}</p>}
      </div>
      {qrCode && <figure className="justify-self-center text-center">
        <Image src={qrCode} alt={t("shared.qrAlt")} width={140} height={140} unoptimized className="rounded-xl border border-[var(--line)]" />
        <figcaption className="mt-2 text-xs text-[var(--muted)]"><strong className="block">{t("shared.qrTitle")}</strong>{t("shared.qrHint")}</figcaption>
      </figure>}
    </section>
    <section className="mt-8 rounded-[2rem] border border-[var(--line)] bg-white p-6 text-center shadow-[var(--shadow-lg)] md:p-8">
      <Sparkles className="mx-auto text-[var(--teal)]" size={26} />
      <p className="mt-3 text-[var(--muted)]">{t("shared.planYoursHelp")}</p>
      <Link href="/" className="mt-5 inline-flex min-h-12 items-center rounded-2xl bg-[var(--teal)] px-6 font-bold text-white">{t("shared.planYours")}</Link>
    </section>
  </main>;
}
