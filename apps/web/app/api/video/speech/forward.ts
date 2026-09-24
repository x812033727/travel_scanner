import { NextRequest, NextResponse } from "next/server";
import { limitedRequestBody } from "@/lib/request-body";

/**
 * The local video pipeline (tools/video) reaches the narration endpoint through here: nginx
 * exposes only this web app, and the generic `/api/travel` proxy neither forwards
 * `Authorization` nor returns bytes intact, so audio would come back corrupted.
 *
 * Only a video tool token is forwarded, never cookies, so a browser session cannot be used to
 * spend the speech budget from this route.
 */
const MAX_BODY_BYTES = 256 * 1024;
// A narrated line sent back for transcription is a small WAV in base64: far above a text
// request, still under the API's own 5 MiB cap and nginx's 6 MB.
export const TRANSCRIBE_MAX_BODY_BYTES = 3 * 1024 * 1024;
// Synthesizing a long scene takes Azure tens of seconds; nginx allows 300 s for /api/.
const TIMEOUT_MS = Number(process.env.VIDEO_SPEECH_PROXY_TIMEOUT_MS || 180_000);
const TOKEN = /^Bearer mkv_[A-Za-z0-9_-]{36,76}$/;
const PASSED_BACK = ["content-type", "x-billable-characters", "retry-after", "www-authenticate"];

export function problem(status: number, code: string, detail: string) {
  return NextResponse.json(
    { title: "請求未完成", status, code, detail },
    { status, headers: { "Cache-Control": "no-store" } },
  );
}

export async function forwardToSpeech(request: NextRequest, path: string, method: "GET" | "POST", maxBodyBytes = MAX_BODY_BYTES) {
  const authorization = request.headers.get("authorization") ?? "";
  if (!TOKEN.test(authorization)) {
    return problem(401, "video_tool_token_invalid", "缺少或格式不對的影片工具權杖");
  }
  let body: ArrayBuffer | undefined;
  if (method === "POST") {
    try {
      body = (await limitedRequestBody(request, maxBodyBytes)) ?? new ArrayBuffer(0);
    } catch {
      return problem(413, "video_speech_request_too_long", "一次送出的內容太大，請分段");
    }
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    const upstream = await fetch(`${base}/api/v1/video/${path}`, {
      method,
      headers: {
        Authorization: authorization,
        Accept: request.headers.get("accept") || "*/*",
        "Accept-Language": request.headers.get("accept-language") || "zh-TW",
        ...(body ? { "Content-Type": "application/json" } : {}),
      },
      body,
      cache: "no-store",
      signal: controller.signal,
    });
    const headers = new Headers({ "Cache-Control": "no-store" });
    for (const name of PASSED_BACK) {
      const value = upstream.headers.get(name);
      if (value) headers.set(name, value);
    }
    return new NextResponse(await upstream.arrayBuffer(), { status: upstream.status, headers });
  } catch {
    return problem(502, "upstream_unavailable", "API 服務目前無法回應");
  } finally {
    clearTimeout(timeout);
  }
}
