"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { useWhen } from "@/components/admin-video-review-card";
import { type ModelOption, Panel, PROVIDERS, providerLabels, SaveRow, SettingsPermissionNotice, type VideoSettingsView, VoiceFields, type VoiceOptions } from "@/components/admin-video-settings";
import {
  type Campaign, type Consent, type ConsentState, countsOf, message, type PatternSegment, SCOPE_FIELDS, settingsBody, SHORTS_LINES, SHORTS_LOCALES,
  type ShortsSettings, type ShortsSettingsBody, SUBJECT_VARIANTS, type SubjectModel, type SubjectVariant, timesOf,
} from "@/components/admin-video-shorts-data";
import { Button, fieldClass } from "@/components/community/ui";
import { api } from "@/lib/api";

// The Shorts' own settings and the owner's standing consent to publish
// (docs/videos/SHORTS.md, the sections on slots and on the consent). Saving, starting the run and
// the consent take settings.manage; anyone who reviews videos reads them. The consent is for the
// settings as they are saved, in the server's wording: the owner reads that wording here and
// agrees to it by its hash, and the page never composes it.
const consentTone: Record<ConsentState, string> = { none: "inactive", valid: "ok", expiring: "warning", expired: "failed", invalid: "failed" };
const NUMBERS = {
  calendar: [["max_per_day", 1, 4], ["lock_hours", 1, 72], ["stock_days", 0, 30], ["upload_ahead_days", 1, 30]],
  length: [["seconds_min", 10, 180], ["seconds_max", 10, 180]],
  budget: [["budget_ntd_30d", 0, 1_000_000], ["budget_soft_ntd", 0, 1_000_000], ["budget_total_ntd", 0, 10_000_000]],
  automation: [["max_per_month", 0, 400]],
} as const;
// The model menus of the AI settings page, read with the tutorial's settings.
type ModelMenus = { options: Partial<Record<string, ModelOption[]>>; configured: string[] };
type NumberField = (typeof NUMBERS)[keyof typeof NUMBERS][number][0];
type Draft = ShortsSettingsBody & { times: string; pattern: Array<{ days: number; counts: string }> };

const draftOf = (view: ShortsSettings | ShortsSettingsBody): Draft => ({
  ...settingsBody(view),
  times: view.slot_times.join(", "),
  pattern: view.daily_pattern.map((segment) => ({ days: segment.days, counts: segment.counts.join(", ") })),
});

/** The pattern as the API stores it, or null while a stretch's counts cannot be read. */
function patternOf(draft: Draft): PatternSegment[] | null {
  const segments = draft.pattern.map((segment) => ({ days: segment.days, counts: countsOf(segment.counts) }));
  return segments.every((segment) => segment.counts !== null && Number.isInteger(segment.days) && segment.days >= 1)
    ? segments.map((segment) => ({ days: segment.days, counts: segment.counts ?? [] }))
    : null;
}

/** How many days and slots a pattern makes: the run's own arithmetic, from the owner's settings. */
export function patternSize(pattern: PatternSegment[]): { days: number; slots: number } {
  let days = 0;
  let slots = 0;
  for (const segment of pattern) {
    for (let index = 0; index < segment.days; index += 1) slots += segment.counts[index % segment.counts.length] ?? 0;
    days += segment.days;
  }
  return { days, slots };
}

/** What a save sends, or null while the pattern cannot be read. A line that is off has no quota. */
function bodyOf(draft: Draft): ShortsSettingsBody | null {
  const pattern = patternOf(draft);
  if (!pattern) return null;
  const quota = Object.fromEntries(SHORTS_LINES.filter((line) => draft.lines.includes(line)).map((line) => [line, draft.weekly_quota[line] ?? 0]));
  return { ...settingsBody(draft), weekly_quota: quota, daily_pattern: pattern, slot_times: timesOf(draft.times) };
}

/**
 * The models an experiment tests, under a and b, from the AI settings page's menus. The worker cannot
 * name one: the server runs the subject stage on these (app/video_automation/ai.py subject_choice).
 * No a means no experiment runs; no b tests a's model both ways.
 */
function SubjectModels({ value, menus, disabled, onChange }: { value: ShortsSettingsBody["subject_models"]; menus: ModelMenus | null; disabled: boolean; onChange: (value: ShortsSettingsBody["subject_models"]) => void }) {
  const t = useTranslations("admin.videoShorts");
  const set = (variant: SubjectVariant, choice: SubjectModel | null) => {
    const next = { ...value };
    if (choice) next[variant] = choice;
    else delete next[variant];
    onChange(next);
  };
  return <div className="grid gap-3 md:grid-cols-2">{SUBJECT_VARIANTS.map((variant) => {
    const choice = value[variant];
    const options = (choice && menus?.options[choice.provider]) || [];
    // A model saved before it left the menu still shows as what is saved.
    const listed = choice && !options.some((option) => option.value === choice.model) && choice.model ? [{ value: choice.model, label: choice.model }, ...options] : options;
    return <fieldset key={variant} className="grid gap-2 rounded-xl border border-[var(--line)] p-3">
      <legend className="px-1 font-bold">{t(`settings.subjects.${variant}`)}</legend>
      <label className="block text-sm">{t("settings.subjects.provider")}
        <select className={fieldClass} value={choice?.provider ?? ""} disabled={disabled} onChange={(event) => {
          const provider = event.target.value;
          set(variant, provider ? { provider, model: menus?.options[provider]?.[0]?.value ?? "" } : null);
        }}>
          <option value="">{t(variant === "a" ? "settings.subjects.none" : "settings.subjects.sameAsA")}</option>
          {PROVIDERS.map((provider) => <option key={provider} value={provider}>{providerLabels[provider]}{menus && !menus.configured.includes(provider) ? ` (${t("settings.subjects.notReady")})` : ""}</option>)}
        </select>
      </label>
      {choice && (listed.length > 0
        ? <label className="block text-sm">{t("settings.subjects.model")}
          <select className={fieldClass} value={choice.model} disabled={disabled} onChange={(event) => set(variant, { ...choice, model: event.target.value })}>
            {listed.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
          </select>
        </label>
        : <label className="block text-sm">{t("settings.subjects.model")}
          <input className={fieldClass} value={choice.model} disabled={disabled} onChange={(event) => set(variant, { ...choice, model: event.target.value.trim() })} />
        </label>)}
    </fieldset>;
  })}</div>;
}

/** The consent card: where the consent stands, the wording to agree to, and taking it back. */
function ConsentCard({ consent, canManage, unsaved, onAnswer }: { consent: Consent; canManage: boolean; unsaved: boolean; onAnswer: (view: ShortsSettings) => void }) {
  const t = useTranslations("admin.videoShorts");
  const when = useWhen();
  const [readHash, setReadHash] = useState<string | null>(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const send = async (init: RequestInit) => {
    setBusy(true);
    setError("");
    try {
      onAnswer(await api<ShortsSettings>("/admin/video-shorts/autopublish", init));
      setReadHash(null);
    } catch (problem) {
      setError(t("settings.consent.error", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  const offer = consent.offer;
  const read = offer !== null && readHash === offer.text_sha256;
  const [first, ...terms] = (offer?.text ?? "").split("\n").filter(Boolean);
  // What was agreed to is still what would be agreed to now: nothing new to read.
  const current = consent.state === "valid" && offer !== null && offer.text_sha256 === consent.text_sha256;
  return <Panel title={t("settings.consent.title")}>
    <p className="flex flex-wrap items-center gap-2"><AdminStatusPill status={consentTone[consent.state]}>{t(`settings.consent.states.${consent.state}`)}</AdminStatusPill>
      {consent.granted_at && <span className="text-sm text-[var(--muted)]">{t("settings.consent.grantedAt", { time: when(consent.granted_at) })}</span>}
      {consent.expires_at && <span className="text-sm text-[var(--muted)]">{t("settings.consent.expiresAt", { time: when(consent.expires_at) })}</span>}
    </p>
    {consent.problem && <p role="status" className="text-sm leading-6 text-amber-800">{consent.problem}</p>}
    <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.consent.help")}</p>
    {offer ? <div className="grid gap-2 rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-7" aria-label={t("settings.consent.offerTitle")}>
      <p className="font-semibold">{first}</p>
      <ul className="grid gap-1">{terms.map((term) => <li key={term}>{term}</li>)}</ul>
    </div> : <p className="text-sm leading-6 text-amber-800">{t("settings.consent.noChannel")}</p>}
    {unsaved && <p className="text-sm leading-6 text-amber-800">{t("settings.consent.unsaved")}</p>}
    {canManage && offer && !current && <label className="flex min-h-11 items-start gap-2 text-sm font-semibold"><input type="checkbox" className="mt-1" checked={read} disabled={busy || unsaved} onChange={(event) => setReadHash(event.target.checked ? offer.text_sha256 : null)} />{t("settings.consent.read")}</label>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {canManage && <div className="flex flex-wrap gap-3">
      {offer && !current && <Button disabled={busy || unsaved || !read} onClick={() => void send({ method: "POST", body: JSON.stringify({ text_sha256: offer.text_sha256 }) })}>{busy ? t("saving") : t("settings.consent.agree")}</Button>}
      {consent.state !== "none" && <Button secondary disabled={busy} onClick={() => { if (window.confirm(t("settings.consent.revokeConfirm"))) void send({ method: "DELETE" }); }}>{t("settings.consent.revoke")}</Button>}
    </div>}
  </Panel>;
}

/** The day the first Short goes public; starting builds the calendar from it. */
function CampaignCard({ start, canManage, unsaved, onStarted }: { start: string | null; canManage: boolean; unsaved: boolean; onStarted: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const [day, setDay] = useState(start ?? "");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [built, setBuilt] = useState<Campaign | null>(null);
  const begin = async () => {
    if (start && !window.confirm(t("settings.campaign.rebuildConfirm"))) return;
    setBusy(true);
    setError("");
    try {
      setBuilt(await api<Campaign>("/admin/video-shorts/campaign/start", { method: "POST", body: JSON.stringify({ first_day: day }) }));
      onStarted();
    } catch (problem) {
      setError(t("settings.campaign.error", { message: message(problem) }));
    } finally {
      setBusy(false);
    }
  };
  return <Panel title={t("settings.campaign.title")}>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.campaign.help")}</p>
    {start && <p className="text-sm font-semibold">{t("settings.campaign.current", { start })}</p>}
    <label className="block text-sm font-semibold md:w-1/2">{t("settings.campaign.firstDay")}
      <input type="date" className={fieldClass} value={day} disabled={!canManage || busy} onChange={(event) => setDay(event.target.value)} />
    </label>
    {unsaved && <p className="text-sm leading-6 text-amber-800">{t("settings.campaign.unsaved")}</p>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {built && <p role="status" className="text-sm text-[var(--teal)]">{t("settings.campaign.started", { slots: built.slots, assigned: built.assigned, last: built.last_day })}</p>}
    <div><Button disabled={!canManage || busy || unsaved || !day} onClick={() => void begin()}>{busy ? t("saving") : start ? t("settings.campaign.rebuild") : t("settings.campaign.start")}</Button></div>
  </Panel>;
}

export function ShortsSettingsPanel({ onChanged }: { onChanged: () => void }) {
  const t = useTranslations("admin.videoShorts");
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<ShortsSettings | null>(null);
  const [draft, setDraft] = useState<Draft | null>(null);
  const [voices, setVoices] = useState<VoiceOptions | null>(null);
  const [menus, setMenus] = useState<ModelMenus | null>(null);
  const [loadError, setLoadError] = useState("");
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState("");
  const take = useCallback((value: ShortsSettings) => { setView(value); setDraft(draftOf(value)); }, []);
  const load = useCallback(() => {
    api<ShortsSettings>("/admin/video-shorts/settings").then((value) => { take(value); setLoadError(""); }).catch((problem: unknown) => setLoadError(message(problem)));
    // The voices the site can speak in, and the AI settings page's model menus, are listed with the tutorial's settings.
    api<VideoSettingsView>("/admin/video-automation/settings").then((value) => {
      setVoices(value.voice_options);
      setMenus(value.model_options ? { options: value.model_options, configured: value.configured_providers ?? [] } : null);
    }).catch(() => { setVoices(null); setMenus(null); });
  }, [take]);
  useEffect(load, [load]);
  if (loadError) return <AdminErrorState title={t("loadError")} detail={loadError} retry={load} retryLabel={t("retry")} />;
  if (!view || !draft) return <p className="text-[var(--muted)]">{t("loading")}</p>;

  const disabled = !manage.allowed || busy;
  const edit = (change: Partial<Draft>) => { setDraft((current) => (current ? { ...current, ...change } : current)); setSaved(false); };
  const body = bodyOf(draft);
  // Both sides go through the same reading, so only what the owner changed counts as a change.
  const stored = bodyOf(draftOf(view));
  const unsaved = JSON.stringify(body) !== JSON.stringify(stored);
  const widens = view.autopublish && body !== null && stored !== null && SCOPE_FIELDS.some((field) => JSON.stringify(body[field]) !== JSON.stringify(stored[field]));
  const size = body ? patternSize(body.daily_pattern) : null;
  const save = async () => {
    if (!body) return;
    // Said again at the moment it happens: the save itself is what ends the consent.
    if (widens && !window.confirm(t("settings.scopeConfirm"))) return;
    setBusy(true);
    setError("");
    try {
      take(await api<ShortsSettings>("/admin/video-shorts/settings", { method: "PUT", body: JSON.stringify(body) }));
      setSaved(true);
      onChanged();
    } catch (problem) {
      setError(message(problem) || t("settings.saveError"));
    } finally {
      setBusy(false);
    }
  };
  const numberInput = ([key, min, max]: readonly [NumberField, number, number]) => <label key={key} className="block text-sm font-semibold">{t(`settings.fields.${key}`)}
    <input className={fieldClass} type="number" min={min} max={max} value={draft[key]} disabled={disabled} onChange={(event) => edit({ [key]: Number(event.target.value) })} />
  </label>;
  const segment = (index: number, change: Partial<Draft["pattern"][number]>) => edit({ pattern: draft.pattern.map((each, position) => (position === index ? { ...each, ...change } : each)) });
  const answered = (value: ShortsSettings) => { take(value); onChanged(); };

  return <div className="grid gap-5" aria-label={t("views.settings")}>
    <SettingsPermissionNotice capability="settings.manage" />
    <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.help")}</p>

    <Panel title={t("settings.paceTitle")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.paceHelp")}</p>
      <ol className="grid gap-3">{draft.pattern.map((each, index) => <li key={index} className="grid gap-3 rounded-xl border border-[var(--line)] p-3 md:grid-cols-[1fr_1fr_auto] md:items-end">
        <label className="block text-sm font-semibold">{t("settings.fields.pattern_days")}
          <input className={fieldClass} type="number" min={1} max={366} value={each.days} disabled={disabled} onChange={(event) => segment(index, { days: Number(event.target.value) })} />
        </label>
        <label className="block text-sm font-semibold">{t("settings.fields.pattern_counts")}
          <input className={fieldClass} value={each.counts} disabled={disabled} aria-invalid={countsOf(each.counts) === null} onChange={(event) => segment(index, { counts: event.target.value })} />
        </label>
        <Button secondary disabled={disabled || draft.pattern.length === 1} onClick={() => edit({ pattern: draft.pattern.filter((_each, position) => position !== index) })}>{t("settings.removeSegment")}</Button>
      </li>)}</ol>
      <div><Button secondary disabled={disabled || draft.pattern.length >= 12} onClick={() => edit({ pattern: [...draft.pattern, { days: 30, counts: "1" }] })}>{t("settings.addSegment")}</Button></div>
      <p className="text-sm text-[var(--muted)]">{size ? t("settings.patternSize", { days: size.days, slots: size.slots }) : t("settings.patternInvalid")}</p>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="block text-sm font-semibold">{t("settings.fields.slot_times")}
          <input className={fieldClass} value={draft.times} disabled={disabled} onChange={(event) => edit({ times: event.target.value })} />
        </label>
        <label className="block text-sm font-semibold">{t("settings.fields.timezone")}
          <input className={fieldClass} value={draft.timezone} disabled={disabled} onChange={(event) => edit({ timezone: event.target.value.trim() })} />
        </label>
      </div>
      <div className="grid gap-3 md:grid-cols-4">{NUMBERS.calendar.map(numberInput)}</div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.calendarHelp")}</p>
    </Panel>

    <Panel title={t("settings.linesTitle")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.linesHelp")}</p>
      <div className="grid gap-3 md:grid-cols-3">{SHORTS_LINES.map((line) => <div key={line} className="grid gap-2 rounded-xl border border-[var(--line)] p-3">
        <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.lines.includes(line)} disabled={disabled}
          onChange={(event) => edit({ lines: SHORTS_LINES.filter((each) => (each === line ? event.target.checked : draft.lines.includes(each))) })} />{t(`lines.${line}`)}</label>
        <label className="block text-sm font-semibold">{t("settings.fields.weekly_quota")}
          <input className={fieldClass} type="number" min={0} max={28} value={draft.weekly_quota[line] ?? 0} disabled={disabled || !draft.lines.includes(line)} onChange={(event) => edit({ weekly_quota: { ...draft.weekly_quota, [line]: Number(event.target.value) } })} />
        </label>
      </div>)}</div>
    </Panel>

    <Panel title={t("settings.makingTitle")}>
      <div className="grid gap-3 md:grid-cols-2">{NUMBERS.length.map(numberInput)}</div>
      {voices ? <VoiceFields voice={draft.voice} options={voices} disabled={disabled} onChange={(change) => edit({ voice: { ...draft.voice, ...change } })} />
        : <p className="text-sm text-[var(--muted)]">{t("settings.voiceNow", { voice: `${draft.voice.provider} ${draft.voice.name}` })}</p>}
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.voiceHelp")}</p>
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("settings.fields.locales")}</legend>
        {SHORTS_LOCALES.map((locale) => <label key={locale} className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={draft.locales.includes(locale)} disabled={disabled}
          onChange={(event) => edit({ locales: SHORTS_LOCALES.filter((each) => (each === locale ? event.target.checked : draft.locales.includes(each))) })} />{t(`settings.locales.${locale}`)}</label>)}
      </fieldset>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.localesHelp")}</p>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.auto_approve} disabled={disabled} onChange={(event) => edit({ auto_approve: event.target.checked })} />{t("settings.fields.auto_approve")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.made_for_kids} disabled={disabled} onChange={(event) => edit({ made_for_kids: event.target.checked })} />{t("settings.fields.made_for_kids")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.enabled} disabled={disabled} onChange={(event) => edit({ enabled: event.target.checked })} />{t("settings.fields.enabled")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.enabledHelp")}</p>
    </Panel>

    <Panel title={t("settings.subjects.title")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.subjects.help")}</p>
      <SubjectModels value={draft.subject_models ?? {}} menus={menus} disabled={disabled} onChange={(subject_models) => edit({ subject_models })} />
      <div className="grid gap-3 md:grid-cols-2">{NUMBERS.automation.map(numberInput)}</div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.subjects.monthHelp")}</p>
    </Panel>

    <Panel title={t("settings.budgetTitle")}>
      <div className="grid gap-3 md:grid-cols-3">{NUMBERS.budget.map(numberInput)}</div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("settings.budgetHelp")}</p>
    </Panel>

    {widens && <p role="status" className="rounded-xl border border-amber-600 bg-amber-50 p-3 text-sm leading-6">{t("settings.scopeWarning")}</p>}
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    <SaveRow label={t("settings.save")} busy={busy} saved={saved && !unsaved} error="" disabled={disabled || !body || !unsaved} onSave={() => void save()} />

    <CampaignCard key={view.campaign_start ?? "none"} start={view.campaign_start} canManage={manage.allowed} unsaved={unsaved} onStarted={() => { load(); onChanged(); }} />
    <ConsentCard consent={view.consent} canManage={manage.allowed} unsaved={unsaved} onAnswer={answered} />
  </div>;
}
