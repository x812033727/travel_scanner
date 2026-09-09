"use client";

import { Activity, ArrowRight, CircleAlert, Clock3, Database, Hotel, LoaderCircle, Server, Soup, UsersRound } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useMemo, useState } from "react";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { AdminErrorState, AdminStatusPill } from "@/components/admin-ui";
import { Link } from "@/i18n/navigation";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import { visibleAdminNavigation } from "@/lib/admin-operations";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";
import { api } from "@/lib/api";

type Dashboard = { counts: Record<string, number>; can_deploy: boolean };

export function AdminDashboard() {
  const locale = useLocale();
  const copy = adminDomainsCopy(locale);
  const operationsCopy = adminOperationsCopy(locale);
  const operations = useAdminOperations();
  const [data, setData] = useState<Dashboard>();
  const [error, setError] = useState("");
  const [reload, setReload] = useState(0);
  useEffect(() => {
    let cancelled = false;
    api<Dashboard>("/admin/dashboard").then((result) => { if (!cancelled) { setData(result); setError(""); } }).catch((reason: Error) => { if (!cancelled) setError(reason.message); });
    return () => { cancelled = true; };
  }, [reload]);
  const pending = operations?.bootstrap.pending_counts ?? {};
  const counts = { ...data?.counts, ...pending };
  const services = operations?.bootstrap.system_status ?? {};
  const navigation = operations ? visibleAdminNavigation(operations.bootstrap) : [];
  const canVisit = (href: string) => !operations || navigation.some((item) => {
    const destination = href.split(/[?#]/, 1)[0];
    return item.href === "/admin" ? destination === "/admin" : destination === item.href || destination.startsWith(`${item.href}/`);
  });
  const number = useMemo(() => new Intl.NumberFormat(locale), [locale]);
  const count = (key: string) => counts[key] == null ? "—" : number.format(counts[key]);
  if (error && !data) return <AdminErrorState title={operationsCopy.dashboardLoadError} detail={error} retry={() => setReload((value) => value + 1)} retryLabel={operationsCopy.retry} />;
  if (!data) return <p role="status" className="mt-6 flex items-center gap-2 text-[var(--muted)]"><LoaderCircle aria-hidden className="animate-spin motion-reduce:animate-none" size={18} />{copy.loading}</p>;

  const summary = [
    { key: "users_total", aliases: ["total_users", "users"], label: operationsCopy.dashboardUsers, icon: UsersRound, href: "/admin/users" },
    { key: "pending_total", aliases: ["hotspots_pending"], label: operationsCopy.dashboardPending, icon: Clock3, href: "/admin/hotspots?tab=review&section=manual&status=pending" },
    { key: "jobs_active", aliases: ["community_jobs_pending", "jobs_pending"], label: operationsCopy.dashboardJobs, icon: Activity, href: "/admin/community" },
    { key: "alerts_total", aliases: ["providers_unhealthy", "providers_errors"], label: operationsCopy.dashboardIncidents, icon: CircleAlert, href: "/admin/settings" },
  ];
  const domains = [
    { key: "hotspots", title: copy.hotspots, icon: Database, total: "hotspots_total", href: "/admin/hotspots", queues: [
      { href: "/admin/hotspots?tab=review&section=manual&status=pending", count: "hotspots_pending", label: copy.hotspotsPending },
      { href: "/admin/hotspots?tab=content&section=guides&status=pending", count: "guides_pending", label: copy.guidesPending },
    ] },
    { key: "foods", title: copy.foods, icon: Soup, total: "foods_total", href: "/admin/foods", queues: [
      { href: "/admin/foods?tab=review&section=dishes&status=pending", count: "foods_pending", label: copy.foodsPending },
      { href: "/admin/foods?tab=review&section=merchants&status=pending", count: "merchants_pending", label: copy.merchantsPending },
    ] },
    { key: "hotels", title: copy.hotels, icon: Hotel, total: "hotels_total", href: "/admin/hotels", queues: [
      { href: "/admin/hotels?tab=review&section=products&status=pending", count: "hotels_pending", label: copy.hotelsPending },
    ] },
  ];
  const serviceHref = (key: string) => key === "database" || key === "backup" ? "/admin/database" : key === "deployment" ? "/admin/deployments" : "/admin/settings";
  const serviceCard = (key: string, service: (typeof services)[string]) => <><span className="min-w-0"><strong className="block truncate text-sm">{service.label || operationsCopy.services[key] || key}</strong>{service.detail && <span className="block truncate text-xs text-[var(--muted)]">{service.detail}</span>}</span><AdminStatusPill status={service.status}>{operationsCopy.serviceStatuses[service.status] || service.status}</AdminStatusPill></>;
  const visibleDomains = domains.filter((domain) => canVisit(domain.href));
  return <div className="mt-7 space-y-6">
    {summary.some((item) => canVisit(item.href)) && <section aria-label={operationsCopy.dashboardSummary} className="grid gap-3 sm:grid-cols-2 xl:grid-cols-4">{summary.filter((item) => canVisit(item.href)).map((item) => {
      const Icon = item.icon;
      const value = [item.key, ...item.aliases].map((key) => counts[key]).find((candidate) => candidate != null);
      return <Link key={item.key} href={item.href} className="group rounded-[1.35rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] transition hover:-translate-y-0.5 hover:shadow-[var(--shadow-md)] motion-reduce:transform-none motion-reduce:transition-none"><div className="flex items-center justify-between"><span className="grid size-10 place-items-center rounded-xl bg-[var(--teal-soft)] text-[var(--teal-dark)]"><Icon aria-hidden size={20} /></span><ArrowRight aria-hidden className="text-[var(--muted)] transition group-hover:translate-x-1 motion-reduce:transform-none" size={17} /></div><p className="mt-5 text-3xl font-black tabular-nums">{value == null ? "—" : number.format(value)}</p><p className="mt-1 text-sm font-semibold text-[var(--muted)]">{item.label}</p></Link>;
    })}</section>}
    {Object.keys(services).length > 0 && <section aria-labelledby="admin-system-health" className="rounded-[1.6rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)] md:p-6"><div className="flex items-center gap-3"><span className="grid size-10 place-items-center rounded-xl bg-[var(--paper)]"><Server aria-hidden size={20} /></span><div><h2 id="admin-system-health" className="font-black">{operationsCopy.dashboardHealth}</h2><p className="text-xs text-[var(--muted)]">{operationsCopy.dashboardHealthDetail}</p></div></div><div className="mt-5 grid gap-2 sm:grid-cols-2 xl:grid-cols-4">{Object.entries(services).map(([key, service]) => canVisit(serviceHref(key)) ? <Link key={key} href={serviceHref(key)} className="flex min-h-14 items-center justify-between gap-3 rounded-xl bg-[var(--paper)] px-3">{serviceCard(key, service)}</Link> : <div key={key} className="flex min-h-14 items-center justify-between gap-3 rounded-xl bg-[var(--paper)] px-3">{serviceCard(key, service)}</div>)}</div></section>}
    {visibleDomains.length > 0 && <section aria-label={operationsCopy.dashboardCatalogs} className="grid items-start gap-4 xl:grid-cols-3">{visibleDomains.map((domain) => { const Icon = domain.icon; return <article role="region" aria-label={domain.title} key={domain.key} className="rounded-[1.6rem] border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]"><div className="flex items-center gap-3"><span className="grid size-11 place-items-center rounded-2xl bg-[var(--teal-soft)] text-[var(--teal-dark)]"><Icon aria-hidden size={22} /></span><div><h2 className="text-xl font-black">{domain.title}</h2><p className="text-xs text-[var(--muted)]">{copy.total} · {count(domain.total)}</p></div></div><div className="mt-5 grid gap-2">{domain.queues.map((queue) => <Link key={queue.href} href={queue.href} className="flex min-h-12 items-center justify-between rounded-xl bg-[var(--paper)] px-3 text-sm"><span>{queue.label}</span><strong className="tabular-nums">{count(queue.count)}</strong></Link>)}</div><Link href={domain.href} className="mt-3 flex min-h-11 items-center justify-between rounded-xl border border-[var(--line)] px-3 text-sm font-bold">{copy.openWorkspace}<ArrowRight aria-hidden size={17} /></Link></article>; })}</section>}
  </div>;
}
