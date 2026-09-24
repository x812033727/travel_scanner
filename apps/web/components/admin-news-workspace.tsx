"use client";

import { useEffect, useMemo, useState } from "react";
import { useLocale } from "next-intl";
import { AdminReadOnlyNotice, useAdminActionGuard } from "@/components/admin-action-guard";
import { ContentBlocks } from "@/components/content-blocks";
import { Button, Empty, Tabs, fieldClass, panelClass } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { adminNewsCopy } from "@/lib/admin-news-copy";
import {
  newsLocales,
  newsProviderLabels,
  newsProviders,
  type NewsCandidate,
  type NewsCandidatePage,
  type NewsLocale,
  type NewsModelOption,
  type NewsProvider,
  type NewsSettings,
  type NewsSource,
  type NewsStats,
  type NewsVertical,
} from "@/lib/admin-news";
import { useAdminQueryState, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";
import { splitGuideBlocks } from "@/lib/guides";

const tabs = ["review", "sources", "settings", "runs"] as const;
const statusTone: Record<string, string> = {
  manual_review: "bg-amber-100 text-amber-900",
  shadow_review: "bg-sky-100 text-sky-900",
  published: "bg-emerald-100 text-emerald-900",
  failed: "bg-red-100 text-red-900",
};

function problemMessage(problem: unknown, fallback: string) {
  return problem instanceof Error && problem.message ? problem.message : fallback;
}

const customModel = "__custom__";

type Copy = ReturnType<typeof adminNewsCopy>;

// Keyed by vendor at the call site, so switching vendors also leaves "custom" mode.
function NewsModelField({ label, value, options, fallback, copy, onChange }: {
  label: string; value: string | null; options: NewsModelOption[]; fallback: string | undefined;
  copy: Copy; onChange: (value: string | null) => void;
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
    <label className="block">{label}<select className={fieldClass} value={custom ? customModel : value ?? ""} onChange={(event) => {
      const next = event.target.value;
      setCustomChosen(next === customModel);
      if (next !== customModel) onChange(next || null);
    }}>
      <option value="">{fallbackLabel ? `${copy.defaultModel} · ${fallbackLabel}` : copy.defaultModel}</option>
      {options.map((option) => <option key={option.value} value={option.value}>{optionLabel(option)}</option>)}
      <option value={customModel}>{copy.customModel}</option>
    </select></label>
    {custom && <input className={`${fieldClass} font-mono text-sm`} aria-label={`${label} · ${copy.customModelLabel}`} placeholder="model-id" value={value ?? ""} onChange={(event) => onChange(event.target.value.trim() || null)} />}
    {description && <p className="mt-1 text-xs text-[var(--muted)]">{description}</p>}
  </div>;
}

export function AdminNewsWorkspace() {
  const locale = useLocale();
  const copy = adminNewsCopy(locale);
  const manage = useAdminActionGuard("content.manage");
  const [tab, setTab] = useAdminQueryState("tab", tabs, "review");
  const [selected, setSelected] = useAdminQueryValue("candidate", "", (value) => /^[0-9a-f-]{36}$/.test(value));
  const [previewLocale, setPreviewLocale] = useState<NewsLocale>("zh-TW");
  const [candidates, setCandidates] = useState<NewsCandidatePage>();
  const [loadedDetail, setDetail] = useState<NewsCandidate>();
  const detail = selected && loadedDetail?.id === selected ? loadedDetail : undefined;
  const [sources, setSources] = useState<NewsSource[]>([]);
  const [settings, setSettings] = useState<NewsSettings>();
  const [stats, setStats] = useState<NewsStats>();
  const [reason, setReason] = useState("");
  const [majorError, setMajorError] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [reload, setReload] = useState(0);
  const [sourceDraft, setSourceDraft] = useState({
    name: "", url: "", format: "rss", role: "evidence", vertical: "ai", interval: "60",
    firstParty: true, allowedHosts: "", config: "{}",
  });

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      api<NewsCandidatePage>("/admin/news/candidates?limit=100", { signal: controller.signal }),
      api<NewsSource[]>("/admin/news/sources", { signal: controller.signal }),
      api<NewsSettings>("/admin/news/settings", { signal: controller.signal }),
      api<NewsStats>("/admin/news/stats", { signal: controller.signal }),
    ]).then(([queue, sourceRows, configuration, totals]) => {
      if (controller.signal.aborted) return;
      setCandidates(queue); setSources(sourceRows); setSettings(configuration); setStats(totals);
    }).catch((problem) => { if (!controller.signal.aborted) setError(problemMessage(problem, copy.error)); });
    return () => controller.abort();
  }, [copy.error, reload]);

  useEffect(() => {
    if (!selected) return;
    const controller = new AbortController();
    api<NewsCandidate>(`/admin/news/candidates/${selected}`, { signal: controller.signal })
      .then((value) => { if (!controller.signal.aborted) setDetail(value); })
      .catch((problem) => { if (!controller.signal.aborted) setError(problemMessage(problem, copy.error)); });
    return () => controller.abort();
  }, [copy.error, reload, selected]);

  const queue = useMemo(
    () => candidates?.candidates.filter((item) => ["manual_review", "shadow_review", "failed", "published"].includes(item.status)) ?? [],
    [candidates],
  );

  async function run(work: () => Promise<void>) {
    if (!manage.allowed || busy) return;
    setBusy(true); setError(""); setNotice("");
    try { await work(); setReload((value) => value + 1); }
    catch (problem) { setError(problemMessage(problem, copy.error)); }
    finally { setBusy(false); }
  }

  const action = (name: "retry" | "verify" | "reject" | "publish" | "major-error") => run(async () => {
    if (!detail || !reason.trim()) { setError(copy.reason); return; }
    const value = await api<NewsCandidate>(`/admin/news/candidates/${detail.id}/${name}`, {
      method: "POST", body: JSON.stringify({ reason: reason.trim(), major_error: majorError }),
    });
    setDetail(value); setReason(""); setMajorError(false); setNotice(copy.saved);
  });

  const addSource = () => run(async () => {
    await api<NewsSource>("/admin/news/sources", {
      method: "POST",
      body: JSON.stringify({
        name: sourceDraft.name, url: sourceDraft.url, format: sourceDraft.format,
        role: sourceDraft.role, vertical: sourceDraft.vertical,
        is_first_party: sourceDraft.firstParty && sourceDraft.role === "evidence",
        enabled: false, scan_interval_minutes: Number(sourceDraft.interval),
        allowed_redirect_hosts: sourceDraft.allowedHosts.split(",").map((value) => value.trim()).filter(Boolean),
        config: JSON.parse(sourceDraft.config) as Record<string, unknown>,
      }),
    });
    setSourceDraft({ name: "", url: "", format: "rss", role: "evidence", vertical: "ai", interval: "60", firstParty: true, allowedHosts: "", config: "{}" });
    setNotice(copy.saved);
  });

  const patchSource = (source: NewsSource, enabled: boolean) => run(async () => {
    await api<NewsSource>(`/admin/news/sources/${source.id}`, {
      method: "PATCH", body: JSON.stringify({ enabled }),
    });
    setNotice(copy.saved);
  });

  const saveSettings = () => run(async () => {
    if (!settings) return;
    const payload: Record<string, unknown> = { ...settings };
    for (const readOnly of ["gates", "updated_at", "model_options", "default_models"]) delete payload[readOnly];
    setSettings(await api<NewsSettings>("/admin/news/settings", {
      method: "PUT", body: JSON.stringify(payload),
    }));
    setNotice(copy.saved);
  });

  const labels = {
    imageCredit: "", imageDescription: copy.preview, tip: "Tip", warning: "Warning", info: "Info",
    summary: copy.preview, faq: "FAQ",
  };
  const document = detail?.documents[previewLocale];
  const contentBlocks = document
    ? splitGuideBlocks(document.blocks).flatMap((segment) => segment.blocks)
    : [];

  return <div className="space-y-6">
    <header><p className="text-sm font-bold uppercase tracking-[.14em] text-[var(--teal)]">NEWS AUTOMATION</p>
      <h1 className="mt-2 text-3xl font-bold md:text-4xl">{copy.title}</h1>
      <p className="mt-3 max-w-4xl leading-7 text-[var(--muted)]">{copy.description}</p></header>
    <AdminReadOnlyNotice capability="content.manage" />
    {error && <p role="alert" className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-900">{error}</p>}
    {notice && <p role="status" className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-900">{notice}</p>}
    <div className="grid gap-3 sm:grid-cols-3">
      {[[copy.pending, stats?.pending_review ?? 0], [copy.failed, stats?.failed ?? 0], [copy.published, stats?.published ?? 0]].map(([label, value]) =>
        <div key={String(label)} className={panelClass}><p className="text-sm text-[var(--muted)]">{label}</p><p className="mt-1 text-3xl font-bold">{value}</p></div>)}
    </div>
    {stats && <p className="text-sm text-[var(--muted)]">Pipeline runs: {stats.pipeline_runs} · failed: {stats.pipeline_failures} · tokens: {stats.input_tokens}/{stats.output_tokens}</p>}
    <Tabs value={tab} onChange={(value) => setTab(value as typeof tab)} label={copy.title}
      items={tabs.map((value) => ({ value, label: copy[value] }))}>
      {tab === "review" && <div className="grid gap-5 xl:grid-cols-[22rem_minmax(0,1fr)]">
        <section className={`${panelClass} space-y-2`} aria-label={copy.review}>
          {!queue.length ? <Empty>{copy.empty}</Empty> : queue.map((item) => <button type="button" key={item.id}
            onClick={() => setSelected(item.id)} className={`w-full rounded-xl border p-3 text-left ${selected === item.id ? "border-[var(--teal)]" : "border-[var(--line)]"}`}>
            <span className={`rounded-full px-2 py-1 text-xs font-bold ${statusTone[item.status] ?? "bg-[var(--paper)]"}`}>{item.status}</span>
            <strong className="mt-2 block">{item.source_title}</strong><span className="mt-1 block text-xs text-[var(--muted)]">{item.vertical.toUpperCase()} · {item.event_date ?? item.created_at.slice(0, 10)}</span>
          </button>)}
        </section>
        {!detail ? <Empty>{copy.empty}</Empty> : <section className="space-y-5">
          <div className={panelClass}><div className="flex flex-wrap items-center gap-2"><span className={`rounded-full px-2 py-1 text-xs font-bold ${statusTone[detail.status] ?? "bg-[var(--paper)]"}`}>{detail.status}</span><strong>{detail.source_title}</strong></div>
            <a href={detail.canonical_url} target="_blank" rel="noopener noreferrer" className="mt-2 block break-all text-sm text-[var(--teal)] underline">{detail.canonical_url}</a>
            {detail.error_code && <p className="mt-3 text-sm text-red-700">{detail.error_code}: {detail.error_detail}</p>}
          </div>
          <div className={panelClass}><h2 className="text-xl font-bold">{copy.evidence}</h2><div className="mt-3 space-y-3">{detail.evidence.map((item) => <article key={item.id} className="rounded-xl bg-[var(--paper)] p-3">
            <p className="font-semibold">{item.title} · {item.is_first_party ? copy.firstParty : item.role === "lead_only" ? copy.leadOnly : copy.evidence}</p>
            <a href={item.url} target="_blank" rel="noopener noreferrer" className="break-all text-sm text-[var(--teal)] underline">{item.url}</a>
            <p className="mt-2 line-clamp-5 whitespace-pre-wrap text-sm leading-6 text-[var(--muted)]">{item.excerpt}</p><code className="mt-2 block break-all text-xs">sha256:{item.content_hash}</code>
          </article>)}</div></div>
          <div className="grid gap-5 lg:grid-cols-2">
            <div className={panelClass}><h2 className="text-xl font-bold">{copy.claims}</h2>{detail.claim_ledger.length === 0 ? <p className="mt-3 text-sm text-[var(--muted)]">—</p> : <ol className="mt-3 list-decimal space-y-3 pl-5 text-sm">{detail.claim_ledger.map((claim, index) => <li key={`${index}-${String(claim.claim ?? "")}`}><p>{String(claim.claim ?? "")}</p><p className="mt-1 break-all text-xs text-[var(--muted)]">{Array.isArray(claim.source_urls) ? claim.source_urls.join(" · ") : ""}</p></li>)}</ol>}</div>
            <div className={panelClass}><h2 className="text-xl font-bold">{copy.checks}</h2>{Object.keys(detail.lint).length === 0 ? <p className="mt-3 text-sm text-[var(--muted)]">—</p> : <div className="mt-3 space-y-3">{Object.entries(detail.lint).map(([lintLocale, problems]) => <article key={lintLocale}><h3 className="font-semibold">{lintLocale}</h3>{problems.length === 0 ? <p className="text-sm text-emerald-700">0 errors</p> : <ul className="list-disc pl-5 text-sm text-red-700">{problems.map((problem) => <li key={problem}>{problem}</li>)}</ul>}</article>)}</div>}</div>
          </div>
          <div className={panelClass}><h2 className="text-xl font-bold">{copy.preview}</h2><div className="mt-3 flex flex-wrap gap-2">{newsLocales.map((value) => <Button key={value} secondary={previewLocale !== value} onClick={() => setPreviewLocale(value)}>{value}</Button>)}</div>
            {!document ? <p className="mt-4 text-[var(--muted)]">{copy.noDocument}</p> : <article className="mt-5 space-y-4"><h2 className="text-2xl font-bold">{document.title}</h2><p className="text-[var(--muted)]">{document.description}</p><ContentBlocks blocks={contentBlocks} labels={labels} locale={previewLocale} />
              <h3 className="font-bold">{copy.source}</h3><ul className="list-disc pl-5 text-sm">{document.sources.map((item) => <li key={item.url}><a href={item.url} target="_blank" rel="noopener noreferrer" className="text-[var(--teal)] underline">{item.title}</a></li>)}</ul></article>}
            {detail.guide_article_id && <div className="mt-4 flex flex-wrap gap-2">{newsLocales.map((value) => <Link key={value} href={`/admin/guides?article=${detail.guide_article_id}&lang=${value}`} className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-3 font-semibold">{copy.openEditor} · {value}</Link>)}</div>}
          </div>
          <div className={panelClass}><h2 className="text-xl font-bold">{copy.assessments}</h2><div className="mt-3 overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr><th className="p-2">{copy.status}</th><th className="p-2">Locale</th><th className="p-2">{copy.confidence}</th><th className="p-2">Model</th><th className="p-2">{copy.reason}</th></tr></thead><tbody>{detail.assessments.map((item) => <tr key={item.id} className="border-t border-[var(--line)]"><td className="p-2">{item.assessment_type}: {item.verdict}{typeof item.details.tier === "string" ? ` (${item.details.tier})` : ""}</td><td className="p-2">{item.locale ?? "—"}</td><td className="p-2">{item.confidence?.toFixed(3) ?? "—"}</td><td className="p-2">{item.provider ?? "—"} {item.model ?? ""}</td><td className="min-w-64 p-2">{item.reasons.join(" · ") || "—"}</td></tr>)}</tbody></table></div></div>
          <div className={panelClass}><label className="font-semibold">{copy.reason}<textarea className={fieldClass} value={reason} onChange={(event) => setReason(event.target.value)} rows={3} /></label><label className="mt-3 flex min-h-11 items-center gap-2"><input type="checkbox" checked={majorError} onChange={(event) => setMajorError(event.target.checked)} />{copy.majorError}</label>
            <div className="mt-4 flex flex-wrap gap-2">{detail.status === "published" ? <Button disabled={!manage.allowed || busy || !reason.trim() || !majorError} onClick={() => void action("major-error")}>{copy.incident}</Button> : <><Button secondary disabled={!manage.allowed || busy || !reason.trim()} onClick={() => void action("retry")}>{copy.retry}</Button><Button secondary disabled={!manage.allowed || busy || !reason.trim() || !detail.guide_article_id} onClick={() => void action("verify")}>{copy.verify}</Button><Button secondary disabled={!manage.allowed || busy || !reason.trim()} onClick={() => void action("reject")}>{copy.reject}</Button><Button disabled={!manage.allowed || busy || !reason.trim() || !detail.guide_article_id} onClick={() => void action("publish")}>{copy.publish}</Button></>}</div>
          </div>
        </section>}
      </div>}
      {tab === "sources" && <div className="space-y-5"><section className={panelClass}><h2 className="text-xl font-bold">{copy.addSource}</h2><div className="mt-4 grid gap-3 md:grid-cols-2">
        <label>{copy.sourceName}<input className={fieldClass} value={sourceDraft.name} onChange={(event) => setSourceDraft({ ...sourceDraft, name: event.target.value })} /></label><label>{copy.sourceUrl}<input className={fieldClass} type="url" value={sourceDraft.url} onChange={(event) => setSourceDraft({ ...sourceDraft, url: event.target.value })} /></label>
        <label>{copy.format}<select className={fieldClass} value={sourceDraft.format} onChange={(event) => setSourceDraft({ ...sourceDraft, format: event.target.value })}>{["rss", "atom", "json", "api", "html"].map((value) => <option key={value}>{value}</option>)}</select></label>
        <label>{copy.role}<select className={fieldClass} value={sourceDraft.role} onChange={(event) => setSourceDraft({ ...sourceDraft, role: event.target.value })}><option value="evidence">evidence</option><option value="lead_only">lead_only</option></select></label>
        <label>{copy.vertical}<select className={fieldClass} value={sourceDraft.vertical} onChange={(event) => setSourceDraft({ ...sourceDraft, vertical: event.target.value })}>{["ai", "tech", "crypto", "mixed"].map((value) => <option key={value}>{value}</option>)}</select></label>
        <label>{copy.interval}<input className={fieldClass} type="number" min={15} max={1440} value={sourceDraft.interval} onChange={(event) => setSourceDraft({ ...sourceDraft, interval: event.target.value })} /></label>
        <label>Redirect allow-list<input className={fieldClass} value={sourceDraft.allowedHosts} placeholder="www.example.com, cdn.example.com" onChange={(event) => setSourceDraft({ ...sourceDraft, allowedHosts: event.target.value })} /></label>
        <label>Parser config (JSON)<textarea className={fieldClass} rows={4} value={sourceDraft.config} onChange={(event) => setSourceDraft({ ...sourceDraft, config: event.target.value })} /></label></div>
        <label className="mt-3 flex min-h-11 items-center gap-2"><input type="checkbox" checked={sourceDraft.firstParty} disabled={sourceDraft.role !== "evidence"} onChange={(event) => setSourceDraft({ ...sourceDraft, firstParty: event.target.checked })} />{copy.firstParty}</label><Button className="mt-3" disabled={!manage.allowed || busy || !sourceDraft.name || !sourceDraft.url} onClick={() => void addSource()}>{copy.add}</Button></section>
        <section className="grid gap-3">{sources.map((item) => <article key={item.id} className={panelClass}><div className="flex flex-wrap items-start justify-between gap-3"><div><h3 className="font-bold">{item.name}</h3><a href={item.url} target="_blank" rel="noopener noreferrer" className="break-all text-sm text-[var(--teal)] underline">{item.url}</a><p className="mt-2 text-sm text-[var(--muted)]">{item.vertical} · {item.role} · {item.last_status} · {item.scan_interval_minutes}m</p>{item.last_error && <p className="mt-2 text-sm text-red-700">{item.last_error}</p>}</div><div className="flex gap-2"><Button secondary disabled={!manage.allowed || busy} onClick={() => void run(async () => { await api(`/admin/news/sources/${item.id}/${item.enabled ? "scan" : "validate"}`, { method: "POST" }); })}>{item.enabled ? copy.scanNow : copy.validate}</Button><Button disabled={!manage.allowed || busy} onClick={() => void patchSource(item, !item.enabled)}>{item.enabled ? copy.disabled : copy.enabled}</Button></div></div></article>)}</section></div>}
      {tab === "settings" && settings && <section className={`${panelClass} space-y-5`}><label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={settings.enabled} onChange={(event) => setSettings({ ...settings, enabled: event.target.checked })} />{copy.enable}</label>
        <label>Mode<select className={fieldClass} value={settings.mode} onChange={(event) => setSettings({ ...settings, mode: event.target.value as NewsSettings["mode"] })}><option value="shadow">{copy.shadow}</option><option value="automatic">{copy.automatic}</option></select></label>
        <div className="grid gap-3 md:grid-cols-2">{(["writer", "verifier"] as const).map((kind) => {
          const provider = settings[`${kind}_provider`];
          return <fieldset key={kind} className="space-y-3 rounded-xl border border-[var(--line)] p-4">
            <legend className="px-1 font-bold">{copy[kind]}</legend>
            <label className="block">{copy.provider}<select className={fieldClass} value={provider} onChange={(event) => setSettings({ ...settings, [`${kind}_provider`]: event.target.value as NewsProvider, [`${kind}_model`]: null })}>{newsProviders.map((value) => <option key={value} value={value}>{newsProviderLabels[value]}</option>)}</select></label>
            <NewsModelField key={provider} label={copy.model} value={settings[`${kind}_model`]} options={settings.model_options?.[provider] ?? []}
              fallback={settings.default_models?.[provider]} copy={copy} onChange={(value) => setSettings({ ...settings, [`${kind}_model`]: value })} />
          </fieldset>;
        })}</div>
        <div className="grid gap-3 md:grid-cols-2">{(["global_concurrency", "per_vertical_concurrency", "min_shadow_days", "min_shadow_candidates"] as const).map((key) => <label key={key}>{key}<input className={fieldClass} type="number" value={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: Number(event.target.value) })} /></label>)}</div>
        <div className="grid gap-3 md:grid-cols-2">{(["min_human_agreement", "jev_act_confidence"] as const).map((key) => <label key={key}>{key}<input className={fieldClass} type="number" min={0} max={1} step="0.01" value={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: Number(event.target.value) })} /></label>)}</div>
        <div className="grid gap-3 md:grid-cols-2">{(["prompt_version", "policy_version"] as const).map((key) => <label key={key}>{key}<input className={fieldClass} value={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: event.target.value })} /></label>)}</div>
        <div className="grid gap-3 md:grid-cols-3">{(["ai", "tech", "crypto"] as NewsVertical[]).map((vertical) => { const gate = settings.gates[vertical]; const key = `auto_publish_${vertical}` as const; return <article key={vertical} className="rounded-xl border border-[var(--line)] p-4"><h3 className="font-bold">{vertical.toUpperCase()} · {copy.gate}</h3><p className={`mt-2 text-sm font-semibold ${gate.eligible ? "text-emerald-700" : "text-amber-700"}`}>{gate.eligible ? copy.eligible : copy.notEligible}</p><p className="mt-1 text-sm">{gate.days}d · {gate.labelled_candidates} · {(gate.agreement_rate * 100).toFixed(1)}% · {gate.serious_false_positives} serious</p>{gate.reasons.length > 0 && <ul className="mt-2 list-disc pl-5 text-xs text-[var(--muted)]">{gate.reasons.map((value) => <li key={value}>{value}</li>)}</ul>}<label className="mt-3 flex min-h-11 items-center gap-2"><input type="checkbox" disabled={!gate.eligible || settings.mode !== "automatic"} checked={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: event.target.checked })} />Auto publish</label></article>; })}</div>
        <Button disabled={!manage.allowed || busy} onClick={() => void saveSettings()}>{copy.save}</Button></section>}
      {tab === "runs" && (!detail ? <Empty>{copy.empty}</Empty> : <section className={panelClass}><h2 className="text-xl font-bold">{copy.runs}</h2><div className="mt-3 overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr><th className="p-2">Stage</th><th className="p-2">{copy.status}</th><th className="p-2">Attempt</th><th className="p-2">Model</th><th className="p-2">Tokens</th></tr></thead><tbody>{detail.runs.map((item) => <tr key={item.id} className="border-t border-[var(--line)]"><td className="p-2">{item.stage}</td><td className="p-2">{item.status}{item.error_code ? ` · ${item.error_code}` : ""}</td><td className="p-2">{item.attempt}</td><td className="p-2">{item.provider ?? "—"} {item.model ?? ""}</td><td className="p-2">{item.input_tokens}/{item.output_tokens}</td></tr>)}</tbody></table></div></section>)}
    </Tabs>
  </div>;
}
