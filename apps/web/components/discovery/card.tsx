"use client";
import { useState, type ReactNode } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useSearchParams } from "next/navigation";
import { BookOpen, Compass, MapPin, Play, Route, Soup, Store, Hotel, ArrowUpRight } from "lucide-react";
import { Link, usePathname } from "@/i18n/navigation";
import { useCommunity } from "@/components/community/provider";
import { ItineraryPreview } from "@/components/community/post";
import { Button, CommunityImage } from "@/components/community/ui";
import { TravelPlanAction } from "@/components/travel-card-actions";
import { BookingPanel, SourceCredits } from "@/components/travel-services/booking-panel";
import type { Product } from "@/components/travel-services/catalog";
import { getDiscoveryCopy, getDiscoveryFeedback, getRecommendationReason } from "@/lib/discovery-copy";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import { useDiscoveryResource, type DiscoveryItem, type DiscoveryPlace } from "@/lib/discovery";
import { safeExternalHref, safeNextPath } from "@/lib/navigation";
import { DiscoveryVideoPlayer } from "./video";
import { SavedContentAction } from "./saved-content-action";
import { useDiscoveryDetailNavigation } from "./detail-drawer";
import styles from "./discovery.module.css";

const icons = { hotspot: Compass, food: Soup, merchant: Store, hotel: Hotel, article: BookOpen, video: Play, post: BookOpen, itinerary: Route };
export function discoveryDetailHref(item: Pick<DiscoveryItem, "kind" | "id">, returnTo: string) {
  const url = new URL(safeNextPath(returnTo, "/explore"), "https://local.invalid");
  url.searchParams.set("content", `${item.kind}:${item.id.split(":").at(-1)}`);
  return `${url.pathname}${url.search}${url.hash}`;
}
export function DiscoveryCard({ item, onDismiss }: { item: DiscoveryItem; onDismiss?: (item: DiscoveryItem) => void }) {
  const locale = useLocale(); const c = getDiscoveryCopy(locale);
  const { flags } = useCommunity();
  const pathname = usePathname(); const params = useSearchParams();
  const navigation = useDiscoveryDetailNavigation();
  const returnTo = `${pathname}${params.size ? `?${params}` : ""}`;
  const href = discoveryDetailHref(item, returnTo);
  const Icon = icons[item.kind] || Compass;
  const thumbnail = safeExternalHref(item.thumbnail_url, ["https:"]);
  const cover = item.content?.media?.[0];
  if ((item.kind === "post" || item.kind === "itinerary" || item.source.kind === "community") && !flags.enabled) return null;
  return <article id={item.id} className={styles.card}>
    <Link href={href} scroll={false} aria-label={`${c.details}: ${item.title}`} onClick={(event) => navigation?.remember(event.currentTarget, href)}>{cover ? <div className={styles.cover}><CommunityImage id={cover.id} alt={cover.alt || item.title} thumbnail /></div> : thumbnail ? <div className={styles.cover}>
      {/* Source-authorized images only. Missing images stay honest type tiles. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={thumbnail} alt={item.title} loading="lazy" decoding="async" referrerPolicy="no-referrer" />
    </div> : <div className={styles.fallback}><Icon size={24} aria-hidden /><span>{c.kinds[item.kind]}</span></div>}</Link>
    <div className={styles.cardBody}>
      <p className={styles.cardMeta}>{item.destination && <><MapPin size={13} aria-hidden />{item.destination.name}<span>·</span></>}{c.kinds[item.kind]}</p>
      <h3 className={styles.cardTitle}><Link href={href} scroll={false} onClick={(event) => navigation?.remember(event.currentTarget, href)}>{item.title}</Link></h3>
      <p className={styles.cardSummary}>{item.summary}</p>
      <p className={styles.cardMeta}>{c.sourceKinds[item.source.kind]} · {item.author?.display_name || item.source.label}{item.published_at && <> · <time dateTime={item.published_at}>{new Date(item.published_at).toLocaleDateString(locale)}</time></>}</p>
      {item.recommendation_reason && <p className={styles.reason}><span className="sr-only">{c.reason}: </span>{getRecommendationReason(locale, item.recommendation_reason)}</p>}
      <div className={styles.cardFooter}><SavedContentAction item={item} returnTo={returnTo} compact resumeEnabled={!params.has("content")} /><TravelPlanAction item={item} returnTo={returnTo} compact resumeEnabled={!params.has("content")} /></div>
      {onDismiss && <button type="button" onClick={() => onDismiss(item)} className="min-h-11 self-start rounded-lg text-xs text-[var(--muted)] underline underline-offset-4 focus-visible:outline focus-visible:outline-2">{c.dismiss}</button>}
    </div>
  </article>;
}
export function DiscoveryDetails({ kind, id, returnTo = "/explore" }: { kind: string; id: string; returnTo?: string }) {
  const locale = useLocale(); const c = getDiscoveryCopy(locale); const f = getFrontendFlowCopy(locale);
  const result = useDiscoveryResource<DiscoveryItem>(`/discovery/content/${encodeURIComponent(kind)}/${encodeURIComponent(id)}`);
  if (result.error) return <div role="alert" className={styles.detailBody}><p>{c.unavailable}</p><Button secondary onClick={result.reload}>{c.retry}</Button></div>;
  if (!result.data) return <div role="status" className={styles.detailBody}><p>{c.loading}</p><div className={`${styles.skeleton} ${styles.skeletonImage}`} /></div>;
  const item = result.data;
  const source = safeExternalHref(item.source.url, ["https:"]);
  const videos = [...new Map([...(item.video ? [item.video] : []), ...(item.content?.video_refs || [])].map((video) => [video.video_id, video])).values()];
  const detail = item.detail;
  return <><div className={styles.detailBody}>
      <h2 className="mb-3 text-2xl font-bold">{item.title}</h2>
      {item.destination && <p className="mb-4 text-sm text-[var(--teal)]">{item.destination.name}</p>}
      {videos.map((video) => <DiscoveryVideoPlayer key={video.video_id} video={video} />)}
      {item.content?.media?.map((media) => <CommunityImage key={media.id} id={media.id} alt={media.alt || item.title} />)}
      <section className={styles.detailSection}><h3 className="sr-only">{f.overview}</h3><p className="whitespace-pre-wrap break-words leading-8">{detail?.intro?.body || item.content?.text || item.summary || f.noDetails}</p></section>
      {detail?.place && <PlaceFacts place={detail.place} />}
      {detail?.merchants?.length ? <section className={styles.detailSection}><h3 className="mb-3 font-bold">{f.nearbyFood}</h3><ul className="space-y-3">{detail.merchants.map((merchant) => <li key={merchant.id}><Link href={discoveryDetailHref({ kind: "merchant", id: merchant.id }, returnTo)} scroll={false} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{merchant.name}</Link><p className="text-sm text-[var(--muted)]">{merchant.address}</p></li>)}</ul></section> : null}
      {detail?.guides?.length ? <section className={styles.detailSection}><h3 className="mb-3 font-bold">{f.relatedGuides}</h3>{detail.guides.map((guide) => <Link key={guide.id} href={discoveryDetailHref(guide, returnTo)} scroll={false} className="flex min-h-11 items-center text-[var(--teal)] underline">{guide.title}</Link>)}</section> : null}
      {detail?.hotel && <HotelDetails product={detail.hotel} />}
      {item.content?.itinerary && <ItineraryPreview itinerary={item.content.itinerary} />}
      <section className={styles.detailSection}><h3 className="mb-3 font-bold">{f.sources}</h3><p className="text-sm leading-6 text-[var(--muted)]">{c.sourceKinds[item.source.kind]} · {item.author?.display_name || item.source.label}<br />{c.originalLanguage}: {item.locale} · {item.published_at ? <time dateTime={item.published_at}>{new Date(item.published_at).toLocaleDateString(locale)}</time> : c.undated}{item.updated_at && <><br />{getDiscoveryFeedback(locale).updated}: <time dateTime={item.updated_at}>{new Date(item.updated_at).toLocaleString(locale)}</time></>}</p>
        {item.author?.handle && <Link href={`/community/profiles/${encodeURIComponent(item.author.handle)}`} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{item.author.display_name}</Link>}
        {source && <ExternalLink href={source}>{c.source}</ExternalLink>}
        {item.href && !item.href.includes("/explore?content=") && <Link href={safeNextPath(item.href, "/explore").replace(/^\/(?:zh-TW|zh-CN|en|ja|ko)(?=\/)/, "")} className="flex min-h-11 items-center text-[var(--teal)] underline">{c.details}</Link>}
      </section>
    </div><footer className={styles.detailFooter}><SavedContentAction item={item} returnTo={returnTo} /><TravelPlanAction item={item} returnTo={returnTo} /></footer></>;
}
function HotelDetails({ product }: { product: Product }) {
  const t = useTranslations("travelServices"); const [open, setOpen] = useState(false);
  return <section className={styles.detailSection}><p className="font-semibold">{product.title}</p>{product.facts?.facilities?.length ? <p className="my-3 text-sm text-[var(--muted)]">{product.facts.facilities.join(" · ")}</p> : null}<Button secondary onClick={() => setOpen(true)}>{t("platforms")}</Button><SourceCredits credits={product.facts?.source_credits} />{open && <BookingPanel product={product} placement="discovery" onClose={() => setOpen(false)} />}</section>;
}
function ExternalLink({ href, children }: { href?: string | null; children: ReactNode }) {
  const safe = safeExternalHref(href, ["https:", "http:"]);
  return safe ? <a href={safe} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-2 pr-4 text-sm font-semibold text-[var(--teal)] underline">{children}<ArrowUpRight size={15} aria-hidden /></a> : null;
}
function PlaceFacts({ place }: { place: DiscoveryPlace }) {
  const locale = useLocale(); const f = getFrontendFlowCopy(locale); const [copied, setCopied] = useState(false);
  const coords = place.coordinates;
  const validCoordinates = Number.isFinite(coords?.latitude) && Number.isFinite(coords?.longitude);
  return <section className={styles.detailSection}>
    {place.status === "stale" && <p role="status" className="mb-4 text-sm text-[var(--muted)]">{f.stale}</p>}
    {place.address && <><h3 className="font-semibold">{f.address}</h3><p className="mb-3 leading-7">{place.address}</p></>}
    {place.opening_hours?.weekday_descriptions?.length ? <><h3 className="font-semibold">{f.hours}</h3><ul className="mb-3 text-sm leading-7">{place.opening_hours.weekday_descriptions.map((line) => <li key={line}>{line}</li>)}</ul></> : null}
    <ExternalLink href={place.google_maps_url}>{f.map}</ExternalLink><ExternalLink href={place.official_website_url}>{f.officialSite}</ExternalLink>
    {validCoordinates && <div className="mt-3"><p className="text-sm">{f.coordinates}: {coords!.latitude}, {coords!.longitude}</p><Button secondary onClick={() => { void navigator.clipboard?.writeText(`${coords!.latitude}, ${coords!.longitude}`).then(() => setCopied(true)).catch(() => setCopied(false)); }}>{copied ? f.copied : f.copy}</Button></div>}
    {(place.fetched_at || place.updated_at) && <p className="mt-3 text-xs text-[var(--muted)]">{getDiscoveryFeedback(locale).updated}: {new Date(place.fetched_at || place.updated_at!).toLocaleString(locale)}{place.data_locale && ` · ${place.data_locale}`}</p>}
    {place.attribution?.provider && <div className="mt-3 text-xs"><ExternalLink href={place.attribution.provider_url}>{place.attribution.provider}</ExternalLink>{place.attribution.third_party?.map((source, index) => <span key={`${source.provider}:${index}`}>{safeExternalHref(source.providerUri) ? <ExternalLink href={source.providerUri}>{source.provider}</ExternalLink> : source.provider}</span>)}</div>}
  </section>;
}
