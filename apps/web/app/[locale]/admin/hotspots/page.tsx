import { AdminHotspotsWorkspace } from "@/components/admin-hotspots-workspace";

export default function AdminHotspotsPage() {
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">景點候選審核</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">檢查景點、地點資料、多語導覽與附近餐廳候選，集中處理探索、核准、拒絕與停用。</p><AdminHotspotsWorkspace /></main>;
}
