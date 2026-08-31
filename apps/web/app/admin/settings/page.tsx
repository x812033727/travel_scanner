import { AdminSettingsPanel } from "@/components/admin-settings-panel";
import { AdminNav } from "@/components/admin-nav";
import { SiteHeader } from "@/components/site-header";

export default function AdminSettingsPage() {
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-4xl font-bold">API 與供應商設定</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">集中管理即時航班、住宿、活動、Google Maps 與日本路線服務。金鑰只會送往後端加密保存，重新載入後僅顯示遮罩。</p><AdminNav current="settings" /><AdminSettingsPanel /></main></>;
}
