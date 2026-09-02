import { AdminSettingsPanel } from "@/components/admin-settings-panel";

export default function AdminSettingsPage() {
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">API 與供應商設定</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">集中管理即時航班、住宿、活動、Google Maps 與日本路線服務；金鑰只會送往後端加密保存。</p><AdminSettingsPanel scope="providers" /></main>;
}
