import { AdminDashboard } from "@/components/admin-dashboard";

export default function AdminDashboardPage() {
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">營運總覽</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">快速掌握公開內容、待審工作與會員狀態，再進入各管理模組處理。</p><AdminDashboard /></main>;
}
