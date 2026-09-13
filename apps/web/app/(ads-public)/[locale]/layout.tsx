import { headers } from "next/headers";
import { redirect } from "next/navigation";
import OriginalLocaleLayout from "@/app/[locale]/layout";
import { getAdsenseSlot } from "@/lib/adsense.server";

export { generateMetadata, generateStaticParams } from "@/app/[locale]/layout";

/**
 * A second document root for the two article routes, and nothing else.
 *
 * Why a root layout rather than just rendering the tag inside the existing one: removing a
 * React `<Script>` cannot retract the observers and timers a vendor has already started
 * (`docs/stay22-module-switch.md:41-62`). Next.js performs a complete document navigation
 * across a root-layout boundary, so a reader who finishes an article and opens their account
 * or a trip gets a new document, and the ad runtime is discarded with the old one.
 *
 * This is a DOM lifetime boundary, NOT a separate origin or cookie sandbox.
 *
 * With advertising off — the default, and every request from a DNT/GPC browser — this calls
 * the ordinary layout with no arguments of its own, so the page is byte-for-byte what it is
 * today. The boundary still costs a full document load on hub → article navigation either
 * way, which is the price of being able to switch advertising on without moving routes.
 */
export default async function AdsPublicLayout({ children, params }: {
  children: React.ReactNode; params: Promise<{ locale: string }>;
}) {
  const ads = await getAdsenseSlot();
  if (!ads.enabled) return OriginalLocaleLayout({ children, params });
  const requestPath = (await headers()).get("x-travel-pathname") || "";
  // Third-party code can read location.href for itself, so a clean article URL is the only
  // way to keep a reader's search terms or campaign tags out of the ad document.
  if (requestPath.includes("?")) redirect(requestPath.split("?")[0]);
  return OriginalLocaleLayout({ children, params, ads });
}
