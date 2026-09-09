import { getLocale, getTranslations } from "next-intl/server";
import { AdminUsersPanel } from "@/components/admin-users-panel";
import { AdminPageHeader } from "@/components/admin-ui";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";

export default async function AdminUsersPage() {
  const [t, locale] = await Promise.all([getTranslations("admin.pageHeaders.users"), getLocale()]);
  const copy = adminOperationsCopy(locale);
  return <main className="admin-page"><AdminPageHeader eyebrow={copy.groups.operations} title={t("title")} description={t("description")} /><AdminUsersPanel /></main>;
}
