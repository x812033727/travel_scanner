"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { isVideoSettings } from "@/components/admin-ai-model-overview";
import { AdminErrorState } from "@/components/admin-ui";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { PROVIDERS, STAGES, providerLabels, type Provider, type StageModels, type VideoSettingsView } from "@/components/admin-video-settings";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";

/**
 * The model of each video stage, on the AI settings page. It saves through its own route, so
 * the rest of the video settings stay on /admin/videos and neither page overwrites the other.
 * The drama has its own six choices (docs/videos/DRAMA-FLOW.md, section 1), or follows the tutorial's
 * when "same as the tutorial" is ticked: the route then receives null. The Shorts have the same
 * block (docs/videos/SHORTS.md), stored on the Shorts settings and saved on its own: it sends
 * only `stage_models` to /admin/video-shorts/settings, so the Shorts tab's settings stay as they are.
 */
export function AdminVideoModelSettings({ onSaved }: { onSaved?: (view: VideoSettingsView) => void }) {
  const t = useTranslations("admin.videoSettings");
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<VideoSettingsView | null>(null);
  const [draft, setDraft] = useState<StageModels | null>(null);
  const [drama, setDrama] = useState<StageModels | null>(null);
  const [error, setError] = useState("");
  const [saveError, setSaveError] = useState("");
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  // undefined until the Shorts settings answer; null follows the tutorial's models.
  const [shorts, setShorts] = useState<StageModels | null | undefined>(undefined);
  const [shortsError, setShortsError] = useState("");
  const [shortsSaved, setShortsSaved] = useState(false);
  const show = useCallback((value: VideoSettingsView) => { setView(value); setDraft(value.stage_models); setDrama(value.drama?.drama_stage_models ?? null); }, []);
  const load = useCallback(() => {
    api<VideoSettingsView>("/admin/video-automation/settings").then((value) => {
      if (!isVideoSettings(value)) throw new Error(t("loadError"));
      show(value);
      setError("");
    })
      .catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
    api<ShortsStageModels>("/admin/video-shorts/settings").then((value) => {
      setShorts(value.stage_models ?? null);
      setShortsError("");
    })
      .catch((problem: unknown) => setShortsError(problem instanceof Error && problem.message ? problem.message : t("shortsModelsLoadError")));
  }, [show, t]);
  useEffect(load, [load]);

  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!view || !draft) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  const disabled = !manage.allowed || busy;
  const edit = (models: StageModels) => { setDraft(models); setSaved(false); };
  const editDrama = (models: StageModels | null) => { setDrama(models); setSaved(false); };
  const editShorts = (models: StageModels | null) => { setShorts(models); setShortsSaved(false); };

  async function save() {
    if (!draft) return;
    setBusy(true);
    setSaveError("");
    try {
      const next = await api<VideoSettingsView>("/admin/video-automation/settings/models", { method: "PUT", body: JSON.stringify({ stage_models: draft, drama_stage_models: drama }) });
      show(next);
      setSaved(true);
      onSaved?.(next);
    } catch (problem) {
      setSaveError(problem instanceof Error ? problem.message : t("saveError"));
    } finally {
      setBusy(false);
    }
  }

  async function saveShorts() {
    if (shorts === undefined) return;
    setBusy(true);
    setShortsError("");
    try {
      const next = await api<ShortsStageModels>("/admin/video-shorts/settings", { method: "PUT", body: JSON.stringify({ stage_models: shorts }) });
      setShorts(next.stage_models ?? null);
      setShortsSaved(true);
    } catch (problem) {
      setShortsError(problem instanceof Error ? problem.message : t("saveError"));
    } finally {
      setBusy(false);
    }
  }

  /** One stage's vendor and model selects; `legend` tells a drama's apart from the tutorial's. */
  const stageFields = (models: StageModels, legend: (stage: (typeof STAGES)[number]) => string, change: (models: StageModels) => void) => STAGES.map((stage) => {
    const choice = models[stage];
    const options = view.model_options[choice.provider] ?? [];
    const description = options.find((option) => option.value === choice.model)?.description;
    return <fieldset key={stage} className="grid gap-2 rounded-xl border border-[var(--line)] p-4">
      <legend className="px-1 font-bold">{legend(stage)}</legend>
      <label className="block text-sm">{t("provider")}
        <select className={fieldClass} value={choice.provider} disabled={disabled} onChange={(event) => {
          const provider = event.target.value as Provider;
          change({ ...models, [stage]: { provider, model: view.model_options[provider]?.[0]?.value ?? "" } });
        }}>{PROVIDERS.map((provider) => <option key={provider} value={provider}>{providerLabels[provider]}{provider === "claude_code" || provider === "codex" ? ` (${t("subscription")})` : ""}{view.configured_providers.includes(provider) ? "" : ` (${t(provider === "claude_code" || provider === "codex" ? "agentOff" : "noKey")})`}</option>)}</select>
      </label>
      <label className="block text-sm">{t("model")}
        <select className={fieldClass} value={choice.model} disabled={disabled} onChange={(event) => change({ ...models, [stage]: { ...choice, model: event.target.value } })}>
          {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
        </select>
      </label>
      {description && <p className="text-xs leading-5 text-[var(--muted)]">{description}</p>}
    </fieldset>;
  });

  return <section id="ai-models-video" className={`${panelClass} grid gap-4 scroll-mt-24`} aria-labelledby="ai-models-video-title">
    <div className="flex flex-wrap items-baseline justify-between gap-2">
      <h2 id="ai-models-video-title" className="text-xl font-bold">{t("modelsTitle")}</h2>
      <Link href="/admin/videos?tab=settings" className="inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline">{t("openVideos")}</Link>
    </div>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("modelsHelp")}</p>
    <div className="grid gap-3 md:grid-cols-2">{stageFields(draft, (stage) => t(`stages.${stage}`), edit)}</div>
    <section aria-label={t("dramaModelsTitle")} className="grid gap-3 border-t border-[var(--line)] pt-4">
      <h3 className="text-lg font-bold">{t("dramaModelsTitle")}</h3>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("dramaModelsHelp")}</p>
      <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={drama === null} disabled={disabled} onChange={(event) => editDrama(event.target.checked ? null : { ...draft })} />{t("fields.drama_stage_models_follow")}</label>
      {drama && <div className="grid gap-3 md:grid-cols-2">{stageFields(drama, (stage) => t("dramaStage", { stage: t(`stages.${stage}`) }), editDrama)}</div>}
    </section>
    {saveError && <p role="alert" className="text-sm text-red-800">{saveError}</p>}
    {saved && <p role="status" className="text-sm text-[var(--teal)]">{t("saved")}</p>}
    <div><Button disabled={disabled} onClick={() => void save()}>{busy ? t("saving") : t("saveModels")}</Button></div>
    <section aria-label={t("shortsModelsTitle")} className="grid gap-3 border-t border-[var(--line)] pt-4">
      <h3 className="text-lg font-bold">{t("shortsModelsTitle")}</h3>
      <p className="text-sm leading-6 text-[var(--muted)]">{t("shortsModelsHelp")}</p>
      {shorts !== undefined && <>
        <label className="flex min-h-11 items-center gap-2 font-semibold"><input type="checkbox" checked={shorts === null} disabled={disabled} onChange={(event) => editShorts(event.target.checked ? null : { ...draft })} />{t("shortsModelsFollow")}</label>
        {shorts && <div className="grid gap-3 md:grid-cols-2">{stageFields(shorts, (stage) => t("shortsStage", { stage: t(`stages.${stage}`) }), editShorts)}</div>}
      </>}
      {shortsError && <p role="alert" className="text-sm text-red-800">{shortsError}</p>}
      {shortsSaved && <p role="status" className="text-sm text-[var(--teal)]">{t("saved")}</p>}
      {shorts !== undefined && <div><Button disabled={disabled} onClick={() => void saveShorts()}>{busy ? t("saving") : t("saveShortsModels")}</Button></div>}
    </section>
  </section>;
}

/** The part of the Shorts settings this block reads and writes (apps/api/app/video_shorts/schemas.py). */
type ShortsStageModels = { stage_models: StageModels | null };
