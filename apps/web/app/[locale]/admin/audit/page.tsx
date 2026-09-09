import { getLocale } from "next-intl/server";
import { AdminAuditPanel } from "@/components/admin-audit-panel";
import { AdminPageHeader } from "@/components/admin-ui";
import { adminOperationsCopy } from "@/lib/admin-operations-copy";

export default async function AdminAuditPage() {
  const copy = adminOperationsCopy(await getLocale());
  return <main className="admin-page"><AdminPageHeader eyebrow={copy.groups.operations} title={copy.auditTitle} description={copy.auditDescription} /><AdminAuditPanel /></main>;
}
