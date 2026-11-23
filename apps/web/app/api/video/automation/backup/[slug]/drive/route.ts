import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";

// The video worker reports the Drive ids of one backed-up video's folder and final cut, so the
// admin can link them (tools/video/automation/backup.mjs linkDriveIds). The slug is checked here
// with the API's own pattern so a stray path never reaches the API.
type Context = { params: Promise<{ slug: string }> };
const SLUG = /^[a-z0-9](?:[a-z0-9-]{0,78}[a-z0-9])?$/;

export async function POST(request: NextRequest, context: Context) {
  const { slug } = await context.params;
  if (!SLUG.test(slug)) return problem(404, "video_backup_video_not_found", "找不到這支影片");
  return forwardToSpeech(request, `automation/backup/${slug}/drive`, "POST");
}
