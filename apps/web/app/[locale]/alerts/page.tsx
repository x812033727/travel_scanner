import { AccountList } from "@/components/account-list";
import { LineConnectionPanel } from "@/components/line-connection-panel";
import { SiteHeader } from "@/components/site-header";
import { BellRing } from "lucide-react";
export default function AlertsPage() {
  return (
    <>
      <SiteHeader />
      <main className="mx-auto max-w-4xl px-5 py-8 md:py-12">
        <section className="app-page-hero mb-7 flex items-start gap-4"><span className="app-page-hero-icon"><BellRing size={23} /></span><div><p className="text-sm font-semibold text-[var(--teal)]">PRICE WATCH</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">價格通知</h1><p className="mt-2 text-sm text-[var(--muted)] md:text-base">集中查看追蹤進度、調整目標價格與 LINE 通知狀態。</p></div></section>
        <LineConnectionPanel />
        <AccountList kind="alerts" />
      </main>
    </>
  );
}
