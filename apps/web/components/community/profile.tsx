"use client";

import { useState, type FormEvent } from "react";
import { useLocale, useTranslations } from "next-intl";
import { Link, useRouter } from "@/i18n/navigation";
import { localeLabels, locales, type Locale } from "@/i18n/routing";
import { useHeaderSession } from "@/components/header-session";
import { api } from "@/lib/api";
import type { PublicProfile, Media } from "@/lib/community/types";
import { useCommunity } from "./provider";
import { Button, CommunityImage, Empty, ErrorNotice, fieldClass, panelClass } from "./ui";
import { ImageUpload } from "./upload";
import { useResource } from "./use-resource";
import { Feed } from "./feed";
import { ReportButton } from "./post";

export function ProfileEditor() {
  const t = useTranslations("community");
  const locale = useLocale();
  const { user, status } = useHeaderSession();
  const { me, refresh, loading } = useCommunity();
  const [form, setForm] = useState({ handle: "", display_name: "", bio: "", languages: [locale], destinations: [] as string[], avatar_id: null as string | null });
  const [images, setImages] = useState<Media[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  const [saved, setSaved] = useState(false);
  const [loaded, setLoaded] = useState<PublicProfile | null>();
  if (loaded !== me?.profile) {
    setLoaded(me?.profile);
    if (me?.profile) {
      const { handle, display_name, bio, languages, destinations, avatar_id } = me.profile;
      setForm({ handle, display_name, bio, languages, destinations, avatar_id });
      setImages(avatar_id ? [{ id: avatar_id, alt: display_name, width: 1, height: 1 }] : []);
    }
  }
  async function submit(e: FormEvent) {
    e.preventDefault(); setBusy(true); setError(undefined); setSaved(false);
    try { await api("/community/me", { method: "PUT", body: JSON.stringify({ ...form, avatar_id: images[0]?.id || null }) }); await refresh(); setSaved(true); }
    catch (reason) { setError(reason); } finally { setBusy(false); }
  }
  if (loading || status === "loading") return <Empty>{t("loading")}</Empty>;
  if (!user) return <Empty><Link href="/login">{t("loginRequired")}</Link></Empty>;
  return <form onSubmit={submit} className={`${panelClass} space-y-5`}>
    <p className="rounded-xl bg-[var(--paper)] p-4 text-sm leading-6">{t("profilePrivacy")}</p>
    <label className="block font-semibold">{t("handle")}<input required pattern="[a-z][a-z0-9_]{2,29}" maxLength={30} disabled={Boolean(me?.profile)} className={fieldClass} value={form.handle} onChange={(e) => setForm({ ...form, handle: e.target.value })} /><span className="text-sm font-normal text-[var(--muted)]">{t("handleHelp")}</span></label>
    <label className="block font-semibold">{t("displayName")}<input required maxLength={80} className={fieldClass} value={form.display_name} onChange={(e) => setForm({ ...form, display_name: e.target.value })} /></label>
    <label className="block font-semibold">{t("bio")}<textarea maxLength={1000} rows={3} className={fieldClass} value={form.bio} onChange={(e) => setForm({ ...form, bio: e.target.value })} /></label>
    <fieldset><legend className="mb-2 font-semibold">{t("languages")}</legend><div className="flex flex-wrap gap-4">{locales.map((value) => <label key={value} className="inline-flex min-h-11 items-center gap-2"><input type="checkbox" checked={form.languages.includes(value)} onChange={(e) => setForm({ ...form, languages: e.target.checked ? [...form.languages, value] : form.languages.filter((item) => item !== value) })} />{localeLabels[value]}</label>)}</div></fieldset>
    <label className="block font-semibold">{t("destinations")}<input className={fieldClass} value={form.destinations.join(", ")} onChange={(e) => setForm({ ...form, destinations: e.target.value.split(",").map((value) => value.trim()).filter(Boolean).slice(0, 10) })} /><span className="text-sm font-normal">{t("commaSeparated")}</span></label>
    {me?.profile && me.verified && <ImageUpload images={images} onChange={setImages} max={1} />}
    <ErrorNotice error={error} />{saved && <p role="status">{t("saved")}</p>}<Button type="submit" disabled={busy}>{busy ? t("saving") : t("save")}</Button>
  </form>;
}

export function BlockedProfiles() {
  const t = useTranslations("community");
  const { me } = useCommunity();
  const resource = useResource<{items: PublicProfile[]}>(me?.profile ? "/community/blocks" : null);
  const [error, setError] = useState<unknown>();
  async function unblock(id: string) {
    try { await api(`/community/profiles/${id}/block`, {method:"DELETE"}); await resource.reload(); }
    catch (reason) { setError(reason); }
  }
  if (!me?.profile) return null;
  return <section className="mt-6 space-y-3"><h2 className="text-xl font-bold">{t("blockedMembers")}</h2>
    <p className="text-sm">{t("blockWarning")}</p><ErrorNotice error={error || resource.error} />
    {resource.data?.items.map((profile) => <div key={profile.id} className={`${panelClass} flex items-center justify-between gap-3`}><span>{profile.display_name} · @{profile.handle}</span><Button secondary onClick={() => void unblock(profile.id)}>{t("unblock")}</Button></div>)}
  </section>;
}

export function ProfileView({ handle }: { handle: string }) {
  const t = useTranslations("community");
  const { user } = useHeaderSession();
  const { me } = useCommunity();
  const router = useRouter();
  const { data: profile, error, reload } = useResource<PublicProfile>(`/community/profiles/${encodeURIComponent(handle)}`);
  const [busy, setBusy] = useState(false);
  const [actionError, setActionError] = useState<unknown>();
  async function action(kind: "follow" | "block" | "message") {
    if (!profile) return;
    setBusy(true); setActionError(undefined);
    try {
      if (kind === "message") {
        const result = await api<{ id: string }>(`/community/conversations/${profile.id}`, { method: "POST" });
        router.push(`/community/messages?conversation=${result.id}`);
      } else {
        await api(`/community/profiles/${profile.id}/${kind}`, { method: kind === "follow" && profile.following ? "DELETE" : "PUT" });
        if (kind === "block") router.push("/community"); else await reload();
      }
    } catch (reason) { setActionError(reason); } finally { setBusy(false); }
  }
  if (error) return <ErrorNotice error={error} />;
  if (!profile) return <Empty>{t("loading")}</Empty>;
  return <div className="space-y-6"><section className={`${panelClass} space-y-4`}>
    {profile.avatar_id && <div className="w-24"><CommunityImage id={profile.avatar_id} alt={profile.display_name} thumbnail /></div>}
    <div><h1 className="text-3xl font-bold">{profile.display_name}</h1><p className="mt-1 text-[var(--muted)]">@{profile.handle}</p></div>
    <p className="whitespace-pre-wrap break-words">{profile.bio}</p>
    <p>{profile.languages.map((lang) => localeLabels[lang as Locale] || lang).join(" · ")}</p>
    <p>{t("followers", { count: profile.followers || 0 })}</p>
    {user?.id === profile.id ? <Link href="/community/settings" className="underline">{t("editProfile")}</Link> : <div className="flex flex-wrap gap-3">
      <Button disabled={busy || !me?.verified} onClick={() => void action("follow")}>{profile.following ? t("unfollow") : t("follow")}</Button>
      <Button secondary disabled={busy || !profile.can_message || !me?.verified} onClick={() => void action("message")}>{t("message")}</Button>
      <Button secondary disabled={busy || !me?.verified} onClick={() => { if (window.confirm(t("blockWarning"))) void action("block"); }}>{t("block")}</Button>
    </div>}
    <ReportButton kind="profile" target={profile.id} /><p className="text-sm text-[var(--muted)]">{t("mutualOnly")}</p><ErrorNotice error={actionError} />
  </section><Feed author={profile.id} /></div>;
}
