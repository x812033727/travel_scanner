import { getTranslations } from "next-intl/server";
import { redirect } from "next/navigation";
import { AdminSettingsPanel, SETTINGS_PAGE_CATEGORIES } from "@/components/admin-settings-panel";
import { Link } from "@/i18n/navigation";
import { AI_SETTINGS_PATH, aiSettingsTab, isAiSettingsProvider } from "@/lib/admin-settings-ownership";

type Search = Record<string, string | string[] | undefined>;

export default async function AdminSettingsPage({ params, searchParams }: { params: Promise<{ locale: string }>; searchParams: Promise<Search> }) {
  const [{ locale }, search] = await Promise.all([params, searchParams]);
  const provider = typeof search.provider === "string" ? search.provider : "";
  if (isAiSettingsProvider(provider)) {
    // Links made before the AI cards moved (the video tool's pairing link among them)
    // land on the AI settings page with every parameter they carried.
    const query = new URLSearchParams({ tab: aiSettingsTab(provider) });
    for (const [key, value] of Object.entries(search)) if (typeof value === "string" && key !== "tab") query.set(key, value);
    redirect(`/${locale}${AI_SETTINGS_PATH}?${query}`);
  }
  const t = await getTranslations("admin.pageHeaders.providers");
  const moved = await getTranslations("admin.aiSettings");
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{t("title")}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p><p className="mt-4 max-w-3xl rounded-xl bg-[var(--paper)] p-4 text-sm leading-6">{moved("movedNotice")} <Link href={`${AI_SETTINGS_PATH}?tab=api`} className="font-semibold text-[var(--teal)] underline">{moved("movedLink")}</Link></p><AdminSettingsPanel scope="providers" categories={SETTINGS_PAGE_CATEGORIES} /></main>;
}
