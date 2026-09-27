"use client";

import { CheckCircle2, Copy, Download, XCircle } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { type FormEvent, useEffect, useMemo, useRef, useState } from "react";
import { AdminStatusPill } from "@/components/admin-ui";
import { Button } from "@/components/community/ui";
import { api } from "@/lib/api";

// What the video pipeline reports (apps/api/app/video_reviews/schemas.py). Payloads come from
// tools/video/review; the page reads them defensively, since an older tool may send less.
// look and storyboard are the drama format's gates (docs/videos/DRAMA.md): the character sheets
// the owner picks one of, and the keyframes of every shot before any clip is paid for. languages
// is a batch of the languages the owner chose after the final cut (docs/videos/LANGUAGES.md): for
// each, its titles and descriptions, captions and dub track; dubs is what that gate was called when
// it carried dub tracks alone (docs/videos/DUBS.md), kept so older rows still read.
// This file holds the review card and the gate bodies, shared by the tutorial list, the drama
// series page and any page that shows a video's reviews; the pages themselves import it, so it
// must not import them back.
// script is an episode's screenplay, read before any image or clip is paid for (docs/videos/SERIES.md).
export type Gate = "outline" | "script" | "look" | "audio" | "storyboard" | "final" | "publish" | "languages" | "dubs";
export type Status = "pending" | "approved" | "rejected" | "superseded";
export type ReviewFile = { role: string; sha256: string; size: number; content_type: string };
export type Review = {
  id: string; gate: Gate; subject?: string | null; content_sha256: string; summary: string; payload: Record<string, unknown>;
  files: ReviewFile[]; status: Status; choice: string | null; note: string | null;
  decided_at: string | null; created_at: string;
};
export type ChecklistItem = { key: string; label: string; done: boolean };
// The languages a video can get on top of Traditional Chinese, in the page's order, and the three
// parts each one is made of (docs/videos/LANGUAGES.md): titles and descriptions, closed captions,
// a dub track. A dub track is timed with its captions, so choosing it means choosing them too.
export const LOCALES = ["en", "ja", "ko", "zh-CN"] as const;
export type Locale = (typeof LOCALES)[number];
export const LOCALE_PARTS = ["metadata", "captions", "dub"] as const;
export type LocalePart = (typeof LOCALE_PARTS)[number];
export type LocaleChoice = Partial<Record<LocalePart, boolean>>;
// Where a chosen part stands, from the server: not reported yet, made, given up on (with the
// worker's reason), or, for a dub track, uploaded by the owner in Studio.
export type LanguagePart = { state: "working" | "ready" | "skipped" | "uploaded" | string; reason?: string | null };
export type ProjectSummary = {
  slug: string; title: string; stage: string; checklist: ChecklistItem[];
  youtube_video_id: string | null; last_synced_at: string; pending: number;
  // Set by the owner on the "ready to upload" card (docs/videos/HANDS-OFF.md), and when the upload
  // confirmation was approved; both absent from an API older than this page.
  youtube_publish_at?: string | null; publish_approved_at?: string | null;
  dropped_at?: string | null; dropped_note?: string | null;
  format?: "slides" | "drama"; media_usd?: number; clip_seconds?: number;
  // The languages the owner chose after the final cut and what of each, when they first decided,
  // where each chosen part stands, and the server's verdict on whether the video may be scheduled
  // (docs/videos/LANGUAGES.md); all absent from an API older than the language panel, which
  // only knew the dub languages.
  locales?: Partial<Record<string, LocaleChoice>>;
  locales_decided_at?: string | null;
  languages?: Partial<Record<string, Partial<Record<string, LanguagePart>>>>;
  ready_to_upload?: boolean;
  // What the site last sent to YouTube for this video and how each step went (docs/videos/HANDS-OFF.md,
  // the YouTube API's first step; admin-video-youtube.tsx shows it).
  youtube_sync?: { at: string; video_id: string | null; reason: string; ok: boolean; steps: { id: string; ok: boolean; detail: string }[]; localizations?: string[]; captions?: string[]; scheduled_at?: string | null; thumbnail_sha256?: string | null } | null;
  dub_locales?: string[];
  series_slug?: string | null; episode_number?: number | null;
};
export type Project = ProjectSummary & { reviews: Review[] };

// How often a list or a page reads the site again while open: the worker moves a video every
// few minutes, so this is enough to watch a step land without reloading.
export const REFRESH_MS = 60_000;

export const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;
export const statusTone: Record<Status, string> = { pending: "pending", approved: "active", rejected: "failed", superseded: "inactive" };
export const control = "min-h-11 w-full rounded-xl border border-[var(--control-border,var(--line))] bg-[var(--surface)] px-3 py-2 text-[var(--ink)]";

// Jev's thresholds for choosing an outline (apps/api/app/video_automation/judge.py and the section
// of docs/videos/HANDS-OFF.md on Jev picking the outline): the chosen option must keep to the
// channel's stance and show something the viewer can do, and the brief must give no advice.
export const PICK_MIN_STANCE = 0.6;
export const PICK_MIN_DEMO = 0.6;
export const PICK_MAX_ADVICE = 0.3;
// The note the server writes on an outline Jev chose (judge.pick_note) starts with "Jev" and the
// two characters U+6311 U+4E86 ("picked"); they are code points here because a component file may
// not carry display text of its own.
const JEV_NOTE = "Jev \u6311\u4e86";
// A video on YouTube keeps its upload package in the review store; the mp4 alone leaves after
// this long, counted from the later of the upload confirmation and the publish time
// (apps/api/app/video_reviews/admin_service.py prune_published_previews).
export const PREVIEW_RETENTION_MS = 7 * 24 * 60 * 60 * 1000;

/** Payload readers: a review's payload is whatever the tool sent, so every field is checked. */
export const record = (value: unknown): Record<string, unknown> => (value && typeof value === "object" && !Array.isArray(value) ? value as Record<string, unknown> : {});
export const list = (value: unknown): unknown[] => (Array.isArray(value) ? value : []);
export const text = (value: unknown): string => (typeof value === "string" ? value : typeof value === "number" ? String(value) : "");
export const count = (value: unknown): number => (typeof value === "number" && Number.isFinite(value) ? value : 0);
export const number = (value: unknown): number | null => (typeof value === "number" && Number.isFinite(value) ? value : null);

export function fileUrl(slug: string, file: ReviewFile | undefined): string | undefined {
  return file ? `/api/admin-video-files/${slug}/${file.sha256}` : undefined;
}

export const fileFor = (review: Review, role: string) => review.files.find((file) => file.role === role);

/** An outline the server approved from Jev's pick, as opposed to one the owner chose. */
export const jevPicked = (review: Review) => review.gate === "outline" && review.status === "approved" && (review.note ?? "").startsWith(JEV_NOTE);

/** The worker reports a video that stopped with stage "blocked" and a first checklist row of that key. */
export const isBlocked = (project: ProjectSummary) => project.stage === "blocked" || project.checklist.some((item) => item.key === "blocked" && !item.done);
/**
 * What waits for the owner: a decision, a video that stopped (docs/videos/HANDS-OFF.md), or a
 * finished cut whose languages they have not chosen yet (docs/videos/LANGUAGES.md).
 */
export const needsOwner = (project: ProjectSummary) => !project.dropped_at && (project.pending > 0 || isBlocked(project) || publishState(project) === "deciding");
/** A summary from an API with the language panel carries the server's verdict on scheduling. */
const knowsLanguages = (project: ProjectSummary) => typeof project.ready_to_upload === "boolean";
/**
 * The video may be scheduled: the server says so (its upload confirmation approved, its languages
 * decided and every chosen part made), and the owner has not pasted a YouTube address yet. An
 * older API has no languages, so its verdict is the approved upload confirmation alone.
 */
export const readyToUpload = (project: ProjectSummary) => !project.dropped_at && !project.youtube_video_id
  && (knowsLanguages(project) ? Boolean(project.ready_to_upload) : Boolean(project.publish_approved_at));
/** The final cut is approved: the checklist says so, or something that comes after it already happened. */
export const finalApproved = (project: ProjectSummary & { reviews?: Review[] }) =>
  project.checklist.some((item) => item.key === "final_video_approved" && item.done)
  || Boolean(project.publish_approved_at || project.locales_decided_at || project.youtube_video_id)
  || (project.reviews ?? []).some((review) => review.gate === "final" && review.status === "approved");

export type PublishState = "deciding" | "making" | "ready" | "scheduled" | "published";
/**
 * Where the video is on its way to YouTube (docs/videos/LANGUAGES.md, the publish flow's five
 * states), or null before the final cut is approved and once the video is dropped: the owner has
 * still to choose its languages, the languages are in the making (so the upload can wait to be
 * scheduled), it may be uploaded, it is scheduled, or it is public. An older API knows only
 * "ready" and the two YouTube states.
 */
export function publishState(project: ProjectSummary, now = Date.now()): PublishState | null {
  if (project.dropped_at) return null;
  if (project.youtube_video_id) return project.youtube_publish_at && Date.parse(project.youtube_publish_at) > now ? "scheduled" : "published";
  if (!knowsLanguages(project)) return readyToUpload(project) ? "ready" : null;
  if (!finalApproved(project)) return null;
  if (!project.locales_decided_at) return "deciding";
  return project.ready_to_upload ? "ready" : "making";
}

/** Whether the store has let go of this video's mp4 (the same rule as the server's prune). */
export function mp4Retired(project: ProjectSummary, now = Date.now()): boolean {
  if (!project.youtube_video_id || !project.publish_approved_at) return false;
  const since = Math.max(Date.parse(project.publish_approved_at), project.youtube_publish_at ? Date.parse(project.youtube_publish_at) : 0);
  return Number.isFinite(since) && since + PREVIEW_RETENTION_MS <= now;
}

const YOUTUBE_ID = /^[A-Za-z0-9_-]{11}$/;
const YOUTUBE_HOSTS = new Set(["youtu.be", "youtube.com", "www.youtube.com", "m.youtube.com", "studio.youtube.com"]);
const YOUTUBE_PATH_KINDS = new Set(["shorts", "embed", "live", "video", "v"]);

/**
 * The eleven-character id in what the owner pasted, or null: youtu.be/<id>, watch?v=<id>,
 * shorts/<id>, Studio's video/<id>/edit or the bare id. The server (admin_service.youtube_video_id)
 * applies the same rule; this copy only tells the owner before they submit.
 */
export function youtubeVideoId(value: string): string | null {
  const trimmed = value.trim();
  if (YOUTUBE_ID.test(trimmed)) return trimmed;
  let parsed: URL;
  try {
    parsed = new URL(trimmed.includes("://") ? trimmed : `https://${trimmed}`);
  } catch {
    return null;
  }
  const host = parsed.hostname.toLowerCase();
  if ((parsed.protocol !== "https:" && parsed.protocol !== "http:") || !YOUTUBE_HOSTS.has(host)) return null;
  const parts = parsed.pathname.split("/").filter(Boolean);
  let candidate: string | null = null;
  if (host === "youtu.be") candidate = parts[0] ?? null;
  else if (parts[0] === "watch") candidate = parsed.searchParams.get("v");
  else if (parts.length >= 2 && YOUTUBE_PATH_KINDS.has(parts[0])) candidate = parts[1];
  return candidate && YOUTUBE_ID.test(candidate) ? candidate : null;
}

const sizeOf = (bytes: number) => (bytes >= 1_000_000 ? `${(bytes / 1_000_000).toFixed(1)} MB` : `${Math.max(1, Math.round(bytes / 1000))} KB`);

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

/** A probability against its threshold: green on the passing side, red on the other. */
function Score({ value, passes }: { value: number | null; passes: (value: number) => boolean }) {
  if (value === null) return <span className="text-[var(--muted)]">—</span>;
  return <AdminStatusPill status={passes(value) ? "ok" : "failed"}>{value.toFixed(2)}</AdminStatusPill>;
}

/**
 * Why Jev chose an outline (docs/videos/HANDS-OFF.md, the section on Jev picking it). payload.pick is
 * { choice, probabilities: { key: p }, options: { key: { stance, demo } }, advice }; a pending
 * review may carry a pick that did not clear the thresholds, and shows the same table.
 */
function PickTable({ review }: { review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const pick = record(review.payload.pick);
  const scores = record(pick.options);
  const probabilities = record(pick.probabilities);
  const listed = list(review.payload.options).map(record).map((option) => text(option.key)).filter(Boolean);
  const keys = [...listed, ...Object.keys(scores).filter((key) => !listed.includes(key))];
  const choice = text(pick.choice);
  const advice = number(pick.advice);
  if (keys.length === 0 && !choice && advice === null) return null;
  const chosen = record(scores[choice]);
  const passed = (number(chosen.stance) ?? 0) >= PICK_MIN_STANCE && (number(chosen.demo) ?? 0) >= PICK_MIN_DEMO && advice !== null && advice <= PICK_MAX_ADVICE;
  return <div className="grid gap-3 rounded-2xl border border-[var(--line)] p-4" aria-label={t("pickReasons")}>
    <p className="font-bold">{t("pickReasons")}</p>
    <table className="w-full text-sm">
      <thead><tr className="text-left text-xs text-[var(--muted)]"><th className="py-1 pr-3 font-semibold">{t("pickOption")}</th><th className="py-1 pr-3 font-semibold">{t("pickProbability")}</th><th className="py-1 pr-3 font-semibold">{t("pickStance")}</th><th className="py-1 font-semibold">{t("pickDemo")}</th></tr></thead>
      <tbody>{keys.map((key) => {
        const score = record(scores[key]);
        const probability = number(probabilities[key]);
        return <tr key={key} className={key === choice ? "font-bold" : ""}>
          <td className="py-1 pr-3">{t("option", { key })}{key === choice && <span className="ml-2 text-xs text-[var(--teal)]">{t("pickChosen")}</span>}</td>
          <td className="py-1 pr-3 font-mono">{probability === null ? "—" : probability.toFixed(2)}</td>
          <td className="py-1 pr-3"><Score value={number(score.stance)} passes={(value) => value >= PICK_MIN_STANCE} /></td>
          <td className="py-1"><Score value={number(score.demo)} passes={(value) => value >= PICK_MIN_DEMO} /></td>
        </tr>;
      })}</tbody>
    </table>
    <p className="flex flex-wrap items-center gap-2 text-sm"><span>{t("pickAdvice")}</span><Score value={advice} passes={(value) => value <= PICK_MAX_ADVICE} /></p>
    <p className="text-xs text-[var(--muted)]">{t("pickThresholds", { min: PICK_MIN_STANCE, max: PICK_MAX_ADVICE })}</p>
    {review.status === "pending" && !passed && <p className="text-sm text-amber-800">{t("pickBelow")}</p>}
  </div>;
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
    <PickTable review={review} />
    {brief && <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("brief")}</summary><div className="mt-3 max-h-[32rem] overflow-y-auto whitespace-pre-wrap text-sm leading-7">{brief}</div></details>}
  </div>;
}

const COVERAGE_KEYS = ["hook", "conflict", "turn", "cliffhanger"] as const;
// The checker's verdicts are Chinese words (delivered, weak, missing): the tones go by code point.
const coverageTone: Record<string, string> = { "\u6709": "ok", "\u5f31": "warning", "\u7121": "failed" };
const beatOf = (beats: Record<string, unknown>, key: string) => {
  const value = beats[key];
  return value && typeof value === "object" && !Array.isArray(value) ? text((value as Record<string, unknown>).text) : text(value);
};

/**
 * The script gate (docs/videos/SERIES.md): the checker's coverage of the episode's beats and what
 * jars come first, then every scene's lines with their speakers, and a shot's prompt beside them.
 */
function ScriptBody({ review }: { review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const coverage = record(review.payload.coverage);
  const problems = list(review.payload.continuity_problems).map(text).filter(Boolean);
  const beats = record(review.payload.beats);
  const scenes = list(review.payload.scenes).map(record);
  const minutes = review.payload.minutes;
  // A chapter heading where the chapter changes, so the scenes read as acts.
  const headings = scenes.map((scene, index) => (text(scene.chapter) && text(scene.chapter) !== text(scenes[index - 1]?.chapter) ? text(scene.chapter) : ""));
  return <div className="grid gap-4">
    {Object.keys(coverage).length > 0 && <p className="flex flex-wrap items-center gap-2 text-sm"><strong>{t("scriptCoverage")}</strong>{COVERAGE_KEYS.map((key) => <span key={key} className="flex items-center gap-1">{t(`scriptBeats.${key}`)}<AdminStatusPill status={coverageTone[text(coverage[key])] ?? "inactive"}>{text(coverage[key]) || "—"}</AdminStatusPill></span>)}</p>}
    {problems.length > 0 && <ul className="grid gap-1 rounded-xl bg-[var(--paper)] p-3 text-sm leading-6" aria-label={t("scriptProblems")}>{problems.map((problem) => <li key={problem}>• {problem}</li>)}</ul>}
    {Object.keys(beats).length > 0 && <dl className="grid gap-1 text-sm md:grid-cols-2">{COVERAGE_KEYS.map((key) => beatOf(beats, key) && <div key={key}><dt className="inline font-semibold">{t(`scriptBeats.${key}`)}</dt><dd className="inline"> · {beatOf(beats, key)}</dd></div>)}</dl>}
    {typeof minutes === "number" && <p className="text-sm text-[var(--muted)]">{t("scriptMinutes", { minutes })}</p>}
    <ol className="grid gap-3">{scenes.map((scene, index) => {
      return <li key={text(scene.id) || index} className="grid gap-1 rounded-2xl border border-[var(--line)] p-3">
        {headings[index] && <span className="text-sm font-bold text-[var(--teal)]">{headings[index]}</span>}
        <span className="text-xs text-[var(--muted)]">{index + 1}. {text(scene.id)}{text(scene.template) && text(scene.template) !== "shot" ? ` · ${text(scene.template)}` : ""}</span>
        {list(scene.lines).map(record).map((line) => <span key={text(line.id)} className="leading-7">{text(line.name) ? <strong>【{text(line.name)}】</strong> : <span className="text-[var(--muted)]">{t("narrator")}：</span>}{text(line.emotion) && <span className="text-xs text-[var(--muted)]">（{text(line.emotion)}）</span>}{text(line.text)}</span>)}
        {text(scene.prompt) && <details><summary className="cursor-pointer text-xs text-[var(--muted)]">{t("scriptPrompt")}</summary><p className="mt-1 text-xs leading-5 text-[var(--muted)]">{text(scene.prompt)}</p></details>}
      </li>;
    })}</ol>
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

/**
 * A check report as the worker sends it (docs/videos/HANDS-OFF.md, the automatic quality check): a final review's
 * payload.qa over the eleven ids assemble, render, narration, pace, captions, metadata, facts,
 * links, thumbnail, policy, disclosure, and a publish review's payload.package over files,
 * descriptions, captions, disclosure. Shape: { ok, final_sha256, items: [{ id, ok, detail,
 * warnings? }] }. The failed items come first with their detail; warnings sit under their item.
 */
export function CheckItems({ report, title }: { report: unknown; title: string }) {
  const t = useTranslations("admin.videoReviews");
  const items = list(record(report).items).map(record).filter((item) => text(item.id));
  if (items.length === 0) return null;
  const failed = items.filter((item) => item.ok !== true);
  const passed = items.filter((item) => item.ok === true);
  const label = (id: string) => (t.has(`qaItems.${id}`) ? t(`qaItems.${id}`) : id);
  return <div className="grid gap-2" aria-label={title}>
    <p className="flex flex-wrap items-center gap-2 font-bold">{title}<AdminStatusPill status={failed.length ? "failed" : "ok"}>{failed.length ? t("qaFailedCount", { count: failed.length }) : t("qaAllPassed", { count: items.length })}</AdminStatusPill></p>
    <ul className="grid gap-1 text-sm leading-6">{[...failed, ...passed].map((item) => {
      const id = text(item.id);
      const ok = item.ok === true;
      const warnings = list(item.warnings).map(text).filter(Boolean);
      return <li key={id} className={ok ? "" : "rounded-xl bg-red-50 p-2 text-red-900"}>
        <span className="flex items-start gap-2">
          {ok ? <CheckCircle2 aria-hidden size={16} className="mt-1 shrink-0 text-[var(--teal)]" /> : <XCircle aria-hidden size={16} className="mt-1 shrink-0" />}
          <span><strong>{label(id)}</strong>{text(item.detail) && <span className={ok ? "text-[var(--muted)]" : ""}> · {text(item.detail)}</span>}</span>
        </span>
        {warnings.length > 0 && <ul className="ml-6 grid gap-0.5 text-amber-800">{warnings.map((warning) => <li key={warning}>{t("qaWarning")}{warning}</li>)}</ul>}
      </li>;
    })}</ul>
  </div>;
}

/** Text to paste into Studio, with a copy button; when the clipboard is refused the text is selected for Ctrl+C. */
function CopyField({ label, value, rows }: { label: string; value: string; rows: number }) {
  const t = useTranslations("admin.videoReviews");
  const field = useRef<HTMLTextAreaElement>(null);
  const [status, setStatus] = useState<"idle" | "copied" | "failed">("idle");
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(value);
      setStatus("copied");
    } catch {
      field.current?.focus();
      field.current?.select();
      setStatus("failed");
    }
  };
  return <div className="grid gap-1">
    <label className="grid gap-1 text-sm font-semibold">{label}<textarea ref={field} readOnly rows={rows} value={value} className={`${control} text-sm font-normal`} onFocus={(event) => event.currentTarget.select()} /></label>
    <div className="flex flex-wrap items-center gap-3">
      <Button secondary onClick={() => void copy()} aria-label={`${t("copy")} ${label}`}><Copy aria-hidden size={16} />{status === "copied" ? t("copied") : t("copy")}</Button>
      {status === "failed" && <span role="status" className="text-sm text-amber-800">{t("copyFailed")}</span>}
    </div>
  </div>;
}

/**
 * The upload package a publish (upload confirmation) review carries, for the owner to download and
 * paste into Studio (docs/videos/HANDS-OFF.md, the upload package section). Contract with the worker
 * (tools/video, ticket 2026-09-26-video-hands-off-worker); every field may be missing from an
 * older tool, and the card renders what is there:
 *   payload.package    { ok, final_sha256, items: [{ id: files | descriptions | captions | disclosure, ok, detail, warnings? }] }
 *   payload.minutes    number     the video's length in minutes
 *   payload.chapters   number     how many chapters
 *   payload.locales    string[]   the locales that have captions and a description, e.g. ["zh-TW", "zh-CN", "en", "ja", "ko"]
 *   payload.zh         { title, description, tags: string[] }   the zh-TW metadata the owner pastes
 *   payload.disclosure { synthetic: boolean, reason: string }   whether to tick Studio's "altered or synthetic content"
 *   files[]            { role, sha256, size, content_type } with the roles
 *                        final                 final.mp4                 video/mp4
 *                        thumbnail             thumbnail.jpg             image/jpeg
 *                        captions_<locale>     captions/<locale>.srt     text/plain (application/x-subrip and text/vtt also accepted)
 *                        description_<locale>  description.<locale>.txt  text/plain
 *                        metadata              metadata.json             application/json
 *                      where <locale> is the locale as listed (captions_zh-TW; a role is [a-z][A-Za-z0-9_-]*).
 *                      payload.checklist, the older free-text list, is empty from this worker on.
 *                      Downloads go through /api/admin-video-files/<slug>/<sha256>.
 */
export function UploadPackage({ slug, review, mp4Gone = false }: { slug: string; review: Review; mp4Gone?: boolean }) {
  const t = useTranslations("admin.videoReviews");
  const payload = review.payload;
  const minutes = number(payload.minutes);
  const chapters = number(payload.chapters);
  const locales = list(payload.locales).map(text).filter(Boolean);
  const zh = record(payload.zh);
  const tags = list(zh.tags).map(text).filter(Boolean);
  const disclosure = record(payload.disclosure);
  // The worker names a locale's files with the locale as is (captions_zh-TW); an older spelling
  // lower-cased it with "_" (captions_zh_tw), so both map back to the listed locale.
  const flat = (value: string) => value.toLowerCase().replace(/-/g, "_");
  const localeOf = (role: string, prefix: string) => {
    const suffix = role.slice(prefix.length);
    return locales.find((locale) => flat(locale) === flat(suffix)) ?? suffix;
  };
  const downloads = review.files.flatMap((file) => {
    if (file.role === "final") return mp4Gone ? [] : [{ file, label: t("downloadFinal"), name: "final.mp4" }];
    if (file.role === "thumbnail") return [{ file, label: t("downloadThumbnail"), name: "thumbnail.jpg" }];
    if (file.role.startsWith("captions_")) {
      const locale = localeOf(file.role, "captions_");
      return [{ file, label: t("downloadCaptions", { locale }), name: `${locale}.${file.content_type === "text/vtt" ? "vtt" : "srt"}` }];
    }
    if (file.role.startsWith("description_")) {
      const locale = localeOf(file.role, "description_");
      return [{ file, label: t("downloadDescription", { locale }), name: `description.${locale}.txt` }];
    }
    if (file.role === "metadata") return [{ file, label: t("downloadMetadata"), name: "metadata.json" }];
    return [];
  });
  const facts = [minutes !== null && t("minutes", { minutes }), chapters !== null && t("packageChapters", { count: chapters }), locales.length > 0 && t("packageLocales", { count: locales.length })].filter(Boolean);
  const hasText = Boolean(text(zh.title) || text(zh.description) || tags.length > 0);
  if (facts.length === 0 && downloads.length === 0 && !mp4Gone && !hasText && typeof disclosure.synthetic !== "boolean") return null;
  return <div className="grid gap-4" aria-label={t("uploadPackage")}>
    {facts.length > 0 && <p className="text-sm text-[var(--muted)]">{facts.join(" · ")}</p>}
    {(downloads.length > 0 || mp4Gone) && <div>
      <p className="font-bold">{t("downloads")}</p>
      {mp4Gone && <p className="mt-1 text-sm leading-6 text-[var(--muted)]">{t("mp4Retired")}</p>}
      <ul className="mt-2 flex flex-wrap gap-2">{downloads.map(({ file, label, name }) => <li key={file.sha256}>
        <a href={fileUrl(slug, file)} download={name} className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 text-sm font-semibold hover:border-[var(--teal)]"><Download aria-hidden size={16} />{label}<span className="text-xs font-normal text-[var(--muted)]">{sizeOf(file.size)}</span></a>
      </li>)}</ul>
    </div>}
    {hasText && <div className="grid gap-3">
      {text(zh.title) && <CopyField label={t("zhTitle")} value={text(zh.title)} rows={1} />}
      {text(zh.description) && <CopyField label={t("zhDescription")} value={text(zh.description)} rows={6} />}
      {tags.length > 0 && <CopyField label={t("zhTags")} value={tags.join(", ")} rows={2} />}
    </div>}
    {typeof disclosure.synthetic === "boolean" && <p className="text-sm leading-6">
      <strong>{t("disclosureTitle")}</strong>{" "}
      <AdminStatusPill status={disclosure.synthetic ? "warning" : "ok"}>{disclosure.synthetic ? t("disclosureYes") : t("disclosureNo")}</AdminStatusPill>
      {text(disclosure.reason) && <span className="block text-[var(--muted)]">{text(disclosure.reason)}</span>}
    </p>}
  </div>;
}

/**
 * The owner uploaded the final cut in Studio (private, nothing else filled in): the pasted address
 * and the optional publish time go to POST /admin/videos/{slug}/youtube, which records the id and
 * when it goes public (docs/videos/HANDS-OFF.md, the YouTube API section, step one).
 */
export function UploadedForm({ slug, onLinked }: { slug: string; onLinked: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [url, setUrl] = useState("");
  const [publishAt, setPublishAt] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const id = youtubeVideoId(url);
  const submit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    if (!id) return;
    setBusy(true);
    setError("");
    try {
      // A datetime-local value is the owner's wall clock; the API wants a zoned instant.
      await api(`/admin/videos/${slug}/youtube`, { method: "POST", body: JSON.stringify({ url: url.trim(), publish_at: publishAt ? new Date(publishAt).toISOString() : null }) });
      onLinked();
    } catch (problem) {
      setError(t("uploadedError", { message: problem instanceof Error ? problem.message : "" }));
    } finally {
      setBusy(false);
    }
  };
  return <form onSubmit={(event) => void submit(event)} className="grid gap-3 rounded-2xl border border-[var(--line)] p-4" aria-label={t("uploadedTitle")}>
    <p className="font-bold">{t("uploadedTitle")}</p>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("uploadedHelp")}</p>
    <label className="grid gap-2 text-sm font-semibold">{t("youtubeUrl")}
      <input className={control} value={url} disabled={busy} placeholder={t("youtubeUrlPlaceholder")} onChange={(event) => setUrl(event.target.value)} />
    </label>
    {url.trim() && <p className={`text-sm ${id ? "text-[var(--muted)]" : "text-amber-800"}`}>{id ? t("youtubeId", { id }) : t("youtubeUrlInvalid")}</p>}
    <label className="grid gap-2 text-sm font-semibold">{t("publishAt")}
      <input type="datetime-local" className={control} value={publishAt} disabled={busy} onChange={(event) => setPublishAt(event.target.value)} />
    </label>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <div><Button type="submit" disabled={busy || !id}>{busy ? t("saving") : t("uploadedButton")}</Button></div>
  </form>;
}

function FinalBody({ slug, review, mp4Gone }: { slug: string; review: Review; mp4Gone: boolean }) {
  const t = useTranslations("admin.videoReviews");
  const checks = record(review.payload.checks);
  const problems = list(checks.problems).map(text).filter(Boolean);
  const chapters = list(review.payload.chapters).map(record);
  const metadata = Object.entries(record(review.payload.metadata)).map(([locale, value]) => [locale, record(value)] as const);
  const video = mp4Gone ? undefined : fileUrl(slug, fileFor(review, "preview"));
  const sheet = fileUrl(slug, fileFor(review, "contact_sheet"));
  const poster = fileUrl(slug, fileFor(review, "thumbnail"));
  return <div className="grid gap-4">
    {video && <label className="grid gap-2 font-bold">{t("preview")}<video controls preload="metadata" src={video} poster={poster} className="aspect-video w-full rounded-xl bg-black" /></label>}
    <CheckItems report={review.payload.qa} title={t("qaTitle")} />
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

function PublishBody({ slug, review, mp4Gone }: { slug: string; review: Review; mp4Gone: boolean }) {
  const t = useTranslations("admin.videoReviews");
  const items = list(review.payload.checklist).map(text).filter(Boolean);
  return <div className="grid gap-4">
    <CheckItems report={review.payload.package} title={t("packageTitle")} />
    <UploadPackage slug={slug} review={review} mp4Gone={mp4Gone} />
    {items.length > 0 && <div><p className="font-bold">{t("uploadChecklist")}</p><ul className="mt-2 grid gap-1 text-sm leading-6">{items.map((item) => <li key={item}>• {item}</li>)}</ul></div>}
  </div>;
}

// The file a languages review carries for each part of a language, by role prefix (docs/videos/LANGUAGES.md).
const PART_ROLES: Record<LocalePart, string> = { metadata: "description_", captions: "captions_", dub: "dub_" };

/** A part's state label, for the review card and the language panel: the known four, or the word as sent. */
export function partStateLabel(t: ReturnType<typeof useTranslations>, state: string, reason?: string | null): string {
  if (state === "skipped") return reason ? t("partSkipped", { reason }) : t("partStates.skipped");
  return state === "working" || state === "ready" || state === "uploaded" ? t(`partStates.${state}`) : state;
}

/**
 * A batch of languages the worker finished (docs/videos/LANGUAGES.md): for every language, where
 * each chosen part stands (titles and descriptions, captions, dub track), the reason when one was
 * given up on, and the file to download; when a dub track is ready, the steps on YouTube Studio's
 * Languages page (docs/videos/DUBS.md, what the owner does), since only the owner can upload it. An
 * older dubs review, one track per language with its status at the top level, reads the same way.
 */
function LanguagesBody({ slug, review }: { slug: string; review: Review }) {
  const t = useTranslations("admin.videoReviews");
  const reported = record(review.payload.locales);
  const known: readonly string[] = LOCALES;
  const locales = [...LOCALES.filter((locale) => locale in reported), ...Object.keys(reported).filter((locale) => !known.includes(locale))];
  if (!locales.length) return null;
  const rows = locales.map((locale) => {
    const entry = record(reported[locale]);
    const fallback = text(entry.reason);
    const parts: Record<string, unknown> = review.gate === "dubs" ? { dub: text(entry.status) } : entry;
    const cells = LOCALE_PARTS.flatMap((part) => {
      if (!(part in parts)) return [];
      const value = parts[part];
      const state = typeof value === "string" ? value : text(record(value).status);
      const reason = state === "skipped" ? text(record(value).reason) || fallback : "";
      const file = fileFor(review, `${PART_ROLES[part]}${locale}`) ?? (part === "dub" ? fileFor(review, text(entry.file_role)) : undefined);
      const name = part === "dub" ? text(entry.file) || `${locale}.${text(entry.format) || "m4a"}` : part === "captions" ? `${locale}.srt` : `description.${locale}.txt`;
      return [{ part, state, reason, file, name }];
    });
    return { locale, cells };
  });
  const dubReady = rows.some(({ cells }) => cells.some((cell) => cell.part === "dub" && cell.state === "ready"));
  return <div className="grid gap-4 text-sm leading-6">
    <ul className="grid gap-2">{rows.map(({ locale, cells }) => <li key={locale} className="grid gap-1 sm:grid-cols-[7rem_1fr]">
      <span className="font-semibold">{t.has(`locales.${locale}`) ? t(`locales.${locale}`) : locale}</span>
      <span className="flex flex-wrap gap-x-5 gap-y-1">{cells.map(({ part, state, reason, file, name }) => <span key={part} className="inline-flex flex-wrap items-center gap-2">
        <span>{t(`parts.${part}`)}</span>
        <span className="text-[var(--muted)]">{partStateLabel(t, state, reason)}</span>
        {file && <a className="font-semibold text-[var(--teal)] underline" href={fileUrl(slug, file)} download={name}>{t("downloadTrack", { file: name })}</a>}
      </span>)}</span>
    </li>)}</ul>
    {dubReady && <div className="rounded-2xl border border-[var(--line)] p-4">
      <p className="font-bold">{t("studioTitle")}</p>
      <p className="mt-1 text-[var(--muted)]">{t("studioNote")}</p>
      <ol className="mt-2 grid list-decimal gap-1 pl-5">{(["studioStep1", "studioStep2", "studioStep3"] as const).map((step) => <li key={step}>{t(step)}</li>)}</ol>
    </div>}
  </div>;
}

/** One review of one gate: its body, and the owner's approve or reject with a note. */
export function ReviewCard({ slug, review, canManage, onDecided, mp4Gone = false }: { slug: string; review: Review; canManage: boolean; onDecided: () => void; mp4Gone?: boolean }) {
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
  const approveLabels: Partial<Record<Gate, string>> = { outline: t("approveOutline"), script: t("approveScript"), look: t("approveLook"), storyboard: t("approveStoryboard"), publish: t("approvePublish"), languages: t("approveLanguages"), dubs: t("approveDubs") };
  const approveLabel = approveLabels[review.gate] ?? t("approve");
  const title = review.gate === "look" && text(record(review.payload.character).name) ? `${t("gates.look")}：${text(record(review.payload.character).name)}` : t(`gates.${review.gate}`);
  return <article className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" aria-label={title}>
    <header className="flex flex-wrap items-center gap-3">
      <h3 className="text-lg font-bold">{title}</h3>
      <AdminStatusPill status={statusTone[review.status]}>{t(`statuses.${review.status}`)}</AdminStatusPill>
      {jevPicked(review) && <AdminStatusPill status="active">{t("jevPicked")}</AdminStatusPill>}
      <span className="text-sm text-[var(--muted)]">{t("submittedAt", { time: when(review.created_at) })}</span>
    </header>
    <p className="mt-2 leading-7">{review.summary}</p>
    <div className="mt-4">
      {review.gate === "outline" && <OutlineBody review={review} choice={choice} onChoice={setChoice} disabled={!canManage || busy} />}
      {review.gate === "script" && <ScriptBody review={review} />}
      {review.gate === "look" && <LookBody slug={slug} review={review} choice={choice} onChoice={setChoice} disabled={!canManage || busy} />}
      {review.gate === "storyboard" && <StoryboardBody slug={slug} review={review} />}
      {review.gate === "audio" && <AudioBody slug={slug} review={review} />}
      {review.gate === "final" && <FinalBody slug={slug} review={review} mp4Gone={mp4Gone} />}
      {review.gate === "publish" && <PublishBody slug={slug} review={review} mp4Gone={mp4Gone} />}
      {(review.gate === "languages" || review.gate === "dubs") && <LanguagesBody slug={slug} review={review} />}
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
