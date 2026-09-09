"use client";

import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import {
  AdminReadOnlyNotice,
  useAdminActionGuard,
} from "@/components/admin-action-guard";
import { ApiError, api } from "@/lib/api";
import {
  useAdminQueryState,
  useAdminQueryValue,
} from "@/lib/admin-workspace-navigation";
import {
  adminReviewCopy,
  type CatalogReviewScope,
} from "@/lib/admin-review-copy";
import { adminCatalogBudgetCopy, validCatalogCallLimit } from "@/lib/admin-catalog-budget-copy";
import { useModalSheet } from "@/lib/modal-sheet";
import { safeExternalHref } from "@/lib/navigation";

type Kind = "hotspot" | "food" | "merchant";
type Action = "approve" | "reject" | "keep_pending";
type Mode = "review_pending" | "discover_new";
type Run = {
  id: string;
  scope?: CatalogReviewScope;
  version: number;
  mode: Mode;
  status:
    "queued" | "running" | "completed" | "partial" | "failed" | "cancelled";
  phase: string;
  model: string;
  requested_counts: Record<Kind, number>;
  counts: Record<
    | "total"
    | "assessed"
    | "approved"
    | "rejected"
    | "needs_review"
    | "created"
    | "duplicates"
    | "failed"
    | "applied",
    number
  >;
  usage: {
    calls: number;
    input_tokens: number;
    output_tokens: number;
    thought_tokens?: number;
  };
  error_code: string | null;
  error_message: string | null;
  created_at: string;
  completed_at: string | null;
  review_complete: boolean;
  can_resume: boolean;
  max_calls: number;
  can_extend_budget: boolean;
};
type Item = {
  id: string;
  kind: Kind;
  entity_id: string | null;
  name: string;
  destination_id: string | null;
  phase: "review_pending" | "review_new";
  decision: "approve" | "reject" | "needs_review" | null;
  reason: string;
  evidence: { url: string; quote: string }[];
  gaps: string[];
  allowed_actions: Action[];
  applied_action: string | null;
  status: "pending" | "assessed" | "error" | "applied" | "stale";
  confidence: number | null;
  error_code?: string | null;
};
type Overview = {
  active_run?: { id: string; scope: CatalogReviewScope; status: string } | null;
  configured: boolean;
  model: string;
  daily_call_limit: number;
  run_call_limit: number;
  pending_counts: Record<Kind | "total", number>;
  can_start_review: boolean;
  can_start_discovery: boolean;
  blocking_reasons: string[];
  runs: Run[];
};
type ItemPage = {
  items: Item[];
  total: number;
  page: number;
  page_size: number;
  has_more: boolean;
};
type Outcome = {
  id: string;
  action: string;
  status: "applied" | "skipped";
  reason: string;
};
type Confirmation = {
  runId: string;
  scope: CatalogReviewScope;
  version: number;
  action: Action;
  items: Item[];
  key: string;
};
type BudgetConfirmation = {
  runId: string;
  scope: CatalogReviewScope;
  version: number;
  oldLimit: number;
  newLimit: number;
  calls: number;
  dailyLimit: number;
};

const ROOT = "/admin/catalog-review";
const ACTIONS: Action[] = ["approve", "reject", "keep_pending"];
const KINDS: Kind[] = ["hotspot", "food", "merchant"];
const COUNT_KEYS = [
  "total",
  "assessed",
  "approved",
  "rejected",
  "needs_review",
  "created",
  "duplicates",
  "failed",
  "applied",
] as const;
const buttonBase =
  "min-h-11 rounded-xl border border-[var(--line)] px-4 py-2 text-sm font-semibold disabled:cursor-not-allowed disabled:opacity-40";
const buttonClass = `${buttonBase} bg-white`;
const primaryClass = `${buttonBase} bg-[var(--teal)] text-white`;
const isRunning = (run: Run | null) =>
  run?.status === "queued" || run?.status === "running";
const nonEmptyQuery = (value: string) => value.trim().length > 0;
const positivePage = (value: string) =>
  /^\d+$/.test(value) && Number(value) > 0;

function scopedUrl(path: string, scope?: CatalogReviewScope) {
  return scope
    ? `${path}${path.includes("?") ? "&" : "?"}scope=${scope}`
    : path;
}

function eligible(item: Item, action: Action) {
  return (
    item.status === "assessed" &&
    !item.applied_action &&
    (item.allowed_actions ?? []).includes(action) &&
    (action !== "approve" || (item.gaps ?? []).length === 0)
  );
}

type PanelProps = { scope?: Exclude<CatalogReviewScope, "all"> };

export function AdminCatalogReviewPanel({ scope }: PanelProps = {}) {
  // Scope changes must discard confirmations, selected rows and pending requests.
  return <CatalogReviewContent key={scope ?? "history"} scope={scope} />;
}

function CatalogReviewContent({ scope }: PanelProps) {
  const t = useTranslations("catalogReview");
  const locale = useLocale();
  const copy = adminReviewCopy(locale);
  const budgetCopy = adminCatalogBudgetCopy(locale);
  const manage = useAdminActionGuard("content.manage");
  const overviewUrl = scopedUrl(ROOT, scope);
  const [overview, setOverview] = useState<Overview | null>(null);
  const [runId, setRunId] = useAdminQueryValue("run", "", nonEmptyQuery);
  const runIdRef = useRef(runId);
  useEffect(() => {
    runIdRef.current = runId;
  }, [runId]);
  const [run, setRun] = useState<Run | null>(null);
  const [data, setData] = useState<ItemPage | null>(null);
  const [pageValue, setPageValue] = useAdminQueryValue(
    "page",
    "1",
    positivePage,
  );
  const page = Number(pageValue);
  const [refresh, setRefresh] = useState(0);
  const [loading, setLoading] = useState(true);
  const [itemsLoading, setItemsLoading] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [reconnecting, setReconnecting] = useState(false);
  const [action, setAction] = useAdminQueryState("action", ACTIONS, "approve");
  const [selected, setSelected] = useState<Set<string>>(new Set());
  const [confirmation, setConfirmation] = useState<Confirmation | null>(null);
  const [budgetConfirmation, setBudgetConfirmation] = useState<BudgetConfirmation | null>(null);
  const [outcomes, setOutcomes] = useState<Outcome[]>([]);
  const [updated, setUpdated] = useState<number | null>(null);
  const mutationLock = useRef(false);
  const mutationController = useRef<AbortController | null>(null);
  const startIdentity = useRef<{ signature: string; key: string } | null>(null);
  const confirmRef = useRef<HTMLButtonElement>(null);
  const previewRef = useRef<HTMLButtonElement>(null);
  const active = isRunning(run);
  const budgetDialogRef = useModalSheet<HTMLDivElement>(Boolean(budgetConfirmation), () => {
    if (!mutationLock.current) setBudgetConfirmation(null);
  });

  useEffect(() => () => mutationController.current?.abort(), []);

  useEffect(() => {
    const resetHistorySelection = () => {
      mutationController.current?.abort();
      mutationController.current = null;
      mutationLock.current = false;
      setBusy(false);
      setRun(null);
      setData(null);
      setItemsLoading(Boolean(new URL(window.location.href).searchParams.get("run")));
      setSelected(new Set());
      setConfirmation(null);
      setBudgetConfirmation(null);
      setOutcomes([]);
      setUpdated(null);
      setError("");
    };
    window.addEventListener("popstate", resetHistorySelection);
    return () => window.removeEventListener("popstate", resetHistorySelection);
  }, []);

  useEffect(() => {
    const controller = new AbortController();
    void api<Overview>(overviewUrl, { signal: controller.signal })
      .then((next) => {
        if (controller.signal.aborted) return;
        setOverview(next);
        if (!runIdRef.current) {
          const first = next.runs?.some(
            (item) => item.id === next.active_run?.id,
          )
            ? next.active_run!.id
            : next.runs?.[0]?.id;
          if (first) setRunId(first, true);
        }
      })
      .catch((reason: Error) => {
        if (!controller.signal.aborted) setError(reason.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setLoading(false);
      });
    return () => controller.abort();
  }, [refresh, overviewUrl, setRunId]);

  useEffect(() => {
    if (!runId) return;
    const controller = new AbortController();
    void Promise.all([
      api<Run>(scopedUrl(`${ROOT}/runs/${runId}`, scope), {
        signal: controller.signal,
      }),
      api<ItemPage>(
        scopedUrl(
          `${ROOT}/runs/${runId}/items?page=${page}&page_size=30`,
          scope,
        ),
        { signal: controller.signal },
      ),
    ])
      .then(([next, items]) => {
        if (controller.signal.aborted) return;
        setRun(next);
        setData(items);
        setReconnecting(false);
      })
      .catch((reason: Error) => {
        if (!controller.signal.aborted) setError(reason.message);
      })
      .finally(() => {
        if (!controller.signal.aborted) setItemsLoading(false);
      });
    return () => controller.abort();
  }, [runId, page, refresh, scope]);

  useEffect(() => {
    if (!runId || !active || busy || confirmation || budgetConfirmation || itemsLoading) return;
    const controller = new AbortController();
    let timer: ReturnType<typeof setTimeout>;
    const poll = async () => {
      try {
        // Schedule only after the previous request completes, including slow responses.
        const next = await api<Run>(scopedUrl(`${ROOT}/runs/${runId}`, scope), {
          signal: controller.signal,
        });
        if (controller.signal.aborted) return;
        const items = await api<ItemPage>(
          scopedUrl(
            `${ROOT}/runs/${runId}/items?page=${page}&page_size=30`,
            scope,
          ),
          { signal: controller.signal },
        );
        if (controller.signal.aborted) return;
        let nextOverview: Overview | null = null;
        if (!isRunning(next)) {
          try {
            nextOverview = await api<Overview>(overviewUrl, {
              signal: controller.signal,
            });
          } catch (reason) {
            if (controller.signal.aborted) return;
            // Preserve the final assessment even if capabilities cannot be refreshed.
            setError((reason as Error).message);
            setOverview((current) =>
              current
                ? {
                    ...current,
                    can_start_review: false,
                    can_start_discovery: false,
                  }
                : null,
            );
          }
        }
        if (controller.signal.aborted) return;
        setRun(next);
        setData(items);
        setSelected(
          (current) =>
            new Set(
              items.items
                .filter(
                  (item) => current.has(item.id) && eligible(item, action),
                )
                .map((item) => item.id),
            ),
        );
        setReconnecting(false);
        if (nextOverview) setOverview(nextOverview);
        if (!isRunning(next)) {
          return;
        }
      } catch {
        if (controller.signal.aborted) return;
        setReconnecting(true);
      }
      if (!controller.signal.aborted) timer = setTimeout(poll, 3_000);
    };
    timer = setTimeout(poll, 3_000);
    return () => {
      controller.abort();
      clearTimeout(timer);
    };
  }, [
    runId,
    page,
    active,
    busy,
    confirmation,
    budgetConfirmation,
    itemsLoading,
    action,
    scope,
    overviewUrl,
  ]);

  useEffect(() => {
    if (confirmation) confirmRef.current?.focus();
  }, [confirmation]);

  const history = overview?.runs ?? [];
  // Detail polling is fresher than the overview, including while a run is active.
  const runs = run
    ? history.some((item) => item.id === run.id)
      ? history.map((item) => (item.id === run.id ? run : item))
      : [run, ...history]
    : history;
  const priorReview = runs.find(
    (item) =>
      item.mode === "review_pending" &&
      item.review_complete &&
      item.scope === scope,
  );
  const items = data?.items ?? [];
  const eligibleItems = items.filter((item) => eligible(item, action));
  const selectedItems = eligibleItems.filter((item) => selected.has(item.id));
  const canApply = Boolean(
    manage.allowed &&
    run &&
    run.id === runId &&
    (!scope || run.scope === scope) &&
    !active &&
    !itemsLoading,
  );
  const canReview = Boolean(
    manage.allowed &&
    scope &&
    overview?.configured &&
    validCatalogCallLimit(overview.run_call_limit) &&
    overview.can_start_review,
  );
  const canDiscover = Boolean(
    manage.allowed &&
    scope &&
    overview?.configured &&
    validCatalogCallLimit(overview.run_call_limit) &&
    overview.can_start_discovery &&
    priorReview,
  );
  const requestedCounts =
    scope === "hotspots"
      ? { hotspot: 40, food: 0, merchant: 0 }
      : { hotspot: 0, food: 20, merchant: 40 };
  const targetCount = scope === "hotspots" ? 40 : 60;
  const visibleKinds: Kind[] =
    scope === "hotspots"
      ? ["hotspot"]
      : scope === "foods"
        ? ["food", "merchant"]
        : KINDS;
  const label = (group: string, value: string) =>
    t.has(`${group}.${value}`) ? t(`${group}.${value}`) : value;
  const knownError = (code?: string | null) =>
    code === "catalog_review_call_limit" ? budgetCopy.limitReached :
      code === "validation_error" ? budgetCopy.limitChanged :
        code && t.has(`errors.${code}`) ? t(`errors.${code}`) : null;
  const itemReason = (item: Item) =>
    item.status === "error"
      ? (knownError(item.error_code) ?? t("unknownItemError"))
      : item.reason;
  const dateLabel = (value: string) =>
    new Intl.DateTimeFormat(locale, {
      dateStyle: "short",
      timeStyle: "short",
    }).format(new Date(value));
  const canExtendBudget = Boolean(
    manage.allowed &&
    run && run.id === runId &&
    (!scope || run.scope === scope) &&
    // The server also permits lease-expired worker recovery. Never infer that
    // permission from a queued/running status on the client.
    run.can_extend_budget && !itemsLoading &&
    validCatalogCallLimit(run.max_calls) &&
    validCatalogCallLimit(overview?.run_call_limit) &&
    overview!.run_call_limit > run.max_calls &&
    overview!.run_call_limit > (run.usage?.calls ?? 0) &&
    (!overview?.active_run || overview.active_run.id === run.id),
  );
  const currentBudgetConfirmation = Boolean(
    budgetConfirmation && canExtendBudget &&
    budgetConfirmation.runId === runId &&
    budgetConfirmation.scope === (run?.scope ?? "all") &&
    budgetConfirmation.version === run?.version &&
    budgetConfirmation.oldLimit === run?.max_calls &&
    budgetConfirmation.newLimit === overview?.run_call_limit &&
    budgetConfirmation.calls === (run?.usage?.calls ?? 0) &&
    budgetConfirmation.dailyLimit === overview?.daily_call_limit,
  );

  function selectRun(id: string) {
    setRunId(id);
    setRun(null);
    setData(null);
    setPageValue("1", true);
    setItemsLoading(true);
    setSelected(new Set());
    setConfirmation(null);
    setBudgetConfirmation(null);
    setError("");
    setOutcomes([]);
    setUpdated(null);
  }

  function refreshView() {
    setSelected(new Set());
    setBudgetConfirmation(null);
    setItemsLoading(Boolean(runId));
    setError("");
    setRefresh((value) => value + 1);
  }

  function beginMutation() {
    if (mutationLock.current) return null;
    mutationLock.current = true;
    const controller = new AbortController();
    mutationController.current = controller;
    setBusy(true);
    setError("");
    return controller;
  }

  function endMutation(controller: AbortController) {
    mutationLock.current = false;
    if (!controller.signal.aborted) setBusy(false);
  }

  async function start(mode: Mode) {
    if (!scope) return;
    if (mode === "review_pending" ? !canReview : !canDiscover) return;
    const controller = beginMutation();
    if (!controller) return;
    const payload = {
      mode,
      scope,
      requested_counts: requestedCounts,
      max_calls: overview!.run_call_limit,
      ...(mode === "discover_new"
        ? { prior_review_run_id: priorReview!.id }
        : {}),
    };
    const signature = JSON.stringify(payload);
    if (startIdentity.current?.signature !== signature)
      startIdentity.current = { signature, key: crypto.randomUUID() };
    try {
      const next = await api<Run>(`${ROOT}/runs`, {
        method: "POST",
        signal: controller.signal,
        headers: { "Idempotency-Key": startIdentity.current.key },
        body: signature,
      });
      if (controller.signal.aborted) return;
      startIdentity.current = null;
      selectRun(next.id);
      setRun(next);
      setRefresh((value) => value + 1);
    } catch (reason) {
      if (!controller.signal.aborted) {
        setError((reason instanceof ApiError && knownError(reason.code)) || (reason as Error).message);
        if (reason instanceof ApiError && reason.code === "validation_error") setRefresh((value) => value + 1);
      }
    } finally {
      endMutation(controller);
    }
  }

  async function resume() {
    if (!manage.allowed || !run?.can_resume || run.id !== runId || (scope && run.scope !== scope)) return;
    const controller = beginMutation();
    if (!controller) return;
    try {
      const next = await api<Run>(
        scopedUrl(`${ROOT}/runs/${run.id}/resume`, run.scope ?? "all"),
        { method: "POST", signal: controller.signal },
      );
      if (controller.signal.aborted) return;
      setRun(next);
      refreshView();
    } catch (reason) {
      if (!controller.signal.aborted) setError((reason as Error).message);
    } finally {
      endMutation(controller);
    }
  }

  async function extendBudgetAndResume() {
    if (!budgetConfirmation || !currentBudgetConfirmation) return;
    const controller = beginMutation();
    if (!controller) return;
    try {
      const next = await api<Run>(
        scopedUrl(`${ROOT}/runs/${budgetConfirmation.runId}/resume`, budgetConfirmation.scope),
        {
          method: "POST",
          signal: controller.signal,
          body: JSON.stringify({ expected_version: budgetConfirmation.version, max_calls: budgetConfirmation.newLimit }),
        },
      );
      if (controller.signal.aborted) return;
      setRun(next);
      refreshView();
    } catch (reason) {
      if (controller.signal.aborted) return;
      // Refresh uncertain outcomes as well: a response can be lost after the server
      // accepted the extension. Never replay paid execution without fresh consent.
      setBudgetConfirmation(null);
      setItemsLoading(true);
      setRefresh((value) => value + 1);
      setError(reason instanceof ApiError && reason.code === "catalog_run_not_resumable" ? budgetCopy.limitChanged : (reason instanceof ApiError && knownError(reason.code)) || (reason as Error).message);
    } finally {
      endMutation(controller);
    }
  }

  function closeConfirmation() {
    if (busy) return;
    setConfirmation(null);
    requestAnimationFrame(() => previewRef.current?.focus());
  }

  async function apply() {
    if (
      !confirmation ||
      !canApply ||
      confirmation.runId !== runId ||
      run?.id !== runId
    ) return;
    const controller = beginMutation();
    if (!controller) return;
    try {
      const result = await api<{
        run: Run;
        outcomes: Outcome[];
        updated: number;
      }>(
        scopedUrl(
          `${ROOT}/runs/${confirmation.runId}/apply`,
          confirmation.scope,
        ),
        {
          method: "POST",
          signal: controller.signal,
          headers: { "Idempotency-Key": confirmation.key },
          body: JSON.stringify({
            item_ids: confirmation.items.map((item) => item.id),
            action: confirmation.action,
            expected_version: confirmation.version,
          }),
        },
      );
      if (controller.signal.aborted) return;
      setRun(result.run);
      setOutcomes(result.outcomes ?? []);
      setUpdated(result.updated);
      setConfirmation(null);
      refreshView();
    } catch (reason) {
      if (controller.signal.aborted) return;
      if (reason instanceof ApiError && reason.status === 409) {
        setConfirmation(null);
        setSelected(new Set());
        setItemsLoading(true);
        setRefresh((value) => value + 1);
      }
      // An uncertain response can be retried with the same confirmation and key.
      setError((reason as Error).message);
    } finally {
      endMutation(controller);
    }
  }

  return (
    <div className="mt-7 space-y-6">
      <AdminReadOnlyNotice capability="content.manage" />
      {error && !confirmation && !budgetConfirmation && (
        <p
          role="alert"
          className="rounded-2xl bg-red-50 p-4 text-sm text-red-900"
        >
          {error}
        </p>
      )}
      {reconnecting && (
        <p
          role="status"
          className="rounded-2xl bg-amber-50 p-4 text-sm text-amber-900"
        >
          {t("reconnecting")}
        </p>
      )}
      {loading && <p role="status">{t("loading")}</p>}
      {!scope && (
        <p className="rounded-2xl bg-[var(--paper)] p-4 text-sm">
          {copy.historyOnly}
        </p>
      )}
      {scope && (
        <section
          aria-label={t("workflow")}
          className="grid gap-4 lg:grid-cols-2"
        >
          <article className="rounded-3xl border border-[var(--line)] bg-white p-5">
            <p className="text-xs font-bold text-[var(--teal)]">
              {t("step", { number: 1 })}
            </p>
            <h2 className="mt-2 text-xl font-bold">{t("reviewTitle")}</h2>
            <p className="mt-2 text-sm text-[var(--muted)]">
              {t("reviewDescription")}
            </p>
            <dl className="my-4 grid grid-cols-3 gap-2 text-sm">
              {visibleKinds.map((kind) => (
                <div key={kind}>
                  <dt className="text-[var(--muted)]">{t(`kinds.${kind}`)}</dt>
                  <dd className="mt-1 text-xl font-bold">
                    {overview?.pending_counts?.[kind] ?? "—"}
                  </dd>
                </div>
              ))}
            </dl>
            <button
              type="button"
              disabled={busy || loading || !canReview}
              onClick={() => void start("review_pending")}
              className={primaryClass}
            >
              {t("startReview")}
            </button>
          </article>
          <article className="rounded-3xl border border-[var(--line)] bg-white p-5">
            <p className="text-xs font-bold text-[var(--teal)]">
              {t("step", { number: 2 })}
            </p>
            <h2 className="mt-2 text-xl font-bold">
              {copy.discovery.replace("{count}", String(targetCount))}
            </h2>
            <p className="mt-2 text-sm text-[var(--muted)]">
              {t("discoveryDescription")}
            </p>
            <p className="my-4 text-sm font-semibold">
              {scope === "hotspots" ? copy.hotspotCounts : copy.foodCounts}
            </p>
            <button
              type="button"
              disabled={busy || loading || !canDiscover}
              onClick={() => void start("discover_new")}
              className={primaryClass}
            >
              {copy.startDiscovery.replace("{count}", String(targetCount))}
            </button>
            {!priorReview && (
              <p className="mt-3 text-xs text-[var(--muted)]">
                {t("reviewFirst")}
              </p>
            )}
          </article>
        </section>
      )}
      <section
        aria-label={t("availability")}
        className="rounded-2xl bg-[var(--paper)] p-4 text-sm"
      >
        <p>{t("provider", { model: overview?.model || "—" })}</p>
        <p className="mt-1 text-[var(--muted)]">
          {budgetCopy.defaultLimits.replace("{run}", String(overview?.run_call_limit ?? "—")).replace("{daily}", String(overview?.daily_call_limit ?? "—"))}
        </p>
        <a href={`/${locale}/admin/settings?provider=gemini_guides&field=catalog_review_max_calls`} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline focus-visible:outline-2 focus-visible:outline-offset-2">{budgetCopy.configure}</a>
        <p className="mt-1 text-[var(--muted)]">{copy.sharedQuota}</p>
        {scope &&
          overview?.active_run &&
          overview.active_run.scope !== scope && (
            <p role="status" className="mt-2 text-[var(--ink)]">
              {copy.activeElsewhere.replace(
                "{scope}",
                copy.scopes[overview.active_run.scope],
              )}{" "}
              <a
                href={`/${locale}/admin/catalog-review`}
                className="inline-flex min-h-11 items-center underline"
              >
                {copy.openHistory}
              </a>
            </p>
          )}
        {overview && !overview.configured && (
          <p className="mt-2 text-amber-800">{t("notConfigured")}</p>
        )}
        {(overview?.blocking_reasons ?? []).length > 0 && (
          <ul className="mt-2 list-disc pl-5 text-amber-800">
            {overview!.blocking_reasons.map((reason, index) => (
              <li key={index}>{knownError(reason) ?? reason}</li>
            ))}
          </ul>
        )}
      </section>
      <section className="rounded-3xl border border-[var(--line)] bg-white p-5">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <h2 className="text-xl font-bold">{t("history")}</h2>
          <button
            type="button"
            disabled={busy || itemsLoading}
            onClick={refreshView}
            className={buttonClass}
          >
            {t("refresh")}
          </button>
        </div>
        {runs.length > 0 ? (
          <select
            aria-label={t("selectRun")}
            value={runId ?? ""}
            disabled={busy}
            onChange={(event) => selectRun(event.target.value)}
            className="mt-4 min-h-11 w-full rounded-xl border border-[var(--line)] bg-white px-3"
          >
            {runs.map((item) => (
              <option key={item.id} value={item.id}>
                {dateLabel(item.created_at)} ·{" "}
                {copy.scopes[item.scope ?? "all"]} · {label("modes", item.mode)}{" "}
                · {label("runStatus", item.status)}
              </option>
            ))}
          </select>
        ) : (
          <p className="mt-3 text-sm text-[var(--muted)]">{t("noRuns")}</p>
        )}
        {run && (
          <div className="mt-5 border-t border-[var(--line)] pt-5">
            <div className="flex flex-wrap items-center justify-between gap-3">
              <p className="font-bold">
                {label("modes", run.mode)} ·{" "}
                <span role="status">{label("runStatus", run.status)}</span>
              </p>
              {run.can_resume && manage.allowed && (
                <button
                  type="button"
                  disabled={busy}
                  onClick={() => void resume()}
                  className={buttonClass}
                >
                  {t("resume")}
                </button>
              )}
              {canExtendBudget && (
                <button
                  type="button"
                  disabled={busy || Boolean(confirmation)}
                  onClick={() => {
                    if (!canExtendBudget || !overview || !validCatalogCallLimit(run.max_calls)) return;
                    setError("");
                    setBudgetConfirmation({ runId: run.id, scope: run.scope ?? "all", version: run.version, oldLimit: run.max_calls, newLimit: overview.run_call_limit, calls: run.usage?.calls ?? 0, dailyLimit: overview.daily_call_limit });
                  }}
                  className={buttonClass}
                >
                  {budgetCopy.extend}
                </button>
              )}
            </div>
            <p className="mt-2 text-sm text-[var(--muted)]">
              {budgetCopy.runLimit.replace("{run}", String(run.max_calls ?? "—")).replace("{used}", String(run.usage?.calls ?? 0))}
            </p>
            <p className="mt-2 text-sm text-[var(--muted)]">
              {t("provider", { model: run.model })} ·{" "}
              {label("phases", run.phase)}
            </p>
            <p className="mt-1 text-xs text-[var(--muted)]">
              {t("usage", {
                calls: run.usage?.calls ?? 0,
                input: run.usage?.input_tokens ?? 0,
                output: run.usage?.output_tokens ?? 0,
              })}
              {typeof run.usage?.thought_tokens === "number" && (
                <> · {t("thoughtUsage", { count: run.usage.thought_tokens })}</>
              )}
            </p>
            {run.error_message || run.error_code ? (
              <div
                role="alert"
                className="mt-3 rounded-xl bg-amber-50 p-3 text-sm text-amber-900"
              >
                {(knownError(run.error_code) || run.error_message) && (
                  <p>{knownError(run.error_code) ?? run.error_message}</p>
                )}
                {run.error_code && run.error_code !== run.error_message && (
                  <p
                    className={
                      run.error_message || knownError(run.error_code)
                        ? "mt-1 text-xs"
                        : ""
                    }
                  >
                    {run.error_code}
                  </p>
                )}
              </div>
            ) : null}
            {run.review_complete && (
              <p className="mt-3 text-sm font-semibold text-[var(--teal-dark)]">
                {t("reviewComplete")}
              </p>
            )}
            <dl className="mt-4 grid grid-cols-3 gap-3 sm:grid-cols-5">
              {COUNT_KEYS.map((key) => (
                <div key={key} className="rounded-xl bg-[var(--paper)] p-3">
                  <dt className="text-xs text-[var(--muted)]">
                    {t(`counts.${key}`)}
                  </dt>
                  <dd className="mt-1 text-lg font-bold">
                    {run.counts?.[key] ?? 0}
                  </dd>
                </div>
              ))}
            </dl>
          </div>
        )}
      </section>
      {runId && (
        <section aria-label={t("assessment")} className="space-y-4">
          <div>
            <h2 className="text-xl font-bold">{t("assessment")}</h2>
            <p className="mt-2 text-sm text-[var(--muted)]">
              {t("assessmentDescription")}
            </p>
          </div>
          {active && (
            <p
              role="status"
              className="rounded-xl bg-[var(--paper)] p-3 text-sm"
            >
              {t("waitForRun")}
            </p>
          )}
          <div className="flex flex-wrap items-center gap-3">
            <label className="text-sm font-semibold">
              {t("batchAction")}
            <select
              value={action}
              disabled={!manage.allowed || busy || Boolean(confirmation)}
              title={!manage.allowed ? manage.disabledReason : undefined}
                onChange={(event) => {
                  setAction(event.target.value as Action);
                  setSelected(new Set());
                }}
                className="ml-2 min-h-11 rounded-xl border border-[var(--line)] bg-white px-3"
              >
                {ACTIONS.map((value) => (
                  <option key={value} value={value}>
                    {t(`actions.${value}`)}
                  </option>
                ))}
              </select>
            </label>
            <button
              type="button"
              disabled={busy || !canApply || !eligibleItems.length}
              onClick={() =>
                setSelected(new Set(eligibleItems.map((item) => item.id)))
              }
              className={buttonClass}
            >
              {t("selectPage", { count: eligibleItems.length })}
            </button>
            <button
              type="button"
              disabled={busy || !selected.size}
              onClick={() => setSelected(new Set())}
              className={buttonClass}
            >
              {t("clearSelection")}
            </button>
            <button
              ref={previewRef}
              type="button"
              disabled={busy || !canApply || !selectedItems.length}
              onClick={() => {
                if (run && canApply)
                  setConfirmation({
                    runId: run.id,
                    scope: run.scope ?? "all",
                    version: run.version,
                    action,
                    items: selectedItems,
                    key: crypto.randomUUID(),
                  });
              }}
              className={primaryClass}
            >
              {t("previewAction", { count: selectedItems.length })}
            </button>
          </div>
          {itemsLoading && (
            <p role="status" className="text-sm">
              {t("loading")}
            </p>
          )}
          <table className="block w-full rounded-2xl border border-[var(--line)] bg-white text-left text-sm lg:table">
            <thead className="hidden bg-[var(--paper)] lg:table-header-group">
              <tr>
                {["select", "candidate", "decision", "evidence", "gaps"].map(
                  (key) => (
                    <th key={key} className="p-3">
                      {t(`columns.${key}`)}
                    </th>
                  ),
                )}
              </tr>
            </thead>
            <tbody className="block divide-y divide-[var(--line)] lg:table-row-group">
              {items.map((item) => (
                <tr
                  key={item.id}
                  className="grid gap-2 p-3 align-top lg:table-row lg:p-0"
                >
                  <td className="lg:p-3">
                    <input
                      type="checkbox"
                      aria-label={t("selectItem", { name: item.name })}
                      checked={selected.has(item.id) && eligible(item, action)}
                      disabled={busy || !canApply || !eligible(item, action)}
                      onChange={(event) =>
                        setSelected((current) => {
                          const next = new Set(current);
                          if (event.target.checked) next.add(item.id);
                          else next.delete(item.id);
                          return next;
                        })
                      }
                      className="h-5 w-5"
                    />
                  </td>
                  <td className="lg:p-3">
                    <p className="font-bold">{item.name}</p>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      {t(`kinds.${item.kind}`)} · {item.destination_id || "—"}
                    </p>
                    <p className="mt-1 text-xs text-[var(--muted)]">
                      {label("phases", item.phase)} ·{" "}
                      {label("itemStatus", item.status)}
                    </p>
                  </td>
                  <td className="lg:max-w-sm lg:p-3">
                    <p className="font-semibold">
                      {item.decision
                        ? label("decisions", item.decision)
                        : t("notAssessed")}
                    </p>
                    <p className="mt-1 whitespace-pre-wrap">
                      {itemReason(item)}
                    </p>
                    {item.confidence != null && (
                      <p className="mt-1 text-xs text-[var(--muted)]">
                        {t("confidence", { value: item.confidence })}
                      </p>
                    )}
                    {item.applied_action && (
                      <p className="mt-2 text-xs font-semibold text-[var(--teal-dark)]">
                        {t("appliedAction", {
                          action: label("actions", item.applied_action),
                        })}
                      </p>
                    )}
                  </td>
                  <td className="lg:max-w-sm lg:p-3">
                    <details>
                      <summary className="min-h-9 cursor-pointer font-semibold text-[var(--teal)]">
                        {t("evidenceCount", {
                          count: item.evidence?.length ?? 0,
                        })}
                      </summary>
                      {(item.evidence ?? []).map((source, index) => (
                        <div
                          key={index}
                          className="mt-2 break-words rounded-xl bg-[var(--paper)] p-3"
                        >
                          {safeExternalHref(source.url) ? (
                            <a
                              href={safeExternalHref(source.url)}
                              target="_blank"
                              rel="noreferrer"
                              className="break-all text-xs text-[var(--teal)] underline"
                            >
                              {source.url}
                            </a>
                          ) : (
                            <p className="text-xs text-[var(--muted)]">
                              {t("invalidEvidenceLink")}
                            </p>
                          )}
                          <blockquote className="mt-2 whitespace-pre-wrap text-xs leading-5">
                            {source.quote}
                          </blockquote>
                        </div>
                      ))}
                    </details>
                  </td>
                  <td className="lg:max-w-xs lg:p-3">
                    {item.gaps?.length ? (
                      <ul
                        aria-label={t("itemGaps", { name: item.name })}
                        className="list-disc space-y-1 pl-4 text-xs text-amber-900"
                      >
                        {item.gaps.map((gap, index) => (
                          <li key={index}>{label("gaps", gap)}</li>
                        ))}
                      </ul>
                    ) : (
                      <p className="text-xs text-[var(--muted)]">
                        {t("noGapsReported")}
                      </p>
                    )}
                    {!eligible(item, action) && !item.applied_action && (
                      <p className="mt-2 text-xs text-[var(--muted)]">
                        {t("actionUnavailable", {
                          action: t(`actions.${action}`),
                        })}
                      </p>
                    )}
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!itemsLoading && data && !items.length && (
            <p className="rounded-xl bg-[var(--paper)] p-5 text-sm">
              {t("noItems")}
            </p>
          )}
          <nav
            aria-label={t("pagination")}
            className="flex flex-wrap items-center justify-end gap-3"
          >
            <span className="mr-auto text-sm text-[var(--muted)]">
              {t("pageCount", {
                page: data?.page ?? page,
                total: data?.total ?? 0,
              })}
            </span>
            <button
              type="button"
              disabled={busy || itemsLoading || page <= 1}
              onClick={() => {
                setSelected(new Set());
                setItemsLoading(true);
                setPageValue(String(page - 1));
              }}
              className={buttonClass}
            >
              {t("previous")}
            </button>
            <button
              type="button"
              disabled={busy || itemsLoading || !data?.has_more}
              onClick={() => {
                setSelected(new Set());
                setItemsLoading(true);
                setPageValue(String(page + 1));
              }}
              className={buttonClass}
            >
              {t("next")}
            </button>
          </nav>
        </section>
      )}
      {updated != null && (
        <section
          aria-label={t("applyResults")}
          className="rounded-2xl bg-[var(--paper)] p-4"
        >
          <p role="status" className="font-semibold">
            {t("updated", { count: updated })}
          </p>
          <ul className="mt-3 space-y-2 text-sm">
            {outcomes.map((outcome) => (
              <li key={outcome.id}>
                <span className="font-semibold">
                  {items.find((item) => item.id === outcome.id)?.name ??
                    outcome.id}{" "}
                  · {label("outcomeStatus", outcome.status)}
                </span>
                {outcome.reason && (
                  <p>
                    {outcome.status === "skipped"
                      ? label("applyReasons", outcome.reason)
                      : outcome.reason}
                  </p>
                )}
              </li>
            ))}
          </ul>
        </section>
      )}
      {budgetConfirmation && (
        <div className="fixed inset-0 z-[80] grid place-items-center bg-slate-950/45 p-4">
          <div ref={budgetDialogRef} role="dialog" aria-modal="true" aria-labelledby="catalog-budget-confirm-title" aria-describedby="catalog-budget-confirm-description" tabIndex={-1} className="max-h-[90dvh] w-full max-w-xl overflow-y-auto rounded-3xl border border-[var(--line)] bg-[var(--paper)] p-6 text-[var(--ink)]">
            <h2 id="catalog-budget-confirm-title" className="text-xl font-bold">{budgetCopy.confirmTitle}</h2>
            <p id="catalog-budget-confirm-description" className="mt-3 text-sm text-[var(--muted)]">{budgetCopy.confirmDescription}</p>
            <dl className="my-5 grid gap-3 text-sm sm:grid-cols-2">
              {([
                [budgetCopy.oldLimit, budgetConfirmation.oldLimit],
                [budgetCopy.newLimit, budgetConfirmation.newLimit],
                [budgetCopy.used, budgetConfirmation.calls],
                [budgetCopy.remaining, Math.max(0, budgetConfirmation.newLimit - budgetConfirmation.calls)],
                [budgetCopy.dailyLimit, budgetConfirmation.dailyLimit],
              ] as const).map(([title, value]) => <div key={title} className="rounded-xl border border-[var(--line)] p-3"><dt className="text-[var(--muted)]">{title}</dt><dd className="mt-1 text-xl font-bold">{value}</dd></div>)}
            </dl>
            <p className="text-sm text-[var(--muted)]">{budgetCopy.preservation}</p>
            <div className="mt-5 flex flex-wrap justify-end gap-3">
              <button type="button" disabled={busy} aria-label={t("cancel")} onClick={() => setBudgetConfirmation(null)} className={`${buttonBase} bg-[var(--paper)] focus-visible:outline-2 focus-visible:outline-offset-2`}>{t("cancel")}</button>
              <button type="button" disabled={busy || !currentBudgetConfirmation} onClick={() => void extendBudgetAndResume()} className={primaryClass}>{busy ? budgetCopy.resuming : budgetCopy.confirm}</button>
            </div>
          </div>
        </div>
      )}
      {confirmation && (
        <div className="fixed inset-0 z-[80] grid place-items-center bg-slate-950/45 p-4">
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby="catalog-review-confirm-title"
            onKeyDown={(event) => {
              if (event.key === "Escape") closeConfirmation();
              if (event.key === "Tab") {
                const controls =
                  event.currentTarget.querySelectorAll<HTMLButtonElement>(
                    "button:not(:disabled)",
                  );
                const first = controls[0];
                const last = controls[controls.length - 1];
                if (event.shiftKey && document.activeElement === first) {
                  event.preventDefault();
                  last?.focus();
                } else if (!event.shiftKey && document.activeElement === last) {
                  event.preventDefault();
                  first?.focus();
                }
              }
            }}
            className="max-h-[90dvh] w-full max-w-xl overflow-y-auto rounded-3xl bg-white p-6"
          >
            <h2 id="catalog-review-confirm-title" className="text-xl font-bold">
              {t("confirmTitle", {
                action: t(`actions.${confirmation.action}`),
                count: confirmation.items.length,
              })}
            </h2>
            <p className="mt-3 text-sm text-[var(--muted)]">
              {t("confirmDescription")}
            </p>
            <ul className="my-4 space-y-3">
              {confirmation.items.map((item) => (
                <li
                  key={item.id}
                  className="rounded-xl bg-[var(--paper)] p-3 text-sm"
                >
                  <p className="font-semibold">{item.name}</p>
                  <p className="mt-1">{item.reason}</p>
                </li>
              ))}
            </ul>
            {error && (
              <p
                role="alert"
                className="mb-4 rounded-xl bg-red-50 p-3 text-sm text-red-900"
              >
                {error}
              </p>
            )}
            <div className="flex flex-wrap justify-end gap-3">
              <button
                type="button"
                disabled={busy}
                onClick={closeConfirmation}
                className={buttonClass}
              >
                {t("cancel")}
              </button>
              <button
                ref={confirmRef}
                type="button"
                disabled={busy}
                onClick={() => void apply()}
                className={primaryClass}
              >
                {busy ? t("applying") : t("confirmApply")}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
