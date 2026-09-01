import { Check, History, ShieldCheck } from "lucide-react";
import Link from "next/link";
import { SiteHeader } from "@/components/site-header";
import { getRegistrationAvailability } from "@/lib/registration";

const packages = [
  { name: "輕量包", uses: 10, price: "NT$199", perUse: "每次約 NT$20" },
  { name: "常用包", uses: 30, price: "NT$499", perUse: "每次約 NT$17", featured: true },
  { name: "大量包", uses: 100, price: "NT$1,299", perUse: "每次約 NT$13" },
];

export default async function PricingPage() {
  const registration = await getRegistrationAvailability();
  return <><SiteHeader /><main className="mx-auto max-w-6xl px-5 py-14">
    <div className="mx-auto max-w-3xl text-center">
      <p className="text-sm font-semibold text-[var(--teal)]">買多少、用多少</p>
      <h1 className="mt-2 text-4xl font-bold md:text-5xl">不綁月租的旅遊查價次數</h1>
      <p className="mt-4 leading-7 text-[var(--muted)]">註冊先送 3 次。每次正式查價成功取得可用結果才扣 1 次，失敗不扣；未用完的次數永久保留。</p>
      {registration === "open" ? <Link href="/register" className="mt-7 inline-flex rounded-xl bg-[var(--teal)] px-6 py-3.5 font-semibold text-white">免費取得 3 次</Link> : <p className="mt-7 inline-flex rounded-xl bg-[#e4ebe6] px-6 py-3.5 font-semibold text-[var(--muted)]">{registration === "closed" ? "目前暫停開放註冊" : "暫時無法確認註冊狀態"}</p>}
    </div>

    <section aria-label="次數包" className="mt-12 grid gap-5 md:grid-cols-3">
      {packages.map((item) => <article key={item.uses} className={`relative rounded-[2rem] border bg-white p-7 ${item.featured ? "border-[var(--teal)] shadow-[0_20px_60px_rgba(13,107,104,.14)]" : "border-[var(--line)]"}`}>
        {item.featured && <span className="absolute right-6 top-6 rounded-full bg-[var(--teal-soft)] px-3 py-1 text-xs font-semibold text-[var(--teal-dark)]">最受歡迎</span>}
        <p className="font-semibold text-[var(--teal)]">{item.name}</p>
        <h2 className="mt-3 text-4xl font-bold">{item.uses}<span className="ml-1 text-base font-normal text-[var(--muted)]">次</span></h2>
        <p className="mt-5 text-2xl font-bold">{item.price}</p>
        <p className="mt-1 text-sm text-[var(--muted)]">{item.perUse} · 一次買斷</p>
        <ul className="my-7 space-y-3 text-sm">
          {["所有查價功能皆可使用", "次數永久有效並可累加", "會員專區逐筆留存紀錄"].map((label) => <li key={label} className="flex gap-2"><Check size={18} className="shrink-0 text-[var(--teal)]" />{label}</li>)}
        </ul>
        <button disabled className="w-full rounded-xl bg-[#e4ebe6] p-3 font-semibold text-[var(--muted)]">購買即將開放</button>
      </article>)}
    </section>

    <section className="mt-8 grid gap-4 rounded-[2rem] border border-[var(--line)] bg-white p-6 md:grid-cols-3 md:p-8">
      <p className="flex gap-3"><ShieldCheck className="shrink-0 text-[var(--teal)]" /><span><strong className="block">成功才扣次</strong><span className="mt-1 block text-sm text-[var(--muted)]">沒有可用結果會自動釋放保留次數。</span></span></p>
      <p className="flex gap-3"><History className="shrink-0 text-[var(--teal)]" /><span><strong className="block">逐筆可查</strong><span className="mt-1 block text-sm text-[var(--muted)]">時間、摘要、餘額與流水號都會保留。</span></span></p>
      <p className="flex gap-3"><Check className="shrink-0 text-[var(--teal)]" /><span><strong className="block">功能一致</strong><span className="mt-1 block text-sm text-[var(--muted)]">所有會員都能使用完整功能。</span></span></p>
    </section>
  </main></>;
}
