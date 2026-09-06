"use client";

import { Loader2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { useRouter } from "@/i18n/navigation";
import { api } from "@/lib/api";

type SavedTrip = { id: string; name: string; start_date?: string; end_date?: string };

/**
 * Where Android's share sheet lands.
 *
 * The share target hands over text, a title and sometimes a URL; the place still has to
 * belong to a trip, so this asks which one and posts it to that trip's waiting list. iOS
 * has no share target at all, so the same page takes a paste and says as much instead of
 * leaving iPhone users hunting for a sheet that will never appear.
 */
export function ShareTargetView({ shared }: { shared: string }) {
  const t = useTranslations("trips.shareTarget");
  const router = useRouter();
  const [text, setText] = useState(shared);
  const [trips, setTrips] = useState<SavedTrip[]>([]);
  const [tripId, setTripId] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();

  useEffect(() => {
    api<SavedTrip[]>("/trips")
      .then((value) => {
        const rows = Array.isArray(value) ? value : [];
        setTrips(rows);
        if (rows[0]) setTripId(rows[0].id);
      })
      .catch(() => setError(t("signedOut")));
  }, [t]);

  async function send() {
    if (!tripId || !text.trim()) return;
    setBusy(true);
    setError(undefined);
    try {
      await api(`/trips/${tripId}/places/ingest`, { method: "POST", body: JSON.stringify({ text }) });
      router.push(`/trips/${tripId}`);
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : t("failed"));
      setBusy(false);
    }
  }

  return <main className="mx-auto max-w-xl space-y-4 px-5 py-8">
    <header>
      <h1 className="text-2xl font-bold">{t("title")}</h1>
      <p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("hint")}</p>
    </header>

    <label className="block text-sm font-semibold">
      {t("textLabel")}
      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        rows={4}
        maxLength={8000}
        className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2 font-normal"
      />
    </label>

    <label className="block text-sm font-semibold">
      {t("tripLabel")}
      <select
        value={tripId}
        onChange={(event) => setTripId(event.target.value)}
        className="mt-2 w-full rounded-xl border border-[var(--line)] bg-white px-3 py-3 font-normal"
      >
        {trips.map((trip) => <option key={trip.id} value={trip.id}>{trip.name}</option>)}
      </select>
    </label>

    <button
      type="button"
      onClick={() => void send()}
      disabled={busy || !tripId || !text.trim()}
      className="flex min-h-12 w-full items-center justify-center gap-2 rounded-2xl bg-[var(--teal)] font-bold text-white disabled:opacity-50"
    >
      {busy && <Loader2 size={16} className="animate-spin" />}{t("add")}
    </button>
    {error && <p role="alert" className="text-sm font-semibold text-red-700">{error}</p>}
    <p className="text-xs leading-5 text-[var(--muted)]">{t("iosNote")}</p>
  </main>;
}
