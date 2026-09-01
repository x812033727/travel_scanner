import { AccountList } from "@/components/account-list";
import { LineConnectionPanel } from "@/components/line-connection-panel";
import { SiteHeader } from "@/components/site-header";
export default function AlertsPage() { return <><SiteHeader /><main className="mx-auto max-w-4xl px-5 py-12"><p className="text-sm font-semibold text-[var(--teal)]">PRICE WATCH</p><h1 className="mb-8 mt-2 text-4xl font-bold">價格通知</h1><LineConnectionPanel /><AccountList kind="alerts" /></main></>; }
