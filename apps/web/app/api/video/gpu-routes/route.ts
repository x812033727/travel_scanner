import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../speech/forward";

// Before a batch, a runner asks which GPU route its token may use (Colab, RunPod) and which one
// the site recommends for this canvas. Only the two known query values are passed on.
export async function GET(request: NextRequest) {
  const query = request.nextUrl.searchParams;
  const canvas = query.get("canvas") ?? "736p";
  const upscale = query.get("upscale") ?? "false";
  if (!["736p", "1088p"].includes(canvas) || !["true", "false"].includes(upscale)) {
    return problem(422, "video_gpu_routes_invalid", "canvas 只能是 736p 或 1088p，upscale 只能是 true 或 false");
  }
  return forwardToSpeech(request, `gpu-routes?canvas=${canvas}&upscale=${upscale}`, "GET");
}
