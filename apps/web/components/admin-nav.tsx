"use client";

import {
  BarChart3,
  Database,
  KeyRound,
  LayoutDashboard,
  Menu,
  Rocket,
  Search,
  Settings2,
  Soup,
  UsersRound,
  X,
} from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useState } from "react";
import { Link, usePathname } from "@/i18n/navigation";
import { api } from "@/lib/api";

const items = [
  { key: "dashboard", href: "/admin", icon: LayoutDashboard },
  { key: "users", href: "/admin/users", icon: UsersRound },
  { key: "hotspots", href: "/admin/hotspots", icon: Database },
  { key: "foods", href: "/admin/foods", icon: Soup },
  { key: "usage", href: "/admin/usage-settings", icon: BarChart3 },
  { key: "layout", href: "/admin/layout-settings", icon: Settings2 },
  { key: "system", href: "/admin/system-settings", icon: Settings2 },
  { key: "providers", href: "/admin/settings", icon: KeyRound },
  {
    key: "deployments",
    href: "/admin/deployments",
    icon: Rocket,
    deploy: true,
  },
] as const;

export function AdminNav({ current }: { current?: string } = {}) {
  const t = useTranslations("admin.navigation");
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [canDeploy, setCanDeploy] = useState(false);
  const [query, setQuery] = useState("");
  useEffect(() => {
    api<{ can_deploy?: boolean }>("/auth/me")
      .then((user) => setCanDeploy(Boolean(user.can_deploy)))
      .catch(() => undefined);
  }, []);
  const links = items.filter((item) => !("deploy" in item) || canDeploy);
  const visibleLinks = links.filter((item) =>
    t(item.key).toLocaleLowerCase().includes(query.trim().toLocaleLowerCase()),
  );
  const legacyCurrentHref: Record<string, string> = {
    dashboard: "/admin",
    users: "/admin/users",
    hotspots: "/admin/hotspots",
    foods: "/admin/foods",
    usage: "/admin/usage-settings",
    layout: "/admin/layout-settings",
    system: "/admin/system-settings",
    providers: "/admin/settings",
    deployments: "/admin/deployments",
  };
  const activeFor = (href: string) =>
    current
      ? legacyCurrentHref[current] === href
      : href === "/admin"
        ? pathname === href
        : pathname.startsWith(href);
  const content = (
    <>
      <div className="flex items-center justify-between px-2 pb-4">
        <div>
          <p className="text-[11px] font-bold uppercase tracking-[.16em] text-[var(--teal)]">
            Control center
          </p>
          <strong className="text-lg">Travel Scanner</strong>
        </div>
        <button
          type="button"
          aria-label="Close admin menu"
          onClick={() => setOpen(false)}
          className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] lg:hidden"
        >
          <X size={19} />
        </button>
      </div>
      <label className="relative mb-4 block"><Search aria-hidden className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--muted)]" size={16} /><span className="sr-only">搜尋後台功能</span><input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜尋後台功能" className="h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-9 pr-3 text-sm outline-none transition focus:border-[var(--teal)]" /></label>
      <nav aria-label="管理後台功能" className="grid gap-1.5">
        {visibleLinks.map((item) => {
          const Icon = item.icon;
          const active = activeFor(item.href);
          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={() => setOpen(false)}
              aria-current={active ? "page" : undefined}
              className={`flex min-h-11 items-center gap-3 rounded-xl px-3 text-sm font-semibold transition ${active ? "bg-[var(--ink)] text-white shadow-sm" : "text-[var(--muted)] hover:bg-[var(--teal-soft)] hover:text-[var(--teal-dark)]"}`}
            >
              <Icon size={18} />
              <span>{t(item.key)}</span>
            </Link>
          );
        })}
        {!visibleLinks.length && <p className="rounded-xl bg-[var(--paper)] p-3 text-center text-xs text-[var(--muted)]">沒有符合的後台功能</p>}
      </nav>
    </>
  );
  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="fixed bottom-[calc(5.6rem+env(safe-area-inset-bottom))] right-4 z-50 grid h-12 w-12 place-items-center rounded-2xl bg-[var(--ink)] text-white shadow-lg lg:hidden"
        aria-label="Open admin menu"
      >
        <Menu />
      </button>
      {open && (
        <button
          type="button"
          aria-label="Close admin menu"
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-[70] bg-slate-950/45 lg:hidden"
        />
      )}
      <aside className={`admin-sidebar ${open ? "admin-sidebar-open" : ""}`}>
        {content}
      </aside>
    </>
  );
}
