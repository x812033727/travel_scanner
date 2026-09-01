import { getTranslations } from "next-intl/server";
import { AdminNav } from "@/components/admin-nav";
import { AdminUsageSettingsPanel } from "@/components/admin-usage-settings-panel";
import { SiteHeader } from "@/components/site-header";

export default async function AdminUsageSettingsPage() {
  const t = await getTranslations("admin.usage");
  return <><SiteHeader /><main className="mx-auto max-w-7xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">{t("eyebrow")}</p><h1 className="mt-2 text-4xl font-bold">{t("title")}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p><AdminNav current="usage" /><AdminUsageSettingsPanel /></main></>;
}
