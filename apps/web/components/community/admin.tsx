"use client";
import { useState, type FormEvent, type ReactNode } from "react";
import { useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { api } from "@/lib/api";
import type { Page, Post, PublicProfile } from "@/lib/community/types";
import { useCommunity } from "./provider";
import { Button, CommunityImage, Dialog, Empty, ErrorNotice, fieldClass, panelClass, Tabs } from "./ui";
import { ItineraryPreview } from "./post";
import { RelatedPlaces } from "./places";
import { useResource } from "./use-resource";

export function AdminGate({ children }: { children: ReactNode }) {
 const { user, status } = useHeaderSession();
 const t = useTranslations("community");
 if (status === "loading") return <Empty>{t("loading")}</Empty>;
 return user?.is_admin ? children : <Empty>{t("adminRequired")}</Empty>;
}
export function ReasonAction({ title, onSubmit, onClose }: { title: string; onSubmit: (reason: string) => Promise<void>; onClose: () => void }) {
 const t = useTranslations("community");
 const [reason, setReason] = useState("");
 const [busy, setBusy] = useState(false);
 const [error, setError] = useState<unknown>();
 async function submit(e: FormEvent) { e.preventDefault(); setBusy(true); try { await onSubmit(reason); onClose(); } catch (error) { setError(error); } finally { setBusy(false); } }
 return <Dialog title={title} onClose={onClose}><form onSubmit={submit} className="space-y-4"><label className="block font-semibold">{t("reason")}<textarea required minLength={3} maxLength={1000} rows={3} className={fieldClass} value={reason} onChange={(e) => setReason(e.target.value)} /></label><ErrorNotice error={error} /><Button type="submit" disabled={busy}>{t("confirm")}</Button></form></Dialog>;
}
export function CommunityAdmin() {
 const t = useTranslations("community");
 const [tab, setTab] = useState("posts");
 return <AdminGate><div className="space-y-6"><h1 className="text-3xl font-bold">{t("adminCommunity")}</h1><Tabs label={t("adminCommunity")} value={tab} onChange={setTab} items={["posts", "comments", "reports", "members", "settings", "overview"].map((value) => ({value, label:t(`adminTabs.${value}`)}))}>
 {tab === "posts" && <PostReview />}{tab === "comments" && <CommentReview />}{tab === "reports" && <ReportReview />}{tab === "members" && <MemberReview />}{tab === "settings" && <CommunitySettings />}{tab === "overview" && <CommunityOverview />}
 </Tabs></div></AdminGate>;
}
function PostReview() {
 const t = useTranslations("community");
 const [state, setState] = useState("pending");
 const data = useResource<Page<Post>>(`/admin/community/posts?state=${state}`);
 const [action, setAction] = useState<{ post: Post; action: string }>();
 return <div className="space-y-4"><label className="block max-w-xs font-semibold">{t("status")}<select className={fieldClass} value={state} onChange={(e) => setState(e.target.value)}>{["pending","published","hidden"].map((key) => <option key={key} value={key}>{t(`states.${key}`)}</option>)}</select></label><ErrorNotice error={data.error} />{data.data?.items.length === 0 && <Empty>{t("queueEmpty")}</Empty>}{data.data?.items.map((post) => <article key={post.id} className={`${panelClass} space-y-4`}><header><h2 className="text-xl font-bold">{post.title}</h2><p className="text-sm">{post.author.display_name} · @{post.author.handle} · {post.locale}</p></header><p className="whitespace-pre-wrap break-words">{post.body}</p><div className="grid grid-cols-2 gap-3">{post.media.map((media) => <CommunityImage key={media.id} id={media.id} alt={media.alt} review />)}</div><RelatedPlaces places={post.places || []} />{post.itinerary && <ItineraryPreview itinerary={post.itinerary} />}<div className="flex flex-wrap gap-2">{(state === "pending" ? ["approve","return"] : state === "hidden" ? ["restore"] : ["hide", post.featured ? "unfeature" : "feature"]).map((key) => <Button key={key} secondary onClick={() => setAction({ post, action:key })}>{t(`actions.${key}`)}</Button>)}</div></article>)}
 {action && <ReasonAction title={t(`actions.${action.action}`)} onClose={() => setAction(undefined)} onSubmit={async (reason) => { await api(`/admin/community/posts/${action.post.id}`, {method:"PUT", body:JSON.stringify({ action:action.action, version:action.post.version, reason })}); await data.reload(); }} />}</div>;
}
function CommentReview() {
 const t = useTranslations("community");
 const [hidden, setHidden] = useState(true);
 const data = useResource<Page<{id:string; post_id:string; body:string; hidden:boolean}>>(`/admin/community/comments?hidden=${hidden}`);
 const [selected, setSelected] = useState<string>();
 return <div className="space-y-4"><label className="flex min-h-11 items-center gap-2"><input type="checkbox" checked={hidden} onChange={(e) => setHidden(e.target.checked)} />{t("pendingComments")}</label><ErrorNotice error={data.error} />{data.data?.items.length === 0 && <Empty>{t("queueEmpty")}</Empty>}{data.data?.items.map((row) => <article key={row.id} className={`${panelClass} space-y-3`}><p className="whitespace-pre-wrap break-words">{row.body}</p><Link href={`/community/posts/${row.post_id}`} className="mr-3 underline">{t("viewPost")}</Link><Button secondary onClick={() => setSelected(row.id)}>{t(hidden ? "actions.approve" : "actions.hide")}</Button></article>)}
 {selected && <ReasonAction title={t(hidden ? "actions.approve" : "actions.hide")} onClose={() => setSelected(undefined)} onSubmit={async (reason) => { await api(`/admin/community/comments/${selected}`, {method:"PUT", body:JSON.stringify({hidden:!hidden,reason})}); await data.reload(); }} />}</div>;
}
type Report = {id:string;kind:string;target:string;reason:string;status:string;evidence:{body?:string;title?:string;media_ids?:string[];messages?:Array<{id:number;body:string;sender_id:string;card_post_id:string|null}>;revision_id?:string}};
function ReportReview() {
 const t = useTranslations("community");
 const [status, setStatus] = useState("pending");
 const data = useResource<Page<Report>>(`/admin/community/reports?status=${status}`);
 const [action, setAction] = useState<{id:string;status:string}>();
 return <div className="space-y-4"><p className="text-sm text-[var(--muted)]">{t("reportPrivacyNotice")}</p><label className="block max-w-xs font-semibold">{t("status")}<select className={fieldClass} value={status} onChange={(e) => setStatus(e.target.value)}>{["pending","resolved","dismissed"].map((key) => <option key={key} value={key}>{t(`states.${key}`)}</option>)}</select></label><ErrorNotice error={data.error} />{data.data?.items.length === 0 && <Empty>{t("queueEmpty")}</Empty>}{data.data?.items.map((row) => <article key={row.id} className={`${panelClass} space-y-3`}><h2 className="font-bold">{t(`reportKinds.${row.kind}`)}</h2><p className="whitespace-pre-wrap">{row.reason}</p>{row.evidence.title && <h3 className="font-bold">{row.evidence.title}</h3>}{row.evidence.media_ids?.map((id) => <CommunityImage key={id} id={id} alt={t("postPhoto")} review />)}{row.evidence.body && <blockquote className="border-l-4 border-[var(--line)] pl-3">{row.evidence.body}</blockquote>}{row.evidence.messages?.map((message) => <blockquote key={message.id} className="rounded-xl bg-[var(--paper)] p-3"><span className="text-xs">{t("message")} #{message.id}</span><p className="whitespace-pre-wrap break-words">{message.body}</p>{message.card_post_id && <Link href={`/community/posts/${message.card_post_id}`} className="underline">{t("viewPost")}</Link>}</blockquote>)}{row.kind === "post" && <Link href={`/community/posts/${row.target}`} className="underline">{t("viewPost")}</Link>}<p className="break-all text-xs text-[var(--muted)]">{t("target")}: {row.target}</p><div className="flex gap-2">{["resolved","dismissed"].map((status) => <Button key={status} secondary onClick={() => setAction({id:row.id,status})}>{t(`states.${status}`)}</Button>)}</div></article>)}
 {action && <ReasonAction title={t(`states.${action.status}`)} onClose={() => setAction(undefined)} onSubmit={async (reason) => { await api(`/admin/community/reports/${action.id}`, {method:"PUT",body:JSON.stringify({status:action.status,reason})}); await data.reload(); }} />}</div>;
}
function MemberReview() {
 const t = useTranslations("community");
 const {user} = useHeaderSession();
 const [q,setQ] = useState("");
 const [query,setQuery] = useState("");
 const data = useResource<Page<PublicProfile & {restricted:boolean;approved_posts:number}>>(`/admin/community/profiles?q=${encodeURIComponent(query)}`);
 const [selected,setSelected] = useState<{id:string;restricted:boolean}>();
 return <div className="space-y-4"><form className="flex items-end gap-3" onSubmit={(e) => {e.preventDefault();setQuery(q);}}><label className="font-semibold">{t("search")}<input className={fieldClass} maxLength={80} value={q} onChange={(e) => setQ(e.target.value)} /></label><Button type="submit">{t("search")}</Button></form><ErrorNotice error={data.error} />{data.data?.items.map((row) => <article key={row.id} className={`${panelClass} flex flex-wrap items-center justify-between gap-3`}><div><h2 className="font-bold">{row.display_name} · @{row.handle}</h2><p className="text-sm">{t("approvedPosts",{count:row.approved_posts})}</p></div><Button secondary disabled={row.id === user?.id} onClick={() => setSelected({id:row.id,restricted:!row.restricted})}>{t(row.restricted ? "restoreMember" : "restrictMember")}</Button></article>)}{selected && <ReasonAction title={t(selected.restricted ? "restrictMember" : "restoreMember")} onClose={() => setSelected(undefined)} onSubmit={async (reason) => { await api(`/admin/community/profiles/${selected.id}/restriction`,{method:"PUT",body:JSON.stringify({restricted:selected.restricted,reason})});await data.reload(); }} />}</div>;
}
type Settings = {enabled:boolean;posting_enabled:boolean;comments_enabled:boolean;messaging_enabled:boolean;translation_enabled:boolean;pet_reports_enabled:boolean;uploads_per_day:number;posts_per_day:number;interactions_per_minute:number;translation_characters_per_month:number;pet_verification_days:number;risk_terms:string[]};
function CommunitySettings() {
 const t = useTranslations("community");
 const data = useResource<{settings:Settings;sources:Record<string,string>;services:Record<string,boolean>}>("/admin/community/settings");
 const {refreshFlags} = useCommunity();
 const [form,setForm] = useState<Settings>();
 const [reason,setReason] = useState("");
 const [busy,setBusy] = useState(false);
 const [saved,setSaved] = useState(false);
 const [error,setError] = useState<unknown>();
 const [loaded, setLoaded] = useState(data.data);
 if (loaded !== data.data) { setLoaded(data.data); setForm(data.data?.settings); }
 const flags = ["enabled","posting_enabled","comments_enabled","messaging_enabled","translation_enabled","pet_reports_enabled"] as const;
 const quotas = [["uploads_per_day",1,500],["posts_per_day",1,100],["interactions_per_minute",1,200],["translation_characters_per_month",0,100000000],["pet_verification_days",1,365]] as const;
 async function submit(e:FormEvent) { e.preventDefault();setBusy(true);setError(undefined);setSaved(false);try {await api("/admin/community/settings",{method:"PUT",body:JSON.stringify({settings:{...form,risk_terms:form?.risk_terms.map((term) => term.trim()).filter(Boolean)},reason})});await data.reload();await refreshFlags();setSaved(true);}catch(error){setError(error);}finally{setBusy(false);} }
 if (!form) return data.error ? <ErrorNotice error={data.error} /> : <Empty>{t("loading")}</Empty>;
 return <form onSubmit={submit} className={`${panelClass} space-y-5`}><p className="rounded-xl bg-[var(--paper)] p-4 text-sm leading-6">{t("launchNotice")}</p><div className="grid gap-3 sm:grid-cols-2">{Object.entries(data.data?.services || {}).map(([key,value]) => <p key={key}>{t(`services.${key}`)}: {t(value ? "configured" : "notConfigured")}</p>)}</div>{flags.map((key) => <label key={key} className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={form[key]} onChange={(e) => setForm({...form,[key]:e.target.checked})} /><span>{t(`settings.${key}`)} <small className="text-[var(--muted)]">({t(`sources.${data.data?.sources[key] || "default"}`)})</small></span></label>)}<div className="grid gap-4 sm:grid-cols-2">{quotas.map(([key,min,max]) => <label key={key} className="font-semibold">{t(`settings.${key}`)}<input type="number" required min={min} max={max} step={1} className={fieldClass} value={form[key]} onChange={(e) => setForm({...form,[key]:Number(e.target.value)})} /><small className="font-normal">{min}–{max} · {t(`sources.${data.data?.sources[key] || "default"}`)}</small></label>)}</div><label className="block font-semibold">{t("settings.risk_terms")}<textarea rows={3} className={fieldClass} value={form.risk_terms.join("\n")} onChange={(e) => setForm({...form,risk_terms:e.target.value.split("\n")})} /></label><label className="block font-semibold">{t("reason")}<textarea required minLength={3} maxLength={1000} className={fieldClass} value={reason} onChange={(e) => setReason(e.target.value)} /></label><ErrorNotice error={error} />{saved && <p role="status">{t("saved")}</p>}<Button type="submit" disabled={busy}>{t("save")}</Button></form>;
}
type Audit = {id:string;actor_id:string;action:string;target:string;created_at:string;metadata:unknown};
export function AuditList({items}: {items:Audit[]}) {
 const t = useTranslations("community");
 return <div className="space-y-3">{items.map((row) => <details key={row.id} className={panelClass}><summary className="cursor-pointer break-words text-sm">{row.action} · {row.created_at}</summary><dl className="my-3 space-y-2 break-all text-sm"><dt>{t("actor")}</dt><dd>{row.actor_id}</dd><dt>{t("target")}</dt><dd>{row.target}</dd></dl><pre className="overflow-x-auto whitespace-pre-wrap break-words text-xs">{JSON.stringify(row.metadata,null,2)}</pre></details>)}</div>;
}
function CommunityOverview() {
  const t = useTranslations("community");
  const data = useResource<{
    conversion_funnel_30d: Record<string, number>; unique_users_30d: Record<string, number>;
    active_authors_30d: number; pending_posts: number; oldest_review_seconds: number;
    translation_characters_this_month: number; returning_users_30d: number;
    audit_logs: Audit[]; jobs: Array<{ kind: string; status: string; count: number }>;
  }>("/admin/community/overview");
  if (!data.data) return data.error ? <ErrorNotice error={data.error} /> : <Empty>{t("loading")}</Empty>;
  const row = data.data;
  const stages = ["read", "save", "fork", "trip_created"];
  return <div className="space-y-6">
    <section className="space-y-3">
      <h2 className="text-xl font-bold">{t("conversionFunnel")}</h2>
      <p className="text-sm text-[var(--muted)]">{t("conversionFunnelNotice")}</p>
      <ol className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">{stages.map((key, index) => {
        const count = row.conversion_funnel_30d?.[key] || 0;
        const previous = index ? row.conversion_funnel_30d?.[stages[index - 1]] || 0 : 0;
        return <li key={key} className={panelClass}>
          <h3>{t(`metrics.${key}`)}</h3><p className="mt-2 text-3xl font-bold">{count}</p>
          {index > 0 && <p className="mt-2 text-sm text-[var(--muted)]">{previous
            ? t("conversionRate", { value: Math.round(count / previous * 100) })
            : t("conversionNoBaseline")}</p>}
        </li>;
      })}</ol>
    </section>
    <p className="text-sm text-[var(--muted)]">{t("metricsNotice")}</p>
    <dl className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
      {stages.map((key) => <div key={key} className={panelClass}>
        <dt>{t(`metrics.${key}`)}</dt><dd className="mt-2 text-3xl font-bold">{row.unique_users_30d[key] || 0}</dd>
      </div>)}
      {(["active_authors_30d", "returning_users_30d", "pending_posts", "oldest_review_seconds", "translation_characters_this_month"] as const).map((key) =>
        <div key={key} className={panelClass}><dt>{t(`metrics.${key}`)}</dt><dd className="mt-2 text-3xl font-bold">{row[key] || 0}</dd></div>)}
    </dl>
    <h2 className="text-xl font-bold">{t("backgroundJobs")}</h2>
    <ul>{row.jobs.map((job) => <li key={job.kind + job.status}>
      {t.has(`jobKinds.${job.kind}`) ? t(`jobKinds.${job.kind}`) : job.kind} · {t.has(`states.${job.status}`) ? t(`states.${job.status}`) : job.status}: {job.count}
    </li>)}</ul>
    <h2 className="text-xl font-bold">{t("auditLogs")}</h2><AuditList items={row.audit_logs} />
  </div>;
}
