import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { SiteHeader } from "@/components/site-header";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("contactTitle"), description: t("contactDescription") };
}

export default async function ContactPage() {
  const t = await getTranslations("navigation");
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
        <h1 className="text-3xl font-bold md:text-4xl">{t("footerContact")}</h1>
        <p className="mt-4 text-sm leading-7 text-[var(--muted)]">{t("footerContactBody")}</p>
      </main>
    </>
  );
}
