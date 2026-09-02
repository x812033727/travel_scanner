"use client";

import { X } from "lucide-react";
import { useCallback, useEffect, useRef, useState, type ReactNode } from "react";

type PlannerOverlayProps = {
  open: boolean;
  title: string;
  description?: string;
  onClose: () => void;
  children: ReactNode;
  footer?: ReactNode;
  size?: "default" | "wide";
  expandable?: boolean;
  defaultExpanded?: boolean;
};

export function PlannerOverlay({
  open,
  title,
  description,
  onClose,
  children,
  footer,
  size = "default",
  expandable = false,
  defaultExpanded = false,
}: PlannerOverlayProps) {
  const panelRef = useRef<HTMLElement>(null);
  const onCloseRef = useRef(onClose);
  const [expanded, setExpanded] = useState(defaultExpanded || expandable);

  useEffect(() => {
    onCloseRef.current = onClose;
  }, [onClose]);

  const closeOverlay = useCallback(() => {
    setExpanded(defaultExpanded || expandable);
    onCloseRef.current();
  }, [defaultExpanded, expandable]);

  useEffect(() => {
    if (!open) return;
    const previousFocus = document.activeElement as HTMLElement | null;
    const previousOverflow = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    const panel = panelRef.current;
    const focusables = () => Array.from(
      panel?.querySelectorAll<HTMLElement>(
        "button:not([disabled]), input:not([disabled]), select:not([disabled]), textarea:not([disabled]), a[href], [tabindex]:not([tabindex='-1'])",
      ) || [],
    );
    const focusFrame = requestAnimationFrame(() => focusables()[0]?.focus());

    function onKeyDown(event: KeyboardEvent) {
      if (event.key === "Escape") {
        event.preventDefault();
        closeOverlay();
        return;
      }
      if (event.key !== "Tab") return;
      const candidates = focusables();
      if (!candidates.length) return;
      const first = candidates[0];
      const last = candidates[candidates.length - 1];
      if (event.shiftKey && document.activeElement === first) {
        event.preventDefault();
        last.focus();
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault();
        first.focus();
      }
    }

    document.addEventListener("keydown", onKeyDown);
    return () => {
      cancelAnimationFrame(focusFrame);
      document.removeEventListener("keydown", onKeyDown);
      document.body.style.overflow = previousOverflow;
      previousFocus?.focus();
    };
  }, [closeOverlay, open]);

  if (!open) return null;

  return (
    <div className="planner-overlay" role="presentation" onMouseDown={(event) => {
      if (event.currentTarget === event.target) closeOverlay();
    }}>
      <section
        ref={panelRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby="planner-overlay-title"
        aria-describedby={description ? "planner-overlay-description" : undefined}
        className={`planner-sheet ${size === "wide" ? "planner-sheet-wide" : ""} ${expandable ? "planner-sheet-collapsible" : ""} ${expanded ? "planner-sheet-expanded" : ""}`}
      >
        {expandable ? <button type="button" aria-label={expanded ? "縮小路線面板" : "全螢幕顯示路線面板"} aria-pressed={expanded} onClick={() => setExpanded((value) => !value)} className="planner-sheet-toggle"><span className="planner-sheet-handle" aria-hidden="true" /></button> : <div className="planner-sheet-handle" aria-hidden="true" />}
        <header className="planner-sheet-header flex items-start justify-between gap-4 border-b border-[var(--line)] px-5 py-4 sm:px-6">
          <div>
            <h2 id="planner-overlay-title" className="text-xl font-bold">{title}</h2>
            {description && <p id="planner-overlay-description" className="mt-1 text-sm leading-6 text-[var(--muted)]">{description}</p>}
          </div>
          <button type="button" onClick={closeOverlay} aria-label="關閉" className="grid min-h-11 min-w-11 place-items-center rounded-full bg-[var(--paper)] text-[var(--muted)] transition hover:text-[var(--ink)]">
            <X size={20} />
          </button>
        </header>
        <div className="planner-sheet-body">{children}</div>
        {footer && <footer className="planner-sheet-footer">{footer}</footer>}
      </section>
    </div>
  );
}
