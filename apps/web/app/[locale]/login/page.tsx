import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";
import { AuthForm } from "@/components/auth-form";
import { SiteHeader } from "@/components/site-header";

import { safeNextPath } from "@/lib/navigation";
import { getRegistrationAvailability } from "@/lib/registration";

export default async function LoginPage({ searchParams }: { searchParams: Promise<{ next?: string | string[]; oauth_error?: string }> }) {
  const [params, registration, t] = await Promise.all([searchParams, getRegistrationAvailability(), getTranslations("auth")]);
  const nextPath = safeNextPath(params.next);
  return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">{t("welcomeBack")}</p><h1 className="mt-2 text-3xl font-bold">{t("signInTitle")}</h1><AuthForm mode="login" nextPath={nextPath} oauthError={params.oauth_error} /><p className="mt-5 text-center text-sm text-[var(--muted)]">{registration === "open" ? <>{t("noAccount")} <Link className="text-[var(--teal)] underline" href={`/register?next=${encodeURIComponent(nextPath)}`}>{t("freeRegister")}</Link></> : registration === "closed" ? t("registrationPaused") : t("registrationUnavailable")}</p></div></main></>;
}
