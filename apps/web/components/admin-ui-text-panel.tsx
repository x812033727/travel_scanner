"use client";

import { Check, LoaderCircle, RefreshCw } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useState } from "react";
import { FilterPills } from "@/components/admin-filter-pills";
import { localeLabels, type Locale } from "@/i18n/routing";
import { useRouter } from "@/i18n/navigation";
import { ApiError, api } from "@/lib/api";
import {
  UI_TEXT_BATCH_LIMIT,
  UI_TEXT_MAX_LENGTH,
  chunk,
  hasAdvancedIcu,
  messageParameters,
  overrideProblem,
  type EditableNamespace,
  type UiTextEntries,
} from "@/lib/ui-text";

type UiTextEntry = {
  namespace: string;
  key: string;
  locale: string;
  value: string;
  default_snapshot: string | null;
  updated_at: string;
  updated_by_email: string | null;
};

type UiTextSnapshot = {
  locale: string;
  namespace: string | null;
  version: string;
  entries: UiTextEntry[];
};

type NamespaceSummary = { namespace: EditableNamespace; keyCount: number };

type Props = {
  namespace: EditableNamespace;
  locale: Locale;
  referenceLocale: Locale;
  defaults: UiTextEntries;
  referenceDefaults: UiTextEntries;
  namespaces: NamespaceSummary[];
};

type Row = {
  key: string;
  defaultValue: string | undefined;
  reference: string | undefined;
  override: UiTextEntry | undefined;
  shown: string;
  dirty: boolean;
  pendingRestore: boolean;
  problem: "braces" | "parameters" | undefined;
  orphan: boolean;
};

// Same shape as admin-settings-panel: only 401 and 403 are about who you are signed in as,
// and a rejection that never reached the server carries a browser string, not a server one.
type LoadFailure =
  | { kind: "permission"; detail: string; requestId?: string }
  | { kind: "unreachable" }
  | { kind: "failed"; detail: string; requestId?: string };

function loadFailure(reason: unknown): LoadFailure {
  if (!(reason instanceof ApiError)) return { kind: "unreachable" };
  return {
    kind: reason.status === 401 || reason.status === 403 ? "permission" : "failed",
    detail: reason.message,
    requestId: reason.requestId,
  };
}

const PAGE_SIZE = 50;

export function AdminUiTextPanel({
  namespace,
  locale,
  referenceLocale,
  defaults,
  referenceDefaults,
  namespaces,
}: Props) {
  const t = useTranslations("admin.uiText");
  const shared = useTranslations("admin.settingsPanel");
  const uiLocale = useLocale();
  const router = useRouter();
  const dateTime = useMemo(
    () => new Intl.DateTimeFormat(uiLocale, { dateStyle: "medium", timeStyle: "short" }),
    [uiLocale],
  );

  const [overrides, setOverrides] = useState<Record<string, UiTextEntry>>();
  const [loadError, setLoadError] = useState<LoadFailure>();
  const [drafts, setDrafts] = useState<Record<string, string>>({});
  const [filter, setFilter] = useState("");
  const [query, setQuery] = useState("");
  const [page, setPage] = useState(1);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState<string>();
  const [actionError, setActionError] = useState<string>();

  const path = `/admin/ui-text?namespace=${namespace}&locale=${encodeURIComponent(locale)}`;

  const load = useCallback(async () => {
    const snapshot = await api<UiTextSnapshot>(path);
    return Object.fromEntries(snapshot.entries.map((entry) => [entry.key, entry]));
  }, [path]);

  useEffect(() => {
    let active = true;
    load()
      .then((entries) => {
        if (active) setOverrides(entries);
      })
      .catch((reason: unknown) => {
        if (active) setLoadError(loadFailure(reason));
      });
    return () => {
      active = false;
    };
  }, [load]);

  const rows = useMemo<Row[]>(() => {
    if (!overrides) return [];
    const keys = Object.keys(defaults);
    // Overrides whose key has left the catalog are shown last: the loader skips them, so
    // they are invisible everywhere else and would otherwise be impossible to clean up.
    const orphans = Object.keys(overrides).filter((key) => !(key in defaults));
    return [...keys, ...orphans].map((key) => {
      const defaultValue = defaults[key];
      const override = overrides[key];
      const draft = drafts[key];
      const shown = draft ?? override?.value ?? "";
      const dirty = draft !== undefined && draft !== (override?.value ?? "");
      return {
        key,
        defaultValue,
        reference: referenceDefaults[key],
        override,
        shown,
        dirty,
        pendingRestore: dirty && draft.trim() === "" && Boolean(override),
        problem:
          dirty && draft.trim() !== "" && defaultValue !== undefined
            ? overrideProblem(draft, defaultValue)
            : undefined,
        orphan: defaultValue === undefined,
      };
    });
  }, [overrides, defaults, referenceDefaults, drafts]);

  const counts = useMemo(
    () => ({
      overridden: rows.filter((row) => row.override).length,
      dirty: rows.filter((row) => row.dirty).length,
      parameters: rows.filter((row) => messageParameters(row.defaultValue ?? "").length > 0).length,
      orphans: rows.filter((row) => row.orphan).length,
    }),
    [rows],
  );

  const filtered = useMemo(() => {
    const needle = query.trim().toLocaleLowerCase();
    return rows.filter((row) => {
      if (filter === "overridden" && !row.override) return false;
      if (filter === "dirty" && !row.dirty) return false;
      if (filter === "parameters" && messageParameters(row.defaultValue ?? "").length === 0) {
        return false;
      }
      if (filter === "orphans" && !row.orphan) return false;
      if (!needle) return true;
      return [row.key, row.defaultValue, row.reference, row.override?.value, drafts[row.key]]
        .filter((value): value is string => typeof value === "string")
        .some((value) => value.toLocaleLowerCase().includes(needle));
    });
  }, [rows, filter, query, drafts]);

  const pages = Math.max(1, Math.ceil(filtered.length / PAGE_SIZE));
  const current = Math.min(page, pages);
  const visible = filtered.slice((current - 1) * PAGE_SIZE, current * PAGE_SIZE);
  const dirtyRows = rows.filter((row) => row.dirty);
  const problems = dirtyRows.filter((row) => row.problem).length;

  function navigate(next: { ns?: string; locale?: string; ref?: string }) {
    if (
      dirtyRows.length > 0 &&
      !window.confirm(t("saveBar.leaveConfirm", { count: dirtyRows.length }))
    ) {
      return;
    }
    const target = new URLSearchParams({
      ns: next.ns ?? namespace,
      locale: next.locale ?? locale,
      ref: next.ref ?? referenceLocale,
    });
    router.push(`/admin/ui-text?${target.toString()}`);
  }

  function edit(key: string, value: string) {
    setDrafts((previous) => ({ ...previous, [key]: value }));
    setNotice(undefined);
  }

  function discard(key: string) {
    setDrafts((previous) => {
      const next = { ...previous };
      delete next[key];
      return next;
    });
  }

  async function saveAll() {
    setBusy(true);
    setActionError(undefined);
    setNotice(undefined);
    const entries = dirtyRows.map((row) => ({
      key: row.key,
      value: row.shown.trim() === "" ? null : row.shown,
      // An orphan has no default left to validate against; the API skips the check when
      // the value is null, which is the only edit an orphan row allows.
      default_value: row.defaultValue ?? null,
    }));
    try {
      let latest: UiTextSnapshot | undefined;
      for (const batch of chunk(entries, UI_TEXT_BATCH_LIMIT)) {
        latest = await api<UiTextSnapshot>("/admin/ui-text/batch", {
          method: "POST",
          body: JSON.stringify({ locale, namespace, entries: batch }),
        });
      }
      if (latest) {
        setOverrides(Object.fromEntries(latest.entries.map((entry) => [entry.key, entry])));
      }
      setDrafts({});
      setNotice(t("saveBar.saved", { count: entries.length }));
      router.refresh();
    } catch (reason) {
      setActionError((reason as Error).message);
      // Reload rather than guess which chunk landed, and keep the unsaved text in the form.
      try {
        const refreshed = await load();
        setOverrides(refreshed);
        setDrafts((previous) =>
          Object.fromEntries(
            Object.entries(previous).filter(
              ([key, value]) => value !== (refreshed[key]?.value ?? ""),
            ),
          ),
        );
        setNotice(t("saveBar.partialFailure"));
      } catch {
        // The save error above is the one worth showing.
      }
    } finally {
      setBusy(false);
    }
  }

  if (loadError) {
    return (
      <div className="mt-8 rounded-2xl bg-red-50 p-5 text-red-800">
        <strong>{shared("loadErrorTitle")}</strong>
        <p className="mt-1 text-sm">
          {loadError.kind === "unreachable" ? shared("loadErrorUnreachable") : loadError.detail}
        </p>
        {loadError.kind === "permission" && (
          <p className="mt-2 text-xs">{shared("loadErrorHint")}</p>
        )}
        {loadError.kind !== "unreachable" && loadError.requestId && (
          <p className="mt-2 text-xs">{shared("loadErrorRequestId", { id: loadError.requestId })}</p>
        )}
        {loadError.kind !== "permission" && (
          <button
            type="button"
            onClick={() => {
              setLoadError(undefined);
              load().then(setOverrides).catch((reason: unknown) => setLoadError(loadFailure(reason)));
            }}
            className="mt-3 inline-flex items-center gap-1.5 rounded-lg border border-red-200 bg-white px-3 py-2 text-sm font-semibold"
          >
            <RefreshCw size={14} />
            {shared("loadErrorRetry")}
          </button>
        )}
      </div>
    );
  }

  if (!overrides) {
    return (
      <p className="mt-8 flex items-center gap-2 text-[var(--muted)]">
        <LoaderCircle className="animate-spin" size={18} />
        {t("loading")}
      </p>
    );
  }

  return (
    <div className="mt-8">
      <div className="sticky top-2 z-10 grid gap-3 rounded-2xl border border-[var(--line)] bg-white/95 p-4 backdrop-blur">
        <div className="grid gap-3 md:grid-cols-3">
          <label className="text-sm font-semibold">
            {t("namespaceLabel")}
            <select
              value={namespace}
              onChange={(event) => navigate({ ns: event.target.value })}
              className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal"
            >
              {namespaces.map((entry) => (
                <option key={entry.namespace} value={entry.namespace}>
                  {t("namespaceOption", {
                    label: t(`namespaces.${entry.namespace}`),
                    namespace: entry.namespace,
                    count: entry.keyCount,
                  })}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm font-semibold">
            {t("targetLocaleLabel")}
            <select
              value={locale}
              onChange={(event) => navigate({ locale: event.target.value })}
              className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal"
            >
              {Object.entries(localeLabels).map(([code, label]) => (
                <option key={code} value={code}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label className="text-sm font-semibold">
            {t("referenceLocaleLabel")}
            <select
              value={referenceLocale}
              onChange={(event) => navigate({ ref: event.target.value })}
              className="mt-1 h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal"
            >
              {Object.entries(localeLabels)
                .filter(([code]) => code !== locale)
                .map(([code, label]) => (
                  <option key={code} value={code}>
                    {label}
                  </option>
                ))}
            </select>
          </label>
        </div>
        <label className="text-sm font-semibold">
          <span className="sr-only">{t("searchLabel")}</span>
          <input
            type="search"
            aria-label={t("searchLabel")}
            value={query}
            placeholder={t("searchPlaceholder")}
            onChange={(event) => {
              setQuery(event.target.value);
              setPage(1);
            }}
            className="h-11 w-full rounded-xl border border-[var(--line)] px-3 font-normal"
          />
        </label>
        <FilterPills
          label={t("filters.label")}
          allLabel={t("filters.all")}
          allCount={rows.length}
          value={filter}
          onChange={(code) => {
            setFilter(code);
            setPage(1);
          }}
          options={[
            { code: "overridden", label: t("filters.overridden"), count: counts.overridden },
            { code: "dirty", label: t("filters.dirty"), count: counts.dirty },
            { code: "parameters", label: t("filters.parameters"), count: counts.parameters },
            { code: "orphans", label: t("filters.orphans"), count: counts.orphans },
          ]}
        />
      </div>

      {notice && (
        <p
          role="status"
          className="mt-4 flex items-center gap-2 rounded-xl bg-emerald-50 p-4 text-sm text-emerald-800"
        >
          <Check size={17} />
          {notice}
        </p>
      )}
      {actionError && (
        <p role="alert" className="mt-4 rounded-xl bg-red-50 p-4 text-sm text-red-800">
          {actionError}
        </p>
      )}

      {!filtered.length && <p className="mt-6 text-[var(--muted)]">{t("empty")}</p>}

      <div className="mt-4 grid gap-3">
        {visible.map((row) => {
          const parameters = messageParameters(row.defaultValue ?? "");
          const advanced = hasAdvancedIcu(row.defaultValue ?? "");
          const defaultId = `ui-text-${row.key}-default`;
          const errorId = `ui-text-${row.key}-error`;
          return (
            <article
              key={row.key}
              className="grid gap-3 rounded-2xl border border-[var(--line)] bg-white p-4 md:grid-cols-[minmax(0,2fr)_minmax(0,3fr)]"
            >
              <div className="min-w-0">
                <code className="block break-all font-mono text-xs text-[var(--ink)]">
                  {row.key}
                </code>
                <div className="mt-1.5 flex flex-wrap gap-1.5 text-xs">
                  {row.override && (
                    <span className="rounded-full bg-[var(--teal-soft)] px-2 py-0.5 font-semibold text-[var(--teal-dark)]">
                      {t("row.overridden")}
                    </span>
                  )}
                  {row.dirty && (
                    <span className="rounded-full bg-amber-100 px-2 py-0.5 font-semibold text-amber-900">
                      {row.pendingRestore ? t("row.pendingRestore") : t("row.dirty")}
                    </span>
                  )}
                  {row.orphan && (
                    <span className="rounded-full bg-red-100 px-2 py-0.5 font-semibold text-red-800">
                      {t("row.orphan")}
                    </span>
                  )}
                  {advanced && (
                    <span
                      title={t("row.advancedIcuHelp")}
                      className="rounded-full bg-[var(--paper)] px-2 py-0.5 font-semibold text-[var(--muted)]"
                    >
                      {t("row.advancedIcu")}
                    </span>
                  )}
                </div>
                {row.orphan ? (
                  <p className="mt-2 text-xs leading-5 text-red-800">{t("row.orphanHelp")}</p>
                ) : (
                  <p
                    id={defaultId}
                    className="mt-2 whitespace-pre-line text-sm leading-6 text-[var(--muted)]"
                  >
                    <span className="mr-1 font-semibold">{t("row.defaultLabel")}</span>
                    {row.defaultValue}
                  </p>
                )}
                {row.reference !== undefined && (
                  <p className="mt-1 whitespace-pre-line text-xs leading-5 text-[var(--muted)]">
                    <span className="mr-1 font-semibold">
                      {t("row.referenceLabel", { locale: localeLabels[referenceLocale] })}
                    </span>
                    {row.reference}
                  </p>
                )}
                {parameters.length > 0 && (
                  <p className="mt-1.5 flex flex-wrap items-center gap-1 text-xs text-[var(--muted)]">
                    <span className="font-semibold">{t("row.parametersLabel")}</span>
                    {parameters.map((name) => (
                      <code key={name} className="rounded bg-[var(--paper)] px-1 font-mono">
                        {"{"}
                        {name}
                        {"}"}
                      </code>
                    ))}
                  </p>
                )}
                {row.override && (
                  <p className="mt-1.5 text-xs text-[var(--muted)]">
                    {row.override.updated_by_email
                      ? t("row.updatedBy", {
                          email: row.override.updated_by_email,
                          time: dateTime.format(new Date(row.override.updated_at)),
                        })
                      : t("row.updatedAt", {
                          time: dateTime.format(new Date(row.override.updated_at)),
                        })}
                  </p>
                )}
              </div>
              <div className="min-w-0">
                <textarea
                  rows={2}
                  maxLength={UI_TEXT_MAX_LENGTH}
                  value={row.shown}
                  readOnly={row.orphan}
                  placeholder={row.defaultValue}
                  aria-label={row.key}
                  aria-invalid={row.problem ? true : undefined}
                  aria-describedby={
                    [row.orphan ? undefined : defaultId, row.problem ? errorId : undefined]
                      .filter(Boolean)
                      .join(" ") || undefined
                  }
                  onChange={(event) => edit(row.key, event.target.value)}
                  className="field-sizing-content min-h-[3.25rem] w-full resize-y rounded-xl border border-[var(--line)] p-3 text-sm read-only:bg-[var(--paper)]"
                />
                {row.problem && (
                  <p id={errorId} role="alert" className="mt-1 text-xs text-red-700">
                    {row.problem === "braces"
                      ? t("row.errorBraces")
                      : parameters.length === 0
                        ? t("row.errorNoParameters")
                        : t("row.errorParameters", { expected: parameters.join("、") })}
                  </p>
                )}
                <div className="mt-2 flex justify-end">
                  {row.dirty ? (
                    <button
                      type="button"
                      aria-label={t("row.discardNamed", { key: row.key })}
                      onClick={() => discard(row.key)}
                      className="rounded-lg border border-[var(--line)] px-3 py-1.5 text-xs font-semibold"
                    >
                      {t("row.discard")}
                    </button>
                  ) : (
                    row.override && (
                      <button
                        type="button"
                        aria-label={t("row.restoreNamed", { key: row.key })}
                        onClick={() => edit(row.key, "")}
                        className="rounded-lg border border-[var(--line)] px-3 py-1.5 text-xs font-semibold"
                      >
                        {t("row.restore")}
                      </button>
                    )
                  )}
                </div>
              </div>
            </article>
          );
        })}
      </div>

      {pages > 1 && (
        <div className="mt-5 flex items-center justify-between gap-3">
          <button
            type="button"
            aria-label={t("pager.previous")}
            disabled={current <= 1}
            onClick={() => setPage(current - 1)}
            className="rounded-lg border border-[var(--line)] px-3 py-2 text-sm font-semibold disabled:opacity-40"
          >
            {t("pager.previous")}
          </button>
          <p className="text-sm text-[var(--muted)]">
            {t("pager.summary", { page: current, pages, total: filtered.length })}
          </p>
          <button
            type="button"
            aria-label={t("pager.next")}
            disabled={current >= pages}
            onClick={() => setPage(current + 1)}
            className="rounded-lg border border-[var(--line)] px-3 py-2 text-sm font-semibold disabled:opacity-40"
          >
            {t("pager.next")}
          </button>
        </div>
      )}

      {dirtyRows.length > 0 && (
        <div className="sticky bottom-2 z-10 mt-5 flex flex-wrap items-center justify-between gap-3 rounded-2xl border border-[var(--line)] bg-white/95 p-4 shadow-lg backdrop-blur">
          <p className="text-sm font-semibold">
            {t("saveBar.pending", { count: dirtyRows.length })}
          </p>
          <div className="flex items-center gap-2">
            <button
              type="button"
              onClick={() => {
                if (window.confirm(t("saveBar.discardAllConfirm", { count: dirtyRows.length }))) {
                  setDrafts({});
                }
              }}
              className="rounded-xl border border-[var(--line)] px-3 py-2 text-sm font-semibold"
            >
              {t("saveBar.discardAll")}
            </button>
            <button
              type="button"
              disabled={busy || problems > 0}
              onClick={saveAll}
              className="inline-flex items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-2 text-sm font-semibold text-white disabled:opacity-50"
            >
              {busy && <LoaderCircle className="animate-spin" size={16} />}
              {busy
                ? t("saveBar.saving")
                : problems > 0
                  ? t("saveBar.fixErrors", { count: problems })
                  : t("saveBar.save", { count: dirtyRows.length })}
            </button>
          </div>
        </div>
      )}
    </div>
  );
}
