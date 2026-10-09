"use client";

import { useLocale, useTranslations } from "next-intl";
import { type ReactNode, useCallback, useEffect, useMemo, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { AdminErrorState } from "@/components/admin-ui";
import { AdminVideoSettingsTutorial } from "@/components/admin-video-settings-tutorial";
import { Button, fieldClass, panelClass, Tabs } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { adminCan } from "@/lib/admin-operations";
import { aiModelsHref } from "@/lib/admin-settings-ownership";
import { adminUsersCopy } from "@/lib/admin-users-copy";
import { adminNavigate, useAdminQueryState } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";

// apps/api/app/video_automation/schemas.py. The worker on the host reads the same values with
// its video tool token (docs/videos/AUTOMATION.md).
// The settings tab is two parts, each saved on its own (docs/videos/DRAMA-FLOW.md, section 1): the
// tutorial's (admin-video-settings-tutorial.tsx) and what both formats share (this file, which
// also holds the types, the request bodies and the pieces the parts render). The drama's part
// lives on the drama tab (admin-video-drama-settings.tsx, rendering admin-video-settings-drama.tsx).
// claude_code and codex use subscription accounts on the host; the rest use API keys.
export const PROVIDERS = ["claude_code", "codex", "anthropic", "openai", "gemini", "minimax"] as const;
export const STAGES = ["planner", "writer", "verifier", "listener", "translator", "caption_reviewer"] as const;
export const CAPTION_LOCALES = ["en", "ja", "ko"] as const;
export const SECTIONS = ["tutorial", "shared"] as const;
export type Provider = (typeof PROVIDERS)[number];
export type Stage = (typeof STAGES)[number];
export type CaptionLocale = (typeof CAPTION_LOCALES)[number];
export type Section = (typeof SECTIONS)[number];
export type ModelOption = { value: string; label: string; description: string | null; status: string };
export type Voice = { provider: "azure" | "gemini"; name: string; style: string | null; model: string | null; rate: string };
export type StageModel = { provider: Provider; model: string };
export type StageModels = Record<Stage, StageModel>;
export type StandingInstructions = Partial<Record<Stage, string>>;
// The AI drama route (docs/videos/DRAMA.md): apps/api/app/video_automation/schemas.py DramaSettings.
export const MEDIA_PROVIDERS = ["gemini", "minimax"] as const;
export const STYLE_PRESETS = ["cinematic-3d", "anime-2d", "ink-wash", "flat-explainer", "custom"] as const;
export type MediaProvider = (typeof MEDIA_PROVIDERS)[number];
export type MediaOption = ModelOption & { resolutions: string[]; durations: number[]; reference_images: number; native_audio: boolean; usd_per_second: number | null; usd_per_image: number | null; usd_per_track: number | null };
export type MediaOptions = { images: Record<MediaProvider, MediaOption[]>; clips: Record<MediaProvider, MediaOption[]>; music: Record<MediaProvider, MediaOption[]> };
export type CharacterVoice = { provider: "azure" | "gemini"; name: string; style?: string | null; hint?: string | null };
// The API sends more drama fields than this tab edits (the series_* limits of docs/videos/SERIES.md);
// they ride along untouched because every save spreads the whole object it was given.
export type DramaSettings = {
  drama_enabled: boolean;
  image_provider: MediaProvider;
  image_model: string;
  clip_provider: MediaProvider;
  clip_model: string;
  music_provider: MediaProvider;
  music_model: string;
  clip_resolution: string;
  clip_seconds_default: number;
  clip_native_audio: boolean;
  drama_aspect: "16:9" | "9:16";
  max_clips_per_video: number;
  max_retakes_per_shot: number;
  monthly_clip_seconds_budget: number;
  monthly_images_budget: number;
  monthly_judge_calls_budget: number;
  monthly_music_budget: number;
  max_usd_per_video: number;
  judge_min_score: number;
  auto_approve_storyboard: boolean;
  auto_pick_look: boolean;
  character_voice_pool: CharacterVoice[];
  music_enabled: boolean;
  subtitle_burn_in: boolean;
  style_preset: (typeof STYLE_PRESETS)[number];
  drama_topic_scope: string[];
  // A long series (docs/videos/SERIES.md): the pace, and whether every screenplay waits for the owner.
  series_max_in_flight: number;
  series_script_gate: boolean;
  series_auto_continue: boolean;
  series_chapter_ahead: number;
  series_doc_rewrites: number;
  series_episodes_per_month: number;
  // The drama's own copies of the tutorial's settings (docs/videos/DRAMA-FLOW.md, section 1); the
  // models and the narrator voice are null to follow the tutorial's.
  drama_stage_models: StageModels | null;
  drama_stage_instructions: StandingInstructions;
  drama_voice: Voice | null;
  drama_caption_locales: CaptionLocale[];
  drama_auto_approve_audio: boolean;
  drama_auto_approve_final: boolean;
  drama_max_verify_rounds: number;
  drama_max_retake_rounds: number;
};
// Illustrated slides (docs/videos/ILLUSTRATED.md): the pictures' switch, image model (null follows
// the drama's), per-video cap, whether the storyboard approves itself from the judge's scores, and
// the owner's licensed music file and sound-effect set the worker gives every new video.
export type SlidesSettings = {
  slides_media_enabled: boolean;
  slides_image_model: string | null;
  slides_max_usd_per_video: number;
  slides_auto_approve_storyboard: boolean;
  slides_music_track: string | null;
  slides_sfx_set: string | null;
};
export const SLIDES_IMAGE_MODEL = "gemini-3.1-flash-image";
export type VideoSettings = {
  enabled: boolean;
  draft_interval_hours: number;
  topics_per_run: number;
  max_waiting_drafts: number;
  topic_scope: string[];
  topic_avoid: string[];
  topic_from_site: boolean;
  topic_from_search: boolean;
  stage_models: StageModels;
  voice: Voice;
  target_minutes_min: number;
  target_minutes_max: number;
  caption_locales: CaptionLocale[];
  max_drafts_per_month: number;
  monthly_token_budget_millions: number;
  max_verify_rounds: number;
  max_retake_rounds: number;
  auto_approve_audio: boolean;
  drama: DramaSettings;
  slides: SlidesSettings;
  // Stage -> the owner's standing instructions, which the worker appends to that stage's prompt.
  stage_instructions: StandingInstructions;
  // The hands-off switches (docs/videos/HANDS-OFF.md): what the channel believes, and which gates approve themselves.
  channel_stance: string;
  auto_pick_outline: boolean;
  auto_approve_final: boolean;
};
// The instructions a stage was last sent, as the worker composed them (GET /admin/video-automation/prompts);
// variant names a series document, an episode stage or a fix (docs/videos/SERIES.md), "" for a video's own.
export type StagePrompt = { stage: Stage; format: "slides" | "drama"; variant?: string; slug: string; instructions: string; sent_at: string };
type Usage = { tokens: number; token_budget: number; subscription_tokens?: number; drafts: number; draft_budget: number; calls: number; failed_calls: number };
export type VoiceOptions = { gemini: string[]; gemini_models: string[]; azure: string[] };
export type VideoSettingsView = VideoSettings & {
  model_options: Record<Provider, ModelOption[]>;
  configured_providers: Provider[];
  voice_options: VoiceOptions;
  media_options?: MediaOptions;
  style_presets?: string[];
  usage?: Usage | null;
  updated_at: string | null;
};
export type SectionProps = { view: VideoSettingsView; prompts: StagePrompt[]; canManage: boolean; onSaved: (view: VideoSettingsView) => void };

export const providerLabels: Record<Provider, string> = { claude_code: "Claude Code", codex: "Codex", anthropic: "Anthropic Claude API", openai: "OpenAI API", gemini: "Google Gemini API", minimax: "MiniMax API" };
export const mediaProviderLabels: Record<MediaProvider, string> = { gemini: "Google Gemini API", minimax: "MiniMax API" };

/** One word or phrase per line, blank lines dropped, as the API stores the topic lists. */
export function linesToList(value: string): string[] {
  return value.split(/\r?\n/).map((line) => line.trim()).filter(Boolean);
}

/** The drama object with every field, for a site from before the series or the split existed. */
export function normalizeDrama(drama: Partial<DramaSettings> | undefined): DramaSettings {
  const given = drama ?? {};
  return {
    ...(given as DramaSettings),
    series_max_in_flight: given.series_max_in_flight ?? 1,
    series_script_gate: given.series_script_gate ?? true,
    series_auto_continue: given.series_auto_continue ?? true,
    series_chapter_ahead: given.series_chapter_ahead ?? 2,
    series_doc_rewrites: given.series_doc_rewrites ?? 2,
    series_episodes_per_month: given.series_episodes_per_month ?? 30,
    drama_stage_models: given.drama_stage_models ?? null,
    drama_stage_instructions: given.drama_stage_instructions ?? {},
    drama_voice: given.drama_voice ?? null,
    drama_caption_locales: given.drama_caption_locales ?? [],
    drama_auto_approve_audio: given.drama_auto_approve_audio ?? true,
    drama_auto_approve_final: given.drama_auto_approve_final ?? true,
    drama_max_verify_rounds: given.drama_max_verify_rounds ?? 3,
    drama_max_retake_rounds: given.drama_max_retake_rounds ?? 2,
  };
}

/** The slides object with every field, for a site from before the illustrated slides existed. */
export function normalizeSlides(slides: Partial<SlidesSettings> | undefined): SlidesSettings {
  const given = slides ?? {};
  return {
    slides_media_enabled: given.slides_media_enabled ?? false,
    slides_image_model: given.slides_image_model === undefined ? SLIDES_IMAGE_MODEL : given.slides_image_model,
    slides_max_usd_per_video: given.slides_max_usd_per_video ?? 20,
    slides_auto_approve_storyboard: given.slides_auto_approve_storyboard ?? true,
    slides_music_track: given.slides_music_track ?? null,
    slides_sfx_set: given.slides_sfx_set ?? null,
  };
}

const SETTINGS_KEYS = [
  "enabled", "draft_interval_hours", "topics_per_run", "max_waiting_drafts", "topic_scope", "topic_avoid",
  "topic_from_site", "topic_from_search", "stage_models", "voice", "target_minutes_min", "target_minutes_max",
  "caption_locales", "max_drafts_per_month", "monthly_token_budget_millions", "max_verify_rounds",
  "max_retake_rounds", "auto_approve_audio", "drama", "slides", "stage_instructions", "channel_stance", "auto_pick_outline",
  "auto_approve_final",
] as const satisfies ReadonlyArray<keyof VideoSettings>;

/** The whole settings body (what SettingsWrite holds): the view without its options, every field present. */
export function settingsBody(view: VideoSettingsView | VideoSettings): VideoSettings {
  const body = Object.fromEntries(SETTINGS_KEYS.map((key) => [key, view[key]])) as VideoSettings;
  // A site from before the standing instructions or the hands-off switches existed sends none.
  return {
    ...body,
    stage_instructions: view.stage_instructions ?? {},
    channel_stance: view.channel_stance ?? "",
    auto_pick_outline: view.auto_pick_outline ?? true,
    auto_approve_final: view.auto_approve_final ?? true,
    drama: normalizeDrama(view.drama),
    slides: normalizeSlides(view.slides),
  };
}

// What each part of the tab saves. The API keeps the stored value of every field a save leaves
// out (SettingsSave.merged_over), so a part never sends another part's fields, and the stage
// models are chosen on the AI settings page.
export const TUTORIAL_KEYS = [
  "enabled", "draft_interval_hours", "topics_per_run", "max_waiting_drafts", "topic_scope", "topic_from_site",
  "topic_from_search", "voice", "target_minutes_min", "target_minutes_max", "caption_locales", "max_drafts_per_month",
  "max_verify_rounds", "max_retake_rounds", "auto_approve_audio", "auto_pick_outline", "auto_approve_final",
  "stage_instructions", "slides",
] as const satisfies ReadonlyArray<keyof VideoSettings>;
export const SHARED_KEYS = ["channel_stance", "topic_avoid", "monthly_token_budget_millions"] as const satisfies ReadonlyArray<keyof VideoSettings>;
export type TutorialBody = Pick<VideoSettings, (typeof TUTORIAL_KEYS)[number]>;
export type SharedBody = Pick<VideoSettings, (typeof SHARED_KEYS)[number]>;

export function tutorialBody(draft: VideoSettings, scope: string): TutorialBody {
  const body = Object.fromEntries(TUTORIAL_KEYS.map((key) => [key, draft[key]])) as TutorialBody;
  return { ...body, topic_scope: linesToList(scope) };
}

export function sharedBody(draft: VideoSettings, avoid: string): SharedBody {
  return { channel_stance: draft.channel_stance, topic_avoid: linesToList(avoid), monthly_token_budget_millions: draft.monthly_token_budget_millions };
}

export function dramaBody(drama: DramaSettings, scope: string): Pick<VideoSettings, "drama"> {
  return { drama: { ...drama, drama_topic_scope: linesToList(scope) } };
}

// The admin roles by the key the members page labels them with (lib/admin-users-copy.ts), so a
// role reads the same here as where the owner grants it.
const ROLE_COPY_KEYS: Record<string, string> = {
  viewer: "rolesViewer", support: "rolesSupport", content: "rolesContent", operations: "rolesOperations",
  database_operator: "rolesDatabase", deployer: "rolesDeployer", owner: "rolesOwner",
};

/**
 * Why a settings form is read-only for this account: what it needs, the roles the account holds,
 * and who can change that. A reviewer can run and review dramas with the content role alone, so
 * without this a greyed-out save button looks like a broken page. Renders nothing when the
 * account may edit, or outside an admin route.
 */
export function SettingsPermissionNotice({ capability }: { capability: string }) {
  const t = useTranslations("admin.videoSettings");
  const nav = useTranslations("admin.navigation");
  const locale = useLocale();
  const operations = useAdminOperations();
  if (!operations || adminCan(operations.bootstrap, capability)) return null;
  const copy = adminUsersCopy(locale) as unknown as Record<string, string>;
  const label = (role: string) => copy[ROLE_COPY_KEYS[role] ?? ""] || role;
  const roles = operations.bootstrap.admin_roles.map(label);
  return <aside role="note" className="grid gap-1 rounded-xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6">
    <p className="font-semibold">{t("readOnly")}</p>
    <p>{roles.length ? t("permission.roles", { roles: new Intl.ListFormat(locale, { type: "conjunction" }).format(roles) }) : t("permission.noRoles")}</p>
    <p>{t("permission.fix", { owner: label("owner"), operations: label("operations"), page: nav("users") })}</p>
  </aside>;
}

/** The catalog entry of a chosen media model, or null when the server no longer offers it. */
export function mediaChoice(options: MediaOptions | undefined, kind: keyof MediaOptions, provider: MediaProvider, model: string): MediaOption | null {
  return options?.[kind]?.[provider]?.find((option) => option.value === model) ?? null;
}

/**
 * One part's save: PUT only that part's fields. The view that comes back is the whole, handed to
 * the page and returned to the part, which resets its draft from it (the server trims and drops
 * what it does not keep); null when the save failed.
 */
export function useSettingsSave(onSaved: (view: VideoSettingsView) => void) {
  const t = useTranslations("admin.videoSettings");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [saved, setSaved] = useState(false);
  const save = useCallback(async (body: Partial<VideoSettings>): Promise<VideoSettingsView | null> => {
    setBusy(true);
    setError("");
    try {
      const next = await api<VideoSettingsView>("/admin/video-automation/settings", { method: "PUT", body: JSON.stringify(body) });
      onSaved(next);
      setSaved(true);
      return next;
    } catch (problem) {
      setError(problem instanceof Error ? problem.message : t("saveError"));
      return null;
    } finally {
      setBusy(false);
    }
  }, [onSaved, t]);
  const touch = useCallback(() => setSaved(false), []);
  return { busy, error, saved, save, touch };
}

export function SaveRow({ label, busy, saved, error, disabled, onSave }: { label: string; busy: boolean; saved: boolean; error: string; disabled: boolean; onSave: () => void }) {
  const t = useTranslations("admin.videoSettings");
  return <>
    {error && <p role="alert" className="text-sm text-red-800">{error}</p>}
    {saved && <p role="status" className="text-sm text-[var(--teal)]">{t("saved")}</p>}
    <div><Button disabled={disabled} onClick={onSave}>{busy ? t("saving") : label}</Button></div>
  </>;
}

export function Panel({ title, children }: { title: string; children: ReactNode }) {
  return <section className={`${panelClass} grid gap-4`} aria-label={title}>
    <h2 className="text-xl font-bold">{title}</h2>
    {children}
  </section>;
}

/** The narrator voice: the vendor, the voice, and the model and style (Gemini) or the rate (Azure). */
export function VoiceFields({ voice, options, disabled, onChange }: { voice: Voice; options: VoiceOptions; disabled: boolean; onChange: (change: Partial<Voice>) => void }) {
  const t = useTranslations("admin.videoSettings");
  const names = voice.provider === "gemini" ? options.gemini : options.azure;
  return <>
    <div className="grid gap-3 md:grid-cols-3">
      <label className="block text-sm font-semibold">{t("fields.voice_provider")}
        <select className={fieldClass} value={voice.provider} disabled={disabled} onChange={(event) => {
          const provider = event.target.value as Voice["provider"];
          const offered = provider === "gemini" ? options.gemini : options.azure;
          onChange({ provider, name: offered[0] ?? "", model: null });
        }}><option value="gemini">Google Gemini</option><option value="azure">Azure</option></select>
      </label>
      <label className="block text-sm font-semibold">{t("fields.voice_name")}
        <select className={fieldClass} value={voice.name} disabled={disabled} onChange={(event) => onChange({ name: event.target.value })}>
          {!names.includes(voice.name) && <option value={voice.name}>{voice.name}</option>}
          {names.map((name) => <option key={name} value={name}>{name}</option>)}
        </select>
      </label>
      {voice.provider === "gemini" ? <label className="block text-sm font-semibold">{t("fields.voice_model")}
        <select className={fieldClass} value={voice.model ?? ""} disabled={disabled} onChange={(event) => onChange({ model: event.target.value || null })}>
          <option value="">{t("defaultModel")}</option>
          {options.gemini_models.map((model) => <option key={model} value={model}>{model}</option>)}
        </select>
      </label> : <label className="block text-sm font-semibold">{t("fields.voice_rate")}
        <input className={fieldClass} value={voice.rate} disabled={disabled} pattern="[+-]\d{1,2}%" onChange={(event) => onChange({ rate: event.target.value })} />
      </label>}
    </div>
    {voice.provider === "gemini" && <label className="block text-sm font-semibold">{t("fields.voice_style")}
      <textarea className={fieldClass} rows={3} maxLength={400} value={voice.style ?? ""} disabled={disabled} onChange={(event) => onChange({ style: event.target.value || null })} />
    </label>}
  </>;
}

/** The six stages' models, read only: they are chosen on the AI settings page. */
export function StageModelList({ models, view, note }: { models: StageModels; view: VideoSettingsView; note?: string }) {
  const t = useTranslations("admin.videoSettings");
  return <Panel title={t("modelsTitle")}>
    <p className="text-sm leading-6 text-[var(--muted)]">{note ?? t("modelsManaged")}</p>
    <dl className="grid gap-1 text-sm md:grid-cols-2">{STAGES.map((stage) => {
      const choice = models[stage];
      const label = view.model_options[choice.provider]?.find((option) => option.value === choice.model)?.label ?? choice.model;
      return <div key={stage}><dt className="inline font-semibold">{t(`stages.${stage}`)}</dt><dd className="inline"> · {providerLabels[choice.provider]} · {label}</dd></div>;
    })}</dl>
    <Link href={aiModelsHref("video")} className="inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline">{t("editModels")}</Link>
  </Panel>;
}

/** A stage's standing instructions, six text areas; the worker appends each to that stage's prompt. */
export function InstructionFields({ instructions, disabled, help, onChange }: { instructions: StandingInstructions; disabled: boolean; help: string; onChange: (instructions: StandingInstructions) => void }) {
  const t = useTranslations("admin.videoSettings");
  return <Panel title={t("instructionsTitle")}>
    <p className="text-sm leading-6 text-[var(--muted)]">{help}</p>
    <div className="grid gap-3 md:grid-cols-2">{STAGES.map((stage) => <label key={stage} className="block text-sm font-semibold">{t("instructionFor", { stage: t(`stages.${stage}`) })}
      <textarea className={fieldClass} rows={3} maxLength={4000} value={instructions[stage] ?? ""} disabled={disabled} placeholder={t("instructionPlaceholder")} onChange={(event) => onChange({ ...instructions, [stage]: event.target.value })} />
    </label>)}</div>
  </Panel>;
}

/** The languages the language panel pre-ticks for a new video (docs/videos/LANGUAGES.md). */
export function LocaleDefaults({ locales, disabled, onChange }: { locales: CaptionLocale[]; disabled: boolean; onChange: (locales: CaptionLocale[]) => void }) {
  const t = useTranslations("admin.videoSettings");
  return <>
    <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("fields.caption_locales")}</legend>
      {CAPTION_LOCALES.map((locale) => <label key={locale} className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={locales.includes(locale)} disabled={disabled}
        onChange={(event) => onChange(event.target.checked ? CAPTION_LOCALES.filter((each) => each === locale || locales.includes(each)) : locales.filter((each) => each !== locale))} />{t(`locales.${locale}`)}</label>)}
    </fieldset>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("localesHelp")}</p>
  </>;
}

/** The prompts the worker last sent for one format, read only, the newest per stage and variant. */
export function PromptsList({ prompts, format }: { prompts: StagePrompt[]; format: StagePrompt["format"] }) {
  const t = useTranslations("admin.videoSettings");
  const locale = useLocale();
  const when = useMemo(() => new Intl.DateTimeFormat(locale, { dateStyle: "medium", timeStyle: "short" }), [locale]);
  const shown = prompts.filter((prompt) => prompt.format === format);
  return <Panel title={t("promptsTitle")}>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("promptsHelp")}</p>
    {shown.length === 0 && <p className="text-sm text-[var(--muted)]">{t("promptsEmpty")}</p>}
    {shown.map((prompt) => <details key={`${prompt.stage}-${prompt.variant ?? ""}`} className="rounded-xl border border-[var(--line)] p-3">
      <summary className="cursor-pointer text-sm font-semibold">{t(`stages.${prompt.stage}`)}{prompt.variant ? ` · ${prompt.variant}` : ""} · {t("promptSent", { slug: prompt.slug, time: when.format(new Date(prompt.sent_at)) })}</summary>
      <pre className="mt-3 max-h-96 overflow-auto whitespace-pre-wrap break-words rounded-lg bg-[var(--paper)] p-3 text-xs leading-5">{prompt.instructions}</pre>
    </details>)}
  </Panel>;
}

/** What both formats use: the channel stance, the topics to avoid, and the month's token budget. */
function SharedSettings({ view, canManage, onSaved }: SectionProps) {
  const t = useTranslations("admin.videoSettings");
  const [draft, setDraft] = useState<VideoSettings>(() => settingsBody(view));
  const [avoid, setAvoid] = useState(() => view.topic_avoid.join("\n"));
  const { busy, error, saved, save, touch } = useSettingsSave(onSaved);
  const disabled = !canManage || busy;
  const edit = (change: Partial<VideoSettings>) => { setDraft((current) => ({ ...current, ...change })); touch(); };
  const submit = async () => {
    const next = await save(sharedBody(draft, avoid));
    if (next) { setDraft(settingsBody(next)); setAvoid(next.topic_avoid.join("\n")); }
  };
  return <div className="grid gap-5">
    <p className="text-sm leading-6 text-[var(--muted)]">{t("sharedHelp")}</p>
    <Panel title={t("stanceTitle")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("stanceHelp")}</p>
      <label className="block text-sm font-semibold">{t("fields.channel_stance")}
        <textarea className={fieldClass} rows={8} maxLength={4000} value={draft.channel_stance} disabled={disabled} placeholder={t("stancePlaceholder")} onChange={(event) => edit({ channel_stance: event.target.value })} />
      </label>
    </Panel>
    <Panel title={t("fields.topic_avoid")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("avoidHelp")} {t("onePerLine")}</p>
      <label className="block text-sm font-semibold">{t("fields.topic_avoid")}<textarea className={fieldClass} rows={4} value={avoid} disabled={disabled} onChange={(event) => { setAvoid(event.target.value); touch(); }} /></label>
    </Panel>
    <Panel title={t("tokenTitle")}>
      {view.usage && <p className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">{t("usageTokens", {
        tokens: view.usage.tokens.toLocaleString(), tokenBudget: view.usage.token_budget.toLocaleString(),
        planTokens: (view.usage.subscription_tokens ?? 0).toLocaleString(), calls: view.usage.calls, failed: view.usage.failed_calls,
      })}</p>}
      <label className="block text-sm font-semibold md:w-1/2">{t("fields.monthly_token_budget_millions")}
        <input className={fieldClass} type="number" min={1} max={500} value={draft.monthly_token_budget_millions} disabled={disabled} onChange={(event) => edit({ monthly_token_budget_millions: Number(event.target.value) })} />
      </label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("budgetHelp")}</p>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("subscriptionHelp")}</p>
    </Panel>
    <SaveRow label={t("saveShared")} busy={busy} saved={saved} error={error} disabled={disabled} onSave={() => void submit()} />
  </div>;
}

export function AdminVideoSettings() {
  const t = useTranslations("admin.videoSettings");
  const tabs = useTranslations("admin.videoReviews");
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<VideoSettingsView | null>(null);
  const [prompts, setPrompts] = useState<StagePrompt[] | null>(null);
  const [error, setError] = useState("");
  const [section, setSection] = useAdminQueryState("section", SECTIONS, "tutorial");
  const load = useCallback(() => {
    api<VideoSettingsView>("/admin/video-automation/settings").then((value) => { setView(value); setError(""); }).catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
    // The prompts as the worker last sent them; a site from before they were kept answers 404.
    api<{ prompts: StagePrompt[] }>("/admin/video-automation/prompts").then((value) => setPrompts(value.prompts ?? [])).catch(() => setPrompts([]));
  }, []);
  useEffect(load, [load]);

  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!view) return <p className="mt-6 text-[var(--muted)]">{t("loading")}</p>;
  const props: SectionProps = { view, prompts: prompts ?? [], canManage: manage.allowed, onSaved: setView };
  // The tabs follow the URL through adminNavigate. A plain link would change the address without
  // switching the tab: a pushState fires none of the events the tab state listens for.
  const openDramaTab = () => {
    const target = new URL(window.location.href);
    target.searchParams.set("tab", "drama");
    target.searchParams.delete("section");
    adminNavigate(target);
  };
  return <div className="mt-6 grid gap-5">
    <SettingsPermissionNotice capability="settings.manage" />
    <section className={`${panelClass} grid gap-3`} aria-labelledby="video-settings-drama">
      <h2 id="video-settings-drama" className="text-xl font-bold">{t("dramaTitle")}</h2>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaMoved", { tab: tabs("tabDrama") })}</p>
      <div><Button secondary onClick={openDramaTab}>{t("dramaMovedLink", { tab: tabs("tabDrama") })}</Button></div>
    </section>
    <Tabs value={section} onChange={(value) => setSection(value as Section)} label={t("sectionsLabel")} items={SECTIONS.map((each) => ({ value: each, label: t(`sections.${each}`) }))}>
      {section === "tutorial" && <AdminVideoSettingsTutorial {...props} />}
      {section === "shared" && <SharedSettings {...props} />}
    </Tabs>
  </div>;
}
