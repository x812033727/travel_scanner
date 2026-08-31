import { AccountList } from "@/components/account-list";
import { SiteHeader } from "@/components/site-header";
import { Plus } from "lucide-react";
import Link from "next/link";

export default function TripsPage() { return <><SiteHeader /><main className="mx-auto max-w-5xl px-5 py-12"><div className="mb-8 flex flex-wrap items-end justify-between gap-4"><div><p className="text-sm font-semibold text-[var(--teal)]">SAVED TRIPS</p><h1 className="mt-2 text-4xl font-bold">我的旅程</h1><p className="mt-2 text-[var(--muted)]">從空白開始規劃，或承接查價結果繼續安排每天動線。</p></div><Link href="/trips/new" className="flex items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white"><Plus size={17} />建立新行程</Link></div><AccountList kind="trips" /></main></>; }

