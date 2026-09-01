import { getTranslations } from "next-intl/server";
import { AdminNav } from "@/components/admin-nav";
import { AdminSettingsPanel } from "@/components/admin-settings-panel";
import { SiteHeader } from "@/components/site-header";

export default async function AdminLayoutSettingsPage() {
  const t = await getTranslations("admin.layout");
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-6xl px-5 pb-16 pt-8 md:px-8">
        <p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">{t("eyebrow")}</p>
        <h1 className="mt-2 text-4xl font-bold">{t("title")}</h1>
        <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p>
        <AdminNav current="layout" />
        <AdminSettingsPanel scope="layout" />
      </main>
    </>
  );
}
