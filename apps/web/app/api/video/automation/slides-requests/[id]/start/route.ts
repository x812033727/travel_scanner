import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";

// The video worker claims a queued slides request for the video it has just planned from the
// article; the body names the video's slug (docs/videos/AUTOMATION.md). The id is checked here so a
// stray path never reaches the API.
type Context = { params: Promise<{ id: string }> };
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function POST(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!UUID.test(id)) return problem(404, "video_slides_request_not_found", "no such slides request");
  return forwardToSpeech(request, `automation/slides-requests/${id.toLowerCase()}/start`, "POST");
}
