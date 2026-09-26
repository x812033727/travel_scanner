"use client";

import { useLocale, useTranslations } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { AdminStatusPill } from "@/components/admin-ui";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";

// What the video pipeline reports (apps/api/app/video_reviews/schemas.py). Payloads come from
// tools/video/review; the page reads them defensively, since an older tool may send less.
// look and storyboard are the drama format's gates (docs/videos/DRAMA.md): the character sheets
// the owner picks one of, and the keyframes of every shot before any clip is paid for.
// This file holds the review card and the gate bodies, shared by the tutorial list, the drama
// series page and any page that shows a video's reviews; the pages themselves import it, so it
// must not import them back.
export type Gate = "outline" | "look" | "audio" | "storyboard" | "final" | "publish";
export type Status = "pending" | "approved" | "rejected" | "superseded";
export type ReviewFile = { role: string; sha256: string; size: number; content_type: string };
export type Review = {
  id: string; gate: Gate; subject?: string | null; content_sha256: string; summary: string; payload: Record<string, unknown>;
  files: ReviewFile[]; status: Status; choice: string | null; note: string | null;
  decided_at: string | null; created_at: string;
};
export type ChecklistItem = { key: string; label: string; done: boolean };
export type ProjectSummary = {
  slug: string; title: string; stage: string; checklist: ChecklistItem[];
  youtube_video_id: string | null; last_synced_at: string; pending: number;
  dropped_at?: string | null; dropped_note?: string | null;
  format?: "slides" | "drama"; media_usd?: number; clip_seconds?: number;
};
export type Project = ProjectSummary & { reviews: Review[] };

// How often a list or a page reads the site again while open: the worker moves a video every
// few minutes, so this is enough to watch a step land without reloading.
export const REFRESH_MS = 60_000;

export const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
export const statusTone: Record<Status, string> = { pending: "pending", approved: "active", rejected: "failed", superseded: "inactive" };
export const control = "min-h-11 w-full rounded-xl border border-[var(--control-border,var(--line))] bg-[var(--surface)] px-3 py-2 text-[var(--ink)]";

/** Payload readers: a review's payload is whatever the tool sent, so every field is checked. */
export const record = (value: unknown): Record<string, unknown> => (value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {});
export const list = (value: unknown): unknown[] => (Array.isArray(value) ? value : []);
export const text = (value: unknown): string => (typeof value === "string" ? value : typeof value === "number" ? String(value) : "");
export const count = (value: unknown): number => (typeof value === "number" && Number.isFinite(value) ? value : 0);

export function fileUrl(slug: string, file: ReviewFile | undefined): string | undefined {
  return file ? `/api/admin-video-files/${slug}/${file.sha256}` : undefined;
}

export const fileFor = (review: Review, role: string) => review.files.find((file) => file.role === role);

export function useWhen() {
  const locale = useLocale();
  const formatter = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  return (value: string) => formatter.format(new Date(value));
}

/** Read again every REFRESH_MS while mounted, so progress shows up without a reload. */
export function useRefresh(load: () => void) {
  useEffect(() => {
    load();
    const timer = window.setInterval(load, REFRESH_MS);
    return () => window.clearInterval(timer);
  }, [load]);
}

function OutlineBody({ review, choice, onChoice, disabled }: { review: Review; choice: string; onChoice: (key: string) => void; disabled: boolean }) {
  const t = useTranslations("admin.videoReviews");
  const options = list(review.payload.options).map(record).filter((option) => text(option.key));
  const brief = text(review.payload.brief);
  return <div className="grid gap-4">
    {options.length > 0 && <fieldset className="grid gap-3" disabled={disabled || review.status !== "pending"}>
      <legend className="font-bold">{t("chooseOption")}</legend>
      {options.map((option) => {
        const key = text(option.key);
        const selected = (review.status === "pending" ? choice : review.choice) === key;
        return <label key={key} className={`grid gap-1 rounded-2xl border p-4 ${selected ? "border-[var(--teal)] bg-[var(--paper)]" : "border-[var(--line)]"}`}>
          <span className="flex items-center gap-3 font-bold"><input type="radio" name={`outline-${review.id}`} value={key} checked={selected} onChange={() => onChoice(key)} />{t("option", { key })}{text(option.title) && `: ${text(option.title)}`}</span>
          {text(option.summary) && <span className="text-sm leading-6 text-[var(--muted)]">{text(option.summary)}</span>}
          {text(option.hook) && <span className="text-sm leading-6"><strong>{t("hook")}</strong> {text(option.hook)}</span>}
        </label>;
      })}
    </fieldset>}
    {brief && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("brief")}</summary><div className="mt-3 max-h-[32rem] overflow-y-auto whitespace-pre-wrap text-sm leading-7">{brief}</div></details>}
  </div>;
}

/** A judge's verdict as the tool sends it: an overall score and the faults it named. */
export function JudgeLine({ value }: { value: unknown }) {
  const t = useTranslations("admin.videoReviews");
  const judge = record(value);
  if (typeof judge.overall !== "number") return null;
  const problems = list(judge.problems).map(text).filter(Boolean);
  return <span className="text-sm leading-6 text-[var(--muted)]">{t("judgeScore", { score: judge.overall })}{problems.length > 0 && `：${problems.join("；")}`}</span>;
}

/** The look gate: one character's candidate sheets, the owner picks the one every shot is drawn from. */
function LookBody({ slug, review, choice, onChoice, disabled }: { slug: string; review: Review; choice: string; onChoice: (key: string) => void; disabled: boolean }) {
  const t = useTranslations("admin.videoReviews");
  const character = record(review.payload.character);
  const options = list(review.payload.options).map(record).filter((option) => text(option.key));
  const suggested = text(review.payload.suggested);
  return <div className="grid gap-4">
    {(text(character.name) || text(character.description)) && <p className="leading-7"><strong>{text(character.name)}</strong>{text(character.voice) && <span className="text-sm text-[var(--muted)]"> · {t("voice", { voice: text(character.voice) })}</span>}<span className="block text-sm leading-6 text-[var(--muted)]">{text(character.description)}</span></p>}
    {options.length > 0 && <fieldset className="grid gap-3 md:grid-cols-2 xl:grid-cols-3" disabled={disabled || review.status !== "pending"}>
      <legend className="mb-2 font-bold">{t("chooseLook")}</legend>
      {options.map((option) => {
        const key = text(option.key);
        const selected = (review.status === "pending" ? choice : review.choice) === key;
        const src = fileUrl(slug, fileFor(review, text(option.file_role)));
        return <label key={key} className={`grid gap-2 rounded-2xl border p-3 ${selected ? "border-[var(--teal)] bg-[var(--paper)]" : "border-[var(--line)]"}`}>
          {/* A private, session-bound preview: the image optimizer cannot fetch it. */}
          {/* eslint-disable-next-line @next/next/no-img-element */}
          {src && <img src={src} alt={t("candidate", { key })} className="aspect-video w-full rounded-xl object-cover" loading="lazy" />}
          <span className="flex items-center gap-3 font-bold"><input type="radio" name={`look-${review.id}`} value={key} checked={selected} onChange={() => onChoice(key)} />{t("candidate", { key })}{suggested === key && <span className="text-sm font-semibold text-[var(--teal)]">{t("suggested")}</span>}</span>
          <JudgeLine value={option.judge} />
        </label>;
      })}
    </fieldset>}
  </div>;
}

/** The storyboard gate: every shot's keyframe with the judge's verdict, and the contact sheet. */
function StoryboardBody({ slug, review }: { slug: string; review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const shots = list(review.payload.shots).map(record);
  const duplicates = list(review.payload.duplicates).map(record);
  const sheet = fileUrl(slug, fileFor(review, "contact_sheet"));
  return <div className="grid gap-4">
    <p className="leading-7"><strong>{t("checks")}</strong> <JudgeLine value={review.payload.judge} /></p>
    {duplicates.length > 0 && <p className="text-sm leading-6 text-[var(--muted)]">{t("lookAlike", { pairs: duplicates.map((pair) => `${text(pair.a)}／${text(pair.b)}`).join("、") })}</p>}
    {shots.length > 0 && <ol className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">{shots.map((shot, index) => {
      const src = fileUrl(slug, fileFor(review, text(shot.file_role)));
      return <li key={text(shot.id) || index} className={`grid gap-2 rounded-2xl border p-3 ${shot.needs_review === true ? "border-amber-600" : "border-[var(--line)]"}`}>
        {/* eslint-disable-next-line @next/next/no-img-element */}
        {src && <img src={src} alt={text(shot.id)} className="aspect-video w-full rounded-xl object-cover" loading="lazy" />}
        <span className="font-bold">{index + 1}. {text(shot.id)}{text(shot.chapter) && <span className="text-sm font-normal text-[var(--muted)]"> · {text(shot.chapter)}</span>}{typeof shot.seconds === "number" && <span className="text-sm font-normal text-[var(--muted)]"> · {t("seconds", { seconds: shot.seconds })}</span>}</span>
        {shot.needs_review === true && <span className="text-sm font-semibold text-amber-800">{t("shotNeedsReview")}</span>}
        <span className="text-sm leading-6">{text(shot.prompt)}</span>
        <JudgeLine value={shot.judge} />
      </li>;
    })}</ol>}
    {sheet && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("contactSheet")}</summary>
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={sheet} alt={t("contactSheet")} className="mt-3 w-full rounded-xl" loading="lazy" />
    </details>}
  </div>;
}

function AudioBody({ slug, review }: { slug: string; review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const check = record(review.payload.check);
  const flagged = list(review.payload.flagged_lines).map(record);
  const src = fileUrl(slug, fileFor(review, "narration"));
  return <div className="grid gap-4">
    {src && <label className="grid gap-2 font-bold">{t("narration")}<audio controls preload="metadata" src={src} className="w-full" /></label>}
    {Object.keys(check).length > 0 && <p className="leading-7">
      <strong>{t("check")}</strong>{" "}
      {t("checkSummary", { lines: count(check.lines), exact: count(check.exact), alike: count(check.alike), judged: count(check.judged_fine), flagged: count(check.flagged) })}
    </p>}
    {flagged.length > 0 && <div className="grid gap-2"><p className="font-bold">{t("flaggedLines")}</p>
      <ul className="grid gap-2">{flagged.map((line) => <li key={text(line.id)} className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">
        <span className="block">{t("script")}: {text(line.script)}</span><span className="block">{t("heard")}: {text(line.heard)}</span>
      </li>)}</ul>
    </div>}
  </div>;
}

function FinalBody({ slug, review }: { slug: string; review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const checks = record(review.payload.checks);
  const problems = list(checks.problems).map(text).filter(Boolean);
  const chapters = list(review.payload.chapters).map(record);
  const metadata = Object.entries(record(review.payload.metadata)).map(([locale, value]) => [locale, record(value)] as const);
  const video = fileUrl(slug, fileFor(review, "preview"));
  const sheet = fileUrl(slug, fileFor(review, "contact_sheet"));
  const poster = fileUrl(slug, fileFor(review, "thumbnail"));
  return <div className="grid gap-4">
    {video && <label className="grid gap-2 font-bold">{t("preview")}<video controls preload="metadata" src={video} poster={poster} className="aspect-video w-full rounded-xl bg-black" /></label>}
    {Object.keys(checks).length > 0 && <p className="leading-7"><strong>{t("checks")}</strong>{" "}{checks.ok === true ? t("checksOk") : problems.join("; ")}</p>}
    {chapters.length > 0 && <div><p className="font-bold">{t("chapters")}</p><ol className="mt-2 grid gap-1 text-sm">{chapters.map((chapter, index) => <li key={index}><span className="font-mono">{text(chapter.time)}</span> {text(chapter.title)}</li>)}</ol></div>}
    {sheet && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("contactSheet")}</summary>
      {/* A private, session-bound preview: the image optimizer cannot fetch it. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={sheet} alt={t("contactSheet")} className="mt-3 w-full rounded-xl" loading="lazy" />
    </details>}
    {metadata.length > 0 && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("metadata")}</summary>
      <dl className="mt-3 grid gap-3">{metadata.map(([locale, values]) => <div key={locale}><dt className="font-mono text-xs text-[var(--muted)]">{locale}</dt><dd className="font-semibold">{text(values.title)}</dd><dd className="whitespace-pre-wrap text-sm leading-6">{text(values.description)}</dd></div>)}</dl>
    </details>}
  </div>;
}

function PublishBody({ review }: { review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const items = list(review.payload.checklist).map(text).filter(Boolean);
  return items.length ? <div><p className="font-bold">{t("uploadChecklist")}</p><ul className="mt-2 grid gap-1 text-sm leading-6">{items.map((item) => <li key={item}>• {item}</li>)}</ul></div> : null;
}

/** One review of one gate: its body, and the owner's approve or reject with a note. */
export function ReviewCard({ slug, review, canManage, onDecided }: { slug: string; review: Review; canManage: boolean; onDecided: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [choice, setChoice] = useState("");
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const pending = review.status === "pending";
  const needsChoice = (review.gate === "outline" || review.gate === "look") && list(review.payload.options).length > 0;
  const decide = async (decision: "approve" | "reject") => {
    setBusy(true);
    setError("");
    try {
      await api(`/admin/videos/${slug}/reviews/${review.id}/decision`, {
        method: "POST",
        body: JSON.stringify({ decision, choice: decision === "approve" && needsChoice ? choice : undefined, note: note.trim() || undefined }),
      });
      onDecided();
    } catch (problem) {
      setError(t("decideError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  const approveLabels: Partial<Record<Gate, string>> = { outline: t("approveOutline"), look: t("approveLook"), storyboard: t("approveStoryboard"), publish: t("approvePublish") };
  const approveLabel = approveLabels[review.gate] ?? t("approve");
  const title = review.gate === "look" && text(record(review.payload.character).name) ? `${t("gates.look")}：${text(record(review.payload.character).name)}` : t(`gates.${review.gate}`);
  return <article className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" aria-label={title}>
    <header className="flex flex-wrap items-center gap-3">
      <h3 className="text-lg font-bold">{title}</h3>
      <AdminStatusPill status={statusTone[review.status]}>{t(`statuses.${review.status}`)}</AdminStatusPill>
      <span className="text-sm text-[var(--muted)]">{t("submittedAt", { time: when(review.created_at) })}</span>
    </header>
    <p className="mt-2 leading-7">{review.summary}</p>
    <div className="mt-4">
      {review.gate === "outline" && <OutlineBody review={review} choice={choice} onChoice={setChoice} disabled={!canManage || busy} />}
      {review.gate === "look" && <LookBody slug={slug} review={review} choice={choice} onChoice={setChoice} disabled={!canManage || busy} />}
      {review.gate === "storyboard" && <StoryboardBody slug={slug} review={review} />}
      {review.gate === "audio" && <AudioBody slug={slug} review={review} />}
      {review.gate === "final" && <FinalBody slug={slug} review={review} />}
      {review.gate === "publish" && <PublishBody review={review} />}
    </div>
    {pending ? <div className="mt-5 grid gap-3 border-t border-[var(--line)] pt-4">
      <label className="grid gap-2 text-sm font-semibold">{t("note")}
        <textarea className={control} rows={3} value={note} disabled={!canManage || busy} placeholder={t("notePlaceholder")} onChange={(event) => setNote(event.target.value)} />
      </label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div className="flex flex-wrap gap-3">
        <Button disabled={!canManage || busy || (needsChoice && !choice)} onClick={() => void decide("approve")}>{busy ? t("saving") : approveLabel}</Button>
        <Button secondary disabled={!canManage || busy || !note.trim()} onClick={() => void decide("reject")}>{t("reject")}</Button>
      </div>
    </div> : review.decided_at && <p className="mt-4 border-t border-[var(--line)] pt-4 text-sm leading-6">
      {t("decidedAt", { time: when(review.decided_at) })}
      {review.choice && ` · ${t("choice", { key: review.choice })}`}
      {review.note && <span className="block whitespace-pre-wrap">{review.note}</span>}
    </p>}
  </article>;
}
