"use client";

import { useCallback, useEffect, useRef, useState } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link, useRouter } from "@/i18n/navigation";
import { localeLabels, locales } from "@/i18n/routing";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";
import { api } from "@/lib/api";
import type { Media, Page, Post } from "@/lib/community/types";
import { useCommunity } from "./provider";
import { ImageUpload } from "./upload";
import { ItineraryPreview } from "./post";
import { Button, CommunityImage, Dialog, Empty, ErrorNotice, fieldClass, panelClass } from "./ui";
import { useResource } from "./use-resource";

type Draft = { title: string; body: string; locale: string; destination: string; kind: Post["kind"];
  topics: string; place_ids: string; media: Media[]; source_trip_id: string;
  keep_itinerary: boolean; allow_fork: boolean };
type TripOption = { id: string; name: string; start_date: string; end_date: string; version: number };

export function PostEditor({ id }: { id?: string }) {
  const t = useTranslations("community");
  const locale = useLocale();
  const router = useRouter();
  const { flags } = useCommunity();
  const visibility = useSiteVisibility();
  const trips = useResource<TripOption[]>(featureVisible(visibility, "trips") ? "/trips" : null);
  const initial = useResource<Post>(id ? `/community/posts/${id}/draft` : null);
  const [draft, setDraft] = useState<Draft>({ title: "", body: "", locale, destination: "", kind: "story", topics: "", place_ids: "", media: [], source_trip_id: "", keep_itinerary: false, allow_fork: false });
  const latest = useRef(draft);
  const record = useRef<Post | null>(null);
  const saving = useRef<Promise<Post> | null>(null);
  const savedSnapshot = useRef(JSON.stringify(draft));
  const initialized = useRef(!id);
  const [ready, setReady] = useState(!id);
  const alive = useRef(true);
  const [status, setStatus] = useState("draft");
  const [busy, setBusy] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<unknown>();
  const [preview, setPreview] = useState<Post>();
  const [confirmed, setConfirmed] = useState(false);
  useEffect(() => { alive.current = true; return () => { alive.current = false; }; }, []);
  useEffect(() => {
    if (initialized.current || !initial.data) return;
    const post = initial.data;
    const next: Draft = { title: post.title, body: post.body, locale: post.locale, destination: post.destination,
      kind: post.kind, topics: post.topics.join(", "), place_ids: post.place_ids.join(", "), media: post.media,
      source_trip_id: "", keep_itinerary: Boolean(post.itinerary), allow_fork: post.allow_fork };
    latest.current = next; record.current = post; savedSnapshot.current = JSON.stringify(next);
    setDraft(next); setStatus(post.state || "draft"); initialized.current = true; setReady(true);
  }, [initial.data]);
  function change<K extends keyof Draft>(key: K, value: Draft[K]) {
    const next = { ...latest.current, [key]: value };
    latest.current = next; setDraft(next); setStatus("unsaved");
    if (["source_trip_id", "keep_itinerary", "allow_fork"].includes(key)) setConfirmed(false);
  }
  const save = useCallback(async (): Promise<Post> => {
    if (saving.current) {
      await saving.current;
      if (savedSnapshot.current === JSON.stringify(latest.current) && record.current) return record.current;
    }
    const value = latest.current;
    const snapshot = JSON.stringify(value);
    if (snapshot === savedSnapshot.current && record.current) return record.current;
    setStatus("saving"); setError(undefined);
    const payload = { title: value.title, body: value.body, locale: value.locale, destination: value.destination,
      kind: value.kind, topics: value.topics.split(",").map((item) => item.trim()).filter(Boolean),
      place_ids: value.place_ids.split(",").map((item) => item.trim()).filter(Boolean),
      media_ids: value.media.map((media) => media.id), source_trip_id: value.source_trip_id || null,
      keep_itinerary: value.keep_itinerary, allow_fork: value.allow_fork,
      ...(record.current ? { version: record.current.version } : {}) };
    const request = api<Post>(record.current ? `/community/posts/${record.current.id}` : "/community/posts", {
      method: record.current ? "PUT" : "POST", body: JSON.stringify(payload),
    });
    saving.current = request;
    try {
      const post = await request;
      record.current = post;
      // Once copied, retain the independent public snapshot. Subsequent text edits must
      // not silently re-read changed private trip details.
      const saved = value.source_trip_id
        ? { ...value, source_trip_id: "", keep_itinerary: Boolean(post.itinerary) }
        : value;
      savedSnapshot.current = JSON.stringify(saved);
      if (value.source_trip_id && latest.current.source_trip_id === value.source_trip_id &&
          latest.current.keep_itinerary === value.keep_itinerary) {
        latest.current = { ...latest.current, source_trip_id: "", keep_itinerary: Boolean(post.itinerary) };
        if (alive.current) setDraft(latest.current);
      }
      if (alive.current) setStatus(savedSnapshot.current === JSON.stringify(latest.current) ? "saved" : "unsaved");
      return post;
    } catch (reason) { if (alive.current) { setError(reason); setStatus("unsaved"); } throw reason; }
    finally { saving.current = null; }
  }, []);
  useEffect(() => {
    if (!initialized.current || savedSnapshot.current === JSON.stringify(draft) || !flags.posting_enabled) return;
    const timer = window.setTimeout(() => { void save().catch(() => {}); }, 1200);
    return () => window.clearTimeout(timer);
  }, [draft, save, flags.posting_enabled]);
  useEffect(() => {
    const warn = (event: BeforeUnloadEvent) => { if (savedSnapshot.current !== JSON.stringify(latest.current) || saving.current) { event.preventDefault(); event.returnValue = ""; } };
    window.addEventListener("beforeunload", warn);
    return () => window.removeEventListener("beforeunload", warn);
  }, []);
  async function action(publish: boolean) {
    setBusy(true); setError(undefined);
    try {
      const post = await save();
      if (!publish) { setPreview(post); return; }
      const published = await api<Post>(`/community/posts/${post.id}/publish`, { method: "POST", body: JSON.stringify({ version: post.version }) });
      record.current = published; setStatus(published.pending_revision_id ? "pending" : "published");
      router.replace(`/community/posts/${post.id}/edit`);
    } catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  if (initial.error) return <ErrorNotice error={initial.error} />;
  if (!ready) return <Empty>{t("loading")}</Empty>;
  const hasItinerary = Boolean(draft.source_trip_id || draft.keep_itinerary);
  return <div className="space-y-5"><p className="rounded-xl bg-[var(--paper)] p-4 text-sm leading-6">{t("moderationNotice")}</p>
    <fieldset disabled={!flags.posting_enabled || busy} className={`${panelClass} space-y-5`}>
      <label className="block font-semibold">{t("postTitle")}<input maxLength={160} className={fieldClass} value={draft.title} onChange={(e) => change("title", e.target.value)} /></label>
      <div className="grid gap-4 sm:grid-cols-3"><label className="font-semibold">{t("destination")}<input className={fieldClass} maxLength={160} value={draft.destination} onChange={(e) => change("destination", e.target.value)} /></label>
        <label className="font-semibold">{t("contentLanguage")}<select className={fieldClass} value={draft.locale} onChange={(e) => change("locale", e.target.value)}>{locales.map((value) => <option key={value} value={value}>{localeLabels[value]}</option>)}</select></label>
        <label className="font-semibold">{t("postKind")}<select className={fieldClass} value={draft.kind} onChange={(e) => change("kind", e.target.value as Draft["kind"])}>{["story", "guide", "pet_visit"].map((value) => <option key={value} value={value}>{t(`kinds.${value}`)}</option>)}</select></label>
      </div>
      <label className="block font-semibold">{t("postBody")}<textarea rows={12} maxLength={20000} className={fieldClass} value={draft.body} onChange={(e) => change("body", e.target.value)} /></label>
      <label className="block font-semibold">{t("topics")}<input className={fieldClass} value={draft.topics} onChange={(e) => change("topics", e.target.value)} /><span className="text-sm font-normal">{t("topicsHelp")}</span></label>
      <ImageUpload images={draft.media} onChange={(images) => change("media", images)} onBusyChange={setUploading} />
      <label className="block font-semibold">{t("relatedPlaceIds")}<input className={fieldClass} value={draft.place_ids} onChange={(e) => change("place_ids", e.target.value)} /><span className="text-sm font-normal">{t("placeIdsHelp")}</span></label>
      {featureVisible(visibility, "trips") && <section className="space-y-3 border-t border-[var(--line)] pt-4"><h2 className="text-xl font-bold">{t("publicItinerary")}</h2><p className="text-sm leading-6 text-[var(--muted)]">{t("itineraryPrivacy")}</p>
        <label className="block font-semibold">{t("sourceTrip")}<select className={fieldClass} value={draft.source_trip_id} onChange={(e) => change("source_trip_id", e.target.value)}><option value="">{draft.keep_itinerary ? t("keepSnapshot") : t("noItinerary")}</option>{trips.data?.map((trip) => <option key={trip.id} value={trip.id}>{trip.name}</option>)}</select></label>
        <ErrorNotice error={trips.error} />
        {draft.keep_itinerary && <Button secondary onClick={() => { change("keep_itinerary", false); change("source_trip_id", ""); change("allow_fork", false); }}>{t("removeItinerary")}</Button>}
        {hasItinerary && <label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={draft.allow_fork} onChange={(e) => change("allow_fork", e.target.checked)} />{t("allowFork")}</label>}
      </section>}
    </fieldset>
    <ErrorNotice error={error} /><p role="status" className="text-sm text-[var(--muted)]">{t(`states.${status}`)}</p>
    <div className="flex flex-wrap gap-3"><Button secondary disabled={busy || uploading || !flags.posting_enabled} onClick={() => void save().catch(() => {})}>{t("saveDraft")}</Button><Button secondary disabled={busy || uploading || !flags.posting_enabled} onClick={() => void action(false)}>{t("preview")}</Button><Button disabled={busy || uploading || !flags.posting_enabled || !draft.title || !draft.body || !draft.destination || (hasItinerary && !confirmed)} onClick={() => void action(true)}>{t("publish")}</Button><Link href="/community/drafts" className="rounded-xl px-3 py-2.5 underline">{t("drafts")}</Link></div>
    {hasItinerary && <p className="text-sm">{t("previewRequired")}</p>}
    {preview && <Dialog title={t("preview")} onClose={() => setPreview(undefined)}><div className="space-y-5"><h2 className="text-2xl font-bold">{preview.title}</h2><p className="whitespace-pre-wrap break-words">{preview.body}</p>{preview.media.map((media) => <CommunityImage key={media.id} id={media.id} alt={media.alt} />)}{preview.itinerary && <ItineraryPreview itinerary={preview.itinerary} />}{preview.itinerary && <label className="flex items-start gap-3"><input type="checkbox" checked={confirmed} onChange={(e) => setConfirmed(e.target.checked)} />{t("confirmPublicSnapshot")}</label>}</div></Dialog>}
  </div>;
}

export function Drafts() {
  const t = useTranslations("community");
  const resource = useResource<Page<Post>>("/community/drafts");
  const [error, setError] = useState<unknown>();
  async function remove(post: Post, withdraw: boolean) {
    if (!window.confirm(t(withdraw ? "withdrawConfirm" : "deleteConfirm"))) return;
    try { await api(`/community/posts/${post.id}${withdraw ? "/withdraw" : ""}`, { method: withdraw ? "POST" : "DELETE" }); await resource.reload(); }
    catch (reason) { setError(reason); }
  }
  return <div className="space-y-4"><ErrorNotice error={error || resource.error} />{resource.data?.items.length === 0 && <Empty>{t("noDrafts")}</Empty>}{resource.data?.items.map((post) => <article key={post.id} className={`${panelClass} flex flex-wrap items-center justify-between gap-4`}><div><h2 className="font-bold">{post.title || t("untitled")}</h2><p className="mt-1 text-sm text-[var(--muted)]">{t(`states.${post.pending_revision_id ? "pending" : post.state || "draft"}`)}</p></div><div className="flex flex-wrap gap-2"><Link href={`/community/posts/${post.id}/edit`} className="rounded-xl border border-[var(--line)] px-4 py-2.5">{t("edit")}</Link>{post.state === "published" && <Button secondary onClick={() => void remove(post, true)}>{t("withdraw")}</Button>}<Button secondary onClick={() => void remove(post, false)}>{t("delete")}</Button></div></article>)}</div>;
}
