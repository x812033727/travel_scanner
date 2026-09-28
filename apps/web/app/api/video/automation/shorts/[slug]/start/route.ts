import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../speech/forward";
import { isRefusal, shortPath, SMALL_MAX_BODY_BYTES } from "../../guard";

// The worker starts making a Short under its slug (docs/videos/SHORTS.md): the API marks the
// topic as in the making and answers with what the Short is made from.
type Context = { params: Promise<{ slug: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  const path = shortPath(slug);
  if (isRefusal(path)) return path;
  return forwardToSpeech(request, `${path}/start`, "POST", SMALL_MAX_BODY_BYTES);
}
