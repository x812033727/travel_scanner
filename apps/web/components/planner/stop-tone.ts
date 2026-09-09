import type { TripItem } from "@/lib/trip-types";
import styles from "./stop-tone.module.css";

export type StopTone = "hotel" | "lunch" | "dinner";
export type StopToneVariant = "card" | "summary" | "entry" | "marker" | "badge";

/** A stop's purpose is authoritative; names and times never infer a meal type. */
export function getStopTone(systemRole: TripItem["system_role"]): StopTone | undefined {
  if (systemRole === "hotel_start" || systemRole === "hotel_end") return "hotel";
  if (systemRole === "lunch" || systemRole === "dinner") return systemRole;
  return undefined;
}

export function stopToneClassName(
  systemRole: TripItem["system_role"],
  variant: StopToneVariant = "card",
  skipped = false,
): string {
  const tone = getStopTone(systemRole);
  return tone ? [styles.tone, styles[tone], styles[variant], skipped ? styles.skipped : ""].filter(Boolean).join(" ") : "";
}

export { styles as stopToneStyles };
