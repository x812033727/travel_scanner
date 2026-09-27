import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../../../speech/forward";
import { isRefusal, seriesPath } from "../../../../guard";

// The worker starts an episode under the video's slug (docs/videos/SERIES.md); the API files
// the request row and answers with the episode's context.
type Context = { params: Promise<{ slug: string; number: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { slug, number } = await context.params;
  const path = seriesPath(slug, number);
  if (isRefusal(path)) return path;
  return forwardToSpeech(request, `${path}/start`, "POST");
}
