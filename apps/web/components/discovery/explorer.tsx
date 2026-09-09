"use client";
import { useEffect, useId, useState, type FormEvent, type ReactNode } from "react";
import { useLocale, useTranslations } from "next-intl";
import { useSearchParams } from "next/navigation";
import { ArrowRight, Compass, Search, SlidersHorizontal } from "lucide-react";
import { Link, usePathname, useRouter } from "@/i18n/navigation";
import { locales, localeLabels } from "@/i18n/routing";
import { useHeaderSession } from "@/components/header-session";
import { useCommunity } from "@/components/community/provider";
import { Button, Dialog, fieldClass } from "@/components/community/ui";
import { api } from "@/lib/api";
import { getDiscoveryCopy, getDiscoveryFeedback } from "@/lib/discovery-copy";
import { discoveryKinds, discoveryQuery, useDiscoveryResource, useDiscoveryStatus, type DiscoveryItem, type DiscoveryPage, type DiscoveryQuery } from "@/lib/discovery";
import { loginPath } from "@/lib/navigation";
import { DiscoveryCard, DiscoveryDetails } from "./card";
import { DiscoveryPreferenceEditor } from "./preferences";
import { SearchWorkbench } from "@/components/search-workbench";
import { TravelExplore } from "@/components/community/explore";

export function DiscoveryHomeGate({ children }: { children: ReactNode }) {
  const { enabled } = useDiscoveryStatus();
  return enabled ? <><DiscoveryExplorer home /><section className="mx-auto max-w-4xl px-5 pb-24"><SearchWorkbench /></section></> : children;
}

export function DiscoveryExplorer({ home = false }: { home?: boolean }) {
  const c = getDiscoveryCopy(useLocale());
  const t = useTranslations("community");
  const { enabled, loading } = useDiscoveryStatus();
  if (loading) return <main className="mx-auto min-h-[60vh] max-w-6xl px-5 py-12"><p role="status">{c.loading}</p></main>;
  if (!enabled) return <main className="mx-auto max-w-5xl px-5 py-10"><h1 className="mb-6 text-3xl font-bold">{t("exploreTravel")}</h1><TravelExplore /></main>;
  return <ExplorerContent home={home} />;
}
function ExplorerContent({ home }: { home: boolean }) {
  const locale = useLocale();
  const c = getDiscoveryCopy(locale);
  const params = useSearchParams();
  const router = useRouter();
  const pathname = usePathname();
  const { user, sessionIdentity } = useHeaderSession();
  const { flags } = useCommunity();
  const value: DiscoveryQuery = Object.fromEntries(["q", "type", "destination", "topic", "locale", "mode"].map((key) => [key, home ? "" : params.get(key) || ""]));
  const query = discoveryQuery(value);
  const mode = ["recommended", "latest", "following"].includes(value.mode || "") ? value.mode! : "recommended";
  const [preferences, setPreferences] = useState(false);
  const [revision, setRevision] = useState(0);
  function navigate(patch: DiscoveryQuery) {
    router.push(`/explore?${discoveryQuery({ ...value, ...patch })}`, { scroll: false });
  }
  const kinds = discoveryKinds.filter((kind) => flags.enabled || !["post", "itinerary"].includes(kind));
  return <main className="mx-auto min-h-screen max-w-6xl px-5 pb-24 pt-7 md:px-8 md:pt-14">
    <section className="relative isolate mb-10 overflow-hidden rounded-[2rem] border border-[var(--line)] bg-[var(--surface)] p-6 md:p-10">
      <div aria-hidden className="pointer-events-none absolute -right-16 -top-20 -z-10 size-80 rounded-full border-[36px] border-[var(--line)] opacity-30" />
      <p className="flex items-center gap-2 text-sm font-semibold text-[var(--teal)]"><Compass size={18} aria-hidden />{c.eyebrow}</p>
      <h1 className="mt-4 max-w-3xl text-4xl font-bold leading-tight tracking-tight md:text-6xl">{home ? c.title : c.explore}</h1>
      <p className="mb-6 mt-4 max-w-2xl text-base leading-7 text-[var(--muted)] md:text-lg">{c.subtitle}</p>
      <DiscoverySearch key={value.q || ""} initial={value.q || ""} onSearch={(q) => navigate({ q })} />
      <nav aria-label={c.filters} className="mt-5 flex flex-wrap gap-2">{kinds.slice(0, 6).map((kind) => <Link key={kind} href={`/explore?${discoveryQuery({ type: kind })}`} className="inline-flex min-h-11 items-center rounded-full border border-[var(--line)] bg-[var(--surface)] px-4 text-sm font-semibold hover:border-[var(--teal)] focus-visible:outline focus-visible:outline-2 focus-visible:outline-[var(--teal)]">{c.kinds[kind]}</Link>)}</nav>
    </section>
    <div className="mb-5 flex flex-wrap items-center justify-between gap-3"><h2 className="text-2xl font-bold">{value.q ? `${c.matched}「${value.q}」` : c.feed}</h2>{user ? <Button secondary onClick={() => setPreferences(true)}><SlidersHorizontal size={17} aria-hidden />{c.preferences}</Button> : <Link href={loginPath(`${pathname}${params.size ? `?${params}` : ""}`)} className="inline-flex min-h-11 items-center gap-2 rounded-xl px-3 text-sm font-semibold text-[var(--teal)] underline">{c.preferences}</Link>}</div>
    <div className="mb-6 flex flex-wrap gap-2" aria-label={c.feed}>{(["recommended", "latest", "following"] as const).filter((key) => key !== "following" || flags.enabled).map((key) => <button type="button" key={key} aria-pressed={mode === key} onClick={() => navigate({ mode: key })} className={`min-h-11 rounded-full border px-5 font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--teal)] ${mode === key ? "border-[var(--teal)] bg-[var(--teal)] text-white" : "border-[var(--line)] bg-[var(--surface)]"}`}>{c[key]}</button>)}</div>
    {params.get("resume_item") && user && <PendingDiscoveryItem identifier={params.get("resume_item")!} kind={params.get("resume_kind") || undefined} />}
    {params.get("content") && <LinkedContent identifier={params.get("content")!} onClose={() => { const next = new URLSearchParams(params); next.delete("content"); router.replace(`${pathname}${next.size ? `?${next}` : ""}`, { scroll: false }); }} />}
    {mode === "following" && !user ? <div className="rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-8"><p>{c.loginFollowing}</p><Link href={loginPath(`/explore?${query}`)} className="mt-4 inline-flex min-h-11 items-center font-semibold text-[var(--teal)] underline">{c.login}</Link></div> : <Results key={`${query}:${revision}`} query={{ ...value, mode }} onFilter={navigate} identity={sessionIdentity} />}
    <section className="mt-12 flex flex-wrap items-center justify-between gap-5 rounded-3xl border border-[var(--line)] bg-[var(--paper)] p-6 md:p-8"><div><h2 className="text-xl font-bold">{c.planning}</h2><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{c.planningHelp}</p></div><Link href="/trips/new" className="inline-flex min-h-12 items-center gap-3 rounded-xl bg-[var(--teal)] px-5 font-semibold text-white">{c.plan}<ArrowRight size={18} aria-hidden /></Link></section>
    {preferences && user && <DiscoveryPreferenceEditor key={user.id} onClose={() => setPreferences(false)} onSaved={() => { setPreferences(false); setRevision((n) => n + 1); }} />}
  </main>;
}

function DiscoverySearch({ initial, onSearch }: { initial: string; onSearch: (value: string) => void }) {
  const c = getDiscoveryCopy(useLocale());
  const [text, setText] = useState(initial);
  const [debounced, setDebounced] = useState("");
  const [show, setShow] = useState(false);
  useEffect(() => { const timer = setTimeout(() => setDebounced(text.trim()), 250); return () => clearTimeout(timer); }, [text]);
  const suggestions = useDiscoveryResource<{ query: string; items: Array<{ label: string; query: string }> }>(show && debounced.length >= 2 ? `/discovery/suggestions?q=${encodeURIComponent(debounced)}` : null);
  function submit(event: FormEvent) { event.preventDefault(); setShow(false); onSearch(text.trim()); }
  return <div><form role="search" onSubmit={submit} className="flex flex-wrap gap-2 rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-2">
    <label className="sr-only" htmlFor="discovery-search">{c.searchLabel}</label><input id="discovery-search" type="search" maxLength={160} value={text} onFocus={() => setShow(true)} onChange={(event) => { setText(event.target.value); setShow(true); }} onKeyDown={(event) => { if (event.key === "Escape") setShow(false); }} placeholder={c.placeholder} className="min-h-12 min-w-0 flex-1 rounded-xl bg-[var(--surface)] px-4 text-base outline-none focus:ring-2 focus:ring-[var(--teal)]" />
    <Button type="submit"><Search size={18} aria-hidden />{c.search}</Button>
  </form>{show && suggestions.data?.query === debounced && suggestions.data.items.length > 0 && <div className="mt-2 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3"><p className="px-2 text-xs font-semibold text-[var(--muted)]">{c.suggestions}</p><ul>{suggestions.data.items.map((item) => <li key={item.query}><button type="button" onClick={() => { setText(item.query); setShow(false); onSearch(item.query); }} className="min-h-11 w-full rounded-xl px-3 text-left text-sm hover:bg-[var(--paper)] focus-visible:outline focus-visible:outline-2">{item.label}</button></li>)}</ul></div>}</div>;
}

function Results({ query, onFilter, identity }: { query: DiscoveryQuery; onFilter: (patch: DiscoveryQuery) => void; identity: object | null }) {
  // Recreate pagination on an actual login/logout, including the same principal logging in again.
  const [owner, setOwner] = useState(identity);
  const [cursor, setCursor] = useState<string | null>(null);
  const [previous, setPrevious] = useState<DiscoveryItem[]>([]);
  const [hidden, setHidden] = useState<string[]>([]);
  const [undoItem, setUndoItem] = useState<DiscoveryItem>();
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(false);
  const [filtersOpen, setFiltersOpen] = useState(Boolean(query.type || query.destination || query.topic || query.locale));
  const filterPanelId = useId();
  if (owner !== identity) { setOwner(identity); setCursor(null); setPrevious([]); setHidden([]); setUndoItem(undefined); }
  const locale = useLocale();
  const c = getDiscoveryCopy(locale);
  const { user } = useHeaderSession();
  const { flags } = useCommunity();
  const params = useSearchParams();
  const options = useDiscoveryResource<{ destinations: Array<{ id: string; name: string }>; topics?: Array<{ id: string; label: string }> }>("/discovery/suggestions?q=");
  const path = `/discovery/${query.q ? "search" : "feed"}?${discoveryQuery(query)}${cursor ? `&cursor=${encodeURIComponent(cursor)}` : ""}`;
  const result = useDiscoveryResource<DiscoveryPage>(path);
  const items = [...new Map([...previous, ...(result.data?.items || [])].map((item) => [item.id, item])).values()].filter((item) => !hidden.includes(item.id) && (flags.enabled || (item.source.kind !== "community" && !["post", "itinerary"].includes(item.kind))));
  async function dismiss(item: DiscoveryItem, dismissed: boolean) {
    setBusy(true); setError(false);
    try { await api("/discovery/dismiss", { method: "POST", body: JSON.stringify({ id: item.id, dismissed }) }); setHidden((ids) => dismissed ? [...ids, item.id] : ids.filter((id) => id !== item.id)); setUndoItem(dismissed ? item : undefined); }
    catch { setError(true); } finally { setBusy(false); }
  }
  const kinds = discoveryKinds.filter((kind) => flags.enabled || !["post", "itinerary"].includes(kind));
  return <section aria-label={c.filters} className="space-y-5">
    <Button secondary className="sm:hidden" aria-expanded={filtersOpen} aria-controls={filterPanelId} onClick={() => setFiltersOpen((open) => !open)}><SlidersHorizontal size={17} aria-hidden />{c.filters}</Button>
    <div id={filterPanelId} className={`${filtersOpen ? "grid" : "hidden"} gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-4 sm:grid sm:grid-cols-2 lg:grid-cols-4`}>
      <label className="text-sm font-semibold">{getDiscoveryFeedback(locale).type}<select value={query.type || "all"} onChange={(event) => onFilter({ type: event.target.value })} className={fieldClass}><option value="all">{c.all}</option>{kinds.map((kind) => <option key={kind} value={kind}>{c.kinds[kind]}</option>)}</select></label>
      <label className="text-sm font-semibold">{c.destination}<select value={query.destination || ""} onChange={(event) => onFilter({ destination: event.target.value })} className={fieldClass}><option value="">{c.any}</option>{options.data?.destinations?.map((item) => <option key={item.id} value={item.id}>{item.name}</option>)}{query.destination && !options.data?.destinations?.some((item) => item.id === query.destination) && <option value={query.destination}>{query.destination}</option>}</select></label>
      <label className="text-sm font-semibold">{c.topic}<select value={query.topic || ""} onChange={(event) => onFilter({ topic: event.target.value })} className={fieldClass}><option value="">{c.any}</option>{options.data?.topics?.map((item) => <option key={item.id} value={item.id}>{item.label}</option>)}{query.topic && !options.data?.topics?.some((item) => item.id === query.topic) && <option value={query.topic}>{query.topic}</option>}</select></label>
      <label className="text-sm font-semibold">{c.language}<select value={query.locale || ""} onChange={(event) => onFilter({ locale: event.target.value })} className={fieldClass}><option value="">{c.any}</option>{locales.map((value) => <option key={value} value={value}>{localeLabels[value]}</option>)}</select></label>
    </div>
    {(query.type || query.destination || query.topic || query.locale || query.q) && <Button secondary onClick={() => onFilter({ type: "", destination: "", topic: "", locale: "", q: "" })}>{c.clear}</Button>}
    {undoItem && <div role="status" className="flex flex-wrap items-center gap-3 rounded-xl bg-[var(--paper)] p-3"><p>{c.dismissed}</p><Button secondary disabled={busy} onClick={() => void dismiss(undoItem, false)}>{c.undo}</Button></div>}
    {(Boolean(result.error) || error) && <div role="alert" className="space-y-2"><p>{c.unavailable}</p>{Boolean(result.error) && <Button secondary onClick={() => { if (cursor) { setCursor(null); setPrevious([]); } else result.reload(); }}>{c.retry}</Button>}</div>}
    {result.loading && <p role="status" className="rounded-2xl bg-[var(--paper)] p-6 text-[var(--muted)]">{c.loading}</p>}
    {!result.loading && !result.error && !items.length && <p className="rounded-2xl border border-dashed border-[var(--line)] p-8 text-center leading-7 text-[var(--muted)]">{c.empty}</p>}
    <div className="grid items-stretch gap-5 md:grid-cols-2 lg:grid-cols-3">{items.filter((item) => !user || item.id !== params.get("resume_item")).map((item) => <DiscoveryCard key={item.id} item={item} onDismiss={user && !busy ? (row) => void dismiss(row, true) : undefined} />)}</div>
    {result.data?.next_cursor && <div className="flex justify-center"><Button secondary disabled={result.loading} onClick={() => { setPrevious(items); setCursor(result.data!.next_cursor); }}>{c.more}</Button></div>}
  </section>;
}
function PendingDiscoveryItem({ identifier, kind }: { identifier: string; kind?: string }) {
  const c = getDiscoveryCopy(useLocale());
  const [prefix, id] = identifier.split(":");
  const resolvedKind = kind || (prefix === "guide" ? "article" : prefix);
  const valid = /^[a-f0-9-]{36}$/i.test(id || "") && discoveryKinds.includes(resolvedKind as typeof discoveryKinds[number]);
  const result = useDiscoveryResource<DiscoveryItem>(valid ? `/discovery/content/${resolvedKind}/${id}` : null);
  if (!valid || result.error) return <p role="alert" className="mb-6 rounded-xl bg-[var(--paper)] p-4">{c.unavailable}</p>;
  return result.data ? <div className="mb-6 max-w-lg"><DiscoveryCard key={identifier} item={result.data} /></div> : <p role="status">{c.loading}</p>;
}
function LinkedContent({ identifier, onClose }: { identifier: string; onClose: () => void }) {
  const c = getDiscoveryCopy(useLocale());
  const [kind, id] = identifier.split(":");
  if (!discoveryKinds.includes(kind as typeof discoveryKinds[number]) || !/^[a-f0-9-]{36}$/i.test(id || "")) return <p role="alert">{c.unavailable}</p>;
  return <Dialog title={c.details} onClose={onClose}><DiscoveryDetails kind={kind} id={id} /></Dialog>;
}
