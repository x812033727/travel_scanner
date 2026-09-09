"use client";

import { useRef, useState, type ReactNode } from "react";
import { ChevronRight, Luggage, Settings2, Share2, ArrowLeft } from "lucide-react";
import { plannerCopy } from "@/lib/planner-copy";

export function PlannerToolSections({ locale, preparation, settings, sharing, disabled = false, beforeSectionChange }: {
  locale: string; preparation: ReactNode; settings: ReactNode; sharing: ReactNode; disabled?: boolean;
  beforeSectionChange?: (proceed: () => void) => boolean;
}) {
  const copy = plannerCopy(locale);
  const [section, setSection] = useState<"preparation" | "settings" | "sharing">();
  const menuRef = useRef<HTMLDivElement>(null);
  const headingRef = useRef<HTMLHeadingElement>(null);
  function open(next: typeof section) {
    if (disabled) return;
    const proceed = () => {
      const previous = section;
      setSection(next);
      requestAnimationFrame(() => {
        if (next) headingRef.current?.focus();
        else menuRef.current?.querySelector<HTMLButtonElement>(`[data-section="${previous}"]`)?.focus();
      });
    };
    if (beforeSectionChange?.(proceed) === false) return;
    proceed();
  }
  if (section) return <div className="premium-tool-section">
    <button type="button" disabled={disabled} className="premium-panel-back" onClick={() => open(undefined)}><ArrowLeft size={16} />{copy.back}</button>
    <h3 ref={headingRef} tabIndex={-1} className="mb-4 text-xl font-bold">{copy[section]}</h3>
    <div className="space-y-4">{{ preparation, settings, sharing }[section]}</div>
  </div>;
  return <div ref={menuRef} className="premium-tool-sections">
    {([['preparation', Luggage], ['settings', Settings2], ['sharing', Share2]] as const).map(([id, Icon]) =>
      <button key={id} type="button" disabled={disabled} data-section={id} onClick={() => open(id)} className="premium-tool-entry">
        <span className="premium-tool-entry-icon"><Icon size={23} /></span>
        <span><strong>{copy[id]}</strong><small>{copy[`${id}Hint`]}</small></span><ChevronRight size={18} />
      </button>)}
  </div>;
}
