"use client";

import { BedDouble, ExternalLink, LoaderCircle, X } from "lucide-react";
import { useCallback, useEffect, useId, useState } from "react";
import { useModalSheet } from "@/lib/modal-sheet";
import { isOriginalHotelUrl } from "@/lib/stay22-script";
import { stay22ScriptCopy } from "@/lib/stay22-script-copy";

type Hotel = { id: string; title: string; destination_id: string };
type Option = { id: string; provider: string; name: string | null; url: string };
type State<T> = { status: "loading" | "ready" | "error"; items: T[] };

async function publicJson(path: string, locale: string, signal: AbortSignal) {
  const response = await fetch(`/api/travel${path}`, {
    credentials: "omit", cache: "no-store", signal: AbortSignal.any([signal, AbortSignal.timeout(5_000)]),
    headers: { Accept: "application/json", "x-travel-locale": locale },
  });
  if (!response.ok) throw new Error("Public catalogue unavailable");
  return response.json();
}

function PlatformSheet({ hotel, locale, close }: { hotel: Hotel; locale: string; close: () => void }) {
  const copy = stay22ScriptCopy(locale);
  const id = useId();
  const ref = useModalSheet<HTMLDivElement>(true, close);
  const [attempt, setAttempt] = useState(0);
  const [state, setState] = useState<State<Option>>({ status: "loading", items: [] });
  useEffect(() => {
    const abort = new AbortController();
    publicJson(`/travel-services/${encodeURIComponent(hotel.id)}/stay22-script-options`, locale, abort.signal)
      .then((value: { options?: Option[] }) => {
        if (abort.signal.aborted) return;
        setState({ status: "ready", items: (Array.isArray(value.options) ? value.options : []).filter((option) =>
          typeof option.id === "string" && typeof option.provider === "string"
          && typeof option.url === "string" && isOriginalHotelUrl(option.url)) });
      })
      .catch(() => { if (!abort.signal.aborted) setState({ status: "error", items: [] }); });
    return () => abort.abort();
  }, [hotel.id, locale, attempt]);
  return <div className="fixed inset-0 z-[80] bg-black/35 backdrop-blur-sm" onClick={(event) => { if (event.target === event.currentTarget) close(); }}>
    <div ref={ref} role="dialog" aria-modal="true" aria-labelledby={`${id}-title`} tabIndex={-1} className="absolute inset-x-0 bottom-0 flex max-h-[90dvh] min-w-0 flex-col overflow-hidden rounded-t-3xl border border-[var(--line)] bg-[var(--surface-raised)] shadow-2xl md:inset-y-0 md:left-auto md:w-[min(30rem,100vw)] md:max-h-none md:rounded-l-3xl md:rounded-tr-none">
      <header className="flex shrink-0 items-start justify-between gap-3 border-b border-[var(--line)] p-5">
        <div className="min-w-0"><p className="text-xs font-semibold uppercase tracking-wider text-[var(--teal)]">{copy.open}</p><h2 id={`${id}-title`} className="mt-2 break-words text-xl font-bold">{hotel.title}</h2></div>
        <button type="button" onClick={close} aria-label={copy.close} className="flex min-h-11 min-w-11 items-center justify-center rounded-xl border border-[var(--line)]"><X size={20} /></button>
      </header>
      <div className="min-h-0 space-y-4 overflow-y-auto overscroll-contain p-5">
        <p className="rounded-2xl border border-[var(--line)] bg-[var(--paper)] p-4 text-sm leading-6">{copy.dateNotice}</p>
        {state.status === "loading" && <p role="status" className="flex min-h-16 items-center gap-2"><LoaderCircle aria-hidden size={18} className="motion-safe:animate-spin" />{copy.platformLoading}</p>}
        {state.status === "error" && <div role="alert" className="space-y-3 rounded-2xl border border-[var(--line)] p-4"><p>{copy.platformError}</p><div className="flex flex-wrap gap-2"><button className="min-h-11 rounded-xl border border-[var(--line)] px-4" onClick={() => { setState({ status: "loading", items: [] }); setAttempt((value) => value + 1); }}>{copy.retry}</button><button className="min-h-11 rounded-xl border border-[var(--line)] px-4" onClick={() => window.location.reload()}>{copy.reload}</button></div></div>}
        {state.status === "ready" && !state.items.length && <p>{copy.noLinks}</p>}
        {state.items.map((option) => {
          const name = option.provider === "official" ? copy.official : option.name || option.provider;
          return <a key={option.id} href={option.url} target="_blank" rel="sponsored noopener noreferrer" referrerPolicy="no-referrer" className="flex min-h-16 min-w-0 items-center justify-between gap-3 rounded-2xl border border-[var(--line)] p-4 transition hover:bg-[var(--teal-soft)] focus-visible:outline-2 focus-visible:outline-[var(--teal)]">
            <span className="min-w-0 break-words"><strong className="block">{copy.platform.replace("{platform}", name)}</strong><span className="text-xs text-[var(--muted)]">{copy.newTab}</span></span><ExternalLink aria-hidden size={18} className="shrink-0" />
          </a>;
        })}
        <p className="text-xs leading-6 text-[var(--muted)]">{copy.originalNotice}</p>
        <p className="text-xs leading-6 text-[var(--muted)]">{copy.disclosure}</p>
      </div>
    </div>
  </div>;
}

/** Public content only: deliberately does not import identity, trips, saved data or their hooks. */
export function Stay22PublicHotels({ destinationId, locale }: { destinationId: string; locale: string }) {
  const copy = stay22ScriptCopy(locale);
  const [state, setState] = useState<State<Hotel>>({ status: "loading", items: [] });
  const [selected, setSelected] = useState<Hotel | null>(null);
  const [attempt, setAttempt] = useState(0);
  const close = useCallback(() => setSelected(null), []);
  useEffect(() => {
    const abort = new AbortController();
    const destinations = destinationId === "osaka-kyoto" ? ["osaka", "kyoto"] : [destinationId];
    Promise.all(destinations.map((destination) => publicJson(`/travel-services?destination_id=${encodeURIComponent(destination)}&type=hotel`, locale, abort.signal)))
      .then((responses: { enabled?: boolean; items?: Hotel[] }[]) => {
        if (abort.signal.aborted) return;
        const hotels = responses.flatMap((response) => response.enabled === false || !Array.isArray(response.items) ? [] : response.items)
          .filter((hotel) => typeof hotel.id === "string" && typeof hotel.title === "string");
        setState({ status: "ready", items: Array.from(new Map(hotels.map((hotel) => [hotel.id, hotel])).values()) });
      })
      .catch(() => { if (!abort.signal.aborted) setState({ status: "error", items: [] }); });
    return () => abort.abort();
  }, [destinationId, locale, attempt]);
  return <>
    {state.status === "loading" && <p role="status" className="flex items-center gap-3 rounded-3xl border border-[var(--line)] p-7"><LoaderCircle aria-hidden className="motion-safe:animate-spin" />{copy.loading}</p>}
    {state.status === "error" && <div role="alert" className="space-y-4 rounded-3xl border border-[var(--line)] p-7"><p>{copy.error}</p><button className="min-h-11 rounded-xl border border-[var(--line)] px-5" onClick={() => { setState({ status: "loading", items: [] }); setAttempt((value) => value + 1); }}>{copy.retry}</button></div>}
    {state.status === "ready" && !state.items.length && <p className="rounded-3xl border border-[var(--line)] p-7 text-[var(--muted)]">{copy.empty}</p>}
    <div className="grid min-w-0 gap-5 sm:grid-cols-2 lg:grid-cols-3">
      {state.items.map((hotel) => <article key={hotel.id} className="flex min-w-0 flex-col rounded-3xl border border-[var(--line)] bg-[var(--surface-raised)] p-6 shadow-sm">
        <BedDouble aria-hidden size={28} className="mb-5 text-[var(--teal)]" />
        <h2 className="mb-5 break-words text-xl font-bold leading-7">{hotel.title}</h2>
        <button onClick={() => setSelected(hotel)} className="mt-auto flex min-h-12 items-center justify-between gap-3 rounded-xl bg-[var(--teal)] px-4 py-3 text-left font-semibold text-white focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--teal)]">{copy.open}<ExternalLink aria-hidden size={18} className="shrink-0" /></button>
      </article>)}
    </div>
    {selected && <PlatformSheet key={selected.id} hotel={selected} locale={locale} close={close} />}
  </>;
}
