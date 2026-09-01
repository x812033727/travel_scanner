"use client";

import { Luggage, Menu, X } from "lucide-react";
import { useTranslations } from "next-intl";
import { useEffect, useRef, useState } from "react";
import { LanguageSwitcher } from "@/components/language-switcher";
import { useHeaderSession } from "@/components/header-session";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { Link } from "@/i18n/navigation";
import { featureEnabled, type SiteFeature } from "@/lib/site-features";

const links: Array<{
  key: "home" | "hotspots" | "foods" | "trips" | "alerts" | "flightStatus" | "airlines" | "pricing" | "account";
  href: string;
  feature?: SiteFeature;
}> = [
  { key: "home", href: "/" },
  { key: "hotspots", href: "/hotspots", feature: "hotspots" },
  { key: "foods", href: "/foods" },
  { key: "trips", href: "/trips", feature: "trips" },
  { key: "alerts", href: "/alerts", feature: "alerts" },
  { key: "flightStatus", href: "/flights/status", feature: "flight_status" },
  { key: "airlines", href: "/labs/airlines", feature: "airline_fares" },
  { key: "pricing", href: "/pricing", feature: "pricing" },
  { key: "account", href: "/account" },
];

export function MobileNav() {
  const t = useTranslations("navigation");
  const visibility = useSiteVisibility();
  const { status, user } = useHeaderSession();
  const [open, setOpen] = useState(false);
  const closeButton = useRef<HTMLButtonElement>(null);

  useEffect(() => {
    if (!open) return;
    closeButton.current?.focus();
    const closeOnEscape = (event: KeyboardEvent) => {
      if (event.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [open]);

  return <div className="flex items-center gap-2 md:hidden">
    {featureEnabled(visibility, "trips") && <Link href="/trips" className="flex min-h-11 items-center gap-1.5 whitespace-nowrap rounded-xl px-2.5 text-sm font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)] focus:bg-[var(--teal-soft)]">
      <Luggage aria-hidden size={17} />
      {t("mobileTrips")}
    </Link>}
    <button type="button" aria-label={t("openMenu")} aria-expanded={open} aria-controls="mobile-navigation" onClick={() => setOpen(true)} className="rounded-xl border border-[var(--line)] bg-white p-2.5 text-[var(--ink)]"><Menu size={21} /></button>
    {open && <div className="fixed inset-0 z-50 bg-black/30" onMouseDown={() => setOpen(false)}>
      <nav id="mobile-navigation" aria-label={t("mobileLabel")} onMouseDown={(event) => event.stopPropagation()} className="ml-auto flex h-full w-[min(84vw,22rem)] flex-col bg-white p-5 shadow-2xl">
        <div className="mb-5 flex items-center justify-between"><strong>Travel Scanner</strong><button ref={closeButton} type="button" aria-label={t("closeMenu")} onClick={() => setOpen(false)} className="rounded-xl border border-[var(--line)] p-2"><X size={20} /></button></div>
        <div className="mb-4"><LanguageSwitcher /></div>
        <div className="grid gap-2">{links.filter((item) => !item.feature || featureEnabled(visibility, item.feature)).map((item) => <Link key={item.href} href={item.href} onClick={() => setOpen(false)} className="rounded-xl px-4 py-3 font-semibold text-[var(--ink)] hover:bg-[var(--teal-soft)] focus:bg-[var(--teal-soft)]">{t(item.key)}</Link>)}{status === "authenticated" && user?.is_admin && <Link href="/admin/users" onClick={() => setOpen(false)} className="rounded-xl px-4 py-3 font-semibold text-[var(--teal)] hover:bg-[var(--teal-soft)] focus:bg-[var(--teal-soft)]">{t("admin")}</Link>}</div>
        <Link href="/login" onClick={() => setOpen(false)} className="mt-auto rounded-xl bg-[var(--teal)] px-4 py-3 text-center font-semibold text-white">{t("login")}</Link>
      </nav>
    </div>}
  </div>;
}
