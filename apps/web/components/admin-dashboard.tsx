"use client";

import { ArrowRight, Database, LoaderCircle, Soup, UsersRound } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";

type Dashboard = { counts: Record<string, number>; quick_actions: { id: string; href: string; count_key: string }[]; can_deploy: boolean };
const cards = [
  { key: "hotspots_public", label: "公開景點", icon: Database, color: "bg-emerald-50 text-emerald-800" },
  { key: "foods_public", label: "公開料理", icon: Soup, color: "bg-orange-50 text-orange-800" },
  { key: "users", label: "會員總數", icon: UsersRound, color: "bg-sky-50 text-sky-800" },
] as const;
const actionLabels: Record<string, string> = { review_hotspots: "審核景點候選", review_merchants: "審核美食店家", manage_users: "管理會員與次數" };

export function AdminDashboard() {
  const [data, setData] = useState<Dashboard>();
  const [error, setError] = useState("");
  useEffect(() => { api<Dashboard>("/admin/dashboard").then(setData).catch((reason: Error) => setError(reason.message)); }, []);
  if (error) return <p role="alert" className="rounded-2xl bg-red-50 p-5 text-red-800">{error}</p>;
  if (!data) return <p className="flex items-center gap-2 text-[var(--muted)]"><LoaderCircle className="animate-spin" size={18} />載入營運摘要…</p>;
  return <div className="mt-7 grid gap-6">
    <section className="grid gap-4 sm:grid-cols-3">{cards.map((card) => { const Icon = card.icon; return <article key={card.key} className="rounded-3xl border border-[var(--line)] bg-white p-5 shadow-[var(--shadow-sm)]"><span className={`grid h-11 w-11 place-items-center rounded-2xl ${card.color}`}><Icon size={20} /></span><p className="mt-5 text-sm text-[var(--muted)]">{card.label}</p><strong className="mt-1 block text-3xl">{data.counts[card.key] ?? 0}</strong></article>; })}</section>
    <section className="rounded-3xl border border-[var(--line)] bg-white p-5 md:p-6"><div className="flex items-center justify-between"><div><h2 className="text-xl font-bold">今天要處理</h2><p className="mt-1 text-sm text-[var(--muted)]">把待審項目集中成清楚的工作入口。</p></div><span className="rounded-full bg-[var(--coral-soft)] px-3 py-1 text-xs font-bold text-[#a84334]">{(data.counts.hotspots_pending ?? 0) + (data.counts.merchants_pending ?? 0)} 待審</span></div><div className="mt-5 grid gap-2">{data.quick_actions.map((action) => <Link key={action.id} href={action.href} className="flex min-h-14 items-center rounded-2xl bg-[var(--paper)] px-4 font-semibold transition hover:-translate-y-0.5 hover:shadow-sm"><span className="mr-auto">{actionLabels[action.id] ?? action.id}</span><span className="mr-3 rounded-full bg-white px-2.5 py-1 text-xs">{data.counts[action.count_key] ?? 0}</span><ArrowRight size={18} /></Link>)}</div></section>
  </div>;
}
