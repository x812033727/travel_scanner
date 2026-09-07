"use client";

import { useState, type FormEvent } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link } from "@/i18n/navigation";
import { localeLabels, locales } from "@/i18n/routing";
import { useHeaderSession } from "@/components/header-session";
import { api } from "@/lib/api";
import type { Page, Post, PublicProfile } from "@/lib/community/types";
import { Button, CommunityImage, Empty, ErrorNotice, fieldClass, panelClass, Tabs } from "./ui";
import { useResource } from "./use-resource";
import { useSiteVisibility } from "@/components/site-visibility-provider";
import { featureVisible } from "@/lib/site-features";

export function PostCard({ post }: { post: Post }) {
  const t = useTranslations("community");
  const locale = useLocale();
  return <article className={`${panelClass} flex min-w-0 flex-col gap-3`}>
    {post.media[0] && <Link href={`/community/posts/${post.id}`} tabIndex={-1} aria-hidden><CommunityImage id={post.media[0].id} alt={post.media[0].alt || post.title} thumbnail /></Link>}
    <div className="flex flex-wrap items-center gap-2 text-xs text-[var(--muted)]"><span>{post.destination}</span>{post.featured && <span className="rounded-full bg-[var(--teal-soft)] px-2 py-1 text-[var(--teal)]">{t("officialSelection")}</span>}</div>
    <h2 className="text-xl font-bold"><Link href={`/community/posts/${post.id}`} className="hover:underline">{post.title}</Link></h2>
    <p className="line-clamp-3 whitespace-pre-wrap break-words text-sm leading-6 text-[var(--muted)]">{post.body}</p>
    <Link href={`/community/profiles/${post.author.handle}`} className="mt-auto text-sm font-semibold text-[var(--teal)]">{post.author.display_name}</Link>
    <div className="flex flex-wrap gap-3 text-xs text-[var(--muted)]"><span>{t("likes", { count: post.likes })}</span><span>{t("saves", { count: post.saves })}</span>{post.published_at && <time dateTime={post.published_at}>{new Intl.DateTimeFormat(locale, { dateStyle: "medium" }).format(new Date(post.published_at))}</time>}</div>
    {post.itinerary && <p className="text-xs font-semibold">{t("publicItineraryDays", { count: post.itinerary.days })}</p>}
  </article>;
}

export function Feed({ author, saved = false, compact = false, query = "" }: { author?: string; saved?: boolean; compact?: boolean; query?: string }) {
  const t = useTranslations("community");
  const { user } = useHeaderSession();
  const [mode, setMode] = useState(compact ? "recommended" : "latest");
  const [draft, setDraft] = useState({ destination: "", locale: "", topic: "" });
  const [filters, setFilters] = useState(draft);
  const search = new URLSearchParams({ mode: saved ? "saved" : author ? "latest" : mode, limit: compact ? "4" : "12", ...filters });
  if (author) search.set("author", author);
  if (query) search.set("q", query);
  const path = `/community/feed?${search}`;
  const { data, error, loading } = useResource<Page<Post>>(mode === "following" && !user ? null : path);
  const [extra, setExtra] = useState<Post[]>([]);
  const [cursor, setCursor] = useState<string | number | null>();
  const [moreError, setMoreError] = useState<unknown>();
  const [busy, setBusy] = useState(false);
  const [loaded, setLoaded] = useState(data);
  if (loaded !== data) { setLoaded(data); setExtra([]); setCursor(data?.next_cursor); }
  async function more() {
    if (!cursor) return;
    setBusy(true); setMoreError(undefined);
    try {
      const page = await api<Page<Post>>(`${path}&cursor=${encodeURIComponent(cursor)}`);
      setExtra((previous) => [...previous, ...page.items]); setCursor(page.next_cursor);
    } catch (reason) { setMoreError(reason); } finally { setBusy(false); }
  }
  const posts = [...new Map([...(data?.items || []), ...extra].map((post) => [post.id, post])).values()];
  const content = <div className="space-y-5">
    {!compact && <form className="grid items-end gap-3 rounded-2xl bg-[var(--paper)] p-4 sm:grid-cols-4" onSubmit={(e) => { e.preventDefault(); setFilters(draft); }}>
      <label className="text-sm font-semibold">{t("destination")}<input className={fieldClass} maxLength={160} value={draft.destination} onChange={(e) => setDraft({ ...draft, destination: e.target.value })} /></label>
      <label className="text-sm font-semibold">{t("contentLanguage")}<select className={fieldClass} value={draft.locale} onChange={(e) => setDraft({ ...draft, locale: e.target.value })}><option value="">{t("allLanguages")}</option>{locales.map((locale) => <option key={locale} value={locale}>{localeLabels[locale]}</option>)}</select></label>
      <label className="text-sm font-semibold">{t("topic")}<input className={fieldClass} maxLength={40} value={draft.topic} onChange={(e) => setDraft({ ...draft, topic: e.target.value })} /></label>
      <Button type="submit">{t("filter")}</Button>
    </form>}
    {mode === "following" && !user ? <Empty><Link href="/login">{t("loginRequired")}</Link></Empty> : loading && !data ? <Empty>{t("loading")}</Empty> : <>
      <ErrorNotice error={error} />
      {!error && !posts.length && <Empty>{t("noPosts")}</Empty>}
      <div className={`grid gap-5 ${compact ? "sm:grid-cols-2 lg:grid-cols-4" : "md:grid-cols-2"}`}>{posts.map((post) => <PostCard key={post.id} post={post} />)}</div>
      <ErrorNotice error={moreError} />{cursor && !compact && <Button secondary disabled={busy} onClick={() => void more()}>{t("loadMore")}</Button>}
    </>}
  </div>;
  if (compact || author || saved) return content;
  return <Tabs value={mode} onChange={setMode} label={t("feed")} items={["recommended", "latest", "following"].map((value) => ({ value, label: t(value) }))}>{content}</Tabs>;
}

export function CommunitySearch() {
  const visibility = useSiteVisibility();
  const t = useTranslations("community");
  const [draft, setDraft] = useState("");
  const [query, setQuery] = useState("");
  const [tab, setTab] = useState("posts");
  function submit(e: FormEvent) { e.preventDefault(); setQuery(draft); }
  const profiles = useResource<Page<PublicProfile>>(tab === "authors" ? `/community/search/profiles?q=${encodeURIComponent(query)}` : null);
  const places = useResource<Page<{ id:string; kind:string; name:string; destination:string; href:string }>>(tab === "places" ? `/community/search/places?q=${encodeURIComponent(query)}` : null);
  return <div className="space-y-6"><form onSubmit={submit} className="flex flex-wrap items-end gap-3"><label className="min-w-0 flex-1 font-semibold">{t("search")}<input type="search" value={draft} maxLength={160} className={fieldClass} onChange={(e) => setDraft(e.target.value)} /></label><Button type="submit">{t("search")}</Button></form>
    <p className="text-sm text-[var(--muted)]">{t("searchScope")}</p>
    <Tabs value={tab} onChange={setTab} label={t("search")} items={["posts", "authors", "places"].map((value) => ({ value, label: t(value) }))}>
      {tab === "posts" && <Feed query={query} />}
      {tab === "authors" && <div className="grid gap-3"><ErrorNotice error={profiles.error} />{profiles.data?.items.map((profile) => <Link key={profile.id} className={panelClass} href={`/community/profiles/${profile.handle}`}><strong>{profile.display_name}</strong><span className="ml-3 text-[var(--muted)]">@{profile.handle}</span></Link>)}{profiles.data?.items.length === 0 && <Empty>{t("noResults")}</Empty>}</div>}
      {tab === "places" && <div className="grid gap-3"><ErrorNotice error={places.error} />{places.data?.items.filter((place) => place.kind !== "hotspot" || featureVisible(visibility, "hotspots")).map((place) => <Link key={place.kind + place.id} className={panelClass} href={place.href}><strong>{place.name}</strong><span className="ml-3 text-[var(--muted)]">{place.destination}</span></Link>)}{places.data?.items.length === 0 && <Empty>{t("noResults")}</Empty>}</div>}
    </Tabs></div>;
}
