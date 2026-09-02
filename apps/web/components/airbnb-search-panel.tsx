import { CalendarDays, ExternalLink, House, ReceiptText, ShieldCheck, Users } from "lucide-react";

export type AirbnbSearchCriteria = {
  location: string;
  checkIn: string;
  checkOut: string;
  adults: number;
  children: number;
};

export function buildAirbnbSearchUrl(criteria: AirbnbSearchCriteria) {
  const location = criteria.location.trim() || "日本";
  const url = new URL(`https://www.airbnb.com/s/${encodeURIComponent(location)}/homes`);
  url.searchParams.set("checkin", criteria.checkIn);
  url.searchParams.set("checkout", criteria.checkOut);
  url.searchParams.set("adults", String(Math.max(1, criteria.adults)));
  if (criteria.children > 0) url.searchParams.set("children", String(criteria.children));
  return url.toString();
}

export function AirbnbSearchPanel({ criteria, compact = false }: { criteria: AirbnbSearchCriteria; compact?: boolean }) {
  const searchUrl = buildAirbnbSearchUrl(criteria);

  if (compact) {
    return (
      <a
        href={searchUrl}
        target="_blank"
        rel="noopener noreferrer nofollow"
        className="flex items-center justify-center gap-2 rounded-2xl border border-[var(--teal)] bg-white px-5 py-3.5 font-semibold text-[var(--teal)] transition hover:bg-[var(--teal-soft)]"
      >
        <House size={18} />Airbnb 官方外站搜尋<ExternalLink size={16} />
      </a>
    );
  }

  return (
    <article className="overflow-hidden rounded-[1.75rem] border border-[var(--line)] bg-white shadow-[var(--shadow-lg)]">
      <div className="bg-gradient-to-br from-[var(--teal-soft)] via-white to-[var(--coral-soft)] p-6 md:p-8">
        <div className="flex flex-wrap items-start justify-between gap-5">
          <div className="max-w-2xl">
            <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><House size={18} />Airbnb 官方外站搜尋</p>
            <h2 className="mt-2 text-2xl font-bold">用相同條件查看民宿與整套房源</h2>
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
              Mokaair 只協助帶入搜尋條件，不擷取 Airbnb 報價。請在 Airbnb 確認即時庫存、完整總價與退訂規則。
            </p>
          </div>
          <a
            href={searchUrl}
            target="_blank"
            rel="noopener noreferrer nofollow"
            className="flex shrink-0 items-center gap-2 rounded-2xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white transition hover:bg-[var(--teal-dark)]"
          >
            前往 Airbnb 搜尋<ExternalLink size={17} />
          </a>
        </div>

        <dl className="mt-6 grid gap-3 text-sm sm:grid-cols-3">
          <div className="rounded-2xl bg-white/80 p-4"><dt className="flex items-center gap-2 font-semibold"><House size={16} />目的地</dt><dd className="mt-1 text-[var(--muted)]">{criteria.location}</dd></div>
          <div className="rounded-2xl bg-white/80 p-4"><dt className="flex items-center gap-2 font-semibold"><CalendarDays size={16} />入住日期</dt><dd className="mt-1 text-[var(--muted)]">{criteria.checkIn} → {criteria.checkOut}</dd></div>
          <div className="rounded-2xl bg-white/80 p-4"><dt className="flex items-center gap-2 font-semibold"><Users size={16} />旅客</dt><dd className="mt-1 text-[var(--muted)]">{criteria.adults} 位成人{criteria.children ? `、${criteria.children} 位兒童` : ""}</dd></div>
        </dl>
      </div>

      <div className="grid gap-4 p-6 text-sm md:grid-cols-2 md:p-8">
        <p className="flex items-start gap-3 rounded-2xl bg-[var(--paper)] p-4 leading-6"><ReceiptText className="mt-0.5 shrink-0 text-[var(--coral)]" size={19} /><span><strong>比較完整總價</strong><br /><span className="text-[var(--muted)]">清潔費、服務費與稅金可能在 Airbnb 結帳流程才完整顯示。</span></span></p>
        <p className="flex items-start gap-3 rounded-2xl bg-[var(--paper)] p-4 leading-6"><ShieldCheck className="mt-0.5 shrink-0 text-[var(--teal)]" size={19} /><span><strong>下訂前再次確認</strong><br /><span className="text-[var(--muted)]">查看房東評價、住宿守則、取消政策與精確位置；此入口不扣 Mokaair 搜尋次數。</span></span></p>
      </div>
    </article>
  );
}
