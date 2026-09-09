"use client";

import { useEffect, useId, useRef, useState, type ReactNode, type ButtonHTMLAttributes } from "react";
import { useTranslations } from "next-intl";
import { ApiError, api } from "@/lib/api";
import { useHeaderSession } from "@/components/header-session";

export const fieldClass = "mt-1.5 w-full rounded-xl border border-[var(--line)] bg-[var(--surface)] px-3 py-2.5 text-[var(--ink)] outline-none focus:ring-2 focus:ring-[var(--teal)] disabled:opacity-50";
export const panelClass = "rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-5 md:p-6";
export function Button({ children, secondary, className = "", ...props }: ButtonHTMLAttributes<HTMLButtonElement> & { secondary?: boolean }) {
  return <button type="button" {...props} className={`inline-flex min-h-11 items-center justify-center gap-2 rounded-xl px-4 py-2 font-semibold focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[var(--teal)] disabled:opacity-50 ${secondary ? "border border-[var(--line)] bg-[var(--surface)]" : "bg-[var(--teal)] text-white"} ${className}`}>{children}</button>;
}
export function ErrorNotice({ error }: { error: unknown }) {
  const t = useTranslations("community");
  if (!error) return null;
  const key = error instanceof ApiError && error.code && t.has(`errors.${error.code}`) ? `errors.${error.code}` : "unavailable";
  return <p role="alert" className="rounded-xl border border-[var(--line)] bg-[var(--paper)] p-3 text-sm">{t(key)}</p>;
}
export function Empty({ children }: { children: ReactNode }) {
  return <p className={`${panelClass} text-center text-[var(--muted)]`}>{children}</p>;
}
export function Tabs({ value, onChange, items, children, label }: { value: string; onChange: (value: string) => void;
  items: Array<{ value: string; label: string }>; children: ReactNode; label: string }) {
  const id = useId();
  const refs = useRef<Array<HTMLButtonElement | null>>([]);
  return <div className="space-y-5">
    <label className="block text-sm font-semibold md:hidden">{label}<select className={fieldClass} value={value} onChange={(e) => onChange(e.target.value)}>{items.map((item) => <option key={item.value} value={item.value}>{item.label}</option>)}</select></label>
    <div role="tablist" aria-label={label} className="hidden gap-1 overflow-x-auto border-b border-[var(--line)] pb-2 md:flex">
      {items.map((item, index) => <button key={item.value} ref={(node) => { refs.current[index] = node; }} role="tab" type="button"
        id={`${id}-${item.value}`} aria-selected={value === item.value} aria-controls={`${id}-panel`}
        tabIndex={value === item.value ? 0 : -1} onClick={() => onChange(item.value)}
        onKeyDown={(e) => {
          const next = e.key === "ArrowRight" ? (index + 1) % items.length : e.key === "ArrowLeft" ? (index + items.length - 1) % items.length : e.key === "Home" ? 0 : e.key === "End" ? items.length - 1 : null;
          if (next !== null) { e.preventDefault(); onChange(items[next].value); refs.current[next]?.focus(); }
        }} className={`min-h-11 shrink-0 rounded-xl px-4 font-semibold ${value === item.value ? "bg-[var(--teal)] text-white" : "text-[var(--muted)]"}`}>{item.label}</button>)}
    </div>
    <div role="tabpanel" id={`${id}-panel`} aria-labelledby={`${id}-${value}`}>{children}</div>
  </div>;
}
export function Dialog({ title, children, onClose, returnFocusTo }: { title: string; children: ReactNode; onClose: () => void; returnFocusTo?: HTMLElement | null }) {
  const ref = useRef<HTMLDialogElement>(null);
  const originalTrigger = useRef<HTMLElement | null>(null);
  const id = useId();
  const t = useTranslations("community");
  useEffect(() => {
    const dialog = ref.current;
    if (!originalTrigger.current) originalTrigger.current = returnFocusTo || (document.activeElement instanceof HTMLElement ? document.activeElement : null);
    const trigger = originalTrigger.current;
    if (dialog && !dialog.open) dialog.showModal();
    // Native cancel focus restoration can run after React removes the dialog.
    // Restore on the following frame, once both the top layer and DOM have settled.
    return () => { requestAnimationFrame(() => { if (!dialog?.isConnected && trigger?.isConnected) trigger.focus(); }); };
  }, [returnFocusTo]);
  return <dialog ref={ref} aria-labelledby={id} onCancel={(event) => {
    event.stopPropagation();
    if (event.target !== event.currentTarget) return;
    event.preventDefault();
    onClose();
  }} onClose={(event) => {
    event.stopPropagation();
    if (event.target === event.currentTarget) onClose();
  }}
    className="m-auto max-h-[90dvh] w-[min(42rem,calc(100%-2rem))] overflow-y-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-6 text-[var(--ink)] backdrop:bg-black/50">
    <div className="mb-5 flex items-center justify-between gap-3"><h2 id={id} className="text-xl font-bold">{title}</h2><Button secondary onClick={onClose}>{t("close")}</Button></div>{children}
  </dialog>;
}
export function CommunityImage(props: { id:string;alt:string;review?:boolean;thumbnail?:boolean }) {
  return <SignedImage key={`${props.id}:${props.review}:${props.thumbnail}`} {...props} />;
}
function SignedImage({id,alt,review=false,thumbnail=false}:{id:string;alt:string;review?:boolean;thumbnail?:boolean}) {
  const t = useTranslations("community");
  const { sessionIdentity } = useHeaderSession();
  const [image,setImage]=useState<{identity:object|null;url?:string;error?:unknown}>();
  const current = image?.identity === sessionIdentity ? image : undefined;
  const url = current?.url;
  const error = current?.error;
  const [attempt, setAttempt] = useState(0);
  const box=useRef<HTMLDivElement>(null);
  useEffect(()=>{
    let live=true;
    const fetchImage=()=>{api<{url:string}>(`${review?"/admin/community":"/community"}/media/${id}${thumbnail?"?thumbnail=true":""}`)
      .then((data)=>{if(live)setImage({identity:sessionIdentity,url:data.url});}).catch((error)=>{if(live)setImage({identity:sessionIdentity,error});});};
    const observer=typeof IntersectionObserver==="undefined"?null:new IntersectionObserver((entries)=>{
      if(entries.some((entry)=>entry.isIntersecting)){observer?.disconnect();fetchImage();}
    },{rootMargin:"200px"});
    if(observer&&box.current)observer.observe(box.current);else fetchImage();
    return ()=>{live=false;observer?.disconnect();};
  },[id,review,thumbnail,attempt,sessionIdentity]);
  return <div ref={box}>{error ? <div className="space-y-2"><ErrorNotice error={error}/>
    <Button secondary onClick={() => {
      // Reauthorize on each user-requested retry. Never reuse an expired URL or
      // bypass visibility checks for content that was withdrawn in the meantime.
      setImage(undefined); setAttempt((value) => value + 1);
    }}>{t("retry")}</Button></div> : url ?
    // Fetch only when near the viewport and load immediately within the 60-second authorization.
    // eslint-disable-next-line @next/next/no-img-element
    <img src={url} alt={alt} referrerPolicy="no-referrer" onError={()=>setImage({identity:sessionIdentity,error:new Error()})} className="max-h-[36rem] w-full rounded-xl object-contain"/>
    : <div className="aspect-video animate-pulse rounded-xl bg-[var(--paper)]" aria-busy="true"/>}</div>;
}
