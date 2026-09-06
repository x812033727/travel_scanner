import { AccountPanel } from "@/components/account-panel";
import { AccountSavedItems } from "@/components/account-saved-items";
import { CurrencySwitcher } from "@/components/currency-switcher";
import { LanguageSwitcher } from "@/components/language-switcher";
import { SiteHeader } from "@/components/site-header";
import { getTranslations } from "next-intl/server";
import { UserRound } from "lucide-react";
import type { Metadata } from "next";
import type { Locale } from "@/i18n/routing";

export async function generateMetadata({ params }: { params: Promise<{ locale: Locale }> }): Promise<Metadata> {
  const { locale } = await params;
  const t = await getTranslations({ locale, namespace: "metadata" });
  return { title: t("accountTitle"), description: t("accountDescription") };
}


export default async function AccountPage() {
  const t = await getTranslations("account");
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-6xl px-5 py-8 md:py-12">
        <section className="app-page-hero mb-7 flex items-start gap-4"><span className="app-page-hero-icon"><UserRound size={23} /></span><div><p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{t("title")}</h1></div></section>
        <AccountSavedItems />
        <section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8">
          <h2 className="mb-4 text-xl font-bold">{t("languageTitle")}</h2>
          <LanguageSwitcher showHelp />
        </section>
        <CurrencySwitcher />
        <AccountPanel />
      </main>
    </>
  );
}
