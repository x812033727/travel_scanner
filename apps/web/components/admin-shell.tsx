"use client";

import { ChevronDown, Command, HeartPulse, Search, UserRound, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useCallback, useEffect, useMemo, useRef, useState } from "react";
import { AdminNav } from "@/components/admin-nav";
import { LanguageSwitcher } from "@/components/language-switcher";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { useHeaderSession } from "@/components/header-session";
import { Link, usePathname } from "@/i18n/navigation";
import { visibleAdminNavigation } from "@/lib/admin-operations";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";

const deepLinks = [
  { key: "foodScans", parent: "/admin/foods", href: "/admin/foods?tab=nearby&section=scans", labels: { "zh-TW": "美食 · 餐廳掃描", "zh-CN": "美食 · 餐厅扫描", ja: "フード · 店舗スキャン", ko: "음식 · 매장 스캔", en: "Food · restaurant scans" } },
  { key: "foodSources", parent: "/admin/foods", href: "/admin/foods?tab=nearby&section=sources", labels: { "zh-TW": "美食 · 餐廳來源", "zh-CN": "美食 · 餐厅来源", ja: "フード · 店舗ソース", ko: "음식 · 매장 출처", en: "Food · restaurant sources" } },
  { key: "hotelProviders", parent: "/admin/hotels", href: "/admin/hotels?tab=settings&section=providers", labels: { "zh-TW": "飯店 · 供應商設定", "zh-CN": "酒店 · 供应商设置", ja: "ホテル · プロバイダー", ko: "호텔 · 공급자 설정", en: "Hotels · provider settings" } },
  { key: "hotspotReview", parent: "/admin/hotspots", href: "/admin/hotspots?tab=review&section=manual", labels: { "zh-TW": "景點 · 待審核", "zh-CN": "景点 · 待审核", ja: "スポット · 審査待ち", ko: "명소 · 검토 대기", en: "Hotspots · pending review" } },
] as const;

function safeRecent(value: string | null): string[] {
  try {
    const parsed: unknown = JSON.parse(value || "[]");
    return Array.isArray(parsed) ? parsed.filter((item): item is string => typeof item === "string" && item.startsWith("/admin")).slice(0, 5) : [];
  } catch { return []; }
}

export function AdminShell({ children }: { children: React.ReactNode }) {
  const locale = useLocale();
  const sitePages = useTranslations("admin.sitePages");
  const navigationCopy = useTranslations("admin.navigation");
  const copy = adminOperationsCopy(locale);
  const pathname = usePathname();
  const operations = useAdminOperations();
  if (!operations) throw new Error("AdminShell requires AdminOperationsProvider");
  const { bootstrap, commandOpen, setCommandOpen, sidebarCollapsed } = operations;
  const { user, logout } = useHeaderSession();
  const [accountOpen, setAccountOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [recent, setRecent] = useState<string[]>([]);
  const commandTrigger = useRef<HTMLButtonElement>(null);
  const commandDialog = useRef<HTMLDivElement>(null);
  const accountMenu = useRef<HTMLDivElement>(null);
  const navigation = useMemo(() => visibleAdminNavigation(bootstrap), [bootstrap]);
  const active = [...navigation].sort((a, b) => b.href.length - a.href.length).find((item) => item.href === "/admin" ? pathname === "/admin" : pathname.startsWith(item.href));
  const label = (key: string, supplied?: string) => key === "sitePages" ? sitePages("title")
    : supplied || copy.nav[key] || (navigationCopy.has(key) ? navigationCopy(key) : key);

  useEffect(() => {
    const timer = window.setTimeout(() => {
      try {
        const previous = safeRecent(window.localStorage.getItem("admin-recent-pages"));
        const href = active?.href;
        const next = href ? [href, ...previous.filter((item) => item !== href)].slice(0, 5) : previous;
        setRecent(next);
        window.localStorage.setItem("admin-recent-pages", JSON.stringify(next));
      } catch { /* storage may be blocked */ }
    }, 0);
    return () => window.clearTimeout(timer);
  }, [active?.href]);

  useEffect(() => {
    const onKeyDown = (event: KeyboardEvent) => {
      if ((event.metaKey || event.ctrlKey) && event.key.toLocaleLowerCase() === "k") { event.preventDefault(); setCommandOpen(true); }
    };
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, [setCommandOpen]);

  const closeCommand = useCallback(() => setCommandOpen(false), [setCommandOpen]);
  useEffect(() => {
    if (!commandOpen) return;
    const prior = document.activeElement as HTMLElement | null;
    const triggerNode = commandTrigger.current;
    const root = commandDialog.current;
    root?.querySelector<HTMLInputElement>("input")?.focus();
    const keydown = (event: KeyboardEvent) => {
      if (event.key === "Escape") { event.preventDefault(); closeCommand(); return; }
      if (event.key !== "Tab" || !root) return;
      const elements = Array.from(root.querySelectorAll<HTMLElement>("input, button:not([disabled]), a[href]"));
      const first = elements[0], last = elements[elements.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    };
    document.addEventListener("keydown", keydown);
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.removeEventListener("keydown", keydown); document.body.style.overflow = overflow; (triggerNode ?? prior)?.focus(); };
  }, [closeCommand, commandOpen]);

  useEffect(() => {
    if (!accountOpen) return;
    const outside = (event: PointerEvent) => { if (!accountMenu.current?.contains(event.target as Node)) setAccountOpen(false); };
    const escape = (event: KeyboardEvent) => { if (event.key === "Escape") setAccountOpen(false); };
    document.addEventListener("pointerdown", outside); document.addEventListener("keydown", escape);
    return () => { document.removeEventListener("pointerdown", outside); document.removeEventListener("keydown", escape); };
  }, [accountOpen]);

  const states = Object.values(bootstrap.system_status);
  const health: "healthy" | "degraded" | "unavailable" = states.some((item) => item.status === "unavailable") ? "unavailable" : states.some((item) => item.status === "degraded") ? "degraded" : "healthy";
  const normalizedTerm = query.trim().toLocaleLowerCase(locale);
  const commands = [
    ...navigation.map((item) => ({ key: item.key, href: item.href, label: label(item.key, item.label), group: copy.groups[item.group] })),
    ...deepLinks.filter((item) => navigation.some((entry) => entry.href === item.parent)).map((item) => ({ key: item.key, href: item.href, label: item.labels[locale as keyof typeof item.labels] || item.labels.en, group: copy.groups.content })),
  ].filter((item) => !normalizedTerm || `${item.label} ${item.group}`.toLocaleLowerCase(locale).includes(normalizedTerm));

  return <div className={`admin-console ${sidebarCollapsed ? "admin-console-collapsed" : ""}`}>
    <AdminNav />
    <div className="admin-workspace">
      <header className="admin-topbar">
        <div className="admin-topbar-heading">
          <nav aria-label="Breadcrumb" className="admin-breadcrumb"><Link href="/admin">{copy.console}</Link><span aria-hidden>/</span><span aria-current="page">{active ? label(active.key, active.label) : copy.console}</span></nav>
          <p className="admin-topbar-mobile-title">{active ? label(active.key, active.label) : copy.console}</p>
        </div>
        <div className="admin-topbar-actions">
          <LanguageSwitcher compact />
          <span className={`admin-health admin-health-${health}`} title={copy[health]}><HeartPulse aria-hidden size={16} /><span>{copy[health]}</span></span>
          <span className="admin-environment"><span>{copy.environment}</span><strong>{bootstrap.environment}</strong></span>
          <button ref={commandTrigger} type="button" onClick={() => setCommandOpen(true)} aria-label={copy.command} className="admin-command-trigger"><Search aria-hidden size={17} /><span>{copy.command}</span><kbd><Command aria-hidden size={11} />K</kbd></button>
          <div ref={accountMenu} className="admin-account-control">
            <button type="button" onClick={() => setAccountOpen((value) => !value)} aria-label={copy.account} aria-expanded={accountOpen} className="admin-account-trigger"><span className="admin-account-avatar"><UserRound aria-hidden size={17} /></span><span className="admin-account-email">{bootstrap.user?.email || user?.email}</span><ChevronDown aria-hidden size={15} /></button>
            {accountOpen && <div className="admin-account-menu"><p className="break-all px-3 py-2 text-xs text-[var(--muted)]">{bootstrap.user?.email || user?.email}</p><Link href="/account" onClick={() => setAccountOpen(false)}>{copy.account}</Link><button type="button" onClick={() => void logout()}>{copy.signOut}</button></div>}
          </div>
        </div>
      </header>
      <div className="admin-content" id="admin-main">{children}</div>
    </div>
    {commandOpen && <div className="admin-command-scrim" role="presentation" onMouseDown={(event) => { if (event.currentTarget === event.target) closeCommand(); }}>
      <div ref={commandDialog} role="dialog" aria-modal="true" aria-labelledby="admin-command-title" className="admin-command-dialog">
        <h2 id="admin-command-title" className="sr-only">{copy.command}</h2>
        <div className="admin-command-input"><Search aria-hidden size={20} /><label className="sr-only" htmlFor="admin-command-query">{copy.command}</label><input id="admin-command-query" value={query} onChange={(event) => setQuery(event.target.value)} placeholder={copy.commandHint} /><button type="button" aria-label={copy.closeMenu} onClick={closeCommand}><X aria-hidden size={19} /></button></div>
        {!normalizedTerm && recent.length > 0 && <section className="border-b border-[var(--line)] px-3 py-3"><h3 className="px-3 pb-2 text-xs font-bold uppercase tracking-[.12em] text-[var(--muted)]">{copy.recent}</h3><div className="grid gap-1">{recent.map((href) => { const item = navigation.find((entry) => entry.href === href); return item ? <Link key={href} href={href} onClick={closeCommand} className="admin-command-row"><span>{label(item.key, item.label)}</span><span>{copy.groups[item.group]}</span></Link> : null; })}</div></section>}
        <div className="max-h-[min(60vh,34rem)] overflow-y-auto p-3">{commands.length ? commands.map((item) => <Link key={`${item.key}-${item.href}`} href={item.href} onClick={closeCommand} className="admin-command-row"><span>{item.label}</span><span>{item.group}</span></Link>) : <p className="p-6 text-center text-sm text-[var(--muted)]">{copy.noCommand}</p>}</div>
      </div>
    </div>}
  </div>;
}
