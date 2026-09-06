import { CalendarDays, ExternalLink, House, ReceiptText, ShieldCheck, Users } from "lucide-react";
import { useTranslations } from "next-intl";

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
  const t = useTranslations("search.airbnb");

  if (compact) {
    return (
      <a
        href={searchUrl}
        target="_blank"
        rel="noopener noreferrer nofollow"
        className="flex items-center justify-center gap-2 rounded-2xl border border-[var(--teal)] bg-white px-5 py-3.5 font-semibold text-[var(--teal)] transition hover:bg-[var(--teal-soft)]"
      >
        <House size={18} />{t("title")}<ExternalLink size={16} />
      </a>
    );
  }

  return (
    <article className="overflow-hidden rounded-[1.75rem] border border-[var(--line)] bg-white shadow-[var(--shadow-lg)]">
      <div className="bg-gradient-to-br from-[var(--teal-soft)] via-white to-[var(--coral-soft)] p-6 md:p-8">
        <div className="flex flex-wrap items-start justify-between gap-5">
          <div className="max-w-2xl">
            <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><House size={18} />{t("title")}</p>
            <h2 className="mt-2 text-2xl font-bold">{t("subtitle")}</h2>
            <p className="mt-3 text-sm leading-6 text-[var(--muted)]">
              {t("disclaimer")}
            </p>
          </div>
          <a
            href={searchUrl}
            target="_blank"
            rel="noopener noreferrer nofollow"
            className="flex shrink-0 items-center gap-2 rounded-2xl bg-[var(--teal)] px-5 py-3.5 font-semibold text-white transition hover:bg-[var(--teal-dark)]"
          >
            {t("open")}<ExternalLink size={17} />
          </a>
        </div>

        <dl className="mt-6 grid gap-3 text-sm sm:grid-cols-3">
          <div className="rounded-2xl bg-white/80 p-4"><dt className="flex items-center gap-2 font-semibold"><House size={16} />{t("destination")}</dt><dd className="mt-1 text-[var(--muted)]">{criteria.location}</dd></div>
          <div className="rounded-2xl bg-white/80 p-4"><dt className="flex items-center gap-2 font-semibold"><CalendarDays size={16} />{t("dates")}</dt><dd className="mt-1 text-[var(--muted)]">{criteria.checkIn} → {criteria.checkOut}</dd></div>
          <div className="rounded-2xl bg-white/80 p-4"><dt className="flex items-center gap-2 font-semibold"><Users size={16} />{t("travelers")}</dt><dd className="mt-1 text-[var(--muted)]">{t("adults", { count: criteria.adults })}{criteria.children ? t("children", { count: criteria.children }) : ""}</dd></div>
        </dl>
      </div>

      <div className="grid gap-4 p-6 text-sm md:grid-cols-2 md:p-8">
        <p className="flex items-start gap-3 rounded-2xl bg-[var(--paper)] p-4 leading-6"><ReceiptText className="mt-0.5 shrink-0 text-[var(--coral)]" size={19} /><span><strong>{t("totalTitle")}</strong><br /><span className="text-[var(--muted)]">{t("totalBody")}</span></span></p>
        <p className="flex items-start gap-3 rounded-2xl bg-[var(--paper)] p-4 leading-6"><ShieldCheck className="mt-0.5 shrink-0 text-[var(--teal)]" size={19} /><span><strong>{t("confirmTitle")}</strong><br /><span className="text-[var(--muted)]">{t("confirmBody")}</span></span></p>
      </div>
    </article>
  );
}
