import { AdminHotspotsPanel } from "@/components/admin-hotspots-panel";
import { AdminHotspotGuidesPanel } from "@/components/admin-hotspot-guides-panel";
import { AdminNav } from "@/components/admin-nav";
import { SiteHeader } from "@/components/site-header";

export default function AdminHotspotsPage() {
  return <><SiteHeader /><main className="mx-auto max-w-7xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-4xl font-bold">景點候選審核</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">檢查景點與多語文章／影片候選，支援探索、覆蓋率追蹤、核准、拒絕或停用。</p><AdminNav current="hotspots" /><AdminHotspotsPanel /><AdminHotspotGuidesPanel /></main></>;
}
