"use client";

import { useCallback, useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { AdminErrorState } from "@/components/admin-ui";
import { Button, fieldClass, panelClass } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { adminNewsCopy, fillNewsCopy, type AdminNewsCopy } from "@/lib/admin-news-copy";
import { newsProviderLabels, newsProviders, type NewsModelOption, type NewsProvider, type NewsSettings } from "@/lib/admin-news";
import { api } from "@/lib/api";

const customModel = "__custom__";
const kinds = ["writer", "verifier", "editor"] as const;
type Models = Pick<NewsSettings, "writer_provider" | "writer_model" | "verifier_provider" | "verifier_model" | "editor_provider" | "editor_model">;

export function newsModels(settings: NewsSettings): Models {
  const { writer_provider, writer_model, verifier_provider, verifier_model, editor_provider, editor_model } = settings;
  return { writer_provider, writer_model, verifier_provider, verifier_model, editor_provider, editor_model };
}

/** The label of the model a writer or verifier runs on, with the fallback spelled out. */
export function newsModelLabel(settings: NewsSettings, kind: (typeof kinds)[number], copy: AdminNewsCopy): string {
  const provider = settings[`${kind}_provider`];
  const options = settings.model_options?.[provider] ?? [];
  const chosen = settings[`${kind}_model`];
  const label = (value: string | undefined) => options.find((option) => option.value === value)?.label ?? value ?? "";
  return chosen ? label(chosen) : fillNewsCopy(copy.modelInherited, { model: label(settings.default_models?.[provider]) || copy.defaultModel });
}

// Keyed by vendor at the call site, so switching vendors also leaves "custom" mode.
function NewsModelField({ label, value, options, fallback, copy, disabled, onChange }: {
  label: string; value: string | null; options: NewsModelOption[]; fallback: string | undefined;
  copy: AdminNewsCopy; disabled: boolean; onChange: (value: string | null) => void;
}) {
  const [customChosen, setCustomChosen] = useState(false);
  const selected = options.find((option) => option.value === value);
  const custom = customChosen || (value !== null && !selected);
  const optionLabel = (option: NewsModelOption) => option.status === "stable"
    ? option.label
    : `${option.label} (${option.status === "preview" ? copy.previewModel : copy.retiredModel})`;
  const fallbackLabel = options.find((option) => option.value === fallback)?.label ?? fallback;
  const description = selected?.description ?? (value === null
    ? options.find((option) => option.value === fallback)?.description
    : undefined);
  return <div>
    <label className="block">{label}<select className={fieldClass} value={custom ? customModel : value ?? ""} disabled={disabled} onChange={(event) => {
      const next = event.target.value;
      setCustomChosen(next === customModel);
      if (next !== customModel) onChange(next || null);
    }}>
      <option value="">{fallbackLabel ? `${copy.defaultModel} · ${fallbackLabel}` : copy.defaultModel}</option>
      {options.map((option) => <option key={option.value} value={option.value}>{optionLabel(option)}</option>)}
      <option value={customModel}>{copy.customModel}</option>
    </select></label>
    {custom && <input className={`${fieldClass} font-mono text-sm`} aria-label={`${label} · ${copy.customModelLabel}`} placeholder="model-id" value={value ?? ""} disabled={disabled} onChange={(event) => onChange(event.target.value.trim() || null)} />}
    {description && <p className="mt-1 text-xs text-[var(--muted)]">{description}</p>}
  </div>;
}

/**
 * The news writer, verifier and final editor models, on the AI settings page. They save through their own
 * route, so the rest of the news settings stay on /admin/news and neither page overwrites the
 * other's fields.
 */
export function AdminNewsModelSettings({ onSaved }: { onSaved?: (settings: NewsSettings) => void }) {
  const copy = adminNewsCopy(useLocale());
  const manage = useAdminActionGuard("content.manage");
  const [settings, setSettings] = useState<NewsSettings>();
  const [draft, setDraft] = useState<Models>();
  const [error, setError] = useState("");
  const [saveError, setSaveError] = useState("");
  const [saved, setSaved] = useState(false);
  const [busy, setBusy] = useState(false);
  const show = useCallback((value: NewsSettings) => { setSettings(value); setDraft(newsModels(value)); }, []);
  const load = useCallback(() => {
    api<NewsSettings>("/admin/news/settings").then((value) => { show(value); setError(""); })
      .catch((problem: unknown) => setError(problem instanceof Error ? problem.message : ""));
  }, [show]);
  useEffect(load, [load]);

  if (error) return <AdminErrorState title={copy.modelsTitle} detail={error} retry={load} retryLabel={copy.retry} />;
  if (!settings || !draft) return <p className="text-[var(--muted)]">{copy.loading}</p>;
  const disabled = !manage.allowed || busy;

  async function save() {
    if (!draft) return;
    setBusy(true);
    setSaveError("");
    try {
      const next = await api<NewsSettings>("/admin/news/settings/models", { method: "PUT", body: JSON.stringify(draft) });
      show(next);
      setSaved(true);
      onSaved?.(next);
    } catch (problem) {
      setSaveError(problem instanceof Error ? problem.message : "");
    } finally {
      setBusy(false);
    }
  }

  return <section id="ai-models-news" className={`${panelClass} grid gap-4 scroll-mt-24`} aria-labelledby="ai-models-news-title">
    <div className="flex flex-wrap items-baseline justify-between gap-2">
      <h2 id="ai-models-news-title" className="text-xl font-bold">{copy.modelsTitle}</h2>
      <Link href="/admin/news?tab=settings" className="inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline">{copy.openNews}</Link>
    </div>
    <p className="text-sm leading-6 text-[var(--muted)]">{copy.modelsShadowNote}</p>
    <div className="grid gap-3 md:grid-cols-3">{kinds.map((kind) => {
      const provider = draft[`${kind}_provider`];
      return <fieldset key={kind} className="space-y-3 rounded-xl border border-[var(--line)] p-4">
        <legend className="px-1 font-bold">{copy[kind]}</legend>
        <label className="block">{copy.provider}<select className={fieldClass} value={provider} disabled={disabled} onChange={(event) => { setDraft({ ...draft, [`${kind}_provider`]: event.target.value as NewsProvider, [`${kind}_model`]: null }); setSaved(false); }}>{newsProviders.map((value) => <option key={value} value={value}>{newsProviderLabels[value]}</option>)}</select></label>
        <NewsModelField key={provider} label={copy.model} value={draft[`${kind}_model`]} options={settings.model_options?.[provider] ?? []}
          fallback={settings.default_models?.[provider]} copy={copy} disabled={disabled} onChange={(value) => { setDraft({ ...draft, [`${kind}_model`]: value }); setSaved(false); }} />
      </fieldset>;
    })}</div>
    {saveError && <p role="alert" className="text-sm text-red-800">{saveError}</p>}
    {saved && <p role="status" className="text-sm text-[var(--teal)]">{copy.saved}</p>}
    <div><Button disabled={disabled} onClick={() => void save()}>{copy.saveModels}</Button></div>
  </section>;
}
