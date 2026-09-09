"use client";

import { ArrowLeft, X } from "lucide-react";
import { useLocale } from "next-intl";
import { useCallback, useEffect, useId, useRef, useState, useSyncExternalStore, type ReactNode } from "react";
import { createPortal } from "react-dom";
import { plannerOverlayCopy } from "@/components/planner/overlay-copy";

type PlannerOverlayProps = {
  open: boolean; title: string; description?: string; onClose: () => void; onBack?: () => void;
  children: ReactNode; footer?: ReactNode; size?: "default" | "wide";
  expandable?: boolean; defaultExpanded?: boolean;
};
type OverlayLayer = { container: HTMLDivElement; panel: HTMLElement };
const layers: OverlayLayer[] = [];
let scrollSnapshot: {
  styles: { overflow: string; position: string; top: string; left: string; width: string; paddingRight: string };
  rootOverflow: string; x: number; y: number; focus: HTMLElement | null;
} | undefined;
const subscribeToClient = () => () => undefined;
const themeVariables = [
  "--ink", "--muted", "--paper", "--surface", "--surface-raised", "--surface-tint",
  "--teal", "--teal-dark", "--teal-soft", "--teal-fill", "--teal-fill-hover",
  "--coral", "--coral-soft", "--line",
];

function syncLayers() {
  layers.forEach((layer, index) => {
    const inactive = index !== layers.length - 1;
    layer.container.inert = inactive;
    if (inactive) layer.container.setAttribute("aria-hidden", "true");
    else layer.container.removeAttribute("aria-hidden");
  });
}

function lockPage() {
  if (scrollSnapshot) return;
  const body = document.body;
  scrollSnapshot = {
    styles: {
      overflow: body.style.overflow, position: body.style.position,
      top: body.style.top, left: body.style.left, width: body.style.width, paddingRight: body.style.paddingRight,
    },
    rootOverflow: document.documentElement.style.overflow,
    x: window.scrollX, y: window.scrollY,
    focus: document.activeElement instanceof HTMLElement ? document.activeElement : null,
  };
  // Fixed positioning also stops background rubber-band scrolling on mobile Safari.
  const gutter = Math.max(0, window.innerWidth - document.documentElement.clientWidth);
  if (gutter && document.documentElement.clientWidth) {
    body.style.paddingRight = `${(parseFloat(getComputedStyle(body).paddingRight) || 0) + gutter}px`;
  }
  Object.assign(body.style, {
    overflow: "hidden", position: "fixed", top: `${-window.scrollY}px`, left: `${-window.scrollX}px`, width: "100%",
  });
  document.documentElement.style.overflow = "hidden";
}

function unlockPage() {
  if (layers.length || !scrollSnapshot) return undefined;
  const snapshot = scrollSnapshot;
  scrollSnapshot = undefined;
  Object.assign(document.body.style, snapshot.styles);
  document.documentElement.style.overflow = snapshot.rootOverflow;
  if (window.scrollX !== snapshot.x || window.scrollY !== snapshot.y) {
    window.scrollTo({ left: snapshot.x, top: snapshot.y, behavior: "instant" });
  }
  return snapshot.focus;
}

function focusableElements(panel: HTMLElement) {
  return Array.from(panel.querySelectorAll<HTMLElement>(
    "button:not(:disabled), input:not(:disabled):not([type='hidden']), select:not(:disabled), textarea:not(:disabled), a[href], summary, [tabindex]:not([tabindex='-1'])",
  )).sort((left, right) => left === right ? 0 : left.compareDocumentPosition(right) & Node.DOCUMENT_POSITION_FOLLOWING ? -1 : 1).filter((element) => {
    if (element.tabIndex < 0 || element.closest("[hidden], [inert], [aria-hidden='true']")) return false;
    const closedDetails = element.closest("details:not([open])");
    if (closedDetails && !closedDetails.querySelector(":scope > summary")?.contains(element)) return false;
    for (let node: HTMLElement | null = element; node && node !== panel; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.display === "none" || style.visibility === "hidden") return false;
    }
    return true;
  });
}

// Older service sheets use useModalSheet instead of registering in this stack.
// Their own keyboard trap must win while mounted inside a contextual tool panel.
function hasNestedModal(panel: HTMLElement) {
  return Array.from(panel.querySelectorAll<HTMLElement>('[role="dialog"][aria-modal="true"]')).some((dialog) => {
    if (dialog.closest('[hidden], [inert], [aria-hidden="true"]')) return false;
    for (let node: HTMLElement | null = dialog; node && node !== panel; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.display === "none" || style.visibility === "hidden") return false;
    }
    return true;
  });
}

export function PlannerOverlay(props: PlannerOverlayProps) {
  // Reopening resets presentation only; controlled drafts remain owned by the parent.
  return props.open ? <OpenPlannerOverlay {...props} /> : null;
}

function OpenPlannerOverlay({
  title, description, onClose, onBack, children, footer,
  size = "default", expandable = false, defaultExpanded = false,
}: PlannerOverlayProps) {
  const copy = plannerOverlayCopy(useLocale());
  const id = useId();
  const contextRef = useRef<HTMLSpanElement>(null);
  const containerRef = useRef<HTMLDivElement>(null);
  const panelRef = useRef<HTMLElement>(null);
  const onCloseRef = useRef(onClose);
  const [expanded, setExpanded] = useState(defaultExpanded);
  const mounted = useSyncExternalStore(subscribeToClient, () => true, () => false);
  useEffect(() => { onCloseRef.current = onClose; }, [onClose]);
  const closeOverlay = useCallback(() => onCloseRef.current(), []);

  useEffect(() => {
    const container = containerRef.current;
    const source = contextRef.current?.closest<HTMLElement>("[data-planner-theme]");
    if (!mounted || !container || !source) return;
    function copyTheme() {
      if (!container || !source) return;
      container.dataset.plannerTheme = source.dataset.plannerTheme || "";
      const style = getComputedStyle(source);
      for (const variable of themeVariables) {
        const value = style.getPropertyValue(variable);
        if (value) container.style.setProperty(variable, value);
        else container.style.removeProperty(variable);
      }
    }
    copyTheme();
    const observer = new MutationObserver(copyTheme);
    observer.observe(source, { attributes: true, attributeFilter: ["data-planner-theme", "class", "style"] });
    observer.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme", "class"] });
    return () => observer.disconnect();
  }, [mounted]);

  useEffect(() => {
    const panel = panelRef.current;
    const container = containerRef.current;
    if (!mounted || !panel || !container) return;
    const previousFocus = document.activeElement instanceof HTMLElement ? document.activeElement : null;
    const layer = { container, panel };
    lockPage();
    layers.push(layer);
    syncLayers();
    const isTop = () => layers.at(-1) === layer;
    const focusFrame = requestAnimationFrame(() => {
      if (isTop() && !hasNestedModal(panel)) (panel.querySelector<HTMLElement>("[data-planner-close]") || panel).focus({ preventScroll: true });
    });
    function onKeyDown(event: KeyboardEvent) {
      if (!isTop() || hasNestedModal(panel!) || event.defaultPrevented || event.isComposing) return;
      if (event.key === "Escape") {
        event.preventDefault(); closeOverlay(); return;
      }
      if (event.key !== "Tab") return;
      const candidates = focusableElements(panel!);
      const first = candidates[0];
      const last = candidates.at(-1);
      if (!first || !last) {
        event.preventDefault(); panel!.focus({ preventScroll: true });
      } else if (!panel!.contains(document.activeElement)
        || (event.shiftKey && (document.activeElement === first || document.activeElement === panel))) {
        event.preventDefault(); (event.shiftKey ? last : first).focus({ preventScroll: true });
      } else if (!event.shiftKey && document.activeElement === last) {
        event.preventDefault(); first.focus({ preventScroll: true });
      }
    }
    document.addEventListener("keydown", onKeyDown);
    return () => {
      cancelAnimationFrame(focusFrame);
      document.removeEventListener("keydown", onKeyDown);
      const wasTop = isTop();
      const index = layers.indexOf(layer);
      if (index !== -1) layers.splice(index, 1);
      syncLayers();
      const initialFocus = unlockPage();
      if (!wasTop) return;
      const target = previousFocus?.isConnected && !previousFocus.closest("[inert]")
        ? previousFocus : layers.at(-1)?.panel || initialFocus;
      target?.focus({ preventScroll: true });
    };
  }, [closeOverlay, mounted]);

  if (!mounted) return null;
  return <><span ref={contextRef} hidden aria-hidden="true" />{createPortal(
    <div ref={containerRef} className="planner-overlay planner-overlay-contextual" role="presentation" onMouseDown={(event) => {
      if (event.currentTarget === event.target && layers.at(-1)?.container === event.currentTarget) closeOverlay();
    }}>
      <section ref={panelRef} role="dialog" aria-modal="true" tabIndex={-1}
        aria-labelledby={`${id}-title`} aria-describedby={description ? `${id}-description` : undefined}
        className={`planner-sheet ${size === "wide" ? "planner-sheet-wide" : ""} ${expandable ? "planner-sheet-collapsible" : ""} ${expanded ? "planner-sheet-expanded" : ""}`}>
        {expandable ? <button type="button" aria-label={expanded ? copy.collapse : copy.expand} aria-expanded={expanded} onClick={() => setExpanded((value) => !value)} className="planner-sheet-toggle"><span className="planner-sheet-handle" aria-hidden="true" /></button> : <div className="planner-sheet-handle" aria-hidden="true" />}
        <header className="planner-sheet-header flex items-start justify-between gap-3 border-b border-[var(--line)] px-5 py-4 sm:px-6">
          {onBack && <button type="button" onClick={onBack} aria-label={copy.back} className="grid min-h-11 min-w-11 place-items-center rounded-full text-[var(--muted)]"><ArrowLeft size={20} /></button>}
          <div className="min-w-0 flex-1">
            <h2 id={`${id}-title`} className="text-xl font-bold">{title}</h2>
            {description && <p id={`${id}-description`} className="mt-1 text-sm leading-6 text-[var(--muted)]">{description}</p>}
          </div>
          <button type="button" data-planner-close onClick={closeOverlay} aria-label={copy.close} className="grid min-h-11 min-w-11 shrink-0 place-items-center rounded-full bg-[var(--paper)] text-[var(--muted)] transition hover:text-[var(--ink)]"><X size={20} /></button>
        </header>
        <div className="planner-sheet-body">{children}</div>
        {footer && <footer className="planner-sheet-footer">{footer}</footer>}
      </section>
    </div>, document.body,
  )}</>;
}
