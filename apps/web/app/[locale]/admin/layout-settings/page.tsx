import { getTranslations } from "next-intl/server";
import { AdminSettingsPanel } from "@/components/admin-settings-panel";

export default async function AdminLayoutSettingsPage() {
  const t = await getTranslations("admin.layout");
  return (
      <main className="admin-page">
        <p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">{t("eyebrow")}</p>
        <h1 className="mt-2 text-4xl font-bold">{t("title")}</h1>
        <p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p>
        <AdminSettingsPanel scope="layout" />
      </main>
  );
}
