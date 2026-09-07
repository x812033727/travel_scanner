"use client";

import { useCallback, useEffect, useRef, useState, type FormEvent } from "react";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { api } from "@/lib/api";
import type { Conversation, Message, Notice, Page, Post } from "@/lib/community/types";
import { useCommunity } from "./provider";
import { ReportButton } from "./post";
import { Button, Empty, ErrorNotice, fieldClass, panelClass, Tabs } from "./ui";
import { useResource } from "./use-resource";

export function MessageCenter({ conversationId, showReviews = false }: { conversationId?: string; showReviews?: boolean }) {
  const t = useTranslations("community");
  const { flags } = useCommunity();
  const [tab, setTab] = useState(showReviews ? "reviewResults" : conversationId ? "messages" : "notifications");
  const [selected, setSelected] = useState(conversationId || "");
  const conversations = useResource<Page<Conversation>>(flags.messaging_enabled ? "/community/conversations" : null);
  return <Tabs value={tab} onChange={setTab} label={t("messages")} items={["notifications", "messages", "reviewResults", "notificationSettings"].map((value) => ({ value, label: t(value) }))}>
    {tab === "notifications" && <Notifications />}
    {tab === "reviewResults" && <ReviewResults />}
    {tab === "notificationSettings" && <NotificationSettings />}
    {tab === "messages" && (flags.messaging_enabled ? <div className="grid gap-5 md:grid-cols-[15rem_1fr]">
      <aside className="space-y-3"><p className="text-sm text-[var(--muted)]">{t("mutualOnly")}</p><ErrorNotice error={conversations.error} />
        <label className="block text-sm font-semibold md:hidden">{t("conversations")}<select className={fieldClass} value={selected} onChange={(e) => setSelected(e.target.value)}><option value="">{t("chooseConversation")}</option>{conversations.data?.items.map((item) => <option key={item.id} value={item.id}>{item.other?.display_name || t("deletedMember")}{item.unread ? ` (${item.unread})` : ""}</option>)}</select></label>
        <div className="hidden space-y-2 md:block">{conversations.data?.items.map((item) => <button key={item.id} type="button" onClick={() => setSelected(item.id)} aria-pressed={selected === item.id} className={`block w-full rounded-xl border border-[var(--line)] p-3 text-left ${selected === item.id ? "bg-[var(--teal-soft)]" : "bg-[var(--surface)]"}`}><strong>{item.other?.display_name || t("deletedMember")}</strong>{item.unread > 0 && <span className="ml-2 text-sm">{t("unread", { count: item.unread })}</span>}</button>)}</div>
        {conversations.data?.items.length === 0 && <Empty>{t("noConversations")}</Empty>}
      </aside>{selected ? <ConversationView key={selected} id={selected} /> : <Empty>{t("chooseConversation")}</Empty>}
    </div> : <Empty>{t("messagesClosed")}</Empty>)}
  </Tabs>;
}

type MessagePage = Page<Message> & { can_send: boolean; other_read_id: number; latest_cursor: number };
export async function catchUpMessages(path: string, previous?: MessagePage): Promise<MessagePage> {
  if (!previous) return api<MessagePage>(path);
  let after = previous.latest_cursor;
  const items = new Map(previous.items.map((item) => [item.id, item]));
  while (true) {
    const page = await api<MessagePage>(`${path}?after=${after}`);
    for (const item of page.items) items.set(item.id, item);
    const latest = Math.max(after, page.latest_cursor);
    if (!page.next_cursor) return { ...page, items: [...items.values()].sort((a, b) => a.id - b.id),
      latest_cursor: latest, next_cursor: previous.next_cursor };
    if (latest <= after) throw new Error("community_invalid_cursor");
    after = latest;
  }
}
function ConversationView({ id }: { id: string }) {
  const t = useTranslations("community");
  const synchronized = useRef<MessagePage | undefined>(undefined);
  const fetchMessages = useCallback((path: string) => catchUpMessages(path, synchronized.current), []);
  const resource = useResource<MessagePage>(`/community/conversations/${id}/messages`, fetchMessages);
  const cards = useResource<Page<Post>>("/community/drafts");
  const [body, setBody] = useState("");
  const [card, setCard] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [older, setOlder] = useState<string | number | null>();
  const [selected, setSelected] = useState<number[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  const retry = useRef<{ body: string; card: string; key: string } | undefined>(undefined);
  const read = useRef(0);
  const [loaded, setLoaded] = useState(resource.data);
  if (loaded !== resource.data) {
    setLoaded(resource.data);
    if (resource.data) {
    setMessages((previous) => [...new Map([...previous, ...resource.data!.items].map((item) => [item.id, item])).values()].sort((a, b) => a.id - b.id));
    setOlder((previous) => previous === undefined ? resource.data!.next_cursor : previous);
    }
  }
  useEffect(() => {
    if (resource.data) synchronized.current = resource.data;
    const last = resource.data?.latest_cursor || 0;
    if (last > read.current) {
      void api(`/community/conversations/${id}/read`, { method: "PUT", body: JSON.stringify({ through_id: last }) })
        .then(() => { read.current = Math.max(read.current, last); }).catch(() => {});
    }
  }, [resource.data, id]);
  async function send(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(undefined);
    const request = retry.current?.body === body && retry.current.card === card ? retry.current : { body, card, key: crypto.randomUUID() };
    retry.current = request;
    try {
      await api(`/community/conversations/${id}/messages`, { method: "POST", body: JSON.stringify({ body, card_post_id: card || null, idempotency_key: request.key }) });
      setBody(""); setCard(""); retry.current = undefined; await resource.reload();
    } catch (reason) { setError(reason); await resource.reload(); } finally { setBusy(false); }
  }
  async function history() {
    setBusy(true); setError(undefined);
    try { const page = await api<MessagePage>(`/community/conversations/${id}/messages?before=${older}`); setMessages((rows) => [...page.items, ...rows]); setOlder(page.next_cursor); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  if (resource.error) return <ErrorNotice error={resource.error} />;
  return <section className={`${panelClass} min-w-0 space-y-4`}>
    {older && <Button secondary disabled={busy} onClick={() => void history()}>{t("olderMessages")}</Button>}
    <div role="log" aria-label={t("messages")} className="max-h-[55dvh] space-y-3 overflow-y-auto pr-1">
      {messages.map((message) => <article key={message.id} className={`max-w-[90%] rounded-2xl p-3 ${message.mine ? "ml-auto bg-[var(--teal-soft)]" : "bg-[var(--paper)]"}`}>
        <p className="whitespace-pre-wrap break-words leading-6">{message.body}</p>
        {message.card && <Link href={`/community/posts/${message.card.id}`} className="mt-2 block rounded-xl border border-[var(--line)] p-3 font-semibold underline">{message.card.title}</Link>}
        {message.card_unavailable && <p className="text-sm">{t("contentUnavailable")}</p>}
        {!message.sender_id && <p className="text-xs text-[var(--muted)]">{t("deletedMember")}</p>}
        <div className="mt-2 flex flex-wrap justify-between gap-3 text-xs text-[var(--muted)]"><label className="inline-flex min-h-9 items-center gap-2"><input type="checkbox" checked={selected.includes(message.id)} disabled={!selected.includes(message.id) && selected.length >= 5} onChange={(e) => setSelected(e.target.checked ? [...selected, message.id] : selected.filter((value) => value !== message.id))} />{t("selectToReport")}</label>{message.mine && <span>{message.id <= (resource.data?.other_read_id || 0) ? t("read") : t("sent")}</span>}</div>
      </article>)}
      {!messages.length && <p className="text-sm text-[var(--muted)]">{t("noMessages")}</p>}
    </div>
    {selected.length > 0 && <ReportButton kind="message" target={id} messageIds={selected} />}
    {!resource.data?.can_send && <p role="status" className="text-sm">{t("mutualOnly")}</p>}
    <form onSubmit={send} className="space-y-3"><fieldset disabled={busy || !resource.data?.can_send} className="space-y-3">
      <label className="block text-sm font-semibold">{t("message")}<textarea rows={3} maxLength={2000} value={body} onChange={(e) => setBody(e.target.value)} className={fieldClass} /></label>
      <label className="block text-sm font-semibold">{t("attachPublicCard")}<select value={card} onChange={(e) => setCard(e.target.value)} className={fieldClass}><option value="">{t("none")}</option>{cards.data?.items.filter((post) => post.state === "published").map((post) => <option key={post.id} value={post.id}>{post.title}</option>)}</select></label>
      <p className="text-xs text-[var(--muted)]">{t("privateTripMessageNotice")} <Link href="/community/new" className="underline">{t("publish")}</Link></p>
      <Button type="submit" disabled={busy || !resource.data?.can_send || (!body.trim() && !card)}>{t("send")}</Button>
    </fieldset></form><ErrorNotice error={error} />
  </section>;
}

function noticeHref(notice: Notice): string {
  if (notice.kind === "follow" && notice.actor) return `/community/profiles/${notice.actor.handle}`;
  if (notice.kind === "message") return `/community/messages?conversation=${notice.target}`;
  if (notice.kind === "review") return "/community/messages?tab=reviews";
  return `/community/posts/${notice.target}`;
}
function Notifications() {
  const t = useTranslations("community");
  const resource = useResource<Page<Notice> & { unread: number }>("/community/notifications");
  const [extra, setExtra] = useState<Notice[]>([]);
  const [cursor, setCursor] = useState<string | number | null>();
  const [error, setError] = useState<unknown>();
  const [loaded, setLoaded] = useState(resource.data);
  if (loaded !== resource.data) { setLoaded(resource.data); setExtra([]); setCursor(resource.data?.next_cursor); }
  async function markRead() {
    const through = resource.data?.items[0]?.id;
    if (!through) return;
    try { await api("/community/notifications/read", { method: "PUT", body: JSON.stringify({ through_id: through }) }); await resource.reload(); }
    catch (reason) { setError(reason); }
  }
  async function more() {
    try { const page = await api<Page<Notice>>(`/community/notifications?before=${cursor}`); setExtra((rows) => [...rows, ...page.items]); setCursor(page.next_cursor); }
    catch (reason) { setError(reason); }
  }
  return <section className="space-y-3"><Button secondary onClick={() => void markRead()} disabled={!resource.data?.unread}>{t("markAllRead")}</Button><ErrorNotice error={error || resource.error} />
    {[...(resource.data?.items || []), ...extra].map((notice) => <Link key={notice.id} href={noticeHref(notice)} className={`${panelClass} block ${notice.read ? "" : "border-l-4 border-l-[var(--teal)]"}`}><span className="font-semibold">{notice.actor?.display_name || t("system")}</span><span className="ml-2">{t(`noticeKinds.${notice.kind}`)}</span></Link>)}
    {resource.data?.items.length === 0 && <Empty>{t("noNotifications")}</Empty>}
    {cursor && <Button secondary onClick={() => void more()}>{t("loadMore")}</Button>}
  </section>;
}
function NotificationSettings() {
  const t = useTranslations("community");
  const { me, refresh } = useCommunity();
  const kinds = ["follow", "like", "comment", "reply", "mention", "message", "review"];
  const [preferences, setPreferences] = useState<Record<string, boolean>>({});
  const [error, setError] = useState<unknown>();
  const [saved, setSaved] = useState(false);
  const [loaded, setLoaded] = useState<typeof me>();
  if (loaded !== me) { setLoaded(me); setPreferences(Object.fromEntries(kinds.map((kind) => [kind, me?.notification_preferences[kind] !== false]))); }
  async function save(e: FormEvent) {
    e.preventDefault(); setError(undefined); setSaved(false);
    try { await api("/community/me/notification-preferences", { method: "PUT", body: JSON.stringify(preferences) }); await refresh(); setSaved(true); }
    catch (reason) { setError(reason); }
  }
  return <form onSubmit={save} className={`${panelClass} space-y-3`}>{kinds.map((kind) => <label key={kind} className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={preferences[kind] !== false} onChange={(e) => setPreferences({ ...preferences, [kind]: e.target.checked })} />{t(`notificationKinds.${kind}`)}</label>)}<ErrorNotice error={error} />{saved && <p role="status">{t("saved")}</p>}<Button type="submit">{t("save")}</Button></form>;
}

function ReviewResults() {
  const t = useTranslations("community");
  const data = useResource<{items:Array<{id:string;action:string;reason:string;created_at:string}>;pet_reports:Array<{id:string;place_id:string;status:string;body:string}>}>("/community/me/reviews");
  return <div className="space-y-4"><ErrorNotice error={data.error} />
    {data.data?.items.map((item) => {
      const action = item.action.replace("community_post_", "");
      return <article key={item.id} className={panelClass}><h2 className="font-bold">{t.has(`actions.${action}`) ? t(`actions.${action}`) : t("reviewResults")}</h2><p className="my-2 whitespace-pre-wrap">{item.reason}</p><time className="text-xs text-[var(--muted)]" dateTime={item.created_at}>{item.created_at}</time></article>;
    })}
    {data.data?.pet_reports.map((report) => <article key={report.id} className={panelClass}><p className="font-bold">{t(`states.${report.status}`)}</p><p className="my-2 whitespace-pre-wrap">{report.body}</p><Link className="underline" href={`/pet-friendly/${report.place_id}`}>{t("viewRules")}</Link></article>)}
    {data.data && !data.data.items.length && !data.data.pet_reports.length && <Empty>{t("noReviewResults")}</Empty>}
  </div>;
}
