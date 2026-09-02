import { AccountPanel } from "@/components/account-panel";
import { AccountSavedItems } from "@/components/account-saved-items";
import { LanguageSwitcher } from "@/components/language-switcher";
import { SiteHeader } from "@/components/site-header";
import { getTranslations } from "next-intl/server";

export default async function AccountPage() {
  const t = await getTranslations("account");
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 py-8 md:py-12"><p className="text-sm font-semibold text-[var(--teal)]">{t("eyebrow")}</p><h1 className="mb-8 mt-2 text-3xl font-bold md:text-4xl">{t("title")}</h1><AccountSavedItems /><section className="mb-6 rounded-[2rem] border border-[var(--line)] bg-white p-6 md:p-8"><h2 className="mb-4 text-xl font-bold">{t("languageTitle")}</h2><LanguageSwitcher showHelp /></section><AccountPanel /></main></>;
}
