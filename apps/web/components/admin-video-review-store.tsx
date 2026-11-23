"use client";

import { useLocale } from "next-intl";
import { type FormEvent, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { ApiError, api } from "@/lib/api";
import { fill } from "@/lib/video-backup-copy";
import { videoReviewStoreCopy } from "@/lib/video-review-store-copy";

// How much the preview store may hold (owner, 2026-11-19): GET /admin/videos/store reads what it
// holds, and the cap is the `video_reviews` provider setting (apps/api/app/admin/service.py),
// saved through the provider-settings route. The host's .env value is the default; a saved one
// wins and applies at once.
export const REVIEW_STORE_PATH = "/admin/videos/store";
export const PROVIDER_SETTINGS_PATH = "/admin/provider-settings";
export const REVIEW_STORE_PROVIDER = "video_reviews";
const FIELD = "video_review_max_total_bytes";
// Decimal gigabytes, the unit the setting has always been sized in (the 20 GB default).
export const GB = 1_000_000_000;
const MIN_GB = 1;
const MAX_GB = 500;
const NEARLY_FULL = 0.8;

export type ReviewStoreView = {
  used_bytes: number;
  max_total_bytes: number;
  max_file_bytes: number;
  disk_free_bytes: number | null;
  disk_total_bytes: number | null;
};
type ProviderRow = { provider: string; updated_at: string | null };

/** Bytes in decimal units, the ones the limit is typed in: 80 GB reads back as 80 GB. */
export function sizeText(bytes: number): string {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let value = bytes;
  let unit = 0;
  while (value >= 1000 && unit < units.length - 1) { value /= 1000; unit += 1; }
  return `${value >= 10 || unit === 0 ? Math.round(value) : value.toFixed(1)} ${units[unit]}`;
}

/** The whole gigabytes a typed value names, or null when it is not one from 1 to 500. */
export function wholeGb(text: string): number | null {
  if (!/^\d+$/.test(text.trim())) return null;
  const value = Number(text.trim());
  return value >= MIN_GB && value <= MAX_GB ? value : null;
}

export function VideoReviewStoreCard() {
  const copy = videoReviewStoreCopy(useLocale());
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<ReviewStoreView | null>(null);
  const [failed, setFailed] = useState(false);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState("");
  const [error, setError] = useState("");

  // Bumped to read the store again (after a save, or when the owner asks).
  const [reads, setReads] = useState(0);
  const load = () => setReads((count) => count + 1);

  useEffect(() => {
    let live = true;
    api<ReviewStoreView>(REVIEW_STORE_PATH).then((next) => {
      if (!live) return;
      setView(next);
      setDraft(String(Math.round(next.max_total_bytes / GB)));
      setFailed(false);
    }).catch(() => {
      if (live) setFailed(true);
    });
    return () => { live = false; };
  }, [reads]);

  const save = async (event: FormEvent) => {
    event.preventDefault();
    const gb = wholeGb(draft);
    setNotice("");
    setError("");
    if (gb === null) {
      setError(copy.invalid);
      return;
    }
    setBusy(true);
    try {
      // The provider row's stamp guards a concurrent edit; no row yet is an explicit null.
      const snapshot = await api<{ providers: ProviderRow[] }>(PROVIDER_SETTINGS_PATH);
      const row = snapshot.providers.find((item) => item.provider === REVIEW_STORE_PROVIDER);
      await api(`${PROVIDER_SETTINGS_PATH}/${REVIEW_STORE_PROVIDER}`, {
        method: "PUT",
        body: JSON.stringify({ expected_updated_at: row?.updated_at ?? null, config: { [FIELD]: gb * GB } }),
      });
      load();
      setNotice(fill(copy.saved, { limit: sizeText(gb * GB) }));
    } catch (problem) {
      setError(problem instanceof ApiError && problem.status === 409 ? copy.conflict : problem instanceof Error && problem.message ? problem.message : copy.failed);
    } finally {
      setBusy(false);
    }
  };

  const title = <h3 className="text-lg font-bold">{copy.title}</h3>;
  if (!view) {
    return <section aria-label={copy.title} className={`${panelClass} grid gap-3`}>
      {title}
      {failed
        ? <p role="status" className="text-red-800">{copy.failed} <button type="button" className="underline" onClick={load}>{copy.refresh}</button></p>
        : <p role="status" className="text-[var(--muted)]">{copy.loading}</p>}
    </section>;
  }
  const share = view.max_total_bytes > 0 ? view.used_bytes / view.max_total_bytes : 0;
  const percent = Math.min(100, Math.round(share * 100));
  const draftGb = wholeGb(draft);
  const roomOnDisk = view.disk_free_bytes === null ? null : view.used_bytes + view.disk_free_bytes;
  const overDisk = draftGb !== null && roomOnDisk !== null && draftGb * GB > roomOnDisk;
  return <section aria-label={copy.title} className={`${panelClass} grid gap-3 text-sm`}>
    {title}
    <p className="leading-6 text-[var(--muted)]">{copy.help}</p>
    <p className="font-semibold">{fill(copy.used, { used: sizeText(view.used_bytes), limit: sizeText(view.max_total_bytes), percent })}</p>
    <div role="progressbar" aria-label={copy.title} aria-valuemin={0} aria-valuemax={100} aria-valuenow={percent} className="h-2 w-full overflow-hidden rounded-full bg-[var(--paper)]">
      <div className={`h-full ${share >= NEARLY_FULL ? "bg-red-700" : "bg-[var(--teal)]"}`} style={{ width: `${percent}%` }} />
    </div>
    {share >= NEARLY_FULL && <p role="status" className="font-semibold text-red-800">{copy.nearlyFull}</p>}
    <p className="text-[var(--muted)]">
      {view.disk_free_bytes !== null && view.disk_total_bytes !== null
        ? fill(copy.disk, { free: sizeText(view.disk_free_bytes), total: sizeText(view.disk_total_bytes) })
        : copy.diskUnknown}
    </p>
    {manage.allowed
      ? <form aria-label={copy.limitLabel} className="flex flex-wrap items-end gap-3" onSubmit={(event) => void save(event)}>
        <label className="grid gap-2 font-semibold">{copy.limitLabel}
          <input className={fieldClass} type="number" inputMode="numeric" min={MIN_GB} max={MAX_GB} step={1} value={draft} disabled={busy} onChange={(event) => { setDraft(event.target.value); setNotice(""); setError(""); }} />
        </label>
        <Button type="submit" disabled={busy || draftGb === null || draftGb * GB === view.max_total_bytes}>{busy ? copy.saving : copy.save}</Button>
        <span className="basis-full text-[var(--muted)]">{copy.limitHelp}</span>
        {overDisk && <span role="alert" className="basis-full text-amber-800">{copy.overDisk}</span>}
      </form>
      : <p className="text-[var(--muted)]">{copy.readOnly}</p>}
    {notice && <p role="status">{notice}</p>}
    {error && <p role="alert" className="text-red-800">{error}</p>}
  </section>;
}
