"use client";

import {
  BarChart3, BookOpenCheck, BriefcaseBusiness, ChevronRight, ClipboardCheck,
  Database, Hotel, KeyRound, Languages, LayoutDashboard, Menu, Newspaper, PanelLeftClose,
  PanelLeftOpen, PawPrint, Rocket, Settings2, ShieldCheck, Soup, UsersRound, X,
} from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { useHeaderSession } from "@/components/header-session";
import { MokaairLogo } from "@/components/mokaair-logo";
import { Link, usePathname } from "@/i18n/navigation";
import { fallbackAdminNavigation, visibleAdminNavigation, type AdminBootstrap, type AdminNavigationItem } from "@/lib/admin-operations";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";

const icons: Record<string, typeof LayoutDashboard> = {
  dashboard: LayoutDashboard, guides: Newspaper, hotspots: Database, foods: Soup, hotels: Hotel,
  catalogReview: BookOpenCheck, travelServices: ClipboardCheck, community: UsersRound,
  pets: PawPrint, partners: BriefcaseBusiness, analytics: BarChart3, users: UsersRound,
  usage: BarChart3, audit: ShieldCheck, layout: Settings2, uiText: Languages,
  system: Settings2, providers: KeyRound, database: Database, deployments: Rocket,
};
const groups = ["overview", "content", "community", "operations", "system"] as const;

function permissiveFallback(canDeploy = false): AdminBootstrap {
  return {
    admin_roles: ["legacy_admin"], admin_capabilities: ["*"],
    navigation: fallbackAdminNavigation.filter((item) => item.key !== "deployments" || canDeploy),
    pending_counts: {}, system_status: {}, environment: "production",
    can_deploy: canDeploy, can_manage_database: true,
  };
}

function useDrawerFocus(open: boolean, container: React.RefObject<HTMLElement | null>, trigger: React.RefObject<HTMLElement | null>, close: () => void) {
  useEffect(() => {
    if (!open) return;
    const previous = document.activeElement as HTMLElement | null;
    const triggerNode = trigger.current;
    const root = container.current;
    root?.querySelector<HTMLElement>("input, button, a[href]")?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") { event.preventDefault(); close(); return; }
      if (event.key !== "Tab" || !root) return;
      const focusable = Array.from(root.querySelectorAll<HTMLElement>("a[href], button:not([disabled]), input:not([disabled])"));
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    };
    document.addEventListener("keydown", onKeyDown);
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = overflow;
      const target = triggerNode ?? previous;
      if (target?.isConnected) target.focus();
    };
  }, [close, container, open, trigger]);
}

export function AdminNav({ current }: { current?: string } = {}) {
  const locale = useLocale();
  const copy = adminOperationsCopy(locale);
  const sitePagesTitle = useTranslations("admin.sitePages")("title");
  // Destinations the inline copy table predates (guides) are named by the message catalog.
  const navigationCopy = useTranslations("admin.navigation");
  const pathname = usePathname();
  const operations = useAdminOperations();
  const { user } = useHeaderSession();
  const bootstrap = operations?.bootstrap ?? permissiveFallback(Boolean(user?.can_deploy));
  const links = useMemo(() => visibleAdminNavigation(bootstrap), [bootstrap]);
  const activePath = current ? links.find((item) => item.key === current)?.href ?? pathname : pathname;
  const [mobileOpen, setMobileOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [standaloneCollapsed, setStandaloneCollapsed] = useState(false);
  const collapsed = operations?.sidebarCollapsed ?? standaloneCollapsed;
  const setCollapsed = operations?.setSidebarCollapsed ?? setStandaloneCollapsed;
  const mobilePanel = useRef<HTMLElement>(null);
  const mobileTrigger = useRef<HTMLButtonElement>(null);
  const closeMobile = useCallback(() => setMobileOpen(false), []);
  useDrawerFocus(mobileOpen, mobilePanel, mobileTrigger, closeMobile);

  useEffect(() => {
    try { setCollapsed(window.localStorage.getItem("admin-sidebar-collapsed") === "1"); } catch { /* storage may be blocked */ }
    // This is an initial preference, not a subscription to setter identity.
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);
  function toggleCollapsed() {
    const next = !collapsed;
    setCollapsed(next);
    try { window.localStorage.setItem("admin-sidebar-collapsed", next ? "1" : "0"); } catch { /* storage may be blocked */ }
  }

  const label = (item: AdminNavigationItem) => item.key === "sitePages" ? sitePagesTitle
    : item.label || copy.nav[item.key] || (navigationCopy.has(item.key) ? navigationCopy(item.key) : item.key);
  const term = query.trim().toLocaleLowerCase(locale);
  const filtered = links.filter((item) => !term || label(item).toLocaleLowerCase(locale).includes(term));
  const activeFor = (href: string) => href === "/admin" ? activePath === href : activePath.startsWith(href);

  const content = (mobile: boolean) => <>
    <div className="admin-nav-brand">
      <Link href="/admin" onClick={closeMobile} aria-label={copy.console} className="flex min-h-11 min-w-0 items-center">
        {collapsed && !mobile ? <span className="admin-nav-monogram" aria-hidden>Μ</span> : <MokaairLogo className="text-lg" />}
      </Link>
      {mobile && <button type="button" aria-label={copy.closeMenu} onClick={closeMobile} className="admin-icon-button"><X aria-hidden size={20} /></button>}
    </div>
    {(!collapsed || mobile) && <label className="admin-nav-search"><span className="sr-only">{copy.command}</span><input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder={copy.commandHint} /></label>}
    <nav aria-label={copy.console} className="admin-nav-groups">
      {groups.map((group) => {
        const entries = filtered.filter((item) => item.group === group);
        if (!entries.length) return null;
        return <section key={group} aria-labelledby={`${mobile ? "mobile" : "desktop"}-admin-group-${group}`}>
          {(!collapsed || mobile) && <h2 id={`${mobile ? "mobile" : "desktop"}-admin-group-${group}`}>{copy.groups[group]}</h2>}
          <div className="grid gap-1">{entries.map((item) => {
            const Icon = icons[item.key] ?? ChevronRight;
            const active = activeFor(item.href);
            const badge = item.badge_count ?? bootstrap.pending_counts[item.badge_key ?? item.key];
            return <Link key={item.href} href={item.href} onClick={closeMobile} aria-current={active ? "page" : undefined} title={collapsed && !mobile ? label(item) : undefined} className={`admin-nav-link ${active ? "admin-nav-link-active" : ""}`}>
              <Icon aria-hidden size={18} />{(!collapsed || mobile) && <span className="min-w-0 flex-1 truncate">{label(item)}</span>}{(!collapsed || mobile) && typeof badge === "number" && badge > 0 && <span className="admin-nav-badge">{badge > 99 ? "99+" : badge}</span>}
            </Link>;
          })}</div>
        </section>;
      })}
      {!filtered.length && <p className="rounded-xl bg-[var(--paper)] p-3 text-center text-xs text-[var(--muted)]">{copy.noCommand}</p>}
    </nav>
    {!mobile && <button type="button" onClick={toggleCollapsed} className="admin-sidebar-collapse" aria-label={collapsed ? copy.expand : copy.collapse} title={collapsed ? copy.expand : copy.collapse}>{collapsed ? <PanelLeftOpen aria-hidden size={18} /> : <PanelLeftClose aria-hidden size={18} />}{!collapsed && <span>{copy.collapse}</span>}</button>}
  </>;

  return <>
    <button ref={mobileTrigger} type="button" onClick={() => setMobileOpen(true)} className="admin-mobile-menu" aria-label={copy.openMenu} aria-expanded={mobileOpen} aria-controls="admin-mobile-navigation"><Menu aria-hidden size={20} /><span>{copy.console}</span></button>
    {mobileOpen && <button type="button" aria-label={copy.closeMenu} onClick={closeMobile} className="admin-drawer-scrim" />}
    <aside className={`admin-desktop-sidebar ${collapsed ? "admin-desktop-sidebar-collapsed" : ""}`}>{content(false)}</aside>
    <aside ref={mobilePanel} id="admin-mobile-navigation" aria-hidden={!mobileOpen} inert={mobileOpen ? undefined : true} className={`admin-mobile-sidebar ${mobileOpen ? "admin-mobile-sidebar-open" : ""}`}>{content(true)}</aside>
  </>;
}
