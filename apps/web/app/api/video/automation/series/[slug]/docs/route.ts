import { NextRequest } from "next/server";
import { forwardToSpeech } from "../../../../speech/forward";
import { isRefusal, seriesPath } from "../../guard";

// A document the worker planned (the setting book, the outline, a chapter's outline), filed as
// a new version that waits for the owner (docs/videos/SERIES.md). A whole-series outline with
// a hundred episodes is far larger than a narration request, so the body cap is its own.
type Context = { params: Promise<{ slug: string }> };
const DOC_MAX_BODY_BYTES = 1024 * 1024;

export async function POST(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  const path = seriesPath(slug);
  if (isRefusal(path)) return path;
  return forwardToSpeech(request, `${path}/docs`, "POST", DOC_MAX_BODY_BYTES);
}
