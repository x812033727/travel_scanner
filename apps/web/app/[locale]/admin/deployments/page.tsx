import { AdminDeploymentsPanel } from "@/components/admin-deployments-panel";

export default function AdminDeploymentsPage() {
  return <main className="admin-page"><p className="text-sm font-semibold tracking-[.14em] text-[var(--teal)]">SYSTEM ADMIN</p><h1 className="mt-2 text-3xl font-bold md:text-4xl">部署中心</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">只部署已通過 CI 的最新 main；由受限主機代理執行備份、migration、健康檢查與應用程式回退。</p><AdminDeploymentsPanel /></main>;
}
