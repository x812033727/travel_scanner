import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";
import { AuthForm } from "@/components/auth-form";
import { SiteHeader } from "@/components/site-header";

import { safeNextPath } from "@/lib/navigation";
import { getRegistrationAvailability } from "@/lib/registration";
import { getUsageCatalog } from "@/lib/usage-catalog.server";
import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("registerTitle"), description: t("registerDescription") };
}


export default async function RegisterPage({ searchParams, params: routeParams }: { searchParams: Promise<{ next?: string | string[]; oauth_error?: string }>; params: Promise<{ locale: string }> }) {
  const { locale } = await routeParams;
  const [params, registration, usage, t] = await Promise.all([searchParams, getRegistrationAvailability(), getUsageCatalog(locale), getTranslations("auth")]);
  const nextPath = safeNextPath(params.next);
  if (registration !== "open") {
    const unavailable = registration === "unavailable";
    return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">{unavailable ? t("registrationUnavailable") : t("registrationPaused")}</p><h1 className="mt-2 text-3xl font-bold">{unavailable ? t("registrationUnavailableTitle") : t("registrationPausedTitle")}</h1><p className="mt-3 text-sm leading-6 text-[var(--muted)]">{unavailable ? t("registrationUnavailableHelp") : t("registrationPausedHelp")}</p><Link className="mt-6 inline-flex rounded-xl bg-[var(--teal)] px-5 py-3 font-semibold text-white" href={`/login?next=${encodeURIComponent(nextPath)}`}>{t("goToSignIn")}</Link></div></main></>;
  }
  return <><SiteHeader /><main className="mx-auto max-w-md px-5 py-14"><div className="rounded-[2rem] border border-[var(--line)] bg-white p-8"><p className="text-sm font-semibold text-[var(--teal)]">{usage.status === "ready" ? t("registerBonus", { uses: usage.catalog.trial_uses }) : t("registerBonusUnavailable")}</p><h1 className="mt-2 text-3xl font-bold">{t("registerTitle")}</h1><p className="mt-3 text-sm leading-6 text-[var(--muted)]">{t("registerDescription")}</p><AuthForm mode="register" nextPath={nextPath} oauthError={params.oauth_error} /><p className="mt-5 text-center text-sm text-[var(--muted)]">{t("hasAccount")} <Link className="text-[var(--teal)] underline" href={`/login?next=${encodeURIComponent(nextPath)}`}>{t("signInDirectly")}</Link></p></div></main></>;
}
