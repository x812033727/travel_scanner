"use client";

import { ExternalLink, Loader2, MapPin, X } from "lucide-react";
import { useLocale } from "next-intl";
import { useEffect, useId, useRef, useState, useSyncExternalStore } from "react";
import { buildStay22Map, type Stay22MapContext } from "@/lib/stay22";
import { stay22Copy, stay22Text, type Stay22Copy } from "@/lib/stay22-copy";

const subscribe = () => () => {};
function privacyBlocked() {
  return navigator.doNotTrack === "1" || (navigator as Navigator & { globalPrivacyControl?: boolean }).globalPrivacyControl === true;
}
const serverPrivacy = () => true;

type Props = {
  context?: Stay22MapContext | null;
  area?: { name: string; latitude: number; longitude: number };
  onManualLodging: () => void;
};

export function Stay22MapPanel({ context, area, onManualLodging }: Props) {
  const copy = stay22Copy(useLocale());
  const blocked = useSyncExternalStore(subscribe, privacyBlocked, serverPrivacy);
  const map = buildStay22Map(context, area);
  if (!map || !area || !context) return null;
  // Reset consent on changed search fields; never silently transmit a different trip's context.
  return <MapPanel key={`${blocked}:${map.url}`} map={map} context={context} areaName={area.name} copy={copy} blocked={blocked} onManualLodging={onManualLodging} />;
}

function MapPanel({ map, context, areaName, copy, blocked, onManualLodging }: {
  map: NonNullable<ReturnType<typeof buildStay22Map>>;
  context: Stay22MapContext;
  areaName: string;
  copy: Stay22Copy;
  blocked: boolean;
  onManualLodging: () => void;
}) {
  const [open, setOpen] = useState(false);
  const [attempt, setAttempt] = useState(0);
  const [status, setStatus] = useState<"loading" | "loaded" | "slow">("loading");
  const loadRef = useRef<HTMLButtonElement>(null);
  const frameRef = useRef<HTMLIFrameElement>(null);
  const titleId = useId();
  const privacyId = useId();
  const frameId = useId();

  useEffect(() => {
    if (!open || status !== "loading") return;
    const timer = window.setTimeout(() => setStatus("slow"), 12_000);
    return () => window.clearTimeout(timer);
  }, [open, status, attempt]);

  function close() {
    setOpen(false);
    window.requestAnimationFrame(() => loadRef.current?.focus());
  }

  return <section aria-labelledby={titleId} className="min-w-0 overflow-hidden rounded-2xl border border-[var(--line)] bg-[var(--surface)]">
    <div className="space-y-3 p-4 sm:p-5">
      <div className="flex flex-wrap items-center justify-between gap-2">
        <h3 id={titleId} className="flex items-center gap-2 text-base font-bold"><MapPin size={18} aria-hidden="true" />{copy.title}</h3>
        <span className="rounded-full bg-[var(--teal-soft)] px-2.5 py-1 text-xs font-semibold text-[var(--teal-dark)]">{copy.pilot}</span>
      </div>
      <p className="text-sm font-semibold text-[var(--teal)]">{stay22Text(copy.area, { area: areaName })}</p>
      <p className="text-sm leading-6 text-[var(--muted)]">{copy.description}</p>
      <div className="space-y-1 rounded-xl bg-[var(--paper)] p-3 text-sm">
        <p>{map.datesProvided ? stay22Text(copy.dates, { checkIn: map.checkIn!, checkOut: map.checkOut! }) : copy.datesMissing}</p>
        <p>{map.guestsProvided && context.travelers ? stay22Text(copy.guests, context.travelers) : copy.guestsMissing}</p>
        {map.hasChildren && <p className="text-xs leading-5 text-[var(--muted)]">{copy.children}</p>}
      </div>
      <p id={privacyId} className="text-xs leading-5 text-[var(--muted)]">{copy.privacy}</p>
      <a href="https://www.stay22.com/privacy" target="_blank" rel="noopener noreferrer" className="inline-flex min-h-11 items-center gap-1 text-xs font-semibold text-[var(--teal)] underline">{copy.privacyLink}<ExternalLink size={13} aria-hidden="true" /></a>
      {blocked ? <p role="status" className="text-sm leading-6">{copy.blocked}</p> : <div className="flex flex-wrap items-center gap-2">
        {!open ? <button ref={loadRef} type="button" aria-describedby={privacyId} aria-controls={frameId} aria-expanded={false} onClick={() => { setStatus("loading"); setOpen(true); }} className="planner-system-primary min-h-11">{copy.load}</button>
          : <button type="button" onClick={close} aria-controls={frameId} aria-expanded={true} className="inline-flex min-h-11 items-center gap-1 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold"><X size={16} aria-hidden="true" />{copy.close}</button>}
        <a href={map.url} target="_blank" rel="noopener noreferrer sponsored" referrerPolicy="no-referrer" aria-describedby={privacyId} className="inline-flex min-h-11 items-center gap-1 rounded-xl px-2 text-sm font-semibold text-[var(--teal)] underline">{copy.open}<ExternalLink size={14} aria-hidden="true" /></a>
      </div>}
    </div>
    {open && !blocked && <div id={frameId} className="border-t border-[var(--line)]">
      {status !== "loaded" && <div role="status" className="flex items-start gap-2 p-3 text-sm leading-6 text-[var(--muted)]">
        {status === "loading" && <Loader2 size={16} className="mt-1 shrink-0 animate-spin" aria-hidden="true" />}
        <span>{status === "loading" ? copy.loading : copy.slow}</span>
      </div>}
      <iframe key={attempt} ref={frameRef} src={map.url} title={stay22Text(copy.frameTitle, { area: areaName })}
        width="100%" height="480" loading="lazy" referrerPolicy="no-referrer"
        // Booking stays user-initiated; the third-party frame cannot navigate the parent.
        sandbox="allow-scripts allow-same-origin allow-forms allow-popups allow-popups-to-escape-sandbox"
        allow="fullscreen" className="block h-[min(65svh,480px)] min-h-[360px] w-full border-0"
        onLoad={() => setStatus("loaded")} onErrorCapture={() => setStatus("slow")} />
      <div className="flex flex-wrap gap-2 p-3">
        <button type="button" className="min-h-11 rounded-xl border border-[var(--line)] px-3 text-sm font-semibold" onClick={() => { setStatus("loading"); setAttempt((value) => value + 1); }}>{copy.retry}</button>
        <button type="button" className="min-h-11 rounded-xl px-3 text-sm font-semibold text-[var(--teal)]" onClick={onManualLodging}>{copy.manual}</button>
      </div>
    </div>}
    <div className="space-y-2 border-t border-[var(--line)] px-4 py-3 text-xs leading-5 text-[var(--muted)]">
      <p>{copy.limitations}</p><p>{copy.disclosure}</p>
    </div>
  </section>;
}
