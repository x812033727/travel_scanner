"use client";

import { useLocale } from "next-intl";
import { useEffect, useState } from "react";
import { AdminEmptyState, AdminErrorState, AdminFilterBar, AdminSkeleton, AdminStatusPill } from "@/components/admin-ui";
import { Button } from "@/components/community/ui";
import { updateAdminQuery, useAdminQueryValue } from "@/lib/admin-workspace-navigation";
import { api } from "@/lib/api";
import { videoPlansCopy, videoPlansText } from "@/lib/video-plans-copy";

const CATALOGS = ["season1", "season2", "season3", "brand-stories", "ai-terms"] as const;
type Catalog = (typeof CATALOGS)[number];
type Copy = ReturnType<typeof videoPlansCopy>;
export type VideoPlan = {
  catalog: Catalog;
  id: string;
  video_slug: string;
  title: string;
  stage: keyof Copy["stages"];
  source_status: string;
  target_duration_seconds: number;
  min_duration_seconds: number;
  source_path: string;
  source_sha256: string;
  source_record_sha256: string;
  source_package_path: string | null;
  source_package_sha256: string | null;
  details: { label: keyof Copy["detailLabels"]; text: string }[];
};
export type VideoPlanPage = {
  items: VideoPlan[];
  total: number;
  page: number;
  page_size: number;
  catalogs: { catalog: Catalog; count: number }[];
  catalog_total: number;
  plans_sha256: string;
};
const isCatalog = (value: string) => (CATALOGS as readonly string[]).includes(value);
const isPage = (value: string) => /^[1-9]\d{0,5}$/.test(value);
const isQuery = (value: string) => value.length <= 200;
const PAGE_SIZE = 25;

function PlanSearch({ query, copy }: { query: string; copy: Copy }) {
  const [text, setText] = useState(query);
  return <form onSubmit={(event) => { event.preventDefault(); updateAdminQuery({ plan_q: text.trim(), plan_page: "" }); }} className="flex min-w-0 flex-1 flex-wrap items-end gap-2">
    <label className="grid min-w-0 flex-1 gap-1 text-sm font-semibold">{copy.search}
      <input type="search" maxLength={200} value={text} onChange={(event) => setText(event.target.value)} className="min-h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 font-normal" />
    </label>
    <Button secondary type="submit">{copy.searchButton}</Button>
  </form>;
}

function Plan({ plan, copy }: { plan: VideoPlan; copy: Copy }) {
  const status = copy.sourceStatuses[plan.source_status as keyof Copy["sourceStatuses"]] ?? plan.source_status;
  return <article className="min-w-0 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4 sm:p-5">
    <div className="flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]">
      <span>{copy.catalogs[plan.catalog]}</span><span className="font-mono">{plan.id}</span>
    </div>
    <h3 className="mt-2 break-words text-lg font-bold">{plan.title}</h3>
    <div className="mt-3 flex flex-wrap items-center gap-3">
      <span aria-label={copy.stage}><AdminStatusPill status={plan.stage === "COVERED_DO_NOT_REMAKE" ? "inactive" : "pending"}>{copy.stages[plan.stage]}</AdminStatusPill></span>
      {plan.stage !== "COVERED_DO_NOT_REMAKE" && <span className="text-sm font-semibold">{videoPlansText(copy.target, { minutes: plan.target_duration_seconds / 60 })}</span>}
    </div>
    <details className="mt-4 text-sm">
      <summary className="min-h-11 cursor-pointer content-center font-bold text-[var(--teal)]">{copy.details}</summary>
      <div className="grid min-w-0 gap-5 pt-3">
        <p className="text-[var(--muted)]">{videoPlansText(copy.sourceStatus, { status })}</p>
        {plan.details.map((detail, index) => <section key={`${detail.label}-${index}`}>
          <h4 className="mb-2 font-bold">{copy.detailLabels[detail.label]}</h4>
          <div className="whitespace-pre-wrap break-words leading-7 [overflow-wrap:anywhere]">{detail.text}</div>
        </section>)}
        <div className="rounded-xl bg-[var(--paper)] p-3 text-xs text-[var(--muted)]">
          <p>{copy.historical}</p>
          <p className="mt-2 font-bold">{copy.source}</p>
          <p className="break-all font-mono">{plan.source_path}</p>
          {plan.source_package_path && <p className="break-all font-mono">{plan.source_package_path}</p>}
        </div>
      </div>
    </details>
  </article>;
}

/** A packaged text catalog. Reading it has no relationship to the production queue. */
export function AdminVideoPlans() {
  const copy = videoPlansCopy(useLocale());
  const [catalog] = useAdminQueryValue("plan_catalog", "", isCatalog);
  const [query] = useAdminQueryValue("plan_q", "", isQuery);
  const [pageValue] = useAdminQueryValue("plan_page", "1", isPage);
  const page = Number(pageValue);
  const [reload, setReload] = useState(0);
  const params = new URLSearchParams({ page: String(page), page_size: String(PAGE_SIZE) });
  if (catalog) params.set("catalog", catalog);
  if (query) params.set("q", query);
  const suffix = params.toString();
  const key = `${suffix}#${reload}`;
  const [loaded, setLoaded] = useState<{ key: string; data?: VideoPlanPage; error?: boolean }>();
  const data = loaded?.key === key ? loaded.data : undefined;
  const error = loaded?.key === key && loaded.error;

  useEffect(() => {
    const controller = new AbortController();
    api<VideoPlanPage>(`/admin/video-plans?${suffix}`, { signal: controller.signal }).then((value) => {
      if (controller.signal.aborted) return;
      if (!value || !Array.isArray(value.items) || !Array.isArray(value.catalogs) || !Number.isInteger(value.total)) throw new TypeError("Invalid planning catalog");
      const pages = Math.max(1, Math.ceil(value.total / PAGE_SIZE));
      if (page > pages) updateAdminQuery({ plan_page: pages === 1 ? "" : String(pages) });
      else setLoaded({ key, data: value });
    }).catch(() => {
      if (!controller.signal.aborted) setLoaded({ key, error: true });
    });
    return () => controller.abort();
  }, [key, suffix, page]);

  const changeCatalog = (value: string) => updateAdminQuery({ plan_catalog: value, plan_page: "" });
  const pages = data ? Math.max(1, Math.ceil(data.total / PAGE_SIZE)) : 1;
  return <section aria-label={copy.title} className="grid min-w-0 gap-4">
    <header>
      <h2 className="text-xl font-black">{copy.title}</h2>
      <p className="mt-2 max-w-3xl text-sm leading-7 text-[var(--muted)]">{copy.description}</p>
      {data && <p className="mt-3 font-bold">{videoPlansText(copy.total, { count: data.catalog_total })}</p>}
      <p className="mt-2 text-sm leading-6">{copy.minimum}</p>
      <p className="mt-1 text-sm text-[var(--muted)]">{copy.readOnly}</p>
    </header>
    <AdminFilterBar>
      <label className="grid min-w-0 gap-1 text-sm font-semibold">{copy.catalog}
        <select value={catalog} onChange={(event) => changeCatalog(event.target.value)} className="min-h-11 min-w-0 max-w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3">
          <option value="">{copy.all}{data ? ` (${data.catalog_total})` : ""}</option>
          {CATALOGS.map((value) => <option key={value} value={value}>{copy.catalogs[value]}{data ? ` (${data.catalogs.find((facet) => facet.catalog === value)?.count ?? 0})` : ""}</option>)}
        </select>
      </label>
      <PlanSearch key={query} query={query} copy={copy} />
      {(catalog || query) && <Button secondary onClick={() => updateAdminQuery({ plan_catalog: "", plan_q: "", plan_page: "" })}>{copy.clear}</Button>}
    </AdminFilterBar>
    {error ? <AdminErrorState title={copy.error} detail={copy.errorDetail} retry={() => setReload((value) => value + 1)} retryLabel={copy.retry} />
      : !data ? <AdminSkeleton label={copy.loading} />
        : <>
          <p role="status" className="text-sm text-[var(--muted)]">{videoPlansText(copy.results, { count: data.total })}</p>
          {data.items.length ? <div className="grid min-w-0 gap-3">{data.items.map((plan) => <Plan key={`${plan.catalog}/${plan.id}`} plan={plan} copy={copy} />)}</div>
            : <AdminEmptyState title={copy.empty} detail={copy.emptyDetail} />}
          {pages > 1 && <nav aria-label={copy.pageLabel} className="flex flex-wrap items-center justify-between gap-3">
            <Button secondary disabled={page <= 1} onClick={() => updateAdminQuery({ plan_page: page - 1 === 1 ? "" : String(page - 1) })}>{copy.previous}</Button>
            <span className="text-sm">{videoPlansText(copy.pagination, { page, pages })}</span>
            <Button secondary disabled={page >= pages} onClick={() => updateAdminQuery({ plan_page: String(page + 1) })}>{copy.next}</Button>
          </nav>}
        </>}
  </section>;
}
