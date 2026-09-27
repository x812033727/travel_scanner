"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";
import {
  dramaBody, type DramaSettings, InstructionFields, LocaleDefaults, MEDIA_PROVIDERS, type MediaOptions, type MediaProvider, mediaChoice,
  mediaProviderLabels, normalizeDrama, Panel, PromptsList, SaveRow, type SectionProps, StageModelList, STYLE_PRESETS, useSettingsSave,
  type Voice, VoiceFields,
} from "@/components/admin-video-settings";
import { fieldClass } from "@/components/community/ui";

// The drama part of the settings tab (docs/videos/DRAMA-FLOW.md, section 1): the switch and topics,
// the drama's own stage models (read only), standing instructions, narrator voice and language
// defaults, the media models and the clip's shape, the rounds, the approvals, the series' pace,
// the budgets and the prompts last sent for a drama. It saves the drama object alone.
// The numbers carry the API's bounds; the budgets open wide on purpose (the owner chose to start
// without a cap on 2026-09-26 and to lower them after the pilot).
const numberFields = {
  shape: [["max_clips_per_video", 1, 120], ["max_retakes_per_shot", 0, 5], ["judge_min_score", 0, 10]],
  rounds: [["drama_max_verify_rounds", 1, 5], ["drama_max_retake_rounds", 0, 5]],
  series: [["series_max_in_flight", 1, 2], ["series_chapter_ahead", 0, 10], ["series_doc_rewrites", 0, 5], ["series_episodes_per_month", 0, 500]],
  budget: [["monthly_clip_seconds_budget", 0, 100_000], ["monthly_images_budget", 0, 100_000], ["monthly_judge_calls_budget", 0, 100_000], ["monthly_music_budget", 0, 100_000], ["max_usd_per_video", 0, 10_000]],
} as const;
type NumberField = (typeof numberFields)[keyof typeof numberFields][number][0];
// The message key of each number's label. The media and budget labels carry a drama_ prefix from
// when they sat on the tutorial's form; the rounds reuse the tutorial's labels, since the two
// parts never render together; the series' are their own.
const labelKey: Record<NumberField, string> = {
  max_clips_per_video: "drama_max_clips_per_video", max_retakes_per_shot: "drama_max_retakes_per_shot", judge_min_score: "drama_judge_min_score",
  drama_max_verify_rounds: "max_verify_rounds", drama_max_retake_rounds: "max_retake_rounds",
  series_max_in_flight: "series_max_in_flight", series_chapter_ahead: "series_chapter_ahead", series_doc_rewrites: "series_doc_rewrites", series_episodes_per_month: "series_episodes_per_month",
  monthly_clip_seconds_budget: "drama_monthly_clip_seconds_budget", monthly_images_budget: "drama_monthly_images_budget", monthly_judge_calls_budget: "drama_monthly_judge_calls_budget",
  monthly_music_budget: "drama_monthly_music_budget", max_usd_per_video: "drama_max_usd_per_video",
};

export function AdminVideoSettingsDrama({ view, prompts, canManage, onSaved }: SectionProps) {
  const t = useTranslations("admin.videoSettings");
  const [drama, setDrama] = useState<DramaSettings>(() => normalizeDrama(view.drama));
  const [scope, setScope] = useState(() => (view.drama?.drama_topic_scope ?? []).join("\n"));
  const { busy, error, saved, save, touch } = useSettingsSave(onSaved);
  const disabled = !canManage || busy;
  const edit = (change: Partial<DramaSettings>) => { setDrama((current) => ({ ...current, ...change })); touch(); };
  const setVoice = (change: Partial<Voice>) => edit({ drama_voice: { ...(drama.drama_voice ?? view.voice), ...change } });
  const numberInput = ([key, min, max]: readonly [NumberField, number, number]) => <label key={key} className="block text-sm font-semibold">{t(`fields.${labelKey[key]}`)}
    <input className={fieldClass} type="number" min={min} max={max} value={drama[key]} disabled={disabled} onChange={(event) => edit({ [key]: Number(event.target.value) })} />
  </label>;
  const configured = (provider: MediaProvider) => view.configured_providers.includes(provider);
  const clipModel = mediaChoice(view.media_options, "clips", drama.clip_provider, drama.clip_model);
  /** One provider select and one model select for a kind of media, the model list following the provider. */
  const mediaPicker = (kind: keyof MediaOptions, providerKey: "image_provider" | "clip_provider" | "music_provider", modelKey: "image_model" | "clip_model" | "music_model") => {
    const models = view.media_options?.[kind]?.[drama[providerKey]] ?? [];
    return <div key={kind} className="grid gap-3 md:grid-cols-2">
      <label className="block text-sm font-semibold">{t(`fields.drama_${providerKey}`)}
        <select className={fieldClass} value={drama[providerKey]} disabled={disabled} onChange={(event) => {
          const provider = event.target.value as MediaProvider;
          const first = view.media_options?.[kind]?.[provider]?.[0];
          edit({ [providerKey]: provider, [modelKey]: first?.value ?? drama[modelKey], ...(kind === "clips" && first ? { clip_resolution: first.resolutions[0] ?? drama.clip_resolution, clip_seconds_default: first.durations.includes(drama.clip_seconds_default) ? drama.clip_seconds_default : (first.durations[0] ?? drama.clip_seconds_default) } : {}) });
        }}>
          {MEDIA_PROVIDERS.map((provider) => <option key={provider} value={provider}>{mediaProviderLabels[provider]}{configured(provider) ? "" : ` (${t("noKey")})`}</option>)}
        </select>
      </label>
      <label className="block text-sm font-semibold">{t(`fields.drama_${modelKey}`)}
        <select className={fieldClass} value={drama[modelKey]} disabled={disabled} onChange={(event) => {
          const chosen = models.find((option) => option.value === event.target.value);
          edit({ [modelKey]: event.target.value, ...(kind === "clips" && chosen ? { clip_resolution: chosen.resolutions.includes(drama.clip_resolution) ? drama.clip_resolution : (chosen.resolutions[0] ?? drama.clip_resolution), clip_seconds_default: chosen.durations.includes(drama.clip_seconds_default) ? drama.clip_seconds_default : (chosen.durations[0] ?? drama.clip_seconds_default) } : {}) });
        }}>
          {!models.some((option) => option.value === drama[modelKey]) && <option value={drama[modelKey]}>{drama[modelKey]}</option>}
          {models.map((option) => <option key={option.value} value={option.value}>{option.label}{option.status === "preview" ? ` (${t("preview")})` : ""}{option.usd_per_second ? ` · US$${option.usd_per_second}/s` : option.usd_per_image ? ` · US$${option.usd_per_image}` : option.usd_per_track ? ` · US$${option.usd_per_track}` : ""}</option>)}
        </select>
      </label>
    </div>;
  };
  const voiceInPool = (name: string) => drama.character_voice_pool.some((voice) => voice.provider === "gemini" && voice.name === name);
  const submit = async () => {
    const next = await save(dramaBody(drama, scope));
    if (next) { setDrama(normalizeDrama(next.drama)); setScope((next.drama?.drama_topic_scope ?? []).join("\n")); }
  };

  return <div className="grid gap-5">
    <Panel title={t("dramaTitle")}>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.drama_enabled} disabled={disabled} onChange={(event) => edit({ drama_enabled: event.target.checked })} />{t("fields.drama_enabled")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaHelp")}</p>
      <label className="block text-sm font-semibold">{t("fields.drama_topic_scope")}<textarea className={fieldClass} rows={3} value={scope} disabled={disabled} onChange={(event) => { setScope(event.target.value); touch(); }} /></label>
    </Panel>

    <StageModelList models={drama.drama_stage_models ?? view.stage_models} view={view} note={drama.drama_stage_models ? t("dramaModelsOwn") : t("dramaModelsFollow")} />

    <InstructionFields instructions={drama.drama_stage_instructions} disabled={disabled} help={t("dramaInstructionsHelp")} onChange={(drama_stage_instructions) => edit({ drama_stage_instructions })} />

    <Panel title={t("voiceTitle")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaVoiceHelp")}</p>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.drama_voice === null} disabled={disabled} onChange={(event) => edit({ drama_voice: event.target.checked ? null : { ...view.voice } })} />{t("fields.drama_voice_follows")}</label>
      {drama.drama_voice && <VoiceFields voice={drama.drama_voice} options={view.voice_options} disabled={disabled} onChange={setVoice} />}
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("fields.drama_character_voice_pool")}</legend>
        {view.voice_options.gemini.map((name) => <label key={name} className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={voiceInPool(name)} disabled={disabled}
          onChange={(event) => edit({ character_voice_pool: event.target.checked ? [...drama.character_voice_pool, { provider: "gemini", name }] : drama.character_voice_pool.filter((voice) => !(voice.provider === "gemini" && voice.name === name)) })} />{name}</label>)}
      </fieldset>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("voicePoolHelp")}</p>
      <LocaleDefaults locales={drama.drama_caption_locales} disabled={disabled} onChange={(drama_caption_locales) => edit({ drama_caption_locales })} />
    </Panel>

    <Panel title={t("dramaModels")}>
      {mediaPicker("images", "image_provider", "image_model")}
      {mediaPicker("clips", "clip_provider", "clip_model")}
      {mediaPicker("music", "music_provider", "music_model")}
      <div className="grid gap-3 md:grid-cols-3">
        <label className="block text-sm font-semibold">{t("fields.drama_clip_resolution")}
          <select className={fieldClass} value={drama.clip_resolution} disabled={disabled} onChange={(event) => edit({ clip_resolution: event.target.value })}>
            {!(clipModel?.resolutions ?? []).includes(drama.clip_resolution) && <option value={drama.clip_resolution}>{drama.clip_resolution}</option>}
            {(clipModel?.resolutions ?? []).map((resolution) => <option key={resolution} value={resolution}>{resolution}</option>)}
          </select>
        </label>
        <label className="block text-sm font-semibold">{t("fields.drama_clip_seconds_default")}
          <select className={fieldClass} value={drama.clip_seconds_default} disabled={disabled} onChange={(event) => edit({ clip_seconds_default: Number(event.target.value) })}>
            {!(clipModel?.durations ?? []).includes(drama.clip_seconds_default) && <option value={drama.clip_seconds_default}>{drama.clip_seconds_default}</option>}
            {(clipModel?.durations ?? []).map((seconds) => <option key={seconds} value={seconds}>{seconds}</option>)}
          </select>
        </label>
        <label className="block text-sm font-semibold">{t("fields.drama_aspect")}
          <select className={fieldClass} value={drama.drama_aspect} disabled={disabled} onChange={(event) => edit({ drama_aspect: event.target.value as DramaSettings["drama_aspect"] })}>
            <option value="16:9">16:9</option><option value="9:16">9:16</option>
          </select>
        </label>
      </div>
      <div className="grid gap-3 md:grid-cols-4">
        <label className="block text-sm font-semibold">{t("fields.drama_style_preset")}
          <select className={fieldClass} value={drama.style_preset} disabled={disabled} onChange={(event) => edit({ style_preset: event.target.value as DramaSettings["style_preset"] })}>
            {(view.style_presets ?? [...STYLE_PRESETS]).map((preset) => <option key={preset} value={preset}>{t(`stylePresets.${preset}`)}</option>)}
          </select>
        </label>
        {numberFields.shape.map(numberInput)}
      </div>
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("dramaSwitches")}</legend>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.music_enabled} disabled={disabled} onChange={(event) => edit({ music_enabled: event.target.checked })} />{t("fields.drama_music_enabled")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.subtitle_burn_in} disabled={disabled} onChange={(event) => edit({ subtitle_burn_in: event.target.checked })} />{t("fields.drama_subtitle_burn_in")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.clip_native_audio} disabled={disabled} onChange={(event) => edit({ clip_native_audio: event.target.checked })} />{t("fields.drama_clip_native_audio")}</label>
      </fieldset>
    </Panel>

    <Panel title={t("flowTitle")}>
      <div className="grid gap-3 md:grid-cols-2">{numberFields.rounds.map(numberInput)}</div>
    </Panel>

    <Panel title={t("gatesTitle")}>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.series_script_gate} disabled={disabled} onChange={(event) => edit({ series_script_gate: event.target.checked })} />{t("fields.series_script_gate")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.auto_pick_look} disabled={disabled} onChange={(event) => edit({ auto_pick_look: event.target.checked })} />{t("fields.drama_auto_pick_look")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.drama_auto_approve_audio} disabled={disabled} onChange={(event) => edit({ drama_auto_approve_audio: event.target.checked })} />{t("fields.auto_approve_audio")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.auto_approve_storyboard} disabled={disabled} onChange={(event) => edit({ auto_approve_storyboard: event.target.checked })} />{t("fields.drama_auto_approve_storyboard")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.drama_auto_approve_final} disabled={disabled} onChange={(event) => edit({ drama_auto_approve_final: event.target.checked })} />{t("fields.auto_approve_final")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaGatesHelp")}</p>
    </Panel>

    <Panel title={t("seriesTitle")}>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("seriesHelp")}</p>
      <div className="grid gap-3 md:grid-cols-4">{numberFields.series.map(numberInput)}</div>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.series_auto_continue} disabled={disabled} onChange={(event) => edit({ series_auto_continue: event.target.checked })} />{t("fields.series_auto_continue")}</label>
    </Panel>

    <Panel title={t("budgetTitle")}>
      <div className="grid gap-3 md:grid-cols-2">{numberFields.budget.map(numberInput)}</div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaBudgetHelp")}</p>
    </Panel>

    <PromptsList prompts={prompts} format="drama" />

    <SaveRow label={t("saveDrama")} busy={busy} saved={saved} error={error} disabled={disabled} onSave={() => void submit()} />
  </div>;
}
