"use client";

import { useLocale } from "next-intl";
import type { ReactNode } from "react";
import { AdminAccessState } from "@/components/admin-access-state";
import { useAdminOperations } from "@/components/admin-operations-provider";
import { usePathname } from "@/i18n/navigation";
import { canAccessAdminPath } from "@/lib/admin-operations";

/**
 * The capability check again, on every navigation. `layout.tsx` checks the requested path on a
 * full load, but Next keeps a layout mounted across client-side navigations and does not render
 * it again, so a role-limited admin who followed a `<Link>` to a page outside their capabilities
 * got that page inside the shell. This re-renders whenever the path changes and applies the same
 * test to the same bootstrap. The data was never at risk: every admin endpoint enforces
 * `require_capability`, so this only stops the shell from rendering a page that cannot load.
 */
export default function AdminTemplate({ children }: { children: ReactNode }) {
  const locale = useLocale();
  const pathname = usePathname();
  const bootstrap = useAdminOperations()?.bootstrap;
  if (!bootstrap || !canAccessAdminPath(bootstrap, pathname)) {
    return <AdminAccessState locale={locale} status="forbidden" />;
  }
  return children;
}
