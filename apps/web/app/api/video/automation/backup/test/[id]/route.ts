import { NextRequest } from "next/server";
import { forwardToSpeech, problem } from "../../../../speech/forward";

// The video worker answers the owner's backup test: it wrote and deleted a probe file in Drive,
// and how much space is left (docs/videos/BACKUP.md). The id is checked here so a stray path
// never reaches the API.
type Context = { params: Promise<{ id: string }> };
const UUID = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export async function POST(request: NextRequest, context: Context) {
  const { id } = await context.params;
  if (!UUID.test(id)) return problem(404, "video_backup_test_not_found", "沒有這個待回覆的備份測試");
  return forwardToSpeech(request, `automation/backup/test/${id.toLowerCase()}`, "POST");
}
