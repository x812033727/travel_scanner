import { NextRequest, NextResponse } from "next/server";
import { normalizeLocale, type Locale } from "@/i18n/routing";
import { forwardedClientHeaders } from "@/lib/client-address";
import { siteUrl } from "@/lib/seo";

/**
 * The browser half of linking the site's YouTube channel (docs/videos/HANDS-OFF.md, the YouTube
 * API section). /start asks the API to open a flow and sends the owner to Google's consent
 * screen; Google sends them back to /callback, which hands the code to the API. The API keeps
 * the grant; the browser only ever holds this flow cookie, scoped to these two routes.
 */
export const FLOW_COOKIE = "travel_video_youtube";
export const COOKIE_PATH = "/api/admin-video-youtube";
const CODE = /^[a-z][a-z0-9_]{0,63}$/;

export type Flow = { flowId: string; state: string; binding: string; locale: Locale };

export function encodeFlow(flow: Flow): string {
  return Buffer.from(JSON.stringify(flow)).toString("base64url");
}

export function decodeFlow(value: string | undefined): Flow | null {
  if (!value) return null;
  try {
    const parsed = JSON.parse(Buffer.from(value, "base64url").toString("utf8")) as Partial<Flow>;
    if (!parsed.flowId || !parsed.state || !parsed.binding) return null;
    return { flowId: parsed.flowId, state: parsed.state, binding: parsed.binding, locale: normalizeLocale(parsed.locale) };
  } catch {
    return null;
  }
}

export function apiUrl(path: string): string {
  const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
  return `${base}/api/v1/${path}`;
}

/** The admin's session and step-up cookies, as the API reads them, plus the client address. */
export function adminHeaders(request: NextRequest): Headers {
  const headers = new Headers({ "Content-Type": "application/json" });
  const session = request.cookies.get("travel_access")?.value;
  const stepUp = request.cookies.get("admin_step_up")?.value;
  const cookie = [session && `travel_access=${session}`, stepUp && `admin_step_up=${stepUp}`].filter(Boolean).join("; ");
  if (cookie) headers.set("Cookie", cookie);
  for (const [name, value] of Object.entries(forwardedClientHeaders(request.headers))) headers.set(name, value);
  return headers;
}

/**
 * Back to the settings tab of /admin/videos, with the outcome for the YouTube card to read.
 * Built on the public site URL: behind the reverse proxy the request's own origin is the
 * container's bind address, which no browser can open.
 */
export function backToSettings(locale: Locale, outcome: { linked: true } | { error: string }): NextResponse {
  const url = new URL(`/${locale}/admin/videos`, `${siteUrl}/`);
  url.searchParams.set("tab", "settings");
  if ("linked" in outcome) url.searchParams.set("youtube", "linked");
  else url.searchParams.set("youtube_error", CODE.test(outcome.error) ? outcome.error : "video_youtube_unavailable");
  const response = NextResponse.redirect(url);
  response.cookies.delete({ name: FLOW_COOKIE, path: COOKIE_PATH });
  return response;
}

export function secureCookies(request: NextRequest): boolean {
  return process.env.NODE_ENV === "production" || request.nextUrl.protocol === "https:";
}
