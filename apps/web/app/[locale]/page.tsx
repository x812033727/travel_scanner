import {
  BadgeCheck,
  CalendarClock,
  CircleDollarSign,
  Compass,
  MapPin,
  Route,
  Soup,
  Sparkles,
} from "lucide-react";
import { getTranslations } from "next-intl/server";
import { SearchWorkbench } from "@/components/search-workbench";
import { SiteHeader } from "@/components/site-header";
import { Link } from "@/i18n/navigation";
import { citiesForCountry, countryKeys } from "@/lib/destinations";

export default async function Home() {
  const t = await getTranslations("search");
  const tc = await getTranslations("search.catalog");
  const benefits = [
    { key: "source", icon: BadgeCheck, text: t("sourceBenefit") },
    { key: "route", icon: CalendarClock, text: t("routeBenefit") },
    { key: "cost", icon: CircleDollarSign, text: t("costBenefit") },
  ];
  return (
    <>
      <SiteHeader />
      <main className="mx-auto min-h-screen max-w-6xl px-5 pb-20 md:px-8">
        {/* On a phone the first screen is the request form: a short hero, the
            workbench, and the three trust lines as one scrolling row underneath.
            On desktop the lines keep their place beside the form. */}
        <section className="grid gap-6 pb-6 pt-5 lg:grid-cols-[1fr_1.15fr] lg:items-center lg:gap-8 lg:py-14">
          <div className="lg:pr-4 xl:pr-8">
            <p className="mb-3 flex items-center gap-2 text-sm font-semibold text-[var(--teal)] lg:mb-4">
              <Sparkles size={16} />
              {t("heroEyebrow")}
            </p>
            <h1 className="max-w-2xl text-3xl font-bold leading-[1.12] tracking-[-.04em] md:text-5xl xl:text-[3.5rem]">
              {t("heroTitleLine1")}
              <br />
              {t("heroTitleLine2")}
            </h1>
            <p className="mt-4 max-w-xl text-base leading-7 text-[var(--muted)] md:text-lg lg:mt-5">
              {t("heroDescription")}
            </p>
            <div className="mt-7 hidden gap-3 text-sm lg:grid lg:grid-cols-1">
              {benefits.map(({ key, icon: Icon, text }) => (
                <p
                  key={key}
                  className="flex items-center gap-3 rounded-2xl border border-[var(--line)] bg-white/70 px-4 py-3"
                >
                  <Icon size={18} className="text-[var(--teal)]" />
                  {text}
                </p>
              ))}
            </div>
          </div>
          <SearchWorkbench />
          {/* These used to be one scrolling row, which cut the third line off
              mid-word at 390px with nothing to say it could be scrolled. Three short
              lines stacked instead: they sit below the workbench on a phone, so the
              height costs nothing on the first screen. */}
          <div className="min-w-0 lg:hidden">
            <ul className="grid gap-2">
              {benefits.map(({ key, icon: Icon, text }) => (
                <li
                  key={key}
                  className="flex items-center gap-2.5 rounded-2xl border border-[var(--line)] bg-white/70 px-3.5 py-2.5 text-sm font-medium leading-6"
                >
                  <Icon size={17} className="shrink-0 text-[var(--teal)]" />
                  {text}
                </li>
              ))}
            </ul>
          </div>
        </section>
        <section aria-labelledby="quick-actions-title" className="pb-8">
          <div className="mb-4 flex items-end justify-between gap-4">
            <div>
              <p className="text-sm font-semibold text-[var(--teal)]">
                {t("quickActionsEyebrow")}
              </p>
              <h2 id="quick-actions-title" className="mt-1 text-2xl font-bold">
                {t("quickActionsTitle")}
              </h2>
            </div>
          </div>
          <div className="app-quick-grid">
            <Link href="/hotspots" className="app-quick-card">
              <span className="app-quick-icon bg-emerald-50 text-emerald-800">
                <Compass size={22} />
              </span>
              <span>
                <strong>{t("quickHotspots")}</strong>
                <small>{t("quickHotspotsDescription")}</small>
              </span>
            </Link>
            <Link href="/foods" className="app-quick-card">
              <span className="app-quick-icon bg-orange-50 text-orange-800">
                <Soup size={22} />
              </span>
              <span>
                <strong>{t("quickFoods")}</strong>
                <small>{t("quickFoodsDescription")}</small>
              </span>
            </Link>
            <Link href="/trips" className="app-quick-card">
              <span className="app-quick-icon bg-sky-50 text-sky-800">
                <Route size={22} />
              </span>
              <span>
                <strong>{t("quickTrips")}</strong>
                <small>{t("quickTripsDescription")}</small>
              </span>
            </Link>
          </div>
        </section>
        <section
          aria-labelledby="asia-focus-title"
          className="rounded-[2rem] border border-[var(--line)] bg-white/70 p-6 md:p-8"
        >
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <p className="text-sm font-semibold text-[var(--coral)]">
                {t("destinationEyebrow")}
              </p>
              <h2
                id="asia-focus-title"
                className="mt-1 text-2xl font-bold md:text-3xl"
              >
                {t("destinationTitle")}
              </h2>
            </div>
            <a
              href="#trip-search"
              className="inline-flex min-h-11 items-center rounded-full border border-[var(--teal)] px-4 text-sm font-semibold text-[var(--teal)]"
            >
              {t("backToSearch")}
            </a>
          </div>
          <div className="destination-card-rail mt-6">
            {countryKeys.map((country) => {
              const cities = citiesForCountry(country, tc);
              return (
                <article key={country} className="destination-app-card">
                  <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]">
                    <MapPin size={16} />
                    {tc(`countries.${country}.name`)}
                  </p>
                  <h3 className="mt-2 text-xl font-bold">
                    {t("focusDestinations", { count: cities.length })}
                  </h3>
                  <p className="mt-2 text-sm leading-6 text-[var(--muted)]">
                    {t("countryDescription", { caption: tc(`countries.${country}.caption`) })}
                  </p>
                  <div className="mt-4 flex flex-wrap gap-2">
                    {cities.map((city) => (
                      <Link
                        key={city.id}
                        href={`/hotspots?destination_id=${city.id}`}
                        className="destination-city-chip"
                      >
                        {city.name}
                      </Link>
                    ))}
                  </div>
                </article>
              );
            })}
          </div>
        </section>
      </main>
    </>
  );
}
