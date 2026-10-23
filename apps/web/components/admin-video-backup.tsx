"use client";

import { useLocale } from "next-intl";
import { type FormEvent, useCallback, useEffect, useRef, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { ApiError, api } from "@/lib/api";
import { fill, type VideoBackupCopy, videoBackupCopy } from "@/lib/video-backup-copy";

// The backup to the owner's Google Drive (docs/videos/BACKUP.md): the settings the worker copies
// with, and whether every video on YouTube is in Drive yet (apps/api/app/video_backup).
export const BACKUP_SETTINGS_PATH = "/admin/video-backup/settings";
export const BACKUP_STATUS_PATH = "/admin/video-backup/status";
export const BACKUP_TEST_PATH = "/admin/video-backup/test";
export type Tier = "basic" | "full" | "off";
export type BackupState = "done" | "stale" | "pending" | "failed" | "blocked_quota" | "partial" | "not_queued" | "off";
export type BackupSettingsView = {
  enabled: boolean;
  path: string;
  lock_path: string | null;
  lock_reported_at: string | null;
  problem: string | null;
  tiers: Record<string, Tier>;
  folder_names: Record<string, string>;
  default_folder_names: Record<string, string>;
  full_categories: string[];
  updated_at: string | null;
  test: { pending_id: string | null; requested_at: string | null; status: "success" | "failed" | null; message: string | null; tested_at: string | null };
  space: { free_bytes: number | null; total_bytes: number | null; at: string | null };
};
export type BackupVideoView = {
  slug: string;
  title: string;
  youtube_video_id: string | null;
  series_key: string;
  folder: string;
  tier: Tier;
  state: BackupState;
  complete: boolean;
  bytes: number | null;
  at: string | null;
  error: string | null;
  missing: string[];
  overdue: boolean;
};
export type BackupStatusView = {
  enabled: boolean;
  path: string;
  uploaded: number;
  counts: Record<BackupState, number>;
  all_backed_up: boolean;
  overdue_hours: number;
  videos: BackupVideoView[];
};

type Row = { key: string; tier: Tier | ""; name: string };
type Draft = { enabled: boolean; path: string; rows: Row[] };
const SERIES_KEY = /^[a-z0-9][a-z0-9-]{0,39}$/;
// Drive's own root folder as the owner's PC names it (Traditional Chinese or English Windows).
const DRIVE_ROOTS = ["\u6211\u7684\u96f2\u7aef\u786c\u789f", "my drive"];
const FORBIDDEN = /[<>:"|?*\\\u0000-\u001f\u007f]/;

/** The Drive path a pasted folder saves as, the rule the API applies (target.normalise_path); null when it cannot be one. */
export function drivePath(value: string): string | null {
  let text = value.normalize("NFC").trim().replace(/\\/g, "/");
  if (/^[A-Za-z]:/.test(text)) text = text.slice(2);
  const parts = text.split("/").filter(Boolean);
  if (parts.length && DRIVE_ROOTS.includes(parts[0].toLowerCase())) parts.shift();
  if (!parts.length) return null;
  for (const part of parts) {
    if (part === "." || part === ".." || part.length > 120 || FORBIDDEN.test(part) || part !== part.trim() || part.endsWith(".")) return null;
  }
  const joined = parts.join("/");
  return joined.length <= 400 ? joined : null;
}

function rowsOf(view: BackupSettingsView): Row[] {
  const keys = [...new Set([...Object.keys(view.default_folder_names), ...Object.keys(view.tiers), ...Object.keys(view.folder_names)])].sort();
  return keys.map((key) => ({ key, tier: view.tiers[key] ?? "", name: view.folder_names[key] ?? "" }));
}
const draftOf = (view: BackupSettingsView): Draft => ({ enabled: view.enabled, path: view.path, rows: rowsOf(view) });
const sorted = (entries: [string, string][]) => Object.fromEntries(entries.sort(([a], [b]) => (a < b ? -1 : a > b ? 1 : 0)));
const tiersOf = (rows: Row[]) => sorted(rows.filter((row) => row.tier).map((row) => [row.key, row.tier]));
const namesOf = (rows: Row[]) => sorted(rows.filter((row) => row.name.trim()).map((row) => [row.key, row.name.trim()]));
const same = (left: object, right: object) => JSON.stringify(sorted(Object.entries(left))) === JSON.stringify(sorted(Object.entries(right)));

/** Only what the owner changed, so a save never rewrites a field someone else set meanwhile. */
function changesOf(view: BackupSettingsView, draft: Draft): Record<string, unknown> {
  const changes: Record<string, unknown> = {};
  if (draft.enabled !== view.enabled) changes.enabled = draft.enabled;
  if (draft.path.trim() !== view.path) changes.path = draft.path.trim();
  if (!same(tiersOf(draft.rows), view.tiers)) changes.tiers = tiersOf(draft.rows);
  if (!same(namesOf(draft.rows), view.folder_names)) changes.folder_names = namesOf(draft.rows);
  return changes;
}

export function sizeText(bytes: number): string {
  const units = ["B", "KB", "MB", "GB", "TB"];
  let value = bytes;
  let unit = 0;
  while (value >= 1024 && unit < units.length - 1) { value /= 1024; unit += 1; }
  return `${value >= 10 || unit === 0 ? Math.round(value) : value.toFixed(1)} ${units[unit]}`;
}

const stateLabel = (copy: VideoBackupCopy, state: BackupState) => ({
  done: copy.stateDone, stale: copy.stateStale, pending: copy.statePending, failed: copy.stateFailed,
  blocked_quota: copy.stateQuota, partial: copy.statePartial, not_queued: copy.stateNotQueued, off: copy.stateOff,
})[state];
const stateTone = (state: BackupState) => (state === "done" ? "text-[var(--teal)]" : state === "off" ? "text-[var(--muted)]" : state === "failed" || state === "partial" || state === "blocked_quota" ? "text-red-800" : "text-amber-800");

function VideoRow({ video, root, hours, copy, locale }: { video: BackupVideoView; root: string; hours: number; copy: VideoBackupCopy; locale: string }) {
  const when = video.at ? new Date(video.at) : null;
  const details = [
    video.missing.length ? fill(copy.missing, { files: video.missing.join(", ") }) : "",
    video.error ?? "",
    video.overdue ? fill(copy.overdue, { hours }) : "",
    video.state === "done" && when && Number.isFinite(when.getTime()) ? fill(copy.backedUp, { time: when.toLocaleString(locale), size: sizeText(video.bytes ?? 0) }) : "",
  ].filter(Boolean);
  return <tr className="border-t border-[var(--line)] align-top">
    <td className="py-2 pr-3"><span className="font-semibold">{video.title}</span><br /><code className="text-xs text-[var(--muted)]">{video.slug}</code></td>
    <td className={`py-2 pr-3 font-semibold ${stateTone(video.state)}`}>{stateLabel(copy, video.state)}</td>
    <td className="py-2 pr-3 break-all">{root}/{video.folder}</td>
    <td className="py-2">{details.map((line) => <p key={line} className="break-words">{line}</p>)}</td>
  </tr>;
}

function BackupStatus({ status, copy, locale, all, onToggle }: { status: BackupStatusView; copy: VideoBackupCopy; locale: string; all: boolean; onToggle: () => void }) {
  const left = status.uploaded - status.counts.done - status.counts.off;
  const summary = !status.enabled ? copy.offStatus
    : status.uploaded === 0 ? copy.noneUploaded
    : status.all_backed_up ? fill(copy.allDone, { count: status.uploaded, path: status.path })
    : fill(copy.notAllDone, { count: status.uploaded, left });
  const tone = status.enabled && status.uploaded > 0 && !status.all_backed_up ? "text-amber-800" : status.all_backed_up ? "text-[var(--teal)]" : "";
  return <div className="grid gap-3 rounded-xl bg-[var(--paper)] p-4 text-sm">
    <h3 className="text-base font-bold">{copy.statusTitle}</h3>
    <p role="status" className={`font-semibold ${tone}`}>{summary}</p>
    {status.uploaded > 0 && <p className="text-[var(--muted)]">{(Object.keys(status.counts) as BackupState[]).filter((state) => status.counts[state] > 0).map((state) => `${stateLabel(copy, state)} ${status.counts[state]}`).join(" · ")}</p>}
    {status.videos.length > 0 && <div className="overflow-x-auto"><table className="w-full min-w-[36rem] text-left text-sm">
      <caption className="sr-only">{copy.statusTitle}</caption>
      <thead><tr><th className="pb-2 pr-3">{copy.columnVideo}</th><th className="pb-2 pr-3">{copy.columnState}</th><th className="pb-2 pr-3">{copy.columnFolder}</th><th className="pb-2">{copy.columnDetail}</th></tr></thead>
      <tbody>{status.videos.map((video) => <VideoRow key={video.slug} video={video} root={status.path} hours={status.overdue_hours} copy={copy} locale={locale} />)}</tbody>
    </table></div>}
    {status.uploaded > 0 && <div><Button secondary onClick={onToggle}>{all ? copy.showIncomplete : copy.showAll}</Button></div>}
  </div>;
}

export function VideoBackupCard() {
  const locale = useLocale();
  const copy = videoBackupCopy(locale);
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<BackupSettingsView | null>(null);
  const [status, setStatus] = useState<BackupStatusView | null>(null);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [newKey, setNewKey] = useState("");
  const [all, setAll] = useState(false);
  const [busy, setBusy] = useState<"load" | "save" | "test" | null>("load");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const statusPath = (everything: boolean) => (everything ? `${BACKUP_STATUS_PATH}?all=true` : BACKUP_STATUS_PATH);
  const failure = useCallback((reason: unknown) => (reason instanceof Error && reason.message ? reason.message : copy.failed), [copy.failed]);

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      api<BackupSettingsView>(BACKUP_SETTINGS_PATH, { signal: controller.signal }),
      api<BackupStatusView>(BACKUP_STATUS_PATH, { signal: controller.signal }),
    ])
      .then(([settings, current]) => { if (!controller.signal.aborted) { setView(settings); setDraft(draftOf(settings)); setStatus(current); } })
      .catch((reason: unknown) => { if (!controller.signal.aborted) setError(failure(reason)); })
      .finally(() => { if (!controller.signal.aborted) setBusy(null); });
    return () => controller.abort();
  }, [failure]);
  // The settings tab renders on the client, after the browser's own jump to #video-backup-settings found nothing.
  const section = useRef<HTMLElement>(null);
  const arrived = useRef(false);
  useEffect(() => {
    if (!view || arrived.current) return;
    arrived.current = true;
    if (window.location.hash === "#video-backup-settings") section.current?.scrollIntoView?.({ block: "start" });
  }, [view]);

  const changes = view && draft ? changesOf(view, draft) : {};
  const dirty = Object.keys(changes).length > 0;
  const preview = draft ? drivePath(draft.path) : null;
  const disabled = !manage.allowed || Boolean(busy);

  const refresh = async (everything = all) => {
    if (busy) return;
    setBusy("load"); setError(""); setNotice("");
    try {
      const [settings, current] = await Promise.all([api<BackupSettingsView>(BACKUP_SETTINGS_PATH), api<BackupStatusView>(statusPath(everything))]);
      // Keep the owner's unsaved edits on top of what was just read.
      setView(settings); setStatus(current);
      setDraft(dirty && draft ? draft : draftOf(settings));
      setNotice(copy.refreshed);
    } catch (reason) { setError(failure(reason)); }
    finally { setBusy(null); }
  };
  const toggle = () => { const next = !all; setAll(next); void refresh(next); };
  const save = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (disabled || !view || !draft || !dirty || !preview) return;
    setBusy("save"); setError(""); setNotice("");
    try {
      const next = await api<BackupSettingsView>(BACKUP_SETTINGS_PATH, { method: "PUT", body: JSON.stringify({ ...changes, expected_updated_at: view.updated_at }) });
      setView(next); setDraft(draftOf(next)); setNotice(copy.saved);
      setStatus(await api<BackupStatusView>(statusPath(all)));
    } catch (reason) {
      setError(reason instanceof ApiError && reason.status === 409 ? copy.conflict : failure(reason));
    } finally { setBusy(null); }
  };
  const test = async () => {
    if (disabled || dirty) return;
    setBusy("test"); setError(""); setNotice("");
    try {
      setView(await api<BackupSettingsView>(BACKUP_TEST_PATH, { method: "POST", body: "{}" }));
    } catch (reason) { setError(failure(reason)); }
    finally { setBusy(null); }
  };
  const editRow = (key: string, change: Partial<Row>) => draft && setDraft({ ...draft, rows: draft.rows.map((row) => (row.key === key ? { ...row, ...change } : row)) });
  const addRow = () => {
    const key = newKey.trim();
    if (!draft || !SERIES_KEY.test(key) || draft.rows.some((row) => row.key === key)) return;
    const added: Row = { key, tier: "", name: "" };
    setDraft({ ...draft, rows: [...draft.rows, added].sort((a, b) => (a.key < b.key ? -1 : 1)) });
    setNewKey("");
  };
  const when = (value: string | null) => {
    const date = value ? new Date(value) : null;
    return date && Number.isFinite(date.getTime()) ? date.toLocaleString(locale) : "";
  };

  return <section ref={section} id="video-backup-settings" className={`${panelClass} grid min-w-0 scroll-mt-6 gap-4`} aria-labelledby="video-backup-settings-title">
    <h2 id="video-backup-settings-title" className="text-xl font-bold">{copy.title}</h2>
    <p className="text-sm leading-6 text-[var(--muted)]">{copy.help}</p>
    {!manage.allowed && <p role="note" className="text-sm">{copy.readOnly}</p>}
    {!view && !error && <p role="status">{copy.loading}</p>}
    {status && <BackupStatus status={status} copy={copy} locale={locale} all={all} onToggle={toggle} />}
    {view && draft && <>
      <div className="grid gap-2 rounded-xl bg-[var(--paper)] p-4 text-sm">
        <p>{view.lock_path ? fill(copy.lock, { path: view.lock_path }) : copy.lockUnknown}</p>
        {view.enabled && view.problem && <p role="alert" className="text-red-800">{fill(copy.problem, { problem: view.problem })}</p>}
        <p role={view.test.status === "failed" ? "alert" : "status"}>{view.test.status === "success" ? copy.testSuccess : view.test.status === "failed" ? copy.testFailed : copy.notTested}{view.test.tested_at ? ` · ${copy.lastTest}: ${when(view.test.tested_at)}` : ""}</p>
        {view.test.message && <p>{view.test.message}</p>}
        {view.test.pending_id && <p>{fill(copy.testPending, { time: when(view.test.requested_at) })}</p>}
        {view.space.free_bytes !== null && <p>{view.space.total_bytes !== null ? fill(copy.space, { free: sizeText(view.space.free_bytes), total: sizeText(view.space.total_bytes) }) : fill(copy.spaceFree, { free: sizeText(view.space.free_bytes) })}</p>}
      </div>
      <form onSubmit={(event) => void save(event)} className="grid gap-4" aria-label={copy.title}>
        <label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={draft.enabled} disabled={disabled} onChange={(event) => setDraft({ ...draft, enabled: event.target.checked })} />{copy.enabled}</label>
        <div className="text-sm">
          <label htmlFor="video-backup-path" className="font-semibold">{copy.path}</label>
          <input id="video-backup-path" aria-describedby="video-backup-path-help video-backup-path-preview" className={fieldClass} value={draft.path} disabled={disabled} autoComplete="off" spellCheck={false} onChange={(event) => setDraft({ ...draft, path: event.target.value })} />
          <p id="video-backup-path-help" className="mt-1 text-[var(--muted)]">{copy.pathHelp}</p>
          <p id="video-backup-path-preview" className={`mt-1 ${preview ? "" : "text-red-800"}`}>{preview ? fill(copy.pathPreview, { path: preview }) : copy.pathInvalid}</p>
        </div>
        <fieldset className="grid gap-3 text-sm" disabled={disabled}>
          <legend className="text-base font-bold">{copy.tiersTitle}</legend>
          <p className="leading-6 text-[var(--muted)]">{fill(copy.tiersHelp, { categories: view.full_categories.join(", ") })}</p>
          <div className="overflow-x-auto"><table className="w-full min-w-[30rem] text-left">
            <thead><tr><th className="pb-2 pr-3">{copy.seriesKey}</th><th className="pb-2 pr-3">{copy.tiersTitle}</th><th className="pb-2">{copy.folderName}</th></tr></thead>
            <tbody>{draft.rows.map((row) => <tr key={row.key} className="border-t border-[var(--line)]">
              <td className="py-2 pr-3"><code>{row.key}</code></td>
              <td className="py-2 pr-3"><select aria-label={`${copy.tiersTitle} ${row.key}`} className={fieldClass} value={row.tier} onChange={(event) => editRow(row.key, { tier: event.target.value as Row["tier"] })}>
                <option value="">{copy.tierDefault}</option><option value="basic">{copy.tierBasic}</option><option value="full">{copy.tierFull}</option><option value="off">{copy.tierOff}</option>
              </select></td>
              <td className="py-2"><input aria-label={`${copy.folderName} ${row.key}`} className={fieldClass} value={row.name} maxLength={120} placeholder={view.default_folder_names[row.key] ?? row.key} onChange={(event) => editRow(row.key, { name: event.target.value })} /></td>
            </tr>)}</tbody>
          </table></div>
          <div className="flex flex-wrap items-end gap-2">
            <label className="grid gap-1 font-semibold">{copy.newSeries}<input className={fieldClass} value={newKey} maxLength={40} spellCheck={false} onChange={(event) => setNewKey(event.target.value.toLowerCase())} /></label>
            <Button secondary type="button" disabled={!SERIES_KEY.test(newKey.trim())} onClick={addRow}>{copy.addSeries}</Button>
          </div>
          {newKey.trim() && !SERIES_KEY.test(newKey.trim()) && <p className="text-red-800">{copy.newSeriesInvalid}</p>}
        </fieldset>
        <div><Button type="submit" disabled={disabled || !dirty || !preview}>{busy === "save" ? copy.saving : copy.save}</Button></div>
      </form>
      <div className="flex flex-wrap items-center gap-3">
        <Button secondary disabled={disabled || dirty} onClick={() => void test()}>{busy === "test" ? copy.testing : copy.test}</Button>
        {dirty && <p className="text-sm text-[var(--muted)]">{copy.saveBeforeTest}</p>}
      </div>
    </>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {notice && !error && <p role="status" className="text-sm text-[var(--teal)]">{notice}</p>}
    <div><Button secondary disabled={Boolean(busy)} onClick={() => void refresh()}>{copy.refresh}</Button></div>
  </section>;
}
