"use client";

import { useTranslations } from "next-intl";
import { useCallback, useEffect, useState } from "react";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { isVideoSettings } from "@/components/admin-ai-model-overview";
import { AdminErrorState } from "@/components/admin-ui";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { PROVIDERS, STAGES, providerLabels, type Provider, type VideoSettings, type VideoSettingsView } from "@/components/admin-video-settings";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";

type StageModels = VideoSettings["stage_models"];

/**
 * The model of each video stage, on the AI settings page. It saves through its own route, so
 * the rest of the video settings stay on /admin/videos and neither page overwrites the other.
 */
export function AdminVideoModelSettings({ onSaved }: { onSaved?: (view: VideoSettingsView) => void }) {
  const t = useTranslations("admin.videoSettings");
  const manage = useAdminActionGuard("settings.manage");
  const [view, setView] = useState<VideoSettingsView | null>(null);
  const [draft, setDraft] = useState<StageModels | null>(null);
  const [error, setError] = useState("");
  const [saveError, setSaveError] = useState("");
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  const show = useCallback((value: VideoSettingsView) => { setView(value); setDraft(value.stage_models); }, []);
  const load = useCallback(() => {
    api<VideoSettingsView>("/admin/video-automation/settings").then((value) => {
      if (!isVideoSettings(value)) throw new Error(t("loadError"));
      show(value);
      setError("");
    })
      .catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, [show, t]);
  useEffect(load, [load]);

  if (error) return <AdminErrorState title={t("loadError")} detail={error} retry={load} retryLabel={t("retry")} />;
  if (!view || !draft) return <p className="text-[var(--muted)]">{t("loading")}</p>;
  const disabled = !manage.allowed || busy;
  const edit = (models: StageModels) => { setDraft(models); setSaved(false); };

  async function save() {
    if (!draft) return;
    setBusy(true);
    setSaveError("");
    try {
      const next = await api<VideoSettingsView>("/admin/video-automation/settings/models", { method: "PUT", body: JSON.stringify({ stage_models: draft }) });
      show(next);
      setSaved(true);
      onSaved?.(next);
    } catch (problem) {
      setSaveError(problem instanceof Error ? problem.message : t("saveError"));
    } finally {
      setBusy(false);
    }
  }

  return <section id="ai-models-video" className={`${panelClass} grid gap-4 scroll-mt-24`} aria-labelledby="ai-models-video-title">
    <div className="flex flex-wrap items-baseline justify-between gap-2">
      <h2 id="ai-models-video-title" className="text-xl font-bold">{t("modelsTitle")}</h2>
      <Link href="/admin/videos?tab=settings" className="inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline">{t("openVideos")}</Link>
    </div>
    <p className="text-sm leading-6 text-[var(--muted)]">{t("modelsHelp")}</p>
    <div className="grid gap-3 md:grid-cols-2">{STAGES.map((stage) => {
      const choice = draft[stage];
      const options = view.model_options[choice.provider] ?? [];
      const description = options.find((option) => option.value === choice.model)?.description;
      return <fieldset key={stage} className="grid gap-2 rounded-xl border border-[var(--line)] p-4">
        <legend className="px-1 font-bold">{t(`stages.${stage}`)}</legend>
        <label className="block text-sm">{t("provider")}
          <select className={fieldClass} value={choice.provider} disabled={disabled} onChange={(event) => {
            const provider = event.target.value as Provider;
            edit({ ...draft, [stage]: { provider, model: view.model_options[provider]?.[0]?.value ?? "" } });
          }}>{PROVIDERS.map((provider) => <option key={provider} value={provider}>{providerLabels[provider]}{provider === "claude_code" ? ` (${t("subscription")})` : ""}{view.configured_providers.includes(provider) ? "" : ` (${t(provider === "claude_code" ? "agentOff" : "noKey")})`}</option>)}</select>
        </label>
        <label className="block text-sm">{t("model")}
          <select className={fieldClass} value={choice.model} disabled={disabled} onChange={(event) => edit({ ...draft, [stage]: { ...choice, model: event.target.value } })}>
            {options.map((option) => <option key={option.value} value={option.value}>{option.label}</option>)}
          </select>
        </label>
        {description && <p className="text-xs leading-5 text-[var(--muted)]">{description}</p>}
      </fieldset>;
    })}</div>
    {saveError && <p role="alert" className="text-sm text-red-800">{saveError}</p>}
    {saved && <p role="status" className="text-sm text-[var(--teal)]">{t("saved")}</p>}
    <div><Button disabled={disabled} onClick={() => void save()}>{busy ? t("saving") : t("saveModels")}</Button></div>
  </section>;
}
