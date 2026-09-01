"use client";

import { Link } from "@/i18n/navigation";
import { useTranslations } from "next-intl";
import { useHeaderSession } from "@/components/header-session";

const pillClass = "rounded-full border border-[var(--line)] bg-white px-4 py-2 text-[var(--ink)]";

export function HeaderAuth() {
  const t = useTranslations("auth");
  const nav = useTranslations("navigation");
  const { status, user, logout } = useHeaderSession();
  if (status === "loading") return <span aria-hidden className={`${pillClass} invisible`}>{t("signIn")}</span>;
  if (status === "unavailable") return <span role="status" title={t("statusUnavailableHelp")} className={`${pillClass} border-red-200 bg-red-50 text-red-800`}>{t("statusUnavailable")}</span>;
  if (status === "signed_out" || !user) return <Link className={pillClass} href="/login">{t("signIn")}</Link>;
  return (
    <span className="flex items-center gap-3">
      {user.is_admin && <Link className="font-semibold text-[var(--teal)]" href="/admin/users">{nav("admin")}</Link>}
      <Link className="hidden max-w-48 truncate text-[var(--ink)] sm:inline" title={user.email} href="/account">{user.email}</Link>
      <button onClick={() => void logout()} className={pillClass}>{t("signOut")}</button>
    </span>
  );
}
