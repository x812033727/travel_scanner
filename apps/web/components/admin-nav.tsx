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
import { MokaairLogo } from "@/components/mokaair-logo";
import { Link, usePathname } from "@/i18n/navigation";
import { api } from "@/lib/api";

const items = [
  { key: "dashboard", href: "/admin", icon: LayoutDashboard },
  { key: "analytics", href: "/admin/analytics", icon: BarChart3 },
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
  const [desktopNav, setDesktopNav] = useState(false);

  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const wide = window.matchMedia("(min-width: 1024px)");
    const update = () => setDesktopNav(wide.matches);
    update();
    wide.addEventListener?.("change", update);
    return () => wide.removeEventListener?.("change", update);
  }, []);

  useEffect(() => {
    if (!open) return;
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    document.addEventListener("keydown", onKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
    };
  }, [open]);
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
    analytics: "/admin/analytics",
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
          <p className="text-xs font-bold uppercase tracking-[.16em] text-[var(--teal)]">
            Control center
          </p>
          <MokaairLogo className="text-xl" />
        </div>
        <button
          type="button"
          aria-label={t("closeMenu")}
          onClick={() => setOpen(false)}
          className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] lg:hidden"
        >
          <X size={19} />
        </button>
      </div>
      <label className="relative mb-4 block"><Search aria-hidden className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--muted)]" size={16} /><span className="sr-only">{t("searchPlaceholder")}</span><input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t("searchPlaceholder")} className="h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-9 pr-3 text-sm outline-none transition focus:border-[var(--teal)]" /></label>
      <nav aria-label={t("menuLabel")} className="grid gap-1.5">
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
        {!visibleLinks.length && <p className="rounded-xl bg-[var(--paper)] p-3 text-center text-xs text-[var(--muted)]">{t("noMatches")}</p>}
      </nav>
    </>
  );
  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        // The phone tab bar is hidden inside /admin, so the 5.6rem it used to
        // clear left this floating over the middle of the page with nothing
        // under it. It also carries its label now: a bare hamburger is the only
        // way into ten admin sections.
        className="fixed bottom-[calc(1.25rem+env(safe-area-inset-bottom))] right-4 z-50 inline-flex min-h-12 items-center gap-2 rounded-2xl bg-[var(--ink)] px-4 font-semibold text-white shadow-lg lg:hidden"
        aria-expanded={open}
      >
        <Menu aria-hidden size={20} />
        {t("openMenu")}
      </button>
      {open && (
        <button
          type="button"
          aria-label={t("closeMenu")}
          onClick={() => setOpen(false)}
          className="fixed inset-0 z-[70] bg-slate-950/45 lg:hidden"
        />
      )}
      <aside
        // The closed drawer is only translated off-canvas; without inert its
        // search box and ten links still sit in the Tab order, swallowing
        // keyboard focus into an invisible menu.
        inert={desktopNav || open ? undefined : true}
        className={`admin-sidebar ${open ? "admin-sidebar-open" : ""}`}
      >
        {content}
      </aside>
    </>
  );
}
