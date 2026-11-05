import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";

// The video worker reports a day's brief confirmed for upload. The id is checked here so a stray
// path never reaches the API.
type Context = { params: Promise<{ id: string }> };
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function POST(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!UUID.test(id)) return problem(404, "video_daily_brief_not_found", "no such daily brief");
  return forwardToSpeech(request, `automation/daily-briefs/${id.toLowerCase()}/done`, "POST");
}
