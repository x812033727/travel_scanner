"use client";

import type { ReactNode } from "react";
import { ChevronDown, Hotel, Plane, UtensilsCrossed } from "lucide-react";
import { useTranslations } from "next-intl";
import type { TripItem } from "@/lib/trip-types";
import { getStopTone, stopToneClassName } from "./stop-tone";

export function OptionalStop({ collapsed, kind, systemRole, skipped = false, title, hint, children }: {
  collapsed: boolean; kind: "flight" | "hotel" | "meal"; title: string; hint: string; children: ReactNode;
  systemRole?: TripItem["system_role"]; skipped?: boolean;
}) {
  const t = useTranslations("trips.systemStop");
  const editor = useTranslations("trips.editor");
  if (!collapsed) return children;
  const Icon = kind === "flight" ? Plane : kind === "hotel" ? Hotel : UtensilsCrossed;
  const tone = getStopTone(systemRole);
  const roleLabel = tone === "lunch" || tone === "dinner"
    ? editor(`slot.${tone}`)
    : tone === "hotel" ? t(systemRole === "hotel_start" ? "hotelStart" : "hotelEnd") : undefined;
  return <details className={`premium-optional-stop ${stopToneClassName(systemRole, "summary", skipped)}`}
    data-stop-tone={tone} data-stop-skipped={skipped || undefined}><summary>
    <Icon size={19} aria-hidden="true" /><span>
      {roleLabel && <span className={stopToneClassName(systemRole, "badge", skipped)}>{roleLabel}</span>}
      <strong>{title}</strong><small>{hint}</small>
    </span><ChevronDown size={16} aria-hidden="true" />
  </summary><div className="premium-optional-stop-body">{children}</div></details>;
}
