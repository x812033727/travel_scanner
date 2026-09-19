"use client";

import { useLocale, useTranslations } from "next-intl";
import { type FormEvent, useState, useSyncExternalStore } from "react";
import { Link, useRouter } from "@/i18n/navigation";
import { type Locale, locales } from "@/i18n/routing";
import { ApiError, api } from "@/lib/api";
import { trackAnalytics } from "@/lib/analytics";
import { safeNextPath } from "@/lib/navigation";
import { SocialLoginButtons } from "@/components/social-login-buttons";

/**
 * `/zh-TW/trips/x?tab=1` -> `{ locale: "zh-TW", pathname: "/trips/x?tab=1" }`; a bare
 * `/trips/x` comes back as it is, with no locale.
 *
 * The localized router adds the locale prefix itself, so a `next` that already carried one
 * landed on `/zh-TW/zh-TW/trips/...` and a 404. Such values are ordinary: the admin layout
 * and the price-alert button build `next` from the raw request path, and a pasted URL has
 * the prefix too. The prefix has to be a whole segment (`/japan` is not `/ja`) and is
 * matched without regard to case, because the middleware serves `/zh-tw/` as well; the
 * query string stays with the path. Only one prefix is taken, exactly as the middleware does.
 */
function splitLocalePrefix(pathname: string): { locale?: Locale; pathname: string } {
  const first = pathname.slice(1).split(/[/?#]/, 1)[0];
  const locale = locales.find((candidate) => candidate.toLowerCase() === first.toLowerCase());
  if (!locale) return { pathname };
  const rest = pathname.slice(first.length + 1);
  return { locale, pathname: rest.startsWith("/") ? rest : `/${rest}` };
}

export function AuthForm({ mode, nextPath = "/", oauthError }: { mode: "login" | "register"; nextPath?: string; oauthError?: string }) {
  const router = useRouter();
  const locale = useLocale() as Locale;
  const t = useTranslations("auth");
  const community = useTranslations("community");
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
      const { locale: pathLocale, pathname } = splitLocalePrefix(safeNextPath(nextPath));
      // A locale named in `next` is the route the visitor was on, so it wins over the account's
      // preferred locale; a bare path follows the preference as before. Either way the router
      // adds the prefix exactly once. The second safeNextPath catches a remainder that only
      // becomes protocol-relative once the prefix is gone (`/zh-TW//evil.example`).
      router.push(safeNextPath(pathname), { locale: pathLocale ?? preferredLocale });
      router.refresh();
    } catch (reason) {
      setError((reason as Error).message);
      if (reason instanceof ApiError && [401, 409, 422].includes(reason.status)) setPassword("");
      setBusy(false);
    }
  }
  return <><SocialLoginButtons nextPath={nextPath} oauthError={oauthError} /><form onSubmit={submit} className="space-y-4"><label className="block text-sm font-semibold">{t("email")}<input required disabled={!ready} autoComplete="email" type="email" name="email" value={email} onChange={(event) => setEmail(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal disabled:opacity-60" /></label><label className="block text-sm font-semibold">{t("password")}<input required disabled={!ready} minLength={mode === "register" ? 10 : undefined} autoComplete={mode === "login" ? "current-password" : "new-password"} type="password" name="password" value={password} onChange={(event) => setPassword(event.target.value)} className="mt-2 w-full rounded-xl border border-[var(--line)] p-3 font-normal disabled:opacity-60" />{mode === "register" && <span className="mt-1 block text-xs font-normal text-[var(--muted)]">{t("passwordHint")}</span>}</label>{error && <p role="alert" className="text-sm text-red-700">{error}</p>}<button disabled={!ready || busy} className="w-full rounded-xl bg-[var(--teal)] p-3.5 font-semibold text-white disabled:opacity-50">{busy ? t("working") : mode === "login" ? t("signIn") : t("createAccount")}</button></form>{mode === "login" && <Link href="/forgot-password" className="mt-4 inline-flex min-h-11 items-center text-sm font-semibold text-[var(--teal)] underline">{community("forgotPassword")}</Link>}</>;
}
