import { Link } from "@/i18n/navigation";
import { useTranslations } from "next-intl";

export function AdminNav({ current }: { current: "users" | "usage" | "system" | "layout" | "providers" | "hotspots" | "foods" }) {
  const t = useTranslations("admin.navigation");
  const linkClass = (active: boolean) => `rounded-xl px-4 py-2.5 text-sm font-semibold ${active ? "bg-[var(--ink)] text-white" : "hover:bg-[var(--paper)]"}`;
  return <nav aria-label="管理後台功能" className="mt-6 flex flex-wrap gap-2 rounded-2xl border border-[var(--line)] bg-white p-2">
    <Link href="/admin/users" aria-current={current === "users" ? "page" : undefined} className={linkClass(current === "users")}>{t("users")}</Link>
    <Link href="/admin/usage-settings" aria-current={current === "usage" ? "page" : undefined} className={linkClass(current === "usage")}>{t("usage")}</Link>
    <Link href="/admin/system-settings" aria-current={current === "system" ? "page" : undefined} className={linkClass(current === "system")}>{t("system")}</Link>
    <Link href="/admin/layout-settings" aria-current={current === "layout" ? "page" : undefined} className={linkClass(current === "layout")}>{t("layout")}</Link>
    <Link href="/admin/settings" aria-current={current === "providers" ? "page" : undefined} className={linkClass(current === "providers")}>{t("providers")}</Link>
    <Link href="/admin/hotspots" aria-current={current === "hotspots" ? "page" : undefined} className={linkClass(current === "hotspots")}>{t("hotspots")}</Link>
    <Link href="/admin/foods" aria-current={current === "foods" ? "page" : undefined} className={linkClass(current === "foods")}>{t("foods")}</Link>
  </nav>;
}
