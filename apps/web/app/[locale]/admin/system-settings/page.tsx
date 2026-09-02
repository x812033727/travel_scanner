import { AdminSettingsPanel } from "@/components/admin-settings-panel";

export default function AdminSystemSettingsPage() {
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">系統設定</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">管理公開註冊、資料供應商執行模式與服務保護參數；儲存後會立即套用到後續請求。</p><AdminSettingsPanel scope="system" /></main>;
}
