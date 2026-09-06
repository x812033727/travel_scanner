import { Check, History, ShieldCheck } from "lucide-react";
import { getTranslations } from "next-intl/server";
import { Link } from "@/i18n/navigation";
import { SiteHeader } from "@/components/site-header";
import { getRegistrationAvailability } from "@/lib/registration";
import { getUsageCatalog } from "@/lib/usage-catalog.server";
import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("pricingTitle"), description: t("pricingDescription") };
}


export default async function PricingPage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const [registration, usage, t] = await Promise.all([
    getRegistrationAvailability(),
    getUsageCatalog(locale),
    getTranslations({ locale, namespace: "pricing" }),
  ]);
  const trialUses = usage.status === "ready" ? usage.catalog.trial_uses : null;
  const money = new Intl.NumberFormat(locale, {
    style: "currency",
    currency: "TWD",
    maximumFractionDigits: 0,
  });

  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 py-14">
    <div className="mx-auto max-w-3xl text-center">
      <p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p>
      <h1 className="mt-2 text-4xl font-bold md:text-5xl">{t("title")}</h1>
      <p className="mt-4 leading-7 text-[var(--muted)]">{trialUses === null ? t("descriptionUnavailable") : t("description", { uses: trialUses })}</p>
      {registration === "open" && trialUses !== null
        ? <Link href="/register" className="mt-7 inline-flex rounded-xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white">{t("register", { uses: trialUses })}</Link>
        : <p className="mt-7 inline-flex rounded-xl bg-[#e4ebe6] px-6 py-3.5 font-semibold text-[var(--muted)]">{registration === "closed" ? t("registrationClosed") : t("registrationUnavailable")}</p>}
    </div>

    {usage.status === "unavailable"
      ? <p role="alert" className="mt-12 rounded-2xl border border-amber-200 bg-amber-50 p-6 text-center text-amber-900">{t("catalogUnavailable")}</p>
      : <section aria-label={t("packagesLabel")} className="mt-12 grid gap-5 md:grid-cols-3">
        {usage.catalog.packages.length ? usage.catalog.packages.map((item) => <article key={item.code} className={`relative rounded-[2rem] border bg-white p-7 ${item.is_featured ? "border-[var(--teal)] shadow-[0_20px_60px_rgba(13,107,104,.14)]" : "border-[var(--line)]"}`}>
          {item.is_featured && <span className="absolute right-6 top-6 rounded-full bg-[var(--teal-soft)] px-3 py-1 text-xs font-semibold text-[var(--teal-dark)]">{t("featured")}</span>}
          <p className="font-semibold text-[var(--teal)]">{item.name}</p>
          <h2 className="mt-3 text-4xl font-bold">{item.uses}<span className="ml-1 text-base font-normal text-[var(--muted)]">{t("usesUnit")}</span></h2>
          <p className="mt-5 text-2xl font-bold">{money.format(item.price_twd)}</p>
          <p className="mt-1 text-sm text-[var(--muted)]">{t("perUse", { price: money.format(Math.round(item.price_twd / item.uses)) })} · {t("oneTime")}</p>
          <ul className="my-7 space-y-3 text-sm">
            {[t("benefits.allFeatures"), t("benefits.neverExpires"), t("benefits.history")].map((label) => <li key={label} className="flex gap-2"><Check size={18} className="shrink-0 text-[var(--teal)]" />{label}</li>)}
          </ul>
          <button disabled className="w-full rounded-xl bg-[#e4ebe6] p-3 font-semibold text-[var(--muted)]">{t("purchaseSoon")}</button>
        </article>) : <p className="col-span-full rounded-2xl border border-[var(--line)] bg-white p-6 text-center text-[var(--muted)]">{t("empty")}</p>}
      </section>}

    <section className="mt-8 grid gap-4 rounded-[2rem] border border-[var(--line)] bg-white p-6 md:grid-cols-3 md:p-8">
      <p className="flex gap-3"><ShieldCheck className="shrink-0 text-[var(--teal)]" /><span><strong className="block">{t("promises.successTitle")}</strong><span className="mt-1 block text-sm text-[var(--muted)]">{t("promises.successHelp")}</span></span></p>
      <p className="flex gap-3"><History className="shrink-0 text-[var(--teal)]" /><span><strong className="block">{t("promises.historyTitle")}</strong><span className="mt-1 block text-sm text-[var(--muted)]">{t("promises.historyHelp")}</span></span></p>
      <p className="flex gap-3"><Check className="shrink-0 text-[var(--teal)]" /><span><strong className="block">{t("promises.sameTitle")}</strong><span className="mt-1 block text-sm text-[var(--muted)]">{t("promises.sameHelp")}</span></span></p>
    </section>
  </main></>;
}
