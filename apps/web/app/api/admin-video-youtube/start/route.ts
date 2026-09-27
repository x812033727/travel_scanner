import { randomBytes } from "node:crypto";
import { NextRequest, NextResponse } from "next/server";
import { normalizeLocale } from "@/i18n/routing";
import { adminHeaders, apiUrl, backToSettings, COOKIE_PATH, encodeFlow, FLOW_COOKIE, secureCookies } from "../_shared";

// Google's consent screen is the only place this route sends a browser.
const GOOGLE_AUTHORIZE = "https://accounts.google.com/o/oauth2/v2/auth?";

/** The link button on the YouTube card: open a flow with the API, then go to Google. */
export async function GET(request: NextRequest) {
  const locale = normalizeLocale(request.nextUrl.searchParams.get("locale"));
  if (!request.cookies.get("travel_access")?.value) return backToSettings(locale, { error: "authentication_required" });
  const binding = randomBytes(32).toString("base64url");
  let upstream: Response;
  try {
    upstream = await fetch(apiUrl("admin/video-youtube/oauth/start"), {
      method: "POST",
      headers: adminHeaders(request),
      body: JSON.stringify({ browser_binding: binding }),
      cache: "no-store",
      signal: AbortSignal.timeout(10_000),
    });
  } catch {
    return backToSettings(locale, { error: "video_youtube_unavailable" });
  }
  const payload = await upstream.json().catch(() => ({})) as { authorization_url?: string; flow_id?: string; state?: string; expires_in?: number; code?: string };
  if (!upstream.ok || !payload.flow_id || !payload.state || !payload.authorization_url?.startsWith(GOOGLE_AUTHORIZE)) {
    return backToSettings(locale, { error: payload.code || "video_youtube_unavailable" });
  }
  const response = NextResponse.redirect(payload.authorization_url);
  response.cookies.set(FLOW_COOKIE, encodeFlow({ flowId: payload.flow_id, state: payload.state, binding, locale }), {
    httpOnly: true,
    secure: secureCookies(request),
    // Google comes back with a top-level GET, which carries a Lax cookie.
    sameSite: "lax",
    path: COOKIE_PATH,
    maxAge: Math.min(payload.expires_in || 600, 900),
  });
  return response;
}
