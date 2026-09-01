import { AdminHotspotsPanel } from "@/components/admin-hotspots-panel";
import { AdminNav } from "@/components/admin-nav";
import { SiteHeader } from "@/components/site-header";

export default function AdminHotspotsPage() {
  return <><SiteHeader /><main className="mx-auto max-w-7xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-4xl font-bold">景點候選審核</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">檢查 Wikimedia 自動探索的名稱、類型、距離、瀏覽量與來源，支援多選核准、拒絕或停用。</p><AdminNav current="hotspots" /><AdminHotspotsPanel /></main></>;
}
