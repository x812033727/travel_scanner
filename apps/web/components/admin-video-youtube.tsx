"use client";

import { CheckCircle2, ExternalLink, Send, XCircle } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useRef, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminStatusPill } from "@/components/admin-ui";
import { type ProjectSummary, useWhen } from "@/components/admin-video-review-card";
import { Button } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";

// The YouTube channel the site publishes through (docs/videos/HANDS-OFF.md, the YouTube API's
// first step): after the owner uploads a cut in Studio as private and pastes its address, the
// site adds the titles and descriptions of the chosen languages, the captions and the thumbnail
// and sets the publish time once every chosen language is made (docs/videos/LANGUAGES.md). The
// consent runs on the site; the refresh token stays on the server. This file holds the settings
// tab's connection card and the video page's record of what was sent.

export type Connection = {
  configured: boolean; connected: boolean; channel_id: string | null; channel_title: string | null;
  connected_at: string | null; redirect_uri: string; scope: string;
};
export type SyncStep = { id: string; ok: boolean; detail: string };
export type SyncRecord = {
  at: string; video_id: string | null; reason: string; ok: boolean; steps: SyncStep[];
  localizations?: string[]; captions?: string[]; scheduled_at?: string | null; thumbnail_sha256?: string | null;
};

const SYNC_STEPS = ["video", "schedule", "captions", "thumbnail"] as const;
const REASONS = ["linked", "languages", "manual"] as const;
// The video page reads itself again this long after a send is queued: the sync runs on the queue.
export const RELOAD_AFTER_MS = 5000;
// What the callback's youtube= parameter may say: "connected", or the error Google named.
const OUTCOME = /^[a-z_]{1,40}$/;

/**
 * The settings tab's card: whether the OAuth client is filled in on the provider card, whether
 * a channel is connected, and the owner's connect and revoke buttons. Connecting sends the
 * browser to Google's consent screen and comes back here with youtube=connected, or the error
 * Google named.
 */
export function YouTubeConnectionCard() {
  const t = useTranslations("admin.videoSettings");
  const when = useWhen();
  const owner = useAdminActionGuard("roles.manage");
  const [connection, setConnection] = useState<Connection | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [outcome, setOutcome] = useAdminQueryValue("youtube", "", (value) => OUTCOME.test(value));
  const load = useCallback(() => {
    api<Connection>("/admin/video-youtube/connection").then((value) => { setConnection(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, []);
  useEffect(load, [load]);
  const connect = async () => {
    setBusy(true);
    setError("");
    try {
      const next = `${window.location.pathname}${window.location.search}`;
      const started = await api<{ authorization_url: string }>("/admin/video-youtube/connection/start", { method: "POST", body: JSON.stringify({ next_path: next }) });
      // location.assign() is not protected by React, so the API-supplied URL is scheme-checked.
      const target = safeExternalHref(started.authorization_url);
      if (!target) throw new Error(t("youtubeError", { code: "bad_url" }));
      window.location.assign(target);
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : "");
      setBusy(false);
    }
  };
  const revoke = async () => {
    if (!window.confirm(t("youtubeRevokeConfirm"))) return;
    setBusy(true);
    setError("");
    try {
      setConnection(await api<Connection>("/admin/video-youtube/connection", { method: "DELETE" }));
      setOutcome("");
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : "");
    } finally {
      setBusy(false);
    }
  };
  return <section aria-label={t("youtubeTitle")} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <p className="font-bold">{t("youtubeTitle")}</p>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("youtubeHelp")}</p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {outcome === "connected" && <p role="status" className="text-sm text-[var(--teal)]">{t("youtubeJustConnected")}</p>}
    {outcome && outcome !== "connected" && <p role="alert" className="text-sm text-red-800">{t("youtubeError", { code: outcome })}</p>}
    {connection && <>
      {!connection.configured && <p className="text-sm leading-6">
        {t("youtubeNotConfigured")}{" "}
        <Link href="/admin/ai-accounts" className="inline-flex items-center gap-1 font-semibold text-[var(--teal)] underline">{t("youtubeProviderCard")}<ExternalLink aria-hidden size={14} /></Link>
      </p>}
      <p className="text-sm leading-6"><span className="font-semibold">{t("youtubeRedirectUri")}</span>{" "}<code className="break-all rounded bg-[var(--paper)] px-1">{connection.redirect_uri}</code></p>
      <p className="flex flex-wrap items-center gap-2 text-sm leading-6">
        {connection.connected
          ? <><AdminStatusPill status="active">{t("youtubeConnectedPill")}</AdminStatusPill><span>{t("youtubeConnected", { channel: connection.channel_title ?? connection.channel_id ?? "", time: connection.connected_at ? when(connection.connected_at) : "" })}</span></>
          : <><AdminStatusPill status="inactive">{t("youtubeNotConnectedPill")}</AdminStatusPill><span>{t("youtubeNotConnected")}</span></>}
      </p>
      {!owner.allowed && <p className="text-sm text-[var(--muted)]">{t("youtubeOwnerOnly")}</p>}
      <div className="flex flex-wrap gap-3">
        {!connection.connected && <Button disabled={!owner.allowed || !connection.configured || busy} onClick={() => void connect()}>{t("youtubeConnect")}</Button>}
        {connection.connected && <Button secondary disabled={!owner.allowed || busy} onClick={() => void revoke()}>{t("youtubeRevoke")}</Button>}
      </div>
    </>}
  </section>;
}

const known = <T extends string>(list: readonly T[], value: string): T | null => ((list as readonly string[]).includes(value) ? (value as T) : null);

/**
 * The video page's record of what the site sent to YouTube and how each step went, with a
 * button to send again (a retry never uploads a caption track twice). Shown once the owner has
 * pasted the video's address; before the first send it says so.
 */
export function YouTubeSyncCard({ slug, project, canManage, onSynced }: { slug: string; project: ProjectSummary; canManage: boolean; onSynced: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [busy, setBusy] = useState(false);
  const [queued, setQueued] = useState(false);
  const [error, setError] = useState("");
  const timer = useRef<number | null>(null);
  useEffect(() => () => { if (timer.current !== null) window.clearTimeout(timer.current); }, []);
  const record = project.youtube_sync ?? null;
  const reason = record ? (known(REASONS, record.reason) ?? "manual") : "manual";
  const send = async () => {
    setBusy(true);
    setError("");
    try {
      await api(`/admin/video-youtube/${slug}/sync`, { method: "POST" });
      setQueued(true);
      timer.current = window.setTimeout(() => { setQueued(false); onSynced(); }, RELOAD_AFTER_MS);
    } catch (problem) {
      setError(t("youtubeSyncError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <section aria-label={t("youtubeSyncTitle")} className="grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
    <p className="font-bold">{t("youtubeSyncTitle")}</p>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("youtubeSyncHelp")}</p>
    {!record && <p className="text-sm text-[var(--muted)]">{t("youtubeSyncNone")}</p>}
    {record && <>
      <p className="flex flex-wrap items-center gap-2 text-sm">
        <AdminStatusPill status={record.ok ? "ok" : "failed"}>{record.ok ? t("youtubeSyncOk") : t("youtubeSyncFailed")}</AdminStatusPill>
        <span>{t("youtubeSyncAt", { time: when(record.at), reason: t(`youtubeSyncReasons.${reason}`) })}</span>
      </p>
      <ul className="grid gap-1 text-sm leading-6">{record.steps.map((step, index) => {
        const id = known(SYNC_STEPS, step.id);
        return <li key={`${step.id}-${index}`} className="flex items-start gap-2">
          {step.ok ? <CheckCircle2 aria-hidden size={16} className="mt-1 shrink-0 text-[var(--teal)]" /> : <XCircle aria-hidden size={16} className="mt-1 shrink-0 text-red-700" />}
          <span><span className="font-semibold">{id ? t(`youtubeSyncSteps.${id}`) : step.id}</span>{" "}{step.detail}</span>
        </li>;
      })}</ul>
      {record.scheduled_at && <p className="text-sm text-[var(--muted)]">{t("youtubeSyncScheduled", { time: when(record.scheduled_at) })}</p>}
    </>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {queued && !error && <p role="status" className="text-sm text-[var(--muted)]">{t("youtubeSyncQueued")}</p>}
    <div><Button secondary disabled={!canManage || busy} onClick={() => void send()}><Send aria-hidden size={16} />{t("youtubeSyncRetry")}</Button></div>
  </section>;
}
