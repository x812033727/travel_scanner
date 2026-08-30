import { BadgeCheck, CalendarClock, CircleDollarSign, Sparkles } from "lucide-react";
import { SearchWorkbench } from "@/components/search-workbench";
import { SiteHeader } from "@/components/site-header";

export default function Home() {
  return (
    <><SiteHeader /><main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
      <section className="grid gap-8 pb-10 pt-8 lg:grid-cols-[.8fr_1.2fr] lg:items-center lg:py-14">
        <div className="lg:pr-6">
          <p className="mb-4 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />完整旅程決策工作台</p>
          <h1 className="max-w-2xl text-4xl font-bold leading-[1.12] tracking-[-.04em] md:text-6xl">少開十個分頁，<br />多看懂一趟旅行。</h1>
          <p className="mt-5 max-w-xl text-base leading-7 text-[var(--muted)] md:text-lg">同時衡量機票、住宿、活動與接送，用每日行程看清楚時間、價格與便利性的交換。</p>
          <div className="mt-7 grid gap-3 text-sm sm:grid-cols-3 lg:grid-cols-1">
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><BadgeCheck size={18} className="text-[var(--teal)]" />每筆資料標明來源</p>
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><CalendarClock size={18} className="text-[var(--teal)]" />自動安排每日動線</p>
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><CircleDollarSign size={18} className="text-[var(--teal)]" />即時與估算費用分開</p>
          </div>
        </div>
        <SearchWorkbench />
      </section>
    </main></>
  );
}
