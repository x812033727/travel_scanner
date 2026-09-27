"use client";

import { ArrowLeft, BookOpen } from "lucide-react";
import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminEmptyState, AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { AdminVideoDramaSettings } from "@/components/admin-video-drama-settings";
import { CompilationDownload, control, isBlocked, list, needsOwner, type ProjectSummary, record, text, useRefresh, useWhen } from "@/components/admin-video-review-card";
import type { VideoSettingsView } from "@/components/admin-video-settings";
import { Button } from "@/components/community/ui";
import { useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// The drama tab of /admin/videos (docs/videos/SERIES.md): a long series is planned document by
// document (the setting book, the whole-series outline, each chapter's detailed outline), each
// approved here, and made episode by episode; every episode is a video of its own with the usual
// review cards, reached from the episode table. One-off episodes (a premise, not a series) are
// filed and queued here too.
type SeriesStatus = "setting" | "outline" | "active" | "paused" | "finished";
type DocKind = "setting" | "outline" | "chapter";
type DocStatus = "generating" | "review" | "approved" | "rejected";
type EpisodeStatus = "planned" | "ready" | "queued" | "started" | "done" | "skipped";
type SeriesDoc = { id: string; kind: DocKind; chapter_number: number; version: number; body_md: string; body_json: Record<string, unknown>; status: DocStatus; note: string | null; decided_at: string | null; created_at: string };
type SeriesEpisode = {
  number: number; chapter_number: number; title: string; logline: string; beats: Record<string, unknown>; status: EpisodeStatus; slug: string | null;
  recap: string | null; started_at: string | null; finished_at: string | null; video: ProjectSummary | null;
};
// A binge series (docs/videos/BINGE.md): a genre preset the planner writes from, who leads, and
// how much of the picture is paid clips; hands_off lets the checker approve the documents, and
// compilation joins the finished episodes into one cut the owner downloads from the series page.
type SeriesGenre = "xianxia-bonds" | "rebirth-revenge" | "system-game" | "urban-return" | "empress-rise" | "custom";
type SeriesLead = "female" | "male" | "dual-male";
type VisualTier = "clips" | "hybrid" | "stills";
type SeriesSummary = {
  id: string; slug: string; title: string; premise: string; aspects: string[]; tone: string; style_preset: string; target_minutes: number;
  planned_episodes: number; episodes_per_chapter: number; chapters: number; open_ended: boolean; status: SeriesStatus; note: string | null;
  requested_chapter: number | null; force_next: boolean; episodes_done: number; episodes_started: number; episodes_ready: number; docs_pending: number;
  media_usd: number; clip_seconds: number; created_at: string; updated_at: string;
  // The binge columns; absent from an API older than this page, which reads as the classic series.
  genre?: SeriesGenre; lead?: SeriesLead; hands_off?: boolean; compilation?: boolean; visual_tier?: VisualTier; total_minutes?: number | null;
  compilation_slug?: string | null; compilation_started_at?: string | null; compilation_finished_at?: string | null;
};
// What one binge series would take, from GET series/binge-quote: the shape the server derives from
// the minutes, the media at the settings' prices, and each monthly budget it has to fit in.
type BudgetLine = { needed: number; monthly: number; ok: boolean };
type BingeQuote = { episodes: number; chapters: number; episodes_per_chapter: number; clip_seconds: number; images: number; judge_calls: number; usd: number; budgets: Record<string, BudgetLine>; ok: boolean };
type Series = SeriesSummary & { docs: SeriesDoc[]; episodes: SeriesEpisode[] };
type RequestStatus = "queued" | "started" | "done" | "cancelled";
type DramaRequest = {
  id: string; premise: string; title: string | null; source_guide: string | null; style_preset: string; target_minutes: number;
  note: string | null; status: RequestStatus; slug: string | null; created_at: string; started_at: string | null; finished_at: string | null; cancelled_at: string | null;
};

export const SERIES_SLUG = /^[a-z0-9][a-z0-9-]{1,39}$/;
const ASPECTS = ["world", "bonds", "structure", "mood"] as const;
const TONES = ["dual-male-leads-subtext", "dual-male-leads-explicit", "hetero-leads", "no-romance"] as const;
const PRESETS = ["cinematic-3d", "anime-2d", "ink-wash", "custom"] as const;
const GUIDE_SLUG = /^[a-z0-9][a-z0-9-]{0,118}[a-z0-9]$/;
const GENRES: readonly SeriesGenre[] = ["xianxia-bonds", "rebirth-revenge", "system-game", "urban-return", "empress-rise", "custom"];
const LEADS: readonly SeriesLead[] = ["female", "male", "dual-male"];
const TIERS: readonly VisualTier[] = ["clips", "hybrid", "stills"];
const BUDGETS = ["clip_seconds", "images", "judge_calls", "episodes_per_month"] as const;
// The API's bounds on a binge run (SeriesIn.total_minutes); the episode length is narrower than the
// classic form's 1–8 because the compilation's rhythm is written for two-to-four-minute episodes.
const BINGE_MINUTES = { min: 30, max: 480 } as const;
const EPISODE_MINUTES = { min: 2, max: 4 } as const;
// How long the form waits after a change before asking for a new quote, so a number being typed
// digit by digit costs one request, not one per digit.
const QUOTE_DEBOUNCE_MS = 300;
const seriesTone: Record<SeriesStatus, string> = { setting: "pending", outline: "pending", active: "active", paused: "inactive", finished: "inactive" };
const docTone: Record<DocStatus, string> = { generating: "running", review: "pending", approved: "active", rejected: "failed" };
const episodeTone: Record<EpisodeStatus, string> = { planned: "inactive", ready: "queued", queued: "queued", started: "active", done: "ok", skipped: "inactive" };
const requestTone: Record<RequestStatus, string> = { queued: "pending", started: "active", done: "inactive", cancelled: "inactive" };
const message = (problem: unknown) => (problem instanceof Error ? problem.message : "");
// Where a series' compilation stands, from the summary's compilation columns: not asked for, waiting
// for the episodes, waiting for the worker to pick it up, being cut, or cleared for upload.
type CompilationState = "none" | "waiting" | "queued" | "making" | "done";
function compilationState(series: SeriesSummary): CompilationState {
  if (series.compilation_finished_at) return "done";
  if (series.compilation_slug) return "making";
  if (!series.compilation) return "none";
  return series.status === "finished" ? "queued" : "waiting";
}
const compilationTone: Record<CompilationState, string> = { none: "inactive", waiting: "pending", queued: "queued", making: "running", done: "ok" };
const docPath = (slug: string, doc: SeriesDoc) => `/admin/video-automation/series/${slug}/docs/${doc.kind}${doc.kind === "chapter" ? `/${doc.chapter_number}` : ""}`;

/** The server's quote for the binge form: the shape, the media, the money, and every budget line, the overrun ones red. */
function BingeQuoteView({ quote, error, pending }: { quote: BingeQuote | null; error: string; pending: boolean }) {
  const t = useTranslations("admin.videoSeries");
  return <section aria-label={t("binge.quoteTitle")} className="grid gap-2 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6">
    <p className="font-bold">{t("binge.quoteTitle")}</p>
    {pending && <p className="text-[var(--muted)]">{t("binge.quoteLoading")}</p>}
    {error && <p className="text-red-800">{t("binge.quoteError", { message: error })}</p>}
    {quote && <>
      <p>{t("binge.quote", { episodes: quote.episodes, chapters: quote.chapters, perChapter: quote.episodes_per_chapter, seconds: quote.clip_seconds, images: quote.images, usd: Number(quote.usd ?? 0).toFixed(2) })}</p>
      <ul className="grid gap-1">{BUDGETS.map((key) => {
        const line = quote.budgets?.[key];
        if (!line) return null;
        return <li key={key} className={line.ok ? "text-[var(--muted)]" : "font-semibold text-red-800"}>{t(`binge.${line.ok ? "budgets" : "budgetsOver"}.${key}`, { needed: line.needed, monthly: line.monthly })}</li>;
      })}</ul>
      {!quote.ok && <p className="text-[var(--muted)]">{t("binge.overBudget")}</p>}
    </>}
  </section>;
}

/**
 * The one-button binge form (docs/videos/BINGE.md): a genre, a lead, the total minutes and the
 * visual tier; the server derives the episode count and the chapter size, names the series after
 * the genre until the setting book names it, and the checker approves the documents. The quote is
 * read from the server as the numbers change; a budget it would overrun is a warning, not a stop,
 * since the worker stalls at a spent budget and continues once it is raised on the settings tab.
 */
function NewBingeForm({ onCreated }: { onCreated: (slug: string) => void }) {
  const t = useTranslations("admin.videoSeries");
  const [genre, setGenre] = useState<SeriesGenre>("xianxia-bonds");
  const [lead, setLead] = useState<SeriesLead>("dual-male");
  const [premise, setPremise] = useState("");
  const [totalMinutes, setTotalMinutes] = useState(120);
  const [episodeMinutes, setEpisodeMinutes] = useState(3);
  const [tier, setTier] = useState<VisualTier>("hybrid");
  const [preset, setPreset] = useState<(typeof PRESETS)[number]>("cinematic-3d");
  const [note, setNote] = useState("");
  // The last quote read, with the request it answers: only the answer to the numbers on the form
  // is shown, so a change never displays the previous shape while the new one is on its way.
  const [answer, setAnswer] = useState<{ url: string; quote: BingeQuote | null; error: string } | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const minutesOk = Number.isInteger(totalMinutes) && totalMinutes >= BINGE_MINUTES.min && totalMinutes <= BINGE_MINUTES.max;
  const episodeOk = Number.isInteger(episodeMinutes) && episodeMinutes >= EPISODE_MINUTES.min && episodeMinutes <= EPISODE_MINUTES.max;
  const premiseOk = genre !== "custom" || Boolean(premise.trim());
  const quoteUrl = minutesOk && episodeOk ? `/admin/video-automation/series/binge-quote?total_minutes=${totalMinutes}&episode_minutes=${episodeMinutes}&visual_tier=${tier}` : "";
  useEffect(() => {
    if (!quoteUrl) return;
    let current = true;
    const timer = setTimeout(() => {
      api<BingeQuote>(quoteUrl)
        .then((value) => { if (current) setAnswer({ url: quoteUrl, quote: value, error: "" }); })
        .catch((problem: unknown) => { if (current) setAnswer({ url: quoteUrl, quote: null, error: message(problem) }); });
    }, QUOTE_DEBOUNCE_MS);
    return () => { current = false; clearTimeout(timer); };
  }, [quoteUrl]);
  const shown = answer && answer.url === quoteUrl ? answer : null;
  const create = async () => {
    setBusy(true);
    setError("");
    try {
      const created = await api<Series>("/admin/video-automation/series", {
        method: "POST",
        body: JSON.stringify({
          genre, lead, premise: premise.trim() || undefined, total_minutes: totalMinutes, target_minutes: episodeMinutes, visual_tier: tier, style_preset: preset,
          hands_off: true, compilation: true, open_ended: false, note: note.trim() || undefined,
        }),
      });
      onCreated(created.slug);
    } catch (problem) {
      setError(t("binge.error", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const card = "flex cursor-pointer items-start gap-3 rounded-2xl border border-[var(--line)] p-3 has-[:checked]:border-[var(--teal)] has-[:checked]:bg-[var(--paper)]";
  return <details open className="rounded-[1.5rem] border border-[var(--teal)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="cursor-pointer text-lg font-bold">{t("binge.title")}</summary>
    <form className="mt-4 grid gap-4" onSubmit={(event) => { event.preventDefault(); void create(); }} aria-label={t("binge.title")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("binge.help")}</p>
      <fieldset className="grid gap-2"><legend className="text-sm font-semibold">{t("binge.genre")}</legend>
        <div className="grid gap-2 md:grid-cols-2">{GENRES.map((each) => <label key={each} className={card}>
          <input type="radio" name="binge-genre" className="mt-1" value={each} checked={genre === each} disabled={busy} onChange={() => setGenre(each)} />
          <span className="grid gap-1 text-sm"><span className="font-semibold">{t(`genres.${each}.name`)}</span><span className="text-[var(--muted)]">{t(`genres.${each}.detail`)}</span></span>
        </label>)}</div>
      </fieldset>
      <fieldset className="grid gap-2"><legend className="text-sm font-semibold">{t("binge.lead")}</legend>
        <div className="flex flex-wrap gap-5">{LEADS.map((each) => <label key={each} className="flex min-h-11 items-center gap-2 text-sm"><input type="radio" name="binge-lead" value={each} checked={lead === each} disabled={busy} onChange={() => setLead(each)} />{t(`leads.${each}`)}</label>)}</div>
      </fieldset>
      <label className="grid gap-2 text-sm font-semibold">{genre === "custom" ? t("binge.premiseRequired") : t("binge.premise")}
        <textarea className={control} rows={3} value={premise} disabled={busy} maxLength={4000} placeholder={t("binge.premisePlaceholder")} aria-invalid={!premiseOk} onChange={(event) => setPremise(event.target.value)} />
      </label>
      <div className="grid gap-3 md:grid-cols-3">
        <div className="grid gap-1">
          <label className="grid gap-2 text-sm font-semibold">{t("binge.totalMinutes")}<input className={control} type="number" min={BINGE_MINUTES.min} max={BINGE_MINUTES.max} value={totalMinutes} disabled={busy} aria-invalid={!minutesOk} onChange={(event) => setTotalMinutes(Number(event.target.value))} /></label>
          <span className="text-xs text-[var(--muted)]">{t("binge.totalMinutesHint")}</span>
        </div>
        <label className="grid gap-2 self-start text-sm font-semibold">{t("binge.episodeMinutes")}<input className={control} type="number" min={EPISODE_MINUTES.min} max={EPISODE_MINUTES.max} value={episodeMinutes} disabled={busy} aria-invalid={!episodeOk} onChange={(event) => setEpisodeMinutes(Number(event.target.value))} /></label>
        <label className="grid gap-2 self-start text-sm font-semibold">{t("fields.stylePreset")}
          <select className={control} value={preset} disabled={busy} onChange={(event) => setPreset(event.target.value as (typeof PRESETS)[number])}>{PRESETS.map((each) => <option key={each} value={each}>{t(`presets.${each}`)}</option>)}</select>
        </label>
      </div>
      <fieldset className="grid gap-2"><legend className="text-sm font-semibold">{t("binge.tier")}</legend>
        <div className="grid gap-2 md:grid-cols-3">{TIERS.map((each) => <label key={each} className={card}>
          <input type="radio" name="binge-tier" className="mt-1" value={each} checked={tier === each} disabled={busy} onChange={() => setTier(each)} />
          <span className="grid gap-1 text-sm"><span className="font-semibold">{t(`tiers.${each}.name`)}</span><span className="text-[var(--muted)]">{t(`tiers.${each}.detail`)}</span></span>
        </label>)}</div>
      </fieldset>
      <label className="grid gap-2 text-sm font-semibold">{t("fields.note")}<textarea className={control} rows={2} value={note} disabled={busy} maxLength={2000} placeholder={t("binge.notePlaceholder")} onChange={(event) => setNote(event.target.value)} /></label>
      <BingeQuoteView quote={shown?.quote ?? null} error={shown?.error ?? ""} pending={Boolean(quoteUrl) && !shown} />
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button type="submit" disabled={busy || !minutesOk || !episodeOk || !premiseOk}>{busy ? t("binge.starting") : t("binge.start")}</Button></div>
    </form>
  </details>;
}

/** The binge pills a series card and its page share: the genre, the tier, hands-off, and where the compilation stands. */
function BingePills({ series }: { series: SeriesSummary }) {
  const t = useTranslations("admin.videoSeries");
  const state = compilationState(series);
  return <>
    <AdminStatusPill status="inactive">{t(`genres.${series.genre ?? "xianxia-bonds"}.name`)}</AdminStatusPill>
    <AdminStatusPill status="inactive">{t(`tiers.${series.visual_tier ?? "clips"}.name`)}</AdminStatusPill>
    {series.hands_off && <AdminStatusPill status="active">{t("handsOff")}</AdminStatusPill>}
    {state !== "none" && <AdminStatusPill status={compilationTone[state]}>{t(`compilationStatuses.${state}`)}</AdminStatusPill>}
  </>;
}

/** Start a series: the premise and the shape; the worker plans the setting book from it. */
function NewSeriesForm({ onCreated }: { onCreated: (slug: string) => void }) {
  const t = useTranslations("admin.videoSeries");
  const [slug, setSlug] = useState("");
  const [title, setTitle] = useState("");
  const [premise, setPremise] = useState("");
  const [aspects, setAspects] = useState<string[]>([...ASPECTS]);
  const [tone, setTone] = useState<(typeof TONES)[number]>("dual-male-leads-subtext");
  const [preset, setPreset] = useState<(typeof PRESETS)[number]>("cinematic-3d");
  const [minutes, setMinutes] = useState(3);
  const [planned, setPlanned] = useState(100);
  const [perChapter, setPerChapter] = useState(10);
  const [openEnded, setOpenEnded] = useState(true);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const slugOk = SERIES_SLUG.test(slug.trim());
  const create = async () => {
    setBusy(true);
    setError("");
    try {
      const created = await api<Series>("/admin/video-automation/series", {
        method: "POST",
        body: JSON.stringify({ slug: slug.trim(), title: title.trim(), premise: premise.trim(), aspects, tone, style_preset: preset, target_minutes: minutes, planned_episodes: planned, episodes_per_chapter: perChapter, open_ended: openEnded, note: note.trim() || undefined }),
      });
      onCreated(created.slug);
    } catch (problem) {
      setError(t("createError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="cursor-pointer text-lg font-bold">{t("newSeries")}</summary>
    <form className="mt-4 grid gap-3" onSubmit={(event) => { event.preventDefault(); void create(); }} aria-label={t("newSeries")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("newSeriesHelp")}</p>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="grid gap-2 text-sm font-semibold">{t("fields.title")}<input className={control} value={title} disabled={busy} maxLength={200} onChange={(event) => setTitle(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.slug")}<input className={control} value={slug} disabled={busy} placeholder={t("slugPlaceholder")} aria-invalid={Boolean(slug) && !slugOk} onChange={(event) => setSlug(event.target.value)} /></label>
      </div>
      <label className="grid gap-2 text-sm font-semibold">{t("fields.premise")}
        <textarea className={control} rows={4} value={premise} disabled={busy} maxLength={4000} placeholder={t("premisePlaceholder")} onChange={(event) => setPremise(event.target.value)} />
      </label>
      <fieldset className="grid gap-2"><legend className="text-sm font-semibold">{t("fields.aspects")}</legend>
        <div className="grid gap-2 md:grid-cols-2">{ASPECTS.map((aspect) => <label key={aspect} className="flex min-h-11 items-center gap-2 text-sm"><input type="checkbox" checked={aspects.includes(aspect)} disabled={busy} onChange={(event) => setAspects(event.target.checked ? [...aspects, aspect] : aspects.filter((each) => each !== aspect))} />{t(`aspects.${aspect}`)}</label>)}</div>
      </fieldset>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="grid gap-2 text-sm font-semibold">{t("fields.tone")}
          <select className={control} value={tone} disabled={busy} onChange={(event) => setTone(event.target.value as (typeof TONES)[number])}>{TONES.map((each) => <option key={each} value={each}>{t(`tones.${each}`)}</option>)}</select>
        </label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.stylePreset")}
          <select className={control} value={preset} disabled={busy} onChange={(event) => setPreset(event.target.value as (typeof PRESETS)[number])}>{PRESETS.map((each) => <option key={each} value={each}>{t(`presets.${each}`)}</option>)}</select>
        </label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.targetMinutes")}<input className={control} type="number" min={1} max={8} value={minutes} disabled={busy} onChange={(event) => setMinutes(Number(event.target.value))} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.plannedEpisodes")}<input className={control} type="number" min={1} max={500} value={planned} disabled={busy} onChange={(event) => setPlanned(Number(event.target.value))} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("fields.episodesPerChapter")}<input className={control} type="number" min={4} max={20} value={perChapter} disabled={busy} onChange={(event) => setPerChapter(Number(event.target.value))} /></label>
        <label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={openEnded} disabled={busy} onChange={(event) => setOpenEnded(event.target.checked)} />{t("fields.openEnded")}</label>
      </div>
      <label className="grid gap-2 text-sm font-semibold">{t("fields.note")}<textarea className={control} rows={2} value={note} disabled={busy} maxLength={2000} placeholder={t("notePlaceholder")} onChange={(event) => setNote(event.target.value)} /></label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button type="submit" disabled={busy || !title.trim() || !premise.trim() || !slugOk || aspects.length === 0}>{busy ? t("saving") : t("create")}</Button></div>
    </form>
  </details>;
}

/** One-off episodes: a premise (or an article to adapt), a style and a length; the worker starts it next. */
function NewDramaForm({ onFiled }: { onFiled: () => void }) {
  const t = useTranslations("admin.videoReviews");
  const [premise, setPremise] = useState("");
  const [title, setTitle] = useState("");
  const [guide, setGuide] = useState("");
  const [preset, setPreset] = useState<(typeof PRESETS)[number]>("cinematic-3d");
  const [minutes, setMinutes] = useState(3);
  const [note, setNote] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const guideOk = !guide.trim() || GUIDE_SLUG.test(guide.trim());
  const file = async () => {
    setBusy(true);
    setError("");
    try {
      await api("/admin/video-automation/drama-requests", {
        method: "POST",
        body: JSON.stringify({ premise: premise.trim(), title: title.trim() || undefined, source_guide: guide.trim() || undefined, style_preset: preset, target_minutes: minutes, note: note.trim() || undefined }),
      });
      setPremise(""); setTitle(""); setGuide(""); setNote("");
      onFiled();
    } catch (problem) {
      setError(t("newDramaError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <details className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="cursor-pointer text-lg font-bold">{t("newDrama")}</summary>
    <form className="mt-4 grid gap-3" onSubmit={(event) => { event.preventDefault(); void file(); }} aria-label={t("newDrama")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("newDramaHelp")}</p>
      <label className="grid gap-2 text-sm font-semibold">{t("premise")}
        <textarea className={control} rows={4} value={premise} disabled={busy} maxLength={4000} placeholder={t("premisePlaceholder")} onChange={(event) => setPremise(event.target.value)} />
      </label>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="grid gap-2 text-sm font-semibold">{t("workingTitle")}<input className={control} value={title} disabled={busy} maxLength={200} onChange={(event) => setTitle(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("sourceGuide")}<input className={control} value={guide} disabled={busy} placeholder={t("sourceGuidePlaceholder")} aria-invalid={!guideOk} onChange={(event) => setGuide(event.target.value)} /></label>
        <label className="grid gap-2 text-sm font-semibold">{t("stylePreset")}
          <select className={control} value={preset} disabled={busy} onChange={(event) => setPreset(event.target.value as (typeof PRESETS)[number])}>
            {PRESETS.map((each) => <option key={each} value={each}>{t(`presets.${each}`)}</option>)}
          </select>
        </label>
        <label className="grid gap-2 text-sm font-semibold">{t("targetMinutes")}<input className={control} type="number" min={1} max={8} value={minutes} disabled={busy} onChange={(event) => setMinutes(Number(event.target.value))} /></label>
      </div>
      <label className="grid gap-2 text-sm font-semibold">{t("requestNote")}<textarea className={control} rows={2} value={note} disabled={busy} maxLength={2000} placeholder={t("requestNotePlaceholder")} onChange={(event) => setNote(event.target.value)} /></label>
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
      <div><Button type="submit" disabled={busy || !premise.trim() || !guideOk || minutes < 1 || minutes > 8}>{busy ? t("saving") : t("fileRequest")}</Button></div>
    </form>
  </details>;
}

/** What the owner asked for as one-off episodes and where each stands; a queued one can be withdrawn. */
function DramaQueue({ requests, canManage, onChanged, onOpen }: { requests: DramaRequest[]; canManage: boolean; onChanged: () => void; onOpen: (slug: string) => void }) {
  const t = useTranslations("admin.videoReviews");
  const when = useWhen();
  const [busy, setBusy] = useState("");
  const [error, setError] = useState("");
  const cancel = async (request: DramaRequest) => {
    if (!window.confirm(t("cancelConfirm"))) return;
    setBusy(request.id);
    setError("");
    try {
      await api(`/admin/video-automation/drama-requests/${request.id}`, { method: "DELETE" });
      onChanged();
    } catch (problem) {
      setError(t("cancelError", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  if (!requests.length) return null;
  return <section className="grid gap-3" aria-label={t("queue")}>
    <h3 className="text-lg font-bold">{t("queue")}</h3>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <ul className="grid gap-3">{requests.map((request) => <li key={request.id} className="grid gap-2 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4">
      <span className="flex flex-wrap items-center gap-3">
        <AdminStatusPill status={requestTone[request.status]}>{t(`requestStatuses.${request.status}`)}</AdminStatusPill>
        <span className="font-bold">{request.title || request.premise.slice(0, 40)}</span>
        <span className="text-sm text-[var(--muted)]">{t(`presets.${request.style_preset}`)} · {t("minutes", { minutes: request.target_minutes })} · {t("filedAt", { time: when(request.created_at) })}</span>
      </span>
      <span className="whitespace-pre-wrap text-sm leading-6">{request.premise}</span>
      {request.source_guide && <span className="text-sm text-[var(--muted)]">{t("adaptsArticle", { slug: request.source_guide })}</span>}
      {request.note && <span className="text-sm text-[var(--muted)]">{t("requestNote")}: {request.note}</span>}
      <span className="flex flex-wrap gap-3">
        {request.slug && <Button secondary onClick={() => onOpen(request.slug as string)}>{t("openVideo", { slug: request.slug })}</Button>}
        {canManage && request.status === "queued" && <Button secondary disabled={busy === request.id} onClick={() => void cancel(request)}>{busy === request.id ? t("saving") : t("cancelRequest")}</Button>}
      </span>
    </li>)}</ul>
  </section>;
}

/** The series the owner started, and the one-off episodes; opening a series shows its page. */
function SeriesList({ onOpenSeries, onOpenVideo }: { onOpenSeries: (slug: string) => void; onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoSeries");
  const tv = useTranslations("admin.videoReviews");
  const ts = useTranslations("admin.videoSettings");
  const when = useWhen();
  const manage = useAdminActionGuard("content.manage");
  const [series, setSeries] = useState<SeriesSummary[] | null>(null);
  const [videos, setVideos] = useState<ProjectSummary[]>([]);
  const [requests, setRequests] = useState<DramaRequest[]>([]);
  const [settings, setSettings] = useState<VideoSettingsView | null>(null);
  const [error, setError] = useState("");
  const load = useCallback(() => {
    api<{ series: SeriesSummary[] }>("/admin/video-automation/series").then((value) => { setSeries(value.series ?? []); setError(""); }).catch((problem: unknown) => setError(message(problem)));
    // The one-off episodes (a premise, not a series); an older site ignores the filter and is filtered here.
    api<ProjectSummary[]>("/admin/videos?format=drama").then((value) => setVideos((Array.isArray(value) ? value : []).filter((video) => video.format === "drama" && !video.series_slug))).catch(() => setVideos([]));
    // Finished and withdrawn one-off requests drop off after a week; a site without the route leaves the queue empty.
    api<{ requests: DramaRequest[] }>("/admin/video-automation/drama-requests").then((value) => {
      const recent = Date.now() - 7 * 24 * 3600_000;
      setRequests((value.requests ?? []).filter((request) => request.status === "queued" || request.status === "started" || Date.parse(request.created_at) > recent));
    }).catch(() => setRequests([]));
  }, []);
  useRefresh(load);
  // The settings are read once, not with the minute-by-minute refresh above: the drama settings are
  // a form, and a re-read would throw away what the owner is typing. A site without the route, or an
  // answer without a drama block, shows neither the banner nor the form.
  useEffect(() => {
    let current = true;
    api<VideoSettingsView>("/admin/video-automation/settings")
      .then((value) => { if (current && value && typeof value === "object" && !Array.isArray(value) && value.drama) setSettings(value); })
      .catch(() => undefined);
    return () => { current = false; };
  }, []);
  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  // What waits for the owner comes first, as on the tutorials list; the sort keeps the rest in order.
  const oneOffs = [...videos].sort((a, b) => Number(needsOwner(b)) - Number(needsOwner(a)));
  return <div className="grid gap-4">
    {settings && (settings.drama.drama_enabled
      ? <p role="note" className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6">{t("dramaOn")}</p>
      : <aside role="note" className="grid gap-1 rounded-xl border border-[var(--teal)] bg-[var(--surface)] p-4 text-sm leading-6">
        <p className="font-bold">{t("dramaOff")}</p>
        <p>{t("dramaOffHow", { settings: ts("dramaSettingsTitle"), enable: ts("fields.drama_enabled") })}</p>
      </aside>)}
    {settings && <AdminVideoDramaSettings view={settings} onSaved={setSettings} />}
    {manage.allowed && <NewBingeForm onCreated={(slug) => { load(); onOpenSeries(slug); }} />}
    {manage.allowed && <NewSeriesForm onCreated={(slug) => { load(); onOpenSeries(slug); }} />}
    {series && series.length === 0 && <AdminEmptyState title={t("empty")} detail={t("emptyDetail")} />}
    {series && series.length > 0 && <ul className="grid gap-4" aria-label={t("listTitle")}>{series.map((each) => <li key={each.slug}>
      <button type="button" onClick={() => onOpenSeries(each.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
        <span className="flex flex-wrap items-center gap-3"><BookOpen aria-hidden size={20} className="text-[var(--teal)]" /><span className="text-lg font-bold">{each.title}</span>
          <AdminStatusPill status={seriesTone[each.status]}>{t(`statuses.${each.status}`)}</AdminStatusPill>
          {each.docs_pending > 0 && <AdminStatusPill status="pending">{t("docsPending", { count: each.docs_pending })}</AdminStatusPill>}
          <BingePills series={each} />
        </span>
        <span className="text-sm text-[var(--muted)]">{t("progress", { done: each.episodes_done, total: each.planned_episodes, chapters: each.chapters })}{each.total_minutes ? ` · ${t("totalMinutesLabel", { minutes: each.total_minutes })}` : ""} · {t("spend", { usd: Number(each.media_usd ?? 0).toFixed(2), seconds: each.clip_seconds ?? 0 })}</span>
        <span className="line-clamp-2 text-sm leading-6">{each.premise}</span>
      </button>
    </li>)}</ul>}
    {manage.allowed && <NewDramaForm onFiled={load} />}
    <DramaQueue requests={requests} canManage={manage.allowed} onChanged={load} onOpen={onOpenVideo} />
    {videos.length > 0 && <section className="grid gap-3" aria-label={t("oneOffTitle")}>
      <h3 className="text-lg font-bold">{t("oneOffTitle")}</h3>
      <ul className="grid gap-4">{oneOffs.map((video) => <li key={video.slug}>
        <button type="button" onClick={() => onOpenVideo(video.slug)} className="grid w-full gap-2 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 text-left shadow-[var(--shadow-sm)] hover:border-[var(--teal)]">
          <span className="flex flex-wrap items-center gap-3"><span className="text-lg font-bold">{video.title}</span>
            <AdminStatusPill status="active">{tv("drama")}</AdminStatusPill>
            {video.dropped_at
              ? <AdminStatusPill status="inactive">{tv("dropped")}</AdminStatusPill>
              : <AdminStatusPill status={video.pending ? "pending" : "inactive"}>{video.pending ? tv("pending", { count: video.pending }) : tv("noPendingShort")}</AdminStatusPill>}
            {!video.dropped_at && isBlocked(video) && <AdminStatusPill status="failed">{tv("stuck")}</AdminStatusPill>}
          </span>
          <span className="text-sm text-[var(--muted)]">{tv("progress", { done: video.checklist.filter((item) => item.done).length, total: video.checklist.length })} · {tv("lastSynced", { time: when(video.last_synced_at) })}{typeof video.media_usd === "number" && ` · ${tv("spend", { usd: video.media_usd.toFixed(2), seconds: video.clip_seconds ?? 0 })}`}</span>
          {video.stage && !video.youtube_video_id && !video.dropped_at && <span className="text-sm text-[var(--muted)]">{tv("currentStep", { step: video.checklist.find((item) => !item.done)?.label ?? video.stage })}</span>}
        </button>
      </li>)}</ul>
    </section>}
  </div>;
}

const beatText = (beats: Record<string, unknown>, key: string) => {
  const value = beats[key];
  if (value && typeof value === "object" && !Array.isArray(value)) return text((value as Record<string, unknown>).text) || "";
  return text(value);
};
const cliffType = (beats: Record<string, unknown>) => {
  const value = beats.cliffhanger;
  return value && typeof value === "object" && !Array.isArray(value) ? text((value as Record<string, unknown>).type) : "";
};
const threads = (beats: Record<string, unknown>) => `${list(beats.setups).map(text).join("、") || "—"} / ${list(beats.payoffs).map(text).join("、") || "—"}`;
const tension = (beats: Record<string, unknown>) => list(beats.tension).map(text).join("-");

/** A chapter outline as a table: every episode's hook, conflict, turn, cliffhanger, threads and tension. */
function BeatsTable({ episodes }: { episodes: Record<string, unknown>[] }) {
  const t = useTranslations("admin.videoSeries");
  return <div className="overflow-x-auto"><table className="min-w-full text-sm">
    <thead><tr className="text-left text-xs text-[var(--muted)]">{(["episode", "title", "hook", "conflict", "turn", "cliffhanger", "threads", "tension"] as const).map((key) => <th key={key} className="px-2 py-1 font-semibold">{t(`beats.${key}`)}</th>)}</tr></thead>
    <tbody>{episodes.map((episode) => <tr key={text(episode.number)} className="border-t border-[var(--line)] align-top">
      <td className="px-2 py-2 font-mono">{text(episode.number)}</td>
      <td className="px-2 py-2 font-semibold">{text(episode.title)}</td>
      <td className="px-2 py-2">{beatText(episode, "hook")}</td>
      <td className="px-2 py-2">{beatText(episode, "conflict")}</td>
      <td className="px-2 py-2">{beatText(episode, "turn")}</td>
      <td className="px-2 py-2">{beatText(episode, "cliffhanger")}{cliffType(episode) && <span className="block text-xs text-[var(--muted)]">{cliffType(episode)}</span>}</td>
      <td className="px-2 py-2 font-mono text-xs">{threads(episode)}</td>
      <td className="px-2 py-2 font-mono">{tension(episode)}</td>
    </tr>)}</tbody>
  </table></div>;
}

/** One document of a series: read it, approve it or send it back with a note, or rewrite it yourself. */
function DocPanel({ slug, doc, canManage, onChanged }: { slug: string; doc: SeriesDoc; canManage: boolean; onChanged: () => void }) {
  const t = useTranslations("admin.videoSeries");
  const when = useWhen();
  const [note, setNote] = useState("");
  const [draft, setDraft] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const title = doc.kind === "chapter" ? t("chapterN", { n: doc.chapter_number }) : t(`docKinds.${doc.kind}`);
  const decide = async (decision: "approve" | "reject") => {
    setBusy(true);
    setError("");
    try {
      await api(`${docPath(slug, doc)}/decision`, { method: "POST", body: JSON.stringify({ decision, note: note.trim() || undefined }) });
      setNote("");
      onChanged();
    } catch (problem) {
      setError(t("decideError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const save = async (approve: boolean) => {
    if (draft === null || !draft.trim()) return;
    setBusy(true);
    setError("");
    try {
      await api(docPath(slug, doc), { method: "PUT", body: JSON.stringify({ body_md: draft, approve }) });
      setDraft(null);
      onChanged();
    } catch (problem) {
      setError(t("editError", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const episodes = doc.kind === "chapter" ? list(doc.body_json.episodes).map(record) : [];
  return <details open={doc.status === "review"} className="rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
    <summary className="flex cursor-pointer flex-wrap items-center gap-3">
      <span className="text-lg font-bold">{title}</span>
      <AdminStatusPill status={docTone[doc.status]}>{t(`docStatuses.${doc.status}`)}</AdminStatusPill>
      <span className="text-sm text-[var(--muted)]">{t("version", { n: doc.version })} · {when(doc.created_at)}</span>
    </summary>
    <div className="mt-4 grid gap-4">
      {doc.note && <p className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6"><strong>{doc.status === "rejected" ? t("sentBack") : t("docNote")}</strong> {doc.note}</p>}
      {episodes.length > 0 && <BeatsTable episodes={episodes} />}
      <details className="rounded-2xl border border-[var(--line)] p-4"><summary className="cursor-pointer font-bold">{t("readDoc")}</summary><div className="mt-3 max-h-[40rem] overflow-y-auto whitespace-pre-wrap text-sm leading-7">{doc.body_md}</div></details>
      {canManage && doc.status === "review" && <div className="grid gap-3 border-t border-[var(--line)] pt-4">
        <label className="grid gap-2 text-sm font-semibold">{t("note")}<textarea className={control} rows={3} value={note} disabled={busy} placeholder={t("notePlaceholder")} onChange={(event) => setNote(event.target.value)} /></label>
        <div className="flex flex-wrap gap-3">
          <Button disabled={busy} onClick={() => void decide("approve")}>{busy ? t("saving") : t("approve")}</Button>
          <Button secondary disabled={busy || !note.trim()} onClick={() => void decide("reject")}>{t("reject")}</Button>
        </div>
      </div>}
      {canManage && <details className="rounded-2xl border border-[var(--line)] p-4" onToggle={(event) => { if ((event.target as HTMLDetailsElement).open && draft === null) setDraft(doc.body_md); }}>
        <summary className="cursor-pointer font-bold">{t("editDoc")}</summary>
        <div className="mt-3 grid gap-3">
          <p className="text-sm leading-6 text-[var(--muted)]">{t("editHelp")}</p>
          <textarea className={`${control} font-mono text-xs`} rows={16} value={draft ?? doc.body_md} disabled={busy} aria-label={t("editDoc")} onChange={(event) => setDraft(event.target.value)} />
          <div className="flex flex-wrap gap-3">
            <Button disabled={busy || draft === null || !draft.trim()} onClick={() => void save(true)}>{t("saveApprove")}</Button>
            <Button secondary disabled={busy || draft === null || !draft.trim()} onClick={() => void save(false)}>{t("saveReview")}</Button>
          </div>
        </div>
      </details>}
      {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    </div>
  </details>;
}

/** One series: its documents to approve, its controls, and the episode table. */
function SeriesPage({ slug, onBack, onOpenVideo }: { slug: string; onBack: () => void; onOpenVideo: (slug: string) => void }) {
  const t = useTranslations("admin.videoSeries");
  const tv = useTranslations("admin.videoReviews");
  const manage = useAdminActionGuard("content.manage");
  const [series, setSeries] = useState<Series | null>(null);
  const [compilations, setCompilations] = useState<ProjectSummary[]>([]);
  const [error, setError] = useState("");
  const [actionError, setActionError] = useState("");
  const [busy, setBusy] = useState("");
  const load = useCallback(() => {
    api<Series>(`/admin/video-automation/series/${slug}`).then((value) => { setSeries(value); setError(""); }).catch((problem: unknown) => setError(message(problem)));
    // The compilation is the series' one video without an episode number (docs/videos/BINGE.md);
    // the episodes come with the series itself. An older site ignores the filter and is filtered here.
    api<ProjectSummary[]>(`/admin/videos?series=${slug}`)
      .then((value) => setCompilations((Array.isArray(value) ? value : []).filter((video) => video.series_slug === slug && video.episode_number == null)))
      .catch(() => setCompilations([]));
  }, [slug]);
  useRefresh(load);
  const act = async (what: string, request: () => Promise<unknown>) => {
    setBusy(what);
    setActionError("");
    try {
      await request();
      load();
    } catch (problem) {
      setActionError(t("actionError", { message: message(problem) }));
    } finally {
      setBusy("");
    }
  };
  const patch = (body: Record<string, unknown>) => api(`/admin/video-automation/series/${slug}`, { method: "PATCH", body: JSON.stringify(body) });
  const skip = (number: number) => {
    if (!window.confirm(t("skipConfirm", { n: number }))) return;
    void act(`skip-${number}`, () => api(`/admin/video-automation/series/${slug}/episodes/${number}/skip`, { method: "POST" }));
  };
  const order = (doc: SeriesDoc) => (doc.kind === "setting" ? 0 : doc.kind === "outline" ? 1 : 1 + doc.chapter_number);
  const state = series ? compilationState(series) : "none";
  // The current compilation first; an earlier one (the owner asked for another) only when nothing newer exists.
  const compilation = series ? (compilations.find((video) => video.slug === series.compilation_slug) ?? compilations[0] ?? null) : null;
  const canCompile = series?.status === "finished" && (state === "none" || state === "done");
  return <section className="mt-6 grid gap-5">
    <div><Button secondary onClick={onBack}><ArrowLeft aria-hidden size={18} />{t("back")}</Button></div>
    {error && <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />}
    {series && <>
      <header className="grid gap-2">
        <h2 className="flex flex-wrap items-center gap-3 text-2xl font-bold">{series.title}<AdminStatusPill status={seriesTone[series.status]}>{t(`statuses.${series.status}`)}</AdminStatusPill><BingePills series={series} /></h2>
        <p className="text-sm text-[var(--muted)]">{t("progress", { done: series.episodes_done, total: series.planned_episodes, chapters: series.chapters })}{series.total_minutes ? ` · ${t("totalMinutesLabel", { minutes: series.total_minutes })}` : ""} · {t("spend", { usd: Number(series.media_usd ?? 0).toFixed(2), seconds: series.clip_seconds ?? 0 })} · {t(`leads.${series.lead ?? "dual-male"}`)} · {t(`tones.${series.tone}`)} · {t(`presets.${series.style_preset}`)} · {t("minutesEach", { minutes: series.target_minutes })}</p>
        <p className="whitespace-pre-wrap text-sm leading-6">{series.premise}</p>
        {series.note && <p className="text-sm text-[var(--muted)]">{t("fields.note")}: {series.note}</p>}
        {manage.allowed && <div className="flex flex-wrap gap-3">
          {series.status === "active" && <Button secondary disabled={busy === "pause"} onClick={() => void act("pause", () => patch({ status: "paused" }))}>{t("pause")}</Button>}
          {series.status === "paused" && <Button secondary disabled={busy === "resume"} onClick={() => void act("resume", () => patch({ status: "active" }))}>{t("resume")}</Button>}
          {series.status === "active" && <Button secondary disabled={busy === "plan"} onClick={() => void act("plan", () => api(`/admin/video-automation/series/${slug}/actions/plan-next-chapter`, { method: "POST" }))}>{t("planNextChapter")}</Button>}
          {series.status === "active" && <Button secondary disabled={busy === "start"} onClick={() => void act("start", () => api(`/admin/video-automation/series/${slug}/actions/start-next`, { method: "POST" }))}>{t("startNext")}</Button>}
          {canCompile && <Button secondary disabled={busy === "compile"} onClick={() => void act("compile", () => api(`/admin/video-automation/series/${slug}/actions/compile`, { method: "POST" }))}>{t("compile")}</Button>}
        </div>}
        {manage.allowed && <div className="grid gap-1">
          <label className="flex min-h-11 items-center gap-2 text-sm font-semibold"><input type="checkbox" checked={Boolean(series.hands_off)} disabled={busy === "hands-off"} onChange={(event) => void act("hands-off", () => patch({ hands_off: event.target.checked }))} />{t("handsOff")}</label>
          <p className="text-sm leading-6 text-[var(--muted)]">{t("handsOffHelp")}</p>
        </div>}
        {(series.requested_chapter || series.force_next) && <p className="text-sm text-[var(--muted)]">{series.requested_chapter ? t("chapterRequested", { n: series.requested_chapter }) : ""}{series.force_next ? ` ${t("nextForced")}` : ""}</p>}
        {actionError && <p role="alert" className="text-sm text-red-800">{actionError}</p>}
      </header>
      {(state !== "none" || series.status === "finished" || compilation) && <section className="grid gap-3 rounded-[1.5rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]" aria-label={t("compilation")}>
        <h3 className="flex flex-wrap items-center gap-3 text-lg font-bold">{t("compilation")}{state !== "none" && <AdminStatusPill status={compilationTone[state]}>{t(`compilationStatuses.${state}`)}</AdminStatusPill>}</h3>
        {state === "none" && !compilation && <p className="text-sm leading-6 text-[var(--muted)]">{t("compilationNone")}</p>}
        {state === "waiting" && <p className="text-sm leading-6 text-[var(--muted)]">{t("compilationWaiting")}</p>}
        {state === "queued" && <p className="text-sm leading-6 text-[var(--muted)]">{t("compilationQueued")}</p>}
        {state === "making" && !compilation && <p className="text-sm leading-6 text-[var(--muted)]">{t("compilationStarting")}</p>}
        {compilation && <div className="grid gap-2">
          <p className="flex flex-wrap items-center gap-3">
            <span className="font-semibold">{compilation.title}</span>
            {compilation.stage && !compilation.dropped_at && <span className="text-sm text-[var(--muted)]">{tv("currentStep", { step: compilation.checklist.find((item) => !item.done)?.label ?? compilation.stage })}</span>}
            {compilation.pending > 0 && <AdminStatusPill status="pending">{t("pendingCount", { count: compilation.pending })}</AdminStatusPill>}
            <Button secondary onClick={() => onOpenVideo(compilation.slug)}>{t("openVideo")}</Button>
          </p>
          <CompilationDownload project={{ ...compilation, compilation: true }} />
        </div>}
      </section>}
      <section className="grid gap-4" aria-label={t("docsTitle")}>
        <h3 className="text-lg font-bold">{t("docsTitle")}</h3>
        {series.docs.length === 0 && <p className="text-sm text-[var(--muted)]">{t("docsEmpty")}</p>}
        {[...series.docs].sort((a, b) => order(a) - order(b)).map((doc) => <DocPanel key={doc.id} slug={slug} doc={doc} canManage={manage.allowed} onChanged={load} />)}
      </section>
      <section className="grid gap-3" aria-label={t("episodesTitle")}>
        <h3 className="text-lg font-bold">{t("episodesTitle")}</h3>
        {series.episodes.length === 0 ? <p className="text-sm text-[var(--muted)]">{t("episodesEmpty")}</p> : <div className="overflow-x-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)]"><table className="min-w-full text-sm">
          <thead><tr className="text-left text-xs text-[var(--muted)]">{(["number", "chapter", "title", "status", "step", "pending", "spend", "actions"] as const).map((key) => <th key={key} className="px-3 py-2 font-semibold">{t(`episodeColumns.${key}`)}</th>)}</tr></thead>
          <tbody>{series.episodes.map((episode) => {
            const video = episode.video;
            const step = video ? (video.checklist.find((item) => !item.done)?.label ?? video.stage) : "";
            return <tr key={episode.number} className="border-t border-[var(--line)] align-top">
              <td className="px-3 py-2 font-mono">{episode.number}</td>
              <td className="px-3 py-2">{episode.chapter_number}</td>
              <td className="px-3 py-2"><span className="font-semibold">{episode.title}</span>{episode.logline && <span className="block text-xs text-[var(--muted)]">{episode.logline}</span>}</td>
              <td className="px-3 py-2"><AdminStatusPill status={episodeTone[episode.status]}>{t(`episodeStatuses.${episode.status}`)}</AdminStatusPill></td>
              <td className="px-3 py-2">{step}</td>
              <td className="px-3 py-2">{video?.pending ? t("pendingCount", { count: video.pending }) : ""}</td>
              <td className="px-3 py-2">{video && typeof video.media_usd === "number" ? `US$${video.media_usd.toFixed(2)}` : ""}</td>
              <td className="px-3 py-2"><span className="flex flex-wrap gap-2">
                {episode.slug && <Button secondary onClick={() => onOpenVideo(episode.slug as string)}>{t("openVideo")}</Button>}
                {manage.allowed && (episode.status === "planned" || episode.status === "ready") && <Button secondary disabled={busy === `skip-${episode.number}`} onClick={() => skip(episode.number)}>{t("skip")}</Button>}
              </span></td>
            </tr>;
          })}</tbody>
        </table></div>}
      </section>
    </>}
  </section>;
}

/** The drama tab: the series list, or one series when the query names it. */
export function AdminVideoSeries({ onOpenVideo }: { onOpenVideo: (slug: string) => void }) {
  const [slug, setSlug] = useAdminQueryValue("series", "", (value) => SERIES_SLUG.test(value));
  if (slug) return <SeriesPage slug={slug} onBack={() => setSlug("")} onOpenVideo={onOpenVideo} />;
  return <SeriesList onOpenSeries={setSlug} onOpenVideo={onOpenVideo} />;
}
