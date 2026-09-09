import { getLocale } from "next-intl/server";
import { AdminDatabasePanel } from "@/components/admin-database-panel";
import { AdminPageHeader } from "@/components/admin-ui";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";

export default async function AdminDatabasePage() {
  const copy = adminOperationsCopy(await getLocale());
  return <main className="admin-page"><AdminPageHeader eyebrow={copy.groups.system} title={copy.databaseTitle} description={copy.databaseDescription} /><AdminDatabasePanel /></main>;
}
