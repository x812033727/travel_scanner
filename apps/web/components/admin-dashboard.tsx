"use client";

import { ArrowRight, Database, Hotel, LoaderCircle, Soup } from "lucide-react";
import { useEffect, useState } from "react";
import { useLocale } from "next-intl";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";

type Dashboard = { counts: Record<string, number>; can_deploy: boolean };
export function AdminDashboard() {
  const copy = adminDomainsCopy(useLocale());
  const [data, setData] = useState<Dashboard>();
  const [error, setError] = useState("");
  useEffect(() => {
    let cancelled = false;
    api<Dashboard>("/admin/dashboard").then((result) => { if (!cancelled) setData(result); }).catch((reason: Error) => { if (!cancelled) setError(reason.message); });
    return () => { cancelled = true; };
  }, []);
  if (error) return <p role="alert" className="rounded-2xl border border-[var(--line)] bg-[var(--coral-soft)] p-5 text-[var(--ink)]">{error}</p>;
  if (!data) return <p role="status" className="mt-6 flex items-center gap-2 text-[var(--muted)]"><LoaderCircle aria-hidden className="animate-spin motion-reduce:animate-none" size={18} />{copy.loading}</p>;
  const counts = data.counts ?? {};
  const groups = [
    { key: "hotspots", title: copy.hotspots, icon: Database, total: "hotspots_total", rows: [
      { key: "hotspots_pending", label: copy.hotspotsPending, href: "/admin/hotspots?tab=review&section=manual" },
      { key: "guides_pending", label: copy.guidesPending, href: "/admin/hotspots?tab=content&section=guides" },
      { key: "hotspots_missing_location", label: copy.missingLocation, href: "/admin/hotspots?tab=places&section=identity&missing_location=true" },
    ] },
    { key: "foods", title: copy.foods, icon: Soup, total: null, rows: [
      { key: "foods_pending", label: copy.foodsPending, href: "/admin/foods?tab=review&section=dishes" },
      { key: "merchants_pending", label: copy.merchantsPending, href: "/admin/foods?tab=review&section=merchants" },
      { key: "merchants_missing_area", label: copy.missingArea, href: "/admin/foods?tab=catalog&section=merchants&taxonomy=missing_area" },
      { key: "merchants_missing_category", label: copy.missingCategory, href: "/admin/foods?tab=catalog&section=merchants&taxonomy=missing_category" },
    ] },
    { key: "hotels", title: copy.hotels, icon: Hotel, total: "hotels_total", rows: [
      { key: "hotels_pending", label: copy.hotelsPending, href: "/admin/hotels?tab=review&section=products" },
      { key: "hotels_without_options", label: copy.missingBookingLinks, href: "/admin/hotels?tab=review&section=platforms&missing_options=true" },
    ] },
  ];
  return <div className="mt-7 grid items-start gap-4 xl:grid-cols-3">
    {groups.map((group) => {
      const Icon = group.icon;
      const count = (key: string) => counts[key] == null ? "—" : counts[key].toLocaleString();
      return <section key={group.key} aria-labelledby={"overview-" + group.key} className="min-w-0 rounded-3xl border border-[var(--line)] bg-[var(--surface)] p-5 shadow-[var(--shadow-sm)]">
        <div className="flex items-center gap-3"><span className="grid h-11 w-11 place-items-center rounded-2xl bg-[var(--teal-soft)] text-[var(--teal-dark)]"><Icon aria-hidden size={22} /></span><h2 id={"overview-" + group.key} className="text-xl font-bold">{group.title}</h2></div>
        <dl className="my-5 grid gap-2 border-b border-[var(--line)] pb-5">
          {group.total ? <div><dt className="text-sm text-[var(--muted)]">{copy.total}</dt><dd className="mt-1 text-3xl font-bold tabular-nums">{count(group.total)}</dd></div> : <>
            <div className="flex justify-between"><dt>{copy.merchants}</dt><dd className="font-bold tabular-nums">{count("merchants_total")}</dd></div>
            <div className="flex justify-between"><dt>{copy.dishes}</dt><dd className="font-bold tabular-nums">{count("foods_total")}</dd></div>
          </>}
        </dl>
        <h3 className="mb-3 text-sm font-semibold text-[var(--muted)]">{copy.actions}</h3>
        <div className="grid gap-2">{group.rows.map((row) => <Link key={row.key} href={row.href} className="flex min-h-12 items-center justify-between gap-3 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm hover:text-[var(--teal-dark)] focus-visible:outline-2 focus-visible:outline-[var(--teal)]"><span>{row.label}</span><span className="font-bold tabular-nums">{count(row.key)}</span></Link>)}</div>
        <Link href={"/admin/" + group.key} className="mt-5 flex min-h-11 items-center justify-between rounded-xl border border-[var(--line)] px-3 text-sm font-semibold">{copy.openWorkspace}<ArrowRight aria-hidden size={17} /></Link>
      </section>;
    })}
  </div>;
}
