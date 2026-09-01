import { AdminNav } from "@/components/admin-nav";
import { AdminSettingsPanel } from "@/components/admin-settings-panel";
import { SiteHeader } from "@/components/site-header";

export default function AdminSystemSettingsPage() {
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-4xl font-bold">系統設定</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">管理公開註冊、資料供應商執行模式與服務保護參數；儲存後會立即套用到後續請求。</p><AdminNav current="system" /><AdminSettingsPanel scope="system" /></main></>;
}
