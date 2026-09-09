import { headers } from "next/headers";
import { redirect } from "next/navigation";
import { AdminAccessState } from "@/components/admin-access-state";
import { AdminOperationsProvider } from "@/components/admin-operations-provider";
import { AdminShell } from "@/components/admin-shell";
import { loadAdminBootstrap } from "@/lib/admin-bootstrap.server";
import { canAccessAdminPath } from "@/lib/admin-operations";

type Props = Readonly<{ children: React.ReactNode; params: Promise<{ locale: string }> }>;

function safeNextPath(candidate: string | null, locale: string) {
  if (!candidate?.startsWith("/") || candidate.startsWith("//")) return `/${locale}/admin`;
  return candidate;
}

export default async function AdminLayout({ children, params }: Props) {
  const [{ locale }, requestHeaders, result] = await Promise.all([params, headers(), loadAdminBootstrap()]);
  if (result.status === "signed_out") {
    const next = safeNextPath(requestHeaders.get("x-travel-pathname"), locale);
    redirect(`/${locale}/login?next=${encodeURIComponent(next)}`);
  }
  if (result.status === "forbidden") return <AdminAccessState locale={locale} status="forbidden" />;
  if (result.status === "unavailable") return <AdminAccessState locale={locale} status="unavailable" />;
  const requestedPath = safeNextPath(requestHeaders.get("x-travel-pathname"), locale);
  if (!canAccessAdminPath(result.data, requestedPath, locale)) return <AdminAccessState locale={locale} status="forbidden" />;
  return <AdminOperationsProvider bootstrap={result.data}><AdminShell>{children}</AdminShell></AdminOperationsProvider>;
}
