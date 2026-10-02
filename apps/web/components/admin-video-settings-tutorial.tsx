"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";
import {
  InstructionFields, LocaleDefaults, MEDIA_PROVIDERS, mediaProviderLabels, Panel, PromptsList, SaveRow, type SectionProps, settingsBody,
  type SlidesSettings, StageModelList, tutorialBody, useSettingsSave, type VideoSettings, type Voice, VoiceFields,
} from "@/components/admin-video-settings";
import { fieldClass } from "@/components/community/ui";

// The tutorial part of the settings tab (docs/videos/DRAMA-FLOW.md, section 1): the schedule and
// topics, the stage models (read only), the standing instructions, the channel voice and the
// video's shape, the illustrated slides' pictures (docs/videos/ILLUSTRATED.md), the budget and
// rounds, the approvals, and the prompts last sent for a slides video. It saves only these fields;
// the drama and the shared parts are their own components.
const numberFields = {
  schedule: [["draft_interval_hours", 6, 720], ["topics_per_run", 1, 3], ["max_waiting_drafts", 1, 10]],
  // Every slides video runs at least eight minutes (apps/api migration 0117).
  length: [["target_minutes_min", 8, 30], ["target_minutes_max", 8, 30]],
  budget: [["max_drafts_per_month", 0, 60], ["max_verify_rounds", 1, 5], ["max_retake_rounds", 0, 5]],
} as const;
type NumberField = (typeof numberFields)[keyof typeof numberFields][number][0];

export function AdminVideoSettingsTutorial({ view, prompts, canManage, onSaved }: SectionProps) {
  const t = useTranslations("admin.videoSettings");
  const [draft, setDraft] = useState<VideoSettings>(() => settingsBody(view));
  const [scope, setScope] = useState(() => view.topic_scope.join("\n"));
  const { busy, error, saved, save, touch } = useSettingsSave(onSaved);
  const disabled = !canManage || busy;
  const edit = (change: Partial<VideoSettings>) => { setDraft((current) => ({ ...current, ...change })); touch(); };
  const setVoice = (change: Partial<Voice>) => edit({ voice: { ...draft.voice, ...change } });
  const slides = draft.slides;
  const editSlides = (change: Partial<SlidesSettings>) => edit({ slides: { ...slides, ...change } });
  // Every image model the catalog offers, whichever vendor serves it; "" follows the drama's choice.
  const imageModels = MEDIA_PROVIDERS.flatMap((provider) => (view.media_options?.images?.[provider] ?? []).map((option) => ({ ...option, provider })));
  const imageMissing = slides.slides_image_model !== null && !imageModels.some((option) => option.value === slides.slides_image_model);
  const imageVendor = imageModels.find((option) => option.value === slides.slides_image_model)?.provider ?? draft.drama.image_provider;
  const imageKeyMissing = slides.slides_media_enabled && !view.configured_providers.includes(imageVendor);
  const text = (value: string) => (value.trim() === "" ? null : value.trim());
  const numberInput = ([key, min, max]: readonly [NumberField, number, number]) => <label key={key} className="block text-sm font-semibold">{t(`fields.${key}`)}
    <input className={fieldClass} type="number" min={min} max={max} value={draft[key]} disabled={disabled} onChange={(event) => edit({ [key]: Number(event.target.value) })} />
  </label>;
  const submit = async () => {
    const next = await save(tutorialBody(draft, scope));
    if (next) { setDraft(settingsBody(next)); setScope(next.topic_scope.join("\n")); }
  };

  return <div className="grid gap-5">
    <p className="text-sm leading-6 text-[var(--muted)]">{t("tutorialHelp")}</p>
    <Panel title={t("scheduleTitle")}>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.enabled} disabled={disabled} onChange={(event) => edit({ enabled: event.target.checked })} />{t("fields.enabled")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("enabledHelp")}</p>
      <div className="grid gap-3 md:grid-cols-3">{numberFields.schedule.map(numberInput)}</div>
      <label className="block text-sm font-semibold">{t("fields.topic_scope")}<textarea className={fieldClass} rows={4} value={scope} disabled={disabled} onChange={(event) => { setScope(event.target.value); touch(); }} /></label>
      <p className="text-sm text-[var(--muted)]">{t("onePerLine")} {t("avoidElsewhere")}</p>
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("topicSources")}</legend>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={draft.topic_from_site} disabled={disabled} onChange={(event) => edit({ topic_from_site: event.target.checked })} />{t("fields.topic_from_site")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={draft.topic_from_search} disabled={disabled} onChange={(event) => edit({ topic_from_search: event.target.checked })} />{t("fields.topic_from_search")}</label>
      </fieldset>
    </Panel>

    <StageModelList models={draft.stage_models} view={view} />

    <InstructionFields instructions={draft.stage_instructions} disabled={disabled} help={t("instructionsHelp")} onChange={(stage_instructions) => edit({ stage_instructions })} />

    <Panel title={t("videoTitle")}>
      <VoiceFields voice={draft.voice} options={view.voice_options} disabled={disabled} onChange={setVoice} />
      <div className="grid gap-3 md:grid-cols-2">{numberFields.length.map(numberInput)}</div>
      <LocaleDefaults locales={draft.caption_locales} disabled={disabled} onChange={(caption_locales) => edit({ caption_locales })} />
    </Panel>

    <Panel title={t("slidesTitle")}>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={slides.slides_media_enabled} disabled={disabled} onChange={(event) => editSlides({ slides_media_enabled: event.target.checked })} />{t("fields.slides_media_enabled")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("slidesHelp")}</p>
      {imageKeyMissing && <p role="alert" className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3 text-sm leading-6">{t("slidesKeyWarning", { vendor: mediaProviderLabels[imageVendor] })}</p>}
      <div className="grid gap-3 md:grid-cols-2">
        <label className="block text-sm font-semibold">{t("fields.slides_image_model")}
          <select className={fieldClass} value={slides.slides_image_model ?? ""} disabled={disabled} onChange={(event) => editSlides({ slides_image_model: event.target.value === "" ? null : event.target.value })}>
            <option value="">{t("slidesImageFollows")}</option>
            {imageMissing && slides.slides_image_model && <option value={slides.slides_image_model}>{slides.slides_image_model}</option>}
            {imageModels.map((option) => <option key={`${option.provider}:${option.value}`} value={option.value}>{option.label} · {mediaProviderLabels[option.provider]}{option.usd_per_image ? ` · US$${option.usd_per_image}` : ""}</option>)}
          </select>
        </label>
        <label className="block text-sm font-semibold">{t("fields.slides_max_usd_per_video")}
          <input className={fieldClass} type="number" min={0} max={10_000} value={slides.slides_max_usd_per_video} disabled={disabled} onChange={(event) => editSlides({ slides_max_usd_per_video: Number(event.target.value) })} />
        </label>
        <label className="block text-sm font-semibold">{t("fields.slides_music_track")}
          <input className={fieldClass} type="text" value={slides.slides_music_track ?? ""} placeholder="bed.mp3" disabled={disabled} onChange={(event) => editSlides({ slides_music_track: text(event.target.value) })} />
        </label>
        <label className="block text-sm font-semibold">{t("fields.slides_sfx_set")}
          <input className={fieldClass} type="text" value={slides.slides_sfx_set ?? ""} placeholder="studio-a" disabled={disabled} onChange={(event) => editSlides({ slides_sfx_set: text(event.target.value) })} />
        </label>
      </div>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={slides.slides_auto_approve_storyboard} disabled={disabled} onChange={(event) => editSlides({ slides_auto_approve_storyboard: event.target.checked })} />{t("fields.slides_auto_approve_storyboard")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("slidesMediaHelp")}</p>
    </Panel>

    <Panel title={t("budgetTitle")}>
      {view.usage && <p className="rounded-xl bg-[var(--paper)] p-3 text-sm leading-6">{t("usageDrafts", { drafts: view.usage.drafts, draftBudget: view.usage.draft_budget })}</p>}
      <div className="grid gap-3 md:grid-cols-3">{numberFields.budget.map(numberInput)}</div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("budgetHelp")}</p>
    </Panel>

    <Panel title={t("gatesTitle")}>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.auto_approve_audio} disabled={disabled} onChange={(event) => edit({ auto_approve_audio: event.target.checked })} />{t("fields.auto_approve_audio")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.auto_pick_outline} disabled={disabled} onChange={(event) => edit({ auto_pick_outline: event.target.checked })} />{t("fields.auto_pick_outline")}</label>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={draft.auto_approve_final} disabled={disabled} onChange={(event) => edit({ auto_approve_final: event.target.checked })} />{t("fields.auto_approve_final")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("gatesHelp")}</p>
    </Panel>

    <PromptsList prompts={prompts} format="slides" />

    <SaveRow label={t("saveTutorial")} busy={busy} saved={saved} error={error} disabled={disabled} onSave={() => void submit()} />
  </div>;
}
