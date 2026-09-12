import { Compass, MapPinOff } from "lucide-react";
import { useTranslations } from "next-intl";
import { SiteHeader } from "@/components/site-header";
import { Link } from "@/i18n/navigation";

/**
 * error.tsx already keeps render failures off Next's own screen — English only on a
 * site that ships five languages, with no way back but the browser's buttons. A 404
 * does not go through an error boundary, so it fell through to exactly that screen.
 *
 * The exits are the three places someone who mistyped a URL actually wants: the home
 * page, the explore feed, and their own trips. The header is rendered here rather than
 * in the layout because that is where every other page in this app puts it; without it
 * a mistyped address loses the site navigation along with the route.
 */
export default function LocaleNotFound() {
  const t = useTranslations("errors");
  return (
    <>
      <SiteHeader />
      <main className="mx-auto flex min-h-[70vh] max-w-3xl flex-col items-center justify-center px-5 py-16 text-center md:px-8">
        <MapPinOff aria-hidden className="text-[var(--muted)]" size={44} />
        <h1 className="mt-5 text-3xl font-bold">{t("notFoundTitle")}</h1>
        <p className="mx-auto mt-3 max-w-xl leading-8 text-[var(--muted)]">{t("notFoundBody")}</p>
        <div className="mt-8 flex w-full flex-col gap-3 sm:w-auto sm:flex-row">
          <Link
            href="/"
            className="inline-flex min-h-12 items-center justify-center gap-2 rounded-2xl bg-[var(--teal-fill)] px-6 text-base font-semibold text-white"
          >
            <Compass aria-hidden size={19} />
            {t("backHome")}
          </Link>
          <Link
            href="/explore"
            className="inline-flex min-h-12 items-center justify-center rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-6 text-base font-semibold text-[var(--ink)]"
          >
            {t("notFoundExplore")}
          </Link>
          <Link
            href="/trips"
            className="inline-flex min-h-12 items-center justify-center rounded-2xl border border-[var(--line)] bg-[var(--surface)] px-6 text-base font-semibold text-[var(--ink)]"
          >
            {t("notFoundTrips")}
          </Link>
        </div>
      </main>
    </>
  );
}
