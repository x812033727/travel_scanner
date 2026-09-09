"use client";
import { useEffect, useLayoutEffect, useRef, useState } from "react";
import { useLocale } from "next-intl";
import { useSearchParams } from "next/navigation";
import { useHeaderSession } from "@/components/header-session";
import { useSavedItems } from "@/components/saved-items-provider";
import { Button, Dialog, fieldClass } from "@/components/community/ui";
import { Link, useRouter } from "@/i18n/navigation";
import { getDiscoveryCopy } from "@/lib/discovery-copy";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import { useDiscoveryResource, useDiscoveryStatus, type DiscoveryItem } from "@/lib/discovery";
import { parseSavedKey, type SavedType } from "@/lib/saved-items";
import { loginPath, safeNextPath, safeExternalHref } from "@/lib/navigation";
import { api } from "@/lib/api";
import { DiscoveryCard } from "./card";
import { DiscoveryDetailBoundary } from "./detail-drawer";
import { SavedContentAction } from "./saved-content-action";
import { DiscoverySkeleton } from "./explorer";
import styles from "./discovery.module.css";

type SavedRow = { key: string; type: SavedType; id: string; saved_at: string; unavailable: boolean; discovery?: DiscoveryItem; title?: string; subtitle?: string; href?: string; map_links?: Array<{ label: string; url: string }>; collection_ids: string[] };
type SavedPage = { items: SavedRow[]; next_cursor: string | null; has_more: boolean; total: number };
type Collection = { id: string; name: string };
export function DiscoveryCollections() {
  const c = getDiscoveryCopy(useLocale()); const f = getFrontendFlowCopy(useLocale());
  const { status, user } = useHeaderSession(); const params = useSearchParams();
  return <DiscoveryDetailBoundary><main className={styles.page}><header className="mb-6"><h1 className={styles.title}>{f.allSaved}</h1><p className="mt-3 text-sm text-[var(--muted)]">{f.private}</p></header>{status === "loading" ? <DiscoverySkeleton /> : !user ? <Link href={loginPath(`/explore/collections${params.size ? `?${params}` : ""}`)} className="inline-flex min-h-11 items-center rounded-xl bg-[var(--teal)] px-5 font-semibold text-white">{c.login}</Link> : <CollectionWorkspace />}</main></DiscoveryDetailBoundary>;
}
function CollectionWorkspace() {
  const locale = useLocale(); const c = getDiscoveryCopy(locale); const f = getFrontendFlowCopy(locale);
  const { user, sessionIdentity } = useHeaderSession(); const saved = useSavedItems(); const params = useSearchParams(); const router = useRouter();
  const { enabled } = useDiscoveryStatus();
  const filter = new URLSearchParams();
  for (const key of ["type", "destination", "collection"]) if (params.get(key)) filter.set(key, params.get(key)!);
  const scope = filter.toString(); const selectedList = params.get("collection") || "";
  const [owner, setOwner] = useState(sessionIdentity); const [pages, setPages] = useState<Record<string, { cursor: string | null; previous: SavedRow[] }>>({});
  const [selected, setSelected] = useState<string[]>([]); const [selectScope, setSelectScope] = useState(scope);
  const [create, setCreate] = useState(false); const [name, setName] = useState(""); const [organize, setOrganize] = useState(false);
  const [busy, setBusy] = useState(false); const [error, setError] = useState(false);
  const ownerRef = useRef(sessionIdentity); const requests = useRef(new Set<AbortController>());
  useLayoutEffect(() => { ownerRef.current = sessionIdentity; }, [sessionIdentity]);
  useEffect(() => { const active = requests.current; return () => { active.forEach((request) => request.abort()); }; }, [sessionIdentity]);
  if (owner !== sessionIdentity) { setOwner(sessionIdentity); setPages({}); setSelected([]); setCreate(false); setName(""); setOrganize(false); setBusy(false); setError(false); }
  if (selectScope !== scope) { setSelectScope(scope); setSelected([]); }
  const page = pages[scope]; const cursor = page?.cursor;
  const path = `/saved-items/all?limit=24${scope ? `&${scope}` : ""}${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ""}`;
  const result = useDiscoveryResource<SavedPage>(path, true);
  const lists = useDiscoveryResource<{ items: Collection[] }>("/saved-items/collections");
  const destinations = useDiscoveryResource<{ destinations: Array<{ id: string; name: string }> }>(enabled ? "/discovery/suggestions?q=" : null);
  const rows = [...new Map([...(page?.previous || []), ...(result.data?.items || [])].map((item) => [item.key, item])).values()].filter((row) => saved.state(row.key)?.saved !== false);
  const keys = rows.map((row) => row.key).join("|"); const { ensureStates } = saved;
  useEffect(() => { if (keys) void ensureStates(keys.split("|")).catch(() => {}); }, [keys, ensureStates]);
  const [revision, setRevision] = useState(saved.revision);
  // Saved mutations, not read-only state probes, invalidate the listing. Keep filters.
  if (revision !== saved.revision) { setRevision(saved.revision); if (cursor) setPages((all) => ({ ...all, [scope]: { cursor: null, previous: [] } })); }
  const reload = result.reload;
  const previousRevision = useRef(saved.revision);
  useEffect(() => { if (previousRevision.current !== saved.revision) { previousRevision.current = saved.revision; reload(); } }, [saved.revision, reload]);
  const expected = user ? `?expected_user_id=${encodeURIComponent(user.id)}` : "";
  function navigate(patch: Record<string, string>) { const next = new URLSearchParams(params); for (const [key, value] of Object.entries(patch)) { if (value) next.set(key, value); else next.delete(key); } next.delete("content"); router.push(`/explore/collections${next.size ? `?${next}` : ""}`, { scroll: false }); }
  async function mutate(action: "create" | "delete" | "remove", row?: SavedRow) {
    const controller = new AbortController(); requests.current.add(controller); setBusy(true); setError(false);
    try {
      if (action === "create") { const item = await api<Collection>(`/saved-items/collections${expected}`, { method: "POST", body: JSON.stringify({ name: name.trim() }), signal: controller.signal }); if (controller.signal.aborted || ownerRef.current !== sessionIdentity) return; setCreate(false); setName(""); navigate({ collection: item.id }); }
      else if (action === "delete") { await api(`/saved-items/collections/${encodeURIComponent(selectedList)}${expected}`, { method: "DELETE", signal: controller.signal }); if (controller.signal.aborted || ownerRef.current !== sessionIdentity) return; navigate({ collection: "" }); }
      else if (row) {
        const collection = await api<{ items: Array<{ id: string; kind: string; target: string }> }>(`/saved-items/collections/${encodeURIComponent(selectedList)}`, { signal: controller.signal });
        const entry = collection.items.find((item) => parseSavedKey(`${item.kind}:${item.target}`)?.key === row.key);
        if (entry) await api(`/saved-items/collections/${encodeURIComponent(selectedList)}/items/${encodeURIComponent(entry.id)}${expected}`, { method: "DELETE", signal: controller.signal });
        if (controller.signal.aborted || ownerRef.current !== sessionIdentity) return;
        await saved.ensureStates([row.key], true);
      }
      if (controller.signal.aborted || ownerRef.current !== sessionIdentity) return;
      lists.reload(); result.reload(); setPages({});
    } catch { if (!controller.signal.aborted && ownerRef.current === sessionIdentity) setError(true); }
    finally { requests.current.delete(controller); if (!controller.signal.aborted && ownerRef.current === sessionIdentity) setBusy(false); }
  }
  async function unsave(keys: string[]) {
    if (!window.confirm(keys.length > 1 ? f.confirmRemoveSelected : f.confirmUnsave)) return;
    const identity = sessionIdentity; setBusy(true); setError(false);
    try { for (const key of keys) { if (ownerRef.current !== identity) return; const ref = parseSavedKey(key); if (ref) await saved.setSaved(ref.type, ref.id, false); } if (ownerRef.current !== identity) return; setSelected([]); setPages({}); result.reload(); }
    catch { if (ownerRef.current === identity) setError(true); } finally { if (ownerRef.current === identity) setBusy(false); }
  }
  const selectedRows = rows.filter((row) => selected.includes(row.key));
  return <div className={styles.collectionLayout}>
    <aside><nav className={styles.collectionNav} aria-label={f.manageLists}><button type="button" className={styles.chip} aria-pressed={!selectedList} onClick={() => navigate({ collection: "" })}>{f.allSaved}</button>{lists.data?.items?.map((list) => <button key={list.id} className={styles.chip} aria-pressed={selectedList === list.id} onClick={() => navigate({ collection: list.id })}>{list.name}</button>)}<Button secondary onClick={() => setCreate(true)}>{f.createList}</Button></nav></aside>
    <section className="min-w-0 space-y-5">
      <div className="flex flex-wrap items-center justify-between gap-3"><h2 className="text-xl font-bold">{selectedList ? lists.data?.items?.find((list) => list.id === selectedList)?.name || f.manageLists : f.allSaved}</h2>{typeof result.data?.total === "number" && <p className="text-sm text-[var(--muted)]">{result.data.total} {f.totalSaved}</p>}{selectedList && <Button secondary disabled={busy} onClick={() => { if (window.confirm(f.confirmDeleteList)) void mutate("delete"); }}>{f.deleteList}</Button>}</div>
      <div className="flex flex-wrap gap-3"><label className="text-sm">{getDiscoveryCopy(locale).filters}<select className={fieldClass} value={params.get("type") || "all"} onChange={(event) => navigate({ type: event.target.value === "all" ? "" : event.target.value })}><option value="all">{c.all}</option>{(["hotspot", "food", "merchant", "restaurant", "hotel", "service", "guide", "post"] as const).map((type) => <option key={type} value={type}>{type === "service" ? f.services : type === "guide" ? f.categories.guides : type === "restaurant" ? c.kinds.merchant : c.kinds[type]}</option>)}</select></label><label className="text-sm">{c.destination}<select className={fieldClass} value={params.get("destination") || ""} onChange={(event) => navigate({ destination: event.target.value })}><option value="">{c.any}</option>{destinations.data?.destinations?.map((destination) => <option key={destination.id} value={destination.id}>{destination.name}</option>)}{params.get("destination") && !destinations.data?.destinations?.some((item) => item.id === params.get("destination")) && <option value={params.get("destination")!}>{params.get("destination")}</option>}</select></label></div>
      {selected.length > 0 && <div className="flex flex-wrap items-center gap-3 rounded-xl border border-[var(--line)] bg-[var(--surface)] p-3"><span>{f.selected}: {selected.length}</span><Button secondary disabled={busy || selectedRows.some((row) => row.unavailable)} onClick={() => setOrganize(true)}>{f.addToList}</Button><Button secondary disabled={busy} onClick={() => void unsave(selected)}>{f.removeSelected}</Button></div>}
      {(error || Boolean(lists.error) || Boolean(result.error)) && <div role="alert"><p>{f.error}</p><Button secondary onClick={() => { setError(false); lists.reload(); if (cursor) setPages((all) => ({ ...all, [scope]: { cursor: null, previous: [] } })); else result.reload(); }}>{c.retry}</Button></div>}
      {result.loading && !rows.length && <DiscoverySkeleton />}
      {!result.loading && !result.error && !rows.length && <div className="rounded-xl border border-dashed border-[var(--line)] p-8 text-center"><p className="leading-7 text-[var(--muted)]">{scope ? f.emptyList : f.noSaved}</p><Link href="/explore" className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{f.unchanged}</Link></div>}
      <div className={styles.grid}>{rows.map((row) => <div key={row.key} className="min-w-0"><label className={styles.selection}><input type="checkbox" checked={selected.includes(row.key)} onChange={(event) => setSelected((all) => event.target.checked ? [...all, row.key] : all.filter((key) => key !== row.key))} />{f.select}: {row.title || row.discovery?.title || f.unavailable}</label>{row.discovery && !row.unavailable ? <DiscoveryCard item={row.discovery} /> : <article className="space-y-3 rounded-xl border border-[var(--line)] bg-[var(--surface)] p-5"><h3 className="font-bold">{row.title || f.unavailable}</h3>{row.unavailable ? <p className="text-sm text-[var(--muted)]">{f.unavailable}</p> : <><p>{row.subtitle}</p>{row.href && <Link href={safeNextPath(row.href, "/explore")} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{c.details}</Link>}{row.map_links?.map((map) => { const url = safeExternalHref(map.url); return url ? <a key={url} href={url} target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center pr-3 text-[var(--teal)] underline">{map.label || f.map}</a> : null; })}<SavedContentAction item={{ type: row.type, id: row.id, title: row.title || f.savedItem }} returnTo={`/explore/collections${params.size ? `?${params}` : ""}`} /></>}<Button secondary disabled={busy} onClick={() => void unsave([row.key])}>{f.removeSaved}</Button></article>}{selectedList && <Button secondary disabled={busy} onClick={() => void mutate("remove", row)}>{f.removeFromList}</Button>}</div>)}</div>
      {result.data?.next_cursor && <div className="flex justify-center"><Button secondary disabled={result.loading} onClick={() => setPages((all) => ({ ...all, [scope]: { cursor: result.data!.next_cursor, previous: rows } }))}>{c.more}</Button></div>}
    </section>
    {create && <Dialog title={f.createList} onClose={() => setCreate(false)}><form onSubmit={(event) => { event.preventDefault(); if (name.trim()) void mutate("create"); }}><label className="font-semibold">{f.listName}<input className={fieldClass} required maxLength={80} value={name} onChange={(event) => setName(event.target.value)} /></label><Button type="submit" disabled={busy || !name.trim()}>{f.createList}</Button></form></Dialog>}
    {organize && <BatchOrganize rows={selectedRows} lists={lists.data?.items || []} onClose={() => setOrganize(false)} onSaved={() => { setOrganize(false); setSelected([]); result.reload(); }} />}
  </div>;
}
function BatchOrganize({ rows, lists, onClose, onSaved }: { rows: SavedRow[]; lists: Collection[]; onClose: () => void; onSaved: () => void }) {
  const f = getFrontendFlowCopy(useLocale()); const { user, sessionIdentity } = useHeaderSession(); const saved = useSavedItems();
  const [id, setId] = useState(""); const [busy, setBusy] = useState(false); const [error, setError] = useState(false);
  const controller = useRef<AbortController | null>(null);
  useEffect(() => () => controller.current?.abort(), [sessionIdentity]);
  async function add() {
    const request = new AbortController(); controller.current = request; setBusy(true); setError(false);
    try { for (const row of rows) { if (request.signal.aborted) return; await api(`/saved-items/collections/${encodeURIComponent(id)}/items?expected_user_id=${encodeURIComponent(user!.id)}`, { method: "POST", body: JSON.stringify({ kind: row.type, id: row.id }), signal: request.signal }); } if (request.signal.aborted) return; await saved.ensureStates(rows.map((row) => row.key), true); saved.acceptStates([], true); onSaved(); }
    catch { if (!request.signal.aborted) setError(true); } finally { if (!request.signal.aborted) setBusy(false); }
  }
  return <Dialog title={f.addToList} onClose={onClose}><p>{f.selected}: {rows.length}</p><label className="block py-4">{f.chooseList}<select className={fieldClass} value={id} onChange={(event) => setId(event.target.value)}><option value="">{f.chooseList}</option>{lists.map((list) => <option key={list.id} value={list.id}>{list.name}</option>)}</select></label>{error && <p role="alert">{f.error}</p>}<Button disabled={busy || !id} onClick={() => void add()}>{f.addToList}</Button></Dialog>;
}
