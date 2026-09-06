import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";
import { AccountList } from "@/components/account-list";
import { LineConnectionPanel } from "@/components/line-connection-panel";
import { SiteHeader } from "@/components/site-header";
import { BellRing } from "lucide-react";
import { getTranslations } from "next-intl/server";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("alertsTitle"), description: t("alertsDescription") };
}

export default async function AlertsPage() {
  const t = await getTranslations("alerts");
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-4xl px-5 py-8 md:py-12">
        <section className="app-page-hero mb-7 flex items-start gap-4">
          <span className="app-page-hero-icon"><BellRing size={23} /></span>
          <div>
            <p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p>
            <h1 className="mt-2 text-3xl font-bold md:text-4xl">{t("title")}</h1>
            <p className="mt-2 text-sm text-[var(--muted)] md:text-base">{t("description")}</p>
          </div>
        </section>
        <LineConnectionPanel />
        <AccountList kind="alerts" />
      </main>
    </>
  );
}
