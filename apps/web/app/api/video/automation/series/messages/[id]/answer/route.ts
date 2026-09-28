import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../../speech/forward";

// The model's answer to one of the owner's lines: a reply, and the revised document when the
// owner asked for a change (docs/videos/DRAMA-FLOW.md, section 3). A revised outline with a
// hundred episodes is far larger than a narration request, so the body cap is its own. The id
// is checked here so a stray path never reaches the API.
type Context = { params: Promise<{ id: string }> };
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
const ANSWER_MAX_BODY_BYTES = 1024 * 1024;

export async function POST(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!UUID.test(id)) return problem(404, "video_drama_message_not_found", "no such message");
  return forwardToSpeech(request, `automation/series/messages/${id.toLowerCase()}/answer`, "POST", ANSWER_MAX_BODY_BYTES);
}
