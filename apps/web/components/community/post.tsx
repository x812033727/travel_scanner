"use client";

import { useState, type FormEvent } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link, useRouter } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";
import { api } from "@/lib/api";
import type { Comment, Page, Post, PublicItinerary } from "@/lib/community/types";
import { useCommunity } from "./provider";
import { RelatedPlaces } from "./places";
import { Button, CommunityImage, Dialog, Empty, ErrorNotice, fieldClass, panelClass } from "./ui";
import { useResource } from "./use-resource";
import { DiscoveryVideoPlayer } from "@/components/discovery/video";

export function TranslateText({ kind, id, original, sourceLocale }: { kind: "post" | "comment"; id: string; original: string; sourceLocale: string }) {
  const locale = useLocale();
  return <Translation key={JSON.stringify([kind, id, original, sourceLocale, locale])} kind={kind} id={id} original={original} sourceLocale={sourceLocale} />;
}
function Translation({ kind, id, original, sourceLocale }: { kind: "post" | "comment"; id: string; original: string; sourceLocale: string }) {
  const t = useTranslations("community");
  const locale = useLocale();
  const { flags, me } = useCommunity();
  const [translated, setTranslated] = useState<string>();
  const [show, setShow] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  async function translate() {
    if (show) { setShow(false); return; }
    if (translated) { setShow(true); return; }
    setBusy(true); setError(undefined);
    try { const result = await api<{ text: string }>("/community/translations", { method: "POST", body: JSON.stringify({ kind, target_id: id, locale }) }); setTranslated(result.text); setShow(true); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  return <div className="space-y-3"><p className="whitespace-pre-wrap break-words leading-7">{show ? translated : original}</p>
    {show && <p className="text-xs text-[var(--muted)]">{t("machineTranslation")}</p>}
    {sourceLocale !== locale && flags.translation_enabled && <Button secondary disabled={busy || !me?.profile} onClick={() => void translate()}>{show ? t("showOriginal") : busy ? t("loading") : t("translate")}</Button>}
    <ErrorNotice error={error} /></div>;
}

export function ItineraryPreview({ itinerary }: { itinerary: PublicItinerary }) {
  const t = useTranslations("community");
  const locale = useLocale();
  return <section className={`${panelClass} space-y-4`}><h2 className="text-xl font-bold">{t("publicItinerary")}</h2><p className="text-sm text-[var(--muted)]">{t("itineraryPrivacy")}</p>
    {Array.from({ length: itinerary.days }, (_, index) => index + 1).map((day) => <div key={day}><h3 className="font-bold text-[var(--teal)]">{t("day", { count: day })}</h3><ol className="mt-2 space-y-2 border-l border-[var(--line)] pl-4">
      {itinerary.stops.filter((stop) => stop.day === day).sort((a, b) => a.position - b.position).map((stop, index) => <li key={index} className="flex flex-wrap justify-between gap-2"><span>{stop.names[locale] || stop.title || stop.location_name}</span>{stop.duration_minutes !== null && <span className="text-sm text-[var(--muted)]">{t("minutes", { count: stop.duration_minutes })}</span>}</li>)}
    </ol></div>)}
  </section>;
}

export function ReportButton({ kind, target, messageIds = [] }: { kind: "post" | "comment" | "profile" | "message"; target: string; messageIds?: number[] }) {
  const t = useTranslations("community");
  const { me } = useCommunity();
  const [open, setOpen] = useState(false);
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  const [sent, setSent] = useState(false);
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(undefined);
    try { await api("/community/reports", { method: "POST", body: JSON.stringify({ kind, target, reason, message_ids: messageIds }) }); setSent(true); setOpen(false); }
    catch (value) { setError(value); } finally { setBusy(false); }
  }
  return <><Button secondary disabled={!me?.profile || sent} onClick={() => setOpen(true)}>{sent ? t("reportSent") : t("report")}</Button>{open && <Dialog title={t("report")} onClose={() => setOpen(false)}><form onSubmit={submit} className="space-y-4">
    {kind === "message" && <p>{t("reportMessageScope", { count: messageIds.length })}</p>}
    <label className="block font-semibold">{t("reason")}<textarea required minLength={3} maxLength={2000} rows={4} className={fieldClass} value={reason} onChange={(e) => setReason(e.target.value)} /></label><ErrorNotice error={error} /><Button type="submit" disabled={busy}>{t("submit")}</Button>
  </form></Dialog>}</>;
}

export function CollectButton({ kind, target, discovery = false, initialOpen = false }: { kind: "post" | "pet_place" | "hotspot" | "food" | "merchant" | "guide" | "hotel"; target: string; discovery?: boolean; initialOpen?: boolean }) {
  const t = useTranslations("community");
  const { me } = useCommunity();
  const { user } = useHeaderSession();
  const [open, setOpen] = useState(initialOpen);
  const prefix = discovery ? "/discovery" : "/community";
  const [selected, setSelected] = useState("");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [saved, setSaved] = useState(false);
  const [error, setError] = useState<unknown>();
  const collections = useResource<Page<{ id: string; name: string }>>(open ? `${prefix}/collections` : null);
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(undefined);
    try {
      let id = selected;
      if (!id) { id = (await api<{ id: string }>(`${prefix}/collections`, { method: "POST", body: JSON.stringify({ name }) })).id; setSelected(id); }
      await api(`${prefix}/collections/${id}/items`, { method: discovery ? "POST" : "PUT", body: JSON.stringify(discovery ? { kind, id: target } : { kind, target }) }); setSaved(true); setOpen(false);
    } catch (value) { setError(value); } finally { setBusy(false); }
  }
  return <><Button secondary disabled={discovery ? !user : !me?.profile} onClick={() => setOpen(true)}>{saved ? t("saved") : t("addToCollection")}</Button>{open && <Dialog title={t("collections")} onClose={() => setOpen(false)}><form onSubmit={submit} className="space-y-4"><p>{t("privateCollections")}</p>
    <label className="block font-semibold">{t("collection")}<select className={fieldClass} value={selected} onChange={(e) => setSelected(e.target.value)}><option value="">{t("newCollection")}</option>{collections.data?.items.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}</select></label>
    {!selected && <label className="block font-semibold">{t("name")}<input required maxLength={80} value={name} onChange={(e) => setName(e.target.value)} className={fieldClass} /></label>}
    <ErrorNotice error={error || collections.error} /><Button type="submit" disabled={busy || Boolean(collections.error)}>{t("save")}</Button>
  </form></Dialog>}</>;
}

export function PostDetails({ id }: { id: string }) {
  const t = useTranslations("community");
  const router = useRouter();
  const { user } = useHeaderSession();
  const { me } = useCommunity();
  const visibility = useSiteVisibility();
  const { data: post, error, reload } = useResource<Post>(`/community/posts/${id}`);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<unknown>();
  const [forking, setForking] = useState(false);
  const [startDate, setStartDate] = useState("");
  const [retry, setRetry] = useState<{ date: string; key: string }>();
  async function react(kind: "like" | "save") {
    if (!post) return;
    setBusy(true); setActionError(undefined);
    try { await api(`/community/posts/${id}/reactions/${kind}`, { method: (kind === "like" ? post.liked : post.saved) ? "DELETE" : "PUT" }); await reload(); }
    catch (reason) { setActionError(reason); } finally { setBusy(false); }
  }
  async function fork(e: FormEvent) {
    e.preventDefault(); setBusy(true); setActionError(undefined);
    const request = retry?.date === startDate ? retry : { date: startDate, key: crypto.randomUUID() };
    setRetry(request);
    try { const result = await api<{ trip_id: string }>(`/community/posts/${id}/fork`, { method: "POST", body: JSON.stringify({ start_date: startDate, idempotency_key: request.key }) }); router.push(`/trips/${result.trip_id}`); }
    catch (reason) { setActionError(reason); } finally { setBusy(false); }
  }
  if (error) return <ErrorNotice error={error} />;
  if (!post) return <Empty>{t("loading")}</Empty>;
  return <article className="space-y-6">
    <header className="space-y-3"><p className="text-sm font-semibold text-[var(--teal)]">{post.destination}{post.featured && ` · ${t("officialSelection")}`}</p><h1 className="text-3xl font-bold md:text-4xl">{post.title}</h1><Link href={`/community/profiles/${post.author.handle}`} className="font-semibold underline">{post.author.display_name}</Link></header>
    <div className="grid gap-4 sm:grid-cols-2">{post.media.map((image) => <CommunityImage key={image.id} id={image.id} alt={image.alt || post.title} />)}</div>
    <TranslateText kind="post" id={post.id} original={post.body} sourceLocale={post.locale} />
    {post.video_refs?.map((video) => <DiscoveryVideoPlayer key={video.video_id} video={video} />)}
    <div className="flex flex-wrap gap-2">{post.topics.map((topic) => <span key={topic} className="rounded-full bg-[var(--paper)] px-3 py-1 text-sm">#{topic}</span>)}</div>
    <RelatedPlaces places={post.places || []} />
    <div className="flex flex-wrap gap-3"><Button secondary disabled={busy || !me?.profile} onClick={() => void react("like")}>{post.liked ? t("unlike") : t("like")} · {post.likes}</Button><Button secondary disabled={busy || !me?.profile} onClick={() => void react("save")}>{post.saved ? t("unsave") : t("savePost")} · {post.saves}</Button><CollectButton kind="post" target={id} /><ReportButton kind="post" target={id} />
      {user?.id === post.author.id && <Link href={`/community/posts/${id}/edit`} className="rounded-xl border border-[var(--line)] px-4 py-2.5">{t("edit")}</Link>}
    </div><ErrorNotice error={actionError} />
    {post.itinerary && <><ItineraryPreview itinerary={post.itinerary} />{post.allow_fork && featureVisible(visibility, "trips") ? <Button disabled={!me?.profile} onClick={() => setForking(true)}>{t("forkFree")}</Button> : <p className="text-sm text-[var(--muted)]">{t("forkNotAllowed")}</p>}</>}
    {forking && <Dialog title={t("forkFree")} onClose={() => setForking(false)}><form onSubmit={fork} className="space-y-4"><p>{t("forkNotice")}</p><label className="block font-semibold">{t("departureDate")}<input required type="date" value={startDate} onChange={(e) => setStartDate(e.target.value)} className={fieldClass} /></label><ErrorNotice error={actionError} /><Button type="submit" disabled={busy}>{t("createPrivateTrip")}</Button></form></Dialog>}
    <Comments postId={id} />
  </article>;
}

function Comments({ postId }: { postId: string }) {
  const t = useTranslations("community");
  const locale = useLocale();
  const { flags, me } = useCommunity();
  const { user } = useHeaderSession();
  const resource = useResource<Page<Comment>>(`/community/posts/${postId}/comments`);
  const [extra, setExtra] = useState<Comment[]>([]);
  const [cursor, setCursor] = useState<string | number | null>();
  const [body, setBody] = useState("");
  const [reply, setReply] = useState<Comment>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  const [loaded, setLoaded] = useState(resource.data);
  if (loaded !== resource.data) { setLoaded(resource.data); setExtra([]); setCursor(resource.data?.next_cursor); }
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(undefined);
    try { await api(`/community/posts/${postId}/comments`, { method: "POST", body: JSON.stringify({ body, locale, parent_id: reply?.id || null }) }); setBody(""); setReply(undefined); await resource.reload(); }
    catch (value) { setError(value); } finally { setBusy(false); }
  }
  async function change(comment: Comment, remove: boolean) {
    const value = remove ? null : window.prompt(t("editComment"), comment.body);
    if (!remove && value === null) return;
    if (remove && !window.confirm(t("deleteConfirm"))) return;
    setBusy(true); setError(undefined);
    try { await api(`/community/comments/${comment.id}`, { method: remove ? "DELETE" : "PUT", ...(remove ? {} : { body: JSON.stringify({ body: value, locale: comment.locale, parent_id: comment.parent_id }) }) }); await resource.reload(); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  async function more() {
    setBusy(true); setError(undefined);
    try { const next = await api<Page<Comment>>(`/community/posts/${postId}/comments?cursor=${encodeURIComponent(cursor || "")}`); setExtra((rows) => [...rows, ...next.items]); setCursor(next.next_cursor); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  return <section className="space-y-4 border-t border-[var(--line)] pt-6"><h2 className="text-2xl font-bold">{t("comments")}</h2><ErrorNotice error={error || resource.error} />
    {[...(resource.data?.items || []), ...extra].map((comment) => <article key={comment.id} className={`${panelClass} ${comment.parent_id ? "ml-5" : ""}`}><Link href={`/community/profiles/${comment.author.handle}`} className="font-semibold text-[var(--teal)]">{comment.author.display_name}</Link><TranslateText kind="comment" id={comment.id} original={comment.body} sourceLocale={comment.locale} /><div className="mt-3 flex flex-wrap gap-2">
      {!comment.parent_id && <Button secondary disabled={!me?.verified || !flags.comments_enabled} onClick={() => setReply(comment)}>{t("reply")}</Button>}
      {user?.id === comment.author.id && <><Button secondary disabled={busy} onClick={() => void change(comment, false)}>{t("edit")}</Button><Button secondary disabled={busy} onClick={() => void change(comment, true)}>{t("delete")}</Button></>}<ReportButton kind="comment" target={comment.id} />
    </div></article>)}
    {cursor && <Button secondary disabled={busy} onClick={() => void more()}>{t("loadMore")}</Button>}
    {flags.comments_enabled && me?.verified ? <form onSubmit={submit} className="space-y-3">{reply && <p>{t("replyTo", { name: reply.author.display_name })} <Button secondary onClick={() => setReply(undefined)}>{t("cancel")}</Button></p>}<label className="block font-semibold">{t("writeComment")}<textarea required maxLength={2000} rows={3} value={body} onChange={(e) => setBody(e.target.value)} className={fieldClass} /></label><Button type="submit" disabled={busy}>{t("submit")}</Button></form> : <p className="text-sm text-[var(--muted)]">{flags.comments_enabled ? t("verifyRequired") : t("commentsClosed")}</p>}
  </section>;
}
