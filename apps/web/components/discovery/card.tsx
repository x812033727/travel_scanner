"use client";
import { useState } from "react";
import { useLocale } from "next-intl";
import { useSearchParams } from "next/navigation";
import { BookOpen, Compass, MapPin, Play, Route, Soup, Store, Hotel, ArrowUpRight } from "lucide-react";
import { Link } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useCommunity } from "@/components/community/provider";
import { CollectButton, ItineraryPreview } from "@/components/community/post";
import { Button, CommunityImage, Dialog } from "@/components/community/ui";
import { TravelCardActions } from "@/components/travel-card-actions";
import { getDiscoveryCopy, getDiscoveryFeedback, getRecommendationReason } from "@/lib/discovery-copy";
import { useDiscoveryResource, type DiscoveryItem } from "@/lib/discovery";
import { loginPath, safeExternalHref, safeNextPath } from "@/lib/navigation";
import { DiscoveryVideoPlayer } from "./video";

const icons = { hotspot: Compass, food: Soup, merchant: Store, hotel: Hotel, article: BookOpen, video: Play, post: BookOpen, itinerary: Route };
export function DiscoveryCard({ item, onDismiss }: { item: DiscoveryItem; onDismiss?: (item: DiscoveryItem) => void }) {
  const locale = useLocale();
  const c = getDiscoveryCopy(locale);
  const { user } = useHeaderSession();
  const { flags } = useCommunity();
  const params = useSearchParams();
  const [detailTrigger, setDetailTrigger] = useState<HTMLElement | null>(null);
  const Icon = icons[item.kind] || Compass;
  const thumbnail = safeExternalHref(item.thumbnail_url, ["https:"]);
  const cover = item.content?.media?.[0];
  const ref = item.place_ref;
  const path = ref?.selection_path || null;
  const isCommunity = item.kind === "post" || item.kind === "itinerary" || item.source.kind === "community";
  const collectionQuery = new URLSearchParams(params.toString());
  collectionQuery.set("resume_action", "collection"); collectionQuery.set("resume_item", item.id); collectionQuery.set("resume_kind", item.kind);
  if (isCommunity && !flags.enabled) return null;
  return <article id={ref ? `${ref.kind}-${ref.id}` : item.id} className="flex min-w-0 flex-col overflow-hidden rounded-3xl border border-[var(--line)] bg-[var(--surface)] transition-shadow hover:shadow-md motion-reduce:transition-none">
    {cover ? <div className="relative overflow-hidden bg-[var(--paper)] [&_img]:aspect-[16/9] [&_img]:rounded-none [&_img]:object-cover">
      <CommunityImage id={cover.id} alt={cover.alt || item.title} thumbnail />
      <span className="absolute bottom-3 left-3 rounded-full bg-[var(--surface)] px-3 py-1 text-xs font-semibold text-[var(--ink)]">{c.kinds[item.kind]}</span>
    </div> : thumbnail ? <div className="relative aspect-[16/9] overflow-hidden bg-[var(--paper)]">
      {/* Source-authorized images only; type illustration is the missing-image fallback. */}
      {/* eslint-disable-next-line @next/next/no-img-element */}
      <img src={thumbnail} alt={item.title} loading="lazy" decoding="async" referrerPolicy="no-referrer" className="h-full w-full object-cover" />
      <span className="absolute bottom-3 left-3 rounded-full bg-[var(--surface)] px-3 py-1 text-xs font-semibold text-[var(--ink)]">{c.kinds[item.kind]}</span>
    </div> : <div className="flex min-h-28 items-end justify-between gap-4 border-b border-[var(--line)] bg-[var(--paper)] p-5">
      <span className="grid size-12 place-items-center rounded-2xl border border-[var(--line)] bg-[var(--surface)] text-[var(--teal)]"><Icon size={24} aria-hidden /></span>
      <span className="text-xs font-semibold tracking-wide text-[var(--muted)]">{c.kinds[item.kind]}</span>
    </div>}
    <div className="flex flex-1 flex-col gap-3 p-5">
      {item.destination && <p className="flex items-center gap-1.5 text-xs font-semibold text-[var(--teal)]"><MapPin size={14} aria-hidden />{item.destination.name}</p>}
      <h3 className="break-words text-xl font-bold leading-snug"><button type="button" onClick={(event) => setDetailTrigger(event.currentTarget)} className="min-h-11 text-left underline-offset-4 hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{item.title}</button></h3>
      <p className="line-clamp-3 break-words text-sm leading-6 text-[var(--muted)]">{item.summary}</p>
      <p className="text-xs leading-5 text-[var(--muted)]">{c.sourceKinds[item.source.kind]} · {item.author?.display_name || item.source.label}{item.published_at && <> · <time dateTime={item.published_at}>{new Date(item.published_at).toLocaleDateString(locale)}</time></>}</p>
      {item.recommendation_reason && <p className="rounded-xl bg-[var(--paper)] p-2.5 text-xs leading-5 text-[var(--muted)]"><span className="font-semibold">{c.reason}：</span>{getRecommendationReason(locale, item.recommendation_reason)}</p>}
      <div className="mt-auto flex flex-wrap gap-2 pt-2"><Button secondary onClick={(event) => setDetailTrigger(event.currentTarget)}>{c.details}<ArrowUpRight size={16} aria-hidden /></Button>
        {item.collection_ref && (user ? <CollectButton kind={item.collection_ref.kind} target={item.collection_ref.id} discovery initialOpen={params.get("resume_action") === "collection" && params.get("resume_item") === item.id} /> : <Link href={loginPath(`/explore?${collectionQuery}`)} className="inline-flex min-h-11 items-center rounded-xl border border-[var(--line)] px-4 text-sm font-semibold">{c.collections}</Link>)}
      </div>
      {ref && path && <TravelCardActions type={ref.kind} id={ref.id} title={item.title} selectionPath={path} merchantId={ref.merchant_id || (ref.kind === "merchant" ? ref.id : undefined)} resumeAfterLogin />}
      {onDismiss && <button type="button" onClick={() => onDismiss(item)} className="min-h-11 self-start rounded-lg px-2 text-xs text-[var(--muted)] underline underline-offset-4 focus-visible:outline focus-visible:outline-2">{c.dismiss}</button>}
    </div>
    {detailTrigger && <Dialog title={item.title} returnFocusTo={detailTrigger} onClose={() => setDetailTrigger(null)}><DiscoveryDetails kind={item.kind} id={item.id.split(":").slice(-1)[0]} /></Dialog>}
  </article>;
}

export function DiscoveryDetails({ kind, id }: { kind: string; id: string }) {
  const locale = useLocale();
  const c = getDiscoveryCopy(locale);
  const result = useDiscoveryResource<DiscoveryItem>(`/discovery/content/${encodeURIComponent(kind)}/${encodeURIComponent(id)}`);
  if (result.error) return <div role="alert"><p>{c.unavailable}</p><Button secondary onClick={result.reload}>{c.retry}</Button></div>;
  if (!result.data) return <p role="status">{c.loading}</p>;
  const item = result.data;
  const source = safeExternalHref(item.source.url, ["https:"]);
  const videos = [...new Map([...(item.video ? [item.video] : []), ...(item.content?.video_refs || [])].map((video) => [video.video_id, video])).values()];
  return <div className="space-y-5">
    <p className="text-sm leading-6 text-[var(--muted)]">{c.sourceKinds[item.source.kind]} · {item.author?.display_name || item.source.label}<br />{c.originalLanguage}: {item.locale} · {item.published_at ? <time dateTime={item.published_at}>{new Date(item.published_at).toLocaleDateString(locale)}</time> : c.undated}{item.updated_at && <><br />{getDiscoveryFeedback(locale).updated}: <time dateTime={item.updated_at}>{new Date(item.updated_at).toLocaleString(locale)}</time></>}</p>
    {videos.map((video) => <DiscoveryVideoPlayer key={video.video_id} video={video} />)}
    {item.content?.media?.map((media) => <CommunityImage key={media.id} id={media.id} alt={media.alt || item.title} />)}
    <p className="whitespace-pre-wrap break-words leading-8">{item.content?.text || item.summary}</p>
    {item.content?.itinerary && <ItineraryPreview itinerary={item.content.itinerary} />}
    {item.author?.handle && <Link href={`/community/profiles/${encodeURIComponent(item.author.handle)}`} className="inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{item.author.display_name}</Link>}
    {source && <a href={source} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-2 rounded-lg font-semibold text-[var(--teal)] underline">{c.source}<ArrowUpRight size={16} aria-hidden /></a>}
    {item.href && !item.href.includes("/explore?content=") && <Link href={safeNextPath(item.href, "/explore").replace(/^\/(?:zh-TW|zh-CN|en|ja|ko)(?=\/)/, "")} className="flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{c.details}</Link>}
  </div>;
}
