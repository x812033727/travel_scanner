import { AccountList } from "@/components/account-list";
import { SiteHeader } from "@/components/site-header";
import { Plus, Route } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";
import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("tripsTitle"), description: t("tripsDescription") };
}


export default async function TripsPage() {
  const t = await getTranslations("trips");
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-5xl px-5 py-8 md:py-12">
        <section className="app-page-hero mb-7 flex flex-wrap items-end justify-between gap-4">
          <div className="flex items-start gap-4">
            <span className="app-page-hero-icon"><Route size={23} /></span>
            <div>
            <p className="text-sm font-semibold text-[var(--teal)]">
              {t("savedEyebrow")}
            </p>
            <h1 className="mt-2 text-4xl font-bold">{t("myTrips")}</h1>
            <p className="mt-2 text-[var(--muted)]">
              {t("myTripsDescription")}
            </p>
            </div>
          </div>
          <Link
            href="/trips/new"
            className="app-primary-button"
          >
            <Plus size={17} />
            {t("newTrip")}
          </Link>
        </section>
        <AccountList kind="trips" />
      </main>
    </>
  );
}
