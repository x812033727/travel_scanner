"use client";

import { Server, RefreshCw, ExternalLink } from "lucide-react";
import { useTranslations } from "next-intl";
import { type ReactNode, useCallback, useEffect, useRef, useState } from "react";
import { Button } from "@/components/community/ui";
import { control } from "@/components/admin-video-review-card";
import { api } from "@/lib/api";

type Job = {
  id: string; state: "staging" | "queued" | "running" | "needs_action" | "done" | "cancelled";
  code: string | null; video_id: string | null; upload_started: boolean;
  steps: { id: string; done: boolean }[];
  files: { role: string; size: number; received: number }[];
};
type View = { configured: boolean; linked: boolean; job: Job | null; new_package?: boolean };
type Draft = { title: string; description: string; video_id: string | null };
type Props = { slug?: string; draft?: Draft; onChange?: () => void; children?: ReactNode; disabled?: boolean };

function JobPanel({ slug, draft, onChange }: Required<Pick<Props, "slug">> & Pick<Props, "draft" | "onChange">) {
  const t = useTranslations("admin.videoYoutube.vps");
  const [view, setView] = useState<View | null>(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  const [url, setUrl] = useState(draft?.video_id ?? "");
  const controller = useRef<AbortController | null>(null);
  const path = `/admin/videos/${slug}/youtube/vps`;
  const change = useRef(onChange);
  useEffect(() => { change.current = onChange; }, [onChange]);
  const refresh = useCallback(async (signal?: AbortSignal) => {
    let result = await api<View>(path, { signal });
    if (result.job?.state === "done" && !result.linked && !result.new_package) {
      try {
        result = await api<View>(path + "/record", { method: "POST", body: "{}", signal });
      } catch (e) {
        if (!signal?.aborted) setView(result);
        throw e;
      }
      change.current?.();
    }
    setView(result);
    return result;
  }, [path]);
  useEffect(() => {
    const abort = new AbortController();
    let timer: ReturnType<typeof setTimeout>;
    const poll = async () => {
      try {
        const result = await refresh(abort.signal);
        if (!abort.signal.aborted && ["queued", "running"].includes(result.job?.state ?? "")) timer = setTimeout(() => void poll(), 10_000);
      } catch (e) {
        if (!abort.signal.aborted) setError(e instanceof Error ? e.message : t("failed"));
      }
    };
    void poll();
    return () => { abort.abort(); clearTimeout(timer); };
  }, [refresh, t, view?.job?.state]);
  useEffect(() => () => controller.current?.abort(), []);
  const action = async (name: "start" | "stage" | "resume" | "cancel" | "refresh" | "record") => {
    if (busy) return;
    setBusy(true); setError("");
    const abort = new AbortController(); controller.current = abort;
    try {
      if (name === "refresh" || name === "record") { await refresh(abort.signal); return; }
      const data = name === "start" ? { title: draft?.title, description: draft?.description, url: url.trim() || null } : { url: url.trim() || null };
      let result = await api<View>(name === "start" ? path : path + "/" + name, {
        method: "POST", body: JSON.stringify(data), signal: abort.signal,
      });
      setView(result);
      if (name === "start" || name === "stage" || name === "resume") {
        while (!abort.signal.aborted && result.job?.state === "staging") {
          result = await api<View>(path + "/stage", { method: "POST", body: "{}", signal: abort.signal });
          if (!abort.signal.aborted) setView(result);
        }
      }
    } catch (e) {
      if (!abort.signal.aborted) setError(e instanceof Error ? e.message : t("failed"));
    } finally { if (!abort.signal.aborted) setBusy(false); }
  };
  const job = view?.job;
  const total = job?.files.reduce((sum, f) => sum + f.size, 0) ?? 0;
  const received = job?.files.reduce((sum, f) => sum + Math.min(f.received, f.size), 0) ?? 0;
  const needsId = Boolean(job?.upload_started && !job.video_id);
  return <section className="grid min-w-0 gap-3 rounded-xl border border-[var(--line)] p-4" aria-label={t("title")}>
    <h3 className="font-bold">{t("title")}</h3>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("help")}</p>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {!view && !error && <p role="status">{t("loading")}</p>}
    {view && !view.configured && <p className="text-sm">{t("notConfigured")}</p>}
    {view?.configured && !job && <>
      <label className="grid gap-2 text-sm">{t("existingUrl")}<input className={control} value={url} disabled={busy || Boolean(draft?.video_id)} onChange={(e) => setUrl(e.target.value)} placeholder="https://youtu.be/…" /></label>
      <Button disabled={busy} onClick={() => void action("start")}>{busy ? t("sending") : t("send")}</Button>
    </>}
    {job && <>
      <p role="status" className="font-semibold">{t(`states.${job.state}`)}</p>
      {job.state === "staging" && <>
        <progress className="w-full" value={received} max={total || 1} aria-label={t("transfer")} />
        <p className="text-sm">{t("transferProgress", { received: (received / 1024 ** 2).toFixed(1), total: (total / 1024 ** 2).toFixed(1) })}</p>
        <p className="text-sm text-[var(--muted)]">{t("stagingHelp")}</p>
        <Button disabled={busy} onClick={() => void action("stage")}>{busy ? t("sending") : t("continueTransfer")}</Button>
      </>}
      {["queued", "running"].includes(job.state) && <p className="text-sm">{t("independent")}</p>}
      {job.state === "needs_action" && <>
        <p role="alert" className="text-sm text-amber-900">{t.has(`problems.${job.code}`) ? t(`problems.${job.code}`) : t("problems.studio_changed")}</p>
        <p className="text-sm">{t("desktopHelp")}</p>
        {needsId && <label className="grid gap-2 text-sm">{t("reconcileUrl")}<input className={control} value={url} onChange={(e) => setUrl(e.target.value)} disabled={busy} placeholder="https://youtu.be/…" /></label>}
        <Button disabled={busy || (needsId && !url.trim())} onClick={() => void action("resume")}>{t("resume")}</Button>
      </>}
      {job.state === "cancelled" && !view?.new_package && <Button disabled={busy} onClick={() => void action("resume")}>{t("restart")}</Button>}
      {view?.new_package && ["done", "cancelled"].includes(job.state) && <Button disabled={busy} onClick={() => void action("start")}>{t("newPackage")}</Button>}
      <ul className="grid gap-1 text-sm">{job.steps.map((s) => <li key={s.id}>{s.done ? "✓" : "○"} {t.has(`steps.${s.id}`) ? t(`steps.${s.id}`) : s.id.startsWith("captions_") ? t("captionStep", { language: s.id.slice(9) }) : t("translationStep", { language: s.id.slice(13) })}</li>)}</ul>
      {job.video_id && <a href={`https://studio.youtube.com/video/${job.video_id}/edit`} target="_blank" rel="noreferrer" className="inline-flex min-h-11 items-center gap-2 text-sm text-[var(--teal)] underline"><ExternalLink size={16} aria-hidden />{t("openVideo")}</a>}
      {job.state === "done" && !view?.new_package && <p className="text-sm">{view?.linked ? t("recorded") : t("recordHelp")}</p>}
      {job.state === "done" && !view?.linked && !view?.new_package && <Button disabled={busy} onClick={() => void action("record")}>{t("record")}</Button>}
      {["staging", "queued", "needs_action"].includes(job.state) && <Button secondary disabled={busy || (needsId && !url.trim())} onClick={() => void action("cancel")}>{t("cancel")}</Button>}
    </>}
    <div><Button secondary disabled={busy} onClick={() => void action("refresh")}><RefreshCw size={16} aria-hidden />{t("refresh")}</Button></div>
  </section>;
}

function ProjectPicker({ onChange }: Pick<Props, "onChange">) {
  const t = useTranslations("admin.videoYoutube.vps");
  const [projects, setProjects] = useState<{ slug: string; title: string }[]>([]);
  const [slug, setSlug] = useState("");
  const [error, setError] = useState("");
  useEffect(() => {
    const controller = new AbortController();
    api<{ slug: string; title: string; dropped_at?: string | null }[]>("/admin/videos", { signal: controller.signal })
      .then((items) => setProjects(items.filter((p) => !p.dropped_at)))
      .catch((e: unknown) => { if (!controller.signal.aborted) setError(e instanceof Error ? e.message : t("failed")); });
    return () => controller.abort();
  }, [t]);
  return <div className="grid gap-3">
    {error && <p role="alert">{error}</p>}
    <label className="grid gap-2 text-sm">{t("chooseVideo")}<select className={control} value={slug} onChange={(e) => setSlug(e.target.value)}><option value="">{t("chooseVideo")}</option>{projects.map((p) => <option key={p.slug} value={p.slug}>{p.title}</option>)}</select></label>
    {slug && <JobPanel key={slug} slug={slug} onChange={onChange} />}
  </div>;
}

export function YoutubeVpsUpload({ slug, draft, onChange, children, disabled = false }: Props) {
  const t = useTranslations("admin.videoYoutube.vps");
  const [open, setOpen] = useState(false);
  return <div className="grid min-w-0 gap-3">
    <div><Button secondary disabled={disabled} aria-expanded={open} onClick={() => setOpen((v) => !v)}><Server size={16} aria-hidden />{open ? t("close") : t("open")}</Button></div>
    {open ? slug ? <JobPanel key={slug} slug={slug} draft={draft} onChange={onChange} /> : <ProjectPicker onChange={onChange} /> : children}
  </div>;
}
