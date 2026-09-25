"use client";

import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { AdminReadOnlyNotice, useAdminActionGuard } from "@/components/admin-action-guard";
import { ContentBlocks } from "@/components/content-blocks";
import { Button, Empty, Tabs, fieldClass, panelClass } from "@/components/community/ui";
import { Link } from "@/i18n/navigation";
import { adminNewsCopy, fillNewsCopy } from "@/lib/admin-news-copy";
import {
  newsLocales,
  newsProviderLabels,
  newsProviders,
  type NewsCandidate,
  type NewsCandidatePage,
  type NewsCandidateStatus,
  type NewsCandidateSummary,
  type NewsLocale,
  type NewsModelOption,
  type NewsProvider,
  type NewsSettings,
  type NewsSource,
  type NewsStats,
  type NewsVertical,
} from "@/lib/admin-news";
import { adminNavigate, useAdminQueryState, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";
import { splitGuideBlocks } from "@/lib/guides";

const tabs = ["review", "sources", "settings", "runs"] as const;
// Each list asks the API for exactly these statuses. Fetching the newest rows of every
// status and filtering here let candidates nobody acts on push the ones waiting for a
// person out of the list. The review list holds only what needs a person's decision: on the
// first production day most of it was candidates that stopped before any draft existed.
const queueViews = ["review", "redraft", "evidence", "published", "closed"] as const;
type QueueView = typeof queueViews[number];
const queueStatuses: Record<QueueView, readonly NewsCandidateStatus[]> = {
  review: ["manual_review", "shadow_review"],
  redraft: ["needs_redraft", "failed"],
  evidence: ["needs_evidence"],
  published: ["published"],
  closed: ["rejected", "duplicate"],
};
// Lists whose rows can be ticked and rejected together; rejecting spends no model calls.
const bulkViews: readonly QueueView[] = ["review", "redraft", "evidence"];
const pageSize = 50;
const statusTone: Partial<Record<NewsCandidateStatus, string>> = {
  manual_review: "bg-amber-100 text-amber-900",
  shadow_review: "bg-sky-100 text-sky-900",
  published: "bg-emerald-100 text-emerald-900",
  failed: "bg-red-100 text-red-900",
  needs_evidence: "bg-stone-100 text-stone-800",
  needs_redraft: "bg-orange-100 text-orange-900",
  rejected: "bg-stone-100 text-stone-800",
  duplicate: "bg-stone-100 text-stone-800",
};

// What happened to a candidate, which decides the explanation and the buttons it gets.
type Situation =
  | "zhDraft" | "translationHold" | "readyToPublish" | "finalEditHold" | "jevFinalHold"
  | "shadow" | "jevHold" | "fixArticle" | "duplicate" | "evidenceChanged" | "redraft"
  | "failed" | "needsEvidence" | "published" | "closed" | "working";
type Action = "approve" | "publish" | "verify" | "notDuplicate" | "retry" | "reject" | "incident";
const actionPath: Record<Action, string> = {
  approve: "approve", publish: "publish", verify: "verify", notDuplicate: "not-duplicate",
  retry: "retry", reject: "reject", incident: "major-error",
};
// Only the buttons that can work for the situation, so none sit greyed out unexplained.
const situationActions: Record<Situation, readonly Action[]> = {
  // A verified Traditional Chinese draft: the owner confirms before anything is translated.
  zhDraft: ["approve", "retry", "reject"],
  // Confirmed, then a translation or a check stopped it: run the second stage again.
  translationHold: ["approve", "reject"],
  readyToPublish: ["publish", "verify", "reject"],
  // The five-locale article is saved; the final editor or Jev's last call held it back.
  finalEditHold: ["publish", "verify", "reject"],
  jevFinalHold: ["publish", "verify", "reject"],
  shadow: ["publish", "verify", "reject"],
  jevHold: ["publish", "verify", "reject"],
  fixArticle: ["verify", "reject"],
  duplicate: ["notDuplicate", "reject"],
  // Stored evidence hashes are never refreshed, so publish and reruns fail the same way.
  evidenceChanged: ["reject"],
  redraft: ["retry", "reject"],
  failed: ["approve", "retry", "verify", "reject"],
  // Only lead-only pages: a rerun cannot find a page to cite.
  needsEvidence: ["reject"],
  published: ["incident"],
  closed: [],
  working: [],
};
const primaryActions: readonly Action[] = ["approve", "publish", "notDuplicate", "incident"];

function situationOf(candidate: NewsCandidateSummary): Situation {
  switch (candidate.status) {
    case "shadow_review": return "shadow";
    case "manual_review":
      if (candidate.error_code === "news_duplicate_uncertain") return "duplicate";
      if (candidate.error_code === "news_evidence_changed") return "evidenceChanged";
      if (candidate.error_code === "news_zh_draft_ready") return "zhDraft";
      if (candidate.error_code === "news_ready_to_publish") return "readyToPublish";
      if (candidate.error_code === "news_jev_manual") return "jevHold";
      if (candidate.error_code === "news_final_edit_hold") return "finalEditHold";
      if (candidate.error_code === "news_jev_final_hold") return "jevFinalHold";
      if (candidate.human_decision === "publish") return "translationHold";
      return candidate.guide_article_id ? "fixArticle" : "redraft";
    case "needs_redraft": return "redraft";
    case "failed": return "failed";
    case "needs_evidence": return "needsEvidence";
    case "published": return "published";
    case "rejected":
    case "duplicate": return "closed";
    default: return "working";
  }
}

function availableActions(candidate: NewsCandidateSummary): Action[] {
  return situationActions[situationOf(candidate)].filter((action) => {
    if (action === "verify") return Boolean(candidate.guide_article_id);
    // A failed run can resume translating only after the owner confirmed publication.
    if (action === "approve" && candidate.status === "failed") return candidate.human_decision === "publish";
    return true;
  });
}

function problemMessage(problem: unknown, fallback: string) {
  return problem instanceof Error && problem.message ? problem.message : fallback;
}

function named(names: Record<string, string>, key: string) {
  return names[key] ?? key;
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
  const [queueView] = useAdminQueryState("queue", queueViews, "review");
  const [pageValue, setPage] = useAdminQueryValue("page", "", (value) => /^[1-9]\d{0,4}$/.test(value));
  const page = Number(pageValue || "1");
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
  // Ticked rows belong to one list page; moving to another list or page drops them.
  const listKey = `${queueView}:${page}`;
  const [ticked, setTicked] = useState<{ key: string; ids: string[] }>({ key: "", ids: [] });
  const [bulkReason, setBulkReason] = useState("");
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
      api<NewsSource[]>("/admin/news/sources", { signal: controller.signal }),
      api<NewsSettings>("/admin/news/settings", { signal: controller.signal }),
      api<NewsStats>("/admin/news/stats", { signal: controller.signal }),
    ]).then(([sourceRows, configuration, totals]) => {
      if (controller.signal.aborted) return;
      setSources(sourceRows); setSettings(configuration); setStats(totals);
    }).catch((problem) => { if (!controller.signal.aborted) setError(problemMessage(problem, copy.error)); });
    return () => controller.abort();
  }, [copy.error, reload]);

  useEffect(() => {
    const controller = new AbortController();
    const query = new URLSearchParams({ limit: String(pageSize), page: String(page) });
    for (const status of queueStatuses[queueView]) query.append("status", status);
    api<NewsCandidatePage>(`/admin/news/candidates?${query}`, { signal: controller.signal })
      .then((result) => { if (!controller.signal.aborted) setCandidates(result); })
      .catch((problem) => { if (!controller.signal.aborted) setError(problemMessage(problem, copy.error)); });
    return () => controller.abort();
  }, [copy.error, queueView, page, reload]);

  useEffect(() => {
    if (!selected) return;
    const controller = new AbortController();
    api<NewsCandidate>(`/admin/news/candidates/${selected}`, { signal: controller.signal })
      .then((value) => { if (!controller.signal.aborted) setDetail(value); })
      .catch((problem) => { if (!controller.signal.aborted) setError(problemMessage(problem, copy.error)); });
    return () => controller.abort();
  }, [copy.error, reload, selected]);

  const queue = candidates?.candidates ?? [];
  const pages = candidates?.pages ?? 1;
  const queueCount = (view: QueueView) =>
    queueStatuses[view].reduce((total, status) => total + (stats?.queue_by_status[status] ?? 0), 0);
  const queueLabel: Record<QueueView, string> = {
    review: copy.reviewView, redraft: copy.redraftView, evidence: copy.evidenceView,
    published: copy.publishedView, closed: copy.closedView,
  };
  const queueHint: Partial<Record<QueueView, string>> = {
    review: copy.reviewHint, redraft: copy.redraftHint, evidence: copy.evidenceHint, closed: copy.closedHint,
  };
  const selectable = bulkViews.includes(queueView) && manage.allowed;
  const tickedIds = ticked.key === listKey ? ticked.ids.filter((id) => queue.some((item) => item.id === id)) : [];
  const statusName = (status: string) => named(copy.statuses, status);
  const holdName = (item: NewsCandidateSummary) => item.error_code ? named(copy.holds, item.error_code) : "";

  function chooseView(view: QueueView) {
    const target = new URL(window.location.href);
    target.searchParams.set("queue", view);
    target.searchParams.delete("page");
    adminNavigate(target);
  }

  function tick(id: string, on: boolean) {
    const others = tickedIds.filter((value) => value !== id);
    setTicked({ key: listKey, ids: on ? [...others, id] : others });
  }

  async function run(work: () => Promise<void>) {
    if (!manage.allowed || busy) return;
    setBusy(true); setError(""); setNotice("");
    try { await work(); setReload((value) => value + 1); }
    catch (problem) { setError(problemMessage(problem, copy.error)); }
    finally { setBusy(false); }
  }

  const doneMessage: Record<Action, string> = {
    approve: copy.doneApprove, publish: copy.donePublish, verify: copy.doneVerify,
    notDuplicate: copy.doneNotDuplicate, retry: copy.doneRetry, reject: copy.doneReject,
    incident: copy.doneIncident,
  };
  const actionLabel: Record<Action, string> = {
    approve: copy.approve, publish: copy.publish, verify: copy.verify,
    notDuplicate: copy.notDuplicate, retry: copy.retry, reject: copy.reject,
    incident: copy.incident,
  };
  // Confirming again resumes the translations of a draft the owner already confirmed.
  const labelFor = (name: Action) =>
    name === "approve" && detail?.human_decision === "publish" ? copy.retranslate : actionLabel[name];
  const draftJev = detail?.assessments.filter((item) => item.assessment_type === "jev" && item.locale === "zh-TW" && item.details.stage !== "final").at(-1);

  const act = (name: Action) => run(async () => {
    if (!detail || !reason.trim()) { setError(copy.reasonFirst); return; }
    const value = await api<NewsCandidate>(`/admin/news/candidates/${detail.id}/${actionPath[name]}`, {
      method: "POST", body: JSON.stringify({ reason: reason.trim(), major_error: majorError }),
    });
    setDetail(value); setReason(""); setMajorError(false); setNotice(doneMessage[name]);
  });

  // One request per candidate through the audited single reject, in order; a refusal for
  // one row (it moved on meanwhile) does not stop the others.
  const rejectTicked = () => run(async () => {
    const ids = tickedIds;
    const why = bulkReason.trim();
    if (!ids.length || !why) return;
    if (!window.confirm(fillNewsCopy(copy.bulkConfirm, { count: ids.length }))) return;
    const refused: string[] = [];
    for (const id of ids) {
      try {
        await api<NewsCandidate>(`/admin/news/candidates/${id}/reject`, {
          method: "POST", body: JSON.stringify({ reason: why, major_error: false }),
        });
      } catch {
        refused.push(queue.find((item) => item.id === id)?.source_title ?? id);
      }
    }
    setTicked({ key: listKey, ids: [] }); setBulkReason("");
    setNotice(fillNewsCopy(copy.bulkDone, { done: ids.length - refused.length }));
    if (refused.length) setError(fillNewsCopy(copy.bulkFailed, { failed: refused.length, titles: refused.join(" · ") }));
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
  const situation = detail ? situationOf(detail) : "working";
  const actions = detail ? availableActions(detail) : [];
  const gate = detail && settings ? settings.gates[detail.vertical] : undefined;

  return <div className="space-y-6">
    <header><p className="text-sm font-bold uppercase tracking-[.14em] text-[var(--teal)]">{copy.kicker}</p>
      <h1 className="mt-2 text-3xl font-bold md:text-4xl">{copy.title}</h1>
      <p className="mt-3 max-w-4xl leading-7 text-[var(--muted)]">{copy.description}</p></header>
    <AdminReadOnlyNotice capability="content.manage" />
    {error && <p role="alert" className="rounded-xl border border-red-200 bg-red-50 p-3 text-sm text-red-900">{error}</p>}
    {notice && <p role="status" className="rounded-xl border border-emerald-200 bg-emerald-50 p-3 text-sm text-emerald-900">{notice}</p>}
    <div className="grid gap-3 sm:grid-cols-3">
      {[[copy.pending, stats?.pending_review ?? 0], [copy.failed, stats?.failed ?? 0], [copy.published, stats?.published ?? 0]].map(([label, value]) =>
        <div key={String(label)} className={panelClass}><p className="text-sm text-[var(--muted)]">{label}</p><p className="mt-1 text-3xl font-bold">{value}</p></div>)}
    </div>
    {stats && <p className="text-sm text-[var(--muted)]">{fillNewsCopy(copy.runsSummary, { runs: stats.pipeline_runs, failures: stats.pipeline_failures, input: stats.input_tokens, output: stats.output_tokens })}</p>}
    <Tabs value={tab} onChange={(value) => setTab(value as typeof tab)} label={copy.title}
      items={tabs.map((value) => ({ value, label: copy[value] }))}>
      {tab === "review" && <div className="grid grid-cols-1 gap-5 xl:grid-cols-[24rem_minmax(0,1fr)]">
        <section className={`${panelClass} space-y-2`} aria-label={copy.review}>
          <div className="flex flex-wrap gap-2" role="group" aria-label={copy.queueFilter}>
            {queueViews.map((view) => <Button key={view} secondary={queueView !== view} aria-pressed={queueView === view} onClick={() => chooseView(view)}>{`${queueLabel[view]} · ${queueCount(view)}`}</Button>)}
          </div>
          {queueHint[queueView] && <p className="text-xs leading-5 text-[var(--muted)]">{queueHint[queueView]}</p>}
          {selectable && queue.length > 0 && <div className="space-y-2 rounded-xl bg-[var(--paper)] p-3">
            <div className="flex flex-wrap items-center gap-2 text-sm">
              <Button secondary onClick={() => setTicked({ key: listKey, ids: tickedIds.length === queue.length ? [] : queue.map((item) => item.id) })}>
                {tickedIds.length === queue.length ? copy.clearSelection : copy.selectPage}
              </Button>
              {tickedIds.length > 0 && <span>{fillNewsCopy(copy.selectedCount, { count: tickedIds.length })}</span>}
            </div>
            {tickedIds.length > 0 && <>
              <label className="block text-sm font-semibold">{copy.bulkReason}<input className={fieldClass} value={bulkReason} onChange={(event) => setBulkReason(event.target.value)} /></label>
              <div className="flex flex-wrap gap-2">{copy.quickReasonList.map((value) => <button type="button" key={value} className="rounded-full border border-[var(--line)] px-3 py-1 text-xs" onClick={() => setBulkReason(value)}>{value}</button>)}</div>
              <Button disabled={busy || !bulkReason.trim()} onClick={() => void rejectTicked()}>{copy.bulkReject}</Button>
            </>}
          </div>}
          {!queue.length ? <Empty>{copy.empty}</Empty> : queue.map((item) => <div key={item.id}
            className={`flex items-start gap-3 rounded-xl border p-3 ${selected === item.id ? "border-[var(--teal)]" : "border-[var(--line)]"}`}>
            {selectable && <input type="checkbox" className="mt-1 h-5 w-5 shrink-0" aria-label={fillNewsCopy(copy.selectRow, { title: item.source_title })}
              checked={tickedIds.includes(item.id)} onChange={(event) => tick(item.id, event.target.checked)} />}
            <button type="button" onClick={() => setSelected(item.id)} className="min-w-0 flex-1 text-left">
              <span className={`rounded-full px-2 py-1 text-xs font-bold ${statusTone[item.status] ?? "bg-[var(--paper)]"}`}>{statusName(item.status)}</span>
              {holdName(item) && <span className="mt-2 block text-sm font-semibold">{holdName(item)}</span>}
              <strong className="mt-1 block">{item.source_title}</strong>
              <span className="mt-1 block text-xs text-[var(--muted)]">{item.vertical.toUpperCase()} · {item.event_date ?? item.created_at.slice(0, 10)}</span>
            </button>
          </div>)}
          {pages > 1 && <div className="flex flex-wrap items-center justify-between gap-2 pt-2 text-sm">
            <Button secondary disabled={page <= 1} onClick={() => setPage(page - 1 > 1 ? String(page - 1) : "")}>{copy.previousPage}</Button>
            <span>{fillNewsCopy(copy.pageOf, { page, pages, total: candidates?.total ?? 0 })}</span>
            <Button secondary disabled={page >= pages} onClick={() => setPage(String(page + 1))}>{copy.nextPage}</Button>
          </div>}
        </section>
        {!detail ? <Empty>{copy.pickOne}</Empty> : <section className="space-y-5">
          <div className={panelClass}><div className="flex flex-wrap items-center gap-2"><span className={`rounded-full px-2 py-1 text-xs font-bold ${statusTone[detail.status] ?? "bg-[var(--paper)]"}`}>{statusName(detail.status)}</span><strong>{detail.source_title}</strong></div>
            <a href={detail.canonical_url} target="_blank" rel="noopener noreferrer" className="mt-2 block break-all text-sm text-[var(--teal)] underline">{detail.canonical_url}</a>
            {detail.error_code && <p className="mt-3 text-sm font-semibold text-red-700">{holdName(detail)}</p>}
            {detail.error_detail && <p className="mt-1 break-words text-xs text-[var(--muted)]">{detail.error_detail}</p>}
          </div>
          <div className={`${panelClass} space-y-3`}>
            <h2 className="text-xl font-bold">{copy.nextStep}</h2>
            <p className="leading-7">{copy.next[situation]}</p>
            {situation === "zhDraft" && draftJev && <p className="text-sm">
              {fillNewsCopy(copy.jevOnDraft, { tier: typeof draftJev.details.tier === "string" ? named(copy.tiers, draftJev.details.tier) : named(copy.verdicts, draftJev.verdict), confidence: draftJev.confidence?.toFixed(2) ?? "—" })}
            </p>}
            {(situation === "zhDraft" || situation === "shadow" || situation === "jevHold") && gate && settings && <p className="text-sm text-[var(--muted)]">
              {fillNewsCopy(copy.agreementProgress, { vertical: detail.vertical.toUpperCase(), labelled: gate.labelled_candidates, rate: (gate.agreement_rate * 100).toFixed(0) })}
            </p>}
            {situation === "duplicate" && <div>
              <h3 className="font-semibold">{copy.similarTitles}</h3>
              {detail.similar_titles?.length
                ? <ol className="mt-2 list-decimal space-y-1 pl-5 text-sm">{detail.similar_titles.map((title) => <li key={title}>{title}</li>)}</ol>
                : <p className="mt-2 text-sm text-[var(--muted)]">{copy.noSimilarTitles}</p>}
            </div>}
            {actions.length > 0 && <div className="space-y-3 border-t border-[var(--line)] pt-3">
              <label className="block font-semibold">{copy.reason}<textarea className={fieldClass} value={reason} onChange={(event) => setReason(event.target.value)} rows={2} /></label>
              <div className="flex flex-wrap items-center gap-2 text-xs" role="group" aria-label={copy.quickReasons}>
                <span className="text-[var(--muted)]">{copy.quickReasons}</span>
                {copy.quickReasonList.map((value) => <button type="button" key={value} className="rounded-full border border-[var(--line)] px-3 py-1" onClick={() => setReason(value)}>{value}</button>)}
              </div>
              {(actions.includes("publish") || actions.includes("incident")) && <label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={majorError} onChange={(event) => setMajorError(event.target.checked)} />{copy.majorError}</label>}
              <div className="flex flex-wrap items-center gap-2">
                {actions.map((name) => <Button key={name} secondary={!primaryActions.includes(name)}
                  disabled={!manage.allowed || busy || !reason.trim() || (name === "incident" && !majorError)}
                  onClick={() => void act(name)}>{labelFor(name)}</Button>)}
                {!reason.trim() && <span className="text-xs text-[var(--muted)]">{copy.reasonFirst}</span>}
              </div>
            </div>}
          </div>
          <div className={panelClass}><h2 className="text-xl font-bold">{copy.evidence}</h2><div className="mt-3 space-y-3">{detail.evidence.map((item) => <article key={item.id} className="rounded-xl bg-[var(--paper)] p-3">
            <p className="font-semibold">{item.title} · {item.is_first_party ? copy.firstParty : item.role === "lead_only" ? copy.leadOnly : copy.evidence}</p>
            <a href={item.url} target="_blank" rel="noopener noreferrer" className="break-all text-sm text-[var(--teal)] underline">{item.url}</a>
            <p className="mt-2 line-clamp-5 whitespace-pre-wrap text-sm leading-6 text-[var(--muted)]">{item.excerpt}</p><code className="mt-2 block break-all text-xs">sha256:{item.content_hash}</code>
          </article>)}</div></div>
          <div className="grid gap-5 lg:grid-cols-2">
            <div className={panelClass}><h2 className="text-xl font-bold">{copy.claims}</h2>{detail.claim_ledger.length === 0 ? <p className="mt-3 text-sm text-[var(--muted)]">—</p> : <ol className="mt-3 list-decimal space-y-3 pl-5 text-sm">{detail.claim_ledger.map((claim, index) => <li key={`${index}-${String(claim.claim ?? "")}`}><p>{String(claim.claim ?? "")}</p><p className="mt-1 break-all text-xs text-[var(--muted)]">{Array.isArray(claim.source_urls) ? claim.source_urls.join(" · ") : ""}</p></li>)}</ol>}</div>
            <div className={panelClass}><h2 className="text-xl font-bold">{copy.checks}</h2>{Object.keys(detail.lint).length === 0 ? <p className="mt-3 text-sm text-[var(--muted)]">—</p> : <div className="mt-3 space-y-3">{Object.entries(detail.lint).map(([lintLocale, problems]) => <article key={lintLocale}><h3 className="font-semibold">{lintLocale}</h3>{problems.length === 0 ? <p className="text-sm text-emerald-700">{copy.noErrors}</p> : <ul className="list-disc pl-5 text-sm text-red-700">{problems.map((problem) => <li key={problem}>{problem}</li>)}</ul>}</article>)}</div>}</div>
          </div>
          <div className={panelClass}><h2 className="text-xl font-bold">{copy.preview}</h2><div className="mt-3 flex flex-wrap gap-2">{newsLocales.map((value) => <Button key={value} secondary={previewLocale !== value} onClick={() => setPreviewLocale(value)}>{value}</Button>)}</div>
            {!document ? <p className="mt-4 text-[var(--muted)]">{copy.noDocument}</p> : <article className="mt-5 space-y-4"><h2 className="text-2xl font-bold">{document.title}</h2><p className="text-[var(--muted)]">{document.description}</p><ContentBlocks blocks={contentBlocks} labels={labels} locale={previewLocale} />
              <h3 className="font-bold">{copy.source}</h3><ul className="list-disc pl-5 text-sm">{document.sources.map((item) => <li key={item.url}><a href={item.url} target="_blank" rel="noopener noreferrer" className="text-[var(--teal)] underline">{item.title}</a></li>)}</ul></article>}
            {detail.guide_article_id && <div className="mt-4 flex flex-wrap gap-2">{newsLocales.map((value) => <Link key={value} href={`/admin/guides?article=${detail.guide_article_id}&lang=${value}`} className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-3 font-semibold">{copy.openEditor} · {value}</Link>)}</div>}
          </div>
          <div className={panelClass}><h2 className="text-xl font-bold">{copy.assessments}</h2><div className="mt-3 overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr><th className="p-2">{copy.status}</th><th className="p-2">{copy.locale}</th><th className="p-2">{copy.confidence}</th><th className="p-2">{copy.model}</th><th className="p-2">{copy.reasons}</th></tr></thead><tbody>{detail.assessments.map((item) => <tr key={item.id} className="border-t border-[var(--line)]"><td className="min-w-40 p-2">{named(copy.assessmentTypes, item.assessment_type)}{typeof item.details.stage === "string" && item.details.stage in copy.assessmentStages ? `・${named(copy.assessmentStages, item.details.stage)}` : ""}: {named(copy.verdicts, item.verdict)}{typeof item.details.tier === "string" ? ` (${named(copy.tiers, item.details.tier)})` : ""}</td><td className="p-2">{item.locale ?? "—"}</td><td className="p-2">{item.confidence?.toFixed(3) ?? "—"}</td><td className="p-2">{item.provider === "human" ? copy.assessmentTypes.human : `${item.provider ?? "—"} ${item.model ?? ""}`}</td><td className="min-w-40 p-2">{item.reasons.map((value) => named(copy.reasonCodes, value)).join(" · ") || "—"}</td></tr>)}</tbody></table></div></div>
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
        <label>{copy.mode}<select className={fieldClass} value={settings.mode} onChange={(event) => setSettings({ ...settings, mode: event.target.value as NewsSettings["mode"] })}><option value="shadow">{copy.shadow}</option><option value="automatic">{copy.automatic}</option></select></label>
        <div className="grid gap-3 md:grid-cols-3">{(["writer", "verifier", "editor"] as const).map((kind) => {
          const provider = settings[`${kind}_provider`];
          return <fieldset key={kind} className="space-y-3 rounded-xl border border-[var(--line)] p-4">
            <legend className="px-1 font-bold">{copy[kind]}</legend>
            <label className="block">{copy.provider}<select className={fieldClass} value={provider} onChange={(event) => setSettings({ ...settings, [`${kind}_provider`]: event.target.value as NewsProvider, [`${kind}_model`]: null })}>{newsProviders.map((value) => <option key={value} value={value}>{newsProviderLabels[value]}</option>)}</select></label>
            <NewsModelField key={provider} label={copy.model} value={settings[`${kind}_model`]} options={settings.model_options?.[provider] ?? []}
              fallback={settings.default_models?.[provider]} copy={copy} onChange={(value) => setSettings({ ...settings, [`${kind}_model`]: value })} />
          </fieldset>;
        })}</div>
        <div className="grid gap-3 md:grid-cols-2">{(["global_concurrency", "per_vertical_concurrency"] as const).map((key) => <label key={key}>{key}<input className={fieldClass} type="number" value={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: Number(event.target.value) })} /></label>)}</div>
        <div className="grid gap-3 md:grid-cols-2">{(["jev_act_confidence"] as const).map((key) => <label key={key}>{key}<input className={fieldClass} type="number" min={0} max={1} step="0.01" value={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: Number(event.target.value) })} /></label>)}</div>
        <div className="grid gap-3 md:grid-cols-2">{(["prompt_version", "policy_version"] as const).map((key) => <label key={key}>{key}<input className={fieldClass} value={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: event.target.value })} /></label>)}</div>
        <p className="text-sm text-[var(--muted)]">{copy.agreementHint}</p>
        <div className="grid gap-3 md:grid-cols-3">{(["ai", "tech", "crypto"] as NewsVertical[]).map((vertical) => { const gateView = settings.gates[vertical]; const key = `auto_publish_${vertical}` as const; return <article key={vertical} className="rounded-xl border border-[var(--line)] p-4"><h3 className="font-bold">{vertical.toUpperCase()} · {copy.agreement}</h3><p className="mt-1 text-sm">{gateView.days}d · {gateView.labelled_candidates} · {(gateView.agreement_rate * 100).toFixed(1)}% · {gateView.serious_false_positives} {copy.serious}</p><label className="mt-3 flex min-h-11 items-center gap-2"><input type="checkbox" disabled={settings.mode !== "automatic"} checked={settings[key]} onChange={(event) => setSettings({ ...settings, [key]: event.target.checked })} />{copy.autoPublish}</label></article>; })}</div>
        <Button disabled={!manage.allowed || busy} onClick={() => void saveSettings()}>{copy.save}</Button></section>}
      {tab === "runs" && (!detail ? <Empty>{copy.pickOne}</Empty> : <section className={panelClass}><h2 className="text-xl font-bold">{copy.runs}</h2><div className="mt-3 overflow-x-auto"><table className="w-full text-left text-sm"><thead><tr><th className="p-2">{copy.stage}</th><th className="p-2">{copy.status}</th><th className="p-2">{copy.attempt}</th><th className="p-2">{copy.model}</th><th className="p-2">{copy.tokens}</th></tr></thead><tbody>{detail.runs.map((item) => <tr key={item.id} className="border-t border-[var(--line)]"><td className="p-2">{item.stage}</td><td className="p-2">{item.status}{item.error_code ? ` · ${item.error_code}` : ""}</td><td className="p-2">{item.attempt}</td><td className="p-2">{item.provider ?? "—"} {item.model ?? ""}</td><td className="p-2">{item.input_tokens}/{item.output_tokens}</td></tr>)}</tbody></table></div></section>)}
    </Tabs>
  </div>;
}
