import { SiteHeader } from "@/components/site-header";
import { AccountConfirmation } from "@/components/community/accounts";
import { getTranslations } from "next-intl/server";
export async function generateMetadata() {
 const t = await getTranslations("metadata");
 return { title: t("confirmationTitle"), description: t("confirmationDescription"), robots: { index: false, follow: false }, referrer: "no-referrer" as const };
}
export default async function Page({ searchParams }: { searchParams: Promise<{ purpose?: string }> }) {
 const { purpose } = await searchParams;
 return <><SiteHeader /><main className="mx-auto max-w-xl px-5 py-10"><AccountConfirmation purpose={purpose || ""} /></main></>;
}
