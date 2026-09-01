import { AdminDeploymentsPanel } from "@/components/admin-deployments-panel";
import { AdminNav } from "@/components/admin-nav";
import { SiteHeader } from "@/components/site-header";

export default function AdminDeploymentsPage() {
  return <><SiteHeader /><main className="mx-auto max-w-7xl px-5 pb-16 pt-8 md:px-8"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-4xl font-bold">部署中心</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">只部署已通過 CI 的最新 main；由受限主機代理執行備份、migration、健康檢查與應用程式回退。</p><AdminNav current="deployments" /><AdminDeploymentsPanel /></main></>;
}
