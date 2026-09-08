"use client";

import { BarChart3, ChevronDown, ClipboardCheck, Database, Hotel, KeyRound, Languages, LayoutDashboard, Menu, Rocket, Search, Settings2, Soup, UsersRound, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { MokaairLogo } from "@/components/mokaair-logo";
import { Link, usePathname } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";

const items = [
  { key: "dashboard", href: "/admin", icon: LayoutDashboard, group: "primary" },
  { key: "hotspots", href: "/admin/hotspots", icon: Database, group: "primary" },
  { key: "foods", href: "/admin/foods", icon: Soup, group: "primary" },
  { key: "hotels", href: "/admin/hotels", icon: Hotel, group: "primary" },
  { key: "analytics", href: "/admin/analytics", icon: BarChart3, group: "operations" },
  { key: "users", href: "/admin/users", icon: UsersRound, group: "operations" },
  { key: "community", href: "/admin/community", icon: UsersRound, group: "operations" },
  { key: "pets", href: "/admin/pet-friendly", icon: ClipboardCheck, group: "operations" },
  { key: "catalogReview", href: "/admin/catalog-review", icon: ClipboardCheck, group: "operations" },
  { key: "travelServices", href: "/admin/travel-services", icon: ClipboardCheck, group: "operations" },
  { key: "partners", href: "/admin/partners", icon: UsersRound, group: "operations" },
  { key: "usage", href: "/admin/usage-settings", icon: BarChart3, group: "operations" },
  { key: "layout", href: "/admin/layout-settings", icon: Settings2, group: "system" },
  { key: "uiText", href: "/admin/ui-text", icon: Languages, group: "system" },
  { key: "system", href: "/admin/system-settings", icon: Settings2, group: "system" },
  { key: "providers", href: "/admin/settings", icon: KeyRound, group: "system" },
  { key: "deployments", href: "/admin/deployments", icon: Rocket, group: "system", deploy: true },
] as const;

export function AdminNav({ current }: { current?: string } = {}) {
  const t = useTranslations("admin.navigation");
  const tc = useTranslations("community");
  const copy = adminDomainsCopy(useLocale());
  const pathname = usePathname();
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [expanded, setExpanded] = useState<{ path: string; values: Record<string, boolean> }>({ path: "", values: {} });
  const [desktopNav, setDesktopNav] = useState(false);
  const sidebar = useRef<HTMLElement>(null);
  const opener = useRef<HTMLButtonElement>(null);
  const { user } = useHeaderSession();
  const canDeploy = Boolean(user?.can_deploy);
  const path = current ? items.find((item) => item.key === current)?.href ?? pathname : pathname;
  const names: Record<string, string> = { dashboard: copy.overview, hotspots: copy.hotspots, foods: copy.foods, hotels: copy.hotels, catalogReview: copy.history, travelServices: copy.otherServices, partners: copy.partners, community: tc("adminCommunity"), pets: tc("adminPets") };
  const label = (key: string) => names[key] ?? t(key);
  const links = items.filter((item) => !("deploy" in item) || canDeploy);
  const term = query.trim().toLocaleLowerCase();
  const visible = links.filter((item) => label(item.key).toLocaleLowerCase().includes(term));
  const activeFor = (href: string) => href === "/admin" ? path === href : path.startsWith(href);
  const features = [
    { label: copy.foods + " · " + copy.scans, href: "/admin/foods?tab=nearby&section=scans" },
    { label: copy.foods + " · " + copy.sources, href: "/admin/foods?tab=nearby&section=sources" },
    { label: copy.foods + " · " + copy.coordinates, href: "/admin/foods?tab=completion&section=coordinates" },
    { label: copy.hotspots + " · " + copy.places, href: "/admin/hotspots?tab=places" },
    { label: copy.hotspots + " · " + copy.intros, href: "/admin/hotspots?tab=content&section=intros" },
    { label: copy.hotspots + " · " + copy.ai, href: "/admin/hotspots?tab=review&section=ai" },
    { label: copy.foods + " · " + copy.ai, href: "/admin/foods?tab=review&section=ai" },
    { label: copy.hotelProviderMode, href: "/admin/hotels?tab=settings&section=providers&provider=runtime&field=hotel_provider_mode" },
    ...(["hotspots", "foods", "hotels"] as const).map((domain) => ({ label: copy[domain] + " · " + copy.settings, href: "/admin/" + domain + "?tab=settings" })),
  ].filter((feature) => term && feature.label.toLocaleLowerCase().includes(term));

  useEffect(() => {
    if (typeof window.matchMedia !== "function") return;
    const wide = window.matchMedia("(min-width: 1024px)");
    const update = () => setDesktopNav(wide.matches);
    update();
    wide.addEventListener?.("change", update);
    return () => wide.removeEventListener?.("change", update);
  }, []);
  useEffect(() => {
    if (!open || desktopNav) return;
    const previous = document.activeElement as HTMLElement | null;
    const focusable = () => Array.from(sidebar.current?.querySelectorAll<HTMLElement>("a[href], button, input, select, [tabindex='0']") ?? []).filter((element) => !element.closest("[hidden]") && !element.hasAttribute("disabled"));
    sidebar.current?.querySelector<HTMLInputElement>("input")?.focus();
    const onKeyDown = (event: KeyboardEvent) => {
      if (event.key === "Escape") { event.preventDefault(); setOpen(false); }
      if (event.key === "Tab") {
        const elements = focusable();
        const first = elements[0], last = elements[elements.length - 1];
        if (event.shiftKey && (document.activeElement === first || !sidebar.current?.contains(document.activeElement))) { event.preventDefault(); last?.focus(); }
        else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
      }
    };
    document.addEventListener("keydown", onKeyDown);
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => {
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
      if (previous?.isConnected) previous.focus();
    };
  }, [open, desktopNav]);

  const renderLink = (item: typeof links[number]) => {
    const Icon = item.icon;
    const active = activeFor(item.href);
    return <Link key={item.href} href={item.href} onClick={() => setOpen(false)} aria-current={active ? "page" : undefined}
      className={`flex min-h-11 items-center gap-3 rounded-xl px-3 text-sm font-semibold transition motion-reduce:transition-none focus-visible:outline-2 focus-visible:outline-[var(--teal)] ${active ? "bg-[var(--teal-soft)] text-[var(--teal-dark)]" : "text-[var(--muted)] hover:bg-[var(--paper)] hover:text-[var(--ink)]"}`}>
      <Icon aria-hidden size={18} /><span>{label(item.key)}</span>
    </Link>;
  };
  return <>
    <button ref={opener} type="button" onClick={() => setOpen(true)} className="fixed bottom-[calc(1.25rem+env(safe-area-inset-bottom))] right-4 z-50 inline-flex min-h-12 items-center gap-2 rounded-2xl bg-[var(--teal)] px-4 font-semibold text-white shadow-lg lg:hidden" aria-expanded={open} aria-controls="admin-navigation">
      <Menu aria-hidden size={20} />{t("openMenu")}
    </button>
    {open && <button type="button" aria-label={t("closeMenu")} onClick={() => setOpen(false)} className="fixed inset-0 z-[70] bg-slate-950/45 lg:hidden" />}
    <aside ref={sidebar} id="admin-navigation" inert={desktopNav || open ? undefined : true} className={`admin-sidebar ${open ? "admin-sidebar-open" : ""}`}>
      <div className="flex items-center justify-between px-2 pb-4">
        <MokaairLogo className="text-xl" />
        <button type="button" aria-label={t("closeMenu")} onClick={() => setOpen(false)} className="grid h-11 w-11 place-items-center rounded-xl border border-[var(--line)] lg:hidden"><X aria-hidden size={19} /></button>
      </div>
      <label className="relative mb-4 block">
        <Search aria-hidden className="absolute left-3 top-1/2 -translate-y-1/2 text-[var(--muted)]" size={16} />
        <span className="sr-only">{t("searchPlaceholder")}</span>
        <input type="search" value={query} onChange={(event) => setQuery(event.target.value)} placeholder={t("searchPlaceholder")} className="h-11 w-full rounded-xl border border-[var(--line)] bg-[var(--paper)] pl-9 pr-3 text-sm focus-visible:outline-2 focus-visible:outline-[var(--teal)]" />
      </label>
      <nav aria-label={t("menuLabel")} className="grid gap-1.5">
        {visible.filter((item) => item.group === "primary").map(renderLink)}
        {(["operations", "system"] as const).map((group) => {
          const entries = visible.filter((item) => item.group === group);
          if (term && !entries.length) return null;
          const show = term ? true : (expanded.path === path && group in expanded.values ? expanded.values[group] : entries.some((item) => activeFor(item.href)));
          return <div key={group} className="mt-3 border-t border-[var(--line)] pt-2">
            <button type="button" aria-expanded={show} aria-controls={"admin-group-" + group} onClick={() => setExpanded({ path, values: { ...(expanded.path === path ? expanded.values : {}), [group]: !show } })} className="flex min-h-11 w-full items-center justify-between rounded-xl px-3 text-sm font-semibold text-[var(--muted)] hover:bg-[var(--paper)]">
              {copy[group]}<ChevronDown aria-hidden size={16} className={show ? "rotate-180" : ""} />
            </button>
            <div id={"admin-group-" + group} hidden={!show} className="grid gap-1">{entries.map(renderLink)}</div>
          </div>;
        })}
        {features.map((feature) => <Link key={feature.href} href={feature.href} onClick={() => setOpen(false)} className="flex min-h-11 items-center gap-3 rounded-xl bg-[var(--paper)] px-3 py-2 text-sm"><Search aria-hidden size={16} /><span>{feature.label}</span></Link>)}
        {!visible.length && !features.length && <p className="rounded-xl bg-[var(--paper)] p-3 text-center text-xs text-[var(--muted)]">{t("noMatches")}</p>}
      </nav>
    </aside>
  </>;
}
