"use client";
import { useState, type MouseEvent, type ReactNode } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useSearchParams } from "next/navigation";
import { MapPin, ArrowUpRight, Bookmark } from "lucide-react";
import { Link, usePathname } from "@/i18n/navigation";
import { useCommunity } from "@/components/community/provider";
import { ItineraryPreview } from "@/components/community/post";
import { Button, CommunityImage } from "@/components/community/ui";
import { TravelPlanAction } from "@/components/travel-card-actions";
import { MerchantExternalLinks } from "@/components/merchant-external-links";
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

export function discoveryDetailHref(item: Pick<DiscoveryItem, "kind" | "id">, returnTo: string) {
  const url = new URL(safeNextPath(returnTo, "/explore"), "https://local.invalid");
  url.searchParams.set("content", `${item.kind}:${item.id.split(":").at(-1)}`);
  return `${url.pathname}${url.search}${url.hash}`;
}
function SavedCount({ item }: { item: Pick<DiscoveryItem, "saved_count"> }) {
  // Catalogued in messages/, not lib/discovery-copy.ts: check-i18n rejects new display
  // text there. The community `saves` message already reads a count in all five locales.
  const t = useTranslations("community");
  const count = item.saved_count ?? 0;
  return count > 0 ? <span className={styles.savedCount}><Bookmark size={13} aria-hidden />{t("saves", { count })}</span> : null;
}
export function DiscoveryCard({ item, onDismiss }: { item: DiscoveryItem; onDismiss?: (item: DiscoveryItem) => void }) {
  const locale = useLocale(); const c = getDiscoveryCopy(locale);
  const { flags } = useCommunity();
  const pathname = usePathname(); const params = useSearchParams();
  const navigation = useDiscoveryDetailNavigation();
  const returnTo = `${pathname}${params.size ? `?${params}` : ""}`;
  const href = discoveryDetailHref(item, returnTo);
  const thumbnail = safeExternalHref(item.thumbnail_url, ["https:"]);
  const cover = item.content?.media?.[0];
  const remember = (event: MouseEvent<HTMLAnchorElement>) => {
    if (!event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey && event.button === 0) navigation?.remember(event.currentTarget, href);
  };
  if ((item.kind === "post" || item.kind === "itinerary" || item.source.kind === "community") && !flags.enabled) return null;
  return <article id={item.id} className={styles.card}>
    {(cover || thumbnail) && <Link href={href} scroll={false} aria-label={`${c.details}: ${item.title}`} onClick={remember}>{cover ? <div className={styles.cover}><CommunityImage id={cover.id} alt={cover.alt || item.title} thumbnail /></div> : <div className={styles.cover}>
      {/* Source-authorized images only. No image means no placeholder or empty link. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={thumbnail} alt={item.title} loading="lazy" decoding="async" referrerPolicy="no-referrer" />
    </div>}</Link>}
    <div className={styles.cardBody}>
      <CardMetadata item={item} />
      <h3 className={styles.cardTitle}><Link href={href} scroll={false} onClick={remember}>{item.title}</Link></h3>
      {item.summary?.trim() && <p className={styles.cardSummary}>{item.summary}</p>}
      <p className={styles.cardMeta}>{c.sourceKinds[item.source.kind]} · {item.author?.display_name || item.source.label}{item.published_at && <> · <time dateTime={item.published_at}>{new Date(item.published_at).toLocaleDateString(locale)}</time></>}</p>
      {item.recommendation_reason && <p className={styles.reason}><span className="sr-only">{c.reason}: </span>{getRecommendationReason(locale, item.recommendation_reason)}</p>}
      <div className={styles.cardFooter}><SavedContentAction item={item} returnTo={returnTo} compact resumeEnabled={!params.has("content")} /><TravelPlanAction item={item} returnTo={returnTo} compact resumeEnabled={!params.has("content")} /><SavedCount item={item} /></div>
      {onDismiss && <button type="button" onClick={() => onDismiss(item)} className="min-h-11 self-start rounded-lg text-xs text-[var(--muted)] underline underline-offset-4 focus-visible:outline focus-visible:outline-2">{c.dismiss}</button>}
    </div>
  </article>;
}
function CardMetadata({ item }: { item: DiscoveryItem }) {
  const locale = useLocale(); const c = getDiscoveryCopy(locale);
  const kind = c.kinds[item.kind];
  const normalize = (label: string) => label.trim().normalize("NFKC").toLocaleLowerCase(locale);
  const names = new Set([normalize(kind)]); const ids = new Set<string>();
  const topics = (item.display_topics || []).filter((topic) => {
    const name = normalize(topic.label);
    if (!name || names.has(name) || ids.has(topic.id)) return false;
    names.add(name); ids.add(topic.id); return true;
  });
  return <p className={styles.cardMeta}>
    {item.destination?.name && <span className={styles.cardMetaItem}><MapPin size={13} aria-hidden /><span>{item.destination.name}</span></span>}
    <span className={styles.cardMetaItem}>{item.destination?.name && <span aria-hidden>·</span>}<span>{kind}</span></span>
    {topics.map((topic) => <span className={styles.cardMetaItem} key={topic.id}><span aria-hidden>·</span><span>{topic.label.trim()}</span></span>)}
  </p>;
}
export function DiscoveryDetails({ kind, id, returnTo = "/explore" }: { kind: string; id: string; returnTo?: string }) {
  const locale = useLocale(); const c = getDiscoveryCopy(locale); const f = getFrontendFlowCopy(locale);
  const reading = useTranslations("admin.sitePages");
  const navigation = useDiscoveryDetailNavigation();
  const result = useDiscoveryResource<DiscoveryItem>(`/discovery/content/${encodeURIComponent(kind)}/${encodeURIComponent(id)}`);
  if (result.error) return <div role="alert" className={styles.detailBody}><p>{c.unavailable}</p><Button secondary onClick={result.reload}>{c.retry}</Button></div>;
  if (!result.data) return <div role="status" className={styles.detailBody}><p>{c.loading}</p><div className={`${styles.skeleton} ${styles.skeletonImage}`} /></div>;
  const item = result.data;
  const source = safeExternalHref(item.source.url, ["https:"]);
  const videos = [...new Map([...(item.video ? [item.video] : []), ...(item.content?.video_refs || [])].map((video) => [video.video_id, video])).values()];
  const detail = item.detail;
  const guides = (detail?.guides || []).flatMap((guide) => {
    const href = safeExternalHref(guide.source.url, ["https:", "http:"]);
    return href && (guide.kind === "article" || guide.kind === "video") ? [{ id: guide.id, kind: guide.kind, title: guide.title, href, source: (guide.source.label || "").trim() || new URL(href).hostname }] : [];
  });
  const overview = [detail?.intro?.body, item.content?.text, item.summary].find((text) => text?.trim());
  return <><div className={styles.detailBody} data-discovery-detail-body ref={navigation?.restoreDetails}>
      <h2 tabIndex={-1} className="mb-3 text-2xl font-bold">{item.title}</h2>
      {item.destination && <p className="mb-4 text-sm text-[var(--teal)]">{item.destination.name}</p>}
      {videos.map((video) => <DiscoveryVideoPlayer key={video.video_id} video={video} />)}
      {item.content?.media?.map((media) => <CommunityImage key={media.id} id={media.id} alt={media.alt || item.title} />)}
      {overview && <section className={styles.detailSection}><h3 className="sr-only">{f.overview}</h3><p className="whitespace-pre-wrap break-words leading-8">{overview}</p></section>}
      {detail?.place && <PlaceFacts place={detail.place} />}
      {detail?.merchants?.length ? <section className={styles.detailSection}>
        {kind !== "merchant" && <h3 className="mb-3 font-bold">{f.nearbyFood}</h3>}
        <ul className="space-y-5">{detail.merchants.map((merchant) => {
          const self = kind === "merchant" && merchant.id === id;
          const href = discoveryDetailHref({ kind: "merchant", id: merchant.id }, returnTo);
          return <li key={merchant.id} className="min-w-0">
            {!self && <Link href={href} scroll={false} data-discovery-detail-target={`merchant:${merchant.id}`} onClick={(event) => {
              if (!event.metaKey && !event.ctrlKey && !event.shiftKey && !event.altKey && event.button === 0) navigation?.remember(event.currentTarget, href);
            }} className="inline-flex min-h-11 items-center break-words font-semibold text-[var(--teal)] underline">{merchant.name}</Link>}
            {merchant.address && <p className="mb-3 break-words text-sm text-[var(--muted)]">{merchant.address}</p>}
            <MerchantExternalLinks merchant={merchant} />
          </li>;
        })}</ul>
      </section> : null}
      {guides.length ? <section className={styles.detailSection}><h3 className="mb-3 font-bold">{f.relatedGuides}</h3>{(["article", "video"] as const).map((group) => {
        const entries = guides.filter((guide) => guide.kind === group);
        return entries.length ? <section key={group} aria-label={reading(group === "article" ? "articleGroup" : "videoGroup")} className="mt-5"><h4 className="mb-2 font-semibold">{reading(group === "article" ? "articleGroup" : "videoGroup")}</h4><ul>{entries.map((guide) => <li key={guide.id}><ExternalLink href={guide.href}>{guide.title} ({guide.source})</ExternalLink></li>)}</ul></section> : null;
      })}</section> : null}
      {detail?.hotel && <HotelDetails product={detail.hotel} />}
      {item.content?.itinerary && <ItineraryPreview itinerary={item.content.itinerary} />}
      <section className={styles.detailSection}><h3 className="mb-3 font-bold">{f.sources}</h3><p className="text-sm leading-6 text-[var(--muted)]">{c.sourceKinds[item.source.kind]} · {item.author?.display_name || item.source.label}<br />{c.originalLanguage}: {item.locale} · {item.published_at ? <time dateTime={item.published_at}>{new Date(item.published_at).toLocaleDateString(locale)}</time> : c.undated}{item.updated_at && <><br />{getDiscoveryFeedback(locale).updated}: <time dateTime={item.updated_at}>{new Date(item.updated_at).toLocaleString(locale)}</time></>}</p>
        {item.author?.handle && <Link href={`/community/profiles/${encodeURIComponent(item.author.handle)}`} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{item.author.display_name}</Link>}
        {source && <ExternalLink href={source}>{c.source}</ExternalLink>}
        {item.href && !item.href.includes("/explore?content=") && <Link href={safeNextPath(item.href, "/explore").replace(/^\/(?:zh-TW|zh-CN|en|ja|ko)(?=\/)/, "")} className="flex min-h-11 items-center text-[var(--teal)] underline">{c.details}</Link>}
      </section>
    </div><footer className={styles.detailFooter}><SavedContentAction item={item} returnTo={returnTo} /><TravelPlanAction item={item} returnTo={returnTo} /><SavedCount item={item} /></footer></>;
}
function HotelDetails({ product }: { product: Product }) {
  const t = useTranslations("travelServices"); const [open, setOpen] = useState(false);
  return <section className={styles.detailSection}><p className="font-semibold">{product.title}</p>{product.facts?.facilities?.length ? <p className="my-3 text-sm text-[var(--muted)]">{product.facts.facilities.join(" · ")}</p> : null}<Button secondary onClick={() => setOpen(true)}>{t("platforms")}</Button><SourceCredits credits={product.facts?.source_credits} />{open && <BookingPanel product={product} placement="discovery" onClose={() => setOpen(false)} />}</section>;
}
function ExternalLink({ href, children }: { href?: string | null; children: ReactNode }) {
  const safe = safeExternalHref(href, ["https:", "http:"]);
  return safe ? <a href={safe} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 max-w-full items-center gap-2 pr-4 text-sm font-semibold text-[var(--teal)] underline"><span className="min-w-0 [overflow-wrap:anywhere]">{children}</span><ArrowUpRight size={15} className="shrink-0" aria-hidden /></a> : null;
}
function PlaceFacts({ place }: { place: DiscoveryPlace }) {
  const locale = useLocale(); const f = getFrontendFlowCopy(locale);
  if (!place.address?.trim() && !place.opening_hours?.weekday_descriptions?.length
    && !safeExternalHref(place.google_maps_url, ["http:", "https:"]) && !safeExternalHref(place.official_website_url, ["http:", "https:"])
    && !place.fetched_at && !place.updated_at && !place.attribution?.provider && place.status !== "stale") return null;
  return <section className={styles.detailSection}>
    {place.status === "stale" && <p role="status" className="mb-4 text-sm text-[var(--muted)]">{f.stale}</p>}
    {place.address && <><h3 className="font-semibold">{f.address}</h3><p className="mb-3 leading-7">{place.address}</p></>}
    {place.opening_hours?.weekday_descriptions?.length ? <><h3 className="font-semibold">{f.hours}</h3><ul className="mb-3 text-sm leading-7">{place.opening_hours.weekday_descriptions.map((line) => <li key={line}>{line}</li>)}</ul></> : null}
    <ExternalLink href={place.google_maps_url}>{f.map}</ExternalLink><ExternalLink href={place.official_website_url}>{f.officialSite}</ExternalLink>
    {(place.fetched_at || place.updated_at) && <p className="mt-3 text-xs text-[var(--muted)]">{getDiscoveryFeedback(locale).updated}: {new Date(place.fetched_at || place.updated_at!).toLocaleString(locale)}{place.data_locale && ` · ${place.data_locale}`}</p>}
    {place.attribution?.provider && <div className="mt-3 text-xs"><ExternalLink href={place.attribution.provider_url}>{place.attribution.provider}</ExternalLink>{place.attribution.third_party?.map((source, index) => <span key={`${source.provider}:${index}`}>{safeExternalHref(source.providerUri) ? <ExternalLink href={source.providerUri}>{source.provider}</ExternalLink> : source.provider}</span>)}</div>}
  </section>;
}
