"use client";

import { BookOpen, CircleUserRound, LogIn, Menu, Search, ShieldCheck, Sparkles, X } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { createPortal } from "react-dom";
import { LanguageSwitcher } from "@/components/language-switcher";
import { useTheme } from "@/components/theme-provider";
import { useHeaderSession } from "@/components/header-session";
import { TextSizeSwitcher } from "@/components/text-size-switcher";
import { ThemeSwitcher } from "@/components/theme-switcher";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link, usePathname } from "@/i18n/navigation";
import { useModalSheet } from "@/lib/modal-sheet";
import { type Locale } from "@/i18n/routing";
import { primaryNavLinks } from "@/lib/nav-links";
import { featureVisible } from "@/lib/site-features";
import { useCommunity } from "@/components/community/provider";
import { useDiscoveryStatus } from "@/lib/discovery";
import { frontendCopy } from "@/lib/frontend-navigation";

export function MobileNav() {
  const { status, user } = useHeaderSession();
  const nav = useTranslations("navigation");
  const community = useCommunity();
  const tc = useTranslations("community");
  const locale = useLocale() as Locale;
  const discovery = useDiscoveryStatus();
  const flowCopy = frontendCopy(locale);
  const { preference } = useTheme();
  const themeValue = nav(preference === "system" ? "themeSystem" : preference === "dark" ? "themeDark" : "themeLight");
  const visibility = useSiteVisibility();
  const pathname = usePathname();
  const [openPath, setOpenPath] = useState<string | null>(null);
  const open = openPath === pathname && !discovery.loading && !discovery.enabled;
  const setOpen = (value: boolean) => setOpenPath(value ? pathname : null);
  const sheetRef = useModalSheet<HTMLDivElement>(open, () => setOpenPath(null));
  const closeRef = useRef<HTMLButtonElement>(null);
  const triggerRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    const reset = window.setTimeout(() => setOpenPath((current) => !discovery.loading && !discovery.enabled && current === pathname ? current : null), 0);
    return () => window.clearTimeout(reset);
  }, [pathname, discovery.enabled, discovery.loading]);

  // The bottom tab bar carries only five destinations; flight status, airfares
  // and plans used to be unreachable on a phone without typing the URL.
  const links = primaryNavLinks.filter(
    (item) => !item.feature || featureVisible(visibility, item.feature),
  );

  useEffect(() => {
    if (!open) return;
    const close = () => setOpenPath(null);
    window.addEventListener("popstate", close);
    return () => window.removeEventListener("popstate", close);
  }, [open]);

  // Four unlabelled icons in a row asked the reader to know what a monitor with a
  // gear and a 文A glyph do. Appearance, language and text size are all display
  // preferences, so they moved into the menu where each one has a word next to it,
  // and the bar keeps the two things people reach for: their account and the menu.
  if (discovery.loading) return <div className="flex items-center gap-1 lg:hidden"><LanguageSwitcher compact /><div aria-hidden className="h-11 w-24 rounded-xl bg-[var(--paper)]" /></div>;
  if (discovery.enabled) return <div className="flex items-center gap-1 lg:hidden">
    <LanguageSwitcher compact />
    {/* Without this the phone header had no sign-in entry at all: a visitor had to
        guess that "my" leads somewhere with a login link at the bottom of a list. */}
    <Link href={status === "authenticated" ? "/account" : "/login"} aria-label={status === "authenticated" ? nav("account") : nav("login")} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      {status === "authenticated" ? <CircleUserRound size={21} /> : <LogIn size={21} />}
    </Link>
    <Link href="/explore" aria-label={flowCopy.explore} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] focus-visible:outline focus-visible:outline-2"><Search size={21} aria-hidden /></Link>
    <Link href="/my" aria-label={flowCopy.my} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] focus-visible:outline focus-visible:outline-2"><CircleUserRound size={21} aria-hidden /></Link>
    {/* This branch returns before the menu sheet is rendered, so the guides section would
        be unreachable on a phone in discovery mode without its own entry here. */}
    <Link href="/guides" aria-label={nav("guides")} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] focus-visible:outline focus-visible:outline-2"><BookOpen size={21} aria-hidden /></Link>
    {/* Same reasoning for the lifestyle section: no menu sheet in this branch, so no other
        phone entry. The footer carries both links as well.
        Hidden below 360px because this row cannot hold six of them there. Six 2.75rem
        targets plus their gaps are 322.5px at the large text size, and the header's own
        1.25rem padding puts the right edge at 345px: past a 320px screen. The phone then
        widens its layout viewport to fit -- innerWidth reports 342 instead of 320 -- and
        every coordinate on the page shifts with it, which is what broke the 320px food
        acceptance run. The same overflow is what collapsed the language switcher into an
        icon; see the comment in language-switcher.tsx. */}
    <Link href="/life" aria-label={nav("life")} className="hidden min-[360px]:grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] focus-visible:outline focus-visible:outline-2"><Sparkles size={21} aria-hidden /></Link>
  </div>;
  return <div className="flex items-center gap-1 lg:hidden">
    <LanguageSwitcher compact />
    {/* The desktop nav that carries the admin link is hidden below lg, and neither the
        bottom bar nor the account page offers one, so without this an administrator on a
        phone can only reach the control centre by typing the URL. */}
    {user?.is_admin && <Link href="/admin" aria-label={nav("admin")} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      <ShieldCheck size={21} />
    </Link>}
    <Link href={status === "authenticated" ? "/account" : "/login"} aria-label={status === "authenticated" ? nav("account") : nav("login")} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      {status === "authenticated" ? <CircleUserRound size={21} /> : <LogIn size={21} />}
    </Link>
    <button ref={triggerRef} type="button" aria-label={nav("openMenu")} aria-expanded={open} onClick={(event) => { event.currentTarget.focus(); setOpen(true); }} className="grid h-11 w-11 place-items-center rounded-xl text-[var(--teal)] hover:bg-[var(--teal-soft)]">
      <Menu size={21} />
    </button>
    {/* The site header paints itself with backdrop-filter, which makes it the
        containing block for every fixed descendant: this sheet was being laid out
        inside a 68px strip, so tapping the menu on a phone showed one row of it
        pinned to the top of the screen and nothing else. It belongs on the body. */}
    {open && createPortal(<div role="presentation" className="fixed inset-0 z-[90] bg-slate-950/45 backdrop-blur-sm" onMouseDown={(event) => { if (event.target === event.currentTarget) setOpen(false); }}>
      <div ref={sheetRef} role="dialog" aria-modal="true" aria-label={nav("primaryLabel")} className="absolute inset-x-0 bottom-0 max-h-[85vh] overflow-y-auto rounded-t-[2rem] bg-[var(--surface)] p-5 pb-[calc(1.5rem+env(safe-area-inset-bottom))] shadow-2xl">
        <div className="mb-3 flex items-center justify-between">
          <p className="text-sm font-bold text-[var(--muted)]">{nav("primaryLabel")}</p>
          <button ref={closeRef} type="button" aria-label={nav("closeMenu")} onClick={() => setOpen(false)} className="grid h-11 w-11 place-items-center rounded-full border border-[var(--line)]">
            <X size={18} />
          </button>
        </div>
        {/* Above the destinations, because someone who cannot read the destinations
            needs this first; and each row says what it is set to, so the icon is
            confirmation rather than the only clue. */}
        <div className="mb-5 grid gap-4 border-b border-[var(--line)] pb-5">
          <TextSizeSwitcher variant="expanded" />
          <div className="flex min-h-12 items-center justify-between gap-3">
            <span className="text-sm font-bold text-[var(--muted)]">{nav("themeLabel")}</span>
            <span className="flex items-center gap-2.5">
              <span className="text-sm font-semibold">{themeValue}</span>
              <ThemeSwitcher />
            </span>
          </div>
        <nav aria-label={nav("primaryLabel")} className="grid gap-1">
          {/* The sheet only opens when discovery is off (see `open` above), so anything
              guarded by discovery.enabled here could never render. Removed rather than
              left to mislead the next reader into thinking these links exist. */}
          {community.flags.enabled && [["/community", "title"], ["/pet-friendly", "pets"], ...(!discovery.enabled ? [["/my", "my"]] : [])].map(([href, key]) => <Link key={href} href={href} onClick={() => setOpen(false)} className="flex min-h-12 items-center rounded-xl px-3 font-semibold hover:bg-[var(--teal-soft)]">{tc(key)}</Link>)}
          {links.map((item) => <Link key={item.href} href={item.href} onClick={() => setOpen(false)} className="flex min-h-12 items-center rounded-xl px-3 font-semibold hover:bg-[var(--teal-soft)]">
            {nav(item.key)}
          </Link>)}
        </nav>

        </div>
      </div>
    </div>, document.body)}
  </div>;
}
