import { PlaneTakeoff, Search, Sparkles } from "lucide-react";
import { SiteHeader } from "@/components/site-header";

export default function Home() {
  return (
    <><SiteHeader /><main className="mx-auto min-h-screen max-w-6xl px-5 md:px-8">
      <section className="grid gap-10 py-20 lg:grid-cols-[1fr_.9fr] lg:items-center">
        <div>
          <p className="mb-4 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />不只比價，更比較整趟旅行</p>
          <h1 className="max-w-2xl text-5xl font-bold leading-[1.12] tracking-[-.04em] md:text-7xl">把旅行說出來，<br />我們找出更好的走法。</h1>
          <p className="mt-6 max-w-xl text-lg leading-8 text-[var(--muted)]">一次衡量機票、住宿、交通、活動、時間與便利性，清楚看懂便宜方案究竟犧牲了什麼。</p>
        </div>
        <div><form action="/search" className="rounded-[2rem] border border-[var(--line)] bg-white p-7 shadow-[0_24px_80px_rgba(16,42,43,.12)]">
          <label htmlFor="trip" className="mb-3 block text-sm font-semibold">告訴我你想去哪裡，或直接描述旅行需求</label>
          <textarea id="trip" name="q" defaultValue="11 月兩個人從台北去日本 5 天，預算 6 萬，希望美食購物，不要紅眼航班。" className="h-36 w-full resize-none rounded-2xl border border-[var(--line)] bg-[#fbfcf9] p-4 leading-7 outline-none focus:border-[var(--teal)]" />
          <button className="mt-4 flex w-full items-center justify-center gap-2 rounded-2xl bg-[var(--teal)] px-5 py-4 font-semibold text-white transition hover:bg-[var(--teal-dark)]"><PlaneTakeoff size={19} />開始規劃完整旅程</button>
          <p className="mt-4 text-center text-xs text-[var(--muted)]">Mock MVP · 價格為展示資料，不代表即時報價</p>
        </form><details className="mt-4 rounded-2xl border border-[var(--line)] bg-white p-4"><summary className="flex cursor-pointer items-center gap-2 font-semibold"><Search size={17} />Advanced Search</summary><form action="/search" className="mt-4 grid gap-3 sm:grid-cols-2"><input name="q" aria-label="進階搜尋描述" defaultValue="兩個人從台北去東京 5 天，預算 6 萬，住宿至少 4 星" className="sm:col-span-2 rounded-xl border border-[var(--line)] p-3" /><button className="sm:col-span-2 rounded-xl border border-[var(--teal)] p-3 font-semibold text-[var(--teal)]">使用進階條件搜尋</button></form></details></div>
      </section>
    </main></>
  );
}
