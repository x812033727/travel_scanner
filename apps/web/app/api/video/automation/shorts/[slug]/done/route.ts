import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../speech/forward";
import { isRefusal, shortPath, SMALL_MAX_BODY_BYTES } from "../../guard";

// The worker reports a Short finished: pushed, checked and in the owner's hands or the
// library's (docs/videos/SHORTS.md).
type Context = { params: Promise<{ slug: string }> };

export async function POST(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  const path = shortPath(slug);
  if (isRefusal(path)) return path;
  return forwardToSpeech(request, `${path}/done`, "POST", SMALL_MAX_BODY_BYTES);
}
