"use client";

import { CheckCircle2, Circle, Copy, ExternalLink, Link2, LoaderCircle, MinusCircle, RefreshCw, RotateCcw, Unlink, XCircle } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { type FormEvent, useCallback, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminStatusPill } from "@/components/admin-ui";
import { YoutubeManualUpload } from "@/components/admin-video-manual-upload";
import { YoutubeVpsUpload } from "@/components/admin-video-vps-upload";
import { control, record, type Review, text, useWhen, type YoutubeSync, type YoutubeSyncStep, youtubeVideoId } from "@/components/admin-video-review-card";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { ApiError, api } from "@/lib/api";
import { adminNavigate, useAdminQueryValue } from "@/lib/admin-workspace-navigation";

// The site's link to its own YouTube channel (docs/videos/HANDS-OFF.md, the YouTube API section;
// apps/api/app/video_youtube). The owner pastes their Google Cloud OAuth client on the settings
// tab and presses the link button, which goes through apps/web/app/api/admin-video-youtube to
// Google's consent screen and back. From then on the "ready to upload" card sends a video's
// package to the channel, and the video's page shows each step of the run.
export type YoutubeConnection = {
  client_id: string | null; client_secret_set: boolean; redirect_uri: string; scope: string;
  configured: boolean; linked: boolean; channel_id: string | null; channel_title: string | null; channel_url: string | null;
  linked_at: string | null; verified_at: string | null; problem: string | null; audited: boolean;
};
export type Visibility = "scheduled" | "unlisted" | "private";
const VISIBILITIES: Visibility[] = ["scheduled", "unlisted", "private"];
const TITLE_MAX = 100;
const DESCRIPTION_MAX_BYTES = 5000;
const ERROR_CODE = /^[a-z][a-z0-9_]{0,63}$/;
// How often a run in progress is read again: the mp4 goes up a chunk at a time.
export const SYNC_POLL_MS = 3000;

/** The linked channel, read once per mount; null until it answers or when it cannot be read. */
export function useYoutubeConnection() {
  const [connection, setConnection] = useState<YoutubeConnection | null>(null);
  const load = useCallback(() => {
    api<YoutubeConnection>("/admin/video-youtube").then(setConnection).catch(() => setConnection(null));
  }, []);
  useEffect(load, [load]);
  return { connection, reload: load };
}

/** Whether a video's run is going now. */
export const syncRunning = (sync: YoutubeSync | null | undefined) => Boolean(sync && (sync.status === "queued" || sync.status === "running") && !sync.interrupted);

/**
 * The sentence for a refusal. In zh-TW the API's own sentence is the most specific (it names what
 * YouTube said); the API answers the other locales with a generic sentence for these operator codes,
 * so they read the catalog's by code.
 */
function useProblem() {
  const t = useTranslations("admin.videoYoutube");
  const locale = useLocale();
  return (problem: unknown) => {
    if (locale === "zh-TW" && problem instanceof Error && problem.message) return problem.message;
    if (problem instanceof ApiError && problem.code && t.has(`errors.${problem.code}`)) return t(`errors.${problem.code}`);
    return problem instanceof Error && problem.message ? problem.message : t("errors.generic");
  };
}

/** Switch /admin/videos to its settings tab, where the channel is linked. */
export function openYoutubeSettings() {
  const target = new URL(window.location.href);
  target.searchParams.delete("video");
  target.searchParams.set("tab", "settings");
  adminNavigate(target);
}

function CopyButton({ value, label }: { value: string; label: string }) {
  const t = useTranslations("admin.videoYoutube");
  const [copied, setCopied] = useState(false);
  return <Button secondary aria-label={`${t("copy")} ${label}`} onClick={() => void navigator.clipboard?.writeText(value).then(() => setCopied(true), () => setCopied(false))}>
    <Copy aria-hidden size={16} />{copied ? t("copied") : t("copy")}
  </Button>;
}

/**
 * The settings tab's card: the steps in Google Cloud, the OAuth client, and the link. The secret
 * is written, never read back; the API keeps it and the grant encrypted and away from the page.
 */
export function YoutubeChannelCard() {
  const t = useTranslations("admin.videoYoutube");
  const locale = useLocale();
  const when = useWhen();
  const problemText = useProblem();
  const manage = useAdminActionGuard("settings.manage");
  const [linkedFlag, setLinkedFlag] = useAdminQueryValue("youtube", "", (value) => value === "linked");
  const [failure, setFailure] = useAdminQueryValue("youtube_error", "", (value) => ERROR_CODE.test(value));
  const [connection, setConnection] = useState<YoutubeConnection | null>(null);
  const [loadError, setLoadError] = useState("");
  const [clientId, setClientId] = useState<string | null>(null);
  const [secret, setSecret] = useState("");
  const [audited, setAudited] = useState<boolean | null>(null);
  const [busy, setBusy] = useState(false);
  const [message, setMessage] = useState("");
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<YoutubeConnection>("/admin/video-youtube").then((value) => { setConnection(value); setLoadError(""); }).catch((problem: unknown) => setLoadError(problem instanceof Error ? problem.message : ""));
  }, []);
  useEffect(load, [load]);

  const run = async (action: () => Promise<YoutubeConnection>, done: string) => {
    setBusy(true);
    setError("");
    setMessage("");
    try {
      setConnection(await action());
      setMessage(done);
    } catch (problem) {
      setError(problemText(problem));
    } finally {
      setBusy(false);
    }
  };
  const dismiss = () => { setLinkedFlag("", true); setFailure("", true); };

  if (loadError) return <section className={`${panelClass} grid gap-3`} aria-labelledby="video-settings-youtube"><h2 id="video-settings-youtube" className="text-xl font-bold">{t("title")}</h2><p role="alert" className="text-sm text-red-800">{t("loadError", { message: loadError })}</p></section>;
  if (!connection) return <section className={panelClass} aria-labelledby="video-settings-youtube"><h2 id="video-settings-youtube" className="text-xl font-bold">{t("title")}</h2><p className="mt-2 text-sm text-[var(--muted)]">{t("loading")}</p></section>;
  const disabled = !manage.allowed || busy;
  const shownClientId = clientId ?? connection.client_id ?? "";
  const shownAudited = audited ?? connection.audited;
  const clientValid = /^[0-9]{6,20}-[a-z0-9]{8,64}\.apps\.googleusercontent\.com$/.test(shownClientId.trim());
  const secretReady = connection.client_secret_set || secret.trim().length >= 8;
  const changed = shownClientId.trim() !== (connection.client_id ?? "") || secret.trim() !== "" || shownAudited !== connection.audited;
  const save = (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    void run(async () => {
      const saved = await api<YoutubeConnection>("/admin/video-youtube", { method: "PUT", body: JSON.stringify({ client_id: shownClientId.trim(), client_secret: secret.trim() || null, audited: shownAudited }) });
      setClientId(null);
      setSecret("");
      setAudited(null);
      return saved;
    }, t("saved"));
  };
  const unlink = () => {
    if (!window.confirm(t("unlinkConfirm"))) return;
    void run(async () => {
      const result = await api<{ revoked: boolean; connection: YoutubeConnection }>("/admin/video-youtube/unlink", { method: "POST" });
      if (!result.revoked) setError(t("unlinkNotRevoked"));
      return result.connection;
    }, t("unlinked"));
  };
  const verify = () => void run(() => api<YoutubeConnection>("/admin/video-youtube/verify", { method: "POST" }), t("verified"));

  return <section className={`${panelClass} grid gap-4`} aria-labelledby="video-settings-youtube">
    <h2 id="video-settings-youtube" className="text-xl font-bold">{t("title")}</h2>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("help")}</p>
    {(linkedFlag || failure) && <div role={failure ? "alert" : "status"} className={`flex flex-wrap items-center gap-3 rounded-xl p-3 text-sm ${failure ? "bg-red-50 text-red-800" : "bg-emerald-50 text-emerald-800"}`}>
      <span>{failure ? (t.has(`errors.${failure}`) ? t(`errors.${failure}`) : t("errors.generic")) : t("linkedNow")}</span>
      <Button secondary className="ml-auto" onClick={dismiss}>{t("dismiss")}</Button>
    </div>}

    {connection.linked ? <div className="grid gap-2 rounded-xl bg-[var(--paper)] p-4">
      <p className="flex flex-wrap items-center gap-2 font-semibold">
        <AdminStatusPill status={connection.problem ? "failed" : "active"}>{connection.problem ? t("statusBroken") : t("statusLinked")}</AdminStatusPill>
        {connection.channel_url ? <a href={connection.channel_url} target="_blank" rel="noreferrer" className="inline-flex items-center gap-1 text-[var(--teal)] underline">{connection.channel_title || connection.channel_id}<ExternalLink aria-hidden size={14} /></a> : connection.channel_title}
      </p>
      {connection.linked_at && <p className="text-sm text-[var(--muted)]">{t("linkedAt", { time: when(connection.linked_at) })}{connection.verified_at ? ` · ${t("verifiedAt", { time: when(connection.verified_at) })}` : ""}</p>}
      {connection.problem && <p role="alert" className="text-sm text-red-800">{connection.problem}</p>}
    </div> : <p className="flex items-center gap-2 text-sm"><AdminStatusPill status="inactive">{t("statusNotLinked")}</AdminStatusPill>{connection.configured ? t("readyToLink") : t("needsClient")}</p>}

    <details className="rounded-xl border border-[var(--line)] p-4" open={!connection.configured}>
      <summary className="cursor-pointer font-semibold">{t("stepsTitle")}</summary>
      <ol className="mt-3 grid list-decimal gap-2 pl-5 text-sm leading-6">
        <li>{t("step1")}</li>
        <li>{t("step2")}</li>
        <li>{t("step3")}
          <span className="mt-2 flex flex-wrap items-center gap-2"><code className="break-all rounded bg-[var(--paper)] px-2 py-1 text-xs">{connection.redirect_uri}</code><CopyButton value={connection.redirect_uri} label={t("redirectUri")} /></span>
        </li>
        <li>{t("step4", { scope: connection.scope })}</li>
        <li>{t("step5")}</li>
      </ol>
    </details>

    <form onSubmit={save} className="grid gap-3" aria-label={t("clientTitle")}>
      <p className="font-semibold">{t("clientTitle")}</p>
      <label className="block text-sm font-semibold">{t("clientId")}
        <input className={fieldClass} value={shownClientId} disabled={disabled} autoComplete="off" spellCheck={false} placeholder="123456789012-xxxxxxxx.apps.googleusercontent.com" onChange={(event) => setClientId(event.target.value)} />
      </label>
      {shownClientId.trim() && !clientValid && <p className="text-sm text-amber-800">{t("clientIdInvalid")}</p>}
      <label className="block text-sm font-semibold">{t("clientSecret")}
        <input className={fieldClass} type="password" value={secret} disabled={disabled} autoComplete="new-password" placeholder={connection.client_secret_set ? t("secretKept") : ""} onChange={(event) => setSecret(event.target.value)} />
      </label>
      <label className="flex min-h-11 items-start gap-2 text-sm"><input type="checkbox" className="mt-1" checked={shownAudited} disabled={disabled} onChange={(event) => setAudited(event.target.checked)} /><span><span className="font-semibold">{t("audited")}</span><span className="block text-[var(--muted)]">{t("auditedHelp")}</span></span></label>
      <div><Button type="submit" disabled={disabled || !changed || !clientValid || !secretReady}>{busy ? t("saving") : t("save")}</Button></div>
    </form>

    <div className="flex flex-wrap gap-3">
      {manage.allowed && connection.configured
        ? <a href={`/api/admin-video-youtube/start?locale=${encodeURIComponent(locale)}`} className="inline-flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-2 font-semibold text-white"><Link2 aria-hidden size={18} />{connection.linked ? t("relink") : t("link")}</a>
        : <Button disabled><Link2 aria-hidden size={18} />{t("link")}</Button>}
      {connection.linked && <Button secondary disabled={disabled} onClick={verify}><RefreshCw aria-hidden size={16} />{t("verify")}</Button>}
      {connection.linked && <Button secondary disabled={disabled} onClick={unlink}><Unlink aria-hidden size={16} />{t("unlink")}</Button>}
    </div>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("revokeHelp")}</p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {message && !error && <p role="status" className="text-sm text-[var(--teal)]">{message}</p>}
  </section>;
}

const utf8Bytes = (value: string) => new TextEncoder().encode(value).length;

/**
 * Send a video to the linked channel from the "ready to upload" card or the video's page. The
 * title, the description and the visibility are the owner's (YouTube's Required Minimum
 * Functionality); the rest comes from the approved package. ``videoId`` sends again to a video
 * that is already on YouTube, so the upload choice is not offered.
 */
export function YoutubePublishForm({ slug, review, connection, canUpload, videoId = null, previous = null, onSent }: {
  slug: string; review: Review | null; connection: YoutubeConnection; canUpload: boolean;
  videoId?: string | null; previous?: YoutubeSync["request"] | null; onSent: () => void;
}) {
  const t = useTranslations("admin.videoYoutube");
  const problemText = useProblem();
  const zh = record(review?.payload.zh);
  const uploadAllowed = canUpload && !videoId;
  // A run that failed is sent again as it was: the same source, and the same address.
  const [mode, setMode] = useState<"upload" | "studio">(uploadAllowed ? previous?.mode ?? (connection.audited ? "upload" : "studio") : "studio");
  const [url, setUrl] = useState(videoId ?? (previous?.mode === "studio" ? previous.video_id ?? "" : ""));
  const [title, setTitle] = useState(previous?.title ?? text(zh.title));
  const [description, setDescription] = useState(previous?.description ?? text(zh.description));
  const [visibility, setVisibility] = useState<Visibility>(previous?.visibility ?? "scheduled");
  const [publishAt, setPublishAt] = useState("");
  const [acceptLock, setAcceptLock] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const id = mode === "studio" ? youtubeVideoId(url) : null;
  const titleLength = [...title].length;
  const descriptionBytes = utf8Bytes(description);
  const textProblem = titleLength > TITLE_MAX ? t("titleTooLong", { max: TITLE_MAX }) : descriptionBytes > DESCRIPTION_MAX_BYTES ? t("descriptionTooLong", { max: DESCRIPTION_MAX_BYTES }) : /[<>]/.test(title + description) ? t("angleBrackets", { characters: "< >" }) : "";
  const lockNeeded = mode === "upload" && !connection.audited;
  const ready = !busy && !textProblem && (mode === "upload" ? !lockNeeded || acceptLock : Boolean(id)) && (visibility !== "scheduled" || Boolean(publishAt));
  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!ready) return;
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${slug}/youtube/publish`, {
        method: "POST",
        body: JSON.stringify({
          mode,
          url: mode === "studio" ? url.trim() : null,
          visibility,
          // A datetime-local value is the owner's wall clock; the API wants a zoned instant.
          publish_at: visibility === "scheduled" ? new Date(publishAt).toISOString() : null,
          title: title.trim() ? title : null,
          description: description.trim() ? description : null,
          accept_private_lock: lockNeeded && acceptLock,
        }),
      });
      onSent();
    } catch (problem) {
      setError(problemText(problem));
    } finally {
      setBusy(false);
    }
  };
  return <YoutubeVpsUpload slug={slug} disabled={busy} draft={{ title, description, video_id: videoId ?? id }} onChange={onSent}><YoutubeManualUpload slug={slug} disabled={busy} draft={{ title, description, video_id: videoId ?? id }}><form onSubmit={(event) => void submit(event)} className="grid gap-3 rounded-2xl border border-[var(--teal)] p-4" aria-label={t("publishTitle")}>
    <p className="font-bold">{t("publishTitle")}</p>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("publishHelp", { channel: connection.channel_title || connection.channel_id || "" })}</p>
    {uploadAllowed && <fieldset className="grid gap-2"><legend className="text-sm font-semibold">{t("source")}</legend>
      <label className="flex items-start gap-2 text-sm"><input type="radio" name={`youtube-source-${slug}`} className="mt-1" checked={mode === "upload"} disabled={busy} onChange={() => setMode("upload")} /><span>{t("sourceUpload")}</span></label>
      <label className="flex items-start gap-2 text-sm"><input type="radio" name={`youtube-source-${slug}`} className="mt-1" checked={mode === "studio"} disabled={busy} onChange={() => setMode("studio")} /><span>{t("sourceStudio")}</span></label>
    </fieldset>}
    {lockNeeded && <div className="grid gap-2 rounded-xl bg-amber-50 p-3 text-sm text-amber-900">
      <p>{t("lockWarning")}</p>
      <label className="flex items-start gap-2 font-semibold"><input type="checkbox" className="mt-1" checked={acceptLock} disabled={busy} onChange={(event) => setAcceptLock(event.target.checked)} />{t("lockAccept")}</label>
    </div>}
    {mode === "studio" && <>
      {!videoId && <p className="text-sm leading-6 text-[var(--muted)]">{t("studioHelp")}</p>}
      <label className="grid gap-2 text-sm font-semibold">{t("youtubeUrl")}
        <input className={control} value={url} disabled={busy || Boolean(videoId)} placeholder="https://studio.youtube.com/video/…/edit" onChange={(event) => setUrl(event.target.value)} />
      </label>
      {url.trim() && <p className={`text-sm ${id ? "text-[var(--muted)]" : "text-amber-800"}`}>{id ? t("videoId", { id }) : t("urlInvalid")}</p>}
    </>}
    <div className="grid gap-1">
      <label className="grid gap-2 text-sm font-semibold">{t("videoTitle")}
        <input className={control} value={title} disabled={busy} onChange={(event) => setTitle(event.target.value)} />
      </label>
      <span className="text-xs text-[var(--muted)]">{t("titleCount", { count: titleLength, max: TITLE_MAX })}</span>
    </div>
    <div className="grid gap-1">
      <label className="grid gap-2 text-sm font-semibold">{t("videoDescription")}
        <textarea className={`${control} text-sm font-normal`} rows={6} value={description} disabled={busy} onChange={(event) => setDescription(event.target.value)} />
      </label>
      <span className="text-xs text-[var(--muted)]">{t("descriptionCount", { count: descriptionBytes, max: DESCRIPTION_MAX_BYTES })}</span>
    </div>
    {textProblem && <p className="text-sm text-amber-800">{textProblem}</p>}
    <fieldset className="grid gap-2"><legend className="text-sm font-semibold">{t("visibility")}</legend>
      {VISIBILITIES.map((option) => <label key={option} className="flex items-start gap-2 text-sm"><input type="radio" name={`youtube-visibility-${slug}`} className="mt-1" checked={visibility === option} disabled={busy} onChange={() => setVisibility(option)} /><span>{t(`visibilities.${option}`)}</span></label>)}
    </fieldset>
    {visibility === "scheduled" && <label className="grid gap-2 text-sm font-semibold">{t("publishAt")}
      <input type="datetime-local" className={control} value={publishAt} disabled={busy} onChange={(event) => setPublishAt(event.target.value)} />
    </label>}
    <p className="text-xs leading-5 text-[var(--muted)]">{t("neverPublic")}</p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <div><Button type="submit" disabled={!ready}>{busy ? t("sending") : t("send")}</Button></div>
  </form></YoutubeManualUpload></YoutubeVpsUpload>;
}

const STEP_ICONS: Record<YoutubeSyncStep["state"], typeof Circle> = { pending: Circle, running: LoaderCircle, done: CheckCircle2, failed: XCircle, skipped: MinusCircle };
const STEP_TONES: Record<YoutubeSyncStep["state"], string> = { pending: "text-[var(--muted)]", running: "text-sky-700", done: "text-[var(--teal)]", failed: "text-red-700", skipped: "text-[var(--muted)]" };
const megabytes = (bytes: number) => (bytes / 1_000_000).toFixed(1);

/**
 * What the site last sent this video's YouTube side, step by step, read again every few seconds
 * while a run goes; a run that failed or stopped can be retried, and the finished steps are not
 * repeated.
 */
export function YoutubeSyncPanel({ slug, sync, canManage, onChange }: { slug: string; sync: YoutubeSync; canManage: boolean; onChange: () => void }) {
  const t = useTranslations("admin.videoYoutube");
  const when = useWhen();
  const problemText = useProblem();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const going = syncRunning(sync);
  useEffect(() => {
    if (!going) return;
    const timer = window.setInterval(onChange, SYNC_POLL_MS);
    return () => window.clearInterval(timer);
  }, [going, onChange]);
  const retry = async () => {
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${slug}/youtube/retry`, { method: "POST" });
      onChange();
    } catch (problem) {
      setError(problemText(problem));
    } finally {
      setBusy(false);
    }
  };
  const status = sync.interrupted ? "interrupted" : sync.status;
  const tone = { queued: "queued", running: "running", done: "ok", failed: "failed", interrupted: "warning" }[status];
  const request = sync.request ?? {};
  const progress = sync.progress && sync.progress.total > 0 ? sync.progress : null;
  const uploading = sync.steps.some((step) => step.id === "upload" && step.state === "running");
  return <section aria-label={t("syncTitle")} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <p className="flex flex-wrap items-center gap-2 font-bold">{t("syncTitle")}<AdminStatusPill status={tone}>{t(`statuses.${status}`)}</AdminStatusPill></p>
    <p className="text-sm text-[var(--muted)]">
      {request.visibility === "scheduled" && request.publish_at ? t("summaryScheduled", { time: when(request.publish_at) }) : request.visibility ? t(`visibilities.${request.visibility}`) : ""}
      {request.video_id ? ` · ${t("videoId", { id: request.video_id })}` : ""}
      {sync.finished_at ? ` · ${t("finishedAt", { time: when(sync.finished_at) })}` : ""}
    </p>
    {uploading && progress && <div className="grid gap-1 text-sm">
      <progress className="w-full" max={progress.total} value={progress.sent} aria-label={t("uploadProgress")} />
      <span className="text-[var(--muted)]">{t("progress", { sent: megabytes(progress.sent), total: megabytes(progress.total), percent: Math.floor((progress.sent / progress.total) * 100) })}</span>
    </div>}
    <ol className="grid gap-2">{sync.steps.map((step) => {
      const Icon = STEP_ICONS[step.state] ?? Circle;
      return <li key={step.id} className="grid gap-0.5 text-sm">
        <span className={`flex items-center gap-2 font-semibold ${STEP_TONES[step.state] ?? ""}`}><Icon aria-hidden size={16} className={step.state === "running" ? "animate-spin motion-reduce:animate-none" : ""} />{t(`steps.${step.id}`)} · {t(`stepStates.${step.state}`)}</span>
        {step.detail && <span className="whitespace-pre-wrap pl-6 text-[var(--muted)]">{step.detail}</span>}
      </li>;
    })}</ol>
    {sync.interrupted && <p className="text-sm text-amber-800">{t("interruptedHelp")}</p>}
    {sync.error && <p role="alert" className="text-sm text-red-800">{sync.error}</p>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {canManage && (sync.status === "failed" || sync.interrupted) && <div><Button disabled={busy} onClick={() => void retry()}><RotateCcw aria-hidden size={16} />{busy ? t("sending") : t("retry")}</Button></div>}
    {canManage && !going && !busy && <YoutubeVpsUpload slug={slug} onChange={onChange}><YoutubeManualUpload slug={slug} /></YoutubeVpsUpload>}
  </section>;
}

/** Where the owner links the channel, shown in place of the send form until it is linked. */
export function YoutubeLinkHint() {
  const t = useTranslations("admin.videoYoutube");
  return <div className="grid gap-3 rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">
    <span>{t("linkHint")}</span>
    <Button secondary onClick={openYoutubeSettings}><Link2 aria-hidden size={16} />{t("openSettings")}</Button>
    <YoutubeVpsUpload />
  </div>;
}
