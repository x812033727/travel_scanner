"use client";

import { LoaderCircle, Trash2 } from "lucide-react";
import { useLocale } from "next-intl";
import { useId, useState } from "react";
import { control } from "@/components/admin-video-review-card";
import { Button } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { videoDeleteCopy } from "@/lib/admin-video-delete-copy";
import { api, ApiError } from "@/lib/api";
import { useModalSheet } from "@/lib/modal-sheet";

const STEP_UP_SCOPE = "videos.delete";

type Target = { slug: string; title: string; youtube_video_id?: string | null };

/**
 * The second question before a dropped video is deleted (apps/api/app/video_reviews/admin_deletion.py):
 * what goes, what stays, and the slug typed out, because nothing brings it back. The delete is tried
 * first and the password asked for only when the site wants it: a password opens five minutes, and
 * the site takes five a hour, which a catalog being cleared one video at a time would run through.
 */
function DeleteDialog({ target, onCancel, onDeleted }: { target: Target; onCancel: () => void; onDeleted: () => void }) {
  const copy = videoDeleteCopy(useLocale());
  const titleId = useId();
  const [typed, setTyped] = useState("");
  const [password, setPassword] = useState("");
  const [askPassword, setAskPassword] = useState(false);
  const [noPassword, setNoPassword] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  // What is under way cannot be taken back, so Escape is inert while it runs.
  const panel = useModalSheet<HTMLElement>(true, () => { if (!busy) onCancel(); });
  const remove = async () => {
    setBusy(true);
    setError("");
    try {
      if (askPassword) {
        await api("/admin/step-up", { method: "POST", body: JSON.stringify({ password, scopes: [STEP_UP_SCOPE] }) });
        setPassword("");
        setAskPassword(false);
      }
      await api(`/admin/videos/${target.slug}`, { method: "DELETE" });
      onDeleted();
    } catch (problem) {
      const code = problem instanceof ApiError ? problem.code : undefined;
      if (code?.startsWith("admin_step_up")) setAskPassword(true);
      else {
        if (code === "admin_password_not_set") setNoPassword(true);
        setError(copy.error.replace("{message}", problem instanceof Error ? problem.message : ""));
      }
    } finally {
      setBusy(false);
    }
  };
  return <div className="fixed inset-0 z-[110] grid place-items-center overflow-y-auto bg-slate-950/55 p-4" role="presentation" onMouseDown={(event) => { if (event.currentTarget === event.target && !busy) onCancel(); }}>
    <section ref={panel} role="dialog" aria-modal="true" aria-labelledby={titleId} className="grid w-full max-w-lg gap-3 rounded-[1.75rem] bg-[var(--surface)] p-6 shadow-2xl">
      <h2 id={titleId} className="text-2xl font-black">{copy.title}</h2>
      <p className="font-semibold">{target.title}</p>
      <p className="text-sm leading-6">{copy.goes}</p>
      <p className="text-sm leading-6 text-[var(--muted)]">{copy.stays}</p>
      {target.youtube_video_id && <p role="note" className="rounded-xl border border-amber-600 bg-amber-50 p-3 text-sm font-semibold leading-6 text-amber-950">{copy.youtube.replace("{id}", target.youtube_video_id)}</p>}
      <label className="grid gap-2 text-sm font-semibold">
        <span>{copy.typeSlug} <code className="rounded bg-[var(--paper)] px-1.5 py-0.5">{target.slug}</code></span>
        <input className={`${control} font-mono`} value={typed} disabled={busy} autoComplete="off" onChange={(event) => setTyped(event.target.value)} />
      </label>
      {askPassword && <label className="grid gap-2 text-sm font-semibold">{copy.password}
        <input className={control} type="password" autoComplete="current-password" value={password} disabled={busy} onChange={(event) => setPassword(event.target.value)} />
        <span className="font-normal text-[var(--muted)]">{copy.passwordHelp}</span>
      </label>}
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      {noPassword && <Link href="/forgot-password" className="text-sm font-semibold text-[var(--teal)] underline">{copy.setPassword}</Link>}
      <div className="mt-2 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
        <button type="button" disabled={busy} onClick={onCancel} className="min-h-12 rounded-xl border border-[var(--line)] px-5 font-bold disabled:opacity-50">{copy.cancel}</button>
        <button type="button" disabled={busy || typed !== target.slug || (askPassword && !password)} onClick={() => void remove()} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[var(--coral-fill)] px-5 font-bold text-white disabled:opacity-40">
          {busy && <LoaderCircle aria-hidden className="animate-spin motion-reduce:animate-none" size={17} />}{copy.confirm}
        </button>
      </div>
    </section>
  </div>;
}

/** The delete button of a dropped video; the caller shows it only to someone who may manage content. */
export function DeleteVideo({ project, compact = false, onDeleted }: { project: Target & { dropped_at?: string | null }; compact?: boolean; onDeleted: () => void }) {
  const copy = videoDeleteCopy(useLocale());
  const [open, setOpen] = useState(false);
  if (!project.dropped_at) return null;
  return <>
    {compact
      ? <button type="button" className="mt-1 inline-flex min-h-8 items-center gap-1 text-xs font-semibold text-red-800 underline-offset-2 hover:underline" onClick={() => setOpen(true)}><Trash2 aria-hidden size={14} />{copy.button}</button>
      : <div><Button secondary onClick={() => setOpen(true)}><Trash2 aria-hidden size={18} />{copy.button}</Button></div>}
    {open && <DeleteDialog target={project} onCancel={() => setOpen(false)} onDeleted={() => { setOpen(false); onDeleted(); }} />}
  </>;
}
