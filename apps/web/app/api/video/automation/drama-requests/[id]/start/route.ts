import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";

// The video worker claims a queued drama request for the video it is about to make; the body
// names the video's slug (docs/videos/DRAMA.md). The id is checked here so a stray path never
// reaches the API.
type Context = { params: Promise<{ id: string }> };
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function POST(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!UUID.test(id)) return problem(404, "video_drama_request_not_found", "找不到這個漫劇請求");
  return forwardToSpeech(request, `automation/drama-requests/${id.toLowerCase()}/start`, "POST");
}
