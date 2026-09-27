"use client";

import { useTranslations } from "next-intl";
import { useState } from "react";
import {
  InstructionFields, LocaleDefaults, Panel, PromptsList, SaveRow, type SectionProps, settingsBody, StageModelList, tutorialBody,
  useSettingsSave, type VideoSettings, type Voice, VoiceFields,
} from "@/components/admin-video-settings";
import { fieldClass } from "@/components/community/ui";

// The tutorial part of the settings tab (docs/videos/DRAMA-FLOW.md, section 1): the schedule and
// topics, the stage models (read only), the standing instructions, the channel voice and the
// video's shape, the budget and rounds, the approvals, and the prompts last sent for a slides
// video. It saves only these fields; the drama and the shared parts are their own components.
const numberFields = {
  schedule: [["draft_interval_hours", 6, 720], ["topics_per_run", 1, 3], ["max_waiting_drafts", 1, 10]],
  length: [["target_minutes_min", 3, 30], ["target_minutes_max", 3, 30]],
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
