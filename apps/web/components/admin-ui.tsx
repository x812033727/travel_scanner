"use client";

import { AlertTriangle, Inbox, LoaderCircle, RefreshCw, X } from "lucide-react";
import { useEffect, useRef, type ReactNode } from "react";

export function AdminPageHeader({ eyebrow = "OPERATIONS", title, description, actions }: { eyebrow?: string; title: string; description: string; actions?: ReactNode }) {
  return <header className="flex flex-col justify-between gap-5 md:flex-row md:items-end"><div className="min-w-0"><p className="text-xs font-black tracking-[.16em] text-[var(--teal)]">{eyebrow}</p><h1 className="mt-2 text-3xl font-black tracking-[-.025em] md:text-4xl">{title}</h1><p className="mt-3 max-w-3xl leading-7 text-[var(--muted)]">{description}</p></div>{actions && <div className="flex flex-wrap gap-2">{actions}</div>}</header>;
}

const statusTones: Record<string, string> = {
  healthy: "bg-emerald-50 text-emerald-800", ok: "bg-emerald-50 text-emerald-800", succeeded: "bg-emerald-50 text-emerald-800", active: "bg-emerald-50 text-emerald-800",
  degraded: "bg-amber-50 text-amber-800", warning: "bg-amber-50 text-amber-800", pending: "bg-amber-50 text-amber-800", queued: "bg-sky-50 text-sky-800", running: "bg-sky-50 text-sky-800",
  unavailable: "bg-red-50 text-red-800", failed: "bg-red-50 text-red-800", suspended: "bg-red-50 text-red-800", inactive: "bg-slate-100 text-slate-700", disabled: "bg-slate-100 text-slate-700",
};
export function AdminStatusPill({ status, children = status }: { status: string; children?: ReactNode }) {
  return <span className={`inline-flex min-h-7 shrink-0 items-center whitespace-nowrap rounded-full px-2.5 py-1 text-xs font-bold ${statusTones[status] ?? "bg-slate-100 text-slate-700"}`}>{children}</span>;
}

export function AdminFilterBar({ children }: { children: ReactNode }) {
  return <div className="mt-6 flex flex-col gap-3 rounded-2xl border border-[var(--line)] bg-[var(--surface)] p-3 shadow-[var(--shadow-sm)] sm:flex-row sm:flex-wrap sm:items-end">{children}</div>;
}

export function AdminSkeleton({ label = "Loading" }: { label?: string }) {
  return <div role="status" className="mt-6 grid gap-3" aria-label={label}><span className="sr-only">{label}</span>{[1, 2, 3].map((item) => <span key={item} className="h-20 animate-pulse rounded-2xl bg-slate-200/65 motion-reduce:animate-none" />)}</div>;
}

export function AdminEmptyState({ title, detail, action }: { title: string; detail?: string; action?: ReactNode }) {
  return <section className="mt-6 rounded-[1.5rem] border border-dashed border-[var(--line)] bg-[var(--surface)] p-8 text-center"><Inbox aria-hidden className="mx-auto text-[var(--muted)]" size={30} /><h2 className="mt-4 font-bold">{title}</h2>{detail && <p className="mx-auto mt-2 max-w-lg text-sm leading-6 text-[var(--muted)]">{detail}</p>}{action && <div className="mt-5">{action}</div>}</section>;
}

export function AdminErrorState({ title, detail, retry, retryLabel = "Retry" }: { title: string; detail: string; retry?: () => void; retryLabel?: string }) {
  return <section role="alert" className="mt-6 rounded-[1.5rem] border border-red-200 bg-red-50 p-6 text-red-950"><div className="flex items-start gap-3"><AlertTriangle aria-hidden className="mt-0.5 shrink-0" size={21} /><div className="min-w-0 flex-1"><h2 className="font-bold">{title}</h2><p className="mt-1 break-words text-sm leading-6">{detail}</p>{retry && <button type="button" onClick={retry} className="mt-4 inline-flex min-h-11 items-center gap-2 rounded-xl bg-white px-4 text-sm font-bold shadow-sm"><RefreshCw aria-hidden size={16} />{retryLabel}</button>}</div></div></section>;
}

export function AdminDataTable({ label, headers, children }: { label: string; headers: string[]; children: ReactNode }) {
  return <div className="mt-5 overflow-x-auto rounded-2xl border border-[var(--line)] bg-[var(--surface)]"><table aria-label={label} className="admin-responsive-table w-full min-w-[760px] text-left text-sm"><thead><tr className="border-b border-[var(--line)] bg-[var(--paper)] text-xs text-[var(--muted)]">{headers.map((header) => <th key={header} className="px-4 py-3 font-bold">{header}</th>)}</tr></thead><tbody>{children}</tbody></table></div>;
}

export function AdminDetailDrawer({ open, title, onClose, children, footer, closeLabel = "Close" }: { open: boolean; title: string; onClose: () => void; children: ReactNode; footer?: ReactNode; closeLabel?: string }) {
  const panel = useRef<HTMLElement>(null);
  const close = useRef<HTMLButtonElement>(null);
  const onCloseRef = useRef(onClose);
  useEffect(() => { onCloseRef.current = onClose; }, [onClose]);
  useEffect(() => {
    if (!open) return;
    const previous = document.activeElement as HTMLElement | null;
    close.current?.focus();
    const keydown = (event: KeyboardEvent) => {
      if (event.key === "Escape") { event.preventDefault(); onCloseRef.current(); return; }
      if (event.key !== "Tab" || !panel.current) return;
      const focusable = Array.from(panel.current.querySelectorAll<HTMLElement>("button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href]"));
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    };
    document.addEventListener("keydown", keydown);
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.removeEventListener("keydown", keydown); document.body.style.overflow = overflow; previous?.focus(); };
  }, [open]);
  if (!open) return null;
  return <div className="fixed inset-0 z-[95] bg-slate-950/45" role="presentation" onMouseDown={(event) => { if (event.currentTarget === event.target) onClose(); }}><aside ref={panel} role="dialog" aria-modal="true" aria-labelledby="admin-detail-title" className="absolute inset-y-0 right-0 flex w-full max-w-2xl flex-col overflow-hidden bg-[var(--surface)] shadow-2xl"><header className="flex min-h-[4.5rem] items-center justify-between gap-4 border-b border-[var(--line)] px-5"><h2 id="admin-detail-title" className="min-w-0 truncate text-xl font-black">{title}</h2><button ref={close} type="button" aria-label={closeLabel} onClick={onClose} className="admin-icon-button"><X aria-hidden size={20} /></button></header><div className="min-h-0 flex-1 overflow-y-auto overscroll-contain p-5 md:p-7">{children}</div>{footer && <footer className="border-t border-[var(--line)] bg-[var(--surface)] p-4">{footer}</footer>}</aside></div>;
}

export function AdminConfirmDialog({ open, title, description, confirmationLabel, confirmation, expectedConfirmation, password, passwordLabel, recoveryAction, busy, cancelLabel = "Cancel", confirmLabel = "Confirm", onConfirmationChange, onPasswordChange, onCancel, onConfirm }: { open: boolean; title: string; description: string; confirmationLabel: string; confirmation: string; expectedConfirmation: string; password: string; passwordLabel: string; recoveryAction?: ReactNode; busy?: boolean; cancelLabel?: string; confirmLabel?: string; onConfirmationChange: (value: string) => void; onPasswordChange: (value: string) => void; onCancel: () => void; onConfirm: () => void }) {
  const input = useRef<HTMLInputElement>(null);
  const panel = useRef<HTMLElement>(null);
  const onCancelRef = useRef(onCancel);
  const busyRef = useRef(Boolean(busy));
  useEffect(() => { onCancelRef.current = onCancel; busyRef.current = Boolean(busy); }, [busy, onCancel]);
  useEffect(() => {
    if (!open) return;
    const previous = document.activeElement as HTMLElement | null;
    input.current?.focus();
    const keydown = (event: KeyboardEvent) => {
      if (event.key === "Escape") {
        if (!busyRef.current) { event.preventDefault(); onCancelRef.current(); }
        return;
      }
      if (event.key !== "Tab" || !panel.current) return;
      const focusable = Array.from(panel.current.querySelectorAll<HTMLElement>("button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href]"));
      const first = focusable[0], last = focusable[focusable.length - 1];
      if (event.shiftKey && document.activeElement === first) { event.preventDefault(); last?.focus(); }
      else if (!event.shiftKey && document.activeElement === last) { event.preventDefault(); first?.focus(); }
    };
    document.addEventListener("keydown", keydown);
    const overflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { document.removeEventListener("keydown", keydown); document.body.style.overflow = overflow; previous?.focus(); };
  }, [open]);
  if (!open) return null;
  return <div className="fixed inset-0 z-[110] grid place-items-center overflow-y-auto bg-slate-950/55 p-4" role="presentation" onMouseDown={(event) => { if (event.currentTarget === event.target && !busy) onCancel(); }}><section ref={panel} role="dialog" aria-modal="true" aria-labelledby="admin-confirm-title" className="w-full max-w-lg rounded-[1.75rem] bg-[var(--surface)] p-6 shadow-2xl"><h2 id="admin-confirm-title" className="text-2xl font-black">{title}</h2><p className="mt-2 text-sm leading-6 text-[var(--muted)]">{description}</p>{recoveryAction && <div className="mt-3 text-sm font-semibold text-[var(--teal)]">{recoveryAction}</div>}<label className="mt-5 block text-sm font-bold">{passwordLabel}<input ref={input} type="password" autoComplete="current-password" value={password} onChange={(event) => onPasswordChange(event.target.value)} className="mt-2 min-h-12 w-full rounded-xl border border-[var(--line)] px-4" /></label><label className="mt-4 block text-sm font-bold">{confirmationLabel}<code className="ml-2 rounded bg-[var(--paper)] px-1.5 py-0.5">{expectedConfirmation}</code><input value={confirmation} onChange={(event) => onConfirmationChange(event.target.value)} className="mt-2 min-h-12 w-full rounded-xl border border-[var(--line)] px-4 font-mono" /></label><div className="mt-6 flex flex-col-reverse gap-2 sm:flex-row sm:justify-end"><button type="button" disabled={busy} onClick={onCancel} className="min-h-12 rounded-xl border border-[var(--line)] px-5 font-bold disabled:opacity-50">{cancelLabel}</button><button type="button" disabled={busy || !password || confirmation !== expectedConfirmation} onClick={onConfirm} className="inline-flex min-h-12 items-center justify-center gap-2 rounded-xl bg-[var(--coral-fill)] px-5 font-bold text-white disabled:opacity-40">{busy && <LoaderCircle aria-hidden className="animate-spin motion-reduce:animate-none" size={17} />}{confirmLabel}</button></div></section></div>;
}
