import { NextRequest, NextResponse } from "next/server";
import { forwardedClientHeaders } from "@/lib/client-address";
import { limitedRequestBody } from "@/lib/request-body";
import { problem } from "../speech/forward";

/**
 * How the local video pipeline (tools/video) gets a token without anyone copying one: it opens a
 * pairing here, the owner allows it on the admin card, and a poll here collects the token.
 *
 * Neither call carries a credential, so nothing is forwarded but the JSON body and the caller's
 * address (the API rate-limits pairings per address and shows it to the owner). Cookies are
 * never forwarded: a browser session must not be able to answer its own pairing.
 */
const MAX_BODY_BYTES = 4 * 1024;
const TIMEOUT_MS = 15_000;
const PASSED_BACK = ["content-type", "retry-after"];

export async function forwardPairing(request: NextRequest, path: "pairings" | "pairings/poll") {
  let body: ArrayBuffer;
  try {
    body = (await limitedRequestBody(request, MAX_BODY_BYTES)) ?? new ArrayBuffer(0);
  } catch {
    // Details here are read by the local tool, not shown in the UI, so they stay out of the catalog.
    return problem(413, "video_pairing_request_too_long", "request body too large");
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    const upstream = await fetch(`${base}/api/v1/video/${path}`, {
      method: "POST",
      headers: {
        Accept: "application/json",
        "Accept-Language": request.headers.get("accept-language") || "zh-TW",
        "Content-Type": "application/json",
        ...forwardedClientHeaders(request.headers),
      },
      body,
      cache: "no-store",
      signal: controller.signal,
    });
    // The poll that collects a token carries it in this body, so nothing may cache it.
    const headers = new Headers({ "Cache-Control": "no-store" });
    for (const name of PASSED_BACK) {
      const value = upstream.headers.get(name);
      if (value) headers.set(name, value);
    }
    return new NextResponse(await upstream.arrayBuffer(), { status: upstream.status, headers });
  } catch {
    return problem(502, "upstream_unavailable", "the API is not responding");
  } finally {
    clearTimeout(timeout);
  }
}
