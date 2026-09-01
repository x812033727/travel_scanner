import { AccountList } from "@/components/account-list";
import { SiteHeader } from "@/components/site-header";
import { Plus } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { getTranslations } from "next-intl/server";

export default async function TripsPage() { const t = await getTranslations("trips"); return <><SiteHeader /><main className="mx-auto max-w-5xl px-5 py-12"><div className="mb-8 flex flex-wrap items-end justify-between gap-4"><div><p className="text-sm font-semibold text-[var(--teal)]">{t("savedEyebrow")}</p><h1 className="mt-2 text-4xl font-bold">{t("myTrips")}</h1><p className="mt-2 text-[var(--muted)]">{t("myTripsDescription")}</p></div><Link href="/trips/new" className="flex items-center gap-2 rounded-xl bg-[var(--teal)] px-4 py-3 text-sm font-semibold text-white"><Plus size={17} />{t("newTrip")}</Link></div><AccountList kind="trips" /></main></>; }
