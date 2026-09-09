"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import { useLocale } from "next-intl";
import { itineraryCopy, itineraryText } from "@/lib/itinerary-copy";

/** Pointer drag is confined to a dedicated handle, leaving the card scrollable. */
export function EditableItineraryTimeline({
  children, onMove, onOpenMove,
}: { children: ReactNode; onMove: (id: string, beforeId?: string) => void; onOpenMove: (id: string) => void }) {
  const ref = useRef<HTMLOListElement>(null);
  const drag = useRef<{ id: string; title: string; x: number; y: number; active: boolean; target?: string } | undefined>(undefined);
  const callback = useRef(onMove);
  const openMove = useRef(onOpenMove);
  const suppressClick = useRef(false);
  const [moving, setMoving] = useState("");
  const copy = itineraryCopy(useLocale());
  useEffect(() => { callback.current = onMove; }, [onMove]);
  useEffect(() => { openMove.current = onOpenMove; }, [onOpenMove]);
  useEffect(() => {
    const list = ref.current;
    if (!list) return;
    let scrollFrame = 0;
    let pointerY = 0;
    function clear() {
      cancelAnimationFrame(scrollFrame);
      list?.querySelectorAll("[data-drop-active]").forEach((node) => node.removeAttribute("data-drop-active"));
      list?.querySelectorAll("[data-drag-active]").forEach((node) => node.removeAttribute("data-drag-active"));
      drag.current = undefined; setMoving("");
    }
    function locate(y: number) {
      const current = drag.current;
      if (!current || !list) return;
      const gaps = Array.from(list.querySelectorAll<HTMLElement>("[data-itinerary-gap]"))
        .filter((node) => node.dataset.itineraryGap !== current.id);
      let closest: HTMLElement | undefined;
      let distance = Infinity;
      for (const gap of gaps) {
        const rect = gap.getBoundingClientRect();
        const delta = Math.abs(rect.top + rect.height / 2 - y);
        if (delta < distance) { closest = gap; distance = delta; }
        gap.removeAttribute("data-drop-active");
      }
      closest?.setAttribute("data-drop-active", "true");
      current.target = closest?.dataset.itineraryGap;
    }
    function scroll() {
      const direction = pointerY < 110 ? -9 : pointerY > window.innerHeight - 150 ? 9 : 0;
      if (direction) { window.scrollBy(0, direction); locate(pointerY); }
      scrollFrame = requestAnimationFrame(scroll);
    }
    function move(event: PointerEvent) {
      const current = drag.current;
      if (!current) return;
      pointerY = event.clientY;
      if (!current.active && Math.hypot(event.clientX - current.x, event.clientY - current.y) < 6) return;
      event.preventDefault();
      if (!current.active) {
        current.active = true;
        list?.querySelector<HTMLElement>(`[data-stop-id="${current.id}"]`)?.setAttribute("data-drag-active", "true");
        setMoving(current.title);
        scrollFrame = requestAnimationFrame(scroll);
      }
      locate(event.clientY);
    }
    function finish(event: PointerEvent) {
      if (!drag.current) return;
      const current = drag.current;
      if (current.active) {
        suppressClick.current = true;
        event.preventDefault();
        if (current.target !== undefined) callback.current(current.id, current.target || undefined);
      }
      clear();
    }
    function escape(event: KeyboardEvent) {
      if (event.key === "Escape" && drag.current) {
        event.preventDefault(); suppressClick.current = true; clear();
      }
    }
    window.addEventListener("pointermove", move, { passive: false });
    window.addEventListener("pointerup", finish);
    window.addEventListener("pointercancel", clear);
    window.addEventListener("keydown", escape);
    return () => {
      cancelAnimationFrame(scrollFrame);
      window.removeEventListener("pointermove", move); window.removeEventListener("pointerup", finish);
      window.removeEventListener("pointercancel", clear); window.removeEventListener("keydown", escape);
    };
  }, []);
  return <>
    <ol ref={ref} className="planner-timeline itinerary-editable-timeline relative"
      onPointerDown={(event) => {
        const handle = (event.target as HTMLElement).closest<HTMLElement>("[data-itinerary-drag]");
        if (!handle || event.button !== 0) return;
        suppressClick.current = false;
        handle.setPointerCapture?.(event.pointerId);
        drag.current = { id: handle.dataset.itineraryDrag!, title: handle.dataset.stopTitle || "", x: event.clientX, y: event.clientY, active: false };
      }}
      onClick={(event) => {
        const handle = (event.target as HTMLElement).closest<HTMLElement>("[data-itinerary-drag]");
        if (!handle) return;
        if (event.detail === 0 || !suppressClick.current) openMove.current(handle.dataset.itineraryDrag!);
        suppressClick.current = false;
      }}
    >{children}</ol>
    <span className="sr-only" role="status" aria-live="polite">{moving ? itineraryText(copy.moving, { title: moving }) : ""}</span>
  </>;
}
