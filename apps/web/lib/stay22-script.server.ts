import { cache } from "react";
import { headers } from "next/headers";
import { CITIES } from "@/components/travel-services/options";
import { disabledStay22Script, isStay22ScriptOrigin, validStay22ScriptConfig, type Stay22ScriptConfig } from "./stay22-script";

/** Public only: never forward cookies, authorization, query strings, or account state. */
export async function loadStay22ScriptConfig(): Promise<Stay22ScriptConfig> {
  const incoming = await headers();
  if (!isStay22ScriptOrigin(`https://${incoming.get("host") || ""}`)) return disabledStay22Script;
  if (incoming.get("dnt") === "1" || incoming.get("sec-gpc") === "1") return disabledStay22Script;
  // proxy.ts overwrites this header from NextRequest's actual URL. An explicit
  // non-hotel view must retain the full original catalogue, not become hotels.
  const path = incoming.get("x-travel-pathname") || "";
  const destination = path.split("?")[0].match(/^\/(?:en|ja|ko|zh-TW|zh-CN)\/destinations\/([^/]+)\/services\/?$/)?.[1];
  if (!destination || !(CITIES as readonly string[]).includes(destination) && destination !== "osaka-kyoto") return disabledStay22Script;
  const query = new URLSearchParams(path.includes("?") ? path.slice(path.indexOf("?") + 1) : "");
  const kinds = query.getAll("type");
  if (kinds.some((kind) => kind !== "hotel")) return disabledStay22Script;
  const base = (process.env.API_INTERNAL_URL || "http://localhost:8000").replace(/\/$/, "");
  try {
    const response = await fetch(`${base}/api/v1/travel-services/stay22-script-config`, {
      headers: { Accept: "application/json" },
      cache: "no-store",
      signal: AbortSignal.timeout(3_000),
    });
    if (!response.ok) return disabledStay22Script;
    const config: unknown = await response.json();
    return validStay22ScriptConfig(config) ? config : disabledStay22Script;
  } catch { return disabledStay22Script; }
}

// The public layout and its page must make the same decision within one request.
export const getStay22ScriptConfig = cache(loadStay22ScriptConfig);
