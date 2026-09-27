import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../../speech/forward";
import { isRefusal, seriesPath } from "../../../guard";

// The worker starts the compilation of a finished binge series under the video's slug
// (docs/videos/BINGE.md); the API files the slug and answers with the episodes to join.
type Context = { params: Promise<{ slug: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  const path = seriesPath(slug);
  if (isRefusal(path)) return path;
  return forwardToSpeech(request, `${path}/compilation/start`, "POST");
}
