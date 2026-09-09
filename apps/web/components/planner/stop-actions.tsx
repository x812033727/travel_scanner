"use client";

import { useEffect, useRef, type ReactNode } from "react";
import { Ellipsis } from "lucide-react";

/** A native disclosure, not a second modal. Ordinary buttons keep keyboard semantics. */
export function StopActions({ label, children }: { label: string; children: ReactNode }) {
  const ref = useRef<HTMLDetailsElement>(null);
  useEffect(() => {
    const closeOutside = (event: PointerEvent) => {
      if (ref.current?.open && event.target instanceof Node && !ref.current.contains(event.target)) ref.current.open = false;
    };
    document.addEventListener("pointerdown", closeOutside);
    return () => document.removeEventListener("pointerdown", closeOutside);
  }, []);
  return <details ref={ref} className="premium-stop-actions" onKeyDown={(event) => {
    if (event.key === "Escape" && ref.current?.open) {
      event.preventDefault(); event.stopPropagation(); ref.current.open = false;
      ref.current.querySelector("summary")?.focus();
    }
  }}>
    <summary aria-label={label}><Ellipsis size={21} /></summary>
    <div className="premium-stop-action-list" onClick={(event) => {
      if (event.target instanceof Element && event.target.closest("button") && ref.current) {
        ref.current.open = false;
        ref.current.querySelector("summary")?.focus();
      }
    }}>{children}</div>
  </details>;
}
