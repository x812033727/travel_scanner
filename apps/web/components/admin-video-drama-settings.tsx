"use client";

import { useLocale, useTranslations } from "next-intl";
import { useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import {
  type DramaSettings, dramaSaveBody, MEDIA_PROVIDERS, mediaChoice, type MediaOptions, type MediaProvider, mediaProviderLabels,
  SettingsPermissionNotice, STYLE_PRESETS, type VideoSettingsView,
} from "@/components/admin-video-settings";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { settingsHref } from "@/lib/admin-settings-ownership";
import { api } from "@/lib/api";

// The drama's numbers, with the API's bounds; the budgets open wide on purpose (the owner chose
// to start without a cap on 2026-09-26 and to lower them after the pilot).
const dramaNumberFields = {
  shape: [["max_clips_per_video", 1, 120], ["max_retakes_per_shot", 0, 5], ["judge_min_score", 0, 10]],
  budget: [["monthly_clip_seconds_budget", 0, 100_000], ["monthly_images_budget", 0, 100_000], ["monthly_judge_calls_budget", 0, 100_000], ["monthly_music_budget", 0, 100_000], ["max_usd_per_video", 0, 10_000]],
} as const;
type DramaNumberField = (typeof dramaNumberFields)[keyof typeof dramaNumberFields][number][0];

/**
 * The media vendors the chosen models need and the site has no key for, in the catalog's order.
 * The API refuses to turn the route on while any of them is missing (settings.py drama_problems),
 * so the tab says so before the owner presses save.
 */
export function missingMediaKeys(drama: Pick<DramaSettings, "image_provider" | "clip_provider" | "music_provider">, configured: readonly string[]): MediaProvider[] {
  const wanted = new Set<string>([drama.image_provider, drama.clip_provider, drama.music_provider]);
  return MEDIA_PROVIDERS.filter((provider) => wanted.has(provider) && !configured.includes(provider));
}

/**
 * The drama route's settings, on the drama tab beside the series and the one-off requests
 * (docs/videos/DRAMA.md). The parent reads the settings once and hands them in, so the tab's
 * minute-by-minute refresh never throws away what the owner is typing. A save sends the settings
 * as the API stored them a moment ago with only the drama block replaced, then hands back what
 * the API answered.
 */
export function AdminVideoDramaSettings({ view, onSaved }: { view: VideoSettingsView; onSaved: (view: VideoSettingsView) => void }) {
  const t = useTranslations("admin.videoSettings");
  const locale = useLocale();
  const manage = useAdminActionGuard("settings.manage");
  const [drama, setDrama] = useState<DramaSettings>(view.drama);
  const [dramaScope, setDramaScope] = useState((view.drama.drama_topic_scope ?? []).join("\n"));
  // Open while the route is off, so the switch that starts everything is the first thing in view.
  const [open] = useState(!view.drama.drama_enabled);
  const [saveError, setSaveError] = useState("");
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  const disabled = !manage.allowed || busy;
  const editDrama = (change: Partial<DramaSettings>) => { setDrama({ ...drama, ...change }); setSaved(false); };
  const numberInput = ([key, min, max]: readonly [DramaNumberField, number, number]) => <label key={key} className="block text-sm font-semibold">{t(`fields.drama_${key}`)}
    <input className={fieldClass} type="number" min={min} max={max} value={drama[key]} disabled={disabled} onChange={(event) => editDrama({ [key]: Number(event.target.value) })} />
  </label>;
  const configured = (provider: MediaProvider) => view.configured_providers.includes(provider);
  const clipModel = mediaChoice(view.media_options, "clips", drama.clip_provider, drama.clip_model);
  const missing = drama.drama_enabled ? missingMediaKeys(drama, view.configured_providers) : [];
  /** One vendor select and one model select for a kind of media, the model list following the vendor. */
  const mediaPicker = (kind: keyof MediaOptions, providerKey: "image_provider" | "clip_provider" | "music_provider", modelKey: "image_model" | "clip_model" | "music_model") => {
    const models = view.media_options?.[kind]?.[drama[providerKey]] ?? [];
    return <div key={kind} className="grid gap-3 md:grid-cols-2">
      <label className="block text-sm font-semibold">{t(`fields.drama_${providerKey}`)}
        <select className={fieldClass} value={drama[providerKey]} disabled={disabled} onChange={(event) => {
          const provider = event.target.value as MediaProvider;
          const first = view.media_options?.[kind]?.[provider]?.[0];
          editDrama({ [providerKey]: provider, [modelKey]: first?.value ?? drama[modelKey], ...(kind === "clips" && first ? { clip_resolution: first.resolutions[0] ?? drama.clip_resolution, clip_seconds_default: first.durations.includes(drama.clip_seconds_default) ? drama.clip_seconds_default : (first.durations[0] ?? drama.clip_seconds_default) } : {}) });
        }}>
          {MEDIA_PROVIDERS.map((provider) => <option key={provider} value={provider}>{mediaProviderLabels[provider]}{configured(provider) ? "" : ` (${t("noKey")})`}</option>)}
        </select>
      </label>
      <label className="block text-sm font-semibold">{t(`fields.drama_${modelKey}`)}
        <select className={fieldClass} value={drama[modelKey]} disabled={disabled} onChange={(event) => {
          const chosen = models.find((option) => option.value === event.target.value);
          editDrama({ [modelKey]: event.target.value, ...(kind === "clips" && chosen ? { clip_resolution: chosen.resolutions.includes(drama.clip_resolution) ? drama.clip_resolution : (chosen.resolutions[0] ?? drama.clip_resolution), clip_seconds_default: chosen.durations.includes(drama.clip_seconds_default) ? drama.clip_seconds_default : (chosen.durations[0] ?? drama.clip_seconds_default) } : {}) });
        }}>
          {!models.some((option) => option.value === drama[modelKey]) && <option value={drama[modelKey]}>{drama[modelKey]}</option>}
          {models.map((option) => <option key={option.value} value={option.value}>{option.label}{option.status === "preview" ? ` (${t("preview")})` : ""}{option.usd_per_second ? ` · US$${option.usd_per_second}/s` : option.usd_per_image ? ` · US$${option.usd_per_image}` : option.usd_per_track ? ` · US$${option.usd_per_track}` : ""}</option>)}
        </select>
      </label>
    </div>;
  };
  const voiceInPool = (name: string) => drama.character_voice_pool.some((voice) => voice.provider === "gemini" && voice.name === name);

  async function save() {
    setBusy(true);
    setSaveError("");
    try {
      // Read the stored settings again, so the settings tab's fields go back exactly as they are now.
      const current = await api<VideoSettingsView>("/admin/video-automation/settings");
      const next = await api<VideoSettingsView>("/admin/video-automation/settings", { method: "PUT", body: JSON.stringify(dramaSaveBody(current, drama, dramaScope)) });
      setSaved(true);
      onSaved(next);
    } catch (problem) {
      setSaveError(problem instanceof Error ? problem.message : t("saveError"));
    } finally {
      setBusy(false);
    }
  }

  return <details className={panelClass} open={open}>
    <summary className="cursor-pointer text-lg font-bold">{t("dramaSettingsTitle")}</summary>
    <div className="mt-4 grid gap-4">
      <SettingsPermissionNotice capability="settings.manage" />
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama.drama_enabled} disabled={disabled} onChange={(event) => editDrama({ drama_enabled: event.target.checked })} />{t("fields.drama_enabled")}</label>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaHelp")}</p>
      {missing.length > 0 && <p role="alert" className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3 text-sm leading-6">
        {t("dramaKeyWarning", { vendors: new Intl.ListFormat(locale, { type: "conjunction" }).format(missing.map((provider) => mediaProviderLabels[provider])) })}{" "}
        <Link href={settingsHref("providers", "ai_vendors")} className="font-semibold text-[var(--teal)] underline">{t("dramaKeyLink")}</Link>
      </p>}
      <fieldset className="grid gap-3"><legend className="mb-1 text-sm font-semibold">{t("dramaModels")}</legend>
        {mediaPicker("images", "image_provider", "image_model")}
        {mediaPicker("clips", "clip_provider", "clip_model")}
        {mediaPicker("music", "music_provider", "music_model")}
      </fieldset>
      <div className="grid gap-3 md:grid-cols-3">
        <label className="block text-sm font-semibold">{t("fields.drama_clip_resolution")}
          <select className={fieldClass} value={drama.clip_resolution} disabled={disabled} onChange={(event) => editDrama({ clip_resolution: event.target.value })}>
            {!(clipModel?.resolutions ?? []).includes(drama.clip_resolution) && <option value={drama.clip_resolution}>{drama.clip_resolution}</option>}
            {(clipModel?.resolutions ?? []).map((resolution) => <option key={resolution} value={resolution}>{resolution}</option>)}
          </select>
        </label>
        <label className="block text-sm font-semibold">{t("fields.drama_clip_seconds_default")}
          <select className={fieldClass} value={drama.clip_seconds_default} disabled={disabled} onChange={(event) => editDrama({ clip_seconds_default: Number(event.target.value) })}>
            {!(clipModel?.durations ?? []).includes(drama.clip_seconds_default) && <option value={drama.clip_seconds_default}>{drama.clip_seconds_default}</option>}
            {(clipModel?.durations ?? []).map((seconds) => <option key={seconds} value={seconds}>{seconds}</option>)}
          </select>
        </label>
        <label className="block text-sm font-semibold">{t("fields.drama_aspect")}
          <select className={fieldClass} value={drama.drama_aspect} disabled={disabled} onChange={(event) => editDrama({ drama_aspect: event.target.value as DramaSettings["drama_aspect"] })}>
            <option value="16:9">16:9</option><option value="9:16">9:16</option>
          </select>
        </label>
      </div>
      <div className="grid gap-3 md:grid-cols-3">
        <label className="block text-sm font-semibold">{t("fields.drama_style_preset")}
          <select className={fieldClass} value={drama.style_preset} disabled={disabled} onChange={(event) => editDrama({ style_preset: event.target.value as DramaSettings["style_preset"] })}>
            {(view.style_presets ?? [...STYLE_PRESETS]).map((preset) => <option key={preset} value={preset}>{t(`stylePresets.${preset}`)}</option>)}
          </select>
        </label>
        {dramaNumberFields.shape.map(numberInput)}
      </div>
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("dramaSwitches")}</legend>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.music_enabled} disabled={disabled} onChange={(event) => editDrama({ music_enabled: event.target.checked })} />{t("fields.drama_music_enabled")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.subtitle_burn_in} disabled={disabled} onChange={(event) => editDrama({ subtitle_burn_in: event.target.checked })} />{t("fields.drama_subtitle_burn_in")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.clip_native_audio} disabled={disabled} onChange={(event) => editDrama({ clip_native_audio: event.target.checked })} />{t("fields.drama_clip_native_audio")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.auto_approve_storyboard} disabled={disabled} onChange={(event) => editDrama({ auto_approve_storyboard: event.target.checked })} />{t("fields.drama_auto_approve_storyboard")}</label>
        <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={drama.auto_pick_look} disabled={disabled} onChange={(event) => editDrama({ auto_pick_look: event.target.checked })} />{t("fields.drama_auto_pick_look")}</label>
      </fieldset>
      <fieldset className="flex flex-wrap gap-5"><legend className="mb-2 text-sm font-semibold">{t("fields.drama_character_voice_pool")}</legend>
        {view.voice_options.gemini.map((name) => <label key={name} className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={voiceInPool(name)} disabled={disabled}
          onChange={(event) => editDrama({ character_voice_pool: event.target.checked ? [...drama.character_voice_pool, { provider: "gemini", name }] : drama.character_voice_pool.filter((voice) => !(voice.provider === "gemini" && voice.name === name)) })} />{name}</label>)}
      </fieldset>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("voicePoolHelp")}</p>
      <div className="grid gap-3 md:grid-cols-2">{dramaNumberFields.budget.map(numberInput)}</div>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaBudgetHelp")}</p>
      <label className="block text-sm font-semibold">{t("fields.drama_topic_scope")}<textarea className={fieldClass} rows={3} value={dramaScope} disabled={disabled} onChange={(event) => { setDramaScope(event.target.value); setSaved(false); }} /></label>
      {saveError && <p role="alert" className="text-sm text-red-800">{saveError}</p>}
      {saved && <p role="status" className="text-sm text-[var(--teal)]">{t("saved")}</p>}
      <div><Button disabled={disabled} onClick={() => void save()}>{busy ? t("saving") : t("dramaSave")}</Button></div>
    </div>
  </details>;
}
