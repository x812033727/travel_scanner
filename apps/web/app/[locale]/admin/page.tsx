import { getLocale } from "next-intl/server";
import { adminDomainsCopy } from "@/lib/admin-domains-copy";
import { AdminDashboard } from "@/components/admin-dashboard";

export default async function AdminDashboardPage() {
  const copy = adminDomainsCopy(await getLocale());
  return <main className="admin-page"><h1 className="text-3xl font-bold md:text-4xl">{copy.overview}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{copy.overviewDescription}</p><AdminDashboard /></main>;
}
