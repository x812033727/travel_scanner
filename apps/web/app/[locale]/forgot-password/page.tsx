import { SiteHeader } from "@/components/site-header";
import { ForgotPassword } from "@/components/community/accounts";
import { getTranslations } from "next-intl/server";
export async function generateMetadata() {
  const t = await getTranslations("metadata");
  return { title: t("recoverTitle"), description: t("recoverDescription"), robots: { index: false, follow: true } };
}
export default async function Page() { const t = await getTranslations("community"); return <><SiteHeader /><main className="mx-auto max-w-xl px-5 py-10"><h1 className="mb-6 text-3xl font-bold">{t("forgotPassword")}</h1><ForgotPassword /></main></>; }
