import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../../../speech/forward";
import { isRefusal, seriesPath } from "../../../../guard";

// The worker reports an episode cleared for upload: the next one may start
// (docs/videos/SERIES.md).
type Context = { params: Promise<{ slug: string; number: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { slug, number } = await context.params;
  const path = seriesPath(slug, number);
  if (isRefusal(path)) return path;
  return forwardToSpeech(request, `${path}/done`, "POST");
}
