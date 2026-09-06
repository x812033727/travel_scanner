"use client";

import {
  Bot,
  CheckCircle2,
  ChevronDown,
  CircleAlert,
  ExternalLink,
  Languages,
  LoaderCircle,
  RefreshCw,
  RotateCw,
  Search,
  Sparkles,
  TriangleAlert,
  X,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { FormEvent, useCallback, useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import { safeExternalHref } from "@/lib/navigation";

const locales = ["en", "ja", "ko", "zh-TW", "zh-CN"] as const;
const providers = ["minimax", "openai", "anthropic"] as const;
type Locale = (typeof locales)[number];
type Provider = (typeof providers)[number];
type ContentType = "article" | "video";
type Depth = "economy" | "balanced" | "deep";
type GuideCandidate = {
  id: string;
  hotspot_name: string;
  type: ContentType;
  provider: string;
  locale: string;
  title: string;
  creator_name: string;
  url: string;
  language_confidence: number;
  status: string;
  discovery_method: string;
  ai_provider: Provider | null;
  relevance_score: number | null;
  quality_score: number | null;
  recommendation_reason: string | null;
  search_query: string | null;
};
type GuideResponse = {
  items: GuideCandidate[];
  total: number;
  page: number;
  pages: number;
};
type CoverageItem = {
  id: string;
  name: string;
  complete: boolean;
  coverage: Record<Locale, { article: number; video: number }>;
};
type CoverageResponse = {
  items: CoverageItem[];
  total: number;
  complete: number;
  quotas: {
    youtube: { used: number; automatic_limit: number };
    brave: { used: number; limit: number };
  };
  ai_search: {
    enabled: boolean;
    default_provider: Provider;
    providers: Record<Provider, boolean>;
    sources: { brave: boolean; youtube: boolean };
    quota: {
      runs_used: number;
      runs_limit: number;
      calls_used: number;
      calls_limit: number;
    };
  };
};
type SearchRun = {
  run_id: string;
  status: "queued" | "running" | "partial" | "completed" | "failed";
  progress: number;
  current: { locale?: string; stage?: string };
  usage: Record<string, number>;
  result: {
    created?: number;
    evaluated?: number;
    errors?: RunError[];
    notices?: RunError[];
  };
  error_code: string | null;
  error_message?: string | null;
  retryable?: boolean;
};
type SearchDraft = {
  hotspotId: string;
  hotspotName: string;
  locales: Locale[];
  contentTypes: ContentType[];
  provider: Provider;
  depth: Depth;
  onlyMissing: boolean;
  customInstructions: string;
};
const depthQueries: Record<Depth, number> = {
  economy: 1,
  balanced: 3,
  deep: 5,
};

type RunError = {
  locale: string | null;
  code: string;
  message?: string | null;
  detail?: string | null;
};
type ManualGuideResponse = {
  created: number;
  guide_id: string;
  review_status: "approved" | "pending";
  locale?: string;
};
type DiscoverReport = {
  hotspot_id: string;
  created: number;
  providers: Partial<
    Record<"youtube" | "brave", "ready" | "not_configured" | "quota_exhausted">
  >;
  errors: Array<{ provider: string; locale: string; error: string }>;
};
type Translator = ReturnType<typeof useTranslations>;
type NoticeTone = "info" | "success" | "warning" | "error";
type Notice = { text: string; tone: NoticeTone; details?: string[] };

const runErrorCodes = new Set([
  "ai_quota_exhausted",
  "brave_not_configured",
  "brave_quota_exhausted",
  "brave_search_failed",
  "youtube_not_configured",
  "youtube_quota_exhausted",
  "youtube_search_failed",
  "ai_search_failed",
  "queue_unavailable",
  "provider_unavailable",
  "hotspot_guide_ai_provider_not_configured",
  "hotspot_not_found",
  "no_new_candidates",
  "scope_covered",
]);
const providerLabels: Record<string, string> = { youtube: "YouTube", brave: "Brave" };
const noticeClasses: Record<NoticeTone, string> = {
  info: "bg-[var(--paper)] text-[var(--muted)]",
  success: "bg-emerald-50 text-emerald-800",
  warning: "bg-amber-50 text-amber-900",
  error: "bg-red-50 text-red-800",
};

function isRunActive(run: SearchRun | null): boolean {
  return Boolean(run && (run.status === "queued" || run.status === "running"));
}

function runErrorLabel(t: Translator, code: string | null | undefined): string {
  if (!code) return t("runFailedUnknown");
  return runErrorCodes.has(code) ? t(`runError.${code}`) : code;
}

function runIssueText(t: Translator, issue: RunError): string {
  const prefix = issue.locale ? `${issue.locale}：` : "";
  const detail = issue.detail ? ` — ${issue.detail}` : "";
  return `${prefix}${runErrorLabel(t, issue.code)}${detail}`;
}

function NoticeBox({
  notice,
  className = "",
}: {
  notice: Notice | null;
  className?: string;
}) {
  if (!notice) return null;
  return (
    <div
      role={notice.tone === "error" ? "alert" : "status"}
      className={`rounded-xl px-4 py-3 text-sm ${noticeClasses[notice.tone]} ${className}`}
    >
      <p>{notice.text}</p>
      {notice.details?.length ? (
        <ul className="mt-1 list-disc pl-5">
          {notice.details.map((detail, index) => (
            <li key={`${index}-${detail}`}>{detail}</li>
          ))}
        </ul>
      ) : null}
    </div>
  );
}

export function AdminHotspotGuidesPanel() {
  const t = useTranslations("hotspotAdmin");
  const [data, setData] = useState<GuideResponse | null>(null);
  const [coverage, setCoverage] = useState<CoverageResponse | null>(null);
  const [status, setStatus] = useState("pending");
  const [locale, setLocale] = useState("");
  const [type, setType] = useState("");
  const [source, setSource] = useState("");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [message, setMessage] = useState("");
  const [loading, setLoading] = useState(true);
  const [draft, setDraft] = useState<SearchDraft | null>(null);
  const [run, setRun] = useState<SearchRun | null>(null);
  const [manual, setManual] = useState({
    hotspot_id: "",
    locale: "zh-TW",
    content_type: "article",
    url: "",
    title: "",
    creator_name: "",
    summary: "",
    approve: true,
  });
  const [hotspotFilter, setHotspotFilter] = useState("");
  const [manualNotice, setManualNotice] = useState<Notice | null>(null);
  const [sheetError, setSheetError] = useState("");
  const [discoverNotice, setDiscoverNotice] = useState<
    (Notice & { hotspotId: string }) | null
  >(null);
  const [showAllCoverage, setShowAllCoverage] = useState(false);
  const runActive = isRunActive(run);

  const load = useCallback(async () => {
    setLoading(true);
    const params = new URLSearchParams({ limit: "50" });
    if (status) params.set("status", status);
    if (locale) params.set("locale", locale);
    if (type) params.set("type", type);
    if (source) params.set("discovery_method", source);
    try {
      const [guides, coverageResult] = await Promise.all([
        api<GuideResponse>(`/admin/hotspots/guides?${params}`),
        api<CoverageResponse>("/admin/hotspots/guides/coverage"),
      ]);
      setData(guides);
      setCoverage(coverageResult);
      setSelected(new Set());
      if (coverageResult.items[0])
        setManual((current) =>
          current.hotspot_id
            ? current
            : { ...current, hotspot_id: coverageResult.items[0].id },
        );
    } catch (error) {
      setMessage((error as Error).message);
    } finally {
      setLoading(false);
    }
  }, [locale, source, status, type]);

  useEffect(() => {
    const timer = window.setTimeout(() => void load(), 0);
    return () => window.clearTimeout(timer);
  }, [load]);
  useEffect(() => {
    if (!run || !isRunActive(run)) return;
    const timer = window.setInterval(
      () =>
        void api<SearchRun>(`/admin/hotspots/guides/ai-search/${run.run_id}`)
          .then((next) => {
            setRun(next);
            if (!isRunActive(next)) void load();
          })
          .catch((error: Error) => setMessage(error.message)),
      1500,
    );
    return () => window.clearInterval(timer);
  }, [load, run]);
  useEffect(() => {
    if (!draft) return;
    const handleKey = (event: KeyboardEvent) => {
      if (event.key === "Escape" && !runActive) setDraft(null);
      if (event.key !== "Tab") return;
      const dialog = document.querySelector<HTMLElement>("[role='dialog']");
      const focusable = dialog?.querySelectorAll<HTMLElement>(
        "button:not(:disabled), select:not(:disabled), textarea:not(:disabled), input:not(:disabled), a[href]",
      );
      if (!focusable?.length) return;
      const first = focusable[0];
      const last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    };
    document.body.style.overflow = "hidden";
    window.addEventListener("keydown", handleKey);
    return () => {
      document.body.style.overflow = "";
      window.removeEventListener("keydown", handleKey);
    };
  }, [draft, runActive]);

  const estimate = useMemo(() => {
    if (!draft) return { ai: 0, brave: 0, youtube: 0 };
    const queries = depthQueries[draft.depth] * draft.locales.length;
    return {
      ai: draft.locales.length * 2,
      brave: draft.contentTypes.includes("article") ? queries : 0,
      youtube: draft.contentTypes.includes("video") ? queries : 0,
    };
  }, [draft]);
  const visibleIds = useMemo(
    () => data?.items?.map((item) => item.id) ?? [],
    [data],
  );
  const allVisibleSelected =
    visibleIds.length > 0 && visibleIds.every((id) => selected.has(id));
  const sortedCoverage = useMemo(
    () =>
      [...(coverage?.items ?? [])].sort(
        (a, b) =>
          Number(a.complete) - Number(b.complete) || a.name.localeCompare(b.name),
      ),
    [coverage],
  );
  const visibleCoverage = showAllCoverage
    ? sortedCoverage
    : sortedCoverage.slice(0, 12);
  const hotspotOptions = useMemo(() => {
    const needle = hotspotFilter.trim().toLocaleLowerCase();
    const filtered = [...(coverage?.items ?? [])]
      .filter(
        (item) => !needle || item.name.toLocaleLowerCase().includes(needle),
      )
      .sort((a, b) => a.name.localeCompare(b.name));
    const current = coverage?.items.find((item) => item.id === manual.hotspot_id);
    if (current && !filtered.some((item) => item.id === current.id))
      return [current, ...filtered];
    return filtered;
  }, [coverage, hotspotFilter, manual.hotspot_id]);

  function changeHotspotFilter(value: string) {
    setHotspotFilter(value);
    const needle = value.trim().toLocaleLowerCase();
    if (!needle) return;
    const matches = (coverage?.items ?? [])
      .filter((item) => item.name.toLocaleLowerCase().includes(needle))
      .sort((a, b) => a.name.localeCompare(b.name));
    if (matches.length && !matches.some((item) => item.id === manual.hotspot_id))
      setManual((current) => ({ ...current, hotspot_id: matches[0].id }));
  }

  function openSearch(item: CoverageItem) {
    const missingLocales = locales.filter(
      (value) =>
        item.coverage[value].article < 1 || item.coverage[value].video < 1,
    );
    const missingTypes = (["article", "video"] as ContentType[]).filter(
      (kind) => missingLocales.some((value) => item.coverage[value][kind] < 1),
    );
    setRun(null);
    setSheetError("");
    setDraft({
      hotspotId: item.id,
      hotspotName: item.name,
      locales: missingLocales.length ? missingLocales : [...locales],
      contentTypes: missingTypes.length ? missingTypes : ["article", "video"],
      provider: coverage?.ai_search.default_provider || "minimax",
      depth: "deep",
      onlyMissing: true,
      customInstructions: "",
    });
  }
  async function startSearch() {
    if (!draft || !draft.locales.length || !draft.contentTypes.length) return;
    setLoading(true);
    setSheetError("");
    try {
      setRun(
        await api<SearchRun>("/admin/hotspots/guides/ai-search", {
          method: "POST",
          headers: { "Idempotency-Key": crypto.randomUUID() },
          body: JSON.stringify({
            hotspot_id: draft.hotspotId,
            locales: draft.locales,
            content_types: draft.contentTypes,
            provider: draft.provider,
            depth: draft.depth,
            only_missing: draft.onlyMissing,
            custom_instructions: draft.customInstructions || null,
          }),
        }),
      );
    } catch (error) {
      setSheetError((error as Error).message);
    } finally {
      setLoading(false);
    }
  }
  async function review(action: "approve" | "reject" | "disable") {
    if (!selected.size) return;
    setLoading(true);
    try {
      await api("/admin/hotspots/guides/review", {
        method: "POST",
        body: JSON.stringify({
          ids: [...selected],
          action,
          ...(locale ? { locale } : {}),
        }),
      });
      setSelected(new Set());
      await load();
    } catch (error) {
      setMessage((error as Error).message);
      setLoading(false);
    }
  }
  async function discover(hotspotId: string) {
    setLoading(true);
    setDiscoverNotice(null);
    try {
      const { reports } = await api<{ reports: DiscoverReport[] }>(
        "/admin/hotspots/guides/discover",
        {
          method: "POST",
          body: JSON.stringify({ hotspot_ids: [hotspotId], locales }),
        },
      );
      const report =
        reports.find((item) => item.hotspot_id === hotspotId) ?? reports[0];
      const created = report?.created ?? 0;
      const details = [
        ...Object.entries(report?.providers ?? {})
          .filter(([, state]) => state && state !== "ready")
          .map(([provider, state]) =>
            t(`discoverProvider.${state}`, {
              provider: providerLabels[provider] ?? provider,
            }),
          ),
        ...(report?.errors ?? []).map((item) =>
          t("discoverError", {
            provider: providerLabels[item.provider] ?? item.provider,
            locale: item.locale,
            error: item.error,
          }),
        ),
      ];
      const summary = t("discoverCompleted", { created });
      setDiscoverNotice({
        hotspotId,
        text: details.length ? `${summary}｜${t("discoverIssues")}` : summary,
        tone: details.length ? "warning" : created ? "success" : "info",
        details,
      });
      await load();
    } catch (error) {
      setDiscoverNotice({
        hotspotId,
        text: (error as Error).message,
        tone: "error",
      });
      setLoading(false);
    }
  }
  async function submitManual(event: FormEvent) {
    event.preventDefault();
    setLoading(true);
    setManualNotice(null);
    const isArticle = manual.content_type === "article";
    try {
      const result = await api<ManualGuideResponse>(
        "/admin/hotspots/guides/manual",
        {
          method: "POST",
          body: JSON.stringify({
            hotspot_id: manual.hotspot_id,
            locale: manual.locale,
            content_type: manual.content_type,
            url: manual.url,
            title: isArticle ? manual.title : null,
            creator_name: isArticle ? manual.creator_name : null,
            summary: isArticle ? manual.summary.trim() || null : null,
            approve: manual.approve,
          }),
        },
      );
      const approved = result.review_status === "approved";
      const key = result.created
        ? approved
          ? "manualSavedApproved"
          : "manualSavedPending"
        : approved
          ? "manualUpdatedApproved"
          : "manualUpdatedPending";
      setManualNotice({
        text: t(key, { locale: result.locale ?? manual.locale }),
        tone: "success",
      });
      setManual((current) => ({
        ...current,
        url: "",
        title: "",
        creator_name: "",
        summary: "",
      }));
      await load();
    } catch (error) {
      setManualNotice({ text: (error as Error).message, tone: "error" });
      setLoading(false);
    }
  }
  function toggleLocale(value: Locale) {
    setDraft((current) =>
      current
        ? {
            ...current,
            locales: current.locales.includes(value)
              ? current.locales.filter((item) => item !== value)
              : [...current.locales, value],
          }
        : null,
    );
  }
  function toggleType(value: ContentType) {
    setDraft((current) =>
      current
        ? {
            ...current,
            contentTypes: current.contentTypes.includes(value)
              ? current.contentTypes.filter((item) => item !== value)
              : [...current.contentTypes, value],
          }
        : null,
    );
  }

  return (
    <section className="mt-10 border-t border-[var(--line)] pt-8">
      <div className="flex flex-wrap items-end justify-between gap-4">
        <div>
          <p className="flex items-center gap-2 text-sm font-bold text-[var(--teal)]">
            <Languages size={17} />
            {t("title")}
          </p>
          <h2 className="mt-2 text-2xl font-bold">{t("coverage")}</h2>
          <p className="mt-1 text-sm text-[var(--muted)]">
            {t("coverageSummary", {
              complete: coverage?.complete || 0,
              total: coverage?.total || 0,
            })}
          </p>
          {coverage?.quotas && (
            <p className="mt-2 text-xs text-[var(--muted)]">
              YouTube {coverage.quotas.youtube.used}/
              {coverage.quotas.youtube.automatic_limit} · Brave{" "}
              {coverage.quotas.brave.used}/{coverage.quotas.brave.limit} · AI{" "}
              {coverage.ai_search.quota.calls_used}/
              {coverage.ai_search.quota.calls_limit}
            </p>
          )}
        </div>
        <button
          type="button"
          onClick={() => void load()}
          className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] bg-white"
          aria-label={t("refresh")}
        >
          <RefreshCw size={17} className={loading ? "animate-spin" : ""} />
        </button>
      </div>
      <div className="mt-4 flex flex-wrap items-center justify-between gap-2 text-xs text-[var(--muted)]">
        <p>
          {t("coverageLegend")} · {t("coverageApprovedOnly")}
        </p>
        {sortedCoverage.length > 12 && (
          <button
            type="button"
            aria-pressed={showAllCoverage}
            onClick={() => setShowAllCoverage((current) => !current)}
            className="min-h-9 rounded-lg border border-[var(--line)] bg-white px-3 font-semibold text-[var(--ink)]"
          >
            {showAllCoverage
              ? t("showFewer")
              : t("showAll", { count: sortedCoverage.length })}
          </button>
        )}
      </div>
      <div className="mt-3 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
        {visibleCoverage.map((item) => (
          <article
            key={item.id}
            className="rounded-3xl border border-[var(--line)] bg-white p-4 shadow-sm"
          >
            <div className="flex items-start justify-between gap-3">
              <h3 className="font-bold">{item.name}</h3>
              <span
                className={`rounded-full px-2 py-1 text-xs ${item.complete ? "bg-emerald-100 text-emerald-800" : "bg-amber-100 text-amber-900"}`}
              >
                {item.complete ? t("complete") : t("missingContent")}
              </span>
            </div>
            <div className="mt-3 grid grid-cols-5 gap-1 text-center text-[10px]">
              {locales.map((value) => (
                <div key={value} className="rounded-lg bg-[var(--paper)] p-1.5">
                  <strong>{value}</strong>
                  <span className="mt-1 block text-[var(--muted)]">
                    {item.coverage[value].article}/{item.coverage[value].video}
                  </span>
                </div>
              ))}
            </div>
            <div className="mt-3 grid grid-cols-2 gap-2">
              <button
                type="button"
                onClick={() => openSearch(item)}
                disabled={!coverage?.ai_search.enabled}
                className="flex min-h-11 items-center justify-center gap-2 rounded-xl bg-[var(--ink)] px-3 py-2 text-xs font-semibold text-white disabled:opacity-40"
              >
                <Sparkles size={15} />
                {t("aiSearch")}
              </button>
              <button
                type="button"
                onClick={() => void discover(item.id)}
                className="min-h-11 rounded-xl border border-[var(--teal)] px-3 py-2 text-xs font-semibold text-[var(--teal)]"
              >
                {t("normalDiscover")}
              </button>
            </div>
            {discoverNotice?.hotspotId === item.id && (
              <NoticeBox notice={discoverNotice} className="mt-3" />
            )}
          </article>
        ))}
      </div>
      <div className="mt-7 grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-4">
        <select
          value={status}
          onChange={(e) => setStatus(e.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="pending">{t("pending")}</option>
          <option value="approved">{t("approved")}</option>
          <option value="rejected">{t("rejected")}</option>
          <option value="disabled">{t("disabled")}</option>
          <option value="">{t("allStatuses")}</option>
        </select>
        <select
          value={locale}
          onChange={(e) => setLocale(e.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">{t("allLanguages")}</option>
          {locales.map((value) => (
            <option key={value}>{value}</option>
          ))}
        </select>
        <select
          value={type}
          onChange={(e) => setType(e.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">{t("allTypes")}</option>
          <option value="article">{t("article")}</option>
          <option value="video">{t("video")}</option>
        </select>
        <select
          value={source}
          onChange={(e) => setSource(e.target.value)}
          className="h-11 rounded-xl border px-3"
        >
          <option value="">{t("allSources")}</option>
          <option value="ai_research">{t("aiSource")}</option>
          <option value="standard">{t("standardSource")}</option>
          <option value="manual">{t("manualSource")}</option>
        </select>
      </div>
      <div className="mt-3 flex flex-wrap items-center gap-2">
        <button
          type="button"
          disabled={!visibleIds.length || loading}
          aria-pressed={allVisibleSelected}
          onClick={() =>
            setSelected(allVisibleSelected ? new Set() : new Set(visibleIds))
          }
          className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-4 text-sm font-semibold disabled:opacity-40"
        >
          {t(allVisibleSelected ? "clearSelection" : "selectAll")}
        </button>
        <span className="mr-auto text-sm text-[var(--muted)]">
          {t("selected", { count: selected.size })}
        </span>
        <button
          disabled={!selected.size || loading}
          onClick={() => void review("approve")}
          className="min-h-11 rounded-xl bg-[var(--teal)] px-4 text-sm font-semibold text-white disabled:opacity-40"
        >
          {t("approve")}
        </button>
        <button
          disabled={!selected.size || loading}
          onClick={() => void review("reject")}
          className="min-h-11 rounded-xl border border-[var(--coral)] px-4 text-sm text-[var(--coral)] disabled:opacity-40"
        >
          {t("reject")}
        </button>
        <button
          disabled={!selected.size || loading}
          onClick={() => void review("disable")}
          className="min-h-11 rounded-xl border px-4 text-sm disabled:opacity-40"
        >
          {t("disable")}
        </button>
      </div>
      {message && (
        <p
          role="alert"
          className="mt-3 rounded-xl bg-red-50 px-4 py-3 text-sm text-red-800"
        >
          {message}
        </p>
      )}
      <div className="mt-3 overflow-hidden rounded-2xl border border-[var(--line)] bg-white">
        <div className="divide-y divide-[var(--line)]">
          {data?.items?.map((item) => (
            <article
              key={item.id}
              className="grid gap-3 p-4 md:grid-cols-[auto_1fr_auto] md:items-center"
            >
              <input
                type="checkbox"
                aria-label={item.title}
                checked={selected.has(item.id)}
                onChange={(event) =>
                  setSelected((current) => {
                    const next = new Set(current);
                    if (event.target.checked) next.add(item.id);
                    else next.delete(item.id);
                    return next;
                  })
                }
              />
              <div className="min-w-0">
                <div className="flex flex-wrap items-center gap-2">
                  {item.discovery_method === "ai_research" && (
                    <span className="inline-flex items-center gap-1 rounded-full bg-violet-100 px-2 py-1 text-[11px] font-bold text-violet-800">
                      <Bot size={12} />
                      AI · {item.ai_provider}
                    </span>
                  )}
                  <span className="rounded-full bg-[var(--paper)] px-2 py-1 text-[11px]">
                    {item.locale} · {t(item.type)}
                  </span>
                </div>
                <h3 className="mt-2 font-semibold">{item.title}</h3>
                <p className="text-xs text-[var(--muted)]">
                  {item.hotspot_name} · {item.creator_name} · {t("confidence")}{" "}
                  {Math.round(item.language_confidence * 100)}%
                </p>
                {item.relevance_score !== null && (
                  <details className="mt-2">
                    <summary className="flex cursor-pointer list-none items-center gap-1 text-xs font-semibold text-violet-700">
                      {t("aiScore", {
                        relevance: item.relevance_score,
                        quality: item.quality_score || 0,
                      })}
                      <ChevronDown size={13} />
                    </summary>
                    <p className="mt-2 rounded-xl bg-violet-50 p-3 text-xs leading-5 text-violet-950">
                      {item.recommendation_reason}
                    </p>
                    {item.search_query && (
                      <p className="mt-1 text-[11px] text-[var(--muted)]">
                        {t("searchQuery")}: {item.search_query}
                      </p>
                    )}
                  </details>
                )}
              </div>
              <a
                href={safeExternalHref(item.url)}
                target="_blank"
                rel="noopener noreferrer"
                className="grid h-11 w-11 place-items-center rounded-xl border text-[var(--teal)]"
                aria-label={t("openNewTab")}
              >
                <ExternalLink size={17} />
              </a>
            </article>
          ))}
        </div>
        {!loading && !data?.items?.length && (
          <p className="p-7 text-center text-[var(--muted)]">{t("empty")}</p>
        )}
      </div>
      <form
        onSubmit={submitManual}
        className="mt-7 grid gap-3 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 md:grid-cols-3"
      >
        <h3 className="font-bold md:col-span-3">{t("manual")}</h3>
        <div className="grid gap-2">
          <input
            value={hotspotFilter}
            onChange={(e) => changeHotspotFilter(e.target.value)}
            aria-label={t("hotspotFilter")}
            placeholder={t("hotspotFilter")}
            className="h-11 rounded-xl border px-3"
          />
          <select
            required
            aria-label={t("hotspot")}
            value={manual.hotspot_id}
            onChange={(e) => setManual({ ...manual, hotspot_id: e.target.value })}
            className="h-11 rounded-xl border px-3"
          >
            {hotspotOptions.map((item) => (
              <option key={item.id} value={item.id}>
                {item.name}
              </option>
            ))}
          </select>
        </div>
        <select
          aria-label={t("locale")}
          value={manual.locale}
          onChange={(e) => setManual({ ...manual, locale: e.target.value })}
          className="h-11 rounded-xl border px-3"
        >
          {locales.map((value) => (
            <option key={value}>{value}</option>
          ))}
        </select>
        <select
          aria-label={t("contentTypes")}
          value={manual.content_type}
          onChange={(e) =>
            setManual({
              ...manual,
              content_type: e.target.value,
              ...(e.target.value === "video"
                ? { title: "", creator_name: "", summary: "" }
                : {}),
            })
          }
          className="h-11 rounded-xl border px-3"
        >
          <option value="article">{t("article")}</option>
          <option value="video">{t("video")}</option>
        </select>
        <input
          required
          type="url"
          value={manual.url}
          onChange={(e) => setManual({ ...manual, url: e.target.value })}
          placeholder={t("url")}
          className="h-11 rounded-xl border px-3 md:col-span-3"
        />
        {manual.content_type === "article" && (
          <>
            <input
              required
              value={manual.title}
              onChange={(e) => setManual({ ...manual, title: e.target.value })}
              placeholder={t("contentTitle")}
              className="h-11 rounded-xl border px-3"
            />
            <input
              required
              value={manual.creator_name}
              onChange={(e) =>
                setManual({ ...manual, creator_name: e.target.value })
              }
              placeholder={t("creator")}
              className="h-11 rounded-xl border px-3"
            />
            <label className="block text-sm md:col-span-3">
              <textarea
                maxLength={500}
                value={manual.summary}
                onChange={(e) => setManual({ ...manual, summary: e.target.value })}
                aria-label={t("summary")}
                placeholder={t("summary")}
                className="min-h-20 w-full resize-y rounded-xl border p-3"
              />
              <span className="mt-1 block text-right text-xs text-[var(--muted)]">
                {manual.summary.length}/500
              </span>
            </label>
          </>
        )}
        <div className="flex flex-wrap items-center gap-3 md:col-span-3">
          <label className="flex min-h-11 items-center gap-2 text-sm">
            <input
              type="checkbox"
              checked={manual.approve}
              onChange={(e) => setManual({ ...manual, approve: e.target.checked })}
            />
            <span>
              <strong>{t("approveNow")}</strong>
              <small className="block text-[var(--muted)]">
                {t("approveNowHelp")}
              </small>
            </span>
          </label>
          <button
            disabled={loading}
            className="ml-auto h-11 rounded-xl bg-[var(--teal)] px-4 font-semibold text-white disabled:opacity-40"
          >
            {manual.approve ? t("saveApproved") : t("save")}
          </button>
        </div>
        <NoticeBox notice={manualNotice} className="md:col-span-3" />
      </form>
      {draft && (
        <AISearchSheet
          draft={draft}
          setDraft={setDraft}
          run={run}
          coverage={coverage}
          estimate={estimate}
          loading={loading}
          sheetError={sheetError}
          startSearch={startSearch}
          toggleLocale={toggleLocale}
          toggleType={toggleType}
          t={t}
        />
      )}
    </section>
  );
}

type SheetProps = {
  draft: SearchDraft;
  setDraft: (draft: SearchDraft | null) => void;
  run: SearchRun | null;
  coverage: CoverageResponse | null;
  estimate: { ai: number; brave: number; youtube: number };
  loading: boolean;
  sheetError: string;
  startSearch: () => Promise<void>;
  toggleLocale: (locale: Locale) => void;
  toggleType: (type: ContentType) => void;
  t: ReturnType<typeof useTranslations>;
};

function AISearchSheet({
  draft,
  setDraft,
  run,
  coverage,
  estimate,
  loading,
  sheetError,
  startSearch,
  toggleLocale,
  toggleType,
  t,
}: SheetProps) {
  const active = isRunActive(run);
  const failed = run?.status === "failed";
  const partial = run?.status === "partial";
  const [touchStart, setTouchStart] = useState<number | null>(null);
  return (
    <div
      className="fixed inset-0 z-50 bg-black/45 backdrop-blur-sm"
      onMouseDown={(event) => {
        if (event.target === event.currentTarget && !active) setDraft(null);
      }}
    >
      <section
        role="dialog"
        aria-modal="true"
        aria-labelledby="ai-search-title"
        onTouchStart={(event) =>
          setTouchStart(event.touches[0]?.clientY ?? null)
        }
        onTouchEnd={(event) => {
          const end = event.changedTouches[0]?.clientY;
          if (
            !active &&
            touchStart !== null &&
            end !== undefined &&
            end - touchStart > 100
          )
            setDraft(null);
          setTouchStart(null);
        }}
        className="absolute inset-x-0 bottom-0 max-h-[94dvh] overflow-y-auto rounded-t-[2rem] bg-white px-5 pb-[calc(1.25rem+env(safe-area-inset-bottom))] pt-4 shadow-2xl md:inset-y-0 md:left-auto md:w-[560px] md:max-h-none md:rounded-none md:px-7 md:pt-7"
      >
        <div className="mx-auto mb-4 h-1.5 w-12 rounded-full bg-slate-200 md:hidden" />
        <div className="flex items-start justify-between gap-4">
          <div>
            <p className="flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-violet-700">
              <Sparkles size={15} />
              {t("aiDeepResearch")}
            </p>
            <h2 id="ai-search-title" className="mt-2 text-2xl font-bold">
              {draft.hotspotName}
            </h2>
            <p className="mt-1 text-sm text-[var(--muted)]">
              {t("aiSearchDescription")}
            </p>
          </div>
          <button
            autoFocus
            type="button"
            onClick={() => {
              if (!active) setDraft(null);
            }}
            disabled={Boolean(active)}
            className="grid h-11 w-11 shrink-0 place-items-center rounded-full bg-[var(--paper)] disabled:opacity-40"
            aria-label={t("close")}
          >
            <X size={19} />
          </button>
        </div>
        {sheetError && (
          <p
            role="alert"
            className="mt-4 rounded-xl bg-red-50 p-3 text-sm text-red-800"
          >
            {sheetError}
          </p>
        )}
        {run ? (
          <div className="mt-7">
            <div className="flex items-center justify-between text-sm">
              <strong>{t(`runStatus.${run.status}`)}</strong>
              <span>{run.progress}%</span>
            </div>
            <div className="mt-2 h-2 overflow-hidden rounded-full bg-slate-100">
              <div
                className="h-full rounded-full bg-violet-600 transition-all"
                style={{ width: `${run.progress}%` }}
              />
            </div>
            <div
              className={`mt-5 rounded-2xl p-4 ${
                failed
                  ? "border border-red-200 bg-red-50"
                  : partial
                    ? "border border-amber-200 bg-amber-50"
                    : "bg-[var(--paper)]"
              }`}
            >
              {active ? (
                <p className="flex items-center gap-2">
                  <LoaderCircle
                    className="animate-spin text-violet-600"
                    size={18}
                  />
                  {run.current.locale ? `${run.current.locale} · ` : ""}
                  {run.current.stage
                    ? t(`runStage.${run.current.stage}`)
                    : t("preparing")}
                </p>
              ) : failed ? (
                <>
                  <p className="flex items-center gap-2 font-bold text-red-800">
                    <CircleAlert size={18} />
                    {t("runFailed")}
                  </p>
                  <p className="mt-2 text-sm text-red-900">
                    {run.error_message || runErrorLabel(t, run.error_code)}
                  </p>
                </>
              ) : (
                <>
                  <p className="flex items-center gap-2">
                    {partial ? (
                      <TriangleAlert className="text-amber-600" size={18} />
                    ) : (
                      <CheckCircle2 className="text-emerald-600" size={18} />
                    )}
                    {t("runResult", {
                      created: run.result.created || 0,
                      evaluated: run.result.evaluated || 0,
                    })}
                  </p>
                  {partial && (
                    <p className="mt-2 text-sm text-amber-900">
                      {run.error_message || t("runPartialNote")}
                    </p>
                  )}
                </>
              )}
              <p className="mt-2 text-xs text-[var(--muted)]">
                AI {run.usage.ai_calls || 0} · Brave{" "}
                {run.usage.brave_calls || 0} · YouTube{" "}
                {run.usage.youtube_calls || 0}
              </p>
            </div>
            {run.result.errors?.length ? (
              <div className="mt-4 rounded-2xl border border-amber-200 bg-amber-50 p-4 text-sm text-amber-950">
                <p className="font-bold">{t("runErrors")}</p>
                <ul className="mt-1 list-disc pl-5">
                  {run.result.errors.map((issue, index) => (
                    <li key={`${issue.locale}-${issue.code}-${index}`}>
                      {runIssueText(t, issue)}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
            {run.result.notices?.length ? (
              <div className="mt-4 rounded-2xl bg-[var(--paper)] p-4 text-sm">
                <p className="font-bold">{t("runNotices")}</p>
                <ul className="mt-1 list-disc pl-5">
                  {run.result.notices.map((issue, index) => (
                    <li key={`${issue.locale}-${issue.code}-${index}`}>
                      {runIssueText(t, issue)}
                    </li>
                  ))}
                </ul>
              </div>
            ) : null}
            <div
              className={`mt-6 grid gap-2 ${failed && run.retryable ? "grid-cols-2" : ""}`}
            >
              {failed && run.retryable && (
                <button
                  type="button"
                  onClick={() => void startSearch()}
                  disabled={loading}
                  className="flex min-h-12 items-center justify-center gap-2 rounded-2xl bg-violet-700 font-semibold text-white disabled:opacity-40"
                >
                  <RotateCw size={17} />
                  {t("retryRun")}
                </button>
              )}
              <button
                type="button"
                onClick={() => setDraft(null)}
                disabled={Boolean(active)}
                className="min-h-12 w-full rounded-2xl bg-[var(--ink)] font-semibold text-white disabled:opacity-40"
              >
                {t("done")}
              </button>
            </div>
          </div>
        ) : (
          <>
            <fieldset className="mt-7">
              <legend className="text-sm font-bold">{t("languages")}</legend>
              <div className="mt-2 flex flex-wrap gap-2">
                {locales.map((value) => (
                  <button
                    type="button"
                    key={value}
                    onClick={() => toggleLocale(value)}
                    className={`min-h-11 rounded-xl border px-3 text-sm font-semibold ${draft.locales.includes(value) ? "border-violet-600 bg-violet-50 text-violet-800" : "border-[var(--line)]"}`}
                  >
                    {value}
                  </button>
                ))}
              </div>
            </fieldset>
            <fieldset className="mt-5">
              <legend className="text-sm font-bold">{t("contentTypes")}</legend>
              <div className="mt-2 grid grid-cols-2 gap-2">
                {(["article", "video"] as ContentType[]).map((value) => (
                  <button
                    type="button"
                    key={value}
                    onClick={() => toggleType(value)}
                    className={`min-h-11 rounded-xl border px-3 text-sm font-semibold ${draft.contentTypes.includes(value) ? "border-violet-600 bg-violet-50 text-violet-800" : "border-[var(--line)]"}`}
                  >
                    {t(value)}
                  </button>
                ))}
              </div>
            </fieldset>
            <label className="mt-5 block text-sm font-bold">
              {t("aiProvider")}
              <select
                value={draft.provider}
                onChange={(event) =>
                  setDraft({
                    ...draft,
                    provider: event.target.value as Provider,
                  })
                }
                className="mt-2 h-12 w-full rounded-xl border px-3"
              >
                {providers.map((value) => (
                  <option
                    key={value}
                    value={value}
                    disabled={!coverage?.ai_search.providers[value]}
                  >
                    {t(`providers.${value}`)}
                    {!coverage?.ai_search.providers[value]
                      ? ` · ${t("notConfigured")}`
                      : ""}
                  </option>
                ))}
              </select>
            </label>
            <label className="mt-5 block text-sm font-bold">
              {t("searchDepth")}
              <select
                value={draft.depth}
                onChange={(event) =>
                  setDraft({ ...draft, depth: event.target.value as Depth })
                }
                className="mt-2 h-12 w-full rounded-xl border px-3"
              >
                <option value="economy">{t("depth.economy")}</option>
                <option value="balanced">{t("depth.balanced")}</option>
                <option value="deep">{t("depth.deep")}</option>
              </select>
            </label>
            <label className="mt-5 flex min-h-11 items-center gap-3 rounded-xl bg-[var(--paper)] px-3 text-sm">
              <input
                type="checkbox"
                checked={draft.onlyMissing}
                onChange={(event) =>
                  setDraft({ ...draft, onlyMissing: event.target.checked })
                }
              />
              <span>
                <strong>{t("onlyMissing")}</strong>
                <small className="block text-[var(--muted)]">
                  {t("onlyMissingHelp")}
                </small>
              </span>
            </label>
            <label className="mt-5 block text-sm font-bold">
              {t("customInstructions")}
              <textarea
                maxLength={500}
                value={draft.customInstructions}
                onChange={(event) =>
                  setDraft({ ...draft, customInstructions: event.target.value })
                }
                placeholder={t("customInstructionsPlaceholder")}
                className="mt-2 min-h-24 w-full resize-y rounded-xl border p-3 font-normal"
              />
              <span className="mt-1 block text-right text-xs font-normal text-[var(--muted)]">
                {draft.customInstructions.length}/500
              </span>
            </label>
            <div className="mt-5 rounded-2xl border border-violet-200 bg-violet-50 p-4">
              <p className="text-sm font-bold text-violet-950">
                {t("estimatedCalls")}
              </p>
              <div className="mt-2 grid grid-cols-3 gap-2 text-center text-xs">
                <span>
                  AI<strong className="block text-lg">{estimate.ai}</strong>
                </span>
                <span>
                  Brave
                  <strong className="block text-lg">{estimate.brave}</strong>
                </span>
                <span>
                  YouTube
                  <strong className="block text-lg">{estimate.youtube}</strong>
                </span>
              </div>
              <p className="mt-2 text-xs text-violet-800">
                {t("remainingQuota", {
                  runs: Math.max(
                    0,
                    (coverage?.ai_search.quota.runs_limit || 0) -
                      (coverage?.ai_search.quota.runs_used || 0),
                  ),
                  calls: Math.max(
                    0,
                    (coverage?.ai_search.quota.calls_limit || 0) -
                      (coverage?.ai_search.quota.calls_used || 0),
                  ),
                })}
              </p>
              <p className="mt-1 text-xs text-violet-800">
                Brave{" "}
                {Math.max(
                  0,
                  (coverage?.quotas.brave.limit || 0) -
                    (coverage?.quotas.brave.used || 0),
                )}{" "}
                · YouTube{" "}
                {Math.max(0, 100 - (coverage?.quotas.youtube.used || 0))}
              </p>
            </div>
            {((draft.contentTypes.includes("article") &&
              !coverage?.ai_search.sources.brave) ||
              (draft.contentTypes.includes("video") &&
                !coverage?.ai_search.sources.youtube)) && (
              <p className="mt-4 rounded-xl bg-amber-50 p-3 text-sm text-amber-900">
                {t("sourceNotConfigured")}
              </p>
            )}
            <button
              type="button"
              onClick={() => void startSearch()}
              disabled={
                loading ||
                !draft.locales.length ||
                !draft.contentTypes.length ||
                !coverage?.ai_search.providers[draft.provider] ||
                (draft.contentTypes.includes("article") &&
                  !coverage.ai_search.sources.brave) ||
                (draft.contentTypes.includes("video") &&
                  !coverage.ai_search.sources.youtube)
              }
              className="mt-6 flex min-h-12 w-full items-center justify-center gap-2 rounded-2xl bg-violet-700 px-4 font-semibold text-white disabled:opacity-40"
            >
              <Search size={18} />
              {t("startAiSearch")}
            </button>
          </>
        )}
      </section>
    </div>
  );
}
