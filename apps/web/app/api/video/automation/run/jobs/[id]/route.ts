import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";

export async function GET(request: NextRequest, context: { params: Promise<{ id: string }> }) {
  const { id } = await context.params;
  const hash = request.nextUrl.searchParams.get("input_hash") ?? "";
  if (!/^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i.test(id) || !/^[0-9a-f]{64}$/.test(hash)) {
    return problem(400, "video_ai_receipt_invalid", "工作編號或來源雜湊格式不正確");
  }
  return forwardToSpeech(request, `automation/run/jobs/${id}?input_hash=${hash}`, "GET", undefined, 30_000);
}
