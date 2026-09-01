"use client";

import { Link } from "@/i18n/navigation";
import { usePathname, useRouter } from "@/i18n/navigation";
import { useLocale, useTranslations } from "next-intl";
import { isLocale } from "@/i18n/routing";
import { useEffect, useState } from "react";
import { ApiError, api } from "@/lib/api";

type Me = { id: string; email: string; is_admin?: boolean; preferred_locale: string };

const pillClass = "rounded-full border border-[var(--line)] bg-white px-4 py-2 text-[var(--ink)]";

export function HeaderAuth() {
  const router = useRouter();
  const pathname = usePathname();
  const locale = useLocale();
  const t = useTranslations("auth");
  const nav = useTranslations("navigation");
  const [me, setMe] = useState<Me | null>(null);
  const [ready, setReady] = useState(false);
  const [serviceError, setServiceError] = useState(false);
  useEffect(() => {
    let active = true;
    api<Me>("/auth/me")
      .then((user) => {
        if (!active) return;
        setMe(user);
        if (isLocale(user.preferred_locale) && user.preferred_locale !== locale) {
          document.cookie = `travel_locale=${user.preferred_locale}; path=/; max-age=31536000; samesite=lax`;
          router.replace(pathname, { locale: user.preferred_locale });
        }
      })
      .catch((reason) => {
        if (!active) return;
        if (reason instanceof ApiError && reason.status === 401) setMe(null);
        else setServiceError(true);
      })
      .finally(() => { if (active) setReady(true); });
    return () => { active = false; };
  }, [locale, pathname, router]);
  async function logout() {
    try { await api("/auth/logout", { method: "POST" }); } catch { /* BFF 已清除 cookie */ }
    setMe(null);
    router.push("/");
    router.refresh();
  }
  if (!ready) return <span aria-hidden className={`${pillClass} invisible`}>{t("signIn")}</span>;
  if (serviceError) return <span role="status" title={t("statusUnavailableHelp")} className={`${pillClass} border-red-200 bg-red-50 text-red-800`}>{t("statusUnavailable")}</span>;
  if (!me) return <Link className={pillClass} href="/login">{t("signIn")}</Link>;
  return (
    <span className="flex items-center gap-3">
      {me.is_admin && <Link className="font-semibold text-[var(--teal)]" href="/admin/users">{nav("admin")}</Link>}
      <Link className="hidden max-w-48 truncate text-[var(--ink)] sm:inline" title={me.email} href="/account">{me.email}</Link>
      <button onClick={logout} className={pillClass}>{t("signOut")}</button>
    </span>
  );
}
