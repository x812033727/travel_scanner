"use client";

import type { ReactNode } from "react";
import { ChevronDown, Hotel, Plane, UtensilsCrossed } from "lucide-react";

export function OptionalStop({ collapsed, kind, title, hint, children }: {
  collapsed: boolean; kind: "flight" | "hotel" | "meal"; title: string; hint: string; children: ReactNode;
}) {
  if (!collapsed) return children;
  const Icon = kind === "flight" ? Plane : kind === "hotel" ? Hotel : UtensilsCrossed;
  return <details className="premium-optional-stop"><summary>
    <Icon size={17} /><span><strong>{title}</strong><small>{hint}</small></span><ChevronDown size={16} />
  </summary><div className="premium-optional-stop-body">{children}</div></details>;
}
