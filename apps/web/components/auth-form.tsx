"use client";

import { useLocale, useTranslations } from "next-intl";
import { type FormEvent, useState, useSyncExternalStore } from "react";
import { useRouter } from "@/i18n/navigation";
import type { Locale } from "@/i18n/routing";
import { ApiError, api } from "@/lib/api";
import { trackAnalytics } from "@/lib/analytics";
import { safeNextPath } from "@/lib/navigation";

export function AuthForm({ mode, nextPath = "/" }: { mode: "login" | "register"; nextPath?: string }) {
  const router = useRouter();
  const locale = useLocale() as Locale;
  const t = useTranslations("auth");
  const [error, setError] = useState<string>();
  const [busy, setBusy] = useState(false);
  const ready = useSyncExternalStore(
    () => () => undefined,
    () => true,
    () => false,
  );
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  async function submit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setBusy(true); setError(undefined);
    try {
      const result = await api<{ user?: { preferred_locale?: Locale } }>(`/auth/${mode}`, {
        method: "POST",
        body: JSON.stringify({ email, password, ...(mode === "register" ? { preferred_locale: locale } : {}) }),
      });
      const preferredLocale = result.user?.preferred_locale || locale;
      if (mode === "register") trackAnalytics("registration_completed");
      document.cookie = `travel_locale=${preferredLocale}; path=/; max-age=31536000; samesite=lax`;
      router.push(safeNextPath(nextPath), { locale: preferredLocale });
      router.refresh();
    } catch (reason) {
      setError((reason as Error).message);
      if (reason instanceof ApiError && [401, 409, 422].includes(reason.status)) setPassword("");
      setBusy(false);
    }
  }
  return <form onSubmit={submit} className="mt-7 space-y-4"><label className="block text-sm font-semibold">{t("email")}<input required disabled={!ready} autoComplete="email" type="email" name="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal disabled:opacity-60" /></label><label className="block text-sm font-semibold">{t("password")}<input required disabled={!ready} minLength={10} autoComplete={mode === "login" ? "current-password" : "new-password"} type="password" name="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal disabled:opacity-60" /><span className="mt-1 block text-xs font-normal text-[var(--muted)]">{t("passwordHint")}</span></label>{error && <p role="alert" className="text-sm text-red-700">{error}</p>}<button disabled={!ready || busy} className="w-full rounded-xl bg-[var(--teal)] p-3.5 font-semibold text-white disabled:opacity-50">{busy ? t("working") : mode === "login" ? t("signIn") : t("createAccount")}</button></form>;
}
