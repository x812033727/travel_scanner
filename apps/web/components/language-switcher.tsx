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
    document.cookie = `${localeCookieName}=${encodeURIComponent(nextLocale)}; Max-Age=31536000; Path=/; SameSite=Lax`;
    const query = searchParams.toString();
    router.replace(`${pathname}${query ? `?${query}` : ""}`, { locale: nextLocale });
    try {
      await api("/auth/me", { method: "PATCH", body: JSON.stringify({ preferred_locale: nextLocale }) });
    } catch (error) {
      if (!(error instanceof ApiError && error.status === 401)) setSyncFailed(true);
    }
  }

  return <div className={showHelp ? "space-y-2" : ""}>
    <label className={`flex items-center gap-2 ${compact ? "text-sm" : "text-sm font-semibold"}`}>
      <Languages aria-hidden size={compact ? 17 : 19} className="shrink-0 text-[var(--teal)]" />
      {!compact && <span>{common("language")}</span>}
      <select aria-label={common("language")} value={locale} onChange={(event) => void changeLocale(event.target.value as Locale)} className="min-h-11 rounded-xl border border-[var(--line)] bg-white px-3 text-sm font-semibold text-[var(--ink)] outline-none focus:border-[var(--teal)] focus:ring-4 focus:ring-[var(--teal-soft)]">
        {locales.map((value) => <option key={value} value={value}>{localeLabels[value]}</option>)}
      </select>
    </label>
    {showHelp && <p className="text-xs leading-5 text-[var(--muted)]">{account("languageHelp")}</p>}
    {syncFailed && <p role="status" className="text-xs text-amber-800">{account("syncFailed")}</p>}
  </div>;
}
