import type { Metadata } from "next";
import { getTranslations } from "next-intl/server";
import type { Locale } from "@/i18n/routing";
import { SiteHeader } from "@/components/site-header";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("termsTitle"), description: t("termsDescription") };
}

export default async function TermsPage() {
  const t = await getTranslations("navigation");
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-3xl px-5 py-10 md:py-14">
        <h1 className="text-3xl font-bold md:text-4xl">{t("footerTerms")}</h1>
        {/* Deliberately not a policy. The wording of a privacy policy or terms of service
            has to be written and approved by the people who run the site; anything generated
            here would read as a commitment nobody made. The page exists so the footer link
            has somewhere honest to land until that text is ready. */}
        <p className="mt-4 text-lg font-semibold">{t("footerPendingTitle")}</p>
        <p className="mt-3 text-sm leading-7 text-[var(--muted)]">{t("footerPendingBody")}</p>
      </main>
    </>
  );
}
