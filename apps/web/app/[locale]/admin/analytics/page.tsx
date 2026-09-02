import { getTranslations } from "next-intl/server";
import { AdminAnalyticsPanel } from "@/components/admin-analytics-panel";

export default async function AdminAnalyticsPage() {
  const t = await getTranslations("admin.analytics");
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">{t("eyebrow")}</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{t("title")}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p><AdminAnalyticsPanel /></main>;
}
