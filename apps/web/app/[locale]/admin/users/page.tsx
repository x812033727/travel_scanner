import { getTranslations } from "next-intl/server";
import { AdminUsersPanel } from "@/components/admin-users-panel";

export default async function AdminUsersPage() {
  const t = await getTranslations("admin.pageHeaders.users");
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">{t("title")}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{t("description")}</p><AdminUsersPanel /></main>;
}
