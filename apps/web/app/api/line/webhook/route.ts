import { NextRequest, NextResponse } from "next/server";
import { limitedRequestBody } from "@/lib/request-body";

const MAX_BODY_BYTES = Number(process.env.LINE_WEBHOOK_MAX_BODY_BYTES || 1024 * 1024);
const TIMEOUT_MS = Number(process.env.API_PROXY_TIMEOUT_MS || 15_000);

function problem(status: number, code: string, detail: string) {
  return NextResponse.json(
    { title: "請求未完成", status, code, detail },
    { status, headers: { "Cache-Control": "no-store" } },
  );
}

export async function POST(request: NextRequest) {
  const signature = request.headers.get("x-line-signature");
  if (!signature) return problem(401, "line_signature_missing", "缺少 LINE webhook 簽章");
  let body: ArrayBuffer;
  try {
    // This endpoint is unauthenticated and internet-facing: the body is counted as it streams so
    // the limit applies before anything is buffered in full.
    body = (await limitedRequestBody(request, MAX_BODY_BYTES)) ?? new ArrayBuffer(0);
  } catch {
    return problem(413, "line_webhook_too_large", "LINE webhook 內容過大");
  }
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), TIMEOUT_MS);
  try {
    const base = process.env.API_INTERNAL_URL || "http://localhost:8000";
    const upstream = await fetch(`${base}/api/v1/line/webhook`, {
      method: "POST",
      headers: {
        "Content-Type": request.headers.get("content-type") || "application/json",
        "X-Line-Signature": signature,
      },
      body,
      cache: "no-store",
      signal: controller.signal,
    });
    return new NextResponse(await upstream.arrayBuffer(), {
      status: upstream.status,
      headers: {
        "Content-Type": upstream.headers.get("content-type") || "application/json",
        "Cache-Control": "no-store",
      },
    });
  } catch {
    return problem(502, "upstream_unavailable", "API 服務目前無法回應");
  } finally {
    clearTimeout(timeout);
  }
}
