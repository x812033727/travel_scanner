"use client";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";
import { useCommunity } from "./provider";
import { Feed } from "./feed";
import { panelClass } from "./ui";
import { useDiscoveryStatus } from "@/lib/discovery";
import { frontendCopy } from "@/lib/frontend-navigation";
import { primaryNavLinks } from "@/lib/nav-links";
import { PaletteSwitcher } from "@/components/palette-switcher";
import { TextSizeSwitcher } from "@/components/text-size-switcher";
import { ThemeSwitcher } from "@/components/theme-switcher";
export function CommunityHero() {
  const t = useTranslations("community");
  const { flags } = useCommunity();
  if (!flags.enabled) return null;
  return <div className="mt-5 flex flex-wrap gap-3"><Link href="/community" className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-4 font-semibold text-white">{t("findInspiration")}</Link><Link href="/#trip-search" className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-4 font-semibold">{t("startPlanning")}</Link></div>;
}
export function CommunityHome({ pets = false }: { pets?: boolean }) {
  const t = useTranslations("community");
  const { user } = useHeaderSession();
  const { flags } = useCommunity();
  if (!flags.enabled) return null;
  return <section className="my-10 space-y-5"><h2 className="text-2xl font-bold">{t(pets ? "pets" : "inspiration")}</h2><p className="text-[var(--muted)]">{t(pets ? "petIntroduction" : "communityIntroduction")}</p>{pets ? <Link className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-4 font-semibold text-white" href="/pet-friendly">{t("explorePets")}</Link> : <><Feed key={user?.id || "guest"} compact /><Link href="/community" className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{t("allStories")}</Link></>}</section>;
}
export function MyDirectory() {
  const t = useTranslations("community");
  const nav = useTranslations("navigation");
  const copy = frontendCopy(useLocale());
  const { user, logout } = useHeaderSession();
  const { flags, me } = useCommunity();
  const discovery = useDiscoveryStatus();
  const visibility = useSiteVisibility();
  const links = [
    ...(discovery.enabled ? [["/explore/collections", "collections"]] : []),
    ...(featureVisible(visibility, "trips") ? [["/trips", "myTrips"]] : []),
    ...(flags.enabled && flags.posting_enabled ? [["/community/new", "publish"]] : []),
    ...(flags.enabled ? [...(!discovery.enabled ? [["/community/collections", "collections"]] : []), [me?.profile ? `/community/profiles/${me.profile.handle}` : "/community/settings", "profile"], ["/community/settings", "profileSettings"], ["/community/drafts", "drafts"], ["/community/messages", "messages"]] : []),
    ["/account", "accountSettings"],
    ...(user?.is_admin ? [["/admin", "admin"]] : []),
    ...(!user ? [["/login", "login"]] : []),
  ];
  return <div className="space-y-8"><nav aria-label={t("my")} className="mb-6 grid gap-4 sm:grid-cols-2">{links.map(([href, key]) => <Link key={key} href={href} className={`${panelClass} flex min-h-16 items-center font-semibold hover:border-[var(--teal)]`}>{t(key)}</Link>)}</nav>
    {discovery.enabled && <>
      <section className={panelClass}><h2 className="mb-4 text-lg font-bold">{copy.tools}</h2><nav aria-label={copy.tools} className="grid gap-2 sm:grid-cols-2"><Link href="/search/new" className="min-h-12 rounded-xl px-3 py-3 font-semibold text-[var(--teal)]">{copy.search}</Link>{primaryNavLinks.filter((item) => item.key !== "trips" && (!item.feature || featureVisible(visibility, item.feature))).map((item) => <Link key={item.key} href={item.href} className="min-h-12 rounded-xl px-3 py-3 hover:bg-[var(--paper)]">{nav(item.key)}</Link>)}</nav></section>
      {user && <button type="button" onClick={() => void logout()} className="min-h-11 rounded-xl border border-[var(--line)] px-5">{copy.logout}</button>}
    </>}
    <section className={panelClass}><h2 className="mb-4 text-lg font-bold">{copy.display}</h2><div className="grid gap-5"><TextSizeSwitcher variant="expanded" /><div className="flex min-h-12 items-center justify-between"><span>{nav("themeLabel")}</span><ThemeSwitcher /></div><PaletteSwitcher /></div></section>
  </div>;
}
