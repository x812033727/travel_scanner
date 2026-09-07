"use client";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";
import { useCommunity } from "./provider";
import { Feed } from "./feed";
import { panelClass } from "./ui";
export function CommunityHero() {
  const t = useTranslations("community");
  const { flags } = useCommunity();
  if (!flags.enabled) return null;
  return <div className="mt-5 flex flex-wrap gap-3"><Link href="/community" className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-4 font-semibold text-white">{t("findInspiration")}</Link><Link href="/#trip-search" className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-4 font-semibold">{t("startPlanning")}</Link></div>;
}
export function CommunityHome({ pets = false }: { pets?: boolean }) {
  const t = useTranslations("community");
  const { flags } = useCommunity();
  if (!flags.enabled) return null;
  return <section className="my-10 space-y-5"><h2 className="text-2xl font-bold">{t(pets ? "pets" : "inspiration")}</h2><p className="text-[var(--muted)]">{t(pets ? "petIntroduction" : "communityIntroduction")}</p>{pets ? <Link className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-4 font-semibold text-white" href="/pet-friendly">{t("explorePets")}</Link> : <><Feed compact /><Link href="/community" className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{t("allStories")}</Link></>}</section>;
}
export function MyDirectory() {
  const t = useTranslations("community");
  const { user } = useHeaderSession();
  const { flags, me } = useCommunity();
  const visibility = useSiteVisibility();
  const links = [
    ...(featureVisible(visibility, "trips") ? [["/trips", "myTrips"]] : []),
    ...(flags.enabled ? [["/community/collections", "collections"], [me?.profile ? `/community/profiles/${me.profile.handle}` : "/community/settings", "profile"], ["/community/settings", "profileSettings"], ["/community/drafts", "drafts"], ["/community/messages", "messages"]] : []),
    ["/account", "accountSettings"],
    ...(user?.is_admin ? [["/admin", "admin"]] : []),
    ...(!user ? [["/login", "login"]] : []),
  ];
  return <nav aria-label={t("my")} className="mb-6 grid gap-4 sm:grid-cols-2">{links.map(([href, key]) => <Link key={key} href={href} className={`${panelClass} flex min-h-16 items-center font-semibold hover:border-[var(--teal)]`}>{t(key)}</Link>)}</nav>;
}
