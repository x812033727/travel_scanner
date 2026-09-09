"use client";
import { useEffect, useId, useLayoutEffect, useRef, useState, type FormEvent, type ReactNode } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useSearchParams } from "next/navigation";
import { ArrowRight, Search, SlidersHorizontal, X } from "lucide-react";
import { Link, usePathname, useRouter } from "@/i18n/navigation";
import { locales, localeLabels } from "@/i18n/routing";
import { useHeaderSession } from "@/components/header-session";
import { useCommunity } from "@/components/community/provider";
import { Button, fieldClass } from "@/components/community/ui";
import { api } from "@/lib/api";
import { getDiscoveryCopy, getDiscoveryFeedback } from "@/lib/discovery-copy";
import { getFrontendFlowCopy } from "@/lib/frontend-flow-copy";
import { discoveryCategories, discoveryKinds, discoveryQuery, useDiscoveryResource, useDiscoveryStatus, type DiscoveryItem, type DiscoveryPage, type DiscoveryQuery } from "@/lib/discovery";
import { loginPath } from "@/lib/navigation";
import { DiscoveryCard } from "./card";
import { DiscoveryDetailBoundary } from "./detail-drawer";
import { DiscoveryPreferenceEditor } from "./preferences";
import { TravelExplore } from "@/components/community/explore";
import styles from "./discovery.module.css";

export function DiscoveryHomeGate({ children }: { children: ReactNode }) {
  const { enabled, loading } = useDiscoveryStatus(); const router = useRouter();
  useEffect(() => {
    if (!enabled) return;
    const redirect = () => { if (window.location.hash === "#trip-search") router.replace("/search/new"); };
    redirect(); window.addEventListener("hashchange", redirect); return () => window.removeEventListener("hashchange", redirect);
  }, [enabled, router]);
  return loading ? <main className={styles.page}><DiscoverySkeleton /></main> : enabled ? <DiscoveryExplorer home /> : children;
}
export function DiscoveryExplorer({ home = false }: { home?: boolean }) {
  const t = useTranslations("community"); const { enabled, loading } = useDiscoveryStatus();
  if (loading) return <main className={styles.page}><DiscoverySkeleton /></main>;
  if (!enabled) return <main className="mx-auto max-w-5xl px-5 py-10"><h1 className="mb-6 text-3xl font-bold">{t("exploreTravel")}</h1><TravelExplore /></main>;
  return <DiscoveryDetailBoundary><ExplorerContent home={home} /></DiscoveryDetailBoundary>;
}
function ExplorerContent({ home }: { home: boolean }) {
  const locale = useLocale(); const c = getDiscoveryCopy(locale); const f = getFrontendFlowCopy(locale);
  const params = useSearchParams(); const router = useRouter(); const pathname = usePathname();
  const { user, sessionIdentity } = useHeaderSession(); const { flags } = useCommunity();
  const value: DiscoveryQuery = Object.fromEntries(["q", "type", "category", "destination", "topic", "locale", "mode"].map((key) => [key, params.get(key) || ""]));
  const mode = ["recommended", "latest", "following"].includes(value.mode || "") ? value.mode! : "recommended";
  const [preferences, setPreferences] = useState(false); const [revision, setRevision] = useState(0); const [advanced, setAdvanced] = useState(false);
  const filterId = useId();
  const options = useDiscoveryResource<{ destinations: Array<{ id: string; name: string }>; topics?: Array<{ id: string; label: string }> }>("/discovery/suggestions?q=");
  function navigate(patch: DiscoveryQuery) { const next = discoveryQuery({ ...value, ...patch }); router.push(`/explore${next ? `?${next}` : ""}`, { scroll: false }); }
  const kinds = discoveryKinds.filter((kind) => flags.enabled || !["post", "itinerary"].includes(kind));
  const selectedFilters = (["q", "destination", "type", "topic", "locale"] as const).filter((key) => value[key] && value[key] !== "all");
  return <main className={styles.page}>
    <header className={styles.masthead}><div><p className={styles.eyebrow}>{c.eyebrow}</p><h1 className={styles.title}>{home ? f.editorial : f.results}</h1><p className={styles.intro}>{c.subtitle}</p></div><div className={styles.searchArea}><DiscoverySearch key={value.q || ""} initial={value.q || ""} onSearch={(q) => navigate({ q })} /></div></header>
    <div className={styles.filters}><nav className={styles.categories} aria-label={c.filters}>{discoveryCategories.map((category) => <button key={category} type="button" className={styles.chip} aria-pressed={(value.category || "all") === category} onClick={() => navigate({ category, type: "" })}>{f.categories[category]}</button>)}</nav>
      <div className={styles.toolbar}><label className="sr-only" htmlFor={`${filterId}-destination`}>{c.destination}</label><select id={`${filterId}-destination`} className={styles.destination} value={value.destination || ""} onChange={(event) => navigate({ destination: event.target.value })}><option value="">{c.destination}: {c.any}</option>{options.data?.destinations?.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}{value.destination && !options.data?.destinations?.some((item) => item.id === value.destination) && <option value={value.destination}>{value.destination}</option>}</select><button type="button" className={styles.chip} aria-expanded={advanced} aria-controls={filterId} onClick={() => setAdvanced((open) => !open)}><SlidersHorizontal size={17} aria-hidden />{f.advanced}</button></div>
    </div>
    {advanced && <section id={filterId} aria-label={f.advanced} className="mb-5 grid gap-3 rounded-xl border border-[var(--line)] bg-[var(--surface)] p-4 sm:grid-cols-3">
      <label className="text-sm font-semibold">{getDiscoveryFeedback(locale).type}<select value={value.type || "all"} onChange={(event) => navigate({ type: event.target.value })} className={fieldClass}><option value="all">{c.all}</option>{kinds.map((kind) => <option key={kind} value={kind}>{c.kinds[kind]}</option>)}</select></label>
      <label className="text-sm font-semibold">{c.topic}<select value={value.topic || ""} onChange={(event) => navigate({ topic: event.target.value })} className={fieldClass}><option value="">{c.any}</option>{options.data?.topics?.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}{value.topic && !options.data?.topics?.some((item) => item.id === value.topic) && <option value={value.topic}>{value.topic}</option>}</select></label>
      <label className="text-sm font-semibold">{c.language}<select value={value.locale || ""} onChange={(event) => navigate({ locale: event.target.value })} className={fieldClass}><option value="">{c.any}</option>{locales.map((value) => <option key={value} value={value}>{localeLabels[value]}</option>)}</select></label>
    </section>}
    {selectedFilters.length > 0 && <div className="mb-4 flex flex-wrap gap-2">{selectedFilters.map((key) => { const label = key === "destination" ? options.data?.destinations?.find((item) => item.id === value[key])?.name || value[key] : key === "type" ? c.kinds[value.type as typeof discoveryKinds[number]] || value.type : key === "topic" ? options.data?.topics?.find((item) => item.id === value[key])?.label || value[key] : value[key]; return <button key={key} className={styles.chip} onClick={() => navigate({ [key]: "" })} aria-label={`${f.removeFilter}: ${label}`}>{label}<X size={14} aria-hidden /></button>; })}<Button secondary onClick={() => navigate({ q: "", type: "", destination: "", topic: "", locale: "", category: "" })}>{c.clear}</Button></div>}
    <div className="mb-4 flex flex-wrap items-center justify-between gap-2"><h2 className={value.q ? "text-xl font-bold" : "sr-only"}>{value.q ? `${c.matched}「${value.q}」` : c.feed}</h2><div className="flex flex-wrap items-center gap-1" aria-label={c.feed}>{(["recommended", "latest", "following"] as const).filter((key) => key !== "following" || flags.enabled).map((key) => <button type="button" key={key} aria-pressed={mode === key} onClick={() => navigate({ mode: key })} className="min-h-11 rounded-lg px-3 text-sm aria-pressed:font-bold aria-pressed:underline aria-pressed:decoration-[var(--teal)] aria-pressed:underline-offset-8 focus-visible:outline focus-visible:outline-2">{c[key]}</button>)}</div>{user ? <Button secondary onClick={() => setPreferences(true)}>{c.preferences}</Button> : <Link href={loginPath(`${pathname}${params.size ? `?${params}` : ""}`)} className="inline-flex min-h-11 items-center text-sm text-[var(--teal)] underline">{c.preferences}</Link>}</div>
    {mode === "following" && !user ? <section className="rounded-xl border border-[var(--line)] p-6"><p>{c.loginFollowing}</p><Link href={loginPath(`/explore?${discoveryQuery(value)}`)} className="inline-flex min-h-11 items-center text-[var(--teal)] underline">{c.login}</Link></section> : <Results query={{ ...value, mode }} identity={sessionIdentity} revision={revision} />}
    <section className="mt-10 flex flex-wrap items-center justify-between gap-4 border-t border-[var(--line)] py-7"><div><h2 className="font-bold">{c.planning}</h2><p className="mt-1 text-sm text-[var(--muted)]">{c.planningHelp}</p></div><Link href="/search/new" className="inline-flex min-h-11 items-center gap-2 font-semibold text-[var(--teal)] underline">{f.searchTrips}<ArrowRight size={17} aria-hidden /></Link></section>
    {preferences && user && <DiscoveryPreferenceEditor key={user.id} onClose={() => setPreferences(false)} onSaved={() => { setPreferences(false); setRevision((n) => n + 1); }} />}
  </main>;
}
export function DiscoverySearch({ initial, onSearch }: { initial: string; onSearch: (value: string) => void }) {
  const c = getDiscoveryCopy(useLocale()); const [text, setText] = useState(initial); const [debounced, setDebounced] = useState(""); const [show, setShow] = useState(false); const id = useId();
  const box = useRef<HTMLDivElement>(null);
  const input = useRef<HTMLInputElement>(null);
  useEffect(() => {
    const dismiss = (event: PointerEvent) => { if (event.target instanceof Node && !box.current?.contains(event.target)) setShow(false); };
    document.addEventListener("pointerdown", dismiss);
    return () => document.removeEventListener("pointerdown", dismiss);
  }, []);
  useEffect(() => { const timer = setTimeout(() => setDebounced(text.trim()), 250); return () => clearTimeout(timer); }, [text]);
  const suggestions = useDiscoveryResource<{ query: string; items: Array<{ label: string; query: string }> }>(show && debounced.length >= 2 ? `/discovery/suggestions?q=${encodeURIComponent(debounced)}` : null);
  const visible = Boolean(show && suggestions.data?.query === debounced && suggestions.data.items?.length);
  function submit(event: FormEvent) { event.preventDefault(); setShow(false); onSearch(text.trim()); }
  return <div ref={box} onBlur={(event) => { if (!event.currentTarget.contains(event.relatedTarget)) setShow(false); }} onKeyDown={(event) => {
    if (event.nativeEvent.isComposing) return;
    if (event.key === "Escape" && show && (visible || suggestions.loading)) { event.preventDefault(); event.stopPropagation(); input.current?.focus(); setShow(false); }
    if (visible && ["ArrowDown", "ArrowUp"].includes(event.key)) {
      const options = Array.from(box.current?.querySelectorAll<HTMLButtonElement>("[data-search-suggestion]") || []);
      const index = options.indexOf(document.activeElement as HTMLButtonElement);
      const next = event.key === "ArrowDown" ? (index + 1) % options.length : (index <= 0 ? options.length - 1 : index - 1);
      event.preventDefault(); options[next]?.focus();
    }
  }}><form role="search" onSubmit={submit} className={styles.search}><label className="sr-only" htmlFor={id}>{c.searchLabel}</label><input ref={input} id={id} type="search" maxLength={160} value={text} aria-controls={visible ? `${id}-suggestions` : undefined} onFocus={() => setShow(true)} onChange={(event) => { setText(event.target.value); setShow(true); }} placeholder={c.placeholder} /><Button type="submit" aria-label={c.search}><Search size={18} aria-hidden /></Button></form>
    {visible && <div className="mt-2 rounded-xl border border-[var(--line)] bg-[var(--surface)] p-2"><p className="px-2 text-xs text-[var(--muted)]">{c.suggestions}</p><ul id={`${id}-suggestions`} aria-label={c.suggestions}>{suggestions.data!.items.map((item) => <li key={item.query}><button data-search-suggestion type="button" onClick={() => { setText(item.query); setShow(false); onSearch(item.query); }} className="min-h-11 w-full rounded-lg px-3 text-left text-sm focus-visible:outline focus-visible:outline-2">{item.label}</button></li>)}</ul></div>}
  </div>;
}
type PageState = { cursor: string | null; previous: DiscoveryItem[] };
function Results({ query, identity, revision }: { query: DiscoveryQuery; identity: object | null; revision: number }) {
  const c = getDiscoveryCopy(useLocale()); const { user } = useHeaderSession(); const { flags } = useCommunity();
  const scope = `${discoveryQuery(query)}:${revision}`;
  const [owner, setOwner] = useState(identity); const [pages, setPages] = useState<Record<string, PageState>>({});
  const [hidden, setHidden] = useState<string[]>([]); const [undoItem, setUndoItem] = useState<DiscoveryItem>(); const [busy, setBusy] = useState(false); const [error, setError] = useState(false);
  const ownerRef = useRef(identity); const requests = useRef(new Set<AbortController>());
  useLayoutEffect(() => { ownerRef.current = identity; }, [identity]);
  useEffect(() => { const active = requests.current; return () => { active.forEach((request) => request.abort()); }; }, [identity]);
  if (owner !== identity) { setOwner(identity); setPages({}); setHidden([]); setUndoItem(undefined); }
  const page = pages[scope]; const cursor = page?.cursor;
  const path = `/discovery/${query.q ? "search" : "feed"}?${discoveryQuery(query)}${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ""}`;
  const result = useDiscoveryResource<DiscoveryPage>(path, true);
  const data = result.data;
  const items = [...new Map([...(page?.previous || []), ...(data?.items || [])].map((item) => [item.id, item])).values()].filter((item) => !hidden.includes(item.id) && (flags.enabled || (item.source.kind !== "community" && !["post", "itinerary"].includes(item.kind))));
  async function dismiss(item: DiscoveryItem, dismissed: boolean) {
    const controller = new AbortController(); requests.current.add(controller);
    setBusy(true); setError(false);
    try { await api("/discovery/dismiss", { method: "POST", body: JSON.stringify({ id: item.id, dismissed }), signal: controller.signal }); if (controller.signal.aborted || ownerRef.current !== identity) return; setHidden((ids) => dismissed ? [...ids, item.id] : ids.filter((id) => id !== item.id)); setUndoItem(dismissed ? item : undefined); }
    catch { if (!controller.signal.aborted && ownerRef.current === identity) setError(true); } finally { requests.current.delete(controller); if (!controller.signal.aborted && ownerRef.current === identity) setBusy(false); }
  }
  return <section aria-label={c.feed} className="space-y-5">
    {undoItem && <div role="status" className="flex items-center gap-3 rounded-xl bg-[var(--paper)] p-3"><p>{c.dismissed}</p><Button secondary disabled={busy} onClick={() => void dismiss(undoItem, false)}>{c.undo}</Button></div>}
    {(Boolean(result.error) || error) && <div role="alert"><p>{c.unavailable}</p><Button secondary onClick={() => { setError(false); if (cursor) setPages((all) => ({ ...all, [scope]: { cursor: null, previous: [] } })); else result.reload(); }}>{c.retry}</Button></div>}
    {result.loading && !items.length && <DiscoverySkeleton />}
    {!result.loading && !result.error && !items.length && <p className="rounded-xl border border-dashed border-[var(--line)] p-8 text-center text-[var(--muted)]">{c.empty}</p>}
    <div className={styles.grid}>{items.map((item) => <DiscoveryCard key={item.id} item={item} onDismiss={user && !busy ? (row) => void dismiss(row, true) : undefined} />)}</div>
    {data?.next_cursor && <div className="flex justify-center"><Button secondary disabled={result.loading} onClick={() => setPages((all) => ({ ...all, [scope]: { cursor: data.next_cursor, previous: items } }))}>{c.more}</Button></div>}
  </section>;
}
export function DiscoverySkeleton() {
  const c = getFrontendFlowCopy(useLocale());
  return <div role="status" aria-label={c.loading}><span className="sr-only">{c.loading}</span><div aria-hidden className={styles.grid}>{[0, 1, 2].map((index) => <div key={index} className={styles.card}><div className={`${styles.skeleton} ${styles.skeletonImage}`} /><div className={styles.cardBody}><div className={`${styles.skeleton} ${styles.skeletonLine}`} /><div className={`${styles.skeleton} ${styles.skeletonLine}`} /></div></div>)}</div></div>;
}
