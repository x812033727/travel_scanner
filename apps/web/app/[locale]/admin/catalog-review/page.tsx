import { getLocale } from "next-intl/server";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import { AdminCatalogReviewPanel } from "@/components/admin-catalog-review-panel";

export default async function AdminCatalogReviewPage() {
  const copy = adminDomainsCopy(await getLocale());
  return (
    <main className="admin-page">
      <h1 className="text-3xl font-bold md:text-4xl">{copy.history}</h1>
      <AdminCatalogReviewPanel />
    </main>
  );
}
