import { BadgeCheck, CalendarClock, CircleDollarSign, MapPin, Sparkles } from "lucide-react";
import { getTranslations } from "next-intl/server";
import { SearchWorkbench } from "@/components/search-workbench";
import { SiteHeader } from "@/components/site-header";
import { citiesForCountry, countries } from "@/lib/destinations";

export default async function Home() {
  const t = await getTranslations("search");
  return (
    <><SiteHeader /><main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
      <section className="grid gap-8 pb-10 pt-8 lg:grid-cols-[1fr_1.15fr] lg:items-center lg:py-14">
        <div className="lg:pr-4 xl:pr-8">
          <p className="mb-4 flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Sparkles size={16} />{t("heroEyebrow")}</p>
          <h1 className="max-w-2xl text-4xl font-bold leading-[1.12] tracking-[-.04em] md:text-5xl xl:text-[3.5rem]">{t("heroTitleLine1")}<br />{t("heroTitleLine2")}</h1>
          <p className="mt-5 max-w-xl text-base leading-7 text-[var(--muted)] md:text-lg">{t("heroDescription")}</p>
          <div className="mt-7 grid gap-3 text-sm sm:grid-cols-3 lg:grid-cols-1">
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><BadgeCheck size={18} className="text-[var(--teal)]" />{t("sourceBenefit")}</p>
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><CalendarClock size={18} className="text-[var(--teal)]" />{t("routeBenefit")}</p>
            <p className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"><CircleDollarSign size={18} className="text-[var(--teal)]" />{t("costBenefit")}</p>
          </div>
        </div>
        <SearchWorkbench />
      </section>
      <section aria-labelledby="asia-focus-title" className="rounded-[2rem] border border-[var(--line)] bg-white/70 p-6 md:p-8">
        <div className="flex flex-wrap items-end justify-between gap-4">
          <div><p className="text-sm font-semibold text-[var(--coral)]">{t("destinationEyebrow")}</p><h2 id="asia-focus-title" className="mt-1 text-2xl font-bold md:text-3xl">{t("destinationTitle")}</h2></div>
          <a href="#trip-search" className="rounded-full border border-[var(--teal)] px-4 py-2 text-sm font-semibold text-[var(--teal)]">{t("backToSearch")}</a>
        </div>
        <div className="mt-6 grid gap-4 md:grid-cols-3">{countries.map((country) => {
          const cities = citiesForCountry(country.key);
          return <article key={country.key} className="rounded-3xl border border-[var(--line)] bg-white p-5"><p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><MapPin size={16} />{country.label}</p><h3 className="mt-2 text-xl font-bold">{t("focusDestinations", { count: cities.length })}</h3><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{t("countryDescription", { caption: country.caption })}</p><div className="mt-4 flex flex-wrap gap-2">{cities.map((city) => <span key={city.id} className="rounded-full bg-[var(--paper)] px-2.5 py-1 text-xs">{city.name}</span>)}</div></article>;
        })}</div>
      </section>
    </main></>
  );
}
