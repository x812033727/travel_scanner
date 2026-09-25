"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminErrorState } from "@/components/admin-ui";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { aiModelsHref } from "@/lib/admin-settings-ownership";
import { api } from "@/lib/api";

// apps/api/app/video_automation/schemas.py. The worker on the host reads the same values with
// its video tool token (docs/videos/AUTOMATION.md).
// claude_code: the Claude subscription accounts the host's AI accounts agent signs in; the rest
// are the site's API keys.
export const PROVIDERS = ["claude_code", "anthropic", "openai", "gemini", "minimax"] as const;
export const STAGES = ["planner", "writer", "verifier", "listener", "translator", "caption_reviewer"] as const;
export const CAPTION_LOCALES = ["en", "ja", "ko", "zh-CN"] as const;
export type Provider = (typeof PROVIDERS)[number];
export type Stage = (typeof STAGES)[number];
type CaptionLocale = (typeof CAPTION_LOCALES)[number];
type ModelOption = { value: string; label: string; description: string | null; status: string };
type Voice = { provider: "azure" | "gemini"; name: string; style: string | null; model: string | null; rate: string };
export type VideoSettings = {
  enabled: boolean;
  draft_interval_hours: number;
  topics_per_run: number;
  max_waiting_drafts: number;
  topic_scope: string[];
  topic_avoid: string[];
  topic_from_site: boolean;
  topic_from_search: boolean;
  stage_models: Record<Stage, { provider: Provider; model: string }>;
  voice: Voice;
  target_minutes_min: number;
  target_minutes_max: number;
  caption_locales: CaptionLocale[];
  max_drafts_per_month: number;
  monthly_token_budget_millions: number;
  max_verify_rounds: number;
  max_retake_rounds: number;
  subscription_max_usage_percent: number;
  auto_approve_audio: boolean;
};
type Usage = { tokens: number; token_budget: number; subscription_tokens?: number; drafts: number; draft_budget: number; calls: number; failed_calls: number };
export type VideoSettingsView = VideoSettings & {
  model_options: Record<Provider, ModelOption[]>;
  configured_providers: Provider[];
  voice_options: { gemini: string[]; gemini_models: string[]; azure: string[] };
  usage?: Usage | null;
  updated_at: string | null;
};

export const providerLabels: Record<Provider, string> = { claude_code: "Claude Code", anthropic: "Anthropic Claude API", openai: "OpenAI API", gemini: "Google Gemini API", minimax: "MiniMax API" };
const numberFields = {
  schedule: [["draft_interval_hours", 6, 720], ["topics_per_run", 1, 3], ["max_waiting_drafts", 1, 10]],
  length: [["target_minutes_min", 3, 30], ["target_minutes_max", 3, 30]],
  budget: [["max_drafts_per_month", 0, 60], ["monthly_token_budget_millions", 1, 500], ["subscription_max_usage_percent", 10, 100], ["max_verify_rounds", 1, 5], ["max_retake_rounds", 0, 5]],
} as const;
type NumberField = (typeof numberFields)[keyof typeof numberFields][number][0];

/** One word or phrase per line, blank lines dropped, as the API stores the topic lists. */
export function linesToList(value: string): string[] {
  return value.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
}

const SETTINGS_KEYS = [
  "enabled", "draft_interval_hours", "topics_per_run", "max_waiting_drafts", "topic_scope", "topic_avoid",
  "topic_from_site", "topic_from_search", "stage_models", "voice", "target_minutes_min", "target_minutes_max",
  "caption_locales", "max_drafts_per_month", "monthly_token_budget_millions", "max_verify_rounds",
  "max_retake_rounds", "subscription_max_usage_percent", "auto_approve_audio",
] as const satisfies ReadonlyArray<keyof VideoSettings>;

/** The body the API's SettingsWrite accepts (it refuses unknown fields): the view without its options. */
export function settingsBody(view: VideoSettingsView | VideoSettings): VideoSettings {
  return Object.fromEntries(SETTINGS_KEYS.map((key) => [key, view[key]])) as VideoSettings;
}

/** What the settings tab saves: the stage models are chosen on the AI settings page and left out. */
export function saveBody(draft: VideoSettings, scope: string, avoid: string): Omit<VideoSettings, "stage_models"> {
  const rest: Partial<VideoSettings> = { ...draft };
  delete rest.stage_models;
  return { ...(rest as Omit<VideoSettings, "stage_models">), topic_scope: linesToList(scope), topic_avoid: linesToList(avoid) };
}

export function AdminVideoSettings() {
  const t = useTranslations("admin.videoSettings");
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<VideoSettingsView | null>(null);
  const [draft, setDraft] = useState<VideoSettings | null>(null);
  const [scope, setScope] = useState("");
  const [avoid, setAvoid] = useState("");
  const [error, setError] = useState("");
  const [saveError, setSaveError] = useState("");
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  const show = useCallback((value: VideoSettingsView) => {
    setView(value);
    setDraft(settingsBody(value));
    setScope(value.topic_scope.join("\n"));
    setAvoid(value.topic_avoid.join("\n"));
  }, []);
  const load = useCallback(() => {
    api<VideoSettingsView>("/admin/video-automation/settings").then((value) => { show(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, [show]);
  useEffect(load, [load]);

  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!view || !draft) return <p className="mt-6 text-[var(--muted)]">{t("loading")}</p>;
  const disabled = !manage.allowed || busy;
  const edit = (change: Partial<VideoSettings>) => { setDraft({ ...draft, ...change }); setSaved(false); };
  const setVoice = (change: Partial<Voice>) => edit({ voice: { ...draft.voice, ...change } });
  const numberInput = ([key, min, max]: readonly [NumberField, number, number]) => <label key={key} className="block text-sm font-semibold">{t(`fields.${key}`)}
    <input className={fieldClass} type="number" min={min} max={max} value={draft[key]} disabled={disabled} onChange={(event) => edit({ [key]: Number(event.target.value) })} />
  </label>;
  const voiceNames = draft.voice.provider === "gemini" ? view.voice_options.gemini : view.voice_options.azure;

  async function save() {
    if (!draft) return;
    setBusy(true);
    setSaveError("");
    try {
      show(await api<VideoSettingsView>("/admin/video-automation/settings", { method: "PUT", body: JSON.stringify(saveBody(draft, scope, avoid)) }));
      setSaved(true);
    } catch (problem) {
      setSaveError(problem instanceof Error ? problem.message : t("saveError"));
    } finally {
      setBusy(false);
    }
  }

  return <div className="mt-6 grid gap-5">
    {!manage.allowed && <p className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm">{t("readOnly")}</p>}
    <section className={`${panelClass} grid gap-4`} aria-labelledby="video-settings-schedule">
      <h2 id="video-settings-schedule" className="text-xl font-bold">{t("scheduleTitle")}</h2>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.enabled} disabled={disabled} onChange={(event) => edit({ enabled: event.target.checked })} />{t("fields.enabled")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("enabledHelp")}</p>
      <div className="grid gap-3 md:grid-cols-3">{numberFields.schedule.map(numberInput)}</div>
      <div className="grid gap-3 md:grid-cols-2">
        <label className="block text-sm font-semibold">{t("fields.topic_scope")}<textarea className={fieldClass} rows={4} value={scope} disabled={disabled} onChange={(event) => { setScope(event.target.value); setSaved(false); }} /></label>
        <label className="block text-sm font-semibold">{t("fields.topic_avoid")}<textarea className={fieldClass} rows={4} value={avoid} disabled={disabled} onChange={(event) => { setAvoid(event.target.value); setSaved(false); }} /></label>
      </div>
      <p className="text-sm text-[var(--muted)]">{t("onePerLine")}</p>
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("topicSources")}</legend>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={draft.topic_from_site} disabled={disabled} onChange={(event) => edit({ topic_from_site: event.target.checked })} />{t("fields.topic_from_site")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={draft.topic_from_search} disabled={disabled} onChange={(event) => edit({ topic_from_search: event.target.checked })} />{t("fields.topic_from_search")}</label>
      </fieldset>
    </section>

    <section className={`${panelClass} grid gap-3`} aria-labelledby="video-settings-models">
      <h2 id="video-settings-models" className="text-xl font-bold">{t("modelsTitle")}</h2>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("modelsManaged")}</p>
      <dl className="grid gap-1 text-sm md:grid-cols-2">{STAGES.map((stage) => {
        const choice = draft.stage_models[stage];
        const label = view.model_options[choice.provider]?.find((option) => option.value === choice.model)?.label ?? choice.model;
        return <div key={stage}><dt className="inline font-semibold">{t(`stages.${stage}`)}</dt><dd className="inline"> · {providerLabels[choice.provider]} · {label}</dd></div>;
      })}</dl>
      <Link href={aiModelsHref("video")} className="inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline">{t("editModels")}</Link>
    </section>

    <section className={`${panelClass} grid gap-4`} aria-labelledby="video-settings-video">
      <h2 id="video-settings-video" className="text-xl font-bold">{t("videoTitle")}</h2>
      <div className="grid gap-3 md:grid-cols-3">
        <label className="block text-sm font-semibold">{t("fields.voice_provider")}
          <select className={fieldClass} value={draft.voice.provider} disabled={disabled} onChange={(event) => {
            const provider = event.target.value as Voice["provider"];
            const names = provider === "gemini" ? view.voice_options.gemini : view.voice_options.azure;
            setVoice({ provider, name: names[0] ?? "", model: null });
          }}><option value="gemini">Google Gemini</option><option value="azure">Azure</option></select>
        </label>
        <label className="block text-sm font-semibold">{t("fields.voice_name")}
          <select className={fieldClass} value={draft.voice.name} disabled={disabled} onChange={(event) => setVoice({ name: event.target.value })}>
            {!voiceNames.includes(draft.voice.name) && <option value={draft.voice.name}>{draft.voice.name}</option>}
            {voiceNames.map((name) => <option key={name} value={name}>{name}</option>)}
          </select>
        </label>
        {draft.voice.provider === "gemini" ? <label className="block text-sm font-semibold">{t("fields.voice_model")}
          <select className={fieldClass} value={draft.voice.model ?? ""} disabled={disabled} onChange={(event) => setVoice({ model: event.target.value || null })}>
            <option value="">{t("defaultModel")}</option>
            {view.voice_options.gemini_models.map((model) => <option key={model} value={model}>{model}</option>)}
          </select>
        </label> : <label className="block text-sm font-semibold">{t("fields.voice_rate")}
          <input className={fieldClass} value={draft.voice.rate} disabled={disabled} pattern="[+-]\d{1,2}%" onChange={(event) => setVoice({ rate: event.target.value })} />
        </label>}
      </div>
      {draft.voice.provider === "gemini" && <label className="block text-sm font-semibold">{t("fields.voice_style")}
        <textarea className={fieldClass} rows={3} maxLength={400} value={draft.voice.style ?? ""} disabled={disabled} onChange={(event) => setVoice({ style: event.target.value || null })} />
      </label>}
      <div className="grid gap-3 md:grid-cols-2">{numberFields.length.map(numberInput)}</div>
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("fields.caption_locales")}</legend>
        {CAPTION_LOCALES.map((locale) => <label key={locale} className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={draft.caption_locales.includes(locale)} disabled={disabled}
          onChange={(event) => edit({ caption_locales: event.target.checked ? CAPTION_LOCALES.filter((each) => each === locale || draft.caption_locales.includes(each)) : draft.caption_locales.filter((each) => each !== locale) })} />{t(`locales.${locale}`)}</label>)}
      </fieldset>
    </section>

    <section className={`${panelClass} grid gap-4`} aria-labelledby="video-settings-budget">
      <h2 id="video-settings-budget" className="text-xl font-bold">{t("budgetTitle")}</h2>
      {view.usage && <p className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">{t("usage", {
        tokens: view.usage.tokens.toLocaleString(), tokenBudget: view.usage.token_budget.toLocaleString(),
        drafts: view.usage.drafts, draftBudget: view.usage.draft_budget, calls: view.usage.calls, failed: view.usage.failed_calls,
        planTokens: (view.usage.subscription_tokens ?? 0).toLocaleString(),
      })}</p>}
      <div className="grid gap-3 md:grid-cols-2">{numberFields.budget.map(numberInput)}</div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("budgetHelp")}</p>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("subscriptionHelp")}</p>
    </section>

    <section className={`${panelClass} grid gap-3`} aria-labelledby="video-settings-gates">
      <h2 id="video-settings-gates" className="text-xl font-bold">{t("gatesTitle")}</h2>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.auto_approve_audio} disabled={disabled} onChange={(event) => edit({ auto_approve_audio: event.target.checked })} />{t("fields.auto_approve_audio")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("gatesHelp")}</p>
    </section>

    {saveError && <p role="alert" className="text-sm text-red-800">{saveError}</p>}
    {saved && <p role="status" className="text-sm text-[var(--teal)]">{t("saved")}</p>}
    <div><Button disabled={disabled} onClick={() => void save()}>{busy ? t("saving") : t("save")}</Button></div>
  </div>;
}
