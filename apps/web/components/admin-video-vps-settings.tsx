"use client";

import { ExternalLink } from "lucide-react";
import { useLocale } from "next-intl";
import { type FormEvent, useEffect, useRef, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { ApiError, api } from "@/lib/api";
import { videoVpsCopy } from "@/lib/video-vps-copy";

export const VPS_SETTINGS_PATH = "/admin/video-youtube/vps/settings";
export type YoutubeVpsSettingsView = {
  enabled: boolean;
  url: string | null;
  channel_id: string | null;
  desktop_url: string | null;
  secret_set: boolean;
  configured: boolean;
  source: "database" | "environment" | "none";
  updated_at: string | null;
  last_test_status: "success" | "failed" | null;
  last_test_message: string | null;
  last_tested_at: string | null;
  browser_status?: "idle" | "working" | "stopped" | null;
  active_jobs?: number | null;
};
type Fields = { enabled: boolean; url: string; channel_id: string; desktop_url: string };
const fieldsOf = (view: YoutubeVpsSettingsView): Fields => ({
  enabled: view.enabled, url: view.url ?? "", channel_id: view.channel_id ?? "", desktop_url: view.desktop_url ?? "",
});
function changedFields(view: YoutubeVpsSettingsView, draft: Fields): Partial<Fields> {
  const changes: Partial<Fields> = {};
  if (draft.enabled !== view.enabled) changes.enabled = draft.enabled;
  for (const key of ["url", "channel_id", "desktop_url"] as const) {
    if (draft[key].trim() !== (view[key] ?? "")) changes[key] = draft[key].trim();
  }
  return changes;
}

export const youtubeVpsSettingsHref = (locale: string) => `/${encodeURIComponent(locale)}/admin/videos?tab=settings#youtube-vps-settings`;

/** Use only a saved desktop address, with a second protocol check before making it clickable. */
export function safeVpsDesktopUrl(value: string | null | undefined): string | null {
  if (!value || /[\s\\]/.test(value)) return null;
  try {
    const url = new URL(value);
    const host = url.hostname;
    const octets = /^\d+\.\d+\.\d+\.\d+$/.test(host) ? host.split(".").map(Number) : null;
    const privateV4 = octets && (octets[0] === 10 || octets[0] === 127 || (octets[0] === 172 && octets[1] >= 16 && octets[1] <= 31) || (octets[0] === 192 && octets[1] === 168));
    const privateHost = ["localhost", "mokaair-studio-uploader", "[::1]"].includes(host) || /^\[f[cd][0-9a-f]{2}:/.test(host) || privateV4;
    return !url.username && !url.password && !url.search && !url.hash && (url.protocol === "https:" || (url.protocol === "http:" && privateHost)) ? url.href : null;
  } catch { return null; }
}

export function YoutubeVpsDesktopLink({ url }: { url: string | null | undefined }) {
  const copy = videoVpsCopy(useLocale());
  const href = safeVpsDesktopUrl(url);
  return href ? <a href={href} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-2 text-sm font-semibold text-[var(--teal)] underline"><ExternalLink size={16} aria-hidden />{copy.openDesktop}</a> : null;
}

export function YoutubeVpsSettingsCard() {
  const locale = useLocale();
  const copy = videoVpsCopy(locale);
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<YoutubeVpsSettingsView | null>(null);
  const [draft, setDraft] = useState<Fields | null>(null);
  const [secret, setSecret] = useState("");
  const [busy, setBusy] = useState<"load" | "save" | "test" | null>("load");
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    api<YoutubeVpsSettingsView>(VPS_SETTINGS_PATH, { signal: controller.signal })
      .then((next) => { if (!controller.signal.aborted) { setView(next); setDraft(fieldsOf(next)); } })
      .catch((reason: unknown) => { if (!controller.signal.aborted) setError(reason instanceof Error ? reason.message : copy.failed); })
      .finally(() => { if (!controller.signal.aborted) setBusy(null); });
    return () => controller.abort();
  }, [copy.failed]);
  // The uploader's settings link names this card by its fragment, but the settings tab renders on
  // the client, after the browser's own jump found nothing to scroll to: arrive here once, when
  // the saved settings first show.
  const section = useRef<HTMLElement>(null);
  const arrived = useRef(false);
  useEffect(() => {
    if (!view || arrived.current) return;
    arrived.current = true;
    if (window.location.hash === "#youtube-vps-settings") section.current?.scrollIntoView?.({ block: "start" });
  }, [view]);

  const refresh = async () => {
    if (busy) return;
    setBusy("load"); setError(""); setNotice("");
    // Rebase only the user's edited fields on a newly read revision; preserve their secret.
    const edits = view && draft ? changedFields(view, draft) : {};
    try {
      const next = await api<YoutubeVpsSettingsView>(VPS_SETTINGS_PATH);
      setView(next); setDraft({ ...fieldsOf(next), ...edits });
      setNotice(copy.refreshed);
    } catch (reason) { setError(reason instanceof Error ? reason.message : copy.failed); }
    finally { setBusy(null); }
  };
  const changes = view && draft ? changedFields(view, draft) : {};
  const dirty = Object.keys(changes).length > 0 || Boolean(secret.trim());
  const needsNewSecret = Boolean(changes.url && !secret.trim());
  const secretValid = !secret.trim() || secret.trim().length >= 32;
  const complete = draft && (!draft.enabled || (draft.url.trim() && /^UC[A-Za-z0-9_-]{22}$/.test(draft.channel_id.trim()) && (view?.secret_set || secret.trim().length >= 32)));
  const disabled = !manage.allowed || Boolean(busy);
  const save = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (disabled || !view || !draft || !dirty || !complete || needsNewSecret || !secretValid) return;
    setBusy("save"); setError(""); setNotice("");
    try {
      const next = await api<YoutubeVpsSettingsView>(VPS_SETTINGS_PATH, {
        method: "PUT", body: JSON.stringify({ ...changes, ...(secret.trim() ? { secret: secret.trim() } : {}), expected_updated_at: view.updated_at }),
      });
      setView(next); setDraft(fieldsOf(next)); setSecret(""); setNotice(copy.saved);
    } catch (reason) {
      setError(reason instanceof ApiError && reason.status === 409 ? copy.conflict : reason instanceof Error ? reason.message : copy.failed);
    } finally { setBusy(null); }
  };
  const test = async () => {
    if (disabled || dirty || !view?.configured) return;
    setBusy("test"); setError(""); setNotice("");
    try {
      const next = await api<YoutubeVpsSettingsView>(VPS_SETTINGS_PATH + "/test", { method: "POST", body: "{}" });
      setView(next); setDraft(fieldsOf(next));
    } catch (reason) { setError(reason instanceof Error ? reason.message : copy.failed); }
    finally { setBusy(null); }
  };
  const source = view?.source === "database" ? copy.sourceDatabase : view?.source === "environment" ? copy.sourceEnvironment : copy.sourceNone;
  const browser = view?.browser_status === "working" ? copy.browserWorking : view?.browser_status === "idle" ? copy.browserIdle : view?.browser_status === "stopped" ? copy.browserStopped : null;
  const timestamp = view?.last_tested_at ? new Date(view.last_tested_at) : null;

  return <section ref={section} id="youtube-vps-settings" className={`${panelClass} grid min-w-0 scroll-mt-6 gap-4`} aria-labelledby="youtube-vps-settings-title">
    <h2 id="youtube-vps-settings-title" className="text-xl font-bold">{copy.title}</h2>
    <p className="text-sm leading-6 text-[var(--muted)]">{copy.help}</p>
    {!manage.allowed && <p role="note" className="text-sm">{copy.readOnly}</p>}
    {!view && !error && <p role="status">{copy.loading}</p>}
    {view && draft && <>
      <div className="grid gap-2 rounded-xl bg-[var(--paper)] p-4 text-sm">
        <p className="font-semibold">{!view.enabled ? copy.disabled : view.configured ? copy.configured : copy.notConfigured}</p>
        <p>{copy.source}: {source}</p>
        <p role={view.last_test_status === "failed" ? "alert" : "status"}>{view.last_test_status === "success" ? copy.testSuccess : view.last_test_status === "failed" ? copy.testFailed : copy.notTested}</p>
        {view.last_test_message && <p>{view.last_test_message}</p>}
        {timestamp && Number.isFinite(timestamp.getTime()) && <p>{copy.lastTest}: <time dateTime={view.last_tested_at!}>{timestamp.toLocaleString(locale)}</time></p>}
        {browser && <p>{copy.browser}: {browser}</p>}
        {typeof view.active_jobs === "number" && <p>{copy.activeJobs}: {view.active_jobs}</p>}
      </div>
      <form onSubmit={(event) => void save(event)} className="grid gap-3" aria-label={copy.title}>
        <label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={draft.enabled} disabled={disabled} onChange={(event) => setDraft({ ...draft, enabled: event.target.checked })} />{copy.enabled}</label>
        <div className="text-sm"><label htmlFor="vps-service-url" className="font-semibold">{copy.url}</label><input id="vps-service-url" aria-describedby="vps-service-url-help" type="url" className={fieldClass} value={draft.url} disabled={disabled} autoComplete="off" spellCheck={false} onChange={(event) => setDraft({ ...draft, url: event.target.value })} /><p id="vps-service-url-help" className="mt-1 text-[var(--muted)]">{copy.urlHelp}</p></div>
        <label className="block text-sm font-semibold">{copy.channel}<input className={fieldClass} value={draft.channel_id} disabled={disabled} autoComplete="off" spellCheck={false} onChange={(event) => setDraft({ ...draft, channel_id: event.target.value })} /></label>
        <div className="text-sm"><label htmlFor="vps-service-secret" className="font-semibold">{copy.secret}</label><input id="vps-service-secret" aria-describedby="vps-service-secret-help" type="password" minLength={32} className={fieldClass} value={secret} disabled={disabled} autoComplete="new-password" placeholder={view.secret_set ? copy.secretKept : ""} onChange={(event) => setSecret(event.target.value)} /><p id="vps-service-secret-help" className="mt-1 text-[var(--muted)]">{copy.secretHelp}</p></div>
        {needsNewSecret && <p className="text-sm text-amber-800">{copy.newSecretRequired}</p>}
        <div className="text-sm"><label htmlFor="vps-desktop-url" className="font-semibold">{copy.desktop}</label><input id="vps-desktop-url" aria-describedby="vps-desktop-url-help" type="url" className={fieldClass} value={draft.desktop_url} disabled={disabled} autoComplete="off" spellCheck={false} onChange={(event) => setDraft({ ...draft, desktop_url: event.target.value })} /><p id="vps-desktop-url-help" className="mt-1 text-[var(--muted)]">{copy.desktopHelp}</p></div>
        <div><Button type="submit" disabled={disabled || !dirty || !complete || needsNewSecret || !secretValid}>{busy === "save" ? copy.saving : copy.save}</Button></div>
      </form>
      <div className="flex flex-wrap items-center gap-3">
        <Button secondary disabled={disabled || dirty || !view.configured} onClick={() => void test()}>{busy === "test" ? copy.testing : copy.test}</Button>
        <YoutubeVpsDesktopLink url={view.desktop_url} />
      </div>
      {dirty && <p className="text-sm text-[var(--muted)]">{copy.saveBeforeTest}</p>}
      <p className="text-sm leading-6 text-[var(--muted)]">{copy.loginNote}</p>
    </>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {notice && !error && <p role="status" className="text-sm text-[var(--teal)]">{notice}</p>}
    <div><Button secondary disabled={Boolean(busy)} onClick={() => void refresh()}>{copy.refresh}</Button></div>
  </section>;
}
