import { NextRequest } from "next/server";
import { normalizeLocale } from "@/i18n/routing";
import { adminHeaders, apiUrl, backToSettings, decodeFlow, FLOW_COOKIE } from "../_shared";

/**
 * Where Google sends the owner back: the redirect URI the owner registers with their OAuth client
 * (shown on the YouTube card). The code goes to the API with the flow this browser started; the
 * owner lands on the settings tab either way, with the outcome in the address.
 */
export async function GET(request: NextRequest) {
  const flow = decodeFlow(request.cookies.get(FLOW_COOKIE)?.value);
  const locale = flow?.locale ?? normalizeLocale(request.cookies.get("travel_locale")?.value);
  const params = request.nextUrl.searchParams;
  // access_denied: the owner pressed Cancel on Google's screen.
  if (params.get("error")) return backToSettings(locale, { error: "video_youtube_cancelled" });
  const code = params.get("code");
  const state = params.get("state");
  if (!flow || !code || !state || state !== flow.state) return backToSettings(locale, { error: "video_youtube_state_invalid" });
  let upstream: Response;
  try {
    upstream = await fetch(apiUrl("admin/video-youtube/oauth/exchange"), {
      method: "POST",
      headers: adminHeaders(request),
      body: JSON.stringify({ flow_id: flow.flowId, state, code, browser_binding: flow.binding }),
      cache: "no-store",
      signal: AbortSignal.timeout(20_000),
    });
  } catch {
    return backToSettings(locale, { error: "video_youtube_unavailable" });
  }
  if (upstream.ok) {
    await upstream.body?.cancel();
    return backToSettings(locale, { linked: true });
  }
  const payload = await upstream.json().catch(() => ({})) as { code?: string };
  return backToSettings(locale, { error: payload.code || "video_youtube_unavailable" });
}
