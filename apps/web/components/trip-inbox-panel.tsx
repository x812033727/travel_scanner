"use client";

import { Loader2, MapPin, Plus, Trash2 } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { api } from "@/lib/api";

export type PlaceCandidate = {
  id: string;
  status: string;
  source: string;
  raw_input: string;
  title: string;
  location_name?: string | null;
  google_place_id?: string | null;
  maps_url?: string | null;
  latitude?: number | null;
  longitude?: number | null;
  hotspot_id?: string | null;
  names?: Record<string, Record<string, string>>;
  data?: Record<string, unknown>;
};
type IngestResponse = { created: PlaceCandidate[]; matched: number; items: PlaceCandidate[] };

/**
 * The waiting list beside the days.
 *
 * Pasting a link is not the same as planning: everything lands here until the traveller
 * says which day it belongs to. `onAdd` puts one row into a day; the row only leaves the
 * list once that has happened, so a failed save does not lose what was pasted.
 */
export function TripInboxPanel({
  tripId,
  disabled,
  onAdd,
}: {
  tripId: string;
  disabled?: boolean;
  onAdd: (candidate: PlaceCandidate) => Promise<boolean> | boolean;
}) {
  const t = useTranslations("trips.inbox");
  const [items, setItems] = useState<PlaceCandidate[]>([]);
  const [text, setText] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<string>();
  const [notice, setNotice] = useState<string>();

  const load = useCallback(() => {
    api<{ items: PlaceCandidate[] }>(`/trips/${tripId}/places`)
      .then((value) => setItems(value.items))
      .catch(() => undefined);
  }, [tripId]);

  useEffect(load, [load]);

  async function ingest() {
    if (!text.trim()) return;
    setBusy(true);
    setError(undefined);
    setNotice(undefined);
    try {
      const value = await api<IngestResponse>(`/trips/${tripId}/places/ingest`, {
        method: "POST",
        body: JSON.stringify({ text }),
      });
      setItems(value.items);
      setText("");
      setNotice(t("added", { count: value.created.length, matched: value.matched }));
    } catch (reason) {
      setError(reason instanceof Error ? reason.message : t("failed"));
    } finally {
      setBusy(false);
    }
  }

  async function place(candidate: PlaceCandidate) {
    const added = await onAdd(candidate);
    if (!added) return;
    await api(`/trips/${tripId}/places/${candidate.id}/used`, { method: "POST" }).catch(() => undefined);
    setItems((current) => current.filter((row) => row.id !== candidate.id));
  }

  async function dismiss(candidate: PlaceCandidate) {
    await api(`/trips/${tripId}/places/${candidate.id}`, { method: "DELETE" }).catch(() => undefined);
    setItems((current) => current.filter((row) => row.id !== candidate.id));
  }

  return <section aria-label={t("title")} className="planner-tool-card">
    <div className="mb-3">
      <h3 className="font-bold">{t("title")}</h3>
      <p className="mt-1 text-xs leading-5 text-[var(--muted)]">{t("hint")}</p>
    </div>
    <label className="block text-sm font-semibold">
      <span className="sr-only">{t("pasteLabel")}</span>
      <textarea
        value={text}
        onChange={(event) => setText(event.target.value)}
        rows={3}
        maxLength={8000}
        placeholder={t("placeholder")}
        aria-label={t("pasteLabel")}
        className="w-full rounded-xl border border-[var(--line)] bg-white px-3 py-2 font-normal"
      />
    </label>
    <div className="mt-2 flex items-center gap-3">
      <button
        type="button"
        onClick={() => void ingest()}
        disabled={busy || disabled || !text.trim()}
        className="flex min-h-11 items-center gap-2 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white disabled:opacity-50"
      >
        {busy ? <Loader2 size={16} className="animate-spin" /> : <Plus size={16} />}
        {t("read")}
      </button>
      {notice && <span className="text-xs text-[var(--teal-dark)]">{notice}</span>}
      {error && <span role="alert" className="text-xs font-semibold text-red-700">{error}</span>}
    </div>

    {items.length > 0 && <ul className="mt-4 space-y-2">
      {items.map((candidate) => <li key={candidate.id} className="flex items-start gap-2 rounded-xl bg-[var(--paper)] p-3">
        <MapPin size={16} className="mt-0.5 shrink-0 text-[var(--muted)]" />
        <div className="min-w-0 flex-1">
          <p className="truncate text-sm font-semibold">{candidate.title}</p>
          <p className="truncate text-xs text-[var(--muted)]">
            {candidate.hotspot_id ? t("fromCatalog", { city: candidate.location_name || "" }) : t("fromPaste")}
          </p>
        </div>
        <button
          type="button"
          onClick={() => void place(candidate)}
          disabled={disabled}
          className="min-h-11 shrink-0 rounded-xl border border-[var(--teal)] px-3 text-xs font-semibold text-[var(--teal)] disabled:opacity-40"
        >
          {t("addToDay")}
        </button>
        <button
          type="button"
          aria-label={t("remove", { title: candidate.title })}
          onClick={() => void dismiss(candidate)}
          className="grid h-11 w-11 shrink-0 place-items-center rounded-xl text-[var(--muted)]"
        >
          <Trash2 size={15} />
        </button>
      </li>)}
    </ul>}
  </section>;
}
