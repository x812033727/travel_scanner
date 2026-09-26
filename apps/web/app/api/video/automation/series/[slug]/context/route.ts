import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../speech/forward";
import { isRefusal, seriesPath } from "../../guard";

// What a series' prompts need: the approved documents, the episodes so far and the recaps
// (docs/videos/SERIES.md). `episode` narrows it to one episode's chapter.
type Context = { params: Promise<{ slug: string }> };
const EPISODE = /^[1-9][0-9]{0,3}$/;

export async function GET(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  const path = seriesPath(slug);
  if (isRefusal(path)) return path;
  const episode = request.nextUrl.searchParams.get("episode");
  const query = episode && EPISODE.test(episode) ? `?episode=${episode}` : "";
  return forwardToSpeech(request, `${path}/context${query}`, "GET");
}
