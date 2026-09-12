"use client";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { primaryNavLinks } from "@/lib/nav-links";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";
import { useCommunity } from "./provider";
import { panelClass } from "./ui";
export function TravelExplore() {
 const t = useTranslations("navigation");
 const tc = useTranslations("community");
 const visibility = useSiteVisibility();
 const { flags } = useCommunity();
 return <div className="grid gap-4 sm:grid-cols-2"><Link className={panelClass} href="/#trip-search">{tc("startPlanning")}</Link>{primaryNavLinks.filter((item) => item.key !== "life" && (!item.feature || featureVisible(visibility, item.feature))).map((item) => <Link className={panelClass} key={item.href} href={item.href}>{t(item.key)}</Link>)}{flags.enabled && <><Link className={panelClass} href="/community/search">{tc("searchCommunity")}</Link><Link className={panelClass} href="/pet-friendly">{tc("pets")}</Link></>}</div>;
}
