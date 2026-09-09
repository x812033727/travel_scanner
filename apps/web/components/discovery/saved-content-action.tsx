"use client";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { useSearchParams } from "next/navigation";
import { Bookmark, Check, FolderPlus } from "lucide-react";
import { Link, usePathname, useRouter } from "@/i18n/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useSavedItems } from "@/components/saved-items-provider";
import { Button, Dialog, fieldClass } from "@/components/community/ui";
import { api } from "@/lib/api";
import { useDiscoveryResource } from "@/lib/discovery";
import { contentSavedReference, savedReference, type SavedContentItem } from "@/lib/saved-items";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import { loginPath, safeNextPath } from "@/lib/navigation";

/** One canonical save, shared by discovery and the existing place/product cards. */
export function SavedContentAction({ item, returnTo, compact = false, resumeEnabled = true }: { item: SavedContentItem; returnTo: string; compact?: boolean; resumeEnabled?: boolean }) {
  const c = getFrontendFlowCopy(useLocale());
  const session = useHeaderSession();
  const saved = useSavedItems();
  const params = useSearchParams();
  const pathname = usePathname();
  const router = useRouter();
  const ref = contentSavedReference(item);
  const [owner, setOwner] = useState(session.sessionIdentity);
  const [open, setOpen] = useState(false);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const [notice, setNotice] = useState(false);
  const current = useRef(session.sessionIdentity);
  useLayoutEffect(() => { current.current = session.sessionIdentity; }, [session.sessionIdentity]);
  if (owner !== session.sessionIdentity) { setOwner(session.sessionIdentity); setOpen(false); setBusy(false); setError(false); setNotice(false); }
  const key = ref?.key;
  const { ensureStates } = saved;
  useEffect(() => {
    if (!key || !session.user) return;
    let active = true;
    void ensureStates([key]).catch(() => { if (active) setError(true); });
    return () => { active = false; };
  }, [key, session.user, session.sessionIdentity, ensureStates]);
  if (!ref) return null;
  const state = saved.state(ref.key);
  const resume = Boolean(resumeEnabled && session.user && params.get("save_key") === ref.key);
  function clearResume() { const next = new URLSearchParams(params); next.delete("save_key"); router.replace(`${pathname}${next.size ? `?${next}` : ""}`, { scroll: false }); }
  async function save(next: boolean) {
    const identity = session.sessionIdentity;
    setBusy(true); setError(false);
    try { await saved.setSaved(ref!.type, ref!.id, next); if (current.current !== identity) return; setNotice(next); if (resume) clearResume(); }
    catch { if (current.current === identity) setError(true); }
    finally { if (current.current === identity) setBusy(false); }
  }
  const path = new URL(safeNextPath(returnTo, "/explore"), "https://local.invalid");
  path.searchParams.set("save_key", ref.key);
  // A deep link restores a confirmable card, never performs the save on mount.
  if (item.kind && ["hotspot", "food", "merchant", "hotel", "article", "video", "post", "itinerary"].includes(item.kind)) path.searchParams.set("content", `${item.kind}:${ref.id}`);
  return <div className="flex flex-wrap items-center gap-2">
    {!session.user ? <Link href={loginPath(`${path.pathname}${path.search}${path.hash}`)} className="inline-flex min-h-11 items-center gap-2 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"><Bookmark size={17} aria-hidden />{c.saveItem}</Link> : <>
      <Button secondary disabled={busy || !state || saved.status !== "authenticated"} aria-pressed={Boolean(state?.saved)} onClick={() => state?.saved ? setOpen(true) : void save(true)}>{state?.saved ? <Check size={17} aria-hidden /> : <Bookmark size={17} aria-hidden />}{state?.saved ? c.savedItem : c.saveItem}</Button>
      {state?.saved && !compact && <Button secondary onClick={() => setOpen(true)} aria-label={`${c.organize}: ${item.title}`}><FolderPlus size={17} aria-hidden />{c.organize}</Button>}
    </>}
    {notice && <div role="status" className="flex items-center gap-2 text-xs text-[var(--muted)]"><span>{c.addedSaved}</span><Button secondary disabled={busy} onClick={() => { if (!state?.collection_ids.length || window.confirm(c.confirmUnsave)) { setNotice(false); void save(false); } }}>{c.undo}</Button></div>}
    {error && <div role="alert" className="text-sm"><p>{c.error}</p><Button secondary onClick={() => { setError(false); void ensureStates([ref.key], true).catch(() => setError(true)); }}>{c.retryStates}</Button></div>}
    {resume && <Dialog title={c.confirmSave} onClose={clearResume}><p className="mb-4">{item.title}</p><Button disabled={busy || !state} onClick={() => state?.saved ? clearResume() : void save(true)}>{state?.saved ? c.unchanged : c.confirmSave}</Button></Dialog>}
    {open && session.user && <OrganizeSavedContent item={item} onClose={() => setOpen(false)} onUnsave={async () => { await save(false); setOpen(false); }} />}
  </div>;
}

export function OrganizeSavedContent({ item, onClose, onUnsave }: { item: SavedContentItem; onClose: () => void; onUnsave?: () => Promise<void> }) {
  const c = getFrontendFlowCopy(useLocale());
  const { user, sessionIdentity } = useHeaderSession();
  const saved = useSavedItems();
  const ref = contentSavedReference(item)!;
  const lists = useDiscoveryResource<{ items: Array<{ id: string; name: string }> }>("/saved-items/collections");
  const [name, setName] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const active = useRef(true);
  const requests = useRef(new Set<AbortController>());
  useEffect(() => { active.current = true; const all = requests.current; return () => { active.current = false; all.forEach((request) => request.abort()); }; }, [sessionIdentity]);
  const expected = user ? `?expected_user_id=${encodeURIComponent(user.id)}` : "";
  async function mutate(collectionId?: string, remove = false) {
    const controller = new AbortController(); requests.current.add(controller);
    setBusy(true); setError(false);
    try {
      let id = collectionId;
      if (!id) { const created = await api<{ id: string }>(`/saved-items/collections${expected}`, { method: "POST", body: JSON.stringify({ name: name.trim() }), signal: controller.signal }); id = created.id; }
      if (remove) {
        const collection = await api<{ items: Array<{ id: string; kind: string; target: string }> }>(`/saved-items/collections/${encodeURIComponent(id)}`, { signal: controller.signal });
        const membership = collection.items.find((entry) => savedReference(entry.kind, entry.target)?.key === ref.key);
        if (membership) await api(`/saved-items/collections/${encodeURIComponent(id)}/items/${encodeURIComponent(membership.id)}${expected}`, { method: "DELETE", signal: controller.signal });
      } else await api(`/saved-items/collections/${encodeURIComponent(id)}/items${expected}`, { method: "POST", body: JSON.stringify({ kind: ref.type, id: ref.id }), signal: controller.signal });
      if (controller.signal.aborted || !active.current) return;
      await saved.ensureStates([ref.key], true); saved.acceptStates([], true); setName(""); lists.reload();
    } catch { if (!controller.signal.aborted && active.current) setError(true); }
    finally { requests.current.delete(controller); if (!controller.signal.aborted && active.current) setBusy(false); }
  }
  return <Dialog title={`${c.organize}: ${item.title}`} onClose={onClose}>
    <p className="mb-4 text-sm text-[var(--muted)]">{c.private}</p>
    {lists.loading && <p role="status">{c.loading}</p>}
    {(error || Boolean(lists.error)) && <div role="alert"><p>{c.error}</p><Button secondary onClick={lists.reload}>{c.retryStates}</Button></div>}
    <div className="space-y-2">{lists.data?.items.map((list) => { const included = saved.state(ref.key)?.collection_ids.includes(list.id); return <div key={list.id} className="flex flex-wrap items-center justify-between gap-3 border-b border-[var(--line)] py-2"><span>{list.name}</span><Button secondary disabled={busy} onClick={() => void mutate(list.id, included)}>{included ? c.removeFromList : c.addToList}</Button></div>; })}</div>
    <form onSubmit={(event) => { event.preventDefault(); if (name.trim()) void mutate(); }} className="my-5 space-y-3"><label className="block text-sm font-semibold">{c.listName}<input className={fieldClass} required maxLength={80} value={name} onChange={(event) => setName(event.target.value)} /></label><Button type="submit" disabled={busy || !name.trim()}>{c.createList}</Button></form>
    {onUnsave && <Button secondary disabled={busy} onClick={() => { if (window.confirm(c.confirmUnsave)) void onUnsave(); }}>{c.removeSaved}</Button>}
  </Dialog>;
}
