import { headers } from "next/headers";
import OriginalLocaleLayout from "@/app/[locale]/layout";
import { AdsenseDocument } from "@/components/ads/adsense-loader";
import { getAdsenseSlot } from "@/lib/adsense.server";

export { generateMetadata, generateStaticParams } from "@/app/[locale]/layout";

const filterableTutorialHub = /^\/(?:en|ja|ko|zh-TW|zh-CN)\/life\/(?:codex-learning-hub|claude-code-tutorials)\/?$/;

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
  // Third-party code can read location.href for itself, so a URL carrying search terms or
  // campaign tags is served without the tag rather than redirected to its bare path, which
  // threw the tags away before analytics could read them. `adsenseRequestGate` has already
  // refused such a request; this repeats it where the tag is actually loaded.
  // The two tutorial directories write search terms and filters into the URL after
  // hydration, so they stay ad-free on a clean URL too: the vendor would still observe
  // later URL changes.
  if (requestPath.includes("?") || filterableTutorialHub.test(requestPath)) {
    return OriginalLocaleLayout({ children, params });
  }
  // The root layout is not rendered again on a client-side navigation, so whether this
  // document loaded the tag is decided here, once, for every article it will show.
  return OriginalLocaleLayout({ children: <AdsenseDocument>{children}</AdsenseDocument>, params, ads });
}
