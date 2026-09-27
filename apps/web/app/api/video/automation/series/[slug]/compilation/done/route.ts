import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../../speech/forward";
import { isRefusal, seriesPath } from "../../../guard";

// The worker reports the compilation cleared for upload; the 1080p cut stays on its volume
// and the owner downloads it from the series page (docs/videos/BINGE.md).
type Context = { params: Promise<{ slug: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  const path = seriesPath(slug);
  if (isRefusal(path)) return path;
  return forwardToSpeech(request, `${path}/compilation/done`, "POST");
}
