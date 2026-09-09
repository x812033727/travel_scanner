"use client";
import { useState, type FormEvent } from "react";
import { useLocale } from "next-intl";
import { api } from "@/lib/api";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import { useResource } from "./use-resource";
import { Button, fieldClass, panelClass, ErrorNotice } from "./ui";
type Invitation = { user_id: string; invited: boolean; version: number; updated_at: string | null };
export function CreatorInvitations() {
  const c = getDiscoveryCopy(useLocale());
  const [input, setInput] = useState("");
  const [userId, setUserId] = useState("");
  const result = useResource<{ items: Invitation[] }>(userId ? `/admin/community/creator-invitations?user_id=${encodeURIComponent(userId)}` : null);
  return <section className={`${panelClass} space-y-5`}><h2 className="text-xl font-bold">{c.invitations}</h2><p className="text-sm leading-6 text-[var(--muted)]">{c.inviteHelp}</p><form onSubmit={(event) => { event.preventDefault(); setUserId(input.trim()); }} className="flex flex-wrap items-end gap-3"><label className="min-w-0 flex-1 font-semibold">{c.userId}<input value={input} onChange={(event) => setInput(event.target.value)} required pattern="[a-fA-F0-9-]{36}" className={fieldClass} /></label><Button type="submit">{c.lookup}</Button></form><ErrorNotice error={result.error} />{result.loading && <p role="status">{c.loading}</p>}{result.data?.items.map((item) => <InvitationForm key={`${item.user_id}:${item.version}`} item={item} onSaved={() => void result.reload()} />)}</section>;
}
function InvitationForm({ item, onSaved }: { item: Invitation; onSaved: () => void }) {
  const c = getDiscoveryCopy(useLocale());
  const [invited, setInvited] = useState(item.invited);
  const [reason, setReason] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState<unknown>();
  async function submit(event: FormEvent) {
    event.preventDefault(); setBusy(true); setError(undefined);
    try { await api(`/admin/community/creator-invitations/${item.user_id}`, { method: "PUT", body: JSON.stringify({ version: item.version, invited, reason }) }); onSaved(); }
    catch (value) { setError(value); } finally { setBusy(false); }
  }
  return <form className="space-y-4" onSubmit={(event) => void submit(event)}><label className="flex min-h-11 items-center gap-3"><input type="checkbox" checked={invited} onChange={(event) => setInvited(event.target.checked)} />{c.invited}</label><label className="block font-semibold">{c.reasonLabel}<textarea required minLength={3} maxLength={1000} value={reason} onChange={(event) => setReason(event.target.value)} className={fieldClass} /></label><ErrorNotice error={error} /><Button disabled={busy} type="submit">{c.update}</Button></form>;
}
