"use client";

import { Languages } from "lucide-react";
import { useLocale, useTranslations } from "next-intl";
import { useSearchParams } from "next/navigation";
import { useState } from "react";
import { usePathname, useRouter } from "@/i18n/navigation";
import { localeCookieName, localeLabels, locales, type Locale } from "@/i18n/routing";
import { api, ApiError } from "@/lib/api";

export function LanguageSwitcher({ compact = false, showHelp = false }: { compact?: boolean; showHelp?: boolean }) {
  const locale = useLocale() as Locale;
  const pathname = usePathname();
  const searchParams = useSearchParams();
  const router = useRouter();
  const common = useTranslations("common");
  const account = useTranslations("account");
  const [syncFailed, setSyncFailed] = useState(false);

  async function changeLocale(nextLocale: Locale) {
    if (nextLocale === locale) return;
    setSyncFailed(false);
    try {
      // Tells HeaderSessionProvider not to bounce the page back to the stored
      // preference while the PATCH below is still on its way.
      window.sessionStorage.setItem("travel-locale-picked", "1");
    } catch { /* storage can be blocked */ }
    document.cookie = `${localeCookieName}=${encodeURIComponent(nextLocale)}; Max-Age=31536000; Path=/; SameSite=Lax`;
    const query = searchParams.toString();
    router.replace(`${pathname}${query ? `?${query}` : ""}`, { locale: nextLocale });
    try {
      await api("/auth/me", { method: "PATCH", body: JSON.stringify({ preferred_locale: nextLocale }) });
    } catch (error) {
      if (!(error instanceof ApiError && error.status === 401)) setSyncFailed(true);
    }
  }

  // Compact mode is the phone header: a full-width select pushed a 360px header
  // onto two sticky rows, so it collapses to the same 44px icon pattern as the
  // theme switcher, with the real select invisibly on top.
  if (compact) {
    return <label className="theme-switcher" title={localeLabels[locale]}>
      <Languages aria-hidden size={19} />
      <span className="sr-only">{common("language")}</span>
      <select aria-label={common("language")} value={locale} onChange={(event) => void changeLocale(event.target.value as Locale)}>
        {locales.map((value) => <option key={value} value={value}>{localeLabels[value]}</option>)}
      </select>
    </label>;
  }

  return <div className={showHelp ? "space-y-2" : ""}>
    <label className="flex items-center gap-2 text-sm font-semibold">
      <Languages aria-hidden size={19} className="shrink-0 text-[var(--teal)]" />
      <span>{common("language")}</span>
      <select aria-label={common("language")} value={locale} onChange={(event) => void changeLocale(event.target.value as Locale)} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold text-[var(--ink)] outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]">
        {locales.map((value) => <option key={value} value={value}>{localeLabels[value]}</option>)}
      </select>
    </label>
    {showHelp && <p className="text-xs leading-5 text-[var(--muted)]">{account("languageHelp")}</p>}
    {syncFailed && <p role="status" className="text-xs text-amber-800">{account("syncFailed")}</p>}
  </div>;
}
