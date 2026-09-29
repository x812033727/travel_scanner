"use client";

import { useTranslations } from "next-intl";
import { useCallback, useState } from "react";
import { AdminStatusPill } from "@/components/admin-ui";
import { control, useRefresh, useWhen } from "@/components/admin-video-review-card";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";

// The discussion on one document or one episode's screenplay (docs/videos/DRAMA-FLOW.md, section 3):
// the owner asks or asks for a change, the worker's model answers in the same thread, and a new
// version it writes shows up as the document's next version while the lines stay. The series page
// (admin-video-series.tsx) puts one on every document panel and the video page (admin-video-reviews.tsx)
// on the script gate card; this file only reads the helpers of admin-video-review-card.tsx, so that
// file never has to import it back.
export type MessageAuthor = "owner" | "planner" | "writer";
export type ThreadMessage = {
  id: string; subject: string; author: MessageAuthor; body_md: string;
  // "v3" when the line was said about version 3 of a document, the screenplay's hash cut short, or
  // null before the first version existed.
  refers_to: string | null;
  // Set once the model answered an owner's line; null on an owner's line means it is still waiting.
  answered_at: string | null;
  created_at: string; created_by_user_id: string | null;
};
export type Thread = { messages: ThreadMessage[] };

/** The thread's subject as the API names it: a document by kind (and chapter), a screenplay by episode. */
export const docSubject = (kind: string, chapter: number) => (kind === "chapter" ? `chapter:${chapter}` : kind);
export const scriptSubject = (episode: number) => `script:${episode}`;
export const threadPath = (seriesSlug: string, subject: string) => `/admin/video-automation/series/${seriesSlug}/messages?subject=${encodeURIComponent(subject)}`;
const message = (problem: unknown) => (problem instanceof Error ? problem.message : "");
const messagesOf = (value: unknown): ThreadMessage[] => {
  const messages = value && typeof value === "object" ? (value as { messages?: unknown }).messages : undefined;
  return Array.isArray(messages) ? messages as ThreadMessage[] : [];
};
const waitingOn = (messages: ThreadMessage[]) => messages.some((line) => line.author === "owner" && !line.answered_at);

/**
 * One thread: its lines (who, about which version, when), and the owner's input unless the
 * document or screenplay is approved, when the thread stays as a record. `waiting` lets the parent
 * say the model still owes an answer before the lines are read.
 */
export function DiscussionThread({ seriesSlug, subject, canManage, readOnly = false, waiting = false, onPosted, onMessagesLoaded }: {
  seriesSlug: string; subject: string; canManage: boolean; readOnly?: boolean; waiting?: boolean; onPosted?: () => void; onMessagesLoaded?: (messages: ThreadMessage[]) => void;
}) {
  const t = useTranslations("admin.videoSeries");
  const when = useWhen();
  const [messages, setMessages] = useState<ThreadMessage[] | null>(null);
  const [draft, setDraft] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [loadError, setLoadError] = useState("");
  const load = useCallback(() => {
    api<Thread>(threadPath(seriesSlug, subject)).then((value) => {
      const loaded = messagesOf(value);
      setMessages(loaded);
      setLoadError("");
      onMessagesLoaded?.(loaded);
    }).catch((problem: unknown) => setLoadError(message(problem) || "?"));
  }, [seriesSlug, subject, onMessagesLoaded]);
  useRefresh(load);
  const send = async () => {
    const body = draft.trim();
    if (!body) return;
    setBusy(true);
    setError("");
    try {
      const posted = await api<ThreadMessage>(`/admin/video-automation/series/${seriesSlug}/messages`, { method: "POST", body: JSON.stringify({ subject, body }) });
      setDraft("");
      // The thread is read again for anything said meanwhile; if that read fails, the line the
      // server took (the 201 body) still shows rather than vanishing until the next poll.
      const thread = await api<Thread>(threadPath(seriesSlug, subject)).catch(() => null);
      if (thread) setMessages(messagesOf(thread));
      else setMessages((current) => [...(current ?? []), posted]);
      onPosted?.();
    } catch (problem) {
      setError(t("thread.sendError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const refersTo = (line: ThreadMessage) => {
    if (!line.refers_to) return "";
    const version = /^v(\d+)$/.exec(line.refers_to);
    return version ? t("thread.aboutVersion", { n: Number(version[1]) }) : t("thread.aboutScript", { hash: line.refers_to });
  };
  const lines = messages ?? [];
  const pending = waiting || waitingOn(lines);
  if (readOnly && lines.length === 0) return null;
  return <section className="grid gap-3 rounded-2xl border border-[var(--line)] p-4" aria-label={t("thread.title")}>
    <p className="flex flex-wrap items-center gap-3 font-bold">{t("thread.title")}{pending && <AdminStatusPill status="running">{t("thread.waiting")}</AdminStatusPill>}</p>
    {messages && lines.length === 0 && <p className="text-sm leading-6 text-[var(--muted)]">{t("thread.empty")}</p>}
    {lines.length > 0 && <ol className="grid gap-2">{lines.map((line) => <li key={line.id} className={`grid gap-1 rounded-xl p-3 text-sm ${line.author === "owner" ? "bg-[var(--paper)]" : "border border-[var(--line)]"}`}>
      <span className="flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
        <strong className="text-[var(--ink)]">{t(`thread.authors.${line.author}`)}</strong>
        {refersTo(line) && <span>{refersTo(line)}</span>}
        <span>{when(line.created_at)}</span>
        {line.author === "owner" && !line.answered_at && <AdminStatusPill status="running">{t("thread.waiting")}</AdminStatusPill>}
      </span>
      <span className="whitespace-pre-wrap leading-6">{line.body_md}</span>
    </li>)}</ol>}
    {readOnly && <p className="text-sm text-[var(--muted)]">{t("thread.closed")}</p>}
    {canManage && !readOnly && <form className="grid gap-2" onSubmit={(event) => { event.preventDefault(); void send(); }}>
      <label className="grid gap-2 text-sm font-semibold">{t("thread.input")}
        <textarea className={control} rows={3} value={draft} disabled={busy} maxLength={8000} placeholder={t("thread.placeholder")} onChange={(event) => setDraft(event.target.value)} />
      </label>
      <div><Button type="submit" disabled={busy || !draft.trim()}>{busy ? t("thread.sending") : t("thread.send")}</Button></div>
    </form>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {loadError && !messages && <p role="alert" className="text-sm text-red-800">{t("thread.loadError", { message: loadError })}</p>}
  </section>;
}
