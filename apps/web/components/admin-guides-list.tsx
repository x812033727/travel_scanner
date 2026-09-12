"use client";

import { useEffect, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useAdminActionGuard } from "@/components/admin-action-guard";
import { FilterPills } from "@/components/admin-filter-pills";
import { AdminEmptyState, AdminErrorState, AdminFilterBar, AdminStatusPill } from "@/components/admin-ui";
import { Button, Dialog } from "@/components/community/ui";
import { adminNavigate, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api, ApiError } from "@/lib/api";
import { guideKinds, isGuideKind, type GuideTopic } from "@/lib/guides";
import {
  articleStatuses, isArticleStatus, isPageNumber,
  type ArticleList, type ArticleStatus, type ArticleSummary, type BatchVisibilityResult,
} from "@/lib/guides-admin";
import { sitePageLocales, type SitePageLocale } from "@/lib/site-pages";

const control = "min-h-11 w-full rounded-xl border border-[var(--control-border,var(--line))] bg-[var(--surface)] px-3 py-2 text-[var(--ink)]";
const PAGE_SIZE = 30;
const statusTone: Record<ArticleStatus, string> = { published: "active", draft: "pending", hidden: "disabled", expired: "warning" };
const localeTone = { published: "active", draft: "pending", none: "inactive" } as const;

export type VisibilityAction = "hide" | "unhide";

/** Writes several query keys in one history entry, so a filter change and its page reset are one step back. */
export function updateAdminQuery(changes: Record<string, string>) {
  const target = new URL(window.location.href);
  for (const [key, value] of Object.entries(changes)) {
    if (value) target.searchParams.set(key, value);
    else target.searchParams.delete(key);
  }
  adminNavigate(target);
}

/**
 * The gate every visibility change goes through, single or batch: the same reason and the
 * same explicit tick the publish and withdraw dialogs already require, because hiding takes
 * an article off the site with exactly the same weight as withdrawing it.
 */
export function GuideVisibilityDialog({ action, count, busy, error, onConfirm, onClose }: {
  action: VisibilityAction; count: number; busy: boolean; error: string;
  onConfirm: (reason: string) => void; onClose: () => void;
}) {
  const t = useTranslations("admin.guides");
  const [reason, setReason] = useState("");
  const [confirmed, setConfirmed] = useState(false);
  const confirmLabel = t(action === "hide" ? "confirmHide" : "confirmUnhide");
  return <Dialog title={confirmLabel} onClose={() => { if (!busy) onClose(); }}>
    <div className="space-y-5">
      <p className="leading-7">{t(action === "hide" ? "hideHelp" : "unhideHelp")}</p>
      {count > 1 && <p className="font-semibold">{t(action === "hide" ? "batchHide" : "batchUnhide", { count })}</p>}
      <label className="grid gap-2">{t("reason")}
        <input className={control} disabled={busy} value={reason} onChange={(event) => setReason(event.target.value)} />
      </label>
      <label className="flex min-h-11 items-start gap-3">
        <input type="checkbox" className="mt-1" disabled={busy} checked={confirmed} onChange={(event) => setConfirmed(event.target.checked)} />{t("confirmed")}
      </label>
      {error && <p role="alert">{error}</p>}
      <Button disabled={busy || !confirmed || !reason.trim()} onClick={() => onConfirm(reason.trim())}>{confirmLabel}</Button>
    </div>
  </Dialog>;
}

export function visibilityError(problem: unknown, t: (key: string) => string): string {
  if (problem instanceof ApiError && problem.code === "guide_version_conflict") return t("conflict");
  return problem instanceof Error ? problem.message : t("error");
}

function articleTitle(article: ArticleSummary, locale: SitePageLocale): string {
  const own = article.locales.find((row) => row.locale === locale)?.title;
  return own || article.locales.find((row) => row.title)?.title || article.slug;
}

export function AdminGuidesList({ onOpen, onCreate }: { onOpen: (id: string) => void; onCreate: () => void }) {
  const t = useTranslations("admin.guides");
  const interfaceLocale = useLocale();
  const manage = useAdminActionGuard("content.manage");
  const locale: SitePageLocale = sitePageLocales.includes(interfaceLocale as SitePageLocale) ? interfaceLocale as SitePageLocale : "zh-TW";
  const [status] = useAdminQueryValue("status", "", isArticleStatus);
  const [kind] = useAdminQueryValue("kind", "", isGuideKind);
  const [destination] = useAdminQueryValue("destination");
  const [topic] = useAdminQueryValue("topic");
  const [query] = useAdminQueryValue("q");
  const [pageValue] = useAdminQueryValue("page", "1", isPageNumber);
  const page = Number(pageValue);
  const [topics, setTopics] = useState<GuideTopic[]>([]);
  const [search, setSearch] = useState({ q: query, destination });
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");
  const [notice, setNotice] = useState("");
  const [gate, setGate] = useState<{ action: VisibilityAction; articles: ArticleSummary[] } | null>(null);
  const [reload, setReload] = useState(0);

  const params = new URLSearchParams({ locale, page: String(page), limit: String(PAGE_SIZE) });
  if (status) params.set("status", status);
  if (kind) params.set("kind", kind);
  if (destination) params.set("destination", destination);
  if (topic) params.set("topic", topic);
  if (query) params.set("q", query);
  const suffix = params.toString();
  const filtered = Boolean(status || kind || destination || topic || query);
  // The page and the selection are keyed by what they were loaded for: a filter change or a
  // reload shows the loading state and drops the ticks without an effect resetting either.
  const key = `${suffix}#${reload}`;
  const [loaded, setLoaded] = useState<{ key: string; data: ArticleList | null }>();
  const data = loaded?.key === key ? loaded.data : undefined;
  const [selection, setSelection] = useState<{ key: string; ids: Set<string> }>({ key: "", ids: new Set() });
  const selected = selection.key === key ? selection.ids : new Set<string>();
  const setSelected = (ids: Set<string>) => setSelection({ key, ids });

  useEffect(() => {
    const controller = new AbortController();
    Promise.all([
      api<ArticleList>(`/admin/guides?${suffix}`, { signal: controller.signal }),
      api<{ topics: GuideTopic[] }>(`/admin/guides/topics?locale=${encodeURIComponent(locale)}`, { signal: controller.signal }),
    ]).then(([list, vocabulary]) => {
      if (controller.signal.aborted) return;
      setLoaded({ key, data: list });
      setTopics(vocabulary.topics);
      // A batch action can empty the last page; fall back to the new last page.
      if (list.pages > 0 && page > list.pages) updateAdminQuery({ page: String(list.pages) });
    }).catch((problem: unknown) => {
      if (controller.signal.aborted) return;
      setLoaded({ key, data: null });
      setError(visibilityError(problem, t));
    });
    return () => controller.abort();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [suffix, reload]);

  const articles = data?.articles ?? [];
  const chosen = articles.filter((article) => selected.has(article.id));
  const counts = Object.fromEntries((data?.facets.status ?? []).map((item) => [item.code, item.count])) as Partial<Record<ArticleStatus, number>>;
  const allCount = data ? articleStatuses.reduce((sum, code) => sum + (counts[code] ?? 0), 0) : undefined;

  function toggle(id: string, on: boolean) {
    const next = new Set(selected);
    if (on) next.add(id); else next.delete(id);
    setSelected(next);
  }

  async function applyVisibility(reason: string) {
    if (!gate || !manage.allowed || busy) return;
    setBusy(true); setError("");
    try {
      if (gate.articles.length === 1) {
        const [article] = gate.articles;
        await api<ArticleSummary>(`/admin/guides/${article.id}/${gate.action}?locale=${encodeURIComponent(locale)}`, {
          method: "POST",
          body: JSON.stringify({ expected_version: article.version, confirmed: true, reason }),
        });
        setNotice(t(gate.action === "hide" ? "hideSuccess" : "unhideSuccess"));
      } else {
        const result = await api<BatchVisibilityResult>(`/admin/guides/batch?locale=${encodeURIComponent(locale)}`, {
          method: "POST",
          body: JSON.stringify({
            items: gate.articles.map((article) => ({ id: article.id, expected_version: article.version })),
            action: gate.action, confirmed: true, reason,
          }),
        });
        setNotice(t("batchDone", { updated: result.updated, skipped: result.skipped }));
      }
      setGate(null);
      setReload((value) => value + 1);
    } catch (problem) {
      setError(visibilityError(problem, t));
    } finally {
      setBusy(false);
    }
  }

  const headers = ["title", "kind", "destination", "languages", "status", "updated", "actions"] as const;

  return <section className="space-y-5">
    <FilterPills
      label={t("status")}
      allLabel={t("statusAll")}
      allCount={allCount}
      options={articleStatuses.map((code) => ({ code, label: t(`statuses.${code}`), count: counts[code] }))}
      value={status}
      onChange={(code) => updateAdminQuery({ status: code, page: "" })}
    />

    <AdminFilterBar>
      <label className="grid gap-2 text-sm font-semibold">{t("kind")}
        <select className={control} value={kind} onChange={(event) => updateAdminQuery({ kind: event.target.value, page: "" })}>
          <option value="">{t("allKinds")}</option>
          {guideKinds.map((value) => <option key={value} value={value}>{t(value)}</option>)}
        </select>
      </label>
      <label className="grid gap-2 text-sm font-semibold">{t("topics")}
        <select className={control} value={topic} onChange={(event) => updateAdminQuery({ topic: event.target.value, page: "" })}>
          <option value="">{t("allTopics")}</option>
          {topics.map((item) => <option key={item.slug} value={item.slug}>{item.label}</option>)}
        </select>
      </label>
      <form className="flex flex-wrap items-end gap-3" onSubmit={(event) => { event.preventDefault(); updateAdminQuery({ q: search.q.trim(), destination: search.destination.trim(), page: "" }); }}>
        <label className="grid gap-2 text-sm font-semibold">{t("destination")}
          <input className={control} value={search.destination} placeholder={t("allDestinations")} onChange={(event) => setSearch({ ...search, destination: event.target.value })} />
        </label>
        <label className="grid gap-2 text-sm font-semibold">{t("search")}
          <input type="search" className={control} value={search.q} placeholder={t("searchPlaceholder")} onChange={(event) => setSearch({ ...search, q: event.target.value })} />
        </label>
        <Button type="submit" secondary disabled={busy}>{t("search")}</Button>
      </form>
    </AdminFilterBar>

    {notice && <p role="status">{notice}</p>}
    {error && !gate && <AdminErrorState title={t("error")} detail={error} retry={() => { setError(""); setReload((value) => value + 1); }} retryLabel={t("reload")} />}
    {data === undefined && !error && <p role="status">{t("loading")}</p>}

    {data && data.total === 0 && !filtered && <AdminEmptyState title={t("noArticles")} action={<Button disabled={busy || !manage.allowed} onClick={onCreate}>{t("newArticle")}</Button>} />}
    {data && data.total === 0 && filtered && <p role="status">{t("noArticles")}</p>}

    {data && data.total > 0 && <>
      <div className="flex flex-wrap items-center gap-2">
        <span className="mr-auto text-sm text-[var(--muted)]">{t("selectionCount", { selected: selected.size, total: data.total })}</span>
        <Button secondary disabled={!manage.allowed || !chosen.length || busy} onClick={() => setGate({ action: "hide", articles: chosen })}>{t("batchHide", { count: chosen.length })}</Button>
        <Button secondary disabled={!manage.allowed || !chosen.length || busy} onClick={() => setGate({ action: "unhide", articles: chosen })}>{t("batchUnhide", { count: chosen.length })}</Button>
      </div>

      <div className="overflow-x-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)]">
        <table aria-label={t("articleList")} className="admin-responsive-table w-full min-w-[960px] text-left text-sm">
          <thead>
            <tr className="border-b border-[var(--line)] bg-[var(--paper)] text-xs text-[var(--muted)]">
              <th className="px-4 py-3 font-bold">
                <input type="checkbox" aria-label={t("selectAll")}
                  checked={articles.length > 0 && articles.every((article) => selected.has(article.id))}
                  onChange={(event) => setSelected(event.target.checked ? new Set(articles.map((article) => article.id)) : new Set())} />
              </th>
              {headers.map((header) => <th key={header} className="px-4 py-3 font-bold">{t(`table.${header}`)}</th>)}
            </tr>
          </thead>
          <tbody>
            {articles.map((article) => <tr key={article.id} className="border-t border-[var(--line)] align-top">
              <td data-label={t("selectAll")} className="px-4 py-3">
                <input type="checkbox" aria-label={t("selectArticle", { slug: article.slug })} checked={selected.has(article.id)} onChange={(event) => toggle(article.id, event.target.checked)} />
              </td>
              <td data-label={t("table.title")} className="px-4 py-3">
                <button type="button" className="text-left font-semibold underline-offset-2 hover:underline" onClick={() => onOpen(article.id)}>{articleTitle(article, locale)}</button>
                <span className="block text-xs text-[var(--muted)]">{article.slug}{article.featured ? ` · ${t("featured")}` : ""}</span>
              </td>
              <td data-label={t("table.kind")} className="px-4 py-3">{t(article.kind)}</td>
              <td data-label={t("table.destination")} className="px-4 py-3">{article.destination_label ?? t("noDestination")}</td>
              <td data-label={t("table.languages")} className="px-4 py-3">
                <ul className="flex flex-wrap gap-1">
                  {sitePageLocales.map((code) => {
                    const row = article.locales.find((entry) => entry.locale === code);
                    const state = row ? (row.published_version !== null ? "published" : "draft") : "none";
                    return <li key={code}><AdminStatusPill status={localeTone[state]}>{code} · {t(`localeBadge.${state}`)}</AdminStatusPill></li>;
                  })}
                </ul>
              </td>
              <td data-label={t("table.status")} className="px-4 py-3">
                <AdminStatusPill status={statusTone[article.status]}>{t(`statuses.${article.status}`)}</AdminStatusPill>
              </td>
              <td data-label={t("table.updated")} className="px-4 py-3">
                <time dateTime={article.updated_at}>{new Date(article.updated_at).toLocaleString(interfaceLocale)}</time>
              </td>
              <td data-label={t("table.actions")} className="px-4 py-3">
                <div className="flex flex-wrap gap-2">
                  <Button secondary disabled={busy} onClick={() => onOpen(article.id)}>{t("open")}</Button>
                  <Button secondary disabled={busy || !manage.allowed} onClick={() => setGate({ action: article.is_active ? "hide" : "unhide", articles: [article] })}>
                    {article.is_active ? t("hide") : t("unhide")}
                  </Button>
                </div>
              </td>
            </tr>)}
          </tbody>
        </table>
      </div>

      {data.pages > 1 && <nav className="flex flex-wrap items-center gap-3" aria-label={t("page", { page: data.page, pages: data.pages })}>
        <Button secondary disabled={busy || page <= 1} onClick={() => updateAdminQuery({ page: String(page - 1) })}>{t("previous")}</Button>
        <span className="text-sm">{t("page", { page: data.page, pages: data.pages })}</span>
        <Button secondary disabled={busy || page >= data.pages} onClick={() => updateAdminQuery({ page: String(page + 1) })}>{t("next")}</Button>
      </nav>}
    </>}

    {gate && <GuideVisibilityDialog action={gate.action} count={gate.articles.length} busy={busy} error={error}
      onConfirm={(reason) => void applyVisibility(reason)} onClose={() => { setGate(null); setError(""); }} />}
  </section>;
}
