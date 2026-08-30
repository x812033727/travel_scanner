import { BadgeCheck, CalendarClock, CircleDollarSign, MapPin, Sparkles } from "lucide-react";
import { SearchWorkbench } from "@/components/search-workbench";
import { SiteHeader } from "@/components/site-header";
import { citiesForCountry, countries } from "@/lib/destinations";

export default function Home() {
  return (
    <><SiteHeader /><main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
      <section className="grid gap-8 pb-10 pt-8 lg:grid-cols-[.8fr_1.2fr] lg:items-center lg:py-14">
        <div className="lg:pr-6">
          <p className="mb-4 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />完整旅程決策工作台</p>
          <h1 className="max-w-2xl text-4xl font-bold leading-[1.12] tracking-[-.04em] md:text-6xl">少開十個分頁，<br />多看懂一趟旅行。</h1>
          <p className="mt-5 max-w-xl text-base leading-7 text-[var(--muted)] md:text-lg">先深耕日本、韓國與泰國，同時衡量機票、住宿、活動與接送，用每日行程看清楚時間、價格與便利性的交換。</p>
          <div className="mt-7 grid gap-3 text-sm sm:grid-cols-3 lg:grid-cols-1">
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><BadgeCheck size={18} className="text-[var(--teal)]" />每筆資料標明來源</p>
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><CalendarClock size={18} className="text-[var(--teal)]" />自動安排每日動線</p>
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><CircleDollarSign size={18} className="text-[var(--teal)]" />即時與估算費用分開</p>
          </div>
        </div>
        <SearchWorkbench />
      </section>
      <section aria-labelledby="asia-focus-title" className="rounded-[2rem] border border-[var(--line)] bg-white/70 p-6 md:p-8">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div><p className="text-sm font-semibold text-[var(--coral)]">目的地優先資料庫</p><h2 id="asia-focus-title" className="mt-1 text-2xl font-bold md:text-3xl">不是只換機場代碼，而是按城市安排</h2></div>
          <a href="#trip-search" className="rounded-full border border-[var(--teal)] px-4 py-2 text-sm font-semibold text-[var(--teal)]">回到搜尋條件</a>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-3">{countries.map((country) => {
          const cities = citiesForCountry(country.key);
          return <article key={country.key} className="rounded-3xl border border-[var(--line)] bg-white p-5"><p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><MapPin size={16} />{country.label}</p><h3 className="mt-2 text-xl font-bold">{cities.length} 個重點目的地</h3><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{country.caption}，內建建議住宿區域、當地時區與興趣行程。</p><div className="mt-4 flex flex-wrap gap-2">{cities.map((city) => <span key={city.id} className="rounded-full bg-[var(--paper)] px-2.5 py-1 text-xs">{city.name}</span>)}</div></article>;
        })}</div>
      </section>
    </main></>
  );
}
