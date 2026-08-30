import { AccountList } from "@/components/account-list";
import { SiteHeader } from "@/components/site-header";
export default function TripsPage() { return <><SiteHeader /><main className="mx-auto max-w-4xl px-5 py-12"><p className="text-sm font-semibold text-[var(--teal)]">SAVED TRIPS</p><h1 className="mb-8 mt-2 text-4xl font-bold">我的旅程</h1><AccountList kind="trips" /></main></>; }

